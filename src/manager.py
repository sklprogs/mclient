#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Input
from skl_shared.paths import Home

from config import CONFIG, PRODUCT_LOW
from cells import Cells
import sources.stardict.get
import sources.dsl.get
import sources.stardict.run
import sources.multitrancom.run
import sources.multitrandem.run
import sources.dsl.run
import sources.fora.run
import sources.mdic.run


class Sources:
    
    def __init__(self, timeout=5.0):
        self.lgplugin = None
        self.mbplugin = None
        self.mcplugin = None
        self.sdplugin = None
        self.frplugin = None
        self.mdplugin = None
        self.fixed_urls = {}
        self.source = CONFIG.new['source']
        self.plugin = self.mcplugin
        self.timeout = timeout
        self.load()
        #NOTE: either put this on top of 'self.sources' or synchronize with GUI
        self.set(self.source)
        self.set_timeout(self.timeout)
    
    def get_fixed_urls(self):
        f = '[MClient] manager.Sources.get_fixed_urls'
        if not self.plugin:
            rep.empty(f)
            return {}
        return self.fixed_urls
    
    def get_speeches(self):
        f = '[MClient] manager.Sources.get_speeches'
        if not self.plugin:
            rep.empty(f)
            return {}
        return self.plugin.get_speeches()
    
    def get_majors(self):
        f = '[MClient] manager.Sources.get_majors'
        if not self.plugin:
            rep.empty(f)
            return []
        return self.plugin.get_majors()
    
    def get_minors(self):
        f = '[MClient] manager.Sources.get_minors'
        if not self.plugin:
            rep.empty(f)
            return []
        return self.plugin.get_minors()
    
    def get_search(self):
        f = '[MClient] manager.Sources.get_search'
        if not self.plugin:
            rep.empty(f)
            return ''
        return self.plugin.get_search()
    
    def fix_url(self, url):
        f = '[MClient] manager.Sources.fix_url'
        if not self.plugin:
            rep.empty(f)
            return url
        return self.plugin.fix_url(url)
    
    def is_oneway(self):
        f = '[MClient] manager.Sources.is_oneway'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_oneway()
    
    def quit(self):
        self.mbplugin.quit()
        self.mcplugin.quit()
        self.sdplugin.quit()
        self.lgplugin.quit()
        self.frplugin.quit()
        self.mdplugin.quit()
    
    def get_lang1(self):
        f = '[MClient] manager.Sources.get_lang1'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_lang1()
    
    def get_lang2(self):
        f = '[MClient] manager.Sources.get_lang2'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_lang2()
    
    def fix_raw_htm(self, code):
        f = '[MClient] manager.Sources.fix_raw_htm'
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
        f = '[MClient] manager.Sources.get_url'
        if not self.plugin:
            rep.empty(f)
            return ''
        url = self.plugin.get_url(search)
        if not url:
            return ''
        return url
    
    def get_unique(self):
        # Return all non-combined sources
        return (self.sdplugin, self.mcplugin, self.mbplugin, self.lgplugin
               ,self.frplugin)
    
    def set_lang1(self, lang1):
        self.plugin.set_lang1(lang1)
    
    def set_lang2(self, lang2):
        self.plugin.set_lang2(lang2)
    
    def set_timeout(self, timeout=5.0):
        f = '[MClient] manager.Sources.set_timeout'
        if not self.plugin:
            rep.empty(f)
            return
        self.plugin.set_timeout(timeout)
    
    def count_valid(self):
        f = '[MClient] manager.Sources.count_valid'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.count_valid()
    
    def count_invalid(self):
        f = '[MClient] manager.Sources.count_invalid'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.count_invalid()

    def suggest(self, search):
        f = '[MClient] manager.Sources.suggest'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.suggest(search)
    
    def get_sources(self):
        return (_('Multitran'), _('Stardict'), 'Lingvo (.dsl)', _('Local MT'), 'Fora', 'MClient (.mdic)')
    
    def get_offline_sources(self):
        return (_('Stardict'), 'Lingvo (.dsl)', _('Local MT'), 'Fora', 'MClient (.mdic)')
    
    def get_online_sources(self):
        ''' This is used by lg.Welcome to check the availability of online
            sources. Do not put combined sources here.
        '''
        return ['multitran.com']
    
    def get_langs1(self, lang2=''):
        f = '[MClient] manager.Sources.get_langs1'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_langs1(lang2)
    
    def get_langs2(self, lang1=''):
        f = '[MClient] manager.Sources.get_langs2'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_langs2(lang1)

    def load(self):
        self.sdplugin = sources.stardict.run.Plugin()
        self.mcplugin = sources.multitrancom.run.Plugin()
        self.mbplugin = sources.multitrandem.run.Plugin()
        self.lgplugin = sources.dsl.run.Plugin()
        self.frplugin = sources.fora.run.Plugin()
        self.mdplugin = sources.mdic.run.Plugin()
    
    def set(self, source):
        f = '[MClient] manager.Sources.set'
        if not source:
            rep.empty(f)
            return
        self.source = source
        if source == _('Stardict'):
            self.plugin = self.sdplugin
        elif source in (_('Multitran'), 'multitran.com'):
            self.plugin = self.mcplugin
        elif source == 'Lingvo (.dsl)':
            self.plugin = self.lgplugin
        elif source == _('Local MT'):
            self.plugin = self.mbplugin
        elif source == 'Fora':
            self.plugin = self.frplugin
        elif source == 'MClient (.mdic)':
            self.plugin = self.mdplugin
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.source, self.get_sources())
            Message(f, mes, True).show_error()
    
    def get_text(self):
        f = '[MClient] manager.Sources.get_text'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_text()
    
    def get_htm(self):
        f = '[MClient] manager.Sources.get_htm'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_htm()
    
    def request(self, search='', url=''):
        blocks = self.mcplugin.request(search, url)
        blocks += self.sdplugin.request(search, url)
        blocks += self.mbplugin.request(search, url)
        blocks += self.lgplugin.request(search, url)
        blocks += self.frplugin.request(search, url)
        blocks += self.mdplugin.request(search, url)
        return blocks
    
    def is_parallel(self):
        f = '[MClient] manager.Sources.is_parallel'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_parallel()
    
    def is_separate(self):
        f = '[MClient] manager.Sources.is_separate'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.is_separate()
    
    def get_subjects(self):
        # Get all available subjects (if any)
        f = '[MClient] manager.Sources.get_subjects'
        if not self.plugin:
            rep.empty(f)
            return {}
        dic = self.plugin.get_subjects()
        if not dic:
            return {}
        return dic


f = '[MClient] manager.__main__'
if CONFIG.Success:
    SOURCES = Sources(CONFIG.new['timeout'])
else:
    SOURCES = None
    rep.cancel(f)
