#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                       as sh
import sharedGUI                    as sg
import plugins.multitrancom.get     as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags    as tg
import plugins.multitrancom.elems   as el
import plugins.multitrancom.pairs   as pr

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
    
    def server(self):
        return gt.URL
    
    def combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def fix_raw_html(self):
        return gt.com.fix_raw_html(self._html)
    
    def get_url(self,search):
        return gt.com.get_url(search)
    
    def set_pair(self,lang1,lang2):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_pair'
        if lang1 and lang2:
            if lang1 in pr.LANGS and lang2 in pr.LANGS:
                pr.LANG1 = lang1
                pr.LANG2 = lang2
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('Wrong input data!')
                            )
        else:
            sh.com.empty(f)
    
    def set_timeout(self,timeout=6):
        gt.TIMEOUT = timeout
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def langs1(self):
        return pr.objs.pairs().alive()
    
    def langs2(self,lang1):
        return pr.objs.pairs().pairs(lang1)
    
    def request(self,search='',url=''):
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
        self._blocks = el.Elems (blocks  = self._blocks
                                ,iabbr   = self.iabbr
                                ,search  = search
                                ,Debug   = self.Debug
                                ,Shorten = self.Shorten
                                ,MaxRow  = self.MaxRow
                                ,MaxRows = self.MaxRows
                                ).run()
        return self._blocks
