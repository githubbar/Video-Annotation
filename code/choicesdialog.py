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
from PyQt5.QtWidgets import QDialog, QFileDialog, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from PyQt5.QtCore import Qt
import os
from fileio import findFataFile

class ChoicesDialog(QDialog):
    def __init__(self, choices=None, parent=None):
        self.parent = parent         
        super(ChoicesDialog, self).__init__()
        uic.loadUi(findFataFile('choicesdialog.ui'), self)
        self.addChoice.setIcon(QIcon('icons/plus.png'))
        self.removeChoice.setIcon(QIcon('icons/minus.png'))
        self.addChoice.clicked.connect(self.onAddChoice)
        self.removeChoice.clicked.connect(self.onRemoveChoice)
        self.buttonLoad.clicked.connect(self.loadChoicesFromFile)
        for choice in choices:
            item = QListWidgetItem(choice)
            item.setFlags(item.flags () | Qt.ItemIsEditable)        
            self.choices.addItem(item)
        self.show()
            
        
    def onAddChoice(self):
        item = QListWidgetItem('')
        item.setFlags(item.flags () | Qt.ItemIsEditable)        
        self.choices.addItem(item)
        
    def onRemoveChoice(self):
        for i in self.choices.selectedItems():
            self.choices.takeItem(self.choices.row(i))

        
    def loadChoicesFromFile(self):
        filename, _filter = QFileDialog.getOpenFileName(self, "Choose Comma Separated Choices File", os.getcwd())
        if not filename:
            return        
        
        import csv
        reader = csv.reader(open(filename))
        for row in reader:
            for choice in row:
                item = QListWidgetItem(choice)
                item.setFlags(item.flags () | Qt.ItemIsEditable)        
                self.choices.addItem(item)
                
