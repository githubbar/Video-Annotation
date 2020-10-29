# -*- coding: utf-8 -*-
""" Path Item"""

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv

from settings import *
from propertywidget import *
from delegates import *


class AOI(QGraphicsPolygonItem):
    id, description, tags = '', '', ''
    shownFields = ['id', 'description', 'tags', 'font']
    checkableFields = []
    browsableFields = ['fileName']
    colorFields = ['fontColor', 'color']
    dropdownFields = []     
    R = 1.0  # node radius 
    penR = 1.0  # edge width
    indP = None  # current node index
    
    def __init__(self, point=None, font = QFont('Verdana', 2), opacity=1.0):  
        import random
        random.seed()  
        QGraphicsPolygonItem.__init__(self)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setBrush(QColor(Qt.green))
        self.setPen(QPen(QBrush(Qt.green), self.penR))
        self.setCursor(Qt.ArrowCursor)
        self.setOpacity(opacity)
#         self.font = font
        self.font = font
        self.fontColor = QColor(Qt.black)
        self.color = QColor(random.randrange(0, 255,), random.randrange(0, 255,), random.randrange(0, 255,))
        if point: self.addPoint(point)                                         

    def clone(self):    
        other = AOI(self.font, self.opacity())
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
        s << self.fontColor
        s << self.color
        
    def read(self, s, buildNumber):
        p = QPolygonF()
        s >> p
        self.setPolygon(p)
        self.id = s.readQVariant()
        self.description = s.readQVariant()
        self.tags = s.readQVariant()
        opacity = s.readFloat()
        self.setOpacity(opacity)
        if buildNumber < 47:
            self.font = s.readQVariant()
        else:
            s >> self.font
        if buildNumber >= 46:
            s >> self.fontColor
            s >> self.color

        self.update()        
       
    def boundingRect(self):
        r = super(AOI, self).boundingRect()
        return r.adjusted(-self.R, -self.R, self.R, self.R)
        
    def paint(self, painter, option, widget):
#         QGraphicsPolygonItem.paint(self, painter, option, widget)        
        borderPen = QPen(QColor('#0000FF'))
        borderPen.setWidthF(1.0)
        painter.setPen(borderPen)
        painter.setBrush(self.color)        
        painter.drawPolygon(self.polygon())
        painter.setBrush(QBrush(Qt.red))
        painter.setPen(QColor("red"))
        for i in range(self.polygon().count()):
            painter.drawEllipse(self.polygon().at(i), self.R, self.R)
         
#         painter.setFont(self.font)
        painter.setFont(QFont('Verdana', 3))
        if self.boundingRect().width() > self.boundingRect().height():
            angle = 0
        else:
            angle = 90
        self.drawRotatedText(painter, self.boundingRect(), Qt.AlignHCenter | Qt.AlignVCenter, self.id, angle)          
            
    def drawRotatedText(self, painter, rect, flags, text, angle):
        painter.save()
#         painter.setBrush(QColor(0, 0, 0, 255))      
#         painter.fillRect(rect, Qt.SolidPattern)  
        painter.setPen(self.fontColor)        
        painter.translate(rect.center().x(), rect.center().y())
        painter.rotate(angle)            
        if angle > 45:
            w = rect.width()
            h = rect.height()
            rect.setWidth(h)
            rect.setHeight(w)
        rect.moveCenter(QPointF(0, 0))
        painter.setOpacity(1.0)
        painter.drawText(rect, flags, text)
        painter.restore()            
        
    def updatePoint(self, i, p):
        if i == None:
            return            
        poly = self.polygon()
        poly.replace(i, self.snapToGrid(p))
        self.setPolygon(poly)
    
    def update(self, rect=QRectF()):        
        QGraphicsPolygonItem.update(self, rect)
        self.setToolTip(self.description)
 
    def deletePoint(self, i):
        poly = self.polygon()
        poly.remove(i)
        self.setPolygon(poly)
      
        # move to the previous item
        if i != 0 and self.indP == i:
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
        self.indP = self.polygon().count() - 1

    def insertPoint(self, i, p):
        if len(self.polygon()) < 2: 
            return
        self.tags = ''
        self.description = ''
        poly = self.polygon()
        poly.insert(i + 1, p)
        self.indP = i + 1    
        self.setPolygon(poly)

    def focusInEvent (self, event):
        QGraphicsItem.focusInEvent (self, event)
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsItem.focusOutEvent (self, event)
        if self.polygon().count():
            self.scene().saveSignal.emit(self)

    def handleMousePress(self, event):
        print('handle mouse over aoi ' + self.id)
        # get new point closest to mouse and load it        
        sp = event.scenePos()        
        self.indP = self.getNearestPoint(sp)
