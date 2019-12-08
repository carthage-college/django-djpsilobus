from django.conf import settings

import requests
import xml.etree.ElementTree as ET
import json

url = '{}/status'.format(settings.DSPACE_REST_URL)

cookies = {'JSESSIONID': settings.DSPACE_JSESSIONID}
headers = {
    'content-type': 'application/json',
    'Accept': 'application/json'
}

response = requests.get(url=url, cookies=cookies, headers=headers)
print(response.__dict__)

# json response from API
print(response.content)
jason = json.loads(response.content)
print(jason['authenticated'])
if jason['authenticated']:
    print('authenticated')
else:
    print('not authenticated')

#print(response.content['authenticate'])

# XML response from API
#tree = ET.fromstring(response.content)
#print(tree.tag)
#for t in tree:
#    print(t.tag, t.text)
#auth = tree.find('authenticated').text
#print(auth)
