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
import logging, os

import sys, threading, time, \
    qdarkstyle, vlc, menu, searchwidget, buttonevents, helpbrowser
import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QAbstractItemView, QAction, QToolBar, QInputDialog, \
    QFileDialog, QMessageBox, QDialog, QSplitter, QVBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QTimer, QTime, QFile, QIODevice, QDataStream
from PyQt5.QtGui import QIcon, QKeySequence
from vacommands import RemoveCommand

from fileio import findFataFile, QDataExportDialog, fileio
from track import Path

# Create a class for our main window
class Main(PyQt5.QtWidgets.QMainWindow, buttonevents.ButtonEvents, searchwidget.SearchWidget):
    GUI_NORMAL = 0
    GUI_SEARCH = 1
    GUI_EXPORT = 2
    GUI_UPDATESTATS = 2
    BUILD_NUMBER = 47
    READ_ONLY = False  # Global switch to prevent the user from editing 
    go = False  # search/export thread is not running
        
    updateProgress = pyqtSignal(int)        
    updateProgressEdit = pyqtSignal(int)
    completeProgress = pyqtSignal(int)
    
    def __init__(self):
        super(Main, self).__init__()
        logging.debug('Beginning to load UI')
        uic.loadUi(findFataFile('window.ui'), self)
        logging.debug('Loaded UI')
        self.show()
        self.appPath = ""        
        self.help = None
        self.lastDir = os.path.expanduser("~")
#         bool(glutInit) 
        # Menu
        menu.createMenu(self)

        # Toolbar
        self.actions = []
        if self.READ_ONLY:
            self.propertyWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)            
            action = QAction(QIcon(os.path.join(self.appPath, 'icons/Select.png')), 'Select', self)
            self.actions.append(action)
            action.triggered.connect(self.handleToolbarButton)
        else:
            self.toolbar = QToolBar(self)
            n = 1
            for i, text in enumerate(self.graphicsView.scene.modes):
                action = QAction(QIcon(os.path.join(self.appPath, 'icons/') + text + '.png'), text, self)
                if text != 'Separator':
                    action.setShortcut(QKeySequence('Ctrl+' + str(n)))
                    n = n + 1
                    action.setCheckable(True)
                    
                    self.actions.append(action)
                    action.triggered.connect(self.handleToolbarButton)
                else:
                    action.setSeparator(True)
                self.toolbar.addAction(action)
    #        self.addToolBar(Qt.TopToolBarArea,  self.toolbar)
            self.toolbar.setOrientation(Qt.Vertical)
            self.gridLayout.addWidget(self.toolbar, 0, 0, -1, 1)
        self.actions[0].setChecked(True)

        # Video View
        self.Instance = vlc.Instance('--fullscreen --verbose 3')
        self.mediaPlayer = self.Instance.media_player_new()
        self.isPaused = True
        self.playButton.setIcon(QIcon(os.path.join(self.appPath, 'icons/player_play.png')))
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        
        self.fullScreen = False
        toggleFullscreen = QAction(self)
        toggleFullscreen.setShortcut(Qt.Key_F11)        
        toggleFullscreen.triggered.connect(self.handleFullScreen)    
        self.addAction(toggleFullscreen)       
        setRate = QAction(self)
        setRate.setShortcut(QKeySequence('CTRL+R'))        
        setRate.triggered.connect(self.setPlaybackRate)    
        self.addAction(setRate)     
        
        rew = QAction(self)
        rew.setShortcut(Qt.Key_Left)        
        rew.triggered.connect(self.rew)    
        self.addAction(rew)   
        ff = QAction(self)
        ff.setShortcut(Qt.Key_Right)        
        ff.triggered.connect(self.ff)    
        self.addAction(ff)     
        rew1 = QAction(self)
        rew1.setShortcut(QKeySequence('SHIFT+Left'))        
        rew1.triggered.connect(self.rew1)    
        self.addAction(rew1)   
        ff1 = QAction(self)
        ff1.setShortcut(QKeySequence('SHIFT+Right'))        
        ff1.triggered.connect(self.ff1)    
        self.addAction(ff1)                   
        rew5 = QAction(self)
        rew5.setShortcut(QKeySequence('CTRL+Left'))        
        rew5.triggered.connect(self.rew5)    
        self.addAction(rew5)   
        ff5 = QAction(self)
        ff5.setShortcut(QKeySequence('CTRL+Right'))        
        ff5.triggered.connect(self.ff5)    
        self.addAction(ff5)           
   
        self.connectSignals()

        if (len(sys.argv) > 1):
            self.fileOpen(sys.argv[1])
        if (len(sys.argv) > 2):
            self.loadData(sys.argv[2])            
        
        # self.preloadFiles()
