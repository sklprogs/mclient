#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import ssl

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.web as wb

import manager
import subjects.subjects as sj
import config as cf


SPORDER = (_('Noun'),_('Verb'),_('Adjective'),_('Abbreviation'),_('Adverb')
          ,_('Preposition'),_('Pronoun')
          )


class Articles:
    
    def __init__(self):
        self.reset()
    
    def set_values(self):
        self.id = -1
        self.articles = {'ids' : {}}
    
    def reset(self):
        self.set_values()
    
    def is_last(self):
        return self.id == self.get_max_id()
    
    def get_max_id(self):
        f = '[MClientQt] logic.Articles.get_max_id'
        try:
            # Do not use 'max' on an empty sequence
            return len(self.articles['ids']) - 1
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return -1
    
    def get_len(self):
        return self.get_max_id() + 1
    
    def add(self, search='', url='', cells=[], raw_code=''):
        id_ = self.get_max_id() + 1
        self.articles['ids'][id_] = {'source'   : sh.lg.globs['str']['source']
                                    ,'search'   : search
                                    ,'url'      : url
                                    ,'cells'    : cells
                                    ,'raw_code' : raw_code
                                    ,'rowno'    : -1
                                    ,'colno'    : -1
                                    ,'lang1'    : objs.get_plugins().get_lang1()
                                    ,'lang2'    : objs.plugins.get_lang2()
                                    }
        self.set_id(id_)
    
    def clear_article(self):
        f = '[MClientQt] logic.Articles.clear_article'
        try:
            self.articles['ids'][self.id]['raw_code'] = ''
            self.articles['ids'][self.id]['cells'] = []
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
    
    def delete_bookmarks(self):
        f = '[MClientQt] logic.Articles.delete_bookmarks'
        try:
            self.articles['ids']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
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
            sh.objs.get_mes(f,mes).show_warning()
    
    def set_id(self, id_):
        f = '[MClientQt] logic.Articles.set_id'
        try:
            self.articles['ids'][id_]
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
            return
        self.id = id_
    
    def get_search(self):
        f = '[MClientQt] logic.Articles.get_search'
        try:
            return self.articles['ids'][self.id]['search']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_source(self):
        f = '[MClientQt] logic.Articles.get_source'
        try:
            return self.articles['ids'][self.id]['source']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_url(self):
        f = '[MClientQt] logic.Articles.get_url'
        try:
            return self.articles['ids'][self.id]['url']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_lang1(self):
        f = '[MClientQt] logic.Articles.get_lang1'
        try:
            return self.articles['ids'][self.id]['lang1']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_lang2(self):
        f = '[MClientQt] logic.Articles.get_lang2'
        try:
            return self.articles['ids'][self.id]['lang2']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_raw_code(self):
        f = '[MClientQt] logic.Articles.get_raw_code'
        try:
            return self.articles['ids'][self.id]['raw_code']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return ''
    
    def get_cells(self):
        f = '[MClientQt] logic.Articles.get_cells'
        try:
            return self.articles['ids'][self.id]['cells']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
        return []
    
    def find(self, source, search, url):
        f = '[MClientQt] logic.Articles.find'
        try:
            self.articles['ids']
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_warning()
            return
        for id_ in self.articles['ids']:
            if self.articles['ids'][id_]['source'] == source \
            and self.articles['ids'][id_]['search'] == search \
            and self.articles['ids'][id_]['url'] == url:
                return id_
        return -1



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
        if not sh.lg.globs['bool']['AdjustByWidth']:
            sh.com.rep_lazy(f)
            return
        for column in self.columns:
            if column.Fixed:
                column.width = sh.lg.globs['int']['fixed_col_width']
            else:
                column.width = sh.lg.globs['int']['term_col_width']
