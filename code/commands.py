# -*- coding: utf-8 -*-
""" Creates a main menu """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os, datetime, threading, subprocess, time, sys, csv


class AddCommand(QUndoCommand):
    def __init__(self, scene, item, parent = None):
        QUndoCommand.__init__(self, 'Added '+ type(item).__name__ + ' '+item.id.toString(),  parent)
        self.scene = scene
        self.item = item

    def undo(self):
        self.scene.removeItem(self.item)        
        self.scene.update()        

    def redo(self):
        self.scene.addItem(self.item)
        self.scene.update()     
        
class RemoveCommand(AddCommand):
    def __init__(self, scene, item, parent = None):
        QUndoCommand.__init__(self, 'Deleted '+ type(item).__name__ + ' '+item.id.toString(),  parent)
        self.scene = scene
        self.item = item

    def undo(self):
        AddCommand.redo(self)

    def redo(self):
        AddCommand.undo(self)

class AddPointCommand(QUndoCommand):
    def __init__(self, path, i, p, startTime=QTime(), parent = None):
        QUndoCommand.__init__(self, 'Added point to Path ' + path.id.toString() ,  parent)
        self.path = path
        self.i = i
        self.p = p
        self.startTime = self.stopTime = startTime
        self.stopTime = startTime.addMSecs(int(1000/self.path.scene().FPS))
        self.variables = dict()
        # make a copy of node-level variables
        for name in self.path.scene().variables:
                vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.path.scene().variables[name].toList()
                if vEachNode.toBool(): # list
                    if self.i < len(self.path.polygon):
                        self.variables[name] = self.path.variables[name].toList()[self.i]  
                    else:
                        self.variables[name] = QVariant()
                        
    def undo(self):
            self.path.polygon.remove(self.i)
            path = QPainterPath()
            self.path.addQuadFromPolygon(path, self.path.polygon)
#            track.addPolygon(self.track.polygon)
            self.path.setPath(path)
            del[self.path.startTime[self.i]]
            del[self.path.stopTime[self.i]]
            self.path.orientation.remove(self.i)            
            
            for name in self.path.scene().variables:
                vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.path.scene().variables[name].toList()
                if vEachNode.toBool(): # list
                    li = self.path.variables[name].toList()
                    del[li[self.i]]
                    self.path.variables[name] = QVariant(li)
            
            # move to the previous item
            if self.path.indP > 0:
                self.path.indP = self.i-1  
            elif self.path.indP == 0 and len(self.path.polygon)==0:
                self.path.indP = None
            
            self.path.scene().loadSignal.emit(self.path)
                
    def redo(self):
        if self.startTime == QTime() and self.i < len(self.path.polygon):
            delta = self.path.stopTime[self.i-1].toTime().msecsTo(self.path.startTime[self.i].toTime())
            self.startTime = self.stopTime = self.path.stopTime[self.i-1].toTime().addMSecs(delta/2)
           
        self.path.startTime.insert(self.i,  QVariant(self.startTime))        
        self.path.stopTime.insert(self.i,  QVariant(self.stopTime)) 
        self.path.polygon.insert(self.i,  self.p)
        
        for name in self.path.scene().variables:
            vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.path.scene().variables[name].toList()
            if vEachNode.toBool(): # list
                li = self.path.variables[name].toList()
                li.insert(self.i, self.variables[name])
                self.path.variables[name] = QVariant(li)
       
        self.path.indP = self.i
        path = QPainterPath()
        self.path.addQuadFromPolygon(path, self.path.polygon)
#        track.addPolygon(self.track.polygon)
        self.path.setPath(path)
        self.path.orientation.insert(self.i, self.p)
        self.path.scene().loadSignal.emit(self.path)

class RemovePointCommand(AddPointCommand):
    def __init__(self, path, i, p):
        AddPointCommand.__init__(self, path, i, p)
        self.setText('Removed point from Path ' + path.id.toString())
        self.startTime = path.startTime[i]
        self.stopTime = path.stopTime[i]
        
    def undo(self):
        AddPointCommand.redo(self)

    def redo(self):
        AddPointCommand.undo(self)

class UpdatePointCommand(QUndoCommand):
    def __init__(self, path, i, p, parent = None):
        QUndoCommand.__init__(self, 'Updated point position from Path ' + path.id.toString() ,  parent)
        self.path = path
        self.i = i
        self.p = p
        
    def undo(self):
        self.redo()
        
    def redo(self):
        newP = self.p
        self.p = self.path.polygon[self.i]
        self.path.polygon.replace(self.i,  newP)
        path = QPainterPath()
        self.path.addQuadFromPolygon(path, self.path.polygon)
#        track.addPolygon(self.track.polygon)
        self.path.setPath(path)
        
class UpdateOrientationCommand(QUndoCommand):
    def __init__(self, path, i, p, parent = None):
        QUndoCommand.__init__(self, 'Updated point orientation from Path ' + path.id.toString() ,  parent)
        self.path = path
        self.i = i
        self.p = p
        
    def undo(self):
        self.redo()
        
    def redo(self):
        newP = self.p
        self.p = self.path.orientation[self.i]
        self.path.orientation.replace(self.i,  newP)
