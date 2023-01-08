#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Save:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
        self.fill_model()
    
    def set_gui(self):
        self.gui = gi.Save()
        self.set_title()
        self.set_bindings()
    
    def fill_model(self):
        ''' Do not assign 'gi.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = gi.TableModel()
        self.gui.set_model(self.model)
        if self.model.items:
            self._go_row(0)
    
    def _go_row(self,rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno,0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def set_title(self,title=_('Save article')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.bind('F2',self.toggle)
        self.gui.bind('Ctrl+S',self.toggle)
        self.gui.sig_close.connect(self.close)
    
    def centralize(self):
        self.gui.centralize()
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
