#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Popup:
    
    def __init__(self):
        self.gui = gi.Popup()
        self.set_gui()
    
    def fill(self,text):
        self.gui.fill(text)
    
    def set_title(self,title=_('Full cell text')):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.set_bindings()
        self.set_title()
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
