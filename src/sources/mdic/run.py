#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from sources.mdic.get import ALL_DICS
from sources.mdic.elems import Elems


class Source:
    
    def __init__(self):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.name = 'MClient (.mdic)'
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        #TODO: implement
        return []
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        ALL_DICS.close()
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def count_valid(self):
        return int(ALL_DICS.Success)
    
    def count_invalid(self):
        if self.count_valid():
            return 0
        else:
            return 1
    
    def suggest(self, search):
        #TODO: implement
        return []
    
    def request(self, search='', url=''):
        f = '[MClient] sources.mdic.run.Source.request'
        str_lst = ALL_DICS.search(search)
        blocks = Elems(str_lst).run()
        if not blocks:
            rep.empty(f)
            return []
        texts = [block.text for block in blocks]
        #TODO: Implement or drop
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return blocks
