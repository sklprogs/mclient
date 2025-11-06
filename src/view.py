#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table

from instance import Block, Cell
from config import CONFIG
from manager import PLUGINS
from format import Block as fmBlock
from logic import Speech
from subjects import SUBJECTS
from articles import ARTICLES
from columns import COL_WIDTH, Types as ColTypes


class Expand:
    
    def __init__(self, cells):
        ''' - Runs just after 'elems'. Fixed types are not restored yet at this
              point.
            - Run this class before blocking and prioritization since short and
              full values can be sorted differently (especially this concerns
              subjects, in which first letters of shortened and full texts may
              differ).
            - Creating a full clone of cells is necessary since blocks and
              cells change their attributes. 'list' or 'copy.copy' is not
              enough. Works with None.
        '''
        self.cells = copy.deepcopy(cells)
    
    def expand_speeches(self):
        # This takes ~0.0015s for 'set' on AMD E-300 (no IDE, no warnings)
        f = '[MClient] view.Expand.expand_speeches'
        if CONFIG.new['ShortSpeech']:
            rep.lazy(f)
            return
        speeches = PLUGINS.get_speeches()
        if not speeches:
            rep.lazy(f)
            return
        for cell in self.cells:
            try:
                cell.speech = speeches[cell.speech]
            except KeyError:
                mes = _('Wrong input data: "{}"!').format(cell.speech)
                Message(f, mes, True).show_warning()
    
    def expand_subjects(self):
        # This takes ~0.0086s for 'set' on AMD E-300
        f = '[MClient] view.Expand.expand_subjects'
        if CONFIG.new['ShortSubjects']:
            rep.lazy(f)
            return
        for cell in self.cells:
            cell.subj = SUBJECTS.expand(cell.subj)
    
    def run(self):
        self.expand_speeches()
        self.expand_subjects()
        return self.cells



class Omit:
    
    def __init__(self, cells):
        self.cells = cells
        self.subj = []
        self.omit_cells = []
    
    def set_subjects(self):
        f = '[MClient] view.Omit.set_subjects'
        if not CONFIG.new['BlockSubjects']:
            rep.lazy(f)
            return
        subjects = [cell.subj for cell in self.cells]
        subjects = sorted(set(subjects))
        for subject in subjects:
            if SUBJECTS.is_blocked(subject):
                self.subj.append(subject)
        mes = '; '.join(self.subj)
        Message(f, mes).show_debug()
    
    def omit_subjects(self):
        f = '[MClient] view.Omit.omit_subjects'
        if not CONFIG.new['BlockSubjects']:
            rep.lazy(f)
            return
        cells = []
        for cell in self.cells:
            if cell.subj in self.subj:
                # Fixed types are not recreated yet
                self.omit_cells.append(cell.text)
            else:
                cells.append(cell)
        rep.matches(f, len(self.cells) - len(cells))
        self.cells = cells
        mes = _('Omitted cells: {}').format('; '.join(self.omit_cells))
        Message(f, mes).show_debug()
    
    def omit_users(self):
        f = '[MClient] view.Omit.omit_users'
        if CONFIG.new['ShowUserNames']:
            rep.lazy(f)
            return
        count = 0
        for cell in self.cells:
            old_len = len(cell.blocks)
            cell.blocks = [block for block in cell.blocks if block.type != 'user']
            delta = old_len - len(cell.blocks)
            if delta:
                fragms = [block.text for block in cell.blocks]
                cell.text = List(fragms).space_items().strip()
            count += delta
        rep.matches(f, count)
    
    def run(self):
        self.set_subjects()
        self.omit_subjects()
        self.omit_users()
        return self.cells



