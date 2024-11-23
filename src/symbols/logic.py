#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep

from config import CONFIG


class Symbols:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.colnum = 10
        self.line = CONFIG.new['spec_syms']
        self.table = []
    
    def get(self, rowno, colno):
        f = '[MClient] symbols.logic.Symbols.get'
        try:
            return self.table[rowno][colno]
        except IndexError:
            rep.wrong_input(f)
            return ''
    
    def run(self):
        self.set_table()
        return self.table
    
    def set_table(self):
        f = '[MClient] symbols.logic.Symbols.set_table'
        if self.table:
            rep.lazy(f)
            return
        if not self.line or not self.colnum:
            rep.empty(f)
            return
        row = [self.line[0]]
        i = 1
        while i < len(self.line):
            row.append(self.line[i])
            i += 1
            if i % self.colnum == 0:
                self.table.append(row)
                row = []
        if row:
            delta = self.colnum - len(row)
            for no in range(delta):
                row.append('')
            self.table.append(row)
