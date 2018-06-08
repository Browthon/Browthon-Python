#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import os, glob


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
        self.addTab(main.onglet1, QIcon('pyweb.png'), "PyWeb")
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
        self.iconChanged.connect(main.changeIcon)
        self.loadFinished.connect(main.addHistory)
        self.page.fullScreenRequested.connect(self.page.makeFullScreen)
        self.viewSource = QAction(self)
        self.viewSource.setShortcut(Qt.Key_F2)
        self.viewSource.triggered.connect(self.page.vSource)
        self.addAction(self.viewSource)
    
    def event(self, event):
        if event.type() == QEvent.ChildAdded:
            child_ev = event
            widget = child_ev.child()

            if widget:
                widget.installEventFilter(self)
            return True
            
        return super(Onglet, self).event(event)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.MiddleButton:
                temp = self.page.hitTestContent(event.pos())
                self.clickedUrl = temp.linkUrl()
                self.baseUrl = temp.baseUrl()
                print(self.clickedUrl)
                if self.clickedUrl != self.baseUrl and self.clickedUrl != '':
                    if 'http://' in self.clickedUrl or 'https://' in self.clickedUrl:
                        self.main.addOngletWithUrl(self.clickedUrl)
                    else:
                        self.main.addOngletWithUrl("http://"+self.baseUrl.split("/")[2]+self.clickedUrl)
                    event.accept()
                    return True
        return super(Onglet, self).eventFilter(obj, event)
    

class Page(QWebEnginePage):
    def __init__(self, view):
        super(Page, self).__init__()
        self.main = view.main
        self.view = view
    
    def hitTestContent(self, pos):
        return WebHitTestResult(self, pos)
    
    def mapToViewport(self, pos):
	    return QPointF(pos.x(), pos.y())
    
    def executeJavaScript(self, scriptSrc):
        self.loop = QEventLoop()
        self.result = QVariant()
        QTimer.singleShot(500, self.loop.quit)

        self.runJavaScript(scriptSrc, self.callbackJS)
        self.loop.exec_()
        del self.loop
        return self.result

    def callbackJS(self, res):
        if self.loop and self.loop.isRunning():
            self.result = res
            self.loop.quit()

    def vSource(self):
        if "view-source:http" in self.url().toString():
            self.load(QUrl(self.url().toString().split("view-source:")[1]))
        else:
            self.triggerAction(self.ViewSource)
    
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


class WebHitTestResult():
    def __init__(self, page, pos):
        self.page = page
        self.pos = pos
        self.m_linkUrl = self.page.url()
        self.viewportPos = self.page.mapToViewport(self.pos)
        self.source = """(function() {
        let e = document.elementFromPoint(%1, %2)
        if (!e)
            return;
        function isMediaElement(e) {
            return e.tagName == 'AUDIO' || e.tagName == 'VIDEO';
        }
        function isEditableElement(e) {
            if (e.isContentEditable)
                return true;
            if (e.tagName === 'INPUT' || e.tagName === 'TEXTAREA')
                return e.getAttribute('readonly') != 'readonly';
            return false;
        }
        function isSelected(e) {
            let selection = window.getSelection();
            if (selection.type !== 'Range')
                return false;
            return window.getSelection().containsNode(e, true);
        }
        let res = {
            baseUrl: document.baseURI,
            alternateText: e.getAttribute('alt'),
            boundingRect: '',
            imageUrl: '',
            contentEditable: isEditableElement(e),
            contentSelected: isSelected(e),
            linkTitle: '',
            linkUrl: '',
            mediaUrl: '',
            tagName: e.tagName.toLowerCase()
        };
        let r = e.getBoundingClientRect();
        res.boundingRect = [r.top, r.left, r.width, r.height];
        if (e.tagName == 'IMG')
            res.imageUrl = e.getAttribute('src');
        if (e.tagName == 'A') {
            res.linkTitle = e.text;
            res.linkUrl = e.getAttribute('href');
        }
        while (e) {
            if (res.linkTitle === '' && e.tagName === 'A') {
                res.linkTitle = e.text;
        	    if(res.linkUrl === '') {
        		res.linkUrl = e.getAttribute('href');
        	    }
        	}
            if (res.mediaUrl === '' && isMediaElement(e)) {
                res.mediaUrl = e.currentSrc;
                res.mediaPaused = e.paused;
                res.mediaMuted = e.muted;
            }
            e = e.parentElement;
        }
        return res;
        })()"""
        
        self.js = self.source.replace("%1", str(self.viewportPos.x())).replace("%2", str(self.viewportPos.y()))
        self.url = self.page.url()
        self.dic = self.page.executeJavaScript(self.js)
        if self.dic == None:
            return

        self.m_isNull = False
        self.m_baseUrl = self.dic["baseUrl"]
        self.m_alternateText = self.dic["alternateText"]
        self.m_imageUrl = self.dic["imageUrl"]
        self.m_isContentEditable = self.dic["contentEditable"]
        self.m_isContentSelected = self.dic["contentSelected"]
        self.m_linkTitle = self.dic["linkTitle"]
        self.m_linkUrl = self.dic["linkUrl"]
        self.m_tagName = self.dic["tagName"]
    
    def linkUrl(self):
	    return self.m_linkUrl
    
    def baseUrl(self):
        return self.m_baseUrl


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
                self.main.sessionArray.append(ItemSession(self, self.result, urls))
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
                info = QMessageBox().about(self, "Session supprimée", "La session "+self.result+" a été supprimée !")
            else:
                info = QMessageBox().about(self, "Session non trouvée", "La session "+self.result+" n'a pas été trouvé !")
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
        alert = QMessageBox().warning(self, self.main.texts[48], self.main.texts[49])

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
                alert = QMessageBox().warning(self, "Style inconnu", "Le style "+choix+" n'est pas reconnu par PyWeb.")
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


class LangBox(QWidget):
    def __init__(self, main, title, text):
        super(LangBox, self).__init__()
        
        self.main = main
        
        self.setWindowTitle(title)
        self.grid = QGridLayout()

        self.Texte = QLabel(text)
        self.French = QPushButton("Francais")
        self.English = QPushButton("English")

        self.French.clicked.connect(self.setFrench)
        self.English.clicked.connect(self.setEnglish)

        self.grid.addWidget(self.Texte, 1, 1, 1, 2)
        self.grid.addWidget(self.French, 2, 1)
        self.grid.addWidget(self.English, 2, 2)

        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())

    def setFrench(self):
        self.setLang("FR")

    def setEnglish(self):
        self.setLang("EN")

    def setLang(self, txt):
        try:
            with open('config.txt'):
                pass
        except IOError:
            pass
        else:
            contenu = []
            with open('config.txt', 'r') as fichier:
                contenu = fichier.read().split('\n')
                contenu[5] = contenu[5].split(" ")[0]+" "+txt
            contenu = "\n".join(contenu)
            with open('config.txt', 'w') as fichier:
                fichier.write(contenu)
        self.close()
        alert = QMessageBox().warning(self, self.main.texts[48], self.main.texts[49])


class Item:
    def __init__(self, main, title, url):
        self.main = main
        self.url = url
        self.title = title
    
    def setInteraction(self, menu):
        menu.addAction(self.title, self.load)

    def load(self):
        self.main.urlInput.enterUrlGiven(self.url)

class ItemSession:
    def __init__(self, main, title, urls):
        self.main = main
        self.urls = urls
        self.title = title
    
    def setInteraction(self, menu):
        menu.addAction(self.title, self.load)
    
    def load(self):
        for i in self.urls:
            self.main.addOngletWithUrl(i)
