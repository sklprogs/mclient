#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Tag:
    
    def __init__(self):
        self.type_ = ''
        self.text = ''
        self.name = ''
        self.url = ''
        self.dicf = ''
        self.cellno = -1
        self.Close = False
        self.inherent = []



class Block:

    def __init__(self):
        self.Ignore = False
        self.cellno = -1
        self.dic = ''
        self.dicf = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase', 'speech',
            'term', 'transc', 'wform'.
        '''
        self.type_ = 'comment'
        self.url = ''



class Cell:
    
    def __init__(self):
        self.code = ''
        self.text = ''
        self.url = ''
        self.no = -1
        self.blocks = []
        self.fixed_block = None
        self.Ignore = False
        self.subj = ''
        self.wform = ''
        self.transc = ''
        self.speech = ''
        self.priority = 500
