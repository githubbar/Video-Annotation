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
import logging, os, threading, time

from PyQt5.QtCore import Qt, QPointF, QTime, QVariant
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QCheckBox, QTableWidget, QHeaderView, \
    QTableWidgetItem, QFileDialog, QDialog, QWidget, QVBoxLayout, QPushButton

from delegates import URLDelegate
from heatmapSNS import HeatMapSNS
from settings import StrToBoolOrKeep
from torchvision.io import _video_opt
from variableChooserDialog import VariableChooserDialog

TOOLBOX_ITEM_VERTICAL_STEP = 45
class SearchWidget:
    matches = []
    def initSearchWidget(self):
        self.results.setItemDelegate(URLDelegate())        
        self.results.cellDoubleClicked.connect(self.playResultItem)
        self.addFilterWidget(self.checkboxArea, self.listArea, False)
        # self.testHeatmap()

    # Test Heatmap and shaders

    def testHeatmap(self):
        W = int(self.graphicsView.scene.width())
        H = int(self.graphicsView.scene.height())
        hp = []
        for i in range(100, 301, 50):
            hp += [[i,100, 10000*i]]
        p = HeatMapSNS.getPixmap(hp, W, H, self.visRadius.value() * W/100)
        self.graphicsView.scene.heatmap.setPixmap(p)
        self.graphicsView.scene.heatmap.setVisible(True)          

    def addFilterWidget(self, cbParent, lParent, trackLvl=True):
        import operator
        if cbParent != None:
            for i in range(self.checkboxArea.count()): cbParent.itemAt(i).widget().close()
        if lParent != None:
            for i in range(self.listArea.count()): lParent.removeItem(i)        
        sortedList = sorted(self.graphicsView.scene.variables.keys(), key=operator.itemgetter(0))
        # BEGIN TEMP
#         special = "Trip Purpose" 
#         if special in sortedList:
#             sortedList.remove(special)
#             sortedList.insert(0,  QString(special))
        # END TEMP            
        for name in sortedList:
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name]
            vShow = StrToBoolOrKeep(vShow)
            if not vShow:
                continue
            if trackLvl and StrToBoolOrKeep(vEachNode): 
                continue                
            if vType == 'Yes/No' and cbParent != None:
                cbParent.addWidget(QCheckBox(name))
            elif vType in ['DropDown', 'MultiChoice'] and lParent != None:
                w = QTableWidget(self)
                w.setColumnCount(1)                
                w.verticalHeader().setVisible(False)
                w.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                w.setHorizontalHeaderLabels([name])
                lParent.setMinimumHeight(lParent.minimumHeight()+TOOLBOX_ITEM_VERTICAL_STEP)
                lParent.addItem(w, name)
                for i, item in enumerate(vChoices):
                    w.insertRow(i)
                    tableItem = QTableWidgetItem(item)
                    tableItem.setFlags(tableItem.flags() & ~Qt.ItemIsEditable)
                    w.setItem(i, 0, tableItem)
                   
    def searchClicked(self):
        # clear results
        self.matches = []            
        self.results.clearContents()
        self.results.setRowCount(0)        
        self.OnGUIMode(self.GUI_SEARCH)                  
        threading.Thread(target=self.doSearch, name="doSearch").start()

    def matchByCheckable(self, item, cbParent, idx=None):
        # ---------------- filter by CheckBox fields
        for i in range(cbParent.count()): 
            if cbParent.itemAt(i).widget().isChecked():
                name = self.checkboxArea.itemAt(i).widget().text()
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name]
                if StrToBoolOrKeep(vEachNode):
                    if idx != None and not StrToBoolOrKeep(item.variables[name][idx]): return False
                else:
                    if not StrToBoolOrKeep(item.variables[name]): return False
        return True
                    
    def matchByList(self, item, lParent, idx=None):
        for i in range(lParent.count()):  # over all widgets
            widget = lParent.widget(i)
            widgetMatch = len(widget.selectedItems()) == 0            
            name = widget.horizontalHeaderItem(0).text()
            for c in widget.selectedItems():  # over all selected options
                singleMatch = False
                value = c.text()
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name]
                if StrToBoolOrKeep(vEachNode):
                    if idx == None or item.variables[name][idx] == value:  
                        widgetMatch = True
                        break
                else:
                    if not isinstance(item.variables[name], str):
                        print('not string')
                    choices = item.variables[name].split(', ')
                    if value in choices: 
                        widgetMatch = True
                        break
            if not widgetMatch: return False
        return True

    def matchByLineLength(self, item):
        name = 'lineLength'
        vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name]
        if int(item.variables[name][0]) < 2: return True
        else: return False
                            
    def matchByTime(self, item, idx):
        t1 = item.startTime[idx]
        t2 = item.stopTime[idx]
        if not self.timeCheckBox.isChecked() or (t1 > self.startTimeFilter.time() and t2 < self.stopTimeFilter.time()):
            return True
        return False

    def doSearch(self):
        # scan all items
        for i in range(self.items.count()):
            if not self.go: break          
            # FIXME: TypeError: item(self, int): too many arguments                  
            itemId = self.items.item(i).text() 
            item = self.graphicsView.scene.findPath(itemId)
            self.updateProgress.emit(int(100.0 * i / self.items.count()))
            # scan all nodes
            if not self.matchByCheckable(item, self.checkboxArea): continue
            if not self.matchByList(item, self.listArea): continue
            
            for n in range(len(item.polygon)):            
                if not self.matchByCheckable(item, self.checkboxArea, n): continue
                if not self.matchByList(item, self.listArea, n): continue
                if not self.matchByTime(item, n):continue
