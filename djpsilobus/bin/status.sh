#!/bin/bash

# set JSESSIONID env variable from command line
# export JSESSIONID="xxx"

echo ${JSESSIONID}

DSPACEURL="https://carthage.upgrade.dspace-express.com/rest"
ACTION="status"
URL="${DSPACEURL}/${ACTION}"

echo ${DSPACEURL}
echo ${URL}

curl -v --cookie "JSESSIONID=${JSESSIONID}" ${URL}
