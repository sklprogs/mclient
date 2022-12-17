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
        self.gui.set_span(0,0,1,6)
        for i in range(6):
            self.gui.set_col_width(i,150)
    
    def fill(self):
        f = '[MClientQt] welcome.controller.Welcome.fill'
        table = [['<h2>Welcome to MClient!</h2>','','','','','']]
        add = self.logic.run()
        if add:
            table += add
        else:
            sh.com.rep_empty(f)
        model = gi.TableModel(table)
        self.gui.set_model(model)
