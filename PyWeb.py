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
        self.onglets = []
        self.ongletP = QPushButton("+")
        self.onglet1B = QPushButton("O1")
        self.urlInput = UrlInput(self.browser)
        self.onglet1 = Onglet(1, self, self.onglet1B)
        self.onglets.append([self.onglet1,self.onglet1B])
        self.urlEnter = QPushButton("→")
        self.back = QPushButton("<")
        self.forward = QPushButton(">")
        self.reload = QPushButton("↺")
        self.parametreB = QPushButton("⁞")
        self.parametres = QMenu("")
        self.informations = QMessageBox()
        
        self.informations.setWindowTitle("Informations sur PyWeb")
        self.informations.setText("V 0.3.0 : Tab Update \n Créé par LavaPower \n Github : https://github.com/LavaPower/PyWeb")
        self.parametres.addAction("Fermer Onglet", self.closeOnglet)
        self.parametres.addAction("Informations", self.informations.open)
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
        self.ongletP.clicked.connect(self.addOnglet)

        self.grid.addWidget(self.onglet1B, 0, 0)
        self.grid.addWidget(self.ongletP, 0, 10)
        self.grid.addWidget(self.back, 1, 0)
        self.grid.addWidget(self.reload, 1, 1)
        self.grid.addWidget(self.forward, 1, 2)
        self.grid.addWidget(self.urlInput, 1, 3, 1, 6)
        self.grid.addWidget(self.urlEnter, 1, 9)
        self.grid.addWidget(self.parametreB, 1,10)
        self.grid.addWidget(self.browser, 2, 0, 1, 11)

        self.widget.setLayout(self.grid)

        self.setCentralWidget(self.widget)

    def setTitle(self):
        self.setWindowTitle(self.browser.title()+" - PyWeb")
        if len(self.browser.title())>=13:
            titre = self.browser.title()[:9]+"..."
        else:
            titre = self.browser.title()
        self.browser.page().button.setText(titre)

    def addOnglet(self):
        find=False
        for i in self.onglets:
            if i[1].isVisible():
                pass
            else:
                i[0].mainFrame().load(QUrl("http://google.com"))
                i[1].show()
                find = True
                break
        if find == False:
            if len(self.onglets) == 10:
                alert = QMessageBox().warning(self, "ERREUR - Trop d'onglet", "Vous avez 10 onglets, soit le maximum possible...")
            else:
                button = QPushButton("O"+str(len(self.onglets)+1))
                onglet = Onglet(len(self.onglets)+1, self, button)
                self.onglets.append([onglet,button])
                button.clicked.connect(onglet.setOnglet)
                self.grid.addWidget(button, 0, len(self.onglets)-1)

    def closeOnglet(self):
        self.browser.page().button.hide()

app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec_()
