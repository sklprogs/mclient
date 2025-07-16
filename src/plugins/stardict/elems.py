#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.table import Table
from skl_shared.list import List
from skl_shared.logic import Text, punc_array, ru_alphabet, lat_alphabet

import instance as ic

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
        f = '[MClient] plugins.stardict.elems.Phrases._split_block'
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
        f = '[MClient] plugins.stardict.elems.Phrases.split'
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
        f = '[MClient] plugins.stardict.elems.Elems.__init__'
        self.set_values()
        self.blocks = blocks
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)

    def set_values(self):
        self.phsubj_name = _('Phrases')
        self.cells = []
        self.art_subj = {}
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
    
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
    
    def expand_dic(self):
        #TODO (?): implement
        pass
    
    def set_cells(self):
        f = '[MClient] plugins.stardict.elems.Elems.set_cells'
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
    
    def _get_url(self, cell):
        for block in cell.blocks:
            if block.url:
                return block.url
        return ''
    
    def set_urls(self):
        for cell in self.cells:
            cell.url = self._get_url(cell)
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] plugins.stardict.elems.Elems.unite_brackets'
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
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] plugins.stardict.elems.Elems.set_row_nos'
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
        f = '[MClient] plugins.stardict.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
                self.art_subj[block.subjf] = block.subj
        rep.matches(f, count)
    
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
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'transc':
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
    
    def _get_fixed_type(self, cell):
        if cell.fixed_block:
            return cell.fixed_block.type
        else:
            return 'invalid'
    
    def delete_fixed(self):
        f = '[MClient] plugins.stardict.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        rep.matches(f, count)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def set_speech(self):
        for block in self.blocks:
            if block.text in SPEECH_ABBR:
                block.type = 'speech'
    
    def set_subjects(self):
        for block in self.blocks:
            if block.text in SUBJ_ABBR or block.text in SUBJ:
                block.type = 'subj'
    
    def set_synonyms(self):
        for block in self.blocks:
            if 'Syn :' in block.text:
                block.text = block.text.replace('Syn :', _('Synonyms:'))
                block.type = 'comment'
    
    def run(self):
        f = '[MClient] plugins.stardict.elems.Elems.run'
        if not self.Success:
            rep.cancel(f)
            return []
        self.delete_straight_line()
        self.set_subjects()
        self.set_speech()
        self.set_synonyms()
        self.set_fixed_blocks()
        self.run_comments()
        ''' These 2 procedures should not be combined (otherwise, corrections
            will have the same color as comments)
        '''
        self.unite_comments()
        self.set_com_same()
        self.add_space()
        self.expand_dic()
        self.set_phrases()
        self.move_phrases()
        self.set_phsubj_name()
        self.set_phsubj()
        self.blocks = Phrases(self.blocks).run()
        self.set_cells()
        self.set_urls()
        self.unite_brackets()
        self.set_text()
        self.set_fixed_blocks()
        self.set_fixed_cells()
        self.set_row_nos()
        self.set_art_subj()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
    
    def debug(self):
        report = [self._debug_blocks(), self._debug_cells()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def _debug_blocks(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.stradict.elems.Elems._debug_blocks'
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
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.stradict.elems.Elems._debug_cells'
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
        
    def unite_comments(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type == 'comment' \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                if i > 0 and self.blocks[i-1].type == 'comment':
                    self.blocks[i-1].text = List(lst1 = [self.blocks[i-1].text
                                                ,self.blocks[i].text]).space_items()
                    del self.blocks[i]
                    i -= 1
            i += 1
            
    def delete_straight_line(self):
        self.blocks = [block for block in self.blocks if block.text.strip() != '|']
    
    def run_comments(self):
        i = 0
        cellno = -1
        while i < len(self.blocks):
            if self.blocks[i].type in ('comment', 'correction'):
                text_str = self.blocks[i].text.strip()
                ''' Delete comments that are just ';' or ',' (we don't need
                    them, we have a table view). We delete instead of
                    assigning Block attribute because we may need to unblock
                    blocked subjects later.
                '''
                if text_str == ';' or text_str == ',':
                    del self.blocks[i]
                    i -= 1
                elif self.blocks[i].cellno == cellno:
                    # For the following cases: "23 фраз в 9 тематиках"
                    if i > 0 and self.blocks[i-1].type == 'phrase':
                        self.blocks[i].cellno = cellno
                    # Move the comment to the preceding cell
                    if text_str.startswith(',') or text_str.startswith(';') \
                    or text_str.startswith('(') or text_str.startswith(')') \
                    or text_str.startswith('|'):
                        self.blocks[i].cellno = cellno
                        # Mark the next block as a start of a new cell
                        if i < len(self.blocks) - 1 and self.blocks[i+1].type \
                        not in ('comment', 'correction'):
                            cellno += 1
                            self.blocks[i+1].cellno = cellno
            i += 1
            
    def set_com_same(self):
        ''' Sometimes sources do not provide sufficient information on
            SAMECELL blocks, and the tag parser cannot handle sequences
            such as 'any type (not same) -> comment (not same) ->
            any type (not same)'.
            Rules:
            1) (Should be always correct)
                'i >= 0 -> correction (not same)
                    =>
                'i >= 0 -> correction (same)
            2) (Preferable)
                'term (not same) -> comment (not same) -> any type
                (not same)'
                    =>
                'term (not same) -> comment (same) -> any type
                (not same)'
            3) (Generally correct before removing fixed columns)
                'dic/wform/speech/transc -> comment (not same) -> term
                (not same)'
                    =>
                'dic/wform/speech/transc -> comment (not same) -> term
                (same)'
            4) (By guess, check only after ##2&3)
                'any type (same) -> comment (not same) -> any type
                (not same)'
                    =>
                'any type (same) -> comment (same) -> any type
                (not same)'
            5) (Always correct)
                'any type -> comment/correction (not same) -> END'
                    =>
                'any type -> comment/correction (same) -> END'
            6) (Do this in the end of the loop + Readability improvement
               ("в 42 тематиках"))
                'any type (not same) -> comment (not same) -> any type
                (not same)'
                    =>
                'any type (not same) -> comment (same) -> any type
                (not same)'
        '''
        if not self.blocks:
            return
        i = 3
        while i < len(self.blocks):
            cond1 = self.blocks[i].type == 'correction'
            cond2 = False
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                cond2 = True
            cond3 = self.blocks[i-1].type == 'comment' \
                    and self.blocks[i-2].cellno == self.blocks[i-1].cellno
            cond4 = self.blocks[i-2].type == 'term' \
                    and self.blocks[i-3].cellno == self.blocks[i-2].cellno
            cond5 = self.blocks[i-3].cellno == self.blocks[i-2].cellno
            cond6 = self.blocks[i].type == 'term'
            cond7a = self.blocks[i-2].type == 'subj'
            cond7b = self.blocks[i-2].type == 'wform'
            cond7c = self.blocks[i-2].type == 'speech'
            cond7d = self.blocks[i-2].type == 'transc'
            cond7 = cond7a or cond7b or cond7c or cond7d
            # Rule 1
            if cond1 and cond2:
                self.blocks[i].same = 1
            # Rule 2
            elif cond4 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 3
            elif cond7 and cond3 and cond6 and cond2:
                self.blocks[i].same = 1
            # Rule 4:
            elif cond5 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 6:
            elif cond5 and cond3 and cond2:
                self.blocks[i-1].same = 1
            i += 1
        # Rule 5
        # After exiting the loop, the last block
        i = len(self.blocks) - 1
        cond1 = self.blocks[i].type in ('comment', 'correction')
        cond2 = self.blocks[i-1].cellno == self.blocks[i].cellno
        if cond1 and cond2:
            self.blocks[i].cellno = self.blocks[i-1].cellno
    
    def add_space(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cond = False
                if i > 0:
                    if self.blocks[i-1].text[-1] in ['(', '[', '{']:
                        cond = True
                if self.blocks[i].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in punc_array \
                  and not self.blocks[i].text[0] in [')', ']', '}'] \
                  and not cond:
                    self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1

    def _has_sep(self, fragm):
        for sep in ('~', '≈', '*'):
            if sep in fragm:
                return True
    
    def _is_mixed(self, fragm):
        return Text(fragm).has_latin() and Text(fragm).has_cyrillic()
    
    def _is_phrase(self, fragm):
        return self._has_sep(fragm) and self._is_mixed(fragm)
    
    def get_first_phrase(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'phrase':
                return i
    
    def set_phrases(self):
        for block in self.blocks:
            if self._is_phrase(block.text):
                block.type = 'phrase'
    
    def move_phrases(self):
        # phsubj is set to an incorrect row without this
        phrases = [block for block in self.blocks if block.type == 'phrase']
        other = [block for block in self.blocks if block.type != 'phrase']
        self.blocks = other + phrases
    
    def set_phsubj_name(self):
        f = '[MClient] plugins.stradict.elems.Elems.set_phsubj_name'
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
        for block in self.blocks:
            if block.type == 'phrase':
                block.subj = block.subjf = self.phsubj_name
    
    def set_phsubj(self):
        f = '[MClient] plugins.stradict.elems.Elems.set_phsubj'
        no = self.get_first_phrase()
        if no is None:
            rep.lazy(f)
            return
        block = ic.Block()
        if no > 1:
            block.cellno = self.blocks[no-1].cellno + 0.1
        block.subj = self.phsubj_name
        block.subjf = self.phsubj_name
        block.text = self.phsubj_name
        block.type = 'phsubj'
        block.Fixed = True
        self.blocks.insert(no, block)
