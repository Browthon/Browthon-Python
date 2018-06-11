#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.Browthon_utils import *
from files.Browthon_windows import *

import os
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
                self.styleSheetParam = defall[5].split(" ")[1]
        if self.styleSheetParam != "Default":
            try:
                with open('style/'+self.styleSheetParam+".pss"):
                    pass
            except:
                self.styleSheetParam = "Default"
                QMessageBox().warning(self, "Style inconnu", "Le style "+defall[5].split(" ")[1]+" n'est pas reconnu par Browthon.")
            else:
                with open('style/'+self.styleSheetParam+".pss", 'r') as fichier:
                    self.setStyleSheet(fichier.read())
        self.mainWidget = MainWidget(url, self)
        self.setCentralWidget(self.mainWidget)
        self.show()
    
    def closeEvent(self, event):
        self.mainWidget.closeEvent(event)
        

class MainWidget(QWidget):
    def __init__(self, url, mainWindow):
        super(MainWidget, self).__init__()
        self.mainWindow = mainWindow
        self.url = url
        self.versionMinimal = "2.3.0"
        self.versionAll = "V 2.3.0 : Appearance Update"
        self.grid = QGridLayout()
        try:
            with open('config.txt'):
                pass
        except IOError:
            self.js = True
            self.private = False
            self.sessionRecovery = False
            self.deplacement_onglet = True
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
                if defall[6].split(" ")[1] == "True":
                    self.sessionRecovery = True
                else:
                    self.sessionRecovery = False
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
        self.history = self.menu.addMenu("Historique")
        self.fav = self.menu.addMenu("Favoris")
        self.session = self.menu.addMenu("Session")
        self.raccourci = self.menu.addMenu("Raccourci URL")
        self.parametres = self.menu.addMenu("Paramètres")
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
        self.sessionArray = []
        try:
            with open("session.txt"):
                pass
        except IOError:
            pass
        else:
            with open("session.txt", "r") as fichier:
                for i in fichier.read().split('\n'):
                    item = i.split(" | ")
                    self.sessionArray.append(ItemSession(self, item[0], item[1].split(" - ")))
        self.raccourciArray = []
        try:
            with open("raccourci.txt"):
                pass
        except IOError:
            pass
        else:
            with open("raccourci.txt", "r") as fichier:
                for i in fichier.read().split("\n"):
                    item = i.split(" | ")
                    self.raccourciArray.append(Item(self, item[0], item[1]))
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
        self.informations.setWindowTitle('Informations sur Browthon')
        self.informations.setText(self.versionAll+"\n Créé par PastaGames \n Github : https://github.com/LavaPower/Browthon".replace(" \\n ", "\n"))
        self.parametres.addAction("Déplacement Onglet", self.deplaceDefine)
        self.parametres.addAction("Navigation Privée", self.PrivateDefine)
        self.parametres.addAction("JavaScript", self.JSDefine)
        self.parametres.addAction("Définir Moteur", self.moteurDefine)
        self.parametres.addAction("Définir Accueil", self.homeDefine)
        self.parametres.addAction("Dernière Session", self.sessionDefine)
        self.parametres.addAction("Thèmes", self.styleDefine)
        self.parametres.addSeparator()
        self.parametres.addAction("Informations", self.informations.open)
        self.fav.addAction("Ajouter Page", self.addFav)
        self.fav.addAction("Supprimer Page", self.suppFav)
        self.fav.addSeparator()
        for i in self.favArray:
            i.setInteraction(self.fav)
        self.session.addAction("Ajouter Session", self.addSession)
        self.session.addAction("Supprimer Session", self.removeSession)
        self.session.addSeparator()
        for i in self.sessionArray:
            i.setInteraction(self.session)
        self.raccourci.addAction("Ajouter Raccourci", self.addRaccourci)
        self.raccourci.addAction("Supprimer Raccourci", self.removeRaccourci)
        self.raccourci.addSeparator()
        for i in self.raccourciArray:
            i.setInteraction(self.raccourci)
        self.history.addAction("Supprimer", self.removeHistory)
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
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.moteur = MoteurBox(self, "Moteur par défaut", "Choisissez le moteur par défaut")
        self.home = HomeBox(self, "Url d'accueil", "Entrez l'url de votre page d'accueil")
        self.styleBox = StyleBox(self, "Choix du thème", "Entrez le nom du fichier .pss du thème")
        self.addSessionBox = AddSessionBox(self, "Nom Session", "Entrez le nom de la session ou ANNULER")
        self.removeSessionBox = RemoveSessionBox(self, "Nom Session", "Entrez le nom de la session ou ANNULER")
        self.addRaccourciBox = AddRaccourciBox(self, "Nom Raccourci", "Entrez le nom et l'url du raccourci ou ANNULER")
        self.removeRaccourciBox = RemoveRaccourciBox(self, "Nom Raccourci", "Entrez le nom du raccourci ou ANNULER")

        if self.sessionRecovery:
            try:
                with open("last.txt", "r") as fichier:
                    contenu = fichier.read().split("\n")
            except:
                QMessageBox().warning(self, "Pas d'ancienne session", "Aucune ancienne session n'a été trouvée")
            else:
                for i in range(len(contenu)):
                    if i == 0:
                        self.urlInput.enterUrlGiven(contenu[i])
                    else:
                        self.addOngletWithUrl(contenu[i])
        
    def setTitle(self):
        if self.private:
            self.mainWindow.setWindowTitle("[Privé]"+" "+self.browser.title()+" - Browthon")
        else:
            self.mainWindow.setWindowTitle(self.browser.title()+" - Browthon")
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

    def urlAccueil(self):
        self.browser.load(QUrl(self.url))

    def JSDefine(self):
        if self.js:
            rep = QMessageBox().question(self, "Désactiver JS", "Voulez vous désactiver le JavaScript ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
                self.js = False
        else:
            rep = QMessageBox().question(self, "Activer JS", "Voulez vous activer le JavaScript ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
                self.js = True
    
    def sessionDefine(self):
        if self.sessionRecovery:
            rep = QMessageBox().question(self, "Dernière session", "Voulez-vous ne plus recharger la dernière session ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.sessionRecovery = False
        else:
            rep = QMessageBox().question(self, "Dernière session", "Voulez-vous recharger la dernière session ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.sessionRecovery = True

    def deplaceDefine(self):
        if self.deplacement_onglet:
            rep = QMessageBox().question(self, "Désactiver Déplacement", "Voulez vous désactiver le déplacement à l'ouverture d'un onglet ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.deplacement_onglet = False
        else:
            rep = QMessageBox().question(self, "Activer Déplacement", "Voulez vous activer le déplacement à l'ouverture d'un onglet ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                self.deplacement_onglet = True

    def PrivateDefine(self):
        if self.private:
            rep = QMessageBox().question(self, "Désactiver Navigation Privée", "Voulez vous désactiver la navigation privée ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.DiskHttpCache)
                self.private = False
        else:
            rep = QMessageBox().question(self, "Activer Navigation Privée", "Voulez vous activer la navigation privée ?", QMessageBox.Yes, QMessageBox.No)
            if rep == 16384:
                QWebEngineProfile.defaultProfile().setHttpCacheType(QWebEngineProfile.MemoryHttpCache)
                self.private = True

    def addOnglet(self):
        onglet = Onglet(len(self.onglets)+1, self)
        self.onglets.append(onglet)
        self.tabOnglet.addTab(onglet, QIcon('logo.png'), "Browthon")
        onglet.show()
        if self.deplacement_onglet:
            self.tabOnglet.setCurrentWidget(onglet)
    
    def addOngletWithUrl(self, url):
        onglet = Onglet(len(self.onglets)+1, self)
        self.onglets.append(onglet)
        self.tabOnglet.addTab(onglet, QIcon('logo.png'), "Browthon")
        onglet.show()
        self.tabOnglet.setCurrentWidget(onglet)
        self.urlInput.enterUrlGiven(url)

    def closeOnglet(self):
        if self.tabOnglet.count() == 1:
            question = QMessageBox().question(self, "Quitter ?", "Vous avez fermé le dernier onglet... \n Voulez vous quitter Browthon ?".replace(" \\n ", "\n"), QMessageBox.Yes, QMessageBox.No)
            if question == 16384:
                self.mainWindow.close()
            else:
                QMessageBox().about(self, "Annulation", "Le dernier onglet a donc été réouvert")
        else:
            self.tabOnglet.removeTab(self.tabOnglet.currentIndex())

    def addHistory(self):
        if not self.private:
            self.historyArray.append(Item(self, self.browser.title(), self.browser.url().toString()))
            self.history.clear()
            self.history.addAction("Supprimer", self.removeHistory)
            self.history.addSeparator()
            for i in self.historyArray:
                i.setInteraction(self.history)
    
    def addSession(self):
        self.addSessionBox.setWindowModality(Qt.ApplicationModal)
        self.addSessionBox.show()
    
    def removeSession(self):
        self.removeSessionBox.setWindowModality(Qt.ApplicationModal)
        self.removeSessionBox.show()
    
    def addRaccourci(self):
        self.addRaccourciBox.setWindowModality(Qt.ApplicationModal)
        self.addRaccourciBox.show()
    
    def removeRaccourci(self):
        self.removeRaccourciBox.setWindowModality(Qt.ApplicationModal)
        self.removeRaccourciBox.show()

    def removeHistory(self):
        self.historyArray = []
        self.history.clear()
        self.history.addAction("Supprimer", self.removeHistory)
        self.history.addSeparator()
        info = QMessageBox().about(self, "Historique", "Historique supprimé")

    def addFav(self):
        found = False
        for i in self.favArray:
            if self.browser.url().toString() == i.url:
                found = True
        if found:
            QMessageBox().about(self, "Annulation", "Cette page est déjà dans les favoris")
        else:
            self.favArray.append(Item(self, self.browser.title(), self.browser.url().toString()))
            self.fav.clear()
            self.fav.addAction("Ajouter Page", self.addFav)
            self.fav.addAction("Supprimer Page", self.suppFav)
            self.fav.addSeparator()
            for i in self.favArray:
                i.setInteraction(self.fav)
            QMessageBox().about(self, "Ajouter", "Cette page est maintenant dans les favoris")

    def suppFav(self):
        found = False
        for i in range(len(self.favArray)):
            if self.browser.url().toString() == self.favArray[i].url:
                del self.favArray[i]
                found = True
        if found:
            self.fav.clear()
            self.fav.addAction("Ajouter Page", self.addFav)
            self.fav.addAction("Supprimer Page", self.suppFav)
            self.fav.addSeparator()
            for i in self.favArray:
                i.setInteraction(self.fav)
            QMessageBox().about(self, "Supprimer", "Cette page n'est plus dans les favoris")
        else:
            QMessageBox().about(self, "Annulation", "Cette page n'est pas dans les favoris")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R or event.key() == Qt.Key_F5:
            self.browser.reload()
        elif event.key() == Qt.Key_N:
            self.addOnglet()
        elif event.key() == Qt.Key_Q:
            self.closeOnglet()
        elif event.key() == Qt.Key_T:
            self.refreshTheme()
        elif event.key() == Qt.Key_L:
            try:
                with open("last.txt", "r") as fichier:
                    contenu = fichier.read().split("\n")
            except:
                QMessageBox().warning(self, "Pas d'ancienne session", "Aucune ancienne session n'a été trouvée")
            else:
                for i in range(len(contenu)):
                    if i == 0:
                        self.urlInput.enterUrlGiven(contenu[i])
                    else:
                        self.addOngletWithUrl(contenu[i])

    def refreshTheme(self):
        if self.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.mainWindow.setStyleSheet(fichier.read())
                self.moteur.setStyleSheet(fichier.read())
                self.home.setStyleSheet(fichier.read())
                self.styleBox.setStyleSheet(fichier.read())
                self.addSessionBox.setStyleSheet(fichier.read())
                self.removeSessionBox.setStyleSheet(fichier.read())
                self.addRaccourciBox.setStyleSheet(fichier.read())
                self.removeRaccourciBox.setStyleSheet(fichier.read())

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
        if self.raccourciArray == []:
            try:
                with open('raccourci.txt'):
                    pass
            except IOError:
                pass
            else:
                os.remove('raccourci.txt')
        else:
            with open('raccourci.txt', 'w') as fichier:
                message = ""
                for i in range(len(self.raccourciArray)):
                    if i == len(self.raccourciArray)-1:
                        message += self.raccourciArray[i].title + " | " + self.raccourciArray[i].url
                    else:
                        message += self.raccourciArray[i].title + " | " + self.raccourciArray[i].url + '\n'
                fichier.write(message)
        if self.sessionArray == []:
            try:
                with open('session.txt'):
                    pass
            except IOError:
                pass
            else:
                os.remove('session.txt')
        else:
            with open('session.txt', 'w') as fichier:
                message = ""
                for i in range(len(self.sessionArray)):
                    urls = ""
                    for y in self.sessionArray[i].urls:
                        if y == self.sessionArray[i].urls[len(self.sessionArray[i].urls)-1]:
                            urls += y
                        else:
                            urls += y + " - "
                    if i == len(self.sessionArray)-1:
                        message += self.sessionArray[i].title + " | " + urls
                    else:
                        message += self.sessionArray[i].title + " | " + urls + "\n"
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
            contenu[6] = contenu[6].split(" ")[0]+" "+str(self.sessionRecovery)
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
        with open('last.txt', 'w') as fichier:
            contenu = ""
            for i in range(self.tabOnglet.count()):
                if i == self.tabOnglet.count() - 1:
                    contenu += self.tabOnglet.widget(i).url().toString()
                else:
                    contenu += self.tabOnglet.widget(i).url().toString()+"\n"
            fichier.write(contenu)
