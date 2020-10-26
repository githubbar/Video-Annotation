'''OpenGL extension SGIX.texture_scale_bias

This module customises the behaviour of the 
OpenGL.raw.GL.SGIX.texture_scale_bias to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension adds scale, bias, and clamp to [0, 1] operations to the 
	texture pipeline.
	These operations are applied to the filtered result of a texture lookup,
	before that result is used in the texture environment equations and
	before the texture color lookup table of SGI_texture_color_table, 
	if that extension exists.
	These operations are distinct from the scale, bias, and clamp operations
	that appear in the SGI_color_table extension, which are used to
	define a color lookup table.
	
	Scale and bias operations on texels can be used to better utilize the
	color resolution of a particular texture internal format (see EXT_texture).

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/texture_scale_bias.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.SGIX.texture_scale_bias import *
from OpenGL.raw.GL.SGIX.texture_scale_bias import _EXTENSION_NAME

def glInitTextureScaleBiasSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION