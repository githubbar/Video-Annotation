# -*- coding: utf-8 -*-
"""
Annotation Tool: For annotating track time series over human tracking video
Copyright: Alex Leykin @ CIL
Email: cil@indiana.edu
http://indiana.edu/~cil
Software bindings: 
"""
import os

from PyQt5.QtCore import pyqtSignal, QTime, Qt, QDateTime, QPointF, QEvent
from PyQt5.QtGui import QFont, QPixmap, QTransform, QPainterPath, QKeySequence, \
    QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsItem, QUndoStack, \
    QGraphicsPixmapItem, QMessageBox, QGraphicsView, QAction, qApp

from aoi import AOI
from vacommands import AddCommand
from ellipse import Ellipse
from label import Label
from polygon import Polygon
from rectangle import Rectangle
from settings import StrToBoolOrKeep, keyEventToKeySequence
from snapshot import Snapshot
from track import Path


class AnnotateScene(QGraphicsScene):

    requestRowCountSignal = pyqtSignal(QGraphicsItem)        
    loadSignal = pyqtSignal(QGraphicsItem)
    saveSignal = pyqtSignal(QGraphicsItem)
    loadVideoSignal = pyqtSignal('QString')    
    initCategoriesSignal = pyqtSignal()    
    updateVideoSignal = pyqtSignal(QGraphicsItem)    
    addAOIListSignal = pyqtSignal(QGraphicsItem)          
    removeAOIListSignal = pyqtSignal(QGraphicsItem)       
    
    # Item list signals
    addItemListSignal = pyqtSignal('QString')
    updateItemListSignal = pyqtSignal('QString')    
    removeItemListSignal = pyqtSignal('QString')
    changeCurrentItemSignal = pyqtSignal('QString')
        
    modes = ('Select', 'Path', 'Separator', 'Edit', 'Polygon', 'Rectangle', 'Label', 'Snapshot', 'AOI')    
    gridD = 1
    
    currentPath = None        
    currentPolygon = None    
    currentAOI = None    
    backgroundPath = ''
    pathSmoothingFactor = 0.5
    nodeSize = 1.0
    showSegments = True
    showOrientation = True
    showOnlyCurrent = False
    showBackground = True
    FPS = 15
    variables = {}
    font = QFont('Verdana', 2.2)    
    #    add dialog to change K to project properties
    
    time = QTime(0, 0)
    
    def __init__(self):
        QGraphicsScene.__init__(self)
        # Undo stack
        self.nodeColor = Qt.red
        self.undoStack = QUndoStack(self)      
        self.setSceneRect(0, 0, 320.0, 180.0)
        self.clear()
   
    def clear(self):
        QGraphicsScene.clear(self)
        self.heatmap = QGraphicsPixmapItem()
        self.background = QGraphicsPixmapItem()
        self.background.setCursor(Qt.ArrowCursor)
        self.background.setEnabled(False)
        self.addItem(self.heatmap)
        self.addItem(self.background)
        self.heatmap.setZValue(-1)
        self.background.setZValue(-2)        
        self.heatmap.setVisible(False) 
        self.filename = None
        self.currentPath = None
        self.currentPolygon = None              
        self.currentAOI = None         
        self.backgroundPath = ''  
        self.s = None  # current stacking item index
        self.variables.clear()
        
    def removeItem(self, item):
        if type(item) == Path:
            self.removeItemListSignal.emit(item.id)
            self.currentPath = None
        if type(item) == AOI:
            self.removeAOIListSignal.emit(item)
            self.currentAOI = None
        QGraphicsScene.removeItem(self, item)

    def addItem(self, item):
        QGraphicsScene.addItem(self, item)
        if type(item) == Path:
            self.addItemListSignal.emit(item.id)
            self.currentPath = item
            # print(f'QAnnotateScene::addItem new track added ="{self.currentPath.id}"') 
        if type(item) == AOI:
            self.addAOIListSignal.emit(item)
            self.currentAOI = item
            
    def updateProjectProperties(self):
        self.removeItem(self.background)
        self.background = QGraphicsPixmapItem()
        self.background.setEnabled(False)
        self.addItem(self.background)        
        if self.backgroundPath != '' and self.backgroundPath != None:
            pixmap = QPixmap(os.path.join(os.path.dirname(str(self.filename)), self.backgroundPath))
            if pixmap.isNull():
                QMessageBox.warning(None, "Warning!", "Background image is in wrong format!")
            self.background.setPixmap(pixmap)
            self.background.setTransform(QTransform.fromScale((self.width() + 1) / pixmap.width(), (self.height() + 1) / pixmap.height()));
