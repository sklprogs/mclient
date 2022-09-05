#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
import gui as gi

DEBUG = False


class Table:

    def __init__(self):
        self.gui = gi.Table()
        self.set_gui()
    
    def set_row_height(self,height=45):
        for no in range(self.rownum):
            self.gui.set_row_height(no,height)
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        f = '[MClientQt] mclient.Table.set_col_width'
        mes = _('Number of columns: {}').format(self.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        #TODO: Rework, number of fixed columns can be different
        for no in range(self.colnum):
            if no == 0:
                width = 140
            elif no == 1:
                width = sh.lg.globs['int']['fixed_col_width']
            elif no in (2,3):
                width = 63
            else:
                width = sh.lg.globs['int']['term_col_width']
            #mes = 'Column #{}; width: {}'.format(no,width)
            #print(mes)
            self.gui.set_col_width(no,width)
    
    def set_selection(self,rowno,colno):
        if self.rowno == rowno and self.colno == colno:
            return
        ''' We need to get and modify a cell instance as soon as possible since
            it is deleted.
        '''
        self.set_cell_bg('white')
        self.set_cell_by_index(rowno,colno)
        self.set_cell_bg('cyan')
        self.rowno = rowno
        self.colno = colno
    
    def debug_cells(self):
        f = '[MClientQt] mclient.Table.debug_cells'
        codes = []
        rownos = []
        colnos = []
        for cell in self.cells:
            codes.append(cell.code)
            rownos.append(cell.rowno)
            colnos.append(cell.colno)
        headers = (_('ROW #'),_('COLUMN #'),_('CODE'))
        mes = sh.FastTable (headers = headers
                           ,iterable = [rownos,colnos,codes]
                           ,maxrow = 70
                           ).run()
        #TODO: implement 'run_fast_debug'
    
    def get_matrix(self):
        ''' Empty cells must be recreated since QTableView throws an error
            otherwise.
        '''
        f = '[MClientQt] mclient.Table.get_matrix'
        old_rowno = 1
        matrix = []
        row = []
        for i in range(len(self.cells)):
            if old_rowno != self.cells[i].rowno:
                if row:
                    if i > 0:
                        delta = self.colnum - self.cells[i-1].colno - 1
                        for no in range(delta):
                            row.append('')
                    matrix.append(row)
                    row = []
                for j in range(self.cells[i].colno):
                    row.append('')
                old_rowno = self.cells[i].rowno
            row.append(self.cells[i].code)
        if row:
            matrix.append(row)
        return matrix
    
    def reset(self,cells,rownum,colnum):
        self.cells = cells
        self.rownum = rownum
        self.colnum = colnum
        self.clear()
        self.fill()
        self.set_col_width()
        #self.gui.resizeRowsToContents()
        #self.go_start()
        self.set_row_height(40)
        self.show_borders(False)
        #self.set_max_col_width()
        #self.select_cell()
    
    def set_cell_bg(self,color='cyan'):
        self.gui.set_cell_bg(self.cell,color)
    
    def clear(self):
        #self.gui.clear()
        pass
    
    def go_start(self):
        self.gui.go_start()
    
    def fill(self):
        f = '[MClientQt] mclient.Table.fill'
        gi.model = gi.MyTableModel(self.get_matrix())
        timer = sh.Timer(f)
        timer.start()
        self.gui.setModel(gi.model)
        timer.end()
    
    def set_max_row_height(self,height=150):
        self.gui.set_max_row_height(height)
    
    def set_max_col_width(self):
        constraints = []
        for cell in self.cells:
            #TODO: elaborate
            if cell.no < 5:
                value = 63
            else:
                value = 221
            constraints.append(self.gui.get_constraint(value))
        self.gui.set_max_col_width(constraints)
    
    def show_borders(self,Show=False):
        self.gui.show_borders(Show)
    
    def set_spacing(self,value=0):
        self.gui.set_spacing(value)
    
    def set_border_color(self,color='darkgray'):
        self.gui.set_border_color(color)
    
    def set_cell_by_no(self,no):
        f = '[MClientQt] mclient.Table.set_cell_by_no'
        ''' Go to a cell by its number starting from 1. If the cell number is
            outside of table boundaries, only a warning is shown, but no
            exception is thrown. -1 is automatically corrected to 1, positions
            after the end - to the end.
        '''
        self.cell = self.gui.get_cell_by_no(no)
        if not self.cell:
            sh.com.rep_empty(f)
    
    def set_cell_by_index(self,rowno,colno):
        ''' Return a cell by rowno, colno as PyQt5.QtGui.QTextTableCell. Unlike
            'setPosition', numbers start from 0 when using 'cellAt'. If a cell
            number is outside of table boundaries, a segmentation fault will be
            thrown.
        '''
        cell = self.gui.get_cell_by_index(rowno,colno)
        #cur
        if cell:
            self.cell = cell
        else:
            print('NONE!!!!!!')
    
    def set_cell_border_color(self,color='red'):
        # Not working yet
        self.gui.set_cell_border_color(self.cell,color)
    
    def disable_cursor(self):
        self.gui.disable_cursor()
    
    def enable_cursor(self):
        self.gui.enable_cursor()
    
    def select_cell(self,rowno=0,colno=0):
        #TODO: elaborate
        self.set_cell_by_index(rowno,colno)
        self.set_cell_bg('cyan')
        #self.set_cell_border_color('red')
    
    def set_gui(self):
        pass
        #self.set_max_row_height()
        #self.set_spacing(0)
        #self.set_border_color()
        #self.disable_cursor()



class DB:
    
    def __init__(self):
        self.set_values()
        self.db = sqlite3.connect(self.path)
        self.dbc = self.db.cursor()
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
        self.path = '/home/pete/tmp/set.db'
    
    def fetch(self):
        query = 'select NO,ROWNO,COLNO,TEXT,COLOR,FAMILY,SIZE,BOLD,ITALIC \
                 from FONTS order by NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = '[MClient] mclient.DB.close'
        mes = _('Close "{}"').format(self.path)
        #sh.objs.get_mes(f,mes,True).show_info()
        print(mes)
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = '[MClient] mclient.DB.get_max_col_no'
        query = 'select COLNO from FONTS order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = '[MClient] mclient.DB.get_max_row_no'
        query = 'select ROWNO from FONTS order by ROWNO desc'
        self.dbc.execute(query,)
        result = self.dbc.fetchone()
        if result:
            return result[0]



class App:
    
    def __init__(self):
        self.set_values()
        self.gui = gi.App()
        self.set_gui()
        self.update_ui()
    
    def set_values(self):
        self.complex = 0
        self.single = 0
    
    def minimize(self):
        self.gui.minimize()
    
    def reset(self,cells,rownum,colnum):
        mes = _('Table sizes: {}x{}').format(rownum,colnum)
        #sh.objs.get_mes(f,mes,True).show_debug()
        print(mes)
        self.table.reset(cells,rownum,colnum)
    
    def update_ui(self):
        self.gui.panel.ent_src.focus()
        #TODO: load from logic
        sources = (_('Multitran'),_('Stardict'),'Lingvo (DSL)'
                  ,_('Local MT')
                  )
        self.gui.panel.opt_src.reset(sources)
        self.gui.panel.opt_col.reset((1,2,3,4,5,6,7,8,9,10),4)
        #TODO: load from logic
        langs1 = (_('English'),_('Russian'),_('French'))
        langs2 = (_('Russian'),_('English'),_('French'))
        self.gui.panel.opt_lg1.reset(langs1)
        self.gui.panel.opt_lg2.reset(langs2)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def move_down(self):
        #TODO: use smarter logic instead of incrementing a row number
        self.set_selection(self.rowno+1,self.colno)
    
    def move_up(self):
        #TODO: use smarter logic instead of decrementing a row number
        self.set_selection(self.rowno-1,self.colno)
    
    def move_left(self):
        #TODO: use smarter logic instead of decrementing a column number
        self.set_selection(self.rowno,self.colno-1)
    
    def move_right(self):
        #TODO: use smarter logic instead of decrementing a column number
        self.set_selection(self.rowno,self.colno+1)
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Down',self.move_down)
        self.gui.bind('Up',self.move_up)
        self.gui.bind('Left',self.move_left)
        self.gui.bind('Right',self.move_right)
    
    def enable_grid(self):
        #TODO
        #self.table.show_grid(True)
        pass
    
    def disable_grid(self):
        #TODO
        #self.table.show_grid(False)
        pass
    
    def hide_headers(self):
        #TODO
        #self.table.hide_x_header()
        #self.table.hide_y_header()
        pass
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.panel = gi.Panel()
        self.gui.set_gui(self.table.gui,self.panel)
        self.set_title()
        self.hide_headers()
        self.disable_grid()
        self.set_bindings()
    
    def fail(self,f,e):
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        sh.objs.get_mes(f,mes).show_error()


if __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    sh.com.start()
    lg.objs.get_plugins(Debug=False,maxrows=1000)
    db = DB()
    data = db.fetch()
    rownum = db.get_max_row_no()
    colnum = db.get_max_col_no()
    if rownum is not None:
        rownum += 1
    if colnum is not None:
        colnum += 1
    blocks = lg.com.set_blocks(data)
    cells = lg.Cells(blocks).run()
    timer = sh.Timer(f + ': Showing GUI')
    timer.start()
    app = App()
    app.reset(cells,rownum,colnum)
    ''' We can get a constant mouse hovering response only if we install
        the filter like this.
    '''
    sh.objs.get_root().installEventFilter(app.gui.panel)
    sh.objs.get_root().installEventFilter(app.gui.table)
    #app.gui.table.enter_cell(app.table.set_mouse_over)
    timer.end()
    app.show()
    db.close()
    sh.com.end()
