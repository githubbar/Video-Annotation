# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\choicesdialog.ui'
#
# Created: Tue Jan 07 11:35:25 2014
#      by: PyQt5 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ChoicesDialog(object):
    def setupUi(self, ChoicesDialog):
        ChoicesDialog.setObjectName(_fromUtf8("ChoicesDialog"))
        ChoicesDialog.resize(400, 300)
        self.gridLayout_2 = QtGui.QGridLayout(ChoicesDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.choices = QtGui.QListWidget(ChoicesDialog)
        self.choices.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.choices.setObjectName(_fromUtf8("choices"))
        self.gridLayout_2.addWidget(self.choices, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.addChoice = QtGui.QPushButton(ChoicesDialog)
        self.addChoice.setText(_fromUtf8(""))
        self.addChoice.setIconSize(QtCore.QSize(32, 32))
        self.addChoice.setObjectName(_fromUtf8("addChoice"))
        self.gridLayout.addWidget(self.addChoice, 0, 0, 1, 1)
        self.removeChoice = QtGui.QPushButton(ChoicesDialog)
        self.removeChoice.setText(_fromUtf8(""))
        self.removeChoice.setIconSize(QtCore.QSize(32, 32))
        self.removeChoice.setObjectName(_fromUtf8("removeChoice"))
        self.gridLayout.addWidget(self.removeChoice, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChoicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.buttonLoad = QtGui.QPushButton(ChoicesDialog)
        self.buttonLoad.setObjectName(_fromUtf8("buttonLoad"))
        self.gridLayout_2.addWidget(self.buttonLoad, 2, 1, 1, 1)

        self.retranslateUi(ChoicesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChoicesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChoicesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChoicesDialog)

    def retranslateUi(self, ChoicesDialog):
        ChoicesDialog.setWindowTitle(QtGui.QApplication.translate("ChoicesDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.choices.setSortingEnabled(False)
        self.buttonLoad.setText(QtGui.QApplication.translate("ChoicesDialog", "Add From File", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ChoicesDialog = QtGui.QDialog()
    ui = Ui_ChoicesDialog()
    ui.setupUi(ChoicesDialog)
    ChoicesDialog.show()
    sys.exit(app.exec_())

