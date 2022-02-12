#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
from skl_shared.localize import _
import skl_shared.shared as sh


class DB:
    
    def __init__(self):
        self.set_values()
        self.db = sqlite3.connect('/home/pete/tmp/set.db')
        self.dbc = self.db.cursor()
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
    
    def fetch(self):
        query = 'select TYPE,TEXT,ROWNO,COLNO,CELLNO from BLOCKS \
                 where BLOCK = 0 and IGNORE = 0 order by CELLNO,NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        self.dbc.close()



class Table:
    
    def __init__(self):
        pass



class Commands:
    
    def debug_memory(self,data):
        f = 'controller.Commands.debug_memory'
        if not data:
            sh.com.rep_empty(f)
            return
        #TYPE,TEXT,ROWNO,COLNO,CELLNO
        headers = (_('TYPE'),_('TEXT'),_('ROW #'),_('COLUMN #')
                  ,_('CELL #')
                  )
        mes = sh.FastTable (headers = headers
                           ,iterable = data
                           ,maxrows = 1000
                           ,maxrow = 40
                           ,Transpose = 1
                           ).run()
        sh.com.run_fast_debug(f,mes)


com = Commands()


if __name__ == '__main__':
    f = 'controller.__main__'
    db = DB()
    data = db.fetch()
    #com.debug_memory(data)
    db.close()
