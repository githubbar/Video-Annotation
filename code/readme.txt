Annotation Tool: For annotating track time series over tracking video
Copyright: Alex Leykin @ CIL
Email: cil@indiana.edu
https://www.iub.edu/~cil
        
Developed with: 
    Python 3.6.8 x64bit
    
    Python modules: 
        PyQt5: http://www.riverbankcomputing.co.uk/software/pyqt/download    
        PyWin32: http://sourceforge.net/projects/pywin32/ (windows extensions, need it for system uptime)
        PyOpenGL: https://pypi.python.org/pypi/PyOpenGL (pip install from http://www.lfd.uci.edu/~gohlke/pythonlibs/)
        Pillow: https://www.lfd.uci.edu/~gohlke/pythonlibs/
        NumPy: http://www.lfd.uci.edu/~gohlke/pythonlibs/
        MatPlotLib: http://matplotlib.org/ (pip install from http://www.lfd.uci.edu/~gohlke/pythonlibs/)
        QDarkStyle: pip install qdarkstyle
    FFMPeg https://ffmpeg.zeranoe.com/builds/        
    PyDev: http://pydev.org/
    Cx-freeze: http://cx-freeze.sourceforge.net/ (to make executables)
    
    
    Eclipse: 
        Plugins: to compile .ui files with pyuic4.bat, http://marketplace.eclipse.org/content/path-tools
            follow description at https://stackoverflow.com/questions/5541024/eclipse-external-tool-for-qt-ui-to-py-with-pyuic
            
To remove directory from github:

git rm -r --cached FolderName
git commit -m "Removed folder from repository"
git push origin master            