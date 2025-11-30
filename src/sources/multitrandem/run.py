#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

import instance as ic

import sources.multitrandem.get as gt
import sources.multitrandem.tags as tg
import sources.multitrandem.elems as el


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
        #TODO: elaborate
        self.abbr = gt.FILES.get_subject()
        self.name = _('Multitran (offline)')
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        return []
    
    def fix_url(self, url=''):
        # This is needed only for compliance with a general method
        return url
    
    def quit(self):
        gt.FILES.close()
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def count_valid(self):
        return gt.com.count_valid()
    
    def count_invalid(self):
        return gt.com.count_invalid()
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        iget = gt.Get(search)
        chunks = iget.run()
        if not chunks:
            chunks = []
        for i in range(len(chunks)):
            blocks = tg.Tags(chunks[i], i).run()
            if blocks:
                self.blocks += blocks
        self.blocks = el.Elems(blocks=self.blocks, abbr=None
                              ,langs = gt.ALL_DICS.get_langs()
                              ,search=search).run()
        return self.blocks
