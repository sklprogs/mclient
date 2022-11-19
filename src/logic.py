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


class Block:
    
    def __init__(self):
        self.type_ = 'invalid'
        self.text = ''
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
        self.no = -1
        self.rowno = -1
        self.colno = -1



class Font:
    
    def __init__ (self,block,blocked_color1='dim gray'
                 ,blocked_color2='dim gray',blocked_color3='dim gray'
                 ,blocked_color4='dim gray',priority_color1='red'
                 ,priority_color2='red',priority_color3='red'
                 ,priority_color4='red'
                 ):
        self.Success = True
        self.block = block
        self.blocked_color1 = blocked_color1
        self.blocked_color2 = blocked_color2
        self.blocked_color3 = blocked_color3
        self.blocked_color4 = blocked_color4
        self.priority_color1 = priority_color1
        self.priority_color2 = priority_color2
        self.priority_color3 = priority_color3
        self.priority_color4 = priority_color4
    
    def run(self):
        self.check()
        self.set_family()
        self.set_size()
        self.set_color()
        self.set_bold()
        self.set_italic()
        return self.block
    
    def _set_color(self):
        if self.block.type_ in ('dic','wform','speech','transc'):
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
            color = sh.lg.globs['str']['color_comments']
            result = sh.com.get_mod_color (color = color
                                          ,delta = 75
                                          )
            if result:
                color = result
            self.block.color = color
    
    def _set_color_p(self):
        if self.block.type_ in ('dic','wform','speech','transc'):
            if self.colno == 0:
                self.color = self.priority_color1
            elif self.colno == 1:
                self.color = self.priority_color2
            elif self.colno == 2:
                self.color = self.priority_color3
            elif self.colno == 3:
                self.color = self.priority_color4
        else:
            self.color = self.priority_color1
    
    def _set_color_b(self):
        if self.block.type_ in ('dic','wform','speech','transc'):
            if self.colno == 0:
                self.color = self.blocked_color1
            elif self.colno == 1:
                self.color = self.blocked_color2
            elif self.colno == 2:
                self.color = self.blocked_color3
            elif self.colno == 3:
                self.color = self.blocked_color4
        else:
            self.color = 'dim gray'
    
    def set_bold(self):
        f = '[MClient] logic.Font.set_bold'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('dic','wform','speech','transc','phdic'):
            self.block.Bold = True
    
    def set_italic(self):
        f = '[MClient] logic.Font.set_italic'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('comment','correction','phcom'
                               ,'phcount','speech','transc','user'
                               ):
            self.block.Italic = True
    
    def set_color(self):
        f = '[MClient] logic.Font.set_color'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' We need to determine whether a block is blockable or
            prioritizable irrespectively of its state in a current view,
            so we do not rely on 'block' values.
        '''
        if sj.objs.get_article().is_blocked(self.block.text):
            self._set_color_b()
        elif sj.objs.article.get_priority(self.block.text) > 0:
            self._set_color_p()
        else:
            self._set_color()
    
    def check(self):
        f = '[MClient] logic.Font.check'
        if self.block and self.blocked_color1 and self.blocked_color2 \
        and self.blocked_color3 and self.blocked_color4 \
        and self.priority_color1 and self.priority_color2 \
        and self.priority_color3 and self.priority_color4:
            pass
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_family(self):
        f = '[MClient] logic.Font.set_family'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('dic','wform','speech','transc'):
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
        f = '[MClient] logic.Font.set_size'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('dic','wform','speech','transc'):
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
        f = '[MClient] logic.ColumnWidth.set_col_width'
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
        f = '[MClient] logic.ColumnWidth.set_fixed_num'
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
        f = '[MClient] logic.ColumnWidth.set_term_num'
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
        f = '[MClient] logic.SpeechPrior.get_abbr2full'
        if self.Success:
            if not self.abbr2full:
                for i in range(len(self.abbr)):
                    self.abbr2full[self.abbr[i]] = self.full[i]
        else:
            sh.com.cancel(f)
        return self.abbr2full
    
    def get_full2abbr(self):
        f = '[MClient] logic.SpeechPrior.get_full2abbr'
        if self.Success:
            if not self.full2abbr:
                for i in range(len(self.full)):
                    self.full2abbr[self.full[i]] = self.abbr[i]
        else:
            sh.com.cancel(f)
        return self.full2abbr
    
    def get_all2prior(self):
        f = '[MClient] logic.SpeechPrior.get_all2prior'
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
        f = '[MClient] logic.SpeechPrior.debug_all2prior'
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
        f = '[MClient] logic.SpeechPrior._debug_full2abbr'
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
        f = '[MClient] logic.SpeechPrior._debug_abbr2full'
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
        f = '[MClient] logic.SpeechPrior.debug_pairs'
        if self.Success:
            self._debug_full2abbr()
            self._debug_abbr2full()
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClient] logic.SpeechPrior.prioritize'
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
        f = '[MClient] logic.SpeechPrior.check'
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



class Source:
    
    def __init__(self):
        self.title = ''
        self.status = _('not running')
        self.color = 'red'



class Welcome:

    def __init__ (self,product='MClient'
                 ,version='current'
                 ):
        self.set_values()
        self.product = product
        self.version = version
        self.desc = sh.List (lst1 = [self.product
                                    ,self.version
                                    ]
                            ).space_items()

    def set_values(self):
        self.sources = []
        self.sdstat = 0
        self.mtbstat = 0
        self.lgstat = 0
        self.sdcolor = 'red'
        self.mtbcolor = 'red'
        self.lgcolor = 'red'
        self.product = ''
        self.version = ''
        self.desc = ''
    
    def try_sources(self):
        f = '[MClient] logic.Welcome.try_sources'
        old = objs.get_plugins().source
        if sh.lg.globs['bool']['Ping']:
            dics = objs.plugins.get_online_sources()
            if dics:
                for dic in dics:
                    objs.plugins.set(dic)
                    source = Source()
                    source.title = dic
                    if objs.plugins.is_accessible():
                        source.status = _('running')
                        source.color = 'green'
                    self.sources.append(source)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_lazy(f)
        # Try Stardict
        objs.plugins.set(_('Stardict'))
        self.sdstat = objs.get_plugins().is_accessible()
        if self.sdstat:
            self.sdcolor = 'green'
        # Try local Multitran
        objs.plugins.set(_('Local MT'))
        self.mtbstat = objs.plugins.is_accessible()
        if self.mtbstat:
            self.mtbcolor = 'green'
        # Try DSL
        objs.plugins.set('Lingvo (DSL)')
        self.lgstat = objs.plugins.is_accessible()
        if self.lgstat:
            self.lgcolor = 'green'
        objs.plugins.set(old)

    def gen_source_code(self,title,status,color):
        sub = ' {}'.format(status)
        code = '<b>{}</b><font face="Serif" color="{}" size="6">{}'
        code = code.format(title,color,sub)
        self.istr.write(code)
        code = '</font>.<br>'
        self.istr.write(code)
    
    def gen_hint(self,hint):
        code = '<td align="left" valign="top" col width="200">{}</td>'
        code = code.format(hint)
        self.istr.write(code)
    
    def gen_hotkey(self,hotkey):
        code = '<td align="center" valign="top" col width="100">{}</td>'
        code = code.format(sh.Hotkeys(hotkey).run())
        self.istr.write(code)
    
    def gen_row(self,hint1,hotkey1,hint2,hotkey2):
        self.istr.write('<tr>')
        self.gen_hint(hint1)
        self.gen_hotkey(hotkey1)
        # Suppress useless warnings since the 2nd column may be empty
        if hotkey2:
            self.gen_hint(hint2)
            self.gen_hotkey(hotkey2)
        self.istr.write('</tr>')
    
    def set_hotkeys(self):
        self.istr.write('<font face="Serif" size="5"><table>')

        hint1 = _('Translate the current input or selection')
        hotkey1 = ('<Button-1>','<Return>')
        hint2 = _('Copy the current selection')
        hotkey2 = ('<Button-3>'
                   ,sh.lg.globs['str']['bind_copy_sel']
                   ,sh.lg.globs['str']['bind_copy_sel_alt']
                   )
        hint34 = _('Show the program window (system-wide)')
        hotkey34 = '<Alt_L-grave>'
        hint35 = _('Translate selection from an external program')
        hotkey35 = ('<Control_L-Insert-Insert>'
                   ,'<Control_L-c-c>'
                   )
        hint36 = _('Minimize the program window')
        hotkey36 = '<Escape>'
        hint37 = _('Quit the program')
        hotkey37 = ('<Control-q>'
                   ,sh.lg.globs['str']['bind_quit']
                   )
        hint3 = _('Copy the URL of the selected term')
        hotkey3 = sh.lg.globs['str']['bind_copy_url']
        hint4 = _('Copy the URL of the current article')
        hotkey4 = sh.lg.globs['str']['bind_copy_article_url']
        hint5 = _('Go to the previous section of column #%d') % 1
        hotkey5 = sh.lg.globs['str']['bind_col1_up']
        hint6 = _('Go to the next section of column #%d') % 1
        hotkey6 = sh.lg.globs['str']['bind_col1_down']
        hint7 = _('Go to the previous section of column #%d') % 2
        hotkey7 = sh.lg.globs['str']['bind_col2_up']
        hint8 = _('Go to the next section of column #%d') % 2
        hotkey8 = sh.lg.globs['str']['bind_col2_down']
        hint9 = _('Go to the previous section of column #%d') % 3
        hotkey9 = sh.lg.globs['str']['bind_col3_up']
        hint10 = _('Go to the next section of column #%d') % 3
        hotkey10 = sh.lg.globs['str']['bind_col3_down']
        hint11 = _('Open a webpage with a definition of the current term')
        hotkey11 = sh.lg.globs['str']['bind_define']
        hint12 = _('Look up phrases')
        hotkey12 = sh.lg.globs['str']['bind_go_phrases']
        hint13 = _('Go to the preceding article')
        hotkey13 = sh.lg.globs['str']['bind_go_back']
        hint14 = _('Go to the following article')
        hotkey14 = sh.lg.globs['str']['bind_go_forward']
        hint15 = _('Next source language')
        hotkey15 = (sh.lg.globs['str']['bind_next_lang1']
                   ,sh.lg.globs['str']['bind_next_lang1_alt']
                   )
        hint16 = _('Previous source language')
        hotkey16 = (sh.lg.globs['str']['bind_prev_lang1']
                   ,sh.lg.globs['str']['bind_prev_lang1_alt']
                   )
        hint17 = _('Create a printer-friendly page')
        hotkey17 = sh.lg.globs['str']['bind_print']
        hint18 = _('Open the current article in a default browser')
        hotkey18 = (sh.lg.globs['str']['bind_open_in_browser']
                   ,sh.lg.globs['str']['bind_open_in_browser_alt']
                   )
        hint19 = _('Reload the current article')
        hotkey19 = (sh.lg.globs['str']['bind_reload_article']
                   ,sh.lg.globs['str']['bind_reload_article_alt']
                   )
        hint20 = _('Save or copy the current article')
        hotkey20 = (sh.lg.globs['str']['bind_save_article']
                   ,sh.lg.globs['str']['bind_save_article_alt']
                   )
        hint21 = _('Start a new search in the current article')
        hotkey21 = sh.lg.globs['str']['bind_re_search_article']
        hint22 = _('Search the article forward')
        hotkey22 = sh.lg.globs['str']['bind_search_article_forward']
        hint23 = _('Search the article backward')
        hotkey23 = sh.lg.globs['str']['bind_search_article_backward']
        hint24 = _('Show settings')
        hotkey24 = (sh.lg.globs['str']['bind_settings']
                   ,sh.lg.globs['str']['bind_settings_alt']
                   )
        hint25 = _('About the program')
        hotkey25 = sh.lg.globs['str']['bind_show_about']
        hint26 = _('Paste a special symbol')
        hotkey26 = sh.lg.globs['str']['bind_spec_symbol']
        hint27 = _('Toggle alphabetizing')
        hotkey27 = sh.lg.globs['str']['bind_toggle_alphabet']
        hint28 = _('Toggle blacklisting')
        hotkey28 = sh.lg.globs['str']['bind_toggle_block']
        hint29 = _('Toggle History')
        hotkey29 = (sh.lg.globs['str']['bind_toggle_history']
                   ,sh.lg.globs['str']['bind_toggle_history_alt']
                   )
        hint30 = _('Toggle prioritizing')
        hotkey30 = sh.lg.globs['str']['bind_toggle_priority']
        hint31 = _('Toggle terms-only selection')
        hotkey31 = sh.lg.globs['str']['bind_toggle_sel']
        hint32 = _('Toggle the current article view')
        hotkey32 = (sh.lg.globs['str']['bind_toggle_view']
                   ,sh.lg.globs['str']['bind_toggle_view_alt']
                   )
        hint33 = _('Clear History')
        hotkey33 = sh.lg.globs['str']['bind_clear_history']
        hint38 = _('Next target language')
        hotkey38 = (sh.lg.globs['str']['bind_next_lang2']
                   ,sh.lg.globs['str']['bind_next_lang2_alt']
                   )
        hint39 = _('Previous target language')
        hotkey39 = (sh.lg.globs['str']['bind_prev_lang2']
                   ,sh.lg.globs['str']['bind_prev_lang2_alt']
                   )
        hint40 = _('Swap source and target languages')
        hotkey40 = sh.lg.globs['str']['bind_swap_langs']
        
        hint41 = _('Copy the nominative case')
        hotkey41 = sh.lg.globs['str']['bind_copy_nominative']
        
        self.gen_row(hint1,hotkey1,hint2,hotkey2)
        self.gen_row(hint34,hotkey34,hint35,hotkey35)
        self.gen_row(hint36,hotkey36,hint37,hotkey37)
        self.gen_row(hint3,hotkey3,hint4,hotkey4)
        self.gen_row(hint5,hotkey5,hint6,hotkey6)
        self.gen_row(hint7,hotkey7,hint8,hotkey8)
        self.gen_row(hint9,hotkey9,hint10,hotkey10)
        self.gen_row(hint11,hotkey11,hint12,hotkey12)
        self.gen_row(hint13,hotkey13,hint14,hotkey14)
        self.gen_row(hint15,hotkey15,hint16,hotkey16)
        self.gen_row(hint38,hotkey38,hint39,hotkey39)
        self.gen_row(hint40,hotkey40,hint17,hotkey17)
        self.gen_row(hint18,hotkey18,hint19,hotkey19)
        self.gen_row(hint20,hotkey20,hint22,hotkey22)
        self.gen_row(hint23,hotkey23,hint21,hotkey21)
        self.gen_row(hint24,hotkey24,hint25,hotkey25)
        self.gen_row(hint26,hotkey26,hint27,hotkey27)
        self.gen_row(hint28,hotkey28,hint29,hotkey29)
        self.gen_row(hint30,hotkey30,hint31,hotkey31)
        self.gen_row(hint32,hotkey32,hint33,hotkey33)
        self.gen_row(hint41,hotkey41,'','')
        
        self.istr.write('</font></table>')
    
    def generate(self):
        f = '[MClient] logic.Welcome.generate'
        self.istr = io.StringIO()
        sub = _('Welcome to {}!').format(self.desc)
        code = '<html><body><h1>{}</h1><font face="Serif" size="6"><br>'
        code = code.format(sub)
        self.istr.write(code)
        sub = _('This program retrieves translation from online/offline sources.')
        self.istr.write(sub)
        sub = _('Use an entry area below to enter a word/phrase to be translated.')
        code = '<br>{}<br><br>'
        code = code.format(sub)
        self.istr.write(code)
        for source in self.sources:
            self.gen_source_code (title = source.title
                                 ,status = source.status
                                 ,color = source.color
                                 )
        sub1 = _('Offline dictionaries loaded:')
        sub2 = ' Stardict: '
        sub3 = ', Lingvo (DSL): '
        code = '{}{}<font color="{}">{}</font>{}'
        code = code.format(sub1,sub2,self.sdcolor,self.sdstat,sub3)
        self.istr.write(code)
        sub = ', Multitran (Demo): '
        code = '<font color="{}">{}</font>{}<font color="{}'
        code = code.format(self.lgcolor,self.lgstat,sub,self.mtbcolor)
        self.istr.write(code)
        sub1 = _('Main hotkeys')
        sub2 = _('(see documentation for other hotkeys, mouse bindings and functions)')
        code = '">{}</font>{}<br><br><br><br><h1>{}</h1><h2>{}</h2>'
        code = code.format(self.mtbstat,'.',sub1,sub2)
        self.istr.write(code)
        self.set_hotkeys()
        code = '</body></html>'
        self.istr.write(code)
        code = self.istr.getvalue()
        self.istr.close()
        return code

    def run(self):
        self.try_sources()
        return self.generate()



class CurRequest:

    def __init__(self):
        self.set_values()
        self.reset()
    
    def set_values(self):
        self.cols = ('dic','wform','transc','speech')
        self.collimit = sh.lg.globs['int']['colnum'] + len(self.cols)
        ''' Toggling blacklisting should not depend on a number of
            blocked subjects (otherwise, it is not clear how
            blacklisting should be toggled).
            *Temporarily* turn off prioritizing and terms sorting for
            articles with 'sep_words_found' and in phrases; use previous
            settings for new articles.
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
        f = '[MClient] logic.Lists.__init__'
        self.blacklst = objs.get_default().fblock
        self.priorlst = objs.default.fprior
        self.Success = objs.default.Success
    
    def get_blacklist(self):
        f = '[MClient] logic.Lists.get_blacklist'
        if self.Success:
            text = sh.ReadTextFile(self.blacklst,True).get()
            text = sh.Text(text,True).text
            return text.splitlines()
        else:
            sh.com.cancel(f)

    def get_priorities(self):
        f = '[MClient] logic.Lists.get_priorities'
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
                    = self.order = self.blocksdb = self.column_width = None

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
    
    def set_blocks(self,data):
        f = '[MClient] logic.Commands.set_blocks'
        blocks = []
        if not data:
            sh.com.rep_empty(f)
            return blocks
        for row in data:
            block = Block()
            block.no = row[0]
            block.rowno = row[1]
            block.colno = row[2]
            block.text = row[3]
            block.color = row[4]
            block.family = row[5]
            #TODO: delete the multiplier
            #block.size = row[6] * 3
            block.size = row[6]
            block.Bold = row[7]
            block.Italic = row[8]
            blocks.append(block)
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
        f = '[MClient] logic.Commands.export_style'
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
        f = '[MClient] logic.Commands.dump_elems'
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
        f = '[MClient] logic.Commands.suggest'
        items = objs.get_plugins().suggest(search)
        if items:
            if limit:
                items = items[0:limit]
        else:
            items = []
            sh.com.rep_empty(f)
        return items
        
    def use_unverified(self):
        f = '[MClient] logic.Commands.use_unverified'
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
        f = '[MClient] logic.Order._set_lists'
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
    
    def _set_size(self):
        sub = '<span style="font-size:{}pt">{}</span>'
        self.code = sub.format(self.block.size,self.code)
    
    def _set_face(self):
        # style="letter-spacing: 1px"
        sub = '<font face="{}" color="{}">'
        sub = sub.format(self.block.family,self.block.color)
        self.code = sub + self.code
    
    def format(self):
        f = '[MClientQt] logic.Formatter.format'
        if not self.Success:
            sh.com.cancel(f)
            return
        self._set_italic()
        self._set_bold()
        self._set_face()
        self._set_size()
    
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
        f = '[MClient] logic.Cells.debug'
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
        f = '[MClient] logic.Cells.loop'
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
        self.avoid_index_error()
    
    def set_values(self):
        self.table = []
        self.plain = []
        self.cells = []
        self.Success = True
        self.rownum = 0
        self.colnum = 0
    
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
        return(rowno,colno)
    
    def get_last_row(self,rowno,colno):
        f = '[MClientQt] logic.Table.get_last_row'
        if not self.Success:
            sh.com.cancel(f)
            return rowno
        last_rowno = self.rownum - 1
        while last_rowno >= rowno:
            if self.plain[last_rowno][colno]:
                sh.objs.get_mes(f,last_rowno,True).show_debug()
                return last_rowno
            last_rowno -= 1
        return last_rowno
    
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
    
    def avoid_index_error(self):
        f = '[MClientQt] logic.Table.avoid_index_error'
        if not self.Success:
            sh.com.cancel(f)
            return
        plain = []
        table = []
        for rowno in range(self.rownum):
            row = []
            for colno in range(self.colnum):
                row.append('')
            plain.append(row)
            table.append(row)
        for rowno in range(self.rownum):
            for colno in range(self.colnum):
                try:
                    table[rowno][colno] = self.table[rowno][colno]
                    plain[rowno][colno] = self.plain[rowno][colno]
                except IndexError:
                    pass
        #self.plain = plain
        #self.table = table
    
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



class SearchArticle(Table):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def check(self):
        f = '[MClientQt] logic.SearchArticle.check'
        if not self.plain or not self.rownum or not self.colnum:
            self.Success = False
            sh.com.rep_empty(f)
    
    def reset(self,plain,pattern,rowno,colno):
        self.set_values()
        self.plain = plain
        self.pattern = pattern
        self.rowno = rowno
        self.colno = colno
        self.check()
    
    def set_values(self):
        self.plain = []
        self.Success = True
        self.rownum = 0
        self.colnum = 0
        self.rowno = 0
        self.colno = 0
        self.pattern = ''
    
    def search_next(self):
        f = '[MClientQt] logic.SearchArticle.search_next'
        rowno, colno = self.get_next_col(self.rowno,self.colno)
        mes = _('Row #{}. Column #{}: "{}"')
        mes = mes.format(rowno,colno,self.plain[rowno][colno])
        sh.objs.get_mes(f,mes,True).show_debug()
        return(rowno,colno)
    
    def search_prev(self):
        f = '[MClientQt] logic.SearchArticle.search_prev'
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


objs = Objects()
com = Commands()
cf.DefaultKeys()
com.load_config()
# Load lists from files
objs.get_order()
com.set_def_colnum_even()
