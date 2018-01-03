#!/usr/bin/python3.6
# coding: utf-8

import sys
import os

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from files.PyWeb_main import *

app = QApplication(sys.argv)
url = ""
os.chdir("files")
try:
    with open('config.txt'):
        pass
except IOError:
    with open('config.txt', 'w') as fichier:
        fichier.write("https://www.google.fr/?gws_rd=ssl#q=\nhttps://lavapower.github.io/pyweb.html")
        url = "https://lavapower.github.io/pyweb.html"
else:
    with open('config.txt', 'r') as fichier:
        url = fichier.read().split("\n")[1]

main = MainWindow(url)
main.show()

app.exec_()
