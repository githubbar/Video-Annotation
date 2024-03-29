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

class Rectangle(QGraphicsRectItem):
    shownFields = ['id', 'description', 'tags', 'font']
    checkableFields  = []
    colorFields = ['fontColor', 'color']
    dropdownFields = []     
    id, description, tags = '', '', ''
    D = 10.0
    penR = 1.0 # edge width    
    resizing = False
    
    def __init__(self, scenepos=QPointF(), font=QFont('Verdana',  2),  opacity=1.0):    
        QGraphicsRectItem .__init__(self)
        self.setRect(0.0, 0.0, 1.0,  1.0)
        self.setPos(scenepos)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setBrush(QColor(Qt.green))
        self.setPen(QPen(QBrush(Qt.green), self.penR))
        self.setOpacity(opacity)
        self.font = font
        self.setCursor(Qt.ArrowCursor)

    def clone(self):    
        other = Rectangle(self.pos(), self.font, self.opacity())
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
        QGraphicsRectItem.paint(self, painter, option, widget)
        painter.setPen(QColor("black"))
        painter.setFont(self.font)
        if self.rect().width() > self.rect().height():
            angle = 0
        else:
            angle = 90
        self.drawRotatedText(painter, self.rect(), Qt.AlignHCenter | Qt.AlignVCenter, self.id, angle)
         
    def drawRotatedText(self, painter, rect, flags, text, angle):
        painter.save()
        painter.translate(rect.center().x(),  rect.center().y())
        painter.rotate(angle)            
        if angle > 45:
            w = rect.width()
            h = rect.height()
            rect.setWidth(h)
            rect.setHeight(w)
        rect.moveCenter(QPointF(0, 0))
        painter.drawText(rect, flags, text)
        painter.restore()

    def focusInEvent (self, event):
        QGraphicsRectItem.focusInEvent (self, event)
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsRectItem.focusOutEvent (self, event)
        self.scene().saveSignal.emit(self)
        
    def updatePoint(self, p):
        r = self.rect()
        r.setBottomRight(self.snapToGrid(p))
        self.setRect(r)

    def update(self,  rect=QRectF() ):
        QGraphicsRectItem.update(self, rect)
        self.setToolTip(self.description)

    def mousePressEvent(self, event):
#        print 'mouse press over rectangle ' + self.id
        self.scene().loadSignal.emit(self)
        if self.scene().mode == 'Rectangle' or self.scene().mode == 'Edit':
            QGraphicsRectItem.mousePressEvent(self, event)        
            dist = (event.pos()-self.rect().bottomRight()).manhattanLength()
            if dist < (self.rect().center()-self.rect().bottomRight()).manhattanLength() or dist < self.D:
                self.resizing = True
                self.setPos(self.snapToGrid(self.pos()))
                self.updatePoint(event.pos())
            else: 
                self.resizing = False
        
    def mouseMoveEvent(self, event):
        if self.scene().mode == 'Rectangle' or self.scene().mode == 'Edit':        
            if self.resizing:
                self.updatePoint(event.pos())
            else:
                QGraphicsRectItem.mouseMoveEvent(self, event)
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
    
