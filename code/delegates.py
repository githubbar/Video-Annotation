# -*- coding: utf-8 -*-
""" Delegates """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import sys

from settings import *
from choicesdialog import *
from types import *

class CustomDelegate(QStyledItemDelegate):
    def __init__(self, parent = None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        elementType = index.data(EditorTypeRole)
        if elementType == 'NotEditable':
            return None
        elif elementType == 'String':
            return QLineEdit(parent)
        elif elementType == 'UniqueString':            
            qApp.installEventFilter(self)              
            editor = QLineEdit(parent)
            editor.setValidator(UniqueLineEditValidator(index, parent))         
            return editor
        elif elementType == 'Yes/No':
            return None
        elif elementType == 'DropDown':
            qApp.installEventFilter(self)              
            editor = DropDownEditor(parent)
            editor.setEditable(True)
            editor.setInsertPolicy(QComboBox.NoInsert)        
            editor.setAutoCompletion(True)
            editor.setDuplicatesEnabled(False)
            choices = index.data(UserDataRole)
            editor.addItems(choices)
            editor.setCurrentIndex(editor.findText(index.data(Qt.DisplayRole)))
            editor.installEventFilter(self)      
            completer = DropDownCompleter(editor)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            completer.setModel(editor.model())
            editor.setCompleter(completer) 
            return editor
        elif elementType == 'MultiChoice':
            qApp.installEventFilter(self)              
            editor = MultiChoiceEditor(parent)
            editor.setInsertPolicy(QComboBox.NoInsert)        
            editor.setDuplicatesEnabled(False)
            choices = index.data(UserDataRole)
            editor.addItems(choices,  index.data(Qt.EditRole).split(', '))
            editor.installEventFilter(self)      
            return editor            
        elif elementType == 'Double':
            if not StrToBoolOrKeep(index.data(EditorReadOnlyRole)):
                qApp.installEventFilter(self)              
                editor = QLineEdit(parent)
                editor.setValidator(QDoubleValidator(-1e10, 1e10, 2, parent))         
                return editor
            return None
        elif elementType == 'Integer':
            if not StrToBoolOrKeep(index.data(EditorReadOnlyRole)):
                qApp.installEventFilter(self)              
                editor = QLineEdit(parent)
                editor.setValidator(QIntValidator(-sys.maxint, sys.maxint, parent))         
                return editor
            return None
        elif elementType == 'Button':
            return None
        elif elementType == 'File':
            filter = index.data(UserDataRole)
            projectpath = index.data(UserDataRole+1)
            editor = FileOpen(projectpath,  filter, parent)
            editor.installEventFilter(self)            
            return editor
        elif elementType == 'Font':
            (f,  ok) = QFontDialog.getFont(index.data(Qt.EditRole),  None)
            if ok:
                index.model().setData(index,  QVariant(f))
            return None
        elif elementType == 'Time':            
            editor = QTimeEdit(index.model().data(index, Qt.EditRole), parent)
            editor.setDisplayFormat("hh:mm:ss.zzz")
            return editor

    def displayText(self, value, locale):       
        if type(value) == QVariant.Time or type(value) == QVariant.DateTime:
            return value.toString('hh:mm:ss.zzz')
        elif type(value) == QVariant.Invalid:
            return 'None'
        else:
            return QStyledItemDelegate.displayText(self, value, locale)
            
    def setEditorData(self, editor, index):
        elementType = index.data(EditorTypeRole)
        if elementType == 'NotEditable':
            pass
        elif elementType == 'Yes/No':
            pass
#            value = StrToBoolOrKeep(index.model().data(index, Qt.DisplayRole))
#            if value:
#                editor.setCheckState(Qt.Checked)
#            else:
#                editor.setCheckState(Qt.Unchecked)
        elif elementType == 'DropDown':
            value = index.model().data(index, Qt.EditRole)
            editor.setCurrentIndex(editor.findText(value))
        else:
            QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        elementType = index.data(EditorTypeRole)
        if elementType == 'NotEditable':
            pass
        elif elementType == 'Yes/No':
            pass
        elif elementType == 'DropDown':            
            model.setData( index, editor.currentText() )            
        elif elementType == 'MultiChoice':            
            model.setData( index, editor.currentText())    
        else:
            QStyledItemDelegate.setModelData(self, editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        elementType = index.data(EditorTypeRole)
        if option.state & QStyle.State_Selected:
            if option.state & QStyle.State_Active:
                painter.fillRect(option.rect, option.palette.highlight())               
            else:
                painter.fillRect(option.rect, option.palette.window())               

        if elementType == 'NotEditable':
            QStyledItemDelegate.paint(self, painter, option, index)
        if elementType == 'File':        
            if (option.state & QStyle.State_MouseOver):
                painter.fillRect(option.rect, Qt.green);
            QStyledItemDelegate.paint(self, painter, option, index)
        elif elementType == 'Yes/No':
            checked = StrToBoolOrKeep(index.model().data(index, Qt.DisplayRole))    
            check_box_style_option  = QStyleOptionButton()
            check_box_style_option.state |= QStyle.State_Enabled
            if (checked):
                check_box_style_option.state |= QStyle.State_On
            else:
                check_box_style_option.state |= QStyle.State_Off
            check_box_style_option.rect = self.getCheckBoxRect(option)
            check_box_style_option.showDecorationSelected = True
            QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)            
        elif elementType=='Button':
            userData = index.data(UserDataRole)
            if not userData: return
#             FIXME: userData doesn't unpack but does for [1,2] list'
            text, methodToRun = userData
            button  = QStyleOptionButton()
            button.text = text
            button.state = QStyle.State_Active | QStyle.State_Enabled
            button_point = QPoint (option.rect.x() + option.rect.width() / 2 - button.rect.width() / 2, option.rect.y() +option.rect.height() / 2 - button.rect.height() / 2)            
            button.rect = QRect(button_point, button.rect.size())
            QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)
        elif elementType == 'Font':
            painter.save()
            if (option.state & QStyle.State_MouseOver):
                painter.fillRect(option.rect, Qt.green);
            painter.setPen(QPen(Qt.black))
            v= index.data(Qt.EditRole)
            if v.isValid():
                text = v.family() + ' : ' + str(v.pointSize())
                painter.drawText(option.rect, Qt.AlignLeft, text)
            painter.restore()
        else:
            QStyledItemDelegate.paint(self, painter, option, index)
        
    def editorEvent(self, event, model, option, index):
        elementType = index.data(EditorTypeRole)
        if elementType == 'Yes/No':
            if not StrToBoolOrKeep(index.data(EditorReadOnlyRole)):
                # Do not change the checkbox-state
                if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseMove:
                    return False
                if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
                    if event.button() != Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                        return False
                    if event.type() == QEvent.MouseButtonDblClick:
                        return True
                elif event.type() == QEvent.KeyPress:
                    if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                        return False
                    else:
                        return False
                # Change the checkbox-state
                checked = StrToBoolOrKeep(index.data())
                return model.setData(index, not checked, Qt.EditRole)
        elif elementType=='Button':    
            userData = index.data(UserDataRole)
            if userData: 
                text, methodToRun = userData
                if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
                    if event.button() == Qt.LeftButton and methodToRun != None:
                            result = methodToRun(model.data(index, Qt.DisplayRole))
                            model.setData(index, result, Qt.DisplayRole)      
            return QStyledItemDelegate.editorEvent(self, event, model, option, index)
        return QStyledItemDelegate.editorEvent(self, event, model, option, index)
            
    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint (option.rect.x() +
                            option.rect.width() / 2 -
                            check_box_rect.width() / 2,
                            option.rect.y() +
                            option.rect.height() / 2 -
                            check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())
        
