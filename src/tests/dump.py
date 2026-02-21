#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep


class Dsl:
    
    def __init__(self):
        from sources.dsl.get import ALL_DICS
        self.source = ALL_DICS
        self.limit = 1500
        self.report = []
    
    def add_report(self, dump):
        f = '[MClient] tests.dump.Dsl.add_report'
        self.report.append(f + ':')
        if not self.source.Success:
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
        self.add_report(self.source.dump(self.limit))
    
    def run_loops(self, loops=1):
        for i in range(loops):
            self.get_next()
    
    def run_all(self):
        f = '[MClient] tests.dump.Dsl.run_all'
        while True:
            dump = self.source.dump(self.limit)
            if not dump:
                mes = _('All dictionaries have been dumped')
                Message(f, mes).show_info()
                return
            self.add_report(dump)
    
    def run(self):
        #self.limit = 1000
        #self.run_loops(2)
        self.run_all()
        return '\n'.join(self.report)
        