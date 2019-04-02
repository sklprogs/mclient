#!/usr/bin/python3

import re
import shared    as sh
import sharedGUI as sg
import page      as pg
import logic     as lg
import tags      as tg


class Commands:
    
    def __init__(self):
        pass
    
    def tags(self):
        code = sh.ReadTextFile('/home/pete/tmp/ars/stardict').get()
        tags = tg.Tags (source = _('Offline')
                       ,text   = code
                       )
        tags.run()
        tags.debug_tags()
        tags.debug_blocks()


if __name__ == '__main__':
    sg.objs.start()
    com = Commands()
    print(com.tags())
    sg.objs.end()
