#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.Browthon_utils import *
from files.Browthon_windows import *
from files.Browthon_elements import *
from files.Browthon_download import DownloadManagerWidget

import logging
import logging.handlers


class MainWindow(QMainWindow):
    def __init__(self, url, urltemp):
        super(MainWindow, self).__init__()
        self.layout = self.layout()
        try:
            with open('config.txt', 'r') as fichier:
                defall = fichier.read().split('\n')
                self.styleSheetParam = defall[5].split(" ")[1]
                self.niveauLog = defall[7].split(" ")[1]
        except IOError:
            self.styleSheetParam = "Default"
            self.niveauLog = "INFO"
        self.logger = logging.getLogger("logger")
        if self.niveauLog == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif self.niveauLog == "WARNING":
            self.logger.setLevel(logging.WARNING)
        elif self.niveauLog == "ERROR":
            self.logger.setLevel(logging.ERROR)
        elif self.niveauLog == "CRITICAL":
            self.logger.setLevel(logging.CRITICAL)
        else:
            self.logger.setLevel(logging.INFO)
        handler = logging.handlers.RotatingFileHandler(
                "logs/browthon.log", maxBytes=10000, backupCount=3)
        formatter = logging.Formatter('[%(levelname)s] %(filename)s:%(lineno)d - %(message)s (%(asctime)s)')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info("=====================")
        self.logger.info("Lancement de Browthon")
        if self.styleSheetParam != "Default":
            try:
                with open('style/' + self.styleSheetParam + ".bss", 'r') as fichier:
                    bss = parseTheme(fichier.read())
                    self.setStyleSheet(bss)
                    self.logger.debug("Le thème %s a été chargé", defall[5].split(" ")[1])
            except Exception as e:
                self.styleSheetParam = "Default"
                QMessageBox().warning(self, "Style inconnu", "Le style " + defall[5].split(" ")[1] + " n'est pas reconnu par Browthon.")
                self.logger.warning("Le thème %s est inconnu. Erreur : %s", defall[5].split(" ")[1], e)
        self.mainWidget = MainWidget(url, urltemp, self)
        self.setCentralWidget(self.mainWidget)
        self.show()

    def closeEvent(self, event):
        self.mainWidget.closeEvent(event)


