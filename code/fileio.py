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
import os, sys, time, vlc
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QFileDialog, QVBoxLayout, QCheckBox
import logging

def findFataFile(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    logging.debug(f'Data path is {datadir}')
    return os.path.join(datadir, filename)

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
        reader = csv.reader(open(filename), delimiter='\t')
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
                    for i in range(mainwindow.items.count()):
                        itemId = mainwindow.items.item(i).text() 
                        item = mainwindow.graphicsView.scene.findPath(itemId)
                        if int(item.id[0]) == id:
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
                                                            + ' from ' + QTime(0,0).addMSecs(t1).toString('hh-mm-ss') 
                                                            + ' to ' + QTime(0,0).addMSecs(t2).toString('hh-mm-ss') + '.png'))
                blah = vlc.libvlc_video_take_snapshot(mainwindow.mediaPlayer, 0, outFileName, 0, 0)
                
                    
