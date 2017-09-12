#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo
    - Make transcriptions Selectable
    - Create an option to toggle SELECTABLE (no need to update DB) (see WebFrame.select)
    - Use NO/NODE instead of POS *where appropriate*
    - Loop WebFrame.move_page_up & WebFrame.move_page_down
    - Restore selection upon changing a setting and loading the article again
    - Use the language pair as a part of an article ID. Otherwise, we cannot view same SEARCH in different languages ('RUS-XAL' -> 'липа' -> 'EN-RU')
    - Use borders of the cell, not borders of the block when calculating ShiftScreen
    - Store '_html_raw' value for all articles, not just for the latest new loaded one
    - Move 'insert_fixed' outside of Elems (since fixed columns can vary now)
    -
'''

''' # fix
    - odd fixed columns are inserted
    - NODE1 < NODE2 in some rare cases
    - ShiftScreen with SelectTermsOnly=0 on 'painting'
    - ShiftScreen on 'делать' -> 'Вычислительная техника'
    - PageDown fails on the last block of MAXCOL (do, set) (we need to loop PgUp/PgDn)
    - shift_y does not work properly when changing sizes on-the-fly
    - Changing node still sometimes fails
    - Some blocks on the borders of pages are still not fully readable
    - A Warning appears when only separate words are found
    - When adding a space between blocks, add it to the end of the preceding block; otherwise, sorting terms may not work correctly (башмак -> sabaton)
    - When deleting/inserting fixed columns, preserve URL
    - Clicking the selected block outside the selection causes the 'URL is empty' message
    - EN-RU -> collimit: 4 (w/o fixed) -> 'bow' -> 'арчак' -> Up => No selection
    - EN-RU -> collimit: 4 (w/o fixed) -> 'bow' -> 'Ятенный спорт' -> Up => No selection
    - bind RMB to tkinterhtml widget only, not top; check this on clear_history button
    - Do not warn about an empty URL after clearing history
    - Clear CurRequest data after clearing history
    - Unable to load same phrase sections (e.g., 'Медицина' in different articles)
    - ShiftScreen: A -> Сельское хозяйство -> <Start>
    - Fix Moves (line_start, line_end, PgDown/PgUp) on 'random fury'
    - When there is an article where all dictionaries are blocked, Previous-Next arrows are blank even if the history is not empty
    - Fix links in a saved raw html
    - 'gen_poses' cannot find Search items when Page is forced to use 'file=' (RU-DE, 'tun')
'''

import gettext

gettext.install('mclient','./locale')

import os
import sys
import io
import tkinter     as tk
from tkinter import ttk
import tkinterhtml as th
import shared      as sh
import sharedGUI   as sg
import page        as pg
import tags        as tg
import elems       as el
import cells       as cl
import db
import mkhtml      as mh


product = 'MClient'
version = '5.2'

third_parties = '''
tkinterhtml
https://bitbucket.org/aivarannamaa/tkinterhtml
License: MIT
Copyright (c) <year> aivarannamaa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''



class ConfigMclient(sh.Config):

    def __init__(self):
        super().__init__()
        self.sections         = [sh.SectionBooleans
                                ,sh.SectionIntegers
                                ,sh.SectionVariables
                                ]
        self.sections_abbr    = [sh.SectionBooleans_abbr
                                ,sh.SectionIntegers_abbr
                                ,sh.SectionVariables_abbr
                                ]
        self.sections_func    = [sh.config_parser.getboolean
                                ,sh.config_parser.getint
                                ,sh.config_parser.get
                                ]
        self.message          = _('The following sections and/or keys are missing:') + '\n'
        self.total_keys       = 0
        self.changed_keys     = 0
        self.missing_keys     = 0
        self.missing_sections = 0
        # Create these keys before reading the config
        self.path    = sh.objs.pdir().add('mclient.cfg')
        self.reset()
        h_read       = sh.ReadTextFile(self.path,Silent=self.Silent)
        self.text    = h_read.get()
        self.Success = h_read.Success
        self._default()
        if os.path.exists(self.path):
            self.open()
        else:
            self.Success = False
        self.check()
        self.load()
        self.additional_keys()

    def _default(self):
        sh.globs['bool'].update ({
            'AutoCloseSpecSymbol':False
           ,'SelectTermsOnly'    :True
           ,'Iconify'            :True
                                })
        #---------------------------------------------------
        sh.globs['int'].update ({
            'col_width'         :250
           ,'font_comments_size':3
           ,'font_dics_size'    :4
           ,'font_speech_size'  :4
           ,'font_terms_size'   :4
                               })
        #---------------------------------------------------
        sh.globs['var'].update ({
            'bind_clear_history'          :'<Control-Shift-Delete>'
           ,'bind_clear_search_field'     :'<ButtonRelease-3>'
           ,'bind_copy_article_url'       :'<Shift-F7>'
           ,'bind_copy_history'           :'<ButtonRelease-3>'
           ,'bind_copy_sel_alt'           :'<Control-KP_Enter>'
           ,'bind_copy_sel_alt2'          :'<ButtonRelease-3>'
           ,'bind_copy_sel'               :'<Control-Return>'
           ,'bind_copy_url'               :'<Control-F7>'
           ,'bind_define'                 :'<Control-d>'
           ,'bind_go_back'                :'<Alt-Left>'
           ,'bind_go_forward'             :'<Alt-Right>'
           ,'bind_next_pair'              :'<F8>'
           ,'bind_next_pair_alt'          :'<Control-l>'
           ,'bind_prev_pair'              :'<Shift-F8>'
           ,'bind_prev_pair_alt'          :'<Control-L>'
           ,'bind_open_in_browser_alt'    :'<Control-b>'
           ,'bind_open_in_browser'        :'<F7>'
           ,'bind_paste_search_field'     :'<ButtonRelease-2>'
           ,'bind_print'                  :'<Control-p>'
           ,'bind_quit_now_alt'           :'<F10>'
           ,'bind_quit_now'               :'<Control-q>'
           ,'bind_re_search_article'      :'<Control-F3>'
           ,'bind_reload_article_alt'     :'<Control-r>'
           ,'bind_reload_article'         :'<F5>'
           ,'bind_save_article_alt'       :'<Control-s>'
           ,'bind_save_article'           :'<F2>'
           ,'bind_search_article_backward':'<Shift-F3>'
           ,'bind_search_article_forward' :'<F3>'
           ,'bind_settings'               :'<Alt-s>'
           ,'bind_settings_alt'           :'<F12>'
           ,'bind_show_about'             :'<F1>'
           ,'bind_spec_symbol'            :'<Control-e>'
           ,'bind_toggle_alphabet'        :'<Alt-a>'
           ,'bind_toggle_block'           :'<Alt-b>'
           ,'bind_toggle_history_alt'     :'<Control-h>'
           ,'bind_toggle_history'         :'<F4>'
           ,'bind_toggle_priority'        :'<Alt-p>'
           ,'bind_toggle_view'            :'<F6>'
           ,'bind_toggle_view_alt'        :'<Alt-v>'
           ,'color_comments'              :'gray'
           ,'color_dics'                  :'cadet blue'
           ,'color_speech'                :'red'
           ,'color_terms_sel_bg'          :'cyan'
           ,'color_terms_sel_fg'          :'black'
           ,'color_terms'                 :'black'
           ,'font_comments_family'        :'Mono'
           ,'font_dics_family'            :'Arial'
           ,'font_history'                :'Sans 12'
           ,'font_speech_family'          :'Arial'
           ,'font_style'                  :'Sans 14'
           ,'font_terms_sel'              :'Sans 14 bold italic'
           ,'font_terms_family'           :'Serif'
           ,'pair_afr_rus'                :'l1=31&l2=2&s=%s'
           ,'pair_deu_rus'                :'l1=3&l2=2&s=%s'
           ,'pair_eng_deu'                :'l1=1&l2=3&s=%s'
           ,'pair_eng_est'                :'l1=1&l2=26&s=%s'
           ,'pair_eng_rus'                :'CL=1&s=%s'
           ,'pair_epo_rus'                :'l1=34&l2=2&s=%s'
           ,'pair_est_rus'                :'l1=26&l2=2&s=%s'
           ,'pair_fra_rus'                :'l1=4&l2=2&s=%s'
           ,'pair_ita_rus'                :'l1=23&l2=2&s=%s'
           ,'pair_lav_rus'                :'l1=27&l2=2&s=%s'
           ,'pair_nld_rus'                :'l1=24&l2=2&s=%s'
           ,'pair_root'                   :'https://www.multitran.ru/c/M.exe?'
           ,'pair_rus_xal'                :'l1=2&l2=35&s=%s'
           ,'pair_spa_rus'                :'l1=5&l2=2&s=%s'
           ,'pair_xal_rus'                :'l1=35&l2=2&s=%s'
           ,'repeat_sign'                 :'!'
           ,'repeat_sign2'                :'!!'
           ,'spec_syms'                   :'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ'
           ,'web_search_url'              :'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s'
           ,'win_encoding'                :'windows-1251'
                               })

    def reset(self):
        sh.globs['bool']  = {}
        sh.globs['float'] = {}
        sh.globs['int']   = {}
        sh.globs['var']   = {}

    def additional_keys(self):
        sh.globs['var'].update ({
            'icon_alphabet_off'       :'icon_36x36_alphabet_off.gif'
           ,'icon_alphabet_on'        :'icon_36x36_alphabet_on.gif'
           ,'icon_block_off'          :'icon_36x36_block_off.gif'
           ,'icon_block_on'           :'icon_36x36_block_on.gif'
           ,'icon_clear_search_field' :'icon_36x36_clear_search_field.gif'
           ,'icon_define'             :'icon_36x36_define.gif'
           ,'icon_go_back_off'        :'icon_36x36_go_back_off.gif'
           ,'icon_go_back'            :'icon_36x36_go_back.gif'
           ,'icon_go_forward_off'     :'icon_36x36_go_forward_off.gif'
           ,'icon_go_forward'         :'icon_36x36_go_forward.gif'
           ,'icon_go_search'          :'icon_36x36_go_search.gif'
           ,'icon_mclient'            :'icon_64x64_mclient.gif'
           ,'icon_open_in_browser'    :'icon_36x36_open_in_browser.gif'
           ,'icon_paste'              :'icon_36x36_paste.gif'
           ,'icon_print'              :'icon_36x36_print.gif'
           ,'icon_priority_off'       :'icon_36x36_priority_off.gif'
           ,'icon_priority_on'        :'icon_36x36_priority_on.gif'
           ,'icon_quit_now'           :'icon_36x36_quit_now.gif'
           ,'icon_reload'             :'icon_36x36_reload.gif'
           ,'icon_repeat_sign_off'    :'icon_36x36_repeat_sign_off.gif'
           ,'icon_repeat_sign'        :'icon_36x36_repeat_sign.gif'
           ,'icon_repeat_sign2_off'   :'icon_36x36_repeat_sign2_off.gif'
           ,'icon_repeat_sign2'       :'icon_36x36_repeat_sign2.gif'
           ,'icon_save_article'       :'icon_36x36_save_article.gif'
           ,'icon_search_article'     :'icon_36x36_search_article.gif'
           ,'icon_settings'           :'icon_36x36_settings.gif'
           ,'icon_show_about'         :'icon_36x36_show_about.gif'
           ,'icon_spec_symbol'        :'icon_36x36_spec_symbol.gif'
           ,'icon_toggle_history'     :'icon_36x36_toggle_history.gif'
           ,'icon_toggle_view_hor'    :'icon_36x36_toggle_view_hor.gif'
           ,'icon_toggle_view_ver'    :'icon_36x36_toggle_view_ver.gif'
           ,'icon_watch_clipboard_off':'icon_36x36_watch_clipboard_off.gif'
           ,'icon_watch_clipboard_on' :'icon_36x36_watch_clipboard_on.gif'
                               })
        for key in sh.globs['var']:
            if sh.globs['var'][key].endswith('.gif'):
                old_val = sh.globs['var'][key]
                sh.globs['var'][key] = sh.objs.pdir().add('resources',sh.globs['var'][key])
                sh.log.append ('ConfigMclient.additional_keys'
                              ,_('DEBUG')
                              ,'%s -> %s' % (old_val,sh.globs['var'][key])
                              )



ConfigMclient()


if __name__ == '__main__':
    if sh.oss.win():
        import kl_mod_win as kl_mod
        import pythoncom
    else:
        import kl_mod_lin as kl_mod

sh.globs['_tkhtml_loaded'] = False
sh.globs['geom_top'] = {}
sh.globs['top'] = {}

online_url_safe = sh.globs['var']['pair_root'] + 'l1=2&l2=1&s=%ED%E5%E2%E5%F0%ED%E0%FF+%F1%F1%FB%EB%EA%E0' # 'неверная ссылка'
sep_words_found = 'найдены отдельные слова'

pairs = ('ENG <=> RUS'
        ,'DEU <=> RUS'
        ,'SPA <=> RUS'
        ,'FRA <=> RUS'
        ,'NLD <=> RUS'
        ,'ITA <=> RUS'
        ,'LAV <=> RUS'
        ,'EST <=> RUS'
        ,'AFR <=> RUS'
        ,'EPO <=> RUS'
        ,'RUS <=> XAL'
        ,'XAL <=> RUS'
        ,'ENG <=> DEU'
        ,'ENG <=> EST'
        )

online_dic_urls = (sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_rus']   # ENG <=> RUS, 'CL=1&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_deu_rus']   # DEU <=> RUS, 'l1=3&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_spa_rus']   # SPA <=> RUS, 'l1=5&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_fra_rus']   # FRA <=> RUS, 'l1=4&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_nld_rus']   # NLD <=> RUS, 'l1=24&l2=2&s=%s',
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_ita_rus']   # ITA <=> RUS, 'l1=23&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_lav_rus']   # LAV <=> RUS, 'l1=27&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_est_rus']   # EST <=> RUS, 'l1=26&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_afr_rus']   # AFR <=> RUS, 'l1=31&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_epo_rus']   # EPO <=> RUS, 'l1=34&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_rus_xal']   # RUS <=> XAL, 'l1=2&l2=35&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_xal_rus']   # XAL <=> RUS, 'l1=35&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_deu']   # ENG <=> DEU, 'l1=1&l2=3&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_est']   # ENG <=> EST, 'l1=1&l2=26&s=%s'
                  )

langs = ('English'   # ENG <=> RUS
        ,'German'    # DEU <=> RUS
        ,'Spanish'   # SPA <=> RUS
        ,'French'    # FRA <=> RUS
        ,'Dutch'     # NLD <=> RUS
        ,'Italian'   # ITA <=> RUS
        ,'Latvian'   # LAV <=> RUS
        ,'Estonian'  # EST <=> RUS
        ,'Afrikaans' # AFR <=> RUS
        ,'Esperanto' # EPO <=> RUS
        ,'Kazakh'    # RUS <=> XAL
        ,'Kazakh'    # XAL <=> RUS
        ,'German'    # ENG <=> DEU
        ,'Estonian'  # ENG <=> EST
        )

sources = (_('All'),_('Online'),_('Offline'))



class Objects:

    def __init__(self):
        self._top = self._entry = self._textbox = self._online_mt = self._online_other = self._about = self._blacklist = self._prioritize = self._parties = self._request = self._ext_dics = self._webframe = self._blocks_db = self._moves = None

    def blocks_db(self):
        if not self._blocks_db:
            self._blocks_db = db.Moves()
            self._blocks_db.Selectable = sh.globs['bool']['SelectTermsOnly']
        return self._blocks_db

    def webframe(self):
        if not self._webframe:
            self._webframe = WebFrame()
        return self._webframe

    def ext_dics(self):
        if not self._ext_dics:
            self._ext_dics = pg.ExtDics(path=sh.objs.pdir().add('dics'))
        return self._ext_dics

    def request(self):
        if not self._request:
            self._request = CurRequest()
        return self._request

    def parties(self):
        if not self._parties:
            top = sg.objs.new_top(Maximize=0)
            sg.Geometry(parent_obj=top).set('800x600')
            self._parties = sg.TextBox(parent_obj=top)
            self._parties.icon(sh.globs['var']['icon_mclient'])
            self._parties.title(text=_('Third parties')+':')
            self._parties.insert(text=third_parties,MoveTop=1)
            self._parties.read_only()
        return self._parties

    def entry(self):
        if not self._entry:
            self._entry = sg.Entry(parent_obj=sg.Top(sg.objs.root()))
            self._entry.icon(sh.globs['var']['icon_mclient'])
            self._entry.title(_('Enter a string to search:'))
        return self._entry

    def textbox(self):
        if not self._textbox:
            h_top = sg.Top(sg.objs.root())
            self._textbox = sg.TextBox(parent_obj=h_top)
            sg.Geometry(parent_obj=h_top).set('500x400')
            self._textbox.icon(sh.globs['var']['icon_mclient'])
        return self._textbox

    def online_mt(self):
        if not self._online_mt:
            self._online_mt = sh.Online(MTSpecific=True)
        return self._online_mt

    def online_other(self):
        if not self._online_other:
            self._online_other = sh.Online(MTSpecific=False)
        return self._online_other

    def online(self):
        # todo: create a sub-source
        if objs.request()._source == _('All') or objs.request()._source == _('Online'):
            return self.online_mt()
        else:
            return self.online_other()

    def about(self):
        if not self._about:
            self._about = About()
        return self._about

    def blacklist(self):
        if self._blacklist is None: # Allow empty lists
            self._blacklist = Lists().blacklist()
        return self._blacklist

    def prioritize(self):
        if self._prioritize is None: # Allow empty lists
            self._prioritize = Lists().prioritize()
        return self._prioritize



class CurRequest:

    def __init__(self):
        self.reset()

    def reset(self):
        # note: this should be synchronized with the 'default' value of objs.webframe().menu_columns
        self._collimit     = 8
        self._source       = _('All')
        self._lang         = 'English'
        self._cols         = ('dic','wform','transc','speech')
        # Toggling blacklisting should not depend on a number of blocked dictionaries (otherwise, it is not clear how blacklisting should be toggled)
        self.Block         = True
        self.Prioritize    = True
        self.SortRows      = True
        self.SortTerms     = True
        # *Temporary* turn off prioritizing and terms sorting for articles with 'sep_words_found' and in phrases; use previous settings for new articles
        self.SpecialPage   = False
        self.MouseClicked  = False
        self.CaptureHotkey = True
        self.Reverse       = False
        self._page         = ''
        self._html         = ''
        self._html_raw     = ''
        self._search       = ''
        self._url          = ''




def call_app():
    # Использовать то же сочетание клавиш для вызова окна
    sg.Geometry(parent_obj=objs.webframe().obj).activate(MouseClicked=objs.request().MouseClicked)
    # todo: check if this is still the problem
    # In case of .focus_set() *first* Control-c-c can call an inactive widget
    objs.webframe().search_field.widget.focus_force()

# Перехватить нажатие Control-c-c
def timed_update():
    objs.request().MouseClicked = False
    check = kl_mod.keylistener.check()
    if check:
        if check == 1 and objs._request.CaptureHotkey:
            # Позволяет предотвратить зависание потока в версиях Windows старше XP
            if sh.oss.win():
                kl_mod.keylistener.cancel()
                kl_mod.keylistener.restart()
            objs._request.MouseClicked = True
            new_clipboard = sg.Clipboard().paste()
            if new_clipboard:
                objs._request._search = new_clipboard
                objs.webframe().go_search()
        if check == 2 or objs._request.CaptureHotkey:
            call_app()
    sg.objs.root().widget.after(300,timed_update)



class About:

    def __init__(self):
        self.Active = False
        self.type   = 'About'
        self.obj    = sg.Top(sg.objs.root())
        self.widget = self.obj.widget
        self.obj.icon (sh.globs['var']['icon_mclient'])
        self.obj.title(_('About'))
        frame1 = sg.Frame (parent_obj = self
                          ,expand     = 1
                          ,fill       = 'both'
                          ,side       = 'top'
                          )
        frame2 = sg.Frame (parent_obj = self
                          ,expand     = 1
                          ,fill       = 'both'
                          ,side       = 'left'
                          )
        frame3 = sg.Frame (parent_obj = self
                          ,expand     = 1
                          ,fill       = 'both'
                          ,side       = 'right'
                          )
        label  = sg.Label (parent_obj = frame1
                          ,text       = _('Programming: Peter Sklyar, 2015, 2016.\nVersion: %s\n\nThis program is free and opensource. You can use and modify it freely\nwithin the scope of the provisions set forth in GPL v.3 and the active legislation.\n\nIf you have any questions, requests, etc., please do not hesitate to contact me.\n') % version
                          ,font       = sh.globs['var']['font_style']
                          )
        # Лицензия
        sg.Button (parent_obj = frame2
                  ,text       = _('Third parties')
                  ,hint       = _('View the license')
                  ,action     = self.show_third_parties
                  ,side       = 'left'
                  )
        sg.Button (parent_obj = frame3
                  ,text       = _('License')
                  ,hint       = _('View the license')
                  ,action     = self.open_license_url
                  ,side       = 'left'
                  )
        # Отправить письмо автору
        sg.Button (parent_obj = frame3
                  ,text       = _('Send email to the author')
                  ,hint       = _('Send email to the author')
                  ,action     = self.response_back
                  ,side       = 'right'
                  )
        self.widget.focus_set()
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_show_about']
                ,action   = self.toggle
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = self.close
                )
        self.close()

    def close(self,*args):
        self.obj.close()
        self.Active = False

    def show(self,*args):
        self.obj.show()
        self.Active = True

    def toggle(self,*args):
        if self.Active:
            self.close()
        else:
            self.show()

    # Написать письмо автору
    def response_back(self,*args):
        sh.Email (email   = sh.email
                 ,subject = _('Concerning %s') % product
                 ).create()

    # Открыть веб-страницу с лицензией
    def open_license_url(self,*args):
        objs.online()._url = sh.globs['license_url']
        objs.online().browse()

    # Отобразить информацию о лицензии третьих сторон
    def show_third_parties(self,*args):
        objs.parties().show()



class SaveArticle:

    def __init__(self):
        self.type       = 'SaveArticle'
        self.parent_obj = sg.Top(sg.objs.root())
        self.obj        = sg.ListBox (
                    parent_obj = self.parent_obj
                   ,Multiple   = False
                   ,lst        = [_('Save the current view as a web-page (*.htm)')
                                 ,_('Save the original article as a web-page (*.htm)')
                                 ,_('Save the article as plain text in UTF-8 (*.txt)')
                                 ,_('Copy HTML code of the article to clipboard')
                                 ,_('Copy the text of the article to clipboard')
                                 ]
                   ,title      = _('Select an action:')
                   ,icon       = sh.globs['var']['icon_mclient']
                                     )
        self.widget = self.obj.widget
        # Use this instead of 'close' because there is no selection yet
        self.obj.interrupt()
        self.file = ''

    def close(self,*args):
        self.obj.close()

    def show(self,*args):
        self.obj.show()

    # Fix an extension for Windows
    def fix_ext(self,ext='.htm'):
        if not self.file.endswith(ext):
            self.file += ext

    def select(self,*args):
        self.show()
        opt = self.obj._get
        if opt:
            if opt == _('Save the current view as a web-page (*.htm)'):
                self.view_as_html()
            elif opt == _('Save the original article as a web-page (*.htm)'):
                self.raw_as_html()
            elif opt == _('Save the article as plain text in UTF-8 (*.txt)'):
                self.view_as_txt()
            elif opt == _('Copy HTML code of the article to clipboard'):
                self.copy_raw()
            elif opt == _('Copy the text of the article to clipboard'):
                self.copy_txt()

    def view_as_html(self):
        self.file = sg.dialog_save_file (
                    filetypes = ((_('Web-page'),'.htm')
                                ,(_('Web-page'),'.html')
                                ,(_('All files'),'*')
                                )
                                        )
        if self.file and objs.request()._html:
            self.fix_ext(ext='.htm')
            # We disable AskRewrite because the confirmation is already built in the internal dialog
            sh.WriteTextFile(self.file,AskRewrite=False).write(objs._request._html)
        else:
            sh.log.append ('SaveArticle.view_as_html'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def raw_as_html(self):
        # Ключ 'html' может быть необходим для записи файла, которая производится в кодировке UTF-8, поэтому, чтобы полученная веб-страница нормально читалась, меняем кодировку вручную.
        # Также меняем сокращенные гиперссылки на полные, чтобы они работали и в локальном файле.
        self.file = sg.dialog_save_file (
                    filetypes = ((_('Web-page'),'.htm')
                                ,(_('Web-page'),'.html')
                                ,(_('All files'),'*')
                                )
                                        )
        if self.file and objs.request()._html_raw:
            self.fix_ext(ext='.htm')
            # todo: fix remaining links to localhost
            sh.WriteTextFile(self.file,AskRewrite=False).write(objs._request._html_raw.replace('charset=windows-1251"','charset=utf-8"').replace('<a href="M.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/M.exe?',sh.globs['var']['pair_root']).replace('<a href="m.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/m.exe?',sh.globs['var']['pair_root']))
        else:
            sh.log.append ('SaveArticle.raw_as_html'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def view_as_txt(self):
        self.file = sg.dialog_save_file (
                    filetypes = ((_('Plain text (UTF-8)'),'.txt')
                                ,(_('All files'),'*')
                                )
                                        )
        text = objs.webframe().text()
        if self.file and text:
            self.fix_ext(ext='.txt')
            sh.WriteTextFile(self.file,AskRewrite=False).write(text.strip())
        else:
            sh.log.append ('SaveArticle.view_as_txt'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def copy_raw(self):
        sg.Clipboard().copy(objs.request()._html_raw)

    def copy_txt(self):
        text = objs.webframe().text()
        if text:
            sg.Clipboard().copy(text.strip())
        else:
            sh.log.append ('SaveArticle.copy_txt'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )



# Search IN an article
class SearchArticle:

    def __init__(self):
        self.type   = 'SearchArticle'
        self.obj    = objs.entry()
        self.obj.title(_('Enter a string to search:'))
        self.widget = self.obj.widget
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_search_article_forward']
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = self.close
                )
        self.obj.select_all()
        self.obj.focus()
        self.close()
        self.reset()

    def reset(self,*args):
        self._pos    = -1
        self._first  = -1
        self._last   = -1
        self._search = ''
        # Plus: keeping old input
        # Minus: searching old input after cancelling the search and searching again
        #self.clear()

    def clear(self,*args):
        self.obj.clear_text()

    def close(self,*args):
        self.obj.close()

    def show(self,*args):
        self.obj.show()
        self.obj.select_all()

    def search(self):
        if not self._search:
            self.show()
            self._search = self.widget.get().strip(' ').strip('\n').lower()
        return self._search

    def forward(self,*args):
        pos = objs.blocks_db().search_forward(pos=self._pos,search=self.search())
        if pos or pos == 0:
            objs.webframe()._pos = self._pos = pos
            objs._webframe.key_move()
        elif self._pos < 0:
            sg.Message (func    = 'SearchArticle.forward'
                       ,level   = _('INFO')
                       ,message = _('Nothing has been found!')
                       )
        else:
            sg.Message (func    = 'SearchArticle.forward'
                       ,level   = _('INFO')
                       ,message = _('The start has been reached. Searching from the end.')
                       )
            self._pos = 0
            self.forward()

    def first(self):
        if self._first == -1:
            self._first = objs.blocks_db().search_forward(pos=-1,search=self.search())
        return self._first

    def last(self):
        if self._last == -1:
            max_cell = objs._blocks_db.max_cell()
            if max_cell:
                self._last = objs.blocks_db().search_backward(pos=max_cell[2]+1,search=self.search())
            else:
                sh.log.append ('SearchArticle.last'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._last

    def backward(self,*args):
        if self.first():
            print('first:',self._first) # todo: del
            print('last:',self.last()) # todo: del
            print('_pos:',self._pos) # todo: del
            if self._pos == self._first:
                sg.Message (func    = 'SearchArticle.backward'
                           ,level   = _('INFO')
                           ,message = _('The end has been reached. Searching from the start.')
                           )
                objs.webframe()._pos = self._pos = self.last()
                objs._webframe.key_move()
            else:
                pos = objs.blocks_db().search_backward(pos=self._pos,search=self.search())
                if pos or pos == 0:
                    self._pos = pos
                    objs.webframe()._pos = pos
                    objs._webframe.key_move()
        else:
            sg.Message (func    = 'SearchArticle.backward'
                       ,level   = _('INFO')
                       ,message = _('Nothing has been found!')
                       )



# Search FOR an article
class SearchField:

    def __init__(self,parent_obj,side='left',ipady=5):
        self.type       = 'SearchField'
        self.parent_obj = parent_obj
        # Поле ввода поисковой строки
        self.obj        = sg.Entry (parent_obj = self.parent_obj
                                   ,Composite  = True
                                   ,side       = side
                                   ,ipady      = ipady
                                   )
        self.widget = self.obj.widget

    def clear(self,*args):
        self.obj.clear_text()

    # Очистить строку поиска и вставить в нее заданный текст или содержимое буфера обмена
    def paste(self,event=None,text=None):
        self.clear()
        if text:
            self.widget.insert(0,text)
        else:
            self.widget.insert(0,sg.Clipboard().paste())
        return 'break'

    # Вставить текущий запрос
    def insert_repeat_sign(self,*args):
        sg.Clipboard().copy(str(objs.request()._search))
        self.paste()

    # Вставить предыдущий запрос
    def insert_repeat_sign2(self,*args):
        sg.Clipboard().copy(objs.blocks_db().prev_search())
        self.paste()



class SpecSymbols:

    def __init__(self):
        self.obj    = sg.Top(sg.objs.root())
        self.widget = self.obj.widget
        self.obj.icon (sh.globs['var']['icon_mclient'])
        self.obj.title(_('Paste a special symbol'))
        self.frame  = sg.Frame(self.obj,expand=1)
        for i in range(len(sh.globs['var']['spec_syms'])):
            if i % 10 == 0:
                self.frame = sg.Frame(self.obj,expand=1)
            # lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
            # width и height нужны для Windows
            self.button = tk.Button (
                    self.frame.widget
                   ,text    = sh.globs['var']['spec_syms'][i]
                   ,command = lambda i=i:objs.webframe().insert_sym(sh.globs['var']['spec_syms'][i])
                   ,width   = 2
                   ,height  = 2).pack(side='left',expand=1
                                    )
        self.bindings()
        self.close()

    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = ['<Escape>',sh.globs['var']['bind_spec_symbol']]
                ,action   = self.close
                )

    def show(self,*args):
        self.obj.show()

    def close(self,*args):
        self.obj.close()



class History:

    def __init__(self):
        self._title = _('History')
        self._icon  = sh.globs['var']['icon_mclient']
        self.Active = False
        self.gui()

    def gui(self):
        self.parent_obj = sg.Top(sg.objs.root())
        self.parent_obj.widget.geometry('250x350')
        self.obj = sg.ListBox (parent_obj      = self.parent_obj
                              ,title           = self._title
                              ,icon            = self._icon
                              ,SelectionCloses = False
                              ,SingleClick     = False
                              ,Composite       = True
                              ,user_function   = self.go
                              )
        self.widget = self.obj.widget
        self.bindings()
        self.close()

    def bindings(self):
        sg.bind (obj      = self.parent_obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ,'<Escape>'
                            ]
                ,action = self.toggle
                )
        sg.bind (obj      = self
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.copy
                )
        sg.bind (obj      = self.parent_obj
                ,bindings = sh.globs['var']['bind_clear_history']
                ,action   = self.clear
                )

    def autoselect(self):
        self.obj.clear_selection()
        if objs.request()._search in self.obj.lst:
            self.obj.set(item=objs._request._search)

    def show(self,*args):
        self.Active = True
        self.parent_obj.show()

    def close(self,*args):
        self.Active = False
        self.parent_obj.close()

    def fill(self):
        self.obj.reset(lst=objs.blocks_db().searches(),title=self._title)

    def update(self):
        self.fill()
        self.autoselect()

    def clear(self,*args):
        objs.blocks_db().clear()
        self.obj.clear()
        objs.webframe().reset()
        objs._webframe.search_article.obj.clear_text()
        objs.request().reset()

    def toggle(self,*args):
        if self.Active:
            self.close()
        else:
            self.show()

    def go(self,*args):
        objs.request()._search = self.obj.get()
        # Do not warn after clearing the widget
        if objs._request._search:
            objs.blocks_db().request (source = objs._request._source
                                     ,search = objs._request._search
                                     )
            objs._request._url = objs._blocks_db.urla()
            objs.webframe().load_article()

    # Скопировать элемент истории
    def copy(self,*args):
        sg.Clipboard().copy(self.obj.get())



class WebFrame:

    def __init__(self):
        self.values()
        self.widgets()
        self.gui()

    def reset(self):
        #'widget.reset' is already done in 'self.fill'
        welcome = pg.Welcome(url       = sh.globs['var']['pair_root']
                            ,st_status = len(objs.ext_dics()._dics)
                            ,product   = product
                            ,version   = version
                            )
        self.fill(welcome.run())
        self.update_buttons()
        self.title()

    def values(self):
        self._pos      = -1
        self.direction = 'right'
        self._row_no   = 0

    def gui(self):
        self.obj     = sg.objs.new_top(Maximize=1)
        self.frame   = sg.Frame (parent_obj = self.obj)
        self.bottom  = sg.Frame (parent_obj = self.frame
                                ,expand     = 0
                                ,side       = 'bottom'
                                )
        self.frame_y = sg.Frame (parent_obj = self.frame
                                ,expand     = 0
                                ,fill       = 'y'
                                ,side       = 'right'
                                )
        self.widget  = th.TkinterHtml(self.frame.widget)
        self.widget.pack(expand='1',fill='both')
        self.scrollbars ()
        self.frame_panel()
        self.icon       ()
        self.title      ()
        self.bindings   ()
        self.search_field.widget.focus_set()
        self.obj.widget.protocol("WM_DELETE_WINDOW",self.close)

    def widgets(self):
        self.search_article = SearchArticle ()
        self.spec_symbols   = SpecSymbols   ()
        self.save_article   = SaveArticle   ()
        self.history        = History       ()
        self.settings       = Settings      ()

    def frame_panel(self):
        self._panel = sg.Frame (parent_obj = self.bottom
                               ,expand     = 0
                               ,fill       = 'x'
                               ,side       = 'bottom'
                               )
        # Поле ввода поисковой строки
        self.search_field = SearchField(parent_obj=self._panel)
        self.draw_buttons()

    # Create buttons
    # Bindings are indicated here only to set hints. In order to set bindings, use 'self.bindings'.
    def draw_buttons(self):
        # Кнопка для "чайников", заменяет Enter в search_field
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Translate')
                  ,hint                = _('Translate')
                  ,action              = self.go
                  ,inactive_image_path = sh.globs['var']['icon_go_search']
                  ,active_image_path   = sh.globs['var']['icon_go_search']
                  ,bindings            = ['<Return>'
                                         ,'<KP_Enter>'
                                         ]
                  ) # В данном случае btn = hint

        # Кнопка очистки строки поиска
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Clear')
                  ,hint                = _('Clear search field')
                  ,action              = self.search_field.clear
                  ,inactive_image_path = sh.globs['var']['icon_clear_search_field']
                  ,active_image_path   = sh.globs['var']['icon_clear_search_field']
                  ,bindings            = sh.globs['var']['bind_clear_search_field']
                  )

        # Кнопка вставки
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Paste')
                  ,hint                = _('Paste text from clipboard')
                  ,action              = self.search_field.paste
                  ,inactive_image_path = sh.globs['var']['icon_paste']
                  ,active_image_path   = sh.globs['var']['icon_paste']
                  ,bindings            = ['<Control-v>']
                  )
        # Кнопка вставки текущего запроса
        self.btn_repeat_sign = sg.Button (
                   parent_obj          = self._panel
                  ,text                = '!'
                  ,hint                = _('Paste current request')
                  ,action              = self.search_field.insert_repeat_sign
                  ,inactive_image_path = sh.globs['var']['icon_repeat_sign_off']
                  ,active_image_path   = sh.globs['var']['icon_repeat_sign']
                  ,bindings            = sh.globs['var']['repeat_sign']
                                         )
        # Кнопка вставки предыдущего запроса
        self.btn_repeat_sign2 = sg.Button (
                   parent_obj          = self._panel
                  ,text                = '!!'
                  ,hint                = _('Paste previous request')
                  ,action              = self.search_field.insert_repeat_sign2
                  ,inactive_image_path = sh.globs['var']['icon_repeat_sign2_off']
                  ,active_image_path   = sh.globs['var']['icon_repeat_sign2']
                  ,bindings            = sh.globs['var']['repeat_sign2']
                                          )
        # Кнопка для вставки спец. символов
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Symbols')
                  ,hint                = _('Paste a special symbol')
                  ,action              = self.spec_symbols.show
                  ,inactive_image_path = sh.globs['var']['icon_spec_symbol']
                  ,active_image_path   = sh.globs['var']['icon_spec_symbol']
                  ,bindings            = sh.globs['var']['bind_spec_symbol']
                  )
        self.menu_sources = sg.OptionMenu (parent_obj = self._panel
                                          ,items      = sources
                                          ,command    = self.set_source
                                          )
        # Выпадающий список с вариантами направлений перевода
        self.menu_pairs = sg.OptionMenu (parent_obj = self._panel
                                        ,items      = pairs
                                        ,command    = self.set_lang
                                        )
        self.menu_columns = sg.OptionMenu (parent_obj = self._panel
                                          ,items      = (1,2,3,4,5,6,7,8,9,10)
                                          ,command    = self.set_columns
                                          ,default    = 4
                                          )
        # Кнопка настроек
        self.btn_settings = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Settings')
                  ,hint                = _('Tune up view settings')
                  ,action              = self.settings.show
                  ,inactive_image_path = sh.globs['var']['icon_settings']
                  ,active_image_path   = sh.globs['var']['icon_settings']
                  ,bindings            = [sh.globs['var']['bind_settings']
                                         ,sh.globs['var']['bind_settings_alt']
                                         ]
                                      )
        # Кнопка изменения вида статьи
        self.btn_toggle_view = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Toggle view')
                  ,hint                = _('Toggle the article view mode')
                  ,action              = self.toggle_view
                  ,inactive_image_path = sh.globs['var']['icon_toggle_view_ver']
                  ,active_image_path   = sh.globs['var']['icon_toggle_view_hor']
                  ,bindings            = [sh.globs['var']['bind_toggle_view']
                                         ,sh.globs['var']['bind_toggle_view_alt']
                                         ]
                                         )
        # Кнопка включения/отключения режима блокировки словарей
        self.btn_toggle_block = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Blacklist')
                  ,hint                = _('Toggle the blacklist')
                  ,action              = self.toggle_block
                  ,inactive_image_path = sh.globs['var']['icon_block_off']
                  ,active_image_path   = sh.globs['var']['icon_block_on']
                  ,bindings            = sh.globs['var']['bind_toggle_block']
                                          )
        # Кнопка включения/отключения режима приоритезации словарей
        self.btn_toggle_priority = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Prioritize')
                  ,hint                = _('Toggle prioritizing')
                  ,action              = self.toggle_priority
                  ,inactive_image_path = sh.globs['var']['icon_priority_off']
                  ,active_image_path   = sh.globs['var']['icon_priority_on']
                  ,bindings            = sh.globs['var']['bind_toggle_priority']
                                             )
        # Кнопка включения/отключения сортировки словарей по алфавиту
        self.btn_toggle_alphabet = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Alphabetize')
                  ,hint                = _('Toggle alphabetizing')
                  ,action              = self.toggle_alphabet
                  ,inactive_image_path = sh.globs['var']['icon_alphabet_off']
                  ,active_image_path   = sh.globs['var']['icon_alphabet_on']
                  ,bindings            = sh.globs['var']['bind_toggle_alphabet']
                                             )
        # Кнопка перехода на предыдущую статью
        self.btn_prev = sg.Button (
                   parent_obj          = self._panel
                  ,text                = '←'
                  ,hint                = _('Go to the preceding article')
                  ,action              = self.go_back
                  ,inactive_image_path = sh.globs['var']['icon_go_back_off']
                  ,active_image_path   = sh.globs['var']['icon_go_back']
                  ,bindings            = sh.globs['var']['bind_go_back']
                                  )
        # Кнопка перехода на следующую статью
        self.btn_next = sg.Button (
                   parent_obj          = self._panel
                  ,text                = '→'
                  ,hint                = _('Go to the following article')
                  ,action              = self.go_forward
                  ,inactive_image_path = sh.globs['var']['icon_go_forward_off']
                  ,active_image_path   = sh.globs['var']['icon_go_forward']
                  ,bindings            = sh.globs['var']['bind_go_forward']
                                  )
        # Кнопка включения/отключения и очистки истории
        # todo: fix: do not iconify on RMB (separate button frame from main frame)
        # We may hardcore the hotkey to clear the history because this hotkey is bound to the button
        hint_history = _('Show history')                                      \
                    + '\n'   + sh.globs['var']['bind_toggle_history']         \
                    + ', '   + sh.globs['var']['bind_toggle_history_alt']     \
                    + '\n\n' + _('Clear history')                             \
                    + '\n'   + sh.globs['var']['bind_clear_history']          \
                    + ', <ButtonRelease-3>'
        self.btn_history = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('History')
                  ,hint                = hint_history
                  ,action              = self.history.toggle
                  ,inactive_image_path = sh.globs['var']['icon_toggle_history']
                  ,active_image_path   = sh.globs['var']['icon_toggle_history']
                  ,hint_height         = 80
                                     )
        # Кнопка перезагрузки статьи
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Reload')
                  ,hint                = _('Reload the article')
                  ,action              = self.reload
                  ,inactive_image_path = sh.globs['var']['icon_reload']
                  ,active_image_path   = sh.globs['var']['icon_reload']
                  ,bindings            = [sh.globs['var']['bind_reload_article']
                                         ,sh.globs['var']['bind_reload_article_alt']
                                         ]
                  )
        # Кнопка "Поиск в статье"
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Search')
                  ,hint                = _('Find in the current article')
                  ,action              = self.search_reset
                  ,inactive_image_path = sh.globs['var']['icon_search_article']
                  ,active_image_path   = sh.globs['var']['icon_search_article']
                  ,bindings            = sh.globs['var']['bind_re_search_article']
                  )
        # Кнопка "Сохранить"
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Save')
                  ,hint                = _('Save the current article')
                  ,action              = self.save_article.select
                  ,inactive_image_path = sh.globs['var']['icon_save_article']
                  ,active_image_path   = sh.globs['var']['icon_save_article']
                  ,bindings            = [sh.globs['var']['bind_save_article']
                                         ,sh.globs['var']['bind_save_article_alt']
                                         ]
                  )
        # Кнопка "Открыть в браузере"
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Browse')
                  ,hint                = _('Open the current article in a browser')
                  ,action              = self.open_in_browser
                  ,inactive_image_path = sh.globs['var']['icon_open_in_browser']
                  ,active_image_path   = sh.globs['var']['icon_open_in_browser']
                  ,bindings            = [sh.globs['var']['bind_open_in_browser']
                                         ,sh.globs['var']['bind_open_in_browser_alt']
                                         ]
                  )
        # Кнопка "Печать"
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Print')
                  ,hint                = _('Create a print-ready preview')
                  ,action              = self.print
                  ,inactive_image_path = sh.globs['var']['icon_print']
                  ,active_image_path   = sh.globs['var']['icon_print']
                  ,bindings            = sh.globs['var']['bind_print']
                  )
        # Кнопка толкования термина
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Define')
                  ,hint                = _('Define the current term')
                  ,action              = lambda x:self.define(Selected=False)
                  ,inactive_image_path = sh.globs['var']['icon_define']
                  ,active_image_path   = sh.globs['var']['icon_define']
                  ,bindings            = sh.globs['var']['bind_define']
                  )
        # Кнопка "Перехват Ctrl-c-c"
        self.btn_clipboard = sg.Button (
                   parent_obj          = self._panel
                  ,text                = _('Clipboard')
                  ,hint                = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                  ,action              = self.watch_clipboard
                  ,inactive_image_path = sh.globs['var']['icon_watch_clipboard_off']
                  ,active_image_path   = sh.globs['var']['icon_watch_clipboard_on']
                  ,fg                  = 'red'
                  ,bindings            = []
                                       )
        # Кнопка "О программе"
        sg.Button (parent_obj          = self._panel
                  ,text                = _('About')
                  ,hint                = _('View About')
                  ,action              = objs.about().show
                  ,inactive_image_path = sh.globs['var']['icon_show_about']
                  ,active_image_path   = sh.globs['var']['icon_show_about']
                  ,bindings            = sh.globs['var']['bind_show_about']
                  )
        # Кнопка выхода
        sg.Button (parent_obj          = self._panel
                  ,text                = _('Quit')
                  ,hint                = _('Quit the program')
                  ,action              = self.close
                  ,inactive_image_path = sh.globs['var']['icon_quit_now']
                  ,active_image_path   = sh.globs['var']['icon_quit_now']
                  ,side                = 'right'
                  ,bindings            = [sh.globs['var']['bind_quit_now']
                                         ,sh.globs['var']['bind_quit_now_alt']
                                         ]
                  )

    def bindings(self):
        sg.bind (obj      = self
                ,bindings = '<Motion>'
                ,action   = self.mouse_sel
                )
        sg.bind (obj      = self
                ,bindings = '<Button-1>'
                # todo: This currently means 'self.go_url'. Prioritize/unblock dictionaries in 'self.go'.
                ,action   = self.go
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_copy_sel']
                            ,sh.globs['var']['bind_copy_sel_alt']
                            ,sh.globs['var']['bind_copy_sel_alt2']
                            ]
                ,action   = self.copy_text
                )
        sg.bind (obj = self.obj
                ,bindings = [sh.globs['var']['bind_quit_now']
                            ,sh.globs['var']['bind_quit_now_alt']
                            ]
                ,action=self.close
                )
        # Привязки: горячие клавиши и кнопки мыши
        sg.bind (obj      = self.history
                ,bindings = sh.globs['var']['bind_copy_history']
                ,action   = self.history.copy
                )
        sg.bind (obj      = self.obj
                ,bindings = ['<Return>'
                            ,'<KP_Enter>'
                            ]
                ,action   = self.go
                )
        # todo: do not iconify at <ButtonRelease-3>
        sg.bind (obj      = self.search_field
                ,bindings = sh.globs['var']['bind_clear_search_field']
                ,action   = self.search_field.clear
                )
        sg.bind (obj      = self.search_field
                ,bindings = sh.globs['var']['bind_paste_search_field']
                ,action   = lambda e:self.search_field.paste()
                )
        if sh.oss.win() or sh.oss.mac():
            sg.bind (obj      = self.obj
                    ,bindings = '<MouseWheel>'
                    ,action   = self.mouse_wheel
                    )
        else:
            sg.bind (obj      = self.obj
                    ,bindings = ['<Button 4>'
                                ,'<Button 5>'
                                ]
                    ,action   = self.mouse_wheel
                    )
        # Перейти на предыдущую/следующую статью
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_go_back']
                ,action   = self.go_back
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_go_forward']
                ,action   = self.go_forward
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Left>'
                ,action   = self.move_left
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Right>'
                ,action   = self.move_right
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Down>'
                ,action   = self.move_down
            )
        sg.bind (obj      = self.obj
                ,bindings = '<Up>'
                ,action   = self.move_up
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Home>'
                ,action   = self.move_line_start
                )
        sg.bind (obj      = self.obj
                ,bindings = '<End>'
                ,action   = self.move_line_end
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Control-Home>'
                ,action   = self.move_text_start
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Control-End>'
                ,action   = self.move_text_end
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Prior>'
                ,action   = self.move_page_up
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Next>'
                ,action   = self.move_page_down
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = sg.Geometry(parent_obj=self.obj).minimize
                )
        sg.bind (obj      = self
                ,bindings = '<ButtonRelease-2>'
                ,action   = sg.Geometry(parent_obj=self.obj).minimize
                )
        # Дополнительные горячие клавиши
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_search_article_forward']
                ,action   = self.search_article.forward
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_search_article_backward']
                ,action   = self.search_article.backward
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_re_search_article']
                ,action   = self.search_reset
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_reload_article']
                            ,sh.globs['var']['bind_reload_article_alt']
                            ]
                ,action   = self.reload
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_save_article']
                            ,sh.globs['var']['bind_save_article_alt']
                            ]
                ,action   = self.save_article.select
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_show_about']
                ,action   = objs.about().show
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history']
                            ]
                ,action   = self.history.toggle
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ]
                ,action   = self.history.toggle
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_open_in_browser']
                            ,sh.globs['var']['bind_open_in_browser_alt']
                            ]
                ,action   = self.open_in_browser
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_copy_url']
                ,action   = self.copy_block_url
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_copy_article_url']
                ,action   = self.copy_url
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_spec_symbol']
                ,action   = self.spec_symbols.show
                )
        sg.bind (obj      = self.search_field
                ,bindings = '<Control-a>'
                ,action   = self.search_field.obj.select_all
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_define']
                ,action   = lambda e:self.define(Selected=True)
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_prev_pair']
                            ,sh.globs['var']['bind_prev_pair_alt']
                            ]
                ,action   = self.menu_pairs.set_prev
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_next_pair']
                            ,sh.globs['var']['bind_next_pair_alt']
                            ]
                ,action   = self.menu_pairs.set_next
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_settings']
                            ,sh.globs['var']['bind_settings_alt']
                            ]
                ,action   = self.settings.show
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_toggle_view']
                            ,sh.globs['var']['bind_toggle_view_alt']
                            ]
                ,action   = self.toggle_view
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ]
                ,action   = self.history.toggle
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_clear_history']
                ,action   = self.history.clear
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_toggle_alphabet']
                ,action   = self.toggle_alphabet
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_toggle_block']
                ,action   = self.toggle_block
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_toggle_priority']
                ,action   = self.toggle_priority
                )
        sg.bind (obj      = self.btn_history
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.history.clear
                )
        sg.bind (obj      = self.obj
                ,bindings = sh.globs['var']['bind_print']
                ,action   = self.print
                )

    def scrollbars(self):
        vsb = ttk.Scrollbar (self.frame_y.widget
                            ,orient  = 'vertical'
                            ,command = self.widget.yview
                            )
        vsb.pack(expand=1,fill='y')
        hsb = ttk.Scrollbar (self.bottom.widget
                            ,orient  = 'horizontal'
                            ,command = self.widget.xview
                            )
        hsb.pack(expand=1,fill='x')
        self.widget.configure(xscrollcommand=hsb.set)
        self.widget.configure(yscrollcommand=vsb.set)

    def icon(self,arg=None):
        if not arg:
            arg = sh.globs['var']['icon_mclient']
        self.obj.icon(arg)

    def title(self,arg=None):
        if not arg:
            arg = sh.List(lst1=[product,version]).space_items()
        self.obj.title(arg)

    def text(self,event=None):
        # We will have a Segmentation Fault on empty input
        if objs.request()._html:
            return self.widget.text('text')

    def mouse_sel(self,event=None):
        self.get_pos(event=event)
        self.select()

    # todo: rework?
    def get_pos(self,event=None):
        if event:
            pos = None
            try:
                node1,node2 = self.widget.node(True,event.x,event.y)
                pos         = self.widget.text('offset',node1,node2)
            except ValueError: # Need more than 0 values to unpack
                pass
                '''
                # Too frequent
                sh.log.append ('WebFrame.get_pos'
                              ,_('WARNING')
                              ,_('Unable to get the position!')
                              )
                '''
            if pos is not None:
                objs.blocks_db().Selectable = False
                result = objs._blocks_db.block_pos(pos=pos)
                objs._blocks_db.Selectable = True
                if result:
                    if result[7] == 1: # Selectable
                        self._pos = pos
                else:
                    pass
                    '''
                    # Too frequent
                    sh.log.append ('WebFrame.get_pos'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
                    '''

    def select(self):
        result = objs.blocks_db().selection(pos=self._pos)
        if result:
            try:
                self.widget.tag ('delete','selection')
                self.widget.tag ('add','selection',result[0]
                                ,result[2],result[1],result[3]
                                )
                self.widget.tag ('configure','selection','-background'
                                ,sh.globs['var']['color_terms_sel_bg']
                                )
                self.widget.tag ('configure','selection','-foreground'
                                ,sh.globs['var']['color_terms_sel_fg']
                                )
            except tk.TclError:
                sh.log.append ('WebFrame.select'
                              ,_('WARNING')
                              ,_('Unable to set selection!')
                              )
        else:
            pass
            '''
            # Too frequent
            sh.log.append ('WebFrame.select'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            '''

    def height(self):
        sg.objs.root().widget.update_idletasks()
        '''
        sh.log.append ('WebFrame.height'
                      ,_('DEBUG')
                      ,_('Widget height: %s') % str(_height)
                      )
        '''
        return self.widget.winfo_height()

    def width(self):
        sg.objs.root().widget.update_idletasks()
        '''
        sh.log.append ('WebFrame.width'
                      ,_('DEBUG')
                      ,_('Widget width: %s') % str(_width)
                      )
        '''
        return self.widget.winfo_width()

    def shift_x(self,bbox1,bbox2,row_no):
        _width  = self.width()
        if _width:
            page_no1 = int(bbox1 / _width)
            page_no2 = int(bbox2 / _width)
            min_col  = objs._blocks_db.min_col()
            max_col  = objs._blocks_db.max_col()
            if min_col and max_col:
                min_bbox = min_col[2]
                max_bbox = max_col[2]
                page_no  = 0
                bboxes   = objs._blocks_db.row(row_no=row_no)
                if bboxes:
                    for i in range(len(bboxes)):
                        if page_no != int(bboxes[i][0] / _width) or page_no != int(bboxes[i][1] / _width):
                            page_no += 1
                        if bbox1 == bboxes[i][0]:
                            bbox1 = page_no * _width
                            break
                    fraction = None
                    if bbox1 == min_bbox:
                        fraction = '0.0'
                    elif self.direction == 'left':
                        fraction = (bbox1-5)/max_bbox
                    elif self.direction == 'right':
                        fraction = (bbox1+5)/max_bbox
                    if fraction:
                        self.widget.xview_moveto(fraction=fraction)
                else:
                    sh.log.append ('WebFrame.shift_x'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('WebFrame.shift_x'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.shift_x'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def shift_y(self,bboy1,bboy2,row_no,node):
        _height  = self.height()
        if _height:
            page_no1 = int(bboy1 / _height)
            page_no2 = int(bboy2 / _height)
            if page_no1 == page_no2:
                # This prevents from extra scrolling the same row
                self._row_no = row_no
                page_bboy = page_no1 * _height
                objs._blocks_db.Selectable = False
                node = objs._blocks_db.node_y1(bboy=page_bboy)
                objs._blocks_db.Selectable = sh.globs['bool']['SelectTermsOnly']
                if node:
                    try:
                        self.widget.yview_name(node)
                    except tk._tkinter.TclError:
                        if node:
                            node = node[0]
                        sh.log.append ('WebFrame.shift_screen'
                                      ,_('WARNING')
                                      ,_('Failed to set node "%s"!') % str(node)
                                      )
                else:
                    sh.log.append ('WebFrame.shift_screen'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                # If a part of the selection is readable, then Tkinter thinks that the entire selection is readable. Moreover, in the majority of cases, NODE1 = NODE2 and BBOY1 and BBOY2 refer to the same node. Calculating 'moveto' proportion (max possible BBOY2/BBOY1) does not help, 'scan_dragto' is not implemented, so we use a little trick here.
                # 'Units' means 'lines'
                if self._row_no != row_no:
                    if self.direction in ('down','right'):
                        self.widget.yview_scroll(number=5,what='units')
                    elif self.direction in ('up','left'):
                        self.widget.yview_scroll(number=-5,what='units')
                    self._row_no = row_no
        else:
            sh.log.append ('WebFrame.shift_y'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def shift_screen(self):
        result = objs.blocks_db().selection(pos=self._pos)
        if result:
            self.shift_x (bbox1  = result[4]
                         ,bbox2  = result[5]
                         ,row_no = result[8]
                         )
            self.shift_y (bboy1  = result[6]
                         ,bboy2  = result[7]
                         ,row_no = result[8]
                         ,node   = result[0]
                         )
        else:
            sh.log.append ('WebFrame.shift_screen'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def fill(self,code='<html><body><h1>Nothing has been loaded yet.</h1></body></html>'):
        self.widget.reset()
        self.widget.parse(code)

    def show(self,*args):
        self.obj.show()

    def close(self,*args):
        self.obj.close()

    def load_article(self):
        timer = sh.Timer(func_title='WebFrame.load_article')
        timer.start()
        objs.blocks_db().request (source = objs.request()._source
                                 ,search = objs._request._search
                                 )
        if not objs._blocks_db.present():
            ptimer = sh.Timer(func_title='WebFrame.load_article (Page)')
            ptimer.start()
            page = pg.Page (source       = objs._request._source
                           ,lang         = objs._request._lang
                           ,search       = objs._request._search
                           ,url          = objs._request._url
                           ,win_encoding = sh.globs['var']['win_encoding']
                           ,ext_dics     = objs.ext_dics()
                           #,file        = '/home/pete/tmp/ars/random fury.txt'
                           #,file        = '/home/pete/tmp/ars/lottery.txt'
                           #,file        = '/home/pete/tmp/ars/таратайка.txt'
                           ,file        = '/home/pete/tmp/ars/painting.txt'
                           #,file        = '/home/pete/tmp/ars/рабочая документация.txt'
                           #,file        = '/home/pete/tmp/ars/do.txt'
                           #,file        = '/home/pete/tmp/ars/set.txt'
                           #,file        = '/home/pete/tmp/ars/get.txt'
                           #,file        = '/home/pete/tmp/ars/pack.txt'
                           #,file        = '/home/pete/tmp/ars/counterpart.txt'
                           #,file        = '/home/pete/tmp/ars/test.txt'
                           #,file        = '/home/pete/tmp/ars/cut.txt'
                           #,file        = '/home/pete/tmp/ars/tun.txt'
                           #,file        = '/home/pete/tmp/ars/martyr.txt'
                           )
            page.run()
            ptimer.end()
            # todo: # fix: assign this for already loaded articles too
            objs._request._page     = page._page
            # note: # todo: 'Page' returns '_html_raw' for online pages only; this value can be separated for online & offline sources after introducing sub-sources instead of relying on _('All')
            objs._request._html_raw = page._html_raw

            tags = tg.Tags (text      = objs._request._page
                           ,source    = objs._request._source
                           ,pair_root = sh.globs['var']['pair_root']
                           )
            tags.run()

            elems = el.Elems (blocks = tags._blocks
                             ,source = objs._request._source
                             ,search = objs._request._search
                             ,urla   = objs._request._url
                             )
            elems.run()

            objs._blocks_db.fill(elems._data)

            ph_terma = el.PhraseTerma (dbc    = objs._blocks_db.dbc
                                      ,source = objs._request._source
                                      ,search = objs._request._search
                                      )
            ph_terma.run()

        phrase_dic = objs._blocks_db.phrase_dic()
        data       = objs._blocks_db.assign_bp ()

        bp = cl.BlockPrioritize (data       = data
                                ,source     = objs._request._source
                                ,search     = objs._request._search
                                ,blacklist  = objs.blacklist()
                                ,prioritize = objs.prioritize()
                                ,Block      = objs._request.Block
                                ,Prioritize = objs._request.Prioritize
                                ,phrase_dic = phrase_dic
                                )
        bp.run()
        objs._blocks_db.update(query=bp._query)

        dics = objs._blocks_db.dics(Block=0)
        # todo: make this Multitran-only
        # note: if an article comprises only 1 dic/wform, this is usually a dictionary + terms from the 'Phrases' section
        # Do not rely on the number of wforms; large articles like 'centre' may have only 1 wform (an a plurality of dics)
        if not dics or dics and len(dics) == 1:
            objs._request.SpecialPage = True
            # A dictionary from the 'Phrases' section usually has an 'original + translation' structure, so we need to switch off sorting terms and ensure that the number of columns is divisible by 2
            if objs._request._collimit % 2 != 0:
                if objs._request._collimit == 5:
                    objs._request._collimit += 1
                else:
                    objs._request._collimit -= 1
                sh.log.append ('WebFrame.load_article'
                              ,_('INFO')
                              ,_('Set the column limit to %d') % objs._request._collimit
                              )
        else:
            objs._request.SpecialPage = False # Otherwise, 'SpecialPage' will be inherited

        SortTerms = objs._request.SortTerms and not objs._request.SpecialPage
        objs._blocks_db.reset (cols      = objs._request._cols
                              ,SortRows  = objs._request.SortRows
                              ,SortTerms = SortTerms
                              )
        data  = objs._blocks_db.assign_cells()
        cells = cl.Cells (data       = data
                         ,cols       = objs._request._cols
                         ,collimit   = objs._request._collimit
                         ,phrase_dic = phrase_dic
                         ,Reverse    = objs._request.Reverse
                         )
        cells.run()
        objs._blocks_db.update(query=cells._query)

        get_html = mh.HTML (data       = objs._blocks_db.fetch()
                           ,cols       = objs._request._cols
                           ,collimit   = objs._request._collimit
                           ,blacklist  = objs.blacklist()
                           ,prioritize = objs.prioritize()
                           ,width      = sh.globs['int']['col_width']
                           ,Reverse    = objs._request.Reverse
                           )
        objs._request._html = get_html._html
        self.fill(code=objs._request._html)

        data = objs._blocks_db.assign_pos()
        pos  = cl.Pos(data=data,raw_text=self.text())
        pos.run()
        objs._blocks_db.update(query=pos._query)

        pages = cl.Pages(obj=objs.webframe(),blocks=pos._blocks)
        pages.run()
        objs._blocks_db.update(query=pages._query)

        self.title(arg=objs._request._search)
        self.move_text_start()
        # Empty article is not added either to DB or history, so we just do not clear the search field to be able to correct the typo.
        if pages._blocks:
            self.search_field.clear()
        self.history.update()
        self.search_article.reset()
        self.update_buttons()
        timer.end()

        '''
        objs.blocks_db().dbc.execute('select CELLNO,NO,TYPE,TEXT,POS1,POS2,SELECTABLE from BLOCKS order by CELLNO,NO')
        objs.blocks_db().print(Selected=1,Shorten=1,MaxRow=20,MaxRows=300)
        '''

    # Select either the search string or the URL
    def go(self,*args):
        search = self.search_field.widget.get().strip('\n').strip(' ')
        if search == '':
            self.go_url()
        elif search == sh.globs['var']['repeat_sign']:
            self.search_field.insert_repeat_sign()
        elif search == sh.globs['var']['repeat_sign2']:
            self.search_field.insert_repeat_sign2()
        else:
            objs._request._search = search
            self.go_search()

    # Перейти по URL текущей ячейки
    def go_url(self,*args):
        if not objs.request().MouseClicked:
            url = objs.blocks_db().url(pos=self._pos)
            if url:
                objs.request()._search = objs._blocks_db.text(pos=self._pos)
                objs._request._url     = url
                sh.log.append ('WebFrame.go_url'
                              ,_('INFO')
                              ,_('Open link: %s') % objs._request._url
                              )
                self.load_article()
            else:
                sg.Message ('WebFrame.go_url'
                           ,_('WARNING')
                           ,_('This block does not contain a URL!')
                           )

    def go_search(self):
        if self.control_length():
            self.get_url()
            sh.log.append ('WebFrame.go_search'
                          ,_('DEBUG')
                          ,objs.request()._search
                          )
            self.load_article()

    def set_source(self,*args):
        objs.request()._source = sources[self.menu_sources.index]
        sh.log.append ('WebFrame.set_source'
                      ,_('INFO')
                      ,_('Set source to "%s"') % objs._request._source
                      )
        self.load_article()

    def get_url(self):
        # note: encoding must be UTF-8 here
        if objs.request()._source == _('Offline'):
            objs.online().reset (self.get_pair()
                                ,objs.request()._search
                                ,MTSpecific=False
                                )
        else:
            objs.online().reset (self.get_pair()
                                ,objs.request()._search
                                ,MTSpecific=True
                                )
            objs.request()._url = objs.online().url()
        sh.log.append ('WebFrame.get_url'
                      ,_('DEBUG')
                      ,str(objs.request()._url)
                      )

    def key_move(self):
        self.select()
        self.shift_screen()

    # todo: move 'move_*' procedures to Moves class
    # Перейти на 1-й термин текущей строки
    def move_line_start(self,*args):
        self.direction = 'left'
        self._pos = objs.blocks_db().line_start(pos=self._pos)
        self.key_move()

    # Перейти на последний термин текущей строки
    def move_line_end(self,*args):
        self.direction = 'right'
        self._pos = objs.blocks_db().line_end(pos=self._pos)
        self.key_move()

    # Go to the 1st (non-)selectable block
    def move_text_start(self,*args):
        self.direction = 'up'
        self._pos = objs.blocks_db().start()
        self.key_move()

    # Перейти на последний термин статьи
    def move_text_end(self,*args):
        self.direction = 'down'
        self._pos = objs.blocks_db().end()
        self.key_move()

    # Перейти на страницу вверх
    def move_page_up(self,*args):
        self.direction = 'up'
        result = objs.blocks_db().selection(pos=self._pos)
        height = self.height()
        if result and height:
            result = objs.blocks_db().page_up(bboy=result[6],height=height)
            if result:
                self._pos = result
                self.key_move()

    # Перейти на страницу вниз
    def move_page_down(self,*args):
        self.direction = 'down'
        result = objs.blocks_db().selection(pos=self._pos)
        height = self.height()
        if result and height:
            result = objs.blocks_db().page_down(bboy=result[6],height=height)
            if result:
                self._pos = result
                self.key_move()

    # Перейти на предыдущий термин
    def move_left(self,*args):
        self.direction = 'left'
        self._pos = objs.blocks_db().left(pos=self._pos)
        self.key_move()

    # Перейти на следующий термин
    def move_right(self,*args):
        self.direction = 'right'
        self._pos = objs.blocks_db().right(pos=self._pos)
        self.key_move()

    # Перейти на строку вниз
    def move_down(self,*args):
        self.direction = 'down'
        self._pos = objs.blocks_db().down(pos=self._pos)
        self.key_move()

    # Перейти на строку вверх
    def move_up(self,*args):
        self.direction = 'up'
        self._pos = objs.blocks_db().up(pos=self._pos)
        self.key_move()

    # Задействование колеса мыши для пролистывания экрана
    def mouse_wheel(self,event):
        # todo: fix: too small delta in Windows
        # В Windows XP delta == -120, однако, в других версиях оно другое
        if event.num == 5 or event.delta < 0:
            if sh.oss.lin():
                self.move_page_down()
            else:
                self.move_down()
        # В Windows XP delta == 120, однако, в других версиях оно другое
        if event.num == 4 or event.delta > 0:
            if sh.oss.lin():
                self.move_page_up()
            else:
                self.move_up()
        return 'break'

    # Следить за буфером обмена
    def watch_clipboard(self,*args):
        if objs.request().CaptureHotkey:
            objs._request.CaptureHotkey = False
        else:
            objs._request.CaptureHotkey = True
        self.update_buttons()

    # Открыть URL текущей статьи в браузере
    def open_in_browser(self,*args):
        objs.online()._url = objs.request()._url
        objs.online().browse()

    # Скопировать текст текущего блока
    def copy_text(self,*args):
        text = objs.blocks_db().text(pos=self._pos)
        if text:
            sg.Clipboard().copy(text)
            if sh.globs['bool']['Iconify']:
                sg.Geometry(parent_obj=self.obj).minimize()
        else:
            sg.Message ('WebFrame.copy_text'
                       ,_('WARNING')
                       ,_('This block does not contain any text!')
                       )

    # Скопировать URL текущей статьи
    def copy_url(self,*args):
        sg.Clipboard().copy(objs.request()._url)
        if sh.globs['bool']['Iconify']:
            sg.Geometry(parent_obj=self.obj).minimize()

    # Скопировать URL выделенного блока
    def copy_block_url(self,*args):
        url = objs.blocks_db().url(pos=self._pos)
        if url:
            sg.Clipboard().copy(url)
            if sh.globs['bool']['Iconify']:
                sg.Geometry(parent_obj=self.obj).minimize()
        else:
            sg.Message ('WebFrame.copy_block_url'
                       ,_('WARNING')
                       ,_('This block does not contain a URL!')
                       )

    # Открыть веб-страницу с определением текущего термина
    def define(self,Selected=True): # Selected: True: Выделенный термин; False: Название статьи
        if Selected:
            result = objs.blocks_db().block_pos(pos=self._pos)
            search_str = 'define:' + result[6]
        else:
            search_str = 'define:' + objs.request()._search
        if search_str != 'define:':
            objs.online().reset (base_str   = sh.globs['var']['web_search_url']
                                ,search_str = search_str
                                )
            objs.online().browse()
        else:
            sh.log.append ('WebFrame.define'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Обновить рисунки на кнопках и галки в виджете Settings
    def update_buttons(self):
        searches = objs.blocks_db().searches()
        if searches:
            self.btn_repeat_sign.active()
        else:
            self.btn_repeat_sign.inactive()

        if searches and len(searches) > 1:
            self.btn_repeat_sign2.active()
        else:
            self.btn_repeat_sign2.inactive()

        if objs.blocks_db().prev_search():
            self.btn_prev.active()
        else:
            self.btn_prev.inactive()

        if objs.blocks_db().next_search():
            self.btn_next.active()
        else:
            self.btn_next.inactive()

        if objs.request().CaptureHotkey:
            self.btn_clipboard.active()
        else:
            self.btn_clipboard.inactive()

        if objs._request.Reverse:
            self.btn_toggle_view.inactive()
            self.settings.cb5.enable()
        else:
            self.btn_toggle_view.active()
            self.settings.cb5.disable()

        if not objs._request.SpecialPage and objs._request.SortTerms:
            self.btn_toggle_alphabet.active()
            self.settings.cb2.enable()
        else:
            self.btn_toggle_alphabet.inactive()
            self.settings.cb2.disable()

        if objs._request.Block and objs._blocks_db.blocked():
            self.btn_toggle_block.active()
            self.settings.cb3.enable()
        else:
            self.btn_toggle_block.inactive()
            self.settings.cb3.disable()

        if not objs._request.SpecialPage and objs._request.Prioritize and objs._blocks_db.prioritized():
            self.btn_toggle_priority.active()
            self.settings.cb4.enable()
        else:
            self.btn_toggle_priority.inactive()
            self.settings.cb4.disable()

    # Перейти на предыдущий запрос
    def go_back(self,*args):
        searches = objs.blocks_db().searches()
        if searches:
            result = objs._blocks_db.prev_search()
            if result:
                objs.request()._search = result
                self.load_article()
            # No need to load the same article once again
            elif len(searches) > 1:
                # The list is sorted in the descending order
                objs.request()._search = list(searches)[0]
                self.load_article()
        else:
            sh.log.append ('WebFrame.go_back'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    # Перейти на следующий запрос
    def go_forward(self,*args):
        searches = objs.blocks_db().searches()
        if searches:
            result = objs.blocks_db().next_search()
            if result:
                objs.request()._search = result
                self.load_article()
            # No need to load the same article once again
            elif len(searches) > 1:
                # The list is sorted in the descending order
                objs.request()._search = list(searches)[-1]
                self.load_article()
        else:
            sh.log.append ('WebFrame.go_forward'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def control_length(self): # Confirm too long requests
        Confirmed = True
        if len(objs.request()._search) >= 150:
            if not sg.Message (func    = 'WebFrame.control_length'
                              ,level   = _('QUESTION')
                              ,message = _('The request is long (%d symbols). Do you really want to send it?') % len(objs._request._search)
                              ).Yes:
                Confirmed = False
        return Confirmed

    def search_reset(self,*args): # SearchArticle
        self.search_article.reset()
        self.search_article.forward()

    def set_lang(self,*args):
        objs.request()._lang = langs[self.menu_pairs.index]
        sh.log.append ('WebFrame.set_lang'
                      ,_('INFO')
                      ,_('Set language to "%s"') % objs._request._lang
                      )

    def get_pair(self):
        return online_dic_urls[self.menu_pairs.index]

    def set_columns(self,*args):
        sh.log.append ('WebFrame.set_columns'
                      ,_('INFO')
                      ,str(self.menu_columns.choice)
                      )
        objs.request()._collimit = self.menu_columns.choice + 4
        self.load_article()

    def reload(self,*args):
        objs.blocks_db().clear_cur()
        self.load_article()

    # Вставить спец. символ в строку поиска
    def insert_sym(self,sym):
        self.search_field.widget.insert('end',sym)
        if sh.globs['bool']['AutoCloseSpecSymbol']:
            self.spec_symbols.close()

    def toggle_view(self,*args):
        if objs.request().Reverse:
            objs._request.Reverse = False
        else:
            objs._request.Reverse = True
        self.load_article()

    def toggle_alphabet(self,*args):
        if objs.request().SortTerms:
            objs._request.SortTerms = False
        else:
            objs._request.SortTerms = True
        self.load_article()

    def toggle_block(self,*args):
        if objs.request().Block:
            objs._request.Block = False
            '''
            sg.Message (func    = 'WebFrame.toggle_block'
                       ,level   = _('INFO')
                       ,message = _('Blacklisting is now OFF.')
                       )
            '''
            self.unblock()
        else:
            objs._request.Block = True
            if objs._blacklist:
                '''
                sg.Message (func    = 'WebFrame.toggle_block'
                           ,level   = _('INFO')
                           ,message = _('Blacklisting is now ON.')
                           )
                '''
                pass
            else:
                sg.Message (func    = 'WebFrame.toggle_block'
                           ,level   = _('WARNING')
                           ,message = _('No dictionaries have been provided for blacklisting!')
                           )
        self.load_article()

    def unblock(self):
        result = objs.blocks_db().blocked()
        if result:
            tmp = io.StringIO()
            query = ''
            tmp.write('begin;')
            for no in result:
                tmp.write('update BLOCKS set BLOCK=0 where NO=%d;' % no)
            tmp.write('commit;')
            query = tmp.getvalue()
            tmp.close()
            objs._blocks_db.update(query=query)

    def unprioritize(self):
        result = objs.blocks_db().prioritized()
        if result:
            tmp = io.StringIO()
            query = ''
            tmp.write('begin;')
            for no in result:
                tmp.write('update BLOCKS set PRIORITY=0 where NO=%d;' % no)
            tmp.write('commit;')
            query = tmp.getvalue()
            tmp.close()
            objs._blocks_db.update(query=query)

    def toggle_priority(self,*args):
        if objs.request().Prioritize:
            objs._request.Prioritize = False
            '''
            sg.Message (func    = 'WebFrame.toggle_priority'
                       ,level   = _('INFO')
                       ,message = _('Prioritizing is now OFF.')
                       )
            '''
            self.unprioritize()
        else:
            objs._request.Prioritize = True
            if objs._prioritize:
                '''
                sg.Message (func    = 'WebFrame.toggle_priority'
                           ,level   = _('INFO')
                           ,message = _('Prioritizing is now ON.')
                           )
                '''
                pass
            else:
                sg.Message (func    = 'WebFrame.toggle_priority'
                           ,level   = _('WARNING')
                           ,message = _('No dictionaries have been provided for prioritizing!')
                           )
        self.load_article()

    def print(self,*args):
        code = mh.HTML (data     = objs._blocks_db.fetch()
                       ,collimit = objs._request._collimit
                       ,Printer  = True
                       )._html
        if code:
            sh.WriteTextFile(sh.objs.tmpfile(suffix='.htm',Delete=0),AskRewrite=0).write(code)
            sh.Launch(target=sh.objs._tmpfile).auto()
        else:
            sh.log.append ('WebFrame.print'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def bbox(self,*args):
        return self.widget.tk.call(self.widget,"bbox",*args)

    def zzz(self): # Only needed to move quickly to the end of the class
        pass



class Paths:

    def __init__(self):
        self.dir = sh.Directory(path=sh.objs.pdir().add('dics'))
        self.Success = self.dir.Success

    def blacklist(self):
        if self.Success:
            instance = sh.File(file=os.path.join(self.dir.dir,'block.txt'))
            self.Success = instance.Success
            if self.Success:
                return instance.file
            else:
                sh.log.append ('Paths.blacklist'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Paths.blacklist'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prioritize(self):
        if self.Success:
            instance = sh.File(file=os.path.join(self.dir.dir,'prioritize.txt'))
            self.Success = instance.Success
            if self.Success:
                return instance.file
            else:
                sh.log.append ('Paths.prioritize'
                              ,_('WARNING')
                              ,_('Operation has been canceled.')
                              )
        else:
            sh.log.append ('Paths.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



# Read the blocklist and the prioritize list
class Lists:

    def __init__(self):
        paths            = Paths()
        self._blacklist  = paths.blacklist()
        self._prioritize = paths.prioritize()
        self.Success     = paths.Success

    def blacklist(self):
        if self.Success:
            text = sh.ReadTextFile(file=self._blacklist,Silent=1).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.log.append ('Lists.blacklist'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prioritize(self):
        if self.Success:
            text = sh.ReadTextFile(file=self._prioritize,Silent=1).get()
            text = sh.Text(text=text,Auto=1).text
            return text.splitlines()
        else:
            sh.log.append ('Lists.prioritize'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class Settings:

    def __init__(self):
        self.values()
        self.gui()

    def values(self):
        self._items = (_('Dictionaries')
                      ,_('Word forms')
                      ,_('Parts of speech')
                      ,_('Transcription')
                      ,_('Do not set')
                      )
        self._allowed    = []
        self._hint_width = 200
        self.Active      = False

    def update_col1(self):
        if self.col1.choice != _('Do not set'):
            if self.col1.choice in self._allowed:
                self._allowed.remove(self.col1.choice)
            elif _('Dictionaries') in self._allowed:
                self.col1.set(_('Dictionaries'))
                self._allowed.remove(_('Dictionaries'))
            elif self._allowed:
                self.col1.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (func    = 'Settings.update_col1'
                           ,level   = _('ERROR')
                           ,message = _('Empty input is not allowed!')
                           )

    def update_col2(self):
        if self.col2.choice != _('Do not set'):
            if self.col2.choice in self._allowed:
                self._allowed.remove(self.col2.choice)
            elif _('Word forms') in self._allowed:
                self.col2.set(_('Word forms'))
                self._allowed.remove(_('Word forms'))
            elif self._allowed:
                self.col2.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (func    = 'Settings.update_col2'
                           ,level   = _('ERROR')
                           ,message = _('Empty input is not allowed!')
                           )

    def update_col3(self):
        if self.col3.choice != _('Do not set'):
            if self.col3.choice in self._allowed:
                self._allowed.remove(self.col3.choice)
            elif _('Parts of speech') in self._allowed:
                self.col3.set(_('Parts of speech'))
                self._allowed.remove(_('Parts of speech'))
            elif self._allowed:
                self.col3.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (func    = 'Settings.update_col3'
                           ,level   = _('ERROR')
                           ,message = _('Empty input is not allowed!')
                           )

    def update_col4(self):
        if self.col4.choice != _('Do not set'):
            if self.col4.choice in self._allowed:
                self._allowed.remove(self.col4.choice)
            elif _('Transcription') in self._allowed:
                self.col4.set(_('Transcription'))
                self._allowed.remove(_('Transcription'))
            elif self._allowed:
                self.col4.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (func    = 'Settings.update_col4'
                           ,level   = _('ERROR')
                           ,message = _('Empty input is not allowed!')
                           )

    def update_by_col1(self,*args):
        self._allowed = list(self._items)
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()

    def update_by_col2(self,*args):
        self._allowed = list(self._items)
        self.update_col2()
        self.update_col1()
        self.update_col3()
        self.update_col4()

    def update_by_col3(self,*args):
        self._allowed = list(self._items)
        self.update_col3()
        self.update_col1()
        self.update_col2()
        self.update_col4()

    def update_by_col4(self,*args):
        self._allowed = list(self._items)
        self.update_col4()
        self.update_col1()
        self.update_col2()
        self.update_col3()

    def gui(self):
        self.obj = sg.objs.new_top(Maximize=0)
        self.title()
        self.frames()
        self.columns()
        self.sort_rows()
        self.sort_terms()
        self.block()
        self.prioritize()
        self.vertical()
        self.buttons()
        self.bindings()
        self.icon()

    def vertical(self):
        self.cb5 = sg.CheckBox (parent_obj = self.fr_cb5
                               ,Active     = False
                               ,side       = 'left'
                               )
        self.lb5 = sg.Label (parent_obj = self.fr_cb5
                            ,text       = _('Vertical view')
                            ,side       = 'left'
                            )

    def sort_rows(self):
        self.cb = sg.CheckBox (parent_obj = self.fr_cb
                              ,Active     = True
                              ,side       = 'left'
                              )
        self.lb = sg.Label (parent_obj = self.fr_cb
                           ,text       = _('Sort by each column (if it is set) (except for transcription)')
                           ,side       = 'left'
                           )

    def sort_terms(self):
        self.cb2 = sg.CheckBox (parent_obj = self.fr_cb2
                               ,Active     = True
                               ,side       = 'left'
                               )
        self.lb2 = sg.Label (parent_obj = self.fr_cb2
                            ,text       = _('Alphabetize terms')
                            ,side       = 'left'
                            )

    def block_settings(self,*args):
        sg.Message (func    = 'Settings.block_settings'
                   ,level   = _('INFO')
                   ,message = _('Not implemented yet!')
                   )

    def priority_settings(self,*args):
        sg.Message (func    = 'Settings.priority_settings'
                   ,level   = _('INFO')
                   ,message = _('Not implemented yet!')
                   )

    def block(self):
        self.cb3 = sg.CheckBox (parent_obj = self.fr_cb3
                               ,Active     = True
                               ,side       = 'left'
                               )
        self.lb3 = sg.Label (parent_obj = self.fr_cb3
                            ,text       = _('Block dictionaries from blacklist')
                            ,side       = 'left'
                            )
        sg.Button (parent_obj = self.fr_cb3
                  ,action     = self.block_settings
                  ,hint       = _('Tune up blacklisting')
                  ,hint_width = self._hint_width
                  ,text       = _('Add/Remove')
                  ,side       = 'right'
                  )

    def prioritize(self):
        self.cb4 = sg.CheckBox (parent_obj = self.fr_cb4
                               ,Active     = True
                               ,side       = 'left'
                               )
        self.lb4 = sg.Label (parent_obj = self.fr_cb4
                            ,text       = _('Prioritize dictionaries')
                            ,side       = 'left'
                            )
        sg.Button (parent_obj = self.fr_cb4
                  ,action     = self.priority_settings
                  ,hint       = _('Tune up prioritizing')
                  ,hint_width = self._hint_width
                  ,text       = _('Add/Remove')
                  ,side       = 'right'
                  )

    def reset(self,*args):
        self.col1.set(_('Dictionaries'))
        self.col2.set(_('Word forms'))
        self.col3.set(_('Parts of speech'))
        self.col4.set(_('Transcription'))
        self.cb.enable()
        self.cb2.enable()
        self.cb3.enable()
        self.cb4.enable()
        self.cb5.disable()

    def apply(self,*args):
        # Do not use 'gettext' to name internal types - this will make the program ~0,6 s slower
        lst = [choice for choice in (self.col1.choice,self.col2.choice,self.col3.choice,self.col4.choice) if choice != _('Do not set')]
        '''
        The following assignment does not change the list:
            for item in lst:
                if item == something:
                    item = something_else
        '''
        for i in range(len(lst)):
            if lst[i] == _('Dictionaries'):
                lst[i] = 'dic'
            elif lst[i] == _('Word forms'):
                lst[i] = 'wform'
            elif lst[i] == _('Parts of speech'):
                lst[i] = 'speech'
            elif lst[i] == _('Transcription'):
                lst[i] = 'transc'
            else:
                sg.Message (func    = 'Settings.apply'
                           ,level   = _('ERROR')
                           ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(self._cols[i]),', '.join(_('Dictionaries'),_('Word forms'),_('Parts of speech'),_('Transcription')))
                           )
        if set(lst):
            self.close()
            objs.request()._cols     = tuple(lst)
            objs._request.SortRows   = self.cb.get()
            objs._request.SortTerms  = self.cb2.get()
            objs._request.Block      = self.cb3.get()
            objs._request.Prioritize = self.cb4.get()
            objs._request.Reverse    = self.cb5.get()
            objs.blocks_db().reset (cols      = objs._request._cols
                                   ,SortRows  = objs._request.SortRows
                                   ,SortTerms = objs._request.SortTerms
                                   )
            objs._blocks_db.unignore()
            objs._blocks_db.ignore()
            objs.webframe().load_article()
        else:
            # todo: do we really need this?
            sg.Message (func    = 'Settings.apply'
                       ,level   = _('WARNING')
                       ,message = _('At least one column must be set!')
                       )

    def buttons(self):
        sg.Button (parent_obj = self.fr_but
                  ,action     = self.reset
                  ,hint       = _('Reset settings')
                  ,hint_width = self._hint_width
                  ,text       = _('Reset')
                  ,side       = 'left'
                  )

        sg.Button (parent_obj = self.fr_but
                  ,action     = self.apply
                  ,hint       = _('Apply settings')
                  ,hint_width = self._hint_width
                  ,text       = _('Apply')
                  ,side       = 'right'
                  )

    def frames(self):
        self.fr_col = sg.Frame (parent_obj = self.obj
                               ,expand     = True
                               ,fill       = 'both'
                               )
        self.fr_cb  = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               )
        self.fr_cb2 = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               )
        self.fr_cb3 = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               )
        self.fr_cb4 = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               )
        self.fr_cb5 = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               )
        self.fr_but = sg.Frame (parent_obj = self.obj
                               ,expand     = False
                               ,fill       = 'x'
                               ,side       = 'bottom'
                               )

    def columns(self):
        self.col1 = sg.OptionMenu (parent_obj = self.fr_col
                                  ,items      = self._items
                                  ,side       = 'left'
                                  ,command    = self.update_by_col1
                                  ,default    = _('Dictionaries')
                                  )
        self.col2 = sg.OptionMenu (parent_obj = self.fr_col
                                  ,items      = self._items
                                  ,side       = 'left'
                                  ,command    = self.update_by_col2
                                  ,default    = _('Word forms')
                                  )
        self.col3 = sg.OptionMenu (parent_obj = self.fr_col
                                  ,items      = self._items
                                  ,side       = 'left'
                                  ,command    = self.update_by_col3
                                  ,default    = _('Parts of speech')
                                  )
        self.col4 = sg.OptionMenu (parent_obj = self.fr_col
                                  ,items      = self._items
                                  ,side       = 'left'
                                  ,command    = self.update_by_col4
                                  ,default    = _('Transcription')
                                  )

    def bindings(self):
        sg.bind (obj      = self.lb
                ,bindings = '<Button-1>'
                ,action   = self.cb.toggle
                )
        sg.bind (obj      = self.lb2
                ,bindings = '<Button-1>'
                ,action   = self.cb2.toggle
                )
        sg.bind (obj      = self.lb3
                ,bindings = '<Button-1>'
                ,action   = self.cb3.toggle
                )
        sg.bind (obj      = self.lb4
                ,bindings = '<Button-1>'
                ,action   = self.cb4.toggle
                )
        sg.bind (obj      = self.lb5
                ,bindings = '<Button-1>'
                ,action   = self.cb5.toggle
                )
        sg.bind (obj      = self.obj
                ,bindings = [sh.globs['var']['bind_settings']
                            ,sh.globs['var']['bind_settings_alt']
                            ,'<Escape>'
                            ]
                ,action = self.toggle
                )

    def title(self,text=_('View Settings')):
        self.obj.title(text=text)

    def show(self,*args):
        self.Active = True
        self.obj.show()

    def close(self,*args):
        self.Active = False
        self.obj.close()

    def toggle(self,*args):
        if self.Active:
            self.close()
        else:
            self.show()

    def icon(self,arg=None):
        if not arg:
            arg = sh.globs['var']['icon_mclient']
        self.obj.icon(arg)

    def zzz(self):
        pass



objs = Objects()


if  __name__ == '__main__':
    sg.objs.start()

    ConfigMclient()

    timed_update()

    objs.webframe().reset()
    objs._webframe.show()

    kl_mod.keylistener.cancel()

    sg.objs.end()
