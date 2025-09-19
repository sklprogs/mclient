#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import json

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG
from skl_shared.time import Timer
from skl_shared.paths import Home, Path
from skl_shared.logic import com as shcom

from plugins.dsl.cleanup import CleanUp
from plugins.dsl.get import ALL_DICS
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems

from converters.dsl.shared import Parser as shParser
from converters.dsl.shared import Runner as shRunner

JSON = {}


class Block:
    
    def __init__(self, block):
        self.json = {}
        self.block = block
    
    def assign(self):
        self.json['cellno'] = self.block.cellno
        self.json['subj'] = self.block.subj
        self.json['subjf'] = self.block.subjf
        self.json['text'] = self.block.text
        self.json['url'] = self.block.url
        self.json['type'] = self.block.type
        self.json['Fixed'] = self.block.Fixed
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Block.run'
        if not self.block:
            # Cell.fixed_block is allowed to be None
            rep.lazy(f)
            return {}
        self.assign()
        return self.json



class Cell:
    
    def __init__(self, cell):
        self.json = {}
        self.cell = cell
    
    def assign(self):
        # Attributes that are not stored: wform, text, col1, col2, col3, col4
        self.json['no'] = self.cell.no
        self.json['rowno'] = self.cell.rowno
        self.json['colno'] = self.cell.colno
        self.json['subjpr'] = self.cell.subjpr
        self.json['speechpr'] = self.cell.speechpr
        self.json['code'] = self.cell.code
        self.json['speech'] = self.cell.speech
        self.json['subj'] = self.cell.subj
        self.json['transc'] = self.cell.transc
        self.json['url'] = self.cell.url
        self.json['fixed_block'] = Block(self.cell.fixed_block).run()
        self.json['blocks'] = {}
        for block in self.cell.blocks:
            # Rewrite blocks with the same text (should we allow that?)
            self.json['blocks'][block.text] = Block(block).run()
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Cell.run'
        if not self.cell:
            rep.empty(f)
            return {}
        self.assign()
        return self.json



class Parser(shParser):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = _('unknown source')
    
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
            JSON[self.source][self.wform][cell.text] = Cell(cell).run()
    
    def _add_wform(self, article):
        f = '[MClient] converters.dsl.mdic.Parser._add_wform'
        if not article:
            rep.empty(f)
            self.wform = _('unknown word form')
            if not self.wform in JSON[self.source]:
                JSON[self.source][self.wform] = {}
            return
        article = article.splitlines()
        article[0] = article[0].strip()
        self.wform = article[0].lower()
        article[0] = '[wform]' + article[0] + '[/wform]'
        if not self.wform in JSON[self.source]:
            JSON[self.source][self.wform] = {}
        return '\n'.join(article)
    
    def set_cells(self):
        f = '[MClient] converters.dsl.mdic.Parser.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        self.source = self.idic.dicname
        # Do not overwrite contents of dictionaries having the same name
        if not self.source in JSON:
            JSON[self.source] = {}
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
        ms.STOP = True
        self.set_articles()
        self.set_cells()
        ms.STOP = False
        return self.cells



class Runner(shRunner):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
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
        Dump().run()
        sub = shcom.get_human_time(timer.end())
        mes = _('The operation has taken {}.').format(sub)
        Message(f, mes, True).show_info()



