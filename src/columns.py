#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message

from config import CONFIG
from articles import ARTICLES
from instance import Column as iColumn


class Column(iColumn):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixed_num = 6
    
    def set_type(self):
        f = '[MClient] columns.Column.set_type'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.type = CONFIG.new['columns'][str(self.no+1)]['type']
    
    def set_short(self):
        f = '[MClient] columns.Column.set_short'
        if self.type == _('Sources'):
            self.short = 'source'
        elif self.type == _('Dictionaries'):
            self.short = 'dic'
        elif self.type == _('Subjects'):
            self.short = 'subj'
        elif self.type == _('Word forms'):
            self.short = 'wform'
        elif self.type == _('Parts of speech'):
            self.short = 'speech'
        elif self.type == _('Transcriptions'):
            self.short = 'transc'
        elif self.type == _('Do not set'):
            pass
        else:
            mes = _('Wrong input data: "{}"!').format(self.type)
            Message(f, mes, True).show_error()
    
    def _set_fixed_width(self):
        try:
            self.width = CONFIG.new['columns']['by_type'][self.short]['width']
        except KeyError:
            pass
    
    def set_width(self):
        f = '[MClient] columns.Column.set_width'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        if not CONFIG.new['rows']['height']:
            rep.lazy(f)
            return
        if self.no < self.fixed_num:
            self._set_fixed_width()
        else:
            self.width = CONFIG.new['columns']['terms']['width']
    
    def add(self, no):
        f = '[MClient] columns.Column.add'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.no = no
        if self.no < self.fixed_num:
            self.set_type()
            self.set_short()
        self.set_width()



class Columns:
    ''' Adjust fixed columns to have a constant width. A fixed value in pixels
        rather than percentage should be used to adjust columns since we cannot
        say if gaps between columns are too large without calculating a text
        width first.
    '''
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.term_num = 0
        self.fixed_num = 6
        self.min_width = 1
        self.columns = []
    
    def run(self):
        self.set_term_num()
        self.set_columns()
    
    def get_col_num(self):
        ''' A subject from the 'Phrases' section usually has an 'original +
            translation' structure, so we need to switch off sorting terms and
            ensure that the number of columns is divisible by 2.
        '''
        f = '[MClient] columns.Columns.get_col_num'
        if not CONFIG.Success:
            rep.cancel(f)
            return 2
        if not ARTICLES.is_parallel() or CONFIG.new['columns']['num'] % 2 == 0:
            return CONFIG.new['columns']['num']
        if CONFIG.new['columns']['num'] > 2:
            return CONFIG.new['columns']['num'] - 1
        return 2
    
    def set_term_num(self):
        f = '[MClient] columns.Columns.set_term_num'
        self.term_num = self.get_col_num()
        mes = _('Number of term columns: {}').format(self.term_num)
        Message(f, mes).show_debug()
    
    def set_columns(self):
        f = '[MClient] columns.Columns.set_columns'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        for i in range(self.fixed_num + self.term_num):
            column = Column()
            column.add(i)
            self.columns.append(column)
    
    def get_fixed_short(self):
        f = '[MClient] columns.Columns.get_fixed_short'
        if not CONFIG.Success:
            rep.cancel(f)
            return []
        return [column.short for column in self.columns \
               if column.no < self.fixed_num]
    
    def get_width(self, colno):
        f = '[MClient] columns.Columns.get_width'
        if not CONFIG.Success:
            rep.cancel(f)
            return 0
        try:
            return self.columns[colno].width
        except IndexError:
            rep.wrong_input(f, colno)
            return 0


COL_WIDTH = Columns()
COL_WIDTH.run()
