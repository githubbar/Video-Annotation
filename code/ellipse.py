# -*- coding: utf-8 -*-
""" Graphics Items """

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv

from settings import *
from propertywidget import *
from delegates import *

class Ellipse(QGraphicsEllipseItem):
    shownFields = ['id', 'description', 'tags', 'font']
    checkableFields  = []
    browsableFields = ['fileName']
    colorFields = ['fontColor', 'color']
    dropdownFields = []     
    id, description, tags = '', '', ''
    D = 10.0
    penR = 1.0 # edge width    
    resizing = False
    
    def __init__(self, scenepos=QPointF(), font=QFont('White Rabbit',  2),  opacity=1.0):    
        QGraphicsEllipseItem .__init__(self)
        self.setRect(0.0, 0.0, 1, 1)
        self.setPos(scenepos)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setBrush(QColor(Qt.green))
        self.setPen(QPen(QBrush(Qt.green), self.penR))
        self.setOpacity(opacity)
        self.font = QVariant(font)
        self.setCursor(Qt.ArrowCursor)

    def clone(self):    
        other = Ellipse(self.pos(), self.font, self.opacity())
        other.setRect(self.rect())
        other.id, other.description, other.tags = self.id, self.description, self.tags
        return other
        
    def write(self, s):
        s << self.pos() << self.rect()
        s.writeQVariant(self.id)
        s.writeQVariant(self.description)
        s.writeQVariant(self.tags)
        s.writeFloat(self.opacity())
        s << self.font
        
    def read(self, s, buildNumber):
        r = QRectF()
        p = QPointF()
        s >> p >> r
        self.setPos(p)
        self.setRect(r)
        self.id = s.readQVariant()
        self.description= s.readQVariant()
        self.tags = s.readQVariant()
        opacity = s.readFloat()
        self.setOpacity(opacity)
        s >> self.font             
        self.update()
        
    def paint(self, painter, option, widget):
        QGraphicsEllipseItem.paint(self, painter, option, widget)
        painter.setPen(QColor("black"))
        painter.setFont(self.font.toPyObject())
        painter.drawText(self.rect(), Qt.AlignHCenter | Qt.AlignVCenter,  self.id)
         
    def focusInEvent (self, event):
        QGraphicsEllipseItem.focusInEvent (self, event)
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsEllipseItem.focusOutEvent (self, event)
        self.scene().saveSignal.emit(self)
        
    def updatePoint(self, p):
        r = self.rect()
        r.setBottomRight(self.snapToGrid(p))
        self.setRect(r)

    def update(self,  rect=QRectF() ):
        QGraphicsEllipseItem.update(self, rect)
        self.setToolTip(self.description)
        

    def mousePressEvent(self, event):
        self.scene().loadSignal.emit(self)
        if self.scene().mode == 'Ellipse' or self.scene().mode == 'Edit':        
            QGraphicsEllipseItem.mousePressEvent(self, event)
            dist = (event.pos()-self.rect().bottomRight()).manhattanLength()
            if (dist < (self.rect().center()-self.rect().bottomRight()).manhattanLength() or dist < self.D):
                self.resizing = True
                self.updatePoint(event.pos())
            else: 
                self.resizing = False
        
    def mouseMoveEvent(self, event):
        if self.scene().mode == 'Ellipse' or self.scene().mode == 'Edit':                
            if self.resizing:
                self.updatePoint(event.pos())
            else:
                QGraphicsEllipseItem.mouseMoveEvent(self, event)
                self.limitToScene()
                self.setPos(self.snapToGrid(self.pos()))
            self.scene().update()
            
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
    
