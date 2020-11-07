#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy
import skl_shared.shared as sh
from skl_shared.localize import _


''' Tag patterns:
    •  Dictionary titles:
         define them by the .ifo file, set the tag manually
    •  Short dictionary titles:
         define them manually by the file name
    •  Terms:
         <dtrn></dtrn>
         <kref></kref> (in phrases)
    •  Comments:
         <co></co>
    •  Word forms:
         <k></k>
    •  Transcription:
        <tr></tr>
    •  Parts of speech:
         # A XDXF tag meaning grammar information about the word
         <gr></gr>
    '''

# Full dictionary titles
pdic = '<dic>'

# Comments
pcom = '<co>'

# Word Forms
pwf = '<k>'

# Parts of speech
psp = '<gr>'

# Terms
ptm = '<dtrn>'

# Terms in the 'Phrases' section
pph = '<kref>'

# Transcription
ptr1 = '<tr>'
ptr2 = '</tr>'

useful_tags = [pdic,pcom,ptr1,pwf,ptm,pph,psp]



class Block:

    def __init__(self):
        self.block = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.dic = ''
        self.dicf = ''
        self.dprior = 0
        self.first = -1
        self.i = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.term = ''
        self.text = ''
        self.transc = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'wform'
        '''
        self.type_ = 'comment'
        self.url = ''
        self.urla = ''
        self.wform = ''



class AnalyzeTag:

    def __init__(self,tag):
        self.block = ''
        self.blocks = []
        self.cur = Block()
        self.elems = []
        self.tag = tag

    def set_dic(self):
        f = '[MClient] plugins.stardict.tags.AnalyzeTag.set_dic'
        if pdic in self.block:
            self.cur.type_ = 'dic'
    
    def run(self):
        self.split()
        self.blocks = [block for block in self.blocks if block.strip()]
        for self.block in self.blocks:
            if self.block.startswith('<'):
                if self.is_useful():
                    self.cur.type_ = ''
                    self.set_phrases()
                    # Phrases and word forms have conflicting tags
                    # We check 'type_' to speed up
                    if not self.cur.type_:
                        self.set_wform()
                    if not self.cur.type_:
                        self.set_dic()
                    if not self.cur.type_:
                        self.set_term()
                    if not self.cur.type_:
                        self.set_speech()
                    if not self.cur.type_:
                        self.set_comment()
                    if not self.cur.type_:
                        self.set_transc()
                else:
                    self.cur.type_ = 'invalid'
            else:
                self.run_plain()

    def is_useful(self):
        for tag in useful_tags:
            if tag in self.block:
                return True

    def run_plain(self):
        self.cur.text = self.block
        ''' #NOTE: The analysis must be reset after '</', otherwise,
            plain text following it will be marked as 'invalid' rather
            than 'comment'.
        '''
        if self.cur.type_ != 'invalid':
            self.elems.append(copy.copy(self.cur))

    def split(self):
        ''' Use custom split because we need to preserve delimeters
            (cannot distinguish tags and contents otherwise).
        '''
        tmp = ''
        for sym in self.tag:
            if sym == '>':
                tmp += sym
                self.blocks.append(tmp)
                tmp = ''
            elif sym == '<':
                if tmp:
                    self.blocks.append(tmp)
                tmp = sym
            else:
                tmp += sym
        if tmp:
            self.blocks.append(tmp)

    def set_comment(self):
        if self.block.startswith(pcom):
            self.cur.type_ = 'comment'

    def set_wform(self):
        if pwf in self.block:
            self.cur.type_ = 'wform'

    def set_phrases(self):
        if pph in self.block:
            self.cur.type_ = 'phrase'

    def set_term(self):
        if ptm in self.block:
            self.cur.type_ = 'term'

    # Transcription
    def set_transc(self):
        if ptr1 in self.block:
            type_ = 'transc'
            text = self.block.replace(ptr1,'',1).replace(ptr2,'',1)
            # Will be empty for non-Stardict sources
            if text:
                self.cur.type_, self.cur.text = type_, text
                self.elems.append(copy.copy(self.cur))

    def set_speech(self):
        if psp in self.block:
            self.cur.type_ = 'speech'



class Tags:

    def __init__ (self,text,Debug=False
                 ,maxrow=20,maxrows=1000
                 ):
        if text:
            self.text = list(text)
        else:
            self.text = ''
        self.abbr = {}
        self.blocks = []
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
        self.tags = []

    def get_tags(self):
        ''' Split the text by closing tags. To speed up, we remove
            closing tags right away.
        '''
        if not self.tags:
            Ignore = False
            tmp = ''
            for i in range(len(self.text)):
                if self.text[i] == '<':
                    if i < len(self.text) - 1 \
                    and self.text[i+1] == '/':
                        Ignore = True
                        if tmp:
                            self.tags.append(tmp)
                            tmp = ''
                    else:
                        tmp += self.text[i]
                elif self.text[i] == '>':
                    if Ignore:
                        Ignore = False
                    else:
                        tmp += self.text[i]
                elif not Ignore:
                    tmp += self.text[i]
            # Should be needed only for broken tags
            if tmp:
                self.tags.append(tmp)
        return self.tags

    def debug_tags(self):
        f = '[MClient] plugins.stardict.tags.Tags.debug_tags'
        message = ''
        for i in range(len(self.tags)):
            message += '%d:%s\n' % (i,self.tags[i])
        sh.com.run_fast_debug(f,message)

    def debug_blocks (self):
        f = '[MClient] plugins.stardict.tags.Tags.debug_blocks'
        headers = ('NO','TYPE','TEXT','URL','SAMECELL')
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].type_
                         ,self.blocks[i].text
                         ,self.blocks[i].url
                         ,self.blocks[i].same
                         ]
                        )
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = self.maxrow
                           ,maxrows = self.maxrows
                           ,Transpose = True
                           ).run()
        mes = _('Non-DB blocks:') + '\n\n' + mes
        sh.com.run_fast_debug(f,mes)

    def debug(self):
        if self.Debug:
            self.debug_tags()
            self.debug_blocks()

    def get_blocks(self):
        if not self.blocks:
            for tag in self.tags:
                analyze = AnalyzeTag(tag)
                analyze.run()
                lst = analyze.elems
                for i in range(len(lst)):
                    if i > 0:
                        lst[i].same = 1
                    else:
                        lst[i].same = 0
                self.blocks += lst
        return self.blocks

    def run(self):
        self.get_tags()
        self.get_blocks()
        self.debug()
        return self.blocks
