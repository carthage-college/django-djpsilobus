from django.conf import settings

from djpsilobus.core.data import DEPARTMENTS, ITEM_METADATA
from djpsilobus.core.dspace import Manager

from djzbar.utils.informix import get_session
from djzbar.core.models.courses import AbstractRecord
from djzbar.constants import TERM_LIST

import json
import requests

EARL = settings.INFORMIX_EARL


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
        "language": "en_US"
    }

    manager = Manager()

    jason = manager.request(
        "items/find-by-metadata-field", "post", req_dict
    )

    return jason

def create_item(item):
    """
    Accepts a dictionary with the following keys:
    course_number, title, year, term, user
    """

    data = ITEM_METADATA

    # create database session
    session = get_session(EARL)

    cat = "UG{}".format(item["year"][-2:])
    c = session.query(AbstractRecord).\
        filter_by(crs_no = item["course_number"]).\
        filter_by(cat = cat).one()

    abstr = c.abstr.split('\n')
    if len(abstr) > 1 and abstr[2] != "":
        abstr = abstr[2]
    else:
        abstr = c.abstr

    dept = item["course_number"].split(" ")[0]
    collection_id = DEPARTMENTS[dept]
    # author
    data['metadata'][0]['value'] = "{}, {}".format(
        item["user"].last_name, item["user"].first_name
    )
    # description
    data['metadata'][1]['value'] = c.abstr.split('\n')[2]
    # title
    data['metadata'][2]['value'] = item["title"]
    # title alternative
    data['metadata'][3]['value'] = item["title_alt"]
    # subject: year
    data['metadata'][4]['value'] = item["year"]
    # subject: term
    data['metadata'][5]['value'] = TERM_LIST[item["term"]]
    uri = "collections/{}/items".format(collection_id)

    print "data = {}".format(data)
    print "uri = {}".format(uri)

    manager = Manager()
    new_item = manager.request(uri, "post", data)
    #print "new_item={}".format(new_item)
    #print "id={}".format(new_item['id'])
    return new_item
