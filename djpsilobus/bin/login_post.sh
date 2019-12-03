#!/bin/sh

DSPACEURL="https://dspace.carthage.edu/rest"
EMAIL="larry@carthage.edu"
#PASSWORD=""
PASSWORD="wOr7I#v*6cdIBcuQ%Q8EkDux@&FV40Ln"
TYPE="json"
ACTION="login"

URL="${DSPACEURL}/${ACTION}"

RQST="{
  \"email\":\"${EMAIL}\",
  \"password\":\"${PASSWORD}\"
}"

echo ${DSPACEURL}
echo ${URL}

#curl -4 \
  #-H "Content-Type: application/${TYPE}" \
  #--data "${RQST}" \
  #"${URL}"

curl -v -X POST --data "email=${EMAIL}&password=${PASSWORD}" ${URL}
