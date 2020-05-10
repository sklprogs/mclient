#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.stardict.get     as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags    as tg
import plugins.stardict.elems   as el



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,maxrow=20,maxrows=1000
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #NOTE: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self.set_values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.maxrow  = maxrow
        self.maxrows = maxrows
    
    def set_values(self):
        self.blocks = []
        self.text   = ''
        self.htm    = ''
    
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
        return ''
    
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
        iget      = gt.Get(search)
        self.text = iget.run()
        self.htm  = iget.htm
        self.text = cu.CleanUp(self.text).run()
        if self.text is None:
            self.text = ''
        self.blocks = tg.Tags (text    = self.text
                              ,Debug   = self.Debug
                              ,maxrow  = self.maxrow
                              ,maxrows = self.maxrows
                              ).run()
        self.blocks = el.Elems (blocks = self.blocks
                               ,iabbr  = self.iabbr
                               ).run()
        return self.blocks
