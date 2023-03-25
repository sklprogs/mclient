#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time

import PyQt5.QtWidgets
import PyQt5.QtCore

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

if sh.objs.get_os().is_win():
    import windows as osid
elif sh.objs.os.is_lin():
    import linux as osid
else:
    #TODO: create and import dummy module
    import linux as osid

import gui as gi


class Catcher:
    
    def __init__(self):
        self.Running = True
        self.gui = gi.Catcher()
    
    def run(self):
        while self.Running:
            # 'osid.keylistener.status' is reset to 0 after catching a hotkey
            status = osid.objs.get_listener().check()
            if status:
                self.gui.catch(status)
            time.sleep(.5)
    
    def end(self):
        osid.objs.get_listener().cancel()
        self.Running = False
        self.gui.end()
    
    def move_to_thread(self,thread):
        self.gui.move_to_thread(thread)
    
    def bind_catch(self,action):
        self.gui.bind_catch(action)
    
    def bind_end(self,action):
        self.gui.bind_end(action)
    
    def delete_later(self):
        self.gui.delete_later()



class Thread:
    
    def __init__(self,catch_action):
        self.catch_action = catch_action
        self.catcher = Catcher()
        self.thread = gi.Thread()
    
    def delete_later(self):
        self.catcher.delete_later()
        self.thread.delete_later()
    
    def _bind_start(self):
        self.thread.bind_start(self.catcher.run)
    
    def _bind_end(self):
        self.catcher.bind_end(self.thread.quit)
        self.catcher.bind_end(self.delete_later)
    
    def _bind_catch(self):
        self.catcher.bind_catch(self.catch_action)
    
    def bind(self):
        self._bind_start()
        self._bind_catch()
        self._bind_end()
    
    def start(self):
        osid.com.start()
        self.catcher.move_to_thread(self.thread)
        self.thread.start()
        self.bind()
    
    def wait(self):
        # Calling in-built function
        self.thread.wait()
    
    def end(self):
        self.catcher.end()
        self.wait()



class App(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_thread()
        self.set_gui()
    
    def closeEvent(self,event):
        self.thread.end()
        return super().closeEvent(event)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def report(self):
        print('Triggered')
        self.button.setText('SUCCESS')
    
    def set_gui(self):
        self.button = PyQt5.QtWidgets.QPushButton()
        self.button.setText('Click me!')
        layout_ = PyQt5.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.button)
        self.setLayout(layout_)
    
    def set_thread(self):
        self.thread = Thread(self.report)
        self.thread.start()
        


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    #exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    #app.set_thread()
    app.show()
    #sys.exit(exe.exec_())
    sh.com.end()
