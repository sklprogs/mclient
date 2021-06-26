#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.multitrancom.utils.subjects as us


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    url = 'https://www.multitran.com/m.exe?s=printer&l1=1&l2=2'
    ui_lang = 1
    us.EndPage(url,ui_lang,True).run()
    sh.com.end()
                
