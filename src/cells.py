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
    headers = (_('BLOCK'), _('CELL'), _('TYPE'), _('TEXT'), 'SOURCE', 'DIC'
              ,'SUBJ', 'SUBJF', 'SUBJPR', 'SPEECH', 'SPEECHF', 'SPEECHPR')
    nos = []
    cellnos = []
    types = []
    texts = []
    sources = []
    dics = []
    subj = []
    subjf = []
    subjpr = []
    speech = []
    speechf = []
    speechpr = []
    for block in blocks:
        nos.append(block.no)
        cellnos.append(block.cellno)
        types.append(block.type)
        texts.append(f'"{block.text}"')
        sources.append(block.source)
        dics.append(block.dic)
        subj.append(block.subj)
        subjf.append(block.subjf)
        subjpr.append(block.subjpr)
        speech.append(block.speech)
        speechf.append(block.speechf)
        speechpr.append(block.speechpr)
    mes = Table(headers = headers
               ,iterable = (nos, cellnos, types, texts, sources, dics, subj
                           ,subjf, subjpr, speech, speechf, speechpr)
               ,maxrow = maxrow, maxrows = maxrows).run()
    return f'{f}:\n{mes}'



class Elems:
    
    def __init__(self, blocks):
        self.phurl = ''
        self.art_subj = {}
        self.blocks = blocks
    
    def set_speechf(self):
        for block in self.blocks:
            block.speechf = SPEECH.expand(block.speech)
    
    def set_subjf(self):
        for block in self.blocks:
            block.subjf = SUBJECTS.expand(block.subj)
    
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
        # Works only before deleting fixed blocks and setting subjf
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
        f = '[MClient] cells.Elems.move_brackets'
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
    
    def set_no(self):
        for i in range(len(self.blocks)):
            self.blocks[i].no = i
    
    def delete_empty(self):
        f = '[MClient] cells.Elems.delete_empty'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text.strip()]
        rep.matches(f, old_len - len(self.blocks))
    
    def run(self):
        self.set_no()
        self.set_phurl()
        self.remove_phsubj()
        self.remove_numbering()
        self.convert_comments()
        self.attach_comments()
        self.move_brackets()
        # Remove empty blocks only after sources.multitrancom.elems.Trash
        self.delete_empty()
        self.fill_fixed()
        # Do this only after self.fill_fixed
        self.set_subjf()
        # Do this only after self.fill_fixed
        self.set_speechf()
        # Do this only after self.set_subjf but before self.remove_fixed
        self.set_art_subj()
        self.remove_fixed()
        return self.blocks



class Prioritize:
    
    def __init__(self, blocks):
        self.speech = SPEECH.get_settings()
        self.blocks = blocks
    
    def set_speech(self):
        all_speech = sorted(set([block.speech for block in self.blocks]))
        speech_unp = [speech for speech in all_speech \
                     if not speech in self.speech]
        all_speech = self.speech + speech_unp
        for i in range(len(all_speech)):
            for block in self.blocks:
                if block.speech == all_speech[i]:
                    block.speechpr = i
    
    def set_subjects(self):
        for block in self.blocks:
            block.subjpr = SUBJECTS.get_priority(block.subjf)
    
    def set_sources(self):
        sources = set([block.source for block in self.blocks if block.source])
        ORDER_SOURCES.reset(sources)
        for block in self.blocks:
            block.sourcepr = ORDER_SOURCES.get_priority(block.source)
    
    def run(self):
        self.set_subjects()
        self.set_speech()
        self.set_sources()
        return self.blocks



class Cells:
    
    def __init__(self, blocks):
        self.cells = []
        self.blocks = blocks
    
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
    
    def set_cells(self):
        f = '[MClient] cells.Cells.set_cells'
        if not self.blocks:
            rep.lazy(f)
            return
        cellno = -1
        cell = []
        for block in self.blocks:
            if block.cellno == cellno:
                cell.append(f'{block.cellno}-{block.no}-{block.text}')
            else:
                cellno = block.cellno
                if cell:
                    self.cells.append(cell)
                    cell = []
                cell.append(f'{block.cellno}-{block.no}-{block.text}')
        if cell:
            self.cells.append(cell)
        print(self.cells)
    
    def debug_cells(self):
        f = '[MClient] cells.Cells.debug_cells'
        for cell in self.cells:
            text = [block.text for block in cell]
            text = ' '.join(text)
            nos = [block.no for block in cell]
            min_no = min(nos)
            max_no = max(nos)
            cellnos = [block.cellno for block in cell]
            min_cellno = min(cellnos)
            max_cellno = max(cellnos)
            if min_cellno != max_cellno:
                rep.condition(f, f'{min_cellno} == {max_cellno}')
            cellno = max_cellno
            if min_no == max_no:
                print(f'{cellno}: {max_no}: "{text}"')
            else:
                print(f'{cellno}: {min_no}-{max_no}: "{text}"')
    
    def run(self):
        self.ignore_roman_numbers()
        # Set instance in order to further get blocked subjects and cells
        self.iomit = Omit(self.blocks)
        self.blocks = self.iomit.run()
        self.set_cells()
        #self.debug_cells()
        return self.blocks



class OrderSources:
    
    def __init__(self):
        self.ordered = []
        self.prior = []
    
    def reset(self, sources):
        self.sources = sources
        self.set_prior()
        self.order()
    
    def set_prior(self):
        f = '[MClient] cells.OrderSources.set_prior'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.prior = CONFIG.new['sources']['prioritized'].keys()
        mes = ', '.join(self.prior)
        Message(f, mes).show_debug()
    
    def order(self):
        f = '[MClient] cells.OrderSources.order'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        prior = [source for source in list(self.prior) \
                if source in self.sources]
        other = [source for source in self.sources if not source in prior]
        other = sorted(other, key=lambda x: x.casefold())
        self.ordered = prior + other
        mes = ', '.join(self.ordered)
        Message(f, mes).show_debug()
    
    def get_priority(self, source):
        f = '[MClient] cells.OrderSources.get_priority'
        if not CONFIG.Success:
            rep.cancel(f)
            return -1
        try:
            return self.ordered.index(source)
        except ValueError:
            # This can happen if the source is blocked
            return -1



class Omit:
    
    def __init__(self, blocks):
        self.cells = []
        self.subj = []
        self.omit = []
        self.blocks = blocks
    
    def set_subjects(self):
        f = '[MClient] cells.Omit.set_subjects'
        if not CONFIG.new['BlockSubjects']:
            rep.lazy(f)
            return
        subjects = [block.subj for block in self.blocks]
        subjects = sorted(set(subjects))
        for subject in subjects:
            if SUBJECTS.is_blocked(subject):
                self.subj.append(subject)
        mes = '; '.join(self.subj)
        Message(f, mes).show_debug()
    
    def omit_subjects(self):
        f = '[MClient] cells.Omit.omit_subjects'
        if not CONFIG.new['BlockSubjects']:
            rep.lazy(f)
            return
        for block in self.blocks:
            if block.subj in self.subj:
                block.Block = True
                self.omit.append(block)
        rep.matches(f, len(self.omit))
    
    def omit_users(self):
        f = '[MClient] cells.Omit.omit_users'
        if CONFIG.new['ShowUserNames']:
            rep.lazy(f)
            return
        count = 0
        for block in self.blocks:
            if block.type == 'user':
                count += 1
                #TODO: Block or Ignore?
                block.Block = True
        rep.matches(f, count)
    
    def run(self):
        self.set_subjects()
        self.omit_subjects()
        self.omit_users()
        return self.blocks


ORDER_SOURCES = OrderSources()