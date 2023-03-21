#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtCore
import PyQt5.QtWidgets


class Catcher(PyQt5.QtCore.QObject):
    
    sig_catch = PyQt5.QtCore.pyqtSignal(int)
    sig_end = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def catch(self,status):
        self.sig_catch.emit(status)
    
    def end(self):
        self.sig_end.emit()
    
    def move_to_thread(self,thread):
        # PyQt5.QtCore.QThread
        self.moveToThread(thread)
    
    def bind_catch(self,action):
        self.sig_catch.connect(action)
    
    def bind_end(self,action):
        self.sig_end.connect(action)
    
    def delete_later(self):
        self.deleteLater()



class Thread(PyQt5.QtCore.QThread):
    # In-built methods that are used: start, quit, deleteLater, wait
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def bind_start(self,action):
        self.started.connect(action)
    
    def delete_later(self):
        self.deleteLater()
