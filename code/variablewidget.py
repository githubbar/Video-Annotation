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
from PyQt5.QtCore import QVariant, Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QDialog

from choicesdialog import ChoicesDialog
from delegates import CustomDelegate
from settings import EditorTypeRole, UserDataRole, variableTypes


class VariableWidget(QTableWidget):
    deleteKeyPressed = pyqtSignal()      
     
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.setItemDelegate(CustomDelegate())
        self.itemChanged.connect(self.onItemChanged)
        
    def addVariable(self):
        self.setSortingEnabled(False)
        row = self.rowCount()
        self.insertRow(row)
        newItem = QTableWidgetItem('unknown')
        self.setItem(row,  0,  newItem)
        self.setItem(row,  1,  QTableWidgetItem('String'))        
        self.setItem(row,  2,  QTableWidgetItem('String'))        
        self.setItem(row,  3,  QTableWidgetItem(''))
        self.setItem(row,  4,  QTableWidgetItem(''))
        self.setItem(row,  5,  QTableWidgetItem(''))
        self.setItem(row,  6,  QTableWidgetItem(''))
        self.setItem(row,  7,  QTableWidgetItem(''))
        self.setSortingEnabled(True)
        self.setFocus()
        self.setCurrentCell(row, 0)
        self.updateDelegates()
    
    def onItemChanged(self, it):
        # TODO: add renaming variables without erasing them! Need to define a custom delegate
#         if it.column() == 1: 
#             scene = self.parent().parent().graphicsView.scene        
#             scene.renameVariable('', it.data())
        # turn last column into button for dropdowns
        if it.column() == 1 and self.item(it.row(), 7) and it.data(Qt.DisplayRole) in ['DropDown', 'MultiChoice']:
            self.item(it.row(), 7).setData(EditorTypeRole, 'Button')
            
    def removeVariable(self):
        if not self.selectedRanges(): return
        self.setSortingEnabled(False)
        rowNumbers = []
        for r in self.selectedRanges():
            rowNumbers.extend(list(range(r.topRow(), r.bottomRow()+1))) 
        rowNumbers.sort()
        rowNumbers.reverse()
        for n in rowNumbers:        
            self.removeRow(n)
        self.setSortingEnabled(True)

    def displayChoices(self, choices):
        dlg = ChoicesDialog(choices, self.parent())      
        if dlg.exec_() == QDialog.Accepted:
            choices = []
            for i in range(dlg.choices.count()):
                choices.append(dlg.choices.item(i).text())
            return choices
        else:
            return choices
            

    def updateDelegates(self):
        # Set Choices for dropdowns
        for i in range(self.rowCount()):
            self.item(i, 0).setData(EditorTypeRole,  'String')
            self.item(i, 1).setData(EditorTypeRole,  'String')
            self.item(i, 2).setData(EditorTypeRole,  'DropDown')
            self.item(i, 3).setData(EditorTypeRole,  'Yes/No')
            self.item(i, 4).setData(EditorTypeRole,  'String')
            self.item(i, 5).setData(EditorTypeRole,  'Yes/No')
            self.item(i, 6).setData(EditorTypeRole,  'String')
            self.item(i, 7).setData(EditorTypeRole,  'Button')
            # self.item(i, 2).setData(UserDataRole, '')
            self.item(i, 2).setData(UserDataRole, variableTypes)            
            if self.item(i, 2).data(Qt.DisplayRole) in ['DropDown', 'MultiChoice']:
                self.item(i, 7).setData(UserDataRole, ['...', self.displayChoices])
#            if isReadOnly:
#                for j in range(self.columnCount()):
#                    f = self.item(i, j).font()
#                    f.setBold(True)
#                    self.item(i, j).setFont(f)
#                    self.item(i, j).setData(EditorReadOnlyRole,  True)          
