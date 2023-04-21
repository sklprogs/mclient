#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import operator

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg

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
    
    def set_view(self,cells):
        f = '[MClientQt] cells.Commands.set_view'
        if not cells:
            sh.com.rep_empty(f)
            return
        view = []
        for cell in cells:
            row = [cell.rowno,cell.no,cell.text,cell.code,cell.url,cell.subj
                  ,cell.subjpr,cell.wform,cell.transc,cell.speech,cell.speechpr
                  ]
            view.append(row)
        return view
    
    def order(self,cells):
        cells = Omit(cells).run()
        cells = Prioritize(cells).run()
        cells = Format(cells).run()
        view = View(self.set_view(cells)).run()
        return view



class View:
    # Create user-specific data set
    def __init__(self,view,fixed_types=('subj','wform','transc','speech')):
        ''' 0: rowno, 1: cellno, 2: text, 3: code, 4: url, 5: subj,
            6: subj_prior, 7: wform, 8: transc, 9: speech, 10: speech_prior.
        '''
        self.Success = True
        self.max_len = 11
        self.view = view
        self.fixed_types = fixed_types

    def check(self):
        f = '[MClientQt] cells.View.check'
        if not self.view:
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.view[0]) != self.max_len:
            self.Success = False
            mes = f'{len(self.view[0])} = {self.max_len}'
            sh.com.rep_condition(f,mes)
    
    def sort(self):
        f = '[MClientQt] cells.View.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.view.sort(key=operator.itemgetter(6,5,7,8,10,9,2,1))
    
    def _get_fixed_type_no(self,type_):
        f = '[MClientQt] cells.View._get_fixed_type_no'
        if type_ in ('subj','phsubj'):
            return 5
        elif type_ == 'wform':
            return 7
        elif type_ == 'transc':
            return 8
        elif type_ == 'speech':
            return 9
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format (type_,'; '.join (['subj','phsubj','wform'
                                               ,'speech','transc'
                                               ]
                                              )
                             )
            sh.objs.get_mes(f,mes,True).show_warning()
    
    def _get_fixed_col_no(self,type_):
        f = '[MClientQt] cells.View._get_fixed_col_no'
        try:
            return self.fixed_types.index(type_)
        except ValueError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()
    
    def _get_color(self,colno):
        #TODO: Elaborate
        if colno == 0:
            return sh.lg.globs['str']['color_col1']
        elif colno == 1:
            return sh.lg.globs['str']['color_col2']
        elif colno == 2:
            return sh.lg.globs['str']['color_col3']
        elif colno == 3:
            return sh.lg.globs['str']['color_col4']
        return 'black'
    
    def _format_fixed(self,text,type_):
        #TODO: Do we need to support multi-format fixed cells?
        #TODO: Elaborate
        family = 'Sans'
        size = 11
        colno = self._get_fixed_col_no(type_)
        color = self._get_color(colno)
        code = '''<span style="font-family:{}; font-size:{}pt; color:'{}';">{}</span>'''
        code = code.format(family,size,color,text)
        return code
    
    def _create_fixed_first(self,no,type_):
        new_row = list(self.view[0])
        new_row[1] = 0
        new_row[2] = self.view[0][no]
        new_row[3] = self._format_fixed(new_row[2],type_)
        return new_row
    
    def _create_fixed(self,i,no,cellno,type_):
        new_row = list(self.view[i])
        new_row[1] = cellno
        if self.view[i-1][no] == self.view[i][no]:
            new_row[2] = ''
        else:
            new_row[2] = self.view[i][no]
        new_row[3] = self._format_fixed(new_row[2],type_)
        return new_row
    
    def _is_new_row(self,i):
        # 'i > 0' condition is observed in 'restore_fixed'
        return self.view[i-1][0] != self.view[i][0]
    
    def _restore_fixed(self):
        f = '[MClientQt] cells.View._restore_fixed'
        count = 0
        i = 1
        while i < len(self.view):
            if self._is_new_row(i):
                add = []
                cellno = self.view[i][1] - 0.5
                for type_ in self.fixed_types:
                    no = self._get_fixed_type_no(type_)
                    if no is None:
                        sh.com.rep_empty(f)
                        return
                    cellno += 0.1
                    add.append(self._create_fixed(i,no,cellno,type_))
                    count += 1
                for row in add:
                    self.view.insert(i,row)
                    i += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def _restore_fixed_first(self):
        f = '[MClientQt] cells.View._restore_fixed_first'
        # Add fixed cells for the very first row
        if not self.view:
            sh.com.rep_empty(f)
            return
        count = 0
        add = []
        i = 0
        cellno = 0
        for type_ in self.fixed_types:
            no = self._get_fixed_type_no(type_)
            if no is None:
                sh.com.rep_empty(f)
                return
            cellno += 0.1
            add.append(self._create_fixed_first(no,type_))
            count += 1
        for row in add:
            self.view.insert(i,row)
            i += 1
        sh.com.rep_matches(f,count)
    
    def restore_fixed(self):
        f = '[MClientQt] cells.View.restore_fixed'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._restore_fixed()
        self._restore_fixed_first()
    
    def debug(self):
        f = '[MClientQt] cells.View.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        headers = (_('ROW #'),_('CELL #'),_('TEXT'),_('CODE'),'URL','SUBJ'
                  ,'SUBJPR','WFORM','TRANSC','SPEECH','SPEECHPR'
                  )
        return sh.FastTable (headers = headers
                            ,iterable = self.view
                            ,Transpose = True
                            ,maxrow = 30
                            ).run()
    
    def _renumber_cell_nos(self):
        for i in range(len(self.view)):
            self.view[i][1] = i
    
    def _renumber_row_nos(self):
        # Actually, we do this for prettier debug output
        rownos = [0]
        rowno = 0
        i = 1
        while i < len(self.view):
            if self.view[i-1][0] != self.view[i][0]:
                rowno += 1
            rownos.append(rowno)
            i += 1
        i = 0
        while i < len(self.view):
            self.view[i][0] = rownos[i]
            i += 1
    
    def renumber(self):
        f = '[MClientQt] cells.View.renumber'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._renumber_cell_nos()
        self._renumber_row_nos()
    
    def run(self):
        self.check()
        self.sort()
        self.restore_fixed()
        self.renumber()
        return self.view



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
            row.append(cell[2])
            rowc.append(cell[3])
            cond = len(row) == self.collimit
            if cell[0] != rowno or cond:
                delta = self.collimit - len(row)
                row += [''] * delta
                rowc += [''] * delta
                self.plain.append(row)
                self.code.append(rowc)
                if cond:
                    row = [''] * self.fixed_len + [cell[2]]
                    rowc = [''] * self.fixed_len + [cell[3]]
                else:
                    row = [cell[2]]
                    rowc = [cell[3]]
                rowno = cell[0]
        if row:
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
        self.wrap_x()
        return self.plain


com = Commands()


if __name__ == '__main__':
    sh.com.start()
    com.order([])
    sh.com.end()
