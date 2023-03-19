#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import signal
import time
import PyQt5.QtCore
import PyQt5.QtWidgets

import linux


class Worker(PyQt5.QtCore.QObject):
    
    sig_catch = PyQt5.QtCore.pyqtSignal(int)
    sig_end = PyQt5.QtCore.pyqtSignal()
    
    def initialize(self):
        self.keylistener = linux.KeyListener()
        self.keylistener.add_listener ('Control_L+c+c'
                                      ,lambda:self.keylistener.set_status(status=1)
                                      )
        self.keylistener.add_listener ('Control_R+c+c'
                                      ,lambda:self.keylistener.set_status(status=1)
                                      )
        self.keylistener.add_listener ('Control_L+Insert+Insert'
                                      ,lambda:self.keylistener.set_status(status=1)
                                      )
        self.keylistener.add_listener ('Control_R+Insert+Insert'
                                      ,lambda:self.keylistener.set_status(status=1)
                                      )
        self.keylistener.add_listener ('Alt_L+grave'
                                      ,lambda:self.keylistener.set_status(status=2)
                                      )
        self.keylistener.add_listener ('Alt_R+grave'
                                      ,lambda:self.keylistener.set_status(status=2)
                                      )
    
    def run(self):
        # Do not quit when Control-c is pressed
        #signal.signal(signal.SIGINT,linux.catch_control_c)
        print('Running thread...')
        while not self.keylistener.check():
            time.sleep(.5)
        print('Status changed!')
        self.sig_catch.emit(2)
    
    def cancel(self):
        linux.keylistener.cancel()
        self.sig_end.emit()
    
    def test(self):
        #linux.keylistener.status = 2
        #self.sig_catch.emit(linux.keylistener.status)
        self.keylistener.run()



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
        self.worker.initialize()
        self.thread.started.connect(self.worker.test)
        self.worker.sig_catch.connect(self.report)
        self.worker.sig_end.connect(self.thread.quit)
        self.worker.sig_end.connect(self.worker.deleteLater)
        self.worker.sig_end.connect(self.thread.deleteLater)
        self.thread.start()
        self.worker.run()
        


if __name__ == '__main__':
    f = '__main__'
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    app.run_thread()
    sys.exit(exe.exec_())
