#!/usr/bin/python3.6
# coding: utf-8

from PySide.QtWebKit import *
from PySide.QtGui import *
from PySide.QtCore import *

from files.PyWeb_utils import *

class MainWindow(QWidget):
	def __init__(self, url):
		super(MainWindow, self).__init__()
		self.url = url
		self.grid = QGridLayout()
		self.browser = QWebView()
		self.onglets = []
		self.ongletP = QPushButton("+")
		self.onglet1B = ButtonOnglet(self,"O1")
		self.urlInput = UrlInput(self)
		self.onglet1 = Onglet(1, self, self.onglet1B)
		self.onglets.append([self.onglet1,self.onglet1B])
		self.historyB = QPushButton("H")
		self.history = QMenu("")
		self.fav = QPushButton("★") #Inutilisé pour l'instant
		self.back = QPushButton("<")
		self.forward = QPushButton(">")
		self.reload = QPushButton("↺")
		self.parametreB = QPushButton("⁞")
		self.parametres = QMenu("")
		self.informations = QMessageBox()
		self.historyArray = []
		try:
			with open('history.txt'):
				pass
		except IOError:
			pass
		else:
			with open('history.txt','r') as fichier:
				for i in fichier.read().split("\n"):
					self.historyArray.append(i)
		
		self.informations.setWindowTitle("Informations sur PyWeb")
		self.informations.setText("V 0.5.0 : History Update\nCréé par LavaPower \nGithub : https://github.com/LavaPower/PyWeb")
		self.parametres.addAction("Définir Moteur", self.moteurDefine)
		self.parametres.addAction("Fermer Onglet", self.closeOnglet)
		self.parametres.addSeparator()
		self.parametres.addAction("Informations", self.informations.open)
		self.browser.setPage(self.onglet1)
		self.parametreB.setMenu(self.parametres)
		self.historyB.setMenu(self.history)
		self.history.addAction("Supprimer", self.removeHistory)
		self.history.addSeparator()
		for i in self.historyArray:
			item = i.split(" | ")
			hItem = HistoryItem(self, item[0], item[1])
			self.history.addAction(hItem.title, hItem.load)

		self.browser.urlChanged.connect(self.urlInput.setUrl)
		self.browser.titleChanged.connect(self.setTitle)
		self.browser.loadFinished.connect(self.addHistory)
		self.back.clicked.connect(self.browser.back)
		self.forward.clicked.connect(self.browser.forward)
		self.reload.clicked.connect(self.browser.reload)
		self.urlInput.returnPressed.connect(self.urlInput.enterUrl)
		self.parametreB.clicked.connect(self.parametreB.showMenu)
		self.historyB.clicked.connect(self.history.show)
		self.onglet1B.clicked.connect(self.onglet1.setOnglet)
		self.ongletP.clicked.connect(self.addOnglet)

		self.grid.addWidget(self.onglet1B, 0, 0)
		self.grid.addWidget(self.ongletP, 0, 10)
		self.grid.addWidget(self.back, 1, 0)
		self.grid.addWidget(self.reload, 1, 1)
		self.grid.addWidget(self.forward, 1, 2)
		self.grid.addWidget(self.urlInput, 1, 3, 1, 5)
		self.grid.addWidget(self.historyB, 1, 8)
		self.grid.addWidget(self.fav, 1, 9)
		self.grid.addWidget(self.parametreB, 1,10)
		self.grid.addWidget(self.browser, 2, 0, 1, 11)

		self.setLayout(self.grid)
		
		self.moteur = MoteurBox("Moteur par défaut","Choissez le moteur par défaut")

	def setTitle(self):
		self.setWindowTitle(self.browser.title()+" - PyWeb")
		if len(self.browser.title())>=13:
			titre = self.browser.title()[:9]+"..."
		else:
			titre = self.browser.title()
		self.browser.page().button.setText(titre)
		
	def moteurDefine(self):
		self.moteur.setWindowModality(Qt.ApplicationModal)
		self.moteur.show()

	def addOnglet(self):
		find=False
		for i in self.onglets:
			if i[1].isVisible():
				pass
			else:
				i[0].mainFrame().load(QUrl(self.url))
				i[1].show()
				find = True
				break
		if find == False:
			if len(self.onglets) == 10:
				alert = QMessageBox().warning(self, "ERREUR - Trop d'onglet", "Vous avez 10 onglets, soit le maximum possible...")
			else:
				button = ButtonOnglet(self,"O"+str(len(self.onglets)+1))
				onglet = Onglet(len(self.onglets)+1, self, button)
				self.onglets.append([onglet,button])
				button.clicked.connect(onglet.setOnglet)
				self.grid.addWidget(button, 0, len(self.onglets)-1)

	def closeOnglet(self):
		self.browser.page().button.hide()
		find = False
		for i in self.onglets:
			if i[1].isVisible():
				find=True
				self.browser.setPage(i[0])
				break
		if find == False:
			question = QMessageBox().question(self, "Quitter ?","Vous avez fermé le dernier onglet... \nVoulez vous quitter PyWeb ?", QMessageBox.Yes, QMessageBox.No)
			if question == 16384:
				self.close()
			else:
				info = QMessageBox().about(self, "Annulation","Le dernier onglet a donc été réouvert")
				self.browser.page().button.show()

	def addHistory(self):
		self.historyArray.append(self.browser.title()+" | "+self.browser.url().toString())
		hItem = HistoryItem(self, self.browser.title(), self.browser.url().toString())
		self.history.addAction(hItem.title, hItem.load) #Ne fonctionne pas
	
	def removeHistory(self):
		self.historyArray = []
		self.history.clear()
		self.history.addAction("Supprimer", self.removeHistory)
		self.history.addSeparator()
	
	def keyPressEvent(self,event):
		if event.key() == 16777268:
			self.browser.reload()
		elif event.key() == 16777273:
			self.parametreB.showMenu()
	
	def closeEvent(self, event):
		if self.historyArray == []:
			try:
				with open('history.txt'):
					pass
			except IOError:
				pass
			else:
				os.remove('history.txt')
		else:
			with open('history.txt','w') as fichier:
				message = ""
				for i in range(len(self.historyArray)):
					if i == len(self.historyArray)-1:
						message += self.historyArray[i]
					else:
						message += self.historyArray[i] + "\n"
				fichier.write(message)
