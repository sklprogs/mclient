#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message


class Table:
    ''' To keep the current article functioning if nothing was found, we do not
        use 'Success' or call 'reset' before filling.
    '''
    def __init__(self, blocks=[]):
        self.BlockMode = False
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
        self.up = []
        self.down = []
        self.left = []
        self.right = []
    
    def reset(self, blocks):
        self.set_values()
        self.blocks = blocks
        self.set_size()
        self.set_navigation()
    
    def _get_page_block(self, colno, row_min, row_max):
        for block in self.blocks:
            if block.colno == colno and block.rowno >= row_min \
            and block.rowno <= row_max and block.text.strip() \
            and not block.Ignore:
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
            and block.text.strip() and not block.Ignore:
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
            if block.type == 'term' and block.text.strip() and not block.Ignore:
                return block
    
    def get_start(self):
        for block in self.blocks:
            if block.text.strip() and not block.Ignore:
                return block
    
    def get_end(self):
        for block in self.blocks[::-1]:
            if block.text.strip() and not block.Ignore:
                return block
    
    def _get_left(self, block):
        rowno = block.rowno
        colno = block.colno
        for block in self.blocks[::-1]:
            if block.rowno == rowno and block.colno < colno \
            and block.text.strip() and not block.Ignore:
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
            if block.rowno < rowno and block.text.strip() and not block.Ignore:
                return block
        return self.get_end()
    
    def _get_right(self, block):
        rowno = block.rowno
        colno = block.colno
        for block in self.blocks:
            if block.rowno == rowno and block.colno > colno \
            and block.text.strip() and not block.Ignore:
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
            if block.rowno > rowno and block.text.strip() and not block.Ignore:
                return block
        return self.get_start()
    
    def set_size(self):
        f = '[MClient] table.logic.Table.set_size'
        if not self.blocks:
            rep.empty(f)
            return
        ''' No need to take into account IGNORE here. If blocks are ignored,
            CODE is not assigned. Empty columns have zero width.
        '''
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
        ''' We need to return even empty blocks here. If empty fixed blocks are
            not allowed, rewrite this code.
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
            and block.text.strip() and not block.Ignore:
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
            if block.colno > colno and block.text.strip() and not block.Ignore:
                return block
        return self.get_start()
    
    def set_navigation(self):
        self.up = sorted(self.blocks, key=lambda block: (-block.colno, -block.rowno))
        self.down = sorted(self.blocks, key=lambda block: (block.colno, block.rowno))
        self.right = sorted(self.blocks, key=lambda block: (block.rowno, block.colno))
        self.left = sorted(self.blocks, key=lambda block: (-block.rowno, -block.colno))
    
    def _get_adjacent(self, ref_block):
        f = '[MClient] table.logic.Table._get_adjacent'
        if not ref_block:
            rep.empty(f)
            return
        print(f, f'Final block: "{ref_block.text}": row #{ref_block.rowno}, col #{ref_block.colno}, cell #{ref_block.cellno}, block #{ref_block.no}')
        for block in self.blocks:
            if block.rowno == ref_block.rowno and block.colno == ref_block.colno + 2:
                print(f, f'Adjacent block: "{block.text}": row #{block.rowno}, col #{block.colno}, cell #{block.cellno}, block #{block.no}')
                return
    
    def _get_next_cell(self, ref_block, lst):
        f = '[MClient] table.logic.Table._get_next_cell'
        if not ref_block or not lst:
            rep.empty(f)
            return
        try:
            pos = lst.index(ref_block)
        except ValueError:
            return
        try:
            block = lst[pos + 1]
        except IndexError:
            return
        if not block:
            rep.empty(f)
            return
        if block.Ignore or not block.text.strip() \
        or ref_block.cellno == block.cellno:
            block = self._get_next_cell(block, lst)
        self._get_adjacent(block)
        return block
    
    def get_up(self, block):
        block = self._get_next_cell(block, self.up)
        if block:
            return block
        return self.get_end()
    
    def get_down(self, block):
        block = self._get_next_cell(block, self.down)
        if block:
            return block
        return self.get_start()
    
    def get_right(self, block):
        block = self._get_next_cell(block, self.right)
        if block:
            return block
        return self.get_start()
    
    def get_left(self, block):
        block = self._get_next_cell(block, self.left)
        if block:
            return block
        return self.get_end()
    
    '''
    def _get_up(self, rowno, colno, ref_block):
        for block in self.blocks[::-1]:
            if block.rowno != rowno or block.colno != colno:
                continue
            if block.Ignore or not block.text.strip():
                continue
            if self.BlockMode and block.cellno == ref_block.cellno \
            and block.no < ref_block.no:
                return block
            if block.colno == ref_block.colno \
            and block.rowno < ref_block.rowno:
                return block
            if block.colno < ref_block.colno:
                return block
    
    def get_up(self, ref_block):
        # When going from bottom to top, iterate by columns and then by rows
        f = '[MClient] table.logic.Table.get_up'
        if not self.check_block(ref_block):
            rep.cancel(f)
            return
        print(f, f'Reference block: "{ref_block.text}": row #{ref_block.rowno}, col #{ref_block.colno}, cell #{ref_block.cellno}, block #{ref_block.no}')
        colno = ref_block.colno
        while colno >= 0:
            rowno = self.rownum - 1
            while rowno >= 0:
                block = self._get_up(rowno, colno, ref_block)
                if block:
                    print(f, f'Found block: "{block.text}": row #{block.rowno}, col #{block.colno}, cell #{block.cellno}, block #{block.no}')
                    return block
                rowno -= 1
            colno -= 1
    '''
    
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
            and block.text.strip() and not block.Ignore:
                return block
    
    def get_line_end(self, block):
        f = '[MClient] table.logic.Table.get_line_end'
        if not self.check_block(block):
            rep.cancel(f)
            return
        rowno = block.rowno
        for block in self.blocks[::-1]:
            if block.rowno == rowno and block.text.strip() and not block.Ignore:
                return block
