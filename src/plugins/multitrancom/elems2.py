#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Block:
    # A copy of Tags.Block
    def __init__(self):
        self.Ignore = False
        self.cellno = -1
        self.dic = ''
        self.dicf = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase', 'speech',
            'term', 'transc', 'wform'.
        '''
        self.type_ = 'comment'
        self.url = ''



class Cell:
    
    def __init__(self):
        self.code = ''
        self.text = ''
        self.url = ''
        self.no = -1
        self.blocks = []
        self.Fixed = False
        self.Ignore = False



class Elems:
    
    def __init__(self,blocks):
        self.cells = []
        self.sep_words_found = ('- найдены отдельные слова'
                               ,'- only individual words found'
                               ,'- einzelne Wörter gefunden'
                               ,'- se han encontrado palabras individuales'
                               ,'- знайдено окремі слова'
                               ,'- znaleziono osobne słowa'
                               ,'- 只找到单语'
                               )
        self.blocks = blocks
    
    def _is_block_fixed(self,block):
        return block.type_ in ('dic','wform','speech','transc','phdic')
    
    def _is_cell_fixed(self,cell):
        for block in cell.blocks:
            if block.Fixed:
                return True
    
    def set_fixed_blocks(self):
        for block in self.blocks:
            block.Fixed = self._is_block_fixed(block)
    
    def set_fixed_cells(self):
        for cell in self.cells:
            cell.Fixed = self._is_cell_fixed(cell)
    
    def run_phcount(self):
        f = 'plugins.multitrancom.elems.Elems.run_phcount'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type_ in ('phrase','comment') \
            and self.blocks[i].type_ == 'phcount':
                count += 1
                self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_cells(self):
        f = 'plugins.multitrancom.elems.Elems.set_cells'
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            sh.com.rep_condition(f,mes)
            return
        cell = Cell()
        cell.blocks.append(self.blocks[0])
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cell.blocks.append(self.blocks[i])
            else:
                if cell.blocks:
                    self.cells.append(cell)
                cell = Cell()
                cell.blocks.append(self.blocks[i])
            i += 1
        if cell.blocks:
            self.cells.append(cell)
    
    def renumber(self):
        for i in range(len(self.cells)):
            self.cells[i].no = i
    
    def debug(self):
        #headers = (_('CELL #'),_('IGNORE'),_('FIXED'),_('TEXT'),_('TYPES'))
        headers = (_('FIXED'),_('CELL #'),_('TYPES'),_('TEXT'),'URL')
        nos = []
        texts = []
        fixed = []
        #ignore = []
        types = []
        urls = []
        for cell in self.cells:
            nos.append(cell.no)
            fixed.append(cell.Fixed)
            #ignore.append(cell.Ignore)
            texts.append(cell.text)
            cell_types = [block.type_ for block in cell.blocks]
            types.append(', '.join(cell_types))
            urls.append(cell.url)
        return sh.FastTable (headers = headers
                            ,iterable = (fixed,nos,types,texts,urls)
                            ,maxrow = 60
                            ,maxrows = 0
                            ).run()
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = sh.List(fragms).space_items().strip()
            # 'phdic' text may have multiple spaces for some reason
            cell.text = sh.Text(cell.text).delete_duplicate_spaces()
    
    def delete_semi(self):
        f = 'plugins.multitrancom.elems.Elems.delete_semi'
        count = 0
        for cell in self.cells:
            old_len = len(cell.blocks)
            cell.blocks = [block for block in cell.blocks if block.text != '; ']
            count += old_len - len(cell.blocks)
        sh.com.rep_matches(f,count)
    
    def delete_trash(self):
        f = 'plugins.multitrancom.elems.Elems.delete_trash'
        old_len = len(self.cells)
        self.cells = [cell for cell in self.cells \
                      if not '<!-- -->' in cell.text \
                      and not '<!-- // -->' in cell.text
                     ]
        # The first cell represents an article title
        if len(self.cells) > 1:
            del self.cells[0]
        sh.com.rep_matches(f,old_len-len(self.cells))
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = 'plugins.multitrancom.elems.Elems.unite_brackets'
        count = 0
        for cell in self.cells:
            i = 2
            while i < len(cell.blocks):
                if cell.blocks[i-2].text.strip() == '(' and cell.blocks[i].text.strip() == ')':
                    count += 1
                    ''' Add brackets to text of a cell (usually of the 'user'
                        type), not vice versa, to preserve its type.
                    '''
                    cell.blocks[i-1].text = cell.blocks[i-2].text + cell.blocks[i-1].text + cell.blocks[i].text
                    del cell.blocks[i]
                    del cell.blocks[i-2]
                    i -= 2
                i += 1
        sh.com.rep_matches(f,count)
    
    def separate_fixed(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.separate_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            # There can be multiple 'wform' blocks
            if self.blocks[i-1].Fixed and self.blocks[i].Fixed \
            and self.blocks[i-1].type_ != self.blocks[i].type_:
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        sh.com.rep_matches(f,count)
    
    def convert_wform_dic(self):
        # We have found something like "English thesaurus" entry
        f = '[MClientQt] plugins.multitrancom.elems.Elems.convert_wform_dic'
        count = 0
        i = 5
        while i < len(self.blocks):
            if self.blocks[i-4].type_ == 'wform' \
            and self.blocks[i-3].type_ == 'wform' \
            and self.blocks[i-2].type_ == 'transc' \
            and self.blocks[i-1].type_ == 'speech' \
            and self.blocks[i].type_ == 'dic':
                count += 1
                self.blocks[i].text = self.blocks[i-4].text.strip() + ', ' + self.blocks[i].text.strip()
                del self.blocks[i-4]
                i -= 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def separate_speech(self):
        ''' Speech can come in structures like 'wform + comment + speech', but
            it should always take a separate cell.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.separate_speech'
        count = 0
        i = 1
        while i < len(self.blocks):
            # It is not enough to set 'Fixed'
            if self.blocks[i].type_ == 'speech':
                count += 1
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_transc(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type_ == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                count += 1
                block.type_ = 'transc'
        sh.com.rep_matches(f,count)
    
    def delete_empty(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_empty'
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text.strip()]
        sh.com.rep_matches(f,old_len-len(self.blocks))
    
    def convert_user_dic(self):
        # "Gruzovik" and other entries that function as 'dic'
        f = '[MClientQt] plugins.multitrancom.elems.Elems.convert_user_dic'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'user' \
            and self.blocks[i-1].cellno != self.blocks[i].cellno:
                count += 1
                self.blocks[i].type_ = 'dic'
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_phdic(self):
        i = len(self.blocks) - 4
        while i >= 0:
            if self.blocks[i-3].type_ == 'comment' \
            and self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ == 'phrase':
                self.blocks[i-3].type_ = 'phdic'
            i -= 1
    
    def _set_separate(self):
        blocks = []
        for i in range(len(self.blocks)):
            if self.blocks[i].url.startswith('l'):
                blocks.append(self.blocks[i])
            elif self.blocks[i].text == '|':
                if not self.blocks[i-1].url:
                    blocks.append(self.blocks[i-1])
                if not self.blocks[i+1].url:
                    blocks.append(self.blocks[i+1])
            elif self._has_separate(self.blocks[i].text):
                blocks.append(self.blocks[i])
        self.blocks = blocks

    def _delete_separate(self):
        i = 1
        while i < len(self.blocks):
            ''' Those words that were not found will not have a URL and should
                be kept as comments (as in a source). However, 'cellno' should
                differ from a previous cell.
            '''
            if self.blocks[i].url:
                self.blocks[i].type_ = 'term'
            else:
                for phrase in self.sep_words_found:
                    self.blocks[i].text = self.blocks[i].text.replace(phrase,'')
            self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        self.blocks = [block for block in self.blocks \
                       if block.text and block.text != '|'
                      ]
    
    def set_separate_words(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_separate_words'
        old_len = len(self.blocks)
        tail = self.get_separate_tail()
        if not tail:
            sh.com.rep_lazy(f)
            return
        head = self.get_separate_head()
        if not head:
            sh.com.rep_lazy(f)
            return
        self.blocks = self.blocks[head[1]:tail+1]
        if len(self.blocks) < 3:
            sh.com.rep_lazy(f)
            return
        self._set_separate()
        self._delete_separate()
        sh.com.rep_deleted(f,old_len-len(self.blocks))
        self._add_sep_subject()
    
    def get_separate_head(self):
        blocks = ('Forvo','|','+')
        texts = [block.text for block in self.blocks]
        return sh.List(texts,blocks).find()
    
    def _has_separate(self,text):
        for pattern in self.sep_words_found:
            if pattern in text:
                return True
    
    def get_separate_tail(self):
        i = 0
        while i < len(self.blocks):
            ''' If the last word is correct, then 'block.text' will be
                ' - найдены отдельные слова', otherwise, it will be
                ' wrong_word - найдены отдельные слова'.
            '''
            for pattern in self.sep_words_found:
                if pattern in self.blocks[i].text:
                    return i
            i += 1
    
    def _add_sep_subject(self):
        block = Block()
        block.type_ = 'dic'
        block.text = block.dic = block.dicf = _('Separate words')
        self.blocks.insert(0,block)
    
    def _get_url(self,cell):
        #TODO: Do we need to support several URLs in one cell?
        for block in cell.blocks:
            if block.url:
                return block.url
        return ''
    
    def set_urls(self):
        for cell in self.cells:
            cell.url = self._get_url(cell)
    
    def run(self):
        self.delete_empty()
        self.set_separate_words()
        self.set_transc()
        self.convert_wform_dic()
        self.separate_speech()
        self.convert_user_dic()
        self.set_phdic()
        self.set_fixed_blocks()
        self.separate_fixed()
        self.run_phcount()
        self.set_cells()
        self.set_urls()
        self.delete_semi()
        self.unite_brackets()
        self.set_text()
        self.delete_trash()
        self.set_fixed_cells()
        self.renumber()
