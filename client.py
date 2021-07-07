import requests
import json

datajson = json.loads(open("./data.txt", "r").read())


rq = requests.post("http://127.0.0.1:5000/question", json=datajson)

print(json.dumps(rq.json(), indent=4))
