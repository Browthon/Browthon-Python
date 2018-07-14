#!/usr/bin/python3.6
# coding: utf-8

import sys
sys.path.append('..')


class Test:
    def load(self, main):
        main.mainWindow.logger.info("Chargement de l'addon Test")
    
    def keyPress(self, main, event):
        main.mainWindow.logger.info("Numéro Touche pressé :", event.key())
    
    def enterUrl(self, main, url):
        main.mainWindow.logger.info("Url entré : "+url)
    
    def openOnglet(self, main, url):
        main.mainWindow.logger.info("Nouvel onglet avec url : "+url)
    
    def unload(self, main):
        main.mainWindow.logger.info("Déchargement de l'addon test")

instance = Test
name = "test"