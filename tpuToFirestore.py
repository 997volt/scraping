from bs4 import BeautifulSoup
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


###########################################################
#                   Database Operations                   #
###########################################################

def connect():
    cred = credentials.Certificate('firebase-credentials.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()


def getAllGpus(db, collection):
    allGpus = []
    gpusStream = db.collection(collection).stream()
    for gpu in gpusStream:
        gpuDict = gpu.to_dict()
        gpuDict['gpuName'] = gpu.id
        allGpus.append(gpuDict)
    return allGpus


def setAllGpus(db, collection, allGpus):
    for gpu in allGpus:
        docId = gpu['gpuName']
        gpu.pop('gpuName')
        db.collection(collection).document(docId).set(gpu)


def removeAllCards(allGpus, gpuName):
    for gpu in allGpus:
        if(gpu['gpuName'] == gpuName):
            gpu['cards'] = []


def addCard(allGpus, gpuName, cardToAdd):
    for gpu in allGpus:
        if(gpu['gpuName'] == gpuName):
            gpu['cards'].append(cardToAdd)


###########################################################
#                       Scraping                          #
###########################################################

def getWebpage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers).text
    return BeautifulSoup(source, 'lxml')


def scrapTpuMain(gpuName):
    url = ''
    if(gpuName == 'rtx3060ti'):
        url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-3060-ti.c3681'
    elif(gpuName == 'rtx3080'):
        url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-3080.c3621'

    if(url != ''):
        soup = getWebpage(url)
        table = soup.find(class_="details customboards")
        for product in table.find('tbody').find_all('tr'):
            cardName = product.find('a').text
            cardTpuUrl = 'https://www.techpowerup.com' + product.find('a')['href']
            addCard(allGpus, gpuName, {'name': cardName, 'tpu_url': cardTpuUrl, 'order': -1})


def scrapTpu(url):
    soup = getWebpage(url)


###########################################################
#                           Main                          #
###########################################################

db = connect()
collection = 'gpusTest'
gpuName = 'rtx3060ti'
allGpus = getAllGpus(db, collection)
removeAllCards(allGpus, gpuName)
scrapTpuMain(gpuName)
setAllGpus(db, collection, allGpus)