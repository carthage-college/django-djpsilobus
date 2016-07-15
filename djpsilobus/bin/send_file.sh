#!/bin/bash

DSPACEURL="https://dspace.carthage.edu/rest"
FILE="/data2/www/data/Resistencia_ENERO_MARZO_baja.pdf"
VERB="POST"
TOKEN=""
ACTION="items/1049/bitstreams/?name=Resistencia_ENERO_MARZO_baja.pdf"
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

# response
#{"id":4187,"name":"Resistencia_ENERO_MARZO_baja.pdf","handle":null,"type":"bitstream","link":"/RESTapi/bitstreams/4187","expand":["parent","policies","all"],"bundleName":"ORIGINAL","description":null,"format":"Adobe PDF","mimeType":"application/pdf","sizeBytes":551479,"parentObject":null,"retrieveLink":"/bitstreams/4187/retrieve","checkSum":{"value":"9670d137be9a5810f42e40aabef1f0d6","checkSumAlgorithm":"MD5"},"sequenceId":-1,"policies":null}
