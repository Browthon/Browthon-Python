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
                self.clickedUrl = self.page.hitTestContent(event.pos()).linkUrl()
                if self.clickedUrl.isEmpty():
                    pass
                else:
                    self.main.addOngletWithUrl(self.clickedUrl.toString())
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
        self.source = "(function() {\n"+"var e = document.elementFromPoint("+str(self.viewportPos.x())+", "+str(self.viewportPos.y())+");\n"+"if (!e)\n"+"    return;\n"+"function isMediaElement(e) {\n"+"    return e.tagName == 'AUDIO' || e.tagName == 'VIDEO';\n"+"}\n"+"function isEditableElement(e) {\n"+"    if (e.isContentEditable)\n"+"        return true;\n"+"    if (e.tagName == 'INPUT' || e.tagName == 'TEXTAREA')\n"+"        return e.getAttribute('readonly') != 'readonly';\n"+"    return false;\n"+"}\n"+"function isSelected(e) {\n"+"    var selection = window.getSelection();\n"+"    if (selection.type != 'Range')\n"+"        return false;\n"+"    return window.getSelection().containsNode(e, true);\n"+"}\n"+"var res = {\n"+"    baseUrl: document.baseURI,\n"+"    alternateText: e.getAttribute('alt'),\n"+"    boundingRect: '',\n"+"    imageUrl: '',\n"+"    contentEditable: isEditableElement(e),\n"+"    contentSelected: isSelected(e),\n"+"    linkTitle: '',\n"+"    linkUrl: '',\n"+"    mediaUrl: '',\n"+"    tagName: e.tagName.toLowerCase()\n"+"};\n"+"var r = e.getBoundingClientRect();\n"+"res.boundingRect = [r.top, r.left, r.width, r.height];\n"+"if (e.tagName == 'IMG')\n"+"    res.imageUrl = e.getAttribute('src');\n"+"if (e.tagName == 'A') {\n"+"    res.linkTitle = e.text;\n"+"    res.linkUrl = e.getAttribute('href');\n"+"}\n"+"while (e) {\n"+"    if (res.linkTitle == ''& & e.tagName == 'A')\n"+"        res.linkTitle = e.text;\n"+"    if (res.linkUrl == ''& & e.tagName == 'A')\n"+"        res.linkUrl = e.getAttribute('href');\n"+"    if (res.mediaUrl == ''& & isMediaElement(e)) {\n"+"        res.mediaUrl = e.currentSrc;\n"+"        res.mediaPaused = e.paused;\n"+"        res.mediaMuted = e.muted;\n"+"    }\n"+"    e = e.parentElement;\n"+"}\n"+"return res;\n"+"})()"


        self.js = self.source
        self.url = self.page.url()
        self.temp = self.page.executeJavaScript(self.js)
        if self.temp == None:
            return
        self.map = self.temp.toMap()

        if self.map.isEmpty():
            return

        self.m_isNull = False
        self.m_baseUrl = self.map.value(QStringLiteral("baseUrl")).toUrl()
        self.m_alternateText = self.map.value(QStringLiteral("alternateText")).toString()
        self.m_imageUrl = self.map.value(QStringLiteral("imageUrl")).toUrl()
        self.m_isContentEditable = self.map.value(QStringLiteral("contentEditable")).toBool()
        self.m_isContentSelected = self.map.value(QStringLiteral("contentSelected")).toBool()
        self.m_linkTitle = self.map.value(QStringLiteral("linkTitle")).toString()
        self.m_linkUrl = self.map.value(QStringLiteral("linkUrl")).toUrl()
        self.m_mediaUrl = self.map.value(QStringLiteral("mediaUrl")).toUrl()
        self.m_mediaPaused = self.map.value(QStringLiteral("mediaPaused")).toBool()
        self.m_mediaMuted = self.map.value(QStringLiteral("mediaMuted")).toBool()
        self.m_tagName = self.map.value(QStringLiteral("tagName")).toString()

        if self.m_imageUrl.isEmpty():
            pass
        else:
            self.m_imageUrl = self.url.resolved(self.m_imageUrl)
        if self.m_linkUrl.isEmpty():
            pass
        else:
            self.m_linkUrl = self.m_baseUrl.resolved(self.m_linkUrl)
        if self.m_mediaUrl.isEmpty():
            pass
        else:
            self.m_mediaUrl = self.url.resolved(self.m_mediaUrl)
    
    def linkUrl(self):
	    return self.m_linkUrl


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
        self.grid.addWidget(self.b1, 2, 1)
        n=0
        for i in glob.glob('style/*.pss'):
            self.btemp = QPushButton(i.replace('style/', "").replace(".pss", ""))
            self.btemp.clicked.connect(lambda: self.choose(i.replace('style/', "").replace(".pss", "")))
            self.grid.addWidget(self.btemp, 3+n, 1)
            n+=1
        
        self.setLayout(self.grid)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".pss", 'r') as fichier:
                self.setStyleSheet(fichier.read())
        
    def choose(self, choix):
        print(choix)
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
