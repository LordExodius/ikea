# ikea
Small application for Ikea stock/restock lookup and alerts. A web version is available at https://extremelycorporate.ca/~oscar/ikea/ and is much more convenient if you don't need alerts.

# usage (for alerts)
Download shelf.py and table.py from the root directory.

**ALTERNATIVELY:** Download shelf.py from noRequests directory for a urllib implementation.
- This version is ever so slightly more memory efficient, if that's something you want. There is no functional difference between the two versions.

Navigate to the bottom of shelf.py and replace the default arguments for stockTrack().

```stockTrack(item, country, location)```

```item``` refers to the SKU code of the item you wish to track/look up. This is a 10-digit number (possibly separated by dots) that can be found on an item page under "Article Number" or the last digits in the page URL.
- https://<span>www<span>.ikea.<span>com/ca/en/p/alex-drawer-unit-black-brown-***60473548***
- https://<span>www<span>.ikea.<span>com/ca/en/p/bekant-desk-black-stained-ash-veneer-black-s***59282583***
  
```country``` refers to a two letter code for the country to search in. 
  
I'm still figuring out how to compile store names by store number outside of Canada, so just leave this blank and it'll default to ```ca```. In the future, you should be able to enter ```us``` or ```de``` or any other two letter country code.
  
```location``` refers to the 3-digit store ID of any store in the country. When no store ID is provided, the program will check and output results for every store in the country. It will also provide the corresponding codes and names of all stores, so you can also use this to quickly look up store numbers. Alternatively, you can go to ikea website and find the store ID there.
  
Location takes one or more arguments in a string, separated by commas. Example: ```stockTrack(item, country, "149, 035, 356")```

When a ```location``` argument is provided, a popup will appear if the specified item is available at any of the stores specified. This popup will also say if the item is available online for click-and-collect.

***AUTOMATION***
  
In order to actually have this thing work properly, you must automate the program execution in some way or another.
  
I suggest using Windows Task Scheduler to simply run ```shelf.py``` once every hour or maybe even once per day. This means the program isn't always running all the time hogging resources (however little that may be) and also can auto start when you turn your computer on.
