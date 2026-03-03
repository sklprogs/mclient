#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep

from sources.fora.get import ALL_DICS
from sources.fora.run import Source

import tests.dump.shared
tests.dump.shared.ALL_DICS = ALL_DICS
tests.dump.shared.Source = Source


class Dump(tests.dump.shared.Dump):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run_index(self):
        f = '[MClient] tests.dump.fora.Dump.run_index'
        self.limit = 10
        if not ALL_DICS.dics:
            rep.lazy(f)
            return
        dic = ALL_DICS.dics[0]
        mes = []
        lines = dic.index.dump(self.limit)
        if not lines:
            rep.empty(f)
            return ''
        for line in lines:
            sub = _('"{}": position: {}, length: {}')
            sub = sub.format(line[0], line[1], line[2])
            mes.append(sub)
        return '\n'.join(mes)
    
    def run(self):
        self.limit = 10
        return self.run_loops(2)
        #return self.run_blocks()
        #return self.run_all()
        #return self.run_index()