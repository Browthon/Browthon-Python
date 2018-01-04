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


class MainWindow(QWidget):
    def __init__(self, url):
        super(MainWindow, self).__init__()
        self.url = url
        self.grid = QGridLayout()
        try:
            with open('config.txt'):
                pass
        except IOError:
            self.js = True
            self.private = False
            self.deplacement_onglet = False
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
        self.onglets = []
        self.ongletP = QPushButton("+")
        self.ongletM = QPushButton("-")
        self.urlInput = UrlInput(self)
        self.historyB = QPushButton("H")
        self.history = QMenu("")
        self.favB = QPushButton("★")
        self.fav = QMenu("")
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.parametreB = QPushButton("⁞")
        self.parametres = QMenu("")
        self.informations = QMessageBox()
        self.accueil = QPushButton("⌂")
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
                    self.favArray.append(i)
        self.historyArray = []
        try:
            with open('history.txt'):
                pass
        except IOError:
            pass
        else:
            with open('history.txt', 'r') as fichier:
                for i in fichier.read().split("\n"):
                    self.historyArray.append(i)
        self.informations.setWindowTitle("Informations sur PyWeb")
        self.informations.setText("V 2.0.0 : PyQt5 Update\nCréé par LavaPower \nGithub : https://github.com/LavaPower/PyWeb")
        self.parametres.addAction("Déplacement Onglet", self.deplaceDefine)
        self.parametres.addAction("Navigation Privée", self.PrivateDefine)
        self.parametres.addAction("JavaScript", self.JSDefine)
        self.parametres.addAction("Définir Moteur", self.moteurDefine)
        self.parametres.addSeparator()
        self.parametres.addAction("Informations", self.informations.open)
        self.parametreB.setMenu(self.parametres)
        self.historyB.setMenu(self.history)
        self.favB.setMenu(self.fav)
        self.fav.addAction("Ajouter Page", self.addFav)
        self.fav.addAction("Supprimer Page", self.suppFav)
        self.fav.addSeparator()
        for i in self.favArray:
            item = i.split(" | ")
            fItem = Item(self, item[0], item[1])
            self.fav.addAction(fItem.title, fItem.load)
        self.history.addAction("Supprimer", self.removeHistory)
        self.history.addSeparator()
        for i in self.historyArray:
            item = i.split(" | ")
            hItem = Item(self, item[0], item[1])
            self.history.addAction(hItem.title, hItem.load)

        self.tabOnglet.currentChanged.connect(self.tabOnglet.changeOnglet)
        self.reload.clicked.connect(self.onglet1.reload)
        self.back.clicked.connect(self.onglet1.back)
        self.forward.clicked.connect(self.onglet1.forward)
        self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
        self.parametreB.clicked.connect(self.parametreB.showMenu)
        self.historyB.clicked.connect(self.history.show)
        self.favB.clicked.connect(self.fav.show)
        self.ongletP.clicked.connect(self.addOnglet)
        self.ongletM.clicked.connect(self.closeOnglet)
        self.accueil.clicked.connect(self.urlAccueil)
        self.grid.addWidget(self.back, 1, 0)
        self.grid.addWidget(self.reload, 1, 1)
        self.grid.addWidget(self.forward, 1, 2)
        self.grid.addWidget(self.urlInput, 1, 3, 1, 6)
        self.grid.addWidget(self.accueil, 1, 9)
        self.grid.addWidget(self.historyB, 0, 4, 1, 2)
        self.grid.addWidget(self.favB, 0, 6, 1, 2)
        self.grid.addWidget(self.parametreB, 0, 8, 1, 2)
        self.grid.addWidget(self.tabOnglet, 2, 0, 1, 10)
        self.grid.addWidget(self.ongletP, 0, 0, 1, 2)
        self.grid.addWidget(self.ongletM, 0, 2, 1, 2)
        self.setLayout(self.grid)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True);
        self.moteur = MoteurBox("Moteur par défaut", "Choissez le moteur par défaut")
        page = requests.get('http://lavapower.github.io/version/PyWeb.html', verify=False)
        strpage = page.text.replace("\n", "")
        if "2.0.0" != strpage:
            alert = QMessageBox().warning(self, "Nouvelle Version", "La version "+strpage+" vient de sortir !\nhttps://github.com/LavaPower/PyWeb/releases")

    def setTitle(self):
        if self.private:
            self.setWindowTitle("[Privé] "+self.browser.title()+" - PyWeb")
        else:
            self.setWindowTitle(self.browser.title()+" - PyWeb")
        if len(self.browser.title()) >= 13:
            titre = self.browser.title()[:9]+"..."
        else:
            titre = self.browser.title()
        self.tabOnglet.setTabText(self.tabOnglet.currentIndex(), titre)

    def moteurDefine(self):
        self.moteur.setWindowModality(Qt.ApplicationModal)
        self.moteur.show()

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

    def deplaceDefine(self):
        if self.deplacement_onglet:
            rep = QMessageBox().question(self, "Désactiver Déplacement", "Voulez vous désactiver le déplacement à l'ouverture d'un onglet ?", QMessageBox.Yes, QMessageBox.No)
            print("True : ",rep)
            if rep == 16384:
                self.deplacement_onglet = False
        else:
            rep = QMessageBox().question(self, "Activer Déplacement", "Voulez vous activer le déplacement à l'ouverture d'un onglet ?", QMessageBox.Yes, QMessageBox.No)
            print("False : ", rep)
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
        self.tabOnglet.addTab(onglet, "PyWeb")
        onglet.show()
        if self.deplacement_onglet:
            self.tabOnglet.setCurrentWidget(onglet)

    def closeOnglet(self):
        if self.tabOnglet.count() == 1:
            question = QMessageBox().question(self, "Quitter ?", "Vous avez fermé le dernier onglet... \nVoulez vous quitter PyWeb ?", QMessageBox.Yes, QMessageBox.No)
            if question == 16384:
                self.close()
            else:
                info = QMessageBox().about(self, "Annulation", "Le dernier onglet a donc été réouvert")
        else:
            self.tabOnglet.removeTab(self.tabOnglet.currentIndex())

    def addHistory(self):
        if not self.private:
            self.historyArray.append(self.browser.title()+" | "+self.browser.url().toString())
            hItem = Item(self, self.browser.title(), self.browser.url().toString())
            self.history.addAction(hItem.title, hItem.load)

    def removeHistory(self):
        self.historyArray = []
        self.history.clear()
        self.history.addAction("Supprimer", self.removeHistory)
        self.history.addSeparator()
        info = QMessageBox().about(self, "Historique", "Historique supprimé")

    def addFav(self):
        found = False
        for i in self.favArray:
            if self.browser.url().toString() == i.split(" | ")[1]:
                found = True
        if found:
            info = QMessageBox().about(self, "Annulation", "Cette page est déjà dans les favoris")
        else:
            self.favArray.append(self.browser.title()+" | "+self.browser.url().toString())
            fItem = Item(self, self.browser.title(), self.browser.url().toString())
            self.fav.addAction(fItem.title, fItem.load)
            info = QMessageBox().about(self, "Ajouter", "Cette page est maintenant dans les favoris")

    def suppFav(self):
        found = False
        for i in range(len(self.favArray)):
            if self.browser.url().toString() == self.favArray[i].split(" | ")[1]:
                del self.favArray[i]
                found = True
        if found:
            self.fav.clear()
            self.fav.addAction("Ajouter Page", self.addFav)
            self.fav.addAction("Supprimer Page", self.suppFav)
            self.fav.addSeparator()
            for i in self.favArray:
                item = i.split(" | ")
                fItem = Item(self, item[0], item[1])
                self.fav.addAction(fItem.title, fItem.load)
            info = QMessageBox().about(self, "Supprimer", "Cette page n'est plus dans les favoris")
        else:
            info = QMessageBox().about(self, "Annulation", "Cette page n'est pas dans les favoris")

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
                        message += self.historyArray[i]
                    else:
                        message += self.historyArray[i] + "\n"
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
                        message += self.favArray[i]
                    else:
                        message += self.favArray[i] + '\n'
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