class FileOpen(QLineEdit):
    def __init__(self, relativeToDir = None,  filter = 'All Files (*.*)',  parent = None):
        QLineEdit.__init__(self, parent)
        self.filter = filter
        self.relativeToDir = relativeToDir
        self.button = QToolButton(self)
        self.button.setIcon(QIcon('icons/folder-open.png'))            
        self.button.setIconSize(QSize(16, 16))
        self.button.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        sz = self.button.sizeHint()        
        self.setStyleSheet("QLineEdit { padding-right: %1px; }".arg(sz.width() + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), sz.height() + frameWidth * 2 + 2), max(msz.height(), sz.height() + frameWidth * 2 + 2))
        self.button.clicked.connect(self.openFileName)

    def resizeEvent(self, event):
        sz = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - sz.width(), (self.rect().bottom() + 1 - sz.height())/2)
        
    def openFileName(self):
        fName = QFileDialog.getOpenFileName(self.parent(), 'Open File',  self.relativeToDir, self.filter)
        if self.relativeToDir and fName:
            fName = os.path.relpath(str(fName), str(self.relativeToDir))
        if fName: self.setText(fName.encode("utf-8"))

class UniqueLineEditValidator(QValidator):
    def __init__(self, index,  parent=None):
        QCompleter.__init__(self, parent)
        self.index = index
         
    def validate(self,  input,  pos):
        if input == '':
            return (QValidator.Intermediate, pos)
        matches = 0
        model = self.index.model()
        for i in range(model.rowCount()):
            if input == model.data(model.index(i, self.index.column()),  Qt.EditRole) and i != self.index.row():
                matches += 1
        if matches > 0:
            self.parent().setStyleSheet("QLineEdit{background: red;}");
            return (QValidator.Intermediate, pos)
        else:
            self.parent().setStyleSheet("QLineEdit{background: white;}");
            return (QValidator.Acceptable, pos)
        
class DropDownCompleter(QCompleter):
    def __init__(self, parent=None):
        QCompleter.__init__(self, parent)
        self.local_completion_prefix = ''
        self.source_model = None

    def setModel(self, model):
        self.source_model = model
        QCompleter.setModel(self, self.source_model)

    def updateModel(self):
        local_completion_prefix = self.local_completion_prefix
        class InnerProxyModel(QSortFilterProxyModel):
            def filterAcceptsRow(self, sourceRow, sourceParent):
                index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
                return local_completion_prefix.toLower() in self.sourceModel().data(index0).toLower()
        proxy_model = InnerProxyModel()
        proxy_model.setSourceModel(self.source_model)
        QCompleter.setModel(self, proxy_model)

    def splitPath(self, path):
        self.local_completion_prefix = path
        self.updateModel()
        return ''
        
class DropDownEditor(QComboBox):
    def __init__(self, parent = None):
        QComboBox.__init__(self, parent)
 
    def focusInEvent (self, event):
        QComboBox.focusInEvent (self, event)
        qApp.installEventFilter(self)        
    
    def focusOutEvent (self, event):
        QComboBox.focusOutEvent (self, event)
        qApp.removeEventFilter(self)        

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Shortcut or event.type() == QEvent.ShortcutOverride) \
        and event.key:
            event.accept()
            return True
        else: 
            return QComboBox.eventFilter(self,  object, event)

class MultiChoiceEditor(QComboBox):
    str = ''
    def __init__(self, parent = None):
        QComboBox.__init__(self, parent)
#        self.setModel(MultiChoiceModel())
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.setInsertPolicy(QComboBox.NoInsert)     
        self.view().setSelectionMode(QAbstractItemView.MultiSelection)
 
    def currentText(self):
        text = ''            
        for row in range(self.model().rowCount()):
            if self.model().item(row).checkState() == Qt.Checked:
                text += self.model().item(row).text() + ', '
        return text[:-2]
            
    def addItems(self, choices, selections):
        for row in reversed(range(self.model().rowCount())):
            self.model().removeRow(row)
        for choice in choices:
            item = QStandardItem(choice)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if choice in selections:
                item.setData(Qt.Checked, Qt.CheckStateRole)
            else:
                item.setData(Qt.Unchecked, Qt.CheckStateRole)
            self.model().appendRow(item)

           
    def focusInEvent (self, event):
        QComboBox.focusInEvent (self, event)
        qApp.installEventFilter(self)        
    
    def focusOutEvent (self, event):
        QComboBox.focusOutEvent (self, event)
        qApp.removeEventFilter(self)        

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Shortcut or event.type() == QEvent.ShortcutOverride) \
        and event.key:
            event.accept()
            return True
        else: 
            return QComboBox.eventFilter(self,  object, event)

       
