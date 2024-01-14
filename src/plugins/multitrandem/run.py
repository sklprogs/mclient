#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic

import plugins.multitrandem.get as gt
import plugins.multitrandem.tags as tg
import plugins.multitrandem.elems as el
import plugins.multitrandem.subjects as sj



class Plugin:
    
    def __init__(self, Debug=False, maxrows=1000):
        ''' - Extra unused input variables are preserved so it would be easy to
              use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.multitrandem.get.PATH
              earlier.
        '''
        self.set_values()
        #TODO: elaborate
        self.abbr = gt.objs.get_files().get_subject()
        self.Debug = Debug
        self.maxrows = maxrows
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_speeches(self):
        #TODO: implement or rework
        return {}
    
    def get_fixed_urls(self):
        return self.fixed_urls
    
    def get_htm(self):
        return self.htm
    
    def get_article_subjects(self):
        return self.art_subj
    
    def get_subjects(self):
        return sj.objs.get_subjects().get_list()
    
    def get_majors(self):
        return sj.objs.get_subjects().get_majors()
    
    def get_minors(self):
        return self.minors
    
    def get_search(self):
        return self.search
    
    def set_htm(self, code):
        # This is needed only for compliance with a general method
        self.htm = code
    
    def fix_url(self, url=''):
        # This is needed only for compliance with a general method
        return url
    
    def is_oneway(self):
        return False
    
    def quit(self):
        gt.objs.get_files().close()
    
    def _adapt_lang(self, lang):
        f = '[MClient] plugins.multitrandem.run.Plugin._adapt_lang'
        if lang:
            if lang in self.langloc:
                ind = self.langloc.index(lang)
                return self.langint[ind]
            elif lang in self.langint:
                ind = self.langint.index(lang)
                return self.langloc[ind]
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                modes = self.langloc + self.langint
                mes = mes.format(lang, ';'.join(modes))
                sh.objs.get_mes(f, mes).show_error()
        else:
            sh.com.rep_empty(f)
        return 'English'
    
    def set_values(self):
        ''' #NOTE: 'fixed_urls', 'art_subj', 'Parallel' and 'Separate' are
            temporary variables that should be externally referred to only
            after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.langint = ('English', 'Russian')
        self.langloc = (_('English'), _('Russian'))
        self.cells = []
        self.majors = []
        self.minors = []
        self.fixed_urls = {}
        self.art_subj = {}
        self.htm = ''
        self.search = ''
    
    def get_text(self):
        mes = []
        if not self.text:
            for block in self.blocks:
                if block.text and block.type in ('dic', 'wform', 'term'
                                                ,'comment', 'correction'
                                                ,'user'
                                                ):
                    mes.append(block.text)
            self.text = ''.join(mes)
        return self.text
    
    def get_lang1(self):
        return self._adapt_lang(gt.LANG1)
    
    def get_lang2(self):
        return self._adapt_lang(gt.LANG2)
    
    def fix_raw_htm(self, code=''):
        # This is needed only for compliance with a general method
        return self.htm
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1):
        gt.LANG1 = self._adapt_lang(lang1)
        gt.objs.get_files().reset()
    
    def set_lang2(self, lang2):
        gt.LANG2 = self._adapt_lang(lang2)
        gt.objs.get_files().reset()
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        #TODO: elaborate
        return(_('Any'), _('English'), _('Russian'))
    
    def get_langs2(self, lang1=''):
        #TODO: elaborate
        return(_('Any'), _('English'), _('Russian'))
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        return False
    
    def is_accessible(self):
        return gt.com.is_accessible()
    
    def suggest(self, search):
        return gt.Suggest(search).run()
    
    def request(self, search='', url=''):
        self.blocks = []
        self.search = search
        iget = gt.Get(search)
        chunks = iget.run()
        if not chunks:
            chunks = []
        for chunk in chunks:
            blocks = tg.Tags(chunk).run()
            if blocks:
                # Set speech for words only, not for phrases
                if iget.speech and not ' ' in search:
                    block = ic.Block()
                    block.select = 0
                    block.type = 'wform'
                    block.text = iget.spabbr
                    block.wform = iget.spabbr
                    block.wformf = iget.speech
                    blocks.insert(0, block)
                self.blocks += blocks
        self.cells = el.Elems (blocks = self.blocks
                              ,abbr = None
                              ,langs = gt.objs.get_all_dics().get_langs()
                              ,search = search
                              ).run()
        self.get_text()
        self.get_htm()
        return self.cells
