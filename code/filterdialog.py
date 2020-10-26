from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Ui_filterdialog import Ui_FilterDialog
from variablewidget import *
from track import *
from settings import *



class FilterDialog(QDialog, Ui_FilterDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        Ui_FilterDialog.__init__(self)
        self.setupUi(self)
        self.buttonOk.clicked.connect(self.onOkClicked)
        self.buttonCancel.clicked.connect(self.onCancelClicked)
        
    def onCancelClicked(self):
        self.reject()
        
    def onOkClicked(self):
        self.accept()
