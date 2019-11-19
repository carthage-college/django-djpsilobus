#!/bin/sh

DSPACEURL="https://carthage.upgrade.dspace-express.com/rest"
EMAIL="larry@carthage.edu"
PASSWORD=""
ACTION="login?"
RQST="email=${EMAIL}&password=${PASSWORD}"
URL="${DSPACEURL}/${ACTION}${RQST}"

echo ${DSPACEURL}
echo ${URL}

curl -D - "${URL}"