class Prioritize:
    
    def __init__(self, cells):
        self.speech = Speech().get_settings()
        self.cells = cells
    
    def debug(self, maxrow=60):
        f = '[MClient] view.Prioritize.debug'
        subj = []
        subjpr = []
        text = []
        nos = []
        speech = []
        speechpr = []
        for cell in self.cells:
            text.append(cell.text)
            nos.append(cell.no)
            subj.append(cell.subj)
            subjpr.append(cell.subjpr)
            speech.append(cell.speech)
            speechpr.append(cell.speechpr)
        headers = (_('#'), _('TEXT'), _('SUBJECT'), 'SUBJPR', _('SPEECH')
                  ,'SPEECHPR')
        iterable = [nos, text, subj, subjpr, speech, speechpr]
        mes = Table(headers = headers
                   ,iterable = iterable
                   ,maxrow = maxrow).run()
        return f + ':\n' + mes
    
    def set_speech(self):
        ph_cells = [cell for cell in self.cells if is_phrase_type(cell)]
        all_speech = sorted(set([cell.speech for cell in self.cells \
                                 if not cell in ph_cells]))
        speech_unp = [speech for speech in all_speech \
                     if not speech in self.speech]
        all_speech = self.speech + speech_unp
        for i in range(len(all_speech)):
            for cell in self.cells:
                if cell.speech == all_speech[i]:
                    cell.speechpr = i
        ''' Phrases must be put at the end, otherwise we will have issues in
            the "Cut to the chase" mode.
        '''
        i += 1
        for cell in ph_cells:
            cell.speechpr = i
    
    def get_last_sorted_wform(self):
        ''' Fix a bug when phrases are not at the bottom in the Multitran mode.
            Alternatively, we can use just set 'wform' to 'яяяяя' here
            (Cyrillic letters are sorted such that they are farther in a
            descending order than Latin ones), but this looks hacky.
        '''
        wforms = sorted(set([cell.wform for cell in self.cells]), reverse=True)
        if wforms:
            return wforms[0]
    
    def set_subjects(self):
        ''' All cells must have 'subjpr' set since they will not be further
            sorted by 'subj', so do not cancel this procedure even if there are
            no prioritized subjects, otherwise there may be sorting bugs, e.g.
            multitran.com, EN-RU, 'full of it'.
        '''
        for cell in self.cells:
            priority = SUBJECTS.get_priority(cell.subj)
            if priority is not None:
                cell.subjpr = priority
        pr_cells = [cell for cell in self.cells if cell.subjpr > -1]
        unp_cells = [cell for cell in self.cells if cell.subjpr == -1 \
                    and not is_phrase_type(cell)]
        ph_cells = [cell for cell in self.cells if cell.subjpr == -1 \
                   and is_phrase_type(cell)]
        
        pr_cells.sort(key=lambda x: (x.subjpr, x.no))
        unp_cells.sort(key=lambda x: (x.subj.lower(), x.no))
        
        ''' Keep old 'subjpr' if 'subj' is the same since we may need to
            alphabetize terms later.
        '''
        subj = ''
        subjpr = -1
        for cell in pr_cells:
            if cell.subj == subj:
                cell.subjpr = subjpr
            else:
                subj = cell.subj
                subjpr += 1
                cell.subjpr = subjpr
        for cell in unp_cells:
            if cell.subj == subj:
                cell.subjpr = subjpr
            else:
                subj = cell.subj
                subjpr += 1
                cell.subjpr = subjpr
        wform = self.get_last_sorted_wform()
        if not wform:
            ''' Cyrillic letters are sorted such that they are farther in a
                descending order than Latin ones.
            '''
            wform = 'яяяяя'
        for cell in ph_cells:
            if cell.subj == subj:
                cell.subjpr = subjpr
            else:
                subj = cell.subj
                subjpr += 1
                cell.subjpr = subjpr
            cell.wform = wform
        # [] + ['example'] == ['example']
        self.cells = pr_cells + unp_cells + ph_cells
    
    def run(self):
        self.set_subjects()
        self.set_speech()
        return self.cells



