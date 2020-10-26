# -*- coding: utf-8 -*-
""" Store application wide settings """
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logging
import os
import math
        
# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

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

def getSeconds():
    import win32api
    return 0.001*win32api.GetTickCount()

def keyEventToKeySequence(event):
    modifier = ''
    if (event.modifiers() & Qt.ShiftModifier): modifier += "Shift+"
    if (event.modifiers() & Qt.ControlModifier): modifier += "Ctrl+"
    if (event.modifiers() & Qt.AltModifier): modifier += "Alt+"
    if (event.modifiers() & Qt.MetaModifier): modifier += "Meta+"
    key = QKeySequence(event.key()).toString()
    return QKeySequence(modifier + key)

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

variableTypes = ('String', 'Integer', 'DropDown', 'MultiChoice', 'Double', 'Yes/No',  'Time',  'File', 'Font')
defaultVariableValues = ('', 0, '',  '', 0.0,  False,  QTime(),  '', QFont())

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
                                