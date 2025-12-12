#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Input
from skl_shared.paths import Home
from skl_shared.list import List

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
import sources.multitrancom.pairs


class Sources:
    
    def __init__(self):
        self.sdsource = sources.stardict.run.Source()
        self.mcsource = sources.multitrancom.run.Source()
        self.mbsource = sources.multitrandem.run.Source()
        self.lgsource = sources.dsl.run.Source()
        self.frsource = sources.fora.run.Source()
        self.mdsource = sources.mdic.run.Source()
    
    def fix_url(self, url):
        ''' This method cannot be deleted yet, since it processes both article
            and cell URLs (required by mclient.App.go_url). Expanding and
            fixing URLs in place slows down loading an article.
            #NOTE: If there is more than 1 online source, methods processing
            URLs must be rewritten.
        '''
        return self.mcsource.fix_url(url)
    
    def quit(self):
        self.mbsource.quit()
        self.mcsource.quit()
        self.sdsource.quit()
        self.lgsource.quit()
        self.frsource.quit()
        self.mdsource.quit()
    
    def get_url(self, search):
        url = self.mcsource.get_url(search)
        if not url:
            return ''
        return url
    
    def get_langs(self):
        return sources.multitrancom.pairs.objs.get_pairs().get_alive()
    
    def suggest(self, search):
        lst = [self.sdsource.suggest(search), self.mcsource.suggest(search) \
              ,self.mbsource.suggest(search), self.lgsource.suggest(search) \
              ,self.frsource.suggest(search), self.mdsource.suggest(search)]
        return List([item for item in lst if item]).join_sublists()
    
    def get_offline_sources(self):
        return (self.sdsource, self.lgsource, self.mbsource, self.frsource
               ,self.mdsource)
    
    def get_online_sources(self):
        return (self.mcsource,)
    
    def request(self, search='', url=''):
        blocks = self.mcsource.request(search, url)
        blocks += self.sdsource.request(search, url)
        blocks += self.mbsource.request(search, url)
        blocks += self.lgsource.request(search, url)
        blocks += self.frsource.request(search, url)
        blocks += self.mdsource.request(search, url)
        return blocks
    
    def is_parallel(self):
        return self.sdsource.is_parallel() or self.mcsource.is_parallel() \
        or self.mbsource.is_parallel() or self.lgsource.is_parallel() \
        or self.frsource.is_parallel() or self.mdsource.is_parallel()
    
    def is_separate(self):
        return self.sdsource.is_separate() or self.mcsource.is_separate() \
        or self.mbsource.is_separate() or self.lgsource.is_separate() \
        or self.frsource.is_separate() or self.mdsource.is_separate()
    
    def get_subjects(self):
        # Get all available subjects (if any)
        dic = self.mcsource.get_subjects()
        if not dic:
            return {}
        return dic


f = '[MClient] manager.__main__'
if CONFIG.Success:
    SOURCES = Sources()
else:
    SOURCES = None
    rep.cancel(f)