#        QGraphicsPolygonItem.mousePressEvent(self,  event)             
        if (event.buttons() & Qt.LeftButton): 
            if self.scene().mode == 'AOI' or self.scene().mode == 'Edit':   
#                QGraphicsPolygonItem.mousePressEvent(self, event)
                if (event.modifiers() & Qt.ControlModifier):
                    # add new point between two closest points
                    i = self.getNearestLineSegment(sp)
                    self.insertPoint(i, sp)
                elif self.indP != None and (sp - self.polygon().at(self.indP)).manhattanLength() <= self.scene().gridD:
                    # get new point closest to mouse and load it
                    self.updatePoint(self.indP, sp)      
                else:
                    self.addPoint(sp)         
           
    def mousePressEvent(self, event):
        self.indP = self.getNearestPoint(event.scenePos())
        self.scene().loadSignal.emit(self)
        self.scene().currentAOI = self
        self.setSelected(True)      
        self.update()    

    def mouseMoveEvent(self, event):
        if self.scene().mode == 'AOI' or self.scene().mode == 'Edit':           
            self.updatePoint(self.indP, event.pos())
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deletePoint(self.indP)

    def getNearestPoint(self, p):
        mini = 0
        mind = sys.maxsize
        for i in range(self.polygon().count()):
            dist = (self.polygon().at(i) - p).manhattanLength()
            if  dist < mind:
                mind = dist
                mini = i
        return mini

    def getNearestLineSegment(self, p):
        if self.polygon().count() < 2:
            return 0
        i1 = 0
        d1 = sys.maxsize
        for i in range(self.polygon().count() - 1):
            l = QLineF(self.polygon().at(i), self.polygon().at(i + 1))
            n = l.normalVector()
            n.translate(p - n.p2())
            ip = QPointF() 
            res = l.intersect(n, ip)
            n = QLineF(ip, p)
            res = l.intersect(n, ip)
            if res == QLineF.UnboundedIntersection:
                dist = min([(p - l.p1()).manhattanLength(), (p - l.p2()).manhattanLength()])
            elif res == QLineF.BoundedIntersection:
                dist = (p - ip).manhattanLength()
            else:
                continue
            if dist < d1:
                d1 = dist
                i1 = i
        return i1

    def snapToGrid(self, p):
        dx = p.x() % self.scene().gridD
        dy = p.y() % self.scene().gridD
        if dx > self.scene().gridD - dx: dx = -(self.scene().gridD - dx)
        if dy > self.scene().gridD - dy: dy = -(self.scene().gridD - dy)
        return QPointF(p.x() - dx, p.y() - dy)        

    def limitToScene(self):
        r = self.scene().sceneRect()
        p = self.pos()
        self.setPos(min(r.right() - self.rect().width(), max(p.x(), r.left())), min(r.bottom() - self.rect().height(), max(p.y(), r.top())))
    
    def getTrackLength(self, track):
        l = 0
        idx = sorted(list(range(len(track.startTime))), key=lambda k: track.startTime[k])
        for j, n in enumerate(idx):
            if self.contains(track.polygon.at(n)):
                l += track.getSegmentLength(n)
        return l
    
    def getTrackDuration(self, track):
        d = 0
        idx = sorted(list(range(len(track.startTime))), key=lambda k: track.startTime[k])
        for j, n in enumerate(idx):
            if self.contains(track.polygon.at(n)):
                d += track.startTime[n].secsTo(track.stopTime[n])
        return d
    
