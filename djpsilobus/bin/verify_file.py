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

from django.conf import settings

from djpsilobus.core.dspace import Manager

from pyPdf import PdfFileReader

import argparse

# set up command-line options
desc = """
    Verifies a PDF file by simply attempting to open it.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-f", "--file",
    required=True,
    help="Complete path to file e.g. /opt/data/foo_bar.pdf",
    dest="phile"
)

def main():

    try:
        mypdf = PdfFileReader(file( phile, 'rb'))
        print phile,' is valid pdf'
    except:
        print phile,' is invalid pdf'
        e = sys.exc_info()
        print e

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    phile = args.phile

    sys.exit(main())
