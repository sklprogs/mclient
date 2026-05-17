#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table
from skl_shared.logic import Text

from instance import Block, is_block_fixed
from config import CONFIG
from speech import SPEECH
from subjects import SUBJECTS


def debug(blocks, maxrow=30, maxrows=0):
    f = '[MClient] cells.debug'
    headers = (_('BLOCK #'), _('CELL #'), _('TYPES'), _('TEXT'), 'SOURCE', 'DIC'
              ,'SUBJ', 'SUBJF', _('ROW #'), _('COL #'))
    nos = []
    cellnos = []
    types = []
    texts = []
    sources = []
    dics = []
    subj = []
    subjf = []
    rownos = []
    colnos = []
    for block in blocks:
        nos.append(block.no)
        cellnos.append(block.cellno)
        types.append(block.type)
        texts.append(f'"{block.text}"')
        sources.append(block.source)
        dics.append(block.dic)
        subj.append(block.subj)
        subjf.append(block.subjf)
        rownos.append(block.rowno)
        colnos.append(block.colno)
    mes = Table(headers = headers
               ,iterable = (nos, cellnos, types, texts, sources, dics, subj
                           ,subjf, rownos, colnos)
               ,maxrow = maxrow, maxrows = maxrows).run()
    return f'{f}:\n{mes}'



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
    
    def fill_fixed(self):
        source = dic = subj = subjf = wform = transc = speech = ''
        for block in self.blocks:
            if is_block_fixed(block):
                if block.type == 'source':
                    source = block.text
                elif block.type == 'dic':
                    dic = block.text
                elif block.type == 'subj':
                    subj = block.subj
                    subjf = block.subjf
                elif block.type == 'wform':
                    wform = block.text
                elif block.type == 'speech':
                    speech = block.text
                elif block.type == 'transc':
                    transc = block.text
            else:
                block.source = source
                block.dic = dic
                block.subj = subj
                block.subjf = subjf
                block.wform = wform
                block.speech = speech
                block.transc = transc
    
    def remove_fixed(self):
        f = '[MClient] cells.Elems.remove_fixed'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not is_block_fixed(block)]
        rep.deleted(f, old_len - len(self.blocks))
    
    def run(self):
        self.set_phurl()
        self.remove_phsubj()
        self.remove_numbering()
        self.set_art_subj()
        self.convert_comments()
        self.attach_comments()
        self.move_brackets()
        self.fill_fixed()
        self.remove_fixed()
        return self.blocks



class Cells:
    
    def __init__(self, blocks):
        self.blocks = blocks
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] cells.Cells.set_row_nos'
        count = 0
        if self.blocks:
            count += 1
            self.blocks[0].rowno = 0
        rowno = 0
        i = 1
        while i < len(self.blocks):
            if not is_block_fixed(self.blocks[i-1]) \
            and is_block_fixed(self.blocks[i]):
                count += 1
                rowno += 1
            self.blocks[i].rowno = rowno
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
        return self.blocks



class Expand:
    
    def __init__(self, blocks):
        ''' Run this class before blocking and prioritization since short and
            full values can be sorted differently (especially this concerns
            subjects, in which first letters of shortened and full texts may
            differ).
        '''
        self.blocks = blocks
    
    def expand_speeches(self):
        f = '[MClient] cells.Expand.expand_speeches'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        ''' Even if we expect parts of speech in a short form, we need to
            process them because they should be localized for local sources.
        '''
        if CONFIG.new['ShortSpeech']:
            for block in self.blocks:
                block.speech = SPEECH.shorten(block.speech)
            return
        for block in self.blocks:
            block.speech = SPEECH.expand(block.speech)
    
    def expand_subjects(self):
        # This takes ~0.0086s for 'set' on AMD E-300
        f = '[MClient] cells.Expand.expand_subjects'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if CONFIG.new['ShortSubjects']:
            rep.lazy(f)
            return
        for block in self.blocks:
            block.subj = SUBJECTS.expand(block.subj)
    
    def run(self):
        self.expand_speeches()
        self.expand_subjects()
        return self.blocks