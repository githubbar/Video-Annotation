# Project Dialog wrapper
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Ui_project import Ui_projectDialog
from variabledialog import *

class ProjectDialog(QDialog, Ui_projectDialog):
    def __init__(self, parent=None):
        self.nodeColor = Qt.red
        QDialog.__init__(self, parent)
        Ui_projectDialog.__init__(self)
        self.setupUi(self)
        self.backgroundFileButton.clicked.connect(self.backgroundFileButtonClicked)
        self.colorButton.clicked.connect(self.colorButtonClicked)
        self.variablesButton.clicked.connect(self.variablesClicked)
        
    def backgroundFileButtonClicked(self):
        filename = QFileDialog.getOpenFileName(self, "Choose Background Image File", os.path.dirname(str(self.parent().graphicsView.scene.filename)))
        if not filename:
            return        
        relname = os.path.relpath(str(filename),  os.path.dirname(str(self.parent().graphicsView.scene.filename)))
        self.backgroundFileEdit.setText(relname)

    def colorButtonClicked(self):
        self.nodeColor = QColorDialog.getColor(self.nodeColor,self)
        self.colorButton.setStyleSheet("background-color: "+self.nodeColor.name())
        
        
    def variablesClicked(self):
        dlg = VariableDialog(self.parent())      
        dlg.exec_() 
