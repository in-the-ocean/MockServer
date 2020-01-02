import requests

#requests.put('http://127.0.0.1:5000/api/ranklists',
 #                      data = {'name':'add00'})
requests.put('http://127.0.0.1:5000/api/ranklists/100/candidates',
                       data = {'name':'addcan00','uid':'27'})
response = requests.get('http://127.0.0.1:5000/api/ranklists?name=added00')

json_response = response.json()
print(json_response)
