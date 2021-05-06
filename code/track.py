# -*- coding: utf-8 -*-
""" Path Item"""
import csv
import os
import sys

from PyQt5.QtCore import Qt, QDateTime, QLineF, QTime, QPointF
from PyQt5.QtGui import QFont, QPainterPathStroker, QColor, QPen, QBrush, \
    QPolygonF, QPainterPath, QPainter
from PyQt5.QtWidgets import QGraphicsPathItem, QGraphicsItem
from numpy import math

from settings import StrToBoolOrKeep, defaultVariableValues, variableTypes, \
    BIG_INT
from vacommands import UpdatePointCommand, UpdateOrientationCommand, RemoveCommand, \
    RemovePointCommand, AddPointCommand

NON_EMPTY_TIME = 2000 # time in msec
class Path(QGraphicsPathItem):
    id, videoname = '', ''
    shownFields = ['id', 'videoname', 'startTime', 'stopTime']
    p0 = None  # placeholder for the first point
    indP = None  # current node index
    R = 2.0  # node radius 
    K = 6.0  # orientation line length compared to R    poin
    penR = 0.3  # edge width
    variables, gyro, accel = {}, {}, {}
    def __init__(self, point=None, font=QFont('White Rabbit', 2), opacity=1.0):    
        QGraphicsPathItem.__init__(self)
        self.setCursor(Qt.ArrowCursor)
        self.stroker = QPainterPathStroker()        
        self.stroker.setWidth(1 * self.R)        
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemClipsToShape | QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(QColor(Qt.transparent))
        self.setPen(QPen(QBrush(Qt.blue), self.penR))
        self.setCursor(Qt.ArrowCursor)
        self.startTime, self.stopTime = [], []
        self.polygon = QPolygonF()     
        self.orientation = QPolygonF()     
        self.setOpacity(opacity)
        self.font = font
        self.p0 = point
        self.choosingOrientation = False
#         self.variables = dict()
#         self.gyro = dict()
#         self.accel = dict()
        
                              
    def shape(self):
#        if self.scene().showOnlyCurrent:
#            sh = self.stroker.createStroke(QPainterPath())
#            if self.indP != None:
#                sh.addEllipse(self.polygon[self.indP],  self.K,  self.K)
#        else:
        sh = self.stroker.createStroke(self.path())
        for i in range(self.polygon.count()):
            sh.addEllipse(self.polygon[i], self.K, self.K)
            if self.scene().currentPath == self:
                # Expand for video position indicator
                if i > 0 and self.scene().time > self.stopTime[i - 1] and self.scene().time < self.startTime[i]:
                    sh.addEllipse(self.getSegmentPosInTime(i - 1, self.scene().time), 2 * self.R + 2, 2 * self.R + 2) 
        return sh

    def write(self, s):
        #FIXME: variables length doesn't match startTime length
        n = len(self.startTime)
        for name in self.scene().variables:
            vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.scene().variables[name]
            if StrToBoolOrKeep(vEachNode): # list
                li = self.variables[name]
                del li[n:]
        if len(self.startTime) < len(self.variables["Category Shopped"]):
            print(f'Error: Variables length is more than startTime length, path id = {self.id}')
        
