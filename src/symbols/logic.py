#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Symbols:
    
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        self.Success = True
        self.line = ''
        self.table = []
        self.rownum = 0
        self.colnum = 10
    
    def run(self):
        if not self.table:
            self.load()
            self.set_table()
        return self.table
    
    def load(self):
        f = '[MClientQt] symbols.logic.Symbols.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        #TODO: Load sh.lg.globs['str']['spec_syms']
        self.line = 'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ'
        if not self.line:
            self.Success = False
            sh.com.rep_out(f)
    
    def set_table(self):
        f = '[MClientQt] symbols.logic.Symbols.set_table'
        if not self.Success:
            sh.com.cancel(f)
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
