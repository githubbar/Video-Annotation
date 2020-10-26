'''OpenGL extension QCOM.writeonly_rendering

This module customises the behaviour of the 
OpenGL.raw.GLES1.QCOM.writeonly_rendering to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/QCOM/writeonly_rendering.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES1 import _types
from OpenGL.raw.GLES1.QCOM.writeonly_rendering import *
from OpenGL.raw.GLES1.QCOM.writeonly_rendering import _EXTENSION_NAME

def glInitWriteonlyRenderingQCOM():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION