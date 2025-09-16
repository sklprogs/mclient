#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT

#from converters.dsl.odxml import Runner
from converters.dsl.mdic import Runner


if __name__ == '__main__':
    f = '[MClient] convert.__main__'
    ROOT.get_root()
    Runner().run()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
