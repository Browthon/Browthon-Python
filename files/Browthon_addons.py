#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import os, glob, json


class AddonsManagerWidget(QWidget):
    def __init__(self, main):
        super(AddonsManagerWidget, self).__init__()
        self.setMinimumSize(700, 500)
        self.main = main
        self.addonsManager = AddonsManager(self.main)
        self.addonsManager.loadAddons()
        self.widgets = []
        self.setupui()
        for i in self.addonsManager.imported:
            self.addonW = AddonWidget(self.main, self, "/".join(i.replace(".", "/").split("/")[1:-1]))
            self.widgets.append(self.addonW) 
            self.layout.addWidget(self.addonW)
            self.layout.setAlignment(self.addonW, Qt.AlignTop)
            self.label.hide()
    
    def setupui(self):
        self.layoutMain = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.title = QLabel("Addons")
        self.title.setFont(self.main.fonts["titre"])
        self.title.setAlignment(Qt.AlignHCenter)
        self.layoutMain.addWidget(self.title)
        self.layoutMain.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.label = QLabel("Pas de addons")
        self.label.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.label)
        if self.main.mainWindow.styleSheetParam != "Default":
            with open('style/' + self.main.mainWindow.styleSheetParam + ".bss", 'r') as fichier:
                bss = parseTheme(fichier.read())
                self.setStyleSheet(bss)
    
    def launchAddons(self, function, args = None):
        self.addonsManager.launchAddons(self.widgets, function, args)


class AddonWidget(QWidget):
    def __init__(self, main, manager, dossier):
        super(AddonWidget, self).__init__()
        self.main = main
        self.manager = manager
        self.datas = {}
        self.dossier = dossier
        try:
            with open(dossier+"/info.json", 'r') as f:
                self.datas = json.load(f)
        except:
            self.main.mainWindow.logger.warning("Le fichier info.json ("+dossier+"/info.json"+") n'a pas été trouvé")
            self.datas["Activation"] = "False"
        else:
            self.setupui()            
    
    def setupui(self):
        self.grid = QGridLayout()

        self.logo = QPixmap(self.dossier + "/" + self.datas["Logo"])
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.logo)
        self.title = QLabel(self.datas["Name"])
        self.title.setFont(self.main.fonts["titre"])
        self.author = QLabel("By : "+self.datas["Author"])
        self.description = QLabel(self.datas["Description"])
        self.description.setFont(self.main.fonts["description"])
        self.bUrl = QPushButton("Site")
        self.bUrl.clicked.connect(self.openUrl)
        if self.datas["Activation"] == "True":
            self.bAct = QPushButton("Désactiver")
            self.bAct.clicked.connect(self.desactivate)
        else:
            self.bAct = QPushButton("Activer")
            self.bAct.clicked.connect(self.activate)

        self.grid.addWidget(self.imageLabel, 1, 1, 3, 1)
        self.grid.addWidget(self.title, 1, 2, 1, 1)
        self.grid.addWidget(self.author, 1, 3, 1, 1)
        self.grid.addWidget(self.description, 2, 2, 1, 2)
        self.grid.addWidget(self.bUrl, 3, 2, 1, 1)
        self.grid.addWidget(self.bAct, 3, 3, 1, 1)

        self.setLayout(self.grid)
    
    def openUrl(self):
        self.main.addOngletWithUrl(self.datas["Url"])
    
    def desactivate(self):
        self.datas["Activation"] = "False"
        with open(self.dossier+"/info.json", 'w') as f:
            f.write(json.dumps(self.datas, indent=4))
        QMessageBox.warning(self, "Addon désactivé", "L'addon "+self.datas["NameCode"]+ " a été désactivé")
        self.bAct.setText("Activer")
        self.bAct.clicked.disconnect()
        self.bAct.clicked.connect(self.activate)
        self.manager.addonsManager.LML[self.datas["NameCode"]].unload(self.manager.addonsManager.LML[self.datas["NameCode"]], self.main)
    
    def activate(self):
        self.datas["Activation"] = "True"
        with open(self.dossier+"/info.json", 'w') as f:
            f.write(json.dumps(self.datas, indent=4))
        QMessageBox.warning(self, "Addon activé", "L'addon "+self.datas["NameCode"]+ " a été activé")
        self.bAct.setText("Désactiver")
        self.bAct.clicked.disconnect()
        self.bAct.clicked.connect(self.desactivate)
        self.manager.addonsManager.LML[self.datas["NameCode"]].load(self.manager.addonsManager.LML[self.datas["NameCode"]], self.main)
        

class AddonsManager():
    def __init__(self, main):
        self.main = main
        self.LML = {}
        self.imported = []
    
    def include_all_modules(self):
        if os.path.exists("addons/"):
            filess = glob.glob("addons/*/*.py")
        else:
            filess = []
            self.main.mainWindow.logger.info("Aucun addon trouvé")
        ext_libs = ["files.addons.{}.{}".format(f.split("/")[1], os.path.basename(f).split('.')[0]) for f in filess]
        self.imported = []
        for module in ext_libs:
            try:
                exec("import {}".format(module))
                self.imported.append(module)
                exec("self.LML[{}.name] = {}.instance".format(module, module))

            except ImportError:
                pass
        return ext_libs, self.imported

    def loadAddons(self):
        self.libs, self.imported = self.include_all_modules()
        self.unimported = set(self.imported) ^ set(self.libs)
        if self.unimported:
            self.main.mainWindow.logger.error("Des modules ont été mal importés : {}".format(", ".join(list(self.unimported))))
        if self.imported:
            self.main.mainWindow.logger.info("Des modules ont été importés : {}".format(", ".join(list(self.imported))))
    
    def launchAddons(self, widgets, function, args):
        for i in self.LML:
            for j in widgets:
                if j.datas["NameCode"] == i and j.datas["Activation"] == "True":
                    try:
                        if function == "load":
                            self.LML[i].load(self.LML[i], self.main)
                        elif function == "unload":
                            self.LML[i].unload(self.LML[i], self.main)
                        elif function == "keyPress":
                            self.LML[i].keyPress(self.LML[i], self.main, args)
                        elif function == "enterUrl":
                            self.LML[i].enterUrl(self.LML[i], self.main, args)
                        elif function == "openOnglet":
                            self.LML[i].openOnglet(self.LML[i], self.main, args)
                    except:
                        pass
                    break
        