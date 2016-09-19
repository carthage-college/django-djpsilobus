#!/bin/bash

DSPACEURL="https://dspace.carthage.edu/rest"
FILE="/data2/www/Rosa_Luxemburg_Huelga_masas_23.pdf"
VERB="POST"
TOKEN=""
ACTION="items/1279/bitstreams/?name=Rosa_Luxemburg_Huelga_masas_23.pdf"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}


#   -F file=@"${FILE}" \
#   -F name="${FILE}"
curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "Content-Type: multipart/form-data" \
    -H "accept: application/json" \
    -X ${VERB} ${EARL} \
    -F upload=@"${FILE}"

