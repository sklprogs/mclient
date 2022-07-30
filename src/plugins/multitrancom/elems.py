#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently
    storing in DB.
    Needs attributes in blocks: DIC,DICF,SAMECELL,SPEECH,TERM,TRANSC
                               ,TYPE,WFORM
    Modifies attributes: DIC,DICF,SAMECELL,SELECTABLE,SPEECH,TERM,TEXT
                        ,TRANSC,TYPE,WFORM
    Since TYPE is modified here, SAMECELL is filled here.
'''

import re
from skl_shared.localize import _
import skl_shared.shared as sh
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
        ''' - We should unite items in 'fixed+comment (SAME=1)'
              structures directly since fixed columns having
              supplementary SAME=1 blocks cannot be properly sorted.
            - Running the entire class takes ~0.0131s for 'set' (EN-RU)
              on AMD E-300
        '''
        f = '[MClient] plugins.multitrancom.elems.UniteFixed.run'
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



# A copy of Tags.Block
class Block:
    
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
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        self.transc = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'user', 'wform'
        '''
        self.type_ = 'invalid'
        self.url = ''
        self.wform = ''



class Elems:
    ''' Process blocks before dumping to DB.
        About filling 'term':
        - We fill 'term' from the start in order to ensure the correct
          'term' value for blocks having 'same == 1'
        - We fill 'term' from the end in order to ensure that 'term'
          of blocks of non-selectable types will have the value of
          the 'term' AFTER those blocks
        - We fill 'term' from the end in order to ensure that 'term'
          is also filled for blocks having 'same == 0'
        - When filling 'term' from the start to the end, in order
          to set a default 'term' value, we also search for blocks of
          the 'phrase' type (just to be safe in such cases when
          'phrase' blocks anticipate 'term' blocks). However, we fill
          'term' for 'phrase' blocks from the end to the start because
          we want the 'phrase' subject to have the 'term' value of
          the first 'phrase' block AFTER it
        - Finally, we clear TERM values for fixed columns. Sqlite
          sorts '' before a non-empty string, so we ensure thereby that
          sorting by TERM will be correct. Otherwise, we would have to
          correctly calculate TERM values for fixed columns that will
          vary depending on the view. Incorrect sorting by TERM may
          result in putting a 'term' item before fixed columns.
    '''
    def __init__(self,blocks,Debug=False,maxrows=1000):
        ''' 30 is the maximum to correctly show EN-RU, 'entity'
            (2 or 3 columns).
        '''
        self.max_word_len = 30
        self.fixed = ('dic','wform','transc','speech')
        self.dicurls = {}
        self.phdic = ''
        self.blocks = blocks
        self.Debug = Debug
        self.maxrows = maxrows
    
    def delete_refs(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_refs'
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
    
    def break_long_words(self):
        # Break too long words (e.g., URLs) that spoil the page layout
        # Takes ~0.023s for 'set' on Intel Atom
        f = '[MClient] plugins.multitrancom.elems.Elems.break_long_words'
        count = 0
        for block in self.blocks:
            Match = False
            words = block.text.split(' ')
            for i in range(len(words)):
                if len(words[i]) > self.max_word_len:
                    Match = True
                    count += 1
                    words[i] = self._break_word(words[i])
            if Match:
                block.text = ' '.join(words)
        sh.com.rep_matches(f,count)
    
    def get_phdic_set(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].type_ == 'phdic':
                return i
    
    def set_phcom(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_phcom'
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
        ''' - Reassign a subject title for blocks from the Great
              encyclopedic dictionary.
            - It's not enough just to get CELLNO of the Great
              encyclopedic dictionary and change DIC and DICF since
              DIC and DICF will be reassigned at 'self.fill'.
            - Takes ~0.0014s for 'set' (EN-RU) on AMD E-300
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.convert_ged'
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
            ''' The dictionary will be renamed, we do not need
                the comment duplicating it.
            '''
            self.blocks.remove(ged)
        sh.com.rep_matches(f,count)
        sh.com.rep_deleted(f,len(geds))
    
    def delete_trash_com(self):
        ''' Sometimes it's not enough to delete comment-only tail since
            there might be no 'phdic' type which serves as an indicator.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_trash_com'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if not (block.type_ == 'comment' \
                       and block.text in ('спросить в форуме'
                                         ,'ask in forum','<!--','-->'
                                         ,'Ссылка на эту страницу'
                                         ,'Get short URL'
                                         ,' (у некоторых значений из тезауруса нет переводов в словаре)'
                                         ,' (there may be no translations for some thesaurus entries in the bilingual dictionary)'
                                         )
                              )
                      ]
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def convert_speech(self):
        ''' Blocks inherent to <em> tag are usually 'speech' but not
            always, see, for example, EN-RU, 'blemish'.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.convert_speech'
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
        ''' - This procedure deletes blocks describing languages in
              an original or localized form. After a comment-only head
              was deleted, we will have either a 'dic' + 'term' + 'term'
              or 'term' + 'term' structure, wherein 'dic' is "Subject
              area", and terms have an empty URL. We should delete only
              the first two term occurrences since there could be other
              terms with an empty URL that should not be deleted, e.g.,
              those related to "БЭС".
            - Since we don't have to search for anything, and have
              predermined indexes, this procedure is very fast.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_langs'
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
    
    def set_not_found(self):
        ''' - This is actually not needed since 'self.delete_head' will
              remove the entire article if it consists of comments only.
              We keep this code just to be on a safe side (e.g., in case
              the author of MT adds non-comment blocks).
            - Takes ~0.007s for 'set' (EN-RU) on AMD E-300
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.set_not_found'
        texts = [block.text for block in self.blocks]
        ru = ('Forvo','|','+','\xa0Не найдено')
        en = ('Forvo','|','+','\xa0Not found')
        if sh.List(texts,ru).find() or sh.List(texts,en).find():
            sh.com.rep_deleted(f,len(self.blocks))
            self.blocks = []
        else:
            sh.com.rep_lazy(f)
    
    def get_separate_head(self):
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
    
    def set_separate(self):
        # Takes ~0.0126s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_separate'
        head = self.get_separate_head()
        if head:
            tail = self.get_separate_tail()
            if tail:
                self.blocks = self.blocks[head[1]:tail+1]
                self.blocks = [block for block in self.blocks \
                               if not block.text in ('+','|')
                              ]
                for block in self.blocks:
                    ''' Those words that were not found will not have
                        a URL and should be kept as comments (as in
                        a source). However, SAME should be 0 everywhere.
                    '''
                    if block.url:
                        block.type_ = 'term'
                    else:
                        block.text = block.text.replace(' - найдены отдельные слова','')
                        block.text = block.text.replace(' - only individual words found','')
                    block.same = 0
                block = Block()
                block.type_ = 'dic'
                block.text = block.dic = block.dicf = _('Separate words')
                block.same = 0
                if self.blocks:
                    ''' This allows to avoid a bug when only separate
                        words were found but the 1st word should remain
                        a comment since it was not found (e.g., EN-RU,
                        "Ouest Bureau").
                    '''
                    block.rowno = self.blocks[0].rowno
                self.blocks.insert(0,block)
                ''' The last matching block may be a comment with no
                    text since we have deleted ' - найдены отдельные
                    слова'. Zero-length blocks are not visible in
                    a one-row table, so this may be needed just to
                    output a correct number of matches.
                '''
                self.blocks = [block for block in self.blocks \
                               if block.text
                              ]
                sh.com.rep_matches(f,len(self.blocks))
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_lazy(f)
    
    def make_fixed(self):
        # Takes ~0.0065s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.make_fixed'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].rowno != self.blocks[i].rowno:
                if self.blocks[i].type_ == 'user':
                    self.blocks[i].type_ = 'dic'
                    ''' If DICF was not extracted for a user-type block
                        which is actually a subject, we may set such
                        field here, however, such entries as 'Gruzovik,
                        inform.' will not be expanded (due to a bug at
                        multitran.com, 'Informal' will be used). Thus,
                        we correct such entries in SUBJECTS and just
                        try in 'self.expand_dic_file' to expand them.
                    '''
                    self.blocks[i].dic = self.blocks[i].text
                    count += 1
                elif self.blocks[i].type_ == 'comment':
                    self.blocks[i].type_ = 'wform'
                    count += 1
            i += 1
        sh.com.rep_matches(f,count)
    
    def set_see_also(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.set_see_also'
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
        f = '[MClient] plugins.multitrancom.elems.Elems.set_same'
        # I have witnessed this error despite 'self.check' was passed
        if self.blocks:
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
        else:
            sh.com.rep_empty(f)
    
    def _delete_tail_links(self,poses):
        f = '[MClient] plugins.multitrancom.elems.Elems._delete_tail_links'
        if poses:
            pos1, pos2 = poses[0], poses[1] + 1
            self.blocks[pos1:pos2] = []
            sh.com.rep_deleted(f,pos2-pos1)
    
    def delete_tail_links(self):
        ''' - Sometimes it's not enough to delete comment-only tail
              since there might be no 'phdic' type which serves as
              an indicator.
            - Takes ~0.02s for 'set' (EN-RU) on Intel Atom
        '''
        ru = ('Добавить','|','Сообщить об ошибке','|'
             ,'Ссылка на эту страницу','|'
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
        f = '[MClient] plugins.multitrancom.elems.Elems.set_phdic'
        index_ = self.get_phdic()
        if index_ is None:
            sh.com.rep_lazy(f)
        else:
            text = self.blocks[index_+1].text + self.blocks[index_+2].text
            url = self.blocks[index_+1].url
            del self.blocks[index_]
            del self.blocks[index_]
            self.blocks[index_].type_ = 'phdic'
            self.blocks[index_].url = url
            self.blocks[index_].select = 1
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
        f = '[MClient] plugins.multitrancom.elems.Elems.get_phdic'
        i = len(self.blocks) - 1
        while i > 3:
            if self.blocks[i-3].type_ == 'comment' \
            and self.blocks[i-2].type_ == 'comment' \
            and self.blocks[i-1].type_ == 'comment' \
            and self.blocks[i].type_ in ('phrase','phcount'):
                return i - 3
            i -= 1
    
    def delete_head(self):
        ''' #NOTE: This will actually delete the entire article if it
            consists of comments only but this looks more like a feature
            since only service articles (nothing was found, suggestions
            in case nothing was found, only separate words were found)
            consist of comments only.
        '''
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_head'
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
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_tail'
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
        f = '[MClient] plugins.multitrancom.elems.Elems.delete_semi'
        len_ = len(self.blocks)
        self.blocks = [block for block in self.blocks \
                       if block.text != '; '
                      ]
        sh.com.rep_deleted(f,len_-len(self.blocks))
    
    def set_semino(self):
        semino = 0
        for block in self.blocks:
            if block.text == '; ' and block.type_ == 'term':
                semino += 1
            block.semino = semino
    
    def check(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.check'
        if self.blocks:
            return True
        else:
            sh.com.rep_empty(f)
    
    def reassign_brackets(self):
        ''' It is a common case when an opening bracket, a phrase and 
            a closing bracket are 3 separate blocks. Tkinter (unlike
            popular web browsers) wraps these blocks after ')'.
            We just fix this behavior. This also allows to skip user
            names without showing extra brackets.
        '''
        f = '[MClient] plugins.multitrancom.elems.Elems.reassign_brackets'
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
        f = '[MClient] plugins.multitrancom.elems.Elems.expand_dic_file'
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
        ''' - Empty blocks are useless since we recreate fixed columns
              anyways.
            - This is required since we decode HTM entities after
              extracting tags now. Empty blocks may lead to a wrong
              analysis of blocks, e.g.,
              'comment (SAME=0) - comment (SAME=1)' structure, where
              the second block is empty, will be mistakenly converted
              to 'wform - comment'.
            - Do not strip blocks to check for emptiness since 'comment'
              from a 'wform+comment' structure where 'wform' is a space
              cannot be further converted to 'wform', see RU-EN,
              'цепь: провод'.
        '''
        self.blocks = [block for block in self.blocks if block.text]
    
    def set_term_same(self):
        ''' #NOTE: all blocks of the same cell must have the same TERM,
            otherwise, alphabetizing may put blocks with SAME=1 outside
            of their cells.
        '''
        term = ''
        for block in self.blocks:
            if block.same == 0:
                term = block.term
            elif block.same == 1:
                block.term = term
    
    def get_suggested(self):
        for i in range(len(self.blocks)):
            if self.blocks[i].text in (' Варианты замены: '
                                      ,' Suggest: '
                                      ):
                return i
    
    def set_suggested(self):
        # Takes ~0.005s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_suggested'
        count = 0
        i = self.get_suggested()
        if i is None:
            sh.com.rep_lazy(f)
        else:
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
        f = '[MClient] plugins.multitrancom.elems.Elems.run'
        if self.check():
            # Process special pages before deleting anything
            self.set_not_found()
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
            self.break_long_words()
            # Prepare for cells
            self.fill()
            self.fill_term()
            self.remove_fixed()
            self.insert_fixed()
            self.set_fixed_term()
            self.expand_dic_file()
            self.set_term_same()
            # Extra spaces in the beginning may cause sorting problems
            self.add_space()
            #TODO: expand parts of speech (n -> noun, etc.)
            self.set_selectables()
            self.restore_dic_urls()
            self.debug()
            return self.blocks
        else:
            sh.com.cancel(f)
    
    def debug(self):
        f = 'plugins.multitrancom.elems.Elems.debug'
        if self.Debug:
            headers = ('NO','TYPE','TEXT','URL','SAME','SEMINO','ROWNO'
                      ,'CELLNO','SELECT','DIC','DICF','TERM'
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
                             ,self.blocks[i].select
                             ,self.blocks[i].dic
                             ,self.blocks[i].dicf
                             ,self.blocks[i].term
                             ]
                            )
            # 10'' monitor: 12 symbols per a column
            # 23'' monitor: 20 symbols per a column
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = 12
                               ,maxrows = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
        
    def set_transc(self):
        # Takes ~0.003s for 'set' (EN-RU) on AMD E-300
        f = '[MClient] plugins.multitrancom.elems.Elems.set_transc'
        count = 0
        for block in self.blocks:
            if block.type_ == 'comment' and block.text.startswith('[') \
            and block.text.endswith(']'):
                block.type_ = 'transc'
                count += 1
        sh.com.rep_matches(f,count)
    
    def add_space(self):
        f = '[MClient] plugins.multitrancom.elems.Elems.add_space'
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
        dic = dicf = wform = speech = transc = term = ''
        
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
            if block.type_ in ('term','phrase'):
                term = block.text
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
                ''' #TODO: Is there a difference if we use both
                    term/phrase here or the term only?
                '''
            elif block.type_ in ('term','phrase'):
                term = block.text
            block.dic = dic
            block.dicf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
            if block.same > 0:
                block.term = term
    
    def fill_term(self):
        term = ''
        ''' This is just to get a non-empty value of 'term' if some
            other types besides 'phrase' and 'term' follow them in the
            end.
        '''
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                term = self.blocks[i].text
                break
            i -= 1
        i = len(self.blocks) - 1
        while i >= 0:
            if self.blocks[i].type_ in ('term','phrase'):
                term = self.blocks[i].text
            if not self.blocks[i].same > 0:
                self.blocks[i].term = term
            i -= 1
            
    def set_fixed_term(self):
        for block in self.blocks:
            if block.type_ in self.fixed:
                block.term = ''
                
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].dic \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                ''' #NOTE: We do not inherit SEMINO here since it's not
                    needed anymore.
                '''
                block = Block()
                block.type_ = 'speech'
                block.text = self.blocks[i].speech
                block.dic = self.blocks[i].dic
                block.dicf = self.blocks[i].dicf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                block.term = self.blocks[i].term
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
                block.term = self.blocks[i].term
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
                block.term = self.blocks[i].term
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
                    block.term = self.blocks[i].term
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
                       
    def set_selectables(self):
        # block.no is set only after creating DB
        for block in self.blocks:
            if block.type_ in ('term','phrase','transc','phdic') \
            and block.text:
                block.select = 1
            else:
                block.select = 0
    
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
