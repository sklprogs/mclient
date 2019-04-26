#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared                   as sh
import sharedGUI                as sg
import plugins.multitran.elems  as el
import plugins.multitranru.run  as mr
import plugins.multitrancom.run as mc

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        self.values()
        self.iabbr    = iabbr
        self.Debug    = Debug
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
        self.mrplugin = mr.Plugin (Debug   = self.Debug
                                  ,iabbr   = self.iabbr
                                  ,Shorten = self.Shorten
                                  ,MaxRow  = self.MaxRow
                                  ,MaxRows = self.MaxRows
                                  )
        self.mcplugin = mc.Plugin (Debug   = self.Debug
                                  ,iabbr   = self.iabbr
                                  ,Shorten = self.Shorten
                                  ,MaxRow  = self.MaxRow
                                  ,MaxRows = self.MaxRows
                                  )
    
    def values(self):
        self._html   = ''
        self._text   = ''
        ''' Basically there is no need to update 'self._blocks'; it is
            used for debugging only, but we already have debugging
            inside 'tags' modules.
        '''
        self._blocks = []
        self._data   = []
    
    def fix_raw_html(self):
        #todo: merge htmls
        code1 = self.mrplugin.fix_raw_html()
        code2 = self.mcplugin.fix_raw_html()
        if not code1:
            code1 = ''
        if not code2:
            code2 = ''
        return code1 + code2
    
    def get_url(self,search,Com=False):
        if Com:
            return self.mcplugin.get_url(search)
        else:
            return self.mrplugin.get_url(search)
    
    def set_pair(self,pair):
        self.mrplugin.set_pair(pair)
        self.mcplugin.set_pair(pair)
    
    def set_timeout(self,timeout=6):
        self.mrplugin.set_timeout(timeout)
        self.mcplugin.set_timeout(timeout)
    
    def accessible(self):
        return self.mrplugin.accessible() and self.mcplugin.accessible()
    
    def suggest(self,search):
        lst1 = self.mrplugin.suggest(search)
        lst2 = self.mcplugin.suggest(search)
        lst = [lst1,lst2]
        lst = [list(item) for item in lst if item]
        result = []
        for item in lst:
            result += item
        result = sh.List(lst1=result).duplicates_low()
        return sorted(result,key=lambda s:s.lower())
    
    def langs(self):
        return self.mrplugin.langs()
    
    def pairs(self):
        return self.mrplugin.pairs()
    
    def request (self,search=''
                ,url='',articleid=1
                ):
        ''' We cannot use the same URL for different plugins, so we
            create a plugin-specific URL.
        '''
        mrurl  = self.get_url(search)
        mcurl  = self.get_url(search,Com=True)
        mrdata = self.mrplugin.request (search    = search
                                       ,url       = mrurl
                                       ,articleid = articleid
                                       )
        mcdata = self.mcplugin.request (search    = search
                                       ,url       = mcurl
                                       ,articleid = articleid
                                       )
        if mrdata and mcdata:
            self._data = el.Elems (data1   = mrdata
                                  ,data2   = mcdata
                                  ,Debug   = self.Debug
                                  ,Shorten = self.Shorten
                                  ,MaxRow  = self.MaxRow
                                  ,MaxRows = self.MaxRows
                                  ).run()
        elif mrdata:
            self._data = mrdata
        elif mcdata:
            self._data = mcdata
        else:
            sh.com.empty(f)
        
        tmp = [self.mrplugin._text,self.mcplugin._text]
        tmp = [item for item in tmp if item]
        self._text = ' '.join(tmp)
        #todo: merge web-pages correctly
        tmp = [self.mrplugin._html,self.mcplugin._html]
        tmp = [item for item in tmp if item]
        self._html = ' '.join(tmp)
        return self._data
