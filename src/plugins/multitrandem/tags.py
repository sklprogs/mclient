#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import skl_shared.shared as sh
from skl_shared.localize import _

CODING = 'windows-1251'

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
        self.set_values()
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
            if len(self.tags) % 2 == 0:
                for i in range(len(self.tags)):
                    if i % 2 == 0:
                        self.types.append(self.tags[i])
                    else:
                        self.content.append(self.tags[i])
            else:
                mes = _('Wrong input data: "{}"').format(self.tags)
                sh.objs.get_mes(f,mes,True).show_warning()
    
    def set_types(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.set_types'
        if self.Success:
            for i in range(len(self.content)):
                self.blocks.append(Block())
                self.blocks[-1].text = self.content[i]
                if self.types[i] == self.seplg1:
                    self.blocks[i].type_ = 'term'
                    self.blocks[i].lang = self.lang1
                elif self.types[i] == self.seplg2:
                    self.blocks[i].type_ = 'term'
                    self.blocks[i].lang = self.lang2
                elif self.types[i] == self.sepcom:
                    self.blocks[i].type_ = 'comment'
                elif self.types[i] == self.sepdic:
                    self.blocks[i].type_ = 'dic'
                else:
                    self.blocks[i].type_ = 'invalid'
                    #TODO: convert to a string
                    mes = _('Unknown type "{}"!').format(self.types[i])
                    sh.objs.get_mes(f,mes,True).show_warning()    
        else:
            sh.com.cancel(f)
    
    def debug_blocks(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.debug_blocks'
        mes = _('Debug table:')
        sh.objs.get_mes(f,mes,True).show_info()
        headers = ['TYPE','TEXT']
        rows = []
        for block in self.blocks:
            rows.append ([block.type_
                         ,block.text
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
        for i in range(len(self.tags)):
            message += '{}:{}\n'.format(i,self.tags[i])
        sh.com.run_fast_debug(message)
    
    def decode(self):
        f = '[MClient] plugins.multitrandem.tags.Tags.decode'
        if self.Success:
            i = 1
            while i < len(self.tags):
                if self.tags[i-1] in self.seps:
                    self.tags[i] = self.tags[i].decode (CODING
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
                        self.tags.append(tmp)
                        tmp = b''
                    self.tags.append(self.entry[i:i+1])
                else:
                    tmp += self.entry[i:i+1]
            if tmp:
                self.tags.append(tmp)
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
                    sh.objs.get_mes(f,mes).show_warning()
            else:
                self.Success = False
                sh.com.rep_empty(f)
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
                sh.objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.Success = True
        self.entry   = ''
        # The result of 'struct.pack('<b',15)'
        self.sepdic  = b'\x0f'
        self.sepcom  = b'\x06'
        self.lang1   = 0
        self.lang2   = 0
        self.seplg1  = b''
        self.seplg2  = b''
        self.blocks  = []
        self.tags    = []
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
        return self.blocks



class Block:

    def __init__(self):
        self.block = -1
        self.i     = -1
        self.j     = -1
        self.first = -1
        self.last  = -1
        self.no    = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.same   = 0
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'transc', 'invalid'
        '''
        self.type_    = ''
        self.text     = ''
        self.url      = ''
        self.urla     = ''
        self.dica     = ''
        self.dicaf    = ''
        self.wforma   = ''
        self.speecha  = ''
        self.transca  = ''
        self.terma    = ''
        self.priority = 0
        self.lang     = 0


if __name__ == '__main__':
    itags = Tags (chunk = b'\x01abasin\x02\xe0\xe1\xe0\xe7\xe8\xed\x0f37'
                 ,Debug = True
                 )
    itags.run()
    #itags.debug()
    for i in range(len(itags.blocks)):
        mes = '{}: {}: "{}"'.format (i,itags.blocks[i].type_
                                    ,itags.blocks[i].text
                                    )
        print(mes)
