from threading import Thread
import requests
from bs4 import BeautifulSoup
import roshDyoAPI
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import gui
import pickle as cPickle
printerList = []

try:
    with open('printersDB.rick','rb') as DB:
        printerList = cPickle.load(DB)
except:
    print("0 Printers")
def spitDB():
    for printers in printerList:
        print(printers)
        try:
            print('printers = ' +printers.name)
        except:
            for printer in printers:
                print('printer = ' +printer.name)
spitDB()

def searchDB(model):
    currentPrinters = []
    for printers in printerList:
        if model in printers.name:
            currentPrinters.append(printers)
    if not currentPrinters:
        return 0
    else:
        return currentPrinters

def search():
    #print("printer to search:")
    printerSearchTerm = ui.modelInput.text()
    URL = "https://www.rosh-dyo.co.il/?post_type=printer%2C+product&s=" + str(printerSearchTerm)
    currentPrinterList = searchDB(printerSearchTerm)
    if currentPrinterList == 0 :
        currentPrinterList = roshDyoAPI.getPrinterlist(URL)
        with open('printersDB.rick', 'wb') as printersDB:
            for printers in currentPrinterList:
                printerList.append(printers)
            cPickle.dump(printerList, printersDB)

    ui.tableWidget.setRowCount(len(currentPrinterList))
    row = 0
    nameCol = 0
    typeCol = 1
    def colPick(inkType):
        switch = {
            'שחור':2,
            'צבעוני':3,
            'אדום':4,
            'צהוב':5,
            'כחול':6,
            'תוף':7
        }
        return switch.get(inkType,7)

    def rowInit(row,backGroundColor):
        column = 0
        while column < ui.tableWidget.columnCount():
            ui.tableWidget.setItem(row,column,QtWidgets.QTableWidgetItem(''))
            ui.tableWidget.item(row,column).setBackground(QtGui.QColor(backGroundColor,backGroundColor,backGroundColor))
            column = column+1

    blkCol = 2
    clrCol =3
    megantaCol =4
    yellowCol = 5
    cyanCol =6
    drumCol = 7
    backGroundColor = False

    for printer in currentPrinterList:
        if backGroundColor:
            gray = 220
        else:
            gray = 255
        rowInit(row,gray)

        ui.tableWidget.setItem(row,nameCol,QtWidgets.QTableWidgetItem(printer.name))
        ui.tableWidget.setItem(row,typeCol,QtWidgets.QTableWidgetItem(printer.type))
        ui.tableWidget.item(row, nameCol).setBackground(QtGui.QColor(gray,gray,gray))
        ui.tableWidget.item(row, typeCol).setBackground(QtGui.QColor(gray,gray,gray))

        #print(printer.name)
        #print(printer.type)

        col=2
        for inks in printer.perish:

            try:
                col = colPick(inks.color)
            except Exception as e:
                print(e)
            #print(inks.name)
            #print(inks.color)
            if ui.tableWidget.item(row,col).text() != '':
                #row=row+1
                #print(str(ui.tableWidget.item(row,col)))
                try:
                    ui.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(inks.name+'/'+ui.tableWidget.item(row,col).text()))
                except Exception as e:
                    print(e)
                #ui.tableWidget.insertRow(ui.tableWidget.rowCount())
                try:
                    ui.tableWidget.item(row, col).setBackground(QtGui.QColor(gray,gray,gray))
                except Exception as e:
                    print(e)
                #print('is occupied')

            else:
                ui.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(inks.name))
                ui.tableWidget.item(row, col).setBackground(QtGui.QColor(gray,gray,gray))

            #col = col+1
        row=row+1
        if backGroundColor:
            backGroundColor=False
        else:
            backGroundColor=True

    ui.label_running.hide()

def threadSearch():

    global thread
    thread = Thread(target=search)
    ui.label_running.show()
    thread.start()


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)
ui.tableWidget.setColumnWidth(0,140)
ui.tableWidget.setColumnWidth(1,60)
ui.searchButton.clicked.connect(threadSearch)




MainWindow.show()
sys.exit(app.exec_())
