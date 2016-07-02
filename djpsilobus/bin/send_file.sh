#!/bin/bash

DSPACEURL="https://dspace.carthage.edu/rest"
TOKEN=""
FILE="/d2/www/dspace/Rosa_Luxemburg_Huelga_masas_23.pdf"
VERB="POST"
REQUEST_TYPE="json"
ACTION="items/970/bitstreams/"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}

#curl -k -4 --silent\
#-H "Content-Type: application/${REQUEST_TYPE}" \
#-H "accept: application/${REQUEST_TYPE}" \
curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "accept: application/pdf" \
    -H "Content-Type: multipart/form-data" \
    -X ${VERB} ${EARL} \
    -F upload=@"${FILE}"

# response
# {"id":3909,"name":null,"handle":null,"type":"bitstream","link":"/RESTapi/bitstreams/3909","expand":["parent","policies","all"],"bundleName":"ORIGINAL","description":null,"format":"Unknown","mimeType":"application/octet-stream","sizeBytes":551495,"parentObject":null,"retrieveLink":"/bitstreams/3909/retrieve","checkSum":{"value":"a07802806005e391d6d403987123ed31","checkSumAlgorithm":"MD5"},"sequenceId":-1,"policies":null}
