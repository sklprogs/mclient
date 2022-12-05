#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Symbols:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.colnum = 10
        self.line = sh.lg.globs['str']['spec_syms']
        self.table = []
    
    def run(self):
        self.set_table()
        return self.table
    
    def set_table(self):
        f = '[MClientQt] symbols.logic.Symbols.set_table'
        if self.table:
            sh.com.rep_lazy(f)
            return
        if not self.line or not self.colnum:
            sh.com.rep_empty(f)
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