#         self.exportTrackData('E:\Box Sync\CIL Exchange\Video Annotation\Schnucks Twin Oaks\data.csv')

    def connectSignals(self):
        # Edit tab
#         self.splitterEditTop.setSizes([5,3])

        # Scene->Property Widget signals
        self.graphicsView.scene.loadSignal.connect(self.propertyWidget.loadItem)  
        self.graphicsView.scene.saveSignal.connect(self.propertyWidget.saveItem)

        # Scene->Item List signals 
        self.graphicsView.scene.addItemListSignal.connect(self.items.onAddItem)
        self.graphicsView.scene.removeItemListSignal.connect(self.items.onRemoveItem)  
        self.graphicsView.scene.updateItemListSignal.connect(self.items.onUpdateItem)  
        self.graphicsView.scene.changeCurrentItemSignal.connect(self.items.onChangeCurrentItem)  
        
        # Item List->Scene signals
        self.items.itemClicked.connect(self.onItemClicked)
        self.items.currentItemChanged.connect(self.onCurrentItemChanged)
        self.items.deleteKeyPressed.connect(self.onDeleteItem)


                  
                  
        self.graphicsView.scene.loadVideoSignal.connect(self.loadVideo)          
        self.graphicsView.scene.updateVideoSignal.connect(self.updateVideo)   
        self.graphicsView.scene.addAOIListSignal.connect(self.aois.addItem)  
        self.graphicsView.scene.removeAOIListSignal.connect(self.aois.removeItem)  
        self.aois.deleteKeyPressed.connect(self.deleteAOI)
        self.checkAll.clicked.connect(self.toggleAllItems)
        self.filterTracks.clicked.connect(self.showFilterDialog)
        self.buttonVariables.clicked.connect(self.variablesClicked)
        self.seekSlider.sliderMoved.connect(self.setPosition)
        self.playButton.clicked.connect(self.playClicked)
        self.useAOIs.clicked.connect(self.useAOIsTrigger)
        self.timer.timeout.connect(self.updateUI)
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.progressBarEdit.hide()
        
        # Search tab
#         if (self.READ_ONLY):
#             self.tabWidget.removeTab(self.GUI_SEARCH)
        
        self.searchButton.clicked.connect(self.searchClicked)
        self.exportVideo.clicked.connect(self.exportVideoClicked)
        self.exportData.clicked.connect(self.exportDataClicked)
        self.exportImage.clicked.connect(self.exportImageClicked)
        self.exportStats.clicked.connect(self.exportStatsClicked)
        self.exportAOIData.clicked.connect(self.exportAOIDataClicked)
        self.updateStats.clicked.connect(self.updateStatsClicked)
        self.showHistogram.clicked.connect(self.showHistogramClicked)        
        self.searchCancel.clicked.connect(self.cancelClicked)        
        self.exportCancel.clicked.connect(self.cancelClicked)
        self.updateProgress.connect(self.OnUpdateProgress)       
        self.updateProgressEdit.connect(self.OnUpdateProgressEdit)
        self.completeProgress.connect(self.OnGUIMode)      
        
        self.completeProgress.emit(self.GUI_NORMAL)
        self.tabChanged(self.tabWidget.currentIndex())
        
        # Visualize tab
        self.visButton.clicked.connect(self.visClicked)
#         self.variablesClicked()
                
    def preloadFiles(self):
#         filename  = 'E:\Box Sync\CIL Exchange\Video Annotation\Giant Eagle - Washington\data.vaproj'
#         filename = r'E:\Box Sync\CIL Exchange\Video Annotation Code\code\test.vaproj'
        filename = r'E:\Box Sync\CIL Exchange\Video Annotation\Schnucks Richardson Road\data.vaproj'
        dataFileName = r'E:\Box Sync\CIL Exchange\Video Annotation\Schnucks Richardson Road\Import into VA\Survey for import into VA minus 1.csv'
        self.fileOpen(filename)
        self.loadData(dataFileName)        
