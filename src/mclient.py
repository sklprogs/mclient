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
        self.set_values()
        self.gui = gi.Table()
        self.set_gui()
    
    def set_values(self):
        self.matrix = []
        self.plain = []
        self.rownum = 1
        self.colnum = 1
    
    def go_down(self):
        rowno, colno = self.get_cell()
        next_rowno = self._get_next_useful_row(rowno,colno)
        if rowno == next_rowno:
            print('Need to start over!')
            rowno = 0
        else:
            rowno = next_rowno
        self.select(rowno,colno)
    
    def select(self,rowno,colno):
        old_index = self.gui.get_index()
        new_index = self.model.index(rowno,colno)
        self.gui.set_index(new_index)
        self.gui.delegate.match_index = new_index
        self.model.update(old_index)
        self.model.update(new_index)
    
    def go_up(self):
        rowno, colno = self.get_cell()
        if rowno > 0:
            rowno -= 1
        self.select(rowno,colno)
    
    def go_left(self):
        rowno, colno = self.get_cell()
        if colno > 0:
            colno -= 1
        self.select(rowno,colno)
    
    def go_right(self):
        rowno, colno = self.get_cell()
        if colno + 1 < self.colnum:
            colno += 1
        self.select(rowno,colno)
    
    def scroll_top(self):
        f = '[MClientQt] mclient.Table.scroll_top'
        height = self.gui.get_height()
        rowno, colno = self.get_cell()
        y = self.gui.get_row_y(rowno)
        row_height = self.gui.get_row_height(rowno)
        page_y = y - height + 2 * row_height
        page_row_no = self.gui.get_row_by_y(page_y)
        new_index = self.model.index(page_row_no,colno)
        mes = _('Table height: {}, row #{}, column #{}, row height: {}, row Y: {}, page Y: {}, page row #{}')
        mes = mes.format(height,rowno,colno,row_height,y,page_y,page_row_no)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.gui.scroll2index(new_index)
    
    def go_down(self):
        f = '[MClientQt] mclient.Table.go_down'
        old_index = self.gui.get_index()
        rowno, colno = self.get_cell()
        #TODO: elaborate
        rowno += 1
        new_index = self.model.index(rowno,colno)
        self.gui.set_index(new_index)
        self.gui.delegate.match_index = new_index
        self.model.update(old_index)
        self.model.update(new_index)
    
    def go_cell(self):
        print('go_cell')
    
    def get_cell(self):
        f = '[MClientQt] mclient.Table.get_cell'
        try:
            return self.gui.get_cell()
        except Exception as e:
            sh.com.rep_third_party(f,e)
            return(0,0)
    
    def copy_cell(self):
        f = '[MClientQt] mclient.Table.copy_cell'
        rowno, colno = self.gui.get_cell()
        mes = '"' + self.plain[rowno][colno] + '"'
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def clear(self):
        self.gui.clear()
    
    def _get_last_useful_row(self,rowno,colno):
        f = '[MClientQt] mclient.Table._get_last_useful_row'
        last_rowno = self.rownum - 1
        while last_rowno >= rowno:
            if self.plain[last_rowno][colno]:
                sh.objs.get_mes(f,last_rowno,True).show_debug()
                return last_rowno
            last_rowno -= 1
        return last_rowno
    
    def _get_next_useful_row(self,rowno,colno):
        next_rowno = rowno
        while next_rowno + 1 < self.rownum:
            next_rowno += 1
            if self.plain[next_rowno][colno]:
                return next_rowno
        return rowno
    
    def set_row_height(self,height=42):
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
    
    def set_matrix(self):
        ''' Empty cells must be recreated since QTableView throws an error
            otherwise.
            #TODO: create empty cells with the 'cells' module
        '''
        old_rowno = 1
        # Reset old articles
        self.matrix = []
        self.plain = []
        row = []
        plain_row = []
        for i in range(len(self.cells)):
            if old_rowno != self.cells[i].rowno:
                if row:
                    if i > 0:
                        delta = self.colnum - self.cells[i-1].colno - 1
                        for no in range(delta):
                            row.append('')
                            plain_row.append('')
                    self.matrix.append(row)
                    self.plain.append(plain_row)
                    row = []
                    plain_row = []
                for j in range(self.cells[i].colno):
                    row.append('')
                    plain_row.append('')
                old_rowno = self.cells[i].rowno
            row.append(self.cells[i].code)
            plain_row.append(self.cells[i].plain.strip())
        if row:
            delta = self.colnum - len(row) - 1
            for no in range(delta):
                row.append('')
                plain_row.append('')
            self.matrix.append(row)
            self.plain.append(plain_row)
    
    def reset(self,cells,rownum,colnum):
        f = '[MClientQt] mclient.Table.reset'
        if not cells or not rownum or not colnum:
            sh.com.rep_empty(f)
            return
        self.cells = cells
        self.rownum = rownum
        self.colnum = colnum
        self.clear()
        self.set_matrix()
        self.model = gi.TableModel(self.matrix)
        self.fill()
        self.set_col_width()
        self.set_row_height(42)
        self.show_borders(False)
    
    def go_start(self):
        self.gui.go_start()
    
    def fill(self):
        f = '[MClientQt] mclient.Table.fill'
        timer = sh.Timer(f)
        timer.start()
        self.gui.set_model(self.model)
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
    
    def set_gui(self):
        self.gui.select = self.select
        self.gui.click_left = self.go_cell
        self.gui.click_right = self.copy_cell
        #self.set_max_row_height()



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
        self.gui = gi.App()
        self.set_gui()
        self.update_ui()
    
    def reset(self,cells,rownum,colnum):
        f = '[MClientQt] mclient.App.reset'
        mes = _('Table sizes: {}x{}').format(rownum,colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        self.table.reset(cells,rownum,colnum)
    
    def minimize(self):
        self.gui.minimize()
    
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
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Down',self.table.go_down)
        self.gui.bind('Up',self.table.go_up)
        self.gui.bind('Left',self.table.go_left)
        self.gui.bind('Right',self.table.go_right)
        self.table.gui.click_middle = self.minimize
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.panel = gi.Panel()
        self.gui.set_gui(self.table.gui,self.panel)
        self.set_title()
        self.set_bindings()


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
    timer.end()
    app.show()
    db.close()
    sh.com.end()
