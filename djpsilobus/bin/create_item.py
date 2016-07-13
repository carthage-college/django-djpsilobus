# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.9/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djpsilobus.settings")

import django

django.setup()

from django.conf import settings
from django.contrib.auth.models import User

from djpsilobus.core.dspace import Manager
from djpsilobus.core.data import DEPARTMENTS, ITEM_METADATA

from djzbar.utils.informix import get_session
from djzbar.core.models.courses import AbstractRecord

import argparse

EARL = settings.INFORMIX_EARL

# set up command-line options
desc = """
    Creates a new item in a collection.
    Required: collection ID, a user ID, a course number.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-c", "--cid",
    required=True,
    help="Collection ID",
    dest="cid"
)
parser.add_argument(
    "-u", "--uid",
    required=True,
    help="User ID",
    dest="uid"
)
parser.add_argument(
    "-k", "--course",
    required=True,
    help="Course number enclosed in quotes e.q.'PHY 1030'",
    dest="course"
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

def main():

    data = ITEM_METADATA

    # create database session
    session = get_session(EARL)

    c = session.query(AbstractRecord).\
        filter_by(crs_no=course).\
        filter_by(cat="UG16").one()

    abstr = c.abstr.split('\n')
    if len(abstr) > 1 and abstr[2] != "":
        abstr = abstr[2]
    else:
        abstr = c.abstr

    user = User.objects.get(pk=uid)

    dept = course.split(" ")[0]
    collection_id = DEPARTMENTS[dept]
    # author
    data['metadata'][0]['value'] = "{}, {}".format(
        user.last_name, user.first_name
    )
    # description
    data['metadata'][1]['value'] = c.abstr.split('\n')[2]
    # title
    data['metadata'][2]['value'] = "Operating Systems"
    # year
    data['metadata'][3]['value'] = "2016"
    # term
    data['metadata'][4]['value'] = "Fall"
    uri = "collections/{}/items".format(collection_id)
    if not test:
        manager = Manager()
        new_item = manager.request(data, uri, "post")
        print new_item
    else:
        print dept
        print uri
        print data


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    cid = args.cid
    uid = args.uid
    course = args.course
    test = args.test

    sys.exit(main())
