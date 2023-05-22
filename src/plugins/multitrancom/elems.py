#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic


class Trash:
    
    def __init__(self, blocks):
        self.Parallel = False
        self.head = self.tail = None
        self.blocks = blocks
    
    def _get_head_wform(self):
        # Get trash head for general articles
        pos = None
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'wform' and self.blocks[i].text == ' ':
                pos = i
                break
        ''' If 'wform' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 0):
            return
        if set([block.type_ for block in self.blocks[:pos]]) == {'comment'}:
            return pos
    
    def _get_head_subj(self):
        ''' Get trash head (phrase section, all subjects). The first term
            should be 'Subject' of 'subj' type and next two terms should denote
            languages.
        '''
        pos = None
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].type_ == 'subj' and not self.blocks[i-2].url \
            and self.blocks[i-1].type_ == 'term' and not self.blocks[i-1].url \
            and self.blocks[i].type_ == 'term' and not self.blocks[i].url:
                pos = i
                break
            i += 1
        ''' If 'term' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 2):
            return
        if set([block.type_ for block in self.blocks[:pos-2]]) == {'comment'}:
            return pos
    
    def _get_head_term(self):
        ''' Get trash head (phrase section, single subject). The first two
            terms should denote languages.
        '''
        pos = None
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].type_ == 'term' and not self.blocks[i-1].url \
            and self.blocks[i].type_ == 'term' and not self.blocks[i].url:
                pos = i
                break
            i += 1
        ''' If 'term' block firstly occurs at 0 (which is unlikely), there is
            no trash head and therefore no need to remove it.
        '''
        if pos in (None, 1):
            return
        if set([block.type_ for block in self.blocks[:pos-1]]) == {'comment'}:
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
    
    def set_tail(self):
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ != 'comment':
                return
            if self.blocks[i].text == '<!--':
                self.tail = i
                return
            i -= 1
    
    def report(self):
        f = '[MClientQt] plugins.multitrancom.elems.Trash.report'
        if self.head is not None:
            delete = [block.text for block in self.blocks[:self.head]]
            delete = sh.List(delete).space_items()
            mes = _('Start fragment: "{}"').format(delete)
            sh.objs.get_mes(f,mes,True).show_debug()
        if self.tail is not None:
            delete = [block.text for block in self.blocks[self.tail:]]
            delete = sh.List(delete).space_items()
            mes = _('End fragment: "{}"').format(delete)
            sh.objs.get_mes(f,mes,True).show_debug()
    
    def delete(self):
        f = '[MClientQt] plugins.multitrancom.elems.Trash.delete'
        old_len = len(self.blocks)
        # Tail must be deleted first
        if self.tail is not None:
            self.blocks = self.blocks[:self.tail]
        if self.head is not None:
            self.blocks = self.blocks[self.head+1:]
        sh.com.rep_matches(f,old_len-len(self.blocks))
    
    def run(self):
        self.set_head()
        self.set_tail()
        self.report()
        self.delete()
        return self.blocks



class Thesaurus:
    ''' - "English thesaurus" wform becoming subj. Run after 'delete_empty';
        - Thesaurus is optional so we use 'rep_lazy' instead of 'cancel'.
    '''
    def __init__(self,blocks):
        self.no = None
        self.blocks = blocks
    
    def set_no(self):
        ''' We don't have to delete empty 'wform' blocks since they will be
            deleted at the next step, 'Elems.delete_empty'.
        '''
        i = 0
        while i < len(self.blocks) - 2:
            if self.blocks[i].type_ == 'wform' and self.blocks[i].text == ' ' \
            and self.blocks[i+1].type_ == 'wform' \
            and self.blocks[i+1].text.strip() \
            and self.blocks[i+2].type_ == 'wform' \
            and self.blocks[i+2].text == ' ':
                self.no = i + 1
                self.blocks[self.no].text = self.blocks[self.no].subj = _('Thes.')
                self.blocks[self.no].subjf = _('Thesaurus')
                return
            i += 1
    
    def add(self):
        f = '[MClientQt] plugins.multitrancom.elems.Thesaurus.add'
        if self.no is None:
            sh.com.rep_lazy(f)
            return
        count = 0
        i = self.no + 1
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'subj':
                count += 1
                self.blocks[i].text = sh.List ([self.blocks[self.no].text,','
                                              ,self.blocks[i].text]
                                              ).space_items()
                self.blocks[i].subj = sh.List ([self.blocks[self.no].subj,','
                                              ,self.blocks[i].subj]
                                              ).space_items()
                self.blocks[i].subjf = sh.List ([self.blocks[self.no].subjf,','
                                               ,self.blocks[i].subjf]
                                               ).space_items()
            i += 1
        sh.com.rep_matches(f,count)
    
    def delete(self):
        f = '[MClientQt] plugins.multitrancom.elems.Thesaurus.delete'
        if self.no is None:
            sh.com.rep_lazy(f)
            return
        try:
            del self.blocks[self.no]
        except IndexError:
            # This should never happen. We did the search in the same class.
            mes = _('Wrong input data: "{}"!').format(self.no)
            sh.objs.get_mes(f,mes).show_warning()
    
    def run(self):
        self.set_no()
        self.add()
        self.delete()
        return self.blocks



