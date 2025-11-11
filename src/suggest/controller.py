#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep

from manager import SOURCES
from suggest.gui import Suggest as guiSuggest


class Suggest:
    
    def __init__(self):
        self.set_gui()
    
    def load(self):
        self.gui.load()
    
    def get(self):
        f = '[MClient] suggest.controller.Suggest.get'
        try:
            return self.gui.get()
        except IndexError:
            rep.empty_output(f)
        return ''
    
    def set_geometry(self, x, y, width, height):
        self.gui.set_geometry(x, y, width, height)
    
    def get_height(self):
        return self.gui.get_height()
    
    def set_gui(self):
        self.gui = guiSuggest()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.bind(('Return',), self.load)
        self.gui.bind(('Enter',), self.load) # NumPad
    
    def show(self):
        self.gui.show()
    
    def fill(self, lst):
        f = '[MClient] suggest.controller.Suggest.fill'
        if not lst:
            rep.empty(f)
            return
        self.gui.fill(lst)
    
    def go_end(self):
        f = '[MClient] suggest.controller.Suggest.go_end'
        if not self.gui.model.items:
            rep.lazy(f)
            return
        rowno = len(self.gui.model.items) - 1
        self.go_row(rowno)
    
    def go_row(self, rowno):
        self.gui.clear_selection()
        index_ = self.gui.model.index(rowno, 0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def close(self):
        self.gui.close()
    
    def set_width(self, width):
        self.gui.set_width(width)
    
    def suggest(self, search, limit=0):
        f = '[MClient] suggest.controller.Suggest.suggest'
        items = SOURCES.suggest(search)
        if not items:
            rep.empty(f)
            return []
        return items[0:limit]


SUGGEST = Suggest()
