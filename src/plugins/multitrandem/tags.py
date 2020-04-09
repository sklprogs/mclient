#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import skl_shared.shared as sh
from skl_shared.localize import _

ENCODING = 'windows-1251'

pdic = b'\x0f'

# Comments
pcom = b'\x06'

# Corrective comments
pcor = b''

# Terms
ptm1 = b'\x01'
ptm2 = b'\x02'


class Tags:
    #TODO: elaborate setting languages
    def __init__ (self,chunk,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50,lang1=1,lang2=2
                 ):
        self.values()
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        self.entry   = chunk
        self.lang1   = lang1
        self.lang2   = lang2
    
    def get_types(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.get_types'
        if self.Success:
            if len(self._tags) % 2 == 0:
                for i in range(len(self._tags)):
                    if i % 2 == 0:
                        self.types.append(self._tags[i])
                    else:
                        self.content.append(self._tags[i])
            else:
                mes = _('Wrong input data: "{}"').format(self._tags)
                sh.objs.mes(f,mes,True).warning()
    
    def set_types(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_types'
        if self.Success:
            for i in range(len(self.content)):
                self._blocks.append(Block())
                self._blocks[-1]._text = self.content[i]
                if self.types[i] == self.seplg1:
                    self._blocks[i]._type = 'term'
                    self._blocks[i]._lang = self.lang1
                elif self.types[i] == self.seplg2:
                    self._blocks[i]._type = 'term'
                    self._blocks[i]._lang = self.lang2
                elif self.types[i] == self.sepcom:
                    self._blocks[i]._type = 'comment'
                elif self.types[i] == self.sepdic:
                    self._blocks[i]._type = 'dic'
                else:
                    self._blocks[i]._type = 'invalid'
                    #TODO: convert to a string
                    mes = _('Unknown type "{}"!').format(self.types[i])
                    sh.objs.mes(f,mes,True).warning()    
        else:
            sh.com.cancel(f)
    
    def debug_blocks(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.debug_blocks'
        mes = _('Debug table:')
        sh.objs.mes(f,mes,True).info()
        headers = ['TYPE','TEXT']
        rows = []
        for block in self._blocks:
            rows.append ([block._type
                         ,block._text
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
    
    def debug_tags(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.debug_tags'
        message = ''
        for i in range(len(self._tags)):
            message += '{}:{}\n'.format(i,self._tags[i])
        sh.com.fast_debug(message)
    
    def decode(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.decode'
        if self.Success:
            i = 1
            while i < len(self._tags):
                if self._tags[i-1] in self.seps:
                    self._tags[i] = self._tags[i].decode (ENCODING
                                                         ,'replace'
                                                         )
                i += 1
        else:
            sh.com.cancel(f)
    
    def set_seps(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_seps'
        if self.Success:
            self.seps = [self.seplg1,self.seplg2
                         ,self.sepdic,self.sepcom
                         ]
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.split'
        if self.Success:
            tmp = b''
            for i in range(len(self.entry)):
                if self.entry[i:i+1] in self.seps:
                    if tmp:
                        self._tags.append(tmp)
                        tmp = b''
                    self._tags.append(self.entry[i:i+1])
                else:
                    tmp += self.entry[i:i+1]
            if tmp:
                self._tags.append(tmp)
        else:
            sh.com.cancel(f)
    
    def set_langs(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_langs'
        if self.Success:
            if self.lang1 and self.lang2:
                try:
                    self.seplg1 = struct.pack('<b',self.lang1)
                    self.seplg2 = struct.pack('<b',self.lang2)
                except:
                    self.Success = False
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).warning()
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.check'
        # Dictionary section is optional, so we do not check for it
        if self.entry and self.lang1 and self.lang2:
            if self.lang1 in self.entry \
            and self.lang2 in self.entry:
                return True
            else:
                mes = _('Wrong input data: "{}"!').format(self.entry)
                sh.objs.mes(f,mes).warning()
        else:
            self.Success = False
            sh.com.empty(f)
    
    def values(self):
        self.Success = True
        self.entry   = ''
        # The result of 'struct.pack('<b',15)'
        self.sepdic  = b'\x0f'
        self.sepcom  = b'\x06'
        self.lang1   = 0
        self.lang2   = 0
        self.seplg1  = b''
        self.seplg2  = b''
        self._blocks = []
        self._tags   = []
        self.seps    = []
        self.types   = []
        self.content = []
    
    def run(self):
        self.set_langs()
        self.check()
        self.set_seps()
        self.split()
        self.decode()
        self.get_types()
        self.set_types()
        return self._blocks



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
        self._same     = 0
        ''' '_select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self._select   = -1
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'transc', 'invalid'
        '''
        self._type     = ''
        self._text     = ''
        self._url      = ''
        self._urla     = ''
        self._dica     = ''
        self._dicaf    = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''
        self._terma    = ''
        self._priority = 0
        self._lang     = 0


if __name__ == '__main__':
    itags = Tags (chunk = b'\x01abasin\x02\xe0\xe1\xe0\xe7\xe8\xed\x0f37'
                 ,Debug = True
                 )
    itags.run()
    #itags.debug()
    for i in range(len(itags._blocks)):
        mes = '{}: {}: "{}"'.format (i,itags._blocks[i]._type
                                    ,itags._blocks[i]._text
                                    )
        print(mes)
