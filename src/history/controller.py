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
    
    def fill_model(self,table=[[]]):
        ''' Do not assign 'gi.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = gi.TableModel(table)
        self.gui.set_model(self.model)
    
    def go_down(self):
        f = '[MClient] history.controller.History.go_down'
        if not self.model.items or not self.model.items[0]:
            sh.com.rep_empty(f)
            return
        rowno, colno = self.gui.get_cell()
        mes = _('Current row #{}').format(rowno)
        sh.objs.get_mes(f,mes,True).show_debug()
        if rowno + 1 >= len(self.model.items):
            rowno = -1
        rowno += 1
        mes = _('Next row #{}').format(rowno)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.gui.clear_selection()
        index_ = self.model.index(rowno,colno)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def has_id(self,id_):
        for row in self.model.items:
            if row and row[0] == id_:
                return True
    
    def add_row(self,id_,source,lang1,lang2,search):
        id_ = str(id_)
        if not self.has_id(id_):
            row = [id_,source,lang1,lang2,search]
            self.model.items.insert(0,row)
            self.model.update()
    
    def set_title(self,title=_('History')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.bind('Down',self.go_down)
    
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
