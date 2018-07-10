#!/usr/bin/python3.6
# coding: utf-8

import sys
sys.path.append('..')


class Test:
    def load(self, main):
        print("Chargement de l'addon Test")
    
    def keyPress(self, main, event):
        print("Numéro Touche pressé :", event.key())
    
    def enterUrl(self, main, url):
        print("Url entré : "+url)
    
    def openOnglet(self, main, url):
        print("Nouvel onglet avec url : "+url)
    
    def unload(self, main):
        print("Déchargement de l'addon test")

instance = Test
name = "test"