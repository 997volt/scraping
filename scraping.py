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


def getWebpage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source = requests.get(url, headers=headers).text
    return BeautifulSoup(source, 'lxml')

def priceCleanup(price):
    return float(price.replace(",", ".").replace(" ", "").replace("zł", "").replace("\n", "").replace("\xa0", "").replace("\t", ""))

def scrapSferis(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.sferis.pl/karty-graficzne-2889?f=a806%3A13392.1625&p=' + str(i))
        pages = len(soup.find('nav', id='pagination').find_all('li'))

        for product in soup.find('div', id='list', class_='tiles').find_all('div', class_='standard'):
            card = product.find(class_='product-info').find('a', class_='title')
            if(card != None):
                name = card['title']
                link = card['href']
                price = priceCleanup(product.find('span', class_='price__part price__part--regular').text)

                addCard(database, allCards, 'sferis', name, link, date, price)
                cardsAdded = cardsAdded + 1

        if(i == pages):
            print('Scrapped ' + str(cardsAdded) + ' cards from sferis.pl')
            break 

def scrapXkom(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.x-kom.pl/g-5/c/345-karty-graficzne.html?page=' + str(i))
        pages = int(soup.find('span', class_='sc-11oikyw-2 ekasrY').text.replace('z ', ''))

        for product in soup.find_all('div', class_="sc-1yu46qn-4 zZmhy sc-2ride2-0 eYsBmG"):
            name = product.find('h3').text
            price = priceCleanup(product.find(class_='sc-6n68ef-0 sc-6n68ef-3 hIoPZN').text)
            link = 'https://www.x-kom.pl' + product.find(class_='sc-1h16fat-0 irSQpN')['href']

            addCard(database, allCards, 'xkom', name, link, date, price)
            cardsAdded = cardsAdded + 1
    
        if(i == pages):
            print('Scrapped ' + str(cardsAdded) + ' cards from x-kom.pl')
            break 

def scrapEuro(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.euro.com.pl/karty-graficzne,strona-'+str(i)+'.bhtml')
        pages = len(soup.find('div', class_="paging-numbers").text.replace("\t", "").replace("\n", ""))

        for product in soup.find_all('div', class_="product-for-list"):
            card = product.find('h2', class_='product-name').a

            if(card != None):
                try:
                    name = card.text
                    name = name.replace("\n", "").replace("\t", "")
                    link = "https://www.euro.com.pl" + card['href']
                    price = priceCleanup(product.find('div', class_='price-normal selenium-price-normal').text)

                    addCard(database, allCards, 'euro', name, link, date, price)
                    cardsAdded = cardsAdded + 1
                except:
                    pass

        if(i == pages):
            print('Scrapped ' + str(cardsAdded) + ' cards from Euro.com')
            break  

def scrapFox(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://foxkomputer.pl/pl/c/Karty-graficzne/53/' + str(i) + '/default/1/f_at_393_1186/1/f_at_393_1185/1')

        nvidia = int(soup.find('a', title='NVIDIA').find('em').text[1:-1])
        amd = int(soup.find('a', title='AMD Radeon').find('em').text[1:-1])

        if((i-1) * 12 > nvidia+amd):
            print('Scrapped ' + str(cardsAdded) + ' cards from FoxKomputer.pl')
            break        

        for product in soup.find_all('div', class_="product-inner-wrap"):
            card = product.find('a', class_="prodname f-row")

            if(card != None):
                name = card['title']
                link = "https://foxkomputer.pl" + card['href']
                price = priceCleanup(product.find('div', class_='price f-row').find('em').text)

                addCard(database, allCards, 'fox', name, link, date, price)
                cardsAdded = cardsAdded + 1
    

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

                addCard(database, allCards, 'morele', name, link, date, price)
                cardsAdded = cardsAdded + 1

        if (soup.find('li', class_="pagination-lg btn active") == None):
            print('Scrapped ' + str(cardsAdded) + ' cards from Morele.net')
            break

def scrapKomputronik(database, allCards, date):
    cardsAdded = 0
    for i in range(1,maxPagesNumber):
        soup = getWebpage('https://www.komputronik.pl/category/1099/karty-graficzne.html?showBuyActiveOnly=1&p=' + str(i))
        pages = soup.find('div', class_="product-list-top-pagination").find_all('li')
        pages = int(pages[len(pages)-2].text)
        for product in soup.find('ul', class_='product-entry2-wrap').find_all('li', class_='product-entry2'):
            card = product.find('div', class_='pe2-head')
            if(card != None):
                name = card.text[18:-13]
                link = card.a['href']
                price = priceCleanup(product.find('div', class_='prices').find(class_='price').span.text)

                addCard(database, allCards, 'komputronik', name, link, date, price)
                cardsAdded = cardsAdded + 1
        
        if(i >= pages):
            print('Scrapped ' + str(cardsAdded) + ' cards from Komputeronik.pl')
            break  

def scrapProline(database, allCards, date):
    cardsAdded = 0
    for i in range(0,maxPagesNumber):
        soup = getWebpage('https://proline.pl/?kat=Karty+graficzne+PCI-E&stan=dostepne&page=0' + str(i))
        pages = int(soup.find('input', class_="pageNumber")['max'])
        
        for product in soup.find('table', class_='cennik pbig').find_all('tr'):
            try:
                name = product.a['title'][0:-1]        
                link = 'https://proline.pl/'+product.a['href'] 
                price = priceCleanup(product.find(class_='c').text)

                addCard(database, allCards, 'proline', name, link, date, price)
                cardsAdded = cardsAdded + 1
            except:
                pass

        if(i+1 >= pages):
            print('Scrapped ' + str(cardsAdded) + ' cards from proline.pl')
            break 
            