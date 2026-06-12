#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.list import List
from skl_shared.table import Table

from config import CONFIG
from manager import SOURCES
from format import Block as fmBlock
from subjects import SUBJECTS
from articles import ARTICLES
from columns import COL_WIDTH
from speech import SPEECH


class OrderSources:
    
    def __init__(self):
        self.ordered = []
        self.prior = []
    
    def reset(self, sources):
        self.sources = sources
        self.set_prior()
        self.order()
    
    def set_prior(self):
        f = '[MClient] view.OrderSources.set_prior'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.prior = CONFIG.new['sources']['prioritized'].keys()
        mes = ', '.join(self.prior)
        Message(f, mes).show_debug()
    
    def order(self):
        f = '[MClient] view.OrderSources.order'
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
        f = '[MClient] view.OrderSources.get_priority'
        if not CONFIG.Success:
            rep.cancel(f)
            return -1
        try:
            return self.ordered.index(source)
        except ValueError:
            # This can happen if the source is blocked
            return -1



class Phrases:
    
    def __init__(self, blocks):
        self.sourcepr = -1
        self.dic = ''
        self.subjpr = -1
        self.wform = ''
        self.speechpr = -1
        self.transc = ''
        self.cellno = -1
        self.phname = _('Phrases')
        self.blocks = blocks
        
    def ignore_phcount(self):
        f = '[MClient] view.Phrases.ignore_phcount'
        if CONFIG.new['PhraseCount']:
            rep.lazy(f)
            return
        count = 0
        for block in self.blocks:
            if block.type == 'phcount':
                count += 1
                block.Ignore = True
        rep.matches(f, count)
    
    def set_sourcepr(self):
        f = '[MClient] view.Phrases.set_sourcepr'
        sourcepr = [block.sourcepr for block in self.blocks]
        if not sourcepr:
            rep.lazy(f)
            return
        self.sourcepr = max(sourcepr) + 1
        mes = f'"{self.sourcepr}"'
        Message(f, mes).show_debug()
    
    def set_subjpr(self):
        f = '[MClient] view.Phrases.set_subjpr'
        subjpr = [block.subjpr for block in self.blocks]
        if not subjpr:
            rep.lazy(f)
            return
        self.subjpr = max(subjpr) + 1
        mes = f'"{self.subjpr}"'
        Message(f, mes).show_debug()
    
    def set_dic(self):
        f = '[MClient] view.Phrases.set_dic'
        for block in self.blocks[::-1]:
            if block.dic and not block.type in ('phsubj', 'phrase', 'phcount'
                                               ,'comment'):
                self.dic = block.dic
                mes = f'"{self.dic}"'
                Message(f, mes).show_debug()
                return
    
    def set_wform(self):
        f = '[MClient] view.Phrases.set_wform'
        for block in self.blocks[::-1]:
            if block.wform and not block.type in ('phsubj', 'phrase', 'phcount'
                                                 ,'comment'):
                self.wform = block.wform
                mes = f'"{self.wform}"'
                Message(f, mes).show_debug()
                return
    
    def set_speechpr(self):
        f = '[MClient] view.Phrases.set_speechpr'
        speechpr = [block.speechpr for block in self.blocks]
        if not speechpr:
            rep.lazy(f)
            return
        self.speechpr = max(speechpr) + 1
        mes = f'"{self.speechpr}"'
        Message(f, mes).show_debug()
    
    def set_transc(self):
        f = '[MClient] view.Phrases.set_transc'
        for block in self.blocks[::-1]:
            if block.transc and not block.type in ('phsubj', 'phrase', 'phcount'
                                                  ,'comment'):
                self.transc = block.transc
                mes = f'"{self.transc}"'
                Message(f, mes).show_debug()
                return
    
    def set_cellno(self):
        f = '[MClient] view.Phrases.set_cellno'
        cellnos = [block.cellno for block in self.blocks]
        if not cellnos:
            rep.lazy(f)
            return
        self.cellno = max(cellnos) + 1
        mes = f'"{self.cellno}"'
        Message(f, mes).show_debug()
    
    def reassign(self):
        ''' - phsubj is set to an incorrect row without this.
            - Phrases may have synonyms attached to them and formatted as
              comments, so moving by cellno is more precise.
        '''
        f = '[MClient] view.Phrases.reassign'
        cellnos = [block.cellno for block in self.blocks \
                  if block.type == 'phrase']
        if not cellnos:
            rep.lazy(f)
            return
        phrases = [block for block in self.blocks if block.cellno in cellnos]
        for block in phrases:
            block.cellno = self.cellno
            block.sourcepr = self.sourcepr
            block.dic = self.dic
            block.subjpr = self.subjpr
            block.wform = self.wform
            block.speechpr = self.speechpr
            block.transc = self.transc
            block.cellno = self.cellno
            block.subj = block.subjf = self.phname
            
    def run(self):
        # At this point, blocks may have identical cellno
        self.set_sourcepr()
        self.set_dic()
        self.set_subjpr()
        self.set_wform()
        self.set_speechpr()
        self.set_transc()
        self.set_cellno()
        self.ignore_phcount()
        self.reassign()
        return self.blocks



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
            cell.blocks = [block for block in cell.blocks \
                          if block.type != 'user']
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
    
    def __init__(self, blocks):
        self.speech = SPEECH.get_settings()
        self.blocks = blocks
    
    def debug(self, maxrow=50):
        f = '[MClient] view.Prioritize.debug'
        subj = []
        subjf = []
        subjpr = []
        text = []
        types = []
        sources = []
        sourcepr = []
        nos = []
        speech = []
        speechpr = []
        for block in self.blocks:
            nos.append(block.no)
            text.append(block.text)
            types.append(block.type)
            sources.append(block.source)
            sourcepr.append(block.sourcepr)
            subj.append(block.subj)
            subjf.append(block.subjf)
            subjpr.append(block.subjpr)
            speech.append(block.speech)
            speechpr.append(block.speechpr)
        headers = (_('#'), _('TEXT'), _('TYPE'), 'SOURCE', 'SOURCEPR', 'SUBJ'
                  ,'SUBJF', 'SUBJPR', 'SPEECH', 'SPEECHPR')
        iterable = [nos, text, types, sources, sourcepr, subj, subjf, subjpr, speech
                   ,speechpr]
        mes = Table(headers = headers
                   ,iterable = iterable
                   ,maxrow = maxrow).run()
        return f + ':\n' + mes
    
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
        return Phrases(self.blocks).run()



