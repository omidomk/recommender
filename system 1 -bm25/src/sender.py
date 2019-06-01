#!/usr/bin/python
import requests

# Data needs to be replaced by article data!!!!!!!
data = {
    'data1':'something', 
    'data2':'otherthing'
}

# Custom headers
headers = {
    'content-type': 'multipart/form-data'
}

# Get response from server   needs to be replaced by online server but i dont have api key!!!!
response = requests.post('http://localhost/', data=data, headers=headers)

# If you care about the response
print(response.json())
