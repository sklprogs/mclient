#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
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
        self.text = ''
        self.name = 'StarDict'
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_text(self):
        return self.text
    
    def get_subjects(self):
        return []
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def is_oneway(self):
        return False
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        for idic in gt.ALL_DICS.dics:
            idic.unload()
    
    def get_lang1(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_lang2(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_lang2(self, lang2=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def get_langs2(self, lang1=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def count_valid(self):
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        self.text = gt.ALL_DICS.get(search)
        self.text = cu.CleanUp(self.text).run()
        blocks = tg.Tags(self.text).run()
        ielems = el.Elems(blocks)
        self.blocks = ielems.run()
        self.Parallel = ielems.Parallel
        self.Separate = ielems.Separate
        return self.blocks
