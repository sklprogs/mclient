#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
#from skl_shared.graphics.root.controller import ROOT
import mclient
import convert


#ROOT.get_root()
if len(sys.argv) > 1:
    if sys.argv[1] == '--convert':
        convert.start()
    else:
        print('Only --convert parameter is supported!')
        sys.exit()
else:
    mclient.start()
#ROOT.end()