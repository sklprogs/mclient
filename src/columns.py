#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message

from config import CONFIG
from articles import ARTICLES
from instance import Column


class Types:
    
    def _get(self, type_):
        f = '[MClient] columns.Types._get'
        if type_ == _('Sources'):
            return 'source'
        elif type_ == _('Dictionaries'):
            return 'dic'
        elif type_ == _('Subjects'):
            return 'subj'
        elif type_ == _('Word forms'):
            return 'wform'
        elif type_ == _('Parts of speech'):
            return 'speech'
        elif type_ == _('Transcription'):
            return 'transc'
        elif type_ == _('Do not set'):
            pass
        else:
            mes = _('Wrong input data: "{}"!').format(type_)
            Message(f, mes, True).show_error()
        return ''
    
    def get(self):
        f = '[MClient] columns.Types.get'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        types = [CONFIG.new['columns']['1']['type']
                ,CONFIG.new['columns']['2']['type']
                ,CONFIG.new['columns']['3']['type']
                ,CONFIG.new['columns']['4']['type']
                ,CONFIG.new['columns']['5']['type']
                ,CONFIG.new['columns']['6']['type']]
        for i in range(len(types)):
            types[i] = self._get(types[i])
        mes = ', '.join(types)
        Message(f, mes).show_debug()
        return types
    
    def run(self):
        return self.get()



class Width:
    ''' Adjust fixed columns to have a constant width. A fixed value in pixels
        rather than percentage should be used to adjust columns since we cannot
        say if gaps between columns are too large without calculating a text
        width first.
    '''
    def __init__(self):
        self.reset()
    
    def set_width(self):
        f = '[MClient] columns.Width.set_width'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['rows']['height']:
            rep.lazy(f)
            return
        for column in self.columns:
            if column.Fixed:
                column.width = CONFIG.new['columns']['fixed']['width']
            else:
                column.width = CONFIG.new['columns']['terms']['width']
            '''
            if objs.get_blocksdb().is_col_empty(column.no):
                column.width = self.min_width
            elif column.Fixed:
                column.width = CONFIG.new['columns']['fixed']['width']
            else:
                column.width = CONFIG.new['columns']['terms']['width']
            '''
    
    def reset(self):
        # This approach includes percentage only
        self.fixed_num = 0
        self.term_num = 0
        self.min_width = 1
        self.columns = []
    
    def run(self):
        self.set_fixed_num()
        self.set_term_num()
        self.set_columns()
        self.set_width()
    
    def set_fixed_num(self):
        f = '[MClient] columns.Width.set_fixed_num'
        self.fixed_num = 6
        mes = _('Number of fixed columns: {}').format(self.fixed_num)
        Message(f, mes).show_debug()
    
    def get_col_num(self):
        ''' A subject from the 'Phrases' section usually has an 'original +
            translation' structure, so we need to switch off sorting terms and
            ensure that the number of columns is divisible by 2.
        '''
        f = '[MClient] columns.Width.get_col_num'
        if not CONFIG.Success:
            rep.cancel(f)
            return 2
        if not ARTICLES.is_parallel() or CONFIG.new['columns']['num'] % 2 == 0:
            return CONFIG.new['columns']['num']
        if CONFIG.new['columns']['num'] > 2:
            return CONFIG.new['columns']['num'] - 1
        return 2
    
    def set_term_num(self):
        f = '[MClient] columns.Width.set_term_num'
        self.term_num = self.get_col_num()
        mes = _('Number of term columns: {}').format(self.term_num)
        Message(f, mes).show_debug()
    
    def set_columns(self):
        col_nos = self.fixed_num + self.term_num
        for i in range(self.fixed_num):
            column = Column()
            column.no = i
            column.Fixed = True
            self.columns.append(column)
        i = self.fixed_num
        while i < col_nos:
            column = Column()
            column.no = i
            self.columns.append(column)
            i += 1


COL_WIDTH = Width()
COL_WIDTH.run()
