#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import ssl

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.online.controller import Online
from skl_shared_qt.pretty_html import make_pretty
import skl_shared_qt.temp_file as temp_file
from skl_shared_qt.text_file import Read, Write
from skl_shared_qt.launch import Launch
from skl_shared_qt.paths import PDIR, Home

from config import CONFIG, PRODUCT_LOW
import manager


class Speech:
    ''' It's OK to recreate this class each time it runs since the speech
        dictionary is reused and not recreated.
    '''
    def __init__(self):
        self.dic = objs.get_plugins().get_speeches()
    
    def _get_short(self, full):
        f = '[MClient] logic.Speech._get_short'
        for short in self.dic:
            if self.dic[short] == full:
                return short
        rep.wrong_input(f, full)
        return full
    
    def get_settings(self):
        #f = '[MClient] logic.Speech.get_settings'
        # Source tuple cannot be concatenated with target list
        speeches = [CONFIG.new['speech1'], CONFIG.new['speech2']
                   ,CONFIG.new['speech3'], CONFIG.new['speech4']
                   ,CONFIG.new['speech5'], CONFIG.new['speech6']
                   ,CONFIG.new['speech7']]
        if not self.dic:
            return speeches
        if not CONFIG.new['ShortSpeech']:
            return speeches
        for i in range(len(speeches)):
            speeches[i] = self._get_short(speeches[i])
        #mes = ', '.join(speeches)
        #Message(f, mes).show_debug()
        return speeches



class App:
    
    def open_in_browser(self):
        ionline = Online()
        url = objs.get_request().url
        ionline.url = objs.get_plugins().fix_url(url)
        ionline.browse()
    
    def print(self):
        f = '[MClient] logic.App.print'
        code = make_pretty(objs.get_request().htm)
        if not code:
            rep.empty(f)
            return
        tmp_file = temp_file.get_file(suffix='.htm', Delete=False)
        Write(tmp_file, True).write(code)
        Launch(tmp_file).launch_default()



class HTM:

    def __init__(self, cells, skipped=0):
        ''' - Takes ~0.01s for 'set' on AMD E-300.
            - 'collimit' includes fixed blocks.
        '''
        self.set_values()
        self.cells = cells
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
    
    def set_values(self):
        self.code = ['<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">']
        self.landscape = ''
        self.skipped = 0
    
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
        self.code.append('<table>')
        for row in self.cells:
            self.code.append('<tr>')
            for cell in row:
                if cell.fixed_block:
                    #sub = '<td align="center" valign="top" width="{}">'
                    self.code.append('<td align="center" valign="top">')
                else:
                    self.code.append('<td valign="top">')
                self.code.append(cell.code)
                self.code.append('</td>')
            self.code.append('</tr>')
        self.code.append('</table>')
    
    def create(self):
        self.add_landscape()
        if self.cells:
            self._create_article()
        elif self.skipped:
            self._create_skipped()
        else:
            self._create_not_found()
        self.code.append('</div>')
        self.code.append('</meta></body></html>')



class Source:
    
    def __init__(self):
        self.title = ''
        self.status = _('not running')
        self.color = 'red'
        self.Online = False



class Column:
    
    def __init__(self):
        self.no = 0
        self.width = 0
        self.Fixed = False



class ColumnWidth:
    ''' Adjust fixed columns to have a constant width. A fixed value in pixels
        rather than percentage should be used to adjust columns since we cannot
        say if gaps between columns are too large without calculating a text
        width first.
    '''
    def __init__(self):
        self.set_values()
    
    def set_values(self):
        # This approach includes percentage only
        self.fixed_num = 0
        self.term_num = 0
        self.min_width = 1
        self.columns = []
    
    def set_col_width(self):
        f = '[MClient] logic.ColumnWidth.set_col_width'
        if not CONFIG.new['rows']['height']:
            rep.lazy(f)
            return
        for column in self.columns:
            if column.Fixed:
                column.width = CONFIG.new['columns']['fixed']['width']
            else:
                column.width = CONFIG.new['columns']['terms']['width']
#            if objs.get_blocksdb().is_col_empty(column.no):
#                column.width = self.min_width
#            elif column.Fixed:
#                column.width = CONFIG.new['columns']['fixed']['width']
#            else:
#                column.width = CONFIG.new['columns']['terms']['width']
    
    def reset(self):
        self.set_values()
    
    def run(self):
        self.set_fixed_num()
        self.set_term_num()
        self.set_columns()
        self.set_col_width()
    
    def set_fixed_num(self):
        f = '[MClient] logic.ColumnWidth.set_fixed_num'
        self.fixed_num = 4
        mes = _('Number of fixed columns: {}').format(self.fixed_num)
        Message(f, mes).show_debug()
    
    def set_term_num(self):
        f = '[MClient] logic.ColumnWidth.set_term_num'
        self.term_num = com.get_colnum()
        mes = _('Number of term columns: {}')
        mes = mes.format(self.term_num)
        Message(f, mes).show_debug()
    
    def set_columns(self):
        col_nos = self.fixed_num + self.term_num
        for i in range(self.fixed_num):
            column = Column()
            column.no = i
            column.Fixed = True
            self.columns.append(column)
        i = self.fixed_num
        while i < col_nos:
            column = Column()
            column.no = i
            self.columns.append(column)
            i += 1



class CurRequest:

    def __init__(self):
        self.set_values()
        self.reset()
    
    def set_values(self):
        self.cols = ('subj', 'wform', 'transc', 'speech')
        self.collimit = CONFIG.new['columns']['num'] + len(self.cols)
        ''' Toggling blacklisting should not depend on a number of blocked
            subjects (otherwise, it is not clear how blacklisting should be
            toggled).
            *Temporarily* turn off prioritizing and terms sorting for articles
            with 'sep_words_found' and in phrases; use previous settings for
            new articles.
        '''
    
    def reset(self):
        self.htm = ''
        self.text = ''
        self.search = ''
        self.url = ''



class Objects:
    
    def __init__(self):
        self.online = self.request = self.plugins = self.speech_prior \
                    = self.column_width = self.articles = None

    def get_articles(self):
        if self.articles is None:
            self.articles = Articles()
        return self.articles
    
    def get_column_width(self):
        if self.column_width is None:
            self.column_width = ColumnWidth()
            self.column_width.run()
        return self.column_width
    
    def get_dics(self):
        return Home(PRODUCT_LOW).add_config('dics')
    
    def get_plugins(self, Debug=False, maxrows=1000):
        if self.plugins is None:
            self.plugins = manager.Plugins(sdpath = self.get_dics()
                                          ,mbpath = self.get_dics()
                                          ,timeout = CONFIG.new['timeout']
                                          ,Debug = Debug
                                          ,maxrows = maxrows)
        return self.plugins
    
    def get_request(self):
        if self.request is None:
            self.request = CurRequest()
        return self.request



class Commands:
    
    def __init__(self):
        self.use_unverified()
    
    def _get_col_type(self, type_):
        f = '[MClient] logic.Commands._get_col_type'
        if type_ == _('Subjects'):
            return 'subj'
        elif type_ == _('Word forms'):
            return 'wform'
        elif type_ == _('Parts of speech'):
            return 'speech'
        elif type_ == _('Transcription'):
            return 'transc'
        elif type_ == _('Do not set'):
            pass
        else:
            mes = _('Wrong input data: "{}"!').format(type_)
            Message(f, mes, True).show_error()
        return ''
    
    def get_col_types(self):
        f = '[MClient] logic.Commands.get_col_types'
        types = [CONFIG.new['columns']['1']['type']
                ,CONFIG.new['columns']['2']['type']
                ,CONFIG.new['columns']['3']['type']
                ,CONFIG.new['columns']['4']['type']
                ]
        for i in range(len(types)):
            types[i] = self._get_col_type(types[i])
        mes = ', '.join(types)
        Message(f, mes).show_debug()
        return types
    
    def is_parallel(self):
        return objs.get_articles().get_len() > 0 and objs.articles.is_parallel()
    
    def is_separate(self):
        return objs.get_articles().get_len() > 0 and objs.articles.is_separate()
    
    def get_text(self, cells):
        f = '[MClient] logic.Commands.get_text'
        if not cells:
            rep.empty(f)
            return ''
        return '\n'.join([cell.plain for cell in cells])
    
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
            objs.get_request().htm = objs.request.htm.replace(f"'{color}'", color)
    
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
        objs.get_request().url = objs.get_plugins().get_url(objs.request.search)
        mes = objs.request.url
        Message(f, mes).show_debug()
    
    def control_length(self):
        # Confirm too long requests
        f = '[MClient] logic.Commands.control_length'
        Confirmed = True
        if len(objs.get_request().search) >= 150:
            mes = _('The request is long ({} symbols). Do you really want to send it?')
            mes = mes.format(len(objs.request.search))
            if not Message(f, mes, True).show_question():
                Confirmed = False
        return Confirmed
    
    def get_colnum(self):
        ''' A subject from the 'Phrases' section usually has an 'original +
            translation' structure, so we need to switch off sorting terms and
            ensure that the number of columns is divisible by 2.
        '''
        if not self.is_parallel() or CONFIG.new['columns']['num'] % 2 == 0:
            return CONFIG.new['columns']['num']
        if CONFIG.new['columns']['num'] > 2:
            return CONFIG.new['columns']['num'] - 1
        return 2
    
    def export_style(self):
        f = '[MClient] logic.Commands.export_style'
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0.6s slower.
        '''
        lst = [choice for choice in (CONFIG.new['columns']['1']['type']
                                    ,CONFIG.new['columns']['2']['type']
                                    ,CONFIG.new['columns']['3']['type']
                                    ,CONFIG.new['columns']['4']['type']
                                    ) \
               if choice != _('Do not set')]
        ''' #NOTE: The following assignment does not change the list:
            for item in lst:
                if item == something:
                    item = something_else
        '''
        for i in range(len(lst)):
            if lst[i] == _('Subjects'):
                lst[i] = 'subj'
            elif lst[i] == _('Word forms'):
                lst[i] = 'wform'
            elif lst[i] == _('Parts of speech'):
                lst[i] = 'speech'
            elif lst[i] == _('Transcription'):
                lst[i] = 'transc'
            else:
                sub = (_('Subjects'), _('Word forms'), _('Transcription')
                      ,_('Parts of speech')
                      )
                sub = '; '.join(sub)
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(lst[i], sub)
                Message(f, mes, True).show_error()
        if not lst:
            rep.lazy(f)
            return
        objs.get_request().cols = tuple(lst)
        #TODO: Should we change objs.request.collimit here?
    
    def suggest(self, search, limit=0):
        f = '[MClient] logic.Commands.suggest'
        items = objs.get_plugins().suggest(search)
        if not items:
            rep.empty(f)
            return []
        return items[0:limit]
        
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



class Search(Table):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def check(self):
        f = '[MClient] logic.Search.check'
        if not self.plain or not self.pattern.strip():
            self.Success = False
            rep.empty(f)
    
    def lower(self):
        f = '[MClient] logic.Search.lower'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.Case:
            self.pattern = self.pattern.lower()
            plain = []
            for row in self.plain:
                row = [item.lower() for item in row]
                plain.append(row)
            self.plain = plain
    
    def reset(self, plain, pattern, rowno, colno, Case=False):
        self.set_values()
        self.plain = plain
        self.pattern = pattern
        self.rowno = rowno
        self.colno = colno
        self.Case = Case
        self.check()
        self.set_size()
        self.lower()
    
    def set_values(self):
        self.plain = []
        self.Success = True
        self.Case = False
        self.rownum = 0
        self.colnum = 0
        self.rowno = 0
        self.colno = 0
        self.pattern = ''
    
    def _has_pattern(self):
        for rowno in range(self.rownum):
            for colno in range(self.colnum):
                if self.pattern in self.plain[rowno][colno]:
                    return True
    
    def search_next(self):
        f = '[MClient] logic.Search.search_next'
        if not self.Success:
            rep.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_next_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        Message(f, mes).show_debug()
        return(rowno, colno)
    
    def search_prev(self):
        f = '[MClient] logic.Search.search_prev'
        if not self.Success:
            rep.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_prev_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}. Text: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        Message(f, mes).show_debug()
        return(rowno, colno)
    
    def _get_next_col(self, rowno, colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno, colno)
    
    def _get_prev_col(self, rowno, colno):
        while colno > 0:
            colno -= 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno, colno)


objs = Objects()
com = Commands()
