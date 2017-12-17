#!/usr/bin/python3.6
# coding: utf-8

import sys, os

from PySide.QtWebKit import *
from PySide.QtGui import *
from PySide.QtCore import *

from files.PyWeb_main import *

app = QApplication(sys.argv)
url = ""
os.chdir("files")
try:
	with open('config.txt'):
		pass
except IOError:
	with open('config.txt','w') as fichier:
		fichier.write("https://lavapower.github.io/pyweb.html")
		url = "https://lavapower.github.io/pyweb.html"
else:
	with open('config.txt','r') as fichier:
		url = fichier.read().replace("\n","")

main = MainWindow(url)
main.show()

app.exec_()
