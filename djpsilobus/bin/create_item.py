# -*- coding: utf-8 -*-
import os, sys

# env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpsilobus.settings')

import django

django.setup()

from django.conf import settings

from djpsilobus.core.utils import create_item

import argparse

YEAR = settings.YEAR
SESS = 'RA'

# set up command-line options
desc = """
    Creates a new item in a collection.
    Required: a course number.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    '-c', '--course',
    required=True,
    help="Course number enclosed in quotes e.q.'PHY 1030'",
    dest='course'
)
parser.add_argument(
    '--test',
    action='store_true',
    help="Dry run?",
    dest='test'
)

def main():

    item = {
        'course_number': course,
        'title': 'Operating Systems',
        'year': str(YEAR),
        'fullname': 'Mark Mahoney',
        'title_alt': '2018_RA_CSC_2810_02_Mahoney_Mark_syllabus.pdf',
        'term': SESS
    }
    if test:
        print(item)
    else:
        new_item = create_item(item)
        print("new_item = {}".format(new_item))


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    course = args.course
    test = args.test

    sys.exit(main())
