#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets
import PyQt5.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class About(PyQt5.QtWidgets.QWidget):
    
    sig_close = PyQt5.QtCore.pyqtSignal()
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def closeEvent(self,event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def set_title(self,title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_text(self,text):
        self.lbl_abt.set_text(text)
    
    def set_gui(self):
        self.lbl_abt = sh.Label()
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        self.panel = PyQt5.QtWidgets.QWidget(self)
        policy = PyQt5.QtWidgets.QSizePolicy (PyQt5.QtWidgets.QSizePolicy.Fixed
                                             ,PyQt5.QtWidgets.QSizePolicy.Fixed
                                             )
        # Show the license
        self.btn_thd = sh.Button (text = _('Third parties')
                                 ,hint = _('Third-party licenses')
                                 )
        self.btn_lic = sh.Button (text = _('License')
                                 ,hint = _('View the license')
                                 )
        # Send mail to the author
        self.btn_eml = sh.Button (text = _('Contact the author')
                                 ,hint = _('Draft an email to the author')
                                 )
        self.btn_thd.widget.setSizePolicy(policy)
        self.btn_lic.widget.setSizePolicy(policy)
        self.btn_eml.widget.setSizePolicy(policy)
        self.btn_lay = PyQt5.QtWidgets.QHBoxLayout()
        self.btn_lay.setContentsMargins(4,4,4,4)
        self.btn_lay.addWidget(self.btn_thd.widget)
        self.btn_lay.addWidget(self.btn_lic.widget)
        self.btn_lay.addWidget(self.btn_eml.widget)
        self.panel.setLayout(self.btn_lay)
        self.layout_.addWidget(self.lbl_abt.widget)
        self.layout_.addWidget(self.panel)
        self.setLayout(self.layout_)
        self.set_icon()
