#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep


class Dsl:
    
    def __init__(self):
        from sources.dsl.get import ALL_DICS
        self.source = ALL_DICS
        self.report = []
    
    def add_report(self, dump):
        f = '[MClient] tests.dump.Dsl.add_report'
        self.report.append(f + ':')
        if not self.source.Success:
            rep.cancel(f)
            return
        if not dump:
            rep.empty(f)
            return
        #iarticles = dump[0:3] + dump[-3:]
        iarticles = [dump[0]] + [dump[-1]]
        for iarticle in iarticles:
            self.report.append(f'{iarticle.pos}: {iarticle.search} ({iarticle.dic})')
            self.report.append(iarticle.code)
        self.report.append('')
    
    def get_next(self, limit=1500):
        self.add_report(self.source.dump(limit))
    
    def run2(self):
        self.get_next(100)
        self.get_next(100)
    
    def run3(self):
        self.get_next(10)
        self.get_next(10)
        self.get_next(10)
    
    def run(self):
        self.run3()
        return '\n'.join(self.report)
        