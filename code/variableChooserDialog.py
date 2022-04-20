from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from fileio import findFataFile

class VariableChooserDialog(QDialog):
    def __init__(self, parent):
        super(VariableChooserDialog, self).__init__()
        uic.loadUi(findFataFile('variableChooserDialog.ui'), self)
        self.buttonOk.clicked.connect(self.onOkClicked)
        self.buttonCancel.clicked.connect(self.onCancelClicked)
        self.show()
        
    def onCancelClicked(self):
        self.reject()
        
    def onOkClicked(self):
        self.accept()
