#!/bin/bash

RQST='
{
    "key": "dc.title.alternative",
    "value": "2016_RA_SPN_4200_01_Rodriguez_Lorenzo.pdf","language": "en"
}
'

DSPACEURL="https://dspace.carthage.edu/rest"
TOKEN=""
VERB="POST"
REQUEST_TYPE="json"
# mathematics jterm 2016 collection
ACTION="items/find-by-metadata-field"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}


curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "accept: application/${REQUEST_TYPE}" \
    -H "Content-Type: application/${REQUEST_TYPE}" \
    -X ${VERB} ${EARL} \
    -d "${RQST}"
