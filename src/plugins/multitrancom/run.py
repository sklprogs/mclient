#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared2.shared            as sh
import plugins.multitrancom.get     as gt
import plugins.multitrancom.cleanup as cu
import plugins.multitrancom.tags    as tg
import plugins.multitrancom.elems   as el
import plugins.multitrancom.pairs   as pr
from skl_shared2.localize import _



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=20
                 ):
        self.set_values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def set_values(self):
        self.htm    = ''
        self.text   = ''
        self.blocks = []
    
    # This is needed only for compliance with a general method
    def quit(self):
        pass
    
    def get_lang1(self):
        return pr.LANG1
    
    def get_lang2(self):
        return pr.LANG2
    
    def get_server(self):
        return gt.URL
    
    def is_combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def fix_raw_htm(self):
        return gt.com.fix_raw_htm(self.htm)
    
    def get_url(self,search):
        f = '[MClient] plugins.multitrancom.run.Plugin.get_url'
        code1 = pr.objs.get_pairs().get_code(pr.LANG1)
        code2 = pr.objs.pairs.get_code(pr.LANG2)
        if code1 and code2 and search:
            return gt.com.get_url (code1  = code1
                                  ,code2  = code2
                                  ,search = search
                                  )
        else:
            sh.com.rep_empty(f)
            return ''
    
    def set_lang1(self,lang1):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang1'
        if lang1:
            if lang1 in pr.LANGS:
                pr.LANG1 = lang1
            else:
                mes = _('Wrong input data: "{}"!').format(lang1)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
    def set_lang2(self,lang2):
        f = '[MClient] plugins.multitrancom.run.Plugin.set_lang2'
        if lang2:
            if lang2 in pr.LANGS:
                pr.LANG2 = lang2
            else:
                mes = _('Wrong input data: "{}"!').format(lang2)
                sh.objs.get_mes(f,mes).show_error()
        else:
            sh.com.rep_empty(f)
    
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
    
    def request(self,search='',url=''):
        iget = gt.Get (search = search
                      ,url    = url
                      )
        self.text = iget.run()
        self.text = self.htm = cu.CleanUp(self.text).run()
        if self.text is None:
            self.text = ''
        self.blocks = tg.Tags (text    = self.text
                               ,Debug   = self.Debug
                               ,Shorten = self.Shorten
                               ,MaxRow  = self.MaxRow
                               ,MaxRows = self.MaxRows
                               ).run()
        if self.blocks:
            for block in self.blocks:
                # Prevent useless error output
                if block.url:
                    block.url = gt.com.fix_url(block.url)
        self.blocks = el.Elems (blocks  = self.blocks
                               ,iabbr   = self.iabbr
                               ,langs   = pr.objs.get_pairs().get_alive()
                               ,search  = search
                               ,Debug   = self.Debug
                               ,Shorten = self.Shorten
                               ,MaxRow  = self.MaxRow
                               ,MaxRows = self.MaxRows
                               ).run()
        return self.blocks
