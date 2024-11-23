#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import rep
from skl_shared_qt.list import List
from skl_shared_qt.logic import Text, punc_array
from skl_shared_qt.table import Table

import instance as ic


class Elems:

    def __init__(self, blocks, Debug=False):
        f = '[MClient] plugins.dsl.elems.Elems.__init__'
        self.cells = []
        self.art_subj = {}
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
        self.blocks = blocks
        self.Debug = Debug
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def set_cells(self):
        f = '[MClient] plugins.dsl.elems.Elems.set_cells'
        if not self.blocks:
            rep.empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            rep.condition(f, mes)
            return
        cell = ic.Cell()
        cell.blocks.append(self.blocks[0])
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cell.blocks.append(self.blocks[i])
            else:
                if cell.blocks:
                    self.cells.append(cell)
                cell = ic.Cell()
                cell.blocks.append(self.blocks[i])
            i += 1
        if cell.blocks:
            self.cells.append(cell)
    
    def delete_trash(self):
        self.blocks = [block for block in self.blocks \
                      if block.text.strip() and block.text != ',']
    
    def divide_block(self):
        sep1 = ' || '
        sep2 = '; '
        i = 0
        while i < len(self.blocks):
            if sep1 in self.blocks[i].text \
            or sep2 in self.blocks[i].text:
                text = self.blocks[i].text
                text = text.replace(sep2, sep1)
                split = text.split(sep1)
                block = copy.copy(self.blocks[i])
                del self.blocks[i]
                for item in split[::-1]:
                    block_copy = copy.copy(block)
                    block_copy.text = item
                    self.blocks.insert(i, block_copy)
                i = i - 1 + len(split)
            i += 1
    
    def _is_block_fixed(self, block):
        return block.type in ('subj', 'wform', 'speech', 'transc', 'phsubj')
    
    def _get_fixed_block(self, cell):
        for block in cell.blocks:
            if block.Fixed:
                return block
    
    def _get_last_subj(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type in ('subj', 'phsubj'):
                return cell.text
    
    def _get_last_wform(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'wform':
                return cell.text
    
    def _get_last_speech(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'speech':
                return cell.text
    
    def _get_last_transc(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'transc':
                return cell.text
    
    def set_fixed_blocks(self):
        for block in self.blocks:
            block.Fixed = self._is_block_fixed(block)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] plugins.dsl.elems.Elems.unite_brackets'
        count = 0
        for cell in self.cells:
            i = 2
            while i < len(cell.blocks):
                if cell.blocks[i-2].text.strip() == '(' \
                and cell.blocks[i].text.strip() == ')':
                    count += 1
                    ''' Add brackets to text of a cell (usually of the 'user'
                        type), not vice versa, to preserve its type.
                    '''
                    cell.blocks[i-1].text = cell.blocks[i-2].text \
                                          + cell.blocks[i-1].text \
                                          + cell.blocks[i].text
                    del cell.blocks[i]
                    del cell.blocks[i-2]
                    i -= 2
                i += 1
        rep.matches(f, count)
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = Text(cell.text).delete_duplicate_spaces()
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.fixed_block = self._get_fixed_block(cell)
    
    def rename_phsubj(self):
        for cell in self.cells:
            if cell.fixed_block and cell.fixed_block.type == 'phsubj':
                match = re.search(r'(\d+)', cell.text)
                if match:
                    title = _('Phrases ({})').format(match.group(1))
                    # 'fill_fixed' is block-oriented
                    cell.text = cell.fixed_block.text = cell.fixed_block.subj \
                              = cell.fixed_block.subjf = title
                    # There should be only one 'phsubj'
                    return
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] plugins.dsl.elems.Elems.set_row_nos'
        count = 0
        if self.cells:
            count += 1
            self.cells[0].rowno = 0
        rowno = 0
        i = 1
        while i < len(self.cells):
            if not self.cells[i-1].fixed_block and self.cells[i].fixed_block:
                count += 1
                rowno += 1
            self.cells[i].rowno = rowno
            i += 1
        rep.matches(f, count)
    
    def fill_fixed(self):
        subj = self._get_last_subj()
        wform = self._get_last_wform()
        transc = self._get_last_transc()
        speech = self._get_last_speech()
        i = len(self.cells) - 1
        while i >= 0:
            if not self.cells[i].fixed_block:
                subj = self._get_prev_subj(i)
                wform = self._get_prev_wform(i)
                speech = self._get_prev_speech(i)
                transc = self._get_prev_transc(i)
            self.cells[i].subj = subj
            self.cells[i].wform = wform
            self.cells[i].speech = speech
            self.cells[i].transc = transc
            i -= 1
    
    def delete_fixed(self):
        f = '[MClient] plugins.dsl.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
    def set_cellno(self):
        for i in range(len(self.blocks)):
            self.blocks[i].cellno = i
    
    def _get_prev_subj(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type in ('subj', 'phsubj'):
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_wform(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'wform':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_speech(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'speech':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_transc(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'transc':
                return self.cells[i].text
            i -= 1
        return ''
    
    def run(self):
        f = '[MClient] plugins.dsl.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return []
        self.divide_block()
        self.set_phsubj()
        self.delete_trash()
        self.add_space()
        self.fill()
        #self.remove_fixed()
        #self.insert_fixed()
        self.set_cellno()
        self.set_fixed_blocks()
        self.set_cells()
        self.set_text()
        self.set_fixed_cells()
        self.rename_phsubj()
        self.set_row_nos()
        #self.save_urls()
        #self.set_art_subj()
        self.unite_brackets()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.dsl.elems.Elems._debug_cells'
        headers = ('SUBJ', 'WFORM', 'SPEECH', 'TRANSC', _('ROW #'), _('CELL #')
                  ,_('TYPES'), _('TEXT'), 'URL')
        subj = []
        wform = []
        speech = []
        transc = []
        rownos = []
        nos = []
        types = []
        texts = []
        urls = []
        for cell in self.cells:
            subj.append(cell.subj)
            wform.append(cell.wform)
            speech.append(cell.speech)
            transc.append(cell.transc)
            rownos.append(cell.rowno)
            nos.append(cell.no)
            texts.append(f'"{cell.text}"')
            cell_types = [block.type for block in cell.blocks]
            types.append(', '.join(cell_types))
            urls.append(cell.url)
        mes = [f'{f}:']
        sub = _('Cells:')
        mes.append(sub)
        sub = Table(headers = headers
                   ,iterable = (subj, wform, speech, transc, rownos, nos, types
                               ,texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        mes.append(sub)
        return '\n'.join(mes)
    
    def _debug_blocks(self, maxrow=70, maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        headers = ('NO', 'SUBJ', 'SUBJF', 'WFORM', 'SPEECH', 'TRANSC', 'TYPE'
                  ,'TEXT')
        rows = []
        for i in range(len(self.blocks)):
            rows.append([i + 1, self.blocks[i].subj, self.blocks[i].subjf
                       ,self.blocks[i].wform, self.blocks[i].speech
                       ,self.blocks[i].transc, self.blocks[i].type
                       ,self.blocks[i].text])
        mes = [f'{f}:']
        sub = _('Blocks:')
        mes.append(sub)
        sub = Table(headers = headers, iterable = rows, maxrow = maxrow
                   ,maxrows = maxrows, Transpose = True, encloser = '"').run()
        mes.append(sub)
        mes.append('')
        return '\n'.join(mes)
    
    def debug(self, maxrow=70, maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        if not self.Debug or not self.blocks:
            rep.lazy(f)
            return
        report = [self._debug_blocks(maxrow, maxrows)
                 ,self._debug_cells(maxrow, maxrows)]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def add_space(self):
        f = '[MClient] plugins.dsl.elems.Elems.add_space'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].cellno == self.blocks[i-1].cellno:
                if self.blocks[i].text and self.blocks[i-1].text \
                and not self.blocks[i].text[0].isspace() \
                and not self.blocks[i].text[0] in punc_array \
                and not self.blocks[i].text[0] in [')', ']', '}'] \
                and not self.blocks[i-1].text[-1] in ['(', '[', '{']:
                    count += 1
                    self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
        rep.matches(f, count)

    def set_phsubj(self):
        count = 0
        for block in self.blocks:
            if block.type == 'phrase':
                count += 1
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'phrase':
                block = ic.Block()
                block.type = 'phsubj'
                block.same = 0
                # There is no separate section for phrases
                block.select = 0
                mes = _('{} phrases').format(count)
                block.text = block.subj = block.subjf = mes
                self.blocks.insert(i, block)
                return True
                
    def fill(self):
        subj = wform = speech = transc = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
                break
        for block in self.blocks:
            if block.type == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type == 'transc':
                transc = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            block.subj = block.subjf = subj.strip()
            block.wform = wform
            block.speech = speech
            block.transc = transc
    
    def insert_fixed(self):
        subj = subjf = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if subj != self.blocks[i].subj or subjf != self.blocks[i].subjf \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = ic.Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)

                block = ic.Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                subj = self.blocks[i].subj
                subjf = self.blocks[i].subjf
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                      not in ('subj', 'wform', 'transc', 'speech')]
