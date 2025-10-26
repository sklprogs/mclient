#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

import plugins.multitrancom.get as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags as tg
import plugins.multitrancom.elems as el
import plugins.multitrancom.pairs as pr
import plugins.multitrancom.subjects as ms
import plugins.multitrancom.speech as sp



class Plugin:
    
    def __init__(self, Debug=False, maxrows=1000):
        ''' #NOTE: 'art_subj', 'Parallel' and 'Separate' are temporary
            variables that should be externally referred to only after getting
            a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.blocks = []
        self.majors = []
        self.minors = []
        self.art_subj = {}
        self.htm = ''
        self.text = ''
        self.search = ''
        self.Debug = Debug
        self.maxrows = maxrows
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
    def get_subjects(self):
        return ms.objs.get_subjects().get()
    
    def get_majors(self):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_majors'
        if not self.majors:
            result = ms.objs.get_groups().get_lists()
            if not result:
                rep.empty(f)
                return []
            self.majors, self.minors = result[0], result[1]
        return self.majors
    
    def get_minors(self):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_minors'
        if not self.minors:
            result = ms.objs.get_groups().get_lists()
            if not result:
                rep.empty(f)
                return []
            self.majors, self.minors = result[0], result[1]
        return self.minors
    
    def get_search(self):
        return self.search
    
    def fix_url(self, url):
        return gt.com.fix_url(url)
    
    def is_oneway(self):
        return False
    
    def quit(self):
        # This is needed only for compliance with a general method
        pass
    
    def get_lang1(self):
        return pr.LANG1
    
    def get_lang2(self):
        return pr.LANG2
    
    def fix_raw_htm(self, code):
        return gt.com.fix_raw_htm(code)
    
    def get_url(self, search):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_url'
        code1 = pr.objs.get_pairs().get_code(pr.LANG1)
        code2 = pr.objs.pairs.get_code(pr.LANG2)
        if not (code1 and code2 and search):
            rep.empty(f)
            return ''
        return gt.com.get_url(code1 = code1, code2 = code2, search = search)
    
    def set_lang1(self, lang1):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang1'
        if not lang1:
            rep.empty(f)
            return
        if lang1 in pr.LANGS:
            pr.LANG1 = lang1
        else:
            mes = _('Wrong input data: "{}"!').format(lang1)
            Message(f, mes, True).show_error()
    
    def set_lang2(self, lang2):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang2'
        if not lang2:
            rep.empty(f)
            return
        if lang2 in pr.LANGS:
            pr.LANG2 = lang2
        else:
            mes = _('Wrong input data: "{}"!').format(lang2)
            Message(f, mes, True).show_error()
    
    def set_timeout(self, timeout=6):
        gt.TIMEOUT = timeout
    
    def count_valid(self):
        return gt.com.count_valid()
    
    def count_invalid(self):
        if self.count_valid():
            return 0
        else:
            return 1
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def get_langs1(self, lang2=''):
        if lang2:
            return pr.objs.get_pairs().get_pairs1(lang2)
        else:
            return pr.objs.get_pairs().get_alive()
    
    def get_langs2(self, lang1=''):
        if lang1:
            return pr.objs.get_pairs().get_pairs2(lang1)
        else:
            return pr.objs.get_pairs().get_alive()
    
    def get_article_subjects(self):
        return self.art_subj
    
    def get_speeches(self):
        return sp.objs.get_speech().get_dic()
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def request(self, search='', url=''):
        self.search = search
        self.htm = gt.Get(search = search, url = url).run()
        code = cu.CleanUp(self.htm).run()
        blocks = tg.Tags(code).run()
        ielems = el.Elems(blocks)
        self.blocks = ielems.run()
        self.art_subj = ielems.art_subj
        self.Parallel = ielems.Parallel
        self.Separate = ielems.Separate
        return self.blocks
