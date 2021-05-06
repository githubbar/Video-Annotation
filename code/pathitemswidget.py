from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem 
from PyQt5.QtCore import QItemSelectionModel


class PathItemsWidget(QListWidget):
    deleteKeyPressed = pyqtSignal()      
    idChangedSignal =  pyqtSignal('QString')
    
    def __init__(self, parent):
        QListWidget.__init__(self, parent)
        self.setSortingEnabled(True)
        # self.currentTextChanged.connect(self.onCurrentTextChanged)
    def keyPressEvent(self, event):
        print(f'PathItemsWidget::keyPressEvent ')
        
        if event.key() == Qt.Key_Delete:
            self.deleteKeyPressed.emit()   
    
    def dataChanged(self, topLeft, bottomRight, roles=list()):
        print (f'PathItemsWidget::dataChanged ')
        QListWidget.dataChanged(self,  topLeft,  bottomRight, roles=list())
        # self.idChangedSignal.emit(item.text())

    def onChangeCurrentItem(self, id):        
        print(f'PathItemsWidget::onChangeCurrentItem id={id}')
        matches = self.findItems(id, Qt.MatchExactly)
        if len(matches) > 0:
            self.setCurrentItem(matches[0], QItemSelectionModel.ClearAndSelect)
                
    def onAddItem(self, id):
        print(f'PathItemsWidget::onAddItem id={id}')        
        item = QListWidgetItem(id)
        item.setCheckState(Qt.Unchecked)
        # item.setFlags(Qt.ItemIsEditable | item.flags())
        self.addItem(item)
    
    def onRemoveItem(self, id):
        print(f'PathItemsWidget::onRemoveItem id={id}')
        matches = self.findItems(id, Qt.MatchExactly)
        if len(matches) > 0:
            self.takeItem(self.row(matches[0]))

    def onUpdateItem(self, newid):
        print(f'PathItemsWidget::onUpdateItem id={id}, newid={newid}')
        self.currentItem().setText(newid)
        # self.setCurrentItem(matches[0])

    # def onCurrentTextChanged(self, text):
    #     print(f'PathItemsWidget::onCurrentTextChanged text={text}')
        