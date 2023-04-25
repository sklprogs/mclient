#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Cell:
    
    def __init__(self):
        self.code = ''
        self.text = ''
        self.url = ''
        self.no = -1
        self.rowno = -1
        self.colno = -1
        self.blocks = []
        self.fixed_block = None
        self.subj = ''
        self.wform = ''
        self.transc = ''
        self.speech = ''
        self.subjpr = 0
        self.speechpr = -1



class Block:
    ''' Cannot be reimported in plugins since we would need to load this module
        from different places.    
    '''
    def __init__(self):
        self.cellno = -1
        self.subj = ''
        self.subjf = ''
        self.text = ''
        ''' 'comment', 'correction', 'invalid', 'phcount', 'phrase', 'phsubj',
            'speech', 'subj', 'term', 'transc', 'wform'.
        '''
        self.type_ = 'comment'
        self.url = ''
        self.family = 'Serif'
        self.color = 'black'
        self.size = 12
        self.Bold = False
        self.Italic = False
