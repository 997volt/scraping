from bs4 import BeautifulSoup
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time
import random


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


def createNewDocument(db, collection, gpuName):
    allGpus = getAllGpus(db, collection)
    removeAllCards(allGpus, gpuName)
    scrapTpuMain(allGpus, gpuName)
    scrapAllGpusDetails(allGpus, gpuName)
    setAllGpus(db, collection, allGpus)


def createNewDocumentFromVgabios(db, collection, gpuName):
    allGpus = getAllGpus(db, collection)
    removeAllCards(allGpus, gpuName)
    scrapTpuVgabios(allGpus, gpuName)
    #scrapAllVgabiosDetails(allGpus, gpuName)
    #scrapAllGpusDetails(allGpus, gpuName)
    setAllGpus(db, collection, allGpus)


###########################################################
#                       Scraping                          #
###########################################################  


def createNewCard(cardName, cardTpuUrl):
    newCard = {'slug': slugify(cardName), 'name': cardName, 'tpu_url': cardTpuUrl, 'order': -1, 
    'clock_base': 0, 'clock_boost': 0, 
    'power': {'connector': '', 'max_power_limit': 0, 'stock_power_limit': 0, 'max_vrm_current': 0},
    'design': {'cooler_score': 0, 'slot_width': 0, 'length': 0, 'height': 0, 'width': 0}
    }
    return newCard


def fixCardName(cardName):
    cardName = cardName.replace("STRIX", "Strix").replace("ColorFul", "Colorful").replace("GALAX", "Galax")
    cardName = cardName.replace("GIGABYTE", "Gigabyte").replace("AORUS", "Aorus").replace("KUROTOSHIKOU", "Kurotoshikou")
    cardName = cardName.replace("MAXSUN", "Maxsun").replace("ZOTAC", "Zotac")
    cardName = cardName.replace("MINI", "Mini").replace("DUAL", "Dual").replace("GAMING", "Gaming").replace("ERAZOR", "Erazor")
    cardName = cardName.replace("ULTRA", "Ultra").replace("BOY", "Boy").replace("ELITE", "Elite").replace("MASTER", "Master")
    cardName = cardName.replace("EAGLE", "Eagle").replace("PRO", "Pro").replace("VISION", "Vision").replace("RENEGADE", "Renegade")
    cardName = cardName.replace("RED", "Red").replace("TWIN", "Twin").replace("GALAKURO", "Galakuro").replace("WHITE", "White")
    cardName = cardName.replace("CLASSIC", "Classic").replace("HURRICANE", "Hurricane").replace("AERO", "Aero").replace("TRIO", "Trio")
    cardName = cardName.replace("PLUS", "Plus").replace("FAN", "Fan").replace("VENTUS", "Ventus").replace("REVEL", "Revel")
    cardName = cardName.replace("EPIC", "Epic").replace("UPRISING", "Uprising")
    return cardName


def slugify(cardName):
    return cardName.replace(". ", "_").replace(" ", "_").replace(".", "_").replace("-", "").lower()


def getWebpage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers).text
    return BeautifulSoup(source, 'lxml')


def scrapTpuMain(allGpus, gpuName):
    url = ''
    if(gpuName == 'rtx3060ti'):
        url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-3060-ti.c3681'
    elif(gpuName == 'rtx3080'):
        url = 'https://www.techpowerup.com/gpu-specs/geforce-rtx-3080.c3621'

    if(url != ''):
        soup = getWebpage(url)
        table = soup.find(class_="details customboards")
        for product in table.find('tbody').find_all('tr'):
            cardName = fixCardName(product.find('a').text)
            cardTpuUrl = 'https://www.techpowerup.com' + product.find('a')['href']
            addCard(allGpus, gpuName, createNewCard(cardName, cardTpuUrl))


def scrapTpuVgabios(allGpus, gpuName):
    url = ''
    if(gpuName == 'rtx3060ti'):
        for i in range(1,10):
            url = 'https://www.techpowerup.com/vgabios/?model=RTX+3060+Ti&memSize=8192&page=' + str(i)
            soup = getWebpage(url)
            max = len(soup.find('nav', class_='pager').find(class_='buttons').find_all('a'))
            table = soup.find(class_="bioslist")
            for product in table.find('tbody').find_all('tr'):
                cardTpuVgabiosUrl = product.find('td', class_='name').find('a')['href'][9:15:]
                addCard(allGpus, gpuName, {'tpu_vgabios_nr': cardTpuVgabiosUrl})
            if( i == max):
                break
            time.sleep(random.randrange(10,30))