#             self.background.scale()
            
            self.background.setZValue(-2)        

        # update paths
        for item in list(self.items()):
            if type(item) == Path:
                path = QPainterPath()
                item.addQuadFromPolygon(path, item.polygon)
                item.setPath(path)

    def setAOIVisible(self, visible):
        for item in list(self.items()):
            if type(item) == AOI:
                item.setVisible(visible)
 
    def loadData(self, filename):
        import csv
        reader = csv.reader(open(filename, 'rb'))
        ids = next(reader)
        for line in reader:
            line = list(map(str.strip, line))
            name = line[0]  # variable name
            print(name)
            if not name in self.variables:  # skip non-existing variables
                continue     
            vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices = self.variables[name]
            if StrToBoolOrKeep(vEachNode):  # skip node-level variables: we are importing only Path level variables
                continue
            # set variable value for every track
            for item in list(self.items()):
                if type(item) == Path: 
                    try:
                        intID = str(int(item.id))  # strip leading zeros
                        idx = ids.index(intID)  # find ID in the list
                    except ValueError:
                        continue
                    if vType == 'DropDown':
                        try: 
                            choiceNumber = int(line[idx])
                            item.variables[name] = vChoices[choiceNumber]
                        except ValueError:
                            # if not a number, find an option
                            choice = line[idx].strip()
                            if choice in vChoices:
                                item.variables[name] = choice
                            else: 
                                continue
                    elif vType == 'MultiChoice':
                        strList = []
                        for choiceNumber, choice in enumerate(line[idx].split(',')):
                            try: checked = int(choice)
                            except ValueError: continue
                            if checked == 1:
                                strList.append(str(vChoices[choiceNumber]))
                        item.variables[name] = ', '.join(strList) 
                        
                        pass
                    else:
                        item.variables[name] = line[idx] 
                    
        # update current Path
        if self.currentPath != None:
            self.loadSignal.emit(self.currentPath)
        
    def loadNodeLevelVars(self, filename):
        import csv
        reader = csv.reader(open(filename, 'rb'))
        header = next(reader)
        for line in reader:
            id = line[0].strip() 
            item = next((x for x in list(self.items()) if (type(x) == Path and x.id == id)), None)
            eName, t1, t2 = line[1].strip(), QDateTime.fromString(line[2].strip(), 'dd-MMM-yy hh:mm:ss'), QDateTime.fromString(line[3].strip(), 'dd-MMM-yy hh:mm:ss')
 
#            match = next((x for x in item.startTime if (x > t1.time() and x < t2.time())), None)
            # Find node with the closest start time
            idx = min(list(range(len(item.startTime))), key=lambda i:abs(item.startTime[i].msecsTo(t1.time())))
           
            # TODO: assign check=true to varname and idx pos
            li = item.variables[eName]
            li[idx] = True
            item.variables[eName] = li
        
    def loadBatchData(self, filename):
        import csv
#         scalex = 0.05
#         scaley = 0.04
#         dx = 50
#         dy = 30
#             MAX_X=2000
#             MAX_Y=2000  
        MIN_X = -830
        MAX_X = 1297
        MIN_Y = -876            
        MAX_Y = 976      
#         w=1068
#         h=866
        w = 100
        h = 100  # dimensions of floor in feet
        reader = csv.reader(open(filename, 'rb'))
#         ids = reader.next()
        for line in reader:
            id = line[0]  # variable name
            item = Path()
            item.id = id
            item.videoname = 'videos\LBS_011906_1600PM-XVID.avi'
            self.addItem(item)      
            ts = line[3::3]
            xs = line[4::3]
            ys = line[5::3]
            for t, x, y in zip(ts, xs, ys):
#                 if not (MIN_X<float(x)<MAX_X) or not (MIN_Y<float(y)<MAX_Y):
#                     continue
                if not t.strip():
                    continue;
                tm = QTime(0, 0).addMSecs(1000.0 * int(t) / self.FPS)
#                 X = -float(x)*scalex+dx
#                 Y = float(y)*scaley+dy
#                 X = w*(float(x)-MAX_X)/(MIN_X-MAX_X)
#                 Y = h*(float(y)-MIN_Y)/(MAX_Y-MIN_Y)
                X = w * (1 - float(y))
                Y = h * (1 - float(x))
                item.addPoint(QPointF(X, Y), tm)
