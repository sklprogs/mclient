#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.multitrancom.utils.subjects as us


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    #url = 'https://www.multitran.com/m.exe?s=printer&l1=1&l2=2'
    url = 'https://www.multitran.com/m.exe?s=reticulated+siren&l1=1&l2=10000'
    #us.EndPage(url,1,True).run()
    us.Compare(url,Debug=True).run()
    #us.StartPage(1,2,True).run()
    #us.Extractor(0).run()
    sh.com.end()
                
