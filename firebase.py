import pyrebase
import uuid
from fb import getFirebaseConfig

shops = {
    'komputronik',
    'morele',
    'fox',
    'euro',
    'xkom',
    'sferis',
    'proline',
    'komtek',
    'pcforce',
    'vobis',
    'mediaexpert',
    'avans',
    'oleole',
    'electro'
}

def getDatabase():
    firebaseConfig = getFirebaseConfig()

    firebase = pyrebase.initialize_app(firebaseConfig)
    return firebase.database()

def getAllCards(database):
    return database.child('cards').get()

def addCard(database, allCards, shopName, cardName, cardLink, date, price, cardsAdded):
    if(price != 0):
        cardId = getCardId(allCards, shopName, cardName)
        if(cardId == ''):
            cardId = createRandomName()
            database.child('cards').child(cardId).child(shopName).set({'name': cardName, 'link': cardLink, 'prices': {date: price}})
        else:
            database.child('cards').child(cardId).child(shopName).child('prices').update({date: price})
        return cardsAdded + 1
    return cardsAdded

def getCardId(allCards, shopName, cardName):    
    for card in allCards.each():
        try:
            if (card.val()[shopName]['name'] == cardName):
                return card.key()
        except:
            pass
    return ''

def createRandomName():
    return 'new-' + str(uuid.uuid4())

def isCardInDatabase(allCards, cardId):
    for card in allCards.each():
        if (card.key() == cardId):
            return True
    return False

def giveCardNewName(database, allCards):
    searchFor  = '3060'
    searchFor2 = '3060'
    for card in allCards.each():
        if(card.key()[0:3] == 'new'):
            for shop in shops:
                try:
                    if(searchFor in card.val()[shop]['name'] and searchFor2 in card.val()[shop]['name']):
                        print(card.val()[shop]['name'])
                        newName = input('Give new name: ')
                        if(len(newName) > 5):
                            database.child('cards').child(newName).update(card.val())
                            database.child('cards').child(card.key()).remove()
                except:
                    pass
        