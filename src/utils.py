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
    utcom.com.format_gettext()
    #utcom.Pairs().run()
    '''
    ipairs = utcom.Pairs()
    ipairs.fill()
    print('Code: %d; Language: %s' % (209,ipairs.get_lang(209)))
    print('Code: %d; Language: %s' % (262,ipairs.get_lang(262)))
    '''
    sg.objs.end()
                