#         self.fileSave(filename)        
#         filename  = 'E:\Box Sync\CIL Exchange\Video Annotation\Giant Eagle - Washington\data.vaproj'
#         filename  = 'E:\Box Sync\Video Annotation\Stop n Shop - Wyckoff\data.vaproj'
#         filename  = '.\data.vaproj'
#         filename  = 'E:\Box Sync\CIL Exchange\Video Annotation\American Eagle\AE - Jan 19, 2006.vaproj'
#         filename  = 'E:\Box Sync\CIL Exchange\Video Annotation\Giant Eagle - Washington\data.vaproj'

#         self.graphicsView.scene.loadNodeLevelVars('E:\\Box Sync\\CIL Exchange\\Video Annotation\\American Eagle\\node level variables Jan 12.csv')        
#         self.graphicsView.scene.loadBatchData('E:\Box Sync\CIL Exchange\Video Annotation\American Eagle\AE - Jan 19, 2006 hide invisible.csv')
#         self.visClicked()
#         self.graphicsView.scene.generateFixationSnapshots('E:\Box Sync\Video Annotation\Giant Eagle - Washington\id 129 fixations ANSI.tsv')
#         self.generateFixationSnapshots('E:/Box Sync/Video Annotation/Giant Eagle - Washington/fixations/fixationdata ANSI.tsv')

    def setPlaybackRate(self):
        rate, ok = QInputDialog.getDouble(self, 'Input Dialog', 'Enter playback rate:', 1.0, 0.1, 100)        
        if ok: 
            self.mediaPlayer.set_rate(rate)

    def rew(self):
        self.mediaPlayer.set_time(max(self.mediaPlayer.get_time() - 66, 0))            
        self.updateUI()

    def ff(self):
        self.mediaPlayer.next_frame()
        self.updateUI()

    def rew1(self):
        self.mediaPlayer.set_time(max(self.mediaPlayer.get_time() - 1000, 0))            
        self.updateUI()
        
    def ff1(self):
        self.mediaPlayer.set_time(self.mediaPlayer.get_time() + 1000)            
        self.updateUI()

    def rew5(self):
        self.mediaPlayer.set_time(max(self.mediaPlayer.get_time() - 5000, 0))            
        self.updateUI()

    def ff5(self):
        self.mediaPlayer.set_time(self.mediaPlayer.get_time() + 5000)            
        self.updateUI()        

#    def eventFilter(self, object, event):
#        if (event.type() == QEvent.MouseButtonPress):
#            print "The bad guy which steals the MousePress is"
#            print object
#        return False
        
    def loadVideo(self, filename):
        """Open a media file in a mediaPlayer"""
        if filename == '':
            filename, _filter = QFileDialog.getOpenFileName(self, "Open File", os.getcwd())
        filename = os.path.join(os.path.dirname(str(self.graphicsView.scene.filename)), str(filename))
        filename = 'file:///' + filename   
        self.Media = self.Instance.media_new(str(filename))
        self.mediaPlayer.set_media(self.Media)
        self.Media.parse()
#        self.setWindowTitle(self.Media.get_meta(0))
        if sys.platform == "linux2":  # for Linux using the X Server
            self.mediaPlayer.set_xwindow(self.videoPlayer.winId())
        elif sys.platform == "win32":  # for Windows
            self.mediaPlayer.set_hwnd(self.videoPlayer.winId())
        elif sys.platform == "darwin":  # for MacOS
            self.mediaPlayer.set_agl(self.videoPlayer.windId())

    def findBadNodes(self):
        s = ''
        for item in self.graphicsView.scene.items():
            if type(item) == Path:
                for i, t1 in enumerate(item.startTime):
                    if t1> item.stopTime[i]:
                        s += f'TIME ERROR! track:{item.id} start={t1} stop={item.stopTime[i]} \n'
                        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        
        msg.setText("Node time errors listed below")
        msg.setInformativeText("See details...")
        msg.setWindowTitle("Details")
        msg.setDetailedText(s)
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.exec_()
        
    def loadData(self, filename):
                
        """Load additional track data"""
        if filename == False:
            filename, _filter = QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), 'CSV Files (*.csv)')
        if filename:
            self.graphicsView.scene.loadData(str(filename))
        return None

    def loadFixations(self, filename):
        """Load additional track data"""
        if filename == False:
            filename, _filter = QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), 'TSV Files (*.tsv)')
        if filename:
            self.generateFixationSnapshots(str(filename))
            
    def generateFixationSnapshots(self, filename):
        fileio.generateFixationSnapshots(self, filename)
         
    def exportTrackData(self, filename = False):
        # choose export file
        dlg = QDataExportDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilter("CSV Files (*.csv)")
       
        if not filename and dlg.exec_():
            if len(dlg.selectedFiles()) > 0:
                filename = dlg.selectedFiles()[0]
