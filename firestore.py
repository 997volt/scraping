import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def connect():
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()


def createCardDict(name):
    newCardDict = {'name': name, 'clock_base': 1410, 'clock_boost': 1770, 
        'power': {'connector': '6+8', 'max_power_limit': 270, 'stock_power_limit': 240, 'max_vrm_current': 400}, 'cooler_score': 9,
        'shops': {'best_name': 'xkom', 'best_price': 4499, 'best_url': 'https://www.x-kom.pl...'},  
        'size': {'length': 281, 'height': 40, 'width': 117}}
    return newCardDict


def printCards(gpusStream, gpu):
    for gpus in gpusStream:
        if(gpus.id == gpu):
            gpusDict = gpus.to_dict()
            for card in gpusDict["cards"]:
                print(card['name'])
            gpusDict['cards'].append(createCardDict('testF'))
            db.collection(u'test').document(u'test').update(gpusDict)


def addCard(gpusStream, gpu):
    for gpus in gpusStream:
        if(gpus.id == gpu):
            gpusDict = gpus.to_dict()
            gpusDict['cards'].append(createCardDict('testF'))
            db.collection(u'test').document(u'test').update(gpusDict)



db = connect()
gpusStream = db.collection(u'gpus').stream()
printCards(gpusStream, 'rtx3060ti')

        

