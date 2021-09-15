#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

from django.conf import settings
from djpsilobus.core.dspace import Search


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djpsilobus.settings.shell')

logger = logging.getLogger('debug_logfile')

# set up command-line options
desc = """
    Accepts as input file name prefix and full name of the author.
    e.g.
    python bin/file_search.py
        --name="Larry Kurkowski"
        --file=2021_RA_CDM_1200_04_Kurkowski_Larry_syllabus.pdf
        --test
"""

# RawTextHelpFormatter method allows for new lines in help text
parser = argparse.ArgumentParser(
    description=desc, formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument(
    '-n',
    '--name',
    required=True,
    help='Full name of the author in quotes e.g. "Karl Marx".',
    dest='name',
)
parser.add_argument(
    '-f',
    '--file',
    required=True,
    help='file name prefix of the syllabus.',
    dest='phile',
)
parser.add_argument(
    '--test',
    action='store_true',
    help='Dry run?',
    dest='test',
)

TITLE_ALT = settings.DSPACE_TITLE_ALT


def main():
    """Main function description."""
    search = Search()
    jason = search.file(phile, TITLE_ALT)
    if test:
        print(phile)
        print(name)
        print('json')
        print(jason)
    else:
        logger.debug('phile: %s', phile)
        logger.debug('name: %s', name)


if __name__ == '__main__':
    args = parser.parse_args()
    name = args.name
    phile = args.phile
    test = args.test

    if test:
        print(args)

    sys.exit(main())
