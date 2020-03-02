#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared            as sh
import plugins.multitranbin.get     as gt
import plugins.multitranbin.tags    as tg
import plugins.multitranbin.elems   as el
from skl_shared.localize import _



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.multitranbin.get.PATH
              earlier.
        '''
        self.values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def values(self):
        self._blocks = []
        self._text   = ''
        self._html   = ''
    
    def get_text(self):
        if not self._text:
            iwrite = io.StringIO()
            for block in self._blocks:
                if block._text \
                and block._type in ('dic','wform','term'
                                   ,'comment','correction'
                                   ,'user'
                                   ):
                    iwrite.write(block._text)
            self._text = iwrite.getvalue()
            iwrite.close()
        return self._text
    
    def get_html(self):
        #TODO: elaborate
        self._html = self.get_text()
        return self._html
    
    def lang1(self):
        return gt.LANG1
    
    def lang2(self):
        return gt.LANG2
    
    # This is needed only for compliance with a general method
    def server(self):
        return ''
    
    # This is needed only for compliance with a general method
    def fix_raw_html(self):
        return ''
    
    # This is needed only for compliance with a general method
    def get_url(self,search=''):
        return ''
    
    def set_lang1(self,lang1=''):
        gt.LANG1 = lang1
    
    def set_lang2(self,lang2=''):
        gt.LANG2 = lang2
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    def langs1(self,lang2=''):
        #TODO: implement
        return(_('Any'),'English','Russian')
    
    def langs2(self,lang1=''):
        #TODO: implement
        return(_('Any'),'English','Russian')
    
    def combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def request(self,search='',url=''):
        iget   = gt.Get(search)
        chunks = iget.run()
        if not chunks:
            chunks = []
        self._blocks = []
        for chunk in chunks:
            blocks = tg.Tags (chunk   = chunk
                             ,Debug   = self.Debug
                             ,Shorten = self.Shorten
                             ,MaxRow  = self.MaxRow
                             ,MaxRows = self.MaxRows
                             ).run()
            if blocks:
                self._blocks += blocks
        self._blocks = el.Elems (blocks  = self._blocks
                                ,iabbr   = self.iabbr
                                ,langs   = gt.objs.all_dics().langs()
                                ,search  = search
                                ,Debug   = self.Debug
                                ,Shorten = self.Shorten
                                ,MaxRow  = self.MaxRow
                                ,MaxRows = self.MaxRows
                                ).run()
        self.get_text()
        self.get_html()
        return self._blocks
