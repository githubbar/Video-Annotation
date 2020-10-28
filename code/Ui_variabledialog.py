# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'variabledialog.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_VariablesDialog(object):
    def setupUi(self, VariablesDialog):
        VariablesDialog.setObjectName(("VariablesDialog"))
        VariablesDialog.resize(784, 664)
        self.gridLayout = QtWidgets.QGridLayout(VariablesDialog)
        self.gridLayout.setObjectName(("gridLayout"))
        self.addVariable = QtWidgets.QPushButton(VariablesDialog)
        self.addVariable.setText((""))
        self.addVariable.setIconSize(QtCore.QSize(32, 32))
        self.addVariable.setObjectName(("addVariable"))
        self.gridLayout.addWidget(self.addVariable, 3, 0, 1, 1)
        self.buttonCancel = QtWidgets.QPushButton(VariablesDialog)
        self.buttonCancel.setObjectName(("buttonCancel"))
        self.gridLayout.addWidget(self.buttonCancel, 3, 7, 1, 1)
        self.buttonOk = QtWidgets.QPushButton(VariablesDialog)
        self.buttonOk.setObjectName(("buttonOk"))
        self.gridLayout.addWidget(self.buttonOk, 3, 6, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 5, 1, 1)
        self.table = VariableWidget(VariablesDialog)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setColumnCount(8)
        self.table.setObjectName(("table"))
        self.table.setRowCount(0)
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setSortIndicatorShown(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.table, 0, 0, 1, 9)
        self.removeVariable = QtWidgets.QPushButton(VariablesDialog)
        self.removeVariable.setText((""))
        self.removeVariable.setIconSize(QtCore.QSize(32, 32))
        self.removeVariable.setObjectName(("removeVariable"))
        self.gridLayout.addWidget(self.removeVariable, 3, 1, 1, 1)
        self.exportButton = QtWidgets.QPushButton(VariablesDialog)
        self.exportButton.setObjectName(("exportButton"))
        self.gridLayout.addWidget(self.exportButton, 3, 4, 1, 1)
        self.importButton = QtWidgets.QPushButton(VariablesDialog)
        self.importButton.setObjectName(("importButton"))
        self.gridLayout.addWidget(self.importButton, 3, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)

        self.retranslateUi(VariablesDialog)
        QtCore.QMetaObject.connectSlotsByName(VariablesDialog)

    def retranslateUi(self, VariablesDialog):
        VariablesDialog.setWindowTitle(_translate("VariablesDialog", "Project Variables", None))
        self.buttonCancel.setText(_translate("VariablesDialog", "Cancel", None))
        self.buttonOk.setText(_translate("VariablesDialog", "Ok", None))
        self.table.setSortingEnabled(True)
        self.exportButton.setText(_translate("VariablesDialog", "Export To File", None))
        self.importButton.setText(_translate("VariablesDialog", "Add From File", None))

from variablewidget import VariableWidget
