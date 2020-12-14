FROM openjdk:8 as specs-module-generation-stage
RUN apt-get update
RUN apt install -y npm
WORKDIR /app/openapi
RUN npm install @openapitools/openapi-generator-cli -g
COPY ./slap-api.yaml slap-api.yaml
RUN npx @openapitools/openapi-generator-cli generate \
-i "slap-api.yaml" --additional-properties=projectName=slap-client \
-o slap-client -g javascript
RUN mkdir -p /app/src/modules
RUN cp -rf slap-client /app/src/modules
RUN rm -r slap-client

FROM node:latest as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY --from=specs-module-generation-stage /app/src/modules /app/src/modules
RUN [ -d "/app/src/modules/slap-client" ] && echo "Directory /app/src/modules/slap-client exists."
COPY ./ .
RUN npm run build

FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
