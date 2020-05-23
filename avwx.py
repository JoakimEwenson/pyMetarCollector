#!/usr/bin/python3

import json
import requests
from settings import token

url = "https://avwx.rest/api/metar/ESSA"

headers = {
  'Authorization': token
}

response = requests.get(url, headers=headers)

parsed = json.loads(response.text)

print(json.dumps(parsed, indent=4))