'''OpenGL extension OES.stencil1

This module customises the behaviour of the 
OpenGL.raw.GL.OES.stencil1 to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/stencil1.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.OES.stencil1 import *
from OpenGL.raw.GL.OES.stencil1 import _EXTENSION_NAME

def glInitStencil1OES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION