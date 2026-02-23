#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from cells import Elems
from sources.dsl.run import Source as DslSource


class Dsl:
    
    def __init__(self):
        from sources.dsl.get import ALL_DICS
        self.all_dics = ALL_DICS
        self.limit = 1500
        self.report = []
    
    def add_report(self, dump):
        f = '[MClient] tests.dump.Dsl.add_report'
        self.report.append(f + ':')
        if not self.all_dics.Success:
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
        self.add_report(self.all_dics.dump(self.limit))
    
    def run_loops(self, loops=1):
        for i in range(loops):
            self.get_next()
        return '\n'.join(self.report)
    
    def run_all(self):
        f = '[MClient] tests.dump.Dsl.run_all'
        while True:
            dump = self.all_dics.dump(self.limit)
            if not dump:
                mes = _('All dictionaries have been dumped')
                Message(f, mes).show_info()
                return '\n'.join(self.report)
            self.add_report(dump)
    
    def dump(self):
        f = '[MClient] tests.dump.Dsl.dump'
        self.report.append(f + ':')
        articles = DslSource().dump(3)
        mes = []
        for article in articles:
            # sources.dsl.run.Source.dump already prevents adding empty articles
            ielems = Elems(article.blocks)
            mes.append(ielems.debug())
        return '\n'.join(mes)
    
    def run(self):
        #self.limit = 100
        #return self.run_loops(2)
        #return self.run_all()
        return self.dump()
        