#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinterhtml as th
import shared      as sh
import sharedGUI   as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

product = 'MClient'


class About:

    def __init__(self):
        self.Active = False
        self.type   = 'About'
        self.gui()
        
    def gui(self):
        self.obj    = sg.Top(sg.objs.root())
        self.widget = self.obj.widget
        self.frames()
        self.labels()
        self.buttons()
        self.bindings()
        self.icon()
        self.title()
        self.widget.focus_set()
        
    def title(self,text=None):
        if not text:
            text = _('About')
        self.obj.title(text)
    
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..'
                                              ,'resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
        
    def labels(self):
        self.label = sg.Label (parent = self.frame1
                              ,text   = _('Programming: Peter Sklyar, 2015-2018.\nVersion: %s\n\nThis program is free and opensource. You can use and modify it freely\nwithin the scope of the provisions set forth in GPL v.3 and the active legislation.\n\nIf you have any questions, requests, etc., please do not hesitate to contact me.\n') \
                                        % '0.0'
                              ,font   = 'Sans 14'
                              )
        
    def frames(self):
        self.frame1 = sg.Frame (parent = self
                               ,expand = 1
                               ,fill   = 'both'
                               ,side   = 'top'
                               )
        self.frame2 = sg.Frame (parent = self
                               ,expand = 1
                               ,fill   = 'both'
                               ,side   = 'left'
                               )
        self.frame3 = sg.Frame (parent = self
                               ,expand = 1
                               ,fill   = 'both'
                               ,side   = 'right'
                               )
    def buttons(self):
        # Лицензия
        self.btn_thd = sg.Button (parent = self.frame2
                                 ,text   = _('Third parties')
                                 ,hint   = _('Third-party licenses')
                                 ,side   = 'left'
                                 )
        self.btn_lic = sg.Button (parent = self.frame3
                                 ,text   = _('License')
                                 ,hint   = _('View the license')
                                 ,side   = 'left'
                                 )
        # Отправить письмо автору
        self.btn_eml = sg.Button (parent = self.frame3
                                 ,text   = _('Contact the author')
                                 ,hint   = _('Draft an email to the author')
                                 ,side   = 'right'
                                 )
    
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = self.close
                )

    def close(self,event=None):
        self.Active = False
        self.obj.close()

    def show(self,event=None):
        self.Active = True
        self.obj.show()

    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()



class ThirdParties:
    
    def __init__(self):
        self.gui()
        
    def gui(self):
        self.parent = sg.objs.new_top()
        sg.Geometry(parent=self.parent).set('800x600')
        self.obj = sg.TextBox(parent=self.parent)
        self.icon()
        self.title()
        self.obj.focus()
    
    def title(self,text=None):
        if not text:
            text = _('Third parties') + ':'
        self.parent.title(text)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..'
                                                 ,'resources'
                                                 ,'icon_64x64_mclient.gif'
                                                 )
                             )
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class SearchArticle:
    
    def __init__(self):
        self.gui()
        
    def gui(self):
        self.parent = sg.objs.new_top()
        self.obj    = sg.Entry(parent=self.parent)
        self.widget = self.obj.widget
        self.title()
        self.icon()
        self.bindings()
        self.obj.focus()
    
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = '<Escape>'
                ,action   = self.parent.close
                )
    
    def title(self,text=None):
        if not text:
            text = _('Enter a string to search:')
        self.parent.title(text)
    
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..'
                                                 ,'resources'
                                                 ,'icon_64x64_mclient.gif'
                                                 )
                             )
                             
    def show(self,event=None):
        self.obj.select_all()
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class SaveArticle:

    def __init__(self):
        self.Active = False
        self.type   = 'SaveArticle'
        self._items = [_('Save the current view as a web-page (*.htm)')
                      ,_('Save the original article as a web-page (*.htm)')
                      ,_('Save the article as plain text in UTF-8 (*.txt)')
                      ,_('Copy HTML code of the article to clipboard')
                      ,_('Copy the text of the article to clipboard')
                      ]
        self.gui()
        
    def gui(self):
        self.parent = sg.objs.new_top()
        self.obj    = sg.ListBox (parent   = self.parent
                                 ,Multiple = False
                                 ,lst      = self._items
                                 ,title    = _('Select an action:')
                                 )
        self.widget = self.obj.widget
        self.icon()

    def close(self,event=None):
        self.Active = False
        self.parent.close()

    def show(self,event=None):
        self.Active = True
        self.parent.show()
        
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..'
                                                 ,'resources'
                                                 ,'icon_64x64_mclient.gif'
                                                 )
                             )
                             
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()



