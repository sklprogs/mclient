#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently storing
    in DB.
    Needs attributes in blocks: DIC,DICF,SAMECELL,SPEECH,TERM,TRANSC,TYPE,WFORM
    Modifies attributes: DIC,DICF,SAMECELL,SPEECH,TEXT,TRANSC,TYPE,WFORM
    Since TYPE is modified here, SAMECELL is filled here.
'''

import re
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import plugins.multitrancom.subjects as sj


class UniteFixed:
    
    def __init__(self,blocks):
        self.fixed = ('dic','wform','transc','speech')
        self.cells = []
        self.blocks = blocks
    
    def set_cells(self):
        # Create a temporary structure to help merging blocks
        cell = []
        for block in self.blocks:
            if block.same == 1:
                cell.append(block)
            else:
                if cell:
                    self.cells.append(cell)
                cell = [block]
        if cell:
            self.cells.append(cell)
    
    def has_two_fixed(self,types):
        HasFixed = False
        for type_ in types:
            if type_ in self.fixed:
                if HasFixed:
                    return True
                else:
                    HasFixed = True
    
    def get_first_fixed_type(self,cell):
        for block in cell:
            if block.type_ in self.fixed:
                return block.type_
    
    def run(self):
        ''' - We should unite items in 'fixed+comment (SAME=1)' structures
              directly since fixed columns having supplementary SAME=1 blocks
              cannot be properly sorted.
            - Running the entire class takes ~0.0131s for 'set' (EN-RU) on
              AMD E-300.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.UniteFixed.run'
        count = 0
        self.set_cells()
        for i in range(len(self.cells)):
            types = [block.type_ for block in self.cells[i]]
            if self.has_two_fixed(types):
                count += len(self.cells[i])
                self.cells[i][0].type_ = self.get_first_fixed_type(self.cells[i])
                texts = [block.text for block in self.cells[i] \
                         if block.text
                        ]
                self.cells[i][0].text = sh.List(texts).space_items()
                self.cells[i] = [self.cells[i][0]]
        self.blocks = []
        for cell in self.cells:
            self.blocks += cell
        sh.com.rep_matches(f,count)
        return self.blocks



