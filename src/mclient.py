#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import io
import tkinter   as tk
import shared    as sh
import sharedGUI as sg
import logic     as lg
import gui       as gi
import page      as pg
import tags      as tg
import elems     as el
import cells     as cl
import db
import mkhtml    as mh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','./locale')


product = 'MClient'
version = '5.9'


lg.ConfigMclient()


if __name__ == '__main__':
    if sh.oss.win():
        import kl_mod_win as kl_mod
        import pythoncom
    else:
        import kl_mod_lin as kl_mod

sh.globs['_tkhtml_loaded'] = False
sh.globs['geom_top'] = {}
sh.globs['top'] = {}

sep_words_found = 'найдены отдельные слова'

pairs = ('ENG <=> RUS','DEU <=> RUS','SPA <=> RUS'
        ,'FRA <=> RUS','NLD <=> RUS','ITA <=> RUS'
        ,'LAV <=> RUS','EST <=> RUS','AFR <=> RUS'
        ,'EPO <=> RUS','RUS <=> XAL','XAL <=> RUS'
        ,'ENG <=> DEU','ENG <=> EST'
        )

online_dic_urls = (sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_rus']   # ENG <=> RUS, 'CL=1&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_deu_rus']   # DEU <=> RUS, 'l1=3&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_spa_rus']   # SPA <=> RUS, 'l1=5&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_fra_rus']   # FRA <=> RUS, 'l1=4&l2=2&s=%s'
                  ,sh.globs['var']['pair_root'] + sh.globs['var']['pair_nld_rus']   # NLD <=> RUS, 'l1=24&l2=2&s=%s'
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
        self._top = self._online_mt = self._online_other = self._about \
                  = self._blacklist = self._prioritize = self._request \
                  = self._ext_dics = self._webframe = self._blocks_db \
                  = self._moves = self._logic = None

    def logic(self):
        if not self._logic:
            self._logic = Logic()
        return self._logic
    
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
            self._request = lg.CurRequest()
        return self._request

    def online_mt(self):
        if not self._online_mt:
            self._online_mt = sh.Online(MTSpecific=True)
        return self._online_mt

    def online_other(self):
        if not self._online_other:
            self._online_other = sh.Online(MTSpecific=False)
        return self._online_other

    def online(self):
        #todo: create a sub-source
        if objs.request()._source in (_('All'),_('Online')):
            return self.online_mt()
        else:
            return self.online_other()

    def blacklist(self):
        # Allow empty lists
        if self._blacklist is None:
            self._blacklist = lg.Lists().blacklist()
        return self._blacklist

    def prioritize(self):
        # Allow empty lists
        if self._prioritize is None:
            self._prioritize = lg.Lists().prioritize()
        return self._prioritize



def call_app():
    # Использовать то же сочетание клавиш для вызова окна
    sg.Geometry(parent=objs.webframe().obj).activate(MouseClicked=objs.request().MouseClicked)
    ''' #todo: check if this is still the problem
        In case of .focus_set() *first* Control-c-c can call an inactive
        widget.
    '''
    objs.webframe().search_field.widget.focus_force()

# Перехватить нажатие Control-c-c
def timed_update():
    objs.request().MouseClicked = False
    check = kl_mod.keylistener.check()
    if check:
        if check == 1 and objs._request.CaptureHotkey:
            ''' Позволяет предотвратить зависание потока в версиях
                Windows старше XP
            '''
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
        self.parties = ThirdParties()
        self.gui = gi.About()
        self.bindings()
        self.gui.label.text (_('Programming: Peter Sklyar, 2015-2018.\nVersion: %s\n\nThis program is free and opensource. You can use and modify it freely\nwithin the scope of the provisions set forth in GPL v.3 and the active legislation.\n\nIf you have any questions, requests, etc., please do not hesitate to contact me.\n') \
                             % version
                            )
        self.gui.label.font(sh.globs['var']['font_style'])
        
    def bindings(self):
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_show_about']
                ,action   = self.gui.toggle
                )
        self.gui.btn_thd.action = self.show_third_parties
        self.gui.btn_lic.action = self.open_license_url
        self.gui.btn_eml.action = self.response_back

    # Написать письмо автору
    def response_back(self,event=None):
        sh.Email (email   = sh.email
                 ,subject = _('Concerning %s') % product
                 ).create()

    # Открыть веб-страницу с лицензией
    def open_license_url(self,event=None):
        objs.online()._url = sh.globs['license_url']
        objs.online().browse()

    # Отобразить информацию о лицензии третьих сторон
    def show_third_parties(self,event=None):
        self.parties.gui.show()