class SeparateWords:
    
    def __init__(self,blocks):
        self.patterns = ('- найдены отдельные слова'
                        ,'- only individual words found'
                        ,'- einzelne Wörter gefunden'
                        ,'- se han encontrado palabras individuales'
                        ,'- знайдено окремі слова'
                        ,'- znaleziono osobne słowa'
                        ,'- 只找到单语'
                        )
        self.Separate = False
        self.blocks = blocks
    
    def _set(self):
        ''' Cannot just limit blocks to those which URL starts with 'l1' since
            there can be unknown words.
        '''
        blocks = []
        for i in range(len(self.blocks)):
            if self.blocks[i].url.startswith('l'):
                blocks.append(self.blocks[i])
            elif self.blocks[i].text == '|':
                if not self.blocks[i-1].url:
                    blocks.append(self.blocks[i-1])
                if not self.blocks[i+1].url:
                    blocks.append(self.blocks[i+1])
            elif self._has(self.blocks[i].text):
                blocks.append(self.blocks[i])
        ''' Includes an unknown word that comes last. Other unknown words are
            already included.
        '''
        if len(self.blocks) > 1:
            no = len(self.blocks) - 2
            if self.blocks[no].type_ == 'comment' \
            and self.blocks[no].text.startswith(' ') \
            and not self.blocks[no].url:
                blocks.append(self.blocks[no])
        self.blocks = blocks

    def _delete(self):
        i = 1
        while i < len(self.blocks):
            ''' Those words that were not found will not have a URL and should
                be kept as comments (as in a source). However, 'cellno' should
                differ from a previous cell.
            '''
            if self.blocks[i].url:
                self.blocks[i].type_ = 'term'
            else:
                for pattern in self.patterns:
                    self.blocks[i].text = self.blocks[i].text.replace(pattern,'')
            self.blocks[i].cellno = self.blocks[i-1].cellno
            i += 1
        self.blocks = [block for block in self.blocks \
                       if block.text and block.text != '|'
                      ]
    
    def _has(self, text):
        for pattern in self.patterns:
            if pattern in text:
                return True
    
    def _add_subject(self):
        block = ic.Block()
        block.type_ = 'subj'
        block.text = block.subjf = _('Separate words')
        block.subj = _('sep. words')
        self.blocks.insert(0, block)
    
    def _set_terms(self):
        for i in range(len(self.blocks)):
            self.blocks[i].cellno = i
            if self.blocks[i].type_ == 'comment' \
            and self.blocks[i].url.startswith('l1'):
                self.blocks[i].type_ = 'term'
    
    def set(self):
        f = '[MClientQt] plugins.multitrancom.elems.SeparateWords.set'
        old_len = len(self.blocks)
        tail = self.get_tail()
        if not tail:
            sh.com.rep_lazy(f)
            return
        head = self.get_head()
        if not head:
            sh.com.rep_lazy(f)
            return
        self.blocks = self.blocks[head[1]:tail+1]
        if len(self.blocks) < 3:
            sh.com.rep_lazy(f)
            return
        self._set()
        self._delete()
        self._set_terms()
        sh.com.rep_deleted(f,old_len-len(self.blocks))
        self._add_subject()
        self.Separate = True
    
    def get_head(self):
        blocks = ('Forvo', '|', '+')
        texts = [block.text for block in self.blocks]
        return sh.List(texts, blocks).find()
    
    def get_tail(self):
        i = 0
        while i < len(self.blocks):
            ''' If the last word is correct, then 'block.text' will be
                ' - найдены отдельные слова', otherwise, it will be
                ' wrong_word - найдены отдельные слова'.
            '''
            for pattern in self.patterns:
                if pattern in self.blocks[i].text:
                    return i
            i += 1
    
    def run(self):
        self.set()
        return self.blocks



