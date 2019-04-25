#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                      as sh
import sharedGUI                   as sg
import plugins.multitranru.get     as gt
import plugins.multitranru.cleanup as cu
import plugins.multitranru.tags    as tg
import plugins.multitranru.elems   as el

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        self.values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def values(self):
        self._html   = ''
        self._text   = ''
        self._blocks = []
        self._data   = []
    
    def set_timeout(self,timeout=6):
        gt.TIMEOUT = timeout
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search,pair):
        return gt.Suggest(search,pair).run()
    
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
                ,articleid=1
                ):
        iget = gt.Get (search = search
                      ,url    = url
                      )
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
        if self._blocks:
            for block in self._blocks:
                # Prevent useless error output
                if block._url:
                    block._url = gt.com.fix_url(block._url)
        self._data = el.Elems (blocks    = self._blocks
                              ,articleid = articleid
                              ,iabbr     = self.iabbr
                              ,Debug     = self.Debug
                              ,Shorten   = self.Shorten
                              ,MaxRow    = self.MaxRow
                              ,MaxRows   = self.MaxRows
                              ).run()
        return self._data
