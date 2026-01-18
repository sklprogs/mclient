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

from sources.dsl.cleanup import CleanUp
from sources.dsl.get import ALL_DICS
from sources.dsl.tags import Tags
from sources.dsl.elems import Elems as dslElems
from cells import Elems


class Parser:
    
    def __init__(self, idic):
        self.idic = idic
        self.Success = self.idic.Success
        self.blocks = []
    
    def set_articles(self):
        f = '[MClient] converters.dsl.odxml.Parser.set_articles'
        if not self.Success:
            rep.cancel(f)
            return
        self.idic.set_articles()
        # Reclaim memory
        self.idic.lst = []
        self.idic.poses = []
        self.idic.index_ = []
        self.Success = self.idic.Success and self.idic.articles
    
    def _add_wform(self, article):
        f = '[MClient] converters.dsl.odxml.Parser._add_wform'
        if not article:
            rep.empty(f)
            return
        article = article.splitlines()
        article[0] = '[wform]' + article[0] + '[/wform]'
        return '\n'.join(article)
    
    def set_blocks(self):
        f = '[MClient] converters.dsl.odxml.Parser.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        for article in self.idic.articles:
            blocks = []
            article = self._add_wform(article)
            code = CleanUp(article).run()
            blocks += Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            ''' When exporting to Odict XML, we do not care about cell or row
                numbers, so we do not need sources.fora.run.Source._join_blocks.
            '''
            self.blocks += dslElems(blocks).run()
        # Reclaim memory
        self.idic.articles = []
        if not self.blocks:
            self.Success = False
            rep.empty_output(f)
            return
    
    def remove_phrases(self):
        ''' Dumping to ODXML needs wforms to be sorted; however, combining
            different unassociated articles results in phrases being put at
            the end and their wforms shuffled.
        '''
        f = '[MClient] converters.dsl.odxml.Parser.remove_phrases'
        if not self.Success:
            rep.cancel(f)
            return
        self.blocks = [block for block in self.blocks if block.type != 'phrase']
    
    def set_speech(self):
        # Speech is crucial for OXML, so we must assign it if empty
        f = '[MClient] converters.dsl.odxml.Parser.set_speech'
        if not self.Success:
            rep.cancel(f)
            return
        count = 0
        for block in self.blocks:
            if not block.speech:
                count += 1
                block.speech = 'un'
        rep.matches(count)
    
    def run(self):
        # We do not want millions of debug messages
        ms.STOP = True
        self.set_articles()
        self.set_blocks()
        self.remove_phrases()
        self.set_speech()
        ms.STOP = False
        return self.blocks



class XML:
    
    def __init__(self, blocks, dicname):
        self.Success = True
        self.open = []
        self.xml = []
        self.blocks = blocks
        self.dicname = dicname
    
    def check(self):
        f = '[MClient] converters.dsl.odxml.XML.check'
        if not self.blocks or not self.dicname:
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
        PROGRESS.set_max(round(len(self.blocks) / step))
        PROGRESS.show()
        wform = ''
        speech = ''
        self.open_dictionary()
        count = 0
        for block in self.blocks:
            count += 1
            if count % step == 0:
                PROGRESS.update()
                mes = _('Process block #{}/{}').format(count, len(self.blocks))
                PROGRESS.set_info(mes)
                PROGRESS.inc()
            if not block or not block.text:
                rep.empty(f)
                continue
            if not block.wform:
                mes = _('Empty word forms are not allowed!')
                Message(f, mes).show_warning()
                continue
            if not block.speech:
                mes = _('Empty parts of speech are not allowed!')
                Message(f, mes).show_warning()
                continue
            NewWform = False
            if wform != block.wform:
                NewWform = True
                #TODO: Should we check it?
                self.close_definition()
                self.close_sense()
                self.close_ety()
                self.close_entry()
                wform = block.wform
                self.open_entry(wform)
                self.open_ety()
            if NewWform or speech != block.speech:
                #TODO: Should we check it?
                self.close_definition()
                self.close_sense()
                speech = block.speech
                self.open_sense(speech)
            #TODO: Rework
            self.open_definition(block.text)
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



class Runner:
    
    def __init__(self):
        self.blocks = []
        self.Success = ALL_DICS.Success

    def sort(self):
        f = '[MClient] converters.dsl.odxml.Runner.sort'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Sort blocks')
        Message(f, mes).show_info()
        self.blocks.sort(key=lambda block: (block.wform, block.speech))
    
    def create_xml(self):
        f = '[MClient] converters.dsl.odxml.Runner.create_xml'
        if not self.Success:
            rep.cancel(f)
            return
        dicname = _('.dsl dictionaries: {}. Blocks: {}')
        dicname = dicname.format(len(ALL_DICS.dics), len(self.blocks))
        mes = XML(self.blocks, dicname).run()
        pathw = os.path.join(ALL_DICS.path, 'dsl-odxml.xml')
        Write(pathw, True).write(mes)
        # Reclaim memory
        self.blocks = []
        mes = ''
    
    def set_blocks(self):
        # Call Parser from this module
        f = '[MClient] converters.dsl.odxml.Runner.set_blocks'
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
            ALL_DICS.dics[i].run()
            iparse = Parser(ALL_DICS.dics[i])
            self.blocks += iparse.run()
            self.Success = iparse.Success
            if not self.Success:
                PROGRESS.close()
                return
            PROGRESS.inc()
        PROGRESS.close()
        mes = _('Blocks have been created')
        Message(f, mes).show_info()
    
    def run(self):
        f = '[MClient] converters.dsl.odxml.Runner.run'
        timer = Timer(f)
        timer.start()
        self.set_blocks()
        self.sort()
        self.create_xml()
        sub = shcom.get_human_time(timer.end())
        if self.Success:
            mes = _('The operation has taken {}.').format(sub)
            Message(f, mes, True).show_info()
        else:
            mes = _('The operation has failed! Time wasted: {}').format(sub)
            Message(f, mes, True).show_error()