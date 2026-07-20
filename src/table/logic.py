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
    
    def get_start(self):
        for block in self.blocks:
            if block.text.strip():
                return block
    
    def get_end(self):
        for block in self.blocks[::-1]:
            if block.text.strip():
                return block
    
    def get_left(self, block):
        f = '[MClient] table.logic.Table.get_left'
        if not block:
            rep.empty(f)
            return
        colno = block.colno
        for block in self.blocks[::-1]:
            if block.colno < colno and block.text.strip():
                return block
        return self.get_end()
    
    def get_right(self, block):
        f = '[MClient] table.logic.Table.get_right'
        if not block:
            rep.empty(f)
            return
        colno = block.colno
        for block in self.blocks:
            if block.colno > colno and block.text.strip():
                return block
        return self.get_start()
    
    def reset(self, blocks):
        self.set_values()
        self.blocks = blocks
        self.set_size()
    
    def set_values(self):
        self.rownum = 0
        self.colnum = 0
        ''' This is a constant value and should be manually changed only when
            new fixed types are introduced.
        '''
        self.fixed_num = 6
    
    def get_phsubj(self):
        f = '[MClient] table.logic.Table.get_phsubj'
        for block in self.blocks:
            if block.type == 'phsubj':
                return block
    
    def _get_col(self, block, colno):
        ''' We need to return even empty blocks here. If no empty fixed blocks
            are allowed, rewrite this code.
        '''
        rowno = block.rowno
        for block in self.blocks:
            if block.rowno == rowno and block.colno == colno:
                return block
    
    def get_next_section(self, block, colno):
        f = '[MClient] table.logic.Table.get_next_section'
        if not self.blocks:
            rep.empty(f)
            return
        block = self._get_col(block, colno)
        if block:
            return self.get_next_row(block)
    
    def get_prev_section(self, block, colno):
        f = '[MClient] table.logic.Table.get_prev_section'
        if not self.blocks:
            rep.empty(f)
            return
        block = self._get_col(colno)
        if block:
            return self.get_prev_row(block)
    
    def _get_next_col(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate colno.
            '''
            if block.rowno == rowno and block.colno > colno \
            and block.text.strip():
                return block
    
    def _get_prev_col(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks[::-1]:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate colno.
            '''
            if block.rowno == rowno and block.colno < colno \
            and block.text.strip():
                return block
    
    def get_prev_col(self, block):
        f = '[MClient] table.logic.Table.get_prev_col'
        if not self.blocks:
            rep.empty(f)
            return
        target = self._get_prev_col(block)
        if target:
            return target
        block = self._get_col(block, 0)
        if not block:
            rep.empty(f)
            return
        return self.get_next_row(block)
    
    def _get_prev_row(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks[::-1]:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate rowno.
            '''
            if block.colno == colno and block.rowno < rowno \
            and block.text.strip():
                return block
    
    def get_prev_row(self, block):
        colno = block.colno
        block = self._get_prev_row(block)
        if block:
            return block
        for block in self.blocks[::-1]:
            if block.colno == colno and block.text.strip():
                return block
    
    def _get_next_row(self, block):
        rowno, colno = block.rowno, block.colno
        for block in self.blocks:
            ''' After blocks are sorted and wrapped, rowno and colno increase by
                design, so we don't need to iterate rowno.
            '''
            if block.colno == colno and block.rowno > rowno \
            and block.text.strip():
                return block
    
    def get_next_row(self, block):
        colno = block.colno
        block = self._get_next_row(block)
        if block:
            return block
        for block in self.blocks:
            if block.colno == colno and block.text.strip():
                return block
    
    def get_line_start(self, block):
        rowno = block.rowno
        for block in self.blocks:
            if block.rowno == rowno and block.colno > (self.fixed_num - 1) \
            and block.text.strip():
                return block
    
    def get_line_end(self, block):
        rowno = block.rowno
        for block in self.blocks[::-1]:
            if block.rowno == rowno and block.text.strip():
                return block
    
    def set_size(self):
        f = '[MClient] table.logic.Table.set_size'
        if not self.blocks:
            rep.empty(f)
            return
        rownos = [block.rowno for block in self.blocks]
        colnos = [block.colno for block in self.blocks]
        self.rownum = max(rownos)
        self.colnum = max(colnos)
        mes = _('Table size: {}×{}').format(self.rownum, self.colnum)
        Message(f, mes).show_debug()
