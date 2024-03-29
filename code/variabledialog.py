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
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from unicodeCSV import UnicodeWriter
from track import Path
from fileio import findFataFile
from variablewidget import VariableWidget

class VariableDialog(QDialog):

    def __init__(self, parent):
        self.parent = parent         
        super(VariableDialog, self).__init__()
        uic.loadUi(findFataFile('variabledialog.ui'), self)
        self.buttonOk.clicked.connect(self.onOkClicked)
        self.buttonCancel.clicked.connect(self.onCancelClicked)
        self.importButton.clicked.connect(self.importFromFile)
        self.exportButton.clicked.connect(self.exportToFile)
        
        self.addVariable.setIcon(QIcon('icons/plus.png'))
        self.removeVariable.setIcon(QIcon('icons/minus.png'))
        self.addVariable.clicked.connect(self.table.addVariable)
        self.removeVariable.clicked.connect(self.table.removeVariable)
        self.table.setHorizontalHeaderLabels(('Name', 'Description', 'Type', 'Show?', 'Keyboard Shortcut', 'Apply to Each Node?', 'Group', 'Choices'))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.loadVariables(self.parent.graphicsView.scene.variables)
        self.show()
        
    def loadVariables(self, variables):
        self.table.clearContents()
        self.table.setSortingEnabled(False)
        for name in variables:
            row = self.table.rowCount()
            self.table.insertRow(row)
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, name)
            self.table.setItem(row, 0, item)                    
            for i, col in enumerate(variables[name]):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, col)
                self.table.setItem(row, i + 1, item)        
        self.table.setSortingEnabled(True)
        self.table.updateDelegates()
                    
    def onCancelClicked(self):
        self.reject()
        
    def onOkClicked(self):
        onename = ''
        self.table.sortItems(0)
        for i in range(self.table.rowCount()):
            name = self.table.item(i, 0).data(Qt.DisplayRole)
            if name == onename:
                QMessageBox.warning(self, 'Warning!', 'The names of the variables must be unique and not blank! Please fix the names highlighted in red.')
                return
            onename = name
        
        if QMessageBox.question(self, 'Warning!', 'Saving these changes to your project will affect all the existing data! Are you sure you want to proceed?', \
            QMessageBox.Yes | QMessageBox.No) == QMessageBox.No: 
                return
        scene = self.parent.graphicsView.scene        
        scene.variables.clear()
        
        for i in range(self.table.rowCount()):
            name = self.table.item(i, 0).data(Qt.DisplayRole)
            cols = [self.table.item(i, j).data(Qt.DisplayRole) for j in range(1, self.table.columnCount())]
            scene.variables[name] = cols
        
        # make sure all current paths are updated
        for item in list(scene.items()):
            if type(item) == Path: 
                item.populateVariables()
        if scene.currentPath:
            scene.loadSignal.emit(scene.currentPath)
        self.accept()

    def importFromFile(self):
        filename, _filter = QFileDialog.getOpenFileName(self, "Choose Comma Separated Variables File", os.getcwd(), 'CSV Files (*.csv)')
        if not filename:
            return        
        
        import csv
        reader = csv.reader(open(filename))
        self.table.setSortingEnabled(False)
        for line in reader:
            line = list(map(str.strip, line))
            if line[0] in self.parent.graphicsView.scene.variables:  # edit already existing variables
                del self.parent.graphicsView.scene.variables[line[0]]
                items = self.table.findItems(line[0], Qt.MatchExactly)
                for item in items:
                    self.table.removeRow(item.row())
            row = self.table.rowCount()
            self.table.insertRow(row)            
            for i, col in enumerate(line):
                item = QTableWidgetItem()
                item.setData(Qt.DisplayRole, col)
                self.table.setItem(row, i, item)        
            self.table.setItem(row, 7, QTableWidgetItem())
        self.table.setSortingEnabled(True)                
        self.table.updateDelegates()
                
    def exportToFile(self):
        filename, _filter = QFileDialog.getSaveFileName(self, "Choose Comma Separated Variables File", os.getcwd(), 'CSV Files (*.csv)')
        if not filename:
            return        
        
        writer = UnicodeWriter(open(filename, 'wb'))            
#        writer.writerow(['Name', 'Type', 'Show?', 'Keyboard Shortcut', 'Apply to Each Node?', 'Group', 'Choices'])
        for i in range(self.table.rowCount()):
            row = []
            for j in range(self.table.columnCount()):
                row.append(str(self.table.item(i, j).data(Qt.DisplayRole)))
            writer.writerow(row)
            
