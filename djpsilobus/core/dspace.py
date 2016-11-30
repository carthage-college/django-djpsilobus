# -*- coding: utf-8 -*-
from django.conf import settings

import json
import requests

class Manager(object):

    def __init__(self):

        self.rest_url = settings.DSPACE_REST_URL
        # obtain our token from DSpace server
        login_url = "{}/login".format(self.rest_url)
        login_dict = {
            "email":"{}".format(settings.DSPACE_EMAIL),
            "password":"{}".format(settings.DSPACE_PASSWORD)
        }
        token = requests.post(
            login_url, data=json.dumps(login_dict),
            headers={'content-type': 'application/json'}
        )
        token = token._content
        self.headers = {
            "Content-Type": "application/json",
            "rest-dspace-token": "{}".format(token),
            "accept": "application/json"
        }

    def request(self, uri, action, req_dict=None, phile=None, headers=None):

        if not headers:
            headers = self.headers

        earl = "{}/{}".format(self.rest_url, uri)
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
                    earl,
                    files=files,
                    headers=headers
                )
        elif action == "delete":
            response = action(
                earl, headers=headers
            )
        else:
            response = action(
                earl, data=data, headers=headers
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
