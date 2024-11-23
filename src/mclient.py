#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.pretty_html import make_pretty
from skl_shared_qt.text_file import Read, Write
from skl_shared_qt.paths import Path
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.graphics.debug.controller import Debug
from skl_shared_qt.list import List
from skl_shared_qt.logic import OS, Input, Text
from skl_shared_qt.online import Online
from skl_shared_qt.timer import Timer
from skl_shared_qt.articles import ARTICLES

from config import CONFIG, HistorySubjects
import logic as lg
import gui as gi

import format as fm
import cells as cl
import prior_block.controller as pr
import settings.controller as st
import suggest.controller as sg
import about.controller as ab
import third_parties.controller as tp
import symbols.controller as sm
import welcome.controller as wl
import history.controller as hs
import save.controller as sv
import popup.controller as pp
import keylistener.gui as kg
import subjects as sj


DEBUG = False


class Priorities(pr.Panes):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bindings()
        self.reset()
    
    def toggle_use(self):
        objs.get_prior().gui.cbx_pri.toggle()
        self.save()
    
    def save(self):
        CONFIG.new['subjects']['prioritized'] = self.dump1()
        CONFIG.new['PrioritizeSubjects'] = objs.get_prior().gui.cbx_pri.get()
        objs.get_app().load_article()
    
    def add_bindings(self):
        self.gui.btn_res.set_action(self.reset)
        self.gui.btn_apl.set_action(self.apply)
        self.gui.opt_src.set_action(self.reset)
    
    def set_mode(self):
        f = '[MClient] mclient.Priorities.set_mode'
        mode = self.gui.opt_src.get()
        if mode == _('All subjects'):
            self.dic2 = lg.objs.get_plugins().get_subjects()
        elif mode == _('From the article'):
            self.dic2 = com.get_article_subjects()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, '; '.join(self.gui.opt_src.items))
            Message(f, mes, True).show_error()
            return
        mes = _('Mode: "{}"').format(mode)
        Message(f, mes).show_debug()
    
    def reset(self):
        self.dic1 = CONFIG.new['subjects']['prioritized']
        self.set_mode()
        #TODO: Elaborate
        self.fill(self.dic1, self.dic2)
    
    def apply(self):
        self.close()
        self.save()



class Block(pr.Panes):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_titles()
        self.add_bindings()
        self.reset()
    
    def set_titles(self):
        self.gui.set_title(_('Blocking'))
        self.gui.tree1.set_header(_('Blocked subjects'))
    
    def toggle_use(self):
        objs.get_block().gui.cbx_pri.toggle()
        self.save()
    
    def save(self):
        CONFIG.new['subjects']['blocked'] = self.dump1()
        CONFIG.new['BlockSubjects'] = objs.get_block().gui.cbx_pri.get()
        objs.get_app().load_article()
    
    def add_bindings(self):
        self.gui.btn_res.set_action(self.reset)
        self.gui.btn_apl.set_action(self.apply)
        self.gui.opt_src.set_action(self.reset)
    
    def set_mode(self):
        f = '[MClient] mclient.Block.set_mode'
        mode = self.gui.opt_src.get()
        if mode == _('All subjects'):
            self.dic2 = lg.objs.get_plugins().get_subjects()
        elif mode == _('From the article'):
            self.dic2 = com.get_article_subjects()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, '; '.join(self.gui.opt_src.items))
            Message(f, mes, True).show_error()
            return
        mes = _('Mode: "{}"').format(mode)
        Message(f, mes).show_debug()
    
    def reset(self):
        self.dic1 = CONFIG.new['subjects']['blocked']
        self.set_mode()
        #TODO: Elaborate
        self.fill(self.dic1, self.dic2)
    
    def apply(self):
        self.close()
        self.save()



class UpdateUI:
    
    def __init__(self):
        self.Parallel = lg.com.is_parallel()
        self.Separate = lg.com.is_separate()
    
    def _update_alphabet_image(self):
        if CONFIG.new['AlphabetizeTerms'] and not self.Parallel \
        and not self.Separate:
            gi.objs.get_panel().btn_alp.activate()
        else:
            gi.objs.get_panel().btn_alp.inactivate()
    
    def _update_alphabet_hint(self):
        mes = [_('Sort terms by alphabet')]
        if CONFIG.new['AlphabetizeTerms']:
            mes.append(_('Status: ON'))
        else:
            mes.append(_('Status: OFF'))
        if self.Parallel or self.Separate:
            mes.append(_('This page is not supported'))
        gi.objs.get_panel().btn_alp.hint = '\n'.join(mes)
        gi.objs.panel.btn_alp.set_hint()
    
    def update_alphabetization(self):
        self._update_alphabet_image()
        self._update_alphabet_hint()
    
    def update_global_hotkey(self):
        mes = [_('Capture Ctrl-c-c and Ctrl-Ins-Ins')]
        if CONFIG.new['CaptureHotkey']:
            gi.objs.get_panel().btn_cap.activate()
            mes.append(_('Status: ON'))
        else:
            gi.objs.get_panel().btn_cap.inactivate()
            mes.append(_('Status: OFF'))
        gi.objs.panel.btn_cap.hint = '\n'.join(mes)
        gi.objs.panel.btn_cap.set_hint()
    
    def update_prioritization(self):
        mes = [_('Subject prioritization')]
        prioritized = ARTICLES.get_prioritized()
        if CONFIG.new['PrioritizeSubjects'] and prioritized \
        and not self.Parallel:
            gi.objs.get_panel().btn_pri.activate()
        else:
            gi.objs.get_panel().btn_pri.inactivate()
        if CONFIG.new['PrioritizeSubjects']:
            mes.append(_('Status: ON'))
            objs.get_prior().gui.cbx_pri.enable()
        else:
            mes.append(_('Status: OFF'))
            objs.get_prior().gui.cbx_pri.disable()
        if prioritized:
            sub = _('{} subjects were prioritized')
            sub = sub.format(len(prioritized))
        else:
            sub = _('Nothing to prioritize')
        mes.append(sub)
        gi.objs.panel.btn_pri.hint = '\n'.join(mes)
        gi.objs.panel.btn_pri.set_hint()
    
    def update_block(self):
        f = '[MClient] mclient.UpdateUI.update_block'
        ''' #NOTE: We cannot use 'ARTICLES.get_cells()' since
            it does not have blocked items.
        '''
        blocked_subj = ARTICLES.get_blocked()
        blocked_cells = ARTICLES.get_blocked_cells()
        if blocked_subj:
            blocked_subj = len(blocked_subj)
        else:
            blocked_subj = 0
        if blocked_cells:
            blocked_cells = len(blocked_cells)
        else:
            blocked_cells = 0
        mes = [_('Subject blocking')]
        if CONFIG.new['BlockSubjects'] and blocked_subj:
            gi.objs.get_panel().btn_blk.activate()
        else:
            gi.objs.get_panel().btn_blk.inactivate()
        if CONFIG.new['BlockSubjects'] and blocked_cells:
            mes.append(_('Status: ON'))
            sub = _('Blocked {} subjects ({} cells)')
            sub = sub.format(blocked_subj, blocked_cells)
        else:
            mes.append(_('Status: OFF'))
            sub = _('Nothing was blocked')
        mes.append(sub)
        gi.objs.panel.btn_blk.hint = '\n'.join(mes)
        gi.objs.panel.btn_blk.set_hint()
        if CONFIG.new['BlockSubjects']:
            objs.get_block().gui.cbx_pri.enable()
        else:
            objs.get_block().gui.cbx_pri.disable()
    
    def update_go_next(self):
        if ARTICLES.is_last():
            gi.objs.get_panel().btn_nxt.inactivate()
        else:
            gi.objs.get_panel().btn_nxt.activate()
    
    def update_go_prev(self):
        # Update the button to move to the previous article
        if ARTICLES.get_len():
            gi.objs.get_panel().btn_prv.activate()
        else:
            gi.objs.get_panel().btn_prv.inactivate()
    
    def update_last_search(self):
        # Update the button to insert a current search string
        if ARTICLES.get_len():
            gi.objs.get_panel().btn_rp1.activate()
        else:
            gi.objs.get_panel().btn_rp1.inactivate()
    
    def update_prev_search(self):
        # Update the button to insert a previous search string
        if ARTICLES.get_len() > 1:
            gi.objs.get_panel().btn_rp2.activate()
        else:
            gi.objs.get_panel().btn_rp2.inactivate()
    
    def update_buttons(self):
        f = '[MClient] mclient.UpdateUI.update_buttons'
        self.update_last_search()
        self.update_prev_search()
        # Suppress useless error output
        if lg.objs.get_request().search:
            self.update_go_prev()
            self.update_go_next()
            self.update_block()
            self.update_prioritization()
        else:
            rep.lazy(f)
        self.update_global_hotkey()
        self.update_alphabetization()
    
    def run(self):
        self.update_buttons()



class FontLimits:
    
    def __init__(self, family, size, Bold=False, Italic=False):
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
    
    def set_text(self, text):
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
        space = self.gui.get_space(self.text, self.font)
        #mes = _('Space: {}').format(space)
        #Message(f, mes).show_debug()
        return space



class Save(sv.Save):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bindings()
    
    def _get_text(self):
        f = '[MClient] mclient.Save._get_text'
        text = []
        text_row = []
        cells = ARTICLES.get_table()
        if not cells:
            rep.empty(f)
            return ''
        for row in cells:
            for cell in row:
                if not cell.text.strip():
                    continue
                if cell.colno == 0 and cell.fixed_block:
                    if text_row:
                        text_row = ''.join(text_row)
                        # Removing '; ' before subject-related cells
                        text.append(text_row[:-2])
                        text_row = []
                text_row.append(cell.text)
                if cell.colno == 0 and cell.fixed_block:
                    text_row.append(': ')
                else:
                    text_row.append('; ')
        if text_row:
            # Removing '; ' before subject-related cells
            text_row = ''.join(text_row)
            text.append(text_row[:-2])
        return '\n\n'.join(text)
    
    def add_bindings(self):
        self.gui.save.clicked.connect(self.select)
        self.gui.bind(('Return',), self.select)
        self.gui.bind(('Enter',), self.select)
    
    def select(self):
        f = '[MClient] mclient.Save.select'
        opt = self.get()
        if not opt:
            rep.empty(f)
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
            mes = mes.format(opt, '; '.join(self.model.items))
            Message(f, mes, True).show_error()

    def _add_web_ext(self):
        if not Path(self.file).get_ext_low() in ('.htm', '.html'):
            self.file += '.htm'
    
    def save_view_as_htm(self):
        f = '[MClient] mclient.Save.save_view_as_htm'
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        if not self.file:
            rep.empty(f)
            return
        # Can be an empty list
        cells = ARTICLES.get_table()
        #TODO: elaborate
        skipped = []
        #skipped = com.get_skipped_terms()
        code = lg.HTM(cells, skipped).run()
        if not code:
            rep.empty(f)
            return
        self._add_web_ext()
        # Takes ~0.47s for 'set' on Intel Atom, do not call in 'load_article'
        code = make_pretty(code)
        Write(self.file).write(code)

    def save_raw_as_htm(self):
        f = '[MClient] mclient.Save.save_raw_as_htm'
        ''' Key 'html' may be needed to write a file in the UTF-8 encoding,
            therefore, in order to ensure that the web-page is read correctly,
            we change the encoding manually. We also replace abbreviated
            hyperlinks with full ones in order to ensure that they are also
            valid in the local file.
        '''
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        code = ARTICLES.get_raw_code()
        if not self.file or not code:
            rep.empty(f)
            return
        self._add_web_ext()
        code = lg.objs.get_plugins().fix_raw_htm(code)
        Write(self.file).write(code)

    def save_view_as_txt(self):
        f = '[MClient] mclient.Save.save_view_as_txt'
        self.gui.ask.filter = _('Plain text (*.txt)')
        self.file = self.gui.ask.save()
        text = self._get_text()
        if not self.file or not text:
            rep.empty(f)
            return
        if not Path(self.file).get_ext_low() == '.txt':
            self.file += '.txt'
        Write(self.file).write(text)

    def copy_raw(self):
        CLIPBOARD.copy(ARTICLES.get_raw_code())

    def copy_view(self):
        CLIPBOARD.copy(self._get_text())



class Commands:
    
    def get_article_subjects(self):
        f = '[MClient] mclient.Commands.get_article_subjects'
        subjfs = ARTICLES.get_subjf()
        if not subjfs:
            rep.empty(f)
            return {}
        subjfs = sorted(set(subjfs), key=lambda s: s.casefold())
        dic = {}
        for subjf in subjfs:
            dic[subjf] = {}
        return dic



class Welcome(wl.Welcome):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
    
    def gen_online_source(self, title, status, color):
        return f'<b>{title} <font color="{color}">{status}</font></b>'
    
    def gen_offline_source(self, title, status, color):
        return f'{title}: <font color="{color}">{status}</font>'
    
    def fill(self):
        model = wl.TableModel(self.run())
        self.set_model(model)
    
    def set_online_sources(self):
        f = '[MClient] mclient.Welcome.set_online_sources'
        if not CONFIG.new['Ping']:
            rep.lazy(f)
            return
        old = lg.objs.get_plugins().source
        dics = lg.objs.plugins.get_online_sources()
        if not dics:
            rep.empty(f)
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
        f = '[MClient] mclient.Welcome.set_offline_sources'
        dics = lg.objs.plugins.get_offline_sources()
        if not dics:
            rep.empty(f)
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parties = tp.ThirdParties()
        self.add_bindings()

    def add_bindings(self):
        self.gui.btn_thd.set_action(self.parties.show)
        self.gui.btn_lic.set_action(self.parties.open_license_url)
        self.gui.btn_eml.set_action(self.parties.send_feedback)



