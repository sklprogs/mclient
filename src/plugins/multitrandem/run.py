#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.multitrandem.get   as gt
import plugins.multitrandem.tags  as tg
import plugins.multitrandem.elems as el



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.multitrandem.get.PATH
              earlier.
        '''
        self.set_values()
        self.iabbr   = gt.objs.get_files().get_subject()
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
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
        self.blocks  = []
        self.text    = ''
        self.htm     = ''
        self.langloc = (_('English'),_('Russian'))
        self.langint = ('English','Russian')
    
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
        return ''
    
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
        iget   = gt.Get(search)
        chunks = iget.run()
        if not chunks:
            chunks = []
        self.blocks = []
        for chunk in chunks:
            blocks = tg.Tags (chunk   = chunk
                             ,Debug   = self.Debug
                             ,Shorten = self.Shorten
                             ,MaxRow  = self.MaxRow
                             ,MaxRows = self.MaxRows
                             ).run()
            if blocks:
                # Set speech for words only, not for phrases
                if iget.speech and not ' ' in search:
                    block = tg.Block()
                    block.select  = 0
                    block.type_    = 'wform'
                    block.text    = iget.spabbr
                    block.wforma  = iget.spabbr
                    block.wformaf = iget.speech
                    blocks.insert(0,block)
                self.blocks += blocks
        self.blocks = el.Elems (blocks  = self.blocks
                                ,iabbr   = self.iabbr
                                ,langs   = gt.objs.get_all_dics().get_langs()
                                ,search  = search
                                ,Debug   = self.Debug
                                ,Shorten = self.Shorten
                                ,MaxRow  = self.MaxRow
                                ,MaxRows = self.MaxRows
                                ).run()
        self.get_text()
        self.get_htm()
        return self.blocks
