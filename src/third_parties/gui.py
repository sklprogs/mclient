#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

ICON = sh.objs.get_pdir().add('..','resources','mclient.png')


class ThirdParties(PyQt5.QtWidgets.QWidget):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def fill(self,text):
        self.textbox.clear()
        self.cursor.insertText(text,self.char_fmt)
        self.textbox.moveCursor(self.cursor.Start)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0,0,0,0)
    
    def add_widgets(self):
        self.layout_.addWidget(self.textbox)
        self.setLayout(self.layout_)
    
    def set_gui(self):
        self.set_layout()
        self.textbox = PyQt5.QtWidgets.QTextEdit()
        self.doc = PyQt5.QtGui.QTextDocument()
        self.cursor = PyQt5.QtGui.QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.font = PyQt5.QtGui.QFont('Serif',12)
        self.char_fmt.setFont(self.font)
        self.add_widgets()
        self.resize(600,400)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
