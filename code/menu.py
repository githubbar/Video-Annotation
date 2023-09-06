# -*- coding: utf-8 -*-
"""
====================================================================================
Video Annotation Tool
Copyright (C) 2023 Alex Leykin @ Customer Interface Lab
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
""" Creates a main menu """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

def createMenu(w):
        menubar = w.menuBar()
        fileMenu = menubar.addMenu('&File')        
        newaction = QAction(QIcon('icons/filenew.png'), 'New Project', w)
        newaction.setShortcut('Ctrl+N')
        newaction.triggered.connect(w.fileNew)        
        fileMenu.addAction(newaction)        
        openaction = QAction(QIcon('icons/fileopen.png'), 'Open Project...', w)
        openaction.setShortcut('Ctrl+O')
        openaction.triggered.connect(w.fileOpen)        
        fileMenu.addAction(openaction)        
        saveaction = QAction(QIcon('icons/filesave.png'), 'Save Project', w)
        saveaction.setShortcut('Ctrl+S')
        saveaction.triggered.connect(w.fileSave)        
        fileMenu.addAction(saveaction)        
        saveasaction = QAction(QIcon('icons/filesaveas.png'), 'Save As Project...', w)
        saveasaction.triggered.connect(w.fileSaveAs)              
        fileMenu.addAction(saveasaction)
        mergenaction = QAction(QIcon('icons/filemerge.png'), 'Merge Project...', w)
        mergenaction.triggered.connect(w.fileMerge)        
        fileMenu.addAction(mergenaction)        
        loaddataaction = QAction(QIcon('icons/loaddata.png'), 'Load Data...', w)
        loaddataaction.triggered.connect(w.loadData)        
        fileMenu.addAction(loaddataaction)                
        exportdataaction = QAction('Export Data...', w)
        exportdataaction.setShortcut('Ctrl+E')
        exportdataaction.triggered.connect(w.exportTrackData)        
        fileMenu.addAction(exportdataaction)
        changevidpathsaction = QAction('Change video paths...', w)
        changevidpathsaction.triggered.connect(w.changeVideoPaths)        
        fileMenu.addAction(changevidpathsaction)                
        editMenu = menubar.addMenu('&Edit')
        undoaction = w.graphicsView.scene.undoStack.createUndoAction(w, 'Undo')
        undoaction.setShortcut(QKeySequence.Undo)
        editMenu.addAction(undoaction)
        redoaction = w.graphicsView.scene.undoStack.createRedoAction(w, 'Redo')
        redoaction.setShortcut(QKeySequence('Shift+Ctrl+Z'))
        editMenu.addAction(redoaction)
        undolist = QAction('Show undo history', w)
        undolist.triggered.connect(w.showUndoHistory)        
        editMenu.addAction(undolist)
        w.undoView = QUndoView(w.graphicsView.scene.undoStack);
        w.undoView.setWindowTitle('Undo History')
        w.undoView.setWindowModality(Qt.ApplicationModal)        
        settingstMenu = menubar.addMenu('&Settings')
        w.synctaction = QAction('Sync track on playback', w, checkable=True)
        w.synctaction.setChecked(True)
        settingstMenu.addAction(w.synctaction)        
        projectaction = QAction(QIcon('icons/settings.png'), 'Project Properties', w)
        projectaction.setShortcut('F12')
        projectaction.triggered.connect(w.showProjectProperties)                
        settingstMenu.addAction(projectaction)
        actionMenu = menubar.addMenu('&Action')        
        predictaction = QAction('Predict path', w)
        predictaction.setShortcut('/')
        predictaction.triggered.connect(w.predictPath)
        loadfixations = QAction('Load fixations', w)
        loadfixations.triggered.connect(w.loadFixations)
        findbadnodes = QAction('Find Bad Nodes', w)
        findbadnodes.triggered.connect(w.findBadNodes)        

        actionMenu.addAction(predictaction)
        actionMenu.addAction(loadfixations)                
        actionMenu.addAction(findbadnodes)
        helpMenu = menubar.addMenu('&Help')
        helpaction = QAction('Help', w)
        helpaction.setShortcut('Ctrl+F1')
        w.initHelp()
        helpaction.triggered.connect(w.helpWindow.show)
        helpMenu.addAction(helpaction)
        aboutaction = QAction('About', w)
        aboutaction.triggered.connect(w.about)    
        helpMenu.addAction(aboutaction)



        
