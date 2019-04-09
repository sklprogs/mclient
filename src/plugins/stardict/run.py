#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg
import plugins.stardict.get     as sdget
import plugins.stardict.cleanup as sdcleanup

import gettext, gettext_windows

gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


def run (path,search,url=''
        ,encoding='windows-1251',timeout=6
        ):
    ''' Extra unused input variables are preserved so it would be easy
        to use an abstract class for all dictionary sources.
    '''
    # Assign externally: lg.objs.default().dics()
    sdget.PATH = path
    text = sdget.objs.all_dics().get(search)
    text = sdcleanup.run(text)
    return text
