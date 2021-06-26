#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import plugins.multitrancom.utils as utcom


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    utcom.Subjects2().run()
    sh.com.end()
                
