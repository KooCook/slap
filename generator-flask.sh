#!/bin/bash
java -jar autogen/openapi-generator-cli-4.3.1.jar generate \
-i "openapi/slap-api-server.yaml" --additional-properties=projectName=slap_flask_api \
-o autogen -g python-flask
cd autogen || exit
pip install -r requirements.txt
