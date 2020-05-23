#!/usr/bin/python3

import json
import requests
import sys
from settings import avwx_token

# Settings
baseUrl = "https://avwx.rest/api/metar/"
headers = {
  'Authorization': avwx_token
}
stationId = "ESOK"

# Function for getting METAR data
def getWx(location):
  url = baseUrl + location
  response = requests.get(url, headers=headers)
  return json.loads(response.text)


# Get system arguments
if (len(sys.argv) > 1):
  stationId = sys.argv[1]
else:
  stationId = input("Station ID: ")

parsed = getWx(stationId)

#print(json.dumps(parsed, indent=4))
print(parsed['raw'])