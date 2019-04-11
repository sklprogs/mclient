#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                   as sh
import sharedGUI                as sg
import plugins.stardict.get     as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags    as tg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,path='',search='',url=''
                 ,timeout=6,Debug=False
                 ):
        ''' Extra unused input variables are preserved so it would be
            easy to use an abstract class for all dictionary sources.
        '''
        self._html_raw = ''
        self._blocks   = []
        self._path     = path
        self._search   = search
        self.Debug     = Debug
    
    def run(self):
        gt.PATH        = self._path
        iget           = gt.Get(self._search)
        text           = iget.run()
        self._html_raw = iget._html_raw
        text           = cu.CleanUp(text).run()
        itags          = tg.Tags(text)
        result         = itags.run()
        if result:
            self._blocks = itags._blocks
        if self.Debug:
            itags.debug_tags()
            itags.debug_blocks()
        return self._blocks
        
