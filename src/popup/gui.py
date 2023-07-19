#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5
import PyQt5.QtWidgets

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Popup(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def get_width(self):
        return self.width()
    
    def get_height(self):
        return self.height()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def fill(self, code):
        self.textbox.setHtml(code)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
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
        self.textbox.setReadOnly(True)
        self.font = PyQt5.QtGui.QFont('Serif', 11)
        self.char_fmt.setFont(self.font)
        self.add_widgets()
        self.set_icon()
        flags = self.windowFlags()
        self.setWindowFlags(flags|PyQt5.QtCore.Qt.FramelessWindowHint)
        self.resize(270, 150)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