#         print(f'saving path {self.id}: time len = {len(self.startTime)};'\
#          f'cat shopped = {len(self.variables["Category Shopped"])};' \
#          f'poly = {len(self.polygon)};' \
#          f'ori = {len(self.orientation)}')

        s.writeQVariant(self.id)
        s.writeQVariant(self.videoname)        
        s.writeQVariantList(self.startTime)        
        s.writeQVariantList(self.stopTime)
        s.writeQVariantMap(self.variables)        
        s << self.polygon        
        s << self.orientation
        s.writeFloat(self.opacity())
        s << self.font

    def read(self, s, buildNumber):

        self.id = s.readQVariant()
        self.videoname = s.readQVariant()
        self.startTime = s.readQVariantList()
        self.stopTime = s.readQVariantList()   
        # Fix QDateTime to QTime
        self.startTime = list(map(lambda x: x.time() if type(x) == QDateTime else x, self.startTime))
        self.stopTime = list(map(lambda x: x.time() if type(x) == QDateTime else x, self.stopTime))
        
        self.variables = s.readQVariantMap()   
        s >> self.polygon
        s >> self.orientation
        self.setOpacity(s.readFloat())
        if buildNumber < 47:
            self.font = s.readQVariant()
        else:
            s >> self.font
      
    def addQuadFromPolygon(self, path, polygon):
        if polygon.count() == 0:
            return
        path.moveTo(polygon.at(0))
        # add temporary points
        polygon.prepend(polygon.at(0))
        polygon.append(polygon.at(polygon.count() - 1))       
        
        for i in range(1, polygon.count() - 2):
            c1, c2 = self.getControlPoints(polygon.at(i - 1), polygon.at(i), polygon.at(i + 1), polygon.at(i + 2))
            path.cubicTo(c1, c2, polygon.at(i + 1))
        
        # remove temporary points
        polygon.remove(0)
        polygon.remove(polygon.count() - 1)

    def getQuadFromPoints(self, points=[]):
        if len(points) < 4:
            if len(points) < 2:
                return None
            path = QPainterPath(points[0])
            path.lineTo(points[1])
            return path

        path = QPainterPath(points[1])
        for i in range(1, len(points) - 2):
            c1, c2 = self.getControlPoints(points[i - 1], points[i], points[i + 1], points[i + 2])
            path.cubicTo(c1, c2, points[i + 1])
        return path
        
    def getControlPoints(self, p0, p1, p2, p3):
        if p0 == p1 or p1 == p2 or p2 == p3:
            return (p1 * 2.0 + p2) / 3.0, (p1 + p2 * 2.0) / 3.0        
        K = 1.0
        c1 = (p0 + p1) / 2.0
        c2 = (p1 + p2) / 2.0
        c3 = (p2 + p3) / 2.0
        len1 = math.sqrt((p1 - p0).x() ** 2 + (p1 - p0).y() ** 2)
        len2 = math.sqrt((p2 - p1).x() ** 2 + (p2 - p1).y() ** 2)
        len3 = math.sqrt((p3 - p2).x() ** 2 + (p3 - p2).y() ** 2)

        k1 = len1 / (len1 + len2)
        k2 = len2 / (len2 + len3)

        m1 = c1 + (c2 - c1) * k1
        m2 = c2 + (c3 - c2) * k2
        cp1 = (c2 - m1) * self.scene().pathSmoothingFactor + p1
        cp2 = (c2 - m2) * self.scene().pathSmoothingFactor + p2
        return cp1, cp2
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        if self.scene().showSegments:
            QGraphicsPathItem.paint(self, painter, option, widget)
        painter.setFont(self.font)
        painter.setPen(Qt.red)     
        
        # Draw Orientations >> only for active path
        if self.scene().showOrientation and self.scene().currentPath == self:
            for i in range(self.polygon.count()):
                line = QLineF(self.polygon.at(i), self.orientation.at(i))
                line.setLength(self.K * self.R)
                painter.drawLine(line)             
        # Draw nodes and lines
        for i in range(self.polygon.count()):
            painter.setBrush(QBrush(Qt.white))
            if self.scene().currentPath == self and self.indP == i:
                painter.setPen(QPen(self.scene().nodeColor, 1))
                painter.setBrush(QBrush(Qt.red))
            elif 'purchased' in self.variables and i < len(self.variables['purchased']) and StrToBoolOrKeep(self.variables['purchased'][i]):
                if not self.variables['Category Shopped'][i]:
                    painter.setPen(QPen(Qt.gray, 1))
                else:
                    painter.setPen(QPen(Qt.green, 1))
                 
            elif 'shopped' in self.variables and i < len(self.variables['purchased'])  and StrToBoolOrKeep(self.variables['shopped'][i]):
                if not self.variables['Category Shopped'][i]:
                    painter.setPen(QPen(Qt.gray, 1))
                else:
                    painter.setPen(QPen(Qt.blue, 1))
            else:
                painter.setPen(QPen(self.scene().nodeColor, 1))
            
            nonEmptyMultiplier = 2 if self.startTime[i].msecsTo(self.stopTime[i]) >= NON_EMPTY_TIME else 1                                 
            if (not self.scene().showOnlyCurrent) or (self.startTime[i] <= self.scene().time <= self.stopTime[i]):
                painter.drawEllipse(self.polygon.at(i), nonEmptyMultiplier* self.R * self.scene().nodeSize, nonEmptyMultiplier* self.R * self.scene().nodeSize)
                
            # Paint video position indicator and auto-load properties during playback
            if self.scene().currentPath == self and len(self.stopTime) > 0 :
                painter.setBrush(QBrush(Qt.transparent))                                
                painter.setPen(QPen(QBrush(Qt.red), 2))
