#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table
from skl_shared.logic import Text

import instance as ic


class Trash:
    
    def __init__(self, blocks):
        self.Parallel = False
        self.head = self.tail = None
        self.blocks = blocks
    
    def _get_head_comments(self):
        pos = None
        for i in range(len(self.blocks)):
            if self.blocks[i].type != 'comment':
                pos = i
                break
        if pos is None or pos < 4:
            return
        if set([block.type for block in self.blocks[:pos]]) == {'comment'}:
            return pos - 1
    
    def _get_head_wform(self):
        # Get trash head for general articles
        pos = None
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'wform' and self.blocks[i].text == ' ':
                pos = i
                break
        ''' If 'wform' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 0):
            return
        if set([block.type for block in self.blocks[:pos]]) == {'comment'}:
            return pos
    
    def _get_head_subj(self):
        ''' Get trash head (phrase section, all subjects). The first term
            should be 'Subject' of 'subj' type and next two terms should denote
            languages.
        '''
        pos = None
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type == 'subj' and not self.blocks[i-2].url \
            and self.blocks[i-1].type == 'term' and not self.blocks[i-1].url \
            and self.blocks[i].type == 'term' and not self.blocks[i].url:
                pos = i
                break
            i += 1
        ''' If 'term' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 2):
            return
        if set([block.type for block in self.blocks[:pos-2]]) == {'comment'}:
            return pos
    
    def _get_head_term(self):
        ''' Get trash head (phrase section, single subject). The first two
            terms should denote languages.
        '''
        pos = None
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type == 'term' and not self.blocks[i-1].url \
            and self.blocks[i].type == 'term' and not self.blocks[i].url:
                pos = i
                break
            i += 1
        ''' If 'term' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 1):
            return
        if set([block.type for block in self.blocks[:pos-1]]) == {'comment'}:
            return pos
    
    def set_head(self):
        pos = self._get_head_wform()
        if pos is not None:
            self.head = pos
            return
        pos = self._get_head_subj()
        if pos is not None:
            self.Parallel = True
            self.head = pos
            return
        pos = self._get_head_term()
        if pos is not None:
            self.Parallel = True
            self.head = pos
            return
        pos = self._get_head_comments()
        if pos is not None:
            self.head = pos
    
    def set_tail(self):
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type != 'comment':
                return
            if self.blocks[i].text == '<!--':
                self.tail = i
                return
            i -= 1
    
    def report(self):
        f = '[MClient] plugins.multitrancom.elems.Trash.report'
        if self.head is not None:
            delete = [block.text for block in self.blocks[:self.head]]
            delete = List(delete).space_items()
            mes = _('Start fragment: "{}"').format(delete)
            Message(f, mes).show_debug()
        if self.tail is not None:
            delete = [block.text for block in self.blocks[self.tail:]]
            delete = List(delete).space_items()
            mes = _('End fragment: "{}"').format(delete)
            Message(f, mes).show_debug()
    
    def delete(self):
        f = '[MClient] plugins.multitrancom.elems.Trash.delete'
        old_len = len(self.blocks)
        # Tail must be deleted first
        if self.tail is not None:
            self.blocks = self.blocks[:self.tail]
        if self.head is not None:
            self.blocks = self.blocks[self.head+1:]
        rep.matches(f, old_len-len(self.blocks))
    
    def remove_stresses(self):
        # Remove useless "stresses" block
        f = '[MClient] plugins.multitrancom.elems.Trash.remove_stresses'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not block.url.startswith('a=467&s=')]
        rep.matches(f, old_len-len(self.blocks))
    
    def run(self):
        self.remove_stresses()
        self.set_head()
        self.set_tail()
        self.report()
        self.delete()
        return self.blocks



class Thesaurus:
    ''' - "English thesaurus" wform becoming 'subj';
        - Thesaurus is optional, so we use 'rep_lazy' instead of 'cancel'.
    '''
    def __init__(self, blocks):
        self.no = None
        self.names = ('Английский тезаурус', 'Русский тезаурус')
        # en: 1; ru: 2; de: 3; fr: 4; es: 5; he: 6; pl: 14; zh: 17; uk: 33
        self.en = ('English thesaurus', 'Английский тезаурус'
                  ,'Englisch Thesaurus', 'Anglais glossaire', 'Inglés tesauro'
                  ,'אנגלית אוצר מילים', 'Angielski tezaurus', '英语 词库'
                  ,'Англійський тезаурус')
        self.ru = ('Russian thesaurus', 'Русский тезаурус'
                  ,'Russisch Thesaurus', 'Russe glossaire', 'Ruso tesauro'
                  ,'רוסית אוצר מילים', 'Rosyjski tezaurus', '俄语 词库'
                  , 'Російський тезаурус')
        self.names = self.en + self.ru
        self.blocks = blocks
    
    def set_no(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'comment' \
            and self.blocks[i].text in self.names:
                self.no = i
                self.blocks[self.no].text = self.blocks[self.no].subj = _('thes.')
                self.blocks[self.no].subjf = _('Thesaurus')
                return
    
    def add(self):
        f = '[MClient] plugins.multitrancom.elems.Thesaurus.add'
        if self.no is None:
            rep.lazy(f)
            return
        count = 0
        i = self.no + 1
        while i < len(self.blocks):
            if self.blocks[i].type == 'subj':
                count += 1
                self.blocks[i].text = List([self.blocks[self.no].text, ','
                                          ,self.blocks[i].text]).space_items()
                self.blocks[i].subj = List([self.blocks[self.no].subj, ','
                                          ,self.blocks[i].subj]).space_items()
                self.blocks[i].subjf = List([self.blocks[self.no].subjf
                                           ,',', self.blocks[i].subjf]).space_items()
            i += 1
        rep.matches(f, count)
    
    def delete(self):
        f = '[MClient] plugins.multitrancom.elems.Thesaurus.delete'
        if self.no is None:
            rep.lazy(f)
            return
        try:
            del self.blocks[self.no]
        except IndexError:
            # This should never happen. We did the search in the same class.
            rep.wrong_input(f, self.no)
    
    def run(self):
        self.set_no()
        self.add()
        self.delete()
        return self.blocks



class SeparateWords:
    
    def __init__(self, blocks):
        self.patterns = (' - найдены отдельные слова'
                        ,' - only individual words found'
                        ,' - einzelne Wörter gefunden'
                        ,' - se han encontrado palabras individuales'
                        ,' - знайдено окремі слова'
                        ,' - znaleziono osobne słowa'
                        ,' - 只找到单语')
        self.Separate = False
        self.blocks = blocks
    
    def has(self):
        for block in self.blocks:
            if block.text in self.patterns:
                self.Separate = True
                break
        return self.Separate
    
    def add_subject(self):
        block = ic.Block()
        block.type = 'subj'
        block.text = block.subjf = _('Separate words')
        block.subj = _('sep. words')
        self.blocks.insert(0, block)
    
    def set_terms(self):
        for block in self.blocks:
            block.type = 'term'
    
    def set(self):
        f = '[MClient] plugins.multitrancom.elems.SeparateWords.set'
        if not self.blocks:
            rep.empty(f)
            return
        if len(self.blocks) < 2:
            rep.wrong_input(f, [block.text for block in self.blocks])
            return
        blocks = [self.blocks[0]]
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].text in ('|', '// -->'):
                blocks.append(self.blocks[i])
            i += 1
        rep.deleted(f, len(self.blocks)-len(blocks))
        self.blocks = blocks
    
    def run(self):
        f = '[MClient] plugins.multitrancom.elems.SeparateWords.run'
        if not self.has():
            rep.lazy(f)
            # Blocks are further assigned, do not return None
            return self.blocks
        self.set()
        self.set_terms()
        self.add_subject()
        return self.blocks



class Suggestions:
    
    def __init__(self, blocks):
        self.patterns = (' Варианты замены: ', ' Suggest: '
                        ,' Mögliche Varianten: ', ' Variantes de sustitución: '
                        ,' Варіанти заміни: ', ' Opcje zamiany: ', ' 建议: ')
        self.head = None
        self.tail = None
        # This class can be either failed or interrupted where necessary
        self.Success = True
        self.pattern = ['Forvo', '|', '+']
        self.blocks = blocks
    
    def _has(self, text):
        for pattern in self.patterns:
            if pattern in text:
                return True
    
    def has(self):
        f = '[MClient] plugins.multitrancom.elems.Suggestions.has'
        if not self.Success:
            rep.lazy(f)
            return
        for block in self.blocks:
            if block.type != 'comment':
                continue
            for pattern in self.patterns:
                if pattern == block.text:
                    return
        self.Success = False
        rep.lazy(f)
    
    def set_types(self):
        f = '[MClient] plugins.multitrancom.elems.Suggestions.set_types'
        if not self.Success:
            rep.lazy(f)
            return
        count = 0
        for block in self.blocks:
            if block.type != 'comment':
                mes = _('Unexpected block type: "{}"!').format(block.type)
                Message(f, mes).show_warning()
                continue
            if block.text.strip() == ';':
                continue
            if not block.url:
                count += 1
                # ' Suggest: ' pattern should be stripped
                block.text = block.text.strip()
                block.type = 'subj'
                block.subj = block.subjf = block.text
                block.cellno = count - 1
            elif block.url.startswith('l1='):
                count += 1
                block.type = 'term'
                block.cellno = count - 1
        rep.matches(f, count)
    
    def set_head(self):
        f = '[MClient] plugins.multitrancom.elems.Suggestions.set_head'
        if not self.Success:
            rep.lazy(f)
            return
        texts = [block.text for block in self.blocks]
        found = List(texts, self.pattern).find()
        if found is None:
            self.Success = False
            ''' This should be a warning since we have already determined that
                the article suggests words.
            '''
            rep.empty_output(f)
            return
        if found[1] >= len(self.blocks) - 1:
            # There is no place for tail
            self.Success = False
            rep.wrong_input(f)
            return
        self.head = found[1] + 1
        block = self.blocks[self.head]
        mes = _('Block #{}. Text: "{}". URL: {}')
        mes = mes.format(self.head, block.text, block.url)
        Message(f, mes).show_debug()
    
    def set_tail(self):
        # This one must be "ask in forum"
        f = '[MClient] plugins.multitrancom.elems.Suggestions.set_tail'
        if not self.Success:
            rep.lazy(f)
            return
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].url.startswith('a=46&'):
                mes = _('Block #{}. Text: "{}". URL: {}')
                mes = mes.format(i, self.blocks[i].text, self.blocks[i].url)
                Message(f, mes).show_debug()
                self.tail = i
                return
            i -= 1
        self.Success = False
        ''' This should be a warning since we have already determined that the
            article suggests words.
        '''
        rep.empty_output(f)

    def cut(self):
        f = '[MClient] plugins.multitrancom.elems.Suggestions.cut'
        if not self.Success:
            rep.lazy(f)
            return
        old_len = len(self.blocks)
        self.blocks = self.blocks[self.head:self.tail]
        rep.deleted(f, old_len-len(self.blocks))
    
    def debug(self):
        # Orphaned
        f = '[MClient] plugins.multitrancom.elems.Suggestions.debug'
        if not self.Success:
            rep.lazy(f)
            return
        for i in range(len(self.blocks)):
            block = self.blocks[i]
            mes = _('Block #{}. Type: "{}". Text: "{}". URL: "{}"')
            mes = mes.format(i, block.type, block.text, block.url)
            Message(f, mes).show_debug()
    
    def delete_semi(self):
        # Seems that Elems.delete_semi is not enough
        f = '[MClient] plugins.multitrancom.elems.Suggestions.delete_semi'
        if not self.Success:
            rep.lazy(f)
            return
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                      if not block.text in ('; ', ';')]
        rep.deleted(f, old_len-len(self.blocks))
    
    def run(self):
        self.has()
        self.set_head()
        self.set_tail()
        self.cut()
        self.delete_semi()
        self.set_types()
        return self.blocks



class Elems:
    
    def __init__(self, blocks):
        self.cells = []
        self.art_subj = {}
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
        self.blocks = blocks
    
    def save_urls(self):
        for cell in self.cells:
            if not cell.fixed_block:
                continue
            if cell.fixed_block.type == 'subj':
                self.fixed_urls[cell.fixed_block.type][cell.fixed_block.subj] = cell.url
                self.fixed_urls[cell.fixed_block.type][cell.fixed_block.subjf] = cell.url
            elif cell.fixed_block.type in ('phsubj', 'wform') and cell.url:
                self.fixed_urls[cell.fixed_block.type][cell.text] = cell.url
    
    def _is_block_fixed(self, block):
        return block.type in ('subj', 'wform', 'speech', 'transc', 'phsubj')
    
    def _get_fixed_block(self, cell):
        for block in cell.blocks:
            if block.Fixed:
                return block
    
    def set_fixed_blocks(self):
        for block in self.blocks:
            block.Fixed = self._is_block_fixed(block)
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.fixed_block = self._get_fixed_block(cell)
    
    def run_phcount(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.run_phcount'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type in ('phrase', 'comment') \
            and self.blocks[i].type == 'phcount':
                count += 1
                self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        rep.matches(f, count)
    
    def set_cells(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_cells'
        if not self.blocks:
            rep.empty(f)
            return
        if len(self.blocks) < 2:
            rep.condition(f, f'{len(self.blocks)} >= 2')
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
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def debug(self):
        report = [self._debug_blocks(), self._debug_cells()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def _debug_blocks(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.multitrancom.elems.Elems._debug_blocks'
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
    
    def _debug_cells(self, maxrow=70, maxrows=0):
        f = '[MClient] plugins.multitrancom.elems.Elems._debug_cells'
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
        mes = Table(headers = headers
                   ,iterable = (subj, wform, speech, transc, rownos, nos, types
                               ,texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = Text(cell.text).delete_duplicate_spaces()
    
    def delete_semi(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_semi'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text != '; ']
        rep.matches(f, old_len-len(self.blocks))
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.unite_brackets'
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
    
    def separate_fixed(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.separate_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            # There can be multiple 'wform' blocks
            if self.blocks[i-1].Fixed and self.blocks[i].Fixed \
            and self.blocks[i-1].type != self.blocks[i].type:
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        rep.matches(f, count)
    
    def separate_sp_transc(self):
        ''' There can be structures like 'wform + comment + speech/transc', but
            speech and transc should always take a separate cell.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.separate_sp_transc'
        count = 0
        i = 1
        while i < len(self.blocks):
            # It is not enough to set 'Fixed'
            if self.blocks[i].type in ('speech', 'transc'):
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        rep.matches(f, count)
    
    def set_transc(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                count += 1
                block.type = 'transc'
        rep.matches(f, count)
    
    def delete_empty(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_empty'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text.strip()]
        rep.matches(f, old_len-len(self.blocks))
    
    def convert_user_subj(self):
        # "Gruzovik" and other entries that function as 'subj'
        f = '[MClient] plugins.multitrancom.elems.Elems.convert_user_subj'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type == 'user' \
            and self.blocks[i-1].cellno != self.blocks[i].cellno:
                count += 1
                self.blocks[i].type = 'subj'
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
    
    def set_see_also(self):
        # Example: "beg the question"
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type == 'term' \
            and self.blocks[i-1].text == '⇒ ' \
            and self.blocks[i].type == 'term':
                self.blocks[i-1].type = 'subj'
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
                if not self.blocks[i-1].url:
                    self.blocks[i-1].url = self.blocks[i].url
            i += 1
    
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
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
    def strip_blocks(self):
        # Needed for 'phsubj' and such 'wform' as 'English Thesaurus'
        for block in self.blocks:
            if not block.Fixed:
                continue
            block.text = block.text.strip()
    
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
        f = '[MClient] plugins.multitrancom.elems.Elems.set_row_nos'
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
    
    def set_art_subj(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
        rep.matches(f, count)
    
    def set_not_found(self):
        for block in self.blocks:
            if block.type == 'comment' and block.text \
            and block.url.startswith('a=46&'):
                self.blocks = []
                return
    
    def renumber_by_type(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.renumber_by_type'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                if self.blocks[i].type in ('user', 'correction', 'phcount') \
                or self.blocks[i].text in (')', ']', '}'):
                    for block in self.blocks:
                        if block.cellno == self.blocks[i].cellno:
                            count += 1
                            block.cellno = self.blocks[i-1].cellno
            i += 1
        rep.matches(f, count)
    
    def run_com_sp_com(self):
        ''' '<em>' tag usually denoting a speech part can actually be
            a comment: EN-RU: bit.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.run_com_sp_com'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type == 'comment' \
            and self.blocks[i-1].type == 'speech' \
            and self.blocks[i].type == 'comment':
                self.blocks[i-1].type = 'comment'
            i += 1
        rep.matches(f, count)
    
    def unite_comments(self):
        # Fix dangling brackets: EN-RU: bit
        f = '[MClient] plugins.multitrancom.elems.Elems.unite_comments'
        count = 0
        i = len(self.blocks) - 2
        while i >= 0:
            if self.blocks[i].type == self.blocks[i+1].type == 'comment':
                count += 1
                self.blocks[i].text = List([self.blocks[i].text
                                          ,self.blocks[i+1].text]).space_items()
                del self.blocks[i+1]
            i -= 1
        rep.matches(f, count)
    
    def run(self):
        # Find thesaurus before deleting empty blocks
        self.blocks = Thesaurus(self.blocks).run()
        iseparate = SeparateWords(self.blocks)
        self.blocks = iseparate.run()
        isuggest = Suggestions(self.blocks)
        self.blocks = isuggest.run()
        # Remove trash only after setting separate words
        itrash = Trash(self.blocks)
        self.blocks = itrash.run()
        self.Parallel = itrash.Parallel
        self.Separate = iseparate.Separate or isuggest.Success
        self.set_not_found()
        # Remove empty blocks only after removing trash
        self.delete_empty()
        self.set_transc()
        self.separate_sp_transc()
        self.convert_user_subj()
        self.set_see_also()
        self.set_fixed_blocks()
        self.separate_fixed()
        self.run_phcount()
        self.strip_blocks()
        self.delete_semi()
        self.run_com_sp_com()
        self.unite_comments()
        self.renumber_by_type()
        self.set_cells()
        self.set_urls()
        self.unite_brackets()
        self.set_text()
        self.set_fixed_cells()
        self.rename_phsubj()
        self.set_row_nos()
        self.save_urls()
        self.set_art_subj()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
