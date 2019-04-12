#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy
import shared    as sh
import sharedGUI as sg
import plugins.multitrancom.get

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')



''' Tag patterns:
    •  Abbreviations of dictionaries:
         <td class="subj" width="1"><a href="/m.exe?a=110&amp;l1=1&amp;l2=2&amp;s=computer&amp;sc=197">astronaut.</a>
         td class="subj"
    •  Terms:
         <td class="trans" width="100%"><a href="/m.exe?s=компьютер&amp;l1=2&amp;l2=1"> компьютер</a>
         td class="trans"
    •  Comments:
         <span style="color:gray">(прибора)</span>
         span style="color:gray"
    •  Users:
         (116 is for everyone)
         <a href="/m.exe?a=116&UserName=Буткова">Буткова</a>
         a href="/m.exe?a=116&UserName=
    •  Genders:
         <em>n</em>
         em
    •  Word forms + thesaurus:
         <td colspan="2" class="gray">&nbsp;(quantity) computer <em>n</em></td>
         td colspan="2" class="gray"
    •  Transcription:
         <td colspan="2" class="gray">&nbsp;computer <span style="color:gray">kəm'pju:tə</span> <em>n</em> <span style="color:gray">|</span>
         (same as word forms) ', ə and other marks
    •  Phrase dics (25 is the number of entries in the dic)
        <td class="phras"><a href="/m.exe?a=3&amp;sc=448&amp;s=computer&amp;l1=1&amp;l2=2">Chemical weapons</a></td><td class="phras_cnt">25</td>
        td class="phras"
    '''

# Tag patterns
tag_pattern_del = ['m.exe?a=40&'      # Log in, Вход
                  ,'m.exe?a=256'      # English, Русский
                  ,'m.exe?a=1&'       # Dictionary, Словари
                  ,'&fl=1'            # ⇄
                  ,'a href="#phrases' # phrases, фразы
                  ,'?fscreen=1'       # Full screen, Полный экран
                  ]

# Abbreviated dictionary titles
pdic = 'td class="subj"'

# URLs
purl1 = 'href="/m.exe?'
# Failsafe
purl2 = 'href="/M.exe?'
purl3 = 'href="'
purl4 = '">'

# Comments
pcom1 = 'span style="color:gray"'
pcom2 = '&UserName='

# Word Forms
pwf1 = '<td bgcolor='
pwf2 = '<a href="M.exe?a='     # Do not shorten
pwf3 = '<a href="m.exe?a='     # Do not shorten
pwf4 = '<td bgcolor="#DBDBDB"'
pwf5 = '&ifp='

# Parts of speech
psp1 = '<em>'

# Terms
ptm1 = 'M.exe?t'            # Both terms and word forms
ptm2 = 'm.exe?t'            # Both terms and word forms
ptm3 = '<a href="M.exe?&s='
ptm4 = '<a href="m.exe?&s='
ptm5 = '<a href="M.exe?s='
ptm6 = '<a href="m.exe?s='

# Terms in the 'Phrases' section
pph1 = '<a href="M.exe?a=3&&s='
pph2 = '<a href="m.exe?a=3&&s='
pph3 = '<a href="M.exe?a=3&s='
pph4 = '<a href="m.exe?a=3&s='


useful_tags = [pdic,purl1,purl2
              ,pcom1,pcom2,pwf4
              ,psp1
              ]

if hasattr(plugins.multitrancom.get,'PAIR_ROOT'):
    pair_root = plugins.multitrancom.get.PAIR_ROOT
else:
    pair_root = ''
    sh.objs.mes ('[MClient] plugins.multitrancom.tags.__main__'
                ,_('ERROR')
                ,_('An invalid plugin!')
                )



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

    def run(self):
        self.split()
        self._blocks = [block for block in self._blocks if block.strip()]
        for self._block in self._blocks:
            if self._block.startswith('<'):
                if self.useful() and not self.useless():
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
                    self.url()
                else:
                    self._cur._type = 'invalid'
            else:
                self.plain()

    def useless(self):
        for tag in tag_pattern_del:
            if tag in self._block:
                return True

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
        if pcom1 in self._block or pcom2 in self._block:
            self._cur._type = 'comment'

    def dic(self):
        f = '[MClient] plugins.multitrancom.tags.AnalyzeTag.dic'
        if self._block.startswith(pdic):
            tmp = self._block.replace(pdic,'',1)
            tmp = re.sub('".*','',tmp)
            if tmp == '' or tmp == ' ':
                sh.log.append (f,_('WARNING')
                              ,_('Wrong tag "%s"!') % tmp
                              )
            else:
                self._cur._type = 'dic'
                self._cur._text = tmp
                self._elems.append(copy.copy(self._cur))

    def wform(self):
        cond1 = pwf1 in self._block
        cond2 = pwf2 in self._block and not 'UserName' in self._block
        cond3 = pwf3 in self._block and not 'UserName' in self._block
        cond4 = pwf4 in self._block
        cond5 = pwf5 in self._block and ptm1 in self._block
        cond6 = pwf5 in self._block and ptm2 in self._block
        if cond1 or cond2 or cond3 or cond4 or cond5 or cond6:
            self._cur._type  = 'wform'

    def phrases(self):
        # Old algorithm: 'startswith'
        cond1 = pph1 in self._block
        cond2 = pph2 in self._block
        cond3 = pph3 in self._block
        cond4 = pph4 in self._block
        if cond1 or cond2 or cond3 or cond4:
            self._cur._type = 'phrase'

    def term(self):
        cond1 = ptm1 in self._block
        cond2 = ptm2 in self._block
        cond3 = ptm3 in self._block
        cond4 = ptm4 in self._block
        cond5 = ptm5 in self._block
        cond6 = ptm6 in self._block
        if cond1 or cond2 or cond3 or cond4 or cond5 or cond6:
            self._cur._type = 'term'

    def url(self):
        ''' Otherwise, 'self._block' will be returned when there is
            no match.
        '''
        if purl1 in self._block or purl2 in self._block:
            ind = self._block.find(purl3)
            if ind > 0:
                ind += len(purl1)
                self._cur._url = self._block[ind:]
            if self._cur._url.endswith(purl4):
                self._cur._url = self._cur._url.replace(purl4,'')
                ''' #note: adding a non-Multitran online source will
                    require code modification.
                '''
                self._cur._url = pair_root + self._cur._url
            else:
                self._cur._url = ''

    def speech(self):
        if psp1 in self._block:
            self._cur._type = 'speech'



class Tags:

    def __init__ (self,text,Debug=False
                 ,Shorten=True,MaxRow=20
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
        f = '[MClient] plugins.multitrancom.tags.Tags.debug_tags'
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

    def debug_blocks(self):
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
