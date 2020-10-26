import sys, zipimport
importer = zipimport.zipimporter('build\exe.win32-2.7\VideoAnnotationTool.zip')
moduleName = '__main__'
code = importer.get_code(moduleName)
exec code 
