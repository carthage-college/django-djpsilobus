# -*- coding: utf-8 -*-

import json

import requests
import urllib3
from django.conf import settings
from django.core.cache import cache


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIE_CACHE_KEY = settings.DSPACE_COOKIE_CACHE_KEY
REST_URL = settings.DSPACE_REST_URL


def _get_cookie():

    # obtain our cookie from DSpace server
    login_url = '{0}/login'.format(REST_URL)
    login_dict = {
        'email': '{0}'.format(settings.DSPACE_EMAIL),
        'password': '{0}'.format(settings.DSPACE_PASSWORD),
    }
    response = requests.get(
        url=login_url,
        params=login_dict,
        headers={
            'content-type': 'application/json',
            'Accept': 'application/json',
        },
        verify=False,
    )
    dic = response.cookies.get_dict()
    return dic['JSESSIONID']


def _get_status(cookies):
    # check cookie status
    url = '{0}/status'.format(REST_URL)
    response = requests.get(
        url,
        cookies=cookies,
        headers={
            'content-type': 'application/json',
            'Accept': 'application/json',
        },
        verify=False,
    )
    jason = json.loads(response.content)
    return jason['authenticated']


class Manager(object):
    """Manager class for interacting with the API."""

    def __init__(self):
        """Initialise with java session cookie from the API."""
        self.headers = {
            'content-type': 'application/json',
            'Accept': 'application/json',
        }
        cookie = cache.get(COOKIE_CACHE_KEY)
        if cookie:
            cookies = {'JSESSIONID': cookie}
            if not _get_status(cookies):
                cookie = _get_cookie()
                cache.set(COOKIE_CACHE_KEY, cookie, None)
                cookies = {'JSESSIONID': cookie}
        else:
            cookie = _get_cookie()
            cache.set(COOKIE_CACHE_KEY, cookie, None)
            cookies = {'JSESSIONID': cookie}

        self.cookies = cookies

    def status(self):
        """Returns the status of the java cookie from tomcat."""
        return _get_status(self.cookies)

    def crumble(self):
        """Deletes the java cookie from tomcat."""
        cache.delete(COOKIE_CACHE_KEY)

    def request(self, uri, action, req_dict=None, phile=None, headers=None):
        """Handles generic requests to the REST API."""
        if not headers:
            headers = {
                'content-type': 'application/json',
                'Accept': 'application/json',
            }

        earl = '{0}/{1}'.format(REST_URL, uri)
        if action == 'post':
            action = requests.post
        elif action == 'get':
            action = requests.get
        elif action == 'delete':
            action = requests.delete
        else:
            return None

        # dictionary or string?
        if type(req_dict) is dict:
            jason = json.dumps(req_dict)
        else:
            # collection search by name and file upload use a string
            jason = req_dict

        if phile:
            earl += '?name={0}'.format(jason)
            # we need a new headers container otherwise the multipart addition
            # interferes with the other places we use headers
            file_headers = self.headers
            file_headers['Content-Type'] = 'multipart/form-data'

            with open(phile, 'rb') as payload:
                files = {phile: payload}
                response = action(
                    earl,
                    files=files,
                    headers=file_headers,
                    cookies=self.cookies,
                    verify=False,
                )
        elif action == 'delete':
            response = action(
                earl, headers=headers, cookies=self.cookies, verify=False,
            )
        elif jason:
            response = action(
                earl,
                data=jason,
                headers=headers,
                cookies=self.cookies,
                verify=False,
            )
        else:
            response = action(
                earl, headers=headers, cookies=self.cookies, verify=False,
            )

        try:
            response = json.loads(response.content)
        except ValueError:
            response = response.content

        return response


class Search(Manager):
    """Search the REST API, which extends Manager class."""

    def file(self, phile, metatag):
        """Search for a file by metatag."""
        req_dict = {
            'key': '{0}'.format(metatag),
            'value': '{0}'.format(phile),
            'language': 'en_US',
        }

        return self.request(
            'items/find-by-metadata-field',
            'post',
            req_dict,
            headers={
                'content-type': 'application/json',
                'Accept': 'application/json',
            },
        )

    def collection(self, name=None):
        """Search for a collection."""
        return self.request(
            name, 'collections/find-collection', 'post',
        )