class Block:
    # A copy of Tags.Block
    def __init__(self):
        self.block = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.rowno = -1
        self.dic = ''
        self.dicf = ''
        self.dprior = 0
        self.first = -1
        self.i = -1
        self.semino = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        self.speech = ''
        self.sprior = -1
        self.text = ''
        self.transc = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase', 'speech',
            'term', 'transc', 'user', 'wform'.
        '''
        self.type_ = 'invalid'
        self.url = ''
        self.wform = ''



class Elems:
    # Process blocks before dumping to DB
    def __init__(self,blocks,Debug=False,maxrows=1000):
        self.fixed = ('dic','wform','transc','speech')
        self.sep_words = (' - найдены отдельные слова'
                         ,' - only individual words found'
                         )
        self.dicurls = {}
        self.phdic = ''
        self.blocks = blocks
        self.Debug = Debug
        self.maxrows = maxrows
    
    def delete_refs(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_refs'
        if len(self.blocks) < 3:
            sh.com.rep_lazy(f)
            return
        count = 0
        i = 0
        while i < len(self.blocks):
            if self.blocks[i-1].type_ == 'speech' \
            and self.blocks[i].type_ == 'comment' \
            and self.blocks[i].text == '|' \
            and self.blocks[i+1].type_ == 'wform':
                count += 2
                del self.blocks[i+1]
                del self.blocks[i]
            else:
                i += 1
        sh.com.rep_deleted(f,count)
    
    def _break_word(self,word):
        lst = sh.Text(word).split_by_len(self.max_word_len)
        return ' '.join(lst)
    
    def get_phdic_set(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'phdic':
                return i
    
    def set_phcom(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_phcom'
        count = 0
        i = self.get_phdic_set()
        if i is None:
            sh.com.rep_lazy(f)
        else:
            i += 1
            while i < len(self.blocks):
                if self.blocks[i].type_ == 'comment':
                    self.blocks[i].type_ = 'phcom'
                    count += 1
                i += 1
            sh.com.rep_matches(f,count)
        
    def _get_ged(self):
        geds = []
        for block in self.blocks:
            if block.type_ == 'comment' \
            and block.text == 'Большой Энциклопедический словарь ':
                geds.append(block)
        return geds
    
    def _get_first_dic(self,rowno):
        for block in self.blocks:
            if block.rowno == rowno and block.type_ == 'dic':
                return block
    
    def convert_ged(self):
        ''' - Reassign a subject title for blocks from the Great encyclopedic
              dictionary.
            - It's not enough just to get CELLNO of the Great encyclopedic
              dictionary and change DIC and DICF since DIC and DICF will be
              reassigned at 'self.fill'.
            - Takes ~0.0014s for 'set' (EN-RU) on AMD E-300.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.convert_ged'
        count = 0
        geds = self._get_ged()
        for ged in geds:
            block = self._get_first_dic(ged.rowno)
            if block:
                block.dic = block.text = _('GED')
                block.dicf = _('Great Encyclopedic Dictionary')
                count += 1
            else:
                sh.com.rep_empty(f)
            ''' The dictionary will be renamed, we do not need the comment
                duplicating it.
            '''
            self.blocks.remove(ged)
        sh.com.rep_matches(f,count)
        sh.com.rep_deleted(f,len(geds))
    
    def delete_trash_com(self):
        ''' Sometimes it's not enough to delete comment-only tail since there
            might be no 'phdic' type which serves as an indicator.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_trash_com'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if not (block.type_ == 'comment' \
                       and block.text in ('спросить в форуме'
                                         ,'ask in forum','<!--','-->'
                                         ,'Короткая ссылка','Get short URL'
                                         ,' (у некоторых значений из тезауруса нет переводов в словаре)'
                                         ,' (there may be no translations for some thesaurus entries in the bilingual dictionary)'
                                         )
                              )
                      ]
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def convert_speech(self):
        ''' Blocks inherent to <em> tag are usually 'speech' but not always,
            see, for example, EN-RU, 'blemish'.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.convert_speech'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'speech' \
            and not self.blocks[i-1].type_ in self.fixed:
                self.blocks[i].type_ = 'comment'
                count += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def delete_langs(self):
        ''' - This procedure deletes blocks describing languages in an original
              or localized form. After a comment-only head was deleted, we will
              have either a 'dic' + 'term' + 'term' or 'term' + 'term'
              structure, wherein 'dic' is "Subject area", and terms have an
              empty URL. We should delete only the first two term occurrences
              since there could be other terms with an empty URL that should
              not be deleted, e.g., those related to "БЭС".
            - Since we don't have to search for anything, and have predermined
              indexes, this procedure is very fast.
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_langs'
        if len(self.blocks) > 2:
            if self.blocks[0].type_ == 'dic' \
            and self.blocks[0].text in ('Тематика','Subject area') \
            and self.blocks[1].type_ == 'term' \
            and self.blocks[2].type_ == 'term' \
            and not self.blocks[1].url and not self.blocks[2].url:
                deleted = self.blocks[:3]
                deleted = [item.text for item in deleted]
                mes = '; '.join(deleted)
                sh.objs.get_mes(f,mes,True).show_debug()
                self.blocks = self.blocks[3:]
            elif self.blocks[0].type_ == 'term' \
            and self.blocks[1].type_ == 'term' \
            and not self.blocks[0].url and not self.blocks[1].url:
                deleted = self.blocks[:2]
                deleted = [item.text for item in deleted]
                mes = '; '.join(deleted)
                sh.objs.get_mes(f,mes,True).show_debug()
                self.blocks = self.blocks[2:]
    
    def get_separate_head(self):
        #blocks = ('G','o','o','g','l','e','|','Forvo','|','+')
        blocks = ('Forvo','|','+')
        texts = [block.text for block in self.blocks]
        return sh.List(texts,blocks).find()
    
    def get_separate_tail(self):
        i = 0
        while i < len(self.blocks):
            ''' If the last word is correct, then 'block.text' will be
                ' - найдены отдельные слова', otherwise, it will be
                ' wrong_word - найдены отдельные слова'.
            '''
            if ' - найдены отдельные слова' in self.blocks[i].text \
            or ' - only individual words found' in self.blocks[i].text:
                return i
            i += 1
    
    def _add_sep_subject(self):
        block = Block()
        block.type_ = 'dic'
        block.text = block.dic = block.dicf = _('Separate words')
        block.same = 0
        if self.blocks:
            ''' This allows to avoid a bug when only separate words were found
                but the 1st word should remain a comment since it was not found
                (e.g., EN-RU, "Ouest Bureau").
            '''
            block.rowno = self.blocks[0].rowno
        self.blocks.insert(0,block)
    
    def _has_separate(self,text):
        for phrase in self.sep_words:
            if phrase in text:
                return True
    
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
        for block in self.blocks:
            ''' Those words that were not found will not have a URL and should
                be kept as comments (as in a source). However, SAME should be 0
                everywhere.
            '''
            if block.url:
                block.type_ = 'term'
            else:
                for phrase in self.sep_words:
                    block.text = block.text.replace(phrase,'')
            block.same = 0
        self.blocks = [block for block in self.blocks \
                       if block.text and block.text != '|'
                      ]
    
    def set_separate(self):
        # Takes ~0.0126s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_separate'
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
    
    def make_fixed(self):
        # Takes ~0.0065s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.make_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].rowno != self.blocks[i].rowno:
                if self.blocks[i].type_ == 'user':
                    self.blocks[i].type_ = 'dic'
                    ''' If DICF was not extracted for a user-type block which
                        is actually a subject, we may set such field here,
                        however, such entries as 'Gruzovik, inform.' will not
                        be expanded (due to a bug at multitran.com, 'Informal'
                        will be used). Thus, we correct such entries in
                        SUBJECTS and just try in 'self.expand_dic_file' to
                        expand them.
                    '''
                    self.blocks[i].dic = self.blocks[i].text
                    count += 1
                elif self.blocks[i].type_ == 'comment':
                    self.blocks[i].type_ = 'wform'
                    count += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_see_also(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_see_also'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].rowno != self.blocks[i-1].rowno \
            and self.blocks[i-1].text == '⇒ ' \
            and self.blocks[i-1].rowno == self.blocks[i].rowno \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                self.blocks[i-1].type_ = 'dic'
                self.blocks[i-1].text = self.blocks[i-1].dic \
                                      = self.blocks[i-1].dicf = '⇒'
                self.blocks[i-1].same = 0
                self.blocks[i].same = 0
                count += 2
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_phcount(self):
        for block in self.blocks:
            if block.type_ == 'phcount':
                block.text = ' [{}]'.format(block.text)
                block.same = 1
    
    def set_same(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_same'
        # I have witnessed this error despite 'self.check' was passed
        if not self.blocks:
            sh.com.rep_empty(f)
            return
        self.blocks[0].same = 0
        i = 1
        while i < len(self.blocks):
            # multitran.com originally sets some types with SAME = 1
            if self.blocks[i-1].semino != self.blocks[i].semino \
            or self.blocks[i-1].rowno != self.blocks[i].rowno \
            or self.blocks[i-1].cellno != self.blocks[i].cellno \
            or self.blocks[i].type_ in ('speech','transc'):
                self.blocks[i].same = 0
            elif self.blocks[i].same == -1:
                # Do not overwrite SAME of fixed types
                self.blocks[i].same = 1
            i += 1
    
    def _delete_tail_links(self,poses):
        f = '[MClientQt] plugins.multitrancom.elems.Elems._delete_tail_links'
        if poses:
            pos1, pos2 = poses[0], poses[1] + 1
            self.blocks[pos1:pos2] = []
            sh.com.rep_deleted(f,pos2-pos1)
    
    def delete_tail_links(self):
        ''' - Sometimes it's not enough to delete comment-only tail since there
              might be no 'phdic' type which serves as an indicator.
            - Takes ~0.02s for 'set' (EN-RU) on Intel Atom.
        '''
        ru = ('Добавить','|','Сообщить об ошибке','|','Короткая ссылка','|'
             ,'Способы выбора языков'
             )
        en = ('Add','|','Report an error','|','Get short URL','|'
             ,'Language Selection Tips'
             )
        de = ('Hinzufügen','|','Fehlerhaften Eintrag melden','|'
             ,'Get short URL','|','Hinweise'
             )
        sp = ('Añadir','|','Enviar un mensaje de error','|'
             ,'Enlace corto a esta página','|'
             ,'Modos de seleccionar idiomas'
             )
        uk = ('Додати','|','Повідомити про помилку','|'
             ,'Посилання на цю сторінку','|','Способи вибору мов'
             )
        texts = [block.text for block in self.blocks]
        self._delete_tail_links(sh.List(texts,ru).find())
        self._delete_tail_links(sh.List(texts,en).find())
        self._delete_tail_links(sh.List(texts,de).find())
        self._delete_tail_links(sh.List(texts,sp).find())
        self._delete_tail_links(sh.List(texts,uk).find())
        ru = ('Добавить','|','Способы выбора языков')
        en = ('Add','|','Language Selection Tips')
        self._delete_tail_links(sh.List(texts,ru).find())
        self._delete_tail_links(sh.List(texts,en).find())
    
    def set_phdic(self):
        # Takes ~0.001s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_phdic'
        index_ = self.get_phdic()
        if index_ is None:
            sh.com.rep_lazy(f)
            return
        text = self.blocks[index_+1].text + self.blocks[index_+2].text
        url = self.blocks[index_+1].url
        del self.blocks[index_]
        del self.blocks[index_]
        self.blocks[index_].type_ = 'phdic'
        self.blocks[index_].url = url
        self.blocks[index_].dic = self.phdic = _('phrases')
        self.blocks[index_].dicf = self.blocks[index_].text = text
    
    def get_phdic(self):
        ''' - Sample blocks: "comment"-"comment"-"comment"-"phrase"
              " process: ", "17416 фраз", " в 327 тематиках", "3D-печать"
            - Owing to a bug at 'multitran.com', 'phdic' can be followed
              by 'phcount' and not by 'phrase', although even in this
              case 'phcount' relates to a preceding 'phrase'.
            - This will not work when 'phdic' type is already set
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.get_phdic'
        i = len(self.blocks) - 1
        while i > 3:
            if self.blocks[i-3].type_ == 'comment' \
            and self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ in ('phrase','phcount'):
                return i - 3
            i -= 1
    
    def delete_head(self):
        ''' #NOTE: This will actually delete the entire article if it consists
            of comments only but this looks more like a feature since only
            service articles (nothing was found, suggestions in case nothing
            was found, only separate words were found) consist of comments
            only.
        '''
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_head'
        count = 0
        i = 0
        while i < len(self.blocks):
            if self.blocks[i].type_ == 'comment':
                del self.blocks[i]
                count += 1
                i -= 1
            else:
                break
            i += 1
        sh.com.rep_deleted(f,count)
    
    def get_tail(self):
        i = len(self.blocks) - 1
        while i > 0:
            if self.blocks[i-1].type_ == 'phrase' \
            and self.blocks[i].type_ == 'phcount':
                return i
            i -= 1
    
    def delete_tail(self):
        # Takes ~0.0004s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_tail'
        count = 0
        last = self.get_tail()
        if last is None or last + 1 == len(self.blocks):
            sh.com.rep_lazy(f)
        else:
            last += 1
            count = len(self.blocks) - last
            self.blocks = self.blocks[:last]
            sh.com.rep_deleted(f,count)
    
    def delete_semi(self):
        # I don't like '; ' in special pages, so I delete it everywhere
        f = '[MClientQt] plugins.multitrancom.elems.Elems.delete_semi'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks if block.text != '; ']
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def set_semino(self):
        semino = 0
        for block in self.blocks:
            if block.text == '; ' and block.type_ == 'term':
                semino += 1
            block.semino = semino
    
    def check(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.check'
        if self.blocks:
            return True
        else:
            sh.com.rep_empty(f)
    
    def reassign_brackets(self):
        ''' It is a common case when an opening bracket, a phrase and a closing
            bracket are 3 separate blocks. The following skips user names
            without showing extra brackets (e.g., гематоген -> Фразы: Пан).
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.reassign_brackets'
        count = 0
        i = 2
        while i < len(self.blocks):
            if self.blocks[i-2].text == '(' \
            and self.blocks[i].text == ')' \
            and self.blocks[i-1].type_ in ('comment','user','correction'
                                          ):
                #NOTE: We must inherit i-2 SAME and i-1 TYPE
                self.blocks[i-2].text = '(' + self.blocks[i-1].text + ')'
                self.blocks[i-2].type_ = self.blocks[i-1].type_
                del self.blocks[i-1]
                i -= 1
                del self.blocks[i]
                i -= 1
                count += 2
            i += 1
        sh.com.rep_deleted(f,count)
    
    def expand_dic_file(self):
        ''' Do not delete this, since 'multitran.com' does not provide
            full subject titles in phrase articles!
        '''
        f = '[MClientQt] plugins.multitrancom.elems.Elems.expand_dic_file'
        for block in self.blocks:
            if block.dic and not block.dicf:
                title = sj.objs.get_subjects().get_title(block.dic)
                if title == block.dic:                
                    dics = block.dic.split(', ')
                    dicfs = []
                    for dic in dics:
                        dicfs.append(sj.objs.subjects.get_title(dic))
                    block.dicf = ', '.join(dicfs)
                else:
                    block.dicf = title
    
    def delete_numeration(self):
        # Takes ~0.027s for 'set' (EN-RU) on AMD E-300
        self.blocks = [block for block in self.blocks \
                       if not re.match('^\d+\.$',block.text)
                      ]
    
    def delete_empty(self):
        ''' - Empty blocks are useless since we recreate fixed columns anyways.
            - This is required since we decode HTM entities after extracting
              tags now. Empty blocks may lead to a wrong analysis of blocks,
              e.g., 'comment (SAME=0) - comment (SAME=1)' structure, where the
              second block is empty, will be mistakenly converted to
              'wform - comment'.
            - Do not strip blocks to check for emptiness since 'comment' from a
              'wform+comment' structure where 'wform' is a space cannot be
              further converted to 'wform', see RU-EN, 'цепь: провод'.
        '''
        self.blocks = [block for block in self.blocks if block.text]
    
    def get_suggested(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].text in (' Варианты замены: ',' Suggest: '):
                return i
    
    def set_suggested(self):
        # Takes ~0.005s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_suggested'
        count = 0
        i = self.get_suggested()
        if i is None:
            sh.com.rep_lazy(f)
            return
        rowno = self.blocks[i].rowno
        self.blocks[i].type_ = 'dic'
        self.blocks[i].text = _('Suggestions')
        self.blocks[i].dic = _('Suggestions')
        self.blocks[i].dicf = _('Suggestions')
        self.blocks[i].same = 0
        count += 1
        i += 1
        while i < len(self.blocks):
            if self.blocks[i].rowno == rowno:
                if self.blocks[i].text != '; ':
                    self.blocks[i].type_ = 'term'
                    self.blocks[i].same = 0
                    count += 1
            else:
                break
            i += 1
        sh.com.rep_matches(f,count)
    
    def run(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.run'
        if not self.check():
            sh.com.cancel(f)
            return
        # Process special pages before deleting anything
        self.set_suggested()
        self.set_separate()
        # Do this before deleting ';'
        self.set_semino()
        # Do some cleanup
        self.delete_head()
        self.delete_tail()
        self.delete_empty()
        self.delete_semi()
        self.delete_numeration()
        self.delete_tail_links()
        self.delete_trash_com()
        self.delete_langs()
        self.delete_refs()
        # Reassign types
        if self.blocks and self.blocks[0].dicf != _('Separate words'):
            self.set_phdic()
            self.set_transc()
            self.set_see_also()
            self.convert_speech()
            self.convert_ged()
            self.make_fixed()
            self.set_same()
            self.set_phcom()
        # Prepare contents
        self.set_dic_urls()
        self.set_phcount()
        self.blocks = UniteFixed(self.blocks).run()
        self.reassign_brackets()
        # Prepare for cells
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        self.expand_dic_file()
        # Extra spaces in the beginning may cause sorting problems
        self.add_space()
        #TODO: expand parts of speech (n -> noun, etc.)
        self.restore_dic_urls()
        return self.blocks
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Elems.debug'
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        headers = ('NO','TYPE','TEXT','URL','SAME','SEMINO','ROWNO','CELLNO'
                  ,'DIC','DICF'
                  )
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type_
                         ,'"{}"'.format(self.blocks[i].text)
                         ,'"{}"'.format(self.blocks[i].url)
                         ,self.blocks[i].same
                         ,self.blocks[i].semino
                         ,self.blocks[i].rowno
                         ,self.blocks[i].cellno
                         ,self.blocks[i].dic
                         ,self.blocks[i].dicf
                         ]
                        )
        # 10'' monitor: 12 symbols per a column
        # 23'' monitor: 20 symbols per a column
        return sh.FastTable (headers = headers
                            ,iterable = rows
                            ,maxrow = 23
                            ,maxrows = self.maxrows
                            ,Transpose = True
                            ).run()
        
    def set_transc(self):
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClientQt] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type_ == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                block.type_ = 'transc'
                count += 1
        sh.com.rep_matches(f,count)
    
    def add_space(self):
        f = '[MClientQt] plugins.multitrancom.elems.Elems.add_space'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].same > 0:
                if self.blocks[i].text and self.blocks[i-1].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')',']','}'] \
                  and not self.blocks[i-1].text[-1] in ['(','[','{']:
                      count += 1
                      self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
        if count:
            mes = _('{} matches').format(count)
            sh.objs.get_mes(f,mes,True).show_debug()

    def fill(self):
        dic = dicf = wform = speech = transc = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type_ in ('dic','phdic'):
                dic = block.dic
                dicf = block.dicf
                break
        for block in self.blocks:
            if block.type_ == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type_ == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type_ == 'transc':
                transc = block.text
                break
        
        for block in self.blocks:
            if block.type_ in ('dic','phdic'):
                dic = block.dic
                dicf = block.dicf
            elif block.type_ == 'wform':
                wform = block.text
            elif block.type_ == 'speech':
                speech = block.text
            elif block.type_ == 'transc':
                transc = block.text
            block.dic = dic
            block.dicf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
    
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                ''' #NOTE: We do not inherit SEMINO here since it's not needed
                    anymore.
                '''
                block = Block()
                block.type_ = 'speech'
                block.text = self.blocks[i].speech
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.same = 0
                self.blocks.insert(i,block)
                
                block = Block()
                block.type_ = 'transc'
                block.text = self.blocks[i].transc
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.same = 0
                self.blocks.insert(i,block)

                block = Block()
                block.type_ = 'wform'
                block.text = self.blocks[i].wform
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.same = 0
                self.blocks.insert(i,block)
                
                if self.blocks[i].dic != self.phdic:
                    block = Block()
                    block.type_ = 'dic'
                    block.text = self.blocks[i].dic
                    block.dic = self.blocks[i].dic
                    block.dicf = self.blocks[i].dicf
                    block.wform = self.blocks[i].wform
                    block.speech = self.blocks[i].speech
                    block.transc = self.blocks[i].transc
                    block.same = 0
                    self.blocks.insert(i,block)
                
                dic = self.blocks[i].dic
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks \
                       if block.type_ not in self.fixed
                      ]
                       
    def set_dic_urls(self):
        for block in self.blocks:
            if block.type_ in ('dic','phdic') \
            and not block.text in self.dicurls:
                self.dicurls[block.text] = block.url
    
    def restore_dic_urls(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ in ('dic','phdic') \
            and self.blocks[i].text in self.dicurls:
                self.blocks[i].url = self.dicurls[self.blocks[i].text]
