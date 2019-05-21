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
    utcom.com.format_pairs()
    sg.objs.end()
                
