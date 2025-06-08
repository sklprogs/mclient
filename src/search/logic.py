#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message

from table.logic import Table as lgTable


class Search(lgTable):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def check(self):
        f = '[MClient] search.logic.Search.check'
        if not self.plain or not self.pattern.strip():
            self.Success = False
            rep.empty(f)
    
    def lower(self):
        f = '[MClient] search.logic.Search.lower'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.Case:
            self.pattern = self.pattern.lower()
            plain = []
            for row in self.plain:
                row = [item.lower() for item in row]
                plain.append(row)
            self.plain = plain
    
    def reset(self, plain, pattern, rowno, colno, Case=False):
        self.set_values()
        self.plain = plain
        self.pattern = pattern
        self.rowno = rowno
        self.colno = colno
        self.Case = Case
        self.check()
        self.set_size()
        self.lower()
    
    def set_values(self):
        self.plain = []
        self.Success = True
        self.Case = False
        self.rownum = 0
        self.colnum = 0
        self.rowno = 0
        self.colno = 0
        self.pattern = ''
    
    def _has_pattern(self):
        for rowno in range(self.rownum):
            for colno in range(self.colnum):
                if self.pattern in self.plain[rowno][colno]:
                    return True
    
    def search_next(self):
        f = '[MClient] search.logic.Search.search_next'
        if not self.Success:
            rep.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_next_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        Message(f, mes).show_debug()
        return(rowno, colno)
    
    def search_prev(self):
        f = '[MClient] search.logic.Search.search_prev'
        if not self.Success:
            rep.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_prev_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}. Text: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        Message(f, mes).show_debug()
        return(rowno, colno)
    
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
