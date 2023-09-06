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
import os
import logging
from annotatescene import AnnotateScene
from settings import StrToBoolOrKeep, keyEventToKeySequence


from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QTransform, QKeySequence, QColor
from PyQt5.QtWidgets import QGraphicsView, QAction, qApp


class AnnotateView(QGraphicsView):
    
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
        logging.debug('Loading...')
       
        self.scene = AnnotateScene()
        self.setScene(self.scene)
#        self.scene.setSceneRect(0, 0, 320, 180)
        Z = 1.0
        self.FONT_ZOOM_FACTOR = 1.1
        self.scale(Z, Z)
        self.scene.mode = self.scene.modes[0]
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.scene.filename = ''
        quad1 = QAction(self)
        quad1.setShortcut(QKeySequence('Alt+1'))
        quad1.triggered.connect(lambda: self.fitInView(0, 0, 140, 80, Qt.KeepAspectRatio))                 
        self.addAction(quad1)
        quad2 = QAction(self)
        quad2.setShortcut(QKeySequence('Alt+2'))
        quad2.triggered.connect(lambda: self.fitInView(190, 0, 140, 80, Qt.KeepAspectRatio))                 
        self.addAction(quad2)
        quad3 = QAction(self)
        quad3.setShortcut(QKeySequence('Alt+3'))
        quad3.triggered.connect(lambda: self.fitInView(0, self.size().height() / 2, 140, 80, Qt.KeepAspectRatio))                 
        self.addAction(quad3)
        quad4 = QAction(self)
        quad4.setShortcut(QKeySequence('Alt+4'))
        quad4.triggered.connect(lambda: self.fitInView(self.size().width() / 2, self.size().height() / 2, 140, 80, Qt.KeepAspectRatio))                 
        self.addAction(quad4)        
        
        zoomInFontKey = QAction(self)
        zoomInFontKey.setShortcut(QKeySequence('Ctrl+='))
        zoomInFontKey.triggered.connect(self.zoomInFontPressed)                 
        self.addAction(zoomInFontKey)
        zoomOutFontKey = QAction(self)
        zoomOutFontKey.setShortcut(QKeySequence('Ctrl+-'))
        zoomOutFontKey.triggered.connect(self.zoomOutFontPressed)                 
        self.addAction(zoomOutFontKey)
        startTimeKey = QAction(self)
        startTimeKey.setShortcut(Qt.Key_F1)        
        startTimeKey.triggered.connect(self.startTimeKeyPressed)           
        self.addAction(startTimeKey)        
        stopTimeKey = QAction(self)
        stopTimeKey.setShortcut(Qt.Key_F2)        
        stopTimeKey.triggered.connect(self.stopTimeKeyPressed)           
        self.addAction(stopTimeKey)
        clearKey = QAction(self)
        clearKey.setShortcut(Qt.Key_QuoteLeft)        
        clearKey.triggered.connect(self.clearPointVariablesPressed)           
        self.addAction(clearKey)        
        
        qApp.installEventFilter(self) 
        self.setDragMode(QGraphicsView.ScrollHandDrag)             
        logging.debug('Done Loading...')

#     def keyPressEvent(self, event):
# #         self.setCursor(Qt.DragMoveCursor)
#         if event.modifiers() == Qt.CTRL:
#             self.setCursor(Qt.CrossCursor) 
#         QGraphicsView.keyPressEvent(self,  event)          

    def zoomInFontPressed(self):
        for i in self.scene.selectedItems():
            f = i.font 
            f.setPointSizeF(f.pointSizeF() * self.FONT_ZOOM_FACTOR)
            i.font = f
            self.scene.loadSignal.emit(i)
        self.scene.update()    

    def zoomOutFontPressed(self):
        for i in self.scene.selectedItems():
            f = i.font 
            f.setPointSizeF(f.pointSizeF() / self.FONT_ZOOM_FACTOR)
            i.font = f
            self.scene.loadSignal.emit(i)
        self.scene.update()    

    def clearPointVariablesPressed(self):
#         TEMP: clear for all points
#         if self.scene.currentPath != None:
#             for idx in range(len(self.scene.currentPath.startTime)):
#                 self.scene.currentPath.indP = idx
#                 self.scene.currentPath.clearPointVariables()
#             self.scene.loadSignal.emit(self.scene.currentPath)
       
        if self.scene.currentPath != None and self.scene.currentPath.indP != None:
            self.scene.currentPath.clearPointVariables()
            self.scene.loadSignal.emit(self.scene.currentPath)

    def startTimeKeyPressed(self):
        if self.scene.currentPath != None and self.scene.currentPath.indP != None:
            self.scene.currentPath.startTime[self.scene.currentPath.indP] = self.scene.time
            self.scene.loadSignal.emit(self.scene.currentPath)
            
    def stopTimeKeyPressed(self):
        if self.scene.currentPath != None and self.scene.currentPath.indP != None:
            self.scene.currentPath.stopTime[self.scene.currentPath.indP] = self.scene.time
            self.scene.loadSignal.emit(self.scene.currentPath)

    def eventFilter(self, obj, event):
        if (event.type() == QEvent.KeyPress):
#             if event.modifiers() & Qt.ControlModifier:
#                 self.setCursor(Qt.CrossCursor)            
            for name in self.scene.variables:
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.scene.variables[name]
                shortcut = vShortcut
                if not shortcut.strip():
                    continue
                if shortcut == keyEventToKeySequence(event):
                    # toggle corresponding variable
                    item = self.scene.currentPath                    
                    varType = vType
                    if StrToBoolOrKeep(vEachNode):  # list                    
                        if item.indP == None: continue
                        li = item.variables[name]
                        if varType == 'Yes/No': 
                            li[item.indP] = not StrToBoolOrKeep(li[item.indP])
                        elif varType == 'Integer':
                            val = int(li[item.indP]) if li[item.indP] != None else 0                        
                            li[item.indP] = val + 1
                        item.variables[name] = li
                    else:
                        if varType == 'Yes/No': 
                            item.variables[name] = not item.variables[name]
                        elif varType == 'Integer':
                            val = item.variables[name]                           
                            val = int(val) if val != None else 0      
                            item.variables[name] = val + 1
                    self.scene.loadSignal.emit(item)
                    return True            
        return QGraphicsView.eventFilter(self, obj, event)
            
# Size scene to fit the view
    
    def fitSceneInView(self):
        self.setTransform(QTransform())
        s = min(self.width() / self.scene.width(), self.height() / self.scene.height())
        self.scale(s, s);

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        self.scale(factor, factor)

    def drawBackground (self, painter, r):
        QGraphicsView.drawBackground(self, painter, r)
        if self.scene.showBackground != None:
            painter.setPen(QColor("black"))
            painter.setOpacity(0.1)
            r = self.sceneRect()
            x = r.left()
            while x <= r.right():
                painter.drawLine(x, r.top(), x, r.bottom())     
                x += self.scene.gridD
            y = r.top()            
            while y <= r.bottom():
                painter.drawLine(r.left(), y, r.right(), y)     
                y += self.scene.gridD          
