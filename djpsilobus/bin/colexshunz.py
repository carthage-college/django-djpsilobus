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

import argparse
import json
import requests

REQUEST_TYPE = "json"
TOKEN = settings.DSPACE_TOKEN
HEADERS = {
    "Content-Type": "application/{}".format(REQUEST_TYPE),
    "rest-dspace-token": "{}".format(TOKEN),
    "accept": "application/{}".format(REQUEST_TYPE)
}


# set up command-line options
desc = """
Accepts as input an optional collection name.
Returns collection or all collections if no name provided.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument(
    "-n", "--name",
    required=False,
    help="The name of the collection",
    dest="name"
)

def main():
    """
    Using the DSpace REST API, list all collections or retrieve a
    collection if a name or an ID is provided.
    """

    action = "collections"
    if name:
        action = "collections/find-collection"
    earl = "{}/{}".format(settings.DSPACE_REST_URL, action)

    if name:
        response = requests.post(earl, data=name, headers=HEADERS)
    else:
        # API always times out for this one, for some reason
        response = requests.get(earl, headers=HEADERS)
    #print response.__dict__
    #print response._content
    #print response._content[0]["name"]
    print response.__dict__
    jason = json.loads(response._content)

    return jason

######################
# shell command line
######################

if __name__ == "__main__":
    args = parser.parse_args()
    name = args.name

    sys.exit(main())
