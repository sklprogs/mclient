#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic
import format as fm
import logic as lg
import subjects as sj


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
        f = '[MClientQt] cells.Expand.expand_speeches'
        if sh.lg.globs['bool']['ShortSpeech']:
            sh.com.rep_lazy(f)
            return
        speeches = lg.objs.get_plugins().get_speeches()
        if not speeches:
            sh.com.rep_lazy(f)
            return
        for cell in self.cells:
            try:
                cell.speech = speeches[cell.speech]
            except KeyError:
                mes = _('Wrong input data: "{}"!').format(cell.speech)
                sh.objs.get_mes(f, mes, True).show_warning()
    
    def expand_subjects(self):
        ''' This takes ~0.0084s for 'set' on AMD E-300 (no IDE, no warnings,
            179 lines in 'subjects.json').
        '''
        f = '[MClientQt] cells.Expand.expand_subjects'
        if sh.lg.globs['bool']['ShortSubjects']:
            sh.com.rep_lazy(f)
            return
        for cell in self.cells:
            cell.subj = sj.objs.get_subjects().expand(cell.subj)
    
    def run(self):
        self.expand_speeches()
        self.expand_subjects()
        return self.cells



class Omit:
    
    def __init__(self, cells):
        self.cells = cells
    
    def omit_subjects(self):
        f = '[MClientQt] cells.Omit.omit_subjects'
        if not sh.lg.globs['bool']['BlockSubjects']:
            sh.com.rep_lazy(f)
            return
        old_len = len(self.cells)
        self.cells = [cell for cell in self.cells \
                      if not sj.objs.get_subjects().is_blocked(cell.subj)
                     ]
        sh.com.rep_matches(f, old_len-len(self.cells))
    
    def omit_users(self):
        f = '[MClientQt] cells.Omit.omit_users'
        if sh.lg.globs['bool']['ShowUserNames']:
            sh.com.rep_lazy(f)
            return
        count = 0
        for cell in self.cells:
            old_len = len(cell.blocks)
            i = 1
            while i < len(cell.blocks):
                if cell.blocks[i].type_ == 'user':
                    del cell.blocks[i]
                    i -= 1
                if cell.blocks[i-1].text.endswith(' ') \
                and cell.blocks[i].text == ')':
                    cell.blocks[i-1].text = cell.blocks[i-1].text.rstrip()
                i += 1
            delta = old_len - len(cell.blocks)
            if delta:
                fragms = [block.text for block in cell.blocks]
                cell.text = sh.List(fragms).space_items().strip()
            count += delta
        sh.com.rep_matches(f, count)
    
    def run(self):
        self.omit_subjects()
        self.omit_users()
        return self.cells



