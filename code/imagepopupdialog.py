from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, sys
from Ui_imagepopup import Ui_Dialog
class ImagePopupDialog(QDialog, Ui_Dialog):
    """
    The ImagePopup class shows an image in QLabel 
    """
    def __init__(self, imagename, parent=None):
        QDialog.__init__(self, parent)
        Ui_Dialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
#        imagename  = 'd:/Projects/Visual Attention/Video Annotation/data/IMG_0194.JPG'
#        print imagename
        thumb = QPixmap(imagename)
        self.label.setPixmap(thumb.scaled(800, 600,  Qt.KeepAspectRatio))
