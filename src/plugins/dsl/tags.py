#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import plugins.dsl.cleanup as cu


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
        ''' 'select' is an attribute of a *cell* which is valid if the cell has
            a non-blocked block of types 'term', 'phrase' or 'transc'.
        '''
        self.select = -1
        self.speech = ''
        self.sprior = -1
        self.transc = ''
        self.term = ''
        self.text = ''
        ''' 'comment', 'correction', 'dic', 'invalid', 'phrase', 'speech',
            'term', 'transc', 'wform'.
        '''
        self.type = 'comment'
        self.url = ''
        self.urla = ''
        self.wform = ''



class Tag:
    
    def __init__(self):
        self.text = ''
        self.tags = []



class Tags:
    
    def __init__(self, code, dicname='', Debug=False, maxrows=0):
        self.set_values()
        self.all_prior = [i for i in range(len(self.all_types))]
        self.code = code
        self.Debug = Debug
        self.dicname = dicname
        self.maxrows = maxrows
    
    def set_dic_block(self):
        f = '[MClient] plugins.dsl.tags.Tags.set_dic_block'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.blocks:
            sh.com.rep_lazy(f)
            return
        block = Block()
        block.text = block.dicf = block.dic = self.dicname
        block.type = 'dic'
        self.blocks.insert(0, block)
    
    def set_values(self):
        self.all_types = ['term', 'dic', 'wform', 'transc', 'comment', 'phrase']
        self.blocks = []
        self.fragms = []
        self.open = []
        self.Success = True
        self.tagged = []
    
    def _debug_blocks(self):
        nos = [i + 1 for i in range(len(self.blocks))]
        texts = [block.text for block in self.blocks]
        types = [block.type for block in self.blocks]
        iterable = [nos, types, texts]
        headers = (_('#'), _('TYPES'), _('TEXT'))
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 50
                           ,maxrows = self.maxrows
                           ).run()
        return _('Blocks:') + '\n' + mes
    
    def _get_max_type(self, types):
        f = '[MClient] plugins.dsl.tags.Tags._get_max_type'
        prior = []
        i = 0
        while i < len(types):
            try:
                index_ = self.all_types.index(types[i])
                prior.append(self.all_prior[index_])
            except ValueError:
                mes = _('Wrong input data: "{}"!').format(types[i])
                sh.objs.get_mes(f, mes, True).show_warning()
                del types[i]
                i -= 1
            i += 1
        if types:
            index_ = prior.index(max(prior))
            return types[index_]
        else:
            sh.com.rep_empty(f)
    
    def set_blocks(self):
        f = '[MClient] plugins.dsl.tags.Tags.set_blocks'
        if not self.Success:
            sh.com.cancel(f)
            return
        for item in self.tagged:
            type_ = self._get_max_type(item.tags)
            if not type_:
                sh.com.rep_empty(f)
                continue
            block = Block()
            block.type = type_
            block.text = item.text
            self.blocks.append(block)
    
    def delete_empty(self):
        f = '[MClient] plugins.dsl.tags.Tags.delete_empty'
        if not self.Success:
            sh.com.cancel(f)
            return
        deleted = []
        i = 0
        while i < len(self.tagged):
            if self.tagged[i].tags == []:
                deleted.append(self.tagged[i].text)
                del self.tagged[i]
                i -= 1
            i += 1
        if deleted:
            deleted = sorted(set(deleted))
            deleted = ['"{}"'.format(item) for item in deleted]
            deleted = ', '.join(deleted)
            mes = _('Ignore blocks: {}').format(deleted)
            sh.objs.get_mes(f, mes, True).show_debug()
    
    def keep_useful(self):
        f = '[MClient] plugins.dsl.tags.Tags.keep_useful'
        if not self.Success:
            sh.com.cancel(f)
            return
        useful = ('com', 'ex', 'i', 'p', 'ref', 't', 'term', 'trn', 'wform')
        for item in self.tagged:
            item.tags = [tag for tag in item.tags \
                         if tag in useful or 'ref dict' in tag
                        ]
    
    def rename_types(self):
        f = '[MClient] plugins.dsl.tags.Tags.rename_types'
        if not self.Success:
            sh.com.cancel(f)
            return
        for item in self.tagged:
            for i in range(len(item.tags)):
                if item.tags[i] == 'trn':
                    item.tags[i] = 'term'
                elif item.tags[i] in ('com', 'ex', 'i'):
                    item.tags[i] = 'comment'
                elif item.tags[i] == 'p':
                    item.tags[i] = 'wform'
                elif item.tags[i] == 't':
                    item.tags[i] = 'transc'
                elif item.tags[i] == 'ref' or 'ref dict' in item.tags[i]:
                    item.tags[i] = 'phrase'
    
    def _close_tag(self, tag):
        f = '[MClient] plugins.dsl.tags.Tags._close_tag'
        if tag in self.open:
            self.open.remove(tag)
        elif tag == 'm':
            for item in self.open:
                if re.match('m\d+', item):
                    self.open.remove(item)
        elif tag == 'ref':
            for item in self.open:
                if 'ref dict' in item:
                    self.open.remove(item)
        elif tag == 'lang':
            for item in self.open:
                if 'lang id' in item:
                    self.open.remove(item)
        else:
            mes = _('Tag "{}" has not been opened yet!').format(tag)
            sh.objs.get_mes(f, mes, True).show_warning()
    
    def _get_tag_name(self, tag):
        tag = tag[:-1]
        tag = tag.replace('[', '', 1)
        if tag.startswith('/'):
            tag = tag[1:]
        return tag
    
    def set(self):
        f = '[MClient] plugins.dsl.tags.Tags.set'
        if not self.Success:
            sh.com.cancel(f)
            return
        # The 1st fragment should always be an article title
        i = 1
        for fragm in self.fragms:
            if fragm.startswith('['):
                tag = self._get_tag_name(fragm)
                if fragm.startswith('[/'):
                    self._close_tag(tag)
                elif not tag in self.open:
                    self.open.append(tag)
            else:
                itag = Tag()
                itag.text = fragm
                itag.tags = list(self.open)
                self.tagged.append(itag)
            i += 1
    
    def delete_trash(self):
        ''' Delete unnecessary items by line (as opposite to manipulating the
            entire code in cleanup.CleanUp.delete_trash).
        '''
        f = '[MClient] plugins.dsl.tags.Tags.delete_trash'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.fragms = [fragm.strip() for fragm in self.fragms \
                       if fragm not in ('\n', '\n\t')
                      ]
    
    def _debug_code(self):
        return _('Code:') + '\n' + '"{}"'.format(self.code)
    
    def _debug_fragms(self):
        mes = []
        for i in range(len(self.fragms)):
            sub = '{}: "{}"'.format(i + 1, self.fragms[i])
            mes.append(sub)
        return _('Fragments:') + '\n' + '\n'.join(mes)
    
    def _debug_tagged(self):
        nos = [i + 1 for i in range(len(self.tagged))]
        texts = [item.text for item in self.tagged]
        tags = [', '.join(item.tags) for item in self.tagged]
        iterable = [nos, tags, texts]
        headers = (_('#'), _('TAGS'), _('TEXT'))
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,maxrow = 50
                           ,maxrows = self.maxrows
                           ).run()
        return _('Tags:') + '\n' + mes
    
    def debug(self):
        f = '[MClient] plugins.dsl.tags.Tags.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        mes = [self._debug_code(), self._debug_fragms()
              ,self._debug_tagged(), self._debug_blocks()
              ]
        mes = '\n\n'.join(mes)
        sh.com.run_fast_debug(f, mes)
    
    def check(self):
        f = '[MClient] plugins.dsl.tags.Tags.check'
        if not self.code:
            # Avoid None on output
            self.code = ''
            self.Success = False
            sh.com.rep_empty(f)
    
    def split(self):
        f = '[MClient] plugins.dsl.tags.Tags.split'
        if not self.Success:
            sh.com.cancel(f)
            return
        fragm = ''
        for sym in list(self.code):
            if sym == '[':
                if fragm:
                    self.fragms.append(fragm)
                fragm = sym
            elif sym == ']':
                fragm += sym
                self.fragms.append(fragm)
                fragm = ''
            else:
                fragm += sym
        if fragm:
            self.fragms.append(fragm)
    
    def run(self):
        self.check()
        self.split()
        self.delete_trash()
        self.set()
        self.keep_useful()
        self.delete_empty()
        self.rename_types()
        self.set_blocks()
        self.set_dic_block()
        self.debug()
        return self.blocks


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    file = '/home/pete/bin/mclient/tests/dsl/account balance.txt'
    code = sh.ReadTextFile(file).get()
    code = cu.CleanUp(code).run()
    code = cu.TagLike(code).run()
    Tags(code, True).run()
    sh.com.end()
