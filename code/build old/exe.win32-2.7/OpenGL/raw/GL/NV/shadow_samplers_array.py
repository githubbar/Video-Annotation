'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_NV_shadow_samplers_array'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_NV_shadow_samplers_array')
GL_SAMPLER_2D_ARRAY_SHADOW_NV=_C('GL_SAMPLER_2D_ARRAY_SHADOW_NV',0x8DC4)

