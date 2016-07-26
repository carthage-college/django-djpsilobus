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
    Accepts as input an ID of Item that will be deleted
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-i", "--item",
    required=True,
    help="Item ID",
    dest="item"
)

def main():
    """
    Using the DSpace REST API, delete an item based on ID
    """

    manager = Manager()

    jason = manager.request(
        "items/{}".format(item), "delete"
    )

    print jason

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    item = args.item

    sys.exit(main())
