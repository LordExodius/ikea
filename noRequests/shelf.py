# i just want a goddamn alex drawer please for the love of god
# july 20th 2021
# oscar yu

import urllib.request
import json
import ctypes
from table import table

caStores = {
    "149" : "North York",
    "372" : "Vaughan",
    "256" : "Etobicoke",
    "040" : "Burlington",
    "004" : "Ottawa",
    "039" : "Montreal",
    "414" : "Boucherville",
    "559" : "Quebec City",
    "529" : "Halifax",
    "249" : "Winnepeg",
    "349" : "Edmonton",
    "216" : "Calgary",
    "313" : "Coquitlam",
    "003" : "Richmond"
}

def stockTrack(item : str, country = "ca", location = None) ->  None:
    item = item.replace(".", "")
    url = f"https://api.ingka.ikea.com/cia/availabilities/ru/{country}?itemNos={item}&expand=StoresList,Restocks,SalesLocations"
    headers = {
        "authority": "api.ingka.ikea.com",
        "method": "GET",
        "path": f"/cia/availabilities/ru/{country}?itemNos={item}&expand=StoresList,Restocks,SalesLocations",
        "scheme": "https",
        "accept": "application/json;version=2",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://www.ikea.com",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-client-id": "b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631"
    }

    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode("utf-8"))

    location = location.replace(" ", "").split(",")

    dataTable = [["Store", "StoreID", "Quantity", "Online", "Restock", "Early Restock", "Late Restock"]]
    rowNum = 0

    #file = open("data.json", "w", encoding="utf-8")
    #json.dump(data, file, ensure_ascii=False, indent=4)
    #print(json.dumps(data, sort_keys=True, indent=4))

    availabilities = data["availabilities"]
    for store in availabilities:
        #TABLE
        storeInfo = []
        rowNum += 1

        # Identify store
        storeCode = store["classUnitKey"]["classUnitCode"]

        # If store location is specified, only scan data for that store location
        if location and not storeCode in location:
            continue

        if storeCode in caStores:
            storeName = caStores[storeCode]

            print(f"STORE: {storeName}")
            carrying = store["buyingOption"]["cashCarry"]

            if not "availability" in carrying:
                continue

            # Identify current availability
            availStats = carrying["availability"]
            quantAvail = availStats["quantity"]
            availOnline = store["availableForClickCollect"]

            # If tracking specifict location
            if location and quantAvail > 0:
                    ctypes.windll.user32.MessageBoxW(0, f"Item {item} is in stock at {storeName}\nAvailable Online: {availOnline}", "Ikea Tracker", 0)

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

        # Unknown store
        else:
            pass

    storeTable = table(dataTable)
    print(storeTable)
    if location is None:
        input()

alex_code = "60473548"
country_code = "ca"

stockTrack(alex_code, country_code, "149")