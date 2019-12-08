# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.cache import cache

import json
import requests

"""
Suppress InsecureRequestWarning
https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
"""
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COOKIE_CACHE_KEY = settings.DSPACE_COOKIE_CACHE_KEY
REST_URL = settings.DSPACE_REST_URL
HEADERS = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}


def _get_cookie():

    # obtain our cookie from DSpace server
    login_url = '{}/login'.format(REST_URL)
    login_dict = {
        'email':'{}'.format(settings.DSPACE_EMAIL),
        'password':'{}'.format(settings.DSPACE_PASSWORD)
    }
    response = requests.get(
        url=login_url, params=login_dict, headers=HEADERS, verify=False
    )
    dic = response.cookies.get_dict()
    return dic['JSESSIONID']

def _get_status(headers, cookies):
    # check cookie status
    status = False
    response = requests.get(
        '{}/status'.format(REST_URL), cookies=cookies, headers=headers, verify=False
    )
    jason = json.loads(response.content)
    if jason['authenticated']:
        status = True
    return status


class Manager(object):

    def __init__(self):

        self.headers = HEADERS
        cookie = cache.get(COOKIE_CACHE_KEY)
        if not cookie:
            cookie = _get_cookie()
            cache.set(COOKIE_CACHE_KEY, cookie, None)
            cookies = {'JSESSIONID': cookie}
        else:
            cookies = {'JSESSIONID': cookie}
            if not _get_status(self.headers, cookies):
                cookie = _get_cookie()
                cache.set(COOKIE_CACHE_KEY, cookie, None)
                cookies = {'JSESSIONID': cookie}

        self.cookies = cookies

    def status(self):
        return _get_status(self.headers, self.cookies)

    def crumble(self):
        cache.delete(COOKIE_CACHE_KEY)

    def request(self, uri, action, req_dict=None, phile=None, headers=None):

        if not headers:
            headers = self.headers

        earl = '{}/{}'.format(REST_URL, uri)
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
            data = json.dumps(req_dict)
        else:
            # collection search by name and file upload use a string
            data = req_dict

        if phile:
            earl += '?name={}'.format(data)
            #headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Content-Type'] = 'multipart/form-data'
            #headers['accept'] = 'application/pdf'
            #del headers['accept']

            with open(phile,'rb') as payload:
                files={phile: payload}
                #files={'file': payload}
                #files = {
                    #'file': (phile, payload, 'application/pdf',
                    #{'Expires': '0'})
                #}
                #data = {'name': phile}
                response = action(
                    earl, files=files, headers=headers, cookies=self.cookies,
                    verify=False
                )
        elif action == 'delete':
            response = action(
                earl, headers=headers, cookies=self.cookies, verify=False
            )
        elif data:
            response = action(
                earl, data=data, headers=headers, cookies=self.cookies, verify=False
            )
        else:
            response = action(
                earl, headers=headers, cookies=self.cookies, verify=False
            )

        try:
            response = json.loads(response.content)
        except:
            response = response.content

        return response


class Search(Manager):

    def file(self, phile, metatag):
        """
        Search for a file by metatag
        """

        req_dict = {
            'key': '{}'.format(metatag),
            'value': '{}'.format(phile),
            'language': 'en_US'
        }

        return self.request(
            'items/find-by-metadata-field', 'post', req_dict
        )

    def collection(self, name=None):
        """
        Search for a collection
        """

        return self.request(
            name, 'collections/find-collection', 'post'
        )
