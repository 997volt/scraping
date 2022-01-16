import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def connect():
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()


def getAllGpus(db):
    allGpus = []
    gpusStream = db.collection(u'gpus').stream()
    for gpu in gpusStream:
        allGpus.append(gpu)
    return allGpus

def createCardDict(name):
    newCardDict = {'name': name, 'clock_base': 1410, 'clock_boost': 1770, 
        'power': {'connector': '6+8', 'max_power_limit': 270, 'stock_power_limit': 0, 'max_vrm_current': 0}, 'cooler_score': 0,
        'shops': {'best_name': 'xkom', 'best_price': 0, 'best_url': 'https://www.x-kom.pl'},  
        'size': {'length': 281, 'height': 40, 'width': 117}}
    return newCardDict


def printGpuCards(allGpus, gpuName):
    for gpu in allGpus:
        if(gpu.id == gpuName):
            gpuDict = gpu.to_dict()
            for card in gpuDict["cards"]:
                print(card['name'])


def addCard(db, allGpus, gpuName):
    for gpu in allGpus:
        if(gpu.id == gpuName):
            gpuDict = gpu.to_dict()
            gpuDict['cards'].append(createCardDict('testF'))
            db.collection(u'gpus').document(u'rtx3060ti').update(gpuDict)


def doGpusBackup(db, allGpus):
    for gpu in allGpus:
        if(gpu.id == 'rtx3060ti'):
            db.collection(u'gpusBackup').document(u'rtx3060ti').set(gpu.to_dict())


db = connect()
allGpus = getAllGpus(db)
printGpuCards(allGpus, 'rtx3060ti')
addCard(db, allGpus, 'rtx3060ti')
doGpusBackup(db, allGpus)
        