#                 print(f'i is {i} scene time is {self.scene().time} \nstarttime is {self.startTime[i]} stoptime is {self.stopTime[i]}')
                if i > 0 and self.scene().time > self.stopTime[i - 1] and self.scene().time < self.startTime[i]:
                    painter.drawEllipse(self.getSegmentPosInTime(i - 1, self.scene().time), 2 * self.R * self.scene().nodeSize, 2 * self.R * self.scene().nodeSize)
                elif i < len(self.startTime)-1 and self.scene().time >= self.startTime[i] and self.scene().time < self.startTime[i+1]:
                    # print(f'node------------ {i}')
                    painter.drawEllipse(self.polygon.at(i), self.R * self.scene().nodeSize,  self.R * self.scene().nodeSize) 
                    self.indP = i
                    self.scene().loadSignal.emit(self)
     
    def getSegmentPosInTime(self, i, t, linear=False):
        t0 = QTime(0,0).msecsTo(t)
        t1 = QTime(0,0).msecsTo(self.stopTime[i])
        t2 = QTime(0,0).msecsTo(self.startTime[i + 1])
        p1 = self.polygon.at(i)
        p2 = self.polygon.at(i + 1)       
        if linear:
            return QPointF((p2.x() * (t0 - t1) + p1.x() * (t2 - t0)) / (t2 - t1), (p2.y() * (t0 - t1) + p1.y() * (t2 - t0)) / (t2 - t1))
        else:
            points = [p1, p2]
            if i > 0: points.insert(0, self.polygon.at(i - 1))
            if i < self.polygon.count() - 2: 
                points.append(self.polygon.at(i + 2))
            elif i < self.polygon.count() - 1:
                points.append(self.polygon.at(i + 1))
            path = self.getQuadFromPoints(points)
            return path.pointAtPercent(1.0 * (t0 - t1) / (t2 - t1))
            
    def updatePoint(self, i, p):
        if i == None:
            return        
        self.polygon.replace(i, p)
        path = QPainterPath()
        self.addQuadFromPolygon(path, self.polygon)
        self.setPath(path)
    
    def updatePointCommand(self, i, p):
        if i == None:
            return        
        self.scene().undoStack.push(UpdatePointCommand(self, i, p))
        
    def updateOrientation(self, i, p):
        if i == None:
            return        
        self.orientation.replace(i, p)

    def updateOrientationCommand(self, i, p):
        if i == None:
            return        
        self.scene().undoStack.push(UpdateOrientationCommand(self, i, p))            

    def deletePoint(self):
        if self.indP == None or self.indP == 0 and len(self.polygon) == 1:
            self.scene().undoStack.push(RemoveCommand(self.scene(), self))                            
        else:
            self.scene().undoStack.push(RemovePointCommand(self, self.indP, self.polygon[self.indP]))                                             
    
    def clearPointVariables(self):
        if self.indP != None:
            for name in self.scene().variables:
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.scene().variables[name]
                if StrToBoolOrKeep(vEachNode):
                        self.variables[name][self.indP] = None

    def addPoint(self, p, time):
        idx = len(self.polygon)
        # print(f'Adding point {p} to track id="{self.id}"')
        self.indP = idx        
        self.scene().undoStack.push(AddPointCommand(self, idx, p, time))       
        
        # Block time overlap while adding nodes
        if idx > 0:
            self.startTime[idx] = max(self.startTime[idx], self.stopTime[idx-1].addMSecs(10))
            self.stopTime[idx] = max(self.startTime[idx], self.stopTime[idx])
        
    def insertPoint(self, i, p):
        if len(self.polygon) < 2 or i >= len(self.polygon) - 1: 
            return
        self.scene().undoStack.push(AddPointCommand(self, i + 1, p))                                             

    def getNearestPoint(self, p):
        mini = 0
        mind = BIG_INT
        for i in range(self.polygon.count()):
            dist = (self.polygon.at(i) - p).manhattanLength()
            if  dist < mind:
                mind = dist
                mini = i
        return mini
   
    def getNearestLineSegment(self, p):
        if self.polygon.count() < 2:
            return 0
        i1 = 0
        d1 = BIG_INT
        # FIXME: doesn't always insert for the closest segment (find segment)
        
        for i in range(self.polygon.count() - 1):
            l = QLineF(self.polygon.at(i), self.polygon.at(i + 1))
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
    
    def getSegmentLength(self, n):
        if n == 0:
            return 0
        else:
            p2 = self.polygon.at(n)
            p1 = self.polygon.at(n-1)
            return QLineF(p1, p2).length()
     
    def getPathLength(self):
        l = 0 # the length
        for i in range(self.polygon.count() - 1):
            p1 = self.polygon.at(i)
            p2 = self.polygon.at(i + 1)
            l = l + QLineF(p1, p2).length()
        return l

    # def focusInEvent (self, event):
    #     self.scene().saveSignal.emit(self)
    #     # # save existing currentPath path
    #     # # self.scene().loadSignal.emit(self)
    #
    #     # print('--------------------------------------------------------------------')                
    #     # print(f'QGraphicsItem::focusInEvent in track id="{self.id}" ')
    #     # if self.scene() and self.scene().currentPath:
    #     #     print(f'Current path id="{self.scene().currentPath.id}"')
    #     # else:
    #     #     print(f'No current path')             
    #     # # if self.id != self.scene().currentPath.id:
    #     # if self.scene().currentPath != self and self.polygon.count():
    #     #     self.scene().saveSignal.emit(self.scene().currentPath)         
    #     # self.scene().changeCurrentItemSignal.emit(self.id)
    #     # return QGraphicsItem.focusInEvent(self, event)
    #     # # self.scene().currentPath = self
    #
    #     # QGraphicsItem.focusInEvent(self, event)
    #     # save existing currentPath path
    #     self.scene().changeCurrentItemSignal.emit(self.id)
    #
    #
    #     # QGraphicsItem.focusInEvent(self, event)
    #     # # save existing currentPath path
    #     # if self.scene().currentPath != self and self.polygon.count():
    #     #     self.scene().saveSignal.emit(self.scene().currentPath)        
    #     # self.scene().loadSignal.emit(self)     
    #     # self.scene().currentPath = self
    #     # # self.scene().changeCurrentItemSignal.emit()
    #
    # def focusOutEvent (self, event):
    #     QGraphicsItem.focusOutEvent(self, event)
    #     # When would I need to save on Focus Out?

    def handleMousePress(self, event):
