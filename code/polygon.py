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
""" Path Item"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv

from settings import *
from propertywidget import *
from delegates import *

class Polygon(QGraphicsPolygonItem):
    id, description, tags = '', '', ''
    
    shownFields = ['id', 'description', 'tags', 'font']
    checkableFields  = []
    browsableFields = ['fileName']
    colorFields = ['fontColor', 'color']
    dropdownFields = []     
    R = 1.0 # node radius 
    penR = 1.0 # edge width
    indP = None # current node index
    
    def __init__(self, point=None, font=QFont('White Rabbit',  2),  opacity=1.0):    
        QGraphicsPolygonItem.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setBrush(QColor(Qt.green))
        self.setPen(QPen(QBrush(Qt.green), self.penR))
        self.setCursor(Qt.ArrowCursor)
        self.setOpacity(opacity)
        self.font = font
        if point: self.addPoint(point)                                         

    def clone(self):    
        other = Polygon(None,  self.font,  self.opacity())
        other.indP = self.indP
        other.id, other.description, other.tags = self.id, self.description, self.tags
        other.setPolygon(self.polygon())        
        return other

    def write(self, s):
        s << self.polygon()
        s.writeQVariant(self.id)        
        s.writeQVariant(self.description)
        s.writeQVariant(self.tags)
        s.writeFloat(self.opacity())
        s << self.font
        
    def read(self, s, buildNumber):
        p = QPolygonF()
        s >> p
        self.setPolygon(p)
        self.id = s.readQVariant()
        self.description = s.readQVariant()
        self.tags = s.readQVariant()
        opacity = s.readFloat()
        self.setOpacity(opacity)
        s >> self.font       
        self.update()        
       
    def boundingRect(self):
        r = super(Polygon,  self).boundingRect()
        return r.adjusted(-self.R,  -self.R,  self.R,  self.R)
        
    def paint(self, painter, option, widget):
        QGraphicsPolygonItem.paint(self, painter, option, widget)
        painter.setPen(QColor("black"))
        painter.setFont(self.font)
        painter.drawText(self.boundingRect(), Qt.AlignHCenter | Qt.AlignVCenter,  self.id)        
        painter.setBrush(QBrush(Qt.transparent))
        painter.setPen(QColor("red"))
        for i in range(self.polygon().count()):
            painter.drawEllipse(self.polygon().at(i), self.R, self.R) 
            
    def updatePoint(self, i, p):
        if i == None:
            return            
        poly = self.polygon()
        poly.replace(i,  self.snapToGrid(p))
        self.setPolygon(poly)
    
    def update(self, rect=QRectF() ):        
        QGraphicsPolygonItem.update(self, rect)
        self.setToolTip(self.description)

    def deletePoint(self, i):
        poly = self.polygon()
        poly.remove(i)
        self.setPolygon(poly)
      
        # move to the previous item
        if i !=0 and self.indP == i:
            self.indP -= 1
    
        if not self.polygon().count():        
            self.scene().currentPolygon = None
            self.scene().removeItem(self)
        
    def addPoint(self, p):
        self.tags = ''
        self.description = ''
        poly = self.polygon()
        poly.append(p)
        self.setPolygon(poly)
        self.indP = self.polygon().count()-1

    def insertPoint(self, i, p):
        if len(self.polygon()) < 2: 
            return
        self.tags = ''
        self.description = ''
        poly = self.polygon()
        poly.insert(i+1, p)
        self.indP = i+1    
        self.setPolygon(poly)

    def focusInEvent (self, event):
        QGraphicsItem.focusInEvent (self, event)
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsItem.focusOutEvent (self, event)
        if self.polygon().count():
            self.scene().saveSignal.emit(self)

    def mousePressEvent(self, event):
        self.scene().loadSignal.emit(self)
        self.scene().currentPolygon = self
        self.setSelected(True)        
        if self.scene().mode == 'Polygon' or self.scene().mode == 'Edit':   
            QGraphicsPolygonItem.mousePressEvent(self, event)
            if (event.modifiers() & Qt.ControlModifier):
                # add new point between two closest points
                i = self.getNearestLineSegment(event.pos())
                self.insertPoint(i, event.pos())
            else:
                # get new point closest to mouse and load it
                self.indP = self.getNearestPoint(event.pos())
                if (event.pos()-self.polygon().at(self.indP)).manhattanLength() >self.scene().gridD:
                    self.indP = None            
            self.updatePoint(self.indP, event.pos())
           

    def mouseMoveEvent(self, event):
        if self.scene().mode == 'Polygon' or self.scene().mode == 'Edit':           
            self.updatePoint(self.indP, event.pos())
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deletePoint(self.indP)

    def getNearestPoint(self, p):
        mini=0
        mind = sys.maxint
        for i in range(self.polygon().count()):
            dist = (self.polygon().at(i)-p).manhattanLength()
            if  dist < mind:
                mind = dist
                mini = i
        return mini

    def getNearestLineSegment(self, p):
        if self.polygon().count() < 2:
            return 0
        i1 = 0
        d1 = sys.maxint
        for i in range(self.polygon().count()-1):
            l = QLineF(self.polygon().at(i), self.polygon().at(i+1))
            n = l.normalVector()
            n.translate(p-n.p2())
            ip = QPointF() 
            res = l.intersect(n, ip)
            n = QLineF(ip, p)
            res = l.intersect(n, ip)
            if res == QLineF.UnboundedIntersection:
                dist = min([(p-l.p1()).manhattanLength(), (p-l.p2()).manhattanLength()])
            elif res == QLineF.BoundedIntersection:
                dist = (p-ip).manhattanLength()
            else:
                continue
            if dist < d1:
                d1 = dist
                i1 = i
        return i1

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
    
