# -*- coding: utf-8 -*-
from django.conf import settings

import json
import requests


import logging
logger = logging.getLogger(__name__)

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

    def request(self, req_dict, uri, action, headers=None):

        earl = "{}/{}".format(self.rest_url, uri)

        if action == "post":
            action = requests.post
        elif action == "get":
            action = requests.get
        else:
            return None

        response = action(
            earl, data=json.dumps(req_dict), headers=self.headers
        )

        if uri == "login":
            return response._content
        else:
            return json.loads(response._content)

    def login(self):

        headers = {
            "Content-Type": "application/{}".format(self.request_type),
        }
        response = self.request(
            self.auth_dict, "login", "post", headers
        )

        return response

    def logout(self):
        """
        No output means success, error output means error"
        """

        response = self.request(
            self.auth_dict, "logout", "post"
        )

        return response
