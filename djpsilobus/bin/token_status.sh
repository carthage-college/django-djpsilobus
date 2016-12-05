#!/bin/sh

'''
returns a json object:
{
    "okay":true,"authenticated":true,"email":"larry@example.com",
    "fullname":"Larry","token":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
'''

DSPACEURL="https://dspace.carthage.edu/rest"
TOKEN=""
TYPE="json"
VERB="GET"
ACTION="status"

URL="${DSPACEURL}/${ACTION}"

curl -X ${VERB} \
  -H "Content-Type: application/${TYPE}" \
  -H "Accept: application/${TYPE}" \
  -H "rest-dspace-token: ${TOKEN}" \
  "${URL}"
