#!/bin/bash
java -jar autogen/openapi-generator-cli-4.3.1.jar generate \
-i "openapi/slap-api.yaml" --additional-properties=projectName=slap-client,packageName=slap_client \
-o slap-client-python -g python
cd slap-client-python || exit
pip3 install -r requirements.txt
