#!/bin/bash

# set the EMAIL and PASSWORD env variables from command line
# export PASSWORD="xxx"
# export EMAIL="spam@example.com"

echo ${EMAIL}
echo ${PASSWORD}

ACTION="login"

# POST
DSPACEURL="https://dspace.carthage.edu/rest"
RQST='{"email": "${EMAIL}", "password": "${PASSWORD}"}'
URL="${DSPACEURL}/${ACTION}"

echo ${URL}
echo ${RQST}

curl -v -H "Content-Type: application/json" --data "${RQST}" "${URL}"

# GET
DSPACEURL="https://carthage.upgrade.dspace-express.com/rest"
RQST="?email=${EMAIL}&password=${PASSWORD}"
URL="${DSPACEURL}/${ACTION}${RQST}"

echo ${URL}

curl -D - "${URL}"
