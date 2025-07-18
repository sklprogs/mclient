#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Input
from skl_shared.paths import Home

from config import CONFIG, PRODUCT_LOW
import plugins.stardict.get
import plugins.dsl.get
import plugins.stardict.run as sdrun
import plugins.multitrancom.run as mcrun
import plugins.multitrandem.run as mbrun
import plugins.dsl.run as lgrun


class Plugins:
    
    def __init__(self, sdpath, mbpath, timeout=5.0, Debug=False, maxrows=1000):
        self.set_values()
        self.Debug = Debug
        self.lgpath = sdpath
        self.maxrows = maxrows
        self.mbpath = sdpath
        self.plugin = self.mcplugin
        self.sdpath = sdpath
        self.timeout = timeout
        self.load()
        #NOTE: either put this on top of 'self.sources' or synchronize with GUI
        self.set(self.source)
        self.set_timeout(self.timeout)
    
    def set_values(self):
        self.lgplugin = None
        self.mbplugin = None
        self.mcplugin = None
        self.sdplugin = None
        self.source = CONFIG.new['source']
    
    def get_fixed_urls(self):
        f = '[MClient] manager.Plugins.get_fixed_urls'
        if not self.plugin:
            rep.empty(f)
            return {}
        return self.plugin.get_fixed_urls()
    
    def get_article_subjects(self):
        f = '[MClient] manager.Plugins.get_article_subjects'
        if not self.plugin:
            rep.empty(f)
            return {}
        return self.plugin.get_article_subjects()
    
    def get_speeches(self):
        f = '[MClient] manager.Plugins.get_speeches'
        if not self.plugin:
            rep.empty(f)
            return {}
        return self.plugin.get_speeches()
    
    def get_majors(self):
        f = '[MClient] manager.Plugins.get_majors'
        if not self.plugin:
            rep.empty(f)
            return []
        return self.plugin.get_majors()
    
    def get_minors(self):
        f = '[MClient] manager.Plugins.get_minors'
        if not self.plugin:
            rep.empty(f)
            return []
        return self.plugin.get_minors()
    
    def get_search(self):
        f = '[MClient] manager.Plugins.get_search'
        if not self.plugin:
            rep.empty(f)
            return ''
        return self.plugin.get_search()
    
    def fix_url(self, url):
        f = '[MClient] manager.Plugins.fix_url'
        if not self.plugin:
            rep.empty(f)
            return url
        return self.plugin.fix_url(url)
    
    def is_oneway(self):
        f = '[MClient] manager.Plugins.is_oneway'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_oneway()
    
    def quit(self):
        self.mbplugin.quit()
        self.mcplugin.quit()
        self.sdplugin.quit()
        self.lgplugin.quit()
    
    def get_lang1(self):
        f = '[MClient] manager.Plugins.get_lang1'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_lang1()
    
    def get_lang2(self):
        f = '[MClient] manager.Plugins.get_lang2'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_lang2()
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        f = '[MClient] manager.Plugins.is_combined'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_combined()
    
    def fix_raw_htm(self, code):
        f = '[MClient] manager.Plugins.fix_raw_htm'
        if not self.plugin:
            rep.empty(f)
            return code
        code = self.plugin.fix_raw_htm(code)
        code = Input(f, code).get_not_none()
        if not '</html>' in code.lower():
            search = self.get_search()
            # '.format' does not work properly for 'multitrandem'
            mes = '<!doctype html><title>'
            mes += search
            mes += '</title><body>'
            mes += code
            mes += '</body></html>'
            code = mes
        return code
    
    def get_url(self, search):
        f = '[MClient] manager.Plugins.get_url'
        if not self.plugin:
            rep.empty(f)
            return ''
        url = self.plugin.get_url(search)
        if not url:
            return ''
        return url
    
    def get_unique(self):
        # Return all non-combined plugins
        return (self.sdplugin, self.mcplugin, self.mbplugin, self.lgplugin)
    
    def set_lang1(self, lang1):
        self.plugin.set_lang1(lang1)
    
    def set_lang2(self, lang2):
        self.plugin.set_lang2(lang2)
    
    def set_timeout(self, timeout=5.0):
        f = '[MClient] manager.Plugins.set_timeout'
        if not self.plugin:
            rep.empty(f)
            return
        self.plugin.set_timeout(timeout)
    
    def is_accessible(self):
        f = '[MClient] manager.Plugins.is_accessible'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_accessible()

    def suggest(self, search):
        f = '[MClient] manager.Plugins.suggest'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.suggest(search)
    
    def get_sources(self):
        return (_('Multitran'), _('Stardict'), 'Lingvo (DSL)', _('Local MT'))
    
    def get_offline_sources(self):
        return (_('Stardict'), 'Lingvo (DSL)', _('Local MT'))
    
    def get_online_sources(self):
        ''' This is used by lg.Welcome to check the availability of online
            sources. Do not put combined sources here.
        '''
        return ['multitran.com']
    
    def get_langs1(self, lang2=''):
        f = '[MClient] manager.Plugins.get_langs1'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_langs1(lang2)
    
    def get_langs2(self, lang1=''):
        f = '[MClient] manager.Plugins.get_langs2'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_langs2(lang1)

    def load(self):
        plugins.stardict.get.PATH = self.sdpath
        plugins.dsl.get.PATH = self.lgpath
        plugins.multitrandem.get.PATH = self.mbpath
        plugins.stardict.get.objs.get_all_dics()
        plugins.dsl.get.objs.get_all_dics()
        plugins.multitrandem.get.objs.get_all_dics()
        self.sdplugin = sdrun.Plugin(Debug = self.Debug
                                    ,maxrows = self.maxrows)
        self.mcplugin = mcrun.Plugin(Debug = self.Debug
                                    ,maxrows = self.maxrows)
        self.mbplugin = mbrun.Plugin(Debug = self.Debug
                                    ,maxrows = self.maxrows)
        self.lgplugin = lgrun.Plugin(Debug = self.Debug
                                    ,maxrows = self.maxrows)
    
    def set(self, source):
        f = '[MClient] manager.Plugins.set'
        if not source:
            rep.empty(f)
            return
        self.source = source
        if source == _('Stardict'):
            self.plugin = self.sdplugin
        elif source in (_('Multitran'), 'multitran.com'):
            self.plugin = self.mcplugin
        elif source == 'Lingvo (DSL)':
            self.plugin = self.lgplugin
        elif source == _('Local MT'):
            self.plugin = self.mbplugin
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.source, self.get_sources())
            Message(f, mes, True).show_error()
    
    def get_text(self):
        f = '[MClient] manager.Plugins.get_text'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_text()
    
    def get_htm(self):
        f = '[MClient] manager.Plugins.get_htm'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_htm()
    
    def request(self, search='', url=''):
        f = '[MClient] manager.Plugins.request'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.request(search = search
                                  ,url = url)
    
    def is_parallel(self):
        f = '[MClient] manager.Plugins.is_parallel'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_parallel()
    
    def is_separate(self):
        f = '[MClient] manager.Plugins.is_separate'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_separate()
    
    def get_subjects(self):
        # Get all available subjects (if any)
        f = '[MClient] manager.Plugins.get_subjects'
        if not self.plugin:
            rep.empty(f)
            return {}
        dic = self.plugin.get_subjects()
        if not dic:
            return {}
        return dic


f = '[MClient] manager.__main__'
DICS = Home(PRODUCT_LOW).add_config('dics')
if CONFIG.Success:
    PLUGINS = Plugins(sdpath=DICS, mbpath=DICS, timeout=CONFIG.new['timeout']
                     ,Debug=False, maxrows=1000)
else:
    PLUGINS = None
    rep.cancel(f)
