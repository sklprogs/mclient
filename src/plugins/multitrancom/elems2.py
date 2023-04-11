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



class Elems:
    
    def __init__(self,blocks):
        self.cells = []
        self.blocks = blocks
    
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
        headers = (_('CELL #'),_('TEXT'))
        nos = []
        texts = []
        for cell in self.cells:
            nos.append(cell.no)
            texts.append(cell.text)
        return sh.FastTable (headers = headers
                            ,iterable = (nos,texts)
                            ,maxrow = 150
                            ,maxrows = 1000
                            ).run()
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = sh.List(fragms).space_items().strip()
    
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
    
    def run(self):
        self.run_phcount()
        self.set_cells()
        self.delete_semi()
        self.set_text()
        self.delete_trash()
        self.renumber()
