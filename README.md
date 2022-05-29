# ikea
Small application for Ikea stock/restock lookup and alerts. A web version is available at https://extremelycorporate.ca/~oscar/ikea/ and is much more convenient if you don't need alerts.

The web implementation functionality is provided by ```shelf.py```, which can be run locally. It does not take command line inputs and the function must be called with the correct arguments to fuction correctly.

# ALERTS
The following instructions are only for if you wish to set up notifications for when an item restocks. Also, only works for Windows (for now).

Download ```notifier.py``` and ```data.db``` from the root directory.

Navigate to the bottom of ```notifier.py``` and replace the default arguments for stockTrack().

```stockTrack(item, country, location)```

```item``` refers to the specific item you want to look up. The input can be a link to the item page, or the 8-digit SKU number found on the page under "Article Number"/at the end of the link.
  
```country``` refers to a two letter code for the country to search in. 
  
Currently, only ```ca``` and ```us``` (case insensitive) are available, but I'll work to update the database as soon as possible with other countries.
  
```location``` refers to the 3-digit store ID of any store in the country. This can be multiple arguments, comma separated.

**Examples**: 

```stockTrack("https://www.ikea.com/ca/en/p/malm-bed-frame-high-black-brown-luroey-s69009475/", "ca", "256, 372, 149")```

```stockTrack("60473548", "us", "560")```

A list of available codes will be provided shortly.

***AUTOMATION***
  
In order to actually have this work properly, you must automate the program execution in some way or another.
  
I suggest using Windows Task Scheduler to simply run ```notifier.py``` once every hour or maybe even once per day. This means the program doesn't have to run constantly and can start with power on.
