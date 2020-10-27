from Ui_window import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from heatmap import HeatMap        
from track import Path
from annotateview import AnnotateScene
from delegates import *
import os, threading, logging, time
import matplotlib
TOOLBOX_ITEM_VERTICAL_STEP = 60
class SearchWidget:
    matches = []
    def initSearchWidget(self):
        self.results.setItemDelegate(URLDelegate())        
        self.results.cellDoubleClicked.connect(self.playResultItem)
        self.addFilterWidget(self.checkboxArea, self.listArea, False)
#         self.testHeatmap()

    # Test Heatmap and shaders
    def testHeatmap(self):

        paletteFile = 'palettes/jet.png'
        heatmapScale = 4.0
        W = int(self.graphicsView.scene.width())
        H = int(self.graphicsView.scene.height())
        heatmapBox = [0, W, 0, H]
        hp = [(100,100),(120,100),(100,120)]
        hm = HeatMap(heatmapBox[0], int(heatmapBox[1] * heatmapScale), heatmapBox[2], int(heatmapBox[3] * heatmapScale), paletteFile)
        hm.add_points(hp, self.visRadius.value() * W/100, self.colorScale.value()*256.0 / len(hp))
        heat = hm.get_min_max_heat()
        print('minHeat = ' + str(heat[0]) + ' maxHeat = ' + str(heat[1]))
        hm.transform_color(0.01 * self.visAlpha.value())
        p = QPixmap.fromImage(QImage(hm.get_image_buffer(), hm.width, hm.height, QImage.Format_ARGB32))
        self.graphicsView.scene.heatmap.setPixmap(p)
        self.graphicsView.scene.heatmap.setScale(1.0 / heatmapScale)
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
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name].toList()
            if not vShow.toBool():
                continue
            if trackLvl and vEachNode.toBool(): 
                continue                
            if vType == 'Yes/No' and cbParent != None:
                cbParent.addWidget(QCheckBox(name))
            elif vType in ['DropDown', 'MultiChoice'] and lParent != None:
                w = QTableWidget(self)
                w.setColumnCount(1)                
                w.verticalHeader().setVisible(False)
                w.horizontalHeader().setResizeMode(QHeaderView.Stretch)
                w.setHorizontalHeaderLabels([name])
                lParent.setMinimumHeight(lParent.minimumHeight()+TOOLBOX_ITEM_VERTICAL_STEP)
                lParent.addItem(w, name)
                for i, item in enumerate(vChoices.toList()):
                    w.insertRow(i)
                    tableItem = QTableWidgetItem(item)
                    tableItem.setFlags(tableItem.flags() & ~Qt.ItemIsEditable)
                    w.setItem(i, 0, tableItem)
                   
#             elif vType in ['Integer'] and lParent != None:
#                 w = QSpinBox(self)
#                 w.setMinimumHeight(240)
#                 lParent.addItem(w,  name)
#                 for i,  item in enumerate(vChoices.toList()):
#                     w.insertRow(i)
#                     i.setFlags(i.flags() & ~Qt.ItemIsEditable)
#                     w.setItem(i, 0,  QTableWidgetItem(item))
      

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
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name].toList()
                if vEachNode.toBool():
                    if idx != None and not item.variables[name].toList()[idx].toBool(): return False
                else:
                    if not item.variables[name].toBool(): return False
        return True
                    
    def matchByList(self, item, lParent, idx=None):
        for i in range(lParent.count()):  # over all widgets
            widget = lParent.widget(i)
            widgetMatch = len(widget.selectedItems()) == 0            
            name = widget.horizontalHeaderItem(0).text()
            for c in widget.selectedItems():  # over all selected options
                singleMatch = False
                value = c.text()
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name].toList()
                if vEachNode.toBool():
                    if idx == None or item.variables[name].toList()[idx] == value:  
                        widgetMatch = True
                        break
                else:
                    choices = item.variables[name].split(', ')
                    if value in choices: 
                        widgetMatch = True
                        break
            if not widgetMatch: return False
        return True

    def matchByLineLength(self, item):
        name = 'lineLength'
        vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.graphicsView.scene.variables[name].toList()
        if item.variables[name].toInt()[0] < 2: return True
        else: return False
    
                            
    def matchByTime(self, item, idx):
        t1 = item.startTime[idx]
        t2 = item.stopTime[idx]
        if not self.timeCheckBox.isChecked() or (t1 > self.startTimeFilter.time() and t2 < self.stopTimeFilter.time()):
            return True
        return False

    def doSearch(self):
        # scan all items
        for i in range(self.items.rowCount()):
            if not self.go: break                            
            item = self.items.item(i, 0).g
            self.updateProgress.emit(int(100.0 * i / self.items.rowCount()))
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
            clusterTime = QTime()  # fixation cluster time        
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
            cTime = QTableWidgetItem(match)
            cID.setData(Qt.UserRole, match.item.id)
            cTime.setData(Qt.UserRole , QVariant(match))