#                 item.startTime[item.indP] = tm
#                 item.stopTime[item.indP] = tm
#                 item.polygon.append(QPointF(X,Y))
#                 item.startTime.append(tm))
#                 tm.addMSecs(30)
#                 item.stopTime.append(tm)
#                 print x,y

            print(id) 

    def renameVariable(self, oldname, newname):
        idx = list(self.variables.keys()).index(oldname)
        key = list(self.variables.keys())[idx]
        self.variables[newname] = self.variables.pop(key)
        
        for item in list(self.items()):
            if type(item) == Path: 
                item.renameVariable(oldname, newname)     
        
    def load(self, s, buildNumber, merge=False):
        # read scene properties
        w = s.readFloat()
        h = s.readFloat()
        self.setSceneRect(0, 0, w, h)
        if buildNumber < 47:
            self.backgroundPath = s.readString().decode("utf-8")
        else:
            self.backgroundPath = s.readQVariant()
        
        if (buildNumber >= 44):
            self.nodeColor = s.readQVariant()
        if (buildNumber >= 43):
            self.pathSmoothingFactor = s.readFloat()
            self.nodeSize = s.readFloat()
            self.showSegments = s.readBool()
            self.showOrientation = s.readBool()
            self.showOnlyCurrent = s.readBool()
            
        # read project variables
        if (buildNumber >= 41):
            if merge:
                s.readQVariantMap() 
            else:
                self.variables = s.readQVariantMap()
               
        # read items
        nItems = s.readInt()
        for i in range(nItems):
            cItem = s.readQString()
            item = eval(cItem + '()')  # create an item instance of appropriate type
            if type(item) == QGraphicsPixmapItem:
                continue                      
            item.read(s, buildNumber)
            if merge:
                if type(item) == Path:
                    self.addItem(item)            
            else:
                self.addItem(item)    
        self.updateProjectProperties()

    def save(self, s):
        # write scene properties
        s.writeFloat(self.width())
        s.writeFloat(self.height())
        s.writeQVariant(self.backgroundPath)
        s.writeQVariant(self.nodeColor)
        s.writeFloat(self.pathSmoothingFactor)
        s.writeFloat(self.nodeSize)
        s.writeBool(self.showSegments)
        s.writeBool(self.showOrientation)
        s.writeBool(self.showOnlyCurrent)
        # write project variables
        s.writeQVariantMap(self.variables)
        # write items
        s.writeInt(len(list(self.items())) - 2)  # minus the heatmap and the background image
        for i in list(self.items()):
            # skip heatmap
            if type(i) == QGraphicsPixmapItem:
                continue            
            s.writeQString(i.__class__.__name__)
            i.write(s)
       
    def findPath(self, id):
        matches = [x for x in self.items() if type(x) == Path and x.id == id]
        return matches[0] if len(matches) > 0 else None 
       
    def findFirstOfTypeAtPoint(self, T, sp): 
        items = self.items(sp)
        for i in items:
            if type(i) == T: 
                return i 
        return None

    def mousePressEvent(self, event):
        QGraphicsScene.mousePressEvent(self, event)        
        # Find first item under the mouse
        sp = event.scenePos()
        if event.buttons() & Qt.LeftButton:
            if self.mode == 'Select':
                pass
            if self.mode == 'AOI':
                if (event.modifiers() & Qt.ShiftModifier): 
                    print("Creating new AOI")
                    self.undoStack.push(AddCommand(self, AOI(sp, self.font, 0.7)))                                                             
                else:
                    self.currentAOI = self.findFirstOfTypeAtPoint(AOI, sp)                    
                    if self.currentAOI != None: 
                        self.currentAOI.handleMousePress(event)
            elif self.mode == 'Path':
                if (event.modifiers() & Qt.ShiftModifier):
                    print("Creating new track")
                    newPath = Path(sp, self.font, 1.0)
                    # self.addItemListSignal.emit(newPath.id)
                    self.undoStack.push(AddCommand(self, newPath))
                    self.currentPath.handleMousePress(event)                    
                elif self.findFirstOfTypeAtPoint(Path, sp) != None or (event.modifiers() & Qt.ControlModifier) and self.currentPath != None:
                    print("Mouse press on existing track")
                    self.currentPath.handleMousePress(event)
            else: 
                items = self.items(sp)
                if (event.modifiers() & Qt.ShiftModifier and (self.mode != 'Select')): 
                    self.undoStack.push(AddCommand(self, eval(f'{self.mode}(sp, self.font, 0.4)')))
                else:
                    if items != None and items[0] != None and type(items[0]) != QGraphicsPixmapItem:
                        items[0].handleMousePress(event)
        elif (event.buttons() & Qt.RightButton):
            if self.mode == 'Path' and self.currentPath != None: 
                self.currentPath.handleMousePress(event)
           
          


class AnnotateView(QGraphicsView):
    
    def __init__(self, parent):
        QGraphicsView.__init__(self, parent)
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
