#!/usr/bin/python3.6
# coding: utf-8

import sys
import os

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.PyWeb_main import *

def launch():
	app = QApplication(sys.argv)
	icon = QIcon('files/pyweb.png')
	app.setWindowIcon(icon)
	url = ""
	try:
		with open('config.txt'):
			pass
	except IOError:
		with open('config.txt', 'w') as fichier:
			fichier.write("UrlMoteur https://www.google.fr/?gws_rd=ssl#q=\nUrlAccueil https://lavapower.github.io/PyWeb-site/index.html\nJavaScript True\nNavigationPrivée False\nDéplacementOnglet True\nLangue FR\nStyle Default")
			url = "https://lavapower.github.io/PyWeb-site/index.html"
	else:
		with open('config.txt', 'r') as fichier:
			url = fichier.read().split("\n")[1].split(" ")[1]

	if len(sys.argv)>=2:
		if "." in sys.argv[1]:
			if "http://" in sys.argv[1] or "https://" in sys.argv[1]:
				url = sys.argv[1]
			else:
				url = "http://"+sys.argv[1]
	MainWindow(url)

	app.exec_()


if __name__ == '__main__':
	os.chdir("files")
	launch()