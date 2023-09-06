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
""" 
Build script for cxFreeze library

add ""from PyQt5 import QtNetwork"" to Ui_window.py

Run this file with "build" command line argument to build an exe. Run as administrator to access dll's in system dir.
egg includes (e.g. elixir library) must by unzipped for cx_freeze to find them
"""

from cx_Freeze import setup, Executable
import os, glob
import PyQt5
from main import Main

Target_1 = Executable(
    # what to build
    script = "main.py",
    initScript = None,
    base = 'Win32GUI', # comment this out to see consol to debug
    targetName = "VideoAnnotationTool.exe",
#     compress = True,
#     copyDependentFiles = True,
#     appendScriptToExe = False,
#     appendScriptToLibrary = False, 
    icon = "icons\icon.ico"
    )
    
include_files = ["icons", "palettes","mydark.stylesheet", \
                 'window.ui', 'choicesdialog.ui', 'filterdialog.ui', 'imagepopup.ui', 'project.ui', 'variabledialog.ui']

app = PyQt5.QtWidgets.QApplication([])

# Generate help and add help files and sqlite dll
import subprocess
if Main.READ_ONLY:
    subprocess.call(['qcollectiongenerator', 'help_lite/help.qhcp', '-o', 'help_lite/help.qhc'], shell=True)
    include_files.append(('help_lite', 'help'))
else:
    subprocess.call(['qcollectiongenerator', 'help/help.qhcp', '-o', 'help/help.qhc'], shell=True)
    include_files.append(('help', 'help'))

# Copy necessary dll's from the PyQt plugins directory
include_files.append((os.path.join(str(PyQt5.QtCore.QLibraryInfo.location(PyQt5.QtCore.QLibraryInfo.PluginsPath)), 'sqldrivers', 'qsqlite.dll'), 'plugins/sqldrivers/qsqlite.dll'))  # help stores in sql lite format
include_files.append((os.path.join(str(PyQt5.QtCore.QLibraryInfo.location(PyQt5.QtCore.QLibraryInfo.PluginsPath)), 'imageformats'), 'plugins/imageformats'))

# Copy VLC dll's 
vlcDir = str("c:/Program Files/VideoLAN/VLC")
for f in glob.glob(os.path.join(vlcDir,'*.dll')):
    include_files.append((f, os.path.basename(f)))
include_files.append((os.path.join(vlcDir, 'plugins'), 'plugins'))

# Copy all .py files
codeDir = os.path.dirname(__file__)
for f in glob.glob(os.path.join(codeDir,'*.py')):
    include_files.append((f, os.path.basename(f)))
      
# Copy qt.conf from (without it the icons don't show)
include_files.append('qt.conf')
  
# Copy FFMPEG dll's
ffmpegDir = str("c:/Program Files/ffmpeg")
include_files.append((os.path.join(ffmpegDir, 'bin'), '.'))


setup(
        name = "VideoAnnotationTool",
        version = "1.0."+str(Main.BUILD_NUMBER),
        description = "Video Annotation Tool",
        author = "author",
        options = {"build_exe": {
            "build_exe": "../release/Video Annotation Tool",
            "excludes":  ["tcl","tk","Tkinter"],  
            "includes":  ['qdarkstyle', 'unittest', 'numpy.core._methods', 'numpy.lib.format'],
            "include_files": include_files
            } 
       },
      
       executables = [Target_1]
    )

print('Successfully finished!')
