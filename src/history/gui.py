#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets
import PyQt5.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class History(PyQt5.QtWidgets.QWidget):
    
    close_history = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def create_item(self,text1,text2):
        item = PyQt5.QtWidgets.QTreeWidgetItem(self.history)
        item.setText(0,text1)
        item.setText(1,text2)
        return item
    
    def add_item(self,text1,text2,old_item):
        item = PyQt5.QtWidgets.QTreeWidgetItem(self.history,old_item)
        item.setText(0,text1)
        item.setText(1,text2)
        return item
    
    def insert(self,index,item):
        self.history.insertTopLevelItem(index,item)
    
    def reset(self):
        self.history.clear()
    
    def closeEvent(self,event):
        self.close_history.emit()
        return super().closeEvent(event)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout(self)
        self.history = PyQt5.QtWidgets.QTreeWidget()
        self.history.setColumnCount(2)
        self.layout_.addWidget(self.history)
        self.setLayout(self.layout_)


if __name__ == '__main__':
    sh.com.start()
    ihis = History()
    item = ihis.create_item('1','start')
    item = ihis.add_item('2','hello',item)
    item = ihis.add_item('3','bye',item)
    item = ihis.add_item('4','end',item)
    ihis.show()
    sh.com.end()
