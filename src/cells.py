#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
import instance as ic

#import subjects.subjects as sj


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



class Format:
    
    def __init__(self,cells):
        self.Success = True
        self.cells = cells

    def check(self):
        f = '[MClientQt] cells.Format.check'
        if not self.cells:
            self.Success = False
            sh.com.rep_empty(f)

    def format(self):
        f = '[MClientQt] cells.Format.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        for cell in self.cells:
            cell_code = []
            for block in cell.blocks:
                block = lg.Font(block).run()
                block.code = lg.Format(block).run()
                cell_code.append(block.code)
            cell.code = ''.join(cell_code)

    def run(self):
        self.check()
        self.format()
        return self.cells



class Prioritize:
    
    def __init__(self,cells,subjects=[],speech=[]):
        self.all_subj = []
        self.subj_pri = subjects
        self.speech_pri = speech
        self.cells = cells
    
    def set_subjects(self):
        self.all_subj = sorted(set([cell.subj for cell in self.cells]))
        subj_unp = [subj for subj in self.all_subj \
                    if not subj in self.subj_pri
                   ]
        self.all_subj = self.subj_pri + subj_unp
        for i in range(len(self.all_subj)):
            for cell in self.cells:
                if cell.subj == self.all_subj[i]:
                    cell.subjpr = i
    
    def set_speech(self):
        all_speech = sorted(set([cell.speech for cell in self.cells]))
        speech_unp = [speech for speech in all_speech \
                      if not speech in self.speech_pri
                     ]
        all_speech = self.speech_pri + speech_unp
        for i in range(len(all_speech)):
            for cell in self.cells:
                if cell.speech == all_speech[i]:
                    cell.speechpr = i
    
    def _is_phrase_type(self,cell):
        for block in cell.blocks:
            if block.type_ in ('phsubj','phrase','phcount'):
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
        cells = Format(cells).run()
        cells = View(cells).run()
        return cells



class View:
    # Create user-specific cells
    def __init__(self, cells, fixed_types=('subj', 'wform', 'transc', 'speech')):
        self.Success = True
        self.max_len = 11
        self.view = []
        self.cells = cells
        self.fixed_types = fixed_types

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
    
    def restore_urls(self):
        f = '[MClientQt] cells.View.restore_urls'
        if not self.Success:
            sh.com.cancel(f)
            return
        urls = lg.objs.get_articles().get_fixed_urls()
        if not urls:
            sh.com.rep_empty(f)
            return
        for cell in self.cells:
            if not cell.fixed_block or not cell.text:
                continue
            if cell.fixed_block.type_ in ('subj', 'wform'):
                cell.url = cell.fixed_block.url = lg.objs.articles.get_fixed_url (cell.fixed_block.type_
                                                                                 ,cell.text
                                                                                 )
    
    def run(self):
        self.check()
        self.sort()
        self.restore_fixed()
        self.restore_first()
        self.clear_duplicates()
        self.restore_urls()
        self.renumber()
        return self.cells



class Wrap:
    
    def __init__(self,view,collimit=9):
        ''' Since we create even empty columns, the number of fixed cells in
            a row should always be 4 (unless new fixed types are added).
        '''
        self.fixed_len = 4
        #NOTE: Synchronize with View
        self.max_len = 11
        self.Success = True
        self.plain = []
        self.code = []
        self.view = view
        self.collimit = collimit
    
    def check(self):
        f = '[MClientQt] cells.Wrap.check'
        if not self.view:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.view[0]) != self.max_len:
            self.Success = False
            mes = f'{len(self.view[0])} = {self.max_len}'
            sh.com.rep_condition(f,mes)
        if self.collimit <= self.fixed_len:
            self.Success = False
            mes = f'{self.collimit} > {self.fixed_len}'
            sh.com.rep_condition(f,mes)
    
    def wrap_x(self):
        f = '[MClientQt] cells.Wrap.wrap_x'
        if not self.Success:
            sh.com.cancel(f)
            return
        row = []
        rowc = []
        rowno = 0
        for cell in self.view:
            if len(row) == self.collimit:
                self.plain.append(row)
                self.code.append(rowc)
                if cell[0] == rowno:
                    row = [''] * self.fixed_len
                    rowc = [''] * self.fixed_len
                else:
                    row = []
                    rowc = []
            elif cell[0] != rowno:
                delta = self.collimit - len(row)
                row += [''] * delta
                rowc += [''] * delta
                self.plain.append(row)
                self.code.append(rowc)
                row = []
                rowc = []
            row.append(cell[2])
            rowc.append(cell[3])
            rowno = cell[0]
        delta = self.collimit - len(row)
        row += [''] * delta
        rowc += [''] * delta
        self.plain.append(row)
        self.code.append(rowc)
    
    def _debug_plain(self):
        debug = []
        for row in self.plain:
            new_row = []
            for i in range(len(row)):
                item = f'{i+1}: {row[i]}'
                new_row.append(item)
            debug.append(new_row)
        return str(debug)
    
    def _debug_code(self):
        debug = []
        for row in self.code:
            new_row = []
            for i in range(len(row)):
                item = f'{i+1}: {row[i]}'
                new_row.append(item)
            debug.append(new_row)
        return str(debug)
    
    def debug(self):
        f = '[MClientQt] cells.Wrap.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = []
        mes.append(_('Cell text:'))
        mes.append(str(self._debug_plain()))
        mes.append('')
        '''
        mes.append(_('Cell code:'))
        mes.append(str(self._debug_code()))
        '''
        return '\n'.join(mes)
    
    def run(self):
        self.check()
        self.wrap_x()
        return self.plain


com = Commands()


if __name__ == '__main__':
    sh.com.start()
    com.order([])
    sh.com.end()
