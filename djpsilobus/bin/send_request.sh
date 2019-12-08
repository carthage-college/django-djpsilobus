#!/bin/bash

if [ $# != 5 ]; then
  echo -e "ERRO! Wrong number parameter!"
  echo -e "USE:"
  echo -e "${0} <DSPACEURL> <TOKEN> <REQUEST_DECRIPTOR_FILE> <REQUEST_TYPE [\"json\"/\"xml\"]> <DSPACE_VERSION: [4,5,6]>"
  exit 1
fi

DSPACEURL=${1}
TOKEN=${2}
REQUEST=${3}
REQUEST_TYPE=${4}
DSPACE_VERSION=${5}

if [ -e ${REQUEST} ]; then
  source $REQUEST
else
  echo "ERROR! Request descriptor file not found!"
  exit 1
fi

case ${REQUEST_TYPE} in
  "json") RQST=${RQST_JSON} ;;
  "xml") RQST=${RQST_XML} ;;
  *) echo -e "ERROR! TYPE MUST BE: \"json\" OR \"xml\"."; exit 1 ;;
esac

if [[ ${DSPACE_VERSION} == 6 ]]; then
  AUTH="--cookie \"${TOKEN}\""
else
  AUTH="-H \"rest-dspace-token: ${TOKEN}\""
fi

echo -e "curl -k -4 --silent\
  ${AUTH} \
  -H \"accept: application/${REQUEST_TYPE}\" \
    -H \"Content-Type: application/${REQUEST_TYPE}\" \
    -X ${VERB} \"${DSPACEURL}/${ACTION}\" \
    -d \"${RQST}\""

curl -k -4 --silent\
  ${AUTH} \
  -H "accept: application/${REQUEST_TYPE}" \
    -H "Content-Type: application/${REQUEST_TYPE}" \
    -X ${VERB} "${DSPACEURL}/${ACTION}" \
    -d "${RQST}"

echo ""
