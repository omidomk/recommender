#!/usr/bin/python
import requests
import json
  
def receive( number): 
    #first receive list of all users ids
    resp_get=requests.get("http://localhost/userfeedback", headers={"api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"})
   resps = resp_get.json()
    list=[]
    article=[]
    score=[]
    
    while i < len(resps["userfeedback"]):
      for key in resps["userfeedback"]:
        print "key: %s , value: %s" % (key, resps["userfeedback"][key])
        articlesdict=resps["userfeedback"][key]
        for key in articlesdict:
          article[i].apppend(key) 
          score[i].apppend(articlesdict[key])
        
        i += 1
        
        
    return;
