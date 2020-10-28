# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\choicesdialog.ui'
#
# Created: Tue Jan 07 11:35:25 2014
#      by: PyQt5 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtWidgets

class Ui_ChoicesDialog(object):
    def setupUi(self, ChoicesDialog):
        ChoicesDialog.setObjectName(("ChoicesDialog"))
        ChoicesDialog.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(ChoicesDialog)
        self.gridLayout_2.setObjectName(("gridLayout_2"))
        self.choices = QtWidgets.QListWidget(ChoicesDialog)
        self.choices.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.choices.setObjectName(("choices"))
        self.gridLayout_2.addWidget(self.choices, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName(("gridLayout"))
        self.addChoice = QtWidgets.QPushButton(ChoicesDialog)
        self.addChoice.setText((""))
        self.addChoice.setIconSize(QtCore.QSize(32, 32))
        self.addChoice.setObjectName(("addChoice"))
        self.gridLayout.addWidget(self.addChoice, 0, 0, 1, 1)
        self.removeChoice = QtWidgets.QPushButton(ChoicesDialog)
        self.removeChoice.setText((""))
        self.removeChoice.setIconSize(QtCore.QSize(32, 32))
        self.removeChoice.setObjectName(("removeChoice"))
        self.gridLayout.addWidget(self.removeChoice, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(ChoicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.buttonLoad = QtWidgets.QPushButton(ChoicesDialog)
        self.buttonLoad.setObjectName(("buttonLoad"))
        self.gridLayout_2.addWidget(self.buttonLoad, 2, 1, 1, 1)

        self.retranslateUi(ChoicesDialog)
        self.buttonBox.accepted.connect(ChoicesDialog.accept)
        self.buttonBox.rejected.connect(ChoicesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChoicesDialog)

    def retranslateUi(self, ChoicesDialog):
        ChoicesDialog.setWindowTitle(QtWidgets.QApplication.translate("ChoicesDialog", "Dialog", None, QtWidgets.QApplication.UnicodeUTF8))
        self.choices.setSortingEnabled(False)
        self.buttonLoad.setText(QtWidgets.QApplication.translate("ChoicesDialog", "Add From File", None, QtWidgets.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChoicesDialog = QtWidgets.QDialog()
    ui = Ui_ChoicesDialog()
    ui.setupUi(ChoicesDialog)
    ChoicesDialog.show()
    sys.exit(app.exec_())

