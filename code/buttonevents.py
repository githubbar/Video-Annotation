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
"""Define button/checkbox/tab event handlers for the main window"""
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QProgressDialog

from filterdialog import FilterDialog
from projectdialog import ProjectDialog
from snapshot import Snapshot
from track import Path
from variabledialog import VariableDialog


class ButtonEvents():
    def tabChanged(self,  index):
        if index == 0: # edit
            self.actions[0].trigger() # switch to select mode                
            self.graphicsView.scene.heatmap.setVisible(False)    
            self.splitterEditTop.insertWidget(0, self.graphicsView)
            self.graphicsView.scene.showBackground = True
            self.graphicsView.fitSceneInView()       
            self.graphicsView.scale(0.7, 0.7)
            self.useAOIsTrigger(False)
        if index == 1: # search
            if not self.READ_ONLY:
                self.actions[7].trigger() # switch to AOI
            self.graphicsView.scene.heatmap.setVisible(True)     
            self.graphicsView.scene.showBackground = False
            self.splitterSearch.insertWidget(0, self.graphicsView)
            self.initSearchWidget()        
            self.graphicsView.fitSceneInView()      
            self.useAOIsTrigger(True)
            self.useAOIs.setCheckState(Qt.Checked)
    
    def useAOIsTrigger(self, show):
            self.graphicsView.scene.setAOIVisible(show)

            
    def handleToolbarButton(self):
        sender = self.sender()
        if not sender.isChecked():
            sender.toggle()
        for a in self.actions: 
            if a != sender:
                a.setChecked(False)
        self.graphicsView.scene.mode = sender.text()
       
        #
        # # Update track visibility based on items list checkboxes
        # for n in range(self.items.count()):
        #     if self.items.item(n, 0).checkState() == Qt.Checked:
        #         self.items.item(n, 0).g.setVisible(True)
        #     else:
        #         self.items.item(n, 0).g.setVisible(False)

        # Select or Path modes: show Paths and disable static figures
        paths = (self.graphicsView.scene.mode == 'Select' or self.graphicsView.scene.mode == 'Path') and (self.tabWidget.currentIndex() == 0)
        snapshot = (self.graphicsView.scene.mode == 'Select' or self.graphicsView.scene.mode == 'Snapshot' or  self.graphicsView.scene.mode == 'Edit')
        for i in list(self.graphicsView.scene.items()):
            if type(i) == Path:
                i.setVisible(i.isVisible() and paths)
            elif type(i) == Snapshot:
                i.setEnabled(snapshot)
                if snapshot: i.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
                else: i.setAcceptedMouseButtons(Qt.NoButton)
            else:
                i.setEnabled(not paths)
                if paths: i.setAcceptedMouseButtons(Qt.NoButton)
                else: i.setAcceptedMouseButtons(Qt.LeftButton | Qt.RightButton)
        # Show AOIs only in AOI and Edit mode
        self.useAOIsTrigger(self.graphicsView.scene.mode == 'AOI' or self.graphicsView.scene.mode == 'Edit')
               
        
    def handleFullScreen(self):
        qtMax = 16777215
        if self.fullScreen:
            self.upperPanel.setMaximumHeight(qtMax) 
            self.items.setMaximumWidth(qtMax) 
            self.checkAll.setMaximumWidth(qtMax) 
        else:
            self.upperPanel.setMaximumHeight(0)
            self.items.setMaximumWidth(0) 
            self.checkAll.setMaximumWidth(0) 
        self.fullScreen = not self.fullScreen
        
    def playClicked(self):
        if self.mediaPlayer.is_playing():
            self.mediaPlayer.pause()
            self.playButton.setIcon(QIcon('icons/player_play.png'))
            self.isPaused = True
        elif self.mediaPlayer.play() != -1:            
            self.playButton.setIcon(QIcon('icons/player_pause.png'))
            self.timer.start()
            self.isPaused = False        

    def showProjectProperties(self):
        projectDialog = ProjectDialog(self)
        projectDialog.spinnerW.setValue(self.graphicsView.scene.width())
        projectDialog.spinnerH.setValue(self.graphicsView.scene.height())
        projectDialog.backgroundFileEdit.setText(self.graphicsView.scene.backgroundPath)
        projectDialog.nodeColor = self.graphicsView.scene.nodeColor
        projectDialog.colorButton.setStyleSheet("background-color: "+projectDialog.nodeColor.name())
        projectDialog.pathSmoothingSlider.setValue(int(self.graphicsView.scene.pathSmoothingFactor*100))
        projectDialog.nodeSizeSlider.setValue(int(self.graphicsView.scene.nodeSize*100))
        projectDialog.showSegments.setChecked(self.graphicsView.scene.showSegments)
        projectDialog.showOrientation.setChecked(self.graphicsView.scene.showOrientation)
        projectDialog.showOnlyCurrent.setChecked(self.graphicsView.scene.showOnlyCurrent)
#        projectDialog.setModal(True)
        if projectDialog.exec_() == QDialog.Accepted:
#            if QMessageBox.question(self,  'Warning!', 'Saving these changes to your project will affect all the existing data! Are you sure you want to proceed?', \
#                QMessageBox.Yes | QMessageBox.No) == QMessageBox.No: 
#                    return            
            self.graphicsView.scene.setSceneRect(0, 0, projectDialog.spinnerW.value(),  projectDialog.spinnerH.value())
            self.graphicsView.scene.backgroundPath = str(projectDialog.backgroundFileEdit.text())
            self.graphicsView.scene.nodeColor = projectDialog.nodeColor
            self.graphicsView.scene.pathSmoothingFactor = 0.01*projectDialog.pathSmoothingSlider.value()
            self.graphicsView.scene.nodeSize = 0.01*projectDialog.nodeSizeSlider.value()
            self.graphicsView.scene.showSegments = projectDialog.showSegments.isChecked()
            self.graphicsView.scene.showOrientation = projectDialog.showOrientation.isChecked()
            self.graphicsView.scene.showOnlyCurrent = projectDialog.showOnlyCurrent.isChecked()
            
            # update scene properties to reflect the new settings
            self.graphicsView.scene.updateProjectProperties()
            # update SearchWidget
            self.initSearchWidget()        
            
    def showFilterDialog(self):
        filterDialog = FilterDialog(self)
        filterDialog.checkboxScrollArea.setVisible(False)
        filterDialog.layout().removeWidget(filterDialog.checkboxScrollArea)
        self.addFilterWidget(None, filterDialog.listArea, False)
        if filterDialog.exec_() == QDialog.Accepted:
            progress= QProgressDialog('Filtering records...', 'Cancel', 0, self.items.count(), self)
            progress.setWindowModality(Qt.WindowModal)

            for i in range(self.items.count()):
                progress.setValue(i)
                if (progress.wasCanceled()):
                    break
                item = self.graphicsView.scene.findPath(self.items.item(i).text())
                if item == None: continue
                match = False
                if self.matchByList(item, filterDialog.listArea): 
                    for n in range(len(item.polygon)):           
                        if self.matchByList(item, filterDialog.listArea, n):                    
                            match = True
                            break
                if match:
                    self.items.item(i).setCheckState(Qt.Checked)
                    item.setVisible(True)
                else:         
                    self.items.item(i).setCheckState(Qt.Unchecked)
                    item.setVisible(False)                    
            progress.setValue(self.items.count())
        self.completeProgress.emit(self.GUI_NORMAL)
        
    def variablesClicked(self):
        try:        
            dlg = VariableDialog(self)
            dlg.exec_() 
        except Exception as e: 
            print(e)
            traceback.print_exc()      
            
