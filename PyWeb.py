import sys

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication, QGridLayout, QLineEdit, QWidget, QPushButton
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
urlEnter = QPushButton("Entrer")
back = QPushButton("<")
forward = QPushButton(">")

urlEnter.clicked.connect(urlInput.enterUrl)
browser.urlChanged.connect(urlInput.setUrl)
back.clicked.connect(browser.back)
forward.clicked.connect(browser.forward)

grid.addWidget(back, 0, 0)
grid.addWidget(forward, 0, 1)
grid.addWidget(urlInput, 0, 2)
grid.addWidget(urlEnter, 0, 3)
grid.addWidget(browser, 1, 0, 1, 4)

main = QWidget()
main.setLayout(grid)
main.show()

app.exec_()