#                 if not self.matchByLineLength(item):continue
                self.matches.append(Match(item, n))
               
        if self.removeClusters.isChecked():  # remove clustered data
            clusterCenter = QPointF()  # fixation cluster center
            clusterCount = 0  # fixation cluster count
            clusterTime = QTime(0,0)  # fixation cluster time        
            for i, match in enumerate(self.matches):
                p = QPointF(match.item.polygon.at(match.n).x(), match.item.polygon.at(match.n).y())
                if clusterCount > 0 and (\
                (clusterCenter - p).manhattanLength() > 0.01 * self.maxClusterDistance.value() * int(self.graphicsView.scene.width()) \
                or clusterTime.msecsTo(match.item.startTime[match.n]) > 1000 * self.maxClusterTime.value() \
                ):                    
                    clusterCount = 0
                else:
                    clusterCenter = clusterCenter * clusterCount + p * 1
                    clusterTime = match.item.startTime[match.n]
                    clusterCount += 1                
                    self.matches.pop(i)
        self.completeProgress.emit(self.GUI_NORMAL)
        
    def refreshResults(self):
        for i, match in enumerate(self.matches):
            self.results.insertRow(i)
            cID = QTableWidgetItem(match.item.id)
            cTime = QTableWidgetItem(match.toString())
            cID.setData(Qt.UserRole, match.item.id)
            cTime.setData(Qt.UserRole , match)
#             cID.setForeground(QBrush(QColor("blue")))
#             cTime.setForeground(QBrush(QColor("blue")))
            self.results.setItem(i, 0, cID)    
            self.results.setItem(i, 1, cTime)    

    def playResultItem(self, row, col):
        # FIXME: double-click event handler is called twice
        self.tabWidget.setCurrentIndex(0)
        self.checkAllItems(False)       
        result = self.results.item(row, 1).data(Qt.UserRole)        
        self.graphicsView.scene.currentPath = result.item
        self.graphicsView.scene.currentPath.indP = result.n
        self.scene.changeCurrentItemSignal.emit(self.graphicsView.scene.currentPath.id)      
        if self.mediaPlayer.play() != -1:            
            self.playButton.setIcon(QIcon('icons/player_pause.png'))
            self.timer.start()
            self.isPaused = False        
        # Wait for mediPlayer  to play after playClicked()        
        for i in range(100): 
            time.sleep(0.01) 
            if self.mediaPlayer.is_playing(): break
        self.updateVideo(self.graphicsView.scene.currentPath)        
        
    def visClicked(self):
        self.OnGUIMode(self.GUI_EXPORT)
        ids = set()  # set of subject ids found in matches

        # add data points        
        hp = []
        for i, match in enumerate(self.matches):
            id = match.item.id
            if not id in ids:                 
                ids.add(id)  # add subject id to the set
                        
            self.progressBar.setValue(int(100.0 * i / len(self.matches)))         
            # self.searchWidget.repaint()          
            if not self.go: 
                hp = []
                break                
            n = match.n
            addThis = True