#            if objs.get_blocksdb().is_col_empty(column.no):
#                column.width = self.min_width
#            elif column.Fixed:
#                column.width = sh.lg.globs['int']['fixed_col_width']
#            else:
#                column.width = sh.lg.globs['int']['term_col_width']
    
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
        self.fixed_num = 4
#        columns = objs.get_blocksdb().get_fixed_cols()
#        if not columns:
#            sh.com.rep_lazy(f)
#            return
#        self.fixed_num = len(columns)
        mes = _('An actual number of fixed columns: {}').format(self.fixed_num)
        sh.objs.get_mes(f,mes,True).show_debug()
    
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
        if not self.Success:
            sh.com.cancel(f)
            return self.abbr2full
        if not self.abbr2full:
            for i in range(len(self.abbr)):
                self.abbr2full[self.abbr[i]] = self.full[i]
        return self.abbr2full
    
    def get_full2abbr(self):
        f = '[MClientQt] logic.SpeechPrior.get_full2abbr'
        if not self.Success:
            sh.com.cancel(f)
            return self.full2abbr
        if not self.full2abbr:
            for i in range(len(self.full)):
                self.full2abbr[self.full[i]] = self.abbr[i]
        return self.full2abbr
    
    def get_all2prior(self):
        f = '[MClientQt] logic.SpeechPrior.get_all2prior'
        seq = {}
        if not self.Success:
            sh.com.cancel(f)
            return seq
        for i in range(len(self.prior)):
            seq[self.abbr[i]] = self.prior[i]
            seq[self.full[i]] = self.prior[i]
        return seq
    
    def debug(self):
        self.debug_all2prior()
        self.debug_pairs()
    
    def debug_all2prior(self):
        f = '[MClientQt] logic.SpeechPrior.debug_all2prior'
        if not self.Success:
            sh.com.cancel(f)
            return
        all2prior = self.get_all2prior()
        if not all2prior:
            sh.com.rep_empty(f)
            return
        all_ = all2prior.keys()
        prior = [all2prior.get(key) for key in all2prior.keys()]
        headers = (_('NAME'),_('PRIORITY'))
        iterable = [all_,prior]
        mes = sh.FastTable(iterable,headers).run()
        sh.com.run_fast_debug(f,mes)
    
    def _debug_full2abbr(self):
        f = '[MClientQt] logic.SpeechPrior._debug_full2abbr'
        full2abbr = self.get_full2abbr()
        if not full2abbr:
            sh.com.rep_empty(f)
            return
        full = sorted(full2abbr.keys())
        abbr = [full2abbr.get(item) for item in full]
        headers = (_('NAME'),_('ABBREVIATION'))
        iterable = [full,abbr]
        mes = sh.FastTable(iterable,headers).run()
        sh.com.run_fast_debug(f,mes)
    
    def _debug_abbr2full(self):
        f = '[MClientQt] logic.SpeechPrior._debug_abbr2full'
        abbr2full = self.get_abbr2full()
        if not abbr2full:
            sh.com.rep_empty(f)
            return
        abbr = sorted(abbr2full.keys())
        full = [abbr2full.get(item) for item in abbr]
        headers = (_('ABBREVIATION'),_('NAME'))
        iterable = [abbr,full]
        mes = sh.FastTable(iterable,headers).run()
        sh.com.run_fast_debug(f,mes)
    
    def debug_pairs(self):
        f = '[MClientQt] logic.SpeechPrior.debug_pairs'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._debug_full2abbr()
        self._debug_abbr2full()
    
    def prioritize(self):
        f = '[MClientQt] logic.SpeechPrior.prioritize'
        if not self.Success:
            sh.com.cancel(f)
            return
        lst = [i + 1 for i in range(len(self.abbr))]
        for i in range(len(self.order)):
            try:
                ind = self.full.index(self.order[i])
                self.prior[ind] = lst[i]
            except ValueError:
                mes = _('Wrong input data: "{}"!').format(self.order[i])
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
    
    def check(self):
        f = '[MClientQt] logic.SpeechPrior.check'
        if not len(self.abbr):
            self.Success = False
            sh.com.rep_empty(f)
            return
        if len(self.abbr) != len(self.full):
            self.Success = False
            sub = '{} == {}'.format(len(self.abbr),len(self.full))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
            return
        if len(self.order) > len(self.abbr):
            self.Success = False
            sub = '{} <= {}'.format(len(self.order),len(self.abbr))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
    
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
        self.cols = ('subj','wform','transc','speech')
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
        self.text = ''
        self.search = ''
        self.url = ''



