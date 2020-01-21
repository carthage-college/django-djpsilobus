# -*- coding: utf-8 -*-

"""Views for all operations."""

import datetime
import os
import tarfile
from collections import OrderedDict

import magic
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djimix.decorators.auth import portal_auth_required
from djimix.people.departments import academic_department
from djimix.people.departments import chair_departments
from djimix.people.departments import department_faculty
from djimix.sql.departments import ACADEMIC_DEPARTMENTS
from djpsilobus.core.data import DEPARTMENT_EXCEPTIONS
from djpsilobus.core.dspace import Manager
from djpsilobus.core.dspace import Search
from djpsilobus.core.utils import create_item
from djpsilobus.core.utils import division_departments
from djpsilobus.core.utils import sections
from djpsilobus.core.utils import sheet
from djpsilobus.core.utils import syllabus_name
from djtools.fields.helpers import handle_uploaded_file
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook


TODAY = settings.TODAY
# alternative title meta tag for searching for files
TITLE_ALT = settings.DSPACE_TITLE_ALT

"""
Key for Term codes.
AA  Fall I  UNDG
AB  Fall II     UNDG
AG  Winter  UNDG
AK  Spring I    UNDG
AM  Spring II   UNDG
AS  Summer I    UNDG
AT  Summer II   UNDG

GA  Fall Graduate   GRAD
GB  Winter Graduate     GRAD
GC  Spring Graduate     GRAD
GE  Summer Graduate     GRAD

RA  Fall    UNDG
RB  J-Term  UNDG
RC  Spring  UNDG
RE  Summer  UNDG
"""


