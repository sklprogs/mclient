#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.table import Table

import instance as ic


CODING = 'windows-1251'
pdic = b'\x0f'
# Comments
pcom = b'\x06'
# Corrective comments
pcor = b''
# Wforms
ptm1 = b'\x01'
# Terms
ptm2 = b'\x02'


class Tags:
    #TODO: elaborate setting languages
    def __init__(self, chunk, cellno, Debug=False, maxrow=20, maxrows=50, lang1=1, lang2=2):
        self.set_values()
        self.Debug = Debug
        self.entry = chunk
        self.cellno = cellno
        self.lang1 = lang1
        self.lang2 = lang2
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def get_types(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.get_types'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.tags:
            rep.empty(f)
            return
        if len(self.tags) % 2 != 0:
            ''' #TODO: Number of tags was always even in small mt demos. We
                still have to figure out what does this first attribute do in
                'mt_big_demo.rar'.
            '''
            del self.tags[0]
        for i in range(len(self.tags)):
            if i % 2 == 0:
                self.types.append(self.tags[i])
            else:
                self.content.append(self.tags[i])
    
    def set_types(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_types'
        if not self.Success:
            rep.cancel(f)
            return
        for i in range(len(self.content)):
            self.blocks.append(ic.Block())
            self.blocks[-1].text = self.content[i]
            if self.types[i] == self.seplg1:
                self.blocks[i].type = 'wform'
                self.blocks[i].lang = self.lang1
            elif self.types[i] == self.seplg2:
                self.blocks[i].type = 'term'
                self.blocks[i].lang = self.lang2
            elif self.types[i] == self.sepcom:
                self.blocks[i].type = 'comment'
            elif self.types[i] == self.sepdic:
                self.blocks[i].type = 'subj'
            else:
                self.blocks[i].type = 'invalid'
                #TODO: convert to a string
                mes = _('Unknown type "{}"!').format(self.types[i])
                Message(f, mes).show_warning()
    
    def debug_blocks(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.debug_blocks'
        headers = ('NO', 'TYPE', 'TEXT')
        rows = []
        for i in range(len(self.blocks)):
            rows.append([i+1, self.blocks[i].type, self.blocks[i].text])
        mes = Table(headers=headers, iterable=rows, maxrow=self.maxrow
                   ,maxrows=self.maxrows, Transpose=True).run()
        return f'{f}:\n{mes}'
    
    def debug(self):
        report = [self.debug_tags(), self.debug_blocks()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def debug_tags(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.debug_tags'
        mes = []
        for i in range(len(self.tags)):
            mes.append(f'{i}:{self.tags[i]}')
        mes = '\n'.join(mes)
        return f'{f}:\n{mes}'
    
    def decode(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.decode'
        if not self.Success:
            rep.cancel(f)
            return
        i = 1
        while i < len(self.tags):
            if self.tags[i-1] in self.seps:
                self.tags[i] = self.tags[i].decode(CODING, 'replace')
            i += 1
    
    def set_seps(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_seps'
        if not self.Success:
            rep.cancel(f)
            return
        self.seps = [self.seplg1, self.seplg2, self.sepdic, self.sepcom]
    
    def split(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.split'
        if not self.Success:
            rep.cancel(f)
            return
        tmp = b''
        for i in range(len(self.entry)):
            if self.entry[i:i+1] in self.seps:
                if tmp:
                    self.tags.append(tmp)
                    tmp = b''
                self.tags.append(self.entry[i:i+1])
            else:
                tmp += self.entry[i:i+1]
        if tmp:
            self.tags.append(tmp)
    
    def set_langs(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_langs'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.lang1 or not self.lang2:
            self.Success = False
            rep.empty(f)
            return
        try:
            self.seplg1 = struct.pack('<b', self.lang1)
            self.seplg2 = struct.pack('<b', self.lang2)
        except:
            self.Success = False
            mes = _('Wrong input data!')
            Message(f, mes, True).show_warning()
    
    def check(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.check'
        # Dictionary section is optional, so we do not check for it
        if not self.entry or not self.lang1 or not self.lang2:
            self.Success = False
            rep.empty(f)
            return
        return True
    
    def set_values(self):
        self.blocks = []
        self.content = []
        self.entry = ''
        self.lang1 = 0
        self.lang2 = 0
        self.seplg1 = b''
        self.seplg2 = b''
        # The result of 'struct.pack('<b', 15)'
        self.sepdic = b'\x0f'
        self.sepcom = b'\x06'
        self.seps = []
        self.Success = True
        self.tags = []
        self.types = []
    
    def set_cellnos(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_cellnos'
        if not self.Success:
            rep.cancel(f)
            return
        for block in self.blocks:
            block.cellno = self.cellno
    
    def run(self):
        self.set_langs()
        self.check()
        self.set_seps()
        self.split()
        self.decode()
        self.get_types()
        self.set_types()
        self.set_cellnos()
        return self.blocks
