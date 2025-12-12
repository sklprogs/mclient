#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message

from articles import ARTICLES


class Table:
    ''' To keep the current article functioning if nothing was found, we do not
        use 'Success' or call 'reset' before filling.
    '''
    def __init__(self, plain=[], code=[]):
        self.set_values()
        if plain and code:
            self.reset(plain, code)
    
    def reset(self, plain, code):
        self.set_values()
        self.plain = plain
        self.code = code
        self.set_size()
        self.set_empty_cols()
    
    def set_values(self):
        self.plain = []
        self.code = []
        self.empty_cols = []
        self.rownum = 0
        self.colnum = 0
        ''' This is a constant value and should be manually changed only when
            new fixed types are introduced.
        '''
        self.fixed_num = 6
    
    def get_phsubj(self):
        f = '[MClient] table.logic.Table.get_phsubj'
        table = ARTICLES.get_table()
        if not table:
            rep.empty(f)
            return
        for row in table[::-1]:
            for cell in row:
                if cell.fixed_block and cell.fixed_block.type == 'phsubj':
                    return(cell.text, cell.fixed_block.url)
    
    def get_first_term(self):
        f = '[MClient] table.logic.Table.get_first_term'
        table = ARTICLES.get_table()
        if not table:
            rep.empty(f)
            return
        for row in table:
            for cell in row:
                for block in cell.blocks:
                    if block.type == 'term' and block.text.strip():
                        return(cell.rowno, cell.colno)
    
    def _is_col_empty(self, colno):
        for rowno in range(self.rownum):
            # Cell texts should already be stripped
            if self.plain[rowno][colno]:
                return
        return True
    
    def set_empty_cols(self):
        f = '[MClient] table.logic.Table.set_empty_cols'
        #TODO: Should we run this for fixed columns only?
        for colno in range(self.colnum):
            if self._is_col_empty(colno):
                self.empty_cols.append(colno)
        if self.empty_cols:
            mes = _('Columns with no text: {}')
            mes = mes.format(', '.join([str(item) for item in self.empty_cols]))
        else:
            mes = _('All columns have texts')
        Message(f, mes).show_debug()
    
    def get_next_row_by_col(self, rowno, colno, ref_colno):
        f = '[MClient] table.logic.Table.get_next_row_by_col'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        tuple_ = self._get_next_row(rowno, ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_next_row(rowno - 1, colno)
            if tuple_:
                return tuple_
        elif rowno > 0:
            return self.get_next_row_by_col(-1, colno, ref_colno)
        return(rowno, colno)
    
    def get_prev_row_by_col(self, rowno, colno, ref_colno):
        f = '[MClient] table.logic.Table.get_prev_row_by_col'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        tuple_ = self._get_prev_row(rowno, ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_prev_row(rowno + 1, colno)
            if tuple_:
                return tuple_
        elif rowno < self.rownum:
            return self.get_prev_row_by_col(self.rownum, colno, ref_colno)
        return(rowno, colno)
    
    def _get_next_col(self, rowno, colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_next_col(self, rowno, colno):
        f = '[MClient] table.logic.Table.get_next_col'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        start = rowno
        while rowno < self.rownum:
            if rowno == start:
                tuple_ = self._get_next_col(rowno, colno)
            else:
                tuple_ = self._get_next_col(rowno, -1)
            if tuple_:
                return tuple_
            rowno += 1
        if colno + 1 < self.colnum:
            colno += 1
        if rowno >= self.rownum:
            return self.get_start()
        return(rowno, colno)
    
    def _get_prev_col(self, rowno, colno):
        while colno > 0:
            colno -= 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_prev_col(self, rowno, colno):
        f = '[MClient] table.logic.Table.get_prev_col'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        start = rowno
        while rowno >= 0:
            if rowno == start:
                tuple_ = self._get_prev_col(rowno, colno)
            else:
                tuple_ = self._get_prev_col(rowno, self.colnum)
            if tuple_:
                return tuple_
            rowno -= 1
        if colno > 0:
            colno -= 1
        if rowno < 0:
            return self.get_end()
        return(rowno, colno)
    
    def _get_prev_row(self, rowno, colno):
        while rowno > 0:
            rowno -= 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_prev_row(self, rowno, colno):
        f = '[MClient] table.logic.Table.get_prev_row'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        start = colno
        while colno >= 0:
            if start == colno:
                tuple_ = self._get_prev_row(rowno, colno)
            else:
                tuple_ = self._get_prev_row(self.rownum, colno)
            if tuple_:
                return tuple_
            colno -= 1
        if colno < 0:
            return self.get_end()
        return(rowno, colno)
    
    def _get_next_row(self, rowno, colno):
        while rowno + 1 < self.rownum:
            rowno += 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_next_row(self, rowno, colno):
        f = '[MClient] table.logic.Table.get_next_row'
        if not self.plain:
            rep.empty(f)
            return(rowno, colno)
        start = colno
        while colno < self.colnum:
            if start == colno:
                tuple_ = self._get_next_row(rowno, colno)
            else:
                tuple_ = self._get_next_row(-1, colno)
            if tuple_:
                return tuple_
            colno += 1
        if colno >= self.colnum:
            return self.get_start()
        return(rowno, colno)
    
    def get_start(self):
        return self.get_next_col(0, -1)
    
    def get_line_start(self, rowno):
        return self.get_next_col(rowno, -1)
    
    def get_line_end(self, rowno):
        return self.get_prev_col(rowno, self.colnum)
    
    def set_size(self):
        f = '[MClient] table.logic.Table.set_size'
        if not self.plain:
            rep.empty(f)
            return
        self.rownum = len(self.plain)
        self.colnum = len(self.plain[0])
        mes = _('Table size: {}×{}').format(self.rownum, self.colnum)
        Message(f, mes).show_debug()
    
    def get_end(self):
        return self.get_prev_col(self.rownum - 1, self.colnum)
