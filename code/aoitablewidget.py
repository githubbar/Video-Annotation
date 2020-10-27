from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

                  
class AOITableWidget(QTableWidget):
    deleteKeyPressed = pyqtSignal()      
    
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.itemChanged.connect(self.onItemChanged)
        self.setSortingEnabled(True)     
        self.horizontalHeader().setStretchLastSection(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteKeyPressed.emit()   

    def onItemChanged(self, item):
        if item.column()==0:
            item.g.id = QVariant(item.text())

       
    def addItem(self, item):
        entry = AOITableItem(item.id.toString(), item)
        entry.setCheckState(Qt.Checked)                     
        nRow = self.rowCount()
        self.insertRow(nRow)
        self.setItem(nRow, 0, entry)      
        self.setItem(nRow, 1, QTableWidgetItem('0'))
        self.setItem(nRow, 2, QTableWidgetItem('0'))
        self.setItem(nRow, 3, QTableWidgetItem('0'))
#        self.sortItems(0)  
    
    def removeItem(self, item):
        for n in range(self.rowCount()):
            if self.item(n, 0).g == item:
                self.removeRow(n)
                return

    def updateItem(self, item):
        for n in range(self.rowCount()):
            if self.item(n, 0).g == item:
                self.item(n, 0).setText(item.id.toString())
#                self.setItem(n, 0, PathTableItem(item.id.toString(), item))


    def getAllItems(self):
        lst = []
        for n in range(self.rowCount()):
            lst.append(self.item(n, 0))
        return lst


class AOITableItem(QTableWidgetItem):
    def __init__(self, text,  g):
        QTableWidgetItem.__init__(self,  text)
        self.g = g
#        self.setFlags(Qt.ItemIsSelectable or Qt.ItemIsUserCheckable or Qt.ItemIsEnabled)

