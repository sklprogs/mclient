#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep
import sources.stardict.get as gt
import sources.stardict.cleanup as cu
import sources.stardict.tags as tg
import sources.stardict.elems as el


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
        self.name = 'StarDict'
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        return []
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        for idic in gt.ALL_DICS.dics:
            idic.unload()
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def count_valid(self):
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.ALL_DICS.suggest(search)
    
    def request(self, search):
        f = '[MClient] sources.stardict.run.Source.request'
        if not gt.ALL_DICS.dics:
            rep.lazy(f)
            return []
        self.blocks = []
        for article in gt.ALL_DICS.search(search):
            article.code = cu.CleanUp(article.code).run()
            self.blocks += tg.Tags(article).run()
        ielems = el.Elems(self.blocks)
        self.blocks = ielems.run()
        self.Parallel = ielems.Parallel
        self.Separate = ielems.Separate
        return self.blocks

    def get_blocks(self, article):
        f = '[MClient] sources.stardict.run.Source.get_blocks'
        if not article:
            rep.empty(f)
            return []
        article.code = cu.CleanUp(article.code).run()
        blocks = tg.Tags(article).run()
        return el.Elems(blocks).run()