#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
import PyQt5.QtCore
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

if sh.objs.get_os().is_win():
    import windows as osid
elif sh.objs.os.is_lin():
    import linux as osid
else:
    #TODO: create and import dummy module
    import linux as osid


class Catcher(PyQt5.QtCore.QObject):
    
    sig_catch = PyQt5.QtCore.pyqtSignal(int)
    sig_end = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Running = True
    
    def run(self):
        while self.Running:
            # 'osid.keylistener.status' is reset to 0 after catching a hotkey
            status = osid.keylistener.check()
            if status:
                self.sig_catch.emit(status)
            time.sleep(.5)
    
    def cancel(self):
        osid.keylistener.cancel()
        self.Running = False
        self.sig_end.emit()



class App(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def closeEvent(self,event):
        self.catcher.cancel()
        self.thread.wait()
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
    
    def run_thread(self):
        self.thread = PyQt5.QtCore.QThread()
        self.catcher = Catcher()
        self.catcher.moveToThread(self.thread)
        self.thread.started.connect(self.catcher.run)
        self.catcher.sig_catch.connect(self.report)
        self.catcher.sig_end.connect(self.thread.quit)
        self.catcher.sig_end.connect(self.catcher.deleteLater)
        self.catcher.sig_end.connect(self.thread.deleteLater)
        self.thread.start()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = App()
    app.show()
    app.run_thread()
    sh.com.end()
