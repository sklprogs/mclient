#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from skl_shared.logic import OS

if OS.is_win():
    import keylistener.windows as osid
elif OS.is_lin():
    import keylistener.linux as osid
else:
    import keylistener.unsupported as osid

''' I tried to move non-gui-specific code to 'controller'; however, each time
    I move 'Catcher.run' out, GUI freezes.
'''

class Catcher(QObject):
    
    sig_catch = pyqtSignal(int)
    sig_end = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Running = True
    
    def bind_catch(self, action):
        self.sig_catch.connect(action)
    
    def delete_later(self):
        self.deleteLater()
    
    def move_to_thread(self, thread):
        self.moveToThread(thread)
    
    def run(self):
        while self.Running:
            # 'osid.keylistener.status' is reset to 0 after catching a hotkey
            status = osid.keylistener.check()
            if status:
                self.sig_catch.emit(status)
            time.sleep(.5)
    
    def cancel(self):
        self.Running = False
        osid.keylistener.cancel()
        self.delete_later()
        self.sig_end.emit()



class Thread(QThread):
    # Built-in functions that are called: start, quit, wait
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.catcher = Catcher()
    
    def bind_start(self, action):
        self.started.connect(action)
    
    def bind_catch(self, action):
        self.catcher.sig_catch.connect(action)
    
    def delete_later(self):
        self.deleteLater()
    
    def end(self):
        self.catcher.cancel()
        self.wait()
    
    def run_thread(self):
        # Do not override built-in methods start, run, quit
        self.catcher.move_to_thread(self)
        self.bind_start(self.catcher.run)
        self.catcher.sig_end.connect(self.quit)
        self.catcher.sig_end.connect(self.delete_later)
        self.start()