class BlockMode:
    
    def __init__(self):
        self.cell = None
        self.blockno = -1
    
    def copy_block(self):
        f = '[MClient] mclient.BlockMode.copy_block'
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        try:
            CLIPBOARD.copy(self.cell.blocks[self.blockno].text.strip())
            return True
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(self.blockno)
            Message(f, mes, True).show_warning()
    
    def select_next(self):
        f = '[MClient] mclient.BlockMode.select_next'
        self.enable()
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        self.blockno += 1
        if self.blockno == len(self.cell.blocks):
            self.blockno = 0
        self.set_cell()
        self.select()
    
    def select_prev(self):
        f = '[MClient] mclient.BlockMode.select_prev'
        self.enable()
        if not self.cell or not self.cell.blocks:
            rep.empty(f)
            return
        self.blockno -= 1
        if self.blockno < 0:
            self.blockno = len(self.cell.blocks) - 1
        self.set_cell()
        self.select()
    
    def toggle(self):
        if self.blockno == -1:
            self.enable()
        else:
            self.disable()
    
    def disable(self):
        f = '[MClient] mclient.BlockMode.disable'
        self.blockno = -1
        mes = _('Disable block mode')
        Message(f, mes).show_info()
        self.set_cell()
        self.select()
    
    def enable(self):
        f = '[MClient] mclient.BlockMode.enable'
        if self.blockno > -1:
            rep.lazy(f)
            return
        self.blockno = 0
        mes = _('Enable block mode')
        Message(f, mes).show_info()
        self.set_cell()
        self.select()
    
    def set_cell(self):
        f = '[MClient] mclient.BlockMode.set_cell'
        tuple_ = objs.get_app().table.get_cell()
        if not tuple_:
            rep.empty(f)
            return
        rowno, colno = tuple_[0], tuple_[1]
        mes = _('Row #{}. Column #{}').format(rowno, colno)
        Message(f, mes).show_debug()
        cells = ARTICLES.get_table()
        if not cells:
            rep.empty(f)
            return
        try:
            self.cell = cells[rowno][colno]
        except (KeyError, IndexError):
            mes = _('Wrong input data!')
            Message(f, mes, True).show_warning()
            return
    
    def select(self):
        f = '[MClient] mclient.BlockMode.select'
        if not self.cell:
            rep.empty(f)
            return
        try:
            block = self.cell.blocks[self.blockno]
        except IndexError:
            mes = _('Wrong input data: "{}"!').format(self.blockno)
            Message(f, mes).show_warning()
            return
        code = []
        for i in range(len(self.cell.blocks)):
            code.append(fm.Block(self.cell.blocks[i], self.cell.colno, i==self.blockno).run())
        self.cell.code = List(code).space_items()
        objs.get_app().table.logic.code[self.cell.rowno][self.cell.colno] = self.cell.code
        objs.app.table.reset(objs.app.table.logic.plain, objs.app.table.logic.code)
        objs.app.table.select(self.cell.rowno, self.cell.colno)