class Lists:
    # Read the blocklist and the prioritize list
    def __init__(self):
        self.blacklst = objs.get_default().fblock
        self.priorlst = objs.default.fprior
        self.Success = objs.default.Success
    
    def get_blacklist(self):
        f = '[MClientQt] logic.Lists.get_blacklist'
        if not self.Success:
            sh.com.cancel(f)
            return
        text = sh.ReadTextFile(self.blacklst,True).get()
        text = sh.Text(text,True).text
        return text.splitlines()

    def get_priorities(self):
        f = '[MClientQt] logic.Lists.get_priorities'
        if not self.Success:
            sh.com.cancel(f)
            return
        text = sh.ReadTextFile(self.priorlst,True).get()
        text = sh.Text(text,True).text
        return text.splitlines()



class Objects:
    
    def __init__(self):
        self.online = self.request = self.order = self.default \
                    = self.plugins = self.speech_prior = self.config \
                    = self.order = self.column_width = self.colors \
                    = self.articles = None

    def get_articles(self):
        if self.articles is None:
            self.articles = Articles()
        return self.articles
    
    def get_colors(self):
        if self.colors is None:
            self.colors = Colors()
        return self.colors
    
    def get_column_width(self):
        if self.column_width is None:
            self.column_width = ColumnWidth()
        return self.column_width
    
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
    
    def get_text(self,cells):
        f = '[MClientQt] logic.Commands.get_text'
        if not cells:
            sh.com.rep_empty(f)
            return ''
        return '\n'.join([cell.plain for cell in cells])
    
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
                lst[i] = 'subj'
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
        ''' On *some* systems we can get urllib.error.URLError: <urlopen error
            [SSL: CERTIFICATE_VERIFY_FAILED]>. To get rid of this error, we use
            this small workaround.
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



class Format:
    
    def __init__(self,block):
        self.Success = True
        self.code = ''
        self.block = block
    
    def check(self):
        f = '[MClientQt] logic.Format.check'
        if not self.block:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_code(self):
        f = '[MClientQt] logic.Format.set_code'
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
        self.code = sub.format (self.block.family,self.block.size
                               ,self.block.color,self.code
                               )
    
    def format(self):
        f = '[MClientQt] logic.Format.format'
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



class Table:
    ''' #NOTE: it's not enough to use 'Success' since we do not call 'reset'
        before loading an article.
    '''
    def __init__(self,plain=[],code=[]):
        if plain and code:
            self.reset(plain,code)
    
    def reset(self,plain,code):
        self.set_values()
        self.plain = plain
        self.code = code
        self.set_size()
    
    def set_values(self):
        self.plain = []
        self.code = []
        self.rownum = 0
        self.colnum = 0
    
    def get_next_row_by_col(self,rowno,colno,ref_colno):
        f = '[MClientQt] logic.Table.get_next_row_by_col'
        if not self.plain:
            sh.com.rep_empty(f)
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
        if not self.plain:
            sh.com.rep_empty(f)
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
        if not self.plain:
            sh.com.rep_empty(f)
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
        if not self.plain:
            sh.com.rep_empty(f)
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
        while rowno > 0:
            rowno -= 1
            if self.plain[rowno][colno]:
                return(rowno,colno)
    
    def get_prev_row(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_prev_row'
        if not self.plain:
            sh.com.rep_empty(f)
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
        if not self.plain:
            sh.com.rep_empty(f)
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
        if not self.plain:
            sh.com.rep_empty(f)
            return
        self.rownum = len(self.plain)
        self.colnum = len(self.plain[0])
        mes = _('Table size: {}×{}').format(self.rownum,self.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def get_end(self):
        return self.get_prev_col(self.rownum-1,self.colnum)



class Search(Table):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
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
    
    def reset(self,plain,pattern,rowno,colno,Case=False):
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
        if self.block.type_ in ('subj','phsubj','wform','speech'):
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
        if not self.block.type_ in ('subj','phsubj','wform','transc','speech'):
            self.block.color = self.priority_color1
            return
        if self.block.colno == 0:
            self.block.color = self.priority_color1
        elif self.block.colno == 1:
            self.block.color = self.priority_color2
        elif self.block.colno == 2:
            self.block.color = self.priority_color3
        elif self.block.colno == 3:
            self.block.color = self.priority_color4
    
    def _set_color_b(self):
        if not self.block.type_ in ('subj','phsubj','wform','transc','speech'):
            self.block.color = 'dim gray'
            return
        if self.block.colno == 0:
            self.block.color = self.blocked_color1
        elif self.block.colno == 1:
            self.block.color = self.blocked_color2
        elif self.block.colno == 2:
            self.block.color = self.blocked_color3
        elif self.block.colno == 3:
            self.block.color = self.blocked_color4
    
    def set_bold(self):
        f = '[MClientQt] logic.Font.set_bold'
        if not self.Success:
            sh.com.cancel(f)
            return
        #TODO: elaborate
        if self.block.Fixed:
            self.block.Bold = True
        '''
        if self.block.type_ == 'wform' or self.block.colno == 0 \
        and self.block.type_ in ('subj','phsubj','transc','speech'):
            self.block.Bold = True
        '''
    
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
        if not (self.block and self.blocked_color1 and self.blocked_color2 \
        and self.blocked_color3 and self.blocked_color4 \
        and self.priority_color1 and self.priority_color2 \
        and self.priority_color3 and self.priority_color4):
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_family(self):
        f = '[MClientQt] logic.Font.set_family'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('subj','phsubj','wform','speech'):
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
        if self.block.type_ in ('subj','phsubj','wform','speech'):
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
        ''' Config values should be converted to HEX since they are further
            used to generate a web-page when saving an article, and browsers,
            unlike Qt, may not understand colors like 'cadet blue' (with or
            without quotes).
        '''
        # color_terms
        icolor = sh.Color(sh.lg.globs['str']['color_terms'])
        sh.lg.globs['str']['color_terms'] = icolor.get_hex()
        
        # color_comments
        icolor = sh.Color(sh.lg.globs['str']['color_comments'])
        sh.lg.globs['str']['color_comments'] = icolor.get_hex()
        darker, self.user = icolor.modify(self.factor)
        
        # color_col1
        icolor = sh.Color(sh.lg.globs['str']['color_col1'])
        sh.lg.globs['str']['color_col1'] = icolor.get_hex()
        self.p1, self.b1 = icolor.modify(self.factor)
        
        # color_col2
        icolor = sh.Color(sh.lg.globs['str']['color_col2'])
        sh.lg.globs['str']['color_col2'] = icolor.get_hex()
        self.p2, self.b2 = icolor.modify(self.factor)
        
        # color_col3
        icolor = sh.Color(sh.lg.globs['str']['color_col3'])
        sh.lg.globs['str']['color_col3'] = icolor.get_hex()
        self.p3, self.b3 = icolor.modify(self.factor)
        
        # color_col4
        icolor = sh.Color(sh.lg.globs['str']['color_col4'])
        sh.lg.globs['str']['color_col4'] = icolor.get_hex()
        self.p4, self.b4 = icolor.modify(self.factor)


objs = Objects()
com = Commands()
