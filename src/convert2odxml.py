#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG

import plugins.dsl.get


class DSL(plugins.dsl.get.DSL):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_blocks(self):
        f = '[MClient] convert2odxml.DSL.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.poses:
            self.Success = False
            rep.empty(f)
            return
        i = 1
        while i < len(self.poses):
            block = self.lst[self.poses[i-1]:self.poses[i]]
            self.blocks.append(block)
            i += 1
    
    def debug_blocks(self, limit=1000):
        f = '[MClient] convert2odxml.DSL.debug_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        debug = []
        if limit == 0:
            limit = len(self.blocks)
        else:
            limit = min(limit, len(self.blocks))
        for i in range(limit):
            debug.append(f'{f}: {i+1}')
            debug += self.blocks[i]
            debug.append('\n')
        return '\n'.join(debug)
        


if __name__ == '__main__':
    f = '[MClient] convert2odxml.__main__'
    ROOT.get_root()
    idic = DSL('/home/pete/.config/mclient/dics/ComputerEnRu.dsl')
    idic.run()
    idic.set_blocks()
    mes = idic.debug_blocks()
    shDEBUG.reset(f, mes)
    shDEBUG.show()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
