import sys

from PySide.QtWebKit import *
from PySide.QtGui import *
from PySide.QtCore import *

from PyWeb_utils import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = QWidget()

        self.grid = QGridLayout()
        self.browser = QWebView()
        self.onglet1B = QPushButton("O1")
        self.onglet2B = QPushButton("O2")
        self.urlInput = UrlInput(self.browser)
        self.onglet1 = Onglet(1, self, self.onglet1B)
        self.onglet2 = Onglet(2, self, self.onglet2B)
        self.urlEnter = QPushButton("→")
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.parametreB = QPushButton("⁞")
        self.parametres = QMenu("")
        self.informations = QMessageBox()
        
        self.informations.setWindowTitle("Informations sur PyWeb")
        self.informations.setText("V 0.2.1 : Fix Reload Update \n Créé par LavaPower \n Github : https://github.com/LavaPower/PyWeb")
        self.parametres.addAction("Informations", self.informations.open)
        self.onglet1.mainFrame().load(QUrl("http://google.com"))
        self.onglet2.mainFrame().load(QUrl("http://google.com"))
        self.browser.setPage(self.onglet1)
        self.parametreB.setMenu(self.parametres)

        self.urlEnter.clicked.connect(self.urlInput.enterUrl)
        self.browser.urlChanged.connect(self.urlInput.setUrl)
        self.browser.titleChanged.connect(self.setTitle)
        self.back.clicked.connect(self.browser.back)
        self.forward.clicked.connect(self.browser.forward)
        self.reload.clicked.connect(self.browser.reload)
        self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
        self.parametreB.clicked.connect(self.parametreB.showMenu)
        self.onglet1B.clicked.connect(self.onglet1.setOnglet)
        self.onglet2B.clicked.connect(self.onglet2.setOnglet)

        self.grid.addWidget(self.onglet1B, 0, 0)
        self.grid.addWidget(self.onglet2B, 0, 1)
        self.grid.addWidget(self.back, 1, 0)
        self.grid.addWidget(self.reload, 1, 1)
        self.grid.addWidget(self.forward, 1, 2)
        self.grid.addWidget(self.urlInput, 1, 3)
        self.grid.addWidget(self.urlEnter, 1, 4)
        self.grid.addWidget(self.parametreB, 1,5)
        self.grid.addWidget(self.browser, 2, 0, 1, 6)

        self.widget.setLayout(self.grid)

        self.setCentralWidget(self.widget)

    def setTitle(self):
        self.setWindowTitle(self.browser.title()+" - PyWeb")

app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec_()
