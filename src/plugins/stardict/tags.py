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
        self.fragm = ''
        self.fragms = []
        self.blocks = []
        self.block = ic.Block()
        self.tag = tag

    def set_dic(self):
        if pdic in self.fragm:
            self.block.type = 'subj'
    
    def run(self):
        self.split()
        self.fragms = [fragm for fragm in self.fragms if fragm.strip()]
        for self.fragm in self.fragms:
            if not self.fragm.startswith('<'):
                self.run_plain()
                continue
            if not self.is_useful():
                self.block.type = 'invalid'
                continue
            self.block.type = ''
            self.set_phrases()
            # Phrases and word forms have conflicting tags
            # We check 'type' to speed up
            if not self.block.type:
                self.set_wform()
            if not self.block.type:
                self.set_dic()
            if not self.block.type:
                self.set_term()
            if not self.block.type:
                self.set_speech()
            if not self.block.type:
                self.set_comment()
            if not self.block.type:
                self.set_transc()
        return self.blocks

    def is_useful(self):
        for tag in useful_tags:
            if tag in self.fragm:
                return True

    def run_plain(self):
        self.block.text = self.fragm
        ''' #NOTE: The analysis must be reset after '</', otherwise, plain text
            following it will be marked as 'invalid' rather than 'comment'.
        '''
        if self.block.type != 'invalid':
            self.blocks.append(copy.copy(self.block))

    def split(self):
        ''' Use custom split because we need to preserve delimeters (cannot
            distinguish tags and contents otherwise).
        '''
        tmp = ''
        for sym in self.tag:
            if sym == '>':
                tmp += sym
                self.fragms.append(tmp)
                tmp = ''
            elif sym == '<':
                if tmp:
                    self.fragms.append(tmp)
                tmp = sym
            else:
                tmp += sym
        if tmp:
            self.fragms.append(tmp)

    def set_comment(self):
        if self.fragm.startswith(pcom):
            self.block.type = 'comment'

    def set_wform(self):
        if pwf in self.fragm:
            self.block.type = 'wform'

    def set_phrases(self):
        if pph in self.fragm:
            self.block.type = 'phrase'

    def set_term(self):
        if ptm in self.fragm:
            self.block.type = 'term'

    def set_transc(self):
        if ptr in self.fragm:
            self.block.type = 'transc'

    def set_speech(self):
        if psp in self.fragm:
            self.block.type = 'speech'



class Tags:

    def __init__(self, text, Debug=False, maxrow=20, maxrows=1000):
        if not text:
            text = ''
        self.text = text
        self.abbr = {}
        self.blocks = []
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
        self.tags = []
    
    def set_tags(self):
        ''' Split the text by closing tags. To speed up, we remove closing tags
            right away.
        '''
        Ignore = False
        tmp = ''
        for i in range(len(self.text)):
            if self.text[i] == '<':
                if i < len(self.text) - 1 and self.text[i+1] == '/':
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

    def set_blocks(self):
        cellno = -1
        for tag in self.tags:
            analyze = AnalyzeTag(tag)
            blocks = analyze.run()
            if not blocks:
                continue
            cellno += 1
            blocks[0].cellno = cellno
            i = 1
            while i < len(blocks):
                blocks[i].cellno = cellno
                i += 1
            self.blocks += blocks

    def split_lines(self):
        tags = []
        for tag in self.tags:
            tag = tag.splitlines()
            tag = [item.strip() for item in tag if item.strip()]
            for i in range(len(tag)):
                if not '<' in tag[i] and not '>' in tag[i]:
                    tag[i] = f'<dtrn>{tag[i]}</dtrn>'
            tags += tag
        self.tags = tags
    
    def run(self):
        self.set_tags()
        self.split_lines()
        self.set_blocks()
        return self.blocks
