#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
from skl_shared.localize import _
import skl_shared.shared as sh


class Cell:
    
    def __init__(self,text,rowno,colno,cellno):
        self.text = text
        self.rowno = rowno
        self.colno = colno
        self.cellno = cellno



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



class Cells:
    
    def __init__(self):
        self.cells = []
    
    def _get(self,cellno):
        for i in range(len(self.cells)):
            if self.cells[i].cellno == cellno:
                return i
    
    def reset(self,data):
        f = 'controller.Cells.reset'
        if not data:
            sh.com.rep_empty(f)
            return
        for block in data:
            text, rowno, colno, cellno = block[1], block[2], block[3], block[4]
            i = self._get(cellno)
            if i is None:
                self.cells.append(Cell(text,rowno,colno,cellno))
            else:
                self.cells[i].text += text
    
    def debug(self):
        f = 'controller.Cells.debug'
        if not data:
            sh.com.rep_empty(f)
            return
        texts = []
        rownos = []
        colnos = []
        cellnos = []
        for cell in self.cells:
            texts.append(cell.text)
            rownos.append(cell.rowno)
            colnos.append(cell.colno)
            cellnos.append(cell.cellno)
        headers = (_('TEXT'),_('ROW #'),_('COLUMN #'),_('CELL #'))
        iterable = [texts,rownos,colnos,cellnos]
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrows = 1000
                           ,maxrow = 40
                           ).run()
        sh.com.run_fast_debug(f,mes)



class Table:
    
    def __init__(self):
        self.cells = []
        
    
    def fill(self,data):
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
    icells = Cells()
    icells.reset(data)
    icells.debug()
    #com.debug_memory(data)
    #itable = Table()
    db.close()
