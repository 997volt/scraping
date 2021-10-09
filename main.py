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
    newName = ''
    searchFor  = ['3060', 'Ti', 'Asus']
    searchNot = ['']
    tpuLink = 'https://www.techpowerup.com/gpu-specs/asus-tuf-rtx-3060-ti-v2-gaming.b9092'
    giveCardNewName(database, allCards, newName, searchFor, searchNot, tpuLink)

print('End of program reached')