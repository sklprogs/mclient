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
    
    def __init__ (self,search='',url=''
                 ,timeout=6,Debug=False
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #note: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self._html   = ''
        self._blocks = []
        self._search = search
        self.Debug   = Debug
    
    def run(self):
        iget         = gt.Get(self._search)
        text         = iget.run()
        self._html   = iget._html
        text         = cu.CleanUp(text).run()
        self._blocks = tg.Tags (text  = text
                               ,Debug = self.Debug
                               ).run()
        return self._blocks
        
