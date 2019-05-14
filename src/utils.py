#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import plugins.multitrancom.utils as utcom

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sg.objs.start()
    utcom.com.missing_titles()
    """
    _html = sh.Get (url      = 'https://www.multitran.com/m.exe?s=be%20born%20with%20a%20caul&l1=1&l2=2'
                   ,encoding = 'utf-8'
                   ).run()
    if _html:
        _html = _html.replace('&amp;','&').replace(' ','%20')
        '''
        _html = _html.replace ('<td class="subj" width="1"><a href'
                              ,'<td class="subj" width="1" a href'
                              )
        '''
        #sg.fast_txt(_html)
        search = 'href="/m.exe?a='
        #search = 'td class="subj" width="1" a href="/m.exe?a='
        tags = utcom.Tags (text   = _html
                          ,search = search
                          )
        tags.run()
        print('URLs:',tags._urls)
        print('Titles:',tags._titles)
    else:
        sh.com.empty(f)
    """
    """
    _html = sh.Get (url      = 'https://www.multitran.com/m.exe?a=112&l1=1&l2=2'
                   ,encoding = 'utf-8'
                   ).run()
    if _html:
        _html = _html.replace('&amp;','&').replace(' ','%20')
        #sg.fast_txt(_html)
        tags = utcom.Tags (text   = _html
                          ,search = 'href="/m.exe?a='
                          )
        tags.run()
        tags._urls = tags._urls[5:15]
        tags._titles = tags._titles[5:15]
        print('URLs:',tags._urls)
        print('Titles:',tags._titles)
    else:
        sh.com.empty(f)
    """
    sg.objs.end()
                
