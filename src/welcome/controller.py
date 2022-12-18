#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import logic as lg
from . import gui as gi


class Welcome:
    
    def __init__(self):
        self.logic = lg.Welcome()
        self.set_gui()
    
    def set_gui(self):
        self.gui = gi.App()
        self.set_bindings()
    
    def close(self):
        self.gui.close()
    
    def show(self):
        self.gui.show()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
    
    def set_spans(self):
        self.gui.set_span(0,0,1,lg.COLNUM)
        self.gui.set_span(1,0,1,lg.COLNUM)
        self.gui.set_span(2,0,1,lg.COLNUM)
    
    def set_col_widths(self):
        for i in range(lg.COLNUM):
            self.gui.set_col_width(i,166)
    
    def reset(self):
        self.fill()
        self.set_spans()
        self.set_col_widths()
    
    def fill(self):
        model = gi.TableModel(self.logic.run())
        self.gui.set_model(model)
