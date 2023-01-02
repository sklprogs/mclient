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
    
    def add_row(self,no,lang1,lang2,search):
        # Reuse an empty row created upon initializing History
        if no != '1':
            self.item = PyQt5.QtWidgets.QTreeWidgetItem(self.history,self.item)
        self.item.setText(0,no)
        self.item.setText(1,lang1)
        self.item.setText(2,lang2)
        self.item.setText(3,search)
    
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
    
    def set_icon(self,qicon):
        # Does not accent None
        self.setWindowIcon(qicon)
    
    def set_headers(self):
        headers = [_('#'),_('Source language'),_('Target language')
                  ,_('Request')
                  ]
        self.history.setHeaderLabels(headers)
    
    def set_col_width(self):
        self.history.header().resizeSection(0,50)
    
    def set_gui(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout(self)
        self.history = PyQt5.QtWidgets.QTreeWidget()
        self.history.setColumnCount(4)
        self.set_headers()
        self.layout_.addWidget(self.history)
        self.setLayout(self.layout_)
        self.item = PyQt5.QtWidgets.QTreeWidgetItem(self.history)
        self.set_col_width()
        self.resize(600,300)


if __name__ == '__main__':
    sh.com.start()
    ihis = History()
    item = ihis.add_row('1',_('Russian'),_('English'),'start')
    item = ihis.add_row('2',_('Russian'),_('English'),'hello')
    item = ihis.add_row('3',_('English'),_('Russian'),'bye')
    item = ihis.add_row('4',_('Arabic'),_('French'),'end')
    ihis.show()
    sh.com.end()
