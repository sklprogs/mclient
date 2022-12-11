#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import logic as lg
from . import gui as gi


class Welcome:
    
    def __init__(self,*args,**kwargs):
        self.logic = lg.Welcome()
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
    
    def fill(self):
        table = [['<b>Welcome to MClient!</b>','','','']
                ,['','','','']
                ,['Ctrl+O','Open','Ctrl+S','Save']
                ,['Ctrl+C','Copy','Ctrl+X','Cut the following line in half']
                ]
        add = self.logic.run()
        if add:
            table += add
        model = gi.TableModel(table)
        self.gui.set_model(model)
