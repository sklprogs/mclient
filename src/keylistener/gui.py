#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
import PyQt5.QtCore
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

if sh.objs.get_os().is_win():
    import os_specific.windows as osid
elif sh.objs.os.is_lin():
    import os_specific.linux as osid
else:
    import os_specific.unsupported as osid

''' I tried to move non-gui-specific code to 'controller'; however, each time
    I move 'Catcher.run' out, GUI freezes.
'''

class Catcher(PyQt5.QtCore.QObject):
    
    sig_catch = PyQt5.QtCore.pyqtSignal(int)
    sig_end = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Running = True
    
    def bind_catch(self,action):
        self.sig_catch.connect(action)
    
    def delete_later(self):
        self.deleteLater()
    
    def move_to_thread(self,thread):
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



class Thread(PyQt5.QtCore.QThread):
    # Built-in functions that are called: start, quit, wait
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.catcher = Catcher()
    
    def bind_start(self,action):
        self.started.connect(action)
    
    def bind_catch(self,action):
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



class App(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def closeEvent(self,event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def report(self):
        print('Triggered')
        self.button.setText('SUCCESS')
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_gui(self):
        self.button = PyQt5.QtWidgets.QPushButton()
        self.button.setText('Click me!')
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.button)
        self.setLayout(layout_)


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = App()
    app.show()
    app.run_thread()
    sh.com.end()
