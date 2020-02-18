#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _

pdic = b'\x0f'

# Comments
pcom = b'\x06'

# Corrective comments
pcor = b''

# Terms
ptm1 = b'\x01'
ptm2 = b'\x02'


class AnalyzeTag:
    
    def __init__(self,tag):
        self.values()
        self._tag = tag
    
    def values(self):
        self._fragms = []
        self._blocks = []
    
    def split(self):
        pass
    
    def run(self):
        self.split()
        for fragm in self._fragms:
            self._blocks.append(Block())
            self._blocks[-1]._text = fragm
        self.set_types()
        return self._blocks
    
    def set_types(self):
        pass



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



class AnalyzeTag:

    def __init__(self,tag):
        self.values()
        self._tag = tag
    
    def values(self):
        self._fragms = []
        self._blocks = []

    def correction(self):
        pass
    
    def run(self):
        self.split()
        for fragm in self._fragms:
            self._blocks.append(Block())
            self._blocks[-1]._text = fragm
        self.set_types()
        return self._blocks

    def set_types(self):
        #TODO: elaborate
        for block in self._blocks:
            if block._type == 'comment':
                block._type = 'term'
    
    def split(self):
        pass
        #self._fragms.append(tmp)

    def comment(self):
        pass
        #self._block._type = 'comment'
    
    def dic(self):
        pass
        #self._block._type = 'dic'

    def wform(self):
        pass

    def phrases(self):
        pass

    def term(self):
        pass
        #self._block._type = 'term'

    def speech(self):
        pass
        #self._block._type = 'speech'



class Tags:

    def __init__ (self,chunk,Debug=False
                 ,Shorten=True,MaxRow=20
                 ,MaxRows=50
                 ):
        self.values()
        self.Debug   = Debug
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows

    def values(self):
        self._tags   = []
        self._blocks = []
        self._chunk  = b''
    
    def tags(self):
        pass
        return self._tags

    def debug_tags(self):
        f = '[MClient] plugins.multitranbin.tags.Tags.debug_tags'
        message = ''
        for i in range(len(self._tags)):
            message += '{}:{}\n'.format(i,self._tags[i])
        #sh.objs.mes(f,message,True).debug()
        words = sh.Words (text = message
                         ,Auto = 1
                         )
        words.sent_nos()
        sh.objs.txt().reset(words=words)
        sh.objs._txt.title(f)
        sh.objs._txt.insert(text=message)
        sh.objs._txt.show()

    def debug_blocks(self):
        f = '[MClient] plugins.multitranbin.tags.Tags.debug_blocks'
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
            #self.debug_tags()
            self.debug_blocks()
    
    def blocks(self):
        if not self._blocks:
            for tag in self._tags:
                self._blocks += AnalyzeTag(tag).run()
        return self._blocks

    def run(self):
        self.tags()
        self.blocks()
        self.debug()
        return self._blocks
