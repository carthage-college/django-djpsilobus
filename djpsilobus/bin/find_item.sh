#!/bin/bash

#"value": "2019_RC_CSC_1820_02_Kivolowitz_Perry_syllabus.pdf?",
RQST='
{
    "key": "dc.title.alternative",
    "value": "2017_RC_CSC_1110_02_Wheeler_Erlan_syllabus.pdf",
    "language": "en"
}
'

#DSPACEURL="https://dspace.carthage.edu/rest"
DSPACEURL="https://carthage.upgrade.dspace-express.com/rest"
TOKEN=""
VERB="POST"
REQUEST_TYPE="json"
ACTION="items/find-by-metadata-field"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}


curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "accept: application/${REQUEST_TYPE}" \
    -H "Content-Type: application/${REQUEST_TYPE}" \
    -X ${VERB} ${EARL} \
    -d "${RQST}"
