# -*- coding: utf-8 -*-
from django.conf import settings

import json
import requests


class Manager(object):

    def __init__(self,
        token=settings.DSPACE_TOKEN,
        email = settings.DSPACE_EMAIL,
        password = settings.DSPACE_PASSWORD,
        rest_url=settings.DSPACE_REST_URL, request_type="json"):

        self.email = email
        self.password = password
        self.rest_url = rest_url
        self.request_type = request_type
        self.auth_dict = {
            "email":"{}".format(self.email),
            "password":"{}".format(self.password)
        }
        self.headers = {
            "Content-Type": "application/{}".format(request_type),
            "rest-dspace-token": "{}".format(token),
            "accept": "application/{}".format(request_type)
        }

    def request(self, req_dict, uri, action, phile=None, headers=None):

        if not headers:
            headers = self.headers

        earl = "{}/{}".format(self.rest_url, uri)
        if action == "post":
            action = requests.post
        elif action == "get":
            action = requests.get
        else:
            return None

        # dictionary or string?
        if type(req_dict) is dict:
            data = json.dumps(req_dict)
        else:
            # used only for collection search by name
            data = req_dict

        if phile:
            response = action(
                earl,
                files={'file': open(phile, 'rb')},
                headers=headers
            )
        else:
            response = action(
                earl, data=data, headers=headers
            )

        if uri == "login":
            return response._content
        else:
            return json.loads(response._content)


class Auth(Manager):

    def login(self):
        """
        Sign in to the DSPace REST API.
        Returns authentication token which never expires
        until logout request is sent.
        """

        headers = {
            "Content-Type": "application/{}".format(self.request_type),
        }

        return self.request(
            self.auth_dict, "login", "post", headers=headers
        )

    def logout(self):
        """
        No output means success, error output means error
        """

        return self.request(
            self.auth_dict, "logout", "post"
        )


class Search(Manager):

    def file(self, phile, metatag):
        """
        Search for a file by metatag
        """

        req_dict = {
            "key": "{}".format(metatag),
            "value": "{}".format(phile),
            "language": "en"
        }
        print req_dict

        return self.request(
            req_dict, "items/find-by-metadata-field", "post"
        )

    def collection(self, name=None):
        """
        Search for a collection
        """

        return self.request(
            name, "collections/find-collection", "post"
        )