#         outFileName = QDataExportDialog.getSaveFileName(self, "Choose File to Export To", os.getcwdu())
#         outFileName = 'e:/Projects/Visual Attention/Project Time 2011 Mobile Tier Productivity/Data/Jewel Osco - Naperville/Manual Eye Tracking/test.csv'
        if not filename:
            return
        self.progressBarEdit.show()
        self.repaint()   
        exportDistDuration = True if dlg.checkExportDistDuration.checkState() == Qt.Checked else False
        exportAOIDistDuration = True if dlg.checkExportAOIDistDuration.checkState() == Qt.Checked else False
        threading.Thread(target=self.doExportData, name="exportDataThread", args=(filename, exportDistDuration, exportAOIDistDuration,)).start()

    def fixData(self):
        varNames = ['id', 'seq. number', 'x', 'y', 'video name', 'startTime', 'stopTime']
        varNames.extend([str(key) for key in list(self.graphicsView.scene.variables.keys())])   
        
        for i in range(self.items.count()):
            itemId = self.items.item(i).text() 
            item = self.graphicsView.scene.findPath(itemId)
            # sort indexes by ascending start time 
            idx = sorted(list(range(len(item.startTime))), key=lambda k: item.startTime[k])
            name = 'cartType'
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name]
#                   if StrToBoolOrKeep(vEachNode) and idx != None:
            v = item.variables[name]
            cartType = [x for x in v if x]
            if type(cartType) == list:
                if len(cartType) > 0:
                    pr = cartType[0]
                else:
                    pr = 'empty'    
                print([str(item.id), type(cartType), str(pr)])
            if len(cartType) > 1:
                cartType = cartType[0]
            else:
                cartType = ''
            item.variables[name] = cartType
                
    def doExportData(self, outFileName, exportDistDuration, exportAOIDistDuration):
        import subprocess, csv
        writer = csv.writer(open(outFileName, 'w', newline=''))
        varNames = ['id']
        if exportDistDuration:
            varNames.extend(['trip length', 'trip duration'])
        if exportAOIDistDuration:
            varNames.extend(['AOI Name', 'AOI path legth', 'AOI duration', 'Category Shop Count']) 
        varNames.extend(['seq. number', 'x', 'y', 'startTime', 'stopTime'])
        varNames.extend([key for key in list(self.graphicsView.scene.variables.keys())])   
        writer.writerow(varNames)

        for i in range(self.items.count()):
            itemId = self.items.item(i).text() 
            item = self.graphicsView.scene.findPath(itemId)
#             # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#             # BEGIN TEMP: Crop extra startTime entries in the list
#             item.startTime = item.startTime[:item.polygon.size()]            
#             item.stopTime = item.stopTime[:item.polygon.size()]
#             # END TEMP: Crop extra startTime entries in the list
#             # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            # sort indexes by ascending start time 
            idx = sorted(list(range(len(item.startTime))), key=lambda k: item.startTime[k])
            self.updateProgressEdit.emit(int(100.0 * i / self.items.count()))
          
