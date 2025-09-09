#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import html
import xml.dom.minidom

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG
from skl_shared.paths import Home, Path, File, Directory
from skl_shared.text_file import Write
from skl_shared.time import Timer
from skl_shared.logic import com as shcom

from plugins.dsl.cleanup import CleanUp
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems


class DSL:
    ''' Recreate the class fully since importing plugins.dsl.get will
        automatically read all .dsl files because of ALL_DICS.
    '''
    def __init__(self, file):
        self.set_values()
        self.file = file
        self.check()
    
    def set_blocks(self):
        f = '[MClient] convert2odxml.DSL.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.poses:
            self.Success = False
            rep.empty(f)
            return
        self.poses.append(len(self.lst) - 1)
        i = 1
        while i < len(self.poses):
            block = self.lst[self.poses[i-1]:self.poses[i]]
            self.blocks.append('\n'.join(block))
            i += 1
        return self.blocks
    
    def debug_blocks(self, limit=1000):
        f = '[MClient] convert2odxml.DSL.debug_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        debug = []
        if limit == 0:
            limit = len(self.blocks)
        else:
            limit = min(limit, len(self.blocks))
        for i in range(limit):
            debug.append(f'{f}: {i+1}')
            debug += self.blocks[i]
            debug.append('\n')
        return '\n'.join(debug)
    
    def run(self):
        f = '[MClient] plugins.dsl.get.DSL.run'
        timer = Timer(f)
        timer.start()
        self.load()
        self.cleanup()
        self.get_index()
        timer.end()
    
    def cleanup(self):
        f = '[MClient] plugins.dsl.get.DSL.cleanup'
        if not self.Success:
            rep.cancel(f)
            return
        ''' #NOTE: a line can consist of spaces (actually happened).
            Be careful: 'strip' also deletes tabulation.
        '''
        self.lst = [line.strip(' ') for line in self.lst]
        self.lst = [line for line in self.lst if line \
                   and not line.startswith('#')]
    
    def get_entry(self, pos):
        f = '[MClient] plugins.dsl.get.DSL.get_entry'
        if not self.Success:
            rep.cancel(f)
            return
        pos = Input(f, pos).get_integer()
        # We expect a translation which occupies the following line
        if not (0 <= pos < len(self.lst) - 1):
            sub = '0 <= {} < {}'.format(pos + 1, len(self.lst))
            mes = _('The condition "{}" is not observed!')
            mes = mes.format(sub)
            Message(f, mes, True).show_error()
            return
        article = []
        i = pos + 1
        while i < len(self.lst):
            if self.lst[i].startswith('\t'):
                article.append(self.lst[i])
            else:
                break
            i += 1
        iarticle = Article()
        iarticle.search = self.lst[pos]
        iarticle.code = '\n'.join(article)
        mes = f'"{iarticle.code}"'
        Message(f, mes).show_debug()
        return iarticle
    
    def _delete_curly_brackets(self, line):
        line = re.sub(r'\{.*\}', '', line)
        line = line.strip()
        line = line.lower()
        return line
    
    def get_index(self):
        f = '[MClient] plugins.dsl.get.DSL.get_index'
        if not self.Success:
            rep.cancel(f)
            return self.index_
        if not self.index_:
            for i in range(len(self.lst)):
                if not self.lst[i].startswith('\t'):
                    line = self._delete_curly_brackets(self.lst[i])
                    if line:
                        self.index_.append(line)
                        self.poses.append(i)
            mes = _('Dictionary "{}" ({}) has {} records')
            linesnum = shcom.set_figure_commas(len(self.index_))
            mes = mes.format(self.fname, self.dicname, linesnum)
            Message(f, mes).show_info()
        return self.index_
    
    def check(self):
        f = '[MClient] plugins.dsl.get.DSL.check'
        if not self.file:
            self.Success = False
            rep.empty(f)
            return
        self.Success = File(self.file).Success
    
    def load(self):
        f = '[MClient] plugins.dsl.get.DSL.load'
        if not self.Success:
            rep.cancel(f)
            return
        self.fname = Path(self.file).get_filename()
        mes = _('Load "{}"').format(self.file)
        Message(f, mes).show_info()
        text = ''
        try:
            with open(self.file, 'r', encoding='UTF-16') as fi:
                text = fi.read()
        except Exception as e:
            self.Success = False
            mes = _('Operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            Message(f, mes, True).show_warning()
        ''' Possibly, a memory consumption will be lower if we do not store
            'self.text'.
        '''
        if not text:
            self.Success = False
            rep.empty(f)
            return
        self.lst = text.splitlines()
    
    def set_values(self):
        self.file = ''
        self.fname = ''
        self.lst = []
        self.lang1 = _('Any')
        self.lang2 = _('Any')
        self.poses = []
        self.index_ = []
        self.blocks = []
        self.Success = True
        self.dicname = _('Untitled dictionary')



class Parser:
    
    def __init__(self, file):
        self.Success = True
        self.cells = []
        self.articles = []
        self.file = file
    
    def _has_phrase(self, cell):
        for block in cell.blocks:
            if block.type == 'phrase':
                return True
    
    def remove_phrases(self):
        ''' Dumping to ODXML needs wforms to be sorted; however, combining
            different unassociated articles results in phrases being put at
            the end and their wforms shuffled.
        '''
        f = '[MClient] convert2odxml.Parser.remove_phrases'
        if not self.Success:
            rep.cancel(f)
            return
        self.cells = [cell for cell in self.cells if not self._has_phrase(cell)]
    
    def set_articles(self):
        f = '[MClient] convert2odxml.Parser.set_articles'
        if not self.Success:
            rep.cancel(f)
            return
        idic = DSL(self.file)
        idic.run()
        self.articles = idic.set_blocks()
        self.Success = idic.Success and self.articles
    
    def _add_wform(self, article):
        f = '[MClient] convert2odxml.Parser._add_wform'
        if not article:
            rep.empty(f)
            return
        article = article.splitlines()
        article[0] = '[wform]' + article[0] + '[/wform]'
        return '\n'.join(article)
    
    def set_speech(self):
        # Speech is crucial for OXML, so we must assign it if empty
        f = '[MClient] convert2odxml.Parser.set_speech'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        for cell in self.cells:
            for block in cell.blocks:
                if not block.speech:
                    count += 1
                    block.speech = 'un'
        rep.matches(count)
    
    def set_cells(self):
        f = '[MClient] convert2odxml.Parser.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        for article in self.articles:
            blocks = []
            article = self._add_wform(article)
            code = CleanUp(article).run()
            blocks += Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            ''' When exporting to Odict XML, we do not care about cell or row
                numbers, so we do not need plugins.fora.run.Plugin._join_cells.
            '''
            self.cells += Elems(blocks).run()
        if not self.cells:
            self.Success = False
            rep.empty_output(f)
            return
    
    def run(self):
        self.set_articles()
        self.set_cells()
        self.remove_phrases()
        self.set_speech()
        return self.cells



class XML:
    
    def __init__(self, cells, dicname):
        self.Success = True
        self.xml = []
        self.cells = cells
        self.dicname = dicname
    
    def _make_pretty(self, code):
        f = '[MClient] convert2odxml.XML._make_pretty'
        try:
            code = xml.dom.minidom.parseString(code)
            code = code.toprettyxml()
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            Message(f, mes).show_error()
        return code
    
    def check(self):
        f = '[MClient] convert2odxml.XML.check'
        if not self.cells or not self.dicname:
            self.Success = False
            rep.empty(f)
    
    def open_dictionary(self):
        self.xml.append(f'<dictionary name="{html.escape(self.dicname)}">')
    
    def close_dictionary(self):
        ''' ODXML allows only 1 dictionary, even upon merging, so there is no
            need to check whether it is open.
        '''
        self.xml.append(f'</dictionary>')
    
    def open_entry(self, text):
        self.open.append('entry')
        self.xml.append(f'<entry term="{html.escape(text)}">')
    
    def close_entry(self):
        if 'entry' in self.open:
            self.open.remove('entry')
            self.xml.append(f'</entry>')
    
    def open_ety(self):
        self.open.append('ety')
        self.xml.append('<ety>')
    
    def close_ety(self):
        if 'ety' in self.open:
            self.open.remove('ety')
            self.xml.append('</ety>')
    
    def open_sense(self, speech):
        self.open.append('sense')
        self.xml.append(f'<sense pos="{html.escape(speech)}">')
    
    def close_sense(self):
        if 'sense' in self.open:
            self.open.remove('sense')
            self.xml.append(f'</sense>')
    
    def open_definition(self, term):
        self.open.append('definition')
        self.xml.append(f'<definition value="{html.escape(term)}">')
    
    def close_definition(self):
        if 'definition' in self.open:
            self.open.remove('definition')
            self.xml.append(f'</definition>')
    
    def debug(self):
        for cell in self.cells:
            for i in range(len(cell.blocks)):
                print(f'Block #{i}: text: "{cell.blocks[i].text}", type: "{cell.blocks[i].type}", wform: "{cell.blocks[i].wform}", speech: "{cell.blocks[i].speech}"')
    
    def fill(self):
        f = '[MClient] convert2odxml.XML.fill'
        self.open = []
        wform = ''
        speech = ''
        self.open_dictionary()
        for cell in self.cells:
            if not cell or not cell.text:
                rep.empty(f)
                continue
            if not cell.blocks:
                rep.empty(f)
                continue
            if not cell.blocks[0].wform:
                mes = _('Empty word forms are not allowed!')
                Message(f, mes).show_warning()
                continue
            if not cell.blocks[0].speech:
                mes = _('Empty parts of speech are not allowed!')
                Message(f, mes).show_warning()
                continue
            NewWform = False
            if wform != cell.blocks[0].wform:
                NewWform = True
                #TODO: Should we check it?
                self.close_definition()
                self.close_sense()
                self.close_ety()
                self.close_entry()
                wform = cell.blocks[0].wform
                self.open_entry(wform)
                self.open_ety()
            if NewWform or speech != cell.blocks[0].speech:
                #TODO: Should we check it?
                self.close_definition()
                self.close_sense()
                speech = cell.blocks[0].speech
                self.open_sense(speech)
            #TODO: Rework
            self.open_definition(cell.text)
            self.close_definition()
        #TODO: Should we check it?
        self.close_definition()
        self.close_sense()
        self.close_ety()
        self.close_entry()
        self.close_dictionary()
    
    def run(self):
        f = '[MClient] convert2odxml.XML.run'
        self.check()
        if not self.Success:
            rep.cancel(f)
            return
        #self.debug()
        self.fill()
        return self._make_pretty(''.join(self.xml))



class Runner:
    
    def __init__(self):
        self.files = []
        self.cells = []
        self.path = Home('mclient').add_config('dics')
        self.idir = Directory(self.path)
        self.Success = self.idir.Success
    
    def set_files(self):
        f = '[MClient] convert2odxml.Runner.set_files'
        if not self.Success:
            rep.cancel(f)
            return
        files = self.idir.get_subfiles()
        for file in files:
            if Path(file).get_ext_low() == '.dsl':
                self.files.append(file)
        if not self.files:
            self.Success = False
            rep.empty_output(f)
    
    def set_cells(self):
        f = '[MClient] convert2odxml.Runner.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        for file in self.files:
            iparse = Parser(file)
            self.cells += iparse.run()
            self.Success = iparse.Success
            if not self.Success:
                break
        self.cells = [cell for cell in self.cells if cell]
    
    def sort(self):
        f = '[MClient] convert2odxml.Runner.sort'
        if not self.Success:
            rep.cancel(f)
            return
        self.cells.sort(key=lambda cell: (cell.blocks[0].wform, cell.blocks[0].speech))
    
    def create_xml(self):
        f = '[MClient] convert2odxml.Runner.create_xml'
        if not self.Success:
            rep.cancel(f)
            return
        dicname = _('.dsl dictionaries: {}. Cells: {}')
        dicname = dicname.format(len(self.files), len(self.cells))
        mes = XML(self.cells, dicname).run()
        Write('/home/pete/bin/third-party/odict-bin/single.xml', True).write(mes)
    
    def run(self):
        self.set_files()
        self.set_cells()
        self.sort()
        self.create_xml()
        


if __name__ == '__main__':
    f = '[MClient] convert2odxml.__main__'
    ROOT.get_root()
    Runner().run()
    #shDEBUG.reset(f, mes)
    #shDEBUG.show()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
