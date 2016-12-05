from django.conf import settings

import json
import requests

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
print response._content


