from django.conf import settings

import json
import requests

url = "https://dspace.carthage.edu/rest/login"
email = settings.DSPACE_EMAIL
password = settings.DSPACE_PASSWORD

request_dict = {
  "email":"{}".format(email),
  "password":"{}".format(password)
}

headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(request_dict), headers=headers)
#print response.__dict__
print "token:\n\n"
print response._content
