# -*- coding: utf-8 -*-
""" Graphics Items """

from PyQt4.QtGui import *
from PyQt4.QtCore import *
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
    id, imagename, description, tags = QVariant(''), QVariant(''), QVariant(''), QVariant('')
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
        self.font = QVariant(font)
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
        imagename = os.path.join(os.path.dirname(str(self.scene().filename)), str(self.imagename.toString()))
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
    