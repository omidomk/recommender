"""
Toy Indexer
===========

Toy indexing example for testing purposes.

:Authors: Krisztian Balog, Faegheh Hasibi
"""
from elastic import Elastic
import scrapeMetadata
import json
from elasticsearch import Elasticsearch
from config import ELASTIC_HOSTS, ELASTIC_SETTINGS

def main():
    index_name = "arxiv"

    mappings = {
        #Elastic.FIELD_CATCHALL: Elastic.analyzed_field(),
        "title": Elastic.analyzed_field(),
        "description": Elastic.analyzed_field(),
        "id": Elastic.notanalyzed_searchable_field(),
        "categories": Elastic.analyzed_field(),
        "doi": Elastic.notanalyzed_searchable_field(),
        "comments": Elastic.analyzed_field(),
        "license": Elastic.notanalyzed_searchable_field(),
        "journal": Elastic.analyzed_field(),
        "authors": Elastic.analyzed_field(),
        "datestamp": Elastic.notanalyzed_searchable_field(),
    }






    example = {
        1: {"title": "Rap God",
            "content": "gonna, gonna, Look, I was gonna go easy on you and not to hurt your feelings"
            },
        2: {"title": "Lose Yourself",
            "content": "Yo, if you could just, for one minute Or one split second in time, forget everything Everything that bothers you, or your problems Everything, and follow me"
            },
        3: {"title": "Love The Way You Lie",
            "content": "Just gonna stand there and watch me burn But that's alright, because I like the way it hurts"
            },
        4: {"title": "The Monster",
            "content": ["gonna gonna I'm friends with the monster", "That's under my bed Get along with the voices inside of my head"]
            },
        5: {"title": "Beautiful",
            "content": "Lately I've been hard to reach I've been too long on my own Everybody has a private world Where they can be alone"
            }
    }
    results = scrapeMetadata.harvestMetadataRss()
    with open('articles.json', 'w') as file:
        file.write(json.dumps(results))

    elastic = Elastic(index_name)
    es=Elasticsearch(hosts=ELASTIC_HOSTS)
    if (es.indices.exists(index_name)):
        elastic.create_index(mappings)
        elastic.add_docs_bulk(results)
        print("new index created")
    else:
        elastic.add_docs_bulk(results)
        print(" index updated")
    print("index has been built")



if __name__ == "__main__":
    main()
