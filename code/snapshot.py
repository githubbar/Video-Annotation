# -*- coding: utf-8 -*-
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
""" Graphics Items """

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv

from settings import *
from propertywidget import *
from delegates import *
from imagepopupdialog import *

class Snapshot(QGraphicsRectItem):
    shownFields = ['id', 'imagename', 'description', 'tags', 'font']
    checkableFields  = []
    colorFields = []
    dropdownFields = []     
    id, imagename, description, tags = '', '', '', ''
    D = 10.0
    penR = 1.0 # edge width    
    resizing = False
    
    def __init__(self, scenepos=QPointF(),font=QFont('Verdana',  2),  opacity=1.0):    
        QGraphicsRectItem .__init__(self)
        self.setRect(0, 0, self.D, self.D)
        self.pixmap = QPixmap('icons/Snapshot2.png')
        self.setPos(scenepos)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setOpacity(opacity)
        self.font = font
        self.setCursor(Qt.ArrowCursor)

    def clone(self):    
        other = Snapshot(self.pos(), self.pixmap, self.font, self.opacity())
        other.id, other.description, other.tags = self.id, self.description, self.tags
        return other
        
    def write(self, s):
        s << self.pos() 
        s.writeQVariant(self.id)
        s.writeQVariant(self.imagename)
        s.writeQVariant(self.description)
        s.writeQVariant(self.tags)
        s.writeFloat(self.opacity())
        s << self.font
        
    def read(self, s, buildNumber):
        p = QPointF()
        s >> p 
        self.setPos(p)
        self.id = s.readQVariant()
        self.imagename = s.readQVariant();
        self.description= s.readQVariant()
        self.tags = s.readQVariant()
        opacity = s.readFloat()
        self.setOpacity(opacity)
        s >> self.font       
        self.update()
        
        
    def paint(self, painter, option, widget):
        target = QRect(0, 0, self.D, self.D)
        painter.drawPixmap(target, self.pixmap);

    def focusInEvent (self, event):
        QGraphicsRectItem.focusInEvent (self, event)
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsRectItem.focusOutEvent (self, event)
        self.scene().saveSignal.emit(self)
        
    def mouseDoubleClickEvent (self, event):
        QGraphicsRectItem.mouseDoubleClickEvent (self, event)
        imagename = os.path.join(os.path.dirname(str(self.scene().filename)), str(self.imagename))
        p = ImagePopupDialog(imagename)
        p.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.scene().removeItem(self)
            
    def snapToGrid(self, p):
        dx = p.x() % self.scene().gridD
        dy = p.y() % self.scene().gridD
        if dx > self.scene().gridD-dx: dx = - (self.scene().gridD-dx)
        if dy > self.scene().gridD-dy: dy = - (self.scene().gridD-dy)
        return QPointF(p.x() - dx, p.y() - dy)        

    def limitToScene(self):
        r = self.scene().sceneRect()
        p = self.pos()
        self.setPos(min(r.right()-self.rect().width(), max(p.x(), r.left())), min(r.bottom()-self.rect().height(), max(p.y(), r.top())))
    
