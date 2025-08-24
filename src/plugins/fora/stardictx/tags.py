#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy
import html
from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.localize import _
from skl_shared.table import Table

from instance import Block, Tag


''' Tag patterns:
    •  Full dictionary titles:
         define them by the .ifo file, set the tag manually
         <dic></dic>
    •  Any abbreviation (a short dictionary title, a comment, etc.)
         <abr></abr>
    •  Terms:
         (no tags at all, see "'cellist")
         <dtrn></dtrn>
    •  Comments:
         <co></co>
         <ex></ex>
         <kref></kref> ("See also" section items)
    •  Word forms:
         <k></k>
    •  Transcription:
        <tr></tr>
    •  Parts of speech:
         # XDXF tag meaning grammar information about the word <gr></gr>
    '''


class AnalyzeTag:

    def __init__(self, fragm):
        self.Success = True
        self.tag = Tag()
        self.cur_row = 0
        self.cur_cell = 0
        self.fragm = fragm
    
    def check(self):
        f = '[MClient] plugins.fora.stardictx.tags.AnalyzeTag.check'
        if not self.fragm:
            self.Success = False
            rep.empty(f)
    
    def _set_name(self):
        # Do this before setting a URL
        self.tag.name = self.tag.text
        if self.tag.name.startswith('<'):
            self.tag.name = self.tag.name[1:]
        pos = self.tag.name.find(' ')
        if pos > -1:
            self.tag.name = self.tag.name[:pos]
        self.tag.name = self.tag.name.lower()
    
    def _set_text(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags._set_text'
        self.tag.text = self.fragm
        if self.tag.text.startswith('</'):
            self.tag.text = self.tag.text[2:]
        elif self.tag.text.startswith('<'):
            self.tag.text = self.tag.text[1:]
        else:
            mes = _('Pattern "{}" is not a tag!').format(self.tag.text)
            Message(f, mes).show_warning()
        if self.tag.text.endswith('>'):
            self.tag.text = self.tag.text[:-1]
        else:
            mes = _('Pattern "{}" is not a tag!').format(self.tag.text)
            Message(f, mes).show_warning()

    def _is_tag(self):
        if self.fragm.startswith('<') and self.fragm.endswith('>'):
            return True
    
    def _is_term(self):
        return 'dtrn' in self.tag.text
    
    def _is_subj(self):
        return self.tag.name == 'dic'
    
    def _is_comment(self):
        return self.tag.name in ('co', 'ex', 'kref')
    
    def _is_wform(self):
        return self.tag.name == 'k'
    
    def _is_transc(self):
        return self.tag.name == 'tr'
    
    def _is_speech(self):
        return self.tag.text == 'gr'
    
    def _set_type(self):
        if self._is_term():
            self.tag.type = 'term'
        elif self._is_comment():
            self.tag.type = 'comment'
        elif self._is_subj():
            self.tag.type = 'subj'
        elif self._is_wform():
            self.tag.type = 'wform'
        elif self._is_speech():
            self.tag.type = 'speech'
        elif self._is_transc():
            self.tag.type = 'transc'
        else:
            self.tag.type = 'comment'
    
    def _set_close(self):
        if self.fragm.startswith('</'):
            self.tag.Close = True
    
    def set_attr(self):
        f = '[MClient] plugins.fora.stardictx.tags.AnalyzeTag.set_attr'
        if not self.Success:
            rep.cancel(f)
            return
        if self._is_tag():
            self._set_close()
            self._set_text()
            self._set_name()
            self._set_type()
        else:
            self.tag.type = 'text'
            self.tag.text = self.fragm
    
    def run(self):
        self.check()
        self.set_attr()
        return self.tag



class Tags:
    
    def __init__(self, text):
        self.Success = True
        self.abbr = {}
        self.blocks = []
        self.fragms = []
        self.tags = []
        self.open = []
        self.code = text
    
    def _is_trash(self, tag):
        for subtag in tag.inherent:
            if subtag.type == 'trash':
                return True
    
    def _close(self, name):
        i = len(self.open) - 1
        while i >= 0:
            if self.open[i].name == name:
                del self.open[i]
                return True
            i -= 1
    
    def set_inherent(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.set_inherent'
        if not self.Success:
            rep.cancel(f)
            return
        for tag in self.tags:
            if tag.Close:
                self._close(tag.name)
            elif tag.type == 'text':
                tag.inherent = list(self.open)
            elif tag.type:
                self.open.append(tag)
    
    def set_nos(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.set_nos'
        if not self.Success:
            rep.cancel(f)
            return
        curcell = -1
        for tag in self.tags:
            if not tag.Close:
                if tag.name in ('dic', 'dtrn', 'k', 'tr'):
                    curcell += 1
            tag.cellno = curcell
    
    def _debug_blocks(self):
        nos = [i + 1 for i in range(len(self.blocks))]
        types = [block.type for block in self.blocks]
        texts = [f'"{block.text}"' for block in self.blocks]
        urls = [f'"{block.url}"' for block in self.blocks]
        subjs = [f'"{block.subj}"' for block in self.blocks]
        subjfs = [f'"{block.subjf}"' for block in self.blocks]
        cellnos = [block.cellno for block in self.blocks]
        iterable = [nos, types, texts, urls, subjs, subjfs, cellnos]
        headers = (_('#'), _('TYPE'), _('TEXT'), 'URL', 'SUBJ', 'SUBJF'
                  ,_('CELL #'))
        # 10'' monitor: 20 symbols per a column
        # 23'' monitor: 50 symbols per a column
        mes = Table(iterable = iterable, headers = headers, maxrow = 50
                   ,maxrows = 1000).run()
        return _('Blocks:') + '\n' + mes
    
    def set_blocks(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        tags = [tag for tag in self.tags if tag.type == 'text' \
               and not self._is_trash(tag)]
        for tag in tags:
            block = Block()
            for subtag in tag.inherent:
                if subtag.type == 'url':
                    block.url = subtag.url
                    block.subjf = subtag.subjf
                else:
                    block.type = subtag.type
            block.text = tag.text
            block.cellno = tag.cellno
            block.text = html.unescape(block.text)
            if block.type in ('subj', 'phsubj'):
                block.subj = block.text
            self.blocks.append(block)
    
    def assign(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.assign'
        if not self.Success:
            rep.cancel(f)
            return
        for fragm in self.fragms:
            self.tags.append(AnalyzeTag(fragm).run())
    
    def _debug_code(self):
        return _('Code:') + '\n' + '"{}"'.format(self.code)
    
    def _debug_fragms(self):
        mes = []
        for i in range(len(self.fragms)):
            mes.append(f'{i+1}: "{self.fragms[i]}"')
        return _('Fragments:') + '\n' + '\n'.join(mes)
    
    def _debug_tags(self):
        nos = [i + 1 for i in range(len(self.tags))]
        closes = [f'{tag.Close}' for tag in self.tags]
        names = [f'"{tag.name}"' for tag in self.tags]
        types = [f'"{tag.type}"' for tag in self.tags]
        texts = [f'"{tag.text}"' for tag in self.tags]
        urls = [f'"{tag.url}"' for tag in self.tags]
        subjfs = [f'"{tag.subjf}"' for tag in self.tags]
        cellnos = [f'{tag.cellno}' for tag in self.tags]
        inherent = []
        for tag in self.tags:
            subtags = []
            for subtag in tag.inherent:
                subtags.append(subtag.name)
            subtags = ', '.join(subtags)
            inherent.append(subtags)
        iterable = [nos, closes, names, types, texts, urls, subjfs, inherent
                   ,cellnos]
        headers = (_('#'), _('CLOSING'), _('NAME'), _('TYPE'), _('TEXT'), 'URL'
                  ,'DICF', _('OPEN'), _('CELL'))
        # 10'' monitor: 13 symbols per a column
        # 23'' monitor: 30 symbols per a column
        mes = Table(iterable = iterable, headers = headers, maxrow = 70
                   ,maxrows = 1000).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.debug'
        if not self.Success:
            rep.cancel(f)
            return ''
        '''
        mes = [self._debug_code(), self._debug_fragms(), self._debug_tags()
              ,self._debug_blocks()]
        '''
        mes = [self._debug_tags(), self._debug_blocks()]
        return '\n\n'.join(mes)
    
    def check(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            rep.empty(f)
    
    def split(self):
        f = '[MClient] plugins.fora.stardictx.tags.Tags.split'
        if not self.Success:
            rep.cancel(f)
            return
        fragm = ''
        for sym in list(self.code):
            if sym == '<':
                if fragm:
                    self.fragms.append(fragm)
                fragm = sym
            elif sym == '>':
                fragm += sym
                self.fragms.append(fragm)
                fragm = ''
            else:
                fragm += sym
        if fragm:
            self.fragms.append(fragm)
    
    def run(self):
        self.check()
        self.split()
        self.assign()
        self.set_inherent()
        self.set_nos()
        self.set_blocks()
        return self.blocks
