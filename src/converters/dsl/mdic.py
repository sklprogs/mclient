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
from skl_shared.list import List
from skl_shared.text_file import Write
from skl_shared.launch import Launch

from plugins.dsl.cleanup import CleanUp
from plugins.dsl.get import ALL_DICS
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems

BODY_FOLDER = Home('mclient').add_config('dics', 'MDIC')
INDEX_FOLDER = os.path.join(BODY_FOLDER, 'collection.indexes')
CREATE_FOLDER = Path(BODY_FOLDER).create() and Path(INDEX_FOLDER).create()
BIN_FILE = os.path.join(BODY_FOLDER, 'collection.mdic')
INDEX = {}


class Portion:
    
    def __init__(self, articles, source, pos=0):
        self.json = {}
        self.code = ''
        self.body = []
        self.cells = []
        self.wforms = []
        ''' A source name should not be empty; however, json accepts '' as keys
            so we do not force non-empty sources here.
        '''
        self.Success = self.articles = articles
        self.source = source
        self.pos = pos
   
    def set_wforms(self):
        # Do this only after 'self.set_json'
        f = '[MClient] converters.dsl.mdic.Portion.set_wforms'
        if not self.Success:
            rep.cancel(f)
            return
        self.wforms = [item.lower().strip() for item in self.json.keys() if item]
    
    def set_cells(self):
        f = '[MClient] converters.dsl.mdic.Portion.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        # We do not want millions of debug messages
        ms.STOP = True
        for article in self.articles:
            code = CleanUp(article).run()
            blocks = Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            cells = Elems(blocks).run()
            if cells:
                self.cells.append(cells)
        ms.STOP = False
        if not self.cells:
            self.Success = False
            rep.empty_output(f)
            return
    
    def _get_wform(self, article_cells):
        if not article_cells[0]:
            return ''
        if not article_cells[0].blocks:
            return ''
        return article_cells[0].blocks[0].wform
    
    def set_json(self):
        f = '[MClient] converters.dsl.mdic.Portion.set_json'
        if not self.Success:
            rep.cancel(f)
            return
        ms.STOP = True
        for article_cells in self.cells:
            wform = self._get_wform(article_cells)
            if not wform in self.json:
                self.json[wform] = {'source': self.source, 'cells': {}}
            for cell in article_cells:
                if not cell or not cell.text:
                    rep.empty(f)
                    continue
                ''' Rewrite cells having the same text (may relate to different
                    subjects of the same source) (should we do that?).
                '''
                self.json[wform]['cells'][cell.text] = Cell(cell).run()    
        ms.STOP = False
    
    def _debug_json(self):
        # Debug JSON structure of the current portion
        f = '[MClient] converters.dsl.mdic.Portion._debug_json'
        if not self.Success:
            rep.cancel(f)
            return
        file = Home('mclient').add_config('dics', 'debug-portion-json.txt')
        Write(file, True).write(self.code)
        Launch(file).launch_default()
    
    def dump_json(self):
        f = '[MClient] converters.dsl.mdic.Portion.dump_json'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            ''' Adding 'indent=4' will significantly slow down exporting, but
                we need this to parse the resulting string manually, because
                calling 'json.dumps' on each fragment is unbearably slow.
            '''
            self.code = json.dumps(self.json, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
        #self._debug_json()
    
    def _is_invalid_fragm(self, fragm):
        if not fragm:
            return True
        fragm = fragm.splitlines()
        # When formatted, JSON section should be at least 3 lines long
        if len(fragm) < 3:
            return True
        if fragm[1].strip() == '"": {':
            return True
    
    def _debug_wforms_fragms(self):
        # Debug word forms and fragments as a table upon failure
        f = '[MClient] converters.dsl.mdic.Portion._debug_wforms_fragms'
        mes = ['wforms:'] + self.wforms
        mes.append('')
        mes.append('fragms:')
        for fragm in self.fragms:
            fragm = fragm.splitlines()
            if len(fragm) < 2:
                rep.wrong_input(f, '\n'.join(fragm))
                continue
            mes.append(fragm[1])
        file = Home('mclient').add_config('dics', 'debug-wforms-fragms.txt')
        Write(file, True).write('\n'.join(mes))
        Launch(file).launch_default()
    
    def set_fragms(self):
        f = '[MClient] converters.dsl.mdic.Portion.set_fragms'
        if not self.Success:
            rep.cancel(f)
            return
        self.fragms = Poses(self.code).run()
        old_len = len(self.fragms)
        self.fragms = [fragm for fragm in self.fragms \
                      if not self._is_invalid_fragm(fragm)]
        if not self.fragms:
            rep.empty_output(f)
            self.Success = False
        rep.deleted(f, old_len - len(self.fragms))
        if len(self.wforms) != len(self.fragms):
            self.Success = False
            mes = f'{len(self.wforms)} == {len(self.fragms)}'
            rep.condition(f, mes)
            self._debug_wforms_fragms()
    
    def _get_abbr(self, wform):
        abbr = [char for char in wform.lower() if str(char).isalpha()]
        abbr = ''.join(abbr)
        abbr = abbr[0:2]
        ''' If abbr is empty and there is no extension, the app tries to save
            the file as a directory and fails. Either use an extension or
            do not allow an empty name.
        '''
        if not abbr:
            abbr = 'unknown'
        return abbr
    
    def _add_index(self, i, pos, length):
        abbr = self._get_abbr(self.wforms[i])
        # Do not rewrite index!
        if not abbr in INDEX:
            INDEX[abbr] = {}
        if not self.wforms[i] in INDEX[abbr]:
            INDEX[abbr][self.wforms[i]] = []
        INDEX[abbr][self.wforms[i]].append({'pos': pos, 'len': length})
    
    def set_body(self):
        ''' Without compression, the resulting body is ~7.3 times larger than
            the original DSL source.
        '''
        f = '[MClient] converters.dsl.mdic.Portion.set_body'
        if not self.Success:
            rep.cancel(f)
            return
        for i in range(len(self.fragms)):
            bytes_ = bytes(self.fragms[i], 'utf-8')
            # This is significantly faster than doing += for string of bytes
            self.body.append(bytes_)
            # +1/-1 to get rid of starting/ending commas or curly braces
            self._add_index(i, self.pos+1, len(bytes_)-1)
            self.pos += len(bytes_)
        self.body = b''.join(self.body)
    
    def save_body(self):
        f = '[MClient] converters.dsl.mdic.Portion.save_body'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Write "{}"').format(BIN_FILE)
        Message(f, mes).show_info()
        try:
            with open(BIN_FILE, 'ba') as ibody:
                ibody.write(self.body)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
    
    def free_memory(self):
        # Should be processed even if the class fails
        self.json = {}
        self.code = ''
        self.body = b''
        self.cells = []
        self.fragms = []
        self.wforms = []
        self.articles = []
    
    def add_wforms(self):
        #TODO: Do this somewhere else
        for i in range(len(self.articles)):
            self.articles[i] = self._add_wform(self.articles[i])
    
    def _add_wform(self, article):
        f = '[MClient] converters.dsl.mdic.Portion._add_wform'
        if not article:
            rep.empty(f)
            return ''
        article = article.splitlines()
        article[0] = article[0].strip()
        article[0] = '[wform]' + article[0] + '[/wform]'
        return '\n'.join(article)
    
    def run(self):
        self.add_wforms()
        self.set_cells()
        self.set_json()
        self.dump_json()
        self.set_wforms()
        self.set_fragms()
        self.set_body()
        self.save_body()
        self.free_memory()
        # We return tuple in order not to keep in memory this class
        return(self.Success, self.pos)



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



class Runner:
    
    def __init__(self):
        self.Success = CREATE_FOLDER and ALL_DICS.Success
        self.feed_limit = 1000
    
    def loop_sources(self):
        f = '[MClient] converters.dsl.mdic.Runner.loop_sources'
        if not self.Success:
            rep.cancel(f)
            return
        if self.feed_limit <= 0:
            self.Success = False
            mes = f'{self.feed_limit} > 0'
            rep.condition(f, mes)
            return
        PROGRESS.set_value(0)
        ''' We cannot set the number of articles here since they are
            not processed yet.
        '''
        PROGRESS.set_max(len(ALL_DICS.dics))
        PROGRESS.set_title(_('Process articles'))
        PROGRESS.show()
        pos = 0
        count = 0
        for idic in ALL_DICS.dics:
            if not self.Success:
                break
            idic.set_articles()
            self.Success = idic.Success
            if not self.Success:
                break
            for articles in List(idic.articles).split_by_len(self.feed_limit):
                mes = _('Dictionary: {}\nArticles processed in total: {}')
                mes = mes.format(idic.fname, count)
                PROGRESS.set_info(mes, 69)
                PROGRESS.update()
                count += len(articles)
                self.Success, pos = Portion(articles, idic.fname, pos).run()
                if not self.Success:
                    break
            PROGRESS.inc()
            PROGRESS.update()
        PROGRESS.close()
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Runner.run'
        timer = Timer(f)
        timer.start()
        self.loop_sources()
        self.Success = self.Success and Index().run()
        sub = shcom.get_human_time(timer.end())
        if self.Success:
            mes = _('The operation has taken {}.')
            mes = mes.format(sub)
            Message(f, mes, True).show_info()
        else:
            mes = _('The operation has failed! Time wasted: {}').format(sub)
            Message(f, mes, True).show_error()



class Poses:
    
    def __init__(self, code):
        self.start = []
        self.end = []
        #NOTE: Change this upon changing JSON structure
        self.start_pattern = '\n    "'
        self.end_pattern = '\n    }'
        self.fragms = []
        self.code = code
        self.Success = self.code
    
    def _search(self, pattern, pos):
        return self.code.find(pattern, pos)
    
    def set_start(self):
        f = '[MClient] converters.dsl.mdic.Poses.set_start'
        if not self.Success:
            rep.cancel(f)
            return
        pos = 0
        while True:
            pos = self._search(self.start_pattern, pos)
            if pos == -1:
                break
            self.start.append(pos - 1)
            pos += 1
    
    def set_end(self):
        f = '[MClient] converters.dsl.mdic.Poses.set_end'
        if not self.Success:
            rep.cancel(f)
            return
        pos = 0
        while True:
            pos = self._search(self.end_pattern, pos)
            if pos == -1:
                break
            self.end.append(pos + len(self.end_pattern))
            pos += 1
    
    def check(self):
        f = '[MClient] converters.dsl.mdic.Poses.check'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.start) != len(self.end):
            self.Success = False
            mes = f'{len(self.start)} == {len(self.end)}'
            rep.condition(f, mes)
    
    def set_fragms(self):
        f = '[MClient] converters.dsl.mdic.Poses.set_fragms'
        if not self.Success:
            rep.cancel(f)
            return
        for i in range(len(self.start)):
            self.fragms.append(self.code[self.start[i]:self.end[i]])
        if not self.fragms:
            self.Success = False
            rep.empty_output(f)
    
    def _debug_poses(self):
        f = '[MClient] converters.dsl.mdic.Poses._debug_poses'
        print(f + ':')
        print('start:', self.start)
        print('end:', self.end)
    
    def _debug_fragms(self):
        f = '[MClient] converters.dsl.mdic.Poses._debug_fragms'
        print(f + ':')
        for i in range(len(self.fragms)):
            print(i + 1, ':')
            print('"' + self.fragms[i] + '"')
            print()
    
    def _debug_dics(self):
        f = '[MClient] converters.dsl.mdic.Poses._debug_dics'
        print(f + ':')
        for i in range(len(self.fragms)):
            dic = json.loads(self.fragms[i])
            print(i + 1, ':')
            print(dic)
            print()
    
    def debug(self):
        f = '[MClient] converters.dsl.mdic.Poses.debug'
        if not self.Success:
            rep.cancel(f)
            return
        self._debug_poses()
        self._debug_fragms()
        self._debug_dics()
    
    def free_memory(self):
        f = '[MClient] converters.dsl.mdic.Poses.free_memory'
        if not self.Success:
            rep.cancel(f)
            return
        self.start = []
        self.end = []
        self.code = ''
    
    def run(self):
        self.set_start()
        self.set_end()
        self.check()
        self.set_fragms()
        #self.debug()
        self.free_memory()
        return self.fragms



