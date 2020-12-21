import urllib.request
# https://stackoverflow.com/questions/30755625/urlerror-with-sparqlwrapper-at-sparql-query-convert
# #if the arg is empty in ProxyHandler, urllib will find itself your proxy config.
# proxy_support = urllib.request.ProxyHandler({})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

from contract_models import Artist
from contract_models.song import SongModel

K_POP_QUERY = """
SELECT ?song ?songLabel 
(GROUP_CONCAT(DISTINCT ?performerlabel; SEPARATOR=", ") AS ?performers) 
(GROUP_CONCAT(DISTINCT ?track;SEPARATOR=", ") AS ?sttracks) 
(GROUP_CONCAT(DISTINCT ?gsid;SEPARATOR=", ") AS ?gsids)
(GROUP_CONCAT(DISTINCT ?video;SEPARATOR=", ") AS ?ytVideoIds)
{ ?performer p:P136 [ps:P136 wd:Q213665];
             rdfs:label ?performerlabel. 
  ?song p:P175 [ps:P175 ?performer];
        p:P31 [ps:P31 ?in].
#   ?in p:P279 [ps:P279 wd:Q2188189].
  
  FILTER( LANG(?performerlabel) = "en")
  OPTIONAL { ?song p:P31 [ps:P31 wd:Q134556]. }
  FILTER (?in in (wd:Q7366, wd:Q134556))
   OPTIONAL { ?song p:P1651 [ps:P1651 ?video]. }
 OPTIONAL { ?song p:P2207 [ps:P2207 ?track]. }
 OPTIONAL { ?song p:P6218 [ps:P6218 ?gsid]. }
   SERVICE wikibase:label { bd:serviceParam wikibase:language "en".}        
}
GROUP BY ?song ?songLabel
ORDER BY ?performers
"""


