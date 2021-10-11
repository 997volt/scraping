from pyasn1_modules.rfc2459 import PhysicalDeliveryCountryName
from firebase import getDatabase, getAllCards, giveCardNewName, printCards
from scraping import scrapFromAllShops
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = getAllCards(database)

printCards(allCards, '3060 Ti')

#scrapElectro(database, allCards, today)
if 1:
    scrapFromAllShops(database, allCards, today)
if 0:
    newName = ''
    searchFor  = ['3060', 'Ti']
    searchNot = ['']
    tpuLink = 'https://www.techpowerup.com/gpu-specs/pny-xlr8-rtx-3060-ti-revel-epic-x-lhr.b8944'
    giveCardNewName(database, allCards, newName, searchFor, searchNot, tpuLink)

print('End of program reached')