class View:
    # Create user-specific cells
    def __init__(self, cells):
        self.Success = True
        self.phi = None
        self.view = []
        self.cells = cells
        self.fixed_urls = ARTICLES.get_fixed_urls()
        # Must be recreated for each article loading/reloading
        self.fixed_cols = ColTypes().run()
    
    def check(self):
        f = '[MClient] view.View.check'
        if not self.cells:
            self.Success = False
            rep.empty(f)
            return
    
    def sort(self):
        f = '[MClient] view.View.sort'
        if not self.Success:
            rep.cancel(f)
            return
        if CONFIG.new['AlphabetizeTerms'] and not ARTICLES.is_parallel() \
        and not ARTICLES.is_separate():
            self.cells.sort(key=lambda x: (x.col1, x.col2, x.col3, x.col4, x.col5, x.col6, x.text, x.no))
        else:
            self.cells.sort(key=lambda x: (x.col1, x.col2, x.col3, x.col4, x.col5, x.col6, x.no))
    
    def _create_fixed(self, i, type_, rowno):
        f = '[MClient] view.View._create_fixed'
        cell = Cell()
        block = Block()
        block.type = type_
        cell.fixed_block = block
        cell.blocks = [block]
        cell.rowno = rowno
        if is_phrase_type(self.cells[i]):
            cell.subjpr = self.cells[i].subjpr
            cell.speechpr = self.cells[i].speechpr
            if type_ == 'subj':
                cell.text = block.text = self.cells[i].subj
            return cell
        cell.source = self.cells[i].source
        cell.dic = self.cells[i].dic
        cell.subj = self.cells[i].subj
        cell.subjpr = self.cells[i].subjpr
        cell.wform = self.cells[i].wform
        cell.transc = self.cells[i].transc
        cell.speech = self.cells[i].speech
        cell.speechpr = self.cells[i].speechpr
        if type_ == 'source':
            cell.text = block.text = self.cells[i].source
        elif type_ == 'dic':
            cell.text = block.text = self.cells[i].dic
        elif type_ == 'subj':
            cell.text = block.text = self.cells[i].subj
        elif type_ == 'wform':
            cell.text = block.text = self.cells[i].wform
        elif type_ == 'transc':
            cell.text = block.text = self.cells[i].transc
        elif type_ == 'speech':
            cell.text = block.text = self.cells[i].speech
        elif not type_:
            # Empty types are actually allowed since we can have empty columns
            pass
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(type_, 'source, dic, subj, wform, transc, speech, or empty')
            Message(f, mes, True).show_error()
        return cell
    
    def restore_fixed(self):
        f = '[MClient] view.View.restore_fixed'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        i = 1
        while i < len(self.cells):
            if self.cells[i-1].rowno != self.cells[i].rowno:
                rowno = self.cells[i].rowno
                for type_ in self.fixed_cols:
                    count += 1
                    cell = self._create_fixed(i, type_, rowno)
                    self.cells.insert(i, cell)
                    i += 1
            i += 1
        rep.matches(f, count)
    
    def restore_first(self):
        # Add fixed cells for the very first row
        f = '[MClient] view.View.restore_first'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        rowno = self.cells[0].rowno
        for type_ in self.fixed_cols[::-1]:
            count += 1
            cell = self._create_fixed(0, type_, rowno)
            self.cells.insert(0, cell)
        rep.matches(f, count)
    
    def _has_phrase(self):
        for cell in self.cells[::-1]:
            for block in cell.blocks:
                if block.type == 'phrase':
                    return True
    
    def restore_phsubj(self):
        f = '[MClient] view.View.restore_phsubj'
        if not self.Success:
            rep.cancel(f)
            return
        if not self._has_phrase():
            rep.lazy(f)
            return
        i = len(self.cells) - 1
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type == 'subj':
                self.cells[i].fixed_block.type = 'phsubj'
                self.phi = i
                mes = f'"{self.cells[i].fixed_block.text}"'
                Message(f, mes).show_debug()
                return
            i -= 1
    
    def debug(self, maxrow=35):
        f = '[MClient] view.View.debug'
        if not self.Success:
            rep.cancel(f)
            return
        headers = (_('ROW #'), _('CELL #'), _('TEXT'), _('TYPES'), 'URL'
                  ,'COL1' ,'COL2', 'COL3', 'COL4', 'COL5', 'COL6')
        rowno = []
        no = []
        text = []
        types = []
        url = []
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        col5 = []
        col6 = []
        for cell in self.cells:
            rowno.append(cell.rowno)
            no.append(cell.no)
            text.append(cell.text)
            url.append(cell.url)
            col1.append(cell.col1)
            col2.append(cell.col2)
            col3.append(cell.col3)
            col4.append(cell.col4)
            col5.append(cell.col5)
            col6.append(cell.col6)
            cell_types = []
            for block in cell.blocks:
                cell_types.append(block.type)
            types.append(', '.join(cell_types))
        iterable = [rowno, no, text, types, url, col1, col2, col3, col4, col5, col6]
        return Table(headers=headers, iterable=iterable, maxrow=maxrow).run()
    
    def _renumber_cell_nos(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def _renumber_row_nos(self):
        # Actually, we do this for prettier debug output
        rownos = [0]
        rowno = 0
        i = 1
        while i < len(self.cells):
            if self.cells[i-1].rowno != self.cells[i].rowno:
                rowno += 1
            rownos.append(rowno)
            i += 1
        i = 0
        while i < len(self.cells):
            self.cells[i].rowno = rownos[i]
            i += 1
    
    def renumber(self):
        f = '[MClient] view.View.renumber'
        if not self.Success:
            rep.cancel(f)
            return
        self._renumber_cell_nos()
        self._renumber_row_nos()
    
    def clear_duplicates(self):
        f = '[MClient] view.View.clear_duplicates'
        if not self.Success:
            rep.cancel(f)
            return
        source = dic = subj = wform = transc = speech = ''
        for cell in self.cells:
            if not cell.fixed_block:
               continue
            if cell.fixed_block.type == 'source':
                if cell.text == source:
                    cell.text = cell.fixed_block.text = ''
                else:
                    subj = cell.source
            elif cell.fixed_block.type == 'dic':
                if cell.text == dic:
                    cell.text = cell.fixed_block.text = ''
                else:
                    subj = cell.dic
            elif cell.fixed_block.type == 'subj':
                if cell.text == subj:
                    cell.text = cell.fixed_block.text = ''
                else:
                    subj = cell.subj
            elif cell.fixed_block.type == 'wform':
                if cell.text == wform:
                    cell.text = cell.fixed_block.text = ''
                else:
                    wform = cell.wform
            elif cell.fixed_block.type == 'transc':
                if cell.text == transc:
                    cell.text = cell.fixed_block.text = ''
                else:
                    transc = cell.transc
            elif cell.fixed_block.type == 'speech':
                if cell.text == speech:
                    cell.text = cell.fixed_block.text = ''
                else:
                    speech = cell.speech
    
    def get_fixed_url(self, type_, text):
        f = '[MClient] view.View.get_fixed_url'
        try:
            return self.fixed_urls[type_][text]
        except KeyError:
            mes = _('"{}" has not been found in "{}"!')
            if not type_ in self.fixed_urls:
                mes = mes.format(type_, self.fixed_urls)
            elif not text in self.fixed_urls[type_]:
                mes = mes.format(text, self.fixed_urls[type_])
            Message(f, mes).show_warning()
        return ''
    
    def restore_urls(self):
        f = '[MClient] view.View.restore_urls'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.fixed_urls:
            # Fixed cell URLs are relevant for multitrancom plugin only
            rep.lazy(f)
            return
        for cell in self.cells:
            if not cell.fixed_block or not cell.text:
                continue
            if cell.fixed_block.type in ('subj', 'wform', 'phsubj'):
                cell.url = cell.fixed_block.url = self.get_fixed_url(cell.fixed_block.type
                                                                    ,cell.text)
    
    def clear_phrase_fields(self):
        f = '[MClient] view.View.clear_phrase_fields'
        if not self.Success:
            rep.cancel(f)
            return
        if self.phi is None:
            rep.lazy(f)
            return
        i = self.phi
        while i < len(self.cells):
            cell = self.cells[i]
            if cell.fixed_block \
            and cell.fixed_block.type in ('source', 'dic', 'wform', 'transc', 'speech'):
                cell.text = ''
            cell.source = cell.dic = cell.wform = cell.speech = cell.transc = ''
            i += 1

    def fill_cols(self):
        f = '[MClient] view.View.fill_cols'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.fixed_cols:
            rep.lazy(f)
            return
        for cell in self.cells:
            for i in range(len(self.fixed_cols)):
                match i:
                    case 0:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col1 = cell.source.lower()
                            case 'dic':
                                cell.col1 = cell.dic.lower()
                            case 'subj':
                                cell.col1 = cell.subjpr
                            case 'wform':
                                cell.col1 = cell.wform.lower()
                            case 'speech':
                                cell.col1 = cell.speechpr
                            case 'transc':
                                cell.col1 = cell.transc.lower()
                    case 1:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col2 = cell.source.lower()
                            case 'dic':
                                cell.col2 = cell.dic.lower()
                            case 'subj':
                                cell.col2 = cell.subjpr
                            case 'wform':
                                cell.col2 = cell.wform.lower()
                            case 'speech':
                                cell.col2 = cell.speechpr
                            case 'transc':
                                cell.col2 = cell.transc.lower()
                    case 2:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col3 = cell.source.lower()
                            case 'dic':
                                cell.col3 = cell.dic.lower()
                            case 'subj':
                                cell.col3 = cell.subjpr
                            case 'wform':
                                cell.col3 = cell.wform.lower()
                            case 'speech':
                                cell.col3 = cell.speechpr
                            case 'transc':
                                cell.col3 = cell.transc.lower()
                    case 3:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col4 = cell.source.lower()
                            case 'dic':
                                cell.col4 = cell.dic.lower()
                            case 'subj':
                                cell.col4 = cell.subjpr
                            case 'wform':
                                cell.col4 = cell.wform.lower()
                            case 'speech':
                                cell.col4 = cell.speechpr
                            case 'transc':
                                cell.col4 = cell.transc.lower()
                    case 4:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col5 = cell.source.lower()
                            case 'dic':
                                cell.col5 = cell.dic.lower()
                            case 'subj':
                                cell.col5 = cell.subjpr
                            case 'wform':
                                cell.col5 = cell.wform.lower()
                            case 'speech':
                                cell.col5 = cell.speechpr
                            case 'transc':
                                cell.col5 = cell.transc.lower()
                    case 5:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col6 = cell.source.lower()
                            case 'dic':
                                cell.col6 = cell.dic.lower()
                            case 'subj':
                                cell.col6 = cell.subjpr
                            case 'wform':
                                cell.col6 = cell.wform.lower()
                            case 'speech':
                                cell.col6 = cell.speechpr
                            case 'transc':
                                cell.col6 = cell.transc.lower()
    
    def run(self):
        self.check()
        self.fill_cols()
        self.sort()
        self.restore_fixed()
        self.restore_first()
        self.restore_phsubj()
        self.clear_duplicates()
        self.clear_phrase_fields()
        self.restore_urls()
        self.renumber()
        return self.cells



class Wrap:
    
    def __init__(self, cells):
        ''' Since we create even empty columns, the number of fixed cells in
            a row should always be 6 (unless new fixed types are added).
        '''
        self.Success = True
        self.plain = []
        self.code = []
        self.cells = cells
        self.fixed_len = COL_WIDTH.fixed_num
        self.collimit = COL_WIDTH.fixed_num + COL_WIDTH.term_num
    
    def check(self):
        f = '[MClient] view.Wrap.check'
        if not self.cells:
            self.Success = False
            rep.empty(f)
            return
        if self.collimit <= self.fixed_len:
            self.Success = False
            rep.condition(f, f'{self.collimit} > {self.fixed_len}')
    
    def get_empty_cells(self, delta):
        row = []
        for type_ in range(delta):
            cell = Cell()
            cell.blocks = [Block()]
            row.append(cell)
        return row
    
    def wrap(self):
        f = '[MClient] view.Wrap.wrap'
        if not self.Success:
            rep.cancel(f)
            return
        cells = []
        row = []
        rowno = 0
        for cell in self.cells:
            if len(row) == self.collimit:
                cells.append(row)
                if cell.rowno == rowno:
                    row = self.get_empty_cells(self.fixed_len)
                else:
                    row = []
            elif cell.rowno != rowno:
                row += self.get_empty_cells(self.collimit - len(row))
                cells.append(row)
                row = []
            row.append(cell)
            rowno = cell.rowno
        row += self.get_empty_cells(self.collimit - len(row))
        cells.append(row)
        self.cells = cells
    
    def _get_prev_cell(self, i, j):
        if i >= len(self.cells):
            return
        while j >= 0:
            try:
                return self.cells[i][j]
            except IndexError:
                pass
            j -= 1
    
    def _debug_cells(self, maxrow=60, maxrows=700):
        f = '[MClient] view.Wrap._debug_cells'
        mes = [f'{f}:']
        headers = (_('CELL #'), _('ROW #'), _('COLUMN #'), _('TEXT'), _('CODE')
                  ,'URL')
        no = []
        rowno = []
        colno = []
        text = []
        code = []
        url = []
        for row in self.cells:
            for cell in row:
                no.append(cell.no)
                rowno.append(cell.rowno)
                colno.append(cell.colno)
                text.append(cell.text)
                code.append(cell.code)
                url.append(cell.url)
        iterable = [no, rowno, colno, text, code, url]
        mes += Table(headers=headers, iterable=iterable, maxrow=maxrow
                    ,maxrows=maxrows).run()
        return '\n'.join(mes)
    
    def _debug_plain(self):
        f = '[MClient] view.Wrap._debug_plain'
        mes = [f'{f}:']
        plain = []
        for row in self.cells:
            new_row = []
            for cell in row:
                text = f'({cell.rowno}, {cell.no}): {cell.text}'
                new_row.append(text)
            plain.append(new_row)
        mes.append(str(plain))
        return '\n'.join(mes)
    
    def _debug_code(self):
        f = '[MClient] view.Wrap._debug_code'
        mes = [f'{f}:']
        code = []
        for row in self.cells:
            new_row = []
            for cell in row:
                text = f'({cell.rowno}, {cell.no}): {cell.code}'
                new_row.append(text)
            code.append(new_row)
        mes.append(str(code))
        return '\n'.join(mes)
    
    def debug(self):
        f = '[MClient] view.Wrap.debug'
        if not self.Success:
            rep.cancel(f)
            return
        mes = [self._debug_cells()]
        mes.append(self._debug_plain())
        mes.append(self._debug_code())
        return '\n\n'.join(mes)
    
    def renumber(self):
        f = '[MClient] view.Wrap.renumber'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.cells[0]:
            self.Success = False
            rep.empty(f)
            return
        no = 0
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].no = no
                self.cells[i][j].rowno = i
                self.cells[i][j].colno = j
                no += 1
    
    def format(self):
        # Takes ~0.871s for 'set' on AMD E-300
        f = '[MClient] view.Wrap.format'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            for cell in row:
                cell_code = []
                for block in cell.blocks:
                    cell_code.append(fmBlock(block, cell.colno).run())
                cell.code = List(cell_code).space_items()
    
    def set_plain(self):
        f = '[MClient] view.Wrap.set_plain'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.text)
            self.plain.append(new_row)
    
    def set_code(self):
        f = '[MClient] view.Wrap.set_code'
        if not self.Success:
            rep.cancel(f)
            return
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.code)
            self.code.append(new_row)
    
    def run(self):
        self.check()
        self.wrap()
        self.renumber()
        self.format()
        self.set_plain()
        self.set_code()
        return self.cells



def is_phrase_type(cell):
    for block in cell.blocks:
        if block.type in ('phsubj', 'phrase', 'phcount'):
            return True
