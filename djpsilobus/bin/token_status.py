from django.conf import settings

import json
import requests

'''
returns a json object:
{
    "okay":true,"authenticated":true,"email":"larry@example.com",
    "fullname":"Larry","token":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
'''

tipe = 'json'
action = 'status'
url = 'https://dspace.carthage.edu/rest/{}'.format(action)
token = settings.DSPACE_TOKEN

headers = {
    'content-type': 'application/{}'.format(tipe),
    'Accept': 'application/{}'.format(tipe),
    'rest-dspace-token': token
}

response = requests.get(url, headers=headers)
#print response.__dict__
print "token status:\n\n"
#print response._content["authenticated"]
r = json.loads( response._content )
print r
print r["authenticated"]

