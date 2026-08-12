#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message


class Table:
    ''' To keep the current article functioning if nothing was found, we do not
        use 'Success' or call 'reset' before filling.
    '''
    def __init__(self, blocks=[]):
        self.set_values()
        if blocks:
            self.reset(blocks)
    
    def set_values(self):
        self.rownum = 0
        self.colnum = 0
        ''' This is a constant value and should be manually changed only when
            new fixed types are introduced.
        '''
        self.fixed_num = 6
        self.blocks = []
    
    def reset(self, blocks):
        self.set_values()
        self.blocks = blocks
        self.set_size()
    
    def _get_page_block(self, colno, row_min, row_max):
        for block in self.blocks:
            if block.colno == colno and block.rowno >= row_min \
            and block.rowno <= row_max and block.text.strip():
                return block
    
    def get_page_block(self, colno, row_min, row_max):
        f = '[MClient] table.logic.Table.get_page_block'
        if row_min == -1 or row_max == -1:
            rep.cancel(f)
            return
        if colno < 0 or colno >= self.colnum:
            mes = f'0 <= {colno} < {self.colnum}'
            rep.condition(f, mes)
            return
        if row_min < 0 or row_min >= self.rownum:
            mes = f'0 <= {row_min} < {self.rownum}'
            rep.condition(f, mes)
            return
        if row_max < 0 or row_max >= self.rownum:
            mes = f'0 <= {row_max} < {self.rownum}'
            rep.condition(f, mes)
            return
        block = self._get_page_block(colno, row_min, row_max)
        if block:
            return block
        for block in self.blocks:
            if block.rowno >= row_min and block.colno >= colno \
            and block.text.strip():
                return block
    
    def check_nos(self, rowno, colno):
        f = '[MClient] table.logic.Table.check_nos'
        if rowno < 0 or rowno >= self.rownum:
            mes = f'0 <= {rowno} < {self.rownum}'
            rep.condition(f, mes)
            return
        if colno < 0 or colno >= self.colnum:
            mes = f'0 <= {colno} < {self.colnum}'
            rep.condition(f, mes)
            return
        return True
    
    def check_block(self, block):
        f = '[MClient] table.logic.Table.check_block'
        if not block:
            rep.empty(f)
            return
        return self.check_nos(block.rowno, block.colno)
    
    def get_first_term(self):
        for block in self.blocks:
            if block.type == 'term' and block.text.strip():
                return block
    
    def get_start(self):
        for block in self.blocks:
            if block.text.strip():
                return block
    
    def get_end(self):
        for block in self.blocks[::-1]:
            if block.text.strip():
                return block
    
    def _get_left(self, block):
        rowno = block.rowno
        colno = block.colno
        for block in self.blocks[::-1]:
            if block.rowno == rowno and block.colno < colno \
            and block.text.strip():
                return block
    
    def get_left(self, block):
        f = '[MClient] table.logic.Table.get_left'
        if not self.check_block(block):
            rep.cancel(f)
            return
        rowno = block.rowno
        block = self._get_left(block)
        if block:
            return block
        for block in self.blocks[::-1]:
            if block.rowno < rowno and block.text.strip():
                return block
        return self.get_end()
    
    def _get_right(self, block):
        rowno = block.rowno
        colno = block.colno
        for block in self.blocks:
            if block.rowno == rowno and block.colno > colno \
            and block.text.strip():
                return block
    
    def get_right(self, block):
        f = '[MClient] table.logic.Table.get_right'
        if not self.check_block(block):
            rep.cancel(f)
            return
        rowno = block.rowno
        block = self._get_right(block)
        if block:
            return block
        for block in self.blocks:
            if block.rowno > rowno and block.text.strip():
                return block
        return self.get_start()
    
    def set_size(self):
        f = '[MClient] table.logic.Table.set_size'
        if not self.blocks:
            rep.empty(f)
            return
        rownos = [block.rowno for block in self.blocks]
        colnos = [block.colno for block in self.blocks]
        # Row and column numbers start from 0, so we need +1 to get len
        self.rownum = max(rownos) + 1
        self.colnum = max(colnos) + 1
        mes = _('Table size: {}×{}').format(self.rownum, self.colnum)
        Message(f, mes).show_debug()
    
    def get_phsubj(self):
        f = '[MClient] table.logic.Table.get_phsubj'
        for block in self.blocks:
            if block.type == 'phsubj':
                return block
    
    def get_col(self, block, colno):
        ''' We need to return even empty blocks here. If no empty fixed blocks
            are allowed, rewrite this code.
        '''
        f = '[MClient] table.logic.Table.get_col'
        if not self.check_block(block):
            rep.cancel(f)
            return
        if colno < 0 or colno >= self.colnum:
            mes = f'0 <= {colno} < {self.colnum}'
            rep.condition(f, mes)
            return
        rowno = block.rowno
        for block in self.blocks:
            if block.rowno == rowno and block.colno == colno:
                return block
    
    def _get_down(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate rowno.
            '''
            if block.colno == colno and block.rowno > rowno \
            and block.text.strip():
                return block
    
    def get_down(self, block):
        f = '[MClient] table.logic.Table.get_down'
        if not self.check_block(block):
            rep.cancel(f)
            return
        colno = block.colno
        block = self._get_down(block)
        if block:
            return block
        for block in self.blocks:
            if block.colno > colno and block.text.strip():
                return block
        return self.get_start()
    
    def _get_up(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks[::-1]:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate rowno.
            '''
            if block.colno == colno and block.rowno < rowno \
            and block.text.strip():
                return block
    
    def get_up(self, block):
        f = '[MClient] table.logic.Table.get_up'
        if not self.check_block(block):
            rep.cancel(f)
            return
        colno = block.colno
        block = self._get_up(block)
        if block:
            return block
        for block in self.blocks[::-1]:
            if block.colno < colno and block.text.strip():
                return block
        return self.get_end()
    
    def get_next_section(self, block, colno):
        block = self.get_col(block, colno)
        return self.get_down(block)
    
    def get_prev_section(self, block, colno):
        block = self.get_col(block, colno)
        return self.get_up(block)
    
    def get_line_start(self, block):
        f = '[MClient] table.logic.Table.get_line_start'
        if not self.check_block(block):
            rep.cancel(f)
            return
        rowno = block.rowno
        for block in self.blocks:
            if block.rowno == rowno and block.colno >= self.fixed_num \
            and block.text.strip():
                return block
    
    def get_line_end(self, block):
        f = '[MClient] table.logic.Table.get_line_end'
        if not self.check_block(block):
            rep.cancel(f)
            return
        rowno = block.rowno
        for block in self.blocks[::-1]:
            if block.rowno == rowno and block.text.strip():
                return block