#            if self.visPurchased.isChecked(): addThis &= StrToBoolOrKeep(match.item.purchased[n])
#            if self.visShopped.isChecked(): addThis &= StrToBoolOrKeep(match.item.shopped[n])
            if not addThis: continue
            pt = match.item.polygon.at(n)
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            if t > 0:
                hp += [[int(pt.x()), int(pt.y()), t]]
        if len(ids)==0:
            return
        nSubjects = len(set([x.item.id for x in  self.matches]))
        # print(nSubjects)
        # print("N.Subjects = " + str(len(ids)))
        W = int(self.graphicsView.scene.width())
        H = int(self.graphicsView.scene.height())
        p = HeatMapSNS.getPixmap(hp, W, H, self.visRadius.value() * W/100, nSubjects, self.colorScale.value())
        self.graphicsView.scene.heatmap.setPixmap(p)
        self.graphicsView.scene.heatmap.setVisible(True)          
        self.OnGUIMode(self.GUI_NORMAL)          

    def exportImageClicked(self):
        # choose export file
        outFileName, _filter = QFileDialog.getSaveFileName(self, "Choose File to Export To", os.getcwd())
        if not outFileName:
            return
        self.graphicsView.grab().save(outFileName)
        
    def exportVideoClicked(self):
        # choose export folder
        outDir = QFileDialog.getExistingDirectory(self, "Choose Folder to Export To", os.getcwd())
        if not outDir:
            return        
        self.OnGUIMode(self.GUI_EXPORT)                  
        threading.Thread(target=self.doExportVideo, name="exportVideoThread", args=(outDir,)).start()
        
    def doExportVideo(self, outDir):
        import subprocess, re        
 
        for i, match in enumerate(self.matches):
            self.updateProgress.emit(int(100.0 * i / len(self.matches)))
            
            inFileName = os.path.join(os.path.dirname(str(self.graphicsView.scene.filename)), str(match.item.videoname))
  
            t1 = match.item.startTime[match.n]
            t2 = match.item.stopTime[match.n]
           
            cat = match.item.variables['Category Shopped'][match.n]
            if cat:
                cat = cat.replace('/', '-')
                cat = cat.replace(':', '-')
            else:
                cat = ''
            outFileName = os.path.join(str(outDir), str(match.item.id + ' from ' + t1.toString('hh-mm-ss') + ' to ' + t2.toString('hh-mm-ss') + ' ' + cat + '.avi'))
            if os.path.exists(inFileName):
                logging.debug('Current working directory is ' + str(os.getcwd()))              
                p = subprocess.Popen(['ffmpeg', '-ss', str(QTime(0,0).secsTo(t1)), '-t', str(t1.secsTo(t2)), '-i', inFileName, \
                '-async', '1', '-y', outFileName], shell=True)
                p.wait()
                logging.debug('ffmpeg' + ' -ss ' + str(QTime(0,0).secsTo(t1)) + ' -t ' + str(t1.secsTo(t2)) + ' -i ' + str(inFileName) + ' -y ' + str(outFileName))
            if not self.go: break
        self.completeProgress.emit(self.GUI_NORMAL)
       
    def exportDataClicked(self):
        # choose export file
        outFileName, _filter = QFileDialog.getSaveFileName(self, "Choose File to Export To", os.getcwd())
        if not outFileName:
            return
        
        varDialog = VariableChooserDialog(self.graphicsView.scene.variables)
        if varDialog.exec_() == QDialog.Rejected:
            return
        
        self.OnGUIMode(self.GUI_EXPORT)
        varNames = [b.text() for b in varDialog.listArea.findChildren(QPushButton) if b.isChecked()]
        threading.Thread(target=self.doExportMatchData, name="exportDataThread", args=(outFileName, varNames)).start()

    def doExportMatchData(self, outFileName, varNames):
        import csv
        builtInVarNames = ['id', 'node number', 'x', 'y', 'video name', 'startTime', 'stopTime']
          
        allVarNames = builtInVarNames + varNames
        # print(f'varNames = {varNames}')
        with open(outFileName, 'w') as csvfile:
            writer = csv.writer(csvfile)        
            writer.writerow(allVarNames)
            for i, match in enumerate(self.matches):
                self.updateProgress.emit(int(100.0 * i / len(self.matches)))
                row = [ str(match.item.id), str(match.n), \
                       str(match.item.polygon.at(match.n).x()), str(match.item.polygon.at(match.n).y()), \
                       str(match.item.videoname), \
                  str(match.item.startTime[match.n].toString('hh-mm-ss')), \
                  str(match.item.stopTime[match.n].toString('hh-mm-ss')) ]
                  
                varList = match.item.getVariableValuesList(match.n, varNames)
                row.extend(varList)
                try:
                    writer.writerow(row)
                except UnicodeEncodeError: 
                    continue
                if not self.go: break
                
        self.completeProgress.emit(self.GUI_NORMAL)
 
    def updateStatsClicked(self):
        # clear results        
        self.OnGUIMode(self.GUI_UPDATESTATS)                  
        threading.Thread(target=self.doUpdateStats, name="updateStatsThread").start()

    def exportAOIDataClicked(self):
        # choose export file
        outFileName, _filter = QFileDialog.getSaveFileName(self, "Choose File for Individual AOI Data Export", os.getcwd())
        if not outFileName:
            return
        self.OnGUIMode(self.GUI_EXPORT)                  
        threading.Thread(target=self.doExportIndividualAOIData, name="exportAOIDataThread", args=(outFileName,)).start()
        
    def doExportIndividualAOIData(self, outFileName):
        import subprocess, csv
        ids = set()  # set of subject ids found in matches
        items = {}
        duration = {}    
        for i, match in enumerate(self.matches):
