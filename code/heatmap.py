# -*- coding: utf-8 -*-
"""
Displays a heatmap
Adapted from:
PyHeat http://github.com/amccollum/pyheat
Andrew McCollum <amccollum@gmail.com>
"""
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import io, os, struct, sys
from PIL import Image
import logging
import numpy as Numeric
from textwrap import *
from ctypes import *
import platform
import OpenGL.platform.win32
import OpenGL.arrays.formathandler
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GL.ARB.multitexture import *



class HeatMap(object):
    width = None
    height = None
    fbo = None
    texture = None
    palette = None
    paletteFile = 'palettes/jet.png'
    
    def __init__(self, left, right, bottom, top,  paletteFile):
#        p= Image.open(paletteFile)
#        a = Numeric.array(p) 
#        for i, d in enumerate(a):
##            d[0][0] = a[255-i][0][0]
##            d[0][1] = a[255-i][0][1]
##            d[0][2] = a[255-i][0][2]
##            print d[0][3]
#            d[0][3] = 255-i
#        p = Image.fromarray(a)
#        p.save(paletteFile)
#        sys.exit(0)        
        self.paletteFile = paletteFile
        if bottom > top:
            (bottom, top) = (top, bottom)
            self.invert_y = True
        else:
            self.invert_y = False
            
        if left > right:
            (left, right) = (right, left)
            self.invert_x = True
        else:
            self.invert_x = False
            
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        
        # Check if we need to reinitialize the OpenGL state
        if (self.width != abs(self.right - self.left) or
            self.height != abs(self.top - self.bottom) or
            None in (self.fbo, self.texture, self.palette)):
            self.prepare(abs(right - left), abs(top - bottom))
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        OpenGL.GLU.gluOrtho2D(left, right, bottom, top)
        self._clear_framebuffer()
       
    def cleanup(self):
        if self.fbo: glDeleteFramebuffersEXT(self.fbo)
        if self.texture: glDeleteTextures(self.texture)
        if self.palette: glDeleteTextures(self.palette)
        self.fbo = self.texture = self.palette = None
    
    def offscreenDisplay(self):
        # Clear the color and depth buffers
        pass
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
        # ... render stuff in here ...
        # It will go to an off-screen frame buffer.
    
    def prepare(self, width, height):
        self.cleanup()

        self.width = width
        self.height = height
        
        # Glut Init
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowPosition(2*self.width, 10*self.height)
        glutInitWindowSize(self.width, self.height)
        # BUG: creates a black GL window since update to new PyOpenGL
        self.win = glutCreateWindow("")
        glutDisplayFunc(self.offscreenDisplay)
        # Render Flags
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_1D)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glEnableClientState(GL_VERTEX_ARRAY)
        self._compile_programs()
        self._load_palette()
        self._create_framebuffer()
        

    def _load_palette(self):
        image = Image.open((self.paletteFile))
        self.palette = glGenTextures(1)

        glActiveTextureARB(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_1D, self.palette)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA,
                     image.size[1],
                     0, GL_RGBA, GL_UNSIGNED_BYTE,
                     image.tobytes('raw', 'RGBA', 0, -1))
                     
        glTexParameter(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_CLAMP)


    def _create_framebuffer(self):
        self.texture = glGenTextures(1)
        self.fbo = glGenFramebuffersEXT(1)
        # logging.debug("fbo = {0}".format(self.fbo))

        glActiveTextureARB(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                     self.width, self.height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, None)
