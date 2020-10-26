""" 
Build script for cxFreeze library

add ""from PyQt4 import QtNetwork"" to Ui_window.py

Run this file with "build" command line argument to build an exe. Run as administrator to access dll's in system dir.
egg includes (e.g. elixir library) must by unzipped for cx_freeze to find them
"""

from cx_Freeze import setup, Executable
import sys
import os
import glob
import PyQt4.Qt as qt
from main import Main

Target_1 = Executable(
    # what to build
    script = "main.py",
    initScript = None,
    base = 'Win32GUI',
    targetName = "VideoAnnotationTool.exe",
#     compress = True,
#     copyDependentFiles = True,
#     appendScriptToExe = False,
#     appendScriptToLibrary = False, 
    icon = "icons\icon.ico"
    )
    
    
include_files = ["icons", "palettes","mydark.stylesheet"]

app = qt.QApplication([])

# Generate help and add help files and sqlite dll
import subprocess
if Main.READ_ONLY:
    subprocess.call(['qcollectiongenerator', 'help_lite/help.qhcp', '-o', 'help_lite/help.qhc'], shell=True)
    include_files.append(('help_lite', 'help'))
else:
    subprocess.call(['qcollectiongenerator', 'help/help.qhcp', '-o', 'help/help.qhc'], shell=True)
    include_files.append(('help', 'help'))

# Copy necessary dll's from the PyQt plugins directory
include_files.append((os.path.join(str(qt.QLibraryInfo.location(qt.QLibraryInfo.PluginsPath)), 'sqldrivers', 'qsqlite4.dll'), 'plugins/sqldrivers/qsqlite4.dll'))  # help stores in sql lite format
include_files.append((os.path.join(str(qt.QLibraryInfo.location(qt.QLibraryInfo.PluginsPath)), 'imageformats'), 'plugins/imageformats'))
 

# Copy OpenGL files
# include_files.append(("c:/Python27/Lib/site-packages/PyOpenGL-3.1.0b2-py2.7-win32.egg/OpenGL", "OpenGL"))
  
# Copy VLC dll's 
vlcDir = str("c:/Program Files (x86)/VideoLAN/VLC")
for f in glob.glob(os.path.join(vlcDir,'*.dll')):
    include_files.append((f, os.path.basename(f)))
include_files.append((os.path.join(vlcDir, 'plugins'), 'plugins'))
  
# Copy qt.conf from (without it the icons don't show)
include_files.append('qt.conf')
  
# Copy FFMPEG dll's
ffmpegDir = str("c:/Program Files (x86)/ffmpeg")
include_files.append((os.path.join(ffmpegDir, 'bin'), '.'))

#"ctypes", "OpenGL", "OpenGL.platform", "OpenGL.GLU", "OpenGL.GL", "OpenGL.GLUT", "OpenGL.GL.shaders", "OpenGL.GL.EXT", "OpenGL.GL.ARB"
# OpenGL.arrays.ctypesparameters
# , "OpenGL", "OpenGL.platform", "OpenGL.GLU", "OpenGL.GL", "OpenGL.GLUT", "OpenGL.GL.shaders", "OpenGL.GL.EXT", "OpenGL.GL.ARB", "OpenGL.platform.win32","OpenGL.platform.win32", "OpenGL.arrays.ctypesarrays", "OpenGL.arrays.numpymodule","OpenGL.arrays.lists","OpenGL.arrays.numbers","OpenGL.arrays.strings" 
setup(
        name = "VideoAnnotationTool",
        version = "1.0."+str(Main.BUILD_NUMBER),
        description = "Video Annotation Tool",
        author = "author",
        options = {"build_exe": {
            "excludes":  ["tcl","tk","Tkinter", "collections.abc"],  
            "includes":  ['qdarkstyle', 'unittest', 'numpy.core._methods', 'numpy.lib.format', 'OpenGL.GLU.glustruct'],
            "include_files": include_files,
            "packages": ["OpenGL.arrays", "OpenGL.GL.ARB"]
            } 
       },
       
       executables = [Target_1]
    )

