'''OpenGL extension NV.conditional_render

This module customises the behaviour of the 
OpenGL.raw.GL.NV.conditional_render to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides support for conditional rendering based on the
	results of an occlusion query.  This mechanism allows an application to
	potentially reduce the latency between the completion of an occlusion
	query and the rendering commands depending on its result.  It additionally
	allows the decision of whether to render to be made without application
	intervention.
	
	This extension defines two new functions, BeginConditionalRenderNV and
	EndConditionalRenderNV, between which rendering commands may be discarded
	based on the results of an occlusion query.  If the specified occlusion
	query returns a non-zero value, rendering commands between these calls are
	executed.  If the occlusion query returns a value of zero, all rendering
	commands between the calls are discarded.
	
	If the occlusion query results are not available when
	BeginConditionalRenderNV is executed, the <mode> parameter specifies
	whether the GL should wait for the query to complete or should simply
	render the subsequent geometry unconditionally.
	
	Additionally, the extension provides a set of "by region" modes, allowing
	for implementations that divide rendering work by screen regions to
	perform the conditional query test on a region-by-region basis without
	checking the query results from other regions.  Such a mode is useful for
	cases like split-frame SLI, where a frame is divided between multiple
	GPUs, each of which has its own occlusion query hardware.
	

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/NV/conditional_render.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL import _types
from OpenGL.raw.GL.NV.conditional_render import *
from OpenGL.raw.GL.NV.conditional_render import _EXTENSION_NAME

def glInitConditionalRenderNV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

### END AUTOGENERATED SECTION