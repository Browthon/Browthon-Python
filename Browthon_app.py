#!/usr/bin/python3.6
# coding: utf-8

import sys
import os

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from files.Browthon_main import *

def launch(sys):
	if not os.path.isdir('logs'):
		os.mkdir("logs")
	try:
		with open('logs/browthon.log'):
			pass
	except IOError:
		with open('logs/browthon.log', 'w') as fichier:
			fichier.write("--- Fichier de log : Browthon ---\n")
	app = QApplication(sys.argv)
	icon = QIcon('logo.png')
	app.setWindowIcon(icon)
	url = ""
	try:
		with open('config.txt'):
			pass
	except IOError:
		with open('config.txt', 'w') as fichier:
			fichier.write("UrlMoteur https://www.google.fr/?gws_rd=ssl#q=\nUrlAccueil http://pastagames.fr.nf/browthon/\nJavaScript True\nNavigationPrivée False\nDéplacementOnglet True\nStyle Default\nSession False\nNiveauLog INFO")
			url = "http://pastagames.fr.nf/browthon/"
	else:
		with open('config.txt', 'r') as fichier:
			url = fichier.read().split("\n")[1].split(" ")[1]
	urltemp = url
	if len(sys.argv)>=2:
		if "." in sys.argv[1]:
			if "http://" in sys.argv[1] or "https://" in sys.argv[1]:
				urltemp = sys.argv[1]
			else:
				urltemp = "http://"+sys.argv[1]
	MainWindow(url, urltemp)

	app.exec_()


if __name__ == '__main__':
	os.chdir("files")
	launch(sys)