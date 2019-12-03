from django.conf import settings

import json
import requests

url = 'https://carthage.upgrade.dspace-express.com/rest/login'
email = settings.DSPACE_EMAIL
password = settings.DSPACE_PASSWORD

request_dict = {
  "email":"{}".format(email),
  "password":"{}".format(password)
}

#headers = {'content-type': 'application/json'}
#response = requests.post(url, data=json.dumps(request_dict), headers=headers)

response = requests.get(url=url, params=request_dict)

#print("token:\n\n")
#print(response._content)
print("response")
print(response)
print("dictionary")
print(response.__dict__)
