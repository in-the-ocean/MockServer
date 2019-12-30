import requests

requests.post('http://127.0.0.1:5000/api/ranklists',
                        data = {'name':'added00'})
response = requests.get('http://127.0.0.1:5000/api/ranklists?name=added00')

json_response = response.json()
print(json_response)
