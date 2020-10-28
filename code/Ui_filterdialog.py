# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\filterdialog.ui'
#
# Created: Mon Jan 26 13:36:56 2015
#      by: PyQt5 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_FilterDialog(object):
    def setupUi(self, FilterDialog):
        FilterDialog.setObjectName(("FilterDialog"))
        FilterDialog.resize(429, 562)
        self.gridLayout = QtWidgets.QGridLayout(FilterDialog)
        self.gridLayout.setObjectName(("gridLayout"))
        self.listScrollArea = QtWidgets.QScrollArea(FilterDialog)
        self.listScrollArea.setWidgetResizable(True)
        self.listScrollArea.setObjectName(("listScrollArea"))
        self.listAreaContents = QtWidgets.QWidget()
        self.listAreaContents.setGeometry(QtCore.QRect(0, 0, 287, 495))
        self.listAreaContents.setObjectName(("listAreaContents"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.listAreaContents)
        self.verticalLayout_3.setObjectName(("verticalLayout_3"))
        self.listArea = QtWidgets.QToolBox(self.listAreaContents)
        self.listArea.setStyleSheet(("border: 0px 0px 100px 0px; "))
        self.listArea.setObjectName(("listArea"))
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 269, 450))
        self.page.setObjectName(("page"))
        self.listArea.addItem(self.page, (""))
        self.verticalLayout_3.addWidget(self.listArea)
        self.listScrollArea.setWidget(self.listAreaContents)
        self.gridLayout.addWidget(self.listScrollArea, 0, 0, 1, 1)
        self.checkboxScrollArea = QtWidgets.QScrollArea(FilterDialog)
        self.checkboxScrollArea.setWidgetResizable(True)
        self.checkboxScrollArea.setObjectName(("checkboxScrollArea"))
        self.checkboxAreaContents = QtWidgets.QWidget()
        self.checkboxAreaContents.setGeometry(QtCore.QRect(0, 0, 114, 495))
        self.checkboxAreaContents.setObjectName(("checkboxAreaContents"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.checkboxAreaContents)
        self.verticalLayout_4.setObjectName(("verticalLayout_4"))
        self.checkboxArea = QtWidgets.QVBoxLayout()
        self.checkboxArea.setObjectName(("checkboxArea"))
        self.verticalLayout_4.addLayout(self.checkboxArea)
        self.checkboxScrollArea.setWidget(self.checkboxAreaContents)
        self.gridLayout.addWidget(self.checkboxScrollArea, 0, 1, 1, 1)
        self.widget = QtWidgets.QWidget(FilterDialog)
        self.widget.setObjectName(("widget"))
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(("horizontalLayout_4"))
        self.buttonOk = QtWidgets.QPushButton(self.widget)
        self.buttonOk.setObjectName(("buttonOk"))
        self.horizontalLayout_4.addWidget(self.buttonOk)
        self.buttonCancel = QtWidgets.QPushButton(self.widget)
        self.buttonCancel.setObjectName(("buttonCancel"))
        self.horizontalLayout_4.addWidget(self.buttonCancel)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 2)

        self.retranslateUi(FilterDialog)
        QtCore.QMetaObject.connectSlotsByName(FilterDialog)

    def retranslateUi(self, FilterDialog):
        FilterDialog.setWindowTitle(_translate("FilterDialog", "Dialog", None))
        self.buttonOk.setText(_translate("FilterDialog", "Ok", None))
        self.buttonCancel.setText(_translate("FilterDialog", "Cancel", None))

