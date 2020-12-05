import urllib.request
# https://stackoverflow.com/questions/30755625/urlerror-with-sparqlwrapper-at-sparql-query-convert
# #if the arg is empty in ProxyHandler, urllib will find itself your proxy config.
# proxy_support = urllib.request.ProxyHandler({})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)
from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd


class WikiDataQueryBuilder:
    def __init__(self):
        self.sparql_builder = SPARQLWrapper("https://query.wikidata.org/sparql",
                                            agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")

    def query(self, fields: List[str], where: str) -> pd.DataFrame:
        # From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
        fields_p = " ".join([f'?{field}' for field in fields])
        self.sparql_builder.setQuery(f"""
           SELECT {fields_p}
           WHERE
           {{
             {where}
           }}
           """)
        self.sparql_builder.setReturnFormat(JSON)
        results = self.sparql_builder.query().convert()

        results_df = pd.io.json.json_normalize(results['results']['bindings'])
        results_df[['item.value', 'itemLabel.value']].head()
        return results_df


def main():
    builder = WikiDataQueryBuilder()
    print(builder.query(['itemLabel', 'item'], where="""
      ?item wdt:P31 wd:Q146 .
               SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    """))


if __name__ == '__main__':
    main()
