#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import plugins.stardict.get as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags as tg
import plugins.stardict.elems as el
import plugins.stardict.subjects as sj



class Plugin:
    
    def __init__(self, Debug=False, maxrows=1000):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.stardict.get.PATH earlier.
            - #NOTE: 'Parallel' and 'Separate' are temporary variables that
              should be externally referred to only after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.blocks = []
        self.majors = []
        self.minors = []
        self.htm = ''
        self.text = ''
        self.search = ''
        self.Debug = Debug
        self.maxrows = maxrows
    
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
        return sj.objs.get_subjects().get_list()
    
    def get_group_with_header(self, subject=''):
        return sj.objs.get_subjects().get_group_with_header(subject)
    
    def get_majors(self):
        return sj.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    def set_htm(self, code):
        # This is needed only for compliance with a general method
        self.htm = code
    
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
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        self.search = search
        self.htm = self.text = gt.Get(search).run()
        self.text = cu.CleanUp(self.text).run()
        blocks = tg.Tags(self.text).run()
        ielems = el.Elems(blocks)
        self.blocks = ielems.run()
        self.Parallel = ielems.Parallel
        self.Separate = ielems.Separate
        return self.blocks