class Index:
    
    def __init__(self):
        self.Success = True
    
    def _save(self, abbr, bytes_):
        f = '[MClient] converters.dsl.mdic.Index._save'
        if not self.Success:
            rep.cancel(f)
            return
        file = os.path.join(INDEX_FOLDER, abbr)
        mes = _('Write "{}"').format(file)
        Message(f, mes).show_info()
        try:
            with open(file, 'ba') as iindex:
                iindex.write(bytes_)
        except Exception as e:
            self.Success = False
            rep.third_party(f, e)
        return self.Success
    
    def save(self):
        f = '[MClient] converters.dsl.mdic.Index.save'
        if not self.Success:
            rep.cancel(f)
            return
        abbrs = sorted(INDEX.keys())
        for abbr in abbrs:
            wforms = sorted(INDEX[abbr].keys())
            indexes = []
            for wform in wforms:
                wform_string = []
                wform_lst = INDEX[abbr][wform]
                for wform_dic in wform_lst:
                    wform_string.append(str(wform_dic['pos']))
                    wform_string.append(str(wform_dic['len']))
                wform_string = '\t'.join(wform_string)
                index = f"{wform}\t{wform_string}"
                indexes.append(index)
            bytes_ = bytes('\n'.join(indexes), 'utf-8')
            if not self._save(abbr, bytes_):
                break
    
    def run(self):
        self.save()
        return self.Success