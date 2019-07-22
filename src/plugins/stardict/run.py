#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared        as sh
import plugins.stardict.get     as gt
import plugins.stardict.cleanup as cu
import plugins.stardict.tags    as tg
import plugins.stardict.elems   as el

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



class Plugin:
    
    def __init__ (self,iabbr=None,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        ''' - Extra unused input variables are preserved so it would be
              easy to use an abstract class for all dictionary sources.
            - #note: Do not forget to set plugins.stardict.get.PATH
              earlier.
        '''
        self.values()
        self.iabbr   = iabbr
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
    
    def values(self):
        self._blocks = []
        self._text   = ''
        self._html   = ''
    
    # This is needed only for compliance with a general method
    def lang1(self):
        return _('Any')
    
    # This is needed only for compliance with a general method
    def lang2(self):
        return _('Any')
    
    # This is needed only for compliance with a general method
    def server(self):
        return ''
    
    # This is needed only for compliance with a general method
    def fix_raw_html(self):
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
    def langs1(self,lang2=''):
        return(_('Any'),)
    
    # This is needed only for compliance with a general method
    def langs2(self,lang1=''):
        return(_('Any'),)
    
    def combined(self):
        ''' Whether or not the plugin is actually a wrapper over other
            plugins.
        '''
        return False
    
    def accessible(self):
        return gt.com.accessible()
    
    def suggest(self,search):
        return gt.Suggest(search).run()
    
    def request(self,search='',url=''):
        iget       = gt.Get(search)
        self._text = iget.run()
        self._html = iget._html
        self._text = cu.CleanUp(self._text).run()
        if self._text is None:
            self._text = ''
        self._blocks = tg.Tags (text    = self._text
                               ,Debug   = self.Debug
                               ,Shorten = self.Shorten
                               ,MaxRow  = self.MaxRow
                               ,MaxRows = self.MaxRows
                               ).run()
        self._blocks = el.Elems (blocks    = self._blocks
                                ,iabbr     = self.iabbr
                                ).run()
        return self._blocks
