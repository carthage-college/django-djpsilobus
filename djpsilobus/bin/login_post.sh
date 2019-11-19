#!/bin/sh

DSPACEURL="https://dspace.carthage.edu/rest"
EMAIL="larry@carthage.edu"
PASSWORD=""
TYPE="json"
ACTION="login"

URL="${DSPACEURL}/${ACTION}"

RQST="{
  \"email\":\"${EMAIL}\",
  \"password\":\"${PASSWORD}\"
}"

echo ${DSPACEURL}
echo ${URL}

curl -4 \
  -H "Content-Type: application/${TYPE}" \
  --data "${RQST}" \
  "${URL}"
