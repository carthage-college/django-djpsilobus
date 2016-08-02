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

from djpsilobus.core.utils import create_item

import argparse

YEAR = settings.YEAR
SESS = settings.SESS

# set up command-line options
desc = """
    Creates a new item in a collection.
    Required: collection ID, a user ID, a course number.
"""

parser = argparse.ArgumentParser(description=desc)

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

    user = User.objects.get(pk=uid)

    item = {
        "course_number": course,
        "title": "Operating Systems",
        "year": YEAR,
        "term": SESS,
        "user":user
    }
    new_item = create_item(item)
    print "new_item = {}".format(new_item)

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    uid = args.uid
    course = args.course
    test = args.test

    sys.exit(main())
