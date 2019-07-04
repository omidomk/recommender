#!/usr/bin/python
"""
Send recommendations to ArxivDigest
===========

:Author: Omid Mohammadi Kia
"""
import requests
import json
import retrieval
from typing import Any


def send():  
    #after retrieving articles from elastic we send it to arxivdigest
    
    # Data needs to be replaced by article data!!!!!!!
    #get data from bm25
    #results={}  # type: Any
    #results["recommendations"][userid].append({"article_id": doc_id, "score": str(score["score"])})

    """"
    example = {
        "recommendations": {user_id: [
            {"article_id": "1107.2529", "score": 2},
            {"article_id": "1308.1196", "score": 3},
            {"article_id": "1312.5699", "score": 2}
        ],
        2: [
            {"article_id": "1308.1196", "score": 10},
            {"article_id": "1506.07383", "score": 6}
     ]
    }
    }
    """

    # Custom headers  
    #invalid api key!!!!!!

    headers = {
        "Content-Type": "application/json","api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"
    }
    r=retrieval.main()

    # Get response from server   needs to be replaced by online server but i dont have api key!!!!
    response = requests.post('http://localhost/', data=json.dumps(r), headers=headers)

    # If you care about the response
    print(response.json())
 
    return;
if __name__ == "__main__":
    send()
