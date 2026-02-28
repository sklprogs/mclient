#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from cells import Elems
from sources.dsl.get import ALL_DICS
from sources.dsl.run import Source

import tests.dump.shared
tests.dump.shared.ALL_DICS = ALL_DICS
tests.dump.shared.Source = Source


class Dump(tests.dump.shared.Dump):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.limit = 2
        #return self.run_loops(1)
        #return self.run_all()
        return self.run_blocks()