#             cID.setForeground(QBrush(QColor("blue")))
#             cTime.setForeground(QBrush(QColor("blue")))
            self.results.setItem(i, 0, cID)    
            self.results.setItem(i, 1, cTime)    

    def playResultItem(self, row, col):
        # FIXME: double-click event handler is called twice
        self.tabWidget.setCurrentIndex(0)
        self.checkAllItems(False)       
        result = self.results.item(row, 1).data(Qt.UserRole).toPyObject()        
        self.graphicsView.scene.currentPath = result.item
        self.graphicsView.scene.currentPath.indP = result.n
        self.changeCurrentItem()      
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
        paletteFile = 'palettes/jet.png'
        heatmapScale = 4.0
        W = int(self.graphicsView.scene.width())
        H = int(self.graphicsView.scene.height())
        heatmapBox = [0, W, 0, H]
        hm = HeatMap(heatmapBox[0], int(heatmapBox[1] * heatmapScale), heatmapBox[2], int(heatmapBox[3] * heatmapScale), paletteFile)
       
        # add data points        
        hp = []
        for i, match in enumerate(self.matches):
            id = match.item.id
            if not id in ids:                 
                ids.add(id)  # add subject id to the set
                        
            self.progressBar.setValue(int(100.0 * i / len(self.matches)))         
            self.searchWidget.repaint()          
            if not self.go: 
                hp = []
                break                
            n = match.n
            addThis = True
#            if self.visPurchased.isChecked(): addThis &= match.item.purchased[n].toBool()
#            if self.visShopped.isChecked(): addThis &= match.item.shopped[n].toBool()
            if not addThis: continue
            # create as many points as there are seconds
            if self.visUseTime.isChecked():
                count = match.item.startTime[n].secsTo(match.item.stopTime[n])
            else: count = 1
            for c in range(count):
                hp += [(match.item.polygon.at(n).x() * heatmapScale, match.item.polygon.at(n).y() * heatmapScale)]

        if len(ids)==0:
            return
#         hm.add_points(hp, self.visRadius.value() * heatmapScale, self.colorScale.value() / len(ids))
        hm.add_points(hp, self.visRadius.value() * W/100, self.colorScale.value()*256.0 / len(hp))
        heat = hm.get_min_max_heat()
        print("N.Subjects = " + str(len(ids)))
        print('minHeat = ' + str(heat[0]) + ' maxHeat = ' + str(heat[1]))
#         hm.transform_color(0.01 * self.visAlpha.value())
        hm.transform_color(0.01 * self.visAlpha.value())
        p = QPixmap.fromImage(QImage(hm.get_image_buffer(), hm.width, hm.height, QImage.Format_ARGB32))
        self.graphicsView.scene.heatmap.setPixmap(p)
        self.graphicsView.scene.heatmap.setScale(1.0 / heatmapScale)
        self.graphicsView.scene.heatmap.setVisible(True)          
        self.OnGUIMode(self.GUI_NORMAL)          

    def exportImageClicked(self):
        # choose export file
        outFileName = QFileDialog.getSaveFileName(self, "Choose File to Export To", os.getcwd())
        if not outFileName:
            return
        QPixmap.grabWidget(self.graphicsView).save(outFileName)
        
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
           
            cat = match.item.variables['category'].toList()[match.n]
            cat = cat.replace('/', '-')
            cat = cat.replace(':', '-')
            outFileName = os.path.join(str(outDir), str(match.item.id + ' from ' + t1.toString('hh-mm-ss') + ' to ' + t2.toString('hh-mm-ss') + ' ' + cat + '.avi'))
            if os.path.exists(inFileName):
                logging.debug('Current working directory is ' + str(os.getcwd()))              
                p = subprocess.Popen(['ffmpeg', '-ss', str(QTime().secsTo(t1)), '-t', str(t1.secsTo(t2)), '-i', str(inFileName), \
                '-async', '1', '-y', str(outFileName)], shell=True)
                p.wait()
                logging.debug('ffmpeg' + ' -ss ' + str(QTime().secsTo(t1)) + ' -t ' + str(t1.secsTo(t2)) + ' -i ' + str(inFileName) + ' -y ' + str(outFileName))
            if not self.go: break
        self.completeProgress.emit(self.GUI_NORMAL)
       
    def exportDataClicked(self):
        # choose export file
        outFileName = QFileDialog.getSaveFileName(self, "Choose File to Export To", os.getcwd())
        if not outFileName:
            return
        self.OnGUIMode(self.GUI_EXPORT)
        threading.Thread(target=self.doExportMatchData, name="exportDataThread", args=(outFileName,)).start()

    def doExportMatchData(self, outFileName):
        import subprocess, csv
        # BEGIN TEMP
