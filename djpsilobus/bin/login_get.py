from django.conf import settings

import json
import requests

url = '{}/login'.format(settings.DSPACE_REST_URL)

email = settings.DSPACE_EMAIL
password = settings.DSPACE_PASSWORD

request_dict = {
  "email":"{}".format(email),
  "password":"{}".format(password)
}

headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}
#response = requests.post(url, data=json.dumps(request_dict), headers=headers)
response = requests.get(url=url, params=request_dict, headers=headers)

print("response")
print(response)
print("dictionary")
print(response.__dict__)
print(response.cookies.__dict__)
print(response.cookies.get_dict())
dic = response.cookies.get_dict()
print(dic['JSESSIONID'])
