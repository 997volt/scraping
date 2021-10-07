from firebase import getDatabase, getAllCards, giveCardNewName
from scraping import scrapFromAllShops, scrapAvans
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = getAllCards(database)

#scrapAvans(database, allCards, today)
if 0:
    scrapFromAllShops(database, allCards, today)
if 0:
    giveCardNewName(database, allCards)

print('End of program reached')