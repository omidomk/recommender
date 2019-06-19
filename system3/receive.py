#!/usr/bin/python
import requests
import json
  
def receive( number): 
    #first receive list of all users ids
    users_get=requests.get("http://localhost/users?from="+number, headers={"api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"})
    users = users_get.json()
    list=[]
    #users categories that concated
    queries={}
    users_last=[]
    user_last = []
    i=0
    while i < len(users["users"]["user_ids"]):
        users_last.append(users["users"]["user_ids"][i])
        i += 1
        
        #then get all users preferd categories
        user_get=requests.get("http://localhost/userinfo?user_id="+i, headers={"api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"})
        user = user_get.json()
        j=0
        while j < len(user["userinfo"][i]["categories"]):
          user_last.append(user["userinfo"][i]["categories"][j])
          j += 1
        list.append(user_last)
        s=', '
        userpref=s.join(user_last)
        queries.update({i:userpref})
        with open('queries.json','w') as file:
            file.write(json.dumps(queries))
    return list;
