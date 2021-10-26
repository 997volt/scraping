from bs4 import BeautifulSoup
import requests
from firebase import addCard

maxPagesNumber = 100

def scrapFromAllShops(database, allCards, date):
    scrapKomputronik(database, allCards, date)
    scrapSferis(database, allCards, date)
    scrapXkom(database, allCards, date)
    scrapEuro(database, allCards, date)
    scrapFox(database, allCards, date)
    scrapMorele(database, allCards, date)
    scrapProline(database, allCards, date)
    scrapKomtek(database, allCards, date)
    scrapPcforce(database, allCards, date)
    scrapVobis(database, allCards, date)
    scrapMediaExpert(database, allCards, date)
    scrapAvans(database, allCards, date)
    scrapOleOle(database, allCards, date)
    scrapElectro(database, allCards, date)


def getWebpage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers).text
    return BeautifulSoup(source, 'lxml')


def priceCleanup(price):
    try:
        return float(price.replace("\u202f", "").replace(",", ".").replace(" ", "").replace("zł", "").replace("\n", "").replace("\xa0", "").replace("\t", ""))
    except:
        return 0


def scrapSferis(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.sferis.pl/karty-graficzne-2889?f=a806%3A13392.1625&p=' + str(i))

        for product in soup.find('div', id='list', class_='tiles').find_all('div', class_='standard'):
            card = product.find(class_='product-info').find('a', class_='title')
            if(card != None):
                name = card['title']
                link = card['href']
                price = priceCleanup(product.find('span', class_='price__part price__part--regular').text)
                cardsAdded = addCard(database, allCards, 'sferis', name, link, date, price, cardsAdded)

        if(i >= len(soup.find('nav', id='pagination').find_all('li'))):
            break 
    print('Scrapped ' + str(cardsAdded) + ' cards from sferis.pl')


def scrapXkom(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.x-kom.pl/g-5/c/345-karty-graficzne.html?page=' + str(i))

        for product in soup.find_all('div', class_="sc-1yu46qn-4 zZmhy sc-2ride2-0 eYsBmG"):
            try:
                name = product.find('h3').text
                price = priceCleanup(product.find(class_='sc-6n68ef-0 sc-6n68ef-3 hIoPZN').text)
                link = 'https://www.x-kom.pl' + product.find(class_='sc-1h16fat-0 irSQpN')['href']
                cardsAdded = addCard(database, allCards, 'xkom', name, link, date, price, cardsAdded)
            except:
                pass
    
        if(i >= int(soup.find('span', class_='sc-11oikyw-2 ekasrY').text.replace('z ', ''))):
            break 
    print('Scrapped ' + str(cardsAdded) + ' cards from x-kom.pl')


#almost the same as OleOle
def scrapEuro(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.euro.com.pl/karty-graficzne,strona-'+str(i)+'.bhtml')
        for product in soup.find_all('div', class_="product-for-list"):
            try:
                card = product.find('h2', class_='product-name').a
                name = card.text.replace("\n", "").replace("\t", "")
                link = "https://www.euro.com.pl" + card['href']
                price = priceCleanup(product.find('div', class_='price-normal selenium-price-normal').text)
                cardsAdded = addCard(database, allCards, 'euro', name, link, date, price, cardsAdded)
            except:
                pass

        try:
            if(i >= len(soup.find('div', class_="paging-numbers").text.replace("\t", "").replace("\n", ""))):            
                break  
        except:
            print('ERROR: Only 1 page loaded from Euro.com')
            break
    print('Scrapped ' + str(cardsAdded) + ' cards from Euro.com')


def scrapOleOle(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.oleole.pl/karty-graficzne,strona-'+str(i)+'.bhtml')
        for product in soup.find_all('div', class_="product-for-list"):
            try:
                card = product.find('h2', class_='product-name').a
                name = card.text.replace("\n", "").replace("\t", "")
                link = "https://www.oleole.pl" + card['href']
                price = priceCleanup(product.find('div', class_='price-normal selenium-price-normal').text)
                cardsAdded = addCard(database, allCards, 'oleole', name, link, date, price, cardsAdded)
            except:
                pass
        try:
            if(i >= len(soup.find('div', class_="paging-numbers").text.replace("\t", "").replace("\n", ""))):            
                break  
        except:
            print('ERROR: Only 1 page loaded from OleOle.pl')
            break
    print('Scrapped ' + str(cardsAdded) + ' cards from oleole.com')


def scrapFox(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://foxkomputer.pl/pl/c/Karty-graficzne/53/' + str(i) + '/default/1/f_at_393_1186/1/f_at_393_1185/1')

        nvidia = int(soup.find('a', title='NVIDIA').find('em').text[1:-1])
        amd = int(soup.find('a', title='AMD Radeon').find('em').text[1:-1])

        if((i-1) * 12 > nvidia+amd):
            break        

        for product in soup.find_all('div', class_="product-inner-wrap"):
            card = product.find('a', class_="prodname f-row")
            if(card != None):
                name = card['title']
                link = "https://foxkomputer.pl" + card['href']
                price = priceCleanup(product.find('div', class_='price f-row').find('em').text)
                cardsAdded = addCard(database, allCards, 'fox', name, link, date, price, cardsAdded)

    print('Scrapped ' + str(cardsAdded) + ' cards from FoxKomputer.pl')
    

def scrapMorele(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.morele.net/kategoria/karty-graficzne-12/,,,,,,,,0,,,,/' + str(i))
        for product in soup.find_all('div', class_="cat-product card"):
            card = product.find('a', class_="productLink")
            if(card != None):
                name = card['title']
                link = "https://www.morele.net" + card['href']
                price = priceCleanup(product.find('div', class_="price-new").text)
                cardsAdded = addCard(database, allCards, 'morele', name, link, date, price, cardsAdded)

        if (soup.find('li', class_="pagination-lg btn active") == None):
            break
    print('Scrapped ' + str(cardsAdded) + ' cards from Morele.net')


def scrapKomputronik(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.komputronik.pl/category/1099/karty-graficzne.html?showBuyActiveOnly=1&p=' + str(i))
        pages = soup.find('div', class_="product-list-top-pagination").find_all('li')
        for product in soup.find('ul', class_='product-entry2-wrap').find_all('li', class_='product-entry2'):
            card = product.find('div', class_='pe2-head')
            if(card != None):
                name = card.text[18:-13]
                link = card.a['href']
                price = priceCleanup(product.find('div', class_='prices').find(class_='price').span.text)
                cardsAdded = addCard(database, allCards, 'komputronik', name, link, date, price, cardsAdded)
        
        if(i >= int(pages[len(pages)-2].text)):
            break  
    print('Scrapped ' + str(cardsAdded) + ' cards from Komputeronik.pl')


def scrapProline(database, allCards, date):
    cardsAdded = 0
    for i in range(0,maxPagesNumber):
        soup = getWebpage('https://proline.pl/?kat=Karty+graficzne+PCI-E&stan=dostepne&page=0' + str(i))
        for product in soup.find('table', class_='cennik pbig').find_all('tr'):
            try:
                name = product.a['title'][0:-1]        
                link = 'https://proline.pl/'+product.a['href'] 
                price = priceCleanup(product.find(class_='c').text)
                cardsAdded = addCard(database, allCards, 'proline', name, link, date, price, cardsAdded)
            except:
                pass

        if(i+1 >= int(soup.find('input', class_="pageNumber")['max'])):
            break 
    print('Scrapped ' + str(cardsAdded) + ' cards from proline.pl')


# the same function working for komtek and pcforce 
def getPagesKP(soup):
    try:
        pages = soup.find('ul', class_='paginator').find_all('li')
        return int(pages[len(pages)-2].text)
    except:
        return 1


def scrapKomtek(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://komtek24.pl/komputery/podzespoly-komputerowe/karty-graficzne/'+ str(i) +'/default/4/f_at_17183_33592/1/f_availability_2/1')

        for product in soup.find('div', class_='products viewphot s-row').find_all('div', class_='product-inner-wrap'):
            try:
                card = product.find('a', class_='prodname f-row') 
                name = card['title']    
                link = 'https://komtek24.pl' + card['href'] 
                price = priceCleanup(product.find('div', class_='price f-row').em.text)
                cardsAdded = addCard(database, allCards, 'komtek', name, link, date, price, cardsAdded)
            except:
                pass

        if(i >= getPagesKP(soup)):
            break
    print('Scrapped ' + str(cardsAdded) + ' cards from komtek24.pl')

            
def scrapPcforce(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://pcforce.pl/Podzespoly-komputerowe/Karty-graficzne/Karty-graficzne-nVidia/AMD/' + str(i) + '/default/1/f_availability_2/1')
        for product in  soup.find('div', class_='products viewphot s-row').find_all('div', class_='product-inner-wrap'):
            try:
                card = product.find('a', class_='prodname f-row') 
                name = card['title']    
                link = 'https://pcforce.pl' + card['href'] 
                price = priceCleanup(product.find('div', class_='price f-row').em.text)
                cardsAdded = addCard(database, allCards, 'pcforce', name, link, date, price, cardsAdded)
            except:
                pass

        if(i >= getPagesKP(soup)):
            break 
    print('Scrapped ' + str(cardsAdded) + ' cards from pcforce.pl')


def scrapVobis(database, allCards, date):
    cardsAdded = 0
    finished = False
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://vobis.pl/peryferia/karty-graficzne?limit=100&page='+ str(i))
        for product in soup.find_all('div', class_='m-offerBox_desc'):
            try:
                card = product.find('h2', class_='m-offerBox_name_txt').find('a', class_='js-analyticsLink js-analyticsData')
                name = card['title']    
                link = 'https://vobis.pl' + card['href']
                price = priceCleanup(product.find('p', class_='m-offerBox_price').text)
                if(not 'niedostępny' in product.find('p', class_='m-offerBox_delivery').text):
                    cardsAdded = addCard(database, allCards, 'vobis', name, link, date, price, cardsAdded)
                else:
                    finished = True
            except:
                pass

        if(finished):
            break    
    print('Scrapped ' + str(cardsAdded) + ' cards from vobis.pl')


def scrapMediaExpert(database, allCards, date):
    cardsAdded = 0
    finished = False
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.mediaexpert.pl/komputery-i-tablety/podzespoly-komputerowe/karty-graficzne?limit=50&page='+ str(i))
        for product in soup.find('div', class_='offers-list').find_all('div', class_='offer-box'):
            try:
                if(product.find('div', class_='offer-unavailable') != None):
                    finished = True
                else:
                    card = product.find('h2', class_='name is-section').find('a', class_='is-animate spark-link')
                    name = card.text[15:-14]
                    link = 'https://www.mediaexpert.pl' + card['href']
                    price = priceCleanup(product.find('div', class_='main-price is-big').find('span', class_='whole').text)
                    cardsAdded = addCard(database, allCards, 'mediaexpert', name, link, date, price, cardsAdded)                    
            except:
                pass

        if(finished):
            break    
    print('Scrapped ' + str(cardsAdded) + ' cards from mediaexpert.pl')


def scrapAvans(database, allCards, date):
    cardsAdded = 0
    finished = False
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.avans.pl/komputery-i-tablety/podzespoly-komputerowe/karty-graficzne?limit=50&page='+ str(i))
        for product in soup.find('div', class_='c-grid').find_all('div', class_='c-offerBox is-wide'):
            try:
                if(product.find('div', class_='c-availabilityNotification') != None):
                    finished = True
                else:
                    card = product.find('div', class_='c-offerBox_data').a
                    name = card.text[1:-1]
                    link = 'https://www.avans.pl' + card['href']
                    price_main = product.find('div', class_='c-offerBox_row is-prices').find('div', class_='a-price_new is-big')
                    price = priceCleanup(price_main.find('span', class_='a-price_price').text) + priceCleanup(price_main.find('span', class_='a-price_divider').text)/100
                    cardsAdded = addCard(database, allCards, 'avans', name, link, date, price, cardsAdded) 
            except:
                pass

        if(finished):
            break    
    print('Scrapped ' + str(cardsAdded) + ' cards from avans.pl')


def scrapElectro(database, allCards, date):
    cardsAdded = 0
    finished = False
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.electro.pl/komputery-i-tablety/podzespoly-komputerowe/karty-graficzne?limit=50&page='+ str(i))
        for product in soup.find('div', class_='c-grid').find_all('div', class_='c-offerBox'):
            try:
                if(product.find('div', class_='c-availabilityNotification') != None):
                    finished = True
                else:
                    card = product.find('div', class_='c-offerBox_data').a
                    name = card.text[1:-1]
                    link = 'https://www.electro.pl' + card['href']
                    price_main = product.find('div', class_='c-offerBox_row is-prices').find('div', class_='a-price_new is-big')
                    price = priceCleanup(price_main.find('span', class_='a-price_price').text) + priceCleanup(price_main.find('span', class_='a-price_divider').text)/100
                    cardsAdded = addCard(database, allCards, 'electro', name, link, date, price, cardsAdded) 
            except:
                pass

        if(finished):
            break    
    print('Scrapped ' + str(cardsAdded) + ' cards from electro.pl')


#działa tylko 1 strona, bo jest beznadziejnie napisane
def scrapPcProjekt(database, allCards, date):
    cardsAdded = 0
    soup = getWebpage('https://www.pcprojekt.pl/130-karty-graficzne#/show-all')
    for product in soup.find('ul', class_='product_list grid row').find_all('li', class_='ajax_block_product'):
        try:
            if(product.find('i', class_='fa fa-thumbs-up') != None):
                card = product.find('a', class_='product-name')
                name = card['title']
                link = card['href']
                price = priceCleanup(product.find('span', class_='price product-price').text)
                cardsAdded = addCard(database, allCards, 'pcprojekt', name, link, date, price, cardsAdded) 
                print()
        except:
            pass
    print('Scrapped ' + str(cardsAdded) + ' cards from pcprojekt.pl')


#https://www.gigaserwer.pl/karty-graficzne,57/29?id_kat=29_57&filter_change=1&cena_od=&cena_do=&dostepny=1
#https://www.onexstore.pl/podzespoly-komputerowe/karty-graficzne/
#https://bitcomputer.pl/pl/c/Karty-graficzne/161