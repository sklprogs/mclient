#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import copy
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic


class Elems:

    def __init__(self, blocks, Debug=False):
        f = '[MClient] plugins.dsl.elems.Elems.__init__'
        self.blocks = blocks
        self.Debug = Debug
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def delete_trash(self):
        self.blocks = [block for block in self.blocks if block.text != ',']
    
    def divide_block(self):
        sep1 = ' || '
        sep2 = '; '
        i = 0
        while i < len(self.blocks):
            if sep1 in self.blocks[i].text \
            or sep2 in self.blocks[i].text:
                text = self.blocks[i].text
                text = text.replace(sep2, sep1)
                split = text.split(sep1)
                block = copy.copy(self.blocks[i])
                del self.blocks[i]
                for item in split[::-1]:
                    block_copy = copy.copy(block)
                    block_copy.text = item
                    self.blocks.insert(i, block_copy)
                i = i - 1 + len(split)
            i += 1
    
    def run(self):
        f = '[MClient] plugins.dsl.elems.Elems.run'
        if not self.Success:
            sh.com.cancel(f)
            return []
        self.divide_block()
        self.set_phsubj()
        self.delete_trash()
        self.add_space()
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        return self.blocks
    
    def debug(self, maxrow=20, maxrows=1000):
        f = '[MClient] plugins.dsl.elems.Elems.debug'
        if not self.Debug or not self.blocks:
            sh.com.rep_lazy(f)
            return
        headers = ('NO', 'SUBJ', 'SUBJF', 'WFORM', 'SPEECH', 'TRANSC', 'TYPE'
                  ,'TEXT'
                  )
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].subj
                         ,self.blocks[i].subjf
                         ,self.blocks[i].wform
                         ,self.blocks[i].speech
                         ,self.blocks[i].transc
                         ,self.blocks[i].type
                         ,self.blocks[i].text
                         ]
                        )
        mes = [f'{f}:']
        sub = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ,Transpose = True
                           ).run()
        mes.append(sub)
        sub = _('Blocks:')
        mes.append(sub)
        mes.append('')
        return '\n'.join(mes)
    
    def add_space(self):
        f = '[MClient] plugins.dsl.elems.Elems.add_space'
        count = 0
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].cellno == self.blocks[i-1].cellno:
                if self.blocks[i].text and self.blocks[i-1].text \
                and not self.blocks[i].text[0].isspace() \
                and not self.blocks[i].text[0] in sh.lg.punc_array \
                and not self.blocks[i].text[0] in [')', ']', '}'] \
                and not self.blocks[i-1].text[-1] in ['(', '[', '{']:
                    count += 1
                    self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1
        sh.com.rep_matches(f, count)

    def set_phsubj(self):
        count = 0
        for block in self.blocks:
            if block.type == 'phrase':
                count += 1
        for i in range(len(self.blocks)):
            if self.blocks[i].type == 'phrase':
                block = ic.Block()
                block.type = 'phsubj'
                block.same = 0
                # There is no separate section for phrases
                block.select = 0
                mes = _('{} phrases').format(count)
                block.text = block.subj = block.subjf = mes
                self.blocks.insert(i, block)
                return True
                
    def fill(self):
        subj = wform = speech = transc = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
                break
        for block in self.blocks:
            if block.type == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type == 'transc':
                transc = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                subj = block.text
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            block.subj = block.subjf = subj.strip()
            block.wform = wform
            block.speech = speech
            block.transc = transc
    
    def insert_fixed(self):
        subj = subjf = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if subj != self.blocks[i].subj or subjf != self.blocks[i].subjf \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = ic.Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)

                block = ic.Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                subj = self.blocks[i].subj
                subjf = self.blocks[i].subjf
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                       not in ('subj', 'wform', 'transc', 'speech')
                      ]
