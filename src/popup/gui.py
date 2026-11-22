#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QFont, QShortcut, \
     QKeySequence, QKeyEvent
from PyQt6.QtCore import pyqtSignal, Qt

from skl_shared.graphics.root.controller import ROOT

WIDTH = 270
HEIGHT = 150


class CustomTextEdit(QTextEdit):
    
    sig_up = pyqtSignal()
    sig_down = pyqtSignal()
    sig_left = pyqtSignal()
    sig_right = pyqtSignal()
    sig_pgup = pyqtSignal()
    sig_pgdn = pyqtSignal()
    sig_start = pyqtSignal()
    sig_end = pyqtSignal()
    sig_go = pyqtSignal()
    sig_copy = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_bindings()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_bindings(self):
        self.bind(('Ctrl+Home',), self.sig_start.emit)
        self.bind(('Ctrl+End',), self.sig_end.emit)
        self.bind(('Return', 'Enter',), self.sig_go)
        self.bind(('Ctrl+Return', 'Ctrl+Enter',), self.sig_copy)
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Up:
            self.sig_up.emit()
        elif event.key() == Qt.Key.Key_Down:
            self.sig_down.emit()
        elif event.key() == Qt.Key.Key_Left:
            self.sig_left.emit()
        elif event.key() == Qt.Key.Key_Right:
            self.sig_right.emit()
        elif event.key() == Qt.Key.Key_PageUp:
            self.sig_pgup.emit()
        elif event.key() == Qt.Key.Key_PageDown:
            self.sig_pgdn.emit()
        super().keyPressEvent(event)



class Popup(QWidget):
    
    sig_show = pyqtSignal()
    sig_close = pyqtSignal()
    
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
    
    def emit_show(self):
        self.sig_show.emit()
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def fill(self, code):
        self.textbox.setHtml(code)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_layout(self):
        self.layout_ = QVBoxLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
    
    def add_widgets(self):
        self.layout_.addWidget(self.textbox)
        self.setLayout(self.layout_)
    
    def set_gui(self):
        self.set_layout()
        self.textbox = CustomTextEdit()
        self.doc = QTextDocument()
        self.cursor = QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.textbox.setReadOnly(True)
        self.font = QFont('Serif', 11)
        self.char_fmt.setFont(self.font)
        self.add_widgets()
        flags = self.windowFlags()
        self.setWindowFlags(flags|Qt.WindowType.FramelessWindowHint)
        self.resize(WIDTH, HEIGHT)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
