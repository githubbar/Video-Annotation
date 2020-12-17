# -*- coding: utf-8 -*-
""" PrepertyTree View/Model is a widget for editing object's properties stored in a dictionary attribute *data* """
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from label import *
from track import *
from polygon import *
from rectangle import *
from ellipse import *
from delegates import *

CheckBoxType = QStandardItem.UserType+1

class PropertyWidget(QTreeWidget,  object):
    def __init__(self, parent, task=None):
        QTreeWidget.__init__(self, parent)
        self.expandedCategories = []
        self.currentPath = None
#         self.headerItem().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.itemExpanded.connect(self.onItemExpanded)
        self.itemCollapsed.connect(self.onItemCollapsed)
        
    def dataChanged(self,  topLeft,  bottomRight, roles=list()):
        QTreeWidget.dataChanged(self,  topLeft,  bottomRight)
        if self.currentPath:
            self.saveItem(self.currentPath)
            self.currentPath.update()
            
    def onItemExpanded(self, item):
        self.expandedCategories.append(item.data(0, Qt.EditRole))

    def onItemCollapsed(self, item):
        self.expandedCategories.remove(item.data(0, Qt.EditRole))
  
    def loadItem(self, item):
#         print "Loading Item", item
        import operator
        self.currentPath = item
        self.clear()
        """Load selected item properties"""
        sectionItem = PropertyTreeItem(True, 'Default', item.scene())
        self.addTopLevelItem(sectionItem)   
        sectionItem.setExpanded(True)        
        delegate = CustomDelegate(self)
        self.setItemDelegate(delegate)
        
             
        for name in item.shownFields:
            v = getattr(item, name)
            # if list, get current element
            if type(v) == list:
                if item.indP == None: continue
                v = v[item.indP]
            sectionItem.addChild(PropertyTreeItem(False, name,  item.scene(),  None, v ))
            
        #### Begin display dymanic project variables 
        if type(item) == Path: 
            ## Add Section Headers
            listItems = []
            for key, value in item.scene().variables.items():
                listItem = [key]
                listItem.extend(value)
                listItems.append(listItem)
            listItems.sort(key=lambda x: (StrToBoolOrKeep(x[5]), x[6], x[0]))
            oldGroupName = None
            currentParent = None
            for name, vDescr, vType, vShow, vShortcut, vEachNode, vGroup, vChoices in listItems:
                if StrToBoolOrKeep(vShow):
                    v = item.variables[name]
                    if StrToBoolOrKeep(vEachNode): # list
                        if item.indP == None: continue
                        v = v[item.indP]
                    vUserData = vChoices
                    if vGroup == '': 
                        vGroup = 'General'
                    if oldGroupName != vGroup:
                        sectionItem = PropertyTreeItem(True, vGroup, item.scene())
                        self.addTopLevelItem(sectionItem)
                        sectionItem.setExpanded(sectionItem.data(0, Qt.EditRole) in self.expandedCategories)                                                
                        oldGroupName = vGroup                    
                    sectionItem.addChild(PropertyTreeItem(False, name,  item.scene(),  vDescr, v, vType, vUserData))
       #### End display dymanic project variables 
        self.setIndentation(10)
#        self.expandAll()

    def saveItem(self, item):
#         print("Saving Item",  item)
        for name in item.shownFields:
            # find matching top level item                   
            foundItems = self.findItems(name, Qt.MatchExactly | Qt.MatchRecursive)
            if not foundItems:
                return
            value = foundItems[0].data(1, Qt.EditRole)
            # if list
            l = getattr(item, str(name))
            if type(l) == list:
                if item.indP == None: continue
                l[item.indP] = value
                value = l
            else:
                setattr(item, str(name), value)                
            
        #### Begin save dymanic project variables        
#         self.expandedCategories = []
        if type(item) == Path:         
            for i in range(self.topLevelItemCount()):
                top = self.topLevelItem(i)
#                 if top.isExpanded():
#                     self.expandedCategories.append(top.data(0, Qt.EditRole))
                for row in range(top.childCount()):
                    name = top.child(row).data(0, Qt.EditRole)
                    if name in item.scene().variables:  # temp
                        #### Begin Save dymanic project variables             
                        vDescr, vType, vShow, vShortcut,  vEachNode, vGroup, vChoices = item.scene().variables[name]
                        if StrToBoolOrKeep(vEachNode): # list
                            if item.indP == None: continue
                            li = item.variables[name]
                            li[item.indP] = top.child(row).data(1, Qt.EditRole)
                            item.variables[name] = li
                        else:
#                            if name == 'Employment':
#                                print "PropertyWidget: saveItem", name, "item:", item,"data:", top.child(row).data(1, Qt.EditRole)
                            item.variables[name] = top.child(row).data(1, Qt.EditRole)
                        #### End Save dymanic project variables 
                    else:
                        value = top.child(row).data(1, Qt.EditRole)
                        # load video if selected for the first time
            #            if name == 'videoname' and self.currentPath.videoname=='':
            #                self.currentPath.scene().loadVideoSignal.emit(value)

                        # if list: write to list element
                        l = getattr(item, str(name))
                        if type(l) == list:
                            if item.indP == None:
                                continue
                            else:
                                l[item.indP] = value
                                value = l
                        setattr(item, str(name), value)
            item.scene().updateItemListSignal.emit(item)
        #### End save dymanic project variables 

class PropertyTreeItem(QTreeWidgetItem):
    def __init__(self, header, name,  scene, tooltip=None,  data2=None, vType=None, vUserData=None, parent=None):
        QTreeWidgetItem.__init__(self,  parent)
                        
        self.setData(0, Qt.EditRole, name)    
            
        if header: # section header items
            self.setFirstColumnSpanned(True)        
            self.setBackground(0, QBrush(QColor("#005500")))
            self.setBackground(1, QBrush(QColor("#005500")))
        else: # child items
            if tooltip == None:
                tooltip = name
            self.setToolTip(0, '<p>'+tooltip+'</p>')        
        
            self.setData(1, Qt.EditRole, data2)
            self.setFlags(self.flags() | Qt.ItemIsEditable)
#             f  = self.foreground(1)
#             f.setColor(QColor("#0000FF"))
#             self.setForeground(1, f)
            # set custom delegates for value column
            if name in ['id', 'description','tags']:
                self.setData(1, EditorTypeRole, 'String')                
            elif name in ['startTime', 'stopTime']:
                self.setData(1, EditorTypeRole, 'Time')    
            elif name in ['videoname','imagename']:
                self.setData(1, EditorTypeRole, 'File')    
                self.setData(1, UserDataRole, '*.mp4;;*.avi;;*.*')    
                self.setData(1, CurrentDirDataRole, os.path.dirname(str(scene.filename)))   
            elif name == 'font':
                self.setData(1, EditorTypeRole, 'Font')    
            elif vType:
                self.setData(1, EditorTypeRole,  vType) 
                self.setData(1, UserDataRole, vUserData)    
            else:
                self.setData(1, EditorTypeRole, 'NotEditable')    
            # set name column not editable
            self.setData(0, EditorTypeRole, 'NotEditable')                    

