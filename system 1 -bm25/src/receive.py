#!/usr/bin/python
import requests
import json
#first receive list of all users ids
users_get=requests.get("http://localhost/users?from=1000", headers={"api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"})
users = users_get.json()
while i < len(users["users"]["user_ids"]):
    users_last.append(users["users"]["user_ids"][i])
    i += 1
    #then get all users preferd categories
    user_get=requests.get("http://localhost/userinfo?user_id="+i, headers={"api_key": "355b36dc-7863-4c4a-a088-b3c5e297f04f"})
    user = user_get.json()
    while j < len(user["userinfo"][i]["categories"]):
      user_last.append(user["userinfo"][i]["categories"][j])
      j += 1
