# Project Dialog wrapper
# import os
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5 import QtWidgets, uic
# from variabledialog import *
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog, QColorDialog
from variabledialog import VariableDialog
from PyQt5.QtCore import Qt


class ProjectDialog(QDialog):
    def __init__(self, parent):
        self.parent = parent
        super(ProjectDialog, self).__init__()
        uic.loadUi('project.ui', self)
        self.nodeColor = Qt.red
        self.backgroundFileButton.clicked.connect(self.backgroundFileButtonClicked)
        self.colorButton.clicked.connect(self.colorButtonClicked)
        self.variablesButton.clicked.connect(self.variablesClicked)
        self.show()
        
    def backgroundFileButtonClicked(self):
        filename = QFileDialog.getOpenFileName(self, "Choose Background Image File", os.path.dirname(str(self.parent.graphicsView.scene.filename)))
        if not filename:
            return        
        relname = os.path.relpath(filename[0],  os.path.dirname(str(self.parent.graphicsView.scene.filename)))
        self.backgroundFileEdit.setText(relname)

    def colorButtonClicked(self):
        self.nodeColor = QColorDialog.getColor(self.nodeColor,self)
        self.colorButton.setStyleSheet("background-color: "+self.nodeColor.name())
        
        
    def variablesClicked(self):
        dlg = VariableDialog(self.parent)      
        dlg.exec_() 
