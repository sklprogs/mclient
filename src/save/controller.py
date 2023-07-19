#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import config as cf
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
        self.change_font_size(2)
    
    def get(self):
        f = '[MClientQt] save.controller.Save.get'
        if not self.model.items:
            sh.com.rep_lazy(f)
            return
        return self.model.items[self.gui.get_row()]
    
    def go_start(self):
        f = '[MClientQt] save.controller.Save.go_start'
        if not self.model.items:
            sh.com.rep_lazy(f)
            return
        self._go_row(0)
    
    def go_end(self):
        f = '[MClientQt] save.controller.Save.go_end'
        if not self.model.items:
            sh.com.rep_lazy(f)
            return
        rowno = len(self.model.items) - 1
        self._go_row(rowno)
    
    def go_down(self):
        # Qt already goes down/up, but without looping
        f = '[MClientQt] save.controller.Save.go_down'
        if not self.model.items:
            sh.com.rep_empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == len(self.model.items) - 1:
            rowno = -1
        rowno += 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old, rowno)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def go_up(self):
        # Qt already goes down/up, but without looping
        f = '[MClientQt] save.controller.Save.go_up'
        if not self.model.items:
            sh.com.rep_empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == 0:
            rowno = len(self.model.items)
        rowno -= 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old, rowno)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def change_font_size(self, delta=1):
        f = '[MClientQt] save.controller.Save.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            sh.com.rep_empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            sh.com.rep_condition(f, mes)
            return
        self.gui.set_font_size(size+delta)
    
    def fill_model(self):
        ''' Do not assign 'gi.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = gi.TableModel()
        self.gui.set_model(self.model)
        if self.model.items:
            self._go_row(0)
    
    def _go_row(self, rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno, 0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def set_title(self, title=_('Save article')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc', self.close)
        self.gui.bind('Down', self.go_down)
        self.gui.bind('Up', self.go_up)
        self.gui.bind('Home', self.go_start)
        self.gui.bind('End', self.go_end)
        self.gui.bind('Ctrl+Home', self.go_start)
        self.gui.bind('Ctrl+End', self.go_end)
        self.gui.bind(cf.objs.get_config().new['hotkeys']['save_article'], self.toggle)
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
