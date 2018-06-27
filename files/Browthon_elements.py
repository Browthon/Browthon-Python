#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.Browthon_utils import *

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
                    with open('config.txt', 'r') as fichier:
                        moteur = fichier.read().split("\n")[0].split(" ")[1]
                except IOError:
                    moteur = "https://www.google.fr/?gws_rd=ssl#q="
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
    
    def contextMenuEvent(self, event):
        hit = self.page.hitTestContent(event.pos())
        menu = ContextMenu(self, hit)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/'+self.main.mainWindow.styleSheetParam+".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                bss = fichier.read()
        else:
            bss = ""
        menu.setStyleSheet(bss)
        pos = event.globalPos()
        p = QPoint(pos.x(), pos.y() + 1)
        menu.exec_(p)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.MiddleButton:
                hit = self.page.hitTestContent(event.pos())
                clickedUrl = hit.linkUrl()
                baseUrl = hit.baseUrl()
                if clickedUrl != baseUrl and clickedUrl != '':
                    if 'http://' in clickedUrl or 'https://' in clickedUrl:
                        result = clickedUrl
                    elif clickedUrl == "#":
                        result = baseUrl+clickedUrl
                    else:
                        result = "http://"+baseUrl.split("/")[2]+clickedUrl
                    self.main.addOngletWithUrl(result)
                event.accept()
                return True
        return super(Onglet, self).eventFilter(obj, event)
    

class Page(QWebEnginePage):
    def __init__(self, view):
        super(Page, self).__init__()
        self.main = view.main
        self.view = view
        self.loop = None

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        """Override javaScriptConsoleMessage to use debug log."""
        if level == QWebEnginePage.InfoMessageLevel:
            self.main.mainWindow.logger.info("JS - Ligne {} : {}".format(line, msg))
        elif level == QWebEnginePage.WarningMessageLevel:
            self.main.mainWindow.logger.warning("JS - Ligne {} : {}".format(line, msg))
        else:
            self.main.mainWindow.logger.error("JS - Ligne {} : {}".format(line, msg))
    
    def hitTestContent(self, pos):
        return WebHitTestResult(self, pos)
    
    def mapToViewport(self, pos):
	    return QPointF(pos.x(), pos.y())
    
    def executeJavaScript(self, scriptSrc):
        self.loop = QEventLoop()
        self.result = QVariant()
        QTimer.singleShot(250, self.loop.quit)

        self.runJavaScript(scriptSrc, self.callbackJS)
        self.loop.exec_()
        self.loop = None
        return self.result

    def callbackJS(self, res):
        if self.loop != None and self.loop.isRunning():
            self.result = res
            self.loop.quit()

    def vSource(self):
        if "view-source:http" in self.url().toString():
            self.load(QUrl(self.url().toString().split("view-source:")[1]))
        else:
            self.triggerAction(self.ViewSource)
    
    def cutAction(self):
        self.triggerAction(self.Cut)
    
    def copyAction(self):
        self.triggerAction(self.Copy)
    
    def pasteAction(self):
        self.triggerAction(self.Paste)
    
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