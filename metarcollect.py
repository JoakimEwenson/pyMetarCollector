#!/usr/bin/python3

import requests
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil import parser

class MetarPost:
    raw_text = ""
    station_id = ""
    observation_time = ""
    latitude = ""
    longitude = ""
    temp_c = ""
    dewpoint_c = ""
    wind_dir_degrees = ""
    wind_speed_kt = ""
    visibility_statute_mi = ""
    altim_in_hg = ""
    qnh = ""
    sky_condition = []
    flight_category = ""
    metar_type = ""
    elevation_m = ""

# Get system arguments
if (len(sys.argv) > 1):
    stationId = sys.argv[1]
else:
    stationId = "ESOK"

print("\n--------------------------------/--------------------------------\n")

# Collect data from API and return JSON string
def getMetarData(stationId):
    # Set up url and query string
    APIURL = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?"
    APIPARAMS = "dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=2&mostRecent=false&stationString=" + stationId

    response = requests.request("GET", APIURL + APIPARAMS)
    return response.text

tree = ET.fromstring(getMetarData(stationId))
data = tree.find('data')

for metar in data.iter('METAR'):
    # Create a new metar object
    metarPost = MetarPost()
    metarPost.sky_condition = []

    # Iterate results and insert to metar object
    for child in metar.findall('raw_text'):
        metarPost.raw_text = child.text
    for child in metar.findall('station_id'):
        metarPost.station_id = child.text
    for child in metar.findall('observation_time'):
        metarPost.observation_time = parser.isoparse(child.text)
    for child in metar.findall('latitude'):
        metarPost.latitude = child.text
    for child in metar.findall('longitude'):
        metarPost.longitude = child.text
    for child in metar.findall('temp_c'):
        metarPost.temp_c = int(float(child.text))
    for child in metar.findall('dewpoint_c'):
        metarPost.dewpoint_c = int(float(child.text))
    for child in metar.findall('wind_dir_degrees'):
        metarPost.wind_dir_degrees = child.text
    for child in metar.findall('wind_speed_kt'):
        metarPost.wind_speed_kt = child.text
    for child in metar.findall('visibility_statute_mi'):
        metarPost.visibility_statute_mi = float(child.text)
    for child in metar.findall('altim_in_hg'):
        metarPost.altim_in_hg = float(child.text)
        metarPost.qnh = round(float(child.text) / 0.029529983095997)
    for child in metar.findall('sky_condition'):
        metarPost.sky_condition.append(child.attrib)
    for child in metar.findall('flight_category'):
        metarPost.flight_category = child.text
    for child in metar.findall('metar_type'):
        metarPost.metar_type = child.text
    for child in metar.findall('elevation_m'):
        metarPost.elevation_m = float(child.text)

    # Print data
    print(metarPost.raw_text)
    print()
    print("{0} on {1}".format(metarPost.station_id, datetime.strftime(metarPost.observation_time,'%Y-%m-%d %H:%M')))
    print("wind {0}/{1} kt".format(metarPost.wind_dir_degrees, metarPost.wind_speed_kt))
    print("temp {0}, dewpoint {1}".format(metarPost.temp_c, metarPost.dewpoint_c))
    print("altimeter {0:0.2f}, qnh {1}".format(metarPost.altim_in_hg, metarPost.qnh))
    if(len(metarPost.sky_condition) > 0):
        for clouds in metarPost.sky_condition:
            if (clouds['sky_cover'] in ("CAVOK", "SKC", "CLR", "OVX")):
                print(clouds['sky_cover'])
            elif (clouds['sky_cover'] in ("FEW", "SCT", "BKN", "OVC")):
                print("clouds {0} at {1} ft".format(clouds['sky_cover'], clouds['cloud_base_ft_agl']))
            else:
                print("no cloud data")

    print("\n--------------------------------\\--------------------------------\n")
