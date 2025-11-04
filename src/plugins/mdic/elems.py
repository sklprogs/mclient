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
        self.block.subj = self.json['subj']
        self.block.subjf = self.json['subjf']
        self.block.text = self.json['text']
        self.block.url = self.json['url']
        self.block.type = self.json['type']
    
    def run(self):
        f = '[MClient] plugins.mdic.elems.Block.run'
        # json_cell['fixed_block'] is allowed to be empty
        if not self.json:
            rep.lazy(f)
            return self.block
        self.assign()
        return self.block



class Elems:

    def __init__(self, str_lst):
        f = '[MClient] plugins.mdic.elems.Elems.__init__'
        self.phsubj_name = _('Phrases')
        self.jsons = []
        self.blocks = []
        self.fixed_urls = {'subj':{}, 'wform':{}, 'phsubj':{}}
        self.Parallel = False
        self.Separate = False
        self.str_lst = str_lst
        if self.str_lst:
            self.Success = True
        else:
            self.Success = False
            rep.empty(f)
    
    def _load_json(self, string):
        f = '[MClient] plugins.mdic.elems.Elems._load_json'
        try:
            return json.loads(string)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def set_jsons(self):
        f = '[MClient] plugins.mdic.elems.Elems.set_jsons'
        if not self.Success:
            rep.cancel(f)
            return
        for string in self.str_lst:
            dic = self._load_json(string)
            if not dic:
                self.Success = False
                return
            self.jsons.append(dic)
    
    def expand_dic(self):
        f = '[MClient] plugins.mdic.elems.Elems.expand_dic'
        if not self.Success:
            rep.cancel(f)
            return
        #TODO (?): implement
        pass
    
    def set_blocks(self):
        f = '[MClient] plugins.mdic.elems.Elems.set_blocks'
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
    
    def run(self):
        self.set_jsons()
        self.expand_dic()
        self.set_blocks()
        return self.blocks