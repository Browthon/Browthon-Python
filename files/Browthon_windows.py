#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.Browthon_utils import *


class ParametreBox(QWidget):
    def __init__(self, main):
        super(ParametreBox, self).__init__()
        self.main = main
        self.setWindowTitle("Paramètres")
        self.setMinimumSize(600, 400)
        self.layoutMain = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.title = QLabel("Paramètres")
        self.title.setFont(self.main.fonts["titre"])
        self.title.setAlignment(Qt.AlignHCenter)
        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.scroll)
        self.container = QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QVBoxLayout(self.container)

        self.moteurListe = ["Google", "DuckDuckGo", "Ecosia", "Yahoo", "Bing"]
        self.url = "http://pastagames.fr.nf/browthon"
        self.jsListe = ["Activé", "Désactivé"]
        self.privateListe = ["Désactivé", "Activé"]
        self.deplacementListe = ["Activé", "Désactivé"]
        self.themeListe = ["Blanc", "Sombre", "Bleu", "Rouge"]
        self.sessionListe = ["Désactivé", "Activé"]
        self.logListe = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        try:
            with open('config.txt', 'r') as fichier:
                defall = fichier.read().split('\n')
                if defall[0].split(" ")[1] == "https://www.google.fr/?gws_rd=ssl#q=":
                    temp = "Google"
                elif defall[0].split(" ")[1] == "https://duckduckgo.com/?q=":
                    temp = "DuckDuckGo"
                elif defall[0].split(" ")[1] == "https://www.ecosia.org/search?q=":
                    temp = "Ecosia"
                elif defall[0].split(" ")[1] == "https://fr.search.yahoo.com/search?p=":
                    temp = "Yahoo"
                elif defall[0].split(" ")[1] == "https://www.bing.com/search?q=":
                    temp = "Bing"
                for i in range(len(self.moteurListe)):
                    if self.moteurListe[i] == temp:
                        self.moteurListe[0], self.moteurListe[i] = self.moteurListe[i], self.moteurListe[0]
                        break

                self.url = defall[1].split(" ")[1]

                if defall[2].split(" ")[1] == "True":
                    self.jsListe = ["Activé", "Désactivé"]
                else:
                    self.jsListe = ["Désactivé", "Activé"]

                if defall[3].split(" ")[1] == "True":
                    self.privateListe = ["Activé", "Désactivé"]
                else:
                    self.privateListe = ["Désactivé", "Activé"]

                if defall[4].split(" ")[1] == "True":
                    self.deplacementListe = ["Activé", "Désactivé"]
                else:
                    self.deplacementListe = ["Désactivé", "Activé"]

                if defall[5].split(" ")[1] == "Default":
                    temp = "Blanc"
                elif defall[5].split(" ")[1] == "Dark":
                    temp = "Sombre"
                elif defall[5].split(" ")[1] == "Blue":
                    temp = "Bleu"
                elif defall[5].split(" ")[1] == "Red":
                    temp = "Rouge"
                for i in range(len(self.themeListe)):
                    if self.themeListe[i] == temp:
                        self.themeListe[0], self.themeListe[i] = self.themeListe[i], self.themeListe[0]
                        break

                if defall[6].split(" ")[1] == "True":
                    self.sessionListe = ["Activé", "Désactivé"]
                else:
                    self.sessionListe = ["Désactivé", "Activé"]

                for i in range(len(self.logListe)):
                    if self.logListe[i] == defall[7].split(" ")[1]:
                        self.logListe[0], self.logListe[i] = self.logListe[i], self.logListe[0]
                        break
        except:
            pass

        self.moteur = QLabel("Moteur de recherche")
        self.moteur.setFont(self.main.fonts["description"])
        self.moteur.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.moteur)
        self.moteurBox = QComboBox()
        self.moteurBox.addItems(self.moteurListe)
        self.layout.addWidget(self.moteurBox)

        self.accueil = QLabel("Url d'accueil")
        self.accueil.setFont(self.main.fonts["description"])
        self.accueil.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.accueil)
        self.accueilBox = QLineEdit()
        self.accueilBox.setText(self.url)
        self.layout.addWidget(self.accueilBox)

        self.js = QLabel("JavaScript")
        self.js.setFont(self.main.fonts["description"])
        self.js.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.js)
        self.jsBox = QComboBox()
        self.jsBox.addItems(self.jsListe)
        self.layout.addWidget(self.jsBox)

        self.private = QLabel("Navigation privée")
        self.private.setFont(self.main.fonts["description"])
        self.private.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.private)
        self.privateBox = QComboBox()
        self.privateBox.addItems(self.privateListe)
        self.layout.addWidget(self.privateBox)

        self.deplacement = QLabel("Déplacement à l'ouverture d'un onglet")
        self.deplacement.setFont(self.main.fonts["description"])
        self.deplacement.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.deplacement)
        self.deplacementBox = QComboBox()
        self.deplacementBox.addItems(self.deplacementListe)
        self.layout.addWidget(self.deplacementBox)

        self.style = QLabel("Thème")
        self.style.setFont(self.main.fonts["description"])
        self.style.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.style)
        self.styleBox = QComboBox()
        self.styleBox.addItems(self.themeListe)
        self.layout.addWidget(self.styleBox)

        self.session = QLabel("Chargement de la dernière session")
        self.session.setFont(self.main.fonts["description"])
        self.session.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.session)
        self.sessionBox = QComboBox()
        self.sessionBox.addItems(self.sessionListe)
        self.layout.addWidget(self.sessionBox)

        self.log = QLabel("Niveau minimum des logs")
        self.log.setFont(self.main.fonts["description"])
        self.log.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.log)
        self.logBox = QComboBox()
        self.logBox.addItems(self.logListe)
        self.layout.addWidget(self.logBox)

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.validateChoice)
        self.layout.addWidget(self.valider)

        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

    def validateChoice(self):
        self.texteFile = "UrlMoteur "
        temp = self.moteurListe[self.moteurBox.currentIndex()]
        if temp == "Google":
            self.texteFile += "https://www.google.fr/?gws_rd=ssl#q=\n"
        elif temp == "DuckDuckGo":
            self.texteFile += "https://duckduckgo.com/?q=\n"
        elif temp == "Ecosia":
            self.texteFile += "https://www.ecosia.org/search?q=\n"
        elif temp == "Yahoo":
            self.texteFile += "https://fr.search.yahoo.com/search?p=\n"
        else:
            self.texteFile += "https://www.bing.com/search?q=\n"

        self.texteFile += "UrlAccueil " + self.accueilBox.text() + "\n"

        self.texteFile += "JavaScript "
        if self.jsListe[self.jsBox.currentIndex()] == "Activé":
            self.texteFile += "True\n"
        else:
            self.texteFile += "False\n"

        self.texteFile += "NavigationPrivée "
        if self.privateListe[self.privateBox.currentIndex()] == "Activé":
            self.texteFile += "True\n"
        else:
            self.texteFile += "False\n"

        self.texteFile += "DéplacementOnglet "
        if self.deplacementListe[self.deplacementBox.currentIndex()] == "Activé":
            self.texteFile += "True\n"
        else:
            self.texteFile += "False\n"

        self.texteFile += "Style "
        temp = self.themeListe[self.styleBox.currentIndex()]
        if temp == "Blanc":
            self.texteFile += "Default\n"
        elif temp == "Sombre":
            self.texteFile += "Dark\n"
        elif temp == "Bleu":
            self.texteFile += "Blue\n"
        else:
            self.texteFile += "Red\n"

        self.texteFile += "Session "
        if self.sessionListe[self.sessionBox.currentIndex()] == "Activé":
            self.texteFile += "True\n"
        else:
            self.texteFile += "False\n"

        self.texteFile += "NiveauLog " + self.logListe[self.logBox.currentIndex()]

        with open('config.txt', 'w') as fichier:
            fichier.write(self.texteFile)
        QMessageBox().about(self, "Configuration enregistrée !", "Merci de relancer Browthon.")
        self.close()


