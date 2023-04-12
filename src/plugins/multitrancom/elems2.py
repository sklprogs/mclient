#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Cell:
    
    def __init__(self):
        self.code = ''
        self.text = ''
        self.no = -1
        self.blocks = []
        self.Fixed = False
        self.Ignore = False



class Elems:
    
    def __init__(self,blocks):
        self.cells = []
        self.blocks = blocks
    
    def _is_block_fixed(self,block):
        return block.type_ in ('dic','wform','speech','transc','phdic')
    
    def _is_cell_fixed(self,cell):
        for block in cell.blocks:
            if block.Fixed:
                return True
    
    def set_fixed_blocks(self):
        for block in self.blocks:
            block.Fixed = self._is_block_fixed(block)
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.Fixed = self._is_cell_fixed(cell)
    
    def run_phcount(self):
        f = 'plugins.multitrancom.elems.Elems.run_phcount'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type_ in ('phrase','comment') \
            and self.blocks[i].type_ == 'phcount':
                count += 1
                self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_cells(self):
        f = 'plugins.multitrancom.elems.Elems.set_cells'
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            sh.com.rep_condition(f,mes)
            return
        cell = Cell()
        cell.blocks.append(self.blocks[0])
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cell.blocks.append(self.blocks[i])
            else:
                if cell.blocks:
                    self.cells.append(cell)
                cell = Cell()
                cell.blocks.append(self.blocks[i])
            i += 1
        if cell.blocks:
            self.cells.append(cell)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def debug(self):
        #headers = (_('CELL #'),_('IGNORE'),_('FIXED'),_('TEXT'),_('TYPES'))
        headers = (_('FIXED'),_('CELL #'),_('TYPES'),_('TEXT'))
        nos = []
        texts = []
        fixed = []
        #ignore = []
        types = []
        for cell in self.cells:
            nos.append(cell.no)
            fixed.append(cell.Fixed)
            #ignore.append(cell.Ignore)
            texts.append(cell.text)
            cell_types = [block.type_ for block in cell.blocks]
            types.append(', '.join(cell_types))
        return sh.FastTable (headers = headers
                            ,iterable = (fixed,nos,types,texts)
                            ,maxrow = 130
                            ,maxrows = 0
                            ).run()
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = sh.List(fragms).space_items().strip()
            # 'phdic' text may have multiple spaces for some reason
            cell.text = sh.Text(cell.text).delete_duplicate_spaces()
    
    def delete_semi(self):
        f = 'plugins.multitrancom.elems.Elems.delete_semi'
        count = 0
        for cell in self.cells:
            old_len = len(cell.blocks)
            cell.blocks = [block for block in cell.blocks if block.text != '; ']
            count += old_len - len(cell.blocks)
        sh.com.rep_matches(f,count)
    
    def delete_trash(self):
        f = 'plugins.multitrancom.elems.Elems.delete_trash'
        old_len = len(self.cells)
        self.cells = [cell for cell in self.cells \
                      if not '<!-- -->' in cell.text \
                      and not '<!-- // -->' in cell.text
                     ]
        # The first cell represents an article title
        if len(self.cells) > 1:
            del self.cells[0]
        sh.com.rep_matches(f,old_len-len(self.cells))
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = 'plugins.multitrancom.elems.Elems.unite_brackets'
        count = 0
        for cell in self.cells:
            i = 1
            while i < len(cell.blocks):
                if cell.blocks[i-1].text.strip() == '(' \
                or cell.blocks[i].text.strip() == ')':
                    count += 1
                    cell.blocks[i-1].text = cell.blocks[i-1].text + cell.blocks[i].text
                    del cell.blocks[i]
                i += 1
        sh.com.rep_matches(f,count)
    
    def separate_fixed(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.separate_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            # There can be multiple 'wform' blocks
            if self.blocks[i-1].Fixed and self.blocks[i].Fixed \
            and self.blocks[i-1].type_ != self.blocks[i].type_:
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        sh.com.rep_matches(f,count)
    
    def separate_speech(self):
        ''' Speech can come in structures like 'wform + comment + speech', but
            it should always take a separate cell.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.separate_speech'
        count = 0
        i = 1
        while i < len(self.blocks):
            # It is not enough to set 'Fixed'
            if self.blocks[i].type_ == 'speech':
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_transc(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type_ == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                count += 1
                block.type_ = 'transc'
        sh.com.rep_matches(f,count)
    
    def delete_empty(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_empty'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text.strip()]
        sh.com.rep_matches(f,old_len-len(self.blocks))
    
    def run(self):
        self.delete_empty()
        self.set_transc()
        self.separate_speech()
        self.set_fixed_blocks()
        self.separate_fixed()
        self.run_phcount()
        self.set_cells()
        self.delete_semi()
        self.unite_brackets()
        self.set_text()
        self.delete_trash()
        self.set_fixed_cells()
        self.renumber()
