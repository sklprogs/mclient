#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import ssl

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import manager
import subjects.subjects as sj
import config as cf
import db


SPORDER = (_('Noun'),_('Verb'),_('Adjective'),_('Abbreviation')
          ,_('Adverb'),_('Preposition'),_('Pronoun')
          )


class HTM:

    def __init__(self,cells,skipped=0):
        # 'collimit' includes fixed blocks
        self.set_values()
        self.cells = cells
        self.skipped = skipped
        
    def set_landscape(self):
        f = '[MClientQt] logic.HTM.set_landscape'
        file = sh.objs.get_pdir().add('..','resources','landscape.html')
        code = sh.ReadTextFile(file).get()
        if not code:
            sh.com.rep_empty(f)
            return
        if not '%s' in code:
            mes = _('Wrong input data: "{}"!').format(code)
            sh.objs.get_mes(f,mes).show_warning()
            return
        # Either don't use 'format' here or double all curly braces in script
        self.landscape = code % _('Print')
    
    def run(self):
        # Takes ~0.015s for 'set' on Intel Atom
        self.set_landscape()
        self.generate()
        return self.htm
    
    def set_values(self):
        self.htm = ''
        self.landscape = ''
        self.skipped = 0
    
    def generate(self):
        f = '[MClientQt] logic.HTM.generate'
        code = ['<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">']
        code.append(self.landscape)
        code.append('<div id="printableArea">')
        if self.cells:
            code.append('<table>')
            old_colno = -1
            old_rowno = -1
            for icell in self.cells:
                if old_rowno != icell.rowno:
                    if icell.rowno > 0:
                        code.append('</td></tr>')
                    code.append('<tr>')
                ''' #NOTE: Without checking a row number here finding text may
                    fail in the vertical mode when 2 cells have a different row
                    number but the same column number.
                '''
                if old_rowno != icell.rowno or old_colno != icell.colno:
                    if icell.colno > 0 and old_rowno == icell.rowno:
                        code.append('</td>')
                    ''' #TODO: Port this old code
                    if old_rowno == icell.rowno:
                        delta = icell.colno - old_colno - 1
                    else:
                        delta = icell.colno
                    for i in range(delta):
                        col_width = objs.get_fonts()._get_col_width(i)
                        sub = '<td width="{}"/>'
                        sub = sub.format(col_width)
                        code.append(sub)
                    sub = '<td{} valign="top"{}>'
                    if icell.block.Fixed:
                        sub1 = ' align="center"'
                    else:
                        sub1 = ''
                    if ifont.col_width:
                        sub2 = ' width="{}"'
                        sub2 = sub2.format(ifont.col_width)
                    else:
                        sub2 = ''
                    sub = sub.format(sub1,sub2)
                    '''
                    sub = '<td valign="top">'
                    code.append(sub)
                    old_colno = icell.colno
                ''' Cannot be modified immediately after a new row was
                    discovered since 'rowno' is used after that.
                '''
                if old_rowno != icell.rowno:
                    old_rowno = icell.rowno
                code.append(icell.code)
            code.append('</td></tr></table>')
        elif self.skipped:
            code.append('<h1>')
            mes = _('Nothing has been found (skipped subjects: {}).')
            mes = mes.format(self.skipped)
            code.append(mes)
            code.append('</h1>')
        else:
            code.append('<h1>')
            code.append(_('Nothing has been found.'))
            code.append('</h1>')
        code.append('</div>')
        code.append('</meta></body></html>')
        self.htm = ''.join(code)



class Source:
    
    def __init__(self):
        self.title = ''
        self.status = _('not running')
        self.color = 'red'
        self.Online = False



class Block:
    
    def __init__(self):
        self.type_ = 'invalid'
        self.text = ''
        self.url = ''
        self.no = -1
        self.rowno = -1
        self.colno = -1
        self.cellno = -1
        self.family = 'Serif'
        self.color = 'black'
        self.size = 12
        self.Bold = False
        self.Italic = False



class Cell:
    
    def __init__(self):
        self.code = ''
        self.plain = ''
        self.url = ''
        self.no = -1
        self.rowno = -1
        self.colno = -1



class Column:
    
    def __init__(self):
        self.no = 0
        self.width = 0
        self.Fixed = False



