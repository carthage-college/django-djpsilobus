# -*- coding: utf-8 -*-
import os, sys

# env
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djpsilobus.settings")

from django.conf import settings

from djpsilobus.core.utils import find_file

import argparse

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

    '''
    if jason and jason[0].get("name"):
        print "title = {}".format(jason[0]["name"])
    else:
        print jason
    '''
    print jason


if __name__ == "__main__":
    args = parser.parse_args()
    phile = args.phile

    sys.exit(main())
