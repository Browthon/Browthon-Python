from PySide.QtWebKit import *
from PySide.QtGui import *
from PySide.QtCore import *

class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput,self).__init__("http://google.com")
        self.browser = browser

    def enterUrl(self):
        urlT = self.text()
        if "http://" in urlT or "https://" in urlT:
            url = QUrl(urlT)
        else:
            urlT = "http://"+urlT
            url = QUrl(urlT)
        self.browser.load(url)

    def setUrl(self):
        self.setText(self.browser.url().toString())

class Onglet(QWebPage):
    def __init__(self, nb, main, button):
        super(Onglet,self).__init__()
        self.nb = nb
        self.browser = main.browser
        self.urlInput = main.urlInput
        self.button = button
        self.main = main
            
    def setOnglet(self):
        self.browser.setPage(self)
        self.urlInput.setUrl()
        self.main.setTitle()
