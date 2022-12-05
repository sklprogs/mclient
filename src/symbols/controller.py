#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi
from . import logic as lg


class Symbols:
    
    def __init__(self):
        self.set_logic()
        self.set_gui()
        self.fill()
    
    def set_gui(self):
        self.gui = gi.Symbols()
        self.set_title()
        self.set_bindings()
    
    def set_logic(self):
        self.logic = lg.Symbols()
    
    def fill(self):
        model = gi.TableModel(self.logic.run())
        self.gui.set_model(model)
        self.gui.resize_to_contents()
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
    
    def show(self):
        self.gui.show()
        self.gui.set_size()
        self.gui.centralize()
    
    def set_title(self,title=_('Paste symbols')):
        self.gui.set_title(title)
    
    def close(self):
        self.gui.close()
