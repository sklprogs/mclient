#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import html

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.time import Timer
from skl_shared.logic import com as shcom

from plugins.dsl.cleanup import CleanUp
from plugins.dsl.get import ALL_DICS
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems

from converters.dsl.shared import Parser as shParser
from converters.dsl.shared import Runner as shRunner


class Parser(shParser):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json = {}
        self.source = _('unknown source')
    
    def _add_blocks(self, cell):
        #TODO: implement
        self.json[self.source][self.wform][cell.text]['fixed_block'] = {}
        self.json[self.source][self.wform][cell.text]['blocks'] = {}
    
    def add_cells(self, cells):
        f = '[MClient] converters.dsl.mdic.Parser.add_cells'
        if not self.Success:
            rep.cancel(f)
            return
        for cell in cells:
            if not cell or not cell.text:
                rep.empty(f)
                continue
            ''' Rewrite cells having the same text (may relate to different
                subjects) (should we do that?).
            '''
            self.json[self.source][self.wform][cell.text] = {}
            self.json[self.source][self.wform][cell.text]['no'] = cell.no
            self.json[self.source][self.wform][cell.text]['rowno'] = cell.rowno
            self.json[self.source][self.wform][cell.text]['colno'] = cell.colno
            self.json[self.source][self.wform][cell.text]['subjpr'] = cell.subjpr
            self.json[self.source][self.wform][cell.text]['speechpr'] = cell.speechpr
            self.json[self.source][self.wform][cell.text]['code'] = cell.code
            self.json[self.source][self.wform][cell.text]['speech'] = cell.speech
            self.json[self.source][self.wform][cell.text]['subj'] = cell.subj
            self.json[self.source][self.wform][cell.text]['transc'] = cell.transc
            self.json[self.source][self.wform][cell.text]['url'] = cell.url
            self.json[self.source][self.wform][cell.text]['col1'] = cell.col1
            self.json[self.source][self.wform][cell.text]['col2'] = cell.col2
            self.json[self.source][self.wform][cell.text]['col3'] = cell.col3
            self.json[self.source][self.wform][cell.text]['col4'] = cell.col4
            self._add_blocks(cell)
    
    def _add_wform(self, article):
        f = '[MClient] converters.dsl.mdic.Parser._add_wform'
        if not article:
            rep.empty(f)
            self.wform = _('unknown word form')
            if not self.wform in self.json[self.source]:
                self.json[self.source][self.wform] = {}
            return
        article = article.splitlines()
        article[0] = article[0].strip()
        self.wform = article[0].lower()
        article[0] = '[wform]' + article[0] + '[/wform]'
        if not self.wform in self.json[self.source]:
            self.json[self.source][self.wform] = {}
        return '\n'.join(article)
    
    def set_cells(self):
        f = '[MClient] converters.dsl.mdic.Parser.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        self.source = self.idic.dicname
        # Do not overwrite contents of dictionaries having the same name
        if not self.source in self.json:
            self.json[self.source] = {}
        for article in self.idic.articles:
            blocks = []
            article = self._add_wform(article)
            code = CleanUp(article).run()
            blocks += Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            cells = Elems(blocks).run()
            if not cells:
                rep.empty(f)
                continue
            self.add_cells(cells)
            self.cells += cells
        # Reclaim memory
        self.idic.articles = []
        if not self.cells:
            self.Success = False
            rep.empty_output(f)
            return
    
    def run(self):
        # We do not want millions of debug messages
        #ms.STOP = True
        self.set_articles()
        #cur
        self.idic.articles = [self.idic.articles[0]]
        self.set_cells()
        #ms.STOP = False
        print(self.json)
        return self.cells



class Runner(shRunner):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def sort(self):
        f = '[MClient] converters.dsl.mdic.Runner.sort'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Sort cells')
        Message(f, mes).show_info()
        self.cells.sort(key=lambda cell: (cell.blocks[0].wform, cell.blocks[0].speech))
    
    def set_cells(self):
        # Call Parser from this module
        f = '[MClient] converters.dsl.mdic.Runner.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        PROGRESS.set_title(_('DSL Dictionary Converter'))
        PROGRESS.show()
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(ALL_DICS.dics))
        for i in range(len(ALL_DICS.dics)):
            PROGRESS.update()
            mes = _('Process {} ({}/{})')
            mes = mes.format(ALL_DICS.dics[i].fname, i + 1, len(ALL_DICS.dics))
            PROGRESS.set_info(mes)
            iparse = Parser(ALL_DICS.dics[i])
            self.cells += iparse.run()
            self.Success = iparse.Success
            if not self.Success:
                break
            PROGRESS.inc()
        PROGRESS.close()
        self.cells = [cell for cell in self.cells if cell]
        mes = _('Cells have been created')
        Message(f, mes).show_info()
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Runner.run'
        timer = Timer(f)
        timer.start()
        self.set_cells()
        #self.sort()
        sub = shcom.get_human_time(timer.end())
        mes = _('The operation has taken {}.').format(sub)
        Message(f, mes, True).show_info()
