#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _


class Tag:
    
    def __init__(self):
        self.type = ''
        self.text = ''
        self.name = ''
        self.url = ''
        self.subjf = ''
        self.cellno = -1
        self.Close = False
        self.inherent = []



class Block:
    ''' Cannot be reimported in sources since we would need to load this module
        from different places.    
    '''
    def __init__(self):
        self.subj = ''
        self.subjf = ''
        self.text = ''
        self.url = ''
        ''' 'comment', 'correction', 'invalid', 'phcount', 'phrase', 'phsubj',
            'speech', 'subj', 'term', 'transc', 'user', 'wform'.
        '''
        self.type = 'comment'
        self.dic = ''
        self.source = ''
        # Preserve original order after sorting
        self.no = -1
        self.cellno = -1
        self.Delete = False
        self.speech = ''
        self.speechf = ''
        self.transc = ''
        self.wform = ''
        self.term = ''
        self.reset()
    
    def reset(self):
        self.Ignore = False
        self.Block = False
        self.rowno = -1
        self.colno = -1
        self.subjpr = -1
        self.speechpr = -1
        self.sourcepr = -1
        self.code = ''
        self.col1 = ''
        self.col2 = ''
        self.col3 = ''
        self.col4 = ''
        self.col5 = ''
        self.col6 = ''



class Subject:
    
    def __init__(self):
        self.subj = ''
        self.subjf = ''
        self.prior_index = -1
        self.subjpr = -1
        self.Block = False



class Article:
    
    def __init__(self):
        # Useful for debugging export
        self.pos = 0
        self.dic = ''
        self.code = ''
        self.search = ''
        self.format = ''



class Column:
    
    def __init__(self):
        self.no = 0
        self.width = 0
        self.type = ''



class Source:
    
    def __init__(self):
        self.title = ''
        self.status = _('not running')
        self.color = 'red'
        self.Online = False
        self.successful = 0
        self.failed = 0


def is_block_fixed(block):
    return block.type in ('source', 'dic', 'subj', 'wform', 'speech', 'transc'
                         ,'phsubj')