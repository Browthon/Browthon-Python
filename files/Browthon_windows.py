#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import os, glob

from files.Browthon_utils import *

class AddRaccourciBox(QWidget):
    def __init__(self, main, title, text):
        super(AddRaccourciBox, self).__init__()
        self.main = main
        self.result = ""
        self.on = True
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.Titre = QLineEdit()
        self.Url = QLineEdit()
        self.bValider = QPushButton("Valider")
        
        self.bValider.clicked.connect(self.urlEnter)
        
        self.grid.addWidget(self.Texte, 1, 1)
        self.grid.addWidget(self.Titre, 2, 1)
        self.grid.addWidget(self.Url, 3, 1)
        self.grid.addWidget(self.bValider, 4, 1)
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
    
    def urlEnter(self):
        self.result = self.Titre.text()
        if self.result == "" or self.result == "ANNULER":
            QMessageBox().about(self, "Création annulé", "La création du raccourci a été annulée")
        else:
            found = False
            for i in range(len(self.main.raccourciArray)):
                if self.result == self.main.raccourciArray[i].title:
                    found = True
            if found:
                QMessageBox().about(self, "Création annulé", "Le raccourci "+self.result+" existe déjà !")
            else:
                self.url = self.Url.text()
                found = False
                if "http://" in self.url or "https://" in self.url:
                    found = True
                else:
                    if "." in self.url:
                        found = True
                if not found:
                    QMessageBox().about(self, "Création annulé", "Le raccourci "+self.result+" n'a pas un url valide !")
                else:
                    self.main.raccourciArray.append(Item(self.main, self.result, self.url))
                    self.main.raccourci.clear()
                    self.main.raccourci.addAction("Ajouter Raccourci", self.main.addRaccourci)
                    self.main.raccourci.addAction("Supprimer Raccourci", self.main.removeRaccourci)
                    self.main.raccourci.addSeparator()
                    for i in self.main.raccourciArray:
                        i.setInteraction(self.main.raccourci)
                    QMessageBox().about(self, "Raccourci créée", "Le raccourci "+self.result+" a été créée !")
        self.close()

class RemoveRaccourciBox(QWidget):
    def __init__(self, main, title, text):
        super(RemoveRaccourciBox, self).__init__()
        self.main = main
        self.result = ""
        self.on = True
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.Titre = QLineEdit()
        self.bValider = QPushButton("Valider")
        
        self.bValider.clicked.connect(self.urlEnter)
        
        self.grid.addWidget(self.Texte, 1, 1)
        self.grid.addWidget(self.Titre, 2, 1)
        self.grid.addWidget(self.bValider, 3, 1)
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
    
    def urlEnter(self):
        self.result = self.Titre.text()
        if self.result == "" or self.result == "ANNULER":
            QMessageBox().about(self, "Suppression annulé", "La suppression du raccourci a été annulée")
        else:
            found = False
            for i in range(len(self.main.raccourciArray)):
                if self.result == self.main.raccourciArray[i].title:
                    del self.main.raccourciArray[i]
                    found = True
            if found:
                self.main.raccourci.clear()
                self.main.raccourci.addAction("Ajouter Raccourci", self.main.addRaccourci)
                self.main.raccourci.addAction("Supprimer Raccourci", self.main.removeRaccourci)
                self.main.raccourci.addSeparator()
                for i in self.main.raccourciArray:
                    i.setInteraction(self.main.raccourci)
                QMessageBox().about(self, "Raccourci supprimée", "Le raccourci "+self.result+" a été supprimée !")
            else:
                QMessageBox().about(self, "Raccourci non trouvée", "Le raccourci "+self.result+" n'a pas été trouvé !")
        self.close()

class NameBox(QWidget):
    def __init__(self, main, title, text):
        super(NameBox, self).__init__()
        self.main = main
        self.result = ""
        self.on = True
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.Url = QLineEdit()
        
        self.Url.returnPressed.connect(self.urlEnter)
        
        self.grid.addWidget(self.Texte, 1, 1)
        self.grid.addWidget(self.Url, 2, 1)
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
        
    def urlEnter(self):
        pass

class AddSessionBox(NameBox):
    def __init__(self, main, title, text):
        super(AddSessionBox, self).__init__(main, title, text)
    
    def urlEnter(self):
        self.result = self.Url.text()
        if self.result == "" or self.result == "ANNULER":
            QMessageBox().about(self, "Création annulé", "La création de la session a été annulée")
        else:
            found = False
            for i in range(len(self.main.sessionArray)):
                if self.result == self.main.sessionArray[i].title:
                    found = True
            if found:
                QMessageBox().about(self, "Création annulé", "La session "+self.result+" existe déjà !")
            else:
                urls = []
                for i in range(self.main.tabOnglet.count()):
                    urls.append(self.main.tabOnglet.widget(i).url().toString())
                self.main.sessionArray.append(ItemSession(self.main, self.result, urls))
                self.main.session.clear()
                self.main.session.addAction("Ajouter Session", self.main.addSession)
                self.main.session.addAction("Supprimer Session", self.main.removeSession)
                self.main.session.addSeparator()
                for i in self.main.sessionArray:
                    i.setInteraction(self.main.session)
                QMessageBox().about(self, "Session créée", "La session "+self.result+" a été créée !")
        self.close()

