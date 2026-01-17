#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table
from skl_shared.logic import Text

from instance import Block, Cell, is_block_fixed


class Elems:
    
    def __init__(self, blocks):
        self.art_subj = {}
        self.phsubj_url = ''
        self.blocks = blocks
    
    def debug(self, maxrow=30, maxrows=0):
        f = '[MClient] cells.Elems.debug'
        headers = (_('CELL #'), _('TYPES'), _('TEXT'), 'SUBJ', 'SUBJF', 'URL')
        nos = []
        types = []
        texts = []
        subj = []
        subjf = []
        urls = []
        for block in self.blocks:
            nos.append(block.cellno)
            types.append(block.type)
            texts.append(f'"{block.text}"')
            subj.append(block.subj)
            subjf.append(block.subjf)
            urls.append(block.url)
        mes = Table(headers = headers
                   ,iterable = (nos, types, texts, subj, subjf, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def set_art_subj(self):
        # Works only before deleting fixed blocks
        f = '[MClient] cells.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
        rep.matches(f, count)
    
    def remove_numbering(self):
        f = '[MClient] cells.Elems.remove_numbering'
        pattern = r'[\d+,aA-zZ,аА-яЯ][\),\.][\s]{0,1}'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not re.match(pattern, block.text)]
        rep.deleted(f, old_len - len(self.blocks))
    
    def run(self):
        self.remove_numbering()
        self.set_art_subj()
        iphrases = Phrases(self.blocks)
        self.blocks = iphrases.run()
        self.phsubj_url = iphrases.phsubj_url
        return self.blocks



class Cells:
    
    def __init__(self, blocks):
        self.cells = []
        self.blocks = blocks
    
    def _get_fixed_block(self, cell):
        for block in cell.blocks:
            if is_block_fixed(block):
                return block
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.fixed_block = self._get_fixed_block(cell)
    
    def set_cells(self):
        f = '[MClient] cells.Cells.set_cells'
        if not self.blocks:
            rep.empty(f)
            return
        if len(self.blocks) < 2:
            rep.condition(f, f'{len(self.blocks)} >= 2')
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
    
    def debug(self, maxrow=60, maxrows=0):
        f = '[MClient] cells.Cells.debug'
        headers = (_('SOURCE'), 'SUBJ', 'WFORM', 'SPEECH', 'TRANSC', _('ROW #')
                  ,_('CELL #'), _('TYPES'), _('TEXT'), 'URL')
        sources = []
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
            sources.append(cell.source)
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
        mes = Table(headers = headers
                   ,iterable = (sources, subj, wform, speech, transc, rownos
                               ,nos, types, texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] cells.Cells.unite_brackets'
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
    
    def _get_url(self, cell):
        #TODO: Do we need to support several URLs in one cell?
        for block in cell.blocks:
            if block.url:
                return block.url
        return ''
    
    def set_urls(self):
        for cell in self.cells:
            cell.url = self._get_url(cell)
    
    def _get_last_subj(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type in ('subj', 'phsubj'):
                return cell.text
        return ''
    
    def _get_last_wform(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'wform':
                return cell.text
        return ''
    
    def _get_last_speech(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'speech':
                return cell.text
        return ''
    
    def _get_last_transc(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'transc':
                return cell.text
        return ''
    
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
            if self.cells[i].fixed_block:
                if self.cells[i].fixed_block.type == 'wform':
                    return ''
                if self.cells[i].fixed_block.type == 'transc':
                    return self.cells[i].text
            i -= 1
        return ''
    
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
        f = '[MClient] cells.Cells.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] cells.Cells.set_row_nos'
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
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = Text(cell.text).delete_duplicate_spaces()
    
    def set_sources(self):
        for cell in self.cells:
            if not cell or not cell.blocks:
                continue
            cell.source = cell.blocks[0].source
            cell.dic = cell.blocks[0].dic
    
    def _has_text(self, text):
        for char in text:
            if char.isalpha():
                return True
    
    def _is_roman_number(self, text):
        return text.strip() in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII'
                               ,'IX', 'X')
    
    def delete_trash(self):
        # Either do this on cells or on blocks having unique cellno
        f = '[MClient] cells.Cells.delete_trash'
        old = len(self.cells)
        self.cells = [cell for cell in self.cells \
                     if not self._is_roman_number(cell.text)]
        self.cells = [cell for cell in self.cells if self._has_text(cell.text)]
        rep.deleted(f, old - len(self.cells))
    
    def run(self):
        self.set_cells()
        self.set_urls()
        self.unite_brackets()
        self.set_text()
        self.delete_trash()
        self.set_sources()
        self.set_fixed_cells()
        self.set_row_nos()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells



class Phrases:
    
    def __init__(self, blocks):
        self.phsubj_url = self.phsubj_name = ''
        self.blocks = blocks
        
    def move(self):
        ''' - phsubj is set to an incorrect row without this.
            - Phrases may have synonyms attached to them and formatted as
              comments, so moving by cellno is more precise.
        '''
        cellnos = [block.cellno for block in self.blocks \
                  if block.type == 'phrase']
        move = [block for block in self.blocks if block.cellno in cellnos]
        for block in move:
            block.subj = block.subjf = self.phsubj_name
        other = [block for block in self.blocks if not block.cellno in cellnos]
        self.blocks = other + [self._get_phsubj()] + move
    
    def set_phsubj_name(self):
        f = '[MClient] cells.Phrases.set_phsubj_name'
        count = 0
        for block in self.blocks:
            if block.type == 'phrase':
                count += 1
        if not count:
            rep.lazy(f)
            return
        self.phsubj_name = _('Phrases ({})').format(count)
        mes = f'"{self.phsubj_name}"'
        Message(f, mes).show_debug()
    
    def _get_phsubj(self):
        block = Block()
        block.subj = self.phsubj_name
        block.subjf = self.phsubj_name
        block.text = self.phsubj_name
        block.url = self.phsubj_url
        block.type = 'phsubj'
        return block
    
    def _get_last_subj(self):
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type in ('phsubj', 'subj') and self.blocks[i].url:
                return self.blocks[i]
            i -= 1
    
    def _has_phrases(self):
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type == 'phrase':
                return True
            i -= 1
    
    def set_phsubj_url(self):
        f = '[MClient] cells.Phrases.set_phsubj_url'
        if not self._has_phrases():
            rep.lazy(f)
            return
        block = self._get_last_subj()
        if not block:
            rep.lazy(f)
            return
        self.phsubj_url = block.url
        mes = f'URL: "{self.phsubj_url}"'
        Message(f, mes).show_debug()
    
    def renumber(self):
        cellnos = []
        old = cellno = -1
        for block in self.blocks:
            if block.cellno != old:
                cellno += 1
                old = block.cellno
            cellnos.append(cellno)
        for i in range(len(self.blocks)):
            self.blocks[i].cellno = cellnos[i]
    
    def run(self):
        ''' At this point, blocks may have identical cellno (especially, this
            concerns fixed blocks). Must be fixed before moving to the end.
        '''
        self.renumber()
        self.set_phsubj_url()
        self.set_phsubj_name()
        self.move()
        # Do this again for easier debugging
        self.renumber()
        return self.blocks
