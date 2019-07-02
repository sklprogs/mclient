#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


''' Tag patterns:
    •  Dictionary titles:
         define them by the .ifo file, set the tag manually
    •  Abbreviations of dictionaries:
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
        self._block    = -1
        self.i         = -1
        self.j         = -1
        self._first    = -1
        self._last     = -1
        self._no       = -1
        # Applies to non-blocked cells only
        self._cell_no  = -1
        self._same     = -1
        ''' '_select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self._select   = -1
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'invalid'
        '''
        self._type     = 'comment'
        self._text     = ''
        self._url      = ''
        self._urla     = ''
        self._dica     = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''
        self._terma    = ''
        self._priority = 0



class AnalyzeTag:

    def __init__(self,tag):
        self._tag    = tag
        self._cur    = Block()
        self._blocks = []
        self._elems  = []
        self._block  = ''

    def dic(self):
        f = '[MClient] plugins.stardict.tags.AnalyzeTag.dic'
        if pdic in self._block:
            self._cur._type  = 'dic'
    
    def run(self):
        self.split()
        self._blocks = [block for block in self._blocks if block.strip()]
        for self._block in self._blocks:
            if self._block.startswith('<'):
                if self.useful():
                    self._cur._type = ''
                    self.phrases()
                    # Phrases and word forms have conflicting tags
                    # We check '_type' to speed up
                    if not self._cur._type:
                        self.wform()
                    if not self._cur._type:
                        self.dic()
                    if not self._cur._type:
                        self.term()
                    if not self._cur._type:
                        self.speech()
                    if not self._cur._type:
                        self.comment()
                    if not self._cur._type:
                        self.transc()
                else:
                    self._cur._type = 'invalid'
            else:
                self.plain()

    def useful(self):
        for tag in useful_tags:
            if tag in self._block:
                return True

    def plain(self):
        self._cur._text = self._block
        ''' #note: The analysis must be reset after '</', otherwise,
            plain text following it will be marked as 'invalid' rather
            than 'comment'.
        '''
        if self._cur._type != 'invalid':
            self._elems.append(copy.copy(self._cur))

    def split(self):
        ''' Use custom split because we need to preserve delimeters
            (cannot distinguish tags and contents otherwise).
        '''
        tmp = ''
        for sym in self._tag:
            if sym == '>':
                tmp += sym
                self._blocks.append(tmp)
                tmp = ''
            elif sym == '<':
                if tmp:
                    self._blocks.append(tmp)
                tmp = sym
            else:
                tmp += sym
        if tmp:
            self._blocks.append(tmp)

    def comment(self):
        if self._block.startswith(pcom):
            self._cur._type = 'comment'

    def wform(self):
        if pwf in self._block:
            self._cur._type  = 'wform'

    def phrases(self):
        if pph in self._block:
            self._cur._type = 'phrase'

    def term(self):
        if ptm in self._block:
            self._cur._type = 'term'

    # Transcription
    def transc(self):
        if ptr1 in self._block:
            _type = 'transc'
            _text = self._block.replace(ptr1,'',1).replace(ptr2,'',1)
            # Will be empty for non-Stardict sources
            if _text:
                self._cur._type, self._cur._text = _type, _text
                self._elems.append(copy.copy(self._cur))

    def speech(self):
        if psp in self._block:
            self._cur._type = 'speech'



class Tags:

    def __init__ (self,text,Debug=False
                 ,Shorten=1,MaxRow=20
                 ,MaxRows=20
                 ):
        self._tags   = []
        self._blocks = []
        if text:
            self._text = list(text)
        else:
            self._text = ''
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows

    def tags(self):
        ''' Split the text by closing tags. To speed up, we remove
            closing tags right away.
        '''
        if not self._tags:
            Ignore = False
            tmp = ''
            for i in range(len(self._text)):
                if self._text[i] == '<':
                    if i < len(self._text) - 1 \
                    and self._text[i+1] == '/':
                        Ignore = True
                        if tmp:
                            self._tags.append(tmp)
                            tmp = ''
                    else:
                        tmp += self._text[i]
                elif self._text[i] == '>':
                    if Ignore:
                        Ignore = False
                    else:
                        tmp += self._text[i]
                elif not Ignore:
                    tmp += self._text[i]
            # Should be needed only for broken tags
            if tmp:
                self._tags.append(tmp)
        return self._tags

    def debug_tags(self):
        f = '[MClient] plugins.stardict.tags.Tags.debug_tags'
        import sharedGUI as sg
        message = ''
        for i in range(len(self._tags)):
            message += '%d:%s\n' % (i,self._tags[i])
        '''
        sh.objs.mes (f,_('INFO')
                    ,message
                    )
        '''
        words = sh.Words (text = message
                         ,Auto = 1
                         )
        words.sent_nos()
        sg.objs.txt(words=words).reset_data()
        sg.objs._txt.title(f)
        sg.objs._txt.insert(text=message)
        sg.objs._txt.show()

    def debug_blocks (self):
        print('\nTags.debug_blocks (Non-DB blocks):')
        headers = ['TYPE'
                  ,'TEXT'
                  ,'URL'
                  ,'SAMECELL'
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._type
                         ,block._text
                         ,block._url
                         ,block._same
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = self.Shorten
                 ,MaxRow  = self.MaxRow
                 ,MaxRows = self.MaxRows
                 ).print()

    def debug(self):
        if self.Debug:
            self.debug_tags()
            self.debug_blocks()

    def blocks(self):
        if not self._blocks:
            for tag in self._tags:
                analyze = AnalyzeTag(tag)
                analyze.run()
                lst = analyze._elems
                for i in range(len(lst)):
                    if i > 0:
                        lst[i]._same = 1
                    else:
                        lst[i]._same = 0
                self._blocks += lst
        return self._blocks

    def run(self):
        self.tags()
        self.blocks()
        self.debug()
        return self._blocks
