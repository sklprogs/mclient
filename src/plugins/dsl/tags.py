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
        [ref]phrase[/ref]
        [ref dict="Dic title"]phrase[/ref]
    '''


class Duplicates:
    
    def __init__(self,code,Debug=False):
        self.code = code
        self.Debug = Debug
        self.end = []
        self.poses = []
        self.start = []
        self.Success = True
    
    def run(self):
        self.check()
        self.find_poses()
        self.delete_closing()
        self.debug_poses()
        self.get_borders()
        self.debug_borders()
        self.delete_borders()
        return self.code
    
    def delete_borders(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.delete_borders'
        if self.Success:
            i = len(self.start) - 1
            self.code = list(self.code)
            while i >= 0:
                self.code[self.start[i]:self.end[i]] = ''
                i -= 1
            self.code = ''.join(self.code)
            mes = '"{}"'.format(self.code)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def debug_borders(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.debug_borders'
        if self.Debug:
            if self.Success:
                fragms = []
                nos = [i+1 for i in range(len(self.start))]
                headers = ('NO','START','END','TEXT')
                for i in range(len(self.start)):
                    fragms.append(self.code[self.start[i]:self.end[i]])
                fragms = ['"{}"'.format(fragm) for fragm in fragms]
                iterable = [nos,self.start,self.end,fragms]
                mes = sh.FastTable(iterable,headers).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_lazy(f)
    
    def get_borders(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.get_borders'
        if self.Success:
            for pos in self.poses:
                pos1 = self._get_left(pos)
                if str(pos1).isdigit():
                    self.start.append(pos1)
                    self.end.append(pos+1)
        else:
            sh.com.cancel(f)
    
    def _get_left(self,pos):
        i = pos
        while i >= 0:
            if self.code[i] == '[':
                return i
            i -= 1
    
    def _get_right(self,pos):
        i = pos + 2
        while i < len(self.code):
            if self.code[i] == ']':
                return i
            i += 1
    
    def debug_poses(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.debug_poses'
        if self.Debug:
            if self.Success:
                left = []
                right = []
                fragms = []
                for pos in self.poses:
                    pos1 = self._get_left(pos)
                    pos2 = self._get_right(pos)
                    if str(pos1).isdigit() and str(pos2).isdigit():
                        fragms.append(self.code[pos1:pos2+1])
                mes = '; '.join(fragms)
                sh.objs.get_mes(f,mes,True).show_debug()
            else:
                sh.com.cancel(f)
        else:
            sh.com.rep_lazy(f)
    
    def find_poses(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.find_poses'
        if self.Success:
            pos = 0
            while True:
                pos = self.code.find('][',pos)
                if pos == -1:
                    break
                else:
                    self.poses.append(pos)
                    pos += 1
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.check'
        if not self.code:
            self.Success = False
            sh.com.rep_empty(f)
        
    def delete_closing(self):
        f = '[MClient] plugins.dsl.tags.Duplicates.delete_closing'
        if self.Success:
            i = 0
            deleted = []
            while i < len(self.poses):
                if self._is_closing_left(self.poses[i]) \
                or self._is_closing_right(self.poses[i]):
                    deleted.append(self.poses[i])
                    del self.poses[i]
                    i -= 1
                i += 1
            sh.objs.get_mes(f,deleted,True).show_debug()
        else:
            sh.com.cancel(f)
    
    def _is_closing_right(self,pos):
        if pos + 2 < len(self.code):
            if self.code[pos+2] == '/':
                return True
    
    def _is_closing_left(self,pos):
        if pos > 0:
            code = self.code[:pos]
            code = code[::-1]
            pos1 = code.find('/')
            pos2 = code.find('[')
            if pos1 > -1 and pos1 < pos2:
                return True



class Block:

    def __init__(self):
        self.block = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.dic = ''
        self.dicf = ''
        self.dprior = 0
        self.first = -1
        self.i = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        ''' 'select' is an attribute of a *cell* which is valid
            if the cell has a non-blocked block of types 'term',
            'phrase' or 'transc'.
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.transc = ''
        self.term = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase',
            'speech', 'term', 'transc', 'wform'
        '''
        self.type_ = 'comment'
        self.url = ''
        self.urla = ''
        self.wform = ''



class AnalyzeTag:
    
    def __init__(self,tag):
        self.set_values()
        self.tag = tag
    
    def get_ref_dict(self):
        ''' Due to the algorithm of 'self.get_poses', matches returned
            by this code will be added to the end of the list of blocks,
            but this is OK, since those tags are treated like phrases. 
        '''
        pattern = r'\[ref dict=".*?"\](.*?)\[\/ref\]'
        matches = re.findall(pattern,self.tag)
        if matches:
            self.content += matches
            for i in range(len(matches)):
                self.types.append('ref')
    
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
        self.blocks = []
        self.content = []
        self.poses1 = []
        self.poses2 = []
        self.Success = True
        self.tag = ''
        self.types = []
        self.useful = ['com','ex','p','ref','t','trn']
    
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
        self.get_ref_dict()
        self.set_blocks()
        self.rename_types()
        self.set_same()



class Tags:

    def __init__ (self,lst,Debug=False
                 ,maxrow=50,maxrows=1000
                 ):
        self.set_values()
        self.Debug = Debug
        self.lst = lst
        self.maxrow = maxrow
        self.maxrows = maxrows
    
    def set_dic_block(self,name):
        f = '[MClient] plugins.dsl.tags.Tags.debug'
        if self.Success:
            block = Block()
            block.same = 0
            block.select = 0
            block.type_ = 'dic'
            block.text = block.dic = block.dicf = name
            self.blocks.append(block)
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.blocks = []
        self.Debug = False
        self.lst = []
        self.maxrow = 50
        self.maxrows = 1000
        self.Success = True
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.Tags.check'
        if self.lst:
            ''' We expect at least 3 lines: a dictionary title, a term, 
                a translation.
            '''
            for sublst in self.lst:
                if len(sublst) < 3:
                    self.Success = False
                    sub = '{} > 2'.format(len(sublst))
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_warning()
                    break
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
            for sublst in self.lst:
                self.set_dic_block(sublst[0])
                i = 1
                while i < len(sublst):
                    if sublst[i].startswith('\t'):
                        ianalyze = AnalyzeTag(sublst[i])
                        ianalyze.run()
                        if ianalyze.blocks:
                            self.blocks += ianalyze.blocks
                    else:
                        tag = re.sub('\{.*\}','',sublst[i])
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
                    i += 1
            ''' Tag contents can be empty because of cases
                like '[trn][ref]item[/ref][/trn]'. Such tags
                as '[trn][/trn]' are useless, and we discard them.
            '''
            self.blocks = [block for block in self.blocks if block.text]
        else:
            sh.com.cancel(f)

    def run(self):
        self.check()
        self.set_blocks()
        self.debug()
        return self.blocks


if __name__ == '__main__':
    f = '[MClient] plugins.dsl.tags.__main__'
    code = '{This is} some term\n\t[m1][c][trn][com]this is a comment[/com][/c] this is a term[/trn][/m]'
    '''
    itag = AnalyzeTag(code)
    itag.run()
    itag.debug()
    '''
    #Tags(code,Debug=True).run()
    mes = _('Original:\n"{}"\n\n').format(code)
    mes += _('Final:\n"{}"').format(Duplicates(code,False).run())
    sh.com.run_fast_debug(f,mes)
