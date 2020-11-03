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
        relname = os.path.relpath(filename[0],  os.path.dirname(str(self.parent.graphicsView.scene.filename)))
        self.backgroundFileEdit.setText(relname)

    def colorButtonClicked(self):
        self.nodeColor = QColorDialog.getColor(self.nodeColor,self)
        self.colorButton.setStyleSheet("background-color: "+self.nodeColor.name())
        
        
    def variablesClicked(self):
        dlg = VariableDialog(self.parent)      
        dlg.exec_() 
