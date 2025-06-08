#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared.localize import _
from skl_shared.graphics.entry.controller import Entry
from skl_shared.graphics.button.controller import Button
from skl_shared.graphics.checkbox.controller import CheckBox


class Search(QWidget):

    sig_close = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def clear(self):
        self.ent_src.clear()
    
    def set_title(self, title=_('Search:')):
        self.setWindowTitle(title)
    
    def add_widgets(self):
        self.layout_ = QVBoxLayout()
        self.ent_src = Entry()
        self.cbx_cas = CheckBox(_('Case-sensitive'))
        self.btn_cls = Button(_('Close'))
        self.btn_clr = Button(_('Clear'))
        self.btn_srp = Button(_('Back'))
        self.btn_srn = Button(_('Forward'))
        self.layout_.addWidget(self.ent_src.widget)
        self.layout_.addWidget(self.cbx_cas.widget)
        self.panel = QWidget()
        self.btn_lay = QHBoxLayout()
        self.btn_lay.setContentsMargins(4, 4, 4, 4)
        self.btn_lay.addWidget(self.btn_cls.widget)
        self.btn_lay.addWidget(self.btn_clr.widget)
        self.btn_lay.addWidget(self.btn_srp.widget)
        self.btn_lay.addWidget(self.btn_srn.widget)
        self.panel.setLayout(self.btn_lay)
        self.layout_.addWidget(self.panel)
        self.setLayout(self.layout_)
    
    def set_gui(self):
        self.add_widgets()
        self.set_title()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def get(self):
        return self.ent_src.get()
