import requests
from bs4 import BeautifulSoup
import printerClass

def getPrinterlist(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="post")
    printers = results.find_all('div', class_='single-printer')
    printerList = []
    links = []
    for printer in printers:
        links.append(printer.find('a')['href'])

    for link in links:
        url = link
        #print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        printerName = soup.find('h1').text.strip()
        printerType = None
        if "דיו למדפסת" in printerName:
            printerName = printerName.replace("דיו למדפסת ",'')
            printerType = 'הזרקת דיו'
        if "טונר" in printerName:
            printerName = printerName.replace("טונר למדפסת ",'')
            printerType = "לייזר"
        thisPrinter = printerClass.printerClass(printerName, printerType)

        perishableTable = soup.find(id='products-table')
        perishableTableBody = soup.find('tbody')

        try:
            perishables = perishableTableBody.find_all('tr')  # .text.strip()
        except Exception as e:
            #print(e)
            perishables = ''

        for perishable in perishables:
            try:
                if 'xerox' in printerName.lower() and printerType == 'לייזר':
                    name = [int(i) for i in printerName.split() if i.isdigit()]
                    #print(name)
                    thisPerishableName = 'X' + str(name[0])
                    #print("thisPerishableName= " +thisPerishableName)
                else:
                    #print('Not Xerox')
                    thisPerishableName= perishable.find('a').text.strip()
                thisPerishableName = thisPerishableName.replace("דיו",'')
                thisPerishableName = thisPerishableName.replace("טונר", '')
                thisPerishableName = thisPerishableName.replace("תוף", '')
                if ' - ' in thisPerishableName:
                    thisPerishableName = thisPerishableName.split(' - ')[1]
                thisPerishableColor = perishable.find('td').text.strip()
                if 'DR' in thisPerishableName:
                    thisPerishableColor = 'תוף'
                #   print(perishable.text.strip())
                thisPrinter.perish.append(thisPrinter.perishableClass(thisPerishableName, thisPerishableColor))



            except Exception as e:
                #print(perishable.find('a'))
                #print(perishable.find('td'))
                print(e)
                thisPerishable = ''
                thisPrinter.perish.append(thisPrinter.perishableClass(thisPerishable, ''))

        printerList.append(thisPrinter)
    return printerList
"""
    for prints in printerList:
        print("****start of class*****")
        print(prints.name)
        for pars in prints.perish:
            print(pars.name)
        print("****end of class****")"""
 #   return printerList