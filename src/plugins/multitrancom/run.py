#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                       as sh
import sharedGUI                    as sg
import plugins.multitrancom.get     as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags    as tg

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
        self._search   = search
        self._url      = url
        self._timeout  = timeout
        self.Debug     = Debug
    
    def run(self):
        iget = gt.Get (search  = self._search
                      ,url     = self._url
                      ,timeout = self._timeout
                      )
        text           = iget.run()
        self._html_raw = iget._html_raw
        text           = cu.CleanUp(text).run()
        self._blocks   = tg.Tags (text  = text
                                 ,Debug = self.Debug
                                 ).run()
        return self._blocks
