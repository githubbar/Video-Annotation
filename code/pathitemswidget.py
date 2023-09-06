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
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem 
from PyQt5.QtCore import QItemSelectionModel
import logging, os

class PathItemsWidget(QListWidget):
    deleteKeyPressed = pyqtSignal()      
    idChangedSignal =  pyqtSignal('QString')
    
    def __init__(self, parent):
        logging.debug('Loading...')
        QListWidget.__init__(self, parent)
        self.setSortingEnabled(True)
        # self.currentTextChanged.connect(self.onCurrentTextChanged)
        logging.debug('Done loading...')
    def keyPressEvent(self, event):
        print(f'PathItemsWidget::keyPressEvent ')
        
        if event.key() == Qt.Key_Delete:
            self.deleteKeyPressed.emit()   
    
    def dataChanged(self, topLeft, bottomRight, roles=list()):
        print (f'PathItemsWidget::dataChanged ')
        QListWidget.dataChanged(self,  topLeft,  bottomRight, roles=list())
        # self.idChangedSignal.emit(item.text())

    def onChangeCurrentItem(self, id):        
        print(f'PathItemsWidget::onChangeCurrentItem id={id}')
        matches = self.findItems(id, Qt.MatchExactly)
        if len(matches) > 0:
            self.setCurrentItem(matches[0], QItemSelectionModel.ClearAndSelect)
                
    def onAddItem(self, id):
        # print(f'PathItemsWidget::onAddItem id={id}')        
        item = QListWidgetItem(id)
        item.setCheckState(Qt.Unchecked)
        # item.setFlags(Qt.ItemIsEditable | item.flags())
        self.addItem(item)
    
    def onRemoveItem(self, id):
        print(f'PathItemsWidget::onRemoveItem id={id}')
        matches = self.findItems(id, Qt.MatchExactly)
        if len(matches) > 0:
            self.takeItem(self.row(matches[0]))

    def onUpdateItem(self, newid):
        print(f'PathItemsWidget::onUpdateItem id={id}, newid={newid}')
        self.currentItem().setText(newid)
        # self.setCurrentItem(matches[0])

    # def onCurrentTextChanged(self, text):
    #     print(f'PathItemsWidget::onCurrentTextChanged text={text}')
        