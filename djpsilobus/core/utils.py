# -*- coding: utf-8 -*-

"""Various utilities for interacting with the API."""

import os
import re
import pyodbc

from django.conf import settings
from djimix.constants import TERM_LIST
from djimix.core.database import get_connection
from djimix.core.database import xsql
from djpsilobus.core.data import DEPARTMENTS
from djpsilobus.core.data import ITEM_METADATA
from djpsilobus.core.dspace import Manager
from djpsilobus.core.sql import SECTIONS


def sections(code=None, year=None, sess=None, fid=None):
    """Fetch all course sections.

    Args:
        code: a department code
        year: YYYY
        sess: a tuple of sessions
        fid:  a faculty ID

    Returns:
        all courses that meet the above criteria.
    """

    where = ''

    if code:
        where += ' AND crs_rec.dept = "{0}" '.format(code)
    if year:
        where += ' AND sec_rec.yr = {0} '.format(year)
    if sess:
        where += ' AND sec_rec.sess in {0} '.format(sess)
    if fid:
        where += ' AND sec_rec.fac_id = {0} '.format(fid)

    connection = get_connection()
    # close connection when exiting with block
    sql = SECTIONS(where=where)
    with connection:
        rows = xsql(sql, connection)
        try:
            return rows.fetchall()
        except AttributeError:
            #return None
            return sql

def division_departments(code):
    """Fetch all departments for a division given the four letter code."""
    sql = """
        SELECT * FROM dept_table
        WHERE div = '{0}' ORDER BY txt
    """.format(code)

    connection = get_connection()
    # close connection when exiting with block
    with connection:
        return xsql(sql, connection).fetchall()


def find_file(phile):
    """Using the DSpace REST API, execute a search for a file name
    contained in the dc.title.alternative metadata field.

    Args:
        phile: a file name.

    Returns:
        a json object.

    Raises:
        none.
    """

    req_dict = {
        'key': 'dc.title.alternative',
        'value': '{0}'.format(phile),
        'language': 'en_US',
    }

    manager = Manager()

    return manager.request(
        'items/find-by-metadata-field', 'post', req_dict,
    )


def get_items(collection_id):
    """Fetch items form the API.

    Args:
        collection_id: a collection UUID

    Returns:
        all items in that collection

    Raises:
        none.
    """

    manager = Manager()

    return manager.request(
        'collections/{0}/items'.format(collection_id), 'get',
    )


def create_item(item):
    """Create an item through the API.

    Args:
        item: a dictionary with the following keys:
              course_number, title, year, term, fullname

    Returns:
        new_item: the newly created item

    Raises:
        none.
    """

    item_data = ITEM_METADATA

    prefix = 'UG'
    if item['term'][0] == 'G':
        prefix = 'GR'
    cat = '{0}{1}'.format(prefix, item['year'][-2:])

    sql = 'SELECT * FROM crsabstr_rec WHERE crs_no="{0}" AND cat="{1}"'.format(
        item['course_number'], cat,
    )

    connection = get_connection()
    with connection:
        row = xsql(sql, connection)
        if row:
            row = row.fetchone()

    if row and row.abstr:
        abstr = row.abstr
    else:
        abstr = ''

    dept = item['course_number'].split(' ')[0]
    collection_id = DEPARTMENTS[dept]
    # author
    item_data['metadata'][0]['value'] = item['fullname']
    # description
    item_data['metadata'][1]['value'] = abstr
    # title
    item_data['metadata'][2]['value'] = item['title']
    # title alternative
    item_data['metadata'][3]['value'] = item['title_alt']
    # subject year
    item_data['metadata'][4]['value'] = item['year']
    # subject term
    item_data['metadata'][5]['value'] = TERM_LIST[item['term']]

    uri = 'collections/{0}/items'.format(collection_id)
    manager = Manager()

    return manager.request(uri, 'post', item_data)


def syllabus_name(course):
    """Creates the syllabus name that DSpace expects."""
    lastname = re.sub('[^0-9a-zA-Z]+', '_', course.lastname)
    firstname = re.sub('[^0-9a-zA-Z]+', '_', course.firstname)
    return '{0}_{1}_{2}_{3}_{4}_{5}_syllabus'.format(
        course.yr,
        course.sess,
        course.crs_no.replace(' ', '_'),
        course.sec_no,
        lastname,
        firstname,
    )


def sheet(ws, division, department, courses):
    """Create a spread sheet."""
    # set sheet title
    ws.title = department
    # create a list for each row and insert into workbook
    for course in courses:
        section = []
        for course_item in course:
            section.append(course_item)

        # check for syllabus
        phile = syllabus_name(course)
        path = '{0}{1}/{2}/{3}/{4}/{5}.pdf'.format(
            settings.UPLOADS_DIR,
            course.yr,
            course.sess,
            division,
            department,
            phile,
        )
        if os.path.isfile(path):
            syllabus = 'Yes'
        else:
            syllabus = 'No'

        section.append(syllabus)
        ws.append(section)

    return ws
