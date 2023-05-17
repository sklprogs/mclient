#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Tag:
    
    def __init__(self):
        self.type_ = ''
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
        self.subj = ''
        self.text = ''
        self.transc = ''
        self.url = ''
        self.wform = ''



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
        self.type_ = 'comment'
