#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from plugins.multitrancom.utils.subjects.compile import Compile, Check, Missing
from skl_shared_qt.graphics.root.controller import ROOT


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    #Compile(1).run()
    #Check().run()
    Missing(1).run()
    ROOT.end()
                
