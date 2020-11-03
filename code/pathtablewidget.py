from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class PathTableWidget(QTableWidget):
    deleteKeyPressed = pyqtSignal()      
    
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.itemChanged.connect(self.onItemChanged)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteKeyPressed.emit()   

    def onItemChanged(self, item):
        item.g.id = item.text()

       
    def addItem(self, item):
        entry = PathTableItem(item.id, item)
#         entry.setCheckState(Qt.Checked)
        entry.setCheckState(Qt.Unchecked)                     
        nRow = self.rowCount()
        self.insertRow(nRow)
        self.setItem(nRow, 0, entry)      
        self.sortItems(0)  
    
    def removeItem(self, item):
        for n in range(self.rowCount()):
            if self.item(n, 0).g == item:
                self.removeRow(n)
                return

    def updateItem(self, item):
        for n in range(self.rowCount()):
            if self.item(n, 0).g == item:
                self.item(n, 0).setText(item.id)
#                self.setItem(n, 0, PathTableItem(item.id, item))

class PathTableItem(QTableWidgetItem):
    def __init__(self, text,  g):
        QTableWidgetItem.__init__(self,  text)
        self.g = g
#        self.setFlags(Qt.ItemIsSelectable or Qt.ItemIsUserCheckable or Qt.ItemIsEnabled)