class View:
    # Create user-specific cells
    def __init__(self, cells):
        self.Success = True
        self.view = []
        self.cells = cells
        # Must be recreated for each article loading/reloading
        self.fixed_cols = COL_WIDTH.get_fixed_types()
    
    def check(self):
        f = '[MClient] view.View.check'
        if not self.cells:
            self.Success = False
            rep.empty(f)
    
    def sort(self):
        f = '[MClient] view.View.sort'
        if not self.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['OrderCells']:
            rep.empty(f)
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
    
    def debug(self, maxrow=35):
        f = '[MClient] view.View.debug'
        if not self.Success:
            rep.cancel(f)
            return
        headers = (_('ROW #'), _('CELL #'), _('TEXT'), _('TYPES'), 'URL', 'COL1'
                  ,'COL2', 'COL3', 'COL4', 'COL5', 'COL6')
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
        iterable = [rowno, no, text, types, url, col1, col2, col3, col4, col5
                   ,col6]
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
                    source = cell.source
            elif cell.fixed_block.type == 'dic':
                if cell.text == dic:
                    cell.text = cell.fixed_block.text = ''
                else:
                    dic = cell.dic
            elif cell.fixed_block.type == 'subj':
                if cell.text == subj or (not subj and not cell.subj):
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
    
    def fill_cols(self):
        f = '[MClient] view.View.fill_cols'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.fixed_cols:
            rep.lazy(f)
            return
        ''' Word forms must be case-sensitive; otherwise, they can be ordered
            like AST - ast - AST, etc.
        '''
        for cell in self.cells:
            for i in range(len(self.fixed_cols)):
                match i:
                    case 0:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col1 = cell.sourcepr
                            case 'dic':
                                cell.col1 = cell.dic.lower()
                            case 'subj':
                                cell.col1 = cell.subjpr
                            case 'wform':
                                cell.col1 = cell.wform
                            case 'speech':
                                cell.col1 = cell.speechpr
                            case 'transc':
                                cell.col1 = cell.transc
                    case 1:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col2 = cell.sourcepr
                            case 'dic':
                                cell.col2 = cell.dic.lower()
                            case 'subj':
                                cell.col2 = cell.subjpr
                            case 'wform':
                                cell.col2 = cell.wform
                            case 'speech':
                                cell.col2 = cell.speechpr
                            case 'transc':
                                cell.col2 = cell.transc
                    case 2:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col3 = cell.sourcepr
                            case 'dic':
                                cell.col3 = cell.dic.lower()
                            case 'subj':
                                cell.col3 = cell.subjpr
                            case 'wform':
                                cell.col3 = cell.wform
                            case 'speech':
                                cell.col3 = cell.speechpr
                            case 'transc':
                                cell.col3 = cell.transc
                    case 3:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col4 = cell.sourcepr
                            case 'dic':
                                cell.col4 = cell.dic.lower()
                            case 'subj':
                                cell.col4 = cell.subjpr
                            case 'wform':
                                cell.col4 = cell.wform
                            case 'speech':
                                cell.col4 = cell.speechpr
                            case 'transc':
                                cell.col4 = cell.transc
                    case 4:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col5 = cell.sourcepr
                            case 'dic':
                                cell.col5 = cell.dic.lower()
                            case 'subj':
                                cell.col5 = cell.subjpr
                            case 'wform':
                                cell.col5 = cell.wform
                            case 'speech':
                                cell.col5 = cell.speechpr
                            case 'transc':
                                cell.col5 = cell.transc
                    case 5:
                        match self.fixed_cols[i]:
                            case 'source':
                                cell.col6 = cell.sourcepr
                            case 'dic':
                                cell.col6 = cell.dic.lower()
                            case 'subj':
                                cell.col6 = cell.subjpr
                            case 'wform':
                                cell.col6 = cell.wform
                            case 'speech':
                                cell.col6 = cell.speechpr
                            case 'transc':
                                cell.col6 = cell.transc
    
    def _get_last_subj(self):
        for cell in self.cells[::-1]:
            for block in cell.blocks:
                if block.type == 'subj' and block.text == _('Phrases'):
                    return cell
    
    def restore_url(self):
        f = '[MClient] view.View.restore_url'
        if not self.Success:
            rep.cancel(f)
            return
        last_subj = self._get_last_subj()
        if not last_subj:
            rep.lazy(f)
            return
        last_subj.url = last_subj.fixed_block.url = ARTICLES.get_phurl()
    
    def clear_single_source(self):
        f = '[MClient] view.View.clear_single_source'
        if not self.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['ClearSingleSource']:
            rep.lazy(f)
            return
        sources = set([cell.source for cell in self.cells if cell.source])
        if len(sources) == 1:
            for cell in self.cells:
                cell.source = ''
    
    def run(self):
        self.check()
        self.fill_cols()
        self.sort()
        self.clear_single_source()
        self.restore_fixed()
        self.restore_first()
        self.clear_duplicates()
        self.restore_url()
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


ORDER_SOURCES = OrderSources()