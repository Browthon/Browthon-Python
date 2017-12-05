import sys

from PySide.QtWebKit import QWebView
from PySide.QtGui import QMessageBox, QApplication, QGridLayout, QLineEdit, QWidget, QPushButton, QMenu, QMainWindow
from PySide.QtCore import *

class UrlInput(QLineEdit):
    def __init__(self, browser):
        super(UrlInput,self).__init__("http://google.com")
        self.browser = browser

    def enterUrl(self):
        url = QUrl(self.text())
        self.browser.load(url)

    def setUrl(self):
        self.setText(self.browser.url().toString())

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()

        self.grid = QGridLayout()
        self.browser = QWebView()
        self.browser.load(QUrl("http://google.com"))
        self.urlInput = UrlInput(self.browser)
        self.urlEnter = QPushButton("→")
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.parametreB = QPushButton("⁞")
        self.parametres = QMenu("")
        self.informations = QMessageBox()
        self.informations.setWindowTitle("Informations sur PyWeb")
        self.informations.setText("V 0.1.0 : Url Update \n Créé par LavaPower \n Github : https://github.com/LavaPower/PyWeb")

        self.parametres.addAction("Informations", self.informations.open)

        self.parametreB.setMenu(self.parametres)

        self.urlEnter.clicked.connect(self.urlInput.enterUrl)
        self.browser.urlChanged.connect(self.urlInput.setUrl)
        self.browser.titleChanged.connect(self.setTitle)
        self.back.clicked.connect(self.browser.back)
        self.forward.clicked.connect(self.browser.forward)
        self.reload.clicked.connect(self.browser.reload)
        self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
        self.parametreB.clicked.connect(self.parametreB.showMenu)

        self.grid.addWidget(self.back, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.forward, 0, 2)
        self.grid.addWidget(self.urlInput, 0, 3)
        self.grid.addWidget(self.urlEnter, 0, 4)
        self.grid.addWidget(self.parametreB, 0,5)
        self.grid.addWidget(self.browser, 1, 0, 1, 6)

        self.widget.setLayout(self.grid)

        self.setCentralWidget(self.widget)

    def setTitle(self):
        self.setWindowTitle(self.browser.title())
        
        

app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec_()
