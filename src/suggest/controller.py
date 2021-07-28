#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
from . import gui as gi


class Suggest:
    
    def __init__(self,entry):
        self.entry = entry
        self.gui = None
    
    def close(self,event=None):
        self.get_gui().close()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gi.Suggest()
    
    def select(self,event=None):
        f = '[MClient] suggest.controller.Suggest.select'
        mes = _('This procedure should be overriden')
        sh.objs.get_mes(f,mes,True).show_error()
        
    def _select(self,event=None):
        ''' #NOTE: this works differently in Windows and Linux.
            In Windows selecting an item will hide suggestions,
            in Linux they will be kept open.
        '''
        f = '[MClient] suggest.controller.Suggest._select'
        if self.gui.parent:
            self.entry.clear_text()
            self.entry.insert(self.gui.lbox.get())
            self.entry.select_all()
            self.entry.focus()
        else:
            sh.com.rep_empty(f)
        
    def move_down(self,event=None):
        f = '[MClient] suggest.controller.Suggest.move_down'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.index_add()
            self.gui.lbox.select()
            self._select()
        else:
            sh.com.rep_empty(f)
        
    def move_up(self,event=None):
        f = '[MClient] suggest.controller.Suggest.move_up'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.index_subtract()
            self.gui.lbox.select()
            self._select()
        else:
            sh.com.rep_empty(f)
        
    def move_top(self,event=None):
        f = '[MClient] suggest.controller.Suggest.move_top'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.move_top()
            self._select()
        else:
            sh.com.rep_empty(f)
                          
    def move_bottom(self,event=None):
        f = '[MClient] suggest.controller.Suggest.move_bottom'
        if self.get_gui().parent:
            # Necessary to use arrows on ListBox
            self.gui.lbox.focus()
            self.gui.lbox.move_bottom()
            self._select()
        else:
            sh.com.rep_empty(f)
    
    def suggest(self,event=None):
        f = '[MClient] suggest.controller.Suggest.suggest'
        mes = _('This procedure should be overriden')
        sh.objs.get_mes(f,mes,True).show_error()
    
    def set_bindings(self):
        if self.get_gui().parent:
            sh.com.bind (obj = self.gui.parent
                        ,bindings = '<ButtonRelease-1>'
                        ,action = self.select
                        )