class History:

    def __init__(self):
        self.Active = False
        self._icon  = sh.objs.pdir().add ('..'
                                         ,'resources'
                                         ,'icon_64x64_mclient.gif'
                                         )
        self.gui()

    def gui(self):
        self.parent = sg.objs.new_top()
        self.parent.widget.geometry('250x350')
        self.obj = sg.ListBox (parent          = self.parent
                              ,title           = _('History')
                              ,icon            = self._icon
                              ,SelectionCloses = False
                              ,SingleClick     = True
                              ,Composite       = True
                              )
        self.widget = self.obj.widget
        self.bindings()

    def bindings(self):
        sg.bind (obj      = self
                ,bindings = '<ButtonRelease-3>'
                ,action   = self.copy
                )
        sg.bind (obj      = self
                ,bindings = '<Escape>'
                ,action   = self.close
                )

    def show(self,event=None):
        self.Active = True
        self.parent.show()

    def close(self,event=None):
        self.Active = False
        self.parent.close()

    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()

    # Скопировать элемент истории
    def copy(self,event=None):
        sg.Clipboard().copy(self.obj.get())



class WebFrame:

    def __init__(self):
        self.values()
        self.gui()
        
    ''' Очистить строку поиска и вставить в нее заданный текст или
        содержимое буфера обмена
    '''
    def paste_search(self,event=None,text=None):
        self.search_field.clear_text()
        if text:
            self.search_field.insert(text=text)
        else:
            self.search_field.insert(text=sg.Clipboard().paste())
        return 'break'

    def values(self):
        self._shift  = 1
        self._border = 24
        self.icon_alphabet_off        = sh.objs.pdir().add ('..'
                                                           ,'resources'
                                                           ,'buttons'
                                                           ,'icon_36x36_alphabet_off.gif'
                                                           )
        self.icon_alphabet_on         = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_alphabet_on.gif'
                                                          )
        self.icon_block_off           = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_block_off.gif'
                                                          )
        self.icon_block_on            = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_block_on.gif'
                                                          )
        self.icon_clear_search_field  = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_clear_search_field.gif'
                                                          )
        self.icon_define              = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_define.gif'
                                                          )
        self.icon_go_back_off         = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_go_back_off.gif'
                                                          )
        self.icon_go_back             = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_go_back.gif'
                                                          )
        self.icon_go_forward_off      = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_go_forward_off.gif'
                                                          )
        self.icon_go_forward          = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_go_forward.gif'
                                                          )
        self.icon_go_search           = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_go_search.gif'
                                                          )
        self.icon_open_in_browser     = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_open_in_browser.gif'
                                                          )
        self.icon_paste               = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_paste.gif'
                                                          )
        self.icon_print               = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_print.gif'
                                                          )
        self.icon_priority_off        = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_priority_off.gif'
                                                          )
        self.icon_priority_on         = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_priority_on.gif'
                                                          )
        self.icon_quit_now            = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_quit_now.gif'
                                                          )
        self.icon_reload              = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_reload.gif'
                                                          )
        self.icon_repeat_sign_off     = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_repeat_sign_off.gif'
                                                          )
        self.icon_repeat_sign         = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_repeat_sign.gif'
                                                          )
        self.icon_repeat_sign2_off    = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_repeat_sign2_off.gif'
                                                          )
        self.icon_repeat_sign2        = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_repeat_sign2.gif'
                                                          )
        self.icon_save_article        = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_save_article.gif'
                                                          )
        self.icon_search_article      = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_search_article.gif'
                                                          )
        self.icon_settings            = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_settings.gif'
                                                          )
        self.icon_show_about          = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_show_about.gif'
                                                          )
        self.icon_spec_symbol         = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_spec_symbol.gif'
                                                          )
        self.icon_toggle_history      = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_toggle_history.gif'
                                                          )
        self.icon_toggle_view_hor     = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_toggle_view_hor.gif'
                                                          )
        self.icon_toggle_view_ver     = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_toggle_view_ver.gif'
                                                          )
        self.icon_watch_clipboard_off = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_watch_clipboard_off.gif'
                                                          )
        self.icon_watch_clipboard_on  = sh.objs._pdir.add ('..'
                                                          ,'resources'
                                                          ,'buttons'
                                                          ,'icon_36x36_watch_clipboard_on.gif'
                                                          )

    def gui(self):
        self.obj     = sg.objs.new_top(Maximize=True)
        self.frame   = sg.Frame (parent = self.obj
                                ,expand = 1
                                )
        self.bottom  = sg.Frame (parent = self.frame
                                ,expand = 0
                                ,side   = 'bottom'
                                )
        self.frame_y = sg.Frame (parent = self.frame
                                ,expand = 0
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        self.widget  = th.TkinterHtml(self.frame.widget)
        self.widget.pack(expand='1',fill='both')
        self.scrollbars()
        self.frame_panel()
        self.icon()
        self.title()
        self.bindings()
        self.search_field.focus_set()
        self.obj.widget.protocol("WM_DELETE_WINDOW",self.close)

    def frame_panel(self):
        ''' Do not mix 'self._panel' and 'self.bottom', otherwise, they
            can overlap each other.
        '''
        self._panel = sg.Frame (parent = self.bottom
                               ,expand = 0
                               ,fill   = 'x'
                               )
        # Canvas should be created within a frame
        self.canvas = sg.Canvas (parent = self._panel
                                ,expand = 0
                                )
        self.fr_but = sg.Frame (parent = self._panel
                               ,expand = 0
                               )
        
        # Поле ввода поисковой строки
        self.search_field = sg.Entry (parent    = self.fr_but
                                     ,Composite = True
                                     ,side      = 'left'
                                     ,ipady     = 5
                                     )
        self.draw_buttons()
        self.canvas.embed(obj=self.fr_but)
        ''' #todo: Updating idletasks will show ExtDic messages for too
            long, however, we need to update in order to set canvas
            dimensions correctly.
        '''
        sg.objs.root().widget.update_idletasks()
        height = self.fr_but.widget.winfo_height()
        width  = self.fr_but.widget.winfo_width()
        self.canvas.widget.config(width=self.obj.resolution()[0])
        self.canvas.widget.config(height=height)
        x2 = (width / 2)
        x1 = -x2
        y2 = (height / 2)
        y1 = -y2
        self.canvas.widget.config(scrollregion=(x1,y1,x2,y2))
        # The scrollbar is set at the end for some reason
        self.canvas.widget.xview_moveto(0)

    ''' Create buttons
        Bindings are indicated here only to set hints. In order to set
        bindings, use 'self.bindings'.
    '''
    def draw_buttons(self):
        # Кнопка для "чайников", заменяет Enter в search_field
        self.btn_trns = sg.Button (parent   = self.fr_but
                                  ,text     = _('Translate')
                                  ,hint     = _('Translate')
                                  ,inactive = self.icon_go_search
                                  ,active   = self.icon_go_search
                                  )

        # Кнопка очистки строки поиска
        self.btn_cler = sg.Button (parent   = self.fr_but
                                  ,text     = _('Clear')
                                  ,hint     = _('Clear search field')
                                  ,inactive = self.icon_clear_search_field
                                  ,active   = self.icon_clear_search_field
                                  )

        # Кнопка вставки
        self.btn_past = sg.Button (parent   = self.fr_but
                                  ,text     = _('Paste')
                                  ,hint     = _('Paste text from clipboard')
                                  ,inactive = self.icon_paste
                                  ,active   = self.icon_paste
                                  )
        # Кнопка вставки текущего запроса
        self.btn_rep1 = sg.Button (parent   = self.fr_but
                                  ,text     = '!'
                                  ,hint     = _('Paste current request')
                                  ,inactive = self.icon_repeat_sign_off
                                  ,active   = self.icon_repeat_sign
                                  )
        # Кнопка вставки предыдущего запроса
        self.btn_rep2 = sg.Button (parent   = self.fr_but
                                  ,text     = '!!'
                                  ,hint     = _('Paste previous request')
                                  ,inactive = self.icon_repeat_sign2_off
                                  ,active   = self.icon_repeat_sign2
                                  )
        # Кнопка для вставки спец. символов
        self.btn_spec = sg.Button (parent   = self.fr_but
                                  ,text     = _('Symbols')
                                  ,hint     = _('Paste a special symbol')
                                  ,inactive = self.icon_spec_symbol
                                  ,active   = self.icon_spec_symbol
                                  )
        self.men_srcs = sg.OptionMenu(parent=self.fr_but)
        # Выпадающий список с вариантами направлений перевода
        self.men_pair = sg.OptionMenu(parent=self.fr_but)
        self.men_cols = sg.OptionMenu (parent  = self.fr_but
                                      ,items   = (1,2,3,4,5,6,7,8,9,10)
                                      ,default = 4
                                      )
        ''' After text in optionmenus is reset, tkinter will grow these
            optionmenus and correspondingly shift widgets on the left
            to the left. To prevent this, we set the width of
            the optionmenus by the longest item.
        '''
        self.men_srcs.widget.config (width = len(max((_('All')
                                                     ,_('Online')
                                                     ,_('Offline')
                                                     )
                                                    )
                                                )
                                    )
        # All items of the 'pairs' sequence are of the same length
        self.men_pair.widget.config(width=11)
        self.men_cols.widget.config(width=2)
        # Кнопка настроек
        self.btn_sets = sg.Button (parent   = self.fr_but
                                  ,text     = _('Settings')
                                  ,hint     = _('Tune up view settings')
                                  ,inactive = self.icon_settings
                                  ,active   = self.icon_settings
                                  )
        # Кнопка изменения вида статьи
        self.btn_view = sg.Button (parent   = self.fr_but
                                  ,text     = _('Toggle view')
                                  ,hint     = _('Toggle the article view mode')
                                  ,inactive = self.icon_toggle_view_ver
                                  ,active   = self.icon_toggle_view_hor
                                  )
        # Кнопка включения/отключения режима блокировки словарей
        self.btn_blok = sg.Button (parent   = self.fr_but
                                  ,text     = _('Blacklist')
                                  ,hint     = _('Toggle the blacklist')
                                  ,inactive = self.icon_block_off
                                  ,active   = self.icon_block_on
                                  )
        # Кнопка включения/отключения режима приоритезации словарей
        self.btn_prio = sg.Button (parent   = self.fr_but
                                  ,text     = _('Prioritize')
                                  ,hint     = _('Toggle prioritizing')
                                  ,inactive = self.icon_priority_off
                                  ,active   = self.icon_priority_on
                                  )
        # Кнопка включения/отключения сортировки словарей по алфавиту
        self.btn_alph = sg.Button (parent   = self.fr_but
                                  ,text     = _('Alphabetize')
                                  ,hint     = _('Toggle alphabetizing')
                                  ,inactive = self.icon_alphabet_off
                                  ,active   = self.icon_alphabet_on
                                  )
        # Кнопка перехода на предыдущую статью
        self.btn_prev = sg.Button (parent   = self.fr_but
                                  ,text     = '←'
                                  ,hint     = _('Go to the preceding article')
                                  ,inactive = self.icon_go_back_off
                                  ,active   = self.icon_go_back
                                  )
        # Кнопка перехода на следующую статью
        self.btn_next = sg.Button (parent   = self.fr_but
                                  ,text     = '→'
                                  ,hint     = _('Go to the following article')
                                  ,inactive = self.icon_go_forward_off
                                  ,active   = self.icon_go_forward
                                  )
        # Кнопка включения/отключения и очистки истории
        self.btn_hist = sg.Button (parent      = self.fr_but
                                  ,text        = _('History')
                                  ,inactive    = self.icon_toggle_history
                                  ,active      = self.icon_toggle_history
                                  ,hint_height = 80
                                  )
        # Кнопка перезагрузки статьи
        self.btn_reld = sg.Button (parent   = self.fr_but
                                  ,text     = _('Reload')
                                  ,hint     = _('Reload the article')
                                  ,inactive = self.icon_reload
                                  ,active   = self.icon_reload
                                  )
        # Кнопка "Поиск в статье"
        self.btn_srch = sg.Button (parent   = self.fr_but
                                  ,text     = _('Search')
                                  ,hint     = _('Find in the current article')
                                  ,inactive = self.icon_search_article
                                  ,active   = self.icon_search_article
                                  )
        # Кнопка "Сохранить"
        self.btn_save = sg.Button (parent   = self.fr_but
                                  ,text     = _('Save')
                                  ,hint     = _('Save the current article')
                                  ,inactive = self.icon_save_article
                                  ,active   = self.icon_save_article
                                  )
        # Кнопка "Открыть в браузере"
        self.btn_brws = sg.Button (parent   = self.fr_but
                                  ,text     = _('Browse')
                                  ,hint     = _('Open the current article in a browser')
                                  ,inactive = self.icon_open_in_browser
                                  ,active   = self.icon_open_in_browser
                                  )
        # Кнопка "Печать"
        self.btn_prnt = sg.Button (parent   = self.fr_but
                                  ,text     = _('Print')
                                  ,hint     = _('Create a print-ready preview')
                                  ,inactive = self.icon_print
                                  ,active   = self.icon_print
                                  )
        # Кнопка толкования термина
        self.btn_expl = sg.Button (parent   = self.fr_but
                                  ,text     = _('Define')
                                  ,hint     = _('Define the current term')
                                  ,inactive = self.icon_define
                                  ,active   = self.icon_define
                                  )
        # Кнопка "Перехват Ctrl-c-c"
        self.btn_clip = sg.Button (parent   = self.fr_but
                                  ,text     = _('Clipboard')
                                  ,hint     = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                  ,inactive = self.icon_watch_clipboard_off
                                  ,active   = self.icon_watch_clipboard_on
                                  ,fg       = 'red'
                                  )
        # Кнопка "О программе"
        self.btn_abot = sg.Button (parent   = self.fr_but
                                  ,text     = _('About')
                                  ,hint     = _('View About')
                                  ,inactive = self.icon_show_about
                                  ,active   = self.icon_show_about
                                  )
        # Кнопка выхода
        self.btn_quit = sg.Button (parent   = self.fr_but
                                  ,text     = _('Quit')
                                  ,hint     = _('Quit the program')
                                  ,action   = self.close
                                  ,inactive = self.icon_quit_now
                                  ,active   = self.icon_quit_now
                                  ,side     = 'right'
                                  )

    def bindings(self):
        ''' We need to bind all buttons (inside 'self.fr_but') and also
            gaps between them and between top-bottom borders
            ('self.canvas').
        '''
        sg.bind (obj      = self.canvas
                ,bindings = '<Motion>'
                ,action   = self.motion
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Control-q>'
                ,action   = self.close
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = sg.Geometry(parent=self.obj).minimize
                )
        sg.bind (obj      = self
                ,bindings = '<ButtonRelease-2>'
                ,action   = sg.Geometry(parent=self.obj).minimize
                )
        for child in self.fr_but.widget.winfo_children():
            child.bind('<Motion>',self.motion)

    def scrollbars(self):
        sg.Scrollbar (parent = self.frame_y
                     ,scroll = self
                     )
        sg.Scrollbar (parent     = self.bottom
                     ,scroll     = self
                     ,Horizontal = True
                     )
        
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..'
                                              ,'resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
                          
    def title(self,text=None):
        if not text:
            text = 'MClient'
        self.obj.title(text)

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

    def scroll_x(self,bbox,max_bbox):
        fraction = bbox / max_bbox
        self.widget.xview_moveto(fraction=fraction)
        
    def scroll_y(self,bboy,max_bboy):
        ''' 'tkinterhtml' may think that topmost blocks have higher
            BBOY1 than other blocks (this is probably a bug), but
            correcting this will make the code more complex and
            error-prone.
        '''
        fraction = bboy / max_bboy
        self.widget.yview_moveto(fraction=fraction)

    def show(self,event=None):
        self.obj.show()

    def close(self,event=None):
        self.obj.close()

    def bbox(self,*args):
        return self.widget.tk.call(self.widget,"bbox",*args)
        
    def motion(self,event=None):
        scr_width = self.obj.resolution()[0]
        # Do not move button frame if it is entirely visible
        if self.obj.widget.winfo_width() < self.fr_but.widget.winfo_reqwidth():
            x         = self.canvas.widget.winfo_pointerx()
            ''' We read 'canvas' because it should return positive
                values (in comparison with 'self.fr_but', which is
                movable). 'rootx' should be negative only when 'canvas'
                is partially moved by a user out of screen (but we may
                need this case too).
            '''
            rootx     = self.canvas.widget.winfo_rootx()
            leftx     = max (0,rootx)
            rightx    = min (rootx + self.canvas.widget.winfo_width()
                            ,scr_width
                            )
            if x <= leftx + self._border:
                self.scroll_left()
            elif x >= rightx - self._border:
                self.scroll_right()
            
    def scroll_left(self):
        sh.log.append ('WebFrame.scroll_left'
                      ,_('DEBUG')
                      ,_('Scroll by %d units to left') % self._shift
                      )
        self.canvas.widget.xview_scroll(-self._shift,'units')
        
    def scroll_right(self):
        sh.log.append ('WebFrame.scroll_right'
                      ,_('DEBUG')
                      ,_('Scroll by %d units to right') % self._shift
                      )
        self.canvas.widget.xview_scroll(self._shift,'units')



class Settings:

    def __init__(self):
        self.values()
        self.gui()

    def values(self):
        self._items = (_('Dictionaries')
                      ,_('Word forms')
                      ,_('Transcription')
                      ,_('Parts of speech')
                      ,_('Do not set')
                      )
        self._sc_items = (product
                         ,_('Multitran')
                         ,_('Cut to the chase')
                         ,_('Clearness')
                         ,_('Custom')
                         )
        self._sp_items = (_('Noun'),_('Verb'),_('Adjective')
                         ,_('Abbreviation'),_('Adverb'),_('Preposition')
                         ,_('Pronoun')
                         )
        self._allowed    = []
        self._sp_allowed = []
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

    def update_sc(self,event=None):
        cond11 = self.col1.choice == _('Dictionaries')
        cond12 = self.col1.choice == _('Word forms')
        cond13 = self.col1.choice == _('Parts of speech')
        cond21 = self.col2.choice == _('Word forms')
        cond22 = self.col2.choice == _('Transcription')
        cond31 = self.col3.choice == _('Transcription')
        cond32 = self.col3.choice == _('Parts of speech')
        cond33 = self.col3.choice == _('Do not set')
        cond41 = self.col4.choice == _('Parts of speech')
        cond42 = self.col4.choice == _('Dictionaries')
        cond43 = self.col4.choice == _('Do not set')

        if cond11 and cond21 and cond31 and cond41:
            self.sc.set(product)
        elif cond12 and cond22 and cond32 and cond42:
            self.sc.set(_('Multitran'))
        elif cond13 and cond21 and cond31 and cond42:
            self.sc.set(_('Cut to the chase'))
        elif cond13 and cond21 and cond33 and cond43:
            self.sc.set(_('Clearness'))
        else:
            self.sc.set(_('Custom'))

    def update_by_sc(self,event=None):
        if self.sc.choice == product:
            self.col1.set(_('Dictionaries'))
            self.col2.set(_('Word forms'))
            self.col3.set(_('Transcription'))
            self.col4.set(_('Parts of speech'))
        elif self.sc.choice == _('Multitran'):
            self.col1.set(_('Word forms'))
            self.col2.set(_('Transcription'))
            self.col3.set(_('Parts of speech'))
            self.col4.set(_('Dictionaries'))
        elif self.sc.choice == _('Cut to the chase'):
            self.col1.set(_('Parts of speech'))
            self.col2.set(_('Word forms'))
            self.col3.set(_('Transcription'))
            self.col4.set(_('Dictionaries'))
        elif self.sc.choice == _('Clearness'):
            self.col1.set(_('Parts of speech'))
            self.col2.set(_('Word forms'))
            self.col3.set(_('Do not set'))
            self.col4.set(_('Do not set'))
        elif self.sc.choice == _('Custom'):
            pass
        else:
            sg.Message (func    = 'Settings.update_by_sc'
                       ,level   = _('ERROR')
                       ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                  % (str(self.sc.choice)
                                    ,', '.join(self._sc_items)
                                    )
                       )

    def update_by_col1(self,event=None):
        self._allowed = list(self._items)
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col2(self,event=None):
        self._allowed = list(self._items)
        self.update_col2()
        self.update_col1()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col3(self,event=None):
        self._allowed = list(self._items)
        self.update_col3()
        self.update_col1()
        self.update_col2()
        self.update_col4()
        self.update_sc()

    def update_by_col4(self,event=None):
        self._allowed = list(self._items)
        self.update_col4()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_sc()
        
    def update_by_sp1(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp2(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp2()
        self.update_sp1()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp3(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp3()
        self.update_sp1()
        self.update_sp2()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp4(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp4()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp5(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp5()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp6(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp6()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp7()
        
    def update_by_sp7(self,event=None):
        self._sp_allowed = list(self._sp_items)
        self.update_sp7()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()

    def gui(self):
        self.obj = sg.objs.new_top()
        self.title()
        self.frames()
        self.checkboxes()
        self.labels()
        self.columns()
        self.buttons()
        self.bindings()
        self.icon()

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

    def checkboxes(self):
        self.cb1 = sg.CheckBox (parent = self.fr_cb1
                               ,Active = True
                               ,side   = 'left'
                               )
                               
        self.cb2 = sg.CheckBox (parent = self.fr_cb2
                               ,Active = True
                               ,side   = 'left'
                               )
                               
        self.cb3 = sg.CheckBox (parent = self.fr_cb3
                               ,Active = True
                               ,side   = 'left'
                               )

        self.cb4 = sg.CheckBox (parent = self.fr_cb4
                               ,Active = True
                               ,side   = 'left'
                               )

        self.cb5 = sg.CheckBox (parent = self.fr_cb5
                               ,Active = False
                               ,side   = 'left'
                               )
                               
    def reset(self,event=None):
        self.sc.set(product)
        self.col1.set(_('Dictionaries'))
        self.col2.set(_('Word forms'))
        self.col3.set(_('Parts of speech'))
        self.col4.set(_('Transcription'))
        self.sp1.set(_('Noun'))
        self.sp2.set(_('Verb'))
        self.sp3.set(_('Adjective'))
        self.sp4.set(_('Abbreviation'))
        self.sp5.set(_('Adverb'))
        self.sp6.set(_('Preposition'))
        self.sp7.set(_('Pronoun'))
        self.cb1.enable()
        self.cb2.enable()
        self.cb3.enable()
        self.cb4.enable()
        self.cb5.disable()

    def buttons(self):
        sg.Button (parent     = self.fr_but
                  ,action     = self.reset
                  ,hint       = _('Reset settings')
                  ,hint_width = self._hint_width
                  ,text       = _('Reset')
                  ,side       = 'left'
                  )

        self.btn_aply = sg.Button (parent     = self.fr_but
                                  ,hint       = _('Apply settings')
                                  ,hint_width = self._hint_width
                                  ,text       = _('Apply')
                                  ,side       = 'right'
                                  )
        #cur
        #todo: elaborate
        '''
        self.btn_blok = sg.Button (parent     = self.fr_cb3
                                  ,hint       = _('Tune up blacklisting')
                                  ,hint_width = self._hint_width
                                  ,text       = _('Add/Remove')
                                  ,side       = 'right'
                                  )
        self.btn_prio = sg.Button (parent     = self.fr_cb4
                                  ,hint       = _('Tune up prioritizing')
                                  ,hint_width = self._hint_width
                                  ,text       = _('Add/Remove')
                                  ,side       = 'right'
                                  )
        '''

    def frames(self):
        self.fr_col = sg.Frame (parent = self.obj
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.fr_sp  = sg.Frame (parent = self.obj
                               ,expand = True
                               ,fill   = 'both'
                               )
        self.fr_sc  = sg.Frame (parent = self.fr_col
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_c1  = sg.Frame (parent = self.fr_col
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_c2  = sg.Frame (parent = self.fr_col
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_c3  = sg.Frame (parent = self.fr_col
                               ,expand = False
                               ,side   = 'left'
                               ,fill   = 'both'
                               )
        self.fr_c4  = sg.Frame (parent = self.fr_col
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp1 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp2 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp3 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp4 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp5 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp6 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_sp7 = sg.Frame (parent = self.fr_sp
                               ,side   = 'left'
                               ,expand = False
                               ,fill   = 'both'
                               )
        self.fr_cb1 = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               )
        self.fr_cb2 = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               )
        self.fr_cb3 = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               )
        self.fr_cb4 = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               )
        self.fr_cb5 = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               )
        self.fr_but = sg.Frame (parent = self.obj
                               ,expand = False
                               ,fill   = 'x'
                               ,side   = 'bottom'
                               )

    def labels(self):
        ''' Other possible color schemes:
            font = 'Sans 9 italic', fg = 'khaki4'
        '''
        sg.Label (parent = self.fr_sc
                 ,text   = _('Style:')
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_c1
                 ,text   = _('Column') + ' 1:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_c2
                 ,text   = _('Column') + ' 2:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_c3
                 ,text   = _('Column') + ' 3:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_c4
                 ,text   = _('Column') + ' 4:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        self.lb1 = sg.Label (parent = self.fr_cb1
                            ,text   = _('Sort by each column (if it is set, except for transcription) and order parts of speech')
                            ,side   = 'left'
                            )
        
        self.lb2 = sg.Label (parent = self.fr_cb2
                            ,text   = _('Alphabetize terms')
                            ,side   = 'left'
                            )
        
        self.lb3 = sg.Label (parent = self.fr_cb3
                            ,text   = _('Block dictionaries from blacklist')
                            ,side   = 'left'
                            )

        self.lb4 = sg.Label (parent = self.fr_cb4
                            ,text   = _('Prioritize dictionaries')
                            ,side   = 'left'
                            )
        
        self.lb5 = sg.Label (parent = self.fr_cb5
                            ,text   = _('Vertical view')
                            ,side   = 'left'
                            )
        
        sg.Label (parent = self.fr_sp1
                 ,text   = _('Part of speech') + ' 1:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_sp2
                 ,text   = _('Part of speech') + ' 2:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_sp3
                 ,text   = _('Part of speech') + ' 3:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )

        sg.Label (parent = self.fr_sp4
                 ,text   = _('Part of speech') + ' 4:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
                 
        sg.Label (parent = self.fr_sp5
                 ,text   = _('Part of speech') + ' 5:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
                 
        sg.Label (parent = self.fr_sp6
                 ,text   = _('Part of speech') + ' 6:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
                 
        sg.Label (parent = self.fr_sp7
                 ,text   = _('Part of speech') + ' 7:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
                 
    def columns(self):
        self.sc   = sg.OptionMenu (parent  = self.fr_sc
                                  ,items   = self._sc_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sc
                                  ,default = product
                                  )

        self.col1 = sg.OptionMenu (parent  = self.fr_c1
                                  ,items   = self._items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_col1
                                  ,default = _('Dictionaries')
                                  )

        self.col2 = sg.OptionMenu (parent  = self.fr_c2
                                  ,items   = self._items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_col2
                                  ,default = _('Word forms')
                                  )

        self.col3 = sg.OptionMenu (parent  = self.fr_c3
                                  ,items   = self._items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_col3
                                  ,default = _('Transcription')
                                  )

        self.col4 = sg.OptionMenu (parent  = self.fr_c4
                                  ,items   = self._items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_col4
                                  ,default = _('Parts of speech')
                                  )

        self.sp1  = sg.OptionMenu (parent  = self.fr_sp1
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp1
                                  ,default = self._sp_items[0]
                                  )
                                  
        self.sp2  = sg.OptionMenu (parent  = self.fr_sp2
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp2
                                  ,default = self._sp_items[1]
                                  )
                                  
        self.sp3  = sg.OptionMenu (parent  = self.fr_sp3
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp3
                                  ,default = self._sp_items[2]
                                  )
                                  
        self.sp4  = sg.OptionMenu (parent  = self.fr_sp4
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp4
                                  ,default = self._sp_items[3]
                                  )
                                  
        self.sp5  = sg.OptionMenu (parent  = self.fr_sp5
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp5
                                  ,default = self._sp_items[4]
                                  )
                                  
        self.sp6  = sg.OptionMenu (parent  = self.fr_sp6
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp6
                                  ,default = self._sp_items[5]
                                  )
                                  
        self.sp7  = sg.OptionMenu (parent  = self.fr_sp7
                                  ,items   = self._sp_items
                                  ,side    = 'bottom'
                                  ,action  = self.update_by_sp7
                                  ,default = self._sp_items[6]
                                  )

    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = self.close
                )
        sg.bind (obj      = self.lb1
                ,bindings = '<Button-1>'
                ,action   = self.cb1.toggle
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

    def title(self,text=_('View Settings')):
        self.obj.title(text=text)

    def show(self,event=None):
        self.Active = True
        self.obj.show()

    def close(self,event=None):
        self.Active = False
        self.obj.close()

    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()

    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..'
                                              ,'resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
    
    def update_sp1(self):
        if self.sp1.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp1.choice)
        elif _('Noun') in self._sp_allowed:
            self.sp1.set(_('Noun'))
            self._sp_allowed.remove(_('Noun'))
        elif self._sp_allowed:
            self.sp1.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp1'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
    
    def update_sp2(self):
        if self.sp2.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp2.choice)
        elif _('Verb') in self._sp_allowed:
            self.sp2.set(_('Verb'))
            self._sp_allowed.remove(_('Verb'))
        elif self._sp_allowed:
            self.sp2.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp2'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
                       
    def update_sp3(self):
        if self.sp3.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp3.choice)
        elif _('Adjective') in self._sp_allowed:
            self.sp3.set(_('Adjective'))
            self._sp_allowed.remove(_('Adjective'))
        elif self._sp_allowed:
            self.sp3.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp3'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
                       
    def update_sp4(self):
        if self.sp4.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp4.choice)
        elif _('Abbreviation') in self._sp_allowed:
            self.sp4.set(_('Abbreviation'))
            self._sp_allowed.remove(_('Abbreviation'))
        elif self._sp_allowed:
            self.sp4.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp4'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
                       
    def update_sp5(self):
        if self.sp5.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp5.choice)
        elif _('Adverb') in self._sp_allowed:
            self.sp5.set(_('Adverb'))
            self._sp_allowed.remove(_('Adverb'))
        elif self._sp_allowed:
            self.sp5.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp5'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
                       
    def update_sp6(self):
        if self.sp6.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp6.choice)
        elif _('Preposition') in self._sp_allowed:
            self.sp6.set(_('Preposition'))
            self._sp_allowed.remove(_('Preposition'))
        elif self._sp_allowed:
            self.sp6.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp6'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )
                       
    def update_sp7(self):
        if self.sp7.choice in self._sp_allowed:
            self._sp_allowed.remove(self.sp7.choice)
        elif _('Pronoun') in self._sp_allowed:
            self.sp7.set(_('Pronoun'))
            self._sp_allowed.remove(_('Pronoun'))
        elif self._sp_allowed:
            self.sp7.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (func    = 'Settings.update_sp7'
                       ,level   = _('ERROR')
                       ,message = _('Empty input is not allowed!')
                       )



class SpecSymbols:

    def __init__(self):
        self.Active = False
        self.gui()
        
    def gui(self):
        self.obj    = sg.objs.new_top()
        self.widget = self.obj.widget
        self.frame  = sg.Frame(self.obj,expand=1)
        self.icon()
        self.title()
        self.bindings()
        
    def bindings(self):
        sg.bind (obj      = self.obj
                ,bindings = '<Escape>'
                ,action   = self.close
                )
    
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..'
                                              ,'resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
                          
    def title(self,text=None):
        if not text:
            text = _('Paste a special symbol')
        self.obj.title(text)

    def show(self,event=None):
        self.Active = True
        self.obj.show()

    def close(self,event=None):
        self.Active = False
        self.obj.close()
        
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()



if __name__ == '__main__':
    sg.objs.start()
    WebFrame().show()
    sg.objs.end()
