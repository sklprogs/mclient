#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.graphics.debug.controller import DEBUG
from skl_shared_qt.logic import OS, Input, Text
from skl_shared_qt.online import Online
from skl_shared_qt.time import Timer

from config import CONFIG, HistorySubjects
from manager import PLUGINS
from articles import ARTICLES
from table.controller import TABLE
import logic as lg
from logic import REQUEST
import gui as gi
import format as fm
import cells as cl
from prior_block.controller import BLOCK, PRIOR
from settings.controller import SETTINGS, SAVE_SETTINGS
from suggest.controller import SUGGEST
from about.controller import ABOUT
import symbols.controller as sm
from welcome.controller import WELCOME
import history.controller as hs
from save.controller import Save
from popup.controller import POPUP
import keylistener.gui as kg
from subjects import SUBJECTS
from block_mode import BLOCK_MODE
from columns import COL_WIDTH


#DEBUG = False


class UpdateUI:
    
    def __init__(self):
        self.Parallel = ARTICLES.is_parallel()
        self.Separate = ARTICLES.is_separate()
    
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
            PRIOR.gui.cbx_pri.enable()
        else:
            mes.append(_('Status: OFF'))
            PRIOR.gui.cbx_pri.disable()
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
        ''' #NOTE: We cannot use 'ARTICLES.get_cells()' since it does not have
            blocked items.
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
            BLOCK.gui.cbx_pri.enable()
        else:
            BLOCK.gui.cbx_pri.disable()
    
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
        if REQUEST.search:
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



class App:
    
    def __init__(self):
        # 'thread' name is OK here, but will override a built-in method in GUI
        self.thread = kg.Thread()
        self.logic = lg.App()
        self.gui = gi.App()
        TABLE.gui.WIDE_ROW_COLOR = CONFIG.new["rows"]["border"]["color"]
        TABLE.gui.WIDE_ROW_LEN = CONFIG.new["rows"]["border"]["length"]
        self.set_gui()
        self.set_hints()
        self.update_ui()
    
    def copy_block(self):
        if BLOCK_MODE.copy_block():
            if CONFIG.new['Iconify']:
                self.minimize()
    
    def solve_copy(self):
        if BLOCK_MODE.blockno > -1:
            self.copy_block()
        else:
            self.copy_cell()
    
    def solve_go_left(self):
        if BLOCK_MODE.blockno > -1:
            BLOCK_MODE.select_prev()
        else:
            TABLE.go_left()
    
    def solve_go_right(self):
        if BLOCK_MODE.blockno > -1:
            BLOCK_MODE.select_next()
        else:
            TABLE.go_right()
    
    def solve_go_down(self):
        if BLOCK_MODE.blockno > -1:
            BLOCK_MODE.select_next()
        else:
            TABLE.go_down()
    
    def solve_go_up(self):
        if BLOCK_MODE.blockno > -1:
            BLOCK_MODE.select_prev()
        else:
            TABLE.go_up()
    
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
                ,(gi.objs.panel.btn_qit, 'quit'))
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
        items = SUGGEST.suggest(fragment, 35)
        if not items:
            mes = _('No suggestions are available!')
            Message(f, mes).show_info()
            return
        SUGGEST.fill(items)
        SUGGEST.show()
        x = self.get_x() + gi.objs.panel.ent_src.get_x()
        y = self.get_height() + self.get_y() - SUGGEST.get_height() \
                              - gi.objs.panel.ent_src.get_root_y()
        SUGGEST.set_geometry(x, y, 170, SUGGEST.get_height())
    
    def show_popup(self):
        f = '[MClient] mclient.App.show_popup'
        text = TABLE.get_cell_code()
        if not text:
            rep.empty(f)
            return
        rowno, colno = TABLE.get_cell()
        max_width = self.get_width()
        width = TABLE.get_col_width(colno)
        height = TABLE.get_row_height(rowno)
        win_y = self.get_y()
        x1 = TABLE.get_cell_x(colno) + self.get_x()
        if CONFIG.new['popup']['center']:
            y1 = TABLE.get_cell_y(rowno) + win_y - height / 2
            if y1 < win_y:
                y1 = win_y
        else:
            # The value is picked up by the trial-and-error method
            y1 = TABLE.get_cell_y(rowno) + win_y - height + 10
        x2 = x1 + width
        y2 = y1 + height
        POPUP.fill(text)
        POPUP.adjust_position(x1, width, y1, height, max_width
                             ,CONFIG.new['popup']['center'])
        POPUP.show()
    
    def get_cell(self):
        f = '[MClient] mclient.App.get_cell'
        table = ARTICLES.get_table()
        if not table:
            rep.empty(f)
            return
        rowno, colno = TABLE.get_cell()
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
        url = PLUGINS.fix_url(url)
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
        url = PLUGINS.fix_url(url)
        CLIPBOARD.copy(url)
        if CONFIG.new['Iconify']:
            self.minimize()
    
    def go_phrases(self):
        f = '[MClient] mclient.App.go_phrases'
        tuple_ = TABLE.logic.get_phsubj()
        if not tuple_:
            rep.empty(f)
            return
        text, url = tuple_[0], tuple_[1]
        if not url:
            rep.empty(f)
            return
        REQUEST.search = text
        REQUEST.url = url
        mes = _('Open link: {}').format(REQUEST.url)
        Message(f, mes).show_info()
        self.load_article(REQUEST.search, REQUEST.url)
    
    def activate(self):
        if OS.is_win():
            from windows.geometry.controller import Geometry
            self.geometry = Geometry()
            self.geometry.keyword = self.about.logic.product
            self.geometry.activate()
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
        REQUEST.search = new_clipboard
        self.go_search()
    
    def run_thread(self):
        self.thread.run_thread()
    
    def edit_blacklist(self):
        f = '[MClient] mclient.App.edit_blacklist'
        old_list = CONFIG.new['subjects']['blocked']
        old_key = CONFIG.new['BlockSubjects']
        BLOCK.reset(lst1 = old_list
                   ,lst2=PLUGINS.get_subjects()
                   ,art_subjects = com.get_article_subjects()
                   ,majors = PLUGINS.get_majors())
        BLOCK.set_checkbox(CONFIG.new['BlockSubjects'])
        BLOCK.show()
        CONFIG.new['BlockSubjects'] = self.block.get_checkbox()
        new_list = BLOCK.get1()
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
            pattern = TABLE.get_cell_text()
        else:
            pattern = REQUEST.search
        if not pattern:
            rep.empty(f)
            return
        pattern = _('what is "{}"?').format(pattern)
        Online(base = CONFIG.new['web_search_url']
              ,pattern = pattern).browse()
    
    def reload(self):
        search = ARTICLES.get_search()
        url = ARTICLES.get_url()
        ARTICLES.clear_article()
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
        if not REQUEST.search:
            rep.lazy(f)
            return
        self.history.add_row(id_ = ARTICLES.id
                            ,source = PLUGINS.source
                            ,lang1 = PLUGINS.get_lang1()
                            ,lang2 = PLUGINS.get_lang2()
                            ,search = ARTICLES.get_search())
        # Setting column width works only after updating the model, see https://stackoverflow.com/questions/8364061/how-do-you-set-the-column-width-on-a-qtreeview
        self.history.gui.set_col_width()
    
    def go_history(self, id_):
        f = '[MClient] mclient.App.go_history'
        if id_ is None:
            rep.empty(f)
            return
        ARTICLES.set_id(id_)
        source = ARTICLES.get_source()
        lang1 = ARTICLES.get_lang1()
        lang2 = ARTICLES.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        mes = _('Set source to "{}"')
        mes = mes.format(CONFIG.new['source'])
        Message(f, mes).show_info()
        PLUGINS.set(CONFIG.new['source'])
        PLUGINS.set_lang1(lang1)
        PLUGINS.set_lang2(lang2)
        self.reset_opt(CONFIG.new['source'])
        self.load_article()
    
    def clear_history(self):
        ARTICLES.reset()
        REQUEST.reset()
        self.solve_screen()
    
    def go_back(self):
        f = '[MClient] mclient.App.go_back'
        if ARTICLES.get_len() in (0, 1):
            rep.lazy(f)
            return
        if ARTICLES.id == 0:
            ARTICLES.set_id(ARTICLES.get_max_id())
        else:
            ARTICLES.set_id(ARTICLES.id - 1)
        source = ARTICLES.get_source()
        lang1 = ARTICLES.get_lang1()
        lang2 = ARTICLES.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        PLUGINS.set(CONFIG.new['source'])
        PLUGINS.set_lang1(lang1)
        PLUGINS.set_lang2(lang2)
        self.reset_opt(CONFIG.new['source'])
        self.load_article()
        self.history.go_up()
    
    def go_next(self):
        f = '[MClient] mclient.App.go_next'
        if ARTICLES.get_len() in (0, 1):
            rep.lazy(f)
            return
        if ARTICLES.is_last():
            ARTICLES.set_id(0)
        else:
            ARTICLES.set_id(ARTICLES.id + 1)
        source = ARTICLES.get_source()
        lang1 = ARTICLES.get_lang1()
        lang2 = ARTICLES.get_lang2()
        if not source or not lang1 or not lang2:
            rep.empty(f)
            return
        CONFIG.new['source'] = source
        PLUGINS.set(CONFIG.new['source'])
        PLUGINS.set_lang1(lang1)
        PLUGINS.set_lang2(lang2)
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
        col_num = SETTINGS.gui.ent_num.get()
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
        
        SETTINGS.gui.ent_num.set_text(col_num)
        SETTINGS.gui.ent_fix.set_text(63)
        SETTINGS.gui.ent_trm.set_text(term_width)
    
    def set_col_num(self):
        gi.objs.get_panel().opt_col.set(COL_WIDTH.term_num)
    
    def apply_settings(self):
        SETTINGS.close()
        SUBJECTS.reset(PLUGINS.get_article_subjects())
        SAVE_SETTINGS.run()
        lg.com.export_style()
        COL_WIDTH.reset()
        COL_WIDTH.run()
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
        if not ARTICLES.is_parallel():
            CONFIG.new['columns']['num'] = Input(title = f
                                                ,value = gi.objs.get_panel().opt_col.get()).get_integer()
        collimit = COL_WIDTH.fixed_num + COL_WIDTH.term_num
        mes = _('Set the number of columns to {} ({} in total)')
        mes = mes.format(COL_WIDTH.term_num, collimit)
        Message(f, mes).show_info()
    
    def update_columns(self):
        ''' Update a column number in GUI; adjust the column number (both logic
            and GUI) in special cases.
        '''
        f = '[MClient] mclient.App.update_columns'
        if not ARTICLES.is_parallel():
            CONFIG.new['columns']['num'] = COL_WIDTH.term_num
        gi.objs.get_panel().opt_col.set(COL_WIDTH.term_num)
        collimit = COL_WIDTH.fixed_num + COL_WIDTH.term_num
        mes = _('Set the number of columns to {} ({} in total)')
        mes = mes.format(COL_WIDTH.term_num, collimit)
        Message(f, mes).show_info()
    
    def set_source(self):
        f = '[MClient] mclient.App.set_source'
        CONFIG.new['source'] = gi.objs.get_panel().opt_src.get()
        mes = _('Set source to "{}"').format(CONFIG.new['source'])
        Message(f, mes).show_info()
        PLUGINS.set(CONFIG.new['source'])
        self.reset_opt(CONFIG.new['source'])
        self.go_search()
    
    def auto_swap(self):
        f = '[MClient] mclient.App.auto_swap'
        lang1 = gi.objs.get_panel().opt_lg1.get()
        lang2 = gi.objs.panel.opt_lg2.get()
        if PLUGINS.is_oneway() or not CONFIG.new['Autoswap'] \
        or not REQUEST.search:
            rep.lazy(f)
            return
        if Text(REQUEST.search).has_cyrillic():
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
        lang1 = PLUGINS.get_lang1()
        lang2 = PLUGINS.get_lang2()
        langs1 = PLUGINS.get_langs1()
        langs2 = PLUGINS.get_langs2(lang1)
        sources = PLUGINS.get_sources()
        if not (langs1 and langs2 and lang1 and lang2 and sources):
            rep.empty(f)
            return
        gi.objs.get_panel().opt_lg1.reset(items=langs1, default=lang1)
        gi.objs.panel.opt_lg2.reset(items=langs2, default=lang2)
        #NOTE: change this upon the change of the default source
        gi.objs.panel.opt_src.reset(items=sources, default=default)
    
    def set_next_lang1(self):
        ''' We want to navigate through the full list of supported languages
            rather than through the list of 'lang2' pairs so we reset the
            widget first.
        '''
        old = gi.objs.get_panel().opt_lg1.get()
        gi.objs.panel.opt_lg1.reset(items = PLUGINS.get_langs1()
                                   ,default = old)
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
        gi.objs.panel.opt_lg1.reset(items = PLUGINS.get_langs1()
                                   ,default = old)
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
        if PLUGINS.get_lang1() != lang:
            mes = _('Set language: {}').format(lang)
            Message(f, mes).show_info()
            CONFIG.new['lang1'] = lang
            PLUGINS.set_lang1(lang)
    
    def set_lang2(self):
        f = '[MClient] mclient.App.set_lang2'
        lang = gi.objs.get_panel().opt_lg2.get()
        if PLUGINS.get_lang2() != lang:
            mes = _('Set language: {}').format(lang)
            Message(f, mes).show_info()
            CONFIG.new['lang2'] = lang
            PLUGINS.set_lang2(lang)
    
    def update_lang1(self):
        f = '[MClient] mclient.App.update_lang1'
        self.set_lang1()
        self.set_lang2()
        lang1 = PLUGINS.get_lang1()
        langs1 = PLUGINS.get_langs1()
        if not langs1:
            rep.empty(f)
            return
        gi.objs.get_panel().opt_lg1.set(lang1)
        self.set_lang1()
    
    def update_lang2(self):
        f = '[MClient] mclient.App.update_lang2'
        self.set_lang1()
        self.set_lang2()
        lang1 = PLUGINS.get_lang1()
        lang2 = PLUGINS.get_lang2()
        langs2 = PLUGINS.get_langs2(lang1)
        if not langs2:
            rep.empty(f)
            return
        if not lang2 in langs2:
            lang2 = langs2[0]
        gi.objs.get_panel().opt_lg2.reset(items=langs2, default=lang2)
        self.set_lang2()
    
    def swap_langs(self):
        f = '[MClient] mclient.App.swap_langs'
        if PLUGINS.is_oneway():
            mes = _('Cannot swap languages, this is a one-way dictionary!')
            Message(f, mes, True).show_info()
            return
        self.update_lang1()
        self.update_lang2()
        lang1 = gi.objs.get_panel().opt_lg1.get()
        lang2 = gi.objs.panel.opt_lg2.get()
        lang1, lang2 = lang2, lang1
        langs1 = PLUGINS.get_langs1()
        langs2 = PLUGINS.get_langs2(lang1)
        if not langs1:
            rep.empty(f)
            return
        if not (langs2 and lang1 in langs1 and lang2 in langs2):
            mes = _('Pair {}-{} is not supported!').format(lang1, lang2)
            Message(f, mes, True).show_warning()
            return
        gi.objs.panel.opt_lg1.reset(items=langs1, default=lang1)
        gi.objs.panel.opt_lg2.reset(items=langs2, default=lang2)
        self.update_lang1()
        self.update_lang2()
    
    def insert_repeat_sign2(self):
        # Insert the previous search string
        f = '[MClient] mclient.App.insert_repeat_sign2'
        if ARTICLES.get_len() < 2:
            rep.empty(f)
            return
        ARTICLES.set_id(ARTICLES.id-1)
        CLIPBOARD.copy(ARTICLES.get_search())
        self.paste()
        ARTICLES.set_id(ARTICLES.id+1)
    
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
        cell = TABLE.get_cell()
        if not cell:
            rep.empty(f)
            return
        rowno, colno = cell[0], cell[1]
        cell = ARTICLES.get_cell(rowno, colno)
        if not cell:
            rep.empty(f)
            return
        REQUEST.search = cell.text
        if cell.url:
            REQUEST.url = cell.url
            mes = _('Open link: {}').format(REQUEST.url)
            Message(f, mes).show_info()
            self.load_article(search = REQUEST.search
                             ,url = REQUEST.url)
        else:
            self.go_search()
    
    def copy_cell(self):
        ''' Do not combine these conditions with 'and' since the interpreter
            may decide to check the lighter condition first.
        '''
        if TABLE.copy_cell():
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
        SUGGEST.close()
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
            cells = PLUGINS.request(search=search, url=url)
            SUBJECTS.reset(PLUGINS.get_article_subjects())
            ARTICLES.add(search = search
                        ,url = url
                        ,cells = cells
                        ,fixed_urls = PLUGINS.get_fixed_urls()
                        ,raw_code = PLUGINS.get_htm()
                        ,subjf = SUBJECTS.article
                        ,blocked = SUBJECTS.block
                        ,prioritized = SUBJECTS.prior)
            HistorySubjects().add(PLUGINS.get_article_subjects())
            self.add_history()
        else:
            mes = _('Load article No. {} from memory').format(artid)
            Message(f, mes).show_info()
            ARTICLES.set_id(artid)
            SUBJECTS.reset(PLUGINS.get_article_subjects())
            cells = ARTICLES.get_cells()
            
        self.solve_screen()
        
        cells = cl.Expand(cells).run()
        iomit = cl.Omit(cells)
        cells = iomit.run()
        cells = cl.Prioritize(cells).run()
        
        COL_WIDTH.reset()
        COL_WIDTH.run()
        
        self.update_columns()
        
        cells = cl.View(cells).run()
        iwrap = cl.Wrap(cells)
        iwrap.run()
        
        TABLE.reset(iwrap.plain, iwrap.code)
        
        ARTICLES.set_blocked_cells(iomit.omit_cells)
        ARTICLES.set_table(iwrap.cells)
        
        #REQUEST.text = lg.com.get_text(cells)
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
        TABLE.go_bookmark()
    
    def go_keyboard(self):
        search = gi.objs.get_panel().ent_src.get().strip()
        if search == '':
            self.go_url()
        elif search == CONFIG.new['repeat_sign']:
            self.insert_repeat_sign()
        elif search == CONFIG.new['repeat_sign2']:
            self.insert_repeat_sign2()
        else:
            REQUEST.search = search
            self.go_search()
    
    def go_search(self):
        f = '[MClient] mclient.App.go_search'
        if REQUEST.search is None:
            REQUEST.search = ''
        REQUEST.search = REQUEST.search.strip()
        if lg.com.control_length():
            self.update_lang1()
            self.update_lang2()
            self.auto_swap()
            mes = f'"{REQUEST.search}"'
            Message(f, mes).show_debug()
            lg.com.set_url()
            self.load_article(search = REQUEST.search
                             ,url = REQUEST.url)
    
    def load_suggestion(self, text):
        SUGGEST.close()
        REQUEST.search = text
        self.go_search()
    
    def clear_search_field(self):
        #TODO: implement
        #objs.get_suggest().get_gui().close()
        gi.objs.get_panel().ent_src.clear()
    
    def paste(self):
        gi.objs.get_panel().ent_src.set_text(CLIPBOARD.paste())
    
    def minimize(self):
        POPUP.close()
        SUGGEST.close()
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
        POPUP.close()
        SUGGEST.close()
        self.gui.close()
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.sig_close.connect(self.close)
        self.gui.sig_close.connect(self.quit)
        self.gui.sig_pgdn.connect(TABLE.go_page_down)
        self.gui.sig_pgup.connect(TABLE.go_page_up)
        
        self.gui.bind(('Ctrl+Q',), self.close)
        self.gui.bind(('Esc',), self.minimize)
        self.gui.bind(('Down',), self.solve_go_down)
        self.gui.bind(('Up',), self.solve_go_up)
        self.gui.bind(('Ctrl+Home',), TABLE.go_start)
        self.gui.bind(('Ctrl+End',), TABLE.go_end)
        self.gui.bind(('Home',), TABLE.go_line_start)
        self.gui.bind(('End',), TABLE.go_line_end)
        self.gui.bind(('F1',), ABOUT.toggle)
        self.gui.bind(('F3',), TABLE.search_next)
        self.gui.bind(('Shift+F3',), TABLE.search_prev)
        self.gui.bind(('Ctrl+F',), TABLE.search.show)
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
                     ,lambda:TABLE.go_next_section(0))
        self.gui.bind(CONFIG.new['actions']['col2_down']['hotkeys']
                     ,lambda:TABLE.go_next_section(1))
        self.gui.bind(CONFIG.new['actions']['col3_down']['hotkeys']
                     ,lambda:TABLE.go_next_section(2))
        self.gui.bind(CONFIG.new['actions']['col4_down']['hotkeys']
                     ,lambda:TABLE.go_next_section(3))
        self.gui.bind(CONFIG.new['actions']['col1_up']['hotkeys']
                     ,lambda:TABLE.go_prev_section(0))
        self.gui.bind(CONFIG.new['actions']['col2_up']['hotkeys']
                     ,lambda:TABLE.go_prev_section(1))
        self.gui.bind(CONFIG.new['actions']['col3_up']['hotkeys']
                     ,lambda:TABLE.go_prev_section(2))
        self.gui.bind(CONFIG.new['actions']['col4_up']['hotkeys']
                     ,lambda:TABLE.go_prev_section(3))
        self.gui.bind(CONFIG.new['actions']['go_next']['hotkeys']
                     ,self.go_next)
        self.gui.bind(CONFIG.new['actions']['go_back']['hotkeys']
                     ,self.go_back)
        self.gui.bind(CONFIG.new['actions']['toggle_history']['hotkeys']
                     ,self.history.toggle)
        self.gui.bind(CONFIG.new['actions']['save_article']['hotkeys']
                     ,self.save.toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_settings']['hotkeys']
                     ,SETTINGS.toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                     ,self.symbols.show)
        self.gui.bind(CONFIG.new['actions']['swap_langs']['hotkeys']
                     ,self.swap_langs)
        self.gui.bind(CONFIG.new['actions']['toggle_block']['hotkeys']
                     ,BLOCK.toggle_use)
        self.gui.bind(CONFIG.new['actions']['toggle_priority']['hotkeys']
                     ,PRIOR.toggle_use)
        self.gui.bind(CONFIG.new['actions']['show_block']['hotkeys']
                     ,BLOCK.toggle)
        self.gui.bind(CONFIG.new['actions']['show_prior']['hotkeys']
                     ,PRIOR.toggle)
        self.gui.bind(CONFIG.new['actions']['toggle_popup']['hotkeys']
                     ,TABLE.show_popup)
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
                     ,BLOCK_MODE.toggle)
        
        self.history.gui.bind(CONFIG.new['actions']['toggle_history']['hotkeys']
                             ,self.history.close)
        BLOCK.gui.bind(CONFIG.new['actions']['show_block']['hotkeys']
                      ,BLOCK.close)
        PRIOR.gui.bind(CONFIG.new['actions']['show_prior']['hotkeys']
                      ,PRIOR.close)
        
        SETTINGS.gui.bind(CONFIG.new['actions']['toggle_settings']['hotkeys']
                         ,SETTINGS.close)
                      
        #TODO: iterate through all keys
        if CONFIG.new['actions']['toggle_spec_symbols']['hotkeys'] == ['Ctrl+E']:
            gi.objs.get_panel().ent_src.widget.sig_ctrl_e.connect(self.symbols.show)
        else:
            gi.objs.get_panel().ent_src.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                                            ,self.symbols.show)
        self.symbols.gui.bind(CONFIG.new['actions']['toggle_spec_symbols']['hotkeys']
                             ,self.symbols.close)
        
        TABLE.gui.clicked.connect(self.go_url)
        TABLE.gui.sig_mmb.connect(self.minimize)
        TABLE.gui.sig_rmb.connect(self.solve_copy)
        TABLE.gui.sig_popup.connect(self.show_popup)
        ''' Recalculate pages each time the main window is resized. This allows
            to save resources and avoid getting dummy geometry which will be
            returned before the window is shown.
        '''
        self.gui.parent.resizeEvent = TABLE.set_coords
        
        gi.objs.panel.btn_abt.set_action(ABOUT.toggle)
        gi.objs.panel.btn_alp.set_action(self.toggle_alphabet)
        gi.objs.panel.btn_blk.set_action(BLOCK.toggle)
        gi.objs.panel.btn_brw.set_action(self.logic.open_in_browser)
        gi.objs.panel.btn_cap.set_action(self.watch_clipboard)
        gi.objs.panel.btn_clr.set_action(self.clear_search_field)
        gi.objs.panel.btn_def.set_action(lambda x:self.define(False))
        gi.objs.panel.btn_hst.set_action(self.history.toggle)
        gi.objs.panel.btn_ins.set_action(self.paste)
        gi.objs.panel.btn_nxt.set_action(self.go_next)
        gi.objs.panel.btn_pri.set_action(PRIOR.toggle)
        gi.objs.panel.btn_prn.set_action(self.logic.print)
        gi.objs.panel.btn_prv.set_action(self.go_back)
        gi.objs.panel.btn_qit.set_action(self.close)
        gi.objs.panel.btn_rld.set_action(self.reload)
        gi.objs.panel.btn_rp1.set_action(self.insert_repeat_sign)
        gi.objs.panel.btn_rp2.set_action(self.insert_repeat_sign2)
        gi.objs.panel.btn_sav.set_action(self.save.toggle)
        gi.objs.panel.btn_ser.set_action(TABLE.search.toggle)
        gi.objs.panel.btn_set.set_action(SETTINGS.toggle)
        gi.objs.panel.btn_sym.set_action(self.symbols.show)
        gi.objs.panel.btn_swp.set_action(self.swap_langs)
        gi.objs.panel.btn_trn.set_action(self.go_keyboard)
        
        gi.objs.panel.ent_src.widget.sig_home.connect(TABLE.go_line_start)
        gi.objs.panel.ent_src.widget.sig_end.connect(TABLE.go_line_end)
        gi.objs.panel.ent_src.widget.sig_ctrl_home.connect(TABLE.go_start)
        gi.objs.panel.ent_src.widget.sig_ctrl_end.connect(TABLE.go_end)
        gi.objs.panel.ent_src.widget.sig_ctrl_space.connect(self.show_suggestions)
        # Binding 'Left' and 'Right' to self.gui does not work for some reason
        gi.objs.panel.ent_src.widget.sig_left_arrow.connect(self.solve_go_left)
        gi.objs.panel.ent_src.widget.sig_right_arrow.connect(self.solve_go_right)
        gi.objs.panel.opt_lg1.widget.activated.connect(self.go_search)
        gi.objs.panel.opt_lg2.widget.activated.connect(self.go_search)
        gi.objs.panel.opt_src.widget.activated.connect(self.set_source)
        gi.objs.panel.opt_col.set_action(self.set_columns)
        
        self.symbols.gui.table.clicked.connect(self.paste_symbol)
        self.symbols.gui.table.sig_space.connect(self.paste_symbol)
        self.symbols.gui.sig_return.connect(self.paste_symbol)
        self.symbols.gui.table.sig_rmb.connect(self.copy_symbol)
        self.symbols.gui.sig_ctrl_return.connect(self.copy_symbol)
        
        SETTINGS.gui.btn_apl.set_action(self.apply_settings)
        SETTINGS.gui.btn_sug.set_action(self.suggest_col_widths)
        SETTINGS.gui.sig_close.connect(SETTINGS.close)
        
        self.history.gui.sig_close.connect(self.history.close)
        self.history.gui.sig_go.connect(self.go_history)
        
        SUGGEST.gui.sig_load.connect(self.load_suggestion)
        
        BLOCK.gui.sig_close.connect(BLOCK.close)
        PRIOR.gui.sig_close.connect(PRIOR.close)
        
        BLOCK.gui.sig_load.connect(self.load_article)
        PRIOR.gui.sig_load.connect(self.load_article)
        
        self.thread.bind_catch(self.catch)
    
    def set_title(self, title):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.symbols = sm.Symbols()
        self.history = hs.History()
        self.save = Save()
        self.set_title(ABOUT.logic.product)
        self.set_bindings()


if __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    if CONFIG.Success:
        PLUGINS.Debug = False
        PLUGINS.maxrows = 1000
        app = App()
        app.run_thread()
        WELCOME.reset()
        app.solve_screen()
        app.show()
        WELCOME.resize_rows()
    else:
        mes = _('Invalid configuration!')
        #FIX: quit app normally after common dialog
        Message(f, mes, True).show_error()
        #DEBUG.reset(f, mes)
        #DEBUG.show()
    ROOT.end()
