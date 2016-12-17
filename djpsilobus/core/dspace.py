# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache

import json
import requests

REST_URL = settings.DSPACE_REST_URL
def _get_token():
    # obtain our token from DSpace server
    login_url = "{}/login".format(REST_URL)
    login_dict = {
        "email":"{}".format(settings.DSPACE_EMAIL),
        "password":"{}".format(settings.DSPACE_PASSWORD)
    }
    token = requests.post(
        login_url, data=json.dumps(login_dict),
        headers={'content-type': 'application/json'},
        verify=False
    )
    return token._content

class Manager(object):

    def __init__(self):

        token = cache.get("DSPACE_API_TOKEN")
        if not token:
            # obtain our token from DSpace server
            login_url = "{}/login".format(REST_URL)
            login_dict = {
                "email":"{}".format(settings.DSPACE_EMAIL),
                "password":"{}".format(settings.DSPACE_PASSWORD)
            }
            token = requests.post(
                login_url, data=json.dumps(login_dict),
                headers={'content-type': 'application/json'},
                verify=False
            )
            token = token._content
            token = _get_token()
            cache.set("DSPACE_API_TOKEN", token, None)
        else:
            # check token status
            headers = {
                'content-type': 'application/json',
                'Accept': 'application/json',
                'rest-dspace-token': token
            }
            response = requests.get(
                '{}/status'.format(REST_URL),
                headers=headers, verify=False
            )
            r = json.loads( response._content )

            if r["authenticated"] != "true":
                token = _get_token()
        self.headers = {
            "Content-Type": "application/json",
            "rest-dspace-token": "{}".format(token),
            "accept": "application/json"
        }

    def request(self, uri, action, req_dict=None, phile=None, headers=None):

        if not headers:
            headers = self.headers

        earl = "{}/{}".format(REST_URL, uri)
        if action == "post":
            action = requests.post
        elif action == "get":
            action = requests.get
        elif action == "delete":
            action = requests.delete
        else:
            return None

        # dictionary or string?
        if type(req_dict) is dict:
            data = json.dumps(req_dict)
        else:
            # collection search by name and file upload use a string
            data = req_dict

        if phile:
            earl += "?name={}".format(data)
            #headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["Content-Type"] = "multipart/form-data"
            #headers["accept"] = "application/pdf"
            #del headers["accept"]

            with open(phile,'rb') as payload:
                files={phile: payload}
                #files={'file': payload}
                #files = {'file': (phile, payload, 'application/pdf', {'Expires': '0'})}
                #data = {'name': phile}
                response = action(
                    earl, files=files, headers=headers, verify=False
                )
        elif action == "delete":
            response = action(
                earl, headers=headers, verify=False
            )
        else:
            response = action(
                earl, data=data, headers=headers, verify=False
            )

        try:
            response = json.loads(response._content)
        except:
            response = response._content

        return response


class Search(Manager):

    def file(self, phile, metatag):
        """
        Search for a file by metatag
        """

        req_dict = {
            "key": "{}".format(metatag),
            "value": "{}".format(phile),
            "language": "en_US"
        }

        return self.request(
            "items/find-by-metadata-field", "post", req_dict
        )

    def collection(self, name=None):
        """
        Search for a collection
        """

        return self.request(
            name, "collections/find-collection", "post"
        )
