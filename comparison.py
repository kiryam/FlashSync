import os
import glob
import string

sourcepath = 'C:\\Users\\kiryam\\Documents\\My Dropbox\\Python\\flash_sync'
distpath = 'C:\\Users\\kiryam\\Documents\\My Dropbox\\Python\\flash_sync\\dist'

sourcelist = []
    
for root, dirs, files in os.walk(sourcepath):
    for name in files:
        pathfile = os.path.join(root, name)
        
        #ignore python extensions
        pathfile = string.replace(pathfile, '.pyo', '') 
        pathfile = string.replace(pathfile, '.pyc', '')
        pathfile = string.replace(pathfile, '.py', '')
        #remove root path
        pathfile = string.replace(pathfile, sourcepath, '') 
        sourcelist.append(pathfile)

distlist = []
    
for root, dirs, files in os.walk(distpath):
    for name in files:
        pathfile = os.path.join(root, name)
        
        #ignore python extensions
        pathfile = string.replace(pathfile, '.pyo', '') 
        pathfile = string.replace(pathfile, '.pyc', '')
        pathfile = string.replace(pathfile, '.py', '')
        
        #remove root path      
        pathfile = string.replace(pathfile, distpath, '')   
        distlist.append(pathfile)

sourceset = set(sourcelist)
distset = set(distlist)

missing = sourceset - distset        

for (files) in sorted(missing):
    print files
