from distutils.core import setup
from string import join
import py2exe, sys, os


sys.argv.append('py2exe')

#mfcdir = 'C:\\Python26\\Lib\\site-packages\\pythonwin\\'
#mfcfiles = [join(mfcdir, i) for i in ["Microsoft.VC90.MFC.manifest"]]

data_files = ['favicon.ico', 'App.ico', 'configobj.pyc', 'sync.ini']

setup(
    data_files = data_files,
    windows=[{"script":"flashsync.py"}], 
    options={"py2exe": {"includes":["sip"],'dll_excludes': [ "mswsock.dll", "powrprof.dll" ], 'bundle_files': 1}},
    zipfile = None,
)