#         print('handle mouse over path ' + self.id)
        if self.scene() == None:
            return
        # get new point closest to mouse and load it
        sp = event.scenePos()        
#         QGraphicsPathItem.mousePressEvent(self, event)
        point_append_time = self.scene().time

        if (event.buttons() & Qt.LeftButton and self.scene().mode != 'Select'): 
            if not self.choosingOrientation:
                # save old point
                if (event.modifiers() & Qt.AltModifier):
                    # add new point between two closest points
                    i = self.getNearestLineSegment(sp)
                    self.insertPoint(i, sp)
                elif (not self.scene().showOnlyCurrent) and self.indP != None and QLineF(sp, self.polygon.at(self.indP)).length() < 2 * self.R * self.scene().nodeSize:
                    self.updatePointCommand(self.indP, sp)
                elif (event.modifiers() & Qt.ControlModifier):
                    self.addPoint(sp, point_append_time)
                    self.update()     
        elif (event.buttons() & Qt.RightButton): 
            self.choosingOrientation = True  
        Path.mymousePressEvent(self, event)
            
    def mymousePressEvent(self, event):
        print(f'Track::mousePressEvent id="{self.id}"')
   
        self.scene().changeCurrentItemSignal.emit(self.id)
        if not self.scene().showOnlyCurrent:
            self.indP = self.getNearestPoint(event.scenePos())
            self.scene().currentPath = self
            self.scene().loadSignal.emit(self)
            self.setSelected(True)
                  
        self.scene().updateVideoSignal.emit(self)               
        self.update()
  
    def getVariableValuesList(self, idx=None):
        if idx == None:
            idx = self.indP
        varList = []
        for name in self.scene().variables:
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.scene().variables[name]
            if StrToBoolOrKeep(vEachNode) and idx != None:
                v = self.variables[name][idx]
                if (type(v) == QDateTime):
                    v = v.toString('hh-mm-ss')
                else:
                    v = str(v)                    
                varList.append(str(v))
            else: 
                v = self.variables[name]
                if (type(v) == QDateTime):
                    v = v.toString('hh-mm-ss')
                else:
                    v = str(v)
                varList.append(str(v))
        return varList

    def renameVariable(self, oldname, newname):
        idx = list(self.variables.keys()).index(oldname)
        key = list(self.variables.keys())[idx]
        self.variables[newname] = self.variables.pop(key)
        
    def populateVariables(self):
        # add missing vars
        for name in self.scene().variables:
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.scene().variables[name]
            if not name in self.variables:        
                val = defaultVariableValues[variableTypes.index(vType)]
                vEachNode = StrToBoolOrKeep(vEachNode)
                if vEachNode:
                    self.variables[name] = [val] * len(self.polygon)
                else:
                    self.variables[name] = val                
        # remove extra vars
        namestoremove = []
        for name in self.variables:
            if not name in self.scene().variables:
                namestoremove.append(name)
        for name in namestoremove:
            self.variables.pop(name)

    def itemChange(self, change, value):
        # print(f'Path::itemChange')
        
        if self.scene() == None: 
            return QGraphicsItem.itemChange(self, change, value)
        # print('--------------------------------------------------------------------')                
        # print(f'QGraphicsItem::itemChange in track id="{self.id}" changed. Change type: {change}')
        # if self.scene().currentPath:
        #     print(f'Current path id="{self.scene().currentPath.id}"')
        # else:
        #     print(f'No current path')

        # item selected or made visible => make it the current item
        # if value:        
        #     self.scene().currentPath = self     

        # if change == QGraphicsItem.ItemSelectedHasChanged and value:
        #     self.scene().currentPath = self
        #     print(f'Path selected')
        if change == QGraphicsItem.ItemSceneHasChanged:
            self.populateVariables()       
            if (self.polygon.count() == 0 and self.p0 != None):
                # print(f'Adding point')
                self.addPoint(self.p0, self.scene().time)   
                self.p0 = None 
            path = QPainterPath()
            self.addQuadFromPolygon(path, self.polygon)
            self.setPath(path)
            # load gyro data (on track load)
            if not self.gyro or not self.accel:
                self.gyro, self.accel = self.loadgyroacceldata('gyroacceldata')

            
        if (change == QGraphicsItem.ItemSelectedHasChanged):
            if self.isSelected():
                self.setPen(QPen(QBrush(QColor(255, 165, 0)), self.penR * 1.5))    
