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

from djpsilobus.core.utils import sheet, syllabus_name
from djpsilobus.core.data import HEADERS
from djzbar.utils.academics import sections
from djzbar.utils.academics import division_departments

from openpyxl import Workbook
from openpyxl import load_workbook

import argparse

YEAR = settings.YEAR
SESS = settings.SESS

# set up command-line options
desc = """
    Creates an OpenXML workbook with course syllabi data.
    Required: Department code. e.g. PHY
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "--division",
    required=True,
    help="Department code e.q.'NSSS'",
    dest="division"
)
parser.add_argument(
    "--department",
    required=False,
    help="Department code e.q.'PHY'",
    dest="department"
)
parser.add_argument(
    "--debug",
    action='store_true',
    help="Dry run?",
    dest="debug"
)


def main():

    if debug:
        print "department code = {}".format(department)

    wb = load_workbook('assets/template.xlsx')
    # obtain the active worksheet
    template = wb.active

    if department:
        courses = sections(code=department,year=YEAR,sess=SESS)
        if courses:
            sheet(template, division, department, courses)
            # Save the file
            wb.save("{}.xlsx".format(department))
        else:
            print "no courses found"
    else:
        depts = division_departments(division)
        for d in depts:
            courses = sections(code=d.dept,year=YEAR,sess=SESS)
            if courses:
                ws = wb.copy_worksheet(template)
                ws.title = d.dept
                hoja = sheet(ws, division, d.dept, courses)
        # remove the template sheet
        wb.remove_sheet(template)
        # Save the file
        wb.save("{}.xlsx".format(division))


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    department = args.department
    division = args.division
    debug = args.debug

    sys.exit(main())