#             stimes = sorted(item.startTime)

            tAll = QTime(0, 0).addSecs(item.startTime[0].secsTo(item.stopTime[-1]))
            
            # BEGIN reset AOI aggregates
            aoiName, aoiL, aoiD = {}, {}, {}
            for rowAOI in range(self.aois.rowCount()):
                aoi = self.aois.item(rowAOI, 0)
                aoiName[rowAOI] = aoi.text()
                aoiL[rowAOI] = aoi.g.getTrackLength(item)
                aoiD[rowAOI] = aoi.g.getTrackDuration(item)
            # END reset AOI aggregates
            
            # BEGIN reset Category aggregates
            catShopCount = 1
            currentCat = ''
            # END reset Category aggregates            
            
            for j, n in enumerate(idx):
                varList = item.getVariableValuesList(n)
                row = [ str(item.id)]
                p = item.polygon.at(n)
                tNode = QTime(0, 0).addSecs(item.startTime[n].secsTo(item.stopTime[n]))

                for nn in range(n, len(idx)):
                    cat = item.variables['Category Shopped'][nn] 
                    if (cat and cat == currentCat):
                        catShopCount += 1
                    else:
                        currentCat = cat
                        break

                if exportDistDuration:
                    row.extend([str(item.getPathLength()), str(tAll.toString('hh:mm:ss'))])
                if exportAOIDistDuration:
                    try:
                        rowAOI = next(aoii for aoii, v in enumerate(self.aois.getAllItems()) if v.g.contains(p))
                        row.extend([str(aoiName[rowAOI]), str(aoiL[rowAOI]), str(aoiD[rowAOI]), str(catShopCount)])
                    except:
                        row.extend(['None', '0', '0', '0'])

                row.extend([str(j), str(p.x()), str(p.y()), \
                  str(item.startTime[n].toString('hh:mm:ss')), \
                  str(item.stopTime[n].toString('hh:mm:ss')) ])
                row.extend(varList)
                
                catShopCount = 1
                try:
                    writer.writerow(row)
                except UnicodeEncodeError: 
                    continue
        self.completeProgress.emit(self.GUI_NORMAL)

    def changeVideoPaths(self, dirname=''):
        if dirname == False:
            dirname = QFileDialog.getExistingDirectory(self, "Open Directory")
        if not dirname:
            return
        
        path, fname = os.path.split(str(self.graphicsView.scene.filename))
        relpath = os.path.relpath(str(dirname), path)
        for i in range(self.items.count()):
            itemId = self.items.item(i).text() 
            item = self.graphicsView.scene.findPath(itemId)
            path, fname = os.path.split(str(item.videoname))
            item.videoname = os.path.join(relpath, fname)

    def fileOpen(self, filename=''):
        if not filename:
                        
            filename, _filter = QFileDialog.getOpenFileName(self, "Open File", self.lastDir, "VA Projects (*.vaproj);;All Files (*.*)")

        if not filename:
            return
        self.lastDir = os.path.dirname(filename)
        self.clear()        
        self.fileNew()
        self.graphicsView.scene.filename = filename
        self.setWindowTitle(self.graphicsView.scene.filename + ' - Video Annotation Tool') 
        file = QFile(self.graphicsView.scene.filename)
        file.open(QIODevice.ReadOnly)
        s = QDataStream(file)
        buildNumber = s.readInt()
        if buildNumber < 47:
            s.setVersion(QDataStream.Qt_4_9)
        else:
            s.setVersion(QDataStream.Qt_5_15)
            
        if (self.BUILD_NUMBER != buildNumber):
            QMessageBox.warning(self, "Warning!", "The data file is in format for build " + str(buildNumber) + ' \nCurrent software build is ' + str(self.BUILD_NUMBER))
