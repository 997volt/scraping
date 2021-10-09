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

def checkCardMatch(cardName, searchFor, searchNot):
    match = True
    for s in searchFor:
        if (not (s in cardName or s.upper() in cardName)):
            match = False
            break
    for s in searchNot:
        if (s != '' and (s in cardName or s.upper() in cardName)):
            match = False
            break
    return match

def renameCard(database, card, cardName, newName):
    print('old name: ' + cardName)
    print('new name: ' + newName)
    response = input('write "y" to accept: ')
    if(response == 'y'):
        database.child('cards').child(newName).update(card.val())
        database.child('cards').child(card.key()).remove()

def giveCardNewName(database, allCards, newName, searchFor, searchNot, tpuLink):
    for card in allCards.each():
        if(card.key()[0:3] == 'new'):      
            shop = list(card.val().keys())[0]
            cardName = card.val()[shop]['name']
            if(checkCardMatch(cardName, searchFor, searchNot)):
                renameCard(database, card, cardName, newName)
    response = input('write "y" to replace data in dictionary: ')
    if(response == 'y'):
        addToDictionary(database, newName, searchFor, searchNot, tpuLink)

                
                
def addToDictionary(database, name, searchFor, searchNot, tpuLink):
    searchForParsed = ''
    searchNotParsed = ''
    for s in searchFor:
        searchForParsed = searchForParsed + s + ','
    searchForParsed = searchForParsed[:-1]
    for s in searchNot:
        searchNotParsed = searchNotParsed + s + ','
    searchNotParsed = searchNotParsed[:-1]
    database.child('dictionary').child(name).set({'searchFor': searchForParsed, 'searchNot': searchNotParsed, 'tpuLink': tpuLink})