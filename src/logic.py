#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import ssl

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.online import Online
from skl_shared.pretty_html import make_pretty
import skl_shared.temp_file as temp_file
from skl_shared.text_file import Read, Write
from skl_shared.launch import Launch
from skl_shared.paths import PDIR, Home
from skl_shared.list import List

from config import CONFIG, PRODUCT_LOW
from manager import SOURCES
from articles import ARTICLES
from table.controller import TABLE
from columns import COL_WIDTH
from instance import is_block_fixed


class App:
    
    def open_in_browser(self):
        ionline = Online()
        url = REQUEST.url
        ionline.url = SOURCES.fix_url(url)
        ionline.browse()
    
    def print(self):
        f = '[MClient] logic.App.print'
        #TODO: elaborate
        skipped = []
        #skipped = com.get_skipped_terms()
        code = HTM(TABLE.logic.blocks, skipped).run()
        if not code:
            rep.empty(f)
            return
        code = make_pretty(code)
        if not code:
            rep.empty(f)
            return
        tmp_file = temp_file.get_file(suffix='.htm', Delete=False)
        Write(tmp_file, True).write(code)
        Launch(tmp_file).launch_default()



class HTM:

    def __init__(self, skipped=0):
        ''' - Takes ~0.01s for 'set' on AMD E-300.
            - 'collimit' includes fixed blocks.
        '''
        self.code = ['<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">']
        self.landscape = ''
        self.skipped = 0
        self.skipped = skipped
        
    def set_landscape(self):
        f = '[MClient] logic.HTM.set_landscape'
        file = PDIR.add('..', 'resources', 'landscape.html')
        code = Read(file).get()
        if not code:
            rep.empty(f)
            return
        if not '%s' in code:
            rep.wrong_input(f, code)
            return
        # Either don't use 'format' here or double all curly braces in script
        self.landscape = code % _('Print')
    
    def run(self):
        self.set_landscape()
        self.create()
        return ''.join(self.code)
    
    def add_landscape(self):
        self.code.append(self.landscape)
        self.code.append('<div id="printableArea">')
    
    def _create_not_found(self):
        self.code.append('<h1>')
        self.code.append(_('Nothing has been found.'))
        self.code.append('</h1>')
    
    def _create_skipped(self):
        self.code.append('<h1>')
        mes = _('Nothing has been found (skipped subjects: {}).')
        mes = mes.format(self.skipped)
        self.code.append(mes)
        self.code.append('</h1>')
    
    def _create_article(self):
        rowno = colno = -1
        self.code.append('<table>')
        for block in TABLE.logic.blocks:
            if block.Ignore or block.Block:
                continue
            if (block.colno != colno or block.rowno != rowno) \
            and block.colno > 0:
                self.code.append('</td>')
            elif block.rowno != rowno and block.rowno > 0:
                self.code.append('</td></tr>')
            if block.rowno != rowno:
                colno = block.colno
                rowno = block.rowno
                self.code.append('<tr><td>')
            elif block.colno != colno:
                colno = block.colno
                rowno = block.rowno
                if is_block_fixed(block):
                    self.code.append('<td align="center" valign="top">')
                else:
                    self.code.append('<td valign="top">')
            self.code.append(block.code)
        if TABLE.logic.blocks:
            self.code.append('</td></tr>')
        self.code.append('</table>')
    
    def create(self):
        self.add_landscape()
        if TABLE.logic.blocks:
            self._create_article()
        elif self.skipped:
            self._create_skipped()
        else:
            self._create_not_found()
        self.code.append('</div></meta></body></html>')



class CurRequest:

    def __init__(self):
        self.cols = ('source', 'dic', 'subj', 'wform', 'transc', 'speech')
        self.collimit = len(self.cols)
        ''' Toggling blacklisting should not depend on a number of blocked
            subjects (otherwise, it is not clear how blacklisting should be
            toggled).
            *Temporarily* turn off prioritizing and terms sorting for articles
            with 'sep_words_found' and in phrases; use previous settings for
            new articles.
        '''
        self.reset()
    
    def set_col_limit(self):
        f = '[MClient] logic.CurRequest.set_col_limit'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.collimit = CONFIG.new['columns']['num'] + len(self.cols)
    
    def reset(self):
        self.htm = ''
        self.text = ''
        self.search = ''
        self.url = ''
        self.set_col_limit()



class Commands:
    
    def __init__(self):
        self.use_unverified()
    
    def fix_colors(self, colors):
        ''' We need HTML code both in cells and output to be saved. Qt requires
            that color names are put in quotes; however, browsers do not
            understand color names in quotes, so we must delete these quotes
            before saving to a web-page.
        '''
        f = '[MClient] logic.Commands.fix_colors'
        if not colors:
            rep.empty(f)
            return
        for color in colors:
            REQUEST.htm = REQUEST.htm.replace(f"'{color}'", color)
    
    def get_colors(self, blocks):
        f = '[MClient] logic.Commands.get_colors'
        if not blocks:
            rep.empty(f)
            return
        colors = []
        for block in blocks:
            if not block.color in colors:
                colors.append(block.color)
        return colors
    
    def set_url(self):
        f = '[MClient] logic.Commands.set_url'
        #NOTE: update source and target languages first
        REQUEST.url = SOURCES.get_url(REQUEST.search)
        mes = REQUEST.url
        Message(f, mes).show_debug()
    
    def control_length(self):
        # Confirm too long requests
        f = '[MClient] logic.Commands.control_length'
        Confirmed = True
        if len(REQUEST.search) >= 150:
            mes = _('The request is long ({} symbols). Do you really want to send it?')
            mes = mes.format(len(REQUEST.search))
            if not Message(f, mes, True).show_question():
                Confirmed = False
        return Confirmed
    
    def export_style(self):
        f = '[MClient] logic.Commands.export_style'
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0.6s slower.
        '''
        types = COL_WIDTH.get_fixed_types()
        if not types:
            rep.lazy(f)
            return
        REQUEST.cols = tuple(types)
        #TODO: Should we change REQUEST.collimit here?
        
    def use_unverified(self):
        f = '[MClient] logic.Commands.use_unverified'
        ''' On *some* systems we can get urllib.error.URLError: <urlopen error
            [SSL: CERTIFICATE_VERIFY_FAILED]>. To get rid of this error, we use
            this small workaround.
        '''
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            mes = _('Unable to use unverified certificates!')
            Message(f, mes).show_warning()



com = Commands()
REQUEST = CurRequest()
