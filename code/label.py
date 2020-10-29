# -*- coding: utf-8 -*-
""" Graphics Items """

from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv

from settings import *
from propertywidget import *
from delegates import *

class Label(QGraphicsTextItem):
    id, description = '', ''
    shownFields = ['id', 'description', 'font' ]
    checkableFields  = []
    dropdownFields = []     
    D = 2.0
    def __init__(self, scenepos=QPointF(), font=QFont('White Rabbit',  2),  opacity=1.0):    
        QGraphicsTextItem.__init__(self)
        self.setPos(QPointF(scenepos))
        self.font = QVariant(font)
        self.setFont(font)
        self.setOpacity(opacity)
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable)
        self.setCursor(Qt.ArrowCursor)

    def write(self, s):
        s << self.pos()
        s.writeQVariant(self.id)
        s.writeQVariant(self.description)
        s.writeFloat(self.opacity())
        s << self.font

    def read(self, s, buildNumber):
        pos = QPointF()
        s >> pos
        self.setPos(pos)
        self.id = s.readQVariant()
        self.description= s.readQVariant()
        opacity = s.readFloat()
        self.setOpacity(opacity)
        s >> self.font        
        self.update()
        
    def paint(self, painter, option, widget):
        self.setFont(self.font)
        QGraphicsTextItem.paint(self, painter, option, widget)
        painter.setPen(QColor("blue"))
        painter.drawRoundedRect(self.boundingRect(), self.D, self.D)
        painter.setBrush(QBrush(QColor("red")))
        painter.setPen(QPen(Qt.transparent))
        painter.drawEllipse(0, 0, self.D, self.D) 

    def focusInEvent (self, event):
        QGraphicsTextItem.focusInEvent (self, event)
        qApp.installEventFilter(self)        
        self.scene().loadSignal.emit(self)
    
    def focusOutEvent (self, event):
        QGraphicsTextItem.focusOutEvent (self, event)
        self.id = QVariant(self.toPlainText())
        qApp.removeEventFilter(self)        
        self.scene().loadSignal.emit(self)
        self.scene().saveSignal.emit(self)
        
    def updatePoint(self, p):
        self.setPos(QPointF(p))     

    def update(self,  rect=QRectF() ):
        self.setPlainText(self.id)
        QGraphicsTextItem.update(self, rect)
        self.setToolTip(self.description)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.scene().removeItem(self)
        else: 
            QGraphicsTextItem.keyPressEvent(self, event)

    def eventFilter(self, object, event):
        if (event.type() == QEvent.Shortcut or event.type() == QEvent.ShortcutOverride) \
        and not object.inherits("QGraphicsView") \
        and event.key:
            event.accept()
            return True
        else: 
            return QGraphicsTextItem.eventFilter(self,  object, event)
       
    def mouseMoveEvent(self, event):
        QGraphicsTextItem.mouseMoveEvent(self, event)
        self.scene().update()
    
