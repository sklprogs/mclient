#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List

import sources.dsl.get as gt
import sources.dsl.tags as tg
import sources.dsl.elems as el
import sources.dsl.cleanup as cu
import sources.dsl.subjects as ds


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
        self.majors = []
        self.minors = []
        self.text = ''
        self.search = ''
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_subjects(self):
        #TODO: rework
        #return ds.objs.get_subjects().get_list()
        return {}
    
    def get_minors(self):
        if not self.minors:
            #TODO: implement
            self.minors = []
        return self.minors
    
    def get_text(self):
        return self.text
    
    def get_majors(self):
        return ds.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    # This is needed only for compliance with a general method
    def fix_url(self, url):
        return url
    
    def is_oneway(self):
        return True
    
    # This is needed only for compliance with a general method
    def get_title(self, short):
        return short
    
    def quit(self):
        pass
        #TODO (?): Unload dictionaries
    
    def get_lang1(self):
        f = '[MClient] sources.dsl.run.Source.get_lang1'
        lang = _(gt.LANG1)
        langs = self.get_langs1()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        Message(f, f'"{lang}"').show_debug()
        return lang
    
    def get_lang2(self):
        f = '[MClient] sources.dsl.run.Source.get_lang2'
        lang = _(gt.LANG2)
        langs = self.get_langs2()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        Message(f, f'"{lang}"').show_debug()
        return lang
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1=''):
        f = '[MClient] sources.dsl.run.Source.set_lang1'
        if lang1 == _('Any'):
            rep.lazy(f)
        elif not lang1:
            rep.empty(f)
        else:
            lang1 = gt.ALL_DICS.get_code(lang1)
            gt.LANG1 = lang1
    
    def set_lang2(self, lang2=''):
        f = '[MClient] sources.dsl.run.Source.set_lang2'
        if lang2 == _('Any'):
            rep.lazy(f)
        elif not lang2:
            rep.empty(f)
        else:
            lang2 = gt.ALL_DICS.get_code(lang2)
            gt.LANG2 = lang2
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        if lang2:
            return gt.ALL_DICS.get_pairs(lang2)
        else:
            return gt.ALL_DICS.get_langs1()
    
    def get_langs2(self, lang1=''):
        if lang1:
            return gt.ALL_DICS.get_pairs(lang1)
        else:
            return gt.ALL_DICS.get_langs2()
    
    def count_valid(self):
        return len(gt.ALL_DICS.get_valid())
    
    def count_invalid(self):
        return len(gt.ALL_DICS.get_invalid())
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        cu.FORA = False
        htm = []
        self.search = search
        articles = gt.Get(search).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            self.blocks += tg.Tags(code).run()
        self.htm = '\n'.join(htm)
        texts = [block.text for block in self.blocks if block.text]
        self.text = List(texts).space_items()
        self.blocks = el.Elems(self.blocks).run()
        return self.blocks
