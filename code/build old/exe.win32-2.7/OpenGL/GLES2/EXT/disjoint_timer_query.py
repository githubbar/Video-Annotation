'''OpenGL extension EXT.disjoint_timer_query

This module customises the behaviour of the 
OpenGL.raw.GLES2.EXT.disjoint_timer_query to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/disjoint_timer_query.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper

import ctypes
from OpenGL.raw.GLES2 import _types
from OpenGL.raw.GLES2.EXT.disjoint_timer_query import *
from OpenGL.raw.GLES2.EXT.disjoint_timer_query import _EXTENSION_NAME

def glInitDisjointTimerQueryEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION