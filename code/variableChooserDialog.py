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
from PyQt5 import uic

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt5.Qt import *

from fileio import findFataFile

class VariableChooserDialog(QDialog):
    def __init__(self, variables):
        import operator        
        super(VariableChooserDialog, self).__init__()
        uic.loadUi(findFataFile('variableChooserDialog.ui'), self)
        self.buttonOk.clicked.connect(self.onOkClicked)
        self.buttonCancel.clicked.connect(self.onCancelClicked)
        self.checkAll.clicked.connect(self.toggleAllItems)
                
        sortedList = sorted(variables.keys(), key=operator.itemgetter(0))
        box = QVBoxLayout(self.listArea)
          
        for name in sortedList:
            b = QPushButton(name)
            b.setCheckable(True)
            box.addWidget(b)
    
    def toggleAllItems(self):
        for item in self.listArea.findChildren(QPushButton):
            item.setChecked(self.checkAll.isChecked())
    
    def onCancelClicked(self):
        self.reject()
        
    def onOkClicked(self):
        self.accept()      