from firebase import getDatabase, getAllCards, giveCardNewName
from scraping import scrapFromAllShops
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = getAllCards(database)

if 1:
    scrapFromAllShops(database, allCards, today)
if 0:
    giveCardNewName(database, allCards)

print('End of program reached')