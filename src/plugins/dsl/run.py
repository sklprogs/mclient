#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List

import plugins.dsl.get as gt
import plugins.dsl.tags as tg
import plugins.dsl.elems as el
import plugins.dsl.cleanup as cu
import plugins.dsl.subjects as ds


class Plugin:
    
    def __init__(self, Debug=False, maxrow=20, maxrows=1000):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.dsl.get.PATH earlier.
        '''
        self.set_values()
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def set_values(self):
        ''' #NOTE: 'fixed_urls', 'art_subj', 'Parallel' and 'Separate' are
            temporary variables that should be externally referred to only
            after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.cells = []
        self.majors = []
        self.minors = []
        self.fixed_urls = {}
        self.art_subj = {}
        self.htm = ''
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
    
    def get_speeches(self):
        #TODO: implement
        return {}
    
    def get_minors(self):
        if not self.minors:
            #TODO: implement
            self.minors = []
        return self.minors
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
    def get_fixed_urls(self):
        return self.fixed_urls
    
    def get_article_subjects(self):
        return self.art_subj
    
    def get_majors(self):
        return ds.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    # This is needed only for compliance with a general method
    def set_htm(self, code):
        self.htm = code
    
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
        f = '[MClient] plugins.dsl.run.Plugin.get_lang1'
        lang = _(gt.LANG1)
        langs = self.get_langs1()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        mes = '"{}"'.format(lang)
        Message(f, mes).show_debug()
        return lang
    
    def get_lang2(self):
        f = '[MClient] plugins.dsl.run.Plugin.get_lang2'
        lang = _(gt.LANG2)
        langs = self.get_langs2()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        mes = '"{}"'.format(lang)
        Message(f, mes).show_debug()
        return lang
    
    def fix_raw_htm(self):
        # This is needed only for compliance with a general method
        return self.htm
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1=''):
        f = '[MClient] plugins.dsl.run.Plugin.set_lang1'
        if lang1 == _('Any'):
            rep.lazy(f)
        elif not lang1:
            rep.empty(f)
        else:
            lang1 = gt.objs.get_all_dics().get_code(lang1)
            gt.LANG1 = lang1
    
    def set_lang2(self, lang2=''):
        f = '[MClient] plugins.dsl.run.Plugin.set_lang2'
        if lang2 == _('Any'):
            rep.lazy(f)
        elif not lang2:
            rep.empty(f)
        else:
            lang2 = gt.objs.get_all_dics().get_code(lang2)
            gt.LANG2 = lang2
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        if lang2:
            return gt.objs.get_all_dics().get_pairs(lang2)
        else:
            return gt.objs.get_all_dics().get_langs1()
    
    def get_langs2(self, lang1=''):
        if lang1:
            return gt.objs.get_all_dics().get_pairs(lang1)
        else:
            return gt.objs.get_all_dics().get_langs2()
    
    def is_combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def is_accessible(self):
        return gt.com.is_accessible()
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        self.blocks = []
        htm = []
        self.search = search
        articles = gt.Get(search).run()
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            self.blocks += tg.Tags(code = code
                                  ,Debug = self.Debug
                                  ,maxrows = self.maxrows
                                  ,dicname = iarticle.dic).run()
        self.htm = '\n'.join(htm)
        texts = [block.text for block in self.blocks if block.text]
        self.text = List(texts).space_items()
        self.blocks = el.Elems(blocks = self.blocks
                              ,Debug = self.Debug).run()
        return self.blocks
