from django.conf import settings

import json
import requests

TOKEN = settings.DSPACE_TOKEN
ACTION = "items/find-by-metadata-field"
EARL = "{}/{}".format(settings.DSPACE_REST_URL, ACTION)
VERB = "POST"
REQUEST_TYPE="json"
HEADERS = {
    "Content-Type": "application/{}".format(REQUEST_TYPE),
    "rest-dspace-token": "{}".format(TOKEN),
    "accept": "application/{}".format(REQUEST_TYPE)
}

def find_file(phile):
    """
    Using the DSpace REST API, execute a search for a file name
    contained in the dc.title.alternative metadata field.

    Accepts as a argument a file name.
    Returns a json object
    """

    req_dict = {
        "key": "dc.title.alternative",
        "value": "{}".format(phile),
        "language": "en"
    }

    response = requests.post(EARL, data=json.dumps(req_dict), headers=HEADERS)
    jason = json.loads(response._content)

    return jason