class Suggestions:
    
    def __init__(self, blocks):
        self.patterns = (' Варианты замены: ', ' Suggest: '
                        ,' Mögliche Varianten: ', ' Variantes de sustitución: '
                        ,' Варіанти заміни: ', ' Opcje zamiany: ', ' 建议: '
                        )
        self.blocks = blocks
    
    def _has(self, text):
        for pattern in self.patterns:
            if pattern in text:
                return True
    
    def has(self):
        for block in self.blocks:
            if block.type_ != 'comment':
                continue
            for pattern in self.patterns:
                if pattern == block.text:
                    return True
    
    def _add_subject(self):
        block = ic.Block()
        block.type_ = 'subj'
        block.text = block.subjf = _('Suggestions:')
        block.subj = _('sug.')
        self.blocks.insert(0, block)
    
    def set(self):
        f = '[MClientQt] plugins.multitrancom.elems.Suggestions.set'
        if not self.has():
            sh.com.rep_lazy(f)
            return
        old_len = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if block.url.startswith('l1')
                      ]
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        for block in self.blocks:
            ''' Should have only blocks of 'comment' type by now, but we want
                to be on a safe side.
            '''
            if block.type_ == 'comment':
                block.type_ = 'term'
        sh.com.rep_deleted(f,old_len-len(self.blocks))
        self._add_subject()
    
    def run(self):
        self.set()
        return self.blocks



