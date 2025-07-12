#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy
from skl_shared.localize import _
from skl_shared.table import Table

import instance as ic


''' Tag patterns:
    •  Dictionary titles:
         define them by the .ifo file, set the tag manually
         <dic></dic>
    •  Short dictionary titles:
         define them manually by the file name
         <abr></abr>
    •  Terms:
         (no tags at all, see "'cellist")
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
ptr = '<tr>'

useful_tags = [pdic, pcom, ptr, pwf, ptm, pph, psp]



class AnalyzeTag:

    def __init__(self, tag):
        self.block = ''
        self.blocks = []
        self.cur = ic.Block()
        self.elems = []
        self.tag = tag

    def set_dic(self):
        if pdic in self.block:
            self.cur.type = 'subj'
    
    def run(self):
        self.split()
        self.blocks = [block for block in self.blocks if block.strip()]
        for self.block in self.blocks:
            if not self.block.startswith('<'):
                self.run_plain()
                continue
            if not self.is_useful():
                self.cur.type = 'invalid'
                continue
            self.cur.type = ''
            self.set_phrases()
            # Phrases and word forms have conflicting tags
            # We check 'type' to speed up
            if not self.cur.type:
                self.set_wform()
            if not self.cur.type:
                self.set_dic()
            if not self.cur.type:
                self.set_term()
            if not self.cur.type:
                self.set_speech()
            if not self.cur.type:
                self.set_comment()
            if not self.cur.type:
                self.set_transc()

    def is_useful(self):
        for tag in useful_tags:
            if tag in self.block:
                return True

    def run_plain(self):
        self.cur.text = self.block
        ''' #NOTE: The analysis must be reset after '</', otherwise, plain text
            following it will be marked as 'invalid' rather than 'comment'.
        '''
        if self.cur.type != 'invalid':
            self.elems.append(copy.copy(self.cur))

    def split(self):
        ''' Use custom split because we need to preserve delimeters (cannot
            distinguish tags and contents otherwise).
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
            self.cur.type = 'comment'

    def set_wform(self):
        if pwf in self.block:
            self.cur.type = 'wform'

    def set_phrases(self):
        if pph in self.block:
            self.cur.type = 'phrase'

    def set_term(self):
        if ptm in self.block:
            self.cur.type = 'term'

    def set_transc(self):
        if ptr in self.block:
            self.cur.type = 'transc'

    def set_speech(self):
        if psp in self.block:
            self.cur.type = 'speech'



class Tags:

    def __init__(self, text, Debug=False, maxrow=20, maxrows=1000):
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
        ''' Split the text by closing tags. To speed up, we remove closing tags
            right away.
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
        mes = []
        for i in range(len(self.tags)):
            mes.append(f'{i}:{self.tags[i]}')
        mes.insert(0, f'{f}:')
        return '\n'.join(mes)

    def debug_blocks (self):
        f = '[MClient] plugins.stardict.tags.Tags.debug_blocks'
        headers = ('NO', 'CELLNO', 'TYPE', 'TEXT', 'URL')
        rows = []
        for i in range(len(self.blocks)):
            rows.append([i+1, self.blocks[i].cellno, self.blocks[i].type
                       ,self.blocks[i].text, self.blocks[i].url])
        mes = Table(headers=headers, iterable=rows, maxrow=self.maxrow
                   ,maxrows=self.maxrows, Transpose=True).run()
        return f + ':\n' + mes

    def debug(self):
        report = [self.debug_tags(), self.debug_blocks()]
        report = [item for item in report if item]
        return '\n\n'.join(report)

    def get_blocks(self):
        if not self.blocks:
            cellno = -1
            for tag in self.tags:
                analyze = AnalyzeTag(tag)
                analyze.run()
                lst = analyze.elems
                if not lst:
                    continue
                cellno += 1
                lst[0].cellno = cellno
                i = 1
                while i < len(lst):
                    lst[i].cellno = cellno
                    i += 1
                self.blocks += lst
        return self.blocks

    def run(self):
        self.get_tags()
        self.get_blocks()
        return self.blocks
