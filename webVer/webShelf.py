# IKEA TRACKER WEB
# May 17th, 2022

import requests
import json
import re
import sqlite3
import os
from pathlib import Path

rootPath = os.environ.get('PWD') # FOR DEPLOYMENT

def stockTrack(item : str, country : str) -> list:
    """Returns a 2D list with the inventory status of the requested Ikea item."""

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

    dataTable = [["Store Location", "StoreID", "Quantity", "Online", "Restock", "Early Restock", "Late Restock"]]

    availabilities = data["availabilities"]
    for store in availabilities:
        storeInfo = [] # Table

        # Identify store
        storeCode = store["classUnitKey"]["classUnitCode"]

        # If store is unknown, skip
        if not storeCode in storeCodes:
            continue

        storeName = storeCodes[storeCode]
        carrying = store["buyingOption"]["cashCarry"]

        if not "availability" in carrying:
            continue

        # Identify current availability
        availStats = carrying["availability"]
        quantAvail = availStats["quantity"]
        availOnline = store["availableForClickCollect"]

        #TABLE
        storeInfo.append(storeName)
        storeInfo.append(storeCode)
        storeInfo.append(quantAvail)
        storeInfo.append(availOnline)

        # Identify restock quantity and dates if restock data exists
        if "restocks" in availStats:
            restock = availStats["restocks"][0]
            quantRestock = restock["quantity"]
            restockEarly = restock["earliestDate"]
            restockLate = restock["latestDate"]

            #TABLE
            storeInfo.append(quantRestock)
            storeInfo.append(restockEarly)
            storeInfo.append(restockLate)
        
        #TABLE
        else:
            storeInfo.append("N/A")
            storeInfo.append("N/A")
            storeInfo.append("N/A")
        
        #TABLE
        dataTable.append(storeInfo)

    return dataTable