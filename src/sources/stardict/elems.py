#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.table import Table
from skl_shared.list import List
from skl_shared.logic import Text, punc_array, ru_alphabet, lat_alphabet

from instance import Block, is_block_fixed

SPEECH_ABBR = ('гл.', 'нареч.', 'нар.', 'прил.', 'сокр.', 'сущ.')
SUBJ_ABBR = ('амер.', 'вчт.', 'геогр.', 'карт.', 'мор.', 'разг.', 'уст.', 'хир.', 'эл.')
#TODO: read from file
SUBJ = ('(австралийское)', '(американизм)', '(военное)', '(горное)'
       ,'(железнодорожное)', '(карточное)', '(кулинарное)', '(новозеландское)'
       ,'(профессионализм)', '(разговорное)', '(сленг)', '(спортивное)'
       ,'(текстильное)', '(теннис)', '(химическое)', '(электротехника)')


class Phrases:
    
    def __init__(self, blocks):
        self.blocks = blocks
    
    def _get_prev_wform(self, blockno):
        i = blockno
        while i >= 0:
            if self.blocks[i].type == 'wform':
                return self.blocks[i].text
            i -= 1
    
    def replace_seps(self):
        f = '[MClient] sources.stardict.elems.Phrases.replace_seps'
        for i in range(len(self.blocks)):
            if self.blocks[i].type not in ('term', 'phrase'):
                continue
            wform = self._get_prev_wform(i)
            if not wform:
                rep.empty(f)
                continue
            self.blocks[i].text = self.blocks[i].text.replace('~', wform)
            self.blocks[i].text = self.blocks[i].text.replace('*', wform)
            self.blocks[i].text = self.blocks[i].text.strip()
    
    def _get_first_lang(self, line):
        for char in line:
            if char in ru_alphabet:
                return 'ru'
            elif char in lat_alphabet:
                return 'en'
    
    def _get_new_lang_pos(self, line, first_lang):
        for i in range(len(line)):
            if line[i] in ru_alphabet and first_lang == 'en':
                return i
            elif line[i] in lat_alphabet and first_lang == 'ru':
                return i
    
    def _split_block(self, block):
        f = '[MClient] sources.stardict.elems.Phrases._split_block'
        first_lang = self._get_first_lang(block.text)
        if not first_lang:
            rep.empty(f)
            return
        pos = self._get_new_lang_pos(block.text, first_lang)
        if pos is None:
            rep.empty(f)
            return
        part1 = block.text[:pos].strip()
        part2 = block.text[pos:].strip()
        if not part1 or not part2:
            rep.empty(f)
            return
        block.text = part1
        new_block = copy.deepcopy(block)
        new_block.text = part2
        return new_block
    
    def split(self):
        f = '[MClient] sources.stardict.elems.Phrases.split'
        blocks = []
        for block in self.blocks:
            blocks.append(block)
            if block.type != 'phrase':
                continue
            new_block = self._split_block(block)
            if not new_block:
                rep.empty(f)
                continue
            block.cellno += 0.1
            blocks.append(new_block)
        self.blocks = blocks
    
    def remove_trash(self):
        for block in self.blocks:
            block.text = block.text.strip(' ≈')
            block.text = block.text.strip(' ∙')
            block.text = block.text.strip(' >')
            block.text = block.text.replace('≈', '—')
    
    def fix_bracket(self):
        # Fix bracket after splitting phrases (we should not join them)
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].text.endswith(' ('):
                self.blocks[i-1].text = self.blocks[i-1].text.strip(' (')
                self.blocks[i].text = '(' + self.blocks[i].text
            i += 1
    
    def run(self):
        self.replace_seps()
        self.split()
        self.remove_trash()
        self.fix_bracket()
        return self.blocks



class Elems:

    def __init__(self, blocks):
        f = '[MClient] sources.stardict.elems.Elems.__init__'
        self.art_subj = {}
        self.Parallel = False
        self.Separate = False
        self.blocks = blocks
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def set_art_subj(self):
        f = '[MClient] sources.stardict.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
                self.art_subj[block.subjf] = block.subj
        rep.matches(f, count)
    
    def set_speech(self):
        f = '[MClient] sources.stardict.elems.Elems.set_speech'
        count = 0
        for block in self.blocks:
            if block.text in SPEECH_ABBR:
                count += 1
                block.type = 'speech'
        rep.matches(f, count)
    
    def set_subjects(self):
        f = '[MClient] sources.stardict.elems.Elems.set_subjects'
        count = 0
        for block in self.blocks:
            if block.text in SUBJ_ABBR or block.text in SUBJ:
                count += 1
                block.type = 'subj'
        rep.matches(f, count)
    
    def set_source(self):
        for block in self.blocks:
            block.source = _('Stardict')
    
    def separate_term(self):
        ''' This can be necessary if the dictionary is incorrectly tagged -
            terms following transcription can be not tagged at all.
        '''
        f = '[MClient] sources.stardict.elems.Elems.separate_term'
        count = 0
        i = 1
        while i < len(self.blocks):
            if is_block_fixed(self.blocks[i-1]) \
            and self.blocks[i].type == 'term' \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                count += 1
                self.blocks[i].cellno += 0.01
            i += 1
        rep.matches(f, count)
    
    def run(self):
        f = '[MClient] sources.stardict.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return []
        self.set_subjects()
        self.set_speech()
        self.set_source()
        self.set_art_subj()
        self.separate_term()
        self.set_phrases()
        self.blocks = Phrases(self.blocks).run()
        return self.blocks
    
    def debug(self, maxrow=30, maxrows=0):
        f = '[MClient] sources.stradict.elems.Elems.debug'
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

    def _has_sep(self, fragm):
        for sep in ('~', '≈', '*'):
            if sep in fragm:
                return True
    
    def _is_mixed(self, fragm):
        return Text(fragm).has_latin() and Text(fragm).has_cyrillic()
    
    def _is_phrase(self, fragm):
        return self._has_sep(fragm) and self._is_mixed(fragm)
    
    def set_phrases(self):
        for block in self.blocks:
            if self._is_phrase(block.text):
                block.type = 'phrase'
