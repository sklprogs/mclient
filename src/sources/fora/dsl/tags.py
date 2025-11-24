#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.table import Table

from instance import Block, Tag

from sources.dsl.tags import AnalyzeTag as DslAnalyzeTag
from sources.dsl.tags import Tags as DslTags


class AnalyzeTag(DslAnalyzeTag):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _is_subj(self):
        return False
    
    def _is_comment(self):
        ''' 'p' actually means 'subj', but DSL dictionaries are generally
            poorly converted to Fora.
        '''
        return self.tag.name in ('p', 'c', 'com', 'ex', 'i', 's')



class Tags(DslTags):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def assign(self):
        f = '[MClient] sources.fora.dsl.tags.Tags.assign'
        if not self.Success:
            rep.cancel(f)
            return
        for fragm in self.fragms:
            self.tags.append(AnalyzeTag(fragm).run())
        self.tags = [tag for tag in self.tags if tag]