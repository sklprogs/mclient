#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
#import skl_shared_qt.shared as sh

from . import gui as gi
from . import logic as lg


class Symbols:
    
    def __init__(self):
        self.set_logic()
        self.set_gui()
        self.fill()
    
    def select(self, rowno, colno):
        index_ = self.model.index(rowno, colno)
        self.gui.table.set_cur_index(index_)
    
    def set_gui(self):
        self.gui = gi.Symbols()
        self.set_title()
        self.set_bindings()
    
    def get(self):
        rowno, colno = self.gui.table.get_cur_cell()
        return self.logic.get(rowno, colno)
    
    def set_logic(self):
        self.logic = lg.Symbols()
    
    def fill(self):
        self.model = gi.TableModel(self.logic.run())
        self.gui.set_model(self.model)
        self.gui.resize_to_contents()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.table.sig_select.connect(self.select)
    
    def show(self):
        self.gui.show()
        self.gui.set_size()
        self.gui.centralize()
    
    def set_title(self, title=_('Paste symbols')):
        self.gui.set_title(title)
    
    def close(self):
        self.gui.close()
