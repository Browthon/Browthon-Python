#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import os, zipfile


def parseTheme(bssString):
    bssList = bssString.split("\n")
    i = 0
    while i < len(bssList):
        if bssList[i] != "":
            if bssList[i][0] == "#":
                del bssList[i]
        i += 1
    bssString = "\n".join(bssList)
    bssString.replace("bproperty", "qproperty")
    bssString.replace("blineargradient", "qlineargradient")

    bssString.replace("\\4", "")

    return bssString

def dezip(filezip, pathdst = ''): 
    if pathdst == '': pathdst = os.getcwd() 
    zfile = zipfile.ZipFile(filezip, 'r') 
    for i in zfile.namelist(): 
        if os.path.isdir(i): 
            try: 
                os.makedirs(pathdst + os.sep + i) 
            except: 
                pass 
        else: 
            try: 
                os.makedirs(pathdst + os.sep + os.path.dirname(i)) 
            except: 
                pass 
            data = zfile.read(i)                  
            try:
                fp = open(pathdst + os.sep + i, "wb") 
                fp.write(data)                 
                fp.close() 
            except IsADirectoryError:
                pass
    zfile.close()


class ListWidget(QListWidget):
    def __init__(self, liste):
        super(ListWidget, self).__init__()
        self.liste = liste
        for i in self.liste:
            self.addItem(i.title)

    def deleteAllItems(self):
        for i in range(self.count() - 1, -1, -1):
            self.takeItem(i)

    def updateList(self, liste):
        self.liste = liste
        self.deleteAllItems()
        for i in self.liste:
            self.addItem(i.title)


class ContextMenu(QMenu):
    def __init__(self, onglet, hitTest):
        super(ContextMenu, self).__init__()
        self.onglet = onglet
        contextMenuData = self.onglet.page.contextMenuData()
        hitTest.updateWithContextMenuData(contextMenuData)
        self.addAction("Retour", self.onglet.back)
        self.addAction("Avancer", self.onglet.forward)
        self.addAction("Recharger", self.onglet.reload)
        self.addSeparator()
        self.addAction("Source", self.onglet.page.vSource)
        temp = False
        for i in self.onglet.main.favArray:
            if self.onglet.main.browser.url().toString() == i.url:
                temp = True
        if temp:
            self.addAction("Supprimer Favori", self.onglet.main.suppFav)
        else:
            self.addAction("Ajouter Favori", self.onglet.main.addFav)
        if hitTest.isContentEditable():
            self.addSeparator()
            self.addAction("Couper", self.onglet.page.cutAction)
            self.addAction("Copier", self.onglet.page.copyAction)
            self.addAction("Coller", self.onglet.page.pasteAction)
        if hitTest.imageUrl() != "":
            self.addSeparator()
            self.addAction("Voir Image", lambda: self.onglet.main.addOngletWithUrl(hitTest.imageUrl()))
        self.addSeparator()
        clickedUrl = hitTest.linkUrl()
        baseUrl = hitTest.baseUrl()
        if clickedUrl != baseUrl and clickedUrl != '':
            if 'http://' in clickedUrl or 'https://' in clickedUrl:
                url = clickedUrl
            elif clickedUrl == "#":
                url = baseUrl + clickedUrl
            else:
                url = "http://" + baseUrl.split("/")[2] + clickedUrl
            self.addAction("Ouvrir Nouvel Onglet", lambda: self.onglet.main.addOngletWithUrl(url))


class WebHitTestResult():
    def __init__(self, page, pos):
        self.page = page
        self.pos = pos
        self.m_linkUrl = self.page.url().toString()
        self.m_baseUrl = self.page.url().toString()
        self.viewportPos = self.page.mapToViewport(self.pos)
        self.source = """(function() {
        let e = document.elementFromPoint(%1, %2);
        if (!e)
            return;
        function isMediaElement(e) {
            return e.tagName == 'AUDIO' || e.tagName == 'VIDEO';
        };
        function isEditableElement(e) {
            if (e.isContentEditable)
                return true;
            if (e.tagName === 'INPUT' || e.tagName === 'TEXTAREA')
                return e.getAttribute('readonly') != 'readonly';
            return false;
        };
        function isSelected(e) {
            let selection = window.getSelection();
            if (selection.type !== 'Range')
                return false;
            return window.getSelection().containsNode(e, true);
        };
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
        self.dic = self.page.executeJavaScript(self.js)
        if self.dic is None:
            return

        self.m_isNull = False
        self.m_baseUrl = self.dic["baseUrl"]
        self.m_alternateText = self.dic["alternateText"]
        self.m_imageUrl = self.dic["imageUrl"]
        self.m_isContentEditable = self.dic["contentEditable"]
        self.m_isContentSelected = self.dic["contentSelected"]
        self.m_linkTitle = self.dic["linkTitle"]
        self.m_linkUrl = self.dic["linkUrl"]
        self.m_mediaUrl = self.dic["mediaUrl"]
        try:
            self.m_mediaPaused = self.dic["mediaPaused"]
            self.m_mediaMuted = self.dic["mediaMuted"]
        except:
            pass
        self.m_tagName = self.dic["tagName"]

    def linkUrl(self):
        return self.m_linkUrl

    def isContentEditable(self):
        return self.m_isContentEditable

    def isContentSelected(self):
        return self.m_isContentSelected

    def imageUrl(self):
        try:
            return self.m_imageUrl
        except:
            return ""

    def mediaUrl(self):
        return self.m_mediaUrl

    def baseUrl(self):
        return self.m_baseUrl

    def updateWithContextMenuData(self, data):
        if data.isValid():
            pass
        else:
            return

        self.m_linkTitle = data.linkText()
        self.m_linkUrl = data.linkUrl().toString()
        self.m_isContentEditable = data.isContentEditable()
        if data.selectedText() == "":
            self.m_isContentSelected = False
        else:
            self.m_isContentSelected = True

        if data.mediaType() == QWebEngineContextMenuData.MediaTypeImage:
            self.m_imageUrl = data.mediaUrl().toString()
        elif data.mediaType() == QWebEngineContextMenuData.MediaTypeAudio or data.mediaType() == QWebEngineContextMenuData.MediaTypeVideo:
            self.m_mediaUrl = data.mediaUrl().toString()

class Item:
    def __init__(self, main, title, url):
        self.main = main
        self.url = url
        self.title = title

    def setInteraction(self, menu):
        menu.addAction(self.title, self.load)

    def load(self):
        self.main.addOngletWithUrl(self.url)

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
