'''OpenGL extension EXT.instanced_arrays

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.instanced_arrays to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/instanced_arrays.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.EXT.instanced_arrays import *
from OpenGL.raw.GL.EXT.instanced_arrays import _EXTENSION_NAME

def glInitInstancedArraysEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION