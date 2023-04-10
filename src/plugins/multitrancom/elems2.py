#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Elems:
    
    def __init__(self,blocks):
        self.blocks = blocks
    
    def run_phcount(self):
        f = 'plugins.multitrancom.elems.Elems.run_phcount'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type_ == 'phrase' \
            and self.blocks[i].type_ == 'phcount':
                count += 1
                self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        sh.com.rep_matches(f,count)
    
    def debug(self):
        headers = ('NO','TYPE','TEXT','URL','CELLNO','DIC','DICF')
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type_
                         ,'"{}"'.format(self.blocks[i].text)
                         ,'"{}"'.format(self.blocks[i].url)
                         ,self.blocks[i].cellno
                         ,self.blocks[i].dic
                         ,self.blocks[i].dicf
                         ]
                        )
        # 10'' monitor: 12 symbols per a column
        # 23'' monitor: 20 symbols per a column
        return sh.FastTable (headers = headers
                            ,iterable = rows
                            ,maxrow = 23
                            ,maxrows = 1000
                            ,Transpose = True
                            ).run()
    
    def run(self):
        self.run_phcount()
