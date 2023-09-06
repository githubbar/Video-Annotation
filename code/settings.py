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
""" Store application wide settings """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5
import logging, sys, os, math, traceback

# Log everything, and send it to stderr.
LOG_FORMAT = '%(module)s - %(levelname)s - %(message)s'
logfile = os.path.join(os.getcwd(), 'debug.log')
logging.basicConfig(filename=logfile, level=logging.INFO, format=LOG_FORMAT) 

settings = {
"apiPath": "C:/Program Files/EyeTechDS/bin",  
"defaultFont":"D:/Projects/Visual Attention/VA2/resources/segoeui.ttf", 
"exeName":"C:/Program Files/EyeTechDS/bin/Quick Glance.exe", 
"maxPoints":10000, 
"maxDuration":60, 
"verboseSQL":False, 
"supportGL":True, 
"glMultiSampe": 4,
"calibrateDefaultUser": 0, 
"calibrateStyle": 0,  # {'CAL_STYLE_5_POINT':0,'CAL_STYLE_9_POINT':1,'CAL_STYLE_16_POINT':2}
"calibrateTargetSize": 0.03, 
"calibrateTargetVertices": 50, 
"calibrateRetryAttempts": 5, 
"calibrateTargetDelayTenthsOfSecond": 20, 
"AOIPointSize":  12, 
"fixationDurationThreshold": 0.1, # in seconds
"fixationDispersionThreshold":  40.0/1920 # in percentages 0 to 1
}

BIG_INT = 2147483647

if PyQt5.QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        PyQt5.QtCore.qFatal('')
    sys.excepthook = excepthook

def StrToBoolOrKeep(s): 
    if isinstance(s, str):
        return s.lower() == 'true'
    else: 
        return s
    
def getSeconds():
    import win32api
    return 0.001*win32api.GetTickCount()

def keyEventToKeySequence(event):
    keys = [event.key()]
    if (event.modifiers() & Qt.ShiftModifier): keys.insert(0, Qt.Key_Shift)
    if (event.modifiers() & Qt.ControlModifier): keys.insert(0, Qt.Key_Control)
    if (event.modifiers() & Qt.AltModifier): keys.insert(0, Qt.Key_Alt)
    if (event.modifiers() & Qt.MetaModifier): keys.insert(0, Qt.Key_Meta)
    
    return QKeySequence(*keys)

def distPointToSegment(p, p1, p2):
    a = (p-p1)
    b = (p2-p1)
    c = (p2-p)
    if a*b < 0: # cos(PxP1xP2)<0 distance to p1
        return (p-p1).length
    elif c*b < 0: # cos(PxP2xP1)<0  distance to p2
        return (p-p2).length
    else: # distance to projection
        return (a-b*(a*b)/(b*b)).length()

  

def pointInPolygon(x, y, poly):
    """Determine if a point is inside a given polygon or not. Polygon is a list of (x,y) pairs."""
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside


EditorReadOnlyRole = Qt.UserRole + 2
EditorTypeRole = Qt.UserRole + 3
UserDataRole = Qt.UserRole + 4
CurrentDirDataRole = Qt.UserRole + 5
 
variableTypes = ('String', 'Integer', 'DropDown', 'MultiChoice', 'Double', 'Yes/No',  'Time',  'File', 'Font')
defaultVariableValues = ('', 0, '',  '', 0.0,  False,  QTime(0,0),  '', QFont())

permanentVariableNames = ['tripType','description', 'tags', 'category', 'purchased', 'shopped',  'phone', 'employee']
permanentVariableParams = [        
    ['','DropDown', True, '', False, '',  ['fill in', 'routine', 'stock up', 'occasion'] ],                                    
    ['','String', True, '', True, '', ''], 
    ['','String', True, '', True, '', ''], 
    ['','DropDown', True, '', True, '', ''] , 
    ['','Yes/No', True, '', True, '', ''] , 
    ['','Yes/No', True, '', True, '', ''] , 
    ['','Yes/No', True, '', True, '', ''] , 
    ['','Yes/No', True, '', True, '', ''] 
                                    ]
                                    
#    permanentVariableNames = ['id', 'videoname', 'startTime', 'stopTime']
#    permanentVariableParams = [
#        ['String', True, '', False, ''], 
#        ['File', True, '', False, ''], 
#        ['Time', True, '', True, ''], 
#        ['Time', True, '', True, '']
#                                        ]
                                
