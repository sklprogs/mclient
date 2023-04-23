#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import plugins.multitrancom.get as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags as tg
import plugins.multitrancom.elems as el
import plugins.multitrancom.pairs as pr
import plugins.multitrancom.subjects as sj



class Plugin:
    
    def __init__(self,Debug=False,maxrows=1000):
        self.set_values()
        self.Debug = Debug
        self.maxrows = maxrows
    
    def set_values(self):
        self.blocks = []
        self.fixed_urls = {}
        self.htm = ''
        self.text = ''
        self.search = ''
    
    def get_title(self,short):
        return sj.objs.get_subjects().get_title(short)
    
    def get_subjects(self):
        return sj.objs.get_subjects().get_list()
    
    def get_group_with_header(self,subject=''):
        return sj.objs.get_subjects().get_group_with_header(subject)
    
    def get_majors(self):
        return sj.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    def set_htm(self,code):
        self.htm = code
    
    def fix_url(self,url):
        return gt.com.fix_url(url)
    
    def is_oneway(self):
        return False
    
    def quit(self):
        # This is needed only for compliance with a general method
        pass
    
    def get_lang1(self):
        return pr.LANG1
    
    def get_lang2(self):
        return pr.LANG2
    
    def get_server(self):
        return gt.URL
    
    def is_combined(self):
        # Whether or not the plugin is actually a wrapper over other plugins
        return False
    
    def fix_raw_htm(self):
        return gt.com.fix_raw_htm(self.htm)
    
    def get_url(self,search):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_url'
        code1 = pr.objs.get_pairs().get_code(pr.LANG1)
        code2 = pr.objs.pairs.get_code(pr.LANG2)
        if not (code1 and code2 and search):
            sh.com.rep_empty(f)
            return ''
        return gt.com.get_url (code1 = code1
                              ,code2 = code2
                              ,search = search
                              )
    
    def set_lang1(self,lang1):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang1'
        if not lang1:
            sh.com.rep_empty(f)
            return
        if lang1 in pr.LANGS:
            pr.LANG1 = lang1
        else:
            mes = _('Wrong input data: "{}"!').format(lang1)
            sh.objs.get_mes(f,mes).show_error()
    
    def set_lang2(self,lang2):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang2'
        if not lang2:
            sh.com.rep_empty(f)
            return
        if lang2 in pr.LANGS:
            pr.LANG2 = lang2
        else:
            mes = _('Wrong input data: "{}"!').format(lang2)
            sh.objs.get_mes(f,mes).show_error()
    
    def set_timeout(self,timeout=6):
        gt.TIMEOUT = timeout
    
    def is_accessible(self):
        return gt.com.is_accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def get_langs1(self,lang2=''):
        if lang2:
            return pr.objs.get_pairs().get_pairs1(lang2)
        else:
            return pr.objs.get_pairs().get_alive()
    
    def get_langs2(self,lang1=''):
        if lang1:
            return pr.objs.get_pairs().get_pairs2(lang1)
        else:
            return pr.objs.get_pairs().get_alive()
    
    def get_fixed_urls(self):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_fixed_urls'
        if not self.fixed_urls:
            mes = _('Run {} first!')
            mes = mes.format('plugins.multitrancom.run.Plugin.request')
            sh.objs.get_mes(f,mes,True).show_error()
            return {}
        return self.fixed_urls
    
    def request(self,search='',url=''):
        self.search = search
        self.htm = gt.Get (search = search
                          ,url = url
                          ).run()
        self.text = cu.CleanUp(self.htm).run()
        self.blocks = tg.Tags(self.text).run()
        ielems = el.Elems(self.blocks)
        self.blocks = ielems.run()
        self.fixed_urls = ielems.urls
        return self.blocks
