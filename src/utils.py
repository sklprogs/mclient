#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
#import plugins.multitrancom.utils.subjects.compile as us
import plugins.multitrancom.utils.subjects.check as us


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    #us.Compile(1).run()
    us.Check().run()
    sh.com.end()
                
