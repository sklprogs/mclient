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
            self.set_size()
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
    
    def set_size(self):
        f = '[MClientQt] symbols.logic.Symbols.set_size'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.colnum:
            self.Success = False
            sh.com.rep_empty(f)
            return
        rownum = len(self.line) / 10
        if rownum % 10 == 0:
            rownum += 1
        self.rownum = rownum
        mes = _('Table size: {}×{}').format(self.rownum,self.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_table(self):
        f = '[MClientQt] symbols.logic.Symbols.set_table'
        if not self.Success:
            sh.com.cancel(f)
            return
        row = []
        for i in range(len(self.line)):
            row.append(self.line[i])
            if i % self.colnum == 0 and i > 0:
                self.table.append(row)
                row = []
        if row:
            delta = self.colnum - len(row)
            for no in range(delta):
                row.append('')
            self.table.append(row)
