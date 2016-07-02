#!/bin/bash

RQST='
{"metadata":[
    {
      "key": "dc.contributor.author",
      "value": "Luxemburg, Rosa"
    },
    {
      "key": "dc.description",
      "language": "es_ES",
      "value": "De una manera concreta los debates fundamentales que habían llenado la actividad de la socialdemocracia rusa du- rante años y en la que destacados dirigentes del partido alemán habían participado, se habían resuelto en los acontecimientos revolucionarios."
    },
    {
      "key": "dc.description.abstract",
      "language": "es_ES",
      "value": "Tomando como punto de partida las enseñanzas de la revolución rusa de 1905, Rosa Luxemburgo crítica la política de la dirección de los sindicatos y esboza las lecciones gigantescas que para la lucha por el socialismo entraña esta experiencia: Por primera vez en la historia de la lucha de clases [la revolución rusa] ha hecho posible la grandiosa realización de la idea de la huelga de masas y—como explicaremos más adelante—hasta de la huelga general inaugurando una nueva época en el desarrollo del movimiento obrero"
    },
    {
      "key": "dc.title",
      "language": "es_ES",
      "value": "Huelga de masas partido y sindicatos"
    },
    {
      "key": "dc.subject",
      "language": "en_US",
      "value": "January Term"
    }
]}
'

DSPACEURL="https://dspace.carthage.edu/rest"
TOKEN=""
VERB="POST"
REQUEST_TYPE="json"
# mathematics jterm 2016 collection
ACTION="collections/196/items"
EARL="${DSPACEURL}/${ACTION}"
echo ${EARL}

curl -i -k -4 \
    -H "rest-dspace-token: ${TOKEN}" \
    -H "accept: application/${REQUEST_TYPE}" \
    -H "Content-Type: application/${REQUEST_TYPE}" \
    -X ${VERB} ${EARL} \
    -d "${RQST}"

# returns
# {"id":970,"name":"Huelga de masas partido y sindicatos","handle":"123456789/1084","type":"item","link":"/RESTapi/items/970","expand":["metadata","parentCollection","parentCollectionList","parentCommunityList","bitstreams","all"],"lastModified":"2016-05-13 10:27:11.81","parentCollection":null,"parentCollectionList":null,"parentCommunityList":null,"bitstreams":null,"archived":"true","withdrawn":"false"}
