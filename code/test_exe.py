"""
====================================================================================
Video Annotation Tool
Copyright (C) 2023 Alex Leykin @ CIL
Email: cil@indiana.edu
http://cil.iu.edu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
            
====================================================================================
"""
import sys, zipimport
importer = zipimport.zipimporter('build\exe.win32-2.7\VideoAnnotationTool.zip')
moduleName = '__main__'
code = importer.get_code(moduleName)
exec code 
