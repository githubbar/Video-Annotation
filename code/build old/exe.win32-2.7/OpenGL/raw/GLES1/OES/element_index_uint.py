'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES1 import _types as _cs
# End users want this...
from OpenGL.raw.GLES1._types import *
from OpenGL.raw.GLES1 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES1_OES_element_index_uint'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES1,'GLES1_OES_element_index_uint',error_checker=_errors._error_checker)
GL_UNSIGNED_INT=_C('GL_UNSIGNED_INT',0x1405)
