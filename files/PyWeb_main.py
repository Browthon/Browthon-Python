#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.PyWeb_utils import *

import os
import requests
import sys

class MainWindow(QMainWindow):
    def __init__(self, url):
        super(MainWindow, self).__init__()
        self.layout = self.layout()
        try:
            with open('config.txt'):
                pass
        except IOError:
            self.styleSheetParam = "Default"
        else:
            with open('config.txt', 'r') as fichier:
                defall = fichier.read().split('\n')
                self.styleSheetParam = defall[6].split(" ")[1]
        if self.styleSheetParam != "Default":
            try:
                with open('style/'+self.styleSheetParam+".pss"):
                    pass
            except:
                self.styleSheetParam = "Default"
                alert = QMessageBox().warning(self, "Style inconnu", "Le style "+defall[6].split(" ")[1]+" n'est pas reconnu par PyWeb.")
            else:
                with open('style/'+self.styleSheetParam+".pss", 'r') as fichier:
                    self.setStyleSheet(fichier.read())
        self.mainWidget = MainWidget(url, self)
        self.setCentralWidget(self.mainWidget)
        self.show()
        

class MainWidget(QWidget):
    def __init__(self, url, mainWindow):
        super(MainWidget, self).__init__()
        self.mainWindow = mainWindow
        self.url = url
        self.versionMinimal = "2.2.1"
        self.versionAll = "V 2.2.1 : Fail Update"
        self.grid = QGridLayout()
        try:
            with open('config.txt'):
                pass
        except IOError:
            self.js = True
            self.private = False
            self.deplacement_onglet = True
            self.lang = "FR"
        else:
            with open('config.txt', 'r') as fichier:
                defall = fichier.read().split('\n')
                if defall[2].split(" ")[1] == "True":
                    self.js = True
                else:
                    self.js = False
                if defall[3].split(" ")[1] == "True":
                    self.private = True
                else:
                    self.private = False
                if defall[4].split(" ")[1] == "True":
                    self.deplacement_onglet = True
                else:
                    self.deplacement_onglet = False
                try:
                    with open("lang/"+defall[5].split(" ")[1]+".txt"):
                        pass
                except IOError:
                    alert = QMessageBox().warning(self, "Langue non reconnue", "La langue "+defall[5].split(" ")[1]+" n'est pas reconnu par PyWeb.\nPyWeb va donc utiliser le français")
                    self.lang = "FR"
                else:
                    self.lang = defall[5].split(" ")[1]
        try:
            with open("lang/"+self.lang+".txt"):
                pass
        except IOError:
            if self.lang == "FR":
                alert = QMessageBox().warning(self, "Fichier de langue", "Le fichier "+self.lang+".txt n'a pas pu être ouvert. Merci de rajouter le fichier trouvable sur le github.\nPyWeb va maintenant s'éteindre.")
                sys.exit()
            elif self.lang == "EN":
                alert = QMessageBox().warning(self, "Language file", "The file "+self.lang+".txt can't be found. Can you add the file which is in Github ?\nPyWeb will shutdown.")
                sys.exit()
        else:
            with open("lang/"+self.lang+".txt", 'r') as fichier:
                self.texts = []
                defall = fichier.read().split('\n')
                for i in defall:
                    if " | " in i:
                        self.texts.append(i.split(" | ")[1])
        self.onglets = []
        self.ongletP = QPushButton("+")
        self.ongletM = QPushButton("-")
        self.urlInput = UrlInput(self)
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.informations = QMessageBox()
        self.accueil = QPushButton("⌂")
        self.menu = self.mainWindow.menuBar()
        self.history = self.menu.addMenu(self.texts[50])
        self.fav = self.menu.addMenu(self.texts[51])
        self.parametres = self.menu.addMenu(self.texts[52])
        self.onglet1 = Onglet(1, self)
        self.browser = self.onglet1
        self.onglets.append(self.onglet1)
        self.tabOnglet = TabOnglet(self)
        self.favArray = []
        try:
            with open("fav.txt"):
                pass
        except IOError:
            pass
        else:
            with open("fav.txt", "r") as fichier:
                for i in fichier.read().split('\n'):
                    item = i.split(" | ")
                    self.favArray.append(Item(self, item[0], item[1]))
        self.historyArray = []
        try:
            with open('history.txt'):
                pass
        except IOError:
            pass
        else:
            with open('history.txt', 'r') as fichier:
                for i in fichier.read().split("\n"):
                    item = i.split(" | ")
                    self.historyArray.append(Item(self, item[0], item[1]))
        self.informations.setWindowTitle(self.texts[0])
        self.informations.setText(self.versionAll+self.texts[1].replace(" \\n ", "\n"))
        self.parametres.addAction(self.texts[2], self.deplaceDefine)
        self.parametres.addAction(self.texts[3], self.PrivateDefine)
        self.parametres.addAction(self.texts[4], self.JSDefine)
        self.parametres.addAction(self.texts[5], self.moteurDefine)
        self.parametres.addAction(self.texts[6], self.homeDefine)
        self.parametres.addAction(self.texts[45], self.langDefine)
        self.parametres.addAction("Thèmes", self.styleDefine)
        self.parametres.addSeparator()
        self.parametres.addAction(self.texts[7], self.informations.open)
        self.fav.addAction(self.texts[8], self.addFav)
        self.fav.addAction(self.texts[9], self.suppFav)
        self.fav.addSeparator()
        for i in self.favArray:
            i.setInteraction(self.fav)
        self.history.addAction(self.texts[10], self.removeHistory)
        self.history.addSeparator()
        for i in self.historyArray:
            i.setInteraction(self.history)

        self.tabOnglet.currentChanged.connect(self.tabOnglet.changeOnglet)
        self.reload.clicked.connect(self.onglet1.reload)
        self.back.clicked.connect(self.onglet1.back)
        self.forward.clicked.connect(self.onglet1.forward)
        self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
        self.ongletP.clicked.connect(self.addOnglet)
        self.ongletM.clicked.connect(self.closeOnglet)
        self.accueil.clicked.connect(self.urlAccueil)
        self.grid.addWidget(self.back, 1, 0)
        self.grid.addWidget(self.reload, 1, 1)
        self.grid.addWidget(self.forward, 1, 2)
        self.grid.addWidget(self.urlInput, 1, 3, 1, 6)
        self.grid.addWidget(self.accueil, 1, 11)
        self.grid.addWidget(self.tabOnglet, 2, 0, 1, 12)
        self.grid.addWidget(self.ongletP, 1, 9)
        self.grid.addWidget(self.ongletM, 1, 10)
        self.setLayout(self.grid)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True);
        self.moteur = MoteurBox(self, self.texts[11], self.texts[12])
        self.home = HomeBox(self, self.texts[13], self.texts[14])
        self.lang_box = LangBox(self, self.texts[46], self.texts[47])
        self.styleBox = StyleBox(self, "Choix du thème", "Entrez le nom du fichier .pss du thème")
        page = requests.get('http://lavapower.github.io/PyWeb-site/version.html', verify=False)
        strpage = page.text.replace("\n", "")
        if self.versionMinimal != strpage:
            alert = QMessageBox().warning(self, self.texts[15], self.texts[16].replace(" \\n", "\n")+" "+strpage+" "+self.texts[17].replace(" \\n", "\n"))

    def setTitle(self):
        if self.private:
            self.setWindowTitle(self.texts[18]+" "+self.browser.title()+" - PyWeb")
        else:
            self.setWindowTitle(self.browser.title()+" - PyWeb")
        if len(self.browser.title()) >= 13:
            titre = self.browser.title()[:9]+"..."
        else:
            titre = self.browser.title()
        self.tabOnglet.setTabText(self.tabOnglet.currentIndex(), titre)
    
    def changeIcon(self):
        self.tabOnglet.setTabIcon(self.tabOnglet.currentIndex(), self.browser.icon())

    def moteurDefine(self):
        self.moteur.setWindowModality(Qt.ApplicationModal)
        self.moteur.show()

    def homeDefine(self):
        self.home.setWindowModality(Qt.ApplicationModal)
        self.home.show()

    def styleDefine(self):
        self.styleBox.setWindowModality(Qt.ApplicationModal)
        self.styleBox.show()
    
    def langDefine(self):
        self.lang_box.setWindowModality(Qt.ApplicationModal)
        self.lang_box.show()

    def urlAccueil(self):
        self.browser.load(QUrl(self.url))

    def JSDefine(self):
        if self.js:
            rep = QMessageBox().question(self, self.texts[19], self.texts[20], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
                self.js = False
        else:
            rep = QMessageBox().question(self, self.texts[21], self.texts[22], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                self.js = True

    def deplaceDefine(self):
        if self.deplacement_onglet:
            rep = QMessageBox().question(self, self.texts[23], self.texts[24], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.deplacement_onglet = False
        else:
            rep = QMessageBox().question(self, self.texts[25], self.texts[26], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.deplacement_onglet = True

    def PrivateDefine(self):
        if self.private:
            rep = QMessageBox().question(self, self.texts[27], self.texts[28], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.DiskHttpCache)
                self.private = False
        else:
            rep = QMessageBox().question(self, self.texts[29], self.texts[30], QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
                self.private = True

    def addOnglet(self):
        onglet = Onglet(len(self.onglets)+1, self)
        self.onglets.append(onglet)
        self.tabOnglet.addTab(onglet, QIcon('pyweb.png'), "PyWeb")
        onglet.show()
        if self.deplacement_onglet:
            self.tabOnglet.setCurrentWidget(onglet)

    def closeOnglet(self):
        if self.tabOnglet.count() == 1:
            question = QMessageBox().question(self, self.texts[31], self.texts[32].replace(" \\n ", "\n"), QMessageBox.Yes, QMessageBox.No)
            if question == 16384:
                self.close()
            else:
                info = QMessageBox().about(self, self.texts[33], self.texts[34])
        else:
            self.tabOnglet.removeTab(self.tabOnglet.currentIndex())

    def addHistory(self):
        if not self.private:
            self.historyArray.append(Item(self, self.browser.title(), self.browser.url().toString()))
            self.history.clear()
            self.history.addAction(self.texts[10], self.removeHistory)
            self.history.addSeparator()
            for i in self.historyArray:
                i.setInteraction(self.history)

    def removeHistory(self):
        self.historyArray = []
        self.history.clear()
        self.history.addAction(self.texts[10], self.removeHistory)
        self.history.addSeparator()
        info = QMessageBox().about(self, self.texts[35], self.texts[36])

    def addFav(self):
        found = False
        for i in self.favArray:
            if self.browser.url().toString() == i.url:
                found = True
        if found:
            info = QMessageBox().about(self, self.texts[37], self.texts[38])
        else:
            self.favArray.append(Item(self, self.browser.title(), self.browser.url().toString()))
            self.fav.clear()
            self.fav.addAction(self.texts[8], self.addFav)
            self.fav.addAction(self.texts[9], self.suppFav)
            self.fav.addSeparator()
            for i in self.favArray:
                i.setInteraction(self.fav)
            info = QMessageBox().about(self, self.texts[39], self.texts[40])

    def suppFav(self):
        found = False
        for i in range(len(self.favArray)):
            if self.browser.url().toString() == self.favArray[i].url:
                del self.favArray[i]
                found = True
        if found:
            self.fav.clear()
            self.fav.addAction(self.texts[8], self.addFav)
            self.fav.addAction(self.texts[9], self.suppFav)
            self.fav.addSeparator()
            for i in self.favArray:
                i.setInteraction(self.fav)
            info = QMessageBox().about(self, self.texts[41], self.texts[42])
        else:
            info = QMessageBox().about(self, self.texts[43], self.texts[44])

    def keyPressEvent(self, event):
        if event.key() == 16777268 or event.key() == 82:
            self.browser.reload()
        elif event.key() == 16777273 or event.key() == 80:
            self.parametreB.showMenu()
        elif event.key() == 78:
            self.addOnglet()
        elif event.key() == 72:
            self.historyB.showMenu()
        elif event.key() == 70:
            self.favB.showMenu()
        elif event.key() == 81:
            self.closeOnglet()
        elif event.key() == 84:
            self.refreshTheme()

    def refreshTheme(self):
        if self.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.mainWindow.setStyleSheet(fichier.read())
                self.moteur.setStyleSheet(fichier.read())
                self.home.setStyleSheet(fichier.read())
                self.lang_box.setStyleSheet(fichier.read())
                self.styleBox.setStyleSheet(fichier.read())

    def closeEvent(self, event):
        if self.historyArray == []:
            try:
                with open('history.txt'):
                    pass
            except IOError:
                pass
            else:
                os.remove('history.txt')
        else:
            with open('history.txt', 'w') as fichier:
                message = ""
                for i in range(len(self.historyArray)):
                    if i == len(self.historyArray)-1:
                        message += self.historyArray[i].title + " | " + self.historyArray[i].url
                    else:
                        message += self.historyArray[i].title + " | " + self.historyArray[i].url + "\n"
                fichier.write(message)
        if self.favArray == []:
            try:
                with open('fav.txt'):
                    pass
            except IOError:
                pass
            else:
                os.remove('fav.txt')
        else:
            with open('fav.txt', 'w') as fichier:
                message = ""
                for i in range(len(self.favArray)):
                    if i == len(self.favArray)-1:
                        message += self.favArray[i].title + " | " + self.favArray[i].url
                    else:
                        message += self.favArray[i].title + " | " + self.favArray[i].url + '\n'
                fichier.write(message)
        try:
            with open('config.txt'):
                pass
        except IOError:
            pass
        else:
            contenu = []
            with open('config.txt', 'r') as fichier:
                contenu = fichier.read().split('\n')
                contenu[2] = contenu[2].split(" ")[0]+" "+str(self.js)
                contenu[3] = contenu[3].split(" ")[0]+" "+str(self.private)
                contenu[4] = contenu[4].split(" ")[0]+" "+str(self.deplacement_onglet)
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
