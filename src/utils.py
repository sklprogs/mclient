#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
import plugins.multitrancom.utils.subjects.compile as us
#import plugins.multitrancom.utils.subjects.check as us


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    us.Compile(0).run()
    #us.Check().run()
    #us.Missing(0).run()
    sh.com.end()
                
