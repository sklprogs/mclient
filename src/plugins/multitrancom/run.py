#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                       as sh
import sharedGUI                    as sg
import plugins.multitrancom.get     as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags    as tg
import plugins.multitrancom.elems   as el

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,timeout=6,iabbr=None
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20
                 ):
        self.values()
        self._timeout = timeout
        self.iabbr    = iabbr
        self.Debug    = Debug
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
    
    def values(self):
        self._html   = ''
        self._text   = ''
        self._blocks = []
        self._data   = []
    
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
    
    def request (self,search=''
                ,url='',articleid=1
                ):
        iget = gt.Get (search  = search
                      ,url     = url
                      ,timeout = self._timeout
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
                    block._url = gt.fix_url(block._url)
        self._data = el.Elems (blocks    = self._blocks
                              ,articleid = articleid
                              ,iabbr     = self.iabbr
                              ,Debug     = self.Debug
                              ,Shorten   = self.Shorten
                              ,MaxRow    = self.MaxRow
                              ,MaxRows   = self.MaxRows
                              ).run()
        return self._data
