from firebase import getDatabase, getAllCards, giveCardNewName
from scraping import scrapFromAllShops, scrapKomtek
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
database = getDatabase()
allCards = getAllCards(database)

scrapKomtek(database, allCards, today)

if 0:
    scrapFromAllShops(database, allCards, today)
giveCardNewName(database, allCards)

print('End of program reached')