#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import skl_shared_qt.web as wb

import logic as lg
import gui as gi

import cells as cl
import subjects.priorities.controller as pr
import subjects.blacklist.controller as bl
import subjects.subjects as sj
import settings.controller as st
import suggest.controller as sg
import about.controller as ab
import third_parties.controller as tp
import symbols.controller as sm
import welcome.controller as wl
import settings.controller as st
import history.controller as hs
import save.controller as sv
import popup.controller as pp


DEBUG = False


class UpdateUI:
    
    def __init__(self,gui):
        self.gui = gui
    
    def restore(self):
        ''' Set widget values to those autosave values that were not previously
            restored by other procedures.
        '''
        f = '[MClient] mclient.UpdateUI.restore'
        mes = _('Restore source language: {}')
        mes = mes.format(sh.lg.globs['str']['lang1'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.get_plugins().set_lang1(sh.lg.globs['str']['lang1'])
        mes = _('Restore target language: {}')
        mes = mes.format(sh.lg.globs['str']['lang2'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.plugins.set_lang2(sh.lg.globs['str']['lang2'])
        self.gui.reset_opt()
        self.gui.opt_src.set(sh.lg.globs['str']['source'])
        self.gui.opt_col.set(sh.lg.globs['int']['colnum'])
    
    def _update_alphabet_image(self):
        if sh.lg.globs['bool']['AlphabetizeTerms'] \
        and not lg.objs.request.SpecialPage:
            self.gui.btn_alp.activate()
        else:
            self.gui.btn_alp.inactivate()
    
    def _update_alphabet_hint(self):
        mes = [_('Sort terms by alphabet')]
        if sh.lg.globs['bool']['AlphabetizeTerms']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        if lg.objs.request.SpecialPage:
            mes.append(_('This page is not supported'))
        self.gui.btn_alp.hint = '\n'.join(mes)
        self.gui.btn_alp.set_hint()
    
    def _update_alphabetization(self):
        self._update_alphabet_image()
        self._update_alphabet_hint()
    
    def _update_vertical_view(self):
        mes = [_('Vertical mode')]
        if sh.lg.globs['bool']['VerticalView']:
            self.gui.btn_viw.inactivate()
            mes.append(_('Status: ON'))
        else:
            self.gui.btn_viw.activate()
            mes.append(_('Status: OFF'))
        self.gui.btn_viw.hint = '\n'.join(mes)
        self.gui.btn_viw.set_hint()
    
    def _update_global_hotkey(self):
        mes = [_('Capture Ctrl-c-c and Ctrl-Ins-Ins')]
        if sh.lg.globs['bool']['CaptureHotkey']:
            self.gui.btn_cap.activate()
            mes.append(_('Status: ON'))
        else:
            self.gui.btn_cap.inactivate()
            mes.append(_('Status: OFF'))
        self.gui.btn_cap.hint = '\n'.join(mes)
        self.gui.btn_cap.set_hint()
    
    def _update_prioritization(self):
        mes = [_('Subject prioritization')]
        prioritized = com.get_prioritized()
        if sh.lg.globs['bool']['PrioritizeSubjects'] and prioritized \
        and not lg.objs.request.SpecialPage:
            self.gui.btn_pri.activate()
        else:
            self.gui.btn_pri.inactivate()
        if sh.lg.globs['bool']['PrioritizeSubjects']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        if lg.objs.request.SpecialPage:
            sub = _('This page is not supported')
        elif prioritized:
            sub = _('{} subjects were prioritized')
            sub = sub.format(len(prioritized))
        else:
            sub = _('Nothing to prioritize')
        mes.append(sub)
        self.gui.btn_pri.hint = '\n'.join(mes)
        self.gui.btn_pri.set_hint()
    
    def _update_block(self):
        f = '[MClient] UpdateUI._update_block'
        mes = [_('Subject blocking')]
        skipped_terms = len(com.get_skipped_terms())
        skipped_dics = len(com.get_skipped_dics())
        if sh.lg.globs['bool']['BlockSubjects'] and skipped_terms:
            self.gui.btn_blk.activate()
        else:
            self.gui.btn_blk.inactivate()
        if sh.lg.globs['bool']['BlockSubjects']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        ''' If this does not work as expected, then TERM might not be
            filled properply.
        '''
        if sh.lg.globs['bool']['BlockSubjects'] and skipped_terms:
            sub = _('Skipped {} terms in {} subjects')
            sub = sub.format(skipped_terms,skipped_dics)
        else:
            sub = _('Nothing was blocked')
        mes.append(sub)
        self.gui.btn_blk.hint = '\n'.join(mes)
        self.gui.btn_blk.set_hint()
    
    def _update_go_next(self):
        if lg.objs.blocksdb.get_next_id(False):
            self.gui.btn_nxt.activate()
        else:
            self.gui.btn_nxt.inactivate()
    
    def _update_go_prev(self):
        # Update the button to move to the previous article
        if lg.objs.get_blocksdb().get_prev_id(False):
            self.gui.btn_prv.activate()
        else:
            self.gui.btn_prv.inactivate()
    
    def _update_last_search(self,searches):
        # Update the button to insert a current search string
        if searches:
            self.gui.btn_rp1.activate()
        else:
            self.gui.btn_rp1.inactivate()
    
    def _update_prev_search(self,searches):
        # Update the button to insert a previous search string
        if searches and len(searches) > 1:
            self.gui.btn_rp2.activate()
        else:
            self.gui.btn_rp2.inactivate()
    
    def update_buttons(self):
        f = '[MClient] mclient.UpdateUI.update_buttons'
        searches = lg.objs.get_blocksdb().get_searches()
        self._update_last_search(searches)
        self._update_prev_search(searches)
        # Suppress useless error output
        if lg.objs.get_request().search:
            self._update_go_prev()
            self._update_go_next()
            self._update_block()
            self._update_prioritization()
        else:
            sh.com.rep_lazy(f)
        self._update_global_hotkey()
        self._update_vertical_view()
        self._update_alphabetization()
    
    def run(self):
        self.update_buttons()



class FontLimits:
    
    def __init__(self,family,size,Bold=False,Italic=False):
        self.set_values()
        self.family = family
        self.size = size
        self.Bold = Bold
        self.Italic = Italic
        self.gui = gi.FontLimits()
        self.set_font()
    
    def set_values(self):
        self.family = 'Sans'
        self.text = ''
        self.font = None
        self.size = 0
        self.Bold = False
        self.Italic = False
    
    def set_text(self,text):
        self.text = str(text)
    
    def set_font(self):
        # 400 is normal, 700 - bold
        if self.Bold:
            weight = 700
        else:
            weight = 400
        self.font = self.gui.get_font (self.family
                                      ,size = self.size
                                      ,weight = weight
                                      ,italic = self.Italic
                                      )
    
    def get_space(self):
        f = '[MClientQt] mclient.FontLimits.get_space'
        space = self.gui.get_space(self.text,self.font)
        #mes = _('Space: {}').format(space)
        #sh.objs.get_mes(f,mes,True).show_debug()
        return space



class Save(sv.Save):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_bindings()
    
    def add_bindings(self):
        self.gui.save.clicked.connect(self.select)
        self.gui.bind('Return',self.select)
        self.gui.bind('Enter',self.select)
    
    def select(self):
        f = '[MClientQt] mclient.Save.select'
        opt = self.get()
        if not opt:
            sh.com.rep_empty(f)
            return
        self.close()
        if opt == _('Save the current view as a web-page (*.htm)'):
            self.save_view_as_htm()
        elif opt == _('Save the original article as a web-page (*.htm)'):
            self.save_raw_as_htm()
        elif opt == _('Save the article as plain text in UTF-8 (*.txt)'):
            self.save_view_as_txt()
        elif opt == _('Copy the code of the article to clipboard'):
            self.copy_raw()
        elif opt == _('Copy the text of the article to clipboard'):
            self.copy_view()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(opt,'; '.join(self.model.items))
            sh.objs.get_mes(f,mes).show_error()

    def _add_web_ext(self):
        if not sh.Path(self.file).get_ext_low() in ('.htm','.html'):
            self.file += '.htm'
    
    def save_view_as_htm(self):
        f = '[MClientQt] mclient.Save.save_view_as_htm'
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        # lg.objs.get_request().htm is allowed to be empty
        if not self.file:
            sh.com.rep_empty(f)
            return
        self._add_web_ext()
        # Takes ~0.47s for 'set' on Intel Atom, do not call in 'load_article'
        code = wb.WebPage(lg.objs.request.htm).make_pretty()
        sh.WriteTextFile(self.file).write(code)

    def save_raw_as_htm(self):
        f = '[MClientQt] mclient.Save.save_raw_as_htm'
        ''' Key 'html' may be needed to write a file in the UTF-8
            encoding, therefore, in order to ensure that the web-page
            is read correctly, we change the encoding manually. We also
            replace abbreviated hyperlinks with full ones in order to
            ensure that they are also valid in the local file.
        '''
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        code = lg.objs.get_blocksdb().get_code()
        if not self.file or not code:
            sh.com.rep_empty(f)
            return
        self._add_web_ext()
        lg.objs.get_plugins().set_htm(code)
        code = lg.objs.plugins.fix_raw_htm()
        sh.WriteTextFile (file = self.file
                         ,Rewrite = True
                         ).write(code)

    def save_view_as_txt(self):
        f = '[MClientQt] mclient.Save.save_view_as_txt'
        self.gui.ask.filter = _('Plain text (*.txt)')
        self.file = self.gui.ask.save()
        if not self.file or not lg.objs.get_request().text:
            sh.com.rep_empty(f)
            return
        if not sh.Path(self.file).get_ext_low() == '.txt':
            self.file += '.txt'
        text = sh.Text(lg.objs.request.text,True).text
        sh.WriteTextFile (file = self.file
                         ,Rewrite = True
                         ).write(text)

    def copy_raw(self):
        f = '[MClientQt] mclient.Save.copy_raw'
        code = lg.objs.get_blocksdb().get_code()
        if not code:
            sh.com.rep_empty(f)
            return
        sh.Clipboard().copy(code)

    def copy_view(self):
        f = '[MClientQt] mclient.Save.copy_view'
        text = sh.Text(lg.objs.get_request().text,True).text
        if text:
            sh.Clipboard().copy(text)
        else:
            sh.com.rep_empty(f)



class Commands:
    #NOTE: DB is in controller (not in logic), so DB-related code is here too
    def get_skipped_terms(self):
        f = '[MClientQt] mclient.Commands.get_skipped_terms'
        skipped = lg.objs.get_blocksdb().get_skipped_terms()
        if not skipped:
            return []
        # TERM can be empty for some reason
        skipped = [item for item in skipped if item]
        # We already use 'distinct' in DB, no need to use 'set'
        skipped.sort()
        mes = '; '.join(skipped)
        sh.objs.get_mes(f,mes,True).show_debug()
        return skipped
    
    def get_skipped_dics(self):
        f = '[MClient] mclient.Commands.get_skipped_dics'
        skipped = lg.objs.get_blocksdb().get_skipped_dics()
        if not skipped:
            return []
        skipped = ', '.join(skipped)
        skipped = skipped.split(', ')
        skipped = sorted(set(skipped))
        mes = '; '.join(skipped)
        sh.objs.get_mes(f,mes,True).show_debug()
        return skipped
    
    def get_prioritized(self):
        f = '[MClient] mclient.Commands.get_prioritized'
        prioritized = lg.objs.get_blocksdb().get_prioritized()
        if not prioritized:
            return []
        prioritized = ', '.join(prioritized)
        prioritized = prioritized.split(', ')
        prioritized = set(prioritized)
        mes = '; '.join(prioritized)
        sh.objs.get_mes(f,mes,True).show_debug()
        return prioritized



class Welcome(wl.Welcome):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.sources = []
    
    def loop_online_sources(self):
        code = []
        for source in self.sources:
            if source.Online:
                desc = self.gen_online_source (title = source.title
                                              ,status = source.status
                                              ,color = source.color
                                              )
                code.append(desc)
        code = ', '.join(code) + '.'
        code = self.set_font(code)
        self.logic.table.append([code])
    
    def loop_offline_sources(self):
        code = []
        for source in self.sources:
            if not source.Online:
                desc = self.gen_offline_source (title = source.title
                                               ,status = source.status
                                               ,color = source.color
                                               )
                code.append(desc)
        code = _('Offline dictionaries loaded: ') + ', '.join(code) + '.'
        code = self.set_font(code)
        self.logic.table.append([code])
    
    def gen_online_source(self,title,status,color):
        code = '<b>{} <font color="{}">{}</font></b>'
        code = code.format(title,color,status)
        return code
    
    def gen_offline_source(self,title,status,color):
        code = '{}: <font color="{}">{}</font>'
        code = code.format(title,color,status)
        return code
    
    def fill(self):
        model = wl.TableModel(self.run())
        self.set_model(model)
    
    def set_online_sources(self):
        f = '[MClientQt] mclient.Welcome.set_online_sources'
        if not sh.lg.globs['bool']['Ping']:
            sh.com.rep_lazy(f)
            return
        old = lg.objs.get_plugins().source
        dics = lg.objs.plugins.get_online_sources()
        if not dics:
            sh.com.rep_empty(f)
            return
        for dic in dics:
            lg.objs.plugins.set(dic)
            isource = lg.Source()
            isource.title = dic
            isource.Online = True
            if lg.objs.plugins.is_accessible():
                isource.status = _('running')
                isource.color = 'green'
            self.sources.append(isource)
        lg.objs.plugins.set(old)
    
    def set_offline_sources(self):
        f = '[MClientQt] mclient.Welcome.set_offline_sources'
        dics = lg.objs.plugins.get_offline_sources()
        if not dics:
            sh.com.rep_empty(f)
            return
        old = lg.objs.get_plugins().source
        for dic in dics:
            lg.objs.plugins.set(dic)
            isource = lg.Source()
            isource.title = dic
            dic_num = lg.objs.plugins.is_accessible()
            isource.status = dic_num
            if dic_num:
                isource.color = 'green'
            self.sources.append(isource)
        lg.objs.plugins.set(old)
    
    def set_sources(self):
        self.set_online_sources()
        self.set_offline_sources()

    def set_middle(self):
        self.set_sources()
        self.loop_online_sources()
        self.loop_offline_sources()
    
    def run(self):
        self.set_head()
        self.set_middle()
        self.set_tail()
        return self.logic.table



class About(ab.About):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.parties = tp.ThirdParties()
        self.add_bindings()

    def add_bindings(self):
        self.gui.btn_thd.set_action(self.parties.show)
        self.gui.btn_lic.set_action(self.parties.open_license_url)
        self.gui.btn_eml.set_action(self.parties.send_feedback)



class Table:

    def __init__(self):
        self.set_values()
        self.logic = lg.Table()
        self.gui = gi.Table()
        self.search = Search()
        self.popup = pp.Popup()
        self.set_gui()
    
    def show_popup(self):
        f = '[MClientQt] mclient.Table.show_popup'
        text = self.get_cell_code()
        if not text:
            sh.com.rep_empty(f)
            return
        self.popup.fill(text)
        self.popup.show()
    
    def go_next_section(self,no):
        f = '[MClientQt] mclient.Table.go_next_section'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row_by_col(rowno,colno,no)
        self.select(rowno,colno)
    
    def go_prev_section(self,no):
        f = '[MClientQt] mclient.Table.go_prev_section'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row_by_col(rowno,colno,no)
        self.select(rowno,colno)
    
    def close_search_next(self):
        f = '[MClientQt] mclient.Table.close_search_next'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.search.close()
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno,colno)
    
    def reset_search(self):
        f = '[MClientQt] mclient.Table.reset_search'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        self.search.reset(self.logic.cells,self.logic.plain,rowno,colno)
    
    def search_next(self):
        f = '[MClientQt] mclient.Table.search_next'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno,colno)
    
    def search_prev(self):
        f = '[MClientQt] mclient.Table.search_prev'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.reset_search()
        rowno, colno = self.search.search_prev()
        self.select(rowno,colno)
    
    def set_values(self):
        self.Success = True
        self.model = None
        self.coords = {}
        self.row_height = 42
        self.old_rowno = -1
        self.old_colno = -1
    
    def go_end(self):
        f = '[MClientQt] mclient.Table.go_end'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.logic.get_end()
        self.select(rowno,colno)
    
    def go_start(self):
        f = '[MClientQt] mclient.Table.go_start'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.logic.get_start()
        self.select(rowno,colno)
    
    def go_down(self):
        ''' #NOTE: This should run only after an event since Qt returns dummy
            geometry values right after startup.
        '''
        f = '[MClientQt] mclient.Table.go_down'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row(rowno,colno)
        self.select(rowno,colno)
    
    def select(self,rowno,colno,Mouse=False):
        f = '[MClientQt] mclient.Table.select'
        if not self.Success:
            sh.com.cancel(f)
            return
        if Mouse and self.search.Shown:
            return
        if not self.model:
            sh.com.rep_empty(f)
            return
        if rowno == self.old_rowno and colno == self.old_colno:
            return
        self.old_rowno = rowno
        self.old_colno = colno
        self.model.update(self.gui.get_index())
        new_index = self.model.index(rowno,colno)
        if Mouse:
            self.gui.set_index(new_index)
        else:
            self.gui.set_cur_index(new_index)
        self.model.update(new_index)
        if not Mouse:
            self.scroll_top()
        if Mouse:
            if new_index in self.gui.delegate.long:
                self.popup.adjust_position(self.gui.x_,self.gui.y_)
                self.show_popup()
            else:
                self.popup.close()
    
    def go_up(self):
        f = '[MClientQt] mclient.Table.go_up'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row(rowno,colno)
        self.select(rowno,colno)
    
    def go_line_start(self):
        f = '[MClientQt] mclient.Table.go_line_start'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_start(rowno)
        self.select(rowno,colno)
    
    def go_line_end(self):
        f = '[MClientQt] mclient.Table.go_line_end'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_end(rowno)
        self.select(rowno,colno)
    
    def go_left(self):
        f = '[MClientQt] mclient.Table.go_left'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_col(rowno,colno)
        self.select(rowno,colno)
    
    def go_right(self):
        f = '[MClientQt] mclient.Table.go_right'
        if not self.Success:
            sh.com.cancel(f)
            return
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_col(rowno,colno)
        self.select(rowno,colno)
    
    def scroll_top(self):
        f = '[MClientQt] mclient.Table.scroll_top'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.coords or not self.model:
            sh.com.rep_empty(f)
            return
        rowno, colno = self.gui.get_cell()
        ''' #FIX: Getting KeyError: -1 here when copying a cell, pasting it,
            setting focus to ent_src and pressing Home.
        '''
        index_ = self.model.index(self.coords[rowno],colno)
        self.gui.scroll2index(index_)
    
    def get_cell(self):
        f = '[MClientQt] mclient.Table.get_cell'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            return self.gui.get_cell()
        except Exception as e:
            sh.com.rep_third_party(f,e)
            return(0,0)
    
    def get_cell_text(self):
        f = '[MClientQt] mclient.Table.get_cell_text'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        if not self.logic.cells:
            sh.com.rep_empty(f)
            return ''
        rowno, colno = self.get_cell()
        try:
            #return self.logic.cells[rowno][colno].plain
            return self.logic.plain[rowno][colno]
        except IndexError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_debug()
        return ''
    
    def get_cell_code(self):
        f = '[MClientQt] mclient.Table.get_cell_code'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        if not self.logic.cells:
            sh.com.rep_empty(f)
            return ''
        rowno, colno = self.get_cell()
        try:
            return self.logic.table[rowno][colno]
        except IndexError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_debug()
        return ''
    
    def copy_cell(self):
        f = '[MClientQt] mclient.Table.copy_cell'
        if not self.Success:
            sh.com.cancel(f)
            return
        text = self.get_cell_text()
        if text:
            sh.Clipboard().copy(text)
            return True
        # Do not warn when there are no articles yet
        elif lg.objs.blocksdb.artid == 0:
            sh.com.rep_lazy(f)
        else:
            mes = _('This cell does not contain any text!')
            sh.objs.get_mes(f,mes).show_warning()
    
    def set_row_height(self,height=42):
        for no in range(self.logic.rownum):
            self.gui.set_row_height(no,height)
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        f = '[MClientQt] mclient.Table.set_col_width'
        mes = _('Number of columns: {}').format(self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        #TODO: Rework, number of fixed columns can be different
        for no in range(self.logic.colnum):
            if no == 0:
                width = 140
            elif no == 1:
                width = sh.lg.globs['int']['fixed_col_width']
            elif no in (2,3):
                width = 63
            else:
                width = sh.lg.globs['int']['term_col_width']
            self.gui.set_col_width(no,width)
    
    def reset(self,cells):
        f = '[MClientQt] mclient.Table.reset'
        self.set_values()
        if not cells:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.logic.reset(cells)
        self.Success = self.logic.Success
        self.model = gi.TableModel(self.logic.table)
        self.fill()
        self.set_col_width()
        self.set_row_height(self.row_height)
        self.show_borders(False)
        self.set_long()
        ''' Coordinates are recreated each time the app window is resized. Here
            we merely suppress a warning at 'self.go_start'.
        '''
        self.set_coords()
        self.go_start()
    
    def set_long(self):
        # Takes ~0.56s for 'set' on Intel Atom
        f = '[MClientQt] mclient.Table.set_long'
        if not self.Success:
            sh.com.cancel(f)
            return
        ilimits = FontLimits (family = sh.lg.globs['str']['font_terms_family']
                             ,size = sh.lg.globs['int']['font_terms_size']
                             ,Bold = False
                             ,Italic = False
                             )
        timer = sh.Timer(f)
        timer.start()
        self.gui.delegate.long = []
        for rowno in range(self.logic.rownum):
            for colno in range(self.logic.colnum):
                ilimits.set_text(self.logic.plain[rowno][colno])
                space = ilimits.get_space()
                index_ = self.model.index(rowno,colno)
                hint_space = self.row_height * self.gui.get_col_width(colno)
                if space > hint_space:
                    self.gui.delegate.long.append(index_)
        timer.end()
        mes = _('Number of cells: {}').format(self.logic.rownum*self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Number of long cells: {}').format(len(self.gui.delegate.long))
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_coords(self,event=None):
        ''' Calculating Y is very fast (~0.05s for 'set' on Intel Atom). We
            need None since this procedure overrides
            self.gui.parent.resizeEvent.
        '''
        f = '[MClientQt] mclient.Table.set_coords'
        if not self.Success:
            sh.com.cancel(f)
            return
        height = self.gui.get_height()
        mes = _('Window height: {}').format(height)
        sh.objs.get_mes(f,mes,True).show_debug()
        for rowno in range(self.logic.rownum):
            y = self.gui.get_cell_y(rowno) + self.gui.get_row_height(rowno)
            pageno = int(y / height)
            page_y = pageno * height
            page_rowno = self.gui.get_row_by_y(page_y)
            self.coords[rowno] = page_rowno
    
    def fill(self):
        f = '[MClientQt] mclient.Table.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        timer = sh.Timer(f)
        timer.start()
        self.gui.set_model(self.model)
        timer.end()
    
    def set_max_row_height(self,height=150):
        self.gui.set_max_row_height(height)
    
    def show_borders(self,Show=False):
        self.gui.show_borders(Show)
    
    def set_gui(self):
        #self.set_max_row_height()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.sig_select.connect(self.select)
        self.search.gui.ent_src.bind('Return',self.close_search_next)
        self.search.gui.btn_srp.set_action(self.search_prev)
        self.search.gui.btn_srn.set_action(self.search_next)
        self.popup.gui.sig_close.connect(self.popup.close)



class App:
    
    def __init__(self):
        self.gui = gi.App()
        self.set_gui()
        self.update_ui()
    
    def toggle_view(self):
        if sh.lg.globs['bool']['VerticalView']:
            sh.lg.globs['bool']['VerticalView'] = False
        else:
            sh.lg.globs['bool']['VerticalView'] = True
        #lg.objs.get_blocksdb().delete_bookmarks()
        self.load_article()
    
    def toggle_alphabet(self):
        if sh.lg.globs['bool']['AlphabetizeTerms']:
            sh.lg.globs['bool']['AlphabetizeTerms'] = False
        else:
            sh.lg.globs['bool']['AlphabetizeTerms'] = True
        #lg.objs.get_blocksdb().delete_bookmarks()
        self.load_article()
    
    def add_history(self):
        # Call this only after assigning an article ID for a new article
        f = '[MClientQt] mclient.App.add_history'
        if not lg.objs.get_request().search:
            sh.com.rep_lazy(f)
            return
        self.history.add_row (id_ = lg.objs.get_blocksdb().artid
                             ,source = lg.objs.get_plugins().source
                             ,lang1 = lg.objs.plugins.get_lang1()
                             ,lang2 = lg.objs.plugins.get_lang2()
                             ,search = lg.objs.request.search
                             )
        # Setting column width works only after updating the model, see https://stackoverflow.com/questions/8364061/how-do-you-set-the-column-width-on-a-qtreeview
        self.history.gui.set_col_width()
    
    def go_history(self,id_):
        f = '[MClientQt] mclient.App.go_history'
        if id_ is None:
            sh.com.rep_empty(f)
            return
        lg.objs.get_blocksdb().artid = id_
        result = lg.objs.blocksdb.get_article()
        if not result:
            sh.com.rep_empty(f)
            return
        sh.lg.globs['str']['source'] = result[0] # SOURCE
        lg.objs.request.search = result[1]       # TITLE
        lg.objs.request.url = result[2]          # URL
        mes = _('Set source to "{}"')
        mes = mes.format(sh.lg.globs['str']['source'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
        lg.objs.plugins.set_lang1(result[4])
        lg.objs.plugins.set_lang2(result[5])
        self.reset_opt(sh.lg.globs['str']['source'])
        self.load_article()
    
    def clear_history(self):
        lg.objs.get_blocksdb().clear()
        lg.objs.get_request().reset()
        self.reset()
    
    def go_back(self):
        f = '[MClientQt] mclient.App.go_back'
        result = lg.objs.get_blocksdb().get_prev_id()
        if not result:
            sh.com.rep_empty(f)
            return
        lg.objs.blocksdb.artid = result
        result = lg.objs.blocksdb.get_article()
        if not result:
            sh.com.rep_empty(f)
            return
        sh.lg.globs['str']['source'] = result[0]
        lg.objs.get_request().search = result[1]
        lg.objs.request.url = result[2]
        lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
        lg.objs.plugins.set_lang1(result[4])
        lg.objs.plugins.set_lang2(result[5])
        self.reset_opt(sh.lg.globs['str']['source'])
        self.load_article()
    
    def go_next(self):
        f = '[MClientQt] mclient.App.go_next'
        result = lg.objs.get_blocksdb().get_next_id()
        if not result:
            sh.com.rep_empty(f)
            return
        lg.objs.blocksdb.artid = result
        result = lg.objs.blocksdb.get_article()
        if not result:
            sh.com.rep_empty(f)
            return
        sh.lg.globs['str']['source'] = result[0]
        lg.objs.get_request().search = result[1]
        lg.objs.request.url = result[2]
        lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
        lg.objs.plugins.set_lang1(result[4])
        lg.objs.plugins.set_lang2(result[5])
        self.reset_opt(sh.lg.globs['str']['source'])
        self.load_article()
    
    def get_width(self):
        return self.gui.get_width()
    
    def _set_col_num(self,window_width):
        if window_width <= 1024:
            return 3
        else:
            return 5
    
    def suggest_col_widths(self):
        f = '[MClientQt] mclient.App.suggest_col_widths'
        table_width = self.get_width()
        if not table_width:
            sh.com.rep_empty(f)
            return
        col_num = self.settings.gui.ent_num.get()
        if not col_num:
            col_num = self._set_col_num(table_width)
        col_num = sh.Input(f,col_num).get_integer()
        if not 0 < col_num <= 10:
            mes = _('A value of this field should be within the range of {}-{}!')
            mes = mes.format(1,10)
            sh.objs.get_mes(f,mes).show_warning()
            col_num = self._set_col_num(table_width)
        
        ''' How we got this formula. The recommended fixed column width
            is 63 (provided that there are 4 fixed columns). This value
            does not depend on a screen size (but is font-dependent).
            63 * 4 = 252. 79.77% is the recommended value of
            a calculated term column width. We need this to be less than
            100% since a width of columns in HTML cannot be less than
            the text width, and we may have pretty long lines sometimes.
        '''
        term_width = 0.7977 * ((table_width - 252) / col_num)
        # Values in pixels must be integer
        term_width = int(term_width)
        
        mes = _('Table width: {}').format(table_width)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Term column width: {}').format(term_width)
        sh.objs.get_mes(f,mes,True).show_debug()
        
        self.settings.gui.ent_num.set_text(col_num)
        self.settings.gui.ent_fix.set_text(63)
        self.settings.gui.ent_trm.set_text(term_width)
    
    def set_col_num(self):
        ''' #TODO: Do we need this?
        if not sh.lg.globs['bool']['AdjustByWidth']:
            sh.com.rep_lazy(f)
            return
        '''
        self.gui.panel.opt_col.set(sh.lg.globs['int']['colnum'])
    
    def apply_settings(self):
        self.settings.close()
        st.Save().run()
        lg.com.export_style()
        self.set_col_num()
        # This loads the article and must come the last
        self.set_columns()
    
    def change_col_no(self,no):
        self.gui.panel.opt_col.set(no)
        self.set_columns()

    def set_columns(self):
        self.reset_columns()
        #lg.objs.get_blocksdb().delete_bookmarks()
        self.load_article()
        self.gui.panel.ent_src.focus()

    def reset_columns(self):
        f = '[MClientQt] mclient.App.reset_columns'
        fixed = [col for col in lg.objs.get_request().cols \
                 if col != _('Do not set')
                ]
        sh.lg.globs['int']['colnum'] = sh.Input (title = f
                                                ,value = self.gui.panel.opt_col.get()
                                                ).get_integer()
        lg.objs.request.collimit = sh.lg.globs['int']['colnum'] + len(fixed)
        mes = _('Set the number of columns to {}')
        mes = mes.format(lg.objs.request.collimit)
        sh.objs.get_mes(f,mes,True).show_info()
    
    def update_columns(self):
        ''' Update a column number in GUI; adjust the column number
            (both logic and GUI) in special cases.
        '''
        f = '[MClientQt] mclient.App.update_columns'
        lg.com.update_colnum()
        fixed = [col for col in lg.objs.get_request().cols \
                 if col != _('Do not set')
                ]
        lg.objs.get_request().collimit = len(fixed) + sh.lg.globs['int']['colnum']
        self.gui.panel.opt_col.set(sh.lg.globs['int']['colnum'])
        mes = _('Set the column limit to {} ({} in total)')
        mes = mes.format (sh.lg.globs['int']['colnum']
                         ,lg.objs.request.collimit
                         )
        sh.objs.get_mes(f,mes,True).show_info()
        lg.com.set_def_colnum_even()
    
    def set_source(self):
        f = '[MClientQt] mclient.App.set_source'
        sh.lg.globs['str']['source'] = self.gui.panel.opt_src.get()
        mes = _('Set source to "{}"').format(sh.lg.globs['str']['source'])
        sh.objs.get_mes(f,mes,True).show_info()
        lg.objs.get_plugins().set(sh.lg.globs['str']['source'])
        self.reset_opt(sh.lg.globs['str']['source'])
        self.go_search_focus()
    
    def auto_swap(self):
        f = '[MClientQt] mclient.App.auto_swap'
        lang1 = self.gui.panel.opt_lg1.get()
        lang2 = self.gui.panel.opt_lg2.get()
        if lg.objs.get_plugins().is_oneway() \
        or not sh.lg.globs['bool']['Autoswap'] \
        or not lg.objs.get_request().search:
            sh.com.rep_lazy(f)
            return
        if sh.Text(lg.objs.request.search).has_cyrillic():
            if lang2 in (_('Russian'),'Russian'):
                mes = '{}-{} -> {}-{}'.format(lang1,lang2,lang2,lang1)
                sh.objs.get_mes(f,mes,True).show_info()
                self.swap_langs()
        elif lang1 in (_('Russian'),'Russian'):
            mes = '{}-{} -> {}-{}'.format(lang1,lang2,lang2,lang1)
            sh.objs.get_mes(f,mes,True).show_info()
            self.swap_langs()
    
    def go_search_focus(self):
        self.go_search()
        self.gui.panel.ent_src.focus()
    
    def reset_opt(self,default=_('Multitran')):
        f = '[MClientQt] mclient.App.reset_opt'
        # Reset OptionMenus
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs1 = lg.objs.plugins.get_langs1()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        sources = lg.objs.plugins.get_sources()
        if not (langs1 and langs2 and lang1 and lang2 and sources):
            sh.com.rep_empty(f)
            return
        self.gui.panel.opt_lg1.reset (items = langs1
                                     ,default = lang1
                                     )
        self.gui.panel.opt_lg2.reset (items = langs2
                                     ,default = lang2
                                     )
        #NOTE: change this upon the change of the default source
        self.gui.panel.opt_src.reset (items = sources
                                     ,default = default
                                     )
    
    def set_next_lang1(self):
        ''' We want to navigate through the full list of supported languages
            rather than through the list of 'lang2' pairs so we reset the
            widget first.
        '''
        old = self.gui.panel.opt_lg1.get()
        self.gui.panel.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                                     ,default = old
                                     )
        self.gui.panel.opt_lg1.set_next()
        self.update_lang1()
        self.update_lang2()
    
    def set_next_lang2(self):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        self.gui.panel.opt_lg2.set_next()
        self.update_lang2()
    
    def set_prev_lang1(self):
        ''' We want to navigate through the full list of supported languages
            rather than through the list of 'lang2' pairs so we reset the
            widget first.
        '''
        old = self.gui.panel.opt_lg1.get()
        self.gui.panel.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                                     ,default = old
                                     )
        self.gui.panel.opt_lg1.set_prev()
        self.update_lang1()
        self.update_lang2()
    
    def set_prev_lang2(self):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        self.gui.panel.opt_lg2.set_prev()
        self.update_lang2()
    
    def set_lang1(self):
        f = '[MClientQt] mclient.App.set_lang1'
        lang = self.gui.panel.opt_lg1.get()
        if lg.objs.get_plugins().get_lang1() != lang:
            mes = _('Set language: {}').format(lang)
            sh.objs.get_mes(f,mes,True).show_info()
            sh.lg.globs['str']['lang1'] = lang
            lg.objs.get_plugins().set_lang1(lang)
    
    def set_lang2(self):
        f = '[MClientQt] mclient.App.set_lang2'
        lang = self.gui.panel.opt_lg2.get()
        if lg.objs.get_plugins().get_lang2() != lang:
            mes = _('Set language: {}').format(lang)
            sh.objs.get_mes(f,mes,True).show_info()
            sh.lg.globs['str']['lang2'] = lang
            lg.objs.get_plugins().set_lang2(lang)
    
    def update_lang1(self):
        f = '[MClientQt] mclient.App.update_lang1'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs1 = lg.objs.plugins.get_langs1()
        if not langs1:
            sh.com.rep_empty(f)
            return
        self.gui.panel.opt_lg1.set(lang1)
        self.set_lang1()
    
    def update_lang2(self):
        f = '[MClientQt] mclient.App.update_lang2'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        if not langs2:
            sh.com.rep_empty(f)
            return
        if not lang2 in langs2:
            lang2 = langs2[0]
        self.gui.panel.opt_lg2.reset (items = langs2
                                     ,default = lang2
                                     )
        self.set_lang2()
    
    def swap_langs(self):
        f = '[MClientQt] mclient.App.swap_langs'
        if lg.objs.get_plugins().is_oneway():
            mes = _('Cannot swap languages, this is a one-way dictionary!')
            sh.objs.get_mes(f,mes).show_info()
            return
        self.update_lang1()
        self.update_lang2()
        lang1 = self.gui.panel.opt_lg1.get()
        lang2 = self.gui.panel.opt_lg2.get()
        lang1, lang2 = lang2, lang1
        langs1 = lg.objs.get_plugins().get_langs1()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        if not langs1:
            sh.com.rep_empty(f)
            return
        if not (langs2 and lang1 in langs1 and lang2 in langs2):
            mes = _('Pair {}-{} is not supported!').format(lang1,lang2)
            sh.objs.get_mes(f,mes).show_warning()
            return
        self.gui.panel.opt_lg1.reset (items = langs1
                                     ,default = lang1
                                     )
        self.gui.panel.opt_lg2.reset (items = langs2
                                     ,default = lang2
                                     )
        self.update_lang1()
        self.update_lang2()
    
    def insert_repeat_sign2(self):
        # Insert the previous search string
        f = '[MClientQt] mclient.App.insert_repeat_sign2'
        result = lg.objs.get_blocksdb().get_prev_id()
        if result:
            old = lg.objs.blocksdb.artid
            lg.objs.blocksdb.artid = result
            result = lg.objs.blocksdb.get_article()
            if result:
                sh.Clipboard().copy(result[1])
                self.paste()
            else:
                sh.com.rep_empty(f)
            lg.objs.blocksdb.artid = old
        else:
            sh.com.rep_empty(f)
    
    def insert_repeat_sign(self):
        # Insert the current search string
        sh.Clipboard().copy(lg.objs.get_request().search)
        self.paste()
    
    def go_url(self):
        f = '[MClientQt] mclient.App.go_url'
        rowno, colno = self.table.get_cell()
        cell = lg.com.get_cell(self.table.logic.cells,rowno,colno)
        if not cell:
            sh.com.rep_empty(f)
            return
        if cell.url:
            lg.objs.request.search = self.table.get_cell_text()
            lg.objs.request.url = cell.url
            mes = _('Open link: {}').format(lg.objs.request.url)
            sh.objs.get_mes(f,mes,True).show_info()
            self.load_article()
        elif lg.objs.blocksdb.artid == 0:
            # Do not warn when there are no articles yet
            sh.com.rep_lazy(f)
        else:
            lg.objs.request.search = self.table.get_cell_text()
            self.go_search()
    
    def copy_cell(self):
        ''' Do not combine these conditions with 'and' since the interpreter
            may decide to check the lighter condition first.
        '''
        if self.table.copy_cell():
            if sh.lg.globs['bool']['Iconify']:
                self.minimize()
    
    def copy_symbol(self):
        symbol = self.symbols.get()
        sh.Clipboard().copy(symbol)
    
    def paste_symbol(self):
        symbol = self.symbols.get()
        self.gui.panel.ent_src.insert(symbol)
    
    def load_article(self):
        f = '[MClientQt] mclient.App.load_article'
        ''' #NOTE: each time the contents of the current page is changed
            (e.g., due to prioritizing), bookmarks must be deleted.
        '''
        # Suppress useless error output
        if not lg.objs.get_request().search:
            return
        timer = sh.Timer(f)
        #timer.start()
        # Do not allow selection positions from previous articles
        self.pos = -1

        '''
        order = objs.get_settings().get_speech_prior()
        lg.objs.get_speech_prior().reset(order)
        '''

        artid = lg.objs.get_blocksdb().is_present (source = sh.lg.globs['str']['source']
                                                  ,title = lg.objs.request.search
                                                  ,url = lg.objs.request.url
                                                  )
        if artid:
            mes = _('Load article No. {} from memory').format(artid)
            sh.objs.get_mes(f,mes,True).show_info()
            lg.objs.blocksdb.artid = artid
            #self.get_bookmark()
        else:
            blocks = lg.objs.get_plugins().request (search = lg.objs.request.search
                                                   ,url = lg.objs.request.url
                                                   )
            # 'None' skips the autoincrement
            data = (None                              # (00) ARTICLEID
                   ,sh.lg.globs['str']['source']      # (01) SOURCE
                   ,lg.objs.request.search            # (02) TITLE
                   ,lg.objs.request.url               # (03) URL
                   ,lg.objs.get_plugins().get_lang1() # (04) LANG1
                   ,lg.objs.plugins.get_lang2()       # (05) LANG2
                   ,self.pos                          # (06) BOOKMARK
                   ,lg.objs.plugins.get_htm()         # (07) CODE
                   )
            lg.objs.blocksdb.fill_articles(data)
            lg.objs.blocksdb.artid = lg.objs.blocksdb.get_max_artid()
            data = lg.com.dump_elems (blocks = blocks
                                     ,artid = lg.objs.blocksdb.artid
                                     )
            if data:
                lg.objs.blocksdb.fill_blocks(data)
            
            lg.objs.blocksdb.update_phterm()
            
        timer.start()
        self.phdic = lg.objs.blocksdb.get_phdic()
        if self.phdic:
            if sh.lg.globs['bool']['ShortSubjects']:
                self.phdic = self.phdic[0]
            else:
                self.phdic = self.phdic[1]
        else:
            self.phdic = ''
        
        old_special = lg.objs.request.SpecialPage
        if self.phdic:
            lg.objs.request.SpecialPage = False
        else:
            # Otherwise, 'SpecialPage' will be inherited
            lg.objs.request.SpecialPage = True
        lg.objs.request.NewPageType = old_special != lg.objs.request.SpecialPage
        self.update_columns()
        
        SortTerms = sh.lg.globs['bool']['AlphabetizeTerms'] \
                    and not lg.objs.request.SpecialPage
        ''' We must reset DB as early as possible after setting 'elems',
            otherwise, real and loaded settings may not coincide, which,
            in turn, may lead to a data loss, see, for example, RU-EN:
            "цепь: провод".
        '''
        lg.objs.blocksdb.reset (cols = lg.objs.request.cols
                               ,SortRows = sh.lg.globs['bool']['SortByColumns']
                               ,SortTerms = SortTerms
                               ,ExpandDic = not sh.lg.globs['bool']['ShortSubjects']
                               ,ShowUsers = sh.lg.globs['bool']['ShowUserNames']
                               ,PhraseCount = sh.lg.globs['bool']['PhraseCount']
                               )
        sj.objs.get_article().reset (pairs = lg.objs.blocksdb.get_dic_pairs()
                                    ,Debug = lg.objs.get_plugins().Debug
                                    )
        sj.objs.article.run()
        data = lg.objs.blocksdb.assign_bp()
        spdic = lg.objs.get_speech_prior().get_all2prior()
        bp = cl.BlockPrioritize (data = data
                                ,Block = sh.lg.globs['bool']['BlockSubjects']
                                ,Prioritize = sh.lg.globs['bool']['PrioritizeSubjects']
                                ,phdic = self.phdic
                                ,spdic = spdic
                                ,Debug = lg.objs.plugins.Debug
                                ,maxrows = lg.objs.plugins.maxrows
                                )
        bp.run()
        lg.objs.blocksdb.update(bp.query)
        
        lg.objs.blocksdb.unignore()
        lg.objs.blocksdb.ignore()
        
        data = lg.objs.blocksdb.assign_cells()

        if sh.lg.globs['bool']['ShortSpeech']:
            spdic = {}
        else:
            spdic = lg.objs.speech_prior.get_abbr2full()
        
        cells = cl.Cells (data = data
                         ,cols = lg.objs.request.cols
                         ,collimit = lg.objs.request.collimit
                         ,phdic = self.phdic
                         ,spdic = spdic
                         ,Reverse = sh.lg.globs['bool']['VerticalView']
                         ,Debug = lg.objs.plugins.Debug
                         ,maxrows = lg.objs.plugins.maxrows
                         )
        cells.run()
        cells.dump(lg.objs.blocksdb)
        
        lg.objs.get_column_width().reset()
        lg.objs.column_width.run()
        
        blocks = lg.com.assign_blocks(lg.objs.blocksdb.fetch())
        blocks = lg.com.add_formatting(blocks)
        
        cells = lg.Cells(blocks).run()
        self.table.reset(cells)
        
        skipped = com.get_skipped_terms()
        # This is fast
        lg.objs.request.htm = lg.HTM(cells,skipped).run()
        lg.objs.request.text = lg.com.get_text(cells)
        colors = lg.com.get_colors(blocks)
        lg.com.fix_colors(colors)
        
        ''' Empty article is not added either to DB or history, so we just do
            not clear the search field to be able to correct the typo.
        '''
        if cells or skipped:
            self.gui.panel.ent_src.reset()
        
        self.add_history()
        
        #objs.get_suggest().close()
        UpdateUI(self.panel).run()
        timer.end()
        self.panel.ent_src.focus()
        #self.run_final_debug()
        #self.debug_settings()
        return blocks
    
    def go_keyboard(self):
        f = '[MClientQt] mclient.App.go_keyboard'
        search = self.panel.ent_src.get().strip()
        if search == '':
            self.go_url()
        elif search == sh.lg.globs['str']['repeat_sign']:
            self.insert_repeat_sign()
        elif search == sh.lg.globs['str']['repeat_sign2']:
            self.insert_repeat_sign2()
        else:
            lg.objs.get_request().search = search
            self.go_search()
    
    def go_search(self):
        f = '[MClientQt] mclient.App.go_search'
        if lg.objs.get_request().search is None:
            lg.objs.request.search = ''
        lg.objs.request.search = lg.objs.request.search.strip()
        if lg.com.control_length():
            self.update_lang1()
            self.update_lang2()
            self.auto_swap()
            lg.com.get_url()
            mes = '"{}"'.format(lg.objs.request.search)
            sh.objs.get_mes(f,mes,True).show_debug()
            self.load_article()
    
    def clear_search_field(self):
        #TODO: implement
        #objs.get_suggest().get_gui().close()
        self.panel.ent_src.clear()
    
    def paste(self):
        self.panel.ent_src.set_text(sh.Clipboard().paste())
    
    def reset(self):
        f = '[MClientQt] mclient.App.reset'
        #TODO: show Welcome
    
    def minimize(self):
        self.gui.minimize()
    
    def update_ui(self):
        self.gui.panel.ent_src.focus()
        self.reset_opt()
    
    def show(self):
        self.gui.show()
    
    def quit(self):
        lg.objs.get_order().save()
        lg.com.save_config()
        mes = _('Goodbye!')
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.sig_close.connect(self.quit)
        
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Down',self.table.go_down)
        self.gui.bind('Up',self.table.go_up)
        self.gui.bind('Ctrl+Home',self.table.go_start)
        self.gui.bind('Ctrl+End',self.table.go_end)
        self.gui.bind('Home',self.table.go_line_start)
        self.gui.bind('End',self.table.go_line_end)
        self.gui.bind('Left',self.table.go_left)
        self.gui.bind('Right',self.table.go_right)
        self.gui.bind('F1',self.about.toggle)
        self.gui.bind('F3',self.table.search_next)
        self.gui.bind('Shift+F3',self.table.search_prev)
        self.gui.bind('Ctrl+F',self.table.search.show)
        self.gui.bind('Return',self.go_keyboard)
        self.gui.bind('Enter',self.go_keyboard)
        self.gui.bind('Ctrl+Return',self.copy_cell)
        self.gui.bind('Ctrl+Enter',self.copy_cell)
        
        self.gui.bind (sh.lg.globs['str']['bind_clear_history']
                      ,self.clear_history
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col1_down']
                      ,lambda:self.table.go_next_section(0)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col2_down']
                      ,lambda:self.table.go_next_section(1)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col3_down']
                      ,lambda:self.table.go_next_section(2)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col4_down']
                      ,lambda:self.table.go_next_section(3)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col1_up']
                      ,lambda:self.table.go_prev_section(0)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col2_up']
                      ,lambda:self.table.go_prev_section(1)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col3_up']
                      ,lambda:self.table.go_prev_section(2)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_col4_up']
                      ,lambda:self.table.go_prev_section(3)
                      )
        self.gui.bind (sh.lg.globs['str']['bind_go_next']
                      ,self.go_next
                      )
        self.gui.bind (sh.lg.globs['str']['bind_go_back']
                      ,self.go_back
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_history']
                      ,self.history.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_history_alt']
                      ,self.history.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_save_article']
                      ,self.save.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_save_article_alt']
                      ,self.save.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_settings']
                      ,self.settings.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_settings_alt']
                      ,self.settings.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_spec_symbol']
                      ,self.symbols.show
                      )
        self.gui.bind (sh.lg.globs['str']['bind_swap_langs']
                      ,self.swap_langs
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_priority']
                      ,self.prior.toggle
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_popup']
                      ,self.table.show_popup
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_alphabet']
                      ,self.toggle_alphabet
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_view']
                      ,self.toggle_view
                      )
        self.gui.bind (sh.lg.globs['str']['bind_toggle_view_alt']
                      ,self.toggle_view
                      )
                      
        #TODO: iterate through all keys
        if sh.lg.globs['str']['bind_spec_symbol'] == 'Ctrl+E':
            self.gui.panel.ent_src.widget.sig_ctrl_e.connect(self.symbols.show)
        else:
            self.gui.panel.ent_src.bind (sh.lg.globs['str']['bind_spec_symbol']
                                        ,self.symbols.show
                                        )
        
        self.table.gui.clicked.connect(self.go_url)
        self.table.gui.sig_mmb.connect(self.minimize)
        ''' Recalculate pages each time the main window is resized. This allows
            to save resources and avoid getting dummy geometry which will be
            returned before the window is shown.
        '''
        self.gui.parent.resizeEvent = self.table.set_coords
        
        self.panel.btn_abt.set_action(self.about.toggle)
        self.panel.btn_alp.set_action(self.toggle_alphabet)
        self.panel.btn_clr.set_action(self.clear_search_field)
        self.panel.btn_hst.set_action(self.history.toggle)
        self.panel.btn_ins.set_action(self.paste)
        self.panel.btn_nxt.set_action(self.go_next)
        self.panel.btn_pri.set_action(self.prior.toggle)
        self.panel.btn_prv.set_action(self.go_back)
        self.panel.btn_qit.set_action(self.close)
        self.panel.btn_rp1.set_action(self.insert_repeat_sign)
        self.panel.btn_rp2.set_action(self.insert_repeat_sign2)
        self.panel.btn_ser.set_action(self.table.search.toggle)
        self.panel.btn_set.set_action(self.settings.toggle)
        self.panel.btn_sym.set_action(self.symbols.show)
        self.panel.btn_swp.set_action(self.swap_langs)
        self.panel.btn_trn.set_action(self.go_keyboard)
        self.panel.btn_viw.set_action(self.toggle_view)
        
        self.panel.ent_src.widget.sig_home.connect(self.table.go_line_start)
        self.panel.ent_src.widget.sig_end.connect(self.table.go_line_end)
        self.panel.ent_src.widget.sig_ctrl_home.connect(self.table.go_start)
        self.panel.ent_src.widget.sig_ctrl_end.connect(self.table.go_end)
        self.panel.ent_src.widget.sig_left_arrow.connect(self.table.go_left)
        self.panel.ent_src.widget.sig_right_arrow.connect(self.table.go_right)
        self.panel.opt_lg1.widget.activated.connect(self.go_search_focus)
        self.panel.opt_lg2.widget.activated.connect(self.go_search_focus)
        self.panel.opt_src.widget.activated.connect(self.set_source)
        
        self.table.gui.sig_rmb.connect(self.copy_cell)
        
        self.symbols.gui.table.clicked.connect(self.paste_symbol)
        self.symbols.gui.table.sig_space.connect(self.paste_symbol)
        self.symbols.gui.sig_return.connect(self.paste_symbol)
        self.symbols.gui.table.sig_rmb.connect(self.copy_symbol)
        self.symbols.gui.sig_ctrl_return.connect(self.copy_symbol)
        
        self.settings.gui.btn_apl.set_action(self.apply_settings)
        self.settings.gui.btn_sug.set_action(self.suggest_col_widths)
        self.settings.gui.sig_close.connect(self.settings.close)
        
        self.history.gui.sig_close.connect(self.history.close)
        self.history.gui.sig_go.connect(self.go_history)
        
        self.prior.gui.sig_close.connect(self.prior.close)
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.panel = gi.Panel()
        self.about = About()
        self.symbols = sm.Symbols()
        self.welcome = Welcome(self.about.get_product())
        self.settings = st.objs.get_settings()
        self.history = hs.History()
        self.save = Save()
        self.prior = pr.Priorities()
        self.gui.set_gui(self.table.gui,self.panel)
        self.set_title()
        self.set_bindings()



class Search:
    
    def __init__(self):
        self.Shown = False
        self.logic = lg.Search()
        self.gui = gi.Search()
        self.set_bindings()
        self.gui.ent_src.focus()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
    
    def clear(self):
        self.gui.clear()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def show(self):
        self.Shown = True
        self.gui.show()
    
    def set_bindings(self):
        self.gui.bind('Esc',self.close)
        self.gui.btn_cls.action = self.close
        self.gui.btn_clr.action = self.clear
        self.gui.btn_cls.set_action()
        self.gui.btn_clr.set_action()
        self.gui.sig_close.connect(self.close)
    
    def reset(self,cells,plain,rowno,colno):
        self.pattern = self.gui.ent_src.get()
        Case = self.gui.cbx_cas.get()
        self.logic.reset(cells,plain,self.pattern,rowno,colno,Case)
    
    def search_next(self):
        f = '[MClientQt] mclient.Search.search_next'
        rowno, colno = self.logic.search_next()
        if rowno < self.logic.rowno:
            mes = _('The end has been reached. Searching from the start.')
            sh.objs.get_mes(f,mes).show_info()
        elif rowno == self.logic.rowno and colno == self.logic.colno:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()
        return(rowno,colno)
    
    def search_prev(self):
        f = '[MClientQt] mclient.Search.search_prev'
        rowno, colno = self.logic.search_prev()
        if rowno > self.logic.rowno:
            mes = _('The start has been reached. Searching from the end.')
            sh.objs.get_mes(f,mes).show_info()
        elif rowno == self.logic.rowno and colno == self.logic.colno:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()
        return(rowno,colno)


com = Commands()


if __name__ == '__main__':
    f = '[MClientQt] mclient.__main__'
    sh.com.start()
    lg.com.start()
    lg.objs.get_plugins(Debug=False,maxrows=1000)
    lg.objs.get_request().search = 'tuple'
    timer = sh.Timer(f + ': Showing GUI')
    timer.start()
    app = App()
    lg.com.get_url()
    app.load_article()
    timer.end()
    app.show()
    sh.com.end()
