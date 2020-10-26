'''OpenGL extension OES.blend_func_separate

This module customises the behaviour of the 
OpenGL.raw.GLES1.OES.blend_func_separate to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/OES/blend_func_separate.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES1 import _types
from OpenGL.raw.GLES1.OES.blend_func_separate import *
from OpenGL.raw.GLES1.OES.blend_func_separate import _EXTENSION_NAME

def glInitBlendFuncSeparateOES():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION