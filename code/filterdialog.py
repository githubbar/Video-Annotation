from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from fileio import findFataFile

class FilterDialog(QDialog):
    def __init__(self, parent):
        super(FilterDialog, self).__init__()
        uic.loadUi(findFataFile('filterdialog.ui'), self)
        self.setupUi(self)
        self.buttonOk.clicked.connect(self.onOkClicked)
        self.buttonCancel.clicked.connect(self.onCancelClicked)
        self.show()
        
    def onCancelClicked(self):
        self.reject()
        
    def onOkClicked(self):
        self.accept()
