'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ANGLE_framebuffer_multisample'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_ANGLE_framebuffer_multisample')
GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_ANGLE=_C('GL_FRAMEBUFFER_INCOMPLETE_MULTISAMPLE_ANGLE',0x8D56)
GL_MAX_SAMPLES_ANGLE=_C('GL_MAX_SAMPLES_ANGLE',0x8D57)
GL_RENDERBUFFER_SAMPLES_ANGLE=_C('GL_RENDERBUFFER_SAMPLES_ANGLE',0x8CAB)
@_f
@_p.types(None,_cs.GLenum,_cs.GLsizei,_cs.GLenum,_cs.GLsizei,_cs.GLsizei)
def glRenderbufferStorageMultisampleANGLE(target,samples,internalformat,width,height):pass
