'''OpenGL extension EXT.discard_framebuffer

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.discard_framebuffer to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/discard_framebuffer.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.EXT.discard_framebuffer import *
from OpenGL.raw.GL.EXT.discard_framebuffer import _EXTENSION_NAME

def glInitDiscardFramebufferEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION