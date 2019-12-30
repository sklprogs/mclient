#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
import plugins.stardict.get
import plugins.stardict.run     as sdrun
import plugins.multitrancom.run as mcrun
from skl_shared.localize import _


class Plugins:
    
    def __init__ (self,sdpath,timeout=6
                 ,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        self.sdplugin = None
        self.mcplugin = None
        self.plugin   = self.mcplugin
        #note: change this upon the change of the default source
        self._source  = _('Multitran')
        self._sdpath  = sdpath
        self._timeout = timeout
        self.Debug    = Debug
        self.iabbr    = iabbr
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
        self.load()
        ''' #note: either put this on top of 'self.sources' or
            synchronize with GUI.
        '''
        self.set(self._source)
        self.set_timeout(self._timeout)
    
    def lang1(self):
        f = '[MClient] manager.Plugins.lang1'
        if self.plugin:
            return self.plugin.lang1()
        else:
            sh.com.empty(f)
    
    def lang2(self):
        f = '[MClient] manager.Plugins.lang2'
        if self.plugin:
            return self.plugin.lang2()
        else:
            sh.com.empty(f)
    
    def combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        f = '[MClient] manager.Plugins.combined'
        if self.plugin:
            return self.plugin.combined()
        else:
            sh.com.empty(f)
    
    def fix_raw_html(self):
        f = '[MClient] manager.Plugins.fix_raw_html'
        code = ''
        if self.plugin:
            code = self.plugin.fix_raw_html()
            if not code:
                code = ''
        else:
            sh.com.empty(f)
        return code
    
    def get_url(self,search):
        f = '[MClient] manager.Plugins.get_url'
        url = ''
        if self.plugin:
            url = self.plugin.get_url(search)
            if not url:
                url = ''
        else:
            sh.com.empty(f)
        return url
    
    # Return all non-combined plugins
    def unique(self):
        return (self.sdplugin
               ,self.mcplugin
               )
    
    def set_lang1(self,lang1):
        self.plugin.set_lang1(lang1)
    
    def set_lang2(self,lang2):
        self.plugin.set_lang2(lang2)
    
    def set_timeout(self,timeout=6):
        f = '[MClient] manager.Plugins.set_timeout'
        if self.plugin:
            self.plugin.set_timeout(timeout)
        else:
            sh.com.empty(f)
    
    def accessible(self):
        f = '[MClient] manager.Plugins.accessible'
        if self.plugin:
            return self.plugin.accessible()
        else:
            sh.com.empty(f)
    
    def suggest(self,search):
        f = '[MClient] manager.Plugins.suggest'
        if self.plugin:
            return self.plugin.suggest(search)
        else:
            sh.com.empty(f)
    
    def sources(self):
        return (_('Multitran')
               ,_('Offline')
               )
    
    def online_sources(self):
        ''' This is used by lg.Welcome to check the availability of
            online sources. Do not put combined sources here.
        '''
        return ['multitran.com']
    
    def langs1(self,lang2=''):
        f = '[MClient] manager.Plugins.langs1'
        if self.plugin:
            return self.plugin.langs1(lang2)
        else:
            sh.com.empty(f)
    
    def langs2(self,lang1=''):
        f = '[MClient] manager.Plugins.langs2'
        if self.plugin:
            return self.plugin.langs2(lang1)
        else:
            sh.com.empty(f)
    
    def load(self):
        plugins.stardict.get.PATH = self._sdpath
        plugins.stardict.get.objs.all_dics()
        self.sdplugin = sdrun.Plugin (Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
        self.mcplugin = mcrun.Plugin (Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
    
    def set(self,source):
        f = '[MClient] manager.Plugins.set'
        if source:
            self._source = source
            if source == _('Offline'):
                self.plugin = self.sdplugin
            elif source in (_('Multitran'),'multitran.com'):
                self.plugin = self.mcplugin
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes(self._source,self.sources())
                sh.objs.mes(f,mes).error()
        else:
            sh.com.empty(f)
    
    def get_text(self):
        f = '[MClient] manager.Plugins.get_text'
        if self.plugin:
            return self.plugin._text
        else:
            sh.com.empty(f)
    
    def get_html(self):
        f = '[MClient] manager.Plugins.get_html'
        if self.plugin:
            return self.plugin._html
        else:
            sh.com.empty(f)
    
    def request(self,search='',url=''):
        f = '[MClient] manager.Plugins.request'
        if self.plugin:
            return self.plugin.request (search = search
                                       ,url    = url
                                       )
        else:
            sh.com.empty(f)
