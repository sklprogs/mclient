#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.stardict.get as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags as tg
import plugins.stardict.elems as el
import plugins.stardict.subjects as sj



class Plugin:
    
    def __init__ (self,Debug=False
                 ,maxrow=20,maxrows=1000
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self.set_values()
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def set_values(self):
        self.abbr = {}
        self.blocks = []
        self.text = ''
        self.htm = ''
        self.search = ''
    
    def get_subjects(self):
        return sj.objs.get_subjects().get_list()
    
    def get_group(self,subject=''):
        return sj.objs.get_subjects().get_group(subject)
    
    def get_majors(self):
        return sj.objs.get_subjects().get_majors()
    
    def get_search(self):
        return self.search
    
    # This is needed only for compliance with a general method
    def set_htm(self,code):
        self.htm = code
    
    # This is needed only for compliance with a general method
    def fix_url(self,url):
        return url
    
    def is_oneway(self):
        return False
    
    def get_title(self,short):
        #TODO: implement
        return short
    
    def quit(self):
        for idic in gt.objs.get_all_dics().dics:
            idic.unload()
    
    # This is needed only for compliance with a general method
    def get_lang1(self):
        return _('Any')
    
    # This is needed only for compliance with a general method
    def get_lang2(self):
        return _('Any')
    
    # This is needed only for compliance with a general method
    def get_server(self):
        return ''
    
    # This is needed only for compliance with a general method
    def fix_raw_htm(self):
        return self.htm
    
    # This is needed only for compliance with a general method
    def get_url(self,search=''):
        return ''
    
    # This is needed only for compliance with a general method
    def set_lang1(self,lang1=''):
        pass
    
    # This is needed only for compliance with a general method
    def set_lang2(self,lang2=''):
        pass
    
    # This is needed only for compliance with a general method
    def set_timeout(self,timeout=0):
        pass
    
    # This is needed only for compliance with a general method
    def get_langs1(self,lang2=''):
        return(_('Any'),)
    
    # This is needed only for compliance with a general method
    def get_langs2(self,lang1=''):
        return(_('Any'),)
    
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
        self.search = search
        self.htm = self.text = gt.Get(search).run()
        self.text = cu.CleanUp(self.text).run()
        itags = tg.Tags (text = self.text
                        ,Debug = self.Debug
                        ,maxrow = self.maxrow
                        ,maxrows = self.maxrows
                        )
        self.blocks = itags.run()
        self.blocks = el.Elems (blocks = self.blocks
                               ,abbr = itags.abbr
                               ).run()
        return self.blocks