#        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F,
#                     self.width, self.height, 0, GL_RGBA,
#                     GL_FLOAT, None)
          
          
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT,
                                  GL_TEXTURE_2D, self.texture, 0)

        status = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)
        assert status == GL_FRAMEBUFFER_COMPLETE_EXT, status
            
            
    def _clear_framebuffer(self):
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
        glClear(GL_COLOR_BUFFER_BIT)

    def _compile_programs(self):
        # Shader program to transform color into the proper palette based on the alpha channel
        logging.info("compiling color transform shader")

        self.color_transform_program = compileProgram(
            compileShader("""
                void main() {gl_Position = ftransform();
                }
            """, GL_VERTEX_SHADER), 
            compileShader("""
                uniform float alpha;
                uniform sampler1D palette;
                uniform sampler2D framebuffer;
                uniform vec2 windowSize;
   
                void main() {
                    //gl_FragColor.a = clamp(gl_FragColor.a, 0.0, 1.0);
                    //gl_FragColor.a = normalize(gl_FragColor.a);
                    //gl_FragColor.a = 1.0 - gl_FragColor.a;
                    gl_FragColor.rgba = texture(palette, texture(framebuffer,  gl_FragCoord.xy / windowSize).a).rgba;
                    gl_FragColor.a *= alpha;
                }
            """, GL_FRAGMENT_SHADER), validate=False)
        #  NOTE: pass VALIDATE=False parameter to compileProgram                      
        # Shader program to place heat points
        logging.info("compiling heat point shader")
        self.faded_points_program = compileProgram(
            compileShader("""
                uniform float r;
                attribute vec2 point;
                attribute float scale;
                varying vec2 center;
                varying float hscale;

 
                void main() {
                    gl_Position = ftransform();
                    center = point;
                    hscale = scale;
                }
            """, GL_VERTEX_SHADER),
            compileShader("""
                uniform float r;
                varying vec2 center;
                varying float hscale;
 
                void main() {
                    float d = distance(gl_FragCoord.xy, center);
                    if (d > r) discard;
                 
                    gl_FragColor.rgb = vec3(1.0, 1.0, 1.0);
                    //gl_FragColor.a = (0.5 + cos(d * 3.14159265 / r) * 0.5) * 0.25;
                    gl_FragColor.a = (0.5 + cos(d * 3.14159265 / r) * 0.5) * hscale;
                    // Alternate fading algorithms
                    //gl_FragColor.a = (1.0 - (log(1.1+d) / log(1.1+r)));
                    //gl_FragColor.a = (1.0 - (pow(d, 0.5) / pow(r, 0.5)));
                    //gl_FragColor.a = (1.0 - ((d*d) / (r*r))) / 2.0;
                    //gl_FragColor.a = (1.0 - (d / r)) / 2.0;
                     
                    // Clamp the alpha to the range [0.0, 1.0]
                    // gl_FragColor.a = clamp(gl_FragColor.a, 0.0, 1.0);
                }
            """, GL_FRAGMENT_SHADER))
    
    def add_points(self, points, radius, heatScale):
        # Render all points with the specified radius
        glUseProgram(self.faded_points_program)
        glUniform1f(glGetUniformLocation(self.faded_points_program, 'r'), radius)

        point_attrib_location = glGetAttribLocation(self.faded_points_program, 'point')
        glEnableVertexAttribArray(point_attrib_location)
        glVertexAttribPointer(point_attrib_location, 2, GL_FLOAT, False, 0,
                              struct.pack("ff" * 4 * len(points),
                                          *(val for (x, y) in points
                                                for val in (x - self.left, y - self.bottom) * 4)))
        

        heatscale_attrib_location = glGetAttribLocation(self.faded_points_program, 'scale')        
        glEnableVertexAttribArray(heatscale_attrib_location)
        glVertexAttribPointer(heatscale_attrib_location, 1, GL_FLOAT, False, 0,
                              struct.pack("f" *  len(heatScale),
                                          *(val for val in heatScale)))
        
        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
        glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
        vertices = [point for (x, y) in points
                          for point in ((x + radius, y + radius), (x - radius, y + radius),
                                        (x - radius, y - radius), (x + radius, y - radius))]
        glVertexPointerd(vertices)
        glDrawArrays(GL_QUADS, 0, len(vertices))
        glFlush()
        
        glDisableVertexAttribArray(point_attrib_location)


#     def normalize(self, alphaMax = None):
#         # Render all points with the specified radius
#         glUseProgram(self.normalize_program)
#         glUniform1f(glGetUniformLocation(self.color_transform_program, 'alpha'), alpha)
# 
#         glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
#         glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
#         
#         vertices = [point for (x, y) in points
#                           for point in ((x + radius, y + radius), (x - radius, y + radius),
#                                         (x - radius, y - radius), (x + radius, y - radius))]
#         glVertexPointerd(vertices)
#         glDrawArrays(GL_QUADS, 0, len(vertices))
#         glFlush()
#         
#         glDisableVertexAttribArray(point_attrib_location)
        
    def transform_color(self, alpha):
        # Transform the color into the proper palette
        glUseProgram(self.color_transform_program)
        glUniform1f(glGetUniformLocation(self.color_transform_program, 'alpha'), alpha)
        glUniform1i(glGetUniformLocation(self.color_transform_program, 'palette'), 0)
        glUniform1i(glGetUniformLocation(self.color_transform_program, 'framebuffer'), 1)
        glUniform2f(glGetUniformLocation(self.color_transform_program, 'windowSize'), self.width, self.height)
                    
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, self.fbo)
        glBlendFunc(GL_ONE, GL_ZERO)

        vertices = [(self.left, self.bottom), (self.right, self.bottom),
                    (self.right, self.top), (self.left, self.top)]                    
        glVertexPointerd(vertices)
        glDrawArrays(GL_QUADS, 0, len(vertices))
        glFlush()
   
    def get_min_max_heat(self):
        glActiveTextureARB(GL_TEXTURE1)
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE)
        im = Image.frombuffer('RGBA', (self.width, self.height), data, 'raw', 'RGBA', 0, (1 if self.invert_y else -1))
        return im.getextrema()[3]
           
    def get_image(self):
        # Get the data from the heatmap framebuffer and convert it into a PIL image
        glActiveTextureARB(GL_TEXTURE1)
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE)
        im = Image.frombuffer('RGBA', (self.width, self.height), data, 'raw', 'RGBA', 0, (1 if self.invert_y else -1))
        glutDestroyWindow(self.win)
        if self.invert_x:
            im.transpose(Image.FLIP_LEFT_RIGHT)
        return im

    def get_image_buffer(self):
        # Get the data from the heatmap framebuffer
        glActiveTextureARB(GL_TEXTURE1)
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE)
        glutDestroyWindow(self.win)
        return data


    
