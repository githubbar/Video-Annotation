'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_read_format_bgra'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_EXT_read_format_bgra')
GL_BGRA_EXT=_C('GL_BGRA_EXT',0x80E1)
GL_UNSIGNED_SHORT_1_5_5_5_REV_EXT=_C('GL_UNSIGNED_SHORT_1_5_5_5_REV_EXT',0x8366)
GL_UNSIGNED_SHORT_4_4_4_4_REV_EXT=_C('GL_UNSIGNED_SHORT_4_4_4_4_REV_EXT',0x8365)

