#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
import PyQt5.QtCore
import PyQt5.QtWidgets

import linux


class Worker(PyQt5.QtCore.QObject):
    
    sig_catch = PyQt5.QtCore.pyqtSignal(int)
    sig_end = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Running = True
    
    def run(self):
        print('Running thread...')
        while self.Running:
            # 'linux.keylistener.status' is reset to 0 after catching a hotkey
            status = linux.keylistener.check()
            if status:
                print('Status changed!')
                self.sig_catch.emit(status)
            time.sleep(.5)
    
    def cancel(self):
        linux.keylistener.cancel()
        self.Running = False
        self.sig_end.emit()
    
    def test(self):
        linux.keylistener.status = 2
        self.sig_catch.emit(linux.keylistener.status)



class App(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
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
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.sig_catch.connect(self.report)
        self.worker.sig_end.connect(self.thread.quit)
        self.worker.sig_end.connect(self.worker.deleteLater)
        self.worker.sig_end.connect(self.thread.deleteLater)
        self.thread.start()


if __name__ == '__main__':
    f = '__main__'
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    app.run_thread()
    sys.exit(exe.exec_())
