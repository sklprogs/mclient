#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrandem.get as gt
import plugins.multitrandem.tags as tg
import plugins.multitrandem.elems as el
import plugins.multitrandem.subjects as sj



class Plugin:
    
    def __init__ (self,Debug=False
                 ,maxrow=20,maxrows=1000
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.multitrandem.get.PATH
              earlier.
        '''
        self.set_values()
        #TODO: elaborate
        self.abbr = gt.objs.get_files().get_subject()
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def get_subjects(self):
        return sj.objs.get_subjects().get_list()
    
    def get_group(self,subject=''):
        return sj.objs.get_subjects().get_group(subject)
    
    def get_majors(self):
        return sj.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    # This is needed only for compliance with a general method
    def set_htm(self,code):
        self.htm = code
    
    # This is needed only for compliance with a general method
    def fix_url(self,url):
        return url
    
    def is_oneway(self):
        return False
    
    def get_title(self,abbr):
        #TODO: implement
        return abbr
    
    def get_abbr(self,title):
        #TODO: implement
        return title
    
    def quit(self):
        gt.objs.get_files().close()
    
    def _adapt_lang(self,lang):
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
                mes = mes.format(lang,';'.join(modes))
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
        return 'English'
    
    def set_values(self):
        self.blocks = []
        self.htm = ''
        self.text = ''
        self.search = ''
        self.langint = ('English','Russian')
        self.langloc = (_('English'),_('Russian'))
    
    def get_text(self):
        if not self.text:
            iwrite = io.StringIO()
            for block in self.blocks:
                if block.text \
                and block.type_ in ('dic','wform','term'
                                   ,'comment','correction'
                                   ,'user'
                                   ):
                    iwrite.write(block.text)
            self.text = iwrite.getvalue()
            iwrite.close()
        return self.text
    
    def get_htm(self):
        #TODO: elaborate
        self.htm = self.get_text()
        return self.htm
    
    def get_lang1(self):
        return self._adapt_lang(gt.LANG1)
    
    def get_lang2(self):
        return self._adapt_lang(gt.LANG2)
    
    # This is needed only for compliance with a general method
    def get_server(self):
        return ''
    
    # This is needed only for compliance with a general method
    def fix_raw_htm(self):
        return self.htm
    
    # This is needed only for compliance with a general method
    def get_url(self,search=''):
        return ''
    
    def set_lang1(self,lang1=''):
        gt.LANG1 = self._adapt_lang(lang1)
        gt.objs.get_files().reset()
    
    def set_lang2(self,lang2=''):
        gt.LANG2 = self._adapt_lang(lang2)
        gt.objs.get_files().reset()
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    def get_langs1(self,lang2=''):
        #TODO: elaborate
        return(_('Any'),_('English'),_('Russian'))
    
    def get_langs2(self,lang1=''):
        #TODO: elaborate
        return(_('Any'),_('English'),_('Russian'))
    
    def is_combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def is_accessible(self):
        return gt.com.is_accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def request(self,search='',url=''):
        self.blocks = []
        self.search = search
        iget = gt.Get(search)
        chunks = iget.run()
        if not chunks:
            chunks = []
        for chunk in chunks:
            blocks = tg.Tags (chunk = chunk
                             ,Debug = self.Debug
                             ,maxrow = self.maxrow
                             ,maxrows = self.maxrows
                             ).run()
            if blocks:
                # Set speech for words only, not for phrases
                if iget.speech and not ' ' in search:
                    block = tg.Block()
                    block.select = 0
                    block.type_ = 'wform'
                    block.text = iget.spabbr
                    block.wform = iget.spabbr
                    block.wformf = iget.speech
                    blocks.insert(0,block)
                self.blocks += blocks
        self.blocks = el.Elems (blocks = self.blocks
                               ,abbr = None
                               ,langs = gt.objs.get_all_dics().get_langs()
                               ,search = search
                               ,Debug = self.Debug
                               ,maxrow = self.maxrow
                               ,maxrows = self.maxrows
                               ).run()
        self.get_text()
        self.get_htm()
        return self.blocks
