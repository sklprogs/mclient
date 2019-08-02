#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared          as sh
import plugins.multitrancom.utils as utcom

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    
    sh.com.end()
                
