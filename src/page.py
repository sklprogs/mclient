#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
import html
import shared    as sh
import sharedGUI as sg
import logic     as lg
import plugins.stardict.run     as sd
import plugins.multitranru.run  as mr
import plugins.multitrancom.run as mc

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

SOURCES = (_('All'),_('Online'),_('Offline'))


class Page:

    def __init__ (self,source=_('All'),search=''
                 ,url='',encoding='windows-1251'
                 ,timeout=6
                 ):
        self._text     = ''
        self._source   = source
        self._search   = search
        self._url      = url
        self._encoding = encoding
        self._timeout  = timeout
    
    def get_source(self,source):
        f = '[MClient] page.Page.get_source'
        if hasattr(source,'run'):
            return source.run (path     = lg.objs.default().dics()
                              ,search   = self._search
                              ,url      = self._url
                              ,encoding = self._encoding
                              ,timeout  = self._timeout
                              )
        else:
            sh.objs.mes (f,_('ERROR')
                        ,_('An invalid plugin!')
                        )

    def run(self):
        f = '[MClient] page.Page.run'
        if not self._text:
            if self._source in SOURCES:
                timer = sh.Timer(f)
                timer.start()
                text_sd = ''
                text_mr = ''
                text_mc = ''
                if self._source in (_('All'),_('Offline')):
                    text_sd = self.get_source(sd)
                if self._source in (_('All'),_('Online')):
                    text_mr = self.get_source(mr)
                    text_mc = self.get_source(mc)
                if text_sd is None:
                    text_sd = ''
                if text_mr is None:
                    text_mr = ''
                if text_mc is None:
                    text_mc = ''
                self._text = text_sd + text_mr + text_mc
                timer.end()
            else:
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(self._source),';'.join(SOURCES))
                            )
        return self._text


if __name__ == '__main__':
    f = '[MClient] page.__main__'
    import logic as lg
    sg.objs.start()
    path     = lg.objs.default().dics()
    source   = _('All')
    #search   = 'иммуногенная'
    #url      = 'https://www.multitran.ru/c/M.exe?l1=1&l2=2&s=%E8%EC%F3%ED%ED%EE%E3%E5%ED%ED%E0%FF'
    search   = 'computer'
    url      = 'https://www.multitran.ru/c/m.exe?CL=1&s=computer&l1=1'
    encoding = 'windows-1251'
    timeout  = 6
    
    timer = sh.Timer(func_title=f)
    timer.start()
    text = Page (source   = source
                ,search   = search
                ,url      = url
                ,encoding = encoding
                ,timeout  = timeout
                ).run()
    timer.end()
    sg.objs.txt().insert(text)
    sg.objs._txt.show()
    sg.objs.end()
