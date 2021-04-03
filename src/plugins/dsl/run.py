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
    
    # This is needed only for compliance with a general method
    def fix_url(self,url):
        return url
    
    def is_oneway(self):
        return True
    
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
        f = '[MClient] plugins.dsl.run.Plugin.get_lang1'
        lang = _(gt.LANG1)
        langs = self.get_langs1()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        mes = '"{}"'.format(lang)
        sh.objs.get_mes(f,mes,True).show_debug()
        return lang
    
    def get_lang2(self):
        f = '[MClient] plugins.dsl.run.Plugin.get_lang2'
        lang = _(gt.LANG2)
        langs = self.get_langs2()
        if langs:
            # Ignore a default language if it is not available
            if not lang in langs:
                lang = langs[0]
        else:
            lang = (_('Any'),)
        mes = '"{}"'.format(lang)
        sh.objs.get_mes(f,mes,True).show_debug()
        return lang
    
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
        elif not lang1:
            sh.com.rep_empty(f)
        else:
            lang1 = gt.objs.get_all_dics().get_code(lang1)
            gt.LANG1 = lang1
    
    def set_lang2(self,lang2=''):
        f = '[MClient] plugins.dsl.run.Plugin.set_lang2'
        if lang2 == _('Any'):
            sh.com.rep_lazy(f)
        elif not lang2:
            sh.com.rep_empty(f)
        else:
            lang2 = gt.objs.get_all_dics().get_code(lang2)
            gt.LANG2 = lang2
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    def get_langs1(self,lang2=''):
        if lang2:
            return gt.objs.get_all_dics().get_pairs(lang2)
        else:
            return gt.objs.get_all_dics().get_langs1()
    
    def get_langs2(self,lang1=''):
        if lang1:
            return gt.objs.get_all_dics().get_pairs(lang1)
        else:
            return gt.objs.get_all_dics().get_langs2()
    
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
