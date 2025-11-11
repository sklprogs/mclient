#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import html

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.root.controller import ROOT
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.text_file import Write
from skl_shared.time import Timer
from skl_shared.logic import com as shcom

from sources.dsl.get import ALL_DICS

from converters.dsl.shared import Parser as shParser
from converters.dsl.shared import Runner as shRunner


class Parser(shParser):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _has_phrase(self, cell):
        for block in cell.blocks:
            if block.type == 'phrase':
                return True
    
    def remove_phrases(self):
        ''' Dumping to ODXML needs wforms to be sorted; however, combining
            different unassociated articles results in phrases being put at
            the end and their wforms shuffled.
        '''
        f = '[MClient] converters.dsl.odxml.Parser.remove_phrases'
        if not self.Success:
            rep.cancel(f)
            return
        self.cells = [cell for cell in self.cells if not self._has_phrase(cell)]
    
    def set_speech(self):
        # Speech is crucial for OXML, so we must assign it if empty
        f = '[MClient] converters.dsl.odxml.Parser.set_speech'
        mes = f'{f} is in progress'
        Message(f, mes, True).show_info()
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
    
    def run(self):
        # We do not want millions of debug messages
        ms.STOP = True
        self.set_articles()
        self.set_cells()
        self.remove_phrases()
        self.set_speech()
        ms.STOP = False
        return self.cells



class XML:
    
    def __init__(self, cells, dicname):
        self.Success = True
        self.open = []
        self.xml = []
        self.cells = cells
        self.dicname = dicname
    
    def check(self):
        f = '[MClient] converters.dsl.odxml.XML.check'
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
    
    def fill(self):
        f = '[MClient] converters.dsl.odxml.XML.fill'
        step = 1000
        PROGRESS.set_title(_('Generate XML'))
        PROGRESS.set_value(0)
        PROGRESS.set_max(round(len(self.cells) / step))
        PROGRESS.show()
        wform = ''
        speech = ''
        self.open_dictionary()
        count = 0
        for cell in self.cells:
            count += 1
            if count % step == 0:
                PROGRESS.update()
                mes = _('Process cell #{}/{}').format(count, len(self.cells))
                PROGRESS.set_info(mes)
                PROGRESS.inc()
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
        PROGRESS.close()
    
    def run(self):
        f = '[MClient] converters.dsl.odxml.XML.run'
        self.check()
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Generate HTML')
        Message(f, mes).show_info()
        self.fill()
        return ''.join(self.xml)



class Runner(shRunner):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def sort(self):
        f = '[MClient] converters.dsl.odxml.Runner.sort'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Sort cells')
        Message(f, mes).show_info()
        self.cells.sort(key=lambda cell: (cell.blocks[0].wform, cell.blocks[0].speech))
    
    def create_xml(self):
        f = '[MClient] converters.dsl.odxml.Runner.create_xml'
        if not self.Success:
            rep.cancel(f)
            return
        dicname = _('.dsl dictionaries: {}. Cells: {}')
        dicname = dicname.format(len(ALL_DICS.dics), len(self.cells))
        mes = XML(self.cells, dicname).run()
        # Reclaim memory (but do we need this?)
        self.cells = []
        pathw = os.path.join(ALL_DICS.path, 'dsl-odxml.xml')
        Write(pathw, True).write(mes)
        # Reclaim memory (but do we need this?)
        mes = ''
    
    def set_cells(self):
        # Call Parser from this module
        f = '[MClient] converters.dsl.odxml.Runner.set_cells'
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
        f = '[MClient] converters.dsl.odxml.Runner.run'
        timer = Timer(f)
        timer.start()
        self.set_cells()
        self.sort()
        self.create_xml()
        sub = shcom.get_human_time(timer.end())
        mes = _('The operation has taken {}.').format(sub)
        Message(f, mes, True).show_info()
