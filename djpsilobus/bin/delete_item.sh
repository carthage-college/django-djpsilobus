#!/bin/bash

DSPACEURL="https://dspace.carthage.edu/rest"
TOKEN=""
VERB="DELETE"
REQUEST_TYPE="json"
ACTION="items/1059"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}

curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "accept: application/${REQUEST_TYPE}" \
    -H "Content-Type: application/${REQUEST_TYPE}" \
    -X ${VERB} ${EARL}