#             TODO: check 2 int() conversions in this file
            subjID = int(match.item.id[0])
            self.updateProgress.emit(round(100.0 * i / len(self.matches), 2))
            if not subjID in ids:
                duration[subjID] = [0] * self.aois.count()
                items[subjID] = match.item        
            ids.add(subjID)  # add subject id to the set
            if not self.go: 
                break                
            p = QPointF(match.item.polygon.at(match.n).x(), match.item.polygon.at(match.n).y())
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            for row in range(self.aois.count()):
                aoi = self.aois.item(row, 0).g
                if aoi.contains(p):
                    duration[subjID][row] += t
                    
    
        writer = csv.writer(open(outFileName, 'wb'))          
        varNames = ['id']
        varNames.extend([str(key) for key in self.graphicsView.scene.variables.keys()])
        for row in range(self.aois.count()):
            varNames.append(str(self.aois.item(row, 0).text()))
 
    
        writer.writerow(varNames)
        for subjID in ids:
            line = [subjID]
            line.extend(items[subjID].getVariableValuesList())

            for row in range(self.aois.count()):
                line.append(0.001 * duration[subjID][row])
            try:
                writer.writerow(line)
            except UnicodeEncodeError: 
                continue
            if not self.go: break
                               
        self.completeProgress.emit(self.GUI_NORMAL)
        
    def doUpdateStats(self):
        # add data points        
        print('updating stats!')
        ids = set()  # set of subject ids found in matches
        duration = {}  # dictionary of fixation durations
        durationNoClusters = {}  # dictionary of fixation durations exluding clusters > x sec
        fixated = {}  # dictionary of sets of ids fixated on AOI
        tripDuration = 0  # total cumultative trip duration (from first to last gazepoint)
        videoDuration = 0  # total trip duration (length of video file)
        for i in range(self.aois.count()):
            duration[i] = 0
            durationNoClusters[i] = 0
            fixated[i] = set()
         
        for i, match in enumerate(self.matches):
            id = match.item.id
            self.updateProgress.emit(round(100.0 * i / len(self.matches), 2))    
            if not id in ids:
                minTime = maxTime = QTime(0,0).msecsTo(match.item.startTime[0])
                for t in match.item.startTime:
                    if QTime(0,0).msecsTo(t) < minTime:
                        minTime = QTime(0,0).msecsTo(t) 
                    if QTime(0,0).msecsTo(t) > maxTime:
                        maxTime = QTime(0,0).msecsTo(t)                         
                tripDuration += maxTime - minTime
                self.loadVideo(match.item.videoname)
                videoDuration += self.Media.get_duration()
 
            ids.add(id)  # add subject id to the set
            if not self.go: 
                break                
            p = QPointF(match.item.polygon.at(match.n).x(), match.item.polygon.at(match.n).y())
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            for row in range(self.aois.count()):
                aoi = self.aois.item(row, 0).g
                if aoi.contains(p):
                    duration[row] += t
                    fixated[row].add(id)
        if (len(ids) > 0):
            for row in range(self.aois.count()):
                if len(fixated[row]) > 0:
                    self.aois.item(row, 1).setText(str(round(0.001 * duration[row] / len(fixated[row]), 2)))
                    self.aois.item(row, 2).setText(str(round(100.0 * len(fixated[row]) / len(ids), 1)))            
                    self.aois.item(row, 3).setText(str(len(fixated[row])))
                else:
                    self.aois.item(row, 1).setText('0.0')
                    self.aois.item(row, 2).setText('0.0')            
                    self.aois.item(row, 3).setText('0.0')
     
            self.aois.horizontalHeaderItem(3).setText(f'Number of Subjects: Total = {len(ids)} (avg. trip = {round(0.001 * tripDuration / len(ids), 2)} sec.) \
                                                      (avg. video = {round(0.001 * videoDuration / len(ids), 2)} sec.)')
             
        self.completeProgress.emit(self.GUI_NORMAL)
    
    def showHistogramClicked(self):
        from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
        from matplotlib.figure import Figure
        from collections import OrderedDict
        self.OnGUIMode(self.GUI_UPDATESTATS)                  
        dlg = QDialog(self, Qt.Window)
        dlg.setWindowTitle('Data Distribution for Subjects')
        plot = QWidget()
        dlg.setLayout(QVBoxLayout())
        dlg.layout().addWidget(plot)
        dlg.setMinimumSize(1200, 930)        
        dpi = 300
        fig = Figure((4.0, 3.0), dpi=dpi)
        fig.set_frameon(False)
        canvas = FigureCanvas(fig)
        canvas.setParent(plot)
        axes = fig.add_subplot(111)