#            return
        self.graphicsView.scene.load(s, buildNumber)
        self.checkAllItems(False)
        self.actions[0].trigger()
        self.graphicsView.scene.update()
        self.initSearchWidget()
        self.useAOIsTrigger(False)
      
    def clear(self):
        self.graphicsView.scene.undoStack.clear()
        self.graphicsView.scene.clear()
        self.items.clear()
        self.aois.clearContents()
        self.aois.setRowCount(0)
        self.actions[0].trigger()
        
    def fileNew(self):
        self.clear()
        self.graphicsView.scene.update()

    def fileMerge(self):
        filename, _filter = QFileDialog.getOpenFileName(self, "Open File to Merge", '')
        if not filename:
            return
        if not self.graphicsView.scene.filename:
            self.graphicsView.scene.filename = filename
        file = QFile(filename)
        file.open(QIODevice.ReadOnly)
        s = QDataStream(file)
        buildNumber = s.readInt()        
        if (self.BUILD_NUMBER != buildNumber):
            QMessageBox.warning(self, "Warning!", "The data file is in format for build " + str(buildNumber) + ' \nCurrent software build is ' + str(self.BUILD_NUMBER))
        self.graphicsView.scene.load(s, buildNumber, True)            
        self.graphicsView.scene.update()
        
    def fileSave(self, filename=''):
        import shutil, datetime
        if not filename:
            filename = self.graphicsView.scene.filename
        
        if not self.graphicsView.scene.filename:  # run "save as" if no file name
            filename, _filter = QFileDialog.getSaveFileName(self, "Save File As", self.lastDir, "VA Projects (*.vaproj);;All Files (*.*)")
            if not filename:
                return     
        else:
            if os.path.exists(filename):  # create a backup
                path, name = os.path.split(str(self.graphicsView.scene.filename))
                # create 'backups' folder if not there yet
                backupFolder = os.path.join(path, 'backups')
                if not os.path.exists(backupFolder):
                    os.makedirs(backupFolder)
                shutil.move(str(self.graphicsView.scene.filename), os.path.join(path, 'backups', datetime.datetime.today().strftime("%Y%m%d%H%M%S") + ' backup.vaproj'))
        self.lastDir = os.path.dirname(filename)
        file = QFile(filename)
        file.open(QIODevice.WriteOnly)
        s = QDataStream(file)
        s.writeInt(self.BUILD_NUMBER)
        self.graphicsView.scene.save(s)
        self.graphicsView.scene.filename = filename
            
    def fileSaveAs(self):
        filename, _filter = QFileDialog.getSaveFileName(self, "Save File As", self.lastDir, "VA Projects (*.vaproj);;All Files (*.*)")
        if not filename:
            return     
        self.graphicsView.scene.filename = filename
        self.setWindowTitle(self.graphicsView.scene.filename + ' - Video Annotation Tool') 
        self.fileSave()

    def stop(self):
        """Stop player"""
        self.mediaPlayer.stop()
        self.playButton.setIcon(QIcon('icons/player_play.png'))
        
    def setPosition(self, Position):
        """Set the position"""
        self.mediaPlayer.set_position(Position / 1000.0)

    def updateVideo(self, item):
        # print(f'update video {self.graphicsView.scene.time}')
        """Set the position based on the time on Path node"""
        if item.indP == None or item.startTime[item.indP] == None: 
            return
        time = QTime(0, 0).msecsTo(item.startTime[item.indP])
        self.mediaPlayer.set_time(time + 66)
#        print 'scene time '+self.graphicsView.scene.time.toString('hh:mm:ss.zzz')
#        print 'setting video time to '+item.startTime[item.indP].toString('hh:mm:ss.zzz')
        self.updateUI()
        
    def updateUI(self):
        """updates the user interface"""
        # print(f'update ui {self.graphicsView.scene.time}')
        self.seekSlider.setValue(self.mediaPlayer.get_position() * 1000)
        if not self.mediaPlayer.is_playing():
            self.timer.stop()
            if not self.isPaused:
                self.stop()
        
        time = self.mediaPlayer.get_time()
        if time != -1:
            self.graphicsView.scene.time = QTime(0, 0).addMSecs(time)
            if self.graphicsView.scene.currentPath and self.synctaction.isChecked():
