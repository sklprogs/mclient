#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

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
        self.source = sh.lg.globs['str']['source']
    
    def get_fixed_urls(self):
        f = '[MClient] manager.Plugins.get_fixed_urls'
        if not self.plugin:
            sh.com.rep_empty(f)
            return {}
        return self.plugin.get_fixed_urls()
    
    def get_article_subjects(self):
        f = '[MClient] manager.Plugins.get_article_subjects'
        if not self.plugin:
            sh.com.rep_empty(f)
            return {}
        return self.plugin.get_article_subjects()
    
    def get_speeches(self):
        f = '[MClient] manager.Plugins.get_speeches'
        if not self.plugin:
            sh.com.rep_empty(f)
            return {}
        return self.plugin.get_speeches()
    
    def get_majors(self):
        f = '[MClient] manager.Plugins.get_majors'
        if not self.plugin:
            sh.com.rep_empty(f)
            return []
        return self.plugin.get_majors()
    
    def get_minors(self):
        f = '[MClient] manager.Plugins.get_minors'
        if not self.plugin:
            sh.com.rep_empty(f)
            return []
        return self.plugin.get_minors()
    
    def expand_speech(self, short):
        f = '[MClient] manager.Plugins.expand_speech'
        if not self.plugin:
            sh.com.rep_empty(f)
            return short
        return self.plugin.expand_speech(short)
    
    def expand_subject(self, short):
        f = '[MClient] manager.Plugins.expand_subject'
        if not self.plugin:
            sh.com.rep_empty(f)
            return short
        return self.plugin.expand_subject(short)
    
    def get_search(self):
        f = '[MClient] manager.Plugins.get_search'
        if not self.plugin:
            sh.com.rep_empty(f)
            return ''
        return self.plugin.get_search()
    
    def set_htm(self, htm):
        f = '[MClient] manager.Plugins.set_htm'
        if not self.plugin or not htm:
            sh.com.rep_empty(f)
            return
        self.plugin.set_htm(htm)
    
    def fix_url(self, url):
        f = '[MClient] manager.Plugins.fix_url'
        if not self.plugin:
            sh.com.rep_empty(f)
            return url
        return self.plugin.fix_url(url)
    
    def is_oneway(self):
        f = '[MClient] manager.Plugins.is_oneway'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.is_oneway()
    
    def get_title(self, short):
        f = '[MClient] manager.Plugins.get_title'
        if not self.plugin:
            sh.com.rep_empty(f)
            return short
        return self.plugin.get_title(short)
    
    def quit(self):
        self.mbplugin.quit()
        self.mcplugin.quit()
        self.sdplugin.quit()
        self.lgplugin.quit()
    
    def get_lang1(self):
        f = '[MClient] manager.Plugins.get_lang1'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.get_lang1()
    
    def get_lang2(self):
        f = '[MClient] manager.Plugins.get_lang2'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.get_lang2()
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        f = '[MClient] manager.Plugins.is_combined'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.is_combined()
    
    def fix_raw_htm(self):
        f = '[MClient] manager.Plugins.fix_raw_htm'
        code = ''
        if self.plugin:
            code = self.plugin.fix_raw_htm()
        else:
            sh.com.rep_empty(f)
        code = sh.Input(f, code).get_not_none()
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
            sh.com.rep_empty(f)
            return ''
        url = self.plugin.get_url(search)
        if not url:
            return ''
        return url
    
    def get_unique(self):
        # Return all non-combined plugins
        return (self.sdplugin
               ,self.mcplugin
               ,self.mbplugin
               ,self.lgplugin
               )
    
    def set_lang1(self, lang1):
        self.plugin.set_lang1(lang1)
    
    def set_lang2(self, lang2):
        self.plugin.set_lang2(lang2)
    
    def set_timeout(self, timeout=5.0):
        f = '[MClient] manager.Plugins.set_timeout'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        self.plugin.set_timeout(timeout)
    
    def is_accessible(self):
        f = '[MClient] manager.Plugins.is_accessible'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.is_accessible()

    def suggest(self, search):
        f = '[MClient] manager.Plugins.suggest'
        if not self.plugin:
            sh.com.rep_empty(f)
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
            sh.com.rep_empty(f)
            return
        return self.plugin.get_langs1(lang2)
    
    def get_langs2(self, lang1=''):
        f = '[MClient] manager.Plugins.get_langs2'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.get_langs2(lang1)

    def load(self):
        plugins.stardict.get.PATH = self.sdpath
        plugins.dsl.get.PATH = self.lgpath
        plugins.multitrandem.get.PATH = self.mbpath
        plugins.stardict.get.objs.get_all_dics()
        plugins.dsl.get.objs.get_all_dics()
        plugins.multitrandem.get.objs.get_all_dics()
        self.sdplugin = sdrun.Plugin (Debug = self.Debug
                                     ,maxrows = self.maxrows
                                     )
        self.mcplugin = mcrun.Plugin (Debug = self.Debug
                                     ,maxrows = self.maxrows
                                     )
        self.mbplugin = mbrun.Plugin (Debug = self.Debug
                                     ,maxrows = self.maxrows
                                     )
        self.lgplugin = lgrun.Plugin (Debug = self.Debug
                                     ,maxrows = self.maxrows
                                     )
    
    def set(self, source):
        f = '[MClient] manager.Plugins.set'
        if not source:
            sh.com.rep_empty(f)
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
            sh.objs.get_mes(f, mes).show_error()
    
    def get_text(self):
        f = '[MClient] manager.Plugins.get_text'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.text
    
    def get_htm(self):
        f = '[MClient] manager.Plugins.get_htm'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.htm
    
    def request(self, search='', url=''):
        f = '[MClient] manager.Plugins.request'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.request (search = search
                                   ,url = url
                                   )
    
    def is_parallel(self):
        f = '[MClient] manager.Plugins.is_parallel'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.is_parallel()
    
    def is_separate(self):
        f = '[MClient] manager.Plugins.is_separate'
        if not self.plugin:
            sh.com.rep_empty(f)
            return
        return self.plugin.is_separate()
