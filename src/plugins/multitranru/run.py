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
    
    def set_pair(self,pair):
        f = '[MClient] plugins.multitranru.run.Plugin.set_pair'
        if pair:
            if pair in gt.PAIRS:
                ind = gt.PAIRS.index(pair)
                if ind < len(gt.PAIR_URLS):
                    gt.PAIR = gt.PAIR_URLS[ind]
                else:
                    sh.objs.mes (f,_('ERROR')
                                ,_('The condition "%s" is not observed!')\
                                % ('0 <= ' + str(ind) + ' < %d' \
                                % len(gt.PAIR_URLS)
                                )
                                )
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                            % (str(pair),';'.join(gt.PAIRS))
                            )
        else:
            sh.com.empty(f)
    
    def set_timeout(self,timeout=6):
        gt.TIMEOUT = timeout
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def langs(self):
        return gt.LANGS
    
    def pairs(self):
        return gt.PAIRS
    
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
