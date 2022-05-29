# NOTIFIER
# May 28th, 2022

import requests
import json
import re
import sqlite3
import ctypes
from pathlib import Path
from table import table

rootPath = str(Path(__file__).resolve()).replace("\\","/").rsplit("/", 1)[0]

def stockTrack(item : str, country : str, location : str) ->  None:
    
    country = country.lower() # normalize country code

    # import country codes and locations
    query = "SELECT id, name FROM locations WHERE country=?"
    con = sqlite3.connect(rootPath+'/data.db')
    cur = con.cursor()
    cur.execute(query, (country,))
    rows = cur.fetchall()
    storeCodes = {}
    for row in rows:
        storeCodes[row[0]] = row[1]

    # if item is not a sku code, clean .'s and parse from url
    if len(item) > 8:
        item = item.replace(".", "")
        idPattern = re.compile(r"[0-9]{8}")
        item = re.findall(idPattern, item)[0]
    
    url = f"https://api.ingka.ikea.com/cia/availabilities/ru/{country}?itemNos={item}&expand=StoresList,Restocks,SalesLocations"
    headers = {
        "authority": "api.ingka.ikea.com",
        "method": "GET",
        "path": f"/cia/availabilities/ru/ca?itemNos={item}&expand=StoresList,Restocks,SalesLocations",
        "scheme": "https",
        "accept": "application/json;version=2",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.ikea.com",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-client-id": "b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.content)

    availabilities = data["availabilities"]

    location = location.replace(" ", "").split(",")

    message = ""
    for store in availabilities:
        # Identify store
        storeCode = store["classUnitKey"]["classUnitCode"]

        if not storeCode in location:
            continue

        storeName = storeCodes[storeCode]
        carrying = store["buyingOption"]["cashCarry"]

        if not "availability" in carrying:
            continue

        # Identify current availability
        availStats = carrying["availability"]
        quantAvail = availStats["quantity"]
        availInstore = store["availableForCashCarry"]
        availOnline = store["availableForClickCollect"]

        if quantAvail > 0:
            message += f"{quantAvail} of item {item} are in stock at {storeName}\nAvailable in Store: {availInstore}\nAvailable Online: {availOnline}\n\n"

    ctypes.windll.user32.MessageBoxW(0, message, "Ikea Tracker", 0)

stockTrack("https://www.ikea.com/ca/en/p/malm-bed-frame-high-black-brown-luroey-s69009475/", "ca", "256, 004, 149, 216")