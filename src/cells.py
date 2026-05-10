#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table
from skl_shared.logic import Text

from instance import Block, is_block_fixed


class Elems:
    
    def __init__(self, blocks):
        self.phurl = ''
        self.art_subj = {}
        self.blocks = blocks
    
    def set_phurl(self):
        f = '[MClient] cells.Elems.set_phurl'
        for block in self.blocks:
            if block.type == 'phsubj' and block.url:
                self.phurl = block.url
                mes = f'"{self.phurl}"'
                Message(f, mes).show_debug()
                return
    
    def remove_phsubj(self):
        f = '[MClient] cells.Elems.remove_phsubj'
        cellnos = []
        for block in self.blocks:
            if block.type == 'phsubj':
                cellnos.append(block.cellno)
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not block.cellno in cellnos]
        rep.deleted(f, old_len - len(self.blocks))
    
    def debug(self, maxrow=30, maxrows=0):
        f = '[MClient] cells.Elems.debug'
        headers = (_('BLOCK #'), _('CELL #'), _('TYPES'), _('TEXT'), 'SOURCE'
                  ,'DIC', 'SUBJ', 'SUBJF', 'URL')
        nos = []
        cellnos = []
        types = []
        texts = []
        sources = []
        dics = []
        subj = []
        subjf = []
        urls = []
        for block in self.blocks:
            nos.append(block.no)
            cellnos.append(block.cellno)
            types.append(block.type)
            texts.append(f'"{block.text}"')
            sources.append(block.source)
            dics.append(block.dic)
            subj.append(block.subj)
            subjf.append(block.subjf)
            urls.append(block.url)
        mes = Table(headers = headers
                   ,iterable = (nos, cellnos, types, texts, sources, dics, subj
                               ,subjf, urls)
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
        pattern1 = r'[\d+,aA-zZ,аА-яЯ][\),\.][\s]{0,1}'
        pattern2 = r'((\s){0,1})+((\n|\r){0,1})+((\s){0,1})+\d+[\),\>]\.{0,1}((\s){0,1})+'
        count = 0
        for block in self.blocks:
            if re.fullmatch(pattern1, block.text) \
            or re.fullmatch(pattern2, block.text):
                count += 1
                block.Ignore = True
        rep.deleted(f, count)
    
    def _is_comment_like(self, group):
        for i in group:
            if not self.blocks[i].type in ('comment', 'correction', 'user'):
                return False
        return True
    
    def _is_fixed_like(self, group):
        for i in group:
            if not is_block_fixed(self.blocks[i]):
                return False
        return True
    
    def _get_groups(self):
        groups = []
        group = []
        cellno = -1
        for i in range(len(self.blocks)):
            if self.blocks[i].cellno == cellno:
                group.append(i)
            elif group:
                groups.append(group)
                group = [i]
                cellno = self.blocks[i].cellno
            else:
                group = [i]
                cellno = self.blocks[i].cellno
        if group:
            groups.append(group)
        return groups
    
    def attach_comments(self):
        f = '[MClient] cells.Elems.attach_comments'
        groups = self._get_groups()
        count = 0
        i = 1
        while i < len(groups):
            if self._is_comment_like(groups[i]) \
            and not self._is_fixed_like(groups[i-1]):
                for j in groups[i]:
                    count += 1
                    self.blocks[j].cellno = self.blocks[groups[i-1][-1]].cellno
            i += 1
        rep.matches(f, count)
    
    def convert_comments(self):
        # Or allow articles without terms or with empty terms
        f = '[MClient] cells.Elems.convert_comments'
        count = 0
        i = 1
        while i < len(self.blocks):
            if is_block_fixed(self.blocks[i-1]) \
            and self.blocks[i].type in ('comment', 'correction', 'user') \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                count += 1
                self.blocks[i].type = 'term'
                self.blocks[i].cellno += 0.01
            i += 1
        rep.matches(f, count)
    
    def move_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] cells.Cells.move_brackets'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].text.startswith(')'):
                self.blocks[i-1].text = self.blocks[i-1].text + ')'
                self.blocks[i].text = self.blocks[i].text.lstrip(')')
                self.blocks[i].text = self.blocks[i].text.lstrip()
                count += 1
            elif self.blocks[i-1].text.endswith('('):
                self.blocks[i-1].text = self.blocks[i-1].text.rstrip('(')
                self.blocks[i-1].text = self.blocks[i-1].text.rstrip()
                self.blocks[i].text = '(' + self.blocks[i].text
                count += 1
            i += 1
        rep.matches(f, count)
    
    def run(self):
        self.set_phurl()
        self.remove_phsubj()
        self.remove_numbering()
        self.set_art_subj()
        self.convert_comments()
        self.attach_comments()
        self.move_brackets()
        return self.blocks



class Cells:
    
    def __init__(self, blocks):
        self.cells = []
        self.blocks = blocks
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def debug(self, maxrow=30, maxrows=0):
        f = '[MClient] cells.Cells.debug'
        headers = ('SOURCE', 'DIC', 'SUBJ', 'WFORM', 'SPEECH', 'TRANSC'
                  ,_('ROW #'), _('CELL #'), _('TYPES'), _('TEXT'), 'URL')
        dics = []
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
            dics.append(cell.dic)
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
                   ,iterable = (sources, dics, subj, wform, speech, transc
                               ,rownos, nos, types, texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def _get_last_source(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'source':
                return cell.text
        return ''
    
    def _get_last_dic(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type == 'dic':
                return cell.text
        return ''
    
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
    
    def _get_prev_source(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'source':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_dic(self, i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'dic':
                return self.cells[i].text
            i -= 1
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
        source = self._get_last_source()
        dic = self._get_last_dic()
        subj = self._get_last_subj()
        wform = self._get_last_wform()
        transc = self._get_last_transc()
        speech = self._get_last_speech()
        i = len(self.cells) - 1
        while i >= 0:
            if not self.cells[i].fixed_block:
                source = self._get_prev_source(i)
                dic = self._get_prev_dic(i)
                subj = self._get_prev_subj(i)
                wform = self._get_prev_wform(i)
                speech = self._get_prev_speech(i)
                transc = self._get_prev_transc(i)
            self.cells[i].source = source
            self.cells[i].dic = dic
            self.cells[i].subj = subj
            self.cells[i].wform = wform
            self.cells[i].transc = transc
            self.cells[i].speech = speech
            i -= 1
    
    def delete_fixed(self):
        f = '[MClient] cells.Cells.delete_fixed'
        old_len = len(self.cells)
        self.cells = [cell for cell in self.cells if not cell.fixed_block]
        rep.deleted(f, old_len - len(self.cells))
    
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
    
    def ignore_roman_numbers(self):
        #TODO: Do this on unique cellnos only
        f = '[MClient] cells.Cells.ignore_roman_numbers'
        count = 0
        for block in self.blocks:
            if block.Ignore:
                continue
            if block.text.strip() in ('I', 'II', 'III', 'IV', 'V', 'VI', 'VII'
                                     ,'VIII', 'IX', 'X'):
                block.Ignore = True
        rep.deleted(f, count)
    
    def run(self):
        self.ignore_roman_numbers()
        self.set_row_nos()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
