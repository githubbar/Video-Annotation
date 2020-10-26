'''OpenGL extension OES.stencil_wrap

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.stencil_wrap to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/stencil_wrap.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES1 import _types
from OpenGL.raw.GLES1.OES.stencil_wrap import *
from OpenGL.raw.GLES1.OES.stencil_wrap import _EXTENSION_NAME

def glInitStencilWrapOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION