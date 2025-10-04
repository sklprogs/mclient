#!/usr/bin/python3
# -*- coding: UTF-8 -*-

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



class Cell:
    
    def __init__(self):
        self.fixed_block = None
        self.blocks = []
        self.no = -1
        self.rowno = -1
        self.colno = -1
        self.subjpr = -1
        self.speechpr = -1
        self.code = ''
        self.speech = ''
        self.source = _('Untitled source')
        self.dic = _('Untitled dictionary')
        self.subj = ''
        self.text = ''
        self.transc = ''
        self.url = ''
        self.wform = ''
        self.col1 = ''
        self.col2 = ''
        self.col3 = ''
        self.col4 = ''



class Block:
    ''' Cannot be reimported in plugins since we would need to load this module
        from different places.    
    '''
    def __init__(self):
        self.cellno = -1
        self.subj = ''
        self.subjf = ''
        self.text = ''
        self.url = ''
        ''' 'comment', 'correction', 'invalid', 'phcount', 'phrase', 'phsubj',
            'speech', 'subj', 'term', 'transc', 'wform'.
        '''
        self.type = 'comment'
        self.Fixed = False



class Subject:
    
    def __init__(self):
        self.subj = ''
        self.subjf = ''
        self.prior_index = -1
        self.subjpr = -1
        self.Block = False



class Article:
    
    def __init__(self):
        self.dic = ''
        self.code = ''
        self.search = ''
