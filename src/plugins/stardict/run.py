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
    
    def __init__ (self,search='',url=''
                 ,timeout=6,Debug=False
                 ,articleid=0,iabbr=None
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #note: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self.values()
        self._search    = search
        self.Debug      = Debug
        self._articleid = articleid
        self.iabbr      = iabbr
    
    def values(self):
        self._text   = ''
        self._html   = ''
        self._blocks = []
        self._data   = []
    
    def run(self):
        iget       = gt.Get(self._search)
        self._text = iget.run()
        self._html = iget._html
        self._text = cu.CleanUp(self._text).run()
        if self._text is None:
            self._text = ''
        self._blocks = tg.Tags (text  = self._text
                               ,Debug = self.Debug
                               ).run()
        self._data = el.Elems (blocks    = self._blocks
                              ,articleid = self._articleid
                              ,iabbr     = self.iabbr
                              ).run()
        return self._data
        