#                unselect all other items in the scene
                for i in self.scene().selectedItems():
                    if i != self:
                        i.setSelected(False)
            else: 
                self.setPen(QPen(QBrush(Qt.blue), self.penR))      
        return QGraphicsItem.itemChange(self, change, value)
        
    def mouseReleaseEvent(self, event):                
            # TODO: choosing orientation undo !!!
#            self.updateOrientationCommand(self.indP, sp)
        # self.scene().loadSignal.emit(self)            
        self.choosingOrientation = False

    def mouseMoveEvent(self, event):
        if self.scene().mode == 'Path' and self.indP != None:
            if self.choosingOrientation:
                self.updateOrientation(self.indP, event.pos())
                self.update()
            else:
                self.updatePoint(self.indP, event.pos())
        
    def keyPressEvent(self, event):
#         print('Path key press')
        if event.key() == Qt.Key_Delete:
            self.deletePoint()

    def toString(self):
        return self.id
    
    def loadgyroacceldata(self, path):
        filename = os.path.join(os.path.dirname(str(self.scene().filename)), str(path), self.id+'.tsv')
        gyro = dict()
        accel = dict()
        if os.path.isfile(filename):
            with open(filename, 'rb') as tsvin:
                tsvin = csv.reader(tsvin, delimiter='\t')
                
                for row in tsvin:
                    if row[3]:
                        gyro[row[2]] = row[3:6] # deg/sec
                    if row[6]:
                        accel[row[2]] = row[6:9] # m/(sec^2)
        return gyro, accel
    
    def predictPath(self):
        print('Trying to predict path based on accelerometer data')
        # convert current node's time to msec
        i = self.indP
        msec = QTime(0,0).msecsTo(self.stopTime[i])
        # get current point and orientation point
        p = self.polygon.at(i)
        o = self.orientation.at(i)
        # predict next location
        # 1- remove gravity from accelerometer using gyro data
        # 2 - double integrate to get position
        # this will not work (with any accuracy)
        # ? - improve by modelling with Kalman filter
        # ? - improve by using pedometer algorithm
        
        
        # here is why: http://stackoverflow.com/questions/5550453/ios-movement-precision-in-3d-space
                     