class Prioritize:
    
    def __init__(self, cells):
        self.speech = lg.Speech().get_settings()
        self.cells = cells
    
    def debug(self):
        f = '[MClientQt] cells.Prioritize.debug'
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
                  ,'SPEECHPR'
                  )
        iterable = [nos, text, subj, subjpr, speech, speechpr]
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 60
                           ).run()
        return f + ':\n' + mes
    
    def set_subjects(self):
        ''' All cells must have 'subjpr' set since they will not be further
            sorted by 'subj', so do not cancel this procedure even if there are
            no prioritized subjects, otherwise there may be sorting bugs, e.g.
            multitran.com, EN-RU, 'full of it'.
        '''
        for cell in self.cells:
            priority = sj.objs.get_subjects().get_priority(cell.subj)
            if priority is not None:
                cell.subjpr = priority
        pr_cells = [cell for cell in self.cells if cell.subjpr > -1]
        unp_cells = [cell for cell in self.cells if cell.subjpr == -1 \
                     and not com.is_phrase_type(cell)
                    ]
        ph_cells = [cell for cell in self.cells if cell.subjpr == -1 \
                    and com.is_phrase_type(cell)
                   ]
        
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
        for cell in ph_cells:
            if cell.subj == subj:
                cell.subjpr = subjpr
            else:
                subj = cell.subj
                subjpr += 1
                cell.subjpr = subjpr
        # [] + ['example'] == ['example']
        self.cells = pr_cells + unp_cells + ph_cells

    def set_speech(self):
        ph_cells = [cell for cell in self.cells if com.is_phrase_type(cell)]
        all_speech = sorted(set([cell.speech for cell in self.cells \
                                 if not cell in ph_cells
                                ]))
        speech_unp = [speech for speech in all_speech \
                      if not speech in self.speech
                     ]
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
        self.fixed_types = lg.com.get_col_types()
        self.fixed_urls = lg.objs.plugins.get_fixed_urls()

    def check(self):
        f = '[MClientQt] cells.View.check'
        if not self.cells:
            self.Success = False
            sh.com.rep_empty(f)
            return
    
    def sort(self):
        f = '[MClientQt] cells.View.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        if sh.lg.globs['bool']['AlphabetizeTerms'] \
        and not lg.com.is_parallel() and not lg.com.is_separate():
            self.cells.sort(key=lambda x: (x.col1, x.col2, x.col3, x.col4, x.text, x.no))
        else:
            self.cells.sort(key=lambda x: (x.col1, x.col2, x.col3, x.col4, x.no))
    
    def _create_fixed(self, i, type_, rowno):
        f = '[MClientQt] cells.View._create_fixed'
        cell = ic.Cell()
        block = ic.Block()
        block.type_ = type_
        cell.fixed_block = block
        cell.blocks = [block]
        cell.rowno = rowno
        if com.is_phrase_type(self.cells[i]):
            cell.subjpr = self.cells[i].subjpr
            cell.speechpr = self.cells[i].speechpr
            if type_ == 'subj':
                cell.text = block.text = self.cells[i].subj
            return cell
        cell.subj = self.cells[i].subj
        cell.subjpr = self.cells[i].subjpr
        cell.wform = self.cells[i].wform
        cell.transc = self.cells[i].transc
        cell.speech = self.cells[i].speech
        cell.speechpr = self.cells[i].speechpr
        if type_ == 'subj':
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
            mes = mes.format(type_, 'subj, wform, transc, speech, or empty')
            sh.objs.get_mes(f, mes).show_error()
        return cell
    
    def restore_fixed(self):
        f = '[MClientQt] cells.View.restore_fixed'
        if not self.Success:
            sh.com.cancel(f)
            return
        count = 0
        i = 1
        while i < len(self.cells):
            if self.cells[i-1].rowno != self.cells[i].rowno:
                rowno = self.cells[i].rowno
                for type_ in self.fixed_types:
                    count += 1
                    cell = self._create_fixed(i, type_, rowno)
                    self.cells.insert(i, cell)
                    i += 1
            i += 1
        sh.com.rep_matches(f, count)
    
    def restore_first(self):
        # Add fixed cells for the very first row
        f = '[MClientQt] cells.View.restore_first'
        if not self.Success:
            sh.com.cancel(f)
            return
        count = 0
        rowno = self.cells[0].rowno
        for type_ in self.fixed_types[::-1]:
            count += 1
            cell = self._create_fixed(0, type_, rowno)
            self.cells.insert(0, cell)
        sh.com.rep_matches(f, count)
    
    def _has_phrase(self):
        for cell in self.cells[::-1]:
            for block in cell.blocks:
                if block.type_ == 'phrase':
                    return True
    
    def restore_phsubj(self):
        f = '[MClientQt] cells.View.restore_phsubj'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self._has_phrase():
            sh.com.rep_lazy(f)
            return
        i = len(self.cells) - 1
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type_ == 'subj':
                self.cells[i].fixed_block.type_ = 'phsubj'
                self.phi = i
                mes = f'"{self.cells[i].fixed_block.text}"'
                sh.objs.get_mes(f, mes, True).show_debug()
                return
            i -= 1
    
    def debug(self):
        f = '[MClientQt] cells.View.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        headers = (_('ROW #'), _('CELL #'), _('TEXT'), _('TYPES'), 'URL'
                  ,'COL1' ,'COL2', 'COL3', 'COL4'
                  )
        rowno = []
        no = []
        text = []
        types = []
        url = []
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        for cell in self.cells:
            rowno.append(cell.rowno)
            no.append(cell.no)
            text.append(cell.text)
            url.append(cell.url)
            col1.append(cell.col1)
            col2.append(cell.col2)
            col3.append(cell.col3)
            col4.append(cell.col4)
            cell_types = []
            for block in cell.blocks:
                cell_types.append(block.type_)
            types.append(', '.join(cell_types))
        iterable = [rowno, no, text, types, url, col1, col2, col3, col4]
        return sh.FastTable (headers = headers
                            ,iterable = iterable
                            ,maxrow = 60
                            ).run()
    
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
        f = '[MClientQt] cells.View.renumber'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._renumber_cell_nos()
        self._renumber_row_nos()
    
    def clear_duplicates(self):
        f = '[MClientQt] cells.View.clear_duplicates'
        if not self.Success:
            sh.com.cancel(f)
            return
        subj = wform = transc = speech = ''
        for cell in self.cells:
            if not cell.fixed_block:
               continue
            if cell.fixed_block.type_ == 'subj':
                if cell.text == subj:
                    cell.text = cell.fixed_block.text = ''
                else:
                    subj = cell.subj
            elif cell.fixed_block.type_ == 'wform':
                if cell.text == wform:
                    cell.text = cell.fixed_block.text = ''
                else:
                    wform = cell.wform
            elif cell.fixed_block.type_ == 'transc':
                if cell.text == transc:
                    cell.text = cell.fixed_block.text = ''
                else:
                    transc = cell.transc
            elif cell.fixed_block.type_ == 'speech':
                if cell.text == speech:
                    cell.text = cell.fixed_block.text = ''
                else:
                    speech = cell.speech
    
    def get_fixed_url(self, type_, text):
        f = '[MClientQt] cells.View.get_fixed_url'
        try:
            return self.fixed_urls[type_][text]
        except KeyError:
            mes = _('"{}" has not been found in "{}"!')
            if not type_ in self.fixed_urls:
                mes = mes.format(type_, self.fixed_urls)
            elif not text in self.fixed_urls[type_]:
                mes = mes.format(text, self.fixed_urls[type_])
            sh.objs.get_mes(f, mes, True).show_warning()
        return ''
    
    def restore_urls(self):
        f = '[MClientQt] cells.View.restore_urls'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.fixed_urls:
            # Fixed cell URLs are relevant for multitrancom plugin only
            sh.com.rep_lazy(f)
            return
        for cell in self.cells:
            if not cell.fixed_block or not cell.text:
                continue
            if cell.fixed_block.type_ in ('subj', 'wform', 'phsubj'):
                cell.url = cell.fixed_block.url = self.get_fixed_url (cell.fixed_block.type_
                                                                     ,cell.text
                                                                     )
    
    def clear_phrase_fields(self):
        f = '[MClientQt] cells.View.clear_phrase_fields'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.phi is None:
            sh.com.rep_lazy()
            return
        i = self.phi
        while i < len(self.cells):
            cell = self.cells[i]
            if cell.fixed_block \
            and cell.fixed_block.type_ in ('wform', 'transc', 'speech'):
                cell.text = ''
            cell.wform = cell.speech = cell.transc = ''
            i += 1

    def fill_cols(self):
        f = '[MClientQt] cells.View.fill_cols'
        if not self.Success:
            sh.com.cancel(f)
            return
        types = lg.com.get_col_types()
        if not types:
            sh.com.rep_lazy(f)
            return
        for cell in self.cells:
            for i in range(len(types)):
                if i == 0:
                    if types[i] == 'subj':
                        cell.col1 = cell.subjpr
                    elif types[i] == 'wform':
                        cell.col1 = cell.wform.lower()
                    elif types[i] == 'speech':
                        cell.col1 = cell.speechpr
                    elif types[i] == 'transc':
                        cell.col1 = cell.transc.lower()
                elif i == 1:
                    if types[i] == 'subj':
                        cell.col2 = cell.subjpr
                    elif types[i] == 'wform':
                        cell.col2 = cell.wform.lower()
                    elif types[i] == 'speech':
                        cell.col2 = cell.speechpr
                    elif types[i] == 'transc':
                        cell.col2 = cell.transc.lower()
                elif i == 2:
                    if types[i] == 'subj':
                        cell.col3 = cell.subjpr
                    elif types[i] == 'wform':
                        cell.col3 = cell.wform.lower()
                    elif types[i] == 'speech':
                        cell.col3 = cell.speechpr
                    elif types[i] == 'transc':
                        cell.col3 = cell.transc.lower()
                elif i == 3:
                    if types[i] == 'subj':
                        cell.col4 = cell.subjpr
                    elif types[i] == 'wform':
                        cell.col4 = cell.wform.lower()
                    elif types[i] == 'speech':
                        cell.col4 = cell.speechpr
                    elif types[i] == 'transc':
                        cell.col4 = cell.transc.lower()
    
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
            a row should always be 4 (unless new fixed types are added).
        '''
        self.Success = True
        self.plain = []
        self.code = []
        self.cells = cells
        self.fixed_len = lg.objs.get_column_width().fixed_num
        self.collimit = lg.objs.column_width.fixed_num \
                      + lg.objs.column_width.term_num
        self.fixed_types = lg.com.get_col_types()
    
    def check(self):
        f = '[MClientQt] cells.Wrap.check'
        if not self.cells:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if self.collimit <= self.fixed_len:
            self.Success = False
            mes = f'{self.collimit} > {self.fixed_len}'
            sh.com.rep_condition(f, mes)
    
    def get_empty_cells(self, delta):
        row = []
        for type_ in range(delta):
            cell = ic.Cell()
            cell.blocks = [ic.Block()]
            row.append(cell)
        return row
    
    def wrap_x(self):
        f = '[MClientQt] cells.Wrap.wrap_x'
        if not self.Success:
            sh.com.cancel(f)
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
    
    def _wrap_y(self):
        cells = []
        row = []
        rowno = 0
        for cell in self.cells:
            if cell.rowno != rowno:
                row += self.get_empty_cells(self.collimit - len(row))
                cells.append(row)
                row = []
            row.append(cell)
            rowno = cell.rowno
        row += self.get_empty_cells(self.collimit - len(row))
        cells.append(row)
        self.cells = cells
    
    def get_max_row_len(self):
        f = '[MClientQt] cells.Wrap.get_max_row_len'
        if not self.Success:
            sh.com.cancel(f)
            return
        lens = [len(row) for row in self.cells]
        max_ = max(lens)
        sh.objs.get_mes(f, max_, True).show_debug()
        return max_
    
    def _get_prev_cell(self, i, j):
        if i >= len(self.cells):
            return
        while j >= 0:
            try:
                return self.cells[i][j]
            except IndexError:
                pass
            j -= 1
    
    def _force_cell(self, i, j):
        #FIX: this is inefficient for long articles. Create a copy of elems.
        f = '[MClientQt] cells.Wrap._force_cell'
        try:
            return self.cells[i][j]
        except IndexError:
            cell = self._get_prev_cell(i, j)
            if cell is None:
                mes = _('Create new cell ({}, {})').format(i, j)
                sh.objs.get_mes(f, mes, True).show_debug()
                cell = ic.Cell()
            else:
                cell = copy.deepcopy(cell)
            cell.rowno = i
            cell.colno = i
            cell.text = ''
            cell.code = ''
            cell.blocks = []
            cell.fixed_block = None
            return cell
    
    def wrap_y(self):
        f = '[MClientQt] cells.Wrap.wrap_y'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._wrap_y()
        if not self.cells:
            sh.com.rep_empty(f)
            return
        max_ = self.get_max_row_len()
        if not max_:
            sh.com.rep_empty(f)
            return
        cells = []
        for j in range(max_):
            row = []
            for i in range(len(self.cells)):
                row.append(self._force_cell(i, j))
            cells.append(row)
        self.cells = cells
    
    def wrap(self):
        if sh.lg.globs['bool']['VerticalView']:
            self.wrap_y()
        else:
            self.wrap_x()
    
    def _debug_cells(self):
        f = '[MClientQt] cells.Wrap._debug_cells'
        mes = [f'{f}:']
        headers = (_('CELL #'), _('ROW #'), _('COLUMN #'), _('TEXT'), _('CODE')
                  ,'URL'
                  )
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
        iterable = [no, rowno,  colno, text, code, url]
        return sh.FastTable (headers = headers
                            ,iterable = iterable
                            ,maxrow = 60
                            ,maxrows = 700
                            ).run()
        return '\n'.join(mes)
    
    def _debug_plain(self):
        f = '[MClientQt] cells.Wrap._debug_plain'
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
        f = '[MClientQt] cells.Wrap._debug_code'
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
        f = '[MClientQt] cells.Wrap.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = [self._debug_cells()]
        mes.append(self._debug_plain())
        mes.append(self._debug_code())
        return '\n\n'.join(mes)
    
    def renumber(self):
        f = '[MClientQt] cells.Wrap.renumber'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.cells[0]:
            self.Success = False
            sh.com.rep_empty(f)
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
        f = '[MClientQt] cells.Wrap.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        for row in self.cells:
            for cell in row:
                cell_code = []
                if sh.lg.globs['bool']['VerticalView']:
                    no = cell.rowno
                else:
                    no = cell.colno
                for block in cell.blocks:
                    cell_code.append(fm.Block(block, no).run())
                cell.code = sh.List(cell_code).space_items()
    
    def set_plain(self):
        f = '[MClientQt] cells.Wrap.set_plain'
        if not self.Success:
            sh.com.cancel(f)
            return
        for row in self.cells:
            new_row = []
            for cell in row:
                new_row.append(cell.text)
            self.plain.append(new_row)
    
    def set_code(self):
        f = '[MClientQt] cells.Wrap.set_code'
        if not self.Success:
            sh.com.cancel(f)
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



class Commands:
    
    def is_phrase_type(self, cell):
        for block in cell.blocks:
            if block.type_ in ('phsubj', 'phrase', 'phcount'):
                return True


com = Commands()
