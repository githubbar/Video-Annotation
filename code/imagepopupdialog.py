"""
====================================================================================
Video Annotation Tool
Copyright (C) 2023 Alex Leykin @ Customer Interface Lab
Email: cil@indiana.edu
http://cil.iu.edu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
            
====================================================================================
"""
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