class Dump:
    
    def __init__(self):
        #TODO: Read index from files
        self.index = {}
        self.fragms = b''
        self.body_folder = Home('mclient').add_config('dics', 'MDIC')
        self.index_folder = Home('mclient').add_config('dics', 'MDIC', 'collection.indexes')
        self.file = os.path.join(self.body_folder, 'collection.mdic')
        ''' By design, the index folder is created inside the body folder.
            Path is created recursively. So, just create the index folder.
        '''
        self.Success = JSON and Path(self.index_folder).create()
    
    def _dump_wform(self, dic):
        f = '[MClient] converters.dsl.mdic.Dump._dump_wform'
        try:
            return json.dumps(dic, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
        return ''
    
    def _save_index(self, abbr, bytes_):
        f = '[MClient] converters.dsl.mdic.Dump._save_index'
        if not self.Success:
            rep.cancel(f)
            return
        #file = os.path.join(self.index_folder, str(hash(abbr)))
        file = os.path.join(self.index_folder, abbr)
        mes = _('Write "{}"').format(file)
        Message(f, mes).show_info()
        try:
            with open(file, 'ba') as iindex:
                iindex.write(bytes_)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def save_indexes(self):
        f = '[MClient] converters.dsl.mdic.Dump.save_indexes'
        if not self.Success:
            rep.cancel(f)
            return
        abbrs = sorted(self.index.keys())
        for abbr in abbrs:
            wforms = sorted(self.index[abbr].keys())
            indexes = []
            for wform in wforms:
                index = f"{wform}\t{self.index[abbr][wform]['pos']}\t{self.index[abbr][wform]['len']}"
                indexes.append(index)
            bytes_ = bytes('\n'.join(indexes), 'utf-8')
            self._save_index(abbr, bytes_)
            if not self.Success:
                break
    
    def save_body(self):
        f = '[MClient] converters.dsl.mdic.Dump.save_body'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Write "{}"').format(self.file)
        Message(f, mes).show_info()
        try:
            with open(self.file, 'ba') as ibody:
                ibody.write(self.fragms)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def loop(self):
        f = '[MClient] converters.dsl.mdic.Dump.loop'
        if not self.Success:
            rep.cancel(f)
            return
        # Currently pos is not saved anywhere, so process everything at once
        pos = 0
        for source in JSON:
            wforms = sorted(JSON[source].keys())
            for wform in wforms:
                fragm = self._dump_wform(JSON[source][wform])
                bytes_ = bytes(fragm, 'utf-8')
                length = len(bytes_)
                self.fragms += bytes_
                #TODO: Delete characters not supported in file names
                abbr = wform.replace(' ', '')
                # Index abbreviation may be shorter than 3 characters
                abbr = abbr[0:2]
                # Do not rewrite index!
                if not abbr in self.index:
                    self.index[abbr] = {}
                #TODO: Allow duplicate wforms
                self.index[abbr][wform] = {'pos': pos, 'len': length}
                pos += length
            # Write body binary to release memory before processing new source
            self.save_body()
            # Release memory
            self.fragms = b''
            JSON[source] = {}
        self.save_indexes()
    
    def debug(self):
        # Do this before releasing memory
        f = '[MClient] converters.dsl.mdic.Dump.debug'
        if not self.Success:
            rep.cancel(f)
            return
        mes = self._debug_index() + '\n\n' + self._debug_body()
        shDEBUG.reset(f, mes)
        shDEBUG.show()
    
    def _debug_index(self):
        f = '[MClient] converters.dsl.mdic.Dump._debug_index'
        mes = [f + ':']
        mes.append(self._dump_wform(self.index))
        mes = [item for item in mes if item]
        return '\n'.join(mes)
    
    def _debug_body(self):
        # Do this before releasing memory
        f = '[MClient] converters.dsl.mdic.Dump._debug_body'
        mes = [f + ':']
        abbrs = sorted(self.index.keys())
        for abbr in abbrs:
            wforms = sorted(self.index[abbr].keys())
            for wform in wforms:
                index = f"{wform}\t{self.index[abbr][wform]['pos']}\t{self.index[abbr][wform]['len']}"
                mes.append(index)
                pos1 = self.index[abbr][wform]['pos']
                pos2 = pos1 + self.index[abbr][wform]['len']
                bytes_ = self.fragms[pos1:pos2]
                if not bytes_:
                    rep.empty(f)
                    break
                text = bytes_.decode('utf-8')
                mes.append('"' + text + '"')
                mes.append('')
        return '\n'.join(mes)
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Dump.run'
        self.loop()