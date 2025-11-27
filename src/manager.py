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
        self.timeout = timeout
        self.load()
        self.plugin = self.mcplugin
        self.set_timeout(self.timeout)
    
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
    
    def suggest(self, search):
        f = '[MClient] manager.Sources.suggest'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.suggest(search)
    
    def get_offline_sources(self):
        return (self.sdplugin, self.lgplugin, self.mbplugin, self.frplugin
               ,self.mdplugin)
    
    def get_online_sources(self):
        return (self.mcplugin,)
    
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
        self.sdplugin = sources.stardict.run.Source()
        self.mcplugin = sources.multitrancom.run.Source()
        self.mbplugin = sources.multitrandem.run.Source()
        self.lgplugin = sources.dsl.run.Source()
        self.frplugin = sources.fora.run.Source()
        self.mdplugin = sources.mdic.run.Source()
    
    def get_text(self):
        f = '[MClient] manager.Sources.get_text'
        if not self.plugin:
            rep.empty(f)
            return
        return self.plugin.get_text()
    
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
