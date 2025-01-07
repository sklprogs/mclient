#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from config import CONFIG
from manager import PLUGINS


class Articles:
    
    def __init__(self):
        self.reset()
    
    def set_values(self):
        self.id = -1
        self.articles = {'ids' : {}}
    
    def reset(self):
        self.set_values()
    
    def get_blocked(self):
        f = '[MClient] articles.Articles.get_blocked'
        try:
            return self.articles['ids'][self.id]['blocked']
        except KeyError:
            rep.wrong_input(f)
        return []
    
    def get_prioritized(self):
        f = '[MClient] articles.Articles.get_prioritized'
        try:
            return self.articles['ids'][self.id]['prioritized']
        except KeyError:
            rep.wrong_input(f)
        return []
    
    def get_subjf(self):
        f = '[MClient] articles.Articles.get_subjf'
        try:
            return self.articles['ids'][self.id]['subjf']
        except KeyError:
            rep.wrong_input(f)
    
    def get_fixed_urls(self):
        f = '[MClient] articles.Articles.get_fixed_urls'
        try:
            return self.articles['ids'][self.id]['fixed_urls']
        except KeyError:
            rep.wrong_input(f)
        return {}
    
    def is_last(self):
        return self.id == self.get_max_id()
    
    def get_max_id(self):
        f = '[MClient] articles.Articles.get_max_id'
        try:
            # Do not use 'max' on an empty sequence
            return len(self.articles['ids']) - 1
        except KeyError:
            rep.wrong_input(f)
        return -1
    
    def set_table(self, table):
        f = '[MClient] articles.Articles.set_table'
        if not table:
            rep.empty(f)
            # Keep old article
            return
        try:
            self.articles['ids'][self.id]['table'] = table
        except KeyError:
            rep.wrong_input(f)
    
    def get_table(self):
        f = '[MClient] articles.Articles.get_table'
        try:
            return self.articles['ids'][self.id]['table']
        except KeyError:
            rep.wrong_input(f)
    
    def get_cell(self, rowno, colno):
        f = '[MClient] articles.Articles.get_cell'
        try:
            return self.articles['ids'][self.id]['table'][rowno][colno]
        except (KeyError, IndexError):
            rep.wrong_input(f)
    
    def get_len(self):
        return self.get_max_id() + 1
    
    def add(self, search='', url='', cells=[], table=[], raw_code=''
           ,fixed_urls=[], subjf=[], blocked=[], prioritized=[]):
        f = '[MClient] articles.Articles.add'
        # Do not add articles that were not found to history
        if not cells:
            rep.lazy(f)
            return
        id_ = self.get_max_id() + 1
        self.articles['ids'][id_] = {'source'        : CONFIG.new['source']
                                    ,'lang1'         : PLUGINS.get_lang1()
                                    ,'lang2'         : PLUGINS.get_lang2()
                                    ,'Parallel'      : PLUGINS.is_parallel()
                                    ,'Separate'      : PLUGINS.is_separate()
                                    ,'search'        : search
                                    ,'url'           : url
                                    ,'cells'         : cells
                                    ,'table'         : table
                                    ,'raw_code'      : raw_code
                                    ,'fixed_urls'    : fixed_urls
                                    ,'subjf'         : subjf
                                    ,'blocked'       : blocked
                                    ,'prioritized'   : prioritized
                                    ,'rowno'         : -1
                                    ,'colno'         : -1
                                    ,'blocked_cells' : []}
        self.set_id(id_)
    
    def get_blocked_cells(self):
        f = '[MClient] articles.Articles.get_blocked_cells'
        try:
            return self.articles['ids'][self.id]['blocked_cells']
        except KeyError:
            rep.wrong_input(f)
    
    def set_blocked_cells(self, texts):
        f = '[MClient] articles.Articles.set_blocked_cells'
        try:
            self.articles['ids'][self.id]['blocked_cells'] = texts
        except KeyError:
            rep.wrong_input(f)
    
    def clear_article(self):
        f = '[MClient] articles.Articles.clear_article'
        try:
            del self.articles['ids'][self.id]
        except KeyError:
            rep.wrong_input(f)
            return
        if self.id > 0:
            self.set_id(self.id-1)
        else:
            self.id = -1
    
    def delete_bookmarks(self):
        f = '[MClient] articles.Articles.delete_bookmarks'
        try:
            self.articles['ids']
        except KeyError:
            rep.wrong_input(f)
            return
        for id_ in self.articles['ids']:
            self.articles['ids'][id_]['rowno'] = -1
            self.articles['ids'][id_]['colno'] = -1
    
    def set_bookmark(self, rowno, colno):
        f = '[MClient] articles.Articles.set_bookmark'
        try:
            self.articles['ids'][self.id]['rowno'] = rowno
            self.articles['ids'][self.id]['colno'] = colno
        except KeyError:
            rep.wrong_input(f)
    
    def get_bookmark(self):
        f = '[MClient] articles.Articles.get_bookmark'
        try:
            return (self.articles['ids'][self.id]['rowno']
                   ,self.articles['ids'][self.id]['colno'])
        except KeyError:
            rep.wrong_input(f)
    
    def set_id(self, id_):
        f = '[MClient] articles.Articles.set_id'
        try:
            self.articles['ids'][id_]
        except KeyError:
            rep.wrong_input(f, id_)
            return
        self.id = id_
    
    def get_search(self):
        f = '[MClient] articles.Articles.get_search'
        try:
            return self.articles['ids'][self.id]['search']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_source(self):
        f = '[MClient] articles.Articles.get_source'
        try:
            return self.articles['ids'][self.id]['source']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_url(self):
        f = '[MClient] articles.Articles.get_url'
        try:
            return self.articles['ids'][self.id]['url']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_lang1(self):
        f = '[MClient] articles.Articles.get_lang1'
        try:
            return self.articles['ids'][self.id]['lang1']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_lang2(self):
        f = '[MClient] articles.Articles.get_lang2'
        try:
            return self.articles['ids'][self.id]['lang2']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_raw_code(self):
        f = '[MClient] articles.Articles.get_raw_code'
        try:
            return self.articles['ids'][self.id]['raw_code']
        except KeyError:
            rep.wrong_input(f)
        return ''
    
    def get_cells(self):
        f = '[MClient] articles.Articles.get_cells'
        try:
            return self.articles['ids'][self.id]['cells']
        except KeyError:
            rep.wrong_input(f)
        return []
    
    def find(self, source, search, url):
        f = '[MClient] articles.Articles.find'
        try:
            self.articles['ids']
        except KeyError:
            rep.wrong_input(f)
            return
        for id_ in self.articles['ids']:
            if self.articles['ids'][id_]['source'] == source \
            and self.articles['ids'][id_]['search'] == search \
            and self.articles['ids'][id_]['url'] == url:
                return id_
        return -1
    
    def is_parallel(self):
        f = '[MClient] articles.Articles.is_parallel'
        try:
            return self.get_len() > 0 and self.articles['ids'][self.id]['Parallel']
        except KeyError:
            rep.wrong_input(f)
    
    def is_separate(self):
        f = '[MClient] articles.Articles.is_separate'
        try:
            return self.get_len() > 0 and self.articles['ids'][self.id]['Separate']
        except KeyError:
            rep.wrong_input(f)


ARTICLES = Articles()
