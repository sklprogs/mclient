#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic


class Elems:

    def __init__(self, blocks, abbr, langs=[], search=''):
        f = '[MClient] plugins.multitrandem.elems.Elems.__init__'
        self.cells = []
        self.art_subj = {}
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
        self.abbr = abbr
        self.langs = langs
        self.pattern = search.strip()
        if blocks:
            self.Success = True
            self.blocks = blocks
        else:
            self.Success = False
            sh.com.rep_empty(f)
            self.blocks = []
    
    def _get_pair(self, text):
        f = '[MClient] plugins.multitrandem.elems.Elems._get_pair'
        code = sh.Input(f, text).get_integer()
        return self.abbr.get_pair(code)
    
    def _check_dic_codes(self, text):
        # Emptyness check is performed before that
        if text[0] == ' ' or text[-1] == ' ' or '  ' in text:
            return
        if set(text) == {' '}:
            return
        pattern = sh.lg.digits + ' '
        for sym in text:
            if not sym in pattern:
                return
        return True
    
    def set_dic_titles(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.set_dic_titles'
        if not self.abbr:
            sh.com.rep_empty(f)
            return
        if not self.abbr.Success:
            sh.com.cancel(f)
            return
        for block in self.blocks:
            if block.type != 'subj' or not block.text:
                continue
            if not self._check_dic_codes(block.text):
                mes = _('Wrong input data: "{}"!').format(block.text)
                sh.objs.get_mes(f, mes, True).show_warning()
                continue
            abbr = []
            full = []
            dics = block.text.split(' ')
            for dic in dics:
                pair = self._get_pair(dic)
                if pair:
                    abbr.append(pair[0])
                    full.append(pair[1])
                else:
                    sh.com.rep_empty(f)
            abbr = '; '.join(abbr)
            full = '; '.join(full)
            block.text = abbr
            block.subj = abbr
            block.subjf = full
    
    def strip(self):
        for block in self.blocks:
            block.text = block.text.strip()
    
    def set_cells(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.set_cells'
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            sh.com.rep_condition(f, mes)
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
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClient] plugins.multitrandem.elems.Elems.unite_brackets'
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
        sh.com.rep_matches(f, count)
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = sh.List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = sh.Text(cell.text).delete_duplicate_spaces()
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClient] plugins.multitrandem.elems.Elems.set_row_nos'
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
        sh.com.rep_matches(f, count)
    
    def set_art_subj(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
                self.art_subj[block.subjf] = block.subj
        sh.com.rep_matches(f, count)
    
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
    
    def delete_fixed(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        sh.com.rep_matches(f, count)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def run(self):
        f = '[MClient] plugins.multitrandem.elems.Elems.run'
        if not self.Success:
            sh.com.cancel(f)
            return self.blocks
        # Do some cleanup
        self.strip()
        # Prepare contents
        self.set_dic_titles()
        self.add_brackets()
        # Prepare for cells
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        # Extra spaces in the beginning may cause sorting problems
        self.add_space()
        #TODO: expand parts of speech (n -> noun, etc.)
        self.set_cells()
        self.unite_brackets()
        self.set_text()
        #self.set_fixed_cells()
        #self.rename_phsubj()
        self.set_row_nos()
        #self.save_urls()
        self.set_art_subj()
        self.fill_fixed()
        self.delete_fixed()
        self.renumber()
        return self.cells
    
    def _debug_blocks(self, maxrow=20, maxrows=0):
        f = 'plugins.multitrandem.elems.Elems._debug_blocks'
        headers = ('NO', 'TYPE', 'CELLNO', 'SUBJ', 'TEXT')
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type
                         ,self.blocks[i].cellno
                         ,self.blocks[i].subj
                         ,self.blocks[i].text
                         ]
                        )
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ,Transpose = True
                           ).run()
        return f'{f}:\n{mes}'
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.multitrandem.elems.Elems._debug_cells'
        headers = ('SUBJ', 'WFORM', 'SPEECH', 'TRANSC', _('ROW #'), _('CELL #')
                  ,_('TYPES'), _('TEXT')
                  )
        subj = []
        wform = []
        speech = []
        transc = []
        rownos = []
        nos = []
        types = []
        texts = []
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
        mes = sh.FastTable (headers = headers
                           ,iterable = (subj, wform, speech, transc, rownos
                                       ,nos, types, texts
                                       )
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ).run()
        return f'{f}:\n{mes}'
    
    def debug(self):
        report = [self._debug_blocks(), self._debug_cells()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
        
    def set_transc(self):
        pass
        #block.type = 'transc'
    
    def add_brackets(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type in ('comment', 'user', 'correction'):
                self.blocks[i].cellno = self.blocks[i-1].cellno
                if not self.blocks[i].text.startswith('(') \
                and not self.blocks[i].text.endswith(')'):
                    self.blocks[i].text = '(' + self.blocks[i].text + ')'
            i += 1
    
    def add_space(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                continue
            cond = False
            if i > 0 and self.blocks[i-1].text:
                if self.blocks[i-1].text[-1] in ['(', '[', '{']:
                    cond = True
            if self.blocks[i].text and not self.blocks[i].text[0].isspace() \
            and not self.blocks[i].text[0] in sh.lg.punc_array \
            and not self.blocks[i].text[0] in [')', ']', '}'] and not cond:
                self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
                
    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
                break
        for block in self.blocks:
            if block.type == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type == 'transc':
                transc = block.text
                break
        for block in self.blocks:
            if block.type == 'term' or block.type == 'phrase':
                term = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block.type in ('term', 'phrase'):
                term = block.text
            block.subj = dic
            block.subjf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
                
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].subj or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = ic.Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)

                block = ic.Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                dic = self.blocks[i].subj
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                       not in ('subj', 'wform', 'transc', 'speech')
                      ]


if __name__ == '__main__':
    f = '[MClient] plugins.multitrandem.elems.__main__'
    search = 'phrenosin'
    import get as gt
    import tags as tg
    iget = gt.Get(search)
    chunks = iget.run()
    if not chunks:
        chunks = []
    blocks = []
    for chunk in chunks:
        add = tg.Tags (chunk = chunk
                      ,Debug = True
                      ).run()
        if add:
            blocks += add
    blocks = Elems (blocks = blocks
                   ,abbr = None
                   ,search = search
                   ,Debug = True
                   ).run()
    for i in range(len(blocks)):
        mes = f'{i}: {blocks[i].type}: "{blocks[i].text}"'
        print(mes)
