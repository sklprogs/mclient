#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic
import format as fm
import logic as lg


class Expand:
    
    def __init__(self, cells, Speech=False):
        ''' Run this class before blocking and prioritization since short and
            full values can be sorted differently (especially this concerns
            subjects, in which first letters of shortened and full texts may
            differ).
        '''
        self.cells = cells
        self.Speech = Speech
    
    def expand_speech(self):
        f = '[MClientQt] cells.Expand.expand_speech'
        if not self.Speech:
            sh.com.rep_lazy(f)
            return
        ''' Runs just after 'elems'. Fixed types are not restored yet at this
            point.
        '''
        for cell in self.cells:
            cell.speech = lg.objs.get_plugins().expand_speech(cell.speech)
    
    def run(self):
        self.expand_speech()
        return self.cells



class Omit:
    
    def __init__(self,cells,subjects=[],OmitUsers=False):
        self.cells = cells
        self.subjects = subjects
        self.OmitUsers = OmitUsers
    
    def _is_blocked(self,text):
        if text in self.subjects:
            return True
        parts = text.split(', ')
        for part in parts:
            if part in self.subjects:
                return True
    
    def omit_subjects(self):
        f = '[MClientQt] cells.Omit.omit_subjects'
        old_len = len(self.cells)
        self.cells = [cell for cell in self.cells \
                      if not self._is_blocked(cell.subj)
                     ]
        sh.com.rep_matches(f,old_len-len(self.cells))
    
    def omit_users(self):
        f = '[MClientQt] cells.Omit.omit_users'
        if not self.OmitUsers:
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
        sh.com.rep_matches(f,count)
    
    def run(self):
        self.omit_subjects()
        self.omit_users()
        return self.cells


class Prioritize:
    
    def __init__(self,cells,subjects=[],speech=[]):
        self.all_subj = []
        self.subjects = subjects
        self.speech = speech
        self.cells = cells
    
    def set_subjects(self):
        self.all_subj = sorted(set([cell.subj for cell in self.cells]))
        subj_unp = [subj for subj in self.all_subj if not subj in self.subjects]
        self.all_subj = self.subjects + subj_unp
        for i in range(len(self.all_subj)):
            for cell in self.cells:
                if cell.subj == self.all_subj[i]:
                    cell.subjpr = i
    
    def set_speech(self):
        all_speech = sorted(set([cell.speech for cell in self.cells]))
        speech_unp = [speech for speech in all_speech \
                      if not speech in self.speech
                     ]
        all_speech = self.speech + speech_unp
        for i in range(len(all_speech)):
            for cell in self.cells:
                if cell.speech == all_speech[i]:
                    cell.speechpr = i
    
    def _is_phrase_type(self,cell):
        for block in cell.blocks:
            if block.type_ in ('phsubj', 'phrase', 'phcount'):
                return True
    
    def set_phrases(self):
        subjpr = len(self.all_subj)
        for cell in self.cells:
            if self._is_phrase_type(cell):
                cell.subjpr = subjpr
    
    def run(self):
        self.set_subjects()
        self.set_speech()
        self.set_phrases()
        return self.cells


class Commands:
    
    def order(self, cells):
        cells = Omit(cells).run()
        cells = Prioritize(cells).run()
        cells = View(cells).run()
        return cells


class View:
    # Create user-specific cells
    def __init__(self, cells, fixed_types=('subj', 'wform', 'transc', 'speech'), fixed_urls={}):
        self.Success = True
        self.phi = None
        self.view = []
        self.cells = cells
        self.fixed_types = fixed_types
        self.fixed_urls = fixed_urls

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
        #TODO: Elaborate
        self.cells.sort(key=lambda x: (x.subjpr, x.wform, x.transc, x.speechpr, x.text))
    
    def _create_fixed(self, i, type_, rowno):
        f = '[MClientQt] cells.View._create_fixed'
        cell = ic.Cell()
        block = ic.Block()
        block.type_ = type_
        cell.fixed_block = block
        cell.blocks = [block]
        cell.rowno = rowno
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
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(type_,'subj, wform, trasc, speech')
            sh.objs.get_mes(f,mes).show_warning()
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
                    self.cells.insert(i,cell)
                    i += 1
            i += 1
        sh.com.rep_matches(f,count)
    
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
            self.cells.insert(0,cell)
        sh.com.rep_matches(f,count)
    
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
                return
            i -= 1
    
    def debug(self):
        f = '[MClientQt] cells.View.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        headers = (_('ROW #'),_('CELL #'),_('TEXT'),_('CODE'),'URL','SUBJ'
                  ,'SUBJPR','WFORM','TRANSC','SPEECH','SPEECHPR'
                  )
        rowno = []
        no = []
        text = []
        code = []
        url = []
        subj = []
        subjpr = []
        wform = []
        transc = []
        speech = []
        speechpr = []
        for cell in self.cells:
            rowno.append(cell.rowno)
            no.append(cell.no)
            text.append(cell.text)
            code.append(cell.code)
            url.append(cell.url)
            subj.append(cell.subj)
            subjpr.append(cell.subjpr)
            wform.append(cell.wform)
            transc.append(cell.transc)
            speech.append(cell.speech)
            speechpr.append(cell.speechpr)
        iterable = [rowno, no, text, code, url, subj, subjpr, wform, transc
                   ,speech, speechpr
                   ]
        return sh.FastTable (headers = headers
                            ,iterable = iterable
                            ,maxrow = 30
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
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()
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

    def run(self):
        self.check()
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
    
    def __init__(self, cells, collimit=9, fixed_types=('subj', 'wform', 'transc', 'speech')):
        ''' Since we create even empty columns, the number of fixed cells in
            a row should always be 4 (unless new fixed types are added).
        '''
        self.fixed_len = 4
        self.Success = True
        self.plain = []
        self.code = []
        self.cells = cells
        self.collimit = collimit
    
    def check(self):
        f = '[MClientQt] cells.Wrap.check'
        if not self.cells:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if self.collimit <= self.fixed_len:
            self.Success = False
            mes = f'{self.collimit} > {self.fixed_len}'
            sh.com.rep_condition(f,mes)
    
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
                for block in cell.blocks:
                    cell_code.append(fm.Block(block, cell.colno).run())
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
        self.wrap_x()
        self.renumber()
        self.format()
        self.set_plain()
        self.set_code()
        return self.cells


com = Commands()


if __name__ == '__main__':
    sh.com.start()
    com.order([])
    sh.com.end()
