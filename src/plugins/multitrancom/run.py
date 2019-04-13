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
    
    def __init__ (self,search='',url=''
                 ,timeout=6,Debug=False
                 ,articleid=1,iabbr=None
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        ''' Extra unused input variables are preserved so it would be
            easy to use an abstract class for all dictionary sources.
        '''
        self.values()
        self._search    = search
        self._url       = url
        self._timeout   = timeout
        self._articleid = articleid
        self.iabbr      = iabbr
        self.Debug      = Debug
        self.Shorten    = Shorten
        self.MaxRow     = MaxRow
        self.MaxRows    = MaxRows
    
    def values(self):
        self._html   = ''
        self._text   = ''
        self._blocks = []
        self._data   = []
    
    def run(self):
        iget = gt.Get (search  = self._search
                      ,url     = self._url
                      ,timeout = self._timeout
                      )
        self._text   = iget.run()
        self._html   = iget._html
        self._text   = cu.CleanUp(self._text).run()
        if self._text is None:
            self._text = ''
        self._blocks = tg.Tags (text    = self._text
                               ,Debug   = self.Debug
                               ,Shorten = self.Shorten
                               ,MaxRow  = self.MaxRow
                               ,MaxRows = self.MaxRows
                               ).run()
        self._data = el.Elems (blocks    = self._blocks
                              ,articleid = self._articleid
                              ,iabbr     = self.iabbr
                              ).run()
        return self._data
