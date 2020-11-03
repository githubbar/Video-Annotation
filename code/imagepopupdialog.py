from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from fileio import findFataFile

class ImagePopupDialog(QDialog):
    """
    The ImagePopup class shows an image in QLabel 
    """
    def __init__(self, imagename, parent=None):
        super(ImagePopupDialog, self).__init__()
        uic.loadUi(findFataFile('imagedialog.ui'), self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
#        imagename  = 'd:/Projects/Visual Attention/Video Annotation/data/IMG_0194.JPG'
#        print imagename
        thumb = QPixmap(imagename)
        self.label.setPixmap(thumb.scaled(800, 600,  Qt.KeepAspectRatio))
        self.show()
