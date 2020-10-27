# -*- coding: utf-8 -*-
""" Help browser panel """

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import PyQt5.QtNetwork


class HelpBrowser(QWebEngineView):
    def __init__(self, helpEngine, parent=None):    
        import os
        QWebEngineView.__init__(self, parent)
        self.helpEngine = helpEngine
        path = QFileInfo(self.helpEngine.collectionFile()).path()
        url = QUrl.fromLocalFile( os.path.join(str(path), 'manual.html'))
        QWebEngineView.load(self, url)        
        self.helpEngine.contentWidget().expandAll()
        
#        QWebSettings.globalSettings().setAttribute(QWebSettings.AutoLoadImages, True)
#        QWebSettings.globalSettings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
#        QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
#        QWebSettings.globalSettings().setAttribute(QWebSettings.PluginsEnabled, True)

    def load(self, url):
        import os

        
        if (url.scheme() == "qthelp"):
#            self.setContent(self.helpEngine.fileData(url), QString(), QUrl(u'qthelp://cil.com.va.38/help'))
#            inspector = QWebInspector(self)
#            inspector.setPage(self.page())
#            inspector.setFixedSize(self.width(), 200)
#            inspector.setVisible(True)      
            path = QFileInfo(self.helpEngine.collectionFile()).path()
            fileName = QFileInfo(url.path()).fileName()
            localurl = QUrl.fromLocalFile( os.path.join(str(path), str(fileName)))
            localurl.setFragment(url.fragment())
        QWebEngineView.setUrl(self, localurl)

        
