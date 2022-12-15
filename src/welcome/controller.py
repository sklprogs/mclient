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
    
    def reset(self):
        self.fill()
        self.gui.set_span(0,0,2,4)
        self.gui.set_col_width(0,200)
        self.gui.set_col_width(1,100)
        self.gui.set_col_width(2,200)
        self.gui.set_col_width(3,100)
    
    def fill(self):
        f = '[MClientQt] welcome.controller.Welcome.fill'
        table = [['<b>Welcome to MClient!</b>','','',''],['','','','']]
        add = self.logic.run()
        if add:
            table += add
        else:
            sh.com.rep_empty(f)
        model = gi.TableModel(table)
        self.gui.set_model(model)
