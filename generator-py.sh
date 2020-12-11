#!/bin/bash
java -jar autogen/openapi-generator-cli-4.3.1.jar generate \
-i "openapi/slap-api.yaml" --additional-properties=projectName=slap-client \
-o slap-client-python -g python
