#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import skl_shared.shared as sh
from skl_shared.localize import _


''' Tag patterns:
    #NOTE: tags can be embedded, e.g.,
    [m1][c][trn][com]comment[/com][/c] translation[/trn][/m]
    •  Language:
        #INDEX_LANGUAGE	"English"
    •  Dictionary titles:
        #NAME	"DicTitle (En-Ru)"
    •  Terms:
        <A line that does not start with '\t'>
        [trn]term[/trn]
    •  Comments:
        [com]comment[/com]
        [i]comment[/i]
        [p][i]comment[/i][/p]
    •  Transcription:
        \[[t]-əbl[/t]\]
    •  Parts of speech:
        [p]n[/p]
          adj: adjective
          adv: adverb
          art: article
          cj:  conjunction
          n:   noun
          prp: preposition
          suf: suffix
          v:   verb
    •  Phrases:
        [ref]case[/ref]
    '''


class Block:

    def __init__(self):
        self.block = -1
        self.i     = -1
        self.j     = -1
        self.first = -1
        self.last  = -1
        self.no    = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.same   = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'transc', 'invalid'
        '''
        self.type_    = 'comment'
        self.text     = ''
        self.url      = ''
        self.urla     = ''
        self.dica     = ''
        self.dicaf    = ''
        self.wforma   = ''
        self.speecha  = ''
        self.transca  = ''
        self.terma    = ''
        self.priority = 0



class AnalyzeTag:
    
    def __init__(self,tag):
        self.set_values()
        self.tag = tag
    
    def set_same(self):
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.set_same'
        if self.Success:
            if self.blocks:
                i = 1
                while i < len(self.blocks):
                    self.blocks[i].same = 1
                    i += 1
                self.blocks[0].same = 0
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.tag = ''
        self.types = []
        self.useful = ['com','ex','p','ref','t','trn']
        self.blocks = []
        self.poses1 = []
        self.poses2 = []
        self.content = []
        self.Success = True
    
    def debug(self):
        # This debug will be too frequent, so call it externally
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.debug'
        if self.Success:
            if self.content:
                headers = (_('TYPE'),_('START'),_('END'),_('TEXT'))
                content = ['"{}"'.format(item) for item in self.content]
                iterable = [self.types,self.poses1,self.poses2,content]
                mes = sh.FastTable(iterable,headers).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def rename_types(self):
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.rename_types'
        if self.Success:
            for block in self.blocks:
                if block.type_ == 'trn':
                    block.type_ = 'term'
                elif block.type_ in ('com','ex'):
                    block.type_ = 'comment'
                elif block.type_ == 'p':
                    block.type_ = 'wform'
                elif block.type_ == 'ref':
                    block.type_ = 'phrase'
                elif block.type_ == 't':
                    block.type_ = 'transc'
        else:
            sh.com.cancel(f)
    
    def set_blocks(self):
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.set_blocks'
        if self.Success:
            for i in range(len(self.types)):
                block = Block()
                block.type_ = self.types[i]
                block.text = self.content[i]
                self.blocks.append(block)
        else:
            sh.com.cancel(f)
    
    def _cleanup(self,fragm):
        fragm = re.sub('\[.*\]','',fragm)
        return fragm.strip()
    
    def cut(self):
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.cut'
        if self.Success:
            for i in range(len(self.poses1)):
                fragm = self.tag[self.poses1[i]:self.poses2[i]]
                self.content.append(self._cleanup(fragm))
        else:
            sh.com.cancel(f)
    
    def get_poses(self):
        # Regular expressions will not preserve the order of blocks
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.get_poses'
        if self.Success:
            FoundTag = False
            for item in self.useful:
                opening = '[{}]'.format(item)
                start = self.tag.find(opening)
                if start > -1:
                    closing = '[/{}]'.format(item)
                    end = self.tag.find(closing)
                    if end == -1:
                        mes = _('No such tag: "{}"!').format(closing)
                        sh.objs.get_mes(f,mes,True).show_warning()
                    else:
                        FoundTag = True
                        self.poses1.append(start)
                        self.poses2.append(end)
                        self.types.append(item)
            if not FoundTag:
                tag = self._cleanup(self.tag)
                self.poses1.append(0)
                self.poses2.append(len(self.tag))
                self.types.append('com')
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.AnalyzeTag.check'
        if not self.tag:
            self.Success = False
            sh.com.rep_empty(f)
    
    def run(self):
        self.check()
        self.get_poses()
        self.cut()
        self.set_blocks()
        self.rename_types()
        self.set_same()



class Tags:

    def __init__ (self,lst,Debug=False
                 ,maxrow=50,maxrows=1000
                 ):
        self.set_values()
        self.lst = lst
        self.Debug = Debug
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def set_dic_name(self):
        f = '[MClient] plugins.dsl.tags.Tags.debug'
        if self.Success:
            # 'self.lst' has at least one item since it's not empty
            block = Block()
            block.same = 0
            block.type_ = 'dic'
            block.text = self.lst[0]
            self.blocks.append(block)
            del self.lst[0]
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.lst = []
        self.blocks = []
        self.Debug = False
        self.Success = True
        self.maxrow = 50
        self.maxrows = 1000
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.Tags.check'
        if self.lst:
            ''' We expect at least 3 lines: a dictionary title, a term, 
                a translation.
            '''
            if len(self.lst) < 3:
                self.Success = False
                sub = '{} > 2'.format(len(self.lst))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)

    def debug(self):
        f = '[MClient] plugins.dsl.tags.Tags.debug'
        if self.Success:
            if self.Debug and self.blocks:
                types = [block.type_ for block in self.blocks]
                content = [block.text for block in self.blocks]
                same = [block.same for block in self.blocks]
                headers = (_('TYPE'),_('TEXT'),'SAME')
                content = ['"{}"'.format(item) for item in content]
                iterable = [types,content,same]
                mes = sh.FastTable (iterable = iterable
                                   ,headers  = headers
                                   ,maxrow   = self.maxrow
                                   ,maxrows  = self.maxrows
                                   ).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)

    def set_blocks(self):
        f = '[MClient] plugins.dsl.tags.Tags.set_blocks'
        if self.Success:
            for tag in self.lst:
                if tag.startswith('\t'):
                    ianalyze = AnalyzeTag(tag)
                    ianalyze.run()
                    if ianalyze.blocks:
                        self.blocks += ianalyze.blocks
                else:
                    tag = re.sub('\{.*\}','',tag)
                    tag = tag.strip()
                    if tag:
                        block = Block()
                        block.type_ = 'term'
                        block.text = tag
                        block.same = 0
                        self.blocks.append(block)
                    else:
                        ''' The dictionary probably has a wrong format
                            (or we forgot to delete empty lines with
                            'self.strip').
                        '''
                        sh.com.rep_empty(f)
            ''' Tag contents can be empty because of cases
                like '[trn][ref]item[/ref][/trn]'. Such tags
                as '[trn][/trn]' are useless, and we discard them.
            '''
            self.blocks = [block for block in self.blocks if block.text]
        else:
            sh.com.cancel(f)

    def run(self):
        self.check()
        self.set_dic_name()
        self.set_blocks()
        self.debug()
        return self.blocks


if __name__ == '__main__':
    code = '{This is} some term\n\t[m1][c][trn][com]this is a comment[/com][/c] this is a term[/trn][/m]'
    AnalyzeTag(code).run()
    Tags(code,Debug=True).run()