class MainWidget(QWidget):
    def __init__(self, url, urltemp, mainWindow):
        super(MainWidget, self).__init__()
        self.mainWindow = mainWindow
        self.url = url
        self.urltemp = urltemp
        self.versionMinimal = "2.5.0"
        self.versionAll = "V 2.5.0 : Basic Update"
        self.fonts = {"titre": QFont("Arial", 23, QFont.Bold),
             "description": QFont("Arial", 18)}
        self.grid = QGridLayout()
        try:
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
            self.mainWindow.logger.debug("Config chargé")
        except IOError:
            self.js = True
            self.private = False
            self.sessionRecovery = False
            self.deplacement_onglet = True
            self.mainWindow.logger.warning("Le fichier de config n'a pas été trouvé")
        self.onglets = []
        self.ongletP = QPushButton("+")
        self.ongletM = QPushButton("-")
        self.urlInput = UrlInput(self)
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.accueil = QPushButton("⌂")
        self.menu = self.mainWindow.menuBar()
        self.menu.addAction("Historique", self.openHistory)
        self.menu.addAction("Favoris", self.openFav)
        self.menu.addAction("Téléchargements", self.openDownload)
        self.menu.addAction("Sessions", self.openSession)
        self.menu.addAction("Raccourcis URL", self.openRaccourci)
        self.menu.addAction("Paramètres", self.openParametres)
        self.about = self.menu.addMenu("Informations")
        self.onglet1 = Onglet(1, self)
        self.browser = self.onglet1
        self.onglets.append(self.onglet1)
        self.tabOnglet = TabOnglet(self)
        self.downloadManager = DownloadManagerWidget(self)
        self.browthonInfo = InformationBox(self, "Browthon")
        self.pyqtInfo = InformationBox(self, "PyQt")
        self.qtInfo = InformationBox(self, "Qt")
        self.favArray = []
        try:
            with open("fav.txt", 'r') as fichier:
                for i in fichier.read().split('\n'):
                    item = i.split(" | ")
                    self.favArray.append(Item(self, item[0], item[1]))
        except IOError:
            pass
        self.sessionArray = []
        try:
            with open("session.txt", 'r') as fichier:
                for i in fichier.read().split('\n'):
                    item = i.split(" | ")
                    self.sessionArray.append(ItemSession(self, item[0], item[1].split(" - ")))
        except IOError:
            pass
        self.raccourciArray = []
        try:
            with open("raccourci.txt", "r") as fichier:
                for i in fichier.read().split("\n"):
                    item = i.split(" | ")
                    self.raccourciArray.append(Item(self, item[0], item[1]))
        except IOError:
            pass
        self.historyArray = []
        try:
            with open('history.txt', 'r') as fichier:
                for i in fichier.read().split("\n"):
                    item = i.split(" | ")
                    self.historyArray.append(Item(self, item[0], item[1]))
        except IOError:
            pass
        self.about.addAction("Sur Browthon", lambda: self.openInfo("Browthon"))
        self.about.addAction("Sur PyQt", lambda: self.openInfo("PyQt"))
        self.about.addAction("Sur Qt", lambda: self.openInfo("Qt"))
        self.tabOnglet.currentChanged.connect(self.tabOnglet.changeOnglet)
        self.reload.clicked.connect(self.onglet1.reload)
        self.back.clicked.connect(self.onglet1.back)
        self.forward.clicked.connect(self.onglet1.forward)
        self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
        self.ongletP.clicked.connect(self.addOnglet)
        self.ongletM.clicked.connect(self.closeOnglet)
        self.accueil.clicked.connect(self.urlAccueil)
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.downloadManager.downloadRequested)
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
        self.addSessionBox = AddSessionBox(self, "Nom Session", "Entrez le nom de la session ou ANNULER")
        self.removeSessionBox = RemoveSessionBox(self, "Nom Session", "Entrez le nom de la session ou ANNULER")
        self.addRaccourciBox = AddRaccourciBox(self, "Nom Raccourci", "Entrez le nom et l'url du raccourci ou ANNULER")
        self.removeRaccourciBox = RemoveRaccourciBox(self, "Nom Raccourci", "Entrez le nom du raccourci ou ANNULER")
        self.historyBox = ListeBox(self, self.historyArray, "Historique")
        self.favBox = ListeBox(self, self.favArray, "Favoris")
        self.raccourciBox = ListeBox(self, self.raccourciArray, "Raccourcis URL")
        self.sessionBox = ListeBox(self, self.sessionArray, "Sessions")
        self.parametresBox = ParametreBox(self)
        if self.sessionRecovery:
            try:
                with open("last.txt", "r") as fichier:
                    contenu = fichier.read().split("\n")
                    for i in range(len(contenu)):
                        if i == 0:
                            self.urlInput.enterUrlGiven(contenu[i])
                        else:
                            self.addOngletWithUrl(contenu[i])
            except:
                QMessageBox().warning(self, "Pas d'ancienne session", "Aucune ancienne session n'a été trouvée")
                self.mainWindow.logger.warning("Tentativement de chargement d'ancienne session alors qu'il n'y en a pas")
        self.mainWindow.logger.info("Browthon chargé")

    def setTitle(self):
        if self.private:
            self.mainWindow.setWindowTitle("[Privé]" + " " + self.browser.title() + " - Browthon")
        else:
            self.mainWindow.setWindowTitle(self.browser.title() + " - Browthon")
        if len(self.browser.title()) >= 13:
            titre = self.browser.title()[:9] + "..."
        else:
            titre = self.browser.title()
        self.tabOnglet.setTabText(self.tabOnglet.currentIndex(), titre)

    def openInfo(self, about):
        if about == "Browthon":
            self.browthonInfo.setWindowModality(Qt.ApplicationModal)
            self.browthonInfo.show()
        elif about == "PyQt":
            self.pyqtInfo.setWindowModality(Qt.ApplicationModal)
            self.pyqtInfo.show()
        elif about == "Qt":
            self.qtInfo.setWindowModality(Qt.ApplicationModal)
            self.qtInfo.show()

    def changeIcon(self):
        self.tabOnglet.setTabIcon(self.tabOnglet.currentIndex(), self.browser.icon())

    def urlAccueil(self):
        self.browser.load(QUrl(self.url))

    def openParametres(self):
        self.parametresBox.setWindowModality(Qt.ApplicationModal)
        self.parametresBox.show()

    def addOnglet(self):
        onglet = Onglet(len(self.onglets) + 1, self)
        self.onglets.append(onglet)
        self.tabOnglet.addTab(onglet, QIcon('logo.png'), "Browthon")
        onglet.show()
        if self.deplacement_onglet:
            self.tabOnglet.setCurrentWidget(onglet)

    def addOngletWithUrl(self, url):
        onglet = Onglet(len(self.onglets) + 1, self)
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
            self.tabOnglet.removeTab(self.tabOnglet.currentIndex())

    def openDownload(self):
        self.downloadManager.setWindowModality(Qt.ApplicationModal)
        self.downloadManager.show()

    def openHistory(self):
        self.historyBox.setWindowModality(Qt.ApplicationModal)
        self.historyBox.showUpdate(self.historyArray)

    def addHistory(self):
        if not self.private and self.browser.title() != "":
            self.historyArray.append(Item(self, self.browser.title(), self.browser.url().toString()))

    def removeAllHistory(self):
        self.historyArray = []
        QMessageBox().about(self, "Historique", "Historique supprimé")
        self.mainWindow.logger.debug("Totalité de l'historique supprimé")

    def removeHistory(self, urlToFind):
        found = False
        for i in range(len(self.historyArray) - 1, -1, -1):
            if urlToFind == self.historyArray[i].url:
                del self.historyArray[i]
                found = True
        if found:
            QMessageBox().about(self, "Supprimer", "Cette page n'est plus dans l'historique")
            self.mainWindow.logger.debug("Page %s de l'historique supprimé", urlToFind)
        else:
            QMessageBox().about(self, "Annulation", "Cette page n'est pas dans l'historique")
            self.mainWindow.logger.warning("Page %s n'est pas dans l'historique", urlToFind)

    def openSession(self):
        self.sessionBox.setWindowModality(Qt.ApplicationModal)
        self.sessionBox.showUpdate(self.sessionArray)

    def addSession(self):
        self.addSessionBox.setWindowModality(Qt.ApplicationModal)
        self.addSessionBox.show()

    def removeSession(self):
        self.removeSessionBox.setWindowModality(Qt.ApplicationModal)
        self.removeSessionBox.show()

    def removeAllSession(self):
        self.raccourciArray = []
        QMessageBox().about(self, "Sessions", "Sessions supprimées")
        self.mainWindow.logger.debug("Totalité des sesssions supprimées")

    def openRaccourci(self):
        self.raccourciBox.setWindowModality(Qt.ApplicationModal)
        self.raccourciBox.showUpdate(self.raccourciArray)

    def removeAllRaccourci(self):
        self.raccourciArray = []
        QMessageBox().about(self, "Raccourcis URL", "Raccourcis supprimés")
        self.mainWindow.logger.debug("Totalité de les raccourcis URL supprimés")

    def addRaccourci(self):
        self.addRaccourciBox.setWindowModality(Qt.ApplicationModal)
        self.addRaccourciBox.show()

    def removeRaccourci(self):
        self.removeRaccourciBox.setWindowModality(Qt.ApplicationModal)
        self.removeRaccourciBox.show()

    def openFav(self):
        self.favBox.setWindowModality(Qt.ApplicationModal)
        self.favBox.showUpdate(self.favArray)

    def addFav(self):
        found = False
        for i in self.favArray:
            if self.browser.url().toString() == i.url:
                found = True
        if found:
            QMessageBox().about(self, "Annulation", "Cette page est déjà dans les favoris")
            self.mainWindow.logger.warning("Page %s déja dans les favoris", self.browser.url().toString())
        else:
            self.favArray.append(Item(self, self.browser.title(), self.browser.url().toString()))
            QMessageBox().about(self, "Ajouter", "Cette page est maintenant dans les favoris")
            self.mainWindow.logger.debug("Page %s n'est plus dans les favoris", self.browser.url().toString())

    def removeAllFav(self):
        self.favArray = []
        QMessageBox().about(self, "Favoris", "Favoris supprimé")
        self.mainWindow.logger.debug("Totalité de l'historique supprimé")

    def removeFav(self, url):
        found = False
        for i in range(len(self.favArray) - 1, -1, -1):
            if url == self.favArray[i].url:
                del self.favArray[i]
                found = True
        if found:
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
        elif event.key() == Qt.Key_H:
            self.historyBox.setWindowModality(Qt.ApplicationModal)
            self.historyBox.showUpdate(self.historyArray)
        elif event.key() == Qt.Key_P:
            self.parametresBox.setWindowModality(Qt.ApplicationModal)
            self.parametresBox.show()
        elif event.key() == Qt.Key_S:
            self.sessionBox.setWindowModality(Qt.ApplicationModal)
            self.sessionBox.showUpdate(self.sessionArray)
        elif event.key() == Qt.Key_U:
            self.raccourciBox.setWindowModality(Qt.ApplicationModal)
            self.raccourciBox.showUpdate(self.raccourciArray)
        elif event.key() == Qt.Key_D:
            self.downloadManager.show()
        elif event.key() == Qt.Key_F:
            self.favBox.setWindowModality(Qt.ApplicationModal)
            self.favBox.showUpdate(self.favArray)
        elif event.key() == Qt.Key_L:
            try:
                with open("last.txt", "r") as fichier:
                    contenu = fichier.read().split("\n")
                    for i in range(len(contenu)):
                        if i == 0:
                            self.urlInput.enterUrlGiven(contenu[i])
                        else:
                            self.addOngletWithUrl(contenu[i])
            except:
                QMessageBox().warning(self, "Pas d'ancienne session", "Aucune ancienne session n'a été trouvée")
                self.mainWindow.logger.warning("Tentativement de chargement d'ancienne session alors qu'il n'y en a pas")

    def refreshTheme(self):
        if self.mainWindow.styleSheetParam != "Default":
            with open('style/' + self.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
        else:
            bss = ""
        self.mainWindow.setStyleSheet(bss)
        self.addSessionBox.setStyleSheet(bss)
        self.removeSessionBox.setStyleSheet(bss)
        self.addRaccourciBox.setStyleSheet(bss)
        self.removeRaccourciBox.setStyleSheet(bss)
        self.historyBox.setStyleSheet(bss)
        self.favBox.setStyleSheet(bss)
        self.downloadManager.setStyleSheet(bss)
        self.parametresBox.setStyleSheet(bss)
        self.browthonInfo.setStyleSheet(bss)
        self.pyqtInfo.setStyleSheet(bss)
        self.qtInfo.setStyleSheet(bss)
        self.mainWindow.logger.debug("Thème %s rechargé", self.mainWindow.styleSheetParam)

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
                    if i == len(self.historyArray) - 1:
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
                    if i == len(self.raccourciArray) - 1:
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
                        if y == self.sessionArray[i].urls[len(self.sessionArray[i].urls) - 1]:
                            urls += y
                        else:
                            urls += y + " - "
                    if i == len(self.sessionArray) - 1:
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
                    if i == len(self.favArray) - 1:
                        message += self.favArray[i].title + " | " + self.favArray[i].url
                    else:
                        message += self.favArray[i].title + " | " + self.favArray[i].url + '\n'
                fichier.write(message)
        with open('last.txt', 'w') as fichier:
            contenu = ""
            for i in range(self.tabOnglet.count()):
                if i == self.tabOnglet.count() - 1:
                    contenu += self.tabOnglet.widget(i).url().toString()
                else:
                    contenu += self.tabOnglet.widget(i).url().toString() + "\n"
            fichier.write(contenu)
        self.mainWindow.logger.info("Fermeture de Browthon complète")
