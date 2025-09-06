#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.debug.controller import DEBUG as shDEBUG
from skl_shared.paths import Path
from skl_shared.pretty_html import make_pretty

from plugins.dsl.get import DSL as PLUGIN_DSL
from plugins.dsl.cleanup import CleanUp
from plugins.dsl.get import Get
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems


class DSL(PLUGIN_DSL):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get_name(self):
        ''' Do not put this inside plugins.dsl, since the name depends on Fora
            properties too.
        '''
        f = '[MClient] convert2odxml.DSL.get_name'
        if not self.Success:
            rep.cancel(f)
            return
        if self.dicname:
            return self.dicname
        bname = Path(self.file).get_basename()
        if bname:
            return bname
        return _('DSL Dictionary')
    
    def set_blocks(self):
        f = '[MClient] convert2odxml.DSL.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.poses:
            self.Success = False
            rep.empty(f)
            return
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



class Parser:
    
    def __init__(self, file):
        self.Success = True
        self.cells = []
        self.articles = []
        self.dicname = ''
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
        self.dicname = idic.get_name()
        self.articles = idic.set_blocks()
        #cur
        self.articles = self.articles[:10]
        self.Success = idic.Success and self.dicname and self.articles
    
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
        blocks = []
        for article in self.articles:
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
        self.cells = [cell for cell in self.cells if cell]
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
    
    def check(self):
        f = '[MClient] convert2odxml.XML.check'
        if not self.cells or not self.dicname:
            self.Success = False
            rep.empty(f)
    
    def open_dictionary(self):
        self.xml.append(f'<dictionary name="{self.dicname}">')
    
    def close_dictionary(self):
        ''' ODXML allows only 1 dictionary, even upon merging, so there is no
            need to check whether it is open.
        '''
        self.xml.append(f'</dictionary>')
    
    def open_entry(self, text):
        self.open.append('entry')
        self.xml.append(f'<entry term="{text}">')
    
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
        self.xml.append(f'<sense pos="{speech}">')
    
    def close_sense(self):
        if 'sense' in self.open:
            self.open.remove('sense')
            self.xml.append(f'</sense>')
    
    def open_definition(self, term):
        self.open.append('definition')
        self.xml.append(f'<definition value="{term}">')
    
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
            if not cell:
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
                mes = _('Empty speeches are not allowed!')
                Message(f, mes).show_warning()
                continue
            if wform != cell.blocks[0].wform:
                #TODO: Should we check it?
                self.close_definition()
                self.close_sense()
                self.close_ety()
                self.close_entry()
                wform = cell.blocks[0].wform
                self.open_entry(wform)
                self.open_ety()
            if speech != cell.blocks[0].speech:
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
        return make_pretty('\n'.join(self.xml))


if __name__ == '__main__':
    f = '[MClient] convert2odxml.__main__'
    ROOT.get_root()
    iparse = Parser('/home/pete/.config/mclient/dics/ComputerEnRu.dsl')
    cells = iparse.run()
    if cells:
        mes = XML(cells, iparse.dicname).run()
        shDEBUG.reset(f, mes)
        shDEBUG.show()
    mes = _('Goodbye!')
    Message(f, mes).show_debug()
    ROOT.end()
