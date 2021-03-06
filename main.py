from firebase import getDatabase, giveCardNewName
from scraping import scrapFromAllShops
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = database.child('cards').get()
dictionary = database.child('dictionary').get()

if 1:
    scrapFromAllShops(database, allCards, today)
if 0:
    newName = ''
    searchFor  = ['3060', 'Ti']
    searchNot = ['']
    tpuLink = 'https://www.techpowerup.com/gpu-specs/pny-xlr8-rtx-3060-ti-revel-epic-x-lhr.b8944'
    giveCardNewName(database, allCards, newName, searchFor, searchNot, tpuLink)


print('End of program reached')