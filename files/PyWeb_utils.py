#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


class UrlInput(QLineEdit):
    def __init__(self, main):
        super(UrlInput, self).__init__(main.url)
        self.main = main

    def enterUrl(self):
        urlT = self.text()
        if "http://" in urlT or "https://" in urlT:
            url = QUrl(urlT)
        else:
            if "." in urlT:
                urlT = "http://"+urlT
                url = QUrl(urlT)
            else:
                moteur = ""
                try:
                    with open('config.txt'):
                        pass
                except IOError:
                    moteur = "https://www.google.fr/?gws_rd=ssl#q="
                else:
                    with open('config.txt', 'r') as fichier:
                        moteur = fichier.read().split("\n")[0].split(" ")[1]
                urlT = moteur+urlT
                url = QUrl(urlT)
        self.main.browser.load(url)

    def enterUrlGiven(self, url):
        urlT = url
        if "http://" in urlT or "https://" in urlT:
            url = QUrl(urlT)
        else:
            urlT = "http://"+urlT
            url = QUrl(urlT)
        self.main.browser.load(url)

    def setUrl(self):
        self.setText(self.main.browser.url().toString())


class TabOnglet(QTabWidget):
    def __init__(self, main):
        super(TabOnglet, self).__init__()
        self.setTabPosition(QTabWidget.North)
        self.setMovable(True)
        self.addTab(main.onglet1, "PyWeb")
        self.main = main
        self.main.browser.show()

    def changeOnglet(self):
        self.main.browser = self.currentWidget()
        self.main.urlInput.setUrl()
        self.main.setTitle()
        self.main.addHistory()
        self.main.forward.disconnect()
        self.main.back.disconnect()
        self.main.reload.disconnect()
        self.main.back.clicked.connect(self.main.browser.back)
        self.main.forward.clicked.connect(self.main.browser.forward)
        self.main.reload.clicked.connect(self.main.browser.reload)


class Onglet(QWebEngineView):
    def __init__(self, nb, main):
        super(Onglet, self).__init__()
        self.nb = nb
        self.main = main
        self.page = Page(self)
        self.setPage(self.page)
        self.load(QUrl(main.url))
        self.urlChanged.connect(main.urlInput.setUrl)
        self.titleChanged.connect(main.setTitle)
        self.loadFinished.connect(main.addHistory)
        self.page.fullScreenRequested.connect(self.page.makeFullScreen)


class Page(QWebEnginePage):
    def __init__(self, view):
        super(Page, self).__init__()
        self.main = view.main
        self.view = view
    
    def ExitFS(self):
        self.triggerAction(self.ExitFullScreen)
    
    def makeFullScreen(self, request):
        if request.toggleOn():
            self.fullView = QWebEngineView()
            self.exitFSAction = QAction(self.fullView)
            self.exitFSAction.setShortcut(Qt.Key_Escape)
            self.exitFSAction.triggered.connect(self.ExitFS)
        
            self.fullView.addAction(self.exitFSAction)
            self.setView(self.fullView)
            self.fullView.showFullScreen()
            self.fullView.raise_()
        else:
            del self.fullView
            self.setView(self.view)
        request.accept()


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


class MoteurBox(QWidget):
    def __init__(self, title, text):
        super(MoteurBox, self).__init__()
        
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


class Item:
    def __init__(self, main, title, url):
        self.main = main
        self.url = url
        self.title = title
    
    def setInteraction(self, menu):
        menu.addAction(self.title, self.load)

    def load(self):
        self.main.urlInput.enterUrlGiven(self.url)
