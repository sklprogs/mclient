#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from plugins.fora.get import Get, ALL_DICS
import plugins.fora.stardict0.cleanup
import plugins.fora.stardict0.elems
import plugins.stardict.cleanup
import plugins.stardict.tags
import plugins.stardict.elems


class Plugin:
    
    def __init__(self, Debug=False, maxrows=1000):
        ''' Extra unused input variables are preserved so it would be easy to
            use an abstract class for all dictionary sources.
        '''
        self.set_values()
        self.Debug = Debug
        self.maxrows = maxrows
    
    def set_values(self):
        ''' #NOTE: 'fixed_urls', 'art_subj', 'Parallel' and 'Separate' are
            temporary variables that should be externally referred to only
            after getting a NEW article.
        '''
        self.Parallel = False
        self.Separate = False
        self.majors = []
        self.minors = []
        self.fixed_urls = {}
        self.art_subj = {}
        self.htm = ''
        self.text = ''
        self.search = ''
    
    def is_parallel(self):
        return self.Parallel
    
    def is_separate(self):
        return self.Separate
    
    def get_speeches(self):
        return {}
    
    def get_minors(self):
        return self.minors
    
    def get_fixed_urls(self):
        return self.fixed_urls
    
    def get_htm(self):
        return self.htm
    
    def get_text(self):
        return self.text
    
    def get_article_subjects(self):
        return self.art_subj
    
    def get_subjects(self):
        #TODO: implement
        return []
    
    def get_group_with_header(self, subject=''):
        #TODO: implement
        return []
    
    def get_majors(self):
        #TODO: implement
        return []
    
    def get_search(self):
        return self.search
    
    def set_htm(self, code):
        # This is needed only for compliance with a general method
        self.htm = code
    
    def fix_url(self, url):
        # This is needed only for compliance with a general method
        return url
    
    def is_oneway(self):
        return True
    
    def get_title(self, short):
        #TODO: implement
        return short
    
    def quit(self):
        ALL_DICS.close()
    
    def get_lang1(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_lang2(self):
        # This is needed only for compliance with a general method
        return _('Any')
    
    def get_server(self):
        # This is needed only for compliance with a general method
        return ''
    
    def fix_raw_htm(self, code=''):
        # This is needed only for compliance with a general method
        return self.htm
    
    def get_url(self, search=''):
        # This is needed only for compliance with a general method
        return ''
    
    def set_lang1(self, lang1=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_lang2(self, lang2=''):
        # This is needed only for compliance with a general method
        pass
    
    def set_timeout(self, timeout=0):
        # This is needed only for compliance with a general method
        pass
    
    def get_langs1(self, lang2=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def get_langs2(self, lang1=''):
        # This is needed only for compliance with a general method
        return(_('Any'),)
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        return True
    
    def is_accessible(self):
        return len(ALL_DICS.dics)
    
    def suggest(self, search):
        #TODO: implement
        return []
    
    def request(self, search='', url=''):
        f = '[MClient] plugins.fora.run.Plugin.request'
        self.search = search
        text = ALL_DICS.search(self.search)
        text = plugins.stardict.cleanup.CleanUp(text).run()
        blocks = plugins.stardict.tags.Tags(text).run()
        ielems = plugins.stardict.elems.Elems(blocks)
        self.htm = self.text = text
        cells = ielems.run()
        self.fixed_urls = ielems.fixed_urls
        self.art_subj = ielems.art_subj
        self.Parallel = ielems.Parallel
        self.Separate = ielems.Separate
        return cells
