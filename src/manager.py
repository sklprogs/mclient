#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

import plugins.stardict.get
import plugins.stardict.run     as sdrun
import plugins.multitranru.run  as mrrun
import plugins.multitrancom.run as mcrun



class Plugins:
    
    def __init__ (self,sdpath,timeout=6
                 ,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        self.sdplugin = None
        self.mrplugin = None
        self.mcplugin = None
        self.plugin   = self.mrplugin
        self._source  = 'multitran.ru'
        self._sdpath  = sdpath
        self._timeout = timeout
        self.Debug    = Debug
        self.iabbr    = iabbr
        self.Shorten  = Shorten
        self.MaxRow   = MaxRow
        self.MaxRows  = MaxRows
        self.load()
        #note: this should be synchronized with GUI
        self.set('multitran.ru')
    
    def sources(self):
        return ('multitran.ru'
               ,'multitran.com'
               ,_('Offline')
               )
    
    def online_sources(self):
        return('multitran.ru','multitran.com')
    
    def online_urls(self):
        old = self._source
        self.set('multitran.ru')
        url1 = self.root_url()
        self.set('multitran.com')
        url2 = self.root_url()
        self._source = old
        self.set(self._source)
        return(url1,url2)
    
    def encoding(self):
        f = '[MClient] manager.Plugins.encoding'
        if self.plugin:
            return self.plugin.encoding()
        else:
            sh.com.empty(f)
    
    def root_url(self):
        f = '[MClient] manager.Plugins.root_url'
        if self.plugin:
            return self.plugin.root_url()
        else:
            sh.com.empty(f)
    
    def pair_urls(self):
        f = '[MClient] manager.Plugins.pair_urls'
        if self.plugin:
            return self.plugin.pair_urls()
        else:
            sh.com.empty(f)
    
    def pairs(self):
        f = '[MClient] manager.Plugins.pairs'
        if self.plugin:
            return self.plugin.pairs()
        else:
            sh.com.empty(f)
    
    def pair_root(self):
        f = '[MClient] manager.Plugins.pair_root'
        if self.plugin:
            return self.plugin.pair_root()
        else:
            sh.com.empty(f)
    
    def langs(self):
        f = '[MClient] manager.Plugins.langs'
        if self.plugin:
            return self.plugin.langs()
        else:
            sh.com.empty(f)
    
    def load(self):
        plugins.stardict.get.PATH = self._sdpath
        plugins.stardict.get.objs.all_dics()
        self.sdplugin = sdrun.Plugin (timeout = self._timeout
                                     ,Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
        self.mrplugin = mrrun.Plugin (timeout = self._timeout
                                     ,Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
        self.mcplugin = mcrun.Plugin (timeout = self._timeout
                                     ,Debug   = self.Debug
                                     ,iabbr   = self.iabbr
                                     ,Shorten = self.Shorten
                                     ,MaxRow  = self.MaxRow
                                     ,MaxRows = self.MaxRows
                                     )
    
    def sdstat(self):
        return len(plugins.stardict.get.objs.all_dics()._dics)
    
    def set(self,source):
        f = '[MClient] manager.Plugins.set'
        if source:
            self._source = source
            if source == _('Offline'):
                self.plugin = self.sdplugin
            elif source == 'multitran.ru':
                self.plugin = self.mrplugin
            elif source == 'multitran.com':
                self.plugin = self.mcplugin
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                            % (str(self._source),';'.join(self.sources()))
                            )
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
    
    def request (self,search=''
                ,url='',articleid=1
                ):
        f = '[MClient] manager.Plugins.request'
        if self.plugin:
            return self.plugin.request (search    = search
                                       ,url       = url
                                       ,articleid = articleid
                                       )
        else:
            sh.com.empty(f)
