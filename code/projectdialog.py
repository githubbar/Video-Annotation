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
from PyQt5.QtWidgets import QDialog, QFileDialog, QColorDialog
from PyQt5.QtCore import Qt
from variabledialog import VariableDialog
from fileio import findFataFile



class ProjectDialog(QDialog):
    def __init__(self, parent):
        self.parent = parent
        super(ProjectDialog, self).__init__()
        uic.loadUi(findFataFile('project.ui'), self)
        self.nodeColor = Qt.red
        self.backgroundFileButton.clicked.connect(self.backgroundFileButtonClicked)
        self.colorButton.clicked.connect(self.colorButtonClicked)
        self.variablesButton.clicked.connect(self.variablesClicked)
        self.show()
        
    def backgroundFileButtonClicked(self):
        filename, _filter = QFileDialog.getOpenFileName(self, "Choose Background Image File", os.path.dirname(str(self.parent.graphicsView.scene.filename)))
        if not filename:
            return        
        relname = os.path.relpath(filename,  os.path.dirname(str(self.parent.graphicsView.scene.filename)))
        self.backgroundFileEdit.setText(relname)

    def colorButtonClicked(self):
        self.nodeColor = QColorDialog.getColor(self.nodeColor,self)
        self.colorButton.setStyleSheet("background-color: "+self.nodeColor.name())
        
        
    def variablesClicked(self):
        dlg = VariableDialog(self.parent)      
        dlg.exec_() 