def get_session_term():
    """Obtain the session and term based on date."""
    now = datetime.datetime.now()
    if now.month >= 1 and now.month <= 5:
        sess = settings.SPRING_TERMS
        term = 'spring'
    elif now.month >= 6 and now.month <= 8:
        sess = settings.SUMMER_TERMS
        term = 'summer'
    else:
        sess = settings.FALL_TERMS
        term = 'fall'

    return {'term': term, 'sess': sess}


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied'),
)
def home(request, dept=None, term=None, year=None):
    """Home page view after auth."""
    # change year/sess
    if not year:
        year = TODAY.year
    if request.GET.get('year'):
        year = request.GET.get('year')
    if not term:
        term = request.GET.get('term')
    if term == 'spring':
        session = settings.SPRING_TERMS
    elif term == 'fall':
        session = settings.FALL_TERMS
    elif term == 'summer':
        session = settings.SUMMER_TERMS
    else:
        session = get_session_term()['sess']
    if not term:
        term = get_session_term()['term']
    # current user
    user = request.user
    uid = user.id
    # administrative users
    admin = False
    # division dean or department chair
    dean_chair = None
    # UI display for division deans
    division_name = None
    # code for path for downloads
    division_code = None
    # faculty ID, name, courses
    fid = None
    pfid = None  # post faculty ID
    faculty_name = None
    courses = None
    # fetch our departments
    if uid in settings.ADMINISTRATORS:
        admin = True

        sql = '{0} ORDER BY dept_table.txt'.format(ACADEMIC_DEPARTMENTS)
        connection = get_connection()
        with connection:
            rows = xsql(sql, connection).fetchall()

        depts = OrderedDict()
        for row in rows:
            depts[row.dept_code] = {
                'dept_name': row.dept_name,
                'dept_code': row.dept_code,
                'div_name': row.div_name,
                'div_code': row.div_code,
            }
        depts = {'depts': depts}
    else:
        depts, dean_chair, division_name, division_code = chair_departments(uid)
    dept_list = []
    if admin or depts.get('depts'):
        for dcode, deptartment in depts['depts'].items():
            faculty = department_faculty(dcode, year)
            dept_list.append({
                'dept_name': deptartment['dept_name'],
                'dept_code': deptartment['dept_code'],
                'div_name': deptartment['div_name'],
                'div_code': deptartment['div_code'],
                'faculty': faculty,
            })

    # obtain the courses for department or faculty
    if dept:
        # all faculty courses for department
        courses = sections(code=dept, year=year, sess=session)
        dept = academic_department(dept)
        if dept:
            dept = dept[0]
    elif request.method == 'POST' and not request.FILES:
        substr = 'dept_faculty'
        for key, post_value in request.POST.items():
            if substr in key and post_value:
                pfid = int(post_value)
        if pfid:
            fid = pfid

    # this could be a faculty who is deptartment chair but has
    # courses in other department e.g. renaud
    if not fid and not courses:
        fid = uid
    # faculty courses
    if not courses:
        courses = sections(year=year, sess=session, fid=fid)
        if courses:
            faculty_name = courses[0][settings.FACULTY_FULLNAME_LIST_INDEX]

    secciones = []
    if courses:
        for course in courses:
            phile = syllabus_name(course)
            secciones.append({'obj': course, 'phile': phile})

    # file upload
    phile = None
    if request.method == 'POST' and request.FILES:
        # complete path to directory in which we will store the file
        syllabi = request.FILES.getlist('syllabi[]')
        # POST does not include empty file fields in [] so we use this
        # hidden field and javascript event to track
        syllabih = request.POST.getlist('syllabih[]')
        hidden = len(syllabi)
        for i in range(0, len(syllabih)):
            if syllabih[i] == 'True':
                yr = request.POST.getlist('year[]')[i]
                sess = request.POST.getlist('sess[]')[i]
                crs_no = request.POST.getlist('crs_no[]')[i]
                code = crs_no.split(' ')[0]
                # chapuza for now until we can figure out what to do
                # with department codes that do not translate to actual
                # departments
                if DEPARTMENT_EXCEPTIONS.get(code):
                    code = DEPARTMENT_EXCEPTIONS.get(code)
                dept = academic_department(code)
                sendero = os.path.join(
                    settings.UPLOADS_DIR, yr, sess, dept.div_code,
                    dept.dept_code,
                )
                # for display at UI level
                dept = None
                syllabus = syllabi[len(syllabi) - hidden]
                # must be after the above
                hidden -= 1
                crs_title = request.POST.getlist('crs_title[]')[i]
                filename = request.POST.getlist('phile[]')[i]
                fullname = request.POST.getlist('fullname[]')[i]
                # create our DSpace manager
                manager = Manager()
                # remove existing file if it exists so we can replace it
                # with the current upload
                search = Search()
                jason = search.file('{0}.pdf'.format(filename), TITLE_ALT)
                if jason and jason[0].get('id'):
                    uri = 'items/{0}/'.format(jason[0].get('id'))
                    response = manager.request(
                        uri, 'delete',
                    )
                phile = handle_uploaded_file(
                    syllabus, sendero, filename,
                )
                if phile:
                    upload = '{0}/{1}'.format(sendero, phile)
                    # verify file type is PDF
                    mime = magic.from_file(upload, mime=True)
                    mime_types = ('application/pdf', 'application/octet-stream')
                    if mime in mime_types:
                        # create a new parent item that will contain
                        # the uploaded file
                        item = {
                            'course_number': crs_no,
                            'title': crs_title,
                            'title_alt': phile,
                            'year': yr,
                            'term': sess,
                            'fullname': fullname,
                        }
                        new_item = create_item(item)
                        # send file to DSpace
                        uri = 'items/{0}/bitstreams/'.format(new_item['uuid'])
                        response = manager.request(
                            uri, 'post', phile, phile=upload,
                        )
                        messages.add_message(
                            request, messages.SUCCESS,
                            'The file was uploaded successfully.',
                            extra_tags='success',
                        )
                    else:
                        messages.add_message(
                            request, messages.ERROR,
                            '''
                                Files must be in PDF format. Please convert
                                your file to PDF and try again.
                            ''', extra_tags='danger',
                        )
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        """
                            Something has gone awry with the upload.
                            Please try again.
                        """, extra_tags='danger',
                    )

    # years for form switcher
    years = []
    for yeer in reversed(range(settings.BEGIN_YEAR, TODAY.year + 2)):
        years.append((yeer, yeer))

    return render(
        request, 'home.html', {
            'depts': dept_list,
            'courses': secciones,
            'department': dept,
            'faculty_name': faculty_name,
            'fid': fid,
            'year': year,
            'years': years,
            'term': term,
            'phile': phile,
            'dean_chair': dean_chair,
            'division': {'name': division_name, 'code': division_code},
            'admin': admin,
        },
    )


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied')
)
@csrf_exempt
def dspace_file_search(request):
    if request.method == 'POST':
        phile = request.POST.get('phile')
        name = request.POST.get('name')

        jason = []
        if name.strip() != 'Staff':
            search = Search()
            jason = search.file(phile, TITLE_ALT)
        if jason and jason[0].get('name'):
            earl = '{0}/bitstream/handle/{1}/{2}?sequence=1&isAllowed=y'.format(
                settings.DSPACE_URL, jason[0].get('handle'), phile,
            )
            response = render(
                request, 'view_file.ajax.html', {
                    'earl': earl, 'handle': jason[0].get('handle'),
                },
            )
        else:
            response = HttpResponse(
                '', content_type='text/plain; charset=utf-8',
            )
    else:
        response = HttpResponseRedirect(reverse_lazy('access_denied'))

    return response


