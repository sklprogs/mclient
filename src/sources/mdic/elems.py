#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.table import Table
from skl_shared.list import List

from instance import Block as inBlock


class Block:
    
    def __init__(self, json_block):
        self.json = json_block
        self.block = inBlock()
    
    def assign(self):
        self.block.cellno = self.json['cellno']
        self.block.source = self.json['source']
        self.block.dic = self.json['dic']
        self.block.subj = self.json['subj']
        self.block.subjf = self.json['subjf']
        self.block.text = self.json['text']
        self.block.url = self.json['url']
        self.block.type = self.json['type']
    
    def run(self):
        f = '[MClient] sources.mdic.elems.Block.run'
        # json_cell['fixed_block'] is allowed to be empty
        if not self.json:
            rep.lazy(f)
            return self.block
        self.assign()
        return self.block



class Elems:

    def __init__(self, str_lst):
        f = '[MClient] sources.mdic.elems.Elems.__init__'
        self.jsons = []
        self.blocks = []
        self.Parallel = False
        self.Separate = False
        self.str_lst = str_lst
        if self.str_lst:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def _load_json(self, string):
        f = '[MClient] sources.mdic.elems.Elems._load_json'
        try:
            return json.loads(string)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def set_jsons(self):
        f = '[MClient] sources.mdic.elems.Elems.set_jsons'
        if not self.Success:
            rep.cancel(f)
            return
        for string in self.str_lst:
            dic = self._load_json(string)
            if not dic:
                self.Success = False
                return
            self.jsons.append(dic)
    
    def set_blocks(self):
        f = '[MClient] sources.mdic.elems.Elems.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        for dic in self.jsons:
            for wform in dic:
                for block_text in dic[wform]:
                    self.blocks.append(Block(dic[wform][block_text]).run())
        if not self.blocks:
            self.Success = False
            rep.empty_output(f)
    
    def fill(self):
        dic = dicf = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
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
            if block.type == 'term' or block.type == 'phrase':
                term = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.subj
                dicf = block.subjf
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            elif block.type in ('term', 'phrase'):
                term = block.text
            block.subj = dic
            block.subjf = dicf
            block.wform = wform
            block.speech = speech
            block.transc = transc
                
    def insert_fixed(self):
        subj = wform = speech = ''
        i = 0
        cellno = 0
        while i < len(self.blocks):
            if subj != self.blocks[i].subj or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                if i > 0:
                    cellno = self.blocks[i-1].cellno
                
                block = inBlock()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                block = inBlock()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)

                block = inBlock()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                block = inBlock()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.subjf = self.blocks[i].subjf
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                cellno += 0.01
                block.cellno = cellno
                self.blocks.insert(i, block)
                
                subj = self.blocks[i].subj
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                      not in ('subj', 'wform', 'transc', 'speech')]
    
    def set_cellnos(self):
        cellno = 0
        cellnos = [0]
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                cellno += 1
            cellnos.append(cellno)
            i += 1
        for i in range(len(self.blocks)):
            self.blocks[i].cellno = cellnos[i]
    
    def run(self):
        self.set_jsons()
        self.set_blocks()
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        self.set_cellnos()
        return self.blocks