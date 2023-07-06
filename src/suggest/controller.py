#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Suggest:
    
    def __init__(self):
        self.set_gui()
    
    def load(self):
        self.gui.load(self.get())
    
    def get(self):
        f = '[MClientQt] suggest.controller.Suggest.get'
        try:
            return self.gui.get()
        except IndexError:
            sh.com.rep_input(f)
        return ''
    
    def set_geometry(self, x, y, width, height):
        self.gui.set_geometry(x, y, width, height)
    
    def get_height(self):
        return self.gui.get_height()
    
    def set_gui(self):
        self.gui = gi.Suggest()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind('Esc', self.close)
        self.gui.bind('Return', self.load)
    
    def show(self):
        self.gui.show()
    
    def fill(self, lst):
        f = '[MClientQt] suggest.controller.Suggest.fill'
        if not lst:
            sh.com.rep_empty(f)
            return
        self.gui.fill(lst)
    
    def go_end(self):
        f = '[MClient] suggest.controller.Suggest.go_end'
        if not self.gui.model.items:
            sh.com.rep_lazy(f)
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


if __name__ == '__main__':
    f = '[MClientQt] suggest.controller.Suggest.__main__'
    sh.com.start()
    lst = []
    for i in range(20):
        lst.append(f'item {i+1}')
    app = Suggest()
    app.fill(lst)
    app.go_end()
    app.show()
    app.set_width(96)
    mes = _('Goodbye!')
    sh.objs.get_mes(f, mes, True).show_debug()
    sh.com.end()
