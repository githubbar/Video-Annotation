# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Projects\Video Annotation\Video Annotation Tool\project.ui'
#
# Created: Tue Jan 27 12:17:34 2015
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

class Ui_projectDialog(object):
    def setupUi(self, projectDialog):
        projectDialog.setObjectName(("projectDialog"))
        projectDialog.resize(400, 794)
#         self..setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.variablesButton = QtWidgets.QPushButton(projectDialog)
        self.variablesButton.setGeometry(QtCore.QRect(150, 630, 75, 23))
        self.variablesButton.setObjectName(("variablesButton"))
        
        self.groupBox = QtWidgets.QGroupBox(projectDialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 361, 101))
        self.groupBox.setObjectName(("groupBox"))
        
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(("gridLayout"))
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName(("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.spinnerW = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spinnerW.setMinimum(1.0)
        self.spinnerW.setMaximum(1000.0)
        self.spinnerW.setObjectName(("spinnerW"))
        self.gridLayout.addWidget(self.spinnerW, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName(("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinnerH = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.spinnerH.setMinimum(1.0)
        self.spinnerH.setMaximum(1000.0)
        self.spinnerH.setObjectName(("spinnerH"))
        self.gridLayout.addWidget(self.spinnerH, 1, 1, 1, 1)
        self.backgroundFileGroupBox = QtWidgets.QGroupBox(projectDialog)
        self.backgroundFileGroupBox.setGeometry(QtCore.QRect(20, 160, 361, 101))
        self.backgroundFileGroupBox.setObjectName(("backgroundFileGroupBox"))
        self.backgroundFileEdit = QtWidgets.QLineEdit(self.backgroundFileGroupBox)
        self.backgroundFileEdit.setGeometry(QtCore.QRect(20, 40, 200, 25))
        self.backgroundFileEdit.setObjectName(("backgroundFileEdit"))
        self.backgroundFileButton = QtWidgets.QPushButton(self.backgroundFileGroupBox)
        self.backgroundFileButton.setGeometry(QtCore.QRect(250, 40, 41, 23))
        self.backgroundFileButton.setObjectName(("backgroundFileButton"))
        
        self.nodeSizeGroupBox = QtWidgets.QGroupBox(projectDialog)
        self.nodeSizeGroupBox.setGeometry(QtCore.QRect(20, 280, 361, 280))
        self.nodeSizeGroupBox.setObjectName(("nodeSizeGroupBox"))
        
        self.pathSmoothingSlider = QtWidgets.QSlider(self.nodeSizeGroupBox)
        self.pathSmoothingSlider.setGeometry(QtCore.QRect(20, 40, 321, 19))
        self.pathSmoothingSlider.setMaximum(100)
        self.pathSmoothingSlider.setProperty("value", 1)
        self.pathSmoothingSlider.setOrientation(QtCore.Qt.Horizontal)
        self.pathSmoothingSlider.setObjectName(("pathSmoothingSlider"))
        self.label_Smooth = QtWidgets.QLabel(self.nodeSizeGroupBox)
        self.label_Smooth.setGeometry(QtCore.QRect(20, 60, 321, 21))
        self.label_Smooth.setObjectName(("label_Smooth"))
            
        self.nodeSizeSlider = QtWidgets.QSlider(self.nodeSizeGroupBox)
        self.nodeSizeSlider.setGeometry(QtCore.QRect(20, 90, 321, 19))
        self.nodeSizeSlider.setMaximum(100)
        self.nodeSizeSlider.setProperty("value", 1)
        self.nodeSizeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.nodeSizeSlider.setObjectName(("nodeSizeSlider"))
        self.label_Size = QtWidgets.QLabel(self.nodeSizeGroupBox)
        self.label_Size.setGeometry(QtCore.QRect(20, 110, 321, 21))
        self.label_Size.setObjectName(("label_Size"))
                
        self.showSegments = QtWidgets.QCheckBox(self.nodeSizeGroupBox)
        self.showSegments.setGeometry(QtCore.QRect(20, 140, 200, 25))
        self.showSegments.setChecked(True)
        self.showSegments.setObjectName(("showSegments"))
        self.showOnlyCurrent = QtWidgets.QCheckBox(self.nodeSizeGroupBox)
        self.showOnlyCurrent.setGeometry(QtCore.QRect(20, 170, 200, 25))
        self.showOnlyCurrent.setObjectName(("showOnlyCurrent"))
        self.showOrientation = QtWidgets.QCheckBox(self.nodeSizeGroupBox)
        self.showOrientation.setGeometry(QtCore.QRect(20, 200, 200, 25))
        self.showOrientation.setChecked(True)
        self.showOrientation.setObjectName(("showOrientation"))
        self.label_3 = QtWidgets.QLabel(self.nodeSizeGroupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 230, 110, 25))
        self.label_3.setObjectName(("label_3"))
        self.colorButton = QtWidgets.QPushButton(self.nodeSizeGroupBox)
        self.colorButton.setGeometry(QtCore.QRect(120, 230, 80, 25))
        self.colorButton.setText((""))
        self.colorButton.setObjectName(("colorButton"))
        

        self.buttonBox = QtWidgets.QDialogButtonBox(projectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 690, 321, 61))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(("buttonBox"))
        self.retranslateUi(projectDialog)
        self.buttonBox.accepted.connect(projectDialog.accept)
        self.buttonBox.rejected.connect(projectDialog.reject)        
        QtCore.QMetaObject.connectSlotsByName(projectDialog)

    def retranslateUi(self, projectDialog):
        projectDialog.setWindowTitle(_translate("projectDialog", "Project Properties", None))
        self.groupBox.setTitle(_translate("projectDialog", "Floor Size", None))
        self.label.setText(_translate("projectDialog", "Width", None))
        self.spinnerW.setSuffix(_translate("projectDialog", " ft", None))
        self.label_2.setText(_translate("projectDialog", "Height", None))
        self.spinnerH.setSuffix(_translate("projectDialog", " ft", None))
        self.backgroundFileGroupBox.setTitle(_translate("projectDialog", "Background Image File", None))
        self.backgroundFileButton.setText(_translate("projectDialog", "...", None))
        self.variablesButton.setText(_translate("projectDialog", "Variables", None))
        self.nodeSizeGroupBox.setTitle(_translate("projectDialog", "Path", None))
        self.showSegments.setText(_translate("projectDialog", "Show Path Segments", None))
        self.showOnlyCurrent.setText(_translate("projectDialog", "Show Only Current Node", None))
        self.showOrientation.setText(_translate("projectDialog", "Show Orientation", None))
        self.label_3.setText(_translate("projectDialog", "Node Color: ", None))
        self.label_Smooth.setText(_translate("projectDialog", "Curve Smoothing", None))
        self.label_Size.setText(_translate("projectDialog", "Node Size", None))

