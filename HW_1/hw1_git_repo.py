import json
import requests
service = 'https://api.github.com/users/a18091986/repos'
req = requests.get(service)
data = json.loads(req.text)
with open('repos.json', 'w') as f:
    json.dump(data,f)