class WikiDataQueryBuilder:
    def __init__(self):
        self.sparql_builder = SPARQLWrapper("https://query.wikidata.org/sparql",
                                            agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

    def raw_query(self, fields: List[str], raw: str):
        self.sparql_builder.setQuery(raw)
        self.sparql_builder.setReturnFormat(JSON)
        results = self.sparql_builder.query().convert()
        results_df = pd.json_normalize(results['results']['bindings'])
        results_df = results_df[[f'{field}.value' for field in fields]]
        return results_df

    def query(self, fields: List[str], where: str, limit: int = None) -> pd.DataFrame:
        # From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
        fields_p = " ".join([f'?{field}' for field in fields])
        query = f"""
           SELECT {fields_p}
           WHERE
           {{
             {where}
           }}
           """
        self.sparql_builder.setQuery(query)
        if limit:
            query += f"""
            LIMIT {limit}
            """
        self.sparql_builder.setReturnFormat(JSON)
        results = self.sparql_builder.query().convert()

        results_df = pd.json_normalize(results['results']['bindings'])
        results_df[[f'{field}.value' for field in fields]].head()
        return results_df


builder = WikiDataQueryBuilder()


def get_artist_akas(name: str, lang: str = 'en') -> List[str]:
    if not name:
        raise ValueError("Cannot be empty")
    df = builder.query(['altLabel'], where=f"""
             {{select DISTINCT ?artist where {{
          ?artist skos:altLabel ?exactLabel;
                  p:P4208 ?billboardStruct.
             FILTER ( regex(?exactLabel, '^{name}$', 'i') )
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en".}}    
          }}
              }}
    {{
     ?artist p:P4208 ?billboardStruct;
                p:P136 ?genre;
                skos:altLabel ?altLabel.
        ?billboardStruct ps:P4208 ?artistID.
    }}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en".}}  """)
    df = df[df["altLabel.xml:lang"].str.contains(lang)]
    return df['altLabel.value'].drop_duplicates().tolist()


def get_kpop_songs() -> pd.DataFrame:
    df = builder.raw_query(['ytVideoIds', 'songLabel', 'performers'], K_POP_QUERY)
    df = df.rename(columns={"songLabel.value": "song_title",
                       "performers.value": "performers",
                       "ytVideoIds.value": "video_id"})
    return df


all_song_query = """
SELECT ?song ?songLabel 
(GROUP_CONCAT(DISTINCT ?performerlabel; SEPARATOR=", ") AS ?performers) 
(GROUP_CONCAT(DISTINCT ?track;SEPARATOR=", ") AS ?sttracks) 
(GROUP_CONCAT(DISTINCT ?gsid;SEPARATOR=", ") AS ?gsids)
(GROUP_CONCAT(DISTINCT ?video;SEPARATOR=", ") AS ?ytVideoIds)
{ ?performer p:P136 [ps:P136 wd:Q37073];
             p:P1412 [ps:P1412 wd:Q1860];
             rdfs:label ?performerlabel. 
  ?song p:P175 [ps:P175 ?performer];
        p:P31 [ps:P31 ?in].
 ?in p:P279 [ps:P279 wd:Q2188189].
  
  FILTER( LANG(?performerlabel) = "en")
  OPTIONAL { ?song p:P31 [ps:P31 wd:Q134556]. }
  FILTER (?in in (wd:Q7366, wd:Q134556))
   OPTIONAL { ?song p:P1651 [ps:P1651 ?video]. }
 OPTIONAL { ?song p:P2207 [ps:P2207 ?track]. }
 OPTIONAL { ?song p:P6218 [ps:P6218 ?gsid]. }
   SERVICE wikibase:label { bd:serviceParam wikibase:language "en,[AUTO_LANGUAGE]".}        
}
GROUP BY ?song ?songLabel
ORDER BY RAND()
"""

song_query_v1 = """
SELECT ?song ?songLabel 
(GROUP_CONCAT(DISTINCT ?performerlabel; SEPARATOR=", ") AS ?performers) 
(GROUP_CONCAT(DISTINCT ?track;SEPARATOR=", ") AS ?sttracks) 
(GROUP_CONCAT(DISTINCT ?gsid;SEPARATOR=", ") AS ?gsids)
(GROUP_CONCAT(DISTINCT ?video;SEPARATOR=",") AS ?ytVideoIds)
{{ ?performer p:P136 [ps:P136 wd:Q37073];
             rdfs:label ?performerlabel. 
  ?song p:P175 [ps:P175 ?performer];
        rdfs:label ?song2Label;
        p:P31 [ps:P31 ?in].

  FILTER( LANG(?performerlabel) = "en")
  OPTIONAL {{ ?song p:P31 [ps:P31 wd:Q134556]. }}
  FILTER (?in in (wd:Q7366, wd:Q134556))
  FILTER (STR(?song2Label) = '{title}')
  FILTER (STR(?performerlabel) = '{performer}')

   OPTIONAL {{ ?song p:P1651 [ps:P1651 ?video]. }}
 OPTIONAL {{ ?song p:P2207 [ps:P2207 ?track]. }}
 OPTIONAL {{ ?song p:P6218 [ps:P6218 ?gsid]. }}
   SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,[AUTO_LANGUAGE]".}}        
}}
GROUP BY ?song ?songLabel
LIMIT 5000
"""

song_query = """
SELECT ?song ?songLabel 
(GROUP_CONCAT(DISTINCT ?performerlabel; SEPARATOR=",") AS ?performers) 
(GROUP_CONCAT(DISTINCT ?track;SEPARATOR=",") AS ?sttracks) 
(GROUP_CONCAT(DISTINCT ?gsid;SEPARATOR=",") AS ?gsids)
(GROUP_CONCAT(DISTINCT ?video;SEPARATOR=",") AS ?ytVideoIds)
(GROUP_CONCAT(DISTINCT ?genreLabel;SEPARATOR=",") AS ?genres)
{ ?performer rdfs:label ?performerlabel. 
  ?song p:P175 [ps:P175 ?performer];
        p:P31 [ps:P31 ?in];
        p:P136 [ps:P136 [rdfs:label ?genre]];
        p:P407|p:P [ps:P407 wd:Q1860].
 ?in p:P279 [ps:P279 wd:Q2188189].
  
  FILTER( LANG(?performerlabel) = "en")
  OPTIONAL { ?song p:P31 [ps:P31 wd:Q134556]. }
  FILTER (?in in (wd:Q7366, wd:Q134556))
OPTIONAL { ?song p:P1651 [ps:P1651 ?video]. }
 OPTIONAL { ?song p:P2207 [ps:P2207 ?track]. }
 OPTIONAL { ?song p:P6218 [ps:P6218 ?gsid]. }
   SERVICE wikibase:label { bd:serviceParam wikibase:language "en,[AUTO_LANGUAGE]".}        
}
GROUP BY ?song ?songLabel
ORDER BY ?ytVideoIds
"""

song_id_query = """
SELECT ?songLabel
(GROUP_CONCAT(DISTINCT ?performerLabel; SEPARATOR=",") AS ?performers) 
(GROUP_CONCAT(DISTINCT ?trackLabel;SEPARATOR=",") AS ?sttracks) 
(GROUP_CONCAT(DISTINCT ?video;SEPARATOR=",") AS ?ytVideoIds)
(GROUP_CONCAT(DISTINCT ?genreLabel;SEPARATOR=",") AS ?genres)
{{ wd:{wikidata_id} p:P175 [ps:P175 ?performer];
               p:P136 [ps:P136 ?genre].

 # FILTER( LANG(?performerLabel) = "en")
 OPTIONAL {{ wd:{wikidata_id} p:P1651 [ps:P1651 ?video]. }}
 OPTIONAL {{ wd:{wikidata_id} p:P2207 [ps:P2207 ?track]. }}
 SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en".
                          wd:{wikidata_id} rdfs:label ?songLabel.
                          ?performer rdfs:label ?performerLabel.
                          ?track rdfs:label ?trackLabel.
                          ?genre rdfs:label ?genreLabel
 }}
}}
"""

# TODO: Strategy pattern


def retrieve_song_model_from_wikidata_id(wikidata_id: str) -> SongModel:
    df = builder.raw_query(['songLabel', 'performers', 'ytVideoIds', 'genres'],
                           song_id_query.format(wikidata_id=wikidata_id))
    # raise ValueError("Song Id Not found")
    row = df.iloc[0]
    title = row['songLabel.value']
    performers = row['performers.value'].split(',')
    youtube_id = row['ytVideoIds.value'].split(',')
    genres = row['genres.value'].split(',')

    return SongModel(name=title, _artist_names=performers,
                     youtube_ids=youtube_id,
                     genres=genres)


def retrieve_songmodel_wikidata(song_title: str, artists: List[str]) -> SongModel:
    """

    Args:
        song_title:
        artists: A list of artist's names

    Returns:
        The wikidata id of a given song
    """
    df = builder.raw_query(['song', 'ytVideoIds'], song_query.format(title=song_title, performer=artists[0]))
    # raise ValueError("Song Id Not found")
    wikidata_id = df['song.value'][0].replace('http://www.wikidata.org/entity/', '')
    youtube_id = df['ytVideoIds.value'][0]
    return SongModel(wikidata_id=wikidata_id, youtube_ids=youtube_id)


def retrieve_english_songs() -> List[SongModel]:
    df = builder.raw_query(['song', 'songLabel', 'performers', 'ytVideoIds'], all_song_query)
    s_list = []
    print(df.to_csv(index=False))
    for index, row in df.iterrows():
        wid = row['song.value'].replace('http://www.wikidata.org/entity/', '')
        s = SongModel(wikidata_id=wid,
                      youtube_ids=row['ytVideoIds.value'].split(","),
                      name=row['songLabel.value'],
                      _artist_names=row['performers.value'])
        s.add_artists_from_names(row['performers.value'].split(","))
        s_list.append(s)
    return s_list


def main():
    print(get_kpop_songs().to_dict('records'))


if __name__ == '__main__':
    main()
