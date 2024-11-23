#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QTextDocument, QTextCursor, QFont, QShortcut, QKeySequence

from skl_shared_qt.graphics.root.controller import ROOT


class ThirdParties(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def fill(self, text):
        self.textbox.clear()
        self.cursor.insertText(text, self.char_fmt)
        self.textbox.moveCursor(self.cursor.MoveOperation.Start)
    
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
        self.textbox = QTextEdit()
        self.doc = QTextDocument()
        self.cursor = QTextCursor(self.doc)
        self.char_fmt = self.cursor.charFormat()
        self.textbox.setDocument(self.doc)
        self.textbox.setReadOnly(True)
        self.font = QFont('Serif', 12)
        self.char_fmt.setFont(self.font)
        self.add_widgets()
        self.resize(600, 400)
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