def scrapAllGpusDetails(allGpus, gpuName):
    for gpu in allGpus:
        if(gpu['gpuName'] == gpuName):
            for card in gpu['cards']:
                scrapTpuDetails(card)
                print('Added details for ' + card['name'])
                time.sleep(random.randrange(60,120))


def getTpuCardClocks(card, websiteSection):
    for field in websiteSection.find_all('dl', class_='clearfix'):
        fieldName = field.find('dt').text
        fieldContent = field.find('dd').text
        if(fieldName == 'Base Clock'):
            card['clock_base'] = int(fieldContent.split(' ')[0])
        elif(fieldName == 'Boost Clock'):
            boost = fieldContent.split(' ')
            if(len(boost) == 4):
                card['clock_boost'] = int(boost[1][3::])
            else:
                card['clock_boost'] = int(boost[0])


def getTpuCardSize(card, fieldName, fieldContent):
    value = 0
    if(len(fieldContent.split(' ')) == 3):
        value = fieldContent.split(' ')[0]
    elif(len(fieldContent.split(' ')) == 5):
        value = fieldContent.split(' ')[1][2::]
    value = int(value)
    if(fieldName == 'Length'):
        card['design']['length'] = value
    elif(fieldName == 'Width'):
        card['design']['width'] = value
    elif(fieldName == 'Height'):
        card['design']['height'] = value


def getTpuCardPowerConn(card, fieldContent):
    value = 0
    if(len(fieldContent.split(' ')) == 3):
        value = fieldContent.split(' ')[1][-2::] + fieldContent.split(' ')[2]
    else:
        value =  fieldContent.split(' ')[0] + fieldContent.split(' ')[1]
    card['power']['connector'] = value


def getTpuCardBusWidth(card, fieldContent):
    toCheck = ''
    if(len(fieldContent.split('-')) == 2):
        toCheck = fieldContent.split('-')[0]
    elif(len(fieldContent.split('-')) == 3):
        toCheck = fieldContent.split('-')[1][4::]
    if(toCheck == 'Dual'):
        card['design']['slot_width'] = 2
    elif(toCheck == 'Triple'):
        card['design']['slot_width'] = 3


def getTpuCardDesign(card, websiteSection):
    for field in websiteSection.find_all('dl', class_='clearfix'):
        fieldName = field.find('dt').text
        fieldContent = field.find('dd').text
        if(fieldName == 'Length' or fieldName == 'Width' or fieldName == 'Height'):
            getTpuCardSize(card, fieldName, fieldContent)
        elif(fieldName == 'Power Connectors'):
            getTpuCardPowerConn(card, fieldContent)
        elif(fieldName == 'Slot Width'):
            getTpuCardBusWidth(card, fieldContent)


def scrapTpuDetails(card):
    passed = False
    while(not passed):
        try:
            soup = getWebpage(card['tpu_url'])
            #soup = getWebpage(card)
            for section in soup.find('div', class_='sectioncontainer').find_all('section', class_='details'):
                sectionName = section.find('h2').text.replace('\n','').replace('\t','')
                #if(sectionName == 'Graphics Processor'):
                    #for field in section.find_all('dl', class_='clearfix'):
                        #if(field.find('dt').text == 'GPU Variant'):
                            #t = field.find('dd').text.split('\n')
                            #TODO: finish
                if(sectionName == 'Clock Speeds'):
                    getTpuCardClocks(card, section)
                elif(sectionName == 'Board Design'):
                    getTpuCardDesign(card, section)
            passed = True
        except:
            rand = random.randrange(5*60,15*60)
            print(card['name'] + " failed, waiting " + rand + " seconds")
            time.sleep(rand)


###########################################################
#                           Main                          #
###########################################################

db = connect()
collection = 'gpusTest2'
gpuName = 'rtx3060ti'
createNewDocumentFromVgabios(db, collection, gpuName)
#scrapTpuDetails('https://www.techpowerup.com/gpu-specs/colorful-tomahawk-rtx-3060-ti-deluxe-edition-lhr.b9306')