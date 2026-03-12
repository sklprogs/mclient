#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.paths import Path

from instance import Article
from sources.dsl.get import AllDics as DslDics


class AllDics(DslDics):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #TODO: Do not call sources.dsl.get.AllDics.locate from sources.dsl.get.AllDics.__init__
        # Must be recreated because we need to run self.locate once again
        self.dsls = []
        self.dics = []
        self.locate()
    
    def locate(self):
        f = '[MClient] sources.dsl.dump.AllDics.locate'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.dics:
            if self.walk():
                for dsl in self.dsls:
                    self.dics.append(Dsl(dsl))
            else:
                rep.lazy(f)
        mes = _('{} offline dictionaries are available').format(len(self.dics))
        Message(f, mes).show_info()
        return self.dics



class Dsl:
    # Converters
    def __init__(self, file):
        self.file = ''
        self.fname = ''
        self.body = []
        self.wform = ''
        self.recno = 0
        self.pos = 0
        self.Success = True
        self.lang1 = _('Any')
        self.lang2 = _('Any')
        self.dicname = _('Untitled dictionary')
        self.file = file
        self.load()
    
    def set_dic_name(self, line):
        f = '[MClient] sources.dsl.dump.Dsl.set_dic_name'
        if not self.Success:
            rep.cancel(f)
            return
        if not line:
            rep.empty(f)
            return
        match = re.match('#NAME	"(.*)"', line)
        if match:
            dicname = match.group(1).strip()
            if dicname:
                self.dicname = dicname
        if not self.dicname:
            self.dicname = self.fname
        Message(f, f'"{self.dicname}"').show_debug()
    
    def dump(self, limit):
        f = '[MClient] sources.dsl.dump.Dsl.dump'
        if not self.Success:
            rep.cancel(f)
            return
        articles = []
        while len(articles) < limit:
            article = self.get_next()
            if article:
                articles.append(article)
            else:
                break
        return articles
    
    def load(self):
        f = '[MClient] sources.dsl.dump.Dsl.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.fname = Path(self.file).get_filename()
        try:
            self.open = open(self.file, 'r', encoding='UTF-16-LE')
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def close(self):
        f = '[MClient] sources.dsl.dump.Dsl.close'
        if not self.Success:
            rep.cancel(f)
            return
        self.open.close()
    
    def get_next(self):
        f = '[MClient] sources.dsl.dump.Dsl.get_next'
        if not self.Success:
            rep.cancel(f)
            return
        article = Article()
        while True:
            line = self.open.readline()
            if not line:
                if self.wform and self.body:
                   code = [self.wform + '\n'] + self.body
                   code = ''.join(code)
                   article.search = self.wform
                   article.code = code
                   article.dic = self.fname
                   return article
                return
            if line.startswith('#'):
                if line.startswith('#NAME'):
                    self.set_dic_name(line)
                continue
            if line.startswith('\t'):
                self.body.append(line)
                continue
            #NOTE: a line can consist of spaces (actually happened)
            line = line.strip()
            if not line:
                continue
            if self.wform and self.body:
                code = [self.wform + '\n'] + self.body
                code = ''.join(code)
                article.search = self.wform
                article.code = code
                self.wform = line
                self.body = []
                return article
            self.wform = line


ALL_DICS = AllDics()