class ColumnWidth:
    ''' Adjust fixed columns to have a constant width. A fixed value
        in pixels rather than percentage should be used to adjust
        columns since we cannot say if gaps between columns are too
        large without calculating a text width first.
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
        if not sh.lg.globs['bool']['AdjustByWidth']:
            sh.com.rep_lazy(f)
            return
        for column in self.columns:
            if objs.get_blocksdb().is_col_empty(column.no):
                column.width = self.min_width
            elif column.Fixed:
                column.width = sh.lg.globs['int']['fixed_col_width']
            else:
                column.width = sh.lg.globs['int']['term_col_width']
    
    def reset(self):
        self.set_values()
    
    def run(self):
        self.set_fixed_num()
        self.set_term_num()
        self.set_columns()
        self.set_col_width()
    
    def set_fixed_num(self):
        f = '[MClientQt] logic.ColumnWidth.set_fixed_num'
        if sh.lg.globs['bool']['VerticalView']:
            sh.com.rep_lazy(f)
            return
        columns = objs.get_blocksdb().get_fixed_cols()
        if columns:
            self.fixed_num = len(columns)
            mes = _('An actual number of fixed columns: {}')
            mes = mes.format(self.fixed_num)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_lazy(f)
    
    def set_term_num(self):
        f = '[MClientQt] logic.ColumnWidth.set_term_num'
        self.term_num = sh.lg.globs['int']['colnum']
        mes = _('Number of term columns: {}')
        mes = mes.format(self.term_num)
        sh.objs.get_mes(f,mes,True).show_debug()
    
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



class SpeechPrior:
    
    def __init__(self,order=SPORDER):
        self.reset(order)
    
    def reset(self,order=SPORDER):
        self.set_values()
        self.order = order
        self.check()
        self.prioritize()
    
    def get_abbr2full(self):
        f = '[MClientQt] logic.SpeechPrior.get_abbr2full'
        if self.Success:
            if not self.abbr2full:
                for i in range(len(self.abbr)):
                    self.abbr2full[self.abbr[i]] = self.full[i]
        else:
            sh.com.cancel(f)
        return self.abbr2full
    
    def get_full2abbr(self):
        f = '[MClientQt] logic.SpeechPrior.get_full2abbr'
        if self.Success:
            if not self.full2abbr:
                for i in range(len(self.full)):
                    self.full2abbr[self.full[i]] = self.abbr[i]
        else:
            sh.com.cancel(f)
        return self.full2abbr
    
    def get_all2prior(self):
        f = '[MClientQt] logic.SpeechPrior.get_all2prior'
        seq = {}
        if self.Success:
            for i in range(len(self.prior)):
                seq[self.abbr[i]] = self.prior[i]
                seq[self.full[i]] = self.prior[i]
        else:
            sh.com.cancel(f)
        return seq
    
    def debug(self):
        self.debug_all2prior()
        self.debug_pairs()
    
    def debug_all2prior(self):
        f = '[MClientQt] logic.SpeechPrior.debug_all2prior'
        if self.Success:
            all2prior = self.get_all2prior()
            if all2prior:
                all_ = all2prior.keys()
                prior = [all2prior.get(key) for key in all2prior.keys()]
                headers = (_('NAME'),_('PRIORITY'))
                iterable = [all_,prior]
                mes = sh.FastTable(iterable,headers).run()
                sh.com.run_fast_debug(f,mes)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def _debug_full2abbr(self):
        f = '[MClientQt] logic.SpeechPrior._debug_full2abbr'
        full2abbr = self.get_full2abbr()
        if full2abbr:
            full = sorted(full2abbr.keys())
            abbr = [full2abbr.get(item) for item in full]
            headers = (_('NAME'),_('ABBREVIATION'))
            iterable = [full,abbr]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_empty(f)
    
    def _debug_abbr2full(self):
        f = '[MClientQt] logic.SpeechPrior._debug_abbr2full'
        abbr2full = self.get_abbr2full()
        if abbr2full:
            abbr = sorted(abbr2full.keys())
            full = [abbr2full.get(item) for item in abbr]
            headers = (_('ABBREVIATION'),_('NAME'))
            iterable = [abbr,full]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_empty(f)
    
    def debug_pairs(self):
        f = '[MClientQt] logic.SpeechPrior.debug_pairs'
        if self.Success:
            self._debug_full2abbr()
            self._debug_abbr2full()
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClientQt] logic.SpeechPrior.prioritize'
        if self.Success:
            lst = [i + 1 for i in range(len(self.abbr))]
            for i in range(len(self.order)):
                try:
                    ind = self.full.index(self.order[i])
                    self.prior[ind] = lst[i]
                except ValueError:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(self.order[i])
                    sh.objs.get_mes(f,mes,True).show_warning()
            lst = lst[len(self.order):]
            try:
                ind = self.full.index(_('Phrase'))
                self.prior[ind] = 1000
                lst = lst[:-1]
            except ValueError:
                pass
            j = 0
            for i in range(len(self.prior)):
                if self.prior[i] == -1:
                    self.prior[i] = lst[j]
                    j += 1
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClientQt] logic.SpeechPrior.check'
        if len(self.abbr):
            if len(self.abbr) == len(self.full):
                if len(self.order) > len(self.abbr):
                    self.Success = False
                    sub = '{} <= {}'.format (len(self.order)
                                            ,len(self.abbr)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                self.Success = False
                sub = '{} == {}'.format(len(self.abbr),len(self.full))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.abbr = [_('abbr.')
                    ,_('adj')
                    ,_('adv.')
                    ,_('art.')
                    ,_('conj.')
                    ,_('form')
                    ,_('interj.')
                    ,_('n')
                    ,_('num.')
                    ,_('ord.num.')
                    ,_('part.')
                    ,_('phrase')
                    ,_('predic.')
                    ,_('prepos.')
                    ,_('pron')
                    ,_('suf')
                    ,_('v')
                    ]
        self.full = [_('Abbreviation')
                    ,_('Adjective')
                    ,_('Adverb')
                    ,_('Article')
                    ,_('Conjunction')
                    ,_('Form')
                    ,_('Interjection')
                    ,_('Noun')
                    ,_('Numeral')
                    ,_('Ordinal Numeral')
                    ,_('Particle')
                    ,_('Phrase')
                    ,_('Predicative')
                    ,_('Preposition')
                    ,_('Pronoun')
                    ,_('Suffix')
                    ,_('Verb')
                    ]
        self.prior = [-1 for i in range(len(self.abbr))]
        self.Success = True
        self.abbr2full = {}
        self.full2abbr = {}



class CurRequest:

    def __init__(self):
        self.set_values()
        self.reset()
    
    def set_values(self):
        self.cols = ('dic','wform','transc','speech')
        self.collimit = sh.lg.globs['int']['colnum'] + len(self.cols)
        ''' Toggling blacklisting should not depend on a number of blocked
            subjects (otherwise, it is not clear how blacklisting should be
            toggled).
            *Temporarily* turn off prioritizing and terms sorting for articles
            with 'sep_words_found' and in phrases; use previous settings for
            new articles.
        '''
        self.SpecialPage = False
        self.NewPageType = False
        self.DefColNumEven = False
    
    def reset(self):
        self.htm = ''
        self.search = ''
        self.url = ''



class Lists:
    # Read the blocklist and the prioritize list
    def __init__(self):
        f = '[MClientQt] logic.Lists.__init__'
        self.blacklst = objs.get_default().fblock
        self.priorlst = objs.default.fprior
        self.Success = objs.default.Success
    
    def get_blacklist(self):
        f = '[MClientQt] logic.Lists.get_blacklist'
        if self.Success:
            text = sh.ReadTextFile(self.blacklst,True).get()
            text = sh.Text(text,True).text
            return text.splitlines()
        else:
            sh.com.cancel(f)

    def get_priorities(self):
        f = '[MClientQt] logic.Lists.get_priorities'
        if self.Success:
            text = sh.ReadTextFile(self.priorlst,True).get()
            text = sh.Text(text,True).text
            return text.splitlines()
        else:
            sh.com.cancel(f)



class Objects:
    
    def __init__(self):
        self.online = self.request = self.order = self.default \
                    = self.plugins = self.speech_prior = self.config \
                    = self.order = self.blocksdb = self.column_width \
                    = self.colors = None

    def get_colors(self):
        if self.colors is None:
            self.colors = Colors()
        return self.colors
    
    def get_column_width(self):
        if self.column_width is None:
            self.column_width = ColumnWidth()
        return self.column_width
    
    def get_blocksdb(self):
        if self.blocksdb is None:
            self.blocksdb = db.Moves()
            self.blocksdb.Selectable = sh.lg.globs['bool']['SelectTermsOnly']
        return self.blocksdb
    
    def get_order(self):
        if self.order is None:
            self.order = sj.objs.order = Order()
        return self.order
    
    def get_config(self):
        if self.config is None:
            self.config = sh.Config(objs.get_default().get_config())
            self.config.run()
        return self.config
    
    def get_speech_prior(self,order=[]):
        if self.speech_prior is None:
            self.speech_prior = SpeechPrior(order)
        return self.speech_prior
    
    def get_plugins(self,Debug=False,maxrows=1000):
        if self.plugins is None:
            self.plugins = manager.Plugins (sdpath = self.get_default().get_dics()
                                           ,mbpath = self.default.get_dics()
                                           ,timeout = sh.lg.globs['float']['timeout']
                                           ,Debug = Debug
                                           ,maxrows = maxrows
                                           )
        return self.plugins
    
    def get_default(self,product='mclient'):
        if not self.default:
            self.default = cf.DefaultConfig(product)
            self.default.run()
        return self.default
    
    def get_request(self):
        if self.request is None:
            self.request = CurRequest()
        return self.request



class Commands:
    
    def __init__(self):
        self.use_unverified()
    
    def fix_colors(self,colors):
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
            if not color.startswith('#'):
                continue
            objs.get_request().htm = objs.request.htm.replace(f"'{color}'",color)
    
    def get_colors(self,blocks):
        f = '[MClientQt] logic.Commands.get_colors'
        if not blocks:
            sh.com.rep_empty(f)
            return
        colors = []
        for block in blocks:
            if not block.color in colors:
                colors.append(block.color)
        return colors
    
    def get_cell(self,cells,rowno,colno):
        #TODO: Convert cells to have list-in-list structure and delete
        f = '[MClientQt] logic.Commands.get_cell'
        if not cells:
            sh.com.rep_empty(f)
            return
        for cell in cells:
            if cell.rowno == rowno and cell.colno == colno:
                return cell
    
    def start(self):
        ''' Either run sh.com.start as early as possible, or this, since
            warnings about the invalid config file need GUI.
        '''
        cf.DefaultKeys()
        self.load_config()
        # Load lists from files
        objs.get_order()
        self.set_def_colnum_even()
    
    def get_url(self):
        f = '[MClientQt] logic.Commands.get_url'
        #NOTE: update source and target languages first
        objs.get_request().url = objs.get_plugins().get_url(objs.request.search)
        mes = objs.request.url
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def control_length(self):
        # Confirm too long requests
        f = '[MClientQt] logic.Commands.control_length'
        Confirmed = True
        if len(objs.get_request().search) >= 150:
            mes = _('The request is long ({} symbols). Do you really want to send it?')
            mes = mes.format(len(objs.request.search))
            if not sh.objs.get_mes(f,mes).show_question():
                Confirmed = False
        return Confirmed
    
    def assign_blocks(self,data):
        f = '[MClientQt] logic.Commands.assign_blocks'
        blocks = []
        if not data:
            sh.com.rep_empty(f)
            return blocks
        for row in data:
            block = Block()
            block.type_ = row[0]
            block.text = row[1]
            block.rowno = row[2]
            block.colno = row[3]
            block.no = row[4]
            block.url = row[5]
            blocks.append(block)
        return blocks
    
    def add_formatting(self,blocks):
        f = '[MClientQt] logic.Commands.add_formatting'
        if not blocks:
            sh.com.rep_empty(f)
            return []
        for i in range(len(blocks)):
            blocks[i] = Font (block = blocks[i]
                             ,blocked_color1 = objs.get_colors().b1
                             ,blocked_color2 = objs.colors.b2
                             ,blocked_color3 = objs.colors.b3
                             ,blocked_color4 = objs.colors.b4
                             ,priority_color1 = objs.colors.p1
                             ,priority_color2 = objs.colors.p2
                             ,priority_color3 = objs.colors.p3
                             ,priority_color4 = objs.colors.p4
                             ).run()
        return blocks
    
    def set_def_colnum_even(self):
        if objs.get_request().SpecialPage:
            return
        if sh.lg.globs['int']['colnum'] % 2 == 0:
            objs.request.DefColNumEven = True
        else:
            objs.request.DefColNumEven = False
    
    def update_colnum(self):
        ''' A subject from the 'Phrases' section usually has
            an 'original + translation' structure, so we need to
            switch off sorting terms and ensure that the number of
            columns is divisible by 2.
        '''
        if not objs.get_request().NewPageType:
            return
        if objs.request.SpecialPage:
            if objs.request.DefColNumEven:
                return
            elif sh.lg.globs['int']['colnum'] > 2:
                sh.lg.globs['int']['colnum'] -= 1
            else:
                sh.lg.globs['int']['colnum'] = 2
        elif objs.request.DefColNumEven:
            return
        else:
            sh.lg.globs['int']['colnum'] += 1
    
    def export_style(self):
        f = '[MClientQt] logic.Commands.export_style'
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0,6s slower.
        '''
        lst = [choice for choice in (sh.lg.globs['str']['col1_type']
                                    ,sh.lg.globs['str']['col2_type']
                                    ,sh.lg.globs['str']['col3_type']
                                    ,sh.lg.globs['str']['col4_type']
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
                lst[i] = 'dic'
            elif lst[i] == _('Word forms'):
                lst[i] = 'wform'
            elif lst[i] == _('Parts of speech'):
                lst[i] = 'speech'
            elif lst[i] == _('Transcription'):
                lst[i] = 'transc'
            else:
                sub = (_('Subjects'),_('Word forms'),_('Transcription')
                      ,_('Parts of speech')
                      )
                sub = '; '.join(sub)
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(lst[i],sub)
                sh.objs.get_mes(f,mes).show_error()
        if lst:
            objs.get_request().cols = tuple(lst)
            #TODO: Should we change objs.request.collimit here?
        else:
            sh.com.rep_lazy(f)
    
    def load_config(self):
        objs.get_config()
    
    def save_config(self):
        cf.CreateConfig(objs.get_default().get_config()).run()
    
    def dump_elems(self,blocks,artid):
        f = '[MClientQt] logic.Commands.dump_elems'
        if blocks and artid:
            data = []
            for block in blocks:
                data.append (
                  (None               # (00) Skips the autoincrement
                  ,artid              # (01) ARTICLEID
                  ,block.dic          # (02) DIC (short title)
                  ,block.wform        # (03) WFORM
                  ,block.speech       # (04) SPEECH
                  ,block.transc       # (05) TRANSC
                  ,block.term         # (06) TERM
                  ,block.type_        # (07) TYPE
                  ,block.text         # (08) TEXT
                  ,block.url          # (09) URL
                  ,block.block        # (10) BLOCK
                  ,block.dprior       # (11) DICPR
                  ,block.select       # (12) SELECTABLE
                  ,block.same         # (13) SAMECELL
                  ,block.cellno       # (14) CELLNO
                  ,-1                 # (15) ROWNO
                  ,-1                 # (16) COLNO
                  ,-1                 # (17) POS1
                  ,-1                 # (18) POS2
                  ,''                 # (19) NODE1
                  ,''                 # (20) NODE2
                  ,-1                 # (21) OFFPOS1
                  ,-1                 # (22) OFFPOS2
                  ,-1                 # (23) BBOX1
                  ,-1                 # (24) BBOX2
                  ,-1                 # (25) BBOY1
                  ,-1                 # (26) BBOY2
                  ,block.text.lower() # (27) TEXTLOW
                  ,0                  # (28) IGNORE
                  ,block.sprior       # (29) SPEECHPR
                  ,block.dicf         # (30) DIC (full title)
                  )
                            )
            return data
        else:
            sh.com.rep_empty(f)
    
    def suggest(self,search,limit=0):
        f = '[MClientQt] logic.Commands.suggest'
        items = objs.get_plugins().suggest(search)
        if items:
            if limit:
                items = items[0:limit]
        else:
            items = []
            sh.com.rep_empty(f)
        return items
        
    def use_unverified(self):
        f = '[MClientQt] logic.Commands.use_unverified'
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        if hasattr(ssl,'_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context
        else:
            mes = _('Unable to use unverified certificates!')
            sh.objs.get_mes(f,mes,True).show_warning()



class Order(sj.Order):
    # Do not fail this class - input files are optional
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._set_lists()
    
    def _set_lists(self):
        f = '[MClientQt] logic.Order._set_lists'
        lists = Lists()
        self.blacklst = sh.Input (title = f
                                 ,value = lists.get_blacklist()
                                 ).get_list()
        self.priorlst = sh.Input (title = f
                                 ,value = lists.get_priorities()
                                 ).get_list()
    
    def save(self):
        blackw = objs.get_default().fblock
        priorw = objs.default.fprior
        text = '\n'.join(self.blacklst)
        sh.WriteTextFile(blackw,True,True).write(text)
        text = '\n'.join(self.priorlst)
        sh.WriteTextFile(priorw,True,True).write(text)



class Formatter:
    
    def __init__(self,block):
        self.Success = True
        self.code = ''
        self.block = block
    
    def check(self):
        f = '[MClientQt] logic.Formatter.check'
        if not self.block:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_code(self):
        f = '[MClientQt] logic.Formatter.set_code'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.code = self.block.text
    
    def _set_italic(self):
        if self.block.Italic:
            self.code = '<i>' + self.code + '</i>'
    
    def _set_bold(self):
        if self.block.Bold:
            self.code = '<b>' + self.code + '</b>'
    
    def _set_style(self):
        # Color name must be put in single quotes
        sub = '''<span style="font-family:{}; font-size:{}pt; color:'{}';">{}</span>'''
        self.code = sub.format(self.block.family,self.block.size,self.block.color,self.code)
    
    def format(self):
        f = '[MClientQt] logic.Formatter.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._set_style()
        self._set_italic()
        self._set_bold()
    
    def run(self):
        self.check()
        self.set_code()
        self.format()
        return self.code



class Cells:
    
    def __init__(self,blocks,Debug=False):
        self.Success = True
        self.cells = []
        self.cell = Cell()
        self.blocks = blocks
        self.Debug = Debug
    
    def debug(self):
        f = '[MClientQt] logic.Cells.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        nos = []
        rownos = []
        colnos = []
        codes = []
        for cell in self.cells:
            nos.append(cell.no)
            rownos.append(cell.rowno)
            colnos.append(cell.colno)
            codes.append(cell.code)
        #,maxrow = 200
        mes = sh.FastTable (iterable = [nos,rownos,colnos,codes]
                           ,headers = (_('CELL #'),_('ROW #'),_('COLUMN #')
                                      ,_('CODE')
                                      )
                           ,FromEnd = True
                           ).run()
        #TODO
        import skl_shared.shared as leg
        leg.com.start()
        leg.com.run_fast_debug(f,mes)
        leg.com.end()
        #sh.com.run_fast_debug(f,mes)
        #print(mes)
    
    def loop(self):
        f = '[MClientQt] logic.Cells.loop'
        if not self.Success:
            sh.com.cancel(f)
            return
        for block in self.blocks:
            #if block.cellno != self.cell.no:
            if block.rowno != self.cell.rowno or block.colno != self.cell.colno:
                #if self.cell.no != -1:
                if self.cell.rowno != -1:
                    self.cells.append(self.cell)
                self.cell = Cell()
                #self.cell.no = block.cellno + 1
                self.cell.rowno = block.rowno
                self.cell.colno = block.colno
            self.cell.code += Formatter(block).run()
            self.cell.plain += block.text
            if block.url:
                #TODO (?): Process multiple URLs
                self.cell.url = block.url
        #if self.cell.no != -1:
        if self.cell.rowno != -1:
            self.cells.append(self.cell)
    
    def check(self):
        f = '[MClientQt] logic.Cells.check'
        if not self.blocks:
            self.Success = False
            sh.com.rep_empty(f)
    
    def run(self):
        self.check()
        self.loop()
        self.debug()
        return self.cells



class Table:
    
    def __init__(self):
        self.set_values()
    
    def reset(self,cells):
        self.set_values()
        self.cells = cells
        self.check()
        self.set_size()
        self.set_table()
    
    def set_values(self):
        self.table = []
        self.plain = []
        self.cells = []
        self.Success = True
        self.rownum = 0
        self.colnum = 0
    
    def get_next_row_by_col(self,rowno,colno,ref_colno):
        f = '[MClientQt] logic.Table.get_next_row_by_col'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        tuple_ = self._get_next_row(rowno,ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_next_row(rowno-1,colno)
            if tuple_:
                return tuple_
        elif rowno > 0:
            return self.get_next_row_by_col(-1,colno,ref_colno)
        return(rowno,colno)
    
    def get_prev_row_by_col(self,rowno,colno,ref_colno):
        f = '[MClientQt] logic.Table.get_prev_row_by_col'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        tuple_ = self._get_prev_row(rowno,ref_colno)
        if tuple_:
            rowno = tuple_[0]
            tuple_ = self._get_prev_row(rowno+1,colno)
            if tuple_:
                return tuple_
        elif rowno < self.rownum:
            return self.get_prev_row_by_col(self.rownum,colno,ref_colno)
        return(rowno,colno)
    
    def _get_next_col(self,rowno,colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.plain[rowno][colno]:
                return(rowno,colno)
    
    def get_next_col(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_next_col'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        start = rowno
        while rowno < self.rownum:
            if rowno == start:
                tuple_ = self._get_next_col(rowno,colno)
            else:
                tuple_ = self._get_next_col(rowno,-1)
            if tuple_:
                return tuple_
            rowno += 1
        if colno + 1 < self.colnum:
            colno += 1
        if rowno >= self.rownum:
            return self.get_start()
        return(rowno,colno)
    
    def _get_prev_col(self,rowno,colno):
        while colno > 0:
            colno -= 1
            if self.plain[rowno][colno]:
                return(rowno,colno)
    
    def get_prev_col(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_prev_col'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        start = rowno
        while rowno >= 0:
            if rowno == start:
                tuple_ = self._get_prev_col(rowno,colno)
            else:
                tuple_ = self._get_prev_col(rowno,self.colnum)
            if tuple_:
                return tuple_
            rowno -= 1
        if colno > 0:
            colno -= 1
        if rowno < 0:
            return self.get_end()
        return(rowno,colno)
    
    def _get_prev_row(self,rowno,colno):
        f = '[MClientQt] logic.Table._get_prev_row'
        while rowno > 0:
            rowno -= 1
            if self.plain[rowno][colno]:
                return(rowno,colno)
    
    def get_prev_row(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_prev_row'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        start = colno
        while colno >= 0:
            if start == colno:
                tuple_ = self._get_prev_row(rowno,colno)
            else:
                tuple_ = self._get_prev_row(self.rownum,colno)
            if tuple_:
                return tuple_
            colno -= 1
        if colno < 0:
            return self.get_end()
        return(rowno,colno)
    
    def _get_next_row(self,rowno,colno):
        while rowno + 1 < self.rownum:
            rowno += 1
            if self.plain[rowno][colno]:
                return(rowno,colno)
    
    def get_next_row(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_next_row'
        if not self.Success:
            sh.com.cancel(f)
            return(rowno,colno)
        start = colno
        while colno < self.colnum:
            if start == colno:
                tuple_ = self._get_next_row(rowno,colno)
            else:
                tuple_ = self._get_next_row(-1,colno)
            if tuple_:
                return tuple_
            colno += 1
        if colno >= self.colnum:
            return self.get_start()
        return(rowno,colno)
    
    def get_start(self):
        return self.get_next_col(0,-1)
    
    def get_line_start(self,rowno):
        return self.get_next_col(rowno,-1)
    
    def get_line_end(self,rowno):
        return self.get_prev_col(rowno,self.colnum)
    
    def set_size(self):
        f = '[MClientQt] logic.Table.set_size'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.rownum = self.cells[-1].rowno + 1
        colnos = [cell.colno for cell in self.cells]
        self.colnum = max(colnos) + 1
        mes = _('Table size: {}×{}').format(self.rownum,self.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def check(self):
        f = '[MClientQt] logic.Table.check'
        if not self.cells:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_table(self):
        ''' Empty cells must be recreated since QTableView throws an error
            otherwise.
            #TODO: create empty cells with the 'cells' module
        '''
        f = '[MClientQt] logic.Table.set_table'
        if not self.Success:
            sh.com.cancel(f)
            return
        old_rowno = 1
        row = []
        plain_row = []
        for i in range(len(self.cells)):
            if old_rowno != self.cells[i].rowno:
                if row:
                    if i > 0:
                        delta = self.colnum - self.cells[i-1].colno - 1
                        for no in range(delta):
                            row.append('')
                            plain_row.append('')
                    self.table.append(row)
                    self.plain.append(plain_row)
                    row = []
                    plain_row = []
                for j in range(self.cells[i].colno):
                    row.append('')
                    plain_row.append('')
                old_rowno = self.cells[i].rowno
            row.append(self.cells[i].code)
            plain_row.append(self.cells[i].plain.strip())
        if row:
            delta = self.colnum - len(row)
            for no in range(delta):
                row.append('')
                plain_row.append('')
            self.table.append(row)
            self.plain.append(plain_row)
        if not self.table:
            self.Success = False
            sh.com.rep_out(f)
        
    def get_end(self):
        return self.get_prev_col(self.rownum-1,self.colnum)



class Search(Table):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def check(self):
        f = '[MClientQt] logic.Search.check'
        if not self.cells or not self.plain or not self.pattern.strip():
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
    
    def reset(self,cells,plain,pattern,rowno,colno,Case=False):
        self.set_values()
        self.cells = cells
        self.plain = plain
        self.pattern = pattern
        self.rowno = rowno
        self.colno = colno
        self.Case = Case
        self.check()
        self.set_size()
        self.lower()
    
    def set_values(self):
        self.cells = []
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
            return(self.rowno,self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno,self.colno)
        rowno, colno = self.get_next_col(self.rowno,self.colno)
        mes = _('Row #{}. Column #{}: "{}"')
        mes = mes.format(rowno,colno,self.plain[rowno][colno])
        sh.objs.get_mes(f,mes,True).show_debug()
        return(rowno,colno)
    
    def search_prev(self):
        f = '[MClientQt] logic.Search.search_prev'
        if not self.Success:
            sh.com.cancel(f)
            return(self.rowno,self.colno)
        # Avoid infinite recursion
        if not self._has_pattern():
            return(self.rowno,self.colno)
        rowno, colno = self.get_prev_col(self.rowno,self.colno)
        mes = _('Row #{}. Column #{}. Text: "{}"')
        mes = mes.format(rowno,colno,self.plain[rowno][colno])
        sh.objs.get_mes(f,mes,True).show_debug()
        return(rowno,colno)
    
    def _get_next_col(self,rowno,colno):
        while colno + 1 < self.colnum:
            colno += 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno,colno)
    
    def _get_prev_col(self,rowno,colno):
        while colno > 0:
            colno -= 1
            if self.pattern in self.plain[rowno][colno]:
                return(rowno,colno)



class Font:
    
    def __init__ (self,block,blocked_color1='dim gray'
                 ,blocked_color2='dim gray',blocked_color3='dim gray'
                 ,blocked_color4='dim gray',priority_color1='red'
                 ,priority_color2='red',priority_color3='red'
                 ,priority_color4='red'
                 ):
        self.set_values()
        self.block = block
        self.blocked_color1 = blocked_color1
        self.blocked_color2 = blocked_color2
        self.blocked_color3 = blocked_color3
        self.blocked_color4 = blocked_color4
        self.priority_color1 = priority_color1
        self.priority_color2 = priority_color2
        self.priority_color3 = priority_color3
        self.priority_color4 = priority_color4
    
    def set_values(self):
        self.Success = True
    
    def run(self):
        self.check()
        self.set_text()
        self.set_family()
        self.set_size()
        self.set_color()
        self.set_bold()
        self.set_italic()
        return self.block
    
    def _set_color(self):
        if self.block.type_ in ('dic','phdic','wform','speech'):
            if self.block.colno == 0:
                self.block.color = sh.lg.globs['str']['color_col1']
            elif self.block.colno == 1:
                self.block.color = sh.lg.globs['str']['color_col2']
            elif self.block.colno == 2:
                self.block.color = sh.lg.globs['str']['color_col3']
            elif self.block.colno == 3:
                self.block.color = sh.lg.globs['str']['color_col4']
        elif self.block.type_ in ('phrase','term'):
            self.block.color = sh.lg.globs['str']['color_terms']
        elif self.block.type_ in ('comment','phcom','phcount','transc'):
            self.block.color = sh.lg.globs['str']['color_comments']
        elif self.block.type_ == 'correction':
            self.block.color = 'green'
        elif self.block.type_ == 'user':
            self.block.color = objs.get_colors().user
    
    def _set_color_p(self):
        if self.block.type_ in ('dic','phdic','wform','transc','speech'):
            if self.block.colno == 0:
                self.block.color = self.priority_color1
            elif self.block.colno == 1:
                self.block.color = self.priority_color2
            elif self.block.colno == 2:
                self.block.color = self.priority_color3
            elif self.block.colno == 3:
                self.block.color = self.priority_color4
        else:
            self.block.color = self.priority_color1
    
    def _set_color_b(self):
        if self.block.type_ in ('dic','phdic','wform','transc','speech'):
            if self.block.colno == 0:
                self.block.color = self.blocked_color1
            elif self.block.colno == 1:
                self.block.color = self.blocked_color2
            elif self.block.colno == 2:
                self.block.color = self.blocked_color3
            elif self.block.colno == 3:
                self.block.color = self.blocked_color4
        else:
            self.block.color = 'dim gray'
    
    def set_bold(self):
        f = '[MClientQt] logic.Font.set_bold'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ == 'wform' or self.block.colno == 0 \
        and self.block.type_ in ('dic','phdic','transc','speech'):
            self.block.Bold = True
    
    def set_italic(self):
        f = '[MClientQt] logic.Font.set_italic'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('comment','correction','phcom','phcount'
                               ,'speech','transc','user'
                               ):
            self.block.Italic = True
    
    def set_color(self):
        f = '[MClientQt] logic.Font.set_color'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' We need to determine whether a block is blockable or prioritizable
            irrespectively of its state in a current view, so we do not rely on
            'block' values.
        '''
        if sj.objs.get_article().is_blocked(self.block.text):
            self._set_color_b()
        elif sj.objs.article.get_priority(self.block.text) > 0:
            self._set_color_p()
        else:
            self._set_color()
    
    def set_text(self):
        f = '[MClientQt] logic.Font.set_text'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.text = self.block.text
    
    def check(self):
        f = '[MClientQt] logic.Font.check'
        if self.block and self.blocked_color1 and self.blocked_color2 \
        and self.blocked_color3 and self.blocked_color4 \
        and self.priority_color1 and self.priority_color2 \
        and self.priority_color3 and self.priority_color4:
            pass
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_family(self):
        f = '[MClientQt] logic.Font.set_family'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('dic','phdic','wform','speech'):
            if self.block.colno == 0:
                self.block.family = sh.lg.globs['str']['font_col1_family']
            elif self.block.colno == 1:
                self.block.family = sh.lg.globs['str']['font_col2_family']
            elif self.block.colno == 2:
                self.block.family = sh.lg.globs['str']['font_col3_family']
            elif self.block.colno == 3:
                self.block.family = sh.lg.globs['str']['font_col4_family']
        elif self.block.type_ in ('comment','correction','phcom'
                                 ,'phcount','transc','user'
                                 ):
            self.block.family = sh.lg.globs['str']['font_comments_family']
        elif self.block.type_ in ('phrase','term'):
            self.block.family = sh.lg.globs['str']['font_terms_family']
    
    def set_size(self):
        f = '[MClientQt] logic.Font.set_size'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('dic','phdic','wform','speech'):
            if self.block.colno == 0:
                self.block.size = sh.lg.globs['int']['font_col1_size']
            elif self.block.colno == 1:
                self.block.size = sh.lg.globs['int']['font_col2_size']
            elif self.block.colno == 2:
                self.block.size = sh.lg.globs['int']['font_col3_size']
            elif self.block.colno == 3:
                self.block.size = sh.lg.globs['int']['font_col4_size']
        elif self.block.type_ in ('comment','correction','phcom'
                                 ,'phcount','transc','user'
                                 ):
            self.block.size = sh.lg.globs['int']['font_comments_size']
        elif self.block.type_ in ('phrase','term'):
            self.block.size = sh.lg.globs['int']['font_terms_size']



class Colors:
    
    def __init__(self):
        self.set_values()
        self.set_tints()
    
    def set_values(self):
        self.factor = 140
        # No need to set default colors, Qt ignores empty names at input
        self.p1 = self.p2 = self.p3 = self.p4 = self.b1 = self.b2 = self.b3 \
        = self.b4 = self.user = ''
    
    def set_tints(self):
        self.p1, self.b1 = sh.Color(sh.lg.globs['str']['color_col1']).modify(self.factor)
        self.p2, self.b2 = sh.Color(sh.lg.globs['str']['color_col2']).modify(self.factor)
        self.p3, self.b3 = sh.Color(sh.lg.globs['str']['color_col3']).modify(self.factor)
        self.p4, self.b4 = sh.Color(sh.lg.globs['str']['color_col4']).modify(self.factor)
        darker, self.user = sh.Color(sh.lg.globs['str']['color_comments']).modify(self.factor)


objs = Objects()
com = Commands()
