import sys

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QMessageBox, QApplication, QGridLayout, QLineEdit, QWidget, QPushButton, QMenu
from PyQt4.QtCore import *

class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput,self).__init__("http://google.com")
        self.browser = browser

    def enterUrl(self):
        url = QUrl(self.text())
        browser.load(url)

    def setUrl(self):
        self.setText(browser.url().toString())


app = QApplication(sys.argv)

grid = QGridLayout()
browser = QWebView()
browser.load(QUrl("http://google.com"))
urlInput = UrlInput(browser)
urlEnter = QPushButton("→")
back = QPushButton("<")
forward = QPushButton(">")
reload = QPushButton("↺")
parametreB = QPushButton("⁞")
parametres = QMenu("")
informations = QMessageBox()
informations.setWindowTitle("Informations sur PyWeb")
informations.setText("V 0.1.0 : Url Update \n Créé par LavaPower \n Github : https://github.com/LavaPower/PyWeb")

parametres.addAction("Informations", informations.open)

parametreB.setMenu(parametres)

urlEnter.clicked.connect(urlInput.enterUrl)
browser.urlChanged.connect(urlInput.setUrl)
back.clicked.connect(browser.back)
forward.clicked.connect(browser.forward)
reload.clicked.connect(browser.forward)
urlInput.returnPressed.connect(urlInput.enterUrl)
parametreB.clicked.connect(parametreB.showMenu)

grid.addWidget(back, 0, 0)
grid.addWidget(reload, 0, 1)
grid.addWidget(forward, 0, 2)
grid.addWidget(urlInput, 0, 3)
grid.addWidget(urlEnter, 0, 4)
grid.addWidget(parametreB, 0,5)
grid.addWidget(browser, 1, 0, 1, 6)

main = QWidget()
main.setLayout(grid)
main.show()

app.exec_()
