#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import plugins.multitranru.get     as mtget
import plugins.multitranru.cleanup as mtcleanup

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


def run (path='',search='',url=''
        ,encoding='windows-1251',timeout=6
        ):
    ''' Extra unused input variables are preserved so it would be easy
        to use an abstract class for all dictionary sources.
    '''
    text = mtget.Get (search   = search
                     ,url      = url
                     ,encoding = encoding
                     ,timeout  = timeout
                     ).run()
    text = mtcleanup.CleanUp(text).run()
    return text