class App:
    
    def __init__(self):
        # 'thread' name is OK here, but will override a built-in method in GUI
        self.thread = kg.Thread()
        self.logic = lg.App()
        self.gui = gi.App()
        self.gui.WIDE_ROW_COLOR = CONFIG.new["rows"]["border"]["color"]
        self.gui.WIDE_ROW_LEN = CONFIG.new["rows"]["border"]["length"]
        self.set_gui()
        self.set_hints()
        self.update_ui()
    
    def copy_block(self):
        if self.block_mode.copy_block():
            if CONFIG.new['Iconify']:
                self.minimize()
    
    def solve_copy(self):
        if self.block_mode.blockno > -1:
            self.copy_block()
        else:
            self.copy_cell()
    
    def solve_go_left(self):
        if self.block_mode.blockno > -1:
            self.block_mode.select_prev()
        else:
            self.table.go_left()
    
    def solve_go_right(self):
        if self.block_mode.blockno > -1:
            self.block_mode.select_next()
        else:
            self.table.go_right()
    
    def solve_go_down(self):
        if self.block_mode.blockno > -1:
            self.block_mode.select_next()
        else:
            self.table.go_down()
    
    def solve_go_up(self):
        if self.block_mode.blockno > -1:
            self.block_mode.select_prev()
        else:
            self.table.go_up()
    
    def _set_hint(self, widget, action):
        section = CONFIG.new['actions'][action]
        hotkeys = ', '.join(section['hotkeys'])
        widget.hint = f"{section['hint']}<i><center>{hotkeys}</center></i>"
        widget.set_hint()
    
    def set_hints(self):
        pairs = ((gi.objs.get_panel().btn_sym, 'toggle_spec_symbols')
                ,(gi.objs.panel.btn_swp, 'swap_langs')
                ,(gi.objs.panel.btn_set, 'toggle_settings')
                ,(gi.objs.panel.btn_blk, 'toggle_block')
                ,(gi.objs.panel.btn_pri, 'toggle_priority')
                ,(gi.objs.panel.btn_alp, 'toggle_alphabet')
                ,(gi.objs.panel.btn_prv, 'go_back')
                ,(gi.objs.panel.btn_nxt, 'go_next')
                ,(gi.objs.panel.btn_hst, 'toggle_history')
                ,(gi.objs.panel.btn_rld, 'reload_article')
                ,(gi.objs.panel.btn_ser, 're_search_article')
                ,(gi.objs.panel.btn_sav, 'save_article')
                ,(gi.objs.panel.btn_brw, 'open_in_browser')
                ,(gi.objs.panel.btn_prn, 'print')
                ,(gi.objs.panel.btn_def, 'define')
                ,(gi.objs.panel.btn_abt, 'toggle_about')
                ,(gi.objs.panel.btn_qit, 'quit')
                )
        for pair in pairs:
            self._set_hint(pair[0], pair[1])
    
    def get_x(self):
        return self.gui.get_x()
    
    def get_y(self):
        return self.gui.get_y()
    
    def get_height(self):
        return self.gui.get_height()
    
    def show_suggestions(self):
        ''' Retrieving suggestions online is very slow, so this should be
            implemented with a hotkey rather than as we type.
        '''
        f = '[MClient] mclient.App.show_suggestions'
        fragment = gi.objs.get_panel().ent_src.get().strip()
        if not fragment:
            rep.empty(f)
            return
        items = lg.com.suggest (search = fragment
                               ,limit = 35
                               )
        if not items:
            mes = _('No suggestions are available!')
            Message(f, mes).show_info()
            return
        self.suggest.fill(items)
        self.suggest.show()
        x = self.get_x() + gi.objs.panel.ent_src.get_x()
        y = self.get_height() + self.get_y() - self.suggest.get_height() \
                              - gi.objs.panel.ent_src.get_root_y()
        self.suggest.set_geometry(x, y, 170, self.suggest.get_height())
    
    def get_cell(self):
        f = '[MClient] mclient.App.get_cell'
        table = ARTICLES.get_table()
        if not table:
            rep.empty(f)
            return
        rowno, colno = self.table.get_cell()
        try:
            return table[rowno][colno]
        except IndexError:
            mes = _('Wrong input data: "{}"!').format((rowno, colno))
            Message(f, mes, True).show_warning()
        return
    
    def get_wform(self):
        f = '[MClient] mclient.App.get_wform'
        table = ARTICLES.get_table()
        if not table:
            rep.empty(f)
            return
        cell = self.get_cell()
        if not cell:
            rep.empty(f)
            return
        return cell.wform
    
    def copy_wform(self):
        f = '[MClient] mclient.App.copy_wform'
        if not ARTICLES.get_len():
            # Do not warn when there are no articles yet
            rep.lazy(f)
            return
        wform = self.get_wform()
        if not wform:
            rep.empty(f)
            return
        CLIPBOARD.copy(wform)
        if CONFIG.new['Iconify']:
            self.minimize()
    
    def copy_article_url(self):
        f = '[MClient] mclient.App.copy_article_url'
        if not ARTICLES.get_len():
            # Do not warn when there are no articles yet
            rep.lazy(f)
            return
        url = ARTICLES.get_url()
        if not url:
            rep.empty(f)
            return
        url = lg.objs.get_plugins().fix_url(url)
        CLIPBOARD.copy(url)
        if CONFIG.new['Iconify']:
            self.minimize()
    
    def get_cell_url(self):
        f = '[MClient] mclient.App.get_cell_url'
        cell = self.get_cell()
        if not cell:
            rep.empty(f)
            return
        return cell.url
    
    def copy_cell_url(self):
        f = '[MClient] mclient.App.copy_cell_url'
        if not ARTICLES.get_len():
            # Do not warn when there are no articles yet
            rep.lazy(f)
            return
        url = self.get_cell_url()
        if not url:
            rep.empty(f)
            return
        url = lg.objs.get_plugins().fix_url(url)
        CLIPBOARD.copy(url)
        if CONFIG.new['Iconify']:
            self.minimize()
    
    def go_phrases(self):
        f = '[MClient] mclient.App.go_phrases'
        tuple_ = self.table.logic.get_phsubj()
        if not tuple_:
            rep.empty(f)
            return
        text, url = tuple_[0], tuple_[1]
        if not url:
            rep.empty(f)
            return
        lg.objs.get_request().search = text
        lg.objs.request.url = url
        mes = _('Open link: {}').format(lg.objs.request.url)
        Message(f, mes).show_info()
        self.load_article(lg.objs.request.search, lg.objs.request.url)
    
    def activate(self):
        if OS.is_win():
            objs.get_geometry().keyword = self.about.logic.product
            objs.geometry.activate()
        else:
            self.gui.activate()
    
    def catch(self, status=0):
        f = '[MClient] mclient.App.catch'
        mes = _('Status: {}').format(status)
        Message(f, mes).show_debug()
        if not CONFIG.new['CaptureHotkey'] or not status:
            rep.lazy(f)
            return
        self.activate()
        if status != 1:
            return
        new_clipboard = CLIPBOARD.paste()
        new_clipboard = new_clipboard.strip()
        if not new_clipboard:
            rep.empty(f)
            return
        lg.objs.get_request().search = new_clipboard
        self.go_search()
    
    def run_thread(self):
        self.thread.run_thread()
    
    def edit_blacklist(self):
        f = '[MClient] mclient.App.edit_blacklist'
        old_list = CONFIG.new['subjects']['blocked']
        old_key = CONFIG.new['BlockSubjects']
        objs.get_block().reset (lst1 = old_list
                               ,lst2 = lg.objs.get_plugins().get_subjects()
                               ,art_subjects = com.get_article_subjects()
                               ,majors = lg.objs.plugins.get_majors()
                               )
        objs.block.set_checkbox(CONFIG.new['BlockSubjects'])
        objs.block.show()
        CONFIG.new['BlockSubjects'] = self.block.get_checkbox()
        new_list = objs.block.get1()
        if (old_list == new_list) \
        and (old_key == CONFIG.new['BlockSubjects']):
            rep.lazy(f)
            return
        lg.objs.default.block = new_list
        ARTICLES.delete_bookmarks()
        self.load_article()
    
    def watch_clipboard(self):
        # Watch clipboard
        if CONFIG.new['CaptureHotkey']:
            CONFIG.new['CaptureHotkey'] = False
        else:
            CONFIG.new['CaptureHotkey'] = True
        UpdateUI().update_global_hotkey()
    
    def define(self, Selected=True):
        # Open a web-page with a definition of the current term
        # Selected: True: Selected term; False: Article title
        f = '[MClient] mclient.App.define'
        if Selected:
            pattern = self.table.get_cell_text()
        else:
            pattern = lg.objs.get_request().search
        if not pattern:
            rep.empty(f)
            return
        pattern = _('what is "{}"?').format(pattern)
        Online(base = CONFIG.new['web_search_url']
              ,pattern = pattern).browse()
    
    def reload(self):
        search = ARTICLES.get_search()
        url = lg.objs.articles.get_url()
        lg.objs.articles.clear_article()
        self.load_article(search, url)
    
    def toggle_alphabet(self):
        if CONFIG.new['AlphabetizeTerms']:
            CONFIG.new['AlphabetizeTerms'] = False
        else:
            CONFIG.new['AlphabetizeTerms'] = True
        ARTICLES.delete_bookmarks()
        self.load_article()
    
    def add_history(self):
        # Call this only after assigning an article ID for a new article
        f = '[MClient] mclient.App.add_history'
        if not lg.objs.get_request().search:
            rep.lazy(f)
            return
        self.history.add_row (id_ = ARTICLES.id
                             ,source = lg.objs.get_plugins().source
                             ,lang1 = lg.objs.plugins.get_lang1()
                             ,lang2 = lg.objs.plugins.get_lang2()
                             ,search = lg.objs.articles.get_search()
                             )
        # Setting column width works only after updating the model, see https://stackoverflow.com/questions/8364061/how-do-you-set-the-column-width-on-a-qtreeview
        self.history.gui.set_col_width()
    
    def go_history(self, id_):
        f = '[MClient] mclient.App.go_history'
        if id_ is None:
            rep.empty(f)
            return
        ARTICLES.set_id(id_)
        source = lg.objs.articles.get_source()
        lang1 = lg.objs.articles.get_lang1()
        lang2 = lg.objs.articles.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        mes = _('Set source to "{}"')
        mes = mes.format(CONFIG.new['source'])
        Message(f, mes).show_info()
        lg.objs.get_plugins().set(CONFIG.new['source'])
        lg.objs.plugins.set_lang1(lang1)
        lg.objs.plugins.set_lang2(lang2)
        self.reset_opt(CONFIG.new['source'])
        self.load_article()
    
    def clear_history(self):
        ARTICLES.reset()
        lg.objs.get_request().reset()
        self.solve_screen()
    
    def go_back(self):
        f = '[MClient] mclient.App.go_back'
        if ARTICLES.get_len() in (0, 1):
            rep.lazy(f)
            return
        if lg.objs.articles.id == 0:
            lg.objs.articles.set_id(lg.objs.articles.get_max_id())
        else:
            lg.objs.articles.set_id(lg.objs.articles.id - 1)
        source = lg.objs.articles.get_source()
        lang1 = lg.objs.articles.get_lang1()
        lang2 = lg.objs.articles.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        lg.objs.get_plugins().set(CONFIG.new['source'])
        lg.objs.plugins.set_lang1(lang1)
        lg.objs.plugins.set_lang2(lang2)
        self.reset_opt(CONFIG.new['source'])
        self.load_article()
        self.history.go_up()
    
    def go_next(self):
        f = '[MClient] mclient.App.go_next'
        if ARTICLES.get_len() in (0, 1):
            rep.lazy(f)
            return
        if lg.objs.articles.is_last():
            lg.objs.articles.set_id(0)
        else:
            lg.objs.articles.set_id(lg.objs.articles.id + 1)
        source = lg.objs.articles.get_source()
        lang1 = lg.objs.articles.get_lang1()
        lang2 = lg.objs.articles.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        lg.objs.get_plugins().set(CONFIG.new['source'])
        lg.objs.plugins.set_lang1(lang1)
        lg.objs.plugins.set_lang2(lang2)
        self.reset_opt(CONFIG.new['source'])
        self.load_article()
        self.history.go_down()
    
    def get_width(self):
        return self.gui.get_width()
    
    def _set_col_num(self, window_width):
        if window_width <= 1024:
            return 3
        else:
            return 5
    
    def suggest_col_widths(self):
        f = '[MClient] mclient.App.suggest_col_widths'
        table_width = self.get_width()
        if not table_width:
            rep.empty(f)
            return
        col_num = self.settings.gui.ent_num.get()
        if not col_num:
            col_num = self._set_col_num(table_width)
        col_num = Input(f, col_num).get_integer()
        if not 0 < col_num <= 10:
            mes = _('A value of this field should be within the range of {}-{}!')
            mes = mes.format(1, 10)
            Message(f, mes, True).show_warning()
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
        Message(f, mes).show_debug()
        mes = _('Term column width: {}').format(term_width)
        Message(f, mes).show_debug()
        
        self.settings.gui.ent_num.set_text(col_num)
        self.settings.gui.ent_fix.set_text(63)
        self.settings.gui.ent_trm.set_text(term_width)
    
    def set_col_num(self):
        gi.objs.get_panel().opt_col.set(lg.objs.get_column_width().term_num)
    
    def apply_settings(self):
        self.settings.close()
        st.Save().run()
        lg.com.export_style()
        lg.objs.get_column_width().reset()
        lg.objs.column_width.run()
        self.set_col_num()
        # This loads the article and must come the last
        self.set_columns()
    
    def change_col_no(self, no):
        gi.objs.get_panel().opt_col.set(no)
        self.set_columns()

    def set_columns(self):
        self.reset_columns()
        if not gi.objs.get_article_proxy().is_welcome():
            ARTICLES.delete_bookmarks()
            self.load_article()
        gi.objs.get_panel().ent_src.focus()

    def reset_columns(self):
        ''' Count only term columns since fixed columns can now have zero width
            (they are not visible to the user and are not considered by them).
        '''
        f = '[MClient] mclient.App.reset_columns'
        if not lg.com.is_parallel():
            CONFIG.new['columns']['num'] = Input(title = f
                                                        ,value = gi.objs.get_panel().opt_col.get()).get_integer()
        collimit = lg.objs.get_column_width().fixed_num + lg.objs.column_width.term_num
        mes = _('Set the number of columns to {} ({} in total)')
        mes = mes.format(lg.objs.column_width.term_num, collimit)
        Message(f, mes).show_info()
    
    def update_columns(self):
        ''' Update a column number in GUI; adjust the column number (both logic
            and GUI) in special cases.
        '''
        f = '[MClient] mclient.App.update_columns'
        if not lg.com.is_parallel():
            CONFIG.new['columns']['num'] = lg.objs.get_column_width().term_num
        gi.objs.get_panel().opt_col.set(lg.objs.get_column_width().term_num)
        collimit = lg.objs.get_column_width().fixed_num + lg.objs.column_width.term_num
        mes = _('Set the number of columns to {} ({} in total)')
        mes = mes.format(lg.objs.column_width.term_num, collimit)
        Message(f, mes).show_info()
    
    def set_source(self):
        f = '[MClient] mclient.App.set_source'
        CONFIG.new['source'] = gi.objs.get_panel().opt_src.get()
        mes = _('Set source to "{}"').format(CONFIG.new['source'])
        Message(f, mes).show_info()
        lg.objs.get_plugins().set(CONFIG.new['source'])
        self.reset_opt(CONFIG.new['source'])
        self.go_search()
    
    def auto_swap(self):
        f = '[MClient] mclient.App.auto_swap'
        lang1 = gi.objs.get_panel().opt_lg1.get()
        lang2 = gi.objs.panel.opt_lg2.get()
        if lg.objs.get_plugins().is_oneway() \
        or not CONFIG.new['Autoswap'] \
        or not lg.objs.get_request().search:
            rep.lazy(f)
            return
        if Text(lg.objs.request.search).has_cyrillic():
            if lang2 in (_('Russian'), 'Russian'):
                mes = f'{lang1}-{lang2} -> {lang2}-{lang1}'
                Message(f, mes).show_info()
                self.swap_langs()
        elif lang1 in (_('Russian'), 'Russian'):
            mes = f'{lang1}-{lang2} -> {lang2}-{lang1}'
            Message(f, mes).show_info()
            self.swap_langs()
    
    def reset_opt(self, default=_('Multitran')):
        f = '[MClient] mclient.App.reset_opt'
        # Reset OptionMenus
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs1 = lg.objs.plugins.get_langs1()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        sources = lg.objs.plugins.get_sources()
        if not (langs1 and langs2 and lang1 and lang2 and sources):
            rep.empty(f)
            return
        gi.objs.get_panel().opt_lg1.reset(items = langs1
                                         ,default = lang1)
        gi.objs.panel.opt_lg2.reset(items = langs2
                                   ,default = lang2)
        #NOTE: change this upon the change of the default source
        gi.objs.panel.opt_src.reset(items = sources
                                   ,default = default)
    
    def set_next_lang1(self):
        ''' We want to navigate through the full list of supported languages
            rather than through the list of 'lang2' pairs so we reset the
            widget first.
        '''
        old = gi.objs.get_panel().opt_lg1.get()
        gi.objs.panel.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                                    ,default = old
                                    )
        gi.objs.panel.opt_lg1.set_next()
        self.update_lang1()
        self.update_lang2()
    
    def set_next_lang2(self):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        gi.objs.get_panel().opt_lg2.set_next()
        self.update_lang2()
    
    def set_prev_lang1(self):
        ''' We want to navigate through the full list of supported languages
            rather than through the list of 'lang2' pairs so we reset the
            widget first.
        '''
        old = gi.objs.get_panel().opt_lg1.get()
        gi.objs.panel.opt_lg1.reset (items = lg.objs.get_plugins().get_langs1()
                                    ,default = old
                                    )
        gi.objs.panel.opt_lg1.set_prev()
        self.update_lang1()
        self.update_lang2()
    
    def set_prev_lang2(self):
        # We want to navigate through the limited list here
        self.update_lang1()
        self.update_lang2()
        gi.objs.get_panel().opt_lg2.set_prev()
        self.update_lang2()
    
    def set_lang1(self):
        f = '[MClient] mclient.App.set_lang1'
        lang = gi.objs.get_panel().opt_lg1.get()
        if lg.objs.get_plugins().get_lang1() != lang:
            mes = _('Set language: {}').format(lang)
            Message(f, mes).show_info()
            CONFIG.new['lang1'] = lang
            lg.objs.get_plugins().set_lang1(lang)
    
    def set_lang2(self):
        f = '[MClient] mclient.App.set_lang2'
        lang = gi.objs.get_panel().opt_lg2.get()
        if lg.objs.get_plugins().get_lang2() != lang:
            mes = _('Set language: {}').format(lang)
            Message(f, mes).show_info()
            CONFIG.new['lang2'] = lang
            lg.objs.get_plugins().set_lang2(lang)
    
    def update_lang1(self):
        f = '[MClient] mclient.App.update_lang1'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        langs1 = lg.objs.plugins.get_langs1()
        if not langs1:
            rep.empty(f)
            return
        gi.objs.get_panel().opt_lg1.set(lang1)
        self.set_lang1()
    
    def update_lang2(self):
        f = '[MClient] mclient.App.update_lang2'
        self.set_lang1()
        self.set_lang2()
        lang1 = lg.objs.get_plugins().get_lang1()
        lang2 = lg.objs.plugins.get_lang2()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        if not langs2:
            rep.empty(f)
            return
        if not lang2 in langs2:
            lang2 = langs2[0]
        gi.objs.get_panel().opt_lg2.reset (items = langs2
                                          ,default = lang2
                                          )
        self.set_lang2()
    
    def swap_langs(self):
        f = '[MClient] mclient.App.swap_langs'
        if lg.objs.get_plugins().is_oneway():
            mes = _('Cannot swap languages, this is a one-way dictionary!')
            Message(f, mes, True).show_info()
            return
        self.update_lang1()
        self.update_lang2()
        lang1 = gi.objs.get_panel().opt_lg1.get()
        lang2 = gi.objs.panel.opt_lg2.get()
        lang1, lang2 = lang2, lang1
        langs1 = lg.objs.get_plugins().get_langs1()
        langs2 = lg.objs.plugins.get_langs2(lang1)
        if not langs1:
            rep.empty(f)
            return
        if not (langs2 and lang1 in langs1 and lang2 in langs2):
            mes = _('Pair {}-{} is not supported!').format(lang1, lang2)
            Message(f, mes, True).show_warning()
            return
        gi.objs.panel.opt_lg1.reset (items = langs1
                                    ,default = lang1
                                    )
        gi.objs.panel.opt_lg2.reset (items = langs2
                                    ,default = lang2
                                    )
        self.update_lang1()
        self.update_lang2()
    
    def insert_repeat_sign2(self):
        # Insert the previous search string
        f = '[MClient] mclient.App.insert_repeat_sign2'
        if ARTICLES.get_len() < 2:
            rep.empty(f)
            return
        lg.objs.articles.set_id(lg.objs.articles.id-1)
        CLIPBOARD.copy(lg.objs.articles.get_search())
        self.paste()
        lg.objs.articles.set_id(lg.objs.articles.id+1)
    
    def insert_repeat_sign(self):
        # Insert the current search string
        CLIPBOARD.copy(ARTICLES.get_search())
        self.paste()
    
    def go_url(self):
        f = '[MClient] mclient.App.go_url'
        if ARTICLES.get_len() == 0:
            # Do not warn when there are no articles yet
            rep.lazy(f)
            return
        cell = self.table.get_cell()
        if not cell:
            rep.empty(f)
            return
        rowno, colno = cell[0], cell[1]
        cell = lg.objs.articles.get_cell(rowno, colno)
        if not cell:
            rep.empty(f)
            return
        lg.objs.get_request().search = cell.text
        if cell.url:
            lg.objs.request.url = cell.url
            mes = _('Open link: {}').format(lg.objs.request.url)
            Message(f, mes).show_info()
            self.load_article (search = lg.objs.request.search
                              ,url = lg.objs.request.url
                              )
        else:
            self.go_search()
    
    def copy_cell(self):
        ''' Do not combine these conditions with 'and' since the interpreter
            may decide to check the lighter condition first.
        '''
        if self.table.copy_cell():
            if CONFIG.new['Iconify']:
                self.minimize()
    
    def copy_symbol(self):
        symbol = self.symbols.get()
        CLIPBOARD.copy(symbol)
    
    def paste_symbol(self):
        symbol = self.symbols.get()
        gi.objs.get_panel().ent_src.insert(symbol)
    
    def solve_screen(self):
        if ARTICLES.get_len():
            gi.objs.get_article_proxy().go_article()
        else:
            gi.objs.get_article_proxy().go_welcome()
    
    def load_article(self, search='', url=''):
        f = '[MClient] mclient.App.load_article'
        ''' #NOTE: each time the contents of the current page is changed
            (e.g., due to prioritizing), bookmarks must be deleted.
        '''
        self.suggest.close()
        timer = Timer(f)
        timer.start()

        if search or url:
            artid = ARTICLES.find(source = CONFIG.new['source']
                                 ,search = search
                                 ,url = url)
        else:
            # Just reload the article if no parameters are provided
            artid = ARTICLES.id
            
        if artid == -1:
            cells = lg.objs.get_plugins().request(search = search
                                                 ,url = url)
            sj.objs.get_subjects().reset(lg.objs.plugins.get_article_subjects())
            lg.objs.articles.add(search = search
                                ,url = url
                                ,cells = cells
                                ,fixed_urls = lg.objs.plugins.get_fixed_urls()
                                ,raw_code = lg.objs.plugins.get_htm()
                                ,subjf = sj.objs.subjects.article
                                ,blocked = sj.objs.subjects.block
                                ,prioritized = sj.objs.subjects.prior)
            HistorySubjects().add(lg.objs.plugins.get_article_subjects())
            self.add_history()
        else:
            mes = _('Load article No. {} from memory').format(artid)
            Message(f, mes).show_info()
            lg.objs.articles.set_id(artid)
            sj.objs.get_subjects().reset(lg.objs.get_plugins().get_article_subjects())
            cells = lg.objs.articles.get_cells()
            
        self.solve_screen()
        
        cells = cl.Expand(cells).run()
        iomit = cl.Omit(cells)
        cells = iomit.run()
        cells = cl.Prioritize(cells).run()
        
        lg.objs.get_column_width().reset()
        lg.objs.column_width.run()
        
        self.update_columns()
        
        cells = cl.View(cells).run()
        iwrap = cl.Wrap(cells)
        iwrap.run()
        
        self.table.reset(iwrap.plain, iwrap.code)
        
        lg.objs.articles.set_blocked_cells(iomit.omit_cells)
        lg.objs.articles.set_table(iwrap.cells)
        
        #lg.objs.request.text = lg.com.get_text(cells)
        #colors = lg.com.get_colors(blocks)
        #lg.com.fix_colors(colors)
        
        #TODO: elaborate
        skipped = []
        ''' Empty article is not added either to memory or history, so we just
            do not clear the search field to be able to correct the typo.
        '''
        if iwrap.plain or skipped:
            gi.objs.get_panel().ent_src.reset()
        elif skipped:
            mes = _('Nothing has been found (skipped subjects: {}).')
            mes = mes.format(skipped)
            Message(f, mes, True).show_info()
        else:
            mes = _('Nothing has been found.')
            Message(f, mes, True).show_info()
        
        #objs.get_suggest().close()
        UpdateUI().run()
        timer.end()
        gi.objs.get_panel().ent_src.focus()
        #self.run_final_debug()
        #self.debug_settings()
        ''' Do not put this in 'Table.reset' - that is too early, the article
            dictionary is not filled yet!
        '''
        self.table.go_bookmark()
    
    def go_keyboard(self):
        search = gi.objs.get_panel().ent_src.get().strip()
        if search == '':
            self.go_url()
        elif search == CONFIG.new['repeat_sign']:
            self.insert_repeat_sign()
        elif search == CONFIG.new['repeat_sign2']:
            self.insert_repeat_sign2()
        else:
            lg.objs.get_request().search = search
            self.go_search()
    
    def go_search(self):
        f = '[MClient] mclient.App.go_search'
        if lg.objs.get_request().search is None:
            lg.objs.request.search = ''
        lg.objs.request.search = lg.objs.request.search.strip()
        if lg.com.control_length():
            self.update_lang1()
            self.update_lang2()
            self.auto_swap()
            mes = f'"{lg.objs.request.search}"'
            Message(f, mes).show_debug()
            lg.com.set_url()
            self.load_article(search = lg.objs.request.search
                             ,url = lg.objs.request.url)
    
    def load_suggestion(self, text):
        self.suggest.close()
        lg.objs.get_request().search = text
        self.go_search()
    
    def clear_search_field(self):
        #TODO: implement
        #objs.get_suggest().get_gui().close()
        gi.objs.get_panel().ent_src.clear()
    
    def paste(self):
        gi.objs.get_panel().ent_src.set_text(CLIPBOARD.paste())
    
    def minimize(self):
        self.table.popup.close()
        self.suggest.close()
        self.gui.minimize()
    
    def update_ui(self):
        gi.objs.get_panel().ent_src.focus()
        self.reset_opt(CONFIG.new['source'])
    
    def show(self):
        self.gui.show()
    
    def quit(self):
        f = '[MClient] mclient.App.quit'
        ''' This procedure is called by signal. Do not put 'self.close' here,
            it is run separately.
        '''
        CONFIG.quit()
        self.thread.end()
        ''' For this code to be executed last, it's not enough to put it in 
            '__main__' right before 'ROOT.end'.
        '''
        mes = _('Goodbye!')
        Message(f, mes).show_debug()
    
    def close(self):
        self.table.popup.close()
        self.suggest.close()
        self.gui.close()
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.sig_close.connect(self.close)
        self.gui.sig_close.connect(self.quit)
        self.gui.sig_pgdn.connect(self.table.go_page_down)
        self.gui.sig_pgup.connect(self.table.go_page_up)
        
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.minimize)
        self.gui.bind(('Down',), self.solve_go_down)
        self.gui.bind(('Up',), self.solve_go_up)
        self.gui.bind(('Ctrl+Home',), self.table.go_start)
        self.gui.bind(('Ctrl+End',), self.table.go_end)
        self.gui.bind(('Home',), self.table.go_line_start)
        self.gui.bind(('End',), self.table.go_line_end)
        self.gui.bind(('F1',), self.about.toggle)
        self.gui.bind(('F3',), self.table.search_next)
        self.gui.bind(('Shift+F3',), self.table.search_prev)
        self.gui.bind(('Ctrl+F',), self.table.search.show)
        self.gui.bind(('Return', 'Enter',), self.go_keyboard)
        self.gui.bind(('Ctrl+Return', 'Ctrl+Enter',), self.solve_copy)
        
        self.gui.bind(('Alt+0',), lambda:self.change_col_no(10))
        self.gui.bind(('Alt+1',), lambda:self.change_col_no(1))
        self.gui.bind(('Alt+2',), lambda:self.change_col_no(2))
        self.gui.bind(('Alt+3',), lambda:self.change_col_no(3))
        self.gui.bind(('Alt+4',), lambda:self.change_col_no(4))
        self.gui.bind(('Alt+5',), lambda:self.change_col_no(5))
        self.gui.bind(('Alt+6',), lambda:self.change_col_no(6))
        self.gui.bind(('Alt+7',), lambda:self.change_col_no(7))
        self.gui.bind(('Alt+8',), lambda:self.change_col_no(8))
        self.gui.bind(('Alt+9',), lambda:self.change_col_no(9))
        
        self.gui.bind(CONFIG.new['actions']['clear_history']['hotkeys']
                     ,self.clear_history)
        self.gui.bind(CONFIG.new['actions']['col1_down']['hotkeys']
                     ,lambda:self.table.go_next_section(0))
        self.gui.bind(CONFIG.new['actions']['col2_down']['hotkeys']
                     ,lambda:self.table.go_next_section(1))
        self.gui.bind(CONFIG.new['actions']['col3_down']['hotkeys']
                     ,lambda:self.table.go_next_section(2))
        self.gui.bind(CONFIG.new['actions']['col4_down']['hotkeys']
                     ,lambda:self.table.go_next_section(3))
        self.gui.bind(CONFIG.new['actions']['col1_up']['hotkeys']
                     ,lambda:self.table.go_prev_section(0))
        self.gui.bind(CONFIG.new['actions']['col2_up']['hotkeys']
                     ,lambda:self.table.go_prev_section(1))
        self.gui.bind(CONFIG.new['actions']['col3_up']['hotkeys']
                     ,lambda:self.table.go_prev_section(2))
        self.gui.bind(CONFIG.new['actions']['col4_up']['hotkeys']
                     ,lambda:self.table.go_prev_section(3))
        self.gui.bind(CONFIG.new['actions']['go_next']['hotkeys']
                     ,self.go_next)
        self.gui.bind(CONFIG.new['actions']['go_back']['hotkeys']
                     ,self.go_back)
        self.gui.bind(CONFIG.new['actions']['toggle_history']['hotkeys']
                     ,self.history.toggle)
        self.gui.bind(CONFIG.new['actions']['save_article']['hotkeys']
                     ,self.save.toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_settings']['hotkeys']
                     ,self.settings.toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                     ,self.symbols.show)
        self.gui.bind(CONFIG.new['actions']['swap_langs']['hotkeys']
                     ,self.swap_langs)
        self.gui.bind(CONFIG.new['actions']['toggle_block']['hotkeys']
                     ,objs.get_block().toggle_use)
        self.gui.bind(CONFIG.new['actions']['toggle_priority']['hotkeys']
                     ,objs.get_prior().toggle_use)
        self.gui.bind(CONFIG.new['actions']['show_block']['hotkeys']
                     ,objs.get_block().toggle)
        self.gui.bind(CONFIG.new['actions']['show_prior']['hotkeys']
                     ,objs.get_prior().toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_popup']['hotkeys']
                     ,self.table.show_popup)
        self.gui.bind(CONFIG.new['actions']['toggle_alphabet']['hotkeys']
                     ,self.toggle_alphabet)
        self.gui.bind(CONFIG.new['actions']['reload_article']['hotkeys']
                     ,self.reload)
        self.gui.bind(CONFIG.new['actions']['open_in_browser']['hotkeys']
                     ,self.logic.open_in_browser)
        self.gui.bind(CONFIG.new['actions']['print']['hotkeys']
                     ,self.logic.print)
        self.gui.bind(CONFIG.new['actions']['define']['hotkeys']
                     ,self.define)
        self.gui.bind(CONFIG.new['actions']['go_phrases']['hotkeys']
                     ,self.go_phrases)
        self.gui.bind(CONFIG.new['actions']['copy_article_url']['hotkeys']
                     ,self.copy_article_url)
        self.gui.bind(CONFIG.new['actions']['copy_url']['hotkeys']
                     ,self.copy_cell_url)
        self.gui.bind(CONFIG.new['actions']['copy_nominative']['hotkeys']
                     ,self.copy_wform)
        self.gui.bind(CONFIG.new['actions']['select_block']['hotkeys']
                     ,self.block_mode.toggle)
        
        self.history.gui.bind(CONFIG.new['actions']['toggle_history']['hotkeys']
                             ,self.history.close)
        objs.get_block().gui.bind(CONFIG.new['actions']['show_block']['hotkeys']
                                 ,objs.block.close)
        objs.get_prior().gui.bind(CONFIG.new['actions']['show_prior']['hotkeys']
                                 ,objs.prior.close)
        
        self.settings.gui.bind(CONFIG.new['actions']['toggle_settings']['hotkeys']
                              ,self.settings.close)
                      
        #TODO: iterate through all keys
        if CONFIG.new['actions']['toggle_spec_symbols']['hotkeys'] == ['Ctrl+E']:
            gi.objs.get_panel().ent_src.widget.sig_ctrl_e.connect(self.symbols.show)
        else:
            gi.objs.get_panel().ent_src.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                                            ,self.symbols.show)
        self.symbols.gui.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                             ,self.symbols.close)
        
        gi.objs.get_table().clicked.connect(self.go_url)
        gi.objs.table.sig_mmb.connect(self.minimize)
        ''' Recalculate pages each time the main window is resized. This allows
            to save resources and avoid getting dummy geometry which will be
            returned before the window is shown.
        '''
        self.gui.parent.resizeEvent = self.table.set_coords
        
        gi.objs.panel.btn_abt.set_action(self.about.toggle)
        gi.objs.panel.btn_alp.set_action(self.toggle_alphabet)
        gi.objs.panel.btn_blk.set_action(objs.block.toggle)
        gi.objs.panel.btn_brw.set_action(self.logic.open_in_browser)
        gi.objs.panel.btn_cap.set_action(self.watch_clipboard)
        gi.objs.panel.btn_clr.set_action(self.clear_search_field)
        gi.objs.panel.btn_def.set_action(lambda x:self.define(False))
        gi.objs.panel.btn_hst.set_action(self.history.toggle)
        gi.objs.panel.btn_ins.set_action(self.paste)
        gi.objs.panel.btn_nxt.set_action(self.go_next)
        gi.objs.panel.btn_pri.set_action(objs.prior.toggle)
        gi.objs.panel.btn_prn.set_action(self.logic.print)
        gi.objs.panel.btn_prv.set_action(self.go_back)
        gi.objs.panel.btn_qit.set_action(self.close)
        gi.objs.panel.btn_rld.set_action(self.reload)
        gi.objs.panel.btn_rp1.set_action(self.insert_repeat_sign)
        gi.objs.panel.btn_rp2.set_action(self.insert_repeat_sign2)
        gi.objs.panel.btn_sav.set_action(self.save.toggle)
        gi.objs.panel.btn_ser.set_action(self.table.search.toggle)
        gi.objs.panel.btn_set.set_action(self.settings.toggle)
        gi.objs.panel.btn_sym.set_action(self.symbols.show)
        gi.objs.panel.btn_swp.set_action(self.swap_langs)
        gi.objs.panel.btn_trn.set_action(self.go_keyboard)
        
        gi.objs.panel.ent_src.widget.sig_home.connect(self.table.go_line_start)
        gi.objs.panel.ent_src.widget.sig_end.connect(self.table.go_line_end)
        gi.objs.panel.ent_src.widget.sig_ctrl_home.connect(self.table.go_start)
        gi.objs.panel.ent_src.widget.sig_ctrl_end.connect(self.table.go_end)
        gi.objs.panel.ent_src.widget.sig_ctrl_space.connect(self.show_suggestions)
        # Binding 'Left' and 'Right' to self.gui does not work for some reason
        gi.objs.panel.ent_src.widget.sig_left_arrow.connect(self.solve_go_left)
        gi.objs.panel.ent_src.widget.sig_right_arrow.connect(self.solve_go_right)
        gi.objs.panel.opt_lg1.widget.activated.connect(self.go_search)
        gi.objs.panel.opt_lg2.widget.activated.connect(self.go_search)
        gi.objs.panel.opt_src.widget.activated.connect(self.set_source)
        gi.objs.panel.opt_col.set_action(self.set_columns)
        
        gi.objs.table.sig_rmb.connect(self.solve_copy)
        
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
        
        self.suggest.gui.sig_load.connect(self.load_suggestion)
        
        objs.block.gui.sig_close.connect(objs.block.close)
        objs.prior.gui.sig_close.connect(objs.prior.close)
        
        self.thread.bind_catch(self.catch)
    
    def set_title(self, title):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.about = About()
        self.symbols = sm.Symbols()
        self.welcome = Welcome(self.about.get_product())
        self.settings = st.objs.get_settings()
        self.history = hs.History()
        self.save = Save()
        self.suggest = sg.Suggest()
        self.block_mode = BlockMode()
        self.set_title(self.about.logic.product)
        self.set_bindings()



class Objects:
    
    def __init__(self):
        self.geometry = self.panel = self.block = self.prior = self.app = None
    
    def get_app(self):
        if self.app is None:
            self.app = App()
        return self.app
    
    def get_geometry(self):
        if not self.geometry:
            import windows.geometry.controller as wg
            self.geometry = wg.Geometry()
        return self.geometry
    
    def get_block(self):
        if self.block is None:
            self.block = Block()
        return self.block
    
    def get_prior(self):
        if self.prior is None:
            self.prior = Priorities()
        return self.prior


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    if CONFIG.Success:
        lg.objs.get_plugins(Debug=False, maxrows=1000)
        objs.get_app().run_thread()
        objs.app.welcome.reset()
        objs.app.solve_screen()
        objs.app.show()
        objs.app.welcome.resize_rows()
    else:
        mes = _('Invalid configuration!')
        #FIX: quit app normally after common dialog
        #Message(f, mes, True).show_error()
        idebug = Debug(f, mes)
        idebug.show()
    ROOT.end()