@csrf_exempt
def dspace_dept_courses(request, dept, term, year):
    cache_key = 'DSPACE_API_{0}_{1}_{2}'.format(dept, term, year)
    if term == 'RC':
        term = settings.SPRING_TERMS
    elif term == 'RA':
        term = settings.FALL_TERMS
    else:
        raise Http404
    jay = cache.get(cache_key)
    if not jay:
        courses = sections(code=dept, year=year, sess=term)
        jay = '['
        if courses:
            for c in courses:
                if c[12] == 'Y':
                    phile = '{}.pdf'.format(syllabus_name(c))
                    search = Search()
                    jason = search.file(phile, TITLE_ALT)
                    earl = ''
                    if jason and jason[0].get('name'):
                        earl = '{0}/bitstream/handle/{1}/{2}?sequence=1&isAllowed=y'.format(
                            settings.DSPACE_URL, jason[0].get('handle'), phile,
                        )
                    jay += '{'
                    # json requires doubl quotes
                    jay += """
                        "crs_no":"{}","earl":"{}","sess":"{}","sec_no":"{}",
                        "crs_title":"{}","fullname":"{}","need_syllabi":"{}"
                    """.format(
                        c.crs_no, earl, c.sess, c.sec_no,
                        c.crs_title, c.fullname, c[12],
                    )
                    jay += '},'
            jay = jay[:-1] + ']'
        else:
            jay = jay + ']'
        cache.set(cache_key, jay, None)
    return HttpResponse(
        jay, content_type='text/plain; charset=utf-8',
    )


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied'),
)
def download(request, division, department=None, term=None, year=None):
    response = HttpResponse(content_type='application/x-gzip')
    name = '{}_{}_syllabi'.format(division, department)
    response['Content-Disposition'] = 'attachment; filename={}.tar.gz'.format(
        name
    )
    tar_ball = tarfile.open(fileobj=response, mode='w:gz')
    directory = False
    if not year:
        year= TODAY.year
    if not term:
        #TERM = get_session_term()
        TERM = get_session_term()['sess']
    else:
        if term == 'spring':
            TERM = settings.SPRING_TERMS
        elif term == 'summer':
            TERM = settings.SUMMER_TERMS
        elif term == 'fall':
            TERM = settings.FALL_TERMS
        else:
            #TERM = get_session_term()
            TERM = get_session_term()['sess']

    for sess in TERM:
        directory = '{}{}/{}/{}/{}'.format(
            settings.UPLOADS_DIR,year,sess,division,department
        )
        if os.path.isdir(directory):
            tar_ball.add(directory, arcname=name)
            directory = True
    tar_ball.close()
    if directory:
        return response
    else:
        messages.add_message(
            request, messages.ERROR,
            '''
                Currently, there are no course syllabi for
                that division or department
            ''',
            extra_tags='danger'
        )
        return HttpResponseRedirect(reverse_lazy('home'))


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied')
)
def openxml(request, division, department=None, term=None, year=None):

    wb = load_workbook('{}template.xlsx'.format(settings.MEDIA_ROOT))

    # obtain the active worksheet
    template = wb.active

    if not year:
        year= TODAY.year
    if not term:
        #TERM = get_session_term()
        TERM = get_session_term()['sess']
    else:
        if term == 'spring':
            TERM = settings.SPRING_TERMS
        elif term == 'summer':
            TERM = settings.SUMMER_TERMS
        elif term == 'fall':
            TERM = settings.FALL_TERMS
        else:
            #TERM = get_session_term()
            TERM = get_session_term()['sess']

    if department:
        courses = sections(code=department,year=YEAR,sess=TERM)
        if courses:
            sheet(template, division, department, courses)
        else:
            messages.add_message(
                request, messages.ERROR,
                '''
                    No courses found for that department.
                ''',
                extra_tags='danger'
            )
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        depts = division_departments(division)
        for d in depts:
            courses = sections(code=d.dept,year=YEAR,sess=TERM)
            if courses:
                ws = wb.copy_worksheet(template)
                ws.title = d.dept
                hoja = sheet(ws, division, d.dept, courses)
        # remove the template sheet
        wb.remove_sheet(template)

    # in memory response instead of save to file system
    response = HttpResponse(
        save_virtual_workbook(wb), content_type='application/ms-excel'
    )

    name = '{}_{}_syllabi'.format(division, department)
    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(
        name
    )

    return response
