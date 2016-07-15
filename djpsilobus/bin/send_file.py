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

import argparse

# set up command-line options
desc = """
    Uploads a file to an Item in DSpace.
    Required: Item ID, full path to filename.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-i", "--iid",
    required=True,
    help="Item ID",
    dest="iid"
)
parser.add_argument(
    "-f", "--file",
    required=True,
    help="Complete path to filename e.g. /opt/data/foo_bar.pdf",
    dest="phile"
)
parser.add_argument(
    "--test",
    action='store_true',
    help="Dry run?",
    dest="test"
)

def main():

    uri="items/{}/bitstreams/".format(iid)

    manager = Manager()
    if not test:
        jason = manager.request(
            uri, "post",
            "Rosa_Luxemburg_Huelga_masas_23.pdf",
            phile=phile
        )
        print jason
    else:
        print phile


######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    iid = args.iid
    phile = args.phile
    test = args.test

    sys.exit(main())
