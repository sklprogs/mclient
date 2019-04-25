#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                   as sh
import sharedGUI                as sg
import plugins.stardict.get     as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags    as tg
import plugins.stardict.elems   as el

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #note: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self.values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def values(self):
        self._text   = ''
        self._html   = ''
        self._blocks = []
        self._data   = []
    
    # This is needed only for compliance with a general method
    def set_pair(self,pair=''):
        pass
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def encoding(self):
        return gt.ENCODING
    
    def langs(self):
        return gt.LANGS
    
    def pair_urls(self):
        return gt.PAIR_URLS
    
    def pairs(self):
        return gt.PAIRS
    
    def pair_root(self):
        return gt.PAIR_ROOT
    
    def root_url(self):
        return gt.URL
    
    def request (self,search='',url=''
                ,articleid=0
                ):
        iget       = gt.Get(search)
        self._text = iget.run()
        self._html = iget._html
        self._text = cu.CleanUp(self._text).run()
        if self._text is None:
            self._text = ''
        self._blocks = tg.Tags (text    = self._text
                               ,Debug   = self.Debug
                               ,Shorten = self.Shorten
                               ,MaxRow  = self.MaxRow
                               ,MaxRows = self.MaxRows
                               ).run()
        self._data = el.Elems (blocks    = self._blocks
                              ,articleid = articleid
                              ,iabbr     = self.iabbr
                              ).run()
        return self._data
