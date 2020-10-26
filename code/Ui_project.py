# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\project.ui'
#
# Created: Tue Jan 27 12:17:34 2015
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

class Ui_projectDialog(object):
    def setupUi(self, projectDialog):
        projectDialog.setObjectName(_fromUtf8("projectDialog"))
        projectDialog.resize(418, 594)
        self.buttonBox = QtGui.QDialogButtonBox(projectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 490, 291, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.groupBox = QtGui.QGroupBox(projectDialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 201, 81))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinnerW = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinnerW.setMinimum(1.0)
        self.spinnerW.setMaximum(1000.0)
        self.spinnerW.setObjectName(_fromUtf8("spinnerW"))
        self.gridLayout.addWidget(self.spinnerW, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinnerH = QtGui.QDoubleSpinBox(self.groupBox)
        self.spinnerH.setMinimum(1.0)
        self.spinnerH.setMaximum(1000.0)
        self.spinnerH.setObjectName(_fromUtf8("spinnerH"))
        self.gridLayout.addWidget(self.spinnerH, 1, 1, 1, 1)
        self.backgroundFileGroupBox = QtGui.QGroupBox(projectDialog)
        self.backgroundFileGroupBox.setGeometry(QtCore.QRect(20, 160, 361, 51))
        self.backgroundFileGroupBox.setObjectName(_fromUtf8("backgroundFileGroupBox"))
        self.backgroundFileEdit = QtGui.QLineEdit(self.backgroundFileGroupBox)
        self.backgroundFileEdit.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.backgroundFileEdit.setObjectName(_fromUtf8("backgroundFileEdit"))
        self.backgroundFileButton = QtGui.QPushButton(self.backgroundFileGroupBox)
        self.backgroundFileButton.setGeometry(QtCore.QRect(310, 20, 41, 23))
        self.backgroundFileButton.setObjectName(_fromUtf8("backgroundFileButton"))
        self.pathSmoothingGroupBox = QtGui.QGroupBox(projectDialog)
        self.pathSmoothingGroupBox.setGeometry(QtCore.QRect(20, 230, 361, 51))
        self.pathSmoothingGroupBox.setObjectName(_fromUtf8("pathSmoothingGroupBox"))
        self.pathSmoothingSlider = QtGui.QSlider(self.pathSmoothingGroupBox)
        self.pathSmoothingSlider.setGeometry(QtCore.QRect(10, 20, 341, 19))
        self.pathSmoothingSlider.setMaximum(100)
        self.pathSmoothingSlider.setProperty("value", 1)
        self.pathSmoothingSlider.setOrientation(QtCore.Qt.Horizontal)
        self.pathSmoothingSlider.setObjectName(_fromUtf8("pathSmoothingSlider"))
        self.variablesButton = QtGui.QPushButton(projectDialog)
        self.variablesButton.setGeometry(QtCore.QRect(270, 60, 75, 23))
        self.variablesButton.setObjectName(_fromUtf8("variablesButton"))
        self.nodeSizeGroupBox = QtGui.QGroupBox(projectDialog)
        self.nodeSizeGroupBox.setGeometry(QtCore.QRect(20, 300, 361, 51))
        self.nodeSizeGroupBox.setObjectName(_fromUtf8("nodeSizeGroupBox"))
        self.nodeSizeSlider = QtGui.QSlider(self.nodeSizeGroupBox)
        self.nodeSizeSlider.setGeometry(QtCore.QRect(10, 20, 341, 19))
        self.nodeSizeSlider.setMaximum(100)
        self.nodeSizeSlider.setProperty("value", 1)
        self.nodeSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.nodeSizeSlider.setObjectName(_fromUtf8("nodeSizeSlider"))
        self.showSegments = QtGui.QCheckBox(projectDialog)
        self.showSegments.setGeometry(QtCore.QRect(20, 380, 131, 17))
        self.showSegments.setChecked(True)
        self.showSegments.setObjectName(_fromUtf8("showSegments"))
        self.showOnlyCurrent = QtGui.QCheckBox(projectDialog)
        self.showOnlyCurrent.setGeometry(QtCore.QRect(20, 440, 141, 17))
        self.showOnlyCurrent.setObjectName(_fromUtf8("showOnlyCurrent"))
        self.showOrientation = QtGui.QCheckBox(projectDialog)
        self.showOrientation.setGeometry(QtCore.QRect(20, 410, 131, 17))
        self.showOrientation.setChecked(True)
        self.showOrientation.setObjectName(_fromUtf8("showOrientation"))
        self.colorButton = QtGui.QPushButton(projectDialog)
        self.colorButton.setGeometry(QtCore.QRect(280, 380, 31, 23))
        self.colorButton.setText(_fromUtf8(""))
        self.colorButton.setObjectName(_fromUtf8("colorButton"))
        self.label_3 = QtGui.QLabel(projectDialog)
        self.label_3.setGeometry(QtCore.QRect(220, 380, 61, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(projectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), projectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), projectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(projectDialog)

    def retranslateUi(self, projectDialog):
        projectDialog.setWindowTitle(_translate("projectDialog", "Project Properties", None))
        self.groupBox.setTitle(_translate("projectDialog", "Size", None))
        self.label.setText(_translate("projectDialog", "Width", None))
        self.spinnerW.setSuffix(_translate("projectDialog", " ft", None))
        self.label_2.setText(_translate("projectDialog", "Height", None))
        self.spinnerH.setSuffix(_translate("projectDialog", " ft", None))
        self.backgroundFileGroupBox.setTitle(_translate("projectDialog", "Background Image File", None))
        self.backgroundFileButton.setText(_translate("projectDialog", "...", None))
        self.pathSmoothingGroupBox.setTitle(_translate("projectDialog", "Path Smoothing Factor", None))
        self.variablesButton.setText(_translate("projectDialog", "Variables", None))
        self.nodeSizeGroupBox.setTitle(_translate("projectDialog", "Node Size", None))
        self.showSegments.setText(_translate("projectDialog", "Show Path Segments", None))
        self.showOnlyCurrent.setText(_translate("projectDialog", "Show Only Current Node", None))
        self.showOrientation.setText(_translate("projectDialog", "Show Orientation", None))
        self.label_3.setText(_translate("projectDialog", "Node Color", None))

