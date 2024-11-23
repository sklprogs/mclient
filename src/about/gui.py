#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QSizePolicy, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared_qt.localize import _
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.button.controller import Button
from skl_shared_qt.graphics.label.controller import Label


class About(QWidget):
    
    sig_close = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_text(self, text):
        self.lbl_abt.set_text(text)
    
    def configure(self):
        policy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_thd.widget.setSizePolicy(policy)
        self.btn_lic.widget.setSizePolicy(policy)
        self.btn_eml.widget.setSizePolicy(policy)
    
    def add_buttons(self):
        self.btn_thd = Button(text = _('Third parties')
                             ,hint = _('Third-party licenses'))
        self.btn_lic = Button(text = _('License')
                             ,hint = _('View the license'))
        self.btn_eml = Button(text = _('Contact the author')
                             ,hint = _('Draft an email to the author'))
    
    def add_layout(self):
        self.layout_.addWidget(self.lbl_abt.widget, 0, 0, 1, 3)
        self.layout_.addWidget(self.btn_thd.widget, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.btn_lic.widget, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout_.addWidget(self.btn_eml.widget, 1, 2, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout_)
    
    def add_widgets(self):
        self.lbl_abt = Label()
        self.layout_ = QGridLayout(self)
    
    def set_gui(self):
        self.add_widgets()
        self.add_buttons()
        self.configure()
        self.add_layout()
        self.set_icon()
