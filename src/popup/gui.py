#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6
import PyQt6.QtWidgets

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

WIDTH = 270
HEIGHT = 150


class Popup(PyQt6.QtWidgets.QWidget):
    
    sig_close = PyQt6.QtCore.pyqtSignal()
    
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
        self.move(sh.objs.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def fill(self, code):
        self.textbox.setHtml(code)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = PyQt6.QtWidgets.QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def add_widgets(self):
        self.layout_.addWidget(self.textbox)
        self.setLayout(self.layout_)
    
    def set_gui(self):
        self.set_layout()
        self.textbox = PyQt6.QtWidgets.QTextEdit()
        self.doc = PyQt6.QtGui.QTextDocument()
        self.cursor = PyQt6.QtGui.QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.textbox.setReadOnly(True)
        self.font = PyQt6.QtGui.QFont('Serif', 11)
        self.char_fmt.setFont(self.font)
        self.add_widgets()
        self.set_icon()
        flags = self.windowFlags()
        self.setWindowFlags(flags|PyQt6.QtCore.Qt.WindowType.FramelessWindowHint)
        self.resize(WIDTH, HEIGHT)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
