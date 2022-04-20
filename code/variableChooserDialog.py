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