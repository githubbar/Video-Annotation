'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_OES_texture_compression_astc'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_OES_texture_compression_astc')
GL_COMPRESSED_RGBA_ASTC_10x10_KHR=_C('GL_COMPRESSED_RGBA_ASTC_10x10_KHR',0x93BB)
GL_COMPRESSED_RGBA_ASTC_10x5_KHR=_C('GL_COMPRESSED_RGBA_ASTC_10x5_KHR',0x93B8)
GL_COMPRESSED_RGBA_ASTC_10x6_KHR=_C('GL_COMPRESSED_RGBA_ASTC_10x6_KHR',0x93B9)
GL_COMPRESSED_RGBA_ASTC_10x8_KHR=_C('GL_COMPRESSED_RGBA_ASTC_10x8_KHR',0x93BA)
GL_COMPRESSED_RGBA_ASTC_12x10_KHR=_C('GL_COMPRESSED_RGBA_ASTC_12x10_KHR',0x93BC)
GL_COMPRESSED_RGBA_ASTC_12x12_KHR=_C('GL_COMPRESSED_RGBA_ASTC_12x12_KHR',0x93BD)
GL_COMPRESSED_RGBA_ASTC_3x3x3_OES=_C('GL_COMPRESSED_RGBA_ASTC_3x3x3_OES',0x93C0)
GL_COMPRESSED_RGBA_ASTC_4x3x3_OES=_C('GL_COMPRESSED_RGBA_ASTC_4x3x3_OES',0x93C1)
GL_COMPRESSED_RGBA_ASTC_4x4_KHR=_C('GL_COMPRESSED_RGBA_ASTC_4x4_KHR',0x93B0)
GL_COMPRESSED_RGBA_ASTC_4x4x3_OES=_C('GL_COMPRESSED_RGBA_ASTC_4x4x3_OES',0x93C2)
GL_COMPRESSED_RGBA_ASTC_4x4x4_OES=_C('GL_COMPRESSED_RGBA_ASTC_4x4x4_OES',0x93C3)
GL_COMPRESSED_RGBA_ASTC_5x4_KHR=_C('GL_COMPRESSED_RGBA_ASTC_5x4_KHR',0x93B1)
GL_COMPRESSED_RGBA_ASTC_5x4x4_OES=_C('GL_COMPRESSED_RGBA_ASTC_5x4x4_OES',0x93C4)
GL_COMPRESSED_RGBA_ASTC_5x5_KHR=_C('GL_COMPRESSED_RGBA_ASTC_5x5_KHR',0x93B2)
GL_COMPRESSED_RGBA_ASTC_5x5x4_OES=_C('GL_COMPRESSED_RGBA_ASTC_5x5x4_OES',0x93C5)
GL_COMPRESSED_RGBA_ASTC_5x5x5_OES=_C('GL_COMPRESSED_RGBA_ASTC_5x5x5_OES',0x93C6)
GL_COMPRESSED_RGBA_ASTC_6x5_KHR=_C('GL_COMPRESSED_RGBA_ASTC_6x5_KHR',0x93B3)
GL_COMPRESSED_RGBA_ASTC_6x5x5_OES=_C('GL_COMPRESSED_RGBA_ASTC_6x5x5_OES',0x93C7)
GL_COMPRESSED_RGBA_ASTC_6x6_KHR=_C('GL_COMPRESSED_RGBA_ASTC_6x6_KHR',0x93B4)
GL_COMPRESSED_RGBA_ASTC_6x6x5_OES=_C('GL_COMPRESSED_RGBA_ASTC_6x6x5_OES',0x93C8)
GL_COMPRESSED_RGBA_ASTC_6x6x6_OES=_C('GL_COMPRESSED_RGBA_ASTC_6x6x6_OES',0x93C9)
GL_COMPRESSED_RGBA_ASTC_8x5_KHR=_C('GL_COMPRESSED_RGBA_ASTC_8x5_KHR',0x93B5)
GL_COMPRESSED_RGBA_ASTC_8x6_KHR=_C('GL_COMPRESSED_RGBA_ASTC_8x6_KHR',0x93B6)
GL_COMPRESSED_RGBA_ASTC_8x8_KHR=_C('GL_COMPRESSED_RGBA_ASTC_8x8_KHR',0x93B7)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR',0x93DB)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR',0x93D8)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR',0x93D9)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR',0x93DA)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR',0x93DC)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR',0x93DD)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_3x3x3_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_3x3x3_OES',0x93E0)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x3x3_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x3x3_OES',0x93E1)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR',0x93D0)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x3_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x3_OES',0x93E2)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x4_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_4x4x4_OES',0x93E3)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR',0x93D1)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4x4_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x4x4_OES',0x93E4)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR',0x93D2)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x4_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x4_OES',0x93E5)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x5_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_5x5x5_OES',0x93E6)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR',0x93D3)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5x5_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x5x5_OES',0x93E7)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR',0x93D4)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x5_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x5_OES',0x93E8)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x6_OES=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_6x6x6_OES',0x93E9)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR',0x93D5)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR',0x93D6)
GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR=_C('GL_COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR',0x93D7)