class Elems:
    
    def __init__(self,blocks):
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
            if cell.fixed_block.type_ in ('subj', 'phsubj', 'wform') and cell.url:
                self.fixed_urls[cell.fixed_block.type_][cell.text] = cell.url                
    
    def _is_block_fixed(self,block):
        return block.type_ in ('subj', 'wform', 'speech', 'transc', 'phsubj')
    
    def _get_fixed_block(self,cell):
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
        f = '[MClientQt] plugins.multitrancom.elems.Elems.run_phcount'
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
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_cells'
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        if len(self.blocks) < 2:
            mes = f'{len(self.blocks)} >= 2'
            sh.com.rep_condition(f,mes)
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
        headers = ('SUBJ','WFORM','SPEECH','TRANSC',_('ROW #'),_('CELL #')
                  ,_('TYPES'),_('TEXT'),'URL'
                  )
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
            cell_types = [block.type_ for block in cell.blocks]
            types.append(', '.join(cell_types))
            urls.append(cell.url)
        return sh.FastTable (headers = headers
                            ,iterable = (subj,wform,speech,transc,rownos,nos
                                        ,types,texts,urls
                                        )
                            ,maxrow = 30
                            ,maxrows = 0
                            ).run()
    
    def set_text(self):
        for cell in self.cells:
            fragms = [block.text for block in cell.blocks]
            cell.text = sh.List(fragms).space_items().strip()
            # 'phsubj' text may have multiple spaces for some reason
            cell.text = sh.Text(cell.text).delete_duplicate_spaces()
    
    def delete_semi(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_semi'
        count = 0
        for cell in self.cells:
            old_len = len(cell.blocks)
            cell.blocks = [block for block in cell.blocks if block.text != '; ']
            count += old_len - len(cell.blocks)
        sh.com.rep_matches(f,count)
    
    def unite_brackets(self):
        ''' Combine a cell with a preceding or following bracket such that the
            user would not see '()' when the cell is ignored/blocked.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.unite_brackets'
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
    
    def convert_user_subj(self):
        # "Gruzovik" and other entries that function as 'subj'
        f = '[MClientQt] plugins.multitrancom.elems.Elems.convert_user_subj'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'user' \
            and self.blocks[i-1].cellno != self.blocks[i].cellno:
                count += 1
                self.blocks[i].type_ = 'subj'
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_phsubj(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_phsubj'
        if len(self.blocks) < 4:
            sh.com.rep_lazy(f)
            return
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i-3].type_ == 'comment' \
            and self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ == 'phrase':
                self.blocks[i-3].type_ = 'phsubj'
            i -= 1
    
    def _get_url(self,cell):
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
            if self.blocks[i-1].type_ == 'term' \
            and self.blocks[i-1].text == '⇒ ' \
            and self.blocks[i].type_ == 'term':
                self.blocks[i-1].type_ = 'subj'
                # We just need a different 'cellno' (will be reassigned anyway)
                self.blocks[i].cellno = self.blocks[i-1].cellno + 0.1
                if not self.blocks[i-1].url:
                    self.blocks[i-1].url = self.blocks[i].url
            i += 1
    
    def _get_last_subj(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type_ in ('subj','phsubj'):
                return cell.text
    
    def _get_last_wform(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type_ == 'wform':
                return cell.text
    
    def _get_last_speech(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type_ == 'speech':
                return cell.text
    
    def _get_last_transc(self):
        for cell in self.cells[::-1]:
            if cell.fixed_block and cell.fixed_block.type_ == 'transc':
                return cell.text
    
    def _get_prev_subj(self,i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type_ in ('subj','phsubj'):
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_wform(self,i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type_ == 'wform':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_speech(self,i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type_ == 'speech':
                return self.cells[i].text
            i -= 1
        return ''
    
    def _get_prev_transc(self,i):
        while i >= 0:
            if self.cells[i].fixed_block \
            and self.cells[i].fixed_block.type_ == 'transc':
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
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_fixed'
        count = 0
        i = 0
        while i < len(self.cells):
            if self.cells[i].fixed_block:
                count += 1
                del self.cells[i]
                i -= 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def strip_blocks(self):
        # Needed for 'phsubj' and such 'wform' as 'English Thesaurus'
        for block in self.blocks:
            if not block.Fixed:
                continue
            block.text = block.text.strip()
    
    def rename_phsubj(self):
        for cell in self.cells:
            if cell.fixed_block and cell.fixed_block.type_ == 'phsubj':
                match = re.search(r'(\d+)',cell.text)
                if match:
                    title = _('Phrases ({})').format(match.group(1))
                    # 'fill_fixed' is block-oriented
                    cell.text = cell.fixed_block.text = cell.fixed_block.subj \
                              = cell.fixed_block.subjf = title
                    # There should be only one 'phsubj'
                    return
    
    def set_row_nos(self):
        # Run this before deleting fixed types
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_row_nos'
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
        sh.com.rep_matches(f,count)
    
    def set_art_subj(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_art_subj'
        count = 0
        for block in self.blocks:
            if block.type_ in ('subj', 'phsubj') and block.subj and block.subjf:
                count += 1
                self.art_subj[block.subj] = block.subjf
        sh.com.rep_matches(f,count)
    
    def run(self):
        # Find thesaurus before deleting empty blocks
        self.blocks = Thesaurus(self.blocks).run()
        iseparate = SeparateWords(self.blocks)
        self.blocks = iseparate.run()
        self.blocks = Suggestions(self.blocks).run()
        # Remove trash only after setting separate words
        itrash = Trash(self.blocks)
        self.blocks = itrash.run()
        self.Parallel = itrash.Parallel
        self.Separate = iseparate.Separate
        # Remove empty blocks only after removing trash
        self.delete_empty()
        self.set_transc()
        self.separate_speech()
        self.convert_user_subj()
        self.set_phsubj()
        self.set_see_also()
        self.set_fixed_blocks()
        self.separate_fixed()
        self.run_phcount()
        self.strip_blocks()
        self.set_cells()
        self.set_urls()
        self.delete_semi()
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
