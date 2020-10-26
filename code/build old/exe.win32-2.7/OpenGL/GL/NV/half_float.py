'''OpenGL extension NV.half_float

This module customises the behaviour of the 
OpenGL.raw.GL.NV.half_float to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension introduces a new storage format and data type for
	half-precision (16-bit) floating-point quantities.  The floating-point
	format is very similar to the IEEE single-precision floating-point
	standard, except that it has only 5 exponent bits and 10 mantissa bits.
	Half-precision floats are smaller than full precision floats and provide a
	larger dynamic range than similarly-sized normalized scalar data types.
	
	This extension allows applications to use half-precision floating point
	data when specifying vertices or pixel data.  It adds new commands to
	specify vertex attributes using the new data type, and extends the
	existing vertex array and image specification commands to accept the new
	data type.
	
	This storage format is also used to represent 16-bit components in the
	floating-point frame buffers, as defined in the NV_float_buffer extension.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/half_float.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.NV.half_float import *
from OpenGL.raw.GL.NV.half_float import _EXTENSION_NAME

def glInitHalfFloatNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION