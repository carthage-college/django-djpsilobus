# -*- coding: utf-8 -*-
import os, sys

# env
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/usr/lib/python2.7/')
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
sys.path.append('/data2/django_1.9/')
sys.path.append('/data2/django_projects/')
sys.path.append('/data2/django_third/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djpsilobus.nsettings")

from django.conf import settings

from djpsilobus.core.utils import find_file

import argparse
import json
import requests


# set up command-line options
desc = """
Accepts as input a file name to be searched in the
dc.title.alternative metadata field
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-f", "--filename",
    required=True,
    help="The name of the file for which to search",
    dest="phile"
)

def main():
    """
    Using the DSpace REST API, execute a search for a file named
    in the --file parameter and contained in the dc.title.alternative
    metadata field.
    """

    jason = find_file(phile)

    if len(jason) > 0 and jason[0].get("name"):
        print "title = {}".format(jason[0]["name"])
    else:
        print jason

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    phile = args.phile

    sys.exit(main())
