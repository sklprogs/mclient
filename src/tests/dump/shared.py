#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from cells import Elems
# Do not forget to set these externally
ALL_DICS = None
Source = None


class Dump:
    
    def __init__(self):
        self.limit = 1500
        self.report = []
    
    def add_report(self, dump):
        f = '[MClient] tests.dump.shared.Dump.add_report'
        self.report.append(f + ':')
        if not ALL_DICS.Success:
            rep.cancel(f)
            return
        if not dump:
            # Dictionary length may be less than limit
            rep.lazy(f)
            return
        #iarticles = dump[0:3] + dump[-3:]
        iarticles = [dump[0]] + [dump[-1]]
        for iarticle in iarticles:
            self.report.append(f'{iarticle.pos}: {iarticle.search} ({iarticle.dic})')
            self.report.append(iarticle.code)
        self.report.append('')
    
    def get_next(self):
        self.add_report(ALL_DICS.dump(self.limit))
    
    def run_loops(self, loops=1):
        for i in range(loops):
            self.get_next()
        return '\n'.join(self.report)
    
    def run_all(self):
        f = '[MClient] tests.dump.shared.Dump.run_all'
        while True:
            dump = ALL_DICS.dump(self.limit)
            if not dump:
                mes = _('All dictionaries have been dumped')
                Message(f, mes).show_info()
                return '\n'.join(self.report)
            self.add_report(dump)
    
    def run_blocks(self):
        f = '[MClient] tests.dump.shared.Dump.run_blocks'
        self.report.append(f + ':')
        if not ALL_DICS.Success:
            rep.cancel(f)
            return
        articles = ALL_DICS.dump(1)
        if not articles:
            rep.empty(f)
            return
        blocks = Source().get_blocks(articles[0])
        if not blocks:
            rep.empty(f)
            return
        ielems = Elems(blocks)
        ielems.run()
        return ielems.debug()
    
    def run(self):
        #self.limit = 100
        #return self.run_loops(2)
        #return self.run_all()
        return self.run_blocks()
        