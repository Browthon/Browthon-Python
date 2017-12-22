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
				urlT = "https://www.google.fr/?gws_rd=ssl#q="+urlT
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
