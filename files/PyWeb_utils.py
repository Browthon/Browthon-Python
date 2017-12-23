#!/usr/bin/python3.6
# coding: utf-8

from PySide.QtWebKit import *
from PySide.QtGui import *
from PySide.QtCore import *

class UrlInput(QLineEdit):
	def __init__(self, main):
		super(UrlInput,self).__init__(main.url)
		self.browser = main.browser

	def enterUrl(self):
		urlT = self.text()
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
					with open('config.txt','r') as fichier:
						moteur = fichier.read().split("\n")[0]
				urlT = moteur+urlT
				url = QUrl(urlT)
		self.browser.load(url)
	
	def enterUrlGiven(self, url):
		urlT = url
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
		self.button = button
		self.main = main
		self.mainFrame().load(QUrl(main.url))
			
	def setOnglet(self):
		self.main.browser.setPage(self)
		self.main.urlInput.setUrl()
		self.main.setTitle()
	
class MoteurBox(QWidget):
	def __init__(self, title, text):
		super(MoteurBox, self).__init__()
		self.setWindowTitle(title)
		self.grid = QGridLayout()
		
		Texte = QLabel(text)
		Google = QPushButton("Google")
		DDGo = QPushButton("DuckDuckGo")
		Ecosia = QPushButton("Ecosia")
		Yahoo = QPushButton("Yahoo")
		Bing = QPushButton("Bing")
		
		Google.clicked.connect(self.setGoogle)
		DDGo.clicked.connect(self.setDDGo)
		Ecosia.clicked.connect(self.setEcosia)
		Yahoo.clicked.connect(self.setYahoo)
		Bing.clicked.connect(self.setBing)
		
		self.grid.addWidget(Texte, 1,1,2,1)
		self.grid.addWidget(Google, 2,1,1,1)
		self.grid.addWidget(DDGo, 2,2,1,1)
		self.grid.addWidget(Ecosia, 3,1,1,1)
		self.grid.addWidget(Yahoo, 3,2,1,1)
		self.grid.addWidget(Bing, 4,1,2,1)
		
		self.setLayout(self.grid)
	
	def setGoogle(self):
		self.setMoteur("https://www.google.fr/?gws_rd=ssl#q=")
	
	def setDDGo(self):
		self.setMoteur("https://duckduckgo.com/?q=")
	
	def setEcosia(self):
		self.setMoteur("https://www.ecosia.org/search?q=")
	
	def setYahoo(self):
		self.setMoteur("https://fr.search.yahoo.com/search?p=")
	
	def setBing(self):
		self.setMoteur("https://www.bing.com/search?q=")
	
	def setMoteur(self, txt):
		with open('config.txt','w') as fichier:
			fichier.write(txt+"\nhttps://lavapower.github.io/pyweb.html")
		self.close()

class ButtonOnglet(QPushButton):
	def __init__(self,main,text):
		super(ButtonOnglet,self).__init__(text)
		self.main = main

	def showEvent(self, e):
		for i in self.main.onglets:
			if i[1] == self:
				names = self.main.url.split(".")
				nom = names[0].replace("https://","")
				nom = nom.replace("http://","")
				first = nom[0].upper()
				nom = first + nom[1:]
				
				if len(nom)>=13:
					titre = nom[:9]+"..."
				else:
					titre = nom
				self.setText(titre) 

class HistoryItem:
	def __init__(self, main, title, url):
		self.main = main
		self.url = url
		self.title = title
	
	def load(self):
		print("tet")
		self.main.urlInput.enterUrlGiven(self.url)
