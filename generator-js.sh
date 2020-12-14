#!/bin/bash
java -jar autogen/openapi-generator-cli-4.3.1.jar generate \
-i "openapi/slap-api.yaml" --additional-properties=projectName=slap-client \
-o slap-client -g javascript
cd slap-client || exit
#npm install
#npm run build
cd ..
cp -rf slap-client slap-vue/src/modules
rm -r slap-client
