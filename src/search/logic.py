#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.logic import Text
from table.controller import TABLE


class Search:
    
    def __init__(self):
        self.set_values()
    
    def check(self):
        f = '[MClient] search.logic.Search.check'
        if not TABLE.logic.blocks or not Text(self.pattern).delete_line_breaks():
            self.Success = False
            rep.empty(f)
    
    def reset(self, pattern, Case=False):
        self.set_values()
        self.pattern = pattern
        self.Case = Case
        self.check()
    
    def set_values(self):
        self.Success = True
        self.Case = False
        self.pattern = ''
    
    def _search_sensitive(self, blocks):
        for block in blocks:
            if block.Ignore or block.Block:
                continue
            if self.pattern in block.text:
                return block
    
    def _search_insensitive(self, blocks):
        for block in blocks:
            if block.Ignore or block.Block:
                continue
            if self.pattern.lower() in block.text.lower():
                return block
    
    def _search(self, blocks):
        if self.Case:
            return self._search_sensitive(blocks)
        else:
            return self._search_insensitive(blocks)
    
    def search_start(self):
        f = '[MClient] search.logic.Search.search_start'
        if not self.Success:
            rep.cancel(f)
            return
        return self._search(TABLE.logic.blocks)
    
    def search_end(self):
        f = '[MClient] search.logic.Search.search_end'
        if not self.Success:
            rep.cancel(f)
            return
        return self._search(TABLE.logic.blocks[::-1])
    
    def search_next(self, ref_block):
        f = '[MClient] search.logic.Search.search_next'
        if not self.Success:
            rep.cancel(f)
            return
        if not ref_block:
            rep.empty(f)
            return
        try:
            pos = TABLE.logic.blocks.index(ref_block)
        except ValueError:
            rep.wrong_input(f)
            return
        return self._search(TABLE.logic.blocks[pos+1:])
    
    def search_prev(self, ref_block):
        f = '[MClient] search.logic.Search.search_prev'
        if not self.Success:
            rep.cancel(f)
            return
        if not ref_block:
            rep.empty(f)
            return
        try:
            pos = TABLE.logic.blocks.index(ref_block)
        except ValueError:
            rep.wrong_input(f)
            return
        return self._search(TABLE.logic.blocks[:pos-1][::-1])
    
    def _get_next_col(self, rowno, colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno, colno)
    
    def _get_prev_col(self, rowno, colno):
        while colno > 0:
            colno -= 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno, colno)
