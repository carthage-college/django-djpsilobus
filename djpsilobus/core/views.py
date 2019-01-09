from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from djpsilobus.core.data import DEPARTMENT_EXCEPTIONS
from djpsilobus.core.dspace import Manager, Search
from djpsilobus.core.utils import sheet, syllabus_name
from djpsilobus.core.utils import create_item

from djzbar.decorators.auth import portal_auth_required
from djzbar.utils.informix import do_sql as do_esql
from djzbar.utils.hr import chair_departments, academic_department
from djzbar.utils.hr import department_faculty
from djzbar.utils.academics import sections
from djzbar.utils.academics import division_departments
from djzbar.core.sql import ACADEMIC_DEPARTMENTS
from djzbar.constants import TERM_LIST

from djtools.fields.helpers import handle_uploaded_file

from os.path import join
from collections import OrderedDict
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

import re
import os
import datetime
import json
import magic
import tarfile

# alternative title meta tag for searching for files
TITLE_ALT = settings.DSPACE_TITLE_ALT
YEAR = settings.YEAR


def get_session_term():
    '''
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
    '''
    # constant for now
    return settings.SESS


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied')
)
def home(request, dept=None):
    SESS = get_session_term()
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
    pfid = None # post faculty ID
    faculty_name = None
    courses = None
    # fetch our departments
    if uid in settings.ADMINISTRATORS:
        admin = True

        sql = '{} ORDER BY dept_table.txt'.format(ACADEMIC_DEPARTMENTS)
        objs = do_esql(sql)
        depts = OrderedDict()
        for o in objs:
            depts[o.dept_code] = {
                'dept_name':o.dept_name, 'dept_code':o.dept_code,
                'div_name': o.div_name, 'div_code': o.div_code
            }
        depts = {'depts':depts}
    else:
        depts, dean_chair, division_name, division_code = chair_departments(uid)
    dept_list = []
    if admin or depts.get('depts'):
        for c,d in depts['depts'].iteritems():
            faculty = department_faculty(c, YEAR)
            dept_list.append({
                'dept_name':d['dept_name'],
                'dept_code':d['dept_code'],
                'div_name':d['div_name'],
                'div_code':d['div_code'],
                'faculty':faculty
            })

    # obtain the courses for department or faculty
    if dept:
        # all faculty courses for department
        courses = sections(code=dept,year=YEAR,sess=SESS)
        dept = academic_department(dept)
        if dept:
            dept = dept[0]
    elif request.method == 'POST' and not request.FILES:
        substr = 'dept_faculty'
        for key,val in request.POST.iteritems():
            if substr in key and val:
                pfid = int(val)
        if pfid:
            fid = pfid

    # this could be a faculty who is deptartment chair but has
    # courses in other department e.g. renaud
    if not fid and not courses:
        fid = uid
    # faculty courses
    if not courses:
        courses = sections(year=YEAR,sess=SESS,fid=fid)
        if courses:
            faculty_name = courses[0][11]

    secciones = []
    if courses:
        for course in courses:
            phile = syllabus_name(course)
            obj = {}
            for n,v in course.items():
                if n in ['crs_title','firstname','lastname']:
                    try:
                        v = u'{}'.format(v.decode('cp1252'))
                    except:
                        pass
                obj[n] = v
            secciones.append({'obj':obj,'phile':phile})

    # file upload
    phile = None
    if request.method=='POST' and request.FILES:
        # complete path to directory in which we will store the file
        syllabi = request.FILES.getlist('syllabi[]')
        # POST does not include empty file fields in [] so we use this
        # hidden field and javascript event to track
        syllabih = request.POST.getlist('syllabih[]')
        h = len(syllabi)
        for i in range (0,len(syllabih)):
            if syllabih[i] == 'True':
                year = request.POST.getlist('year[]')[i]
                sess = request.POST.getlist('sess[]')[i]
                crs_no = request.POST.getlist('crs_no[]')[i]
                code = crs_no.split(' ')[0]
                # chapuza for now until we can figure out what to do
                # with department codes that do not translate to actual
                # departments
                if DEPARTMENT_EXCEPTIONS.get(code):
                    code = DEPARTMENT_EXCEPTIONS.get(code)
                dept = academic_department(code)
                sendero = join(
                    settings.UPLOADS_DIR, year, sess, dept.div_code,
                    dept.dept_code
                )
                # for display at UI level
                dept = None
                syllabus = syllabi[len(syllabi)-h]
                # must be after the above
                h -= 1
                crs_title = request.POST.getlist('crs_title[]')[i]
                filename = request.POST.getlist('phile[]')[i]
                fullname = request.POST.getlist('fullname[]')[i]
                # create our DSpace manager
                manager = Manager()
                # remove existing file if it exists so we can replace it
                # with the current upload
                s =  Search()
                jason = s.file('{}.pdf'.format(filename), TITLE_ALT)
                if jason and jason[0].get('id'):
                    uri='items/{}/'.format(jason[0].get('id'))
                    response = manager.request(
                        uri, 'delete'
                    )
                phile = handle_uploaded_file(
                    syllabus, sendero, filename
                )
                if phile:
                    upload = '{}/{}'.format(sendero, phile)
                    # verify file type is PDF
                    mime = magic.from_file(upload, mime=True)
                    if mime == 'application/pdf' or mime == 'application/octet-stream':
                        # create a new parent item that will contain
                        # the uploaded file
                        item = {
                            'course_number': crs_no,
                            'title': crs_title,
                            'title_alt': phile,
                            'year': year,
                            'term': sess,
                            'fullname': fullname
                        }
                        new_item = create_item(item)
                        # send file to DSpace
                        uri='items/{}/bitstreams/'.format(new_item['id'])
                        response = manager.request(
                            uri, 'post', phile, phile=upload
                        )
                        messages.add_message(
                            request, messages.SUCCESS,
                            'The file was uploaded successfully.',
                            extra_tags='success'
                        )
                    else:
                        messages.add_message(
                            request, messages.ERROR,
                            '''
                                Files must be in PDF format. Please convert
                                your file to PDF and try again.
                            ''',
                            extra_tags='danger'
                        )
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        '''
                            Something has gone awry with the upload.
                            Please try again.
                        ''',
                        extra_tags='danger'
                    )

    return render(
        request, 'home.html', {
            'depts':dept_list,'courses':secciones,'department':dept,
            'faculty_name':faculty_name,'fid':fid,'year':YEAR,
            'sess':TERM_LIST[SESS[0]],'phile':phile,'dean_chair':dean_chair,
            'division':{'name':division_name,'code':division_code},
            'admin':admin
        }
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
        content = ''
        if name.strip() != 'Staff':
            s = Search()
            jason = s.file(phile, TITLE_ALT)
        if jason and jason[0].get('name'):
            earl = '{}/bitstream/handle/{}/{}?sequence=1&isAllowed=y'.format(
                settings.DSPACE_URL, jason[0].get('handle'), phile
            )
            response = render(
                request, 'view_file.ajax.html', {
                    'earl':earl,'handle':jason[0].get('handle')
                }
            )
        else:
            response = HttpResponse(
                '', content_type='text/plain; charset=utf-8'
            )
    else:
        response = HttpResponseRedirect(reverse_lazy('access_denied'))

    return response


def dspace_dept_courses(request, dept, term, year):
    cache_key = 'DSPACE_API_{}_{}_{}'.format(dept,term,year)
    if term == 'RC':
        term = settings.SPRING_TERMS
    elif term == 'RA':
        term = settings.FALL_TERMS
    else:
        raise Http404
    jay = cache.get(cache_key)
    if not jay:
        courses = sections(code=dept,year=year,sess=term)
        jay = '['
        if courses:
            for c in courses:
                if c[12] == 'Y':
                    phile = '{}.pdf'.format(syllabus_name(c))
                    s = Search()
                    jason = s.file(phile, TITLE_ALT)
                    earl = ''
                    if jason and jason[0].get('name'):
                        earl = '{}/bitstream/handle/{}/{}?sequence=1&isAllowed=y'.format(
                            settings.DSPACE_URL, jason[0].get('handle'), phile
                        )
                    jay += '{'
                    # json requires doubl quotes
                    jay += '''
                        "crs_no":"{}","earl":"{}","sess":"{}","sec_no":"{}",
                        "crs_title":"{}","fullname":"{}","need_syllabi":"{}"
                    '''.format(
                        c.crs_no, earl, c.sess, c.sec_no,
                        c.crs_title, c.fullname, c[12]
                    )
                    jay += '},'
            jay = jay[:-1] + ']'
        else:
            jay = jay + ']'
        cache.set(cache_key, jay, None)
    return HttpResponse(
        jay, content_type='text/plain; charset=utf-8'
    )


@portal_auth_required(
    session_var='DSPILOBUS_AUTH', redirect_url=reverse_lazy('access_denied')
)
def download(request, division, department=''):
    response = HttpResponse(content_type='application/x-gzip')
    name = '{}_{}_syllabi'.format(division, department)
    response['Content-Disposition'] = 'attachment; filename={}.tar.gz'.format(
        name
    )
    tar_ball = tarfile.open(fileobj=response, mode='w:gz')
    directory = False
    for sess in get_session_term():
        directory = '{}{}/{}/{}/{}'.format(
            settings.UPLOADS_DIR,YEAR,sess,division,department
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
def openxml(request, division, department=''):

    wb = load_workbook('{}template.xlsx'.format(settings.MEDIA_ROOT))

    # obtain the active worksheet
    template = wb.active

    if department:
        courses = sections(code=department,year=YEAR,sess=get_session_term())
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
            courses = sections(code=d.dept,year=YEAR,sess=get_session_term())
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
