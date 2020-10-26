'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_IMG_user_clip_plane'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_IMG_user_clip_plane')
GL_CLIP_PLANE0_IMG=_C('GL_CLIP_PLANE0_IMG',0x3000)
GL_CLIP_PLANE1_IMG=_C('GL_CLIP_PLANE1_IMG',0x3001)
GL_CLIP_PLANE2_IMG=_C('GL_CLIP_PLANE2_IMG',0x3002)
GL_CLIP_PLANE3_IMG=_C('GL_CLIP_PLANE3_IMG',0x3003)
GL_CLIP_PLANE4_IMG=_C('GL_CLIP_PLANE4_IMG',0x3004)
GL_CLIP_PLANE5_IMG=_C('GL_CLIP_PLANE5_IMG',0x3005)
GL_MAX_CLIP_PLANES_IMG=_C('GL_MAX_CLIP_PLANES_IMG',0x0D32)
@_f
@_p.types(None,_cs.GLenum,arrays.GLfloatArray)
def glClipPlanefIMG(p,eqn):pass
@_f
@_p.types(None,_cs.GLenum,ctypes.POINTER(_cs.GLfixed))
def glClipPlanexIMG(p,eqn):pass
