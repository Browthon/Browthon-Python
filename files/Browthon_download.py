#!/usr/bin/python3.6
# coding: utf-8

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


class DownloadSignal(QObject):
    removeClicked = pyqtSignal()

    def __init__(self, parent):
        super(DownloadSignal, self).__init__()
        self.parent = parent


class DownloadWidget(QWidget):
    def __init__(self, download):
        super(DownloadWidget, self).__init__()
        self.setupui()
        self.download = download
        self.downloadSignal = DownloadSignal(self)
        self.title.setText(QFileInfo(self.download.path()).fileName())

        self.cancel.clicked.connect(self.cancelDownload)
        self.download.downloadProgress.connect(self.updateWidget)
        self.download.stateChanged.connect(self.updateWidget)

        self.updateWidget()

    def updateWidget(self):
            totalBytes = self.download.totalBytes()
            receivedBytes = self.download.receivedBytes()

            state = self.download.state()
            if state == QWebEngineDownloadItem.DownloadRequested:
                pass
            elif state == QWebEngineDownloadItem.DownloadInProgress:
                if totalBytes >= 0:
                    self.progressBar.setValue(int(100 * receivedBytes / totalBytes))
                    self.progressBar.setDisabled(False)
                    self.progressBar.setFormat("%p% - {} téléchargés sur {}".format(self.withUnit(receivedBytes), self.withUnit(totalBytes)))
                else:
                    self.progressBar.setValue(0)
                    self.progressBar.setDisabled(False)
                    self.progressBar.setFormat("Taille inconnue - {}téléchargés".format(self.withUnit(receivedBytes)))
            elif state == QWebEngineDownloadItem.DownloadCompleted:
                self.progressBar.setValue(100)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Complété - {} téléchargés".
                  format(self.withUnit(receivedBytes)))
            elif state == QWebEngineDownloadItem.DownloadCancelled:
                self.progressBar.setValue(0)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Annulé - {} téléchargés".
                  format(self.withUnit(receivedBytes)))
            elif state == QWebEngineDownloadItem.DownloadInterrupted:
                self.progressBar.setValue(0)
                self.progressBar.setDisabled(True)
                self.progressBar.setFormat("Interrompu - {}".
                  format(self.download.interruptReasonString()))

            if state == QWebEngineDownloadItem.DownloadInProgress:
                self.cancel.setText("Arrêter")
                self.cancel.setToolTip("Stopper le téléchargement")
            else:
                self.cancel.setText("Supprimer")
                self.cancel.setToolTip("Enlever le téléchargement")

    def cancelDownload(self):
        if self.download.state() == QWebEngineDownloadItem.DownloadInProgress:
            self.download.cancel()
        else:
            self.downloadSignal.removeClicked.emit()

    def withUnit(self, bytesNb):
        if bytesNb < 1 << 10:
            return str(round(bytesNb, 2)) + " B"
        elif bytesNb < 1 << 20:
            return str(round(bytesNb / (1 << 10), 2)) + " KiB"
        elif bytesNb < 1 << 30:
            return str(round(bytesNb / (1 << 20), 2)) + " MiB"
        else:
            return str(round(bytesNb / (1 << 30), 2)) + " GiB"

    def setupui(self):
        self.layout = QGridLayout()
        self.title = QLabel("NAME")
        self.cancel = QPushButton("Cancel")
        self.progressBar = QProgressBar()
        self.layout.addWidget(self.title, 1, 1)
        self.layout.addWidget(self.progressBar, 2, 1)
        self.layout.addWidget(self.cancel, 3, 1)
        self.setLayout(self.layout)


class DownloadManagerWidget(QWidget):
    def __init__(self, main):
        super(DownloadManagerWidget, self).__init__()
        self.setMinimumSize(500, 300)
        self.main = main
        self.nbDownload = 0
        self.setupui()

    def downloadRequested(self, download):
        if download:
            if download.state() == QWebEngineDownloadItem.DownloadRequested:
                path = QFileDialog.getSaveFileName(self, "Sauver comme",
                    download.path())
                if path == "":
                    return
                else:
                    download.setPath(path[0])
                    download.accept()
                    self.add(DownloadWidget(download))

                    self.show()
            else:
                self.main.mainWindow.logger.critical("Le téléchargement n'a pas été demandé ou est nul.")
        else:
            self.main.mainWindow.logger.critical("Le téléchargement n'a pas été demandé ou est nul.")

    def add(self, downloadWidget):
        downloadWidget.downloadSignal.removeClicked.connect(self.remove)
        self.layout.addWidget(downloadWidget)
        self.nbDownload += 1
        if self.nbDownload >= 0:
            self.label.hide()

    def remove(self):
        downloadWidget = self.sender().parent
        self.layout.removeWidget(downloadWidget)
        downloadWidget.deleteLater()
        self.nbDownload -= 1
        if self.nbDownload <= 0:
            self.label.show()

    def setupui(self):
        self.layoutMain = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.layoutMain.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)
        self.layout = QVBoxLayout(self.container)
        self.label = QLabel("Pas de téléchargement")
        self.layout.addWidget(self.label)