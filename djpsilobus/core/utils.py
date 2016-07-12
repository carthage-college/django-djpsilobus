from django.conf import settings

from djpsilobus.core.dspace import Manager

import json
import requests


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

    manager = Manager()

    jason = manager.request(
        req_dict, "items/find-by-metadata-field", "post"
    )

    return jason
