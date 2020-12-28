# Song Lyrics & Popularity (SLAP) API

**Overview**  
This API service gathers and joins song lyrics and popularity.
The main use is to play an instance of Game of Song Association by Elle,
but it can also be used answer questions about the correlation between
some lyrical properties like repetition or memorability of words with popularity.

The main data sources include:
- Spotify
- YouTube
- Wikidata
- Genius

Components include:
- API server
- Client app to visualize data

## Requirements

Django API Server

- Python 3.6+
- Python packages per [requirements.txt](requirements.txt)

Vue application
 
- Node
- npm or yarn

OpenAPI client

- What ever you can use to run openapi generator cli  
  (Below we use Java but anything goes.)

## Quick Start for devs

### Generating a client API

1\. Clone this repo

```sh
git clone https://github.com/KooCook/slap.git
```

2\. Use [openapi generator cli](https://openapi-generator.tech/docs/installation)
    to generate a flask client

```sh
java -jar path/to/openapi-generator-cli-4.3.1.jar generate -i openapi/slap-api.yaml -o autogen -g python-flask
```

### Running the development API server

1\. Install python requirements. (We recommend using virtual environments)

```sh
python -m pip install -r requirements.txt
```

2\. Make Django migrations (go to [`slap_dj/`](slap_dj))

```sh
python manage.py makemigrations
```

3\. Create the database

```sh
python manage.py migrate
```

4\. Populate the database*

```sh
python manage.py populate_data ... # TODO: mode
```

*manually do it for now (see [#data-population](#data-population))

5\. Start the Django API server

```sh
python manage.py runserver
```

### Running the development Vue app to visualize data

See [slap-vue/README.md](slap-vue/README.md)

## Data population

For app v1

```sh
python manage.py populate_data <mode here, see help message -h>
```

For app v2

Call these methods in succession

```
models.wikidata.populate_wikidata_english_songs()
models.wikidata.WikidataSong.retrieve_all_info_from_id()
models.base.Song.link_to_genius() # do this for all songs
models.base.Song.update_compression_ratio() # do this for all songs
```

## Deployment 

## Quickstart with Docker Compose

1.\

```shell
docker-compose up -d
```