class RemoveSessionBox(NameBox):
    def __init__(self, main, title, text):
        super(RemoveSessionBox, self).__init__(main, title, text)
    
    def urlEnter(self):
        self.result = self.Url.text()
        if self.result == "" or self.result == "ANNULER":
            QMessageBox().about(self, "Suppression annulé", "La suppression de la session a été annulée")
        else:
            found = False
            for i in range(len(self.main.sessionArray)):
                if self.result == self.main.sessionArray[i].title:
                    del self.main.sessionArray[i]
                    found = True
            if found:
                self.main.session.clear()
                self.main.session.addAction("Ajouter Session", self.main.addSession)
                self.main.session.addAction("Supprimer Session", self.main.removeSession)
                self.main.session.addSeparator()
                for i in self.main.sessionArray:
                    i.setInteraction(self.main.session)
                QMessageBox().about(self, "Session supprimée", "La session "+self.result+" a été supprimée !")
            else:
                QMessageBox().about(self, "Session non trouvée", "La session "+self.result+" n'a pas été trouvé !")
        self.close()

class HomeBox(QWidget):
    def __init__(self, main, title, text):
        super(HomeBox, self).__init__()
        self.main = main
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.Url = QLineEdit()
        
        self.Url.returnPressed.connect(self.urlEnter)
        
        self.grid.addWidget(self.Texte, 1, 1)
        self.grid.addWidget(self.Url, 2, 1)
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
        
    def urlEnter(self):
        url = self.Url.text()
        self.main.url = url
        try:
            with open('config.txt'):
                pass
        except IOError:
            pass
        else:
            contenu = []
            with open('config.txt', 'r') as fichier:
                contenu = fichier.read().split('\n')
                contenu[1] = contenu[1].split(" ")[0]+" "+url
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
        self.close()
        QMessageBox().warning(self, "Paramètres", "Il faut redémarrer Browthon pour appliquer le changement")

class StyleBox(QWidget):
    def __init__(self, main, title, text):
        super(StyleBox, self).__init__()
        self.main = main
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.grid.addWidget(self.Texte, 1, 1)
        self.b1 = QPushButton("Default")
        self.b1.clicked.connect(lambda: self.choose("Default"))
        self.b2 = QPushButton("Dark")
        self.b2.clicked.connect(lambda: self.choose("Dark"))
        self.b3 = QPushButton("Blue")
        self.b3.clicked.connect(lambda: self.choose("Blue"))
        self.b4 = QPushButton("Red")
        self.b4.clicked.connect(lambda: self.choose("Red"))
        self.grid.addWidget(self.b1, 2, 1)
        self.grid.addWidget(self.b2, 3, 1)
        self.grid.addWidget(self.b3, 4, 1)
        self.grid.addWidget(self.b4, 5, 1)
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
        
    def choose(self, choix):
        if choix == "Default":
            self.main.mainWindow.setStyleSheet("")
        else:
            try:
                with open('style/'+choix+".pss"):
                    pass
            except:
                alert = QMessageBox().warning(self, "Style inconnu", "Le style "+choix+" n'est pas reconnu par Browthon.")
                return
            else:
                with open('style/'+choix+".pss", 'r') as fichier:
                    self.main.mainWindow.setStyleSheet(fichier.read())
        try:
            with open('config.txt'):
                pass
        except IOError:
            pass
        else:
            contenu = []
            with open('config.txt', 'r') as fichier:
                contenu = fichier.read().split('\n')
                contenu[6] = contenu[6].split(" ")[0]+" "+choix
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
        self.close()
        

class MoteurBox(QWidget):
    def __init__(self, main, title, text):
        super(MoteurBox, self).__init__()
        self.main = main
        
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.Google = QPushButton("Google")
        self.DDGo = QPushButton("DuckDuckGo")
        self.Ecosia = QPushButton("Ecosia")
        self.Yahoo = QPushButton("Yahoo")
        self.Bing = QPushButton("Bing")

        self.Google.clicked.connect(self.setGoogle)
        self.DDGo.clicked.connect(self.setDDGo)
        self.Ecosia.clicked.connect(self.setEcosia)
        self.Yahoo.clicked.connect(self.setYahoo)
        self.Bing.clicked.connect(self.setBing)

        self.grid.addWidget(self.Texte, 1, 1, 1, 2)
        self.grid.addWidget(self.Google, 2, 1)
        self.grid.addWidget(self.DDGo, 2, 2)
        self.grid.addWidget(self.Ecosia, 3, 1)
        self.grid.addWidget(self.Yahoo, 3, 2)
        self.grid.addWidget(self.Bing, 4, 1, 1, 2)

        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())

    def setGoogle(self):
        self.setMoteur("https://www.google.fr/?gws_rd=ssl#q=")

    def setDDGo(self):
        self.setMoteur("https://duckduckgo.com/?q=")

    def setEcosia(self):
        self.setMoteur("https://www.ecosia.org/search?q=")

    def setYahoo(self):
        self.setMoteur("https://fr.search.yahoo.com/search?p=")

    def setBing(self):
        self.setMoteur("https://www.bing.com/search?q=")

    def setMoteur(self, txt):
        try:
            with open('config.txt'):
                pass
        except IOError:
            pass
        else:
            contenu = []
            with open('config.txt', 'r') as fichier:
                contenu = fichier.read().split('\n')
                contenu[0] = contenu[0].split(" ")[0]+" "+txt
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
        self.close()
