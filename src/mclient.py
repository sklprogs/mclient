#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
import gui as gi

DEBUG = False


class Formatter:
    
    def __init__(self,block):
        self.Success = True
        self.code = ''
        self.block = block
    
    def check(self):
        f = '[MClientQt] mclient.Formatter.check'
        if not self.block:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_code(self):
        f = '[MClientQt] mclient.Formatter.set_code'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.code = self.block.text
    
    def _set_italic(self):
        if self.block.Italic:
            self.code = '<i>' + self.code + '</i>'
    
    def _set_bold(self):
        if self.block.Bold:
            self.code = '<b>' + self.code + '</b>'
    
    def _set_size(self):
        sub = '<span style="font-size:{}pt">{}</span>'
        self.code = sub.format(self.block.size,self.code)
    
    def _set_face(self):
        sub = '<font face="{}" color="{}">'
        sub = sub.format(self.block.family,self.block.color)
        self.code = sub + self.code
    
    def format(self):
        f = '[MClientQt] mclient.Formatter.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._set_italic()
        self._set_bold()
        self._set_face()
        self._set_size()
    
    def run(self):
        self.check()
        self.set_code()
        self.format()
        return self.code



class Cell:
    
    def __init__(self,cell):
        self.Success = True
        self.gui = gi.Cell()
        self.widget = self.gui.widget
        self.cell = cell
        self.code = []
    
    def check(self):
        f = '[MClient] mclient.Cell.check'
        if not self.cell:
            sh.com.rep_empty(f)
            self.Success = False
    
    def run(self):
        self.check()
        self.format()
        self.set()
        
    def format(self):
        f = '[MClient] mclient.Cell.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        for block in self.cell:
            self.code.append(Formatter(block).run())
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        sh.objs.get_mes(f,mes).show_error()
    
    def set(self):
        f = '[MClient] mclient.Cell.set'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.gui.set_text(''.join(self.code))
        except Exception as e:
            self.fail(f,e)



class Block:
    
    def __init__(self):
        self.type_ = 'invalid'
        self.text = ''
        self.rowno = -1
        self.colno = -1
        self.cellno = -1
        self.family = 'Serif'
        self.color = 'black'
        self.size = 12
        self.Bold = False
        self.Italic = False



class Cells:
    
    def __init__(self,data):
        self.Success = True
        self.cells = []
        self.cell = []
        self.data = data
        self.check()
    
    def check(self):
        f = '[MClient] mclient.Cells.check'
        if not self.data:
            sh.com.rep_empty(f)
            self.Success = False
            return
    
    def run(self):
        self.assign()
        self.debug()
    
    def assign(self):
        f = '[MClient] mclient.Cells.assign'
        if not self.Success:
            sh.com.cancel(f)
            return
        old_cellno = 0
        old_rowno = 0
        cell = []
        row = []
        for item in self.data:
            block = Block()
            block.type_ = item[0]
            block.text = item[1]
            block.rowno = item[2]
            block.colno = item[3]
            block.cellno = item[4]
            block = lg.Font(block).run()
            if old_cellno == block.cellno:
                cell.append(block)
            elif old_rowno == block.rowno:
                if cell:
                    row.append(cell)
                cell = [block]
                old_cellno = block.cellno
            else:
                if row:
                    self.cells.append(row)
                cell = [block]
                row = []
                old_rowno = block.rowno
                old_cellno = block.cellno
        if cell:
            row.append(cell)
        if row:
            self.cells.append(row)
    
    def debug(self):
        f = '[MClient] mclient.Cells.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not DEBUG:
            sh.com.rep_lazy(f)
            return
        cells2 = []
        cell2 = []
        for row in self.cells:
            row2 = []
            for cell in row:
                cell2 = []
                for block in cell:
                    block2 = [block.type_,block.text,block.rowno
                             ,block.colno,block.cellno
                             ]
                    cell2.append(block2)
                row2.append(cell2)
            cells2.append(row2)
        print(cells2)



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
        query = 'select COLNO from BLOCKS where BLOCK = 0 and \
                        IGNORE = 0 order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = '[MClient] mclient.DB.get_max_row_no'
        query = 'select ROWNO from BLOCKS where BLOCK = 0 \
                 and IGNORE = 0 order by ROWNO desc'
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
        self.cells = []
        self.rowno = 0
        self.colno = 0
        self.rownum = 0
        self.colnum = 0
        self.complex = 0
        self.single = 0
    
    def minimize(self):
        self.gui.minimize()
    
    def reset(self,cells,rownum,colnum):
        self.cells = cells
        self.rownum = rownum
        self.colnum = colnum
        self.clear()
        self.set_view()
        self.fill()
    
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
    
    def move_down(self):
        #TODO: use smarter logic instead of incrementing a row number
        self.set_mouse_over(self.rowno+1,self.colno)
    
    def move_up(self):
        #TODO: use smarter logic instead of decrementing a row number
        self.set_mouse_over(self.rowno-1,self.colno)
    
    def move_left(self):
        #TODO: use smarter logic instead of decrementing a column number
        self.set_mouse_over(self.rowno,self.colno-1)
    
    def move_right(self):
        #TODO: use smarter logic instead of decrementing a column number
        self.set_mouse_over(self.rowno,self.colno+1)
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Alt+C',self.clear)
        self.gui.table.enter_cell(self.set_mouse_over)
        self.gui.bind('Down',self.move_down)
        self.gui.bind('Up',self.move_up)
        self.gui.bind('Left',self.move_left)
        self.gui.bind('Right',self.move_right)
    
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
    
    def fail(self,f,e):
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        sh.objs.get_mes(f,mes).show_error()
    
    def create_cell(self,text):
        f = '[MClient] mclient.App.create_cell'
        try:
            return self.gui.table.create_cell(text)
        except Exception as e:
            self.fail(f,e)
    
    def insert_widget(self,widget,rowno,colno):
        f = '[MClient] mclient.App.insert_widget'
        try:
            self.gui.table.insert_widget(widget,rowno,colno)
        except Exception as e:
            self.fail(f,e)
    
    def fill(self):
        f = '[MClient] mclient.App.fill'
        timer = sh.Timer(f)
        timer.start()
        for row in self.cells:
            for cell in row:
                block = cell[0]
                if len(cell) == 1:
                    if not block.text:
                        continue
                    self.single += 1
                    tabitem = self.create_cell(block.text)
                    sh.Font(tabitem,block.family,block.size).run()
                    self.gui.table.set_cell (tabitem,block.rowno
                                            ,block.colno
                                            )
                else:
                    self.complex += 1
                    icell = Cell(cell)
                    icell.run()
                    self.insert_widget (icell.widget
                                       ,block.rowno
                                       ,block.colno
                                       )
        timer.end()
        mes = _('Single-block cells: {}').format(self.single)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Multi-block cells: {}').format(self.complex)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.gui.table.add_layout()


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
    icells = Cells(data)
    icells.run()
    app = App()
    app.reset(icells.cells,rownum,colnum)
    ''' We can get a constant mouse hovering response only if we install
        the filter like this.
    '''
    sh.objs.get_root().installEventFilter(app.gui.panel)
    app.show()
    db.close()
    sh.com.end()
