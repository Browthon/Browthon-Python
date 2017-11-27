import sys

from PyQt4.QtWebKit import QWebView
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl

app = QApplication(sys.argv)

browser = QWebView()
browser.load(QUrl("http://youtube.com"))
browser.show()

app.exec_()
