import win32api,string
import os
import itertools, glob
import threading
import time

from sync import sync 
from systrayicon import SysTrayIcon


class flashsync(threading.Thread):
    tray_icon = '';
    current_sync = '';
    
    def __init__(self):
        
        #self.tray_icon = tray_icon
        #while(1):
        ##    global status
        #    print status
        #    #self.drawIcon()
        #    time.sleep(3)
        threading.Thread.__init__(self)
        
        
    def run(self):
        self.getdrive()
        while(1):
            from sync import sync

            if type(self.current_sync).__class__ != 'sync': self.getdrive()
            else:
                if self.current_sync.isAlive(): pass
                else:
                    self.getdrive()
            time.sleep(10)
        
        
    def getdrive(self):
        drives=win32api.GetLogicalDriveStrings()
        drives=string.splitfields(drives,'\000')
        for drive in drives:
            if self.is_good_drive(drive):
                from sync import sync 
                self.current_sync = sync(drive).start() 


    def is_good_drive(self, drivepath):
        if drivepath == 'A:\\':  return false #no 3.5
        return os.path.exists(drivepath+'/sync.ini')

    
        
status = ''
if __name__ == '__main__':    
    icons = itertools.cycle(glob.glob('*.ico'))
    hover_text = "FlashSync 0.1.5 kiryam@kiryam.ru"

    def start_sync():
        from flashsync import flashsync
        flashsync = flashsync().start()
        #while(1):            
        #    print 'Stratus: ' +status
        #    drawIcon(sysTrayIcon)
        #    time.sleep(3)
            
    def drawIcon(sysTrayIcon):
        ico_name = 'favicon.ico'
        
        if status == 'sync done':
            ico_name = 'App.ico'
            
        sysTrayIcon.icon = ico_name       
        sysTrayIcon.refresh_icon()
        
    def switch_icon(sysTrayIcon):
        sysTrayIcon.icon = icons.next()
        sysTrayIcon.refresh_icon()

    def pass_f(sysTrayIcon): pass
    menu_options = (('Start Sync', icons.next(), pass_f),
                    ('', icons.next(), ()) )
    def bye(sysTrayIcon): pass
    start_sync()
    SysTrayIcon(icons.next(), hover_text, menu_options, on_quit=bye, default_menu_index=1)
    