class SaveArticle:

    def __init__(self):
        self._html_types = ((_('Web-page'),'.htm')
                           ,(_('Web-page'),'.html')
                           ,(_('All files'),'*')
                           )
        self._txt_types  = ((_('Plain text (UTF-8)'),'.txt')
                           ,(_('All files'),'*')
                           )
        self.gui = gi.SaveArticle()
    
    #fix an extension for Windows
    def fix_ext(self,ext='.htm'):
        if not self.file.endswith(ext):
            self.file += ext

    def select(self,event=None):
        opt = self.gui.obj._get
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
        self.file = sg.dialog_save_file(filetypes=self._html_types)
        if self.file and objs.request()._html:
            self.fix_ext(ext='.htm')
            ''' We disable AskRewrite because the confirmation is
                already built in the internal dialog
            '''
            sh.WriteTextFile (file       = self.file
                             ,AskRewrite = False
                             ).write(objs._request._html)
        else:
            sh.log.append ('SaveArticle.view_as_html'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def raw_as_html(self):
        ''' Ключ 'html' может быть необходим для записи файла, которая
            производится в кодировке UTF-8, поэтому, чтобы полученная
            веб-страница нормально читалась, меняем кодировку вручную.
            Также меняем сокращенные гиперссылки на полные, чтобы они
            работали и в локальном файле.
        '''
        self.file = sg.dialog_save_file(filetypes=self._html_types)
        if self.file and objs.request()._html_raw:
            self.fix_ext(ext='.htm')
            #todo: fix remaining links to localhost
            sh.WriteTextFile (file       = self.file
                             ,AskRewrite = False
                             ).write(objs._request._html_raw.replace('charset=windows-1251"','charset=utf-8"').replace('<a href="M.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/M.exe?',sh.globs['var']['pair_root']).replace('<a href="m.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/m.exe?',sh.globs['var']['pair_root']))
        else:
            sh.log.append ('SaveArticle.raw_as_html'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def view_as_txt(self):
        self.file = sg.dialog_save_file(filetypes=self._txt_types)
        text = objs.webframe().text()
        if self.file and text:
            self.fix_ext(ext='.txt')
            sh.WriteTextFile (file       = self.file
                             ,AskRewrite = False
                             ).write(text.strip())
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
        self.gui = gi.Entry()
        self.bindings()
        self.reset()

    def bindings(self):
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_search_article_forward']
                ,action   = self.gui.close
                )
    
    def reset(self,event=None):
        self._pos    = -1
        self._first  = -1
        self._last   = -1
        self._search = ''
        ''' Plus: keeping old input
            Minus: searching old input after cancelling the search and
            searching again
            #self.clear()
        '''

    def clear(self,event=None):
        self.gui.obj.clear_text()

    def close(self,event=None):
        self.gui.close()

    def show(self,event=None):
        self.gui.show()

    def search(self):
        if not self._search:
            self.show()
            self._search = self.gui.widget.get().strip(' ').strip('\n').lower()
        return self._search

    def forward(self,event=None):
        pos = objs.blocks_db().search_forward (pos    = self._pos
                                              ,search = self.search()
                                              )
        if pos or pos == 0:
            objs.webframe()._pos = self._pos = pos
            objs._webframe.select()
            objs._webframe.shift_screen()
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
            self._first = \
            objs.blocks_db().search_forward (pos    = -1
                                            ,search = self.search()
                                            )
        return self._first

    def last(self):
        if self._last == -1:
            max_cell = objs._blocks_db.max_cell()
            if max_cell:
                self._last = \
                objs.blocks_db().search_backward (pos    = max_cell[2]+1
                                                 ,search = self.search()
                                                 )
            else:
                sh.log.append ('SearchArticle.last'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        return self._last

    def backward(self,event=None):
        if self.first():
            if self._pos == self._first:
                sg.Message (func    = 'SearchArticle.backward'
                           ,level   = _('INFO')
                           ,message = _('The end has been reached. Searching from the start.')
                           )
                result = self.last()
                if str(result).isdigit():
                    objs.webframe()._pos = self._pos = result
                    objs._webframe.select()
                    objs._webframe.shift_screen()
            else:
                pos = \
                objs.blocks_db().search_backward (pos    = self._pos
                                                 ,search = self.search()
                                                 )
                if str(pos).isdigit():
                    self._pos = pos
                    objs.webframe()._pos = pos
                    objs._webframe.select()
                    objs._webframe.shift_screen()
        else:
            sg.Message (func    = 'SearchArticle.backward'
                       ,level   = _('INFO')
                       ,message = _('Nothing has been found!')
                       )



class SpecSymbols:

    def __init__(self):
        self.gui = gi.SpecSymbols()
        self.buttons()
        self.bindings()
        
    def buttons(self):
        for i in range(len(sh.globs['var']['spec_syms'])):
            if i % 10 == 0:
                self.frame = sg.Frame (parent = self.gui.obj
                                      ,expand = True
                                      )
            ''' lambda сработает правильно только при моментальной
                упаковке, которая не поддерживается create_button
                (моментальная упаковка возвращает None вместо виджета),
                поэтому не используем эту функцию. По этой же причине
                нельзя привязать кнопкам '<Return>' и '<KP_Enter>',
                сработают только встроенные '<space>' и
                '<ButtonRelease-1>'.
                width и height нужны для Windows
            '''
            tk.Button (
                    master  = self.frame.widget
                   ,text    = sh.globs['var']['spec_syms'][i]
                   ,command = lambda i=i:objs.webframe().insert_sym(sh.globs['var']['spec_syms'][i])
                   ,width   = 2
                   ,height  = 2
                      ).pack (side   = 'left'
                             ,expand = True
                             )

    def bindings(self):
        sg.bind (obj      = self.gui.obj
                ,bindings = ['<Escape>'
                            ,sh.globs['var']['bind_spec_symbol']
                            ]
                ,action   = self.gui.close
                )



class History:

    def __init__(self):
        self.gui = gi.History()
        self.bindings()

    def bindings(self):
        sg.bind (obj      = self.gui.parent
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ,'<Escape>'
                            ]
                ,action = self.gui.toggle
                )
        sg.bind (obj      = self.gui.parent
                ,bindings = sh.globs['var']['bind_clear_history']
                ,action   = self.clear
                )
        ''' #note: the list is reversed, but we think it is still more
            intuitive when Home goes top and End goes bottom
        '''
        sg.bind (obj      = self.gui.parent
                ,bindings = '<Home>'
                ,action   = self.go_first
                )
        sg.bind (obj      = self.gui.parent
                ,bindings = '<End>'
                ,action   = self.go_last
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<<ListboxSelect>>'
                ,action   = self.go
                )
        sg.bind (obj      = self.gui
                ,bindings = sh.globs['var']['bind_copy_history']
                ,action   = self.gui.copy
                )

    def autoselect(self):
        self.gui.obj.clear_selection()
        item = str(objs.blocks_db()._articleid) + ' ► ' \
                                                + objs.request()._search
        self.gui.obj.set(item=item)

    def show(self,event=None):
        self.Active = True
        self.parent.show()

    def close(self,event=None):
        self.Active = False
        self.parent.close()

    def fill(self):
        searches = objs.blocks_db().searches()
        lst = []
        if searches:
            for item in searches:
                lst.append(str(item[0]) + ' ► ' + item[1])
            self.gui.obj.reset (lst   = lst
                               ,title = _('History')
                               )

    def update(self):
        self.fill()
        self.autoselect()

    def clear(self,event=None):
        objs.blocks_db().clear()
        self.gui.obj.clear()
        objs.webframe().reset()
        objs._webframe.search_article.obj.clear_text()
        objs.request().reset()

    def go_first(self,event=None):
        if self.gui.obj.lst:
            self.gui.obj.clear_selection()
            self.gui.obj.set(item=self.gui.obj.lst[0])
            self.go()
        else:
            sh.log.append ('History.go_first'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def go_last(self,event=None):
        if self.gui.obj.lst:
            self.gui.obj.clear_selection()
            self.gui.obj.set(item=self.gui.obj.lst[-1])
            self.go()
        else:
            sh.log.append ('History.go_last'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def go(self,event=None):
        result = self.gui.obj.get()
        result = result.split(' ► ')
        if len(result) == 2:
            objs.blocks_db()._articleid = int(result[0])
            result = objs._blocks_db.article()
            if result:
                objs._request._source = result[0]
                objs._request._search = result[1]
                objs._request._url    = result[2]
                objs.webframe().load_article()
            else:
                sh.log.append ('History.go'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sg.Message (func    = 'History.go'
                       ,level   = _('ERROR')
                       ,message = _('Wrong input data!')
                       )



class WebFrame:

    def __init__(self):
        self.values()
        self.gui = gi.WebFrame()
        self.widgets()
        self.bindings()
    
    # Вставить предыдущий запрос
    def insert_repeat_sign2(self,event=None):
        result = objs.blocks_db().prev_id()
        if result:
            old = objs._blocks_db._articleid
            objs._blocks_db._articleid = result
            result = objs._blocks_db.article()
            if result:
                sg.Clipboard().copy(result[1])
                self.gui.paste_search()
            else:
                sh.log.append ('WebFrame.insert_repeat_sign2'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
            objs._blocks_db._articleid = old
        else:
            sh.log.append ('WebFrame.insert_repeat_sign2'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    # Вставить текущий запрос
    def insert_repeat_sign(self,event=None):
        sg.Clipboard().copy(str(objs.request()._search))
        self.gui.paste_search()
        
    def reset(self):
        #'widget.reset' is already done in 'self.fill'
        welcome = pg.Welcome (url       = sh.globs['var']['pair_root']
                             ,st_status = len(objs.ext_dics()._dics)
                             ,product   = product
                             ,version   = version
                             )
        self.fill(welcome.run())
        self.update_buttons()
        self.title()

    def values(self):
        self._pos   = -1
        self._posn  = -1
        self._phdic = ''

    def widgets(self):
        self.about          = About        ()
        self.settings       = Settings     ()
        self.search_article = SearchArticle()
        self.spec_symbols   = SpecSymbols  ()
        self.save_article   = SaveArticle  ()
        self.history        = History      ()
        #cur
        self.about.parties.gui.close()
        self.about.gui.close()
        self.settings.gui.close()
        self.search_article.gui.close()
        self.spec_symbols.gui.close()
        self.save_article.gui.close()
        self.history.gui.close()

    def bindings(self):
        sg.bind (obj      = self.gui
                ,bindings = '<Motion>'
                ,action   = self.mouse_sel
                )
        sg.bind (obj      = self.gui
                ,bindings = '<Button-1>'
                ,action   = lambda x:self.go(Mouse=True)
                )
        ''' Key and mouse bindings must have different parents,
        otherwise, key bindings will not work, and mouse bindings
        (such as RMB) may fire up when not required. Keys must be
        bound to Top and mouse buttons - to specific widgets
        (Tkinterhtml widget, buttons on the button frame, etc.)
        Parents may be determined automatically, but this looks
        clumsy and unreliable. So I think it is better to hardcode
        mouse bindigs wherever possible and assume the config 
        provides for key bindigs only (or at least they are not
        to be bound to Top).
        '''
        sg.bind (obj      = self.gui
                ,bindings = '<Button-3>'
                ,action   = lambda x:self.go_alt(Mouse=True)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_copy_sel']
                            ,sh.globs['var']['bind_copy_sel_alt']
                            ]
                ,action   = self.copy_text
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_quit_now']
                            ,sh.globs['var']['bind_quit_now_alt']
                            ]
                ,action   = self.gui.close
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = ['<Return>'
                            ,'<KP_Enter>'
                            ]
                ,action   = self.go
                )
        #todo: do not iconify at <ButtonRelease-3>
        sg.bind (obj      = self.gui.search_field
                ,bindings = sh.globs['var']['bind_clear_search_field']
                ,action   = self.gui.search_field.clear_text
                )
        sg.bind (obj      = self.gui.search_field
                ,bindings = sh.globs['var']['bind_paste_search_field']
                ,action   = lambda e:self.gui.paste_search()
                )
        if sh.oss.win() or sh.oss.mac():
            sg.bind (obj      = self.gui.obj
                    ,bindings = '<MouseWheel>'
                    ,action   = self.mouse_wheel
                    )
        else:
            sg.bind (obj      = self.gui.obj
                    ,bindings = ['<Button 4>'
                                ,'<Button 5>'
                                ]
                    ,action   = self.mouse_wheel
                    )
        # Перейти на предыдущую/следующую статью
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_go_back']
                ,action   = self.go_back
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_go_forward']
                ,action   = self.go_forward
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col1_down']
                ,action   = lambda e:self.move_next_section(col_no=0)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col1_up']
                ,action   = lambda e:self.move_prev_section(col_no=0)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col2_down']
                ,action   = lambda e:self.move_next_section(col_no=1)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col2_up']
                ,action   = lambda e:self.move_prev_section(col_no=1)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col3_down']
                ,action   = lambda e:self.move_next_section(col_no=2)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_col3_up']
                ,action   = lambda e:self.move_prev_section(col_no=2)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Left>'
                ,action   = self.move_left
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Right>'
                ,action   = self.move_right
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Down>'
                ,action   = self.move_down
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Up>'
                ,action   = self.move_up
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Home>'
                ,action   = self.move_line_start
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<End>'
                ,action   = self.move_line_end
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Control-Home>'
                ,action   = self.move_text_start
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Control-End>'
                ,action   = self.move_text_end
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Prior>'
                ,action   = self.move_page_up
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = '<Next>'
                ,action   = self.move_page_down
                )
        # Дополнительные горячие клавиши
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_search_article_forward']
                ,action   = self.search_article.forward
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_search_article_backward']
                ,action   = self.search_article.backward
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_re_search_article']
                ,action   = self.search_reset
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_reload_article']
                            ,sh.globs['var']['bind_reload_article_alt']
                            ]
                ,action   = self.reload
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_save_article']
                            ,sh.globs['var']['bind_save_article_alt']
                            ]
                ,action   = self.save_article.select
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_show_about']
                ,action   = self.about.gui.toggle
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history']
                            ]
                ,action   = self.history.gui.toggle
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ]
                ,action   = self.history.gui.toggle
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_open_in_browser']
                            ,sh.globs['var']['bind_open_in_browser_alt']
                            ]
                ,action   = self.open_in_browser
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_copy_url']
                ,action   = self.copy_block_url
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_copy_article_url']
                ,action   = self.copy_url
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_spec_symbol']
                ,action   = self.spec_symbols.gui.show
                )
        sg.bind (obj      = self.gui.search_field
                ,bindings = '<Control-a>'
                ,action   = self.gui.search_field.select_all
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_define']
                ,action   = lambda e:self.define(Selected=True)
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_prev_pair']
                            ,sh.globs['var']['bind_prev_pair_alt']
                            ]
                ,action   = self.gui.men_pair.set_prev
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_next_pair']
                            ,sh.globs['var']['bind_next_pair_alt']
                            ]
                ,action   = self.gui.men_pair.set_next
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_settings']
                            ,sh.globs['var']['bind_settings_alt']
                            ]
                ,action   = self.settings.gui.show
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_toggle_view']
                            ,sh.globs['var']['bind_toggle_view_alt']
                            ]
                ,action   = self.toggle_view
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_toggle_history']
                            ,sh.globs['var']['bind_toggle_history_alt']
                            ]
                ,action   = self.history.gui.toggle
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_clear_history']
                ,action   = self.history.clear
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_toggle_alphabet']
                ,action   = self.toggle_alphabet
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_toggle_block']
                ,action   = self.toggle_block
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_toggle_priority']
                ,action   = self.toggle_priority
                )
        sg.bind (obj      = self.gui.btn_hist
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.history.clear
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_print']
                ,action   = self.print
                )
        sg.bind (obj      = self.gui.obj
                ,bindings = sh.globs['var']['bind_toggle_sel']
                ,action   = self.toggle_sel
                )
        # Set config bindings
        self.gui.btn_hist.hint = _('Show history') \
                + '\n'   + sh.globs['var']['bind_toggle_history'] \
                + ', '   + sh.globs['var']['bind_toggle_history_alt'] \
                + '\n\n' + _('Clear history') \
                + '\n'   + sh.globs['var']['bind_clear_history'] \
                + ', <ButtonRelease-3>'
        self.gui.btn_abot._bindings = sh.globs['var']['bind_show_about']
        self.gui.btn_alph._bindings = sh.globs['var']['bind_toggle_alphabet']
        self.gui.btn_blok._bindings = sh.globs['var']['bind_toggle_block']
        self.gui.btn_brws._bindings = [sh.globs['var']['bind_open_in_browser']
                                      ,sh.globs['var']['bind_open_in_browser_alt']
                                      ]
        self.gui.btn_cler._bindings = sh.globs['var']['bind_clear_search_field']
        self.gui.btn_expl._bindings = sh.globs['var']['bind_define']
        self.gui.btn_next._bindings = sh.globs['var']['bind_go_forward']
        self.gui.btn_past._bindings = '<Control-v>'
        self.gui.btn_prev._bindings = sh.globs['var']['bind_go_back']
        self.gui.btn_prnt._bindings = sh.globs['var']['bind_print']
        self.gui.btn_quit._bindings = [sh.globs['var']['bind_quit_now']
                                      ,sh.globs['var']['bind_quit_now_alt']
                                      ]
        self.gui.btn_prio._bindings = sh.globs['var']['bind_toggle_priority']
        self.gui.btn_reld._bindings = [sh.globs['var']['bind_reload_article']
                                      ,sh.globs['var']['bind_reload_article_alt']
                                      ]
        self.gui.btn_rep1._bindings = sh.globs['var']['repeat_sign']
        self.gui.btn_rep2._bindings = sh.globs['var']['repeat_sign2']
        self.gui.btn_save._bindings = [sh.globs['var']['bind_save_article']
                                      ,sh.globs['var']['bind_save_article_alt']
                                      ]
        self.gui.btn_sets._bindings = [sh.globs['var']['bind_settings']
                                      ,sh.globs['var']['bind_settings_alt']
                                      ]
        self.gui.btn_spec._bindings = sh.globs['var']['bind_spec_symbol']
        self.gui.btn_srch._bindings = sh.globs['var']['bind_re_search_article']
        self.gui.btn_trns._bindings = ['<Return>','<KP_Enter>']
        self.gui.btn_view._bindings = [sh.globs['var']['bind_toggle_view']
                                      ,sh.globs['var']['bind_toggle_view_alt']
                                      ]
        ''' Reset 'hint' for those buttons which bindings have changed
            (in order to show these bindings in tooltip)
        '''
        self.gui.btn_abot.set_hint()
        self.gui.btn_alph.set_hint()
        self.gui.btn_blok.set_hint()
        self.gui.btn_brws.set_hint()
        self.gui.btn_cler.set_hint()
        self.gui.btn_expl.set_hint()
        self.gui.btn_hist.set_hint()
        self.gui.btn_next.set_hint()
        self.gui.btn_past.set_hint()
        self.gui.btn_prev.set_hint()
        self.gui.btn_prio.set_hint()
        self.gui.btn_prnt.set_hint()
        self.gui.btn_quit.set_hint()
        self.gui.btn_reld.set_hint()
        self.gui.btn_rep1.set_hint()
        self.gui.btn_rep2.set_hint()
        self.gui.btn_save.set_hint()
        self.gui.btn_sets.set_hint()
        self.gui.btn_spec.set_hint()
        self.gui.btn_srch.set_hint()
        self.gui.btn_trns.set_hint()
        self.gui.btn_view.set_hint()
        # Set controller actions
        self.gui.btn_abot.action = self.about.gui.show
        self.gui.btn_clip.action = self.watch_clipboard
        self.gui.btn_expl.action = lambda x:self.define(Selected=False)
        self.gui.btn_prnt.action = self.print
        self.gui.btn_brws.action = self.open_in_browser
        self.gui.btn_save.action = self.save_article.select
        self.gui.btn_srch.action = self.search_reset
        self.gui.btn_reld.action = self.reload
        self.gui.btn_hist.action = self.history.gui.toggle
        self.gui.btn_next.action = self.go_forward
        self.gui.btn_prev.action = self.go_back
        self.gui.btn_alph.action = self.toggle_alphabet
        self.gui.btn_prio.action = self.toggle_priority
        self.gui.btn_blok.action = self.toggle_block
        self.gui.btn_view.action = self.toggle_view
        self.gui.btn_sets.action = self.settings.gui.toggle
        self.gui.men_cols.action = self.set_columns
        self.gui.btn_spec.action = self.spec_symbols.gui.show
        self.gui.btn_rep2.action = self.insert_repeat_sign2
        self.gui.btn_rep1.action = self.insert_repeat_sign
        self.gui.btn_past.action = self.gui.paste_search
        self.gui.btn_cler.action = self.gui.search_field.clear_text
        self.gui.btn_trns.action = self.go
        # Reset OptionMenus
        self.gui.men_pair.reset (items  = pairs
                                ,action = self.set_lang
                                )
        self.gui.men_srcs.reset (items   = sources
                                ,action  = self.set_source
                                )
    def title(self,arg=None):
        if not arg:
            arg = sh.List(lst1=[product,version]).space_items()
        self.gui.title(arg)

    def text(self,event=None):
        # We will have a Segmentation Fault on empty input
        if objs.request()._html:
            return self.gui.widget.text('text')

    def mouse_sel(self,event=None):
        self.get_pos(event=event)
        self.select()

    def get_pos(self,event=None):
        if event:
            pos = -1
            try:
                node1,node2 = self.gui.widget.node(True,event.x,event.y)
                pos         = self.gui.widget.text('offset',node1,node2)
            # Need more than 0 values to unpack
            except ValueError:
                pass
                '''
                # Too frequent
                sh.log.append ('WebFrame.get_pos'
                              ,_('WARNING')
                              ,_('Unable to get the position!')
                              )
                '''
            if str(pos).isdigit():
                Selectable = objs.blocks_db().Selectable
                objs._blocks_db.Selectable = False
                result = objs._blocks_db.block_pos(pos=pos)
                if result:
                    self._posn = pos
                if Selectable:
                    objs._blocks_db.Selectable = True
                    result = objs._blocks_db.block_pos(pos=pos)
                    if result:
                        self._pos = pos
                else:
                    self._pos = self._posn
                objs._blocks_db.Selectable = Selectable

    def _select(self,result):
        try:
            self.gui.widget.tag ('delete','selection')
            self.gui.widget.tag ('add','selection',result[0]
                                ,result[2],result[1],result[3]
                                )
            self.gui.widget.tag ('configure','selection','-background'
                                ,sh.globs['var']['color_terms_sel_bg']
                                )
            self.gui.widget.tag ('configure','selection','-foreground'
                                ,sh.globs['var']['color_terms_sel_fg']
                                )
        except tk.TclError:
            pass
            '''
            sh.log.append ('WebFrame._select'
                          ,_('WARNING')
                          ,_('Unable to set selection!')
                          )
            '''
        #cur
        '''
        #No such node: ''
        print('result[0]: "%s"' % str(result[0])) #todo: del
        print('result[1]: "%s"' % str(result[1])) #todo: del
        print('result[2]: "%s"' % str(result[2])) #todo: del
        print('result[3]: "%s"' % str(result[3])) #todo: del
        self.gui.widget.tag ('delete','selection')
        self.gui.widget.tag ('add','selection',result[0]
                            ,result[2],result[1],result[3]
                            )
        self.gui.widget.tag ('configure','selection','-background'
                            ,sh.globs['var']['color_terms_sel_bg']
                            )
        self.gui.widget.tag ('configure','selection','-foreground'
                            ,sh.globs['var']['color_terms_sel_fg']
                            )
        
        '''
    
    def select(self):
        result = objs.blocks_db().selection(pos=self._pos)
        if result:
            objs.blocks_db().set_bookmark(pos=self._pos)
            self._select(result)
        else:
            pass
            '''
            # Too frequent
            sh.log.append ('WebFrame.select'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            '''

    def shift_x(self,bbox1,bbox2):
        _width = self.gui.width()
        result = objs.blocks_db().max_bbox()
        if _width and result:
            max_bbox = result[0]
            page1_no = int(bbox1 / _width)
            page2_no = int(bbox2 / _width)

            if page1_no == page2_no:
                page_bbox = page1_no * _width
                self.gui.scroll_x (bbox     = page_bbox
                                  ,max_bbox = max_bbox
                                  )
            else:
                page1_bbox = page1_no * _width
                page2_bbox = page2_no * _width
                if page2_bbox - page1_bbox > _width:
                    delta = 0
                    sh.log.append ('WebFrame.shift_x'
                                  ,_('WARNING')
                                  ,_('The column is too wide to be fully shown')
                                  )
                else:
                    delta = bbox2 - page2_bbox
                self.gui.scroll_x (bbox     = page1_bbox + delta
                                  ,max_bbox = max_bbox
                                  )
        else:
            sh.log.append ('WebFrame.shift_x'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def shift_y(self,bboy1,bboy2):
        _height = self.gui.height()
        result  = objs.blocks_db().max_bboy()
        if _height and result:
            max_bboy = result[0]
            page1_no = int(bboy1 / _height)
            page2_no = int(bboy2 / _height)
            if page1_no == page2_no:
                page_bboy = page1_no * _height
                self.gui.scroll_y (bboy     = page_bboy
                                  ,max_bboy = max_bboy
                                  )
            else:
                page1_bboy = page1_no * _height
                page2_bboy = page2_no * _height
                if page2_bboy - page1_bboy > _height:
                    delta = 0
                    sh.log.append ('WebFrame.shift_y'
                                  ,_('WARNING')
                                  ,_('The row is too wide to be fully shown')
                                  )
                else:
                    delta = bboy2 - page2_bboy
                self.gui.scroll_y (bboy     = page1_bboy + delta
                                  ,max_bboy = max_bboy
                                  )
        else:
            sh.log.append ('WebFrame.shift_y'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' In order to shift the screen correctly, we need to:
        - make visible the minimum BBOY1 and the maximum BBOY2 of
          the current row;
          - if BBOY2 - BBOY1 exceeds the current height, we should
            scroll to BBOY1 only
        - make visible the minimum BBOX1 and the maximum BBOX2 of
          the current column;
          - if BBOX2 - BBOX1 exceeds the current width, we should
            scroll to BBOX1 only
    '''
    def shift_screen(self):
        result1 = objs.blocks_db().block_pos(pos=self._pos)
        if result1:
            result2 = objs._blocks_db.bbox_limits(col_no=result1[4])
            result3 = objs._blocks_db.bboy_limits(row_no=result1[3])
            if result2 and result3:
                self.shift_x (bbox1 = result2[0]
                             ,bbox2 = result2[1]
                             )
                self.shift_y (bboy1 = result3[0]
                             ,bboy2 = result3[1]
                             )
            else:
                sh.log.append ('WebFrame.shift_screen'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.shift_screen'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def fill(self,code=None):
        self.gui.widget.reset()
        if not code:
            code = '<html><body><h1>' + _('Nothing has been loaded yet.') + '</h1></body></html>'
        try:
            self.gui.widget.parse(code)
            ''' This should not happen now as we strip out non-supported
                characters
            '''
        except tk._tkinter.TclError:
            sg.Message (func    = 'WebFrame.fill'
                       ,level   = _('ERROR')
                       ,message = _('Cannot parse HTML code!\n\nProbably, some symbols are not supported by Tcl.')
                       )
            # Othewise, we will have a segmentation fault here
            self.reset()
            objs.request().reset()

    def load_article(self):
        ''' #note: each time the contents of the current page is changed
            (e.g., due to prioritizing), bookmarks must be deleted.
        '''
        timer = sh.Timer(func_title='WebFrame.load_article')
        timer.start()
        # Do not allow selection positions from previous articles
        self._pos = -1
        articleid = objs.blocks_db().present (source = objs.request()._source
                                             ,title  = objs._request._search
                                             ,url    = objs._request._url
                                             )
        if articleid:
            sh.log.append (func    = 'WebFrame.load_article'
                          ,level   = _('INFO')
                          ,message = _('Load article No. %d from memory')\
                                     % articleid
                          )
            objs._blocks_db._articleid = articleid
            self.get_bookmark()
            page = None
        else:
            # None skips the autoincrement
            data = (None                  # (00) ARTICLEID
                   ,objs._request._source # (01) SOURCE
                   ,objs._request._search # (02) TITLE
                   ,objs._request._url    # (03) URL
                   ,self._pos             # (04) BOOKMARK
                   )
            objs._blocks_db.fill_articles(data=data)
            
            objs._blocks_db._articleid = objs._blocks_db.max_articleid()
            
            ptimer = sh.Timer(func_title='WebFrame.load_article (Page)')
            ptimer.start()
            page = pg.Page (source       = objs._request._source
                           ,lang         = objs._request._lang
                           ,search       = objs._request._search
                           ,url          = objs._request._url
                           ,win_encoding = sh.globs['var']['win_encoding']
                           ,ext_dics     = objs.ext_dics()
                           ,timeout      = sh.globs['int']['timeout']
                           #,file        = '/home/pete/tmp/ars/random fury.txt'
                           #,file        = '/home/pete/tmp/ars/lottery.txt'
                           #,file        = '/home/pete/tmp/ars/таратайка.txt'
                           #,file        = '/home/pete/tmp/ars/painting.txt'
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
                           #,file        = '/home/pete/tmp/ars/œuf.txt'
                           #,file        = '/home/pete/tmp/ars/forward.txt'
                           #,file        = '/home/pete/tmp/ars/palate.txt'
                           #,file        = '/home/pete/tmp/ars/sdict_EnRu_full - cut (manual).txt'
                           #,file        = '/home/pete/tmp/ars/sdict_EnRu_full - cut (manual)2.txt'
                           #,file        = '/home/pete/tmp/ars/sdict_EnRu_full - cut (auto).txt'
                           #,file        = '/home/pete/tmp/ars/scheming.txt'
                           #,file        = '/home/pete/tmp/ars/work.txt'
                           #,file        = '/home/pete/tmp/ars/mayhem - phrases.html'
                           #,file        = '/home/pete/tmp/ars/block.txt'
                           )
            page.run()
            ptimer.end()
            #todo: #fix: assign this for already loaded articles too
            objs._request._page = page._page
            ''' #note: #todo: 'Page' returns '_html_raw' for online
                pages only; this value can be separated for
                online & offline sources after introducing sub-sources
                instead of relying on _('All')
            '''
            objs._request._html_raw = page._html_raw
            
            tags = tg.Tags (text      = objs._request._page
                           ,source    = objs._request._source
                           ,pair_root = sh.globs['var']['pair_root']
                           )
            tags.run()

            elems = el.Elems (blocks    = tags._blocks
                             ,articleid = objs._blocks_db._articleid
                             )
            elems.run()

            objs._blocks_db.fill_blocks(elems._data)
            
            ph_terma = el.PhraseTerma (dbc       = objs._blocks_db.dbc
                                      ,articleid = objs._blocks_db._articleid
                                      )
            ph_terma.run()
            
            ''' The order of parts of speech must be changed only for
                new articles and after changing settings (Settings.apply)
            '''
            # todo (?) insert SPEECHPR in Elems instead of updating
            objs.logic().prioritize_speech()
            
        self._phdic = sh.Input (val        = objs._blocks_db.phrase_dic()
                               ,func_title = 'WebFrame.load_article'
                               ,Silent     = True
                               ).not_none()
        data = objs._blocks_db.assign_bp ()

        bp = cl.BlockPrioritize (data       = data
                                ,blacklist  = objs.blacklist()
                                ,prioritize = objs.prioritize()
                                ,Block      = objs._request.Block
                                ,Prioritize = objs._request.Prioritize
                                ,phrase_dic = self._phdic
                                )
        bp.run()
        objs._blocks_db.update(query=bp._query)

        dics = objs._blocks_db.dics(Block=0)
        ''' #note: if an article comprises only 1 dic/wform, this is
            usually a dictionary + terms from the 'Phrases' section
            Do not rely on the number of wforms; large articles like
            'centre' may have only 1 wform (and a plurality of dics)
        '''
        
        if not dics \
        or dics and len(dics) == 1 \
        or page and page.HasLocal \
        or not self._phdic:
            # or check 'objs._request._search' by pattern '\d+ фраз'
            objs._request.SpecialPage = True
        else:
            # Otherwise, 'SpecialPage' will be inherited
            objs._request.SpecialPage = False

        self.update_columns()
        
        SortTerms = objs._request.SortTerms \
                    and not objs._request.SpecialPage
        objs._blocks_db.reset (cols      = objs._request._cols
                              ,SortRows  = objs._request.SortRows
                              ,SortTerms = SortTerms
                              )
        objs._blocks_db.unignore()
        objs._blocks_db.ignore()
        
        data = objs._blocks_db.assign_cells()

        if objs._request._cols and objs._request._cols[0] == 'speech':
            ExpandAbbr = True
        else:
            ExpandAbbr = False
        
        cells = cl.Cells (data       = data
                         ,cols       = objs._request._cols
                         ,collimit   = objs._request._collimit
                         ,phrase_dic = self._phdic
                         ,Reverse    = objs._request.Reverse
                         ,ExpandAbbr = ExpandAbbr
                         )
        cells.run()
        
        cells.dump(blocks_db=objs._blocks_db)
        
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
        pos  = cl.Pos (data     = data
                      ,raw_text = self.text()
                      )
        pos.run()
        objs._blocks_db.update(query=pos._query)

        pages = cl.Pages (obj    = objs.webframe()
                         ,blocks = pos._blocks
                         )
        pages.run()
        objs._blocks_db.update(query=pages._query)
        
        self.title(arg=objs._request._search)
        if self._pos >= 0:
            self.select()
            self.shift_screen()
        else:
            result = objs._blocks_db.start()
            if str(result).isdigit():
                self._pos = result
                self.select()
            else:
                sh.log.append ('WebFrame.load_article'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
        ''' Empty article is not added either to DB or history, so we
            just do not clear the search field to be able to correct
            the typo.
        '''
        if pages._blocks:
            self.gui.search_field.clear_text()
        self.history.update()
        self.search_article.reset()
        self.update_buttons()
        timer.end()

        '''
        objs._blocks_db.dbc.execute ('select SPEECHPR,SPEECHA,TYPE,TEXT\
                                      from BLOCKS where ARTICLEID = ?\
                                      and POS2 > POS1'
                                    ,(objs._blocks_db._articleid,)
                                    )
        objs._blocks_db.print (Selected=1,Shorten=1,MaxRows=50
                              ,mode='BLOCKS'
                              )
        '''
        
        '''
        objs._blocks_db.dbc.execute ('select ARTICLEID,CELLNO,NO,TYPE\
                                            ,TEXT from BLOCKS \
                                      where BLOCK = 0 and IGNORE = 0 \
                                      and POS1 < POS2 \
                                      order by ARTICLEID,CELLNO,NO'
                                    )
        objs._blocks_db.print(Selected=1,Shorten=1,MaxRow=18,MaxRows=150)
        '''
        
        '''
        objs._blocks_db.dbc.execute ('select CELLNO,NO,DICA,WFORMA\
                                            ,SPEECHA,TYPE,TEXT \
                                      from BLOCKS where ARTICLEID = ? \
                                      and BLOCK = 0 and IGNORE = 0 \
                                      and POS1 < POS2 \
                                      order by CELLNO,NO'
                                    ,(objs._blocks_db._articleid,)
                                    )
        objs._blocks_db.print (Selected=1,Shorten=1
                              ,MaxRow=14,MaxRows=150
                              )
        '''
    
    # Select either the search string or the URL
    def go(self,event=None,Mouse=False):
        if Mouse:
            if objs.blocks_db().Selectable:
                objs._blocks_db.Selectable = False
                result = objs._blocks_db.block_pos(pos=self._posn)
                objs._blocks_db.Selectable = True
                if result and result[8] == 'dic' \
                and result[6] != self._phdic:
                    ''' Variants:
                        1) (current) A LM click on:
                           1) A common dictionary - prioritize
                           2) A prioritized dictionary - increase
                              priority
                           A RM click on:
                           1) A prioritized dictionary - unprioritize
                           2) A blocked dictionary - unblock
                           3) A common dictionary - block
                        or:
                        2) (easy, LM-only) A LM click on:
                           1) A common dictionary - prioritize
                           2) A prioritized dictionary - unprioritize
                           3) A blocked dictionary - unblock
                    '''
                    if result[6] in objs.blacklist():
                        objs.logic().unblock_dic(dic=result[6])
                    else:
                        objs.logic().prioritize_dic(dic=result[6])
                    objs._blocks_db.delete_bookmarks()
                    self.load_article()
                else:
                    self.go_url()
            else:
                self.go_url()
        else:
            search = self.gui.search_field.widget.get().strip('\n').strip(' ')
            if search == '':
                self.go_url()
            elif search == sh.globs['var']['repeat_sign']:
                self.insert_repeat_sign()
            elif search == sh.globs['var']['repeat_sign2']:
                self.insert_repeat_sign2()
            else:
                objs._request._search = search
                self.go_search()

    # Follow the URL of the current block
    def go_url(self,event=None):
        if not objs.request().MouseClicked:
            url = objs.blocks_db().url(pos=self._pos)
            if url:
                objs._request._search = objs._blocks_db.text(pos=self._pos)
                objs._request._url    = url
                sh.log.append ('WebFrame.go_url'
                              ,_('INFO')
                              ,_('Open link: %s') % objs._request._url
                              )
                self.load_article()
            # Do not warn when there are no articles yet
            elif objs._blocks_db._articleid == 0:
                sh.log.append ('WebFrame.go_url'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
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

    def set_source(self,event=None):
        objs.request()._source = sources[self.gui.men_srcs.index]
        sh.log.append ('WebFrame.set_source'
                      ,_('INFO')
                      ,_('Set source to "%s"') % objs._request._source
                      )
        self.load_article()

    def get_url(self):
        #note: encoding must be UTF-8 here
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

    #todo: move 'move_*' procedures to Moves class
    # Перейти на 1-й термин текущей строки
    def move_line_start(self,event=None):
        result = objs.blocks_db().line_start(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_line_start'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на последний термин текущей строки
    def move_line_end(self,event=None):
        result = objs.blocks_db().line_end(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_line_end'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Go to the 1st (non-)selectable block
    def move_text_start(self,event=None):
        result = objs.blocks_db().start()
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_text_start'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на последний термин статьи
    def move_text_end(self,event=None):
        result = objs.blocks_db().end()
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_text_end'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на страницу вверх
    def move_page_up(self,event=None):
        result = objs.blocks_db().selection(pos=self._pos)
        height = self.gui.height()
        if result and height:
            result = objs.blocks_db().page_up (bboy   = result[6]
                                              ,height = height
                                              )
            if str(result).isdigit():
                self._pos = result
                self.select()
                self.shift_screen()

    # Перейти на страницу вниз
    def move_page_down(self,event=None):
        result = objs.blocks_db().selection(pos=self._pos)
        height = self.height()
        if result and height:
            result = objs.blocks_db().page_down (bboy   = result[6]
                                                ,height = height
                                                )
            if str(result).isdigit():
                self._pos = result
                self.select()
                self.shift_screen()

    # Перейти на предыдущий термин
    def move_left(self,event=None):
        result = objs.blocks_db().left(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_left'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на следующий термин
    def move_right(self,event=None):
        result = objs.blocks_db().right(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_right'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на строку вниз
    def move_down(self,event=None):
        result = objs.blocks_db().down(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_down'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Перейти на строку вверх
    def move_up(self,event=None):
        result = objs.blocks_db().up(pos=self._pos)
        if str(result).isdigit():
            self._pos = result
            self.select()
            self.shift_screen()
        else:
            sh.log.append ('WebFrame.move_up'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )

    # Задействование колеса мыши для пролистывания экрана
    def mouse_wheel(self,event):
        ''' #todo: fix: too small delta in Windows
            В Windows XP delta == -120, однако, в других версиях оно
            другое
        '''
        if event.num == 5 or event.delta < 0:
            if sh.oss.lin():
                self.move_page_down()
            else:
                self.move_down()
            ''' В Windows XP delta == 120, однако, в других версиях оно
                другое
            '''
        if event.num == 4 or event.delta > 0:
            if sh.oss.lin():
                self.move_page_up()
            else:
                self.move_up()
        return 'break'

    # Следить за буфером обмена
    def watch_clipboard(self,event=None):
        if objs.request().CaptureHotkey:
            objs._request.CaptureHotkey = False
        else:
            objs._request.CaptureHotkey = True
        self.update_buttons()

    # Открыть URL текущей статьи в браузере
    def open_in_browser(self,event=None):
        objs.online()._url = objs.request()._url
        objs.online().browse()

    # Скопировать текст текущего блока
    def copy_text(self,event=None):
        text = objs.blocks_db().text(pos=self._pos)
        if text:
            sg.Clipboard().copy(text)
            if sh.globs['bool']['Iconify']:
                sg.Geometry(parent=self.gui.obj).minimize()
        # Do not warn when there are no articles yet
        elif objs._blocks_db._articleid == 0:
            sh.log.append ('WebFrame.copy_text'
                          ,_('INFO')
                          ,_('Nothing to do!')
                          )
        else:
            sg.Message ('WebFrame.copy_text'
                       ,_('WARNING')
                       ,_('This block does not contain any text!')
                       )

    # Скопировать URL текущей статьи
    def copy_url(self,event=None):
        sg.Clipboard().copy(objs.request()._url)
        if sh.globs['bool']['Iconify']:
            sg.Geometry(parent=self.gui.obj).minimize()

    # Скопировать URL выделенного блока
    def copy_block_url(self,event=None):
        url = objs.blocks_db().url(pos=self._pos)
        if url:
            sg.Clipboard().copy(url)
            if sh.globs['bool']['Iconify']:
                sg.Geometry(parent=self.gui.obj).minimize()
        else:
            sg.Message ('WebFrame.copy_block_url'
                       ,_('WARNING')
                       ,_('This block does not contain a URL!')
                       )

    # Открыть веб-страницу с определением текущего термина
    # Selected: True: Выделенный термин; False: Название статьи
    def define(self,Selected=True):
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
            self.gui.btn_rep1.active()
        else:
            self.gui.btn_rep1.inactive()

        if searches and len(searches) > 1:
            self.gui.btn_rep2.active()
        else:
            self.gui.btn_rep2.inactive()

        if objs.blocks_db().prev_id(Loop=False):
            self.gui.btn_prev.active()
        else:
            self.gui.btn_prev.inactive()

        if objs.blocks_db().next_id(Loop=False):
            self.gui.btn_next.active()
        else:
            self.gui.btn_next.inactive()

        if objs.request().CaptureHotkey:
            self.gui.btn_clip.active()
        else:
            self.gui.btn_clip.inactive()

        if objs._request.Reverse:
            self.gui.btn_view.inactive()
            self.settings.gui.cb5.enable()
        else:
            self.gui.btn_view.active()
            self.settings.gui.cb5.disable()

        if not objs._request.SpecialPage and objs._request.SortTerms:
            self.gui.btn_alph.active()
            self.settings.gui.cb2.enable()
        else:
            self.gui.btn_alph.inactive()
            self.settings.gui.cb2.disable()

        if objs._request.Block and objs._blocks_db.blocked():
            self.gui.btn_blok.active()
            self.settings.gui.cb3.enable()
        else:
            self.gui.btn_blok.inactive()
            self.settings.gui.cb3.disable()

        if not objs._request.SpecialPage and objs._request.Prioritize \
        and objs._blocks_db.prioritized():
            self.gui.btn_prio.active()
            self.settings.gui.cb4.enable()
        else:
            self.gui.btn_prio.inactive()
            self.settings.gui.cb4.disable()

    # Перейти на предыдущий запрос
    def go_back(self,event=None):
        result = objs.blocks_db().prev_id()
        if result:
            objs._blocks_db._articleid = result
            result = objs._blocks_db.article()
            if result:
                objs._request._source = result[0]
                objs._request._search = result[1]
                objs._request._url    = result[2]
                self.load_article()
            else:
                sh.log.append ('WebFrame.go_back'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.go_back'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )

    # Перейти на следующий запрос
    def go_forward(self,event=None):
        result = objs.blocks_db().next_id()
        if result:
            objs._blocks_db._articleid = result
            result = objs._blocks_db.article()
            if result:
                objs._request._source = result[0]
                objs._request._search = result[1]
                objs._request._url    = result[2]
                self.load_article()
            else:
                sh.log.append ('WebFrame.go_forward'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.go_forward'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )

    # Confirm too long requests
    def control_length(self):
        Confirmed = True
        if len(objs.request()._search) >= 150:
            if not sg.Message (func    = 'WebFrame.control_length'
                              ,level   = _('QUESTION')
                              ,message = _('The request is long (%d symbols). Do you really want to send it?') \
                                         % len(objs._request._search)
                              ).Yes:
                Confirmed = False
        return Confirmed

    # SearchArticle
    def search_reset(self,event=None):
        self.search_article.reset()
        self.search_article.forward()

    def set_lang(self,event=None):
        objs.request()._lang = langs[self.gui.men_pair.index]
        sh.log.append ('WebFrame.set_lang'
                      ,_('INFO')
                      ,_('Set language to "%s"') % objs._request._lang
                      )

    def get_pair(self):
        return online_dic_urls[self.gui.men_pair.index]

    def set_columns(self,event=None):
        sh.log.append ('WebFrame.set_columns'
                      ,_('INFO')
                      ,str(self.gui.men_cols.choice)
                      )
        fixed = [col for col in objs.request()._cols \
                 if col != _('Do not set')
                ]
        objs._request._collimit = self.gui.men_col.choice + len(fixed)
        objs.blocks_db().delete_bookmarks()
        self.load_article()

    def reload(self,event=None):
        objs.blocks_db().clear_cur()
        self.load_article()

    # Вставить спец. символ в строку поиска
    def insert_sym(self,sym):
        self.gui.search_field.insert(pos='end',text=sym)
        if sh.globs['bool']['AutoCloseSpecSymbol']:
            self.spec_symbols.gui.close()

    def toggle_view(self,event=None):
        if objs.request().Reverse:
            objs._request.Reverse = False
        else:
            objs._request.Reverse = True
        objs.blocks_db().delete_bookmarks()
        self.load_article()

    def toggle_alphabet(self,event=None):
        if objs.request().SortTerms:
            objs._request.SortTerms = False
        else:
            objs._request.SortTerms = True
        objs.blocks_db().delete_bookmarks()
        self.load_article()

    def toggle_block(self,event=None):
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
        objs.blocks_db().delete_bookmarks()
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
                tmp.write ('update BLOCKS set PRIORITY=0 where NO=%d;' \
                          % no
                          )
            tmp.write('commit;')
            query = tmp.getvalue()
            tmp.close()
            objs._blocks_db.update(query=query)

    def toggle_priority(self,event=None):
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
        objs.blocks_db().delete_bookmarks()
        self.load_article()

    def print(self,event=None):
        code = mh.HTML (data     = objs._blocks_db.fetch()
                       ,cols     = objs._request._cols
                       ,collimit = objs._request._collimit
                       ,Printer  = True
                       )._html
        if code:
            sh.WriteTextFile (file       = sh.objs.tmpfile(suffix='.htm'
                                                          ,Delete=0
                                                          )
                             ,AskRewrite = False
                             ).write(code)
            sh.Launch(target=sh.objs._tmpfile).auto()
        else:
            sh.log.append ('WebFrame.print'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Update a column number in GUI; adjust the column number (both
        logic and GUI) in special cases
    '''
    def update_columns(self):
        fixed = [col for col in objs.request()._cols \
                 if col != _('Do not set')
                ]
        if objs._request._collimit > len(fixed):
            ''' A dictionary from the 'Phrases' section usually has
                an 'original + translation' structure, so we need to
                switch off sorting terms and ensure that the number of
                columns is divisible by 2
            '''
            if objs._request.SpecialPage \
            and objs._request._collimit % 2 != 0:
                if objs._request._collimit == len(fixed) + 1:
                    objs._request._collimit += 1
                else:
                    objs._request._collimit -= 1
            non_fixed_len = objs._request._collimit - len(fixed)
            self.gui.men_cols.set(non_fixed_len)
            sh.log.append ('WebFrame.update_columns'
                          ,_('INFO')
                          ,_('Set the column limit to %d (%d in total)')\
                          % (non_fixed_len,objs._request._collimit)
                          )
        else:
            sg.Message (func    = 'WebFrame.update_columns'
                       ,level   = _('ERROR')
                       ,message = _('The condition "%s" is not observed!')\
                                  % '%d > %d' % (objs._request._collimit
                                                ,len(fixed)
                                                )
                       )

    def ignore_column(self,col_no):
        if len(objs.request()._cols) > col_no + 1:
            if objs._request._cols[col_no] == 'transc':
                sh.log.append ('WebFrame.ignore_column'
                              ,_('DEBUG')
                              ,_('Select column "%s" instead of "%s"')\
                              % (objs._request._cols[col_no]
                                ,objs._request._cols[col_no+1]
                                )
                              )
                col_no += 1
        return col_no
    
    # Перейти к следующему разделу столбца col_no
    def move_next_section(self,event=None,col_no=0):
        col_no  = self.ignore_column(col_no=col_no)
        result1 = objs.blocks_db().block_pos(pos=self._pos)
        result2 = objs._blocks_db.next_section (pos    = self._pos
                                               ,col_no = col_no
                                               )
        if result1 and result2:
            result3 = objs._blocks_db.next_col (row_no = result2[1]
                                               ,col_no = result1[4]
                                               )
            result4 = objs._blocks_db.next_col (row_no = result2[1]
                                               ,col_no = 0
                                               )
            if result3 or result4:
                if result4 and not result3:
                    pos = result4[0]
                else:
                    pos = result3[0]
                result = objs.blocks_db().block_pos_next(pos=pos)
                if result:
                    self._pos = result[0]
                    self.select()
                    self.shift_screen()
                else:
                    sh.log.append ('WebFrame.move_next_section'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('WebFrame.move_next_section'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.move_next_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    # Перейти к предыдущему разделу столбца col_no
    def move_prev_section(self,event=None,col_no=0):
        col_no  = self.ignore_column(col_no=col_no)
        result1 = objs.blocks_db().block_pos(pos=self._pos)
        result2 = objs._blocks_db.prev_section (pos    = self._pos
                                               ,col_no = col_no
                                               )
        if result1 and result2:
            result3 = objs._blocks_db.next_col (row_no = result2[1]
                                               ,col_no = result1[4]
                                               )
            result4 = objs._blocks_db.next_col (row_no = result2[1]
                                               ,col_no = 0
                                               )
            if result3 or result4:
                if result4 and not result3:
                    pos = result4[0]
                else:
                    pos = result3[0]
                result = objs.blocks_db().block_pos_next(pos=pos)
                if result:
                    self._pos = result[0]
                    self.select()
                    self.shift_screen()
                else:
                    sh.log.append ('WebFrame.move_prev_section'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('WebFrame.move_prev_section'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('WebFrame.move_prev_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def get_bookmark(self):
        result = objs.blocks_db().article()
        if result:
            if str(result[3]).isdigit():
                self._pos = result[3]
                sh.log.append ('WebFrame.get_bookmark'
                              ,_('DEBUG')
                              ,_('Load bookmark %d for article #%d') \
                              % (self._pos,objs._blocks_db._articleid)
                              )
            else:
                sh.log.append ('WebFrame.get_bookmark'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
        else:
            sh.log.append ('WebFrame.get_bookmark'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            result = objs._blocks_db.start()
            if str(result).isdigit():
                self._pos = result()
            else:
                sh.log.append ('WebFrame.get_bookmark'
                              ,_('WARNING')
                              ,_('Wrong input data!')
                              )
    
    def go_alt(self,event=None,Mouse=False):
        if Mouse:
            if objs.blocks_db().Selectable:
                objs._blocks_db.Selectable = False
                result = objs._blocks_db.block_pos(pos=self._posn)
                objs._blocks_db.Selectable = True
                if result and result[8] == 'dic' \
                and result[6] != self._phdic:
                    if result[6] in objs.prioritize():
                        objs.logic().unprioritize_dic(dic=result[6])
                    elif result[6] in objs.blacklist():
                        objs.logic().unblock_dic(dic=result[6])
                    else:
                        objs.logic().block_dic(dic=result[6])
                    objs._blocks_db.delete_bookmarks()
                    self.load_article()
                else:
                    self.copy_text()
            else:
                self.copy_text()
        else:
            self.copy_text()
    
    def toggle_sel(self,event=None):
        if objs.blocks_db().Selectable:
            objs.blocks_db().Selectable = False
            objs._blocks_db.delete_bookmarks()
            self.load_article()
        else:
            objs.blocks_db().Selectable = True
            objs._blocks_db.delete_bookmarks()
            self.load_article()



class Settings:

    def __init__(self):
        self.gui = gi.Settings()
        self.bindings()

    def block_settings(self,event=None):
        sg.Message (func    = 'Settings.block_settings'
                   ,level   = _('INFO')
                   ,message = _('Not implemented yet!')
                   )

    def priority_settings(self,event=None):
        sg.Message (func    = 'Settings.priority_settings'
                   ,level   = _('INFO')
                   ,message = _('Not implemented yet!')
                   )

    def apply(self,event=None):
        ''' Do not use 'gettext' to name internal types - this will make
            the program ~0,6s slower
        '''
        lst = [choice for choice in (self.gui.col1.choice
                                    ,self.gui.col2.choice
                                    ,self.gui.col3.choice
                                    ,self.gui.col4.choice
                                    ) \
               if choice != _('Do not set')
              ]
        ''' #note: The following assignment does not change the list:
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
                           ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                      % (str(self._cols[i])
                                        ,', '.join (_('Dictionaries')
                                                   ,_('Word forms')
                                                   ,_('Transcription')
                                                   ,_('Parts of speech')
                                                   )
                                        )
                           )
        if set(lst):
            self.gui.close()
            objs.request()._cols     = tuple(lst)
            objs._request.SortRows   = self.gui.cb1.get()
            objs._request.SortTerms  = self.gui.cb2.get()
            objs._request.Block      = self.gui.cb3.get()
            objs._request.Prioritize = self.gui.cb4.get()
            objs._request.Reverse    = self.gui.cb5.get()
            if objs._request.SortRows:
                self.prioritize_speech()
                objs.logic().prioritize_speech()
            else:
                objs.blocks_db().unprioritize_speech()
            objs.webframe().set_columns()
        else:
            #todo: do we really need this?
            sg.Message (func    = 'Settings.apply'
                       ,level   = _('WARNING')
                       ,message = _('At least one column must be set!')
                       )
    
    def bindings(self):
        self.gui.btn_aply.action = self.apply
        #todo: implement
        #selb.btn_blok.action = self.block_settings
        #self.btn_prio.action = self.priority_settings
        sg.bind (obj      = self.gui.obj
                ,bindings = [sh.globs['var']['bind_settings']
                            ,sh.globs['var']['bind_settings_alt']
                            ,'<Escape>'
                            ]
                ,action = self.gui.toggle
                )

    def prioritize_speech(self):
        objs.request()
        choices = (self.gui.sp1.choice,self.gui.sp2.choice
                  ,self.gui.sp3.choice,self.gui.sp4.choice
                  ,self.gui.sp5.choice,self.gui.sp6.choice
                  ,self.gui.sp7.choice
                  )
        for i in range(len(choices)):
            if choices[i] == _('Noun'):
                objs._request._pr_n = len(choices) - i
            elif choices[i] == _('Verb'):
                objs._request._pr_v = len(choices) - i
            elif choices[i] == _('Adjective'):
                objs._request._pr_adj = len(choices) - i
            elif choices[i] == _('Abbreviation'):
                objs._request._pr_abbr = len(choices) - i
            elif choices[i] == _('Adverb'):
                objs._request._pr_adv = len(choices) - i
            elif choices[i] == _('Preposition'):
                objs._request._pr_prep = len(choices) - i
            elif choices[i] == _('Pronoun'):
                objs._request._pr_pron = len(choices) - i
            else:
                sg.Message ('Settings.prioritize_speech'
                           ,_('ERROR')
                           ,_('Wrong input data: "%s"') % str(choices[i])
                           )



class Logic:
    
    def prioritize_speech(self):
        # This function takes ~0,07s on 'do'
        query_root = 'update BLOCKS set SPEECHPR = %d where SPEECHA = "%s" or SPEECHA = "%s"'
        query = ['begin']
        # Parts of speech here must be non-localized
        query.append (query_root
                     % (objs._request._pr_n,'Существительное','сущ.')
                     )
        query.append (query_root
                     % (objs._request._pr_v,'Глагол','гл.')
                     )
        query.append (query_root
                     % (objs._request._pr_adj,'Прилагательное','прил.')
                     )
        query.append (query_root
                     % (objs._request._pr_abbr,'Сокращение','сокр.')
                     )
        query.append (query_root
                     % (objs._request._pr_adv,'Наречие','нареч.')
                     )
        query.append (query_root
                     % (objs._request._pr_prep,'Предлог','предл.')
                     )
        query.append (query_root
                     % (objs._request._pr_pron,'Местоимение','мест.')
                     )
        query.append('commit;')
        query = ';'.join(query)
        objs.blocks_db().update(query=query)
    
    def prioritize_dic(self,dic=None):
        if dic:
            objs.prioritize()
            if dic in objs._prioritize:
                sh.log.append ('Logic.prioritize_dic'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                objs._prioritize.append(dic)
        else:
            sh.log.append ('Logic.prioritize_dic'
                          ,_('WARNING')
                          ,_('Empty input data!')
                          )
                          
    def unprioritize_dic(self,dic=None):
        if dic:
            if dic in objs.prioritize():
                objs._prioritize.remove(dic)
            else:
                sh.log.append ('Logic.unprioritize_dic'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.log.append ('Logic.unprioritize_dic'
                          ,_('WARNING')
                          ,_('Empty input data!')
                          )
    
    def block_dic(self,dic=None):
        if dic:
            objs.blacklist()
            if dic in objs._blacklist:
                sh.log.append ('Logic.block_dic'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
            else:
                objs._blacklist.append(dic)
        else:
            sh.log.append ('Logic.block_dic'
                          ,_('WARNING')
                          ,_('Empty input data!')
                          )
    
    def unblock_dic(self,dic=None):
        if dic:
            if dic in objs.blacklist():
                objs._blacklist.remove(dic)
            else:
                sh.log.append ('Logic.unblock_dic'
                              ,_('INFO')
                              ,_('Nothing to do!')
                              )
        else:
            sh.log.append ('Logic.unblock_dic'
                          ,_('WARNING')
                          ,_('Empty input data!')
                          )



class ThirdParties:
    
    def __init__(self):
        self.gui = gi.ThirdParties()
        file = sh.objs.pdir().add('third parties.txt')
        self._text = sh.ReadTextFile(file=file).get()
        self.gui.obj.insert(text=self._text)
        self.gui.obj.read_only()



objs = Objects()


if  __name__ == '__main__':
    sg.objs.start()

    timed_update()

    objs.webframe().reset()
    objs._webframe.gui.show()

    kl_mod.keylistener.cancel()

    sg.objs.end()
