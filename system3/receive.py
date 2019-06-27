#!/usr/bin/python
import requests
import json
  
def receive(): 
    #first receive list of all users ids
    users_get=requests.get("http://127.0.0.1:8000/users", headers={"api_key": "01fd7362-28fc-4538-a1cf-50b650219ea1"})
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
        user_get=requests.get("http://127.0.0.1:8000/userinfo?user_id="+str(i), headers={"api_key": "01fd7362-28fc-4538-a1cf-50b650219ea1"})
        user = user_get.json()
        j=0
        user_last.clear()
        while j < len(user["userinfo"][str(i)]["keywords"]):
            
            user_last.append(user["userinfo"][str(i)]["keywords"][j])
            j += 1
        list.append(user_last)
        s=', '
        userpref=s.join(user_last)
        queries.update({i:userpref})
        with open('queries.json','w') as file:
            file.write(json.dumps(queries))
    return list;
receive()
