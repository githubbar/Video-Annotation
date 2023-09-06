# -*- coding: utf-8 -*-
"""
====================================================================================
Video Annotation Tool
Copyright (C) 2023 Alex Leykin @ CIL
Email: cil@indiana.edu
http://cil.iu.edu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
            
====================================================================================
"""
""" Help browser panel """
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QFileInfo, QUrl


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

        
