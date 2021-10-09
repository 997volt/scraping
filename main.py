from firebase import getDatabase, getAllCards, giveCardNewName
from scraping import scrapFromAllShops
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = getAllCards(database)

#scrapElectro(database, allCards, today)
if 0:
    scrapFromAllShops(database, allCards, today)
if 1:
    newName = 'ASUS Dual RTX 3060 Ti V2 OC'
    searchFor  = ['3060', 'Ti', 'Asus', 'Dual', 'v2', 'Oc']
    searchNot = ['Mini']
    tpuLink = 'https://www.techpowerup.com/gpu-specs/asus-dual-rtx-3060-ti-v2-oc.b9085'
    giveCardNewName(database, allCards, newName, searchFor, searchNot, tpuLink)

print('End of program reached')