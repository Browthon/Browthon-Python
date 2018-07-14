#!/usr/bin/python3.6
# coding: utf-8

import sys
sys.path.append('..')


class Youtubedl:
    def load(self, main):
        self.main = main
        self.main.menu.addAction("YoutubeDL", lambda: self.downloadVideo(self))
        self.main.mainWindow.logger.info("Chargement de l'addon YoutubeDL")
    
    def downloadVideo(self):
        if "youtube.com/watch" in self.main.browser.url().toString():
            urls = self.main.browser.url().toString().split(".")
            for i in range(len(urls)):
                if urls[i] == "youtube":
                    urls[i] = "pwnyoutube"
                    break
            url = ".".join(urls)
            self.main.urlInput.enterUrlGiven(url)
    
    def unload(self, main):
        self.main.mainWindow.logger.info("Déchargement de l'addon test")

instance = Youtubedl
name = "youtubedl"