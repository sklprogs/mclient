#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.dsl.get as gt
import plugins.dsl.tags as tg
import plugins.dsl.elems as el
import plugins.dsl.cleanup as cu


class Plugin:
    
    def __init__ (self,Debug=False
                 ,maxrow=20,maxrows=1000
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.dsl.get.PATH
              earlier.
        '''
        self.set_values()
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def set_values(self):
        self.blocks = []
        self.text = ''
        self.htm = ''
    
    def is_oneway(self):
        return True
    
    # This is needed only for compliance with a general method
    def is_abbr(self,abbr):
        return False
    
    # This is needed only for compliance with a general method
    def get_title(self,abbr):
        return abbr
    
    # This is needed only for compliance with a general method
    def get_abbr(self,title):
        return title
    
    def quit(self):
        pass
        #TODO (?): Unload dictionaries
    
    def get_lang1(self):
        return _(gt.LANG1)
    
    def get_lang2(self):
        return _(gt.LANG2)
    
    # This is needed only for compliance with a general method
    def get_server(self):
        return ''
    
    # This is needed only for compliance with a general method
    def fix_raw_htm(self):
        return ''
    
    # This is needed only for compliance with a general method
    def get_url(self,search=''):
        return ''
    
    def set_lang1(self,lang1=''):
        f = '[MClient] plugins.dsl.run.Plugin.set_lang1'
        if lang1 == _('Any'):
            sh.com.rep_lazy(f)
        else:
            lang1 = gt.objs.get_all_dics().get_code(lang1)
            gt.LANG1 = lang1
    
    def set_lang2(self,lang2=''):
        lang2 = gt.objs.get_all_dics().get_code(lang2)
        gt.LANG2 = lang2
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    def get_langs1(self,lang2=''):
        if lang2:
            pairs = gt.objs.get_all_dics().get_pairs(lang2)
        else:
            pairs = gt.objs.get_all_dics().get_langs()
        if pairs:
            return pairs
        else:
            return (_('Any'),)
    
    def get_langs2(self,lang1=''):
        pairs = gt.objs.get_all_dics().get_pairs(lang1)
        if pairs:
            return pairs
        else:
            return (_('Any'),)
    
    def is_combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def is_accessible(self):
        return gt.com.is_accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def request(self,search='',url=''):
        f = '[MClient] plugins.dsl.run.Plugin.request'
        articles = gt.Get(search).run()
        self.blocks = []
        htm = []
        for iarticle in articles:
            htm.append(iarticle.code)
            code = cu.CleanUp(iarticle.code).run()
            code = cu.TagLike(code).run()
            self.blocks += tg.Tags (code = code
                                   ,Debug = self.Debug
                                   ,maxrows = self.maxrows
                                   ,dicname = iarticle.dic
                                   ).run()
        self.htm = '\n'.join(htm)
        texts = [block.text for block in self.blocks if block.text]
        self.text = sh.List(texts).space_items()
        self.blocks = el.Elems (blocks = self.blocks
                               ,Debug = self.Debug
                               ).run()
        return self.blocks
