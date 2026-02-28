#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from sources.stardict.get import ALL_DICS
from sources.stardict.run import Source

import tests.dump.shared
tests.dump.shared.ALL_DICS = ALL_DICS
tests.dump.shared.Source = Source


class Dump(tests.dump.shared.Dump):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run(self):
        self.limit = 2
        return self.run_loops(1)
        #return self.run_all()
        #return self.run_blocks()