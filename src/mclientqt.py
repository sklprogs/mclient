#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3
import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

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
        self.path = '/home/pete/tmp/hello3.db'
        #self.path = '/home/pete/tmp/set.db'
    
    def fetch(self):
        query = 'select TYPE,TEXT,ROWNO,COLNO,CELLNO from BLOCKS \
                 where BLOCK = 0 and IGNORE = 0 order by CELLNO,NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = '[MClientQt] mclientqt.DB.close'
        mes = _('Close "{}"').format(self.path)
        #sh.objs.get_mes(f,mes,True).show_info()
        print(mes)
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = '[MClientQt] mclientqt.DB.get_max_col_no'
        query = 'select COLNO from BLOCKS where BLOCK = 0 and \
                        IGNORE = 0 order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = '[MClientQt] mclientqt.DB.get_max_row_no'
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
        f = '[MClientQt] mclientqt.Cells.reset'
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
        f = '[MClientQt] mclientqt.Cells.debug'
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



class App:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.App()
        self.set_gui()
    
    def set_values(self):
        self.cells = []
        self.rowno = 0
        self.colno = 0
        self.rownum = 0
        self.colnum = 0
    
    def reset(self,cells,rownum,colnum):
        self.cells = cells
        self.rownum = rownum
        self.colnum = colnum
        self.clear()
        self.set_view()
        self.fill()
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def set_mouse_over(self,rowno,colno):
        if self.rowno == rowno and self.colno == colno:
            return
        ''' We need to get and modify a cell instance as soon as
            possible since it is deleted.
        '''
        old_cell = self.gui.table.get_cell(self.rowno,self.colno)
        new_cell = self.gui.table.get_cell(rowno,colno)
        if not old_cell or not new_cell:
            ''' The table item can be None for some reason. We should
                verify that both old and new items are valid so we
                would not lose our old cell's background.
            '''
            return
        self.gui.table.set_cell_bg(old_cell,'white')
        self.gui.table.set_cell_bg(new_cell,'cyan')
        self.rowno = rowno
        self.colno = colno
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
        self.gui.bind('Alt+C',self.clear)
        self.gui.table.enter_cell(self.set_mouse_over)
    
    def enable_grid(self):
        self.gui.table.show_grid(True)
    
    def disable_grid(self):
        self.gui.table.show_grid(False)
    
    def hide_headers(self):
        self.gui.table.hide_x_header()
        self.gui.table.hide_y_header()
    
    def set_max_row_height(self,height=80):
        self.gui.table.set_max_row_height(height)
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_col_widths(self):
        # Stub
        '''
        # 4 term columns
        self.gui.table.set_col_width(0,85)
        self.gui.table.set_col_width(1,85)
        self.gui.table.set_col_width(2,85)
        self.gui.table.set_col_width(3,85)
        self.gui.table.set_col_width(4,153)
        self.gui.table.set_col_width(5,153)
        self.gui.table.set_col_width(6,153)
        self.gui.table.set_col_width(7,153)
        '''
        # 3 term columns
        self.gui.table.set_col_width(0,135)
        self.gui.table.set_col_width(1,65)
        self.gui.table.set_col_width(2,65)
        self.gui.table.set_col_width(3,65)
        self.gui.table.set_col_width(4,205)
        self.gui.table.set_col_width(5,205)
        self.gui.table.set_col_width(6,205)
    
    def set_view(self):
        self.set_max_row_height(80)
        self.gui.table.resize_fixed()
        mes = _('Table sizes: {}x{}').format(self.rownum,self.colnum)
        #sh.objs.get_mes(f,mes,True).show_debug()
        print(mes)
        self.gui.table.set_col_num(self.colnum)
        self.gui.table.set_row_num(self.rownum)
        self.set_col_widths()
    
    def set_gui(self):
        self.set_title()
        self.hide_headers()
        self.disable_grid()
        self.set_bindings()
    
    def set_row_num(self):
        self.gui.table.set_row_no(self.rownum)
    
    def set_col_num(self):
        self.gui.table.set_col_num(self.colnum)
    
    def clear(self,event=None):
        self.gui.table.clear()
    
    def fill(self):
        for cell in self.cells:
            item = self.gui.table.get_term_cell(cell.text)
            self.gui.table.set_cell(item,cell.rowno,cell.colno)
        self.gui.table.add_layout()



class Commands:
    
    def debug_memory(self,data):
        f = '[MClientQt] mclientqt.Commands.debug_memory'
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
    f = '[MClientQt] mclientqt.__main__'
    db = DB()
    data = db.fetch()
    rownum = db.get_max_row_no()
    colnum = db.get_max_col_no()
    if rownum is not None:
        rownum += 1
    if colnum is not None:
        colnum += 1
    icells = Cells()
    icells.reset(data)
    #icells.debug()
    #com.debug_memory(data)
    exe = PyQt5.QtWidgets.QApplication(sys.argv)
    app = App()
    app.reset(icells.cells,rownum,colnum)
    app.fill()
    ''' We can get a constant mouse hovering response only if we install
        the filter like this.
    '''
    exe.installEventFilter(app.gui.panel)
    app.show()
    db.close()
    sys.exit(exe.exec())