class ListeBox(QWidget):
    def __init__(self, main, liste, texte):
        super(ListeBox, self).__init__()
        self.main = main
        self.liste = liste
        self.texte = texte
        self.on = True
        self.setWindowTitle(texte)
        self.grid = QGridLayout()

        self.title = QLabel(texte)
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setFont(self.main.fonts["titre"])
        self.listeW = ListWidget(liste)
        self.supprimer = QPushButton("Supprimer")
        self.supprimerT = QPushButton("Tout Supprimer")

        self.listeW.itemDoubleClicked.connect(self.launch)
        self.supprimerT.clicked.connect(self.deleteAll)
        self.supprimer.clicked.connect(self.delete)

        self.grid.addWidget(self.title, 1, 1, 1, 2)
        self.grid.addWidget(self.listeW, 2, 1, 1, 2)
        self.grid.addWidget(self.supprimer, 3, 1)
        self.grid.addWidget(self.supprimerT, 3, 2)

        if self.texte == "Favoris":
            self.addFav = QPushButton("Ajouter Favori")
            self.addFav.clicked.connect(self.addFavF)
            self.grid.addWidget(self.addFav, 4, 1, 1, 2)
        elif self.texte == "Raccourcis URL":
            self.addRaccourci = QPushButton("Ajouter Raccourci")
            self.addRaccourci.clicked.connect(self.addRaccourciF)
            self.grid.addWidget(self.addRaccourci, 4, 1, 1, 2)
        elif self.texte == "Sessions":
            self.addSession = QPushButton("Ajouter Session")
            self.addSession.clicked.connect(self.addSessionF)
            self.grid.addWidget(self.addSession, 4, 1, 1, 2)

        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

    def addFavF(self):
        self.close()
        self.main.addFav()

    def addRaccourciF(self):
        self.close()
        self.main.addRaccourci()

    def addSessionF(self):
        self.close()
        self.main.addSession()

    def launch(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i.title == self.listeW.currentItem().text():
                    self.close()
                    i.load()
                    break

    def showUpdate(self, liste):
        self.liste = liste
        self.listeW.updateList(self.liste)
        self.show()

    def delete(self):
        if self.listeW.currentItem():
            for i in self.liste:
                if i.title == self.listeW.currentItem().text():
                    self.close()
                    if self.texte == "Historique":
                        self.main.removeHistory(i.url)
                    elif self.texte == "Sessions":
                        self.main.removeSession()
                    elif self.texte == "Raccourcis URL":
                        self.main.removeRaccourci()
                    else:
                        self.main.removeFav(i.url)

    def deleteAll(self):
        self.listeW.deleteAllItems()
        if self.texte == "Historique":
            self.main.removeAllHistory()
        elif self.texte == "Sessions":
            self.main.removeAllSession()
        elif self.texte == "Raccourcis URL":
            self.main.removeAllRaccourci()
        else:
            self.main.removeAllFav()


class InformationBox(QWidget):
    def __init__(self, main, about):
        super(InformationBox, self).__init__()
        self.about = about
        self.main = main
        self.button = QPushButton("Site")
        if self.about == "Browthon":
            self.setFixedSize(500, 350)
            self.setWindowTitle("Informations sur Browthon")
            self.title = QLabel("Browthon")
            self.description = QLabel(self.main.versionAll + "\nCréé par PastaGames\n\nSite :")
            self.button.clicked.connect(lambda: self.openWebsite("http://pastagames.fr.nf"))
            self.image = QPixmap("logo.png")
        elif self.about == "PyQt":
            self.setFixedSize(500, 350)
            self.setWindowTitle("Informations sur PyQt")
            self.title = QLabel("PyQt")
            self.description = QLabel("Version utilisée: " + PYQT_VERSION_STR + "\nCréé par Riverbank Computing\n\nSite :")
            self.button.clicked.connect(lambda: self.openWebsite("https://riverbankcomputing.com/software/pyqt/intro"))
            self.image = QPixmap("pyqt_logo.png")
        elif self.about == "Qt":
            self.setFixedSize(500, 350)
            self.setWindowTitle("Informations sur Qt")
            self.title = QLabel("Qt")
            self.description = QLabel("Version : " + QT_VERSION_STR +"\nCréé par The Qt Company\n\nSite :")
            self.button.clicked.connect(lambda: self.openWebsite("https://www.qt.io/"))
            self.image = QPixmap("qt_logo.png")
        self.title.setAlignment(Qt.AlignHCenter)
        self.description.setAlignment(Qt.AlignHCenter)
        self.title.setFont(self.main.fonts["titre"])
        self.description.setFont(self.main.fonts["description"])
        self.grid = QGridLayout()
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.image)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.imageLabel, 1, 1)
        self.grid.addWidget(self.title, 2, 1)
        self.grid.addWidget(self.description, 3, 1)
        self.grid.addWidget(self.button, 4, 1)
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

    def openWebsite(self, url):
        self.close()
        self.main.addOngletWithUrl(url)


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
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

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
                QMessageBox().about(self, "Création annulé", "Le raccourci " + self.result + " existe déjà !")
            else:
                self.url = self.Url.text()
                found = False
                if "http://" in self.url or "https://" in self.url:
                    found = True
                else:
                    if "." in self.url:
                        found = True
                if not found:
                    QMessageBox().about(self, "Création annulé", "Le raccourci " + self.result + " n'a pas un url valide !")
                else:
                    self.main.raccourciArray.append(Item(self.main, self.result, self.url))
                    QMessageBox().about(self, "Raccourci créée", "Le raccourci " + self.result + " a été créée !")
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
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

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
                for i in self.main.raccourciArray:
                    i.setInteraction(self.main.raccourci)
                QMessageBox().about(self, "Raccourci supprimée", "Le raccourci " + self.result + " a été supprimée !")
            else:
                QMessageBox().about(self, "Raccourci non trouvée", "Le raccourci " + self.result + " n'a pas été trouvé !")
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
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)

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
                QMessageBox().about(self, "Création annulé", "La session " + self.result + " existe déjà !")
            else:
                urls = []
                for i in range(self.main.tabOnglet.count()):
                    urls.append(self.main.tabOnglet.widget(i).url().toString())
                self.main.sessionArray.append(ItemSession(self.main, self.result, urls))
                QMessageBox().about(self, "Session créée", "La session " + self.result + " a été créée !")
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
                QMessageBox().about(self, "Session supprimée", "La session " + self.result + " a été supprimée !")
            else:
                QMessageBox().about(self, "Session non trouvée", "La session " + self.result + " n'a pas été trouvé !")
        self.close()