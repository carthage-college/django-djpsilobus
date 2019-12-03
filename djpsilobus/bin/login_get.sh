#!/bin/bash

# set the EMAIL and PASSWORD env variables from command line
# export PASSWORD="xxx"
# export EMAIL="spam@example.com"

echo ${EMAIL}
echo ${PASSWORD}

DSPACEURL="https://carthage.upgrade.dspace-express.com/rest"
ACTION="login?"
RQST="email=${EMAIL}&password=${PASSWORD}"
URL="${DSPACEURL}/${ACTION}${RQST}"

echo ${DSPACEURL}
echo ${URL}

#curl -D - "${URL}"
curl -D - --data-urlencode "password=$PASSWORD" --data-urlencode "email=$EMAIL" "${DSPACEURL}/${ACTION}"

