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

app = QApplication(sys.argv)
url = ""
os.chdir("files")
try:
    with open('config.txt'):
        pass
except IOError:
    with open('config.txt', 'w') as fichier:
        fichier.write("UrlMoteur https://www.google.fr/?gws_rd=ssl#q=\nUrlAccueil https://lavapower.github.io/pyweb.html\nJavaScript True\nNavigationPrivée False\nDéplacementOnglet True")
        url = "https://lavapower.github.io/pyweb.html"
else:
    with open('config.txt', 'r') as fichier:
        url = fichier.read().split("\n")[1].split(" ")[1]

main = MainWindow(url)
main.show()

app.exec_()