#                self.graphicsView.scene.currentPath.time = self.graphicsView.scene.time
                self.graphicsView.scene.currentPath.update()
            self.status.setText(self.graphicsView.scene.time.toString('hh:mm:ss.zzz'))
        else:
            self.status.setText(QTime(0, 0).toString('hh:mm:ss.zzz'))
        if self.graphicsView.scene != None and self.graphicsView.scene.currentPath != None:
            self.graphicsView.scene.loadSignal.emit(self.graphicsView.scene.currentPath)
            
    def deleteAOI(self):
        if self.aois.currentItem():
            self.graphicsView.scene.undoStack.push(RemoveCommand(self.graphicsView.scene, self.aois.currentItem().g))                                        
                
    def onDeleteItem(self):
        if self.items.currentItem():
            currentPath = self.graphicsView.scene.findPath(self.items.currentItem().text())        
            if currentPath:            
                print(f'QMainWindow::onDeleteItem new track id="{currentPath.id}"')
        
                self.graphicsView.scene.undoStack.push(RemoveCommand(self.graphicsView.scene, currentPath))                                        

    def onItemClicked(self, item):
        # Find path by id 
        path = self.graphicsView.scene.findPath(item.text())
        if path == None: 
            return
        print(f'QMainWindow::onItemClicked new track id="{path.id}"')        
        if item.checkState() == Qt.Checked:
            path.setVisible(True)
            self.graphicsView.scene.changeCurrentItemSignal.emit(path.id)            
        else:
            path.setVisible(False)
        
    def onCurrentItemChanged(self, current, previous):
        # if previous:
        #     previousPath = self.graphicsView.scene.findPath(previous.text())
        #     if previousPath:
        #         self.propertyWidget.saveItem(previousPath) 
        
        currentPath = self.graphicsView.scene.findPath(current.text())        
        if currentPath:
            print(f'QMainWindow::onCurrentItemChanged new track id="{currentPath.id}"')            
            current.setCheckState(Qt.Checked)
            currentPath.setVisible(True)
            currentPath.setSelected(True)
            
            self.graphicsView.scene.currentPath = currentPath
            self.propertyWidget.loadItem(currentPath)            
            if currentPath.videoname != '': self.loadVideo(currentPath.videoname)               
            self.timer.start()
            
    def toggleAllItems(self):
        nItems = self.items.count()
        if nItems == 0:
            return
        if self.items.item(0).checkState() == Qt.Unchecked:
            self.checkAllItems(True)
        else: 
            self.checkAllItems(False)
            
    def checkAllItems(self, check=True):
        nItems = self.items.count()
        for n in range(nItems):
            self.items.item(n).setCheckState(Qt.Checked if check else Qt.Unchecked)
            path = self.graphicsView.scene.findPath(self.items.item(n).text())
            if path: path.setVisible(check) 
                            
    def showUndoHistory(self):
        self.undoView.show()
        self.undoView.adjustSize()
        self.undoView.setAttribute(Qt.WA_QuitOnClose, False)

    def predictPath(self):
        self.graphicsView.scene.currentPath.predictPath()
        # find current node x,y, time
        
        # extrapolate based on x,y,z acceleration combined with xyz rotation
       
    def about(self):
        import datetime
        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            application_name = sys.executable
        elif __file__:
            application_name = __file__

        msg = QMessageBox(self);
        msg.setWindowTitle('About')
        msg.setInformativeText(
            """
Video Annotation Tool
<p>Copyright \xa9 2023 Alex Leykin @ Customer Interface Lab </p>
<p>Email: <a href="mailto:cil@indiana.edu">cil@indiana.edu</a></p>
<p><a href="http://cil.iu.edu">http://cil.iu.edu</a></p>

<p>This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.</p>

<p>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.</p>

<p>You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
</p>
"""+ \
            '<p>Build number: ' + str(self.BUILD_NUMBER) + \
            '<p>Build date: ' + time.strftime("%Y-%m-%d %H:%M", time.gmtime(os.path.getmtime(application_name))))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        layout = msg.layout()
        layout.setColumnMinimumWidth(1, 1000)
        msg.exec_()
        return
            
    def initHelp(self):
        from PyQt5 import QtHelp
        self.help = QtHelp.QHelpEngine('help/help.qhc', self)
        ok = self.help.setupData()

        self.helpWindow = QDialog(self, Qt.Window)            
        self.helpWindow.setWindowTitle('Video Annotation Help')
        helpBrowser = helpbrowser.HelpBrowser(self.help)
        helpPanel = QSplitter(Qt.Horizontal)
        helpPanel.addWidget(self.help.contentWidget())
        helpPanel.addWidget(helpBrowser)
        helpPanel.setStretchFactor(1, 4)
        self.helpWindow.setLayout(QVBoxLayout())
        self.helpWindow.layout().addWidget(helpPanel)
        self.helpWindow.setMinimumSize(1200, 1400)
        self.help.contentWidget().linkActivated.connect(helpBrowser.load)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Video Annotation Tool')
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    
    myCSStweaks = '''QWidget{ font-size: 18px; }'''
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5() + myCSStweaks)
    app.setOverrideCursor(Qt.CrossCursor)    
    window = Main()
    window.appPath = application_path
    window.move(1920, 0)
    window.resize(1920, 2160)
    window.show()
    sys.exit(app.exec())

  
if __name__ == "__main__":
    # import vlc
    # # print(vlc.__file__)
    # i=vlc.Instance('--verbose 3')
    # print(type(i))
    # p=i.MediaPlayer()
    main()

