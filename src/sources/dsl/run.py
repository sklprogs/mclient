#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

import sources.dsl.get as gt
import sources.dsl.tags as tg
import sources.dsl.elems as el
import sources.dsl.cleanup as cu


class Source:
    
    def __init__(self):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.blocks = []
        self.name = 'Lingvo (.dsl)'
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        #TODO: rework
        return {}
    
    # This is needed only for compliance with a general method
    def fix_url(self, url):
        return url
    
    # This is needed only for compliance with a general method
    def get_title(self, short):
        return short
    
    def quit(self):
        pass
        #TODO (?): Unload dictionaries
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def count_valid(self):
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        cu.FORA = False
        htm = []
        articles = gt.Get(search).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            self.blocks += tg.Tags(code).run()
        self.htm = '\n'.join(htm)
        texts = [block.text for block in self.blocks if block.text]
        self.blocks = el.Elems(self.blocks).run()
        return self.blocks