class ColorPickDelegate(QStyledItemDelegate):
    def __init__(self, parent = None,  color = "#ffffff"):
        QStyledItemDelegate.__init__(self, parent)
        self.color = color

    def createEditor(self, parent, option, index):
        editor = ColorPick(self.color, parent)
        editor.installEventFilter(self)            
        return editor
            
    def setEditorData(self, editor, index):
        QStyledItemDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        QStyledItemDelegate.setModelData(self, editor, model, index)
        if self.parent():
            self.parent().save()
        else:
            session.commit()

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        if (option.state & QStyle.State_MouseOver):
            painter.fillRect(option.rect, Qt.green)
        QStyledItemDelegate.paint(self, painter, option, index)

class ColorPick(QLineEdit):
    def __init__(self, color, parent = None):
        QLineEdit.__init__(self, parent)
        self.button = QToolButton(self)
        self.button.setIcon(QIcon('resources/icons/color-picker.ico'))            
        self.button.setIconSize(QSize(16, 16))
        self.button.setStyleSheet("QToolButton { border: none; padding: 0px; }")
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        sz = self.button.sizeHint()        
        self.setStyleSheet(QString("QLineEdit { padding-right: %1px; }").arg(sz.width() + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), sz.height() + frameWidth * 2 + 2), max(msz.height(), sz.height() + frameWidth * 2 + 2))
        self.connect(self.button, SIGNAL("clicked()"), self.openColor)

    def resizeEvent(self, event):
        sz = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - sz.width(), (self.rect().bottom() + 1 - sz.height())/2)
        
    def openColor(self):
        color = QColorDialog.getColor(QColor(self.color), self)            
        if color: 
            self.setText(color.name())

            
class URLDelegate(QStyledItemDelegate):
    def __init__(self, parent = None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = QCheckBox( parent )
        editor.installEventFilter(self)       
        return editor

    def editorEvent(self,  event,  model,  option,  index):
        if (option.state & QStyle.State_MouseOver):
            self.setCursor(Qt.PointingHandCursor)  
        return QStyledItemDelegate.editorEvent(self,  event,  model,  option,  index)
            
    def paint(self, painter, option, index):
        if (option.state & QStyle.State_MouseOver):
            option.font.setUnderline(True)
        QStyledItemDelegate.paint(self, painter, option, index)
        
#class FontOpen(QLineEdit):
#    def readFont(self):
#        return self._font
#
#    def writeFont(self, val):
#        self._font = val
#
#    font = pyqtProperty(QVariant,  readFont,  writeFont,  None,  None,  None,  True,  True,  True,  True)  
#    
#    def __init__(self, parent = None,  f = QVariant()):
#        QLineEdit.__init__(self, parent)
#        self._font = f
#        self.setAutoFillBackground(True)
#        self.button = QToolButton(self)
#        self.button.setIcon(QIcon('icons/font.png'))            
#        self.setText(f.family() + ' : ' + str(f.pointSize()))            
#        self.button.setIconSize(QSize(16, 16))
#        self.button.setStyleSheet("QToolButton { border: none; padding: 0px;}")
#        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
#        sz = self.button.sizeHint()        
#        self.setStyleSheet(QString("QLineEdit { padding-right: %1px; }").arg(sz.width() + frameWidth + 1))
#        msz = self.minimumSizeHint()
#        self.setMinimumSize(max(msz.width(), sz.height() + frameWidth * 2 + 2), max(msz.height(), sz.height() + frameWidth * 2 + 2))
#
#        self.setProperty('font', f)        
#
#    def mousePressEvent(self, event):
#        self.openFont()
# 
#    def resizeEvent(self, event):
#        sz = self.button.sizeHint()
#        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
#        self.button.move(self.rect().right() - frameWidth - sz.width(), (self.rect().bottom() + 1 - sz.height())/2)
#        
#    def openFont(self):
#        (f,  ok) = QFontDialog.getFont(self._font,  self)
#        if ok:
#            self._font = QVariant(f)
#            self.editingFinished.emit()
