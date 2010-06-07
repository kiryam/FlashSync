import os
import shutil
from configobj import ConfigObj
import threading
import hashlib


class sync(threading.Thread):
    drivepath = 'E:\\'
    musicdir = 'music'
    sourcepath = ''
    exts = 'mp3'
    checksize = 100

    
    def __init__(self, drivepath):
        if drivepath:
            self.drivepath = drivepath
        self.loadconfig()
        
        threading.Thread.__init__(self)
        
    def run(self):
        global status
        status = 'sync'
        print 'Syncing drivepath: '+self.drivepath;
        self.sync_folder(self.sourcepath,self.drivepath+self.musicdir)
        status = 'sync done'
        print 'Syncing '+self.drivepath+' done.';

    def loadconfig(self):
        config = ConfigObj(self.drivepath+'/sync.ini')
        for item in config.iterkeys():
            setattr(self, item, config[item])

    def getListFolders(self, path):
        files = os.listdir(path)
        ret = []
        for f in files:
            if f.find('.') != -1: pass
            else:
                ret.append(f)
        return ret

    def getNeedFilesList(self, path):
        files = os.listdir(path)
        ret = []
        for f in files:
            if f.find('.') == -1: pass
            else:
                for ext in self.exts:
                    if( f.find('.'+ext, (-1*len(ext))-1) != -1 ):                        
                         ret.append(f)
        return ret

    def getMagikMd5ForFile(self, path):
        f = open(path, 'r');
        f.seek(-1*int(self.checksize), 2)
        data = f.read(int(self.checksize))
        #print 'Readed:'+data
        f.close()
        m = hashlib.md5();
        m.update(data)
        md5 = m.digest()
        #print 'md5: '+md5
        return md5

    def sync_folder(self, original, withfolder):
        sourcefolderlist = self.getListFolders(original)
        flashfolderlist = self.getListFolders(withfolder)
        sourcefilelist = self.getNeedFilesList(original)
        flashfilelist = self.getNeedFilesList(withfolder)
        
        for source in sourcefilelist:
            copypathfrom = original+'\\'+source
            copypathto = withfolder+'\\'+source
            
            if source not in flashfilelist:                
                print 'Add: '+copypathfrom

                try:
                    shutil.copy(copypathfrom, copypathto)
                except: pass

            
            else:  #check md5
                try:
                    f = open(path, 'r');
                    f.close()
                    if( self.getMagikMd5ForFile(copypathfrom) != self.getMagikMd5ForFile(copypathto) ):
                        print 'Fixing: '+copypathto;
                        try:
                            os.remove(copypathto)
                            shutil.copy(copypathfrom, copypathto)
                            if self.getMagikMd5ForFile(copypathfrom) == self.getMagikMd5ForFile(copypathto):
                                print 'Fixed!'
                            else: print 'Can\'t Fix';
                            #print 'Removed: '+copypathto;
                        except: pass
                except: pass    
                 

        for flash in flashfilelist:
            if flash not in sourcefilelist:
                removepath = withfolder+'\\'+flash
                print 'Remove: '+removepath
                
                try:
                    os.remove(removepath)
                except: pass

        for folder in flashfolderlist:
            if folder not in sourcefolderlist:
                removedirpath = withfolder+'\\'+folder                
                print 'Remove: '+removedirpath
                try:
                    shutil.rmtree(removedirpath)
                except: pass

        for folder in sourcefolderlist:
            if os.path.exists(withfolder+'\\'+folder): pass
            else:
                try:
                    os.mkdir(withfolder+'\\'+folder)
                except: pass
            self.sync_folder(original+'\\'+folder, withfolder+'\\'+folder)
        #rint flashfilelist
