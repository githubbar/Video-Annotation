from PyQt5.QtWidgets import QDialog, QFileDialog, QListWidgetItem
from Ui_choicesdialog import Ui_ChoicesDialog
# from track import *

class ChoicesDialog(QDialog, Ui_ChoicesDialog):
    def __init__(self, choices=None, parent=None):
        
        QDialog.__init__(self, parent)
        Ui_ChoicesDialog.__init__(self)
        self.setupUi(self)
        self.addChoice.setIcon(QIcon('icons/plus.png'))
        self.removeChoice.setIcon(QIcon('icons/minus.png'))
        self.addChoice.clicked.connect(self.onAddChoice)
        self.removeChoice.clicked.connect(self.onRemoveChoice)
        self.buttonLoad.clicked.connect(self.loadChoicesFromFile)
        for choice in choices:
            item = QListWidgetItem(choice)
            item.setFlags(item.flags () | Qt.ItemIsEditable)        
            self.choices.addItem(item)
        
    def onAddChoice(self):
        item = QListWidgetItem('')
        item.setFlags(item.flags () | Qt.ItemIsEditable)        
        self.choices.addItem(item)
        
    def onRemoveChoice(self):
        for i in self.choices.selectedItems():
            self.choices.takeItem(self.choices.row(i))

        
    def loadChoicesFromFile(self):
        filename = QFileDialog.getOpenFileName(self, "Choose Comma Separated Choices File", os.getcwdu())
        if not filename:
            return        
        
        import csv
        reader = csv.reader(open(filename, 'rb'))
        for row in reader:
            for choice in row:
                item = QListWidgetItem(choice)
                item.setFlags(item.flags () | Qt.ItemIsEditable)        
                self.choices.addItem(item)
                
