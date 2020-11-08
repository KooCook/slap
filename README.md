# Song Lyrics & Popularity (SLAP) API

Main repo for Song Lyrics & Popularity (SLAP) API. 
Used as a 2 week project for DAQ.

## Requirements

- Python 3.6+
- What ever you can use to run openapi generator cli  
  (Below we use Java but anything goes.)

## Quick Start

1\. Clone this repo

```sh
git clone https://github.com/KooCook/slap.git
```

2\. Use [openapi generator cli](https://openapi-generator.tech/docs/installation)
    to generate a flask client

```sh
java -jar openapi/openapi-generator-cli-4.3.1.jar generate -i openapi/slap-api.yaml -o autogen -g python-flask
```

3\. Install python requirements. (We recommend using virtual environemnts)

```sh
python -m pip install -r requirements.txt
```

4\. Start the server

```sh
python app,py
```
