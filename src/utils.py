#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.multitrancom.utils.subjects.compile as us


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    us.Compile().run()
    sh.com.end()
                
