#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from table.controller import TABLE
from search.logic import Search as lgSearch
from search.gui import Search as guiSearch


class Search:
    
    def __init__(self):
        self.Shown = False
        self.logic = lgSearch()
        self.gui = guiSearch()
        self.set_bindings()
        self.gui.ent_src.focus()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
    
    def clear(self):
        self.gui.clear()
        self.show()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def show(self):
        self.Shown = True
        self.gui.show()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.ent_src.bind(('Return',), self.close)
        self.gui.btn_srp.set_action(self.search_prev)
        self.gui.btn_srn.set_action(self.search_next)
        self.gui.btn_cls.action = self.close
        self.gui.btn_clr.action = self.clear
        self.gui.btn_cls.set_action()
        self.gui.btn_clr.set_action()
        self.gui.sig_close.connect(self.close)
    
    def reset(self):
        print('ent_src:', self.gui.ent_src.get())
        print('cbx_cas:', self.gui.cbx_cas.get())
        self.logic.reset(self.gui.ent_src.get(), self.gui.cbx_cas.get())
    
    def search_next(self):
        f = '[MClient] search.controller.Search.search_next'
        self.reset()
        ref_block = TABLE.get_selected_block()
        if not ref_block:
            rep.empty(f)
            return
        block_start = self.logic.search_start()
        block_next = self.logic.search_next(ref_block)
        if not block_start:
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        if not block_next:
            mes = _('The end has been reached. Searching from the start.')
            Message(f, mes, True).show_info()
            TABLE.select(block_start)
            return
        TABLE.select(block_next)
    
    def search_prev(self):
        f = '[MClient] search.controller.Search.search_prev'
        self.reset()
        ref_block = TABLE.get_selected_block()
        if not ref_block:
            rep.empty(f)
            return
        block_end = self.logic.search_end()
        block_prev = self.logic.search_prev(ref_block)
        if not block_end:
            mes = _('No matches!')
            Message(f, mes, True).show_info()
            return
        if not block_prev:
            mes = _('The start has been reached. Searching from the end.')
            Message(f, mes, True).show_info()
            TABLE.select(block_end)
            return
        TABLE.select(block_prev)


SEARCH = Search()