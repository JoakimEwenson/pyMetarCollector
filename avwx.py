#!/usr/bin/python3

import json
import requests

token = "Wa7VJ_CJ0LTjGgPfxu6M2S7KSQ9kQoo-FwQ8EEBOkSw"
url = "https://avwx.rest/api/metar/ESSA"

headers = {
  'Authorization': token
}

response = requests.get(url, headers=headers)

parsed = json.loads(response.text)

print(json.dumps(parsed, indent=4))