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
        for i in self.main.raccourciArray:
            if urlT == i.title:
                urlT = i.url
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
        self.addTab(main.onglet1, QIcon('logo.png'), "Browthon")
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
        self.load(QUrl(main.urltemp))
        self.main.urltemp = self.main.url
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
    