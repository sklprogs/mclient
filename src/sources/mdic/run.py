#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List

from sources.mdic.get import ALL_DICS
from sources.mdic.elems import Elems


class Plugin:
    
    def __init__(self):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.majors = []
        self.minors = []
        self.htm = ''
        self.text = ''
        self.search = ''
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_speeches(self):
        return {}
    
    def get_minors(self):
        return self.minors
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
    def get_subjects(self):
        #TODO: implement
        return []
    
    def get_group_with_header(self, subject=''):
        #TODO: implement
        return []
    
    def get_majors(self):
        #TODO: implement
        return []
    
    def get_search(self):
        return self.search
    
    def set_htm(self, code):
        # This is needed only for compliance with a general method
        self.htm = code
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def is_oneway(self):
        return True
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        ALL_DICS.close()
    
    def get_lang1(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_lang2(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def fix_raw_htm(self, code=''):
        # This is needed only for compliance with a general method
        return self.htm
    
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
        f = '[MClient] sources.mdic.run.Plugin.request'
        self.search = search
        str_lst = ALL_DICS.search(self.search)
        blocks = Elems(str_lst).run()
        if not blocks:
            rep.empty(f)
            return []
        texts = [block.text for block in blocks]
        self.htm = self.text = List(texts).space_items()
        #TODO: Implement or drop
        #self.Parallel = ielems.Parallel
        #self.Separate = ielems.Separate
        return blocks
