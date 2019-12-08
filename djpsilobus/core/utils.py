# -*- coding: utf-8 -*-
from django.conf import settings

from djpsilobus.core.data import DEPARTMENTS, ITEM_METADATA
from djpsilobus.core.dspace import Manager

from djzbar.utils.informix import get_session
from djzbar.core.models.courses import AbstractRecord
from djzbar.constants import TERM_LIST

import os
import re
import json
import requests

EARL = settings.INFORMIX_EARL


def find_file(phile):
    """
    Using the DSpace REST API, execute a search for a file name
    contained in the dc.title.alternative metadata field.

    Accepts as a argument a file name.
    Returns a json object
    """

    req_dict = {
        'key': 'dc.title.alternative',
        'value': '{}'.format(phile),
        'language': 'en_US'
    }

    manager = Manager()

    jason = manager.request(
        'items/find-by-metadata-field', 'post', req_dict
    )

    return jason


def get_items(collection_id):
    """
    accepts a collection UUID and returns all items in that collection
    """
    manager = Manager()

    jason = manager.request(
        'collections/{}/items'.format(collection_id), 'get'
    )

    return jason



def create_item(item):
    """
    Accepts a dictionary with the following keys:
    course_number, title, year, term, fullname
    """

    data = ITEM_METADATA

    # create database session
    session = get_session(EARL)

    prefix = 'UG'
    if item['term'][0] == 'G':
        prefix = 'GR'
    print(item)
    print(prefix)
    print(item['year'][-2:])
    cat = '{}{}'.format(prefix, item['year'][-2:])
    c = session.query(AbstractRecord).\
        filter_by(crs_no = item['course_number']).\
        filter_by(cat = cat).first()
    if c and c.abstr:
        abstr = c.abstr.split('\n')
        if len(abstr) > 1:
            try:
                abstr = abstr[2].decode('cp1252', 'ignore')
            except:
                abstr = c.abstr.decode('cp1252', 'ignore')
        else:
            abstr = c.abstr.decode('cp1252', 'ignore')
    else:
        abstr = ''

    dept = item['course_number'].split(' ')[0]
    collection_id = DEPARTMENTS[dept]
    # author
    data['metadata'][0]['value'] = item['fullname']
    # description
    data['metadata'][1]['value'] = abstr
    # title
    data['metadata'][2]['value'] = item['title']
    # title alternative
    data['metadata'][3]['value'] = item['title_alt']
    # subject: year
    data['metadata'][4]['value'] = item['year']
    # subject: term
    data['metadata'][5]['value'] = TERM_LIST[item['term']]
    uri = 'collections/{}/items'.format(collection_id)
    print(uri)
    manager = Manager()
    new_item = manager.request(uri, 'post', data)
    return new_item


def syllabus_name(course):
    """
    Creates the syllabus name that DSpace expects and
    which is 99.9% unique for search purposes.
    """

    lastname = re.sub('[^0-9a-zA-Z]+', '_', course.lastname)
    firstname = re.sub('[^0-9a-zA-Z]+', '_', course.firstname)
    return u'{}_{}_{}_{}_{}_{}_syllabus'.format(
        course.yr, course.sess, course.crs_no.replace(' ','_'),
        course.sec_no, lastname, firstname
    )


def sheet(ws, division, department, courses):
    # set sheet title
    ws.title = department
    # create a list for each row and insert into workbook
    for c in courses:
        section = []
        for item in c:
            # convert strings in case there are funky characters
            if isinstance(item, str):
                section.append(item.decode('cp1252').encode('utf-8'))
            else:
                section.append(item)

        # check for syllabus
        phile = syllabus_name(c)
        path = '{}{}/{}/{}/{}/{}.pdf'.format(
            settings.UPLOADS_DIR,c.yr,c.sess,
            division, department,phile
        )
        if os.path.isfile(path):
            syllabus='Yes'
        else:
            syllabus='No'

        section.append(syllabus)
        ws.append(section)

    return ws
