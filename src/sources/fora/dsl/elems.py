#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from sources.dsl.elems import Elems as DslElems


class Elems(DslElems):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_source(self):
        for block in self.blocks:
            block.source = 'Fora (DSL)'