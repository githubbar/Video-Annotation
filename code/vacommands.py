# -*- coding: utf-8 -*-
"""
====================================================================================
Video Annotation Tool
Copyright (C) 2023 Alex Leykin @ CIL
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
""" Creates a main menu """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os, datetime, threading, subprocess, time, sys, csv
from settings import *

class AddCommand(QUndoCommand):
    def __init__(self, scene, item, parent = None):
        QUndoCommand.__init__(self, 'Added '+ type(item).__name__ + ' '+item.id,  parent)
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
        QUndoCommand.__init__(self, 'Deleted '+ type(item).__name__ + ' '+item.id,  parent)
        self.scene = scene
        self.item = item

    def undo(self):
        AddCommand.redo(self)

    def redo(self):
        AddCommand.undo(self)

class AddPointCommand(QUndoCommand):
    variables = {}
    
    def __init__(self, path, i, p, startTime=QTime(0,0), parent = None):
        QUndoCommand.__init__(self, 'Added point to Path ' + path.id ,  parent)
        self.path = path
        self.i = i
        self.p = p
        self.startTime = self.stopTime = startTime
        self.stopTime = startTime.addMSecs(int(1000/self.path.scene().FPS))
        # do NOT make a copy of node-level variables
        for name in self.path.scene().variables:
                vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.path.scene().variables[name]
#                 print(f'len = {len(self.variables["purchased"])} i = {i}')
                if StrToBoolOrKeep(vEachNode): # list
                    # if self.i < len(self.path.polygon):
                        # self.variables[name] = self.path.variables[name][self.i]  
                    # else:
                    self.variables[name] = None
                        
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
                vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.path.scene().variables[name]
                if StrToBoolOrKeep(vEachNode): # list
                    li = self.path.variables[name]
                    del[li[self.i]]
#                     self.path.variables[name] = li
            
            # move to the previous item
            if self.path.indP > 0:
                self.path.indP = self.i-1  
            elif self.path.indP == 0 and len(self.path.polygon)==0:
                self.path.indP = None
            
            self.path.scene().loadSignal.emit(self.path)
                
    def redo(self):
        if self.startTime == QTime(0,0) and self.i < len(self.path.polygon):
            delta = self.path.stopTime[self.i-1].msecsTo(self.path.startTime[self.i])
            self.startTime = self.stopTime = self.path.stopTime[self.i-1].addMSecs(delta/2)
           
        self.path.startTime.insert(self.i,  self.startTime)
        self.path.stopTime.insert(self.i,  self.stopTime) 
        self.path.polygon.insert(self.i,  self.p)
        print(f'Adding startTime to track id="{self.path.id}", new length={len(self.path.startTime)}')

        # FIXME: !!!!! all the shit in prev track shifts by +1 on creating new track♦
        # above the starttime length is 1, length of vars below is leftover from the old track, why?
        for name in self.path.scene().variables:
            vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = self.path.scene().variables[name]
            if StrToBoolOrKeep(vEachNode): # list
                li = self.path.variables[name]
                li.insert(self.i, self.variables[name])
#                 self.path.variables[name] = li
        print(f'Adding vars to track id="{self.path.id}", new length={len(self.path.variables["Category Shopped"])}')
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
        self.setText('Removed point from Path ' + path.id)
        self.startTime = path.startTime[i]
        self.stopTime = path.stopTime[i]
        
    def undo(self):
        AddPointCommand.redo(self)

    def redo(self):
        AddPointCommand.undo(self)

class UpdatePointCommand(QUndoCommand):
    def __init__(self, path, i, p, parent = None):
        QUndoCommand.__init__(self, 'Updated point position from Path ' + path.id ,  parent)
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
        QUndoCommand.__init__(self, 'Updated point orientation from Path ' + path.id ,  parent)
        self.path = path
        self.i = i
        self.p = p
        
    def undo(self):
        self.redo()
        
    def redo(self):
        newP = self.p
        self.p = self.path.orientation[self.i]
        self.path.orientation.replace(self.i,  newP)
