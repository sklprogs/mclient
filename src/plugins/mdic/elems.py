#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

from skl_shared.localize import _
from skl_shared.message.controller import rep, Message
from skl_shared.table import Table
from skl_shared.list import List

from instance import Block as inBlock
from instance import Cell as inCell


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
        self.block.Fixed = self.json['Fixed']
    
    def run(self):
        f = '[MClient] plugins.mdic.elems.Block.run'
        # json_cell['fixed_block'] is allowed to be empty
        if not self.json:
            rep.lazy(f)
            return self.block
        self.assign()
        return self.block



class Cell:
    
    def __init__(self, json_cell, wform, cell_text):
        self.cell = inCell()
        self.json = json_cell
        self.wform = wform
        self.text = cell_text
    
    def assign(self):
        # Attributes that are not stored: wform, text, col1, col2, col3, col4
        self.cell.wform = self.wform
        self.cell.text = self.text
        self.cell.no = self.json['no']
        self.cell.rowno = self.json['rowno']
        self.cell.colno = self.json['colno']
        self.cell.subjpr = self.json['subjpr']
        self.cell.speechpr = self.json['speechpr']
        self.cell.code = self.json['code']
        self.cell.speech = self.json['speech']
        self.cell.source = self.json['source']
        self.cell.dic = self.json['dic']
        self.cell.subj = self.json['subj']
        self.cell.transc = self.json['transc']
        self.cell.url = self.json['url']
        self.cell.fixed_block = Block(self.json['fixed_block']).run()
        for json_block in self.json['blocks']:
            block = Block(self.json['blocks'][json_block]).run()
            self.cell.blocks.append(block)
    
    def run(self):
        f = '[MClient] plugins.mdic.elems.Cell.run'
        if not self.json or not self.wform or not self.text:
            rep.empty(f)
            return self.cell
        self.assign()
        return self.cell



class Elems:

    def __init__(self, str_lst):
        f = '[MClient] plugins.mdic.elems.Elems.__init__'
        self.phsubj_name = _('Phrases')
        self.jsons = []
        self.blocks = []
        self.cells = []
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
    
    def set_cells(self):
        f = '[MClient] plugins.mdic.elems.Elems.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        for dic in self.jsons:
            dic_cells = []
            for wform in dic:
                for cell_text in dic[wform]:
                    dic_cells.append(Cell(dic[wform][cell_text], wform, cell_text).run())
            self.cells.append(dic_cells)
        if not self.cells:
            self.Success = False
            rep.empty_output(f)
    
    def join_cells(self):
        f = '[MClient] plugins.mdic.elems.Elems.join_cells'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.cells[0] or not self.cells[0][-1].blocks:
            rep.wrong_input(f)
            return []
        no = self.cells[0][-1].no + 1
        cellno = self.cells[0][-1].blocks[-1].cellno + 1
        i = 1
        while i < len(self.cells):
            for cell in self.cells[i]:
                cell.no = no
                no += 1
                for block in cell.blocks:
                    block.cellno = cellno
                    cellno += 1
            i += 1
        self.cells = List(self.cells).join_sublists()
    
    def set_blocks(self):
        f = '[MClient] plugins.mdic.elems.Elems.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        for cell in self.cells:
            self.blocks += cell.blocks
    
    def run(self):
        self.set_jsons()
        self.expand_dic()
        self.set_cells()
        self.join_cells()
        self.set_blocks()
        return self.blocks
    
    def debug(self):
        f = '[MClient] plugins.mdic.elems.Elems.debug'
        if not self.Success:
            rep.cancel(f)
            return
        report = [self._debug_blocks(), self._debug_cells()]
        report = [item for item in report if item]
        return '\n\n'.join(report)
    
    def _debug_blocks(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.mdic.elems.Elems._debug_blocks'
        headers = (_('CELL #'), _('TYPES'), _('TEXT'), 'SUBJ', 'SUBJF', 'URL')
        nos = []
        types = []
        texts = []
        subj = []
        subjf = []
        urls = []
        for cell in self.cells:
            for block in cell.blocks:
                nos.append(block.cellno)
                types.append(block.type)
                texts.append(f'"{block.text}"')
                subj.append(block.subj)
                subjf.append(block.subjf)
                urls.append(block.url)
        mes = Table(headers = headers
                   ,iterable = (nos, types, texts, subj, subjf, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'
    
    def _debug_cells(self, maxrow=30, maxrows=0):
        f = '[MClient] plugins.mdic.elems.Elems._debug_cells'
        headers = ('SUBJ', 'WFORM', 'SPEECH', 'TRANSC', _('ROW #'), _('CELL #')
                  ,_('TYPES'), _('TEXT'), 'URL')
        subj = []
        wform = []
        speech = []
        transc = []
        rownos = []
        nos = []
        types = []
        texts = []
        urls = []
        for cell in self.cells:
            subj.append(cell.subj)
            wform.append(cell.wform)
            speech.append(cell.speech)
            transc.append(cell.transc)
            rownos.append(cell.rowno)
            nos.append(cell.no)
            texts.append(f'"{cell.text}"')
            cell_types = [block.type for block in cell.blocks]
            types.append(', '.join(cell_types))
            urls.append(cell.url)
        mes = Table(headers = headers
                   ,iterable = (subj, wform, speech, transc, rownos, nos, types
                               ,texts, urls)
                   ,maxrow = maxrow, maxrows = maxrows).run()
        return f'{f}:\n{mes}'