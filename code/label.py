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
from PyQt5.QtCore import QPointF, Qt, QRectF, QEvent
from PyQt5.QtGui import QFont, QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsTextItem, QGraphicsItem, qApp


class Label(QGraphicsTextItem):
    id, description = '', ''
    shownFields = ['id', 'description', 'font' ]
    checkableFields  = []
    dropdownFields = []     
    D = 2.0
    def __init__(self, scenepos=QPointF(), font=QFont('White Rabbit',  2),  opacity=1.0):    
        QGraphicsTextItem.__init__(self)
        self.setPos(QPointF(scenepos))
        self.font = font
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
        self.id = self.toPlainText()
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
    
