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
    
    def count_valid(self):
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        self.blocks = []
        for article in gt.Get(search).run():
            article.code = cu.CleanUp(article.code).run()
            self.blocks += tg.Tags(article).run()
        self.blocks = el.Elems(self.blocks).run()
        return self.blocks
