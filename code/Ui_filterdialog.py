# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\filterdialog.ui'
#
# Created: Mon Jan 26 13:36:56 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName(_fromUtf8("FilterDialog"))
        FilterDialog.resize(429, 562)
        self.gridLayout = QtGui.QGridLayout(FilterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listScrollArea = QtGui.QScrollArea(FilterDialog)
        self.listScrollArea.setWidgetResizable(True)
        self.listScrollArea.setObjectName(_fromUtf8("listScrollArea"))
        self.listAreaContents = QtGui.QWidget()
        self.listAreaContents.setGeometry(QtCore.QRect(0, 0, 287, 495))
        self.listAreaContents.setObjectName(_fromUtf8("listAreaContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.listAreaContents)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.listArea = QtGui.QToolBox(self.listAreaContents)
        self.listArea.setStyleSheet(_fromUtf8("border: 0px 0px 100px 0px; "))
        self.listArea.setObjectName(_fromUtf8("listArea"))
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 269, 450))
        self.page.setObjectName(_fromUtf8("page"))
        self.listArea.addItem(self.page, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.listArea)
        self.listScrollArea.setWidget(self.listAreaContents)
        self.gridLayout.addWidget(self.listScrollArea, 0, 0, 1, 1)
        self.checkboxScrollArea = QtGui.QScrollArea(FilterDialog)
        self.checkboxScrollArea.setWidgetResizable(True)
        self.checkboxScrollArea.setObjectName(_fromUtf8("checkboxScrollArea"))
        self.checkboxAreaContents = QtGui.QWidget()
        self.checkboxAreaContents.setGeometry(QtCore.QRect(0, 0, 114, 495))
        self.checkboxAreaContents.setObjectName(_fromUtf8("checkboxAreaContents"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.checkboxAreaContents)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.checkboxArea = QtGui.QVBoxLayout()
        self.checkboxArea.setObjectName(_fromUtf8("checkboxArea"))
        self.verticalLayout_4.addLayout(self.checkboxArea)
        self.checkboxScrollArea.setWidget(self.checkboxAreaContents)
        self.gridLayout.addWidget(self.checkboxScrollArea, 0, 1, 1, 1)
        self.widget = QtGui.QWidget(FilterDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.buttonOk = QtGui.QPushButton(self.widget)
        self.buttonOk.setObjectName(_fromUtf8("buttonOk"))
        self.horizontalLayout_4.addWidget(self.buttonOk)
        self.buttonCancel = QtGui.QPushButton(self.widget)
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.horizontalLayout_4.addWidget(self.buttonCancel)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 2)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Dialog", None))
        self.buttonOk.setText(_translate("FilterDialog", "Ok", None))
        self.buttonCancel.setText(_translate("FilterDialog", "Cancel", None))

