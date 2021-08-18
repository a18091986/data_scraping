import json
import requests
service = 'https://api.vk.com/method/groups.get?v=5.52&access_token=64bf11db321a76b881c45a70863d376f2748fff20f56fd99f2db8166138387eb8648ab8f61135a993bf3c'
req = requests.get(service)
data = json.loads(req.text)
with open('groups.json', 'w') as f:
     json.dump(data['response']['items'],f)