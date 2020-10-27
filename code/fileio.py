'''
Created on Jul 11, 2017

@author: oleykin
'''

import logging
import os, sys,time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import menu, buttonevents, searchwidget


class QDataExportDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)

        box = QVBoxLayout()

        self.setFixedSize(self.width() + 250, self.height())
        self.checkExportDistDuration = QCheckBox("Export total distance and duration", self)
        self.checkExportAOIDistDuration = QCheckBox("Export AOI distance and duration", self)
        box.addWidget(self.checkExportDistDuration)
        box.addWidget(self.checkExportAOIDistDuration)
        box.addStretch()
        self.layout().addLayout(box, 1, 3, 1, 1)
        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.onFileSelected)
        self.filesSelected.connect(self.onFilesSelected)

        self._fileSelected = None
        self._filesSelected = None
        #             TODO: add checkboxes


    def onChange(self, path):
        pass
        
    def onFileSelected(self, file):
        self._fileSelected = file

    def onFilesSelected(self, files):
        self._filesSelected = files

    def getFileSelected(self):
        return self._fileSelected

    def getFilesSelected(self):
        return self._filesSelected
    
class fileio(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
        
    @staticmethod      
    def generateFixationSnapshots(mainwindow, filename):
        # read TSV export from Tobii in format:
        # Participant name    Recording name    Recording duration    Recording timestamp    Gaze event duration    Eye movement type index    Fixation point X    Fixation point Y
            
#         thresh, ok = QInputDialog.getDouble(mainwindow, 'Input Dialog', 'Minimal fixation duration (sec):', 1.0, 0.1, 10)        
#         if not ok:
#             return
        
        thresh = 1.0
        import csv
        reader = csv.reader(open(filename, 'rb'), delimiter='\t')
        header = next(reader)
        result = []
        seen = {}
        oldid = -1
#         outDir = QFileDialog.getExistingDirectory(mainwindow, "Choose Folder to Export To", os.getcwdu())
#         if not outDir:
#             return      
        
        outDir = 'E:/Box Sync/Video Annotation/Giant Eagle - Washington/screenshots'
#         threading.Thread(target=self.doExportData, name="exportDataThread", args=(outFileName,)).start()
        for line in reader:
            if line[7] and int(line[4]) > thresh * 1000:
                id = int(line[0])
                idx = int(line[5])
                if (id, idx) in seen: continue
                seen[(id, idx)] = 1
                if id != oldid:
                    # find records with this id and get filename
                    for i in range(mainwindow.items.rowCount()):
                        item = mainwindow.items.item(i, 0).g
                        if item.id.toInt()[0] == id:
                            videoname = item.videoname
                            break
                    # load video if different id
                    mainwindow.loadVideo(videoname)
                    mainwindow.mediaPlayer.play()
                    time.sleep(1.0)
                    mainwindow.mediaPlayer.pause()
                    oldid = id
                    
                t1 = int(line[3])
                t2 = t1 + int(line[4])
                mainwindow.mediaPlayer.set_time(max(t1, 0))
                # create sub-folder for id, if doesn't yet exist
                subDir = os.path.join(str(outDir), "{0:0>3}".format(id))
                if not os.path.exists(subDir):
                    os.makedirs(subDir)
                outFileName = os.path.join(subDir, str('image ' 
                                                            + ' from ' + QTime().addMSecs(t1).toString('hh-mm-ss') 
                                                            + ' to ' + QTime().addMSecs(t2).toString('hh-mm-ss') + '.png'))
                blah = vlc.libvlc_video_take_snapshot(mainwindow.mediaPlayer, 0, outFileName, 0, 0)
                
                    
