#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi
from . import logic as lg


class Symbols:
    
    def __init__(self):
        self.logic = lg.Symbols()
        self.gui = gi.Symbols()
        self.set_title()
        self.set_bindings()
    
    def fill(self):
        self.gui.set_model(self.logic.model)
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def set_title(self,title=_('Special symbols')):
        self.gui.set_title(title)
    
    def close(self):
        self.gui.close()
