#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3
import PyQt5
import PyQt5.QtWidgets

from skl_shared.localize import _
import gui as gi


class Cell:
    
    def __init__(self,text,rowno,colno,cellno):
        self.text = text
        self.rowno = rowno
        self.colno = colno
        self.cellno = cellno



class DB:
    
    def __init__(self):
        self.set_values()
        self.db = sqlite3.connect(self.path)
        self.dbc = self.db.cursor()
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
        self.path = '/home/pete/tmp/hello.db'
        #self.path = '/home/pete/tmp/set.db'
    
    def fetch(self):
        query = 'select TYPE,TEXT,ROWNO,COLNO,CELLNO from BLOCKS \
                 where BLOCK = 0 and IGNORE = 0 order by CELLNO,NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = 'controller.DB.close'
        mes = _('Close "{}"').format(self.path)
        #sh.objs.get_mes(f,mes,True).show_info()
        print(mes)
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = 'controller.DB.get_max_col_no'
        query = 'select COLNO from BLOCKS where BLOCK = 0 and \
                        IGNORE = 0 order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = 'controller.DB.get_max_row_no'
        query = 'select ROWNO from BLOCKS where BLOCK = 0 \
                 and IGNORE = 0 order by ROWNO desc'
        self.dbc.execute(query,)
        result = self.dbc.fetchone()
        if result:
            return result[0]



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
            #sh.com.rep_empty(f)
            print('Empty')
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
            #sh.com.rep_empty(f)
            print('empty')
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
        self.set_values()
        self.gui = gi.Table()
    
    def set_values(self):
        self.cells = []
        self.rowno = 0
        self.colno = 0
    
    def reset(self,cells,rowno,colno):
        self.cells = cells
        self.rowno = rowno
        self.colno = colno
        self.clear()
        self.set_view()
        self.fill()
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
        self.gui.bind('Alt+C',self.clear)
    
    def enable_grid(self):
        self.gui.show_grid(True)
    
    def disable_grid(self):
        self.gui.show_grid(False)
    
    def hide_headers(self):
        self.gui.hide_x_header()
        self.gui.hide_y_header()
    
    def set_max_row_height(self,height=80):
        self.gui.set_max_row_height(height)
    
    def set_title(self,title='MClientQT'):
        self.gui.set_title(title)
    
    def set_col_widths(self):
        # Stub
        self.gui.set_col_width(0,150)
        self.gui.set_col_width(1,100)
        self.gui.set_col_width(2,50)
        self.gui.set_col_width(3,50)
    
    def set_view(self):
        self.set_max_row_height(80)
        self.gui.resize_fixed()
        mes = _('Table sizes: {}x{}').format(self.rowno,self.colno)
        #sh.objs.get_mes(f,mes,True).show_debug()
        print(mes)
        self.gui.set_col_no(self.colno)
        self.gui.set_row_no(self.rowno)
    
    def set_gui(self):
        self.set_title()
        self.hide_headers()
        self.disable_grid()
        self.set_bindings()
    
    def set_row_no(self):
        self.gui.set_row_no(self.rowno)
    
    def set_col_no(self):
        self.gui.set_col_no(self.colno)
    
    def clear(self,event=None):
        self.gui.table.clear()
    
    def fill(self):
        for cell in self.cells:
            table_item = self.gui.get_term_item(cell.text)
            self.gui.set_item(table_item,cell.rowno,cell.colno)
        self.gui.add_layout()



class Commands:
    
    def debug_memory(self,data):
        f = 'controller.Commands.debug_memory'
        if not data:
            #sh.com.rep_empty(f)
            print('empty')
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
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    db = DB()
    data = db.fetch()
    rowno = db.get_max_row_no()
    colno = db.get_max_col_no()
    if rowno is not None:
        rowno += 1
    if colno is not None:
        colno += 1
    icells = Cells()
    icells.reset(data)
    #icells.debug()
    #com.debug_memory(data)
    itable = Table()
    itable.reset(icells.cells,rowno,colno)
    itable.set_gui()
    itable.fill()
    itable.show()
    sys.exit(app.exec())
    db.close()
