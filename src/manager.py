#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared2.shared        as sh
import plugins.stardict.get
import plugins.stardict.run     as sdrun
import plugins.multitrancom.run as mcrun
import plugins.multitrandem.run as mbrun
from skl_shared2.localize import _


class Plugins:
    
    def __init__ (self,sdpath,mbpath
                 ,timeout=6,iabbr=None
                 ,Debug=False,Shorten=True
                 ,MaxRow=20,MaxRows=20
                 ):
        self.sdplugin = None
        self.mcplugin = None
        self.mbplugin = None
        self.plugin   = self.mcplugin
        #NOTE: change this upon the change of the default source
        self.source  = _('Multitran')
        self.sdpath  = sdpath
        self.mbpath  = sdpath
        self.timeout = timeout
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        self.load()
        ''' #NOTE: either put this on top of 'self.sources' or
            synchronize with GUI.
        '''
        self.set(self.source)
        self.set_timeout(self.timeout)
    
    def quit(self,event=None):
        self.mbplugin.quit()
        self.mcplugin.quit()
        self.sdplugin.quit()
    
    def get_lang1(self):
        f = '[MClient] manager.Plugins.get_lang1'
        if self.plugin:
            return self.plugin.get_lang1()
        else:
            sh.com.rep_empty(f)
    
    def get_lang2(self):
        f = '[MClient] manager.Plugins.get_lang2'
        if self.plugin:
            return self.plugin.get_lang2()
        else:
            sh.com.rep_empty(f)
    
    def is_combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        f = '[MClient] manager.Plugins.is_combined'
        if self.plugin:
            return self.plugin.is_combined()
        else:
            sh.com.rep_empty(f)
    
    def fix_raw_htm(self):
        f = '[MClient] manager.Plugins.fix_raw_htm'
        code = ''
        if self.plugin:
            code = self.plugin.fix_raw_htm()
            if not code:
                code = ''
        else:
            sh.com.rep_empty(f)
        return code
    
    def get_url(self,search):
        f = '[MClient] manager.Plugins.get_url'
        url = ''
        if self.plugin:
            url = self.plugin.get_url(search)
            if not url:
                url = ''
        else:
            sh.com.rep_empty(f)
        return url
    
    # Return all non-combined plugins
    def get_unique(self):
        return (self.sdplugin
               ,self.mcplugin
               ,self.mbplugin
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
            sh.com.rep_empty(f)
    
    def is_accessible(self):
        f = '[MClient] manager.Plugins.is_accessible'
        if self.plugin:
            return self.plugin.is_accessible()
        else:
            sh.com.rep_empty(f)
    
    def suggest(self,search):
        f = '[MClient] manager.Plugins.suggest'
        if self.plugin:
            return self.plugin.suggest(search)
        else:
            sh.com.rep_empty(f)
    
    def get_sources(self):
        return (_('Multitran')
               ,_('Stardict')
               ,_('Local MT')
               )
    
    def get_online_sources(self):
        ''' This is used by lg.Welcome to check the availability of
            online sources. Do not put combined sources here.
        '''
        return ['multitran.com']
    
    def get_langs1(self,lang2=''):
        f = '[MClient] manager.Plugins.get_langs1'
        if self.plugin:
            return self.plugin.get_langs1(lang2)
        else:
            sh.com.rep_empty(f)
    
    def get_langs2(self,lang1=''):
        f = '[MClient] manager.Plugins.get_langs2'
        if self.plugin:
            return self.plugin.get_langs2(lang1)
        else:
            sh.com.rep_empty(f)
    
    def load(self):
        plugins.stardict.get.PATH = self.sdpath
        plugins.stardict.get.objs.get_all_dics()
        plugins.multitrandem.get.PATH = self.mbpath
        plugins.multitrandem.get.objs.get_all_dics()
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
        self.mbplugin = mbrun.Plugin (Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
    
    def set(self,source):
        f = '[MClient] manager.Plugins.set'
        if source:
            self.source = source
            if source == _('Stardict'):
                self.plugin = self.sdplugin
            elif source in (_('Multitran'),'multitran.com'):
                self.plugin = self.mcplugin
            elif source == _('Local MT'):
                self.plugin = self.mbplugin
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(self.source,self.sources())
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
    def get_text(self):
        f = '[MClient] manager.Plugins.get_text'
        if self.plugin:
            return self.plugin.text
        else:
            sh.com.rep_empty(f)
    
    def get_htm(self):
        f = '[MClient] manager.Plugins.get_htm'
        if self.plugin:
            return self.plugin.htm
        else:
            sh.com.rep_empty(f)
    
    def request(self,search='',url=''):
        f = '[MClient] manager.Plugins.request'
        if self.plugin:
            return self.plugin.request (search = search
                                       ,url    = url
                                       )
        else:
            sh.com.rep_empty(f)
