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
        self._go_article(0)
    
    def go_end(self):
        f = '[MClient] history.controller.History.go_end'
        if not self.model.items:
            sh.com.rep_lazy(f)
            return
        rowno = len(self.model.items) - 1
        self._go_row(rowno)
        self._go_article(rowno)
    
    def fill_model(self,table=[[]]):
        ''' Do not assign 'gi.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = gi.TableModel(table)
        self.gui.set_model(self.model)
        if self.model.items and self.model.items[0]:
            self._go_row(0)
    
    def _go_row(self,rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno,0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def _go_article(self,rowno):
        f = '[MClient] history.controller.History._go_article'
        try:
            id_ = self.model.items[rowno][0]
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(rowno)
            sh.objs.get_mes(f,mes).show_warning()
            return
        self.gui.signal_go.emit(int(id_))
    
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
        self._go_article(rowno)
    
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
        self._go_article(rowno)
    
    def _find_id(self,id_):
        for i in range(len(self.model.items)):
            if self.model.items[i] and self.model.items[i][0] == id_:
                return i
    
    def add_row(self,id_,source,lang1,lang2,search):
        f = '[MClient] history.controller.History.add_row'
        if not self.model.items:
            sh.com.rep_empty(f)
            return
        # Avoid getting out of bounds, since our table is initially [[]]
        if self.model.items[0] == []:
            del self.model.items[0]
        id_ = str(id_)
        rowno = self._find_id(id_)
        if rowno is None:
            row = [id_,source,lang1,lang2,search]
            self.model.items.append(row)
            self.model.update()
            self._go_row(len(self.model.items)-1)
        else:
            self._go_row(rowno)
    
    def set_title(self,title=_('History')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.bind('Down',self.go_down)
        self.gui.bind('Up',self.go_up)
        self.gui.bind('Alt+Left',self.go_up)
        self.gui.bind('Alt+Right',self.go_down)
        self.gui.bind('Home',self.go_start)
        self.gui.bind('End',self.go_end)
        self.gui.bind('Alt+Home',self.go_start)
        self.gui.bind('Alt+End',self.go_end)
        self.gui.bind('Ctrl+Home',self.go_start)
        self.gui.bind('Ctrl+End',self.go_end)
    
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
