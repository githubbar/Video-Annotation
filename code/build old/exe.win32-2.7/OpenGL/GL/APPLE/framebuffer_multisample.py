'''OpenGL extension APPLE.framebuffer_multisample

This module customises the behaviour of the 
OpenGL.raw.GL.APPLE.framebuffer_multisample to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/APPLE/framebuffer_multisample.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.APPLE.framebuffer_multisample import *
from OpenGL.raw.GL.APPLE.framebuffer_multisample import _EXTENSION_NAME

def glInitFramebufferMultisampleAPPLE():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION