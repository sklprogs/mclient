#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import ssl

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.web as wb

import config as cf
import manager


class Speech:
    ''' It's OK to recreate this class each time it runs since the speech
        dictionary is reused and not recreated.
    '''
    def __init__(self):
        self.dic = objs.get_plugins().get_speeches()
    
    def _get_short(self, full):
        f = '[MClientQt] logic.Speech._get_short'
        for short in self.dic:
            if self.dic[short] == full:
                return short
        mes = _('Wrong input data: "{}"!').format(full)
        sh.objs.get_mes(f, mes, True).show_warning()
        return full
    
    def get_settings(self):
        #f = '[MClientQt] logic.Speech.get_settings'
        # Source tuple cannot be concatenated with target list
        speeches = [cf.objs.get_config().new['speech1']
                   ,cf.objs.config.new['speech2']
                   ,cf.objs.config.new['speech3']
                   ,cf.objs.config.new['speech4']
                   ,cf.objs.config.new['speech5']
                   ,cf.objs.config.new['speech6']
                   ,cf.objs.config.new['speech7']
                   ]
        if not self.dic:
            return speeches
        if not cf.objs.config.new['ShortSpeech']:
            return speeches
        for i in range(len(speeches)):
            speeches[i] = self._get_short(speeches[i])
        #mes = ', '.join(speeches)
        #sh.objs.get_mes(f, mes, True).show_debug()
        return speeches



class Articles:
    
    def __init__(self):
        self.reset()
    
    def set_values(self):
        self.id = -1
        self.articles = {'ids' : {}}
    
    def reset(self):
        self.set_values()
    
    def get_blocked(self):
        f = '[MClientQt] logic.Articles.get_blocked'
        try:
            return self.articles['ids'][self.id]['blocked']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return []
    
    def get_prioritized(self):
        f = '[MClientQt] logic.Articles.get_prioritized'
        try:
            return self.articles['ids'][self.id]['prioritized']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return []
    
    def get_subjf(self):
        f = '[MClientQt] logic.Articles.get_subjf'
        try:
            return self.articles['ids'][self.id]['subjf']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def get_fixed_urls(self):
        f = '[MClientQt] logic.Articles.get_fixed_urls'
        try:
            return self.articles['ids'][self.id]['fixed_urls']
        except KeyError:
            sh.com.rep_input(f)
        return {}
    
    def is_last(self):
        return self.id == self.get_max_id()
    
    def get_max_id(self):
        f = '[MClientQt] logic.Articles.get_max_id'
        try:
            # Do not use 'max' on an empty sequence
            return len(self.articles['ids']) - 1
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return -1
    
    def set_table(self, table):
        f = '[MClientQt] logic.Articles.set_table'
        try:
            self.articles['ids'][self.id]['table'] = table
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def get_table(self):
        f = '[MClientQt] logic.Articles.get_table'
        try:
            return self.articles['ids'][self.id]['table']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def get_cell(self, rowno, colno):
        f = '[MClientQt] logic.Articles.get_cell'
        try:
            return self.articles['ids'][self.id]['table'][rowno][colno]
        except (KeyError, IndexError):
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def get_len(self):
        return self.get_max_id() + 1
    
    def add (self, search='', url='', cells=[], table=[], raw_code=''
            ,fixed_urls=[], subjf=[], blocked=[], prioritized=[]
            ):
        f = '[MClientQt] logic.Articles.add'
        # Do not add articles that were not found to history
        if not cells:
            sh.com.rep_lazy(f)
            return
        id_ = self.get_max_id() + 1
        self.articles['ids'][id_] = {'source'        : cf.objs.get_config().new['source']
                                    ,'lang1'         : objs.get_plugins().get_lang1()
                                    ,'lang2'         : objs.plugins.get_lang2()
                                    ,'Parallel'      : objs.plugins.is_parallel()
                                    ,'Separate'      : objs.plugins.is_separate()
                                    ,'search'        : search
                                    ,'url'           : url
                                    ,'cells'         : cells
                                    ,'table'         : table
                                    ,'raw_code'      : raw_code
                                    ,'fixed_urls'    : fixed_urls
                                    ,'subjf'         : subjf
                                    ,'blocked'       : blocked
                                    ,'prioritized'   : prioritized
                                    ,'rowno'         : -1
                                    ,'colno'         : -1
                                    ,'blocked_cells' : []
                                    }
        self.set_id(id_)
    
    def get_blocked_cells(self):
        f = '[MClientQt] logic.Articles.get_blocked_cells'
        try:
            return self.articles['ids'][self.id]['blocked_cells']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def set_blocked_cells(self, texts):
        f = '[MClientQt] logic.Articles.set_blocked_cells'
        try:
            self.articles['ids'][self.id]['blocked_cells'] = texts
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def clear_article(self):
        f = '[MClientQt] logic.Articles.clear_article'
        try:
            del self.articles['ids'][self.id]
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
            return
        if self.id > 0:
            self.set_id(self.id-1)
        else:
            self.id = -1
    
    def delete_bookmarks(self):
        f = '[MClientQt] logic.Articles.delete_bookmarks'
        try:
            self.articles['ids']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
            return
        for id_ in self.articles['ids']:
            self.articles['ids'][id_]['rowno'] = -1
            self.articles['ids'][id_]['colno'] = -1
    
    def set_bookmark(self, rowno, colno):
        f = '[MClientQt] logic.Articles.set_bookmark'
        try:
            self.articles['ids'][self.id]['rowno'] = rowno
            self.articles['ids'][self.id]['colno'] = colno
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def get_bookmark(self):
        f = '[MClientQt] logic.Articles.get_bookmark'
        try:
            return (self.articles['ids'][self.id]['rowno']
                   ,self.articles['ids'][self.id]['colno']
                   )
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def set_id(self, id_):
        f = '[MClientQt] logic.Articles.set_id'
        try:
            self.articles['ids'][id_]
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(id_)
            sh.objs.get_mes(f, mes).show_warning()
            return
        self.id = id_
    
    def get_search(self):
        f = '[MClientQt] logic.Articles.get_search'
        try:
            return self.articles['ids'][self.id]['search']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_source(self):
        f = '[MClientQt] logic.Articles.get_source'
        try:
            return self.articles['ids'][self.id]['source']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_url(self):
        f = '[MClientQt] logic.Articles.get_url'
        try:
            return self.articles['ids'][self.id]['url']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_lang1(self):
        f = '[MClientQt] logic.Articles.get_lang1'
        try:
            return self.articles['ids'][self.id]['lang1']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_lang2(self):
        f = '[MClientQt] logic.Articles.get_lang2'
        try:
            return self.articles['ids'][self.id]['lang2']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_raw_code(self):
        f = '[MClientQt] logic.Articles.get_raw_code'
        try:
            return self.articles['ids'][self.id]['raw_code']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return ''
    
    def get_cells(self):
        f = '[MClientQt] logic.Articles.get_cells'
        try:
            return self.articles['ids'][self.id]['cells']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
        return []
    
    def find(self, source, search, url):
        f = '[MClientQt] logic.Articles.find'
        try:
            self.articles['ids']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
            return
        for id_ in self.articles['ids']:
            if self.articles['ids'][id_]['source'] == source \
            and self.articles['ids'][id_]['search'] == search \
            and self.articles['ids'][id_]['url'] == url:
                return id_
        return -1
    
    def is_parallel(self):
        f = '[MClientQt] logic.Articles.is_parallel'
        try:
            return self.articles['ids'][self.id]['Parallel']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()
    
    def is_separate(self):
        f = '[MClientQt] logic.Articles.is_separate'
        try:
            return self.articles['ids'][self.id]['Separate']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f, mes).show_warning()



class App:
    
    def open_in_browser(self):
        ionline = sh.Online()
        url = objs.get_request().url
        ionline.url = objs.get_plugins().fix_url(url)
        ionline.browse()
    
    def print(self):
        f = '[MClient] logic.App.print'
        code = wb.WebPage(objs.get_request().htm).make_pretty()
        if not code:
            sh.com.rep_empty(f)
            return
        tmp_file = sh.objs.get_tmpfile (suffix = '.htm'
                                       ,Delete = 0
                                       )
        sh.WriteTextFile (file = tmp_file
                         ,Rewrite = True
                         ).write(code)
        sh.Launch(tmp_file).launch_default()



class HTM:

    def __init__(self, cells, skipped=0):
        ''' - Takes ~0.01s for 'set' on AMD E-300.
            - 'collimit' includes fixed blocks.
        '''
        self.set_values()
        self.cells = cells
        self.skipped = skipped
        
    def set_landscape(self):
        f = '[MClientQt] logic.HTM.set_landscape'
        file = sh.objs.get_pdir().add('..', 'resources', 'landscape.html')
        code = sh.ReadTextFile(file).get()
        if not code:
            sh.com.rep_empty(f)
            return
        if not '%s' in code:
            mes = _('Wrong input data: "{}"!').format(code)
            sh.objs.get_mes(f, mes).show_warning()
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
        f = '[MClientQt] logic.ColumnWidth.set_col_width'
        if not cf.objs.get_config().new['rows']['height']:
            sh.com.rep_lazy(f)
            return
        for column in self.columns:
            if column.Fixed:
                column.width = cf.objs.config.new['columns']['fixed']['width']
            else:
                column.width = cf.objs.config.new['columns']['terms']['width']
#            if objs.get_blocksdb().is_col_empty(column.no):
#                column.width = self.min_width
#            elif column.Fixed:
#                column.width = cf.objs.config.new['columns']['fixed']['width']
#            else:
#                column.width = cf.objs.config.new['columns']['terms']['width']
    
    def reset(self):
        self.set_values()
    
    def run(self):
        self.set_fixed_num()
        self.set_term_num()
        self.set_columns()
        self.set_col_width()
    
    def set_fixed_num(self):
        f = '[MClientQt] logic.ColumnWidth.set_fixed_num'
        self.fixed_num = 4
        mes = _('Number of fixed columns: {}').format(self.fixed_num)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def set_term_num(self):
        f = '[MClientQt] logic.ColumnWidth.set_term_num'
        self.term_num = com.get_colnum()
        mes = _('Number of term columns: {}')
        mes = mes.format(self.term_num)
        sh.objs.get_mes(f, mes, True).show_debug()
    
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
        self.collimit = cf.objs.get_config().new['columns']['num'] + len(self.cols)
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
        return sh.Home(cf.PRODUCT_LOW).add_config('dics')
    
    def get_plugins(self, Debug=False, maxrows=1000):
        if self.plugins is None:
            self.plugins = manager.Plugins (sdpath = self.get_dics()
                                           ,mbpath = self.get_dics()
                                           ,timeout = cf.objs.get_config().new['timeout']
                                           ,Debug = Debug
                                           ,maxrows = maxrows
                                           )
        return self.plugins
    
    def get_request(self):
        if self.request is None:
            self.request = CurRequest()
        return self.request



class Commands:
    
    def __init__(self):
        self.use_unverified()
    
    def _get_col_type(self, type_):
        f = '[MClientQt] logic.Commands._get_col_type'
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
            sh.objs.get_mes(f, mes).show_error()
        return ''
    
    def get_col_types(self):
        f = '[MClientQt] logic.Commands.get_col_types'
        types = [cf.objs.get_config().new['columns']['1']['type']
                ,cf.objs.config.new['columns']['2']['type']
                ,cf.objs.config.new['columns']['3']['type']
                ,cf.objs.config.new['columns']['4']['type']
                ]
        for i in range(len(types)):
            types[i] = self._get_col_type(types[i])
        mes = ', '.join(types)
        sh.objs.get_mes(f, mes, True).show_debug()
        return types
    
    def is_parallel(self):
        return objs.get_articles().get_len() > 0 and objs.articles.is_parallel()
    
    def is_separate(self):
        return objs.get_articles().get_len() > 0 and objs.articles.is_separate()
    
    def get_text(self, cells):
        f = '[MClientQt] logic.Commands.get_text'
        if not cells:
            sh.com.rep_empty(f)
            return ''
        return '\n'.join([cell.plain for cell in cells])
    
    def fix_colors(self, colors):
        ''' We need HTML code both in cells and output to be saved. Qt requires
            that color names are put in quotes; however, browsers do not
            understand color names in quotes, so we must delete these quotes
            before saving to a web-page.
        '''
        f = '[MClientQt] logic.Commands.fix_colors'
        if not colors:
            sh.com.rep_empty(f)
            return
        for color in colors:
            objs.get_request().htm = objs.request.htm.replace(f"'{color}'", color)
    
    def get_colors(self, blocks):
        f = '[MClientQt] logic.Commands.get_colors'
        if not blocks:
            sh.com.rep_empty(f)
            return
        colors = []
        for block in blocks:
            if not block.color in colors:
                colors.append(block.color)
        return colors
    
    def set_url(self):
        f = '[MClientQt] logic.Commands.set_url'
        #NOTE: update source and target languages first
        objs.get_request().url = objs.get_plugins().get_url(objs.request.search)
        mes = objs.request.url
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def control_length(self):
        # Confirm too long requests
        f = '[MClientQt] logic.Commands.control_length'
        Confirmed = True
        if len(objs.get_request().search) >= 150:
            mes = _('The request is long ({} symbols). Do you really want to send it?')
            mes = mes.format(len(objs.request.search))
            if not sh.objs.get_mes(f, mes).show_question():
                Confirmed = False
        return Confirmed
    
    def get_colnum(self):
        ''' A subject from the 'Phrases' section usually has an 'original +
            translation' structure, so we need to switch off sorting terms and
            ensure that the number of columns is divisible by 2.
        '''
        if not self.is_parallel() or cf.objs.get_config().new['columns']['num'] % 2 == 0:
            return cf.objs.get_config().new['columns']['num']
        if cf.objs.get_config().new['columns']['num'] > 2:
            return cf.objs.config.new['columns']['num'] - 1
        return 2
    
    def export_style(self):
        f = '[MClientQt] logic.Commands.export_style'
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0.6s slower.
        '''
        lst = [choice for choice in (cf.objs.get_config().new['columns']['1']['type']
                                    ,cf.objs.config.new['columns']['2']['type']
                                    ,cf.objs.config.new['columns']['3']['type']
                                    ,cf.objs.config.new['columns']['4']['type']
                                    ) \
               if choice != _('Do not set')
              ]
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
                sh.objs.get_mes(f, mes).show_error()
        if not lst:
            sh.com.rep_lazy(f)
            return
        objs.get_request().cols = tuple(lst)
        #TODO: Should we change objs.request.collimit here?
    
    def suggest(self, search, limit=0):
        f = '[MClientQt] logic.Commands.suggest'
        items = objs.get_plugins().suggest(search)
        if not items:
            sh.com.rep_empty(f)
            return []
        return items[0:limit]
        
    def use_unverified(self):
        f = '[MClientQt] logic.Commands.use_unverified'
        ''' On *some* systems we can get urllib.error.URLError: <urlopen error
            [SSL: CERTIFICATE_VERIFY_FAILED]>. To get rid of this error, we use
            this small workaround.
        '''
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            mes = _('Unable to use unverified certificates!')
            sh.objs.get_mes(f, mes, True).show_warning()



class Table:
    ''' #NOTE: it's not enough to use 'Success' since we do not call 'reset'
        before loading an article.
    '''
    def __init__(self, plain=[], code=[]):
        self.set_values()
        if plain and code:
            self.reset(plain, code)
    
    def reset(self, plain, code):
        self.set_values()
        self.plain = plain
        self.code = code
        self.set_size()
        self.set_empty_cols()
    
    def set_values(self):
        self.plain = []
        self.code = []
        self.empty_cols = []
        self.rownum = 0
        self.colnum = 0
        ''' This is a constant value and should be manually changed only when
            new fixed types are introduced.
        '''
        self.fixed_num = 4
    
    def get_phsubj(self):
        f = '[MClientQt] logic.Table.get_phsubj'
        table = objs.get_articles().get_table()
        if not table:
            sh.com.rep_empty(f)
            return
        for row in table[::-1]:
            for cell in row:
                if cell.fixed_block and cell.fixed_block.type == 'phsubj':
                    return(cell.text, cell.fixed_block.url)
    
    def get_first_term(self):
        f = '[MClientQt] logic.Table.get_first_term'
        table = objs.get_articles().get_table()
        if not table:
            sh.com.rep_empty(f)
            return
        for row in table:
            for cell in row:
                for block in cell.blocks:
                    if block.type == 'term' and block.text.strip():
                        return(cell.rowno, cell.colno)
    
    def _is_col_empty(self, colno):
        for rowno in range(self.rownum):
            # Cell texts should already be stripped
            if self.plain[rowno][colno]:
                return
        return True
    
    def set_empty_cols(self):
        f = '[MClientQt] logic.Table.set_empty_cols'
        #TODO: Should we run this for fixed columns only?
        for colno in range(self.colnum):
            if self._is_col_empty(colno):
                self.empty_cols.append(colno)
        if self.empty_cols:
            mes = _('Columns with no text: {}')
            mes = mes.format(', '.join([str(item) for item in self.empty_cols]))
        else:
            mes = _('All columns have texts')
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def get_next_row_by_col(self, rowno, colno, ref_colno):
        f = '[MClientQt] logic.Table.get_next_row_by_col'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        tuple_ = self._get_next_row(rowno, ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_next_row(rowno - 1, colno)
            if tuple_:
                return tuple_
        elif rowno > 0:
            return self.get_next_row_by_col(-1, colno, ref_colno)
        return(rowno, colno)
    
    def get_prev_row_by_col(self, rowno, colno, ref_colno):
        f = '[MClientQt] logic.Table.get_prev_row_by_col'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        tuple_ = self._get_prev_row(rowno, ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_prev_row(rowno + 1, colno)
            if tuple_:
                return tuple_
        elif rowno < self.rownum:
            return self.get_prev_row_by_col(self.rownum, colno, ref_colno)
        return(rowno, colno)
    
    def _get_next_col(self, rowno, colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_next_col(self, rowno, colno):
        f = '[MClientQt] logic.Table.get_next_col'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        start = rowno
        while rowno < self.rownum:
            if rowno == start:
                tuple_ = self._get_next_col(rowno, colno)
            else:
                tuple_ = self._get_next_col(rowno, -1)
            if tuple_:
                return tuple_
            rowno += 1
        if colno + 1 < self.colnum:
            colno += 1
        if rowno >= self.rownum:
            return self.get_start()
        return(rowno, colno)
    
    def _get_prev_col(self, rowno, colno):
        while colno > 0:
            colno -= 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_prev_col(self, rowno, colno):
        f = '[MClientQt] logic.Table.get_prev_col'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        start = rowno
        while rowno >= 0:
            if rowno == start:
                tuple_ = self._get_prev_col(rowno, colno)
            else:
                tuple_ = self._get_prev_col(rowno, self.colnum)
            if tuple_:
                return tuple_
            rowno -= 1
        if colno > 0:
            colno -= 1
        if rowno < 0:
            return self.get_end()
        return(rowno, colno)
    
    def _get_prev_row(self, rowno, colno):
        while rowno > 0:
            rowno -= 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_prev_row(self, rowno, colno):
        f = '[MClientQt] logic.Table.get_prev_row'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        start = colno
        while colno >= 0:
            if start == colno:
                tuple_ = self._get_prev_row(rowno, colno)
            else:
                tuple_ = self._get_prev_row(self.rownum, colno)
            if tuple_:
                return tuple_
            colno -= 1
        if colno < 0:
            return self.get_end()
        return(rowno, colno)
    
    def _get_next_row(self, rowno, colno):
        while rowno + 1 < self.rownum:
            rowno += 1
            if self.plain[rowno][colno]:
                return(rowno, colno)
    
    def get_next_row(self, rowno, colno):
        f = '[MClientQt] logic.Table.get_next_row'
        if not self.plain:
            sh.com.rep_empty(f)
            return(rowno, colno)
        start = colno
        while colno < self.colnum:
            if start == colno:
                tuple_ = self._get_next_row(rowno, colno)
            else:
                tuple_ = self._get_next_row(-1, colno)
            if tuple_:
                return tuple_
            colno += 1
        if colno >= self.colnum:
            return self.get_start()
        return(rowno, colno)
    
    def get_start(self):
        return self.get_next_col(0, -1)
    
    def get_line_start(self, rowno):
        return self.get_next_col(rowno, -1)
    
    def get_line_end(self, rowno):
        return self.get_prev_col(rowno, self.colnum)
    
    def set_size(self):
        f = '[MClientQt] logic.Table.set_size'
        if not self.plain:
            sh.com.rep_empty(f)
            return
        self.rownum = len(self.plain)
        self.colnum = len(self.plain[0])
        mes = _('Table size: {}×{}').format(self.rownum, self.colnum)
        sh.objs.get_mes(f, mes, True).show_debug()
    
    def get_end(self):
        return self.get_prev_col(self.rownum - 1, self.colnum)



class Search(Table):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def check(self):
        f = '[MClientQt] logic.Search.check'
        if not self.plain or not self.pattern.strip():
            self.Success = False
            sh.com.rep_empty(f)
    
    def lower(self):
        f = '[MClientQt] logic.Search.lower'
        if not self.Success:
            sh.com.cancel(f)
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
        f = '[MClientQt] logic.Search.search_next'
        if not self.Success:
            sh.com.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_next_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        sh.objs.get_mes(f, mes, True).show_debug()
        return(rowno, colno)
    
    def search_prev(self):
        f = '[MClientQt] logic.Search.search_prev'
        if not self.Success:
            sh.com.cancel(f)
            return(self.rowno, self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno, self.colno)
        rowno, colno = self.get_prev_col(self.rowno, self.colno)
        mes = _('Row #{}. Column #{}. Text: "{}"')
        mes = mes.format(rowno, colno, self.plain[rowno][colno])
        sh.objs.get_mes(f, mes, True).show_debug()
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
