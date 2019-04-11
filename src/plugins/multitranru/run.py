#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                      as sh
import sharedGUI                   as sg
import plugins.multitranru.get     as gt
import plugins.multitranru.cleanup as cu
import plugins.multitranru.tags    as tg

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,search='',url=''
                 ,timeout=6,Debug=False
                 ):
        ''' Extra unused input variables are preserved so it would be
            easy to use an abstract class for all dictionary sources.
        '''
        self.values()
        self._search  = search
        self._url     = url
        self._timeout = timeout
        self.Debug    = Debug
    
    def values(self):
        self._html   = ''
        self._text   = ''
        self._blocks = []
    
    def run(self):
        iget = gt.Get (search  = self._search
                      ,url     = self._url
                      ,timeout = self._timeout
                      )
        self._text   = iget.run()
        self._html   = iget._html
        self._text   = cu.CleanUp(self._text).run()
        self._blocks = tg.Tags (text  = self._text
                               ,Debug = self.Debug
                               ).run()
        if self._text is None:
            self._text = ''
        return self._blocks