#         canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)        
        
        # find number of gazepoints for each id
        ids = set()  # set of subject ids found in matches
        duration = {}  # dictionary of fixation durations
        
        for i, match in enumerate(self.matches):
            id = match.item.id
            self.updateProgress.emit(round(100.0 * i / len(self.matches), 2))
            if not id in ids:
                duration[id] = 0        
            ids.add(id)  # add subject id to the set        
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            duration[id] += t
            
        data = OrderedDict(sorted(duration.items(), key=lambda t: t[0]))
        axes.clear()        
        axes.grid(True)
        axes.bar(
            left=range(len(data)),
            height=sorted([0.001 * x for x in data.values()], reverse=True),
            width=0.9,
            color='g',
            alpha=0.44,
            picker=5)
        axes.grid('off')
        axes.set_xticks([])        
#         axes.set_xticks(range(len(data)))
#         axes.set_xticklabels(data.keys(), fontdict=None, minor=False, size='6',rotation=60)
        axes.set_ylim(0, 200)
        for tick in axes.get_yticklabels():
            tick.set_fontsize(6)
        axes.set_xlabel('Subjects')
        axes.set_ylabel('Total Fixations (sec)')
        fig.subplots_adjust(bottom=0.20)

        fig.savefig('gazepoint histogram.png', dpi=300)
        dlg.exec_() 
        self.completeProgress.emit(self.GUI_NORMAL)
        
    def exportStatsClicked(self):
        # choose export file
        outFileName, _filter = QFileDialog.getSaveFileName(self, "Choose File for AOI Statistics Export", os.getcwd())
        if not outFileName:
            return
        self.OnGUIMode(self.GUI_EXPORT)                  
        threading.Thread(target=self.doExportStats, name="exportStatsThread", args=(outFileName,)).start()

    def doExportStats(self, outFileName):
        import subprocess, csv
        writer = csv.writer(open(outFileName, 'wb'))         
        varNames = ['AOI', 'Average Duration', 'Percentage Fixated', 'Number of Subjects']
        writer.writerow(varNames)
        for row in range(self.aois.count()):
            self.updateProgress.emit(int(100.0 * row / self.aois.count()))           
            row = [ str(self.aois.item(row, 0).text()), str(self.aois.item(row, 1).text()), str(self.aois.item(row, 2).text()), str(self.aois.item(row, 3).text())]
            try:
                writer.writerow(row)
            except UnicodeEncodeError: 
                continue
            if not self.go: break
        self.completeProgress.emit(self.GUI_NORMAL)

    def cancelClicked(self):
        self.go = False
        
    def OnUpdateProgress(self, now):
        self.progressBar.setValue(now)
        self.searchWidget.repaint()     
    
    def OnUpdateProgressEdit(self, now):
        self.progressBarEdit.setValue(now)
        self.repaint()   
                               
    def OnGUIMode(self, searchMode=None):
        if searchMode == self.GUI_NORMAL or searchMode == None:
            self.go = False
            self.searchCancel.hide()                     
            self.exportCancel.hide()                  
            self.progressBar.reset()
            self.progressBar.hide() 
            self.progressBarEdit.reset()
            self.progressBarEdit.hide()            
            self.searchButton.setEnabled(True) 
            self.exportData.setEnabled(True) 
            self.exportVideo.setEnabled(True)  
            self.exportStats.setEnabled(True) 
            self.updateStats.setEnabled(True) 
            self.searchWidget.repaint() 
            self.refreshResults()
            
        elif searchMode == self.GUI_EXPORT:
            self.go = True
            self.exportCancel.show()            
            self.progressBar.reset()
            self.progressBar.show() 
            self.searchButton.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportData.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportStats.setEnabled(False) 
            self.updateStats.setEnabled(False) 
            self.progressBar.setValue(0)     
            self.searchWidget.repaint() 
            
        elif searchMode == self.GUI_SEARCH:
            self.go = True
            self.progressBar.setValue(100)         
            self.searchCancel.show()            
            self.progressBar.reset()
            self.progressBar.show() 
            self.searchButton.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportData.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportStats.setEnabled(False) 
            self.updateStats.setEnabled(False) 
            self.progressBar.setValue(0)     
            self.searchWidget.repaint() 
        
        elif searchMode == self.GUI_UPDATESTATS:
            self.go = True
            self.progressBar.setValue(100)         
            self.searchCancel.show()            
            self.progressBar.reset()
            self.progressBar.show() 
            self.searchButton.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportData.setEnabled(False) 
            self.exportVideo.setEnabled(False) 
            self.exportStats.setEnabled(False) 
            self.updateStats.setEnabled(False) 
            self.progressBar.setValue(0)     
            self.searchWidget.repaint() 
                
class Match:
    def __init__(self, item, n):
        self.item = item
        self.n = n

    def toString(self):
        return self.item.startTime[self.n].toString('hh:mm:ss')
