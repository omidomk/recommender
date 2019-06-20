"""
Toy Indexer
===========

Toy indexing example for testing purposes.

:Authors: Krisztian Balog, Faegheh Hasibi
"""
from elastic import Elastic
import scrapeMetadata

def main():
    index_name = "toy_index"

    mappings = {
        "title": Elastic.analyzed_field(),
        "description": Elastic.analyzed_field(),
        "id": Elastic.analyzed_field(),
        "categories": Elastic.analyzed_field(),
        "doi": Elastic.analyzed_field(),
        "comments": Elastic.analyzed_field(),
        "license": Elastic.analyzed_field(),
        "journal": Elastic.analyzed_field(),
        "authors": Elastic.analyzed_field(),
        "datestamp": Elastic.analyzed_field(),
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
    elastic = Elastic(index_name)
    elastic.create_index(mappings, force=True)
    elastic.add_docs_bulk(results)
    print("index has been built")



if __name__ == "__main__":
    main()
