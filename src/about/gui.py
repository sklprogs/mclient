#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6.QtWidgets
import PyQt6.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class About(PyQt6.QtWidgets.QWidget):
    
    sig_close = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().primaryScreen().geometry().center() - self.rect().center())
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_text(self, text):
        self.lbl_abt.set_text(text)
    
    def configure(self):
        policy = PyQt6.QtWidgets.QSizePolicy (PyQt6.QtWidgets.QSizePolicy.Policy.Fixed
                                             ,PyQt6.QtWidgets.QSizePolicy.Policy.Fixed
                                             )
        self.btn_thd.widget.setSizePolicy(policy)
        self.btn_lic.widget.setSizePolicy(policy)
        self.btn_eml.widget.setSizePolicy(policy)
    
    def add_buttons(self):
        self.btn_thd = sh.Button (text = _('Third parties')
                                 ,hint = _('Third-party licenses')
                                 )
        self.btn_lic = sh.Button (text = _('License')
                                 ,hint = _('View the license')
                                 )
        self.btn_eml = sh.Button (text = _('Contact the author')
                                 ,hint = _('Draft an email to the author')
                                 )
    
    def add_layout(self):
        self.layout_.addWidget(self.lbl_abt.widget, 0, 0, 1, 3)
        self.layout_.addWidget(self.btn_thd.widget, 1, 0, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignLeft)
        self.layout_.addWidget(self.btn_lic.widget, 1, 1, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout_.addWidget(self.btn_eml.widget, 1, 2, 1, 1, PyQt6.QtCore.Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout_)
    
    def add_widgets(self):
        self.lbl_abt = sh.Label()
        self.layout_ = PyQt6.QtWidgets.QGridLayout(self)
    
    def set_gui(self):
        self.add_widgets()
        self.add_buttons()
        self.configure()
        self.add_layout()
        self.set_icon()