#         ids = set() # set of subject ids found in matches
#         for i,  match in enumerate(self.matches):
#             id = match.item.id
#             self.updateProgress.emit(int(100.0*i/len(self.matches)), 2)        
#             if not id in ids:
#                 ids.add(id) 
#         writer = csv.writer(open(outFileName, 'wb'))         
#         for id in ids:
#             writer.writerow([id])
#         self.completeProgress.emit(self.GUI_NORMAL)
#         return
        # END TEMP
        print('running 1')
        writer = csv.writer(open(outFileName, 'wb'))         
        varNames = ['id', 'node number', 'x', 'y', 'video name', 'startTime', 'stopTime']
        varNames.extend([str(key) for key in self.graphicsView.scene.variables.keys()])   
        writer.writerow(varNames)
        for i, match in enumerate(self.matches):
            self.updateProgress.emit(int(100.0 * i / len(self.matches)))
            varList = match.item.getVariableValuesList(match.n)
            row = [ str(match.item.id), str(match.n), \
                   str(match.item.polygon.at(match.n).x()), str(match.item.polygon.at(match.n).y()), \
                   str(match.item.videoname), \
              str(match.item.startTime[match.n].toString('hh-mm-ss')), \
              str(match.item.stopTime[match.n].toString('hh-mm-ss')) ]
            print('running 2')
            row.extend(varList)
            # TODO: write unicode to CSV, also in Path.py line 335
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
        outFileName = QFileDialog.getSaveFileName(self, "Choose File for Individual AOI Data Export", os.getcwd())
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
            subjID = match.item.id.toInt()[0]
            self.updateProgress.emit(int(100.0 * i / len(self.matches)), 2)
            if not subjID in ids:
                duration[subjID] = [0] * self.aois.rowCount()
                items[subjID] = match.item        
            ids.add(subjID)  # add subject id to the set
            if not self.go: 
                break                
            p = QPointF(match.item.polygon.at(match.n).x(), match.item.polygon.at(match.n).y())
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            for row in range(self.aois.rowCount()):
                aoi = self.aois.item(row, 0).g
                if aoi.contains(p):
                    duration[subjID][row] += t
                    
    
        writer = csv.writer(open(outFileName, 'wb'))          
        varNames = ['id']
        varNames.extend([str(key) for key in self.graphicsView.scene.variables.keys()])
        for row in range(self.aois.rowCount()):
            varNames.append(str(self.aois.item(row, 0).text()))
 
    
        writer.writerow(varNames)
        for subjID in ids:
            line = [subjID]
            line.extend(items[subjID].getVariableValuesList())

            for row in range(self.aois.rowCount()):
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
        for i in range(self.aois.rowCount()):
            duration[i] = 0
            durationNoClusters[i] = 0
            fixated[i] = set()
         
        for i, match in enumerate(self.matches):
            id = match.item.id
            self.updateProgress.emit(int(100.0 * i / len(self.matches)), 2)        
            if not id in ids:
                minTime = maxTime = QTime().msecsTo(match.item.startTime[0])
                for t in match.item.startTime:
                    if QTime().msecsTo(t) < minTime:
                        minTime = QTime().msecsTo(t) 
                    if QTime().msecsTo(t) > maxTime:
                        maxTime = QTime().msecsTo(t)                         
                tripDuration += maxTime - minTime
                self.loadVideo(match.item.videoname)
                videoDuration += self.Media.get_duration()
 
            ids.add(id)  # add subject id to the set
            if not self.go: 
                break                
            p = QPointF(match.item.polygon.at(match.n).x(), match.item.polygon.at(match.n).y())
            t = match.item.startTime[match.n].msecsTo(match.item.stopTime[match.n])
            for row in range(self.aois.rowCount()):
                aoi = self.aois.item(row, 0).g
                if aoi.contains(p):
                    duration[row] += t
                    fixated[row].add(id)
        if (len(ids) > 0):
            for row in range(self.aois.rowCount()):
                if len(fixated[row]) > 0:
                    self.aois.item(row, 1).setText(str(round(0.001 * duration[row] / len(fixated[row]), 2)))
                    self.aois.item(row, 2).setText(str(round(100.0 * len(fixated[row]) / len(ids), 1)))            
                    self.aois.item(row, 3).setText(str(len(fixated[row])))
                else:
                    self.aois.item(row, 1).setText('0.0')
                    self.aois.item(row, 2).setText('0.0')            
                    self.aois.item(row, 3).setText('0.0')
     
            self.aois.horizontalHeaderItem(3).setText('Number of Subjects: Total =' + str(len(ids)) + ' (avg. trip = ' + str(0.001 * tripDuration / len(ids)) + ' sec.)' + \
                                                      ' (avg. video = ' + str(0.001 * videoDuration / len(ids)) + ' sec.)')
             
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
            self.updateProgress.emit(int(100.0 * i / len(self.matches)), 2)
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
        outFileName = QFileDialog.getSaveFileName(self, "Choose File for AOI Statistics Export", os.getcwd())
        if not outFileName:
            return
        self.OnGUIMode(self.GUI_EXPORT)                  
        threading.Thread(target=self.doExportStats, name="exportStatsThread", args=(outFileName,)).start()

    def doExportStats(self, outFileName):
        import subprocess, csv
        writer = csv.writer(open(outFileName, 'wb'))         
        varNames = ['AOI', 'Average Duration', 'Percentage Fixated', 'Number of Subjects']
        writer.writerow(varNames)
        for row in range(self.aois.rowCount()):
            self.updateProgress.emit(int(100.0 * row / self.aois.rowCount()))           
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
