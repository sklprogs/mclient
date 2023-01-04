#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class History:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
        self.fill_model()
    
    def set_gui(self):
        self.gui = gi.History()
        self.set_title()
        self.set_bindings()
    
    def go_start(self):
        f = '[MClient] history.controller.History.go_start'
        if not self.model.items:
            sh.com.rep_lazy(f)
            return
        self._go_row(0)
    
    def fill_model(self,table=[[]]):
        ''' Do not assign 'gi.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = gi.TableModel(table)
        self.gui.set_model(self.model)
        self.go_start()
    
    def _go_row(self,rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno,0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def go_down(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] history.controller.History.go_down'
        if not self.model.items or not self.model.items[0]:
            sh.com.rep_empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == len(self.model.items) - 1:
            rowno = -1
        rowno += 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old,rowno)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def go_up(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] history.controller.History.go_up'
        if not self.model.items or not self.model.items[0]:
            sh.com.rep_empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == 0:
            rowno = len(self.model.items)
        rowno -= 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old,rowno)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def _has_id(self,id_):
        for row in self.model.items:
            if row and row[0] == id_:
                return True
    
    def add_row(self,id_,source,lang1,lang2,search):
        f = '[MClient] history.controller.History.add_row'
        if not self.model.items:
            sh.com.rep_empty(f)
            return
        # Avoid getting out of bounds, since our table is initially [[]]
        if self.model.items[0] == []:
            del self.model.items[0]
        id_ = str(id_)
        if not self._has_id(id_):
            row = [id_,source,lang1,lang2,search]
            self.model.items.append(row)
            self.model.update()
        self._go_row(len(self.model.items)-1)
    
    def set_title(self,title=_('History')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.bind('Down',self.go_down)
        self.gui.bind('Up',self.go_up)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
