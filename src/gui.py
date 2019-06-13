#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinterhtml as th
import shared      as sh
import sharedGUI   as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

PRODUCT = 'MClient'
VERSION = '6.1'


class Sources:

    def __init__(self,width=350,height=300):
        self.values()
        self._width  = width
        self._height = height
        self.parent = sg.Top(parent=sg.objs.root())
        sg.Geometry(parent=self.parent).set ('%dx%d' % (self._width
                                                       ,self._height
                                                       )
                                            )
        self.gui()
        
    def icon(self,path=None):
        if path:
            self.parent.icon(path)
        else:
            self.parent.icon (sh.objs.pdir().add ('..','resources'
                                                 ,'icon_64x64_mclient.gif'
                                                 )
                             )
    
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                ,action   = self.close
                )
        self.cvs_prm.top_bindings (top     = self.parent
                                  ,Control = False
                                  )
    
    def selected(self,event=None):
        active = []
        for i in range(len(self._cboxes)):
            if self._cboxes[i].get():
                active.append(self._lbls[i]._text)
        return active
    
    def title(self,text=None):
        if not text:
            text = _('Sources')
        self.parent.title(text)
    
    def region(self):
        f = '[MClient] gui.Sources.region'
        if self._frms:
            self.cvs_prm.region (x        = self._width
                                ,y        = 22 * len(self._frms)
                                ,x_border = 10
                                ,y_border = 20
                                )
            self.cvs_prm.scroll()
        else:
            sh.log.append (f,_('INFO')
                          ,_('Nothing to do!')
                          )
        
    def values(self):
        self._frms   = []
        self._cboxes = []
        self._lbls   = []
        
    def buttons(self):
        self.btn_tgl = sg.Button (parent = self.frm_btl
                                 ,text   = _('Select all')
                                 ,hint   = _('Mark/unmark all checkboxes')
                                 ,side   = 'left'
                                 ,action = self.toggle
                                 )
        self.btn_rst = sg.Button (parent = self.frm_btl
                                 ,text   = _('Reset')
                                 ,hint   = _('Reset to default')
                                 ,side   = 'right'
                                 )
        self.btn_apl = sg.Button (parent = self.frm_btr
                                 ,text   = _('Apply')
                                 ,hint   = _('Close & Apply')
                                 ,side   = 'right'
                                 )
    
    def widgets(self):
        self.cvs_prm = sg.Canvas(parent=self.frm_cnt)
        self.frm_emb = sg.Frame(parent=self.frm_cnt)
        self.cvs_prm.embed(self.frm_emb)
        self.buttons()
        
    def add_row(self,text):
        frm = sg.Frame (parent = self.frm_emb
                       ,expand = False
                       )
        cbx = sg.CheckBox (parent = frm
                          ,side   = 'left'
                          )
        lbl = sg.Label (parent = frm
                       ,text   = text
                       ,side   = 'left'
                       ,Close  = False
                       )
        sg.bind (obj      = lbl
                ,bindings = '<ButtonRelease-1>'
                ,action   = cbx.toggle
                )
        self._frms.append(frm)
        self._cboxes.append(cbx)
        self._lbls.append(lbl)
        
    def toggle(self,event=None):
        Marked = False
        for cbox in self._cboxes:
            if cbox.get():
                Marked = True
                break
        if Marked:
            for cbox in self._cboxes:
                cbox.disable()
        else:
            for cbox in self._cboxes:
                cbox.enable()
    
    def reset(self,lst=[]):
        lst = [str(item) for item in lst]
        for frame in self._frms:
            frame.widget.destroy()
        self.values()
        for item in lst:
            self.add_row(item)
        self.region()
    
    def gui(self):
        self.frames()
        self.widgets()
        self.scrollbars()
        self.bindings()
        self.title()
        self.btn_apl.focus()
        
    def frames(self):
        self.frm_prm = sg.Frame (parent = self.parent)
        self.frm_top = sg.Frame (parent = self.frm_prm
                                ,side   = 'top'
                                )
        self.frm_btm = sg.Frame (parent = self.frm_prm
                                ,side   = 'bottom'
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cnt = sg.Frame (parent = self.frm_top
                                ,side   = 'left'
                                )
        self.frm_ver = sg.Frame (parent = self.frm_top
                                ,expand = False
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        self.frm_hor = sg.Frame (parent = self.frm_btm
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'top'
                                )
        self.frm_btn = sg.Frame (parent = self.frm_btm
                                ,expand = False
                                ,fill   = 'both'
                                ,side   = 'bottom'
                                )
        self.frm_btl = sg.Frame (parent = self.frm_btn
                                ,fill   = 'both'
                                ,side   = 'left'
                                )
        self.frm_btr = sg.Frame (parent = self.frm_btn
                                ,fill   = 'both'
                                ,side   = 'right'
                                )
        
    def scrollbars(self):
        self.scr_hor = sg.Scrollbar (parent = self.frm_hor
                                    ,scroll = self.cvs_prm
                                    ,Horiz  = True
                                    )
        self.scr_ver = sg.Scrollbar (parent = self.frm_ver
                                    ,scroll = self.cvs_prm
                                    )
                                 
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



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
            self.obj.icon (sh.objs.pdir().add ('..','resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
        
    def labels(self):
        self.lbl_abt = sg.Label (parent = self.frm_prm
                                ,text   = _('Programming: Peter Sklyar, 2015-2019.\nVersion: %s\n\nThis program is free and opensource. You can use and modify it freely\nwithin the scope of the provisions set forth in GPL v.3 and the active legislation.\n\nIf you have any questions, requests, etc., please do not hesitate to contact me.\n') \
                                          % VERSION
                                ,font   = 'Sans 14'
                                )
        
    def frames(self):
        self.frm_prm = sg.Frame (parent = self
                                ,expand = 1
                                ,fill   = 'both'
                                ,side   = 'top'
                                )
        self.frm_sec = sg.Frame (parent = self
                                ,expand = 1
                                ,fill   = 'both'
                                ,side   = 'left'
                                )
        self.frm_ter = sg.Frame (parent = self
                                ,expand = 1
                                ,fill   = 'both'
                                ,side   = 'right'
                                )
    def buttons(self):
        # Show the license
        self.btn_thd = sg.Button (parent = self.frm_sec
                                 ,text   = _('Third parties')
                                 ,hint   = _('Third-party licenses')
                                 ,side   = 'left'
                                 )
        self.btn_lic = sg.Button (parent = self.frm_ter
                                 ,text   = _('License')
                                 ,hint   = _('View the license')
                                 ,side   = 'left'
                                 )
        # Send mail to the author
        self.btn_eml = sg.Button (parent = self.frm_ter
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
            self.parent.icon (sh.objs.pdir().add ('..','resources'
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
            self.parent.icon (sh.objs.pdir().add ('..','resources'
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
            self.parent.icon (sh.objs.pdir().add ('..','resources'
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
        self._icon  = sh.objs.pdir().add ('..','resources'
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
        self.obj.focus()
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
        
    def paste_search(self,event=None,text=None):
        ''' Clear the search field and insert set text or
            clipboard contents.
        '''
        self.ent_src.clear_text()
        if text:
            self.ent_src.insert(text=text)
        else:
            self.ent_src.insert(text=sg.Clipboard().paste())
        return 'break'

    def values(self):
        self._shift  = 1
        self._border = 24
        self.icn_al0 = sh.objs.pdir().add ('..','resources','buttons'
                                          ,'icon_36x36_alphabet_off.gif'
                                          )
        self.icn_al1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_alphabet_on.gif'
                                         )
        self.icn_bl0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_block_off.gif'
                                         )
        self.icn_bl1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_block_on.gif'
                                         )
        self.icn_clr = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_clear_search_field.gif'
                                         )
        self.icn_def = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_define.gif'
                                         )
        self.icn_bk0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_back_off.gif'
                                         )
        self.icn_bk1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_back.gif'
                                         )
        self.icn_fw0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_forward_off.gif'
                                         )
        self.icn_fw1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_forward.gif'
                                         )
        self.icn_ret = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_go_search.gif'
                                         )
        self.icn_brw = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_open_in_browser.gif'
                                         )
        self.icn_ins = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_paste.gif'
                                         )
        self.icn_prn = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_print.gif'
                                         )
        self.icn_pr0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_priority_off.gif'
                                         )
        self.icn_pr1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_priority_on.gif'
                                         )
        self.icn_qit = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_quit_now.gif'
                                         )
        self.icn_rld = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_reload.gif'
                                         )
        self.icn_rp0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_repeat_sign_off.gif'
                                         )
        self.icn_rp1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_repeat_sign.gif'
                                         )
        self.icn_r20 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_repeat_sign2_off.gif'
                                         )
        self.icn_r21 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_repeat_sign2.gif'
                                         )
        self.icn_sav = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_save_article.gif'
                                         )
        self.icn_src = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_search_article.gif'
                                         )
        self.icn_set = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_settings.gif'
                                         )
        self.icn_abt = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_show_about.gif'
                                         )
        self.icn_sym = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_spec_symbol.gif'
                                         )
        self.icn_hst = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_toggle_history.gif'
                                         )
        self.icn_hor = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_toggle_view_hor.gif'
                                         )
        self.icn_ver = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_toggle_view_ver.gif'
                                         )
        self.icn_cp0 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_watch_clipboard_off.gif'
                                         )
        self.icn_cp1 = sh.objs._pdir.add ('..','resources','buttons'
                                         ,'icon_36x36_watch_clipboard_on.gif'
                                         )

    def gui(self):
        self.obj     = sg.objs.new_top(Maximize=True)
        self.frm_prm = sg.Frame (parent = self.obj
                                ,expand = 1
                                )
        self.frm_btm = sg.Frame (parent = self.frm_prm
                                ,expand = 0
                                ,side   = 'bottom'
                                )
        self.frm_ver = sg.Frame (parent = self.frm_prm
                                ,expand = 0
                                ,fill   = 'y'
                                ,side   = 'right'
                                )
        self.widget  = th.TkinterHtml(self.frm_prm.widget)
        self.widget.pack(expand='1',fill='both')
        self.scrollbars()
        self.frame_panel()
        self.icon()
        self.title()
        self.bindings()
        self.ent_src.focus_set()
        self.obj.widget.protocol("WM_DELETE_WINDOW",self.close)

    def frame_panel(self):
        ''' Do not mix 'self.frm_pnl' and 'self.frm_btm', otherwise,
            they may overlap each other.
        '''
        self.frm_pnl = sg.Frame (parent = self.frm_btm
                                ,expand = 0
                                ,fill   = 'x'
                                )
        # Canvas should be created within a frame
        self.cvs_prm = sg.Canvas (parent = self.frm_pnl
                                 ,expand = 0
                                 )
        self.frm_btn = sg.Frame (parent = self.frm_pnl
                                ,expand = 0
                                )
        # A search entry field
        self.ent_src = sg.Entry (parent    = self.frm_btn
                                ,Composite = True
                                ,side      = 'left'
                                ,ipady     = 5
                                )
        self.draw_buttons()
        self.cvs_prm.embed(obj=self.frm_btn)
        ''' #todo: Updating idletasks will show the AllDic 'Please wait'
            message for too long, however, we need to update in order to
            set canvas dimensions correctly.
        '''
        sg.objs.root().widget.update_idletasks()
        height = self.frm_btn.widget.winfo_height()
        width  = self.frm_btn.widget.winfo_width()
        self.cvs_prm.widget.config(width=self.obj.resolution()[0])
        self.cvs_prm.widget.config(height=height)
        x2 = (width / 2)
        x1 = -x2
        y2 = (height / 2)
        y1 = -y2
        self.cvs_prm.widget.config(scrollregion=(x1,y1,x2,y2))
        # The scrollbar is set at the end for some reason
        self.cvs_prm.widget.xview_moveto(0)

    def draw_buttons(self):
        ''' Create buttons
            Bindings are indicated here only to set hints. In order to
            set bindings, use 'self.bindings'.
        '''
        # A button for newbies, substitutes Enter in search_field
        self.btn_trn = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Translate')
                                 ,hint     = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active   = self.icn_ret
                                 )

        # A button to clear the search field
        self.btn_clr = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Clear')
                                 ,hint     = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active   = self.icn_clr
                                 )

        # A button to insert text into the search field
        self.btn_ins = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Paste')
                                 ,hint     = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active   = self.icn_ins
                                 )
        # A button to insert a current search
        self.btn_rp1 = sg.Button (parent   = self.frm_btn
                                 ,text     = '!'
                                 ,hint     = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active   = self.icn_rp1
                                 )
        # A button to insert a previous search
        self.btn_rp2 = sg.Button (parent   = self.frm_btn
                                 ,text     = '!!'
                                 ,hint     = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active   = self.icn_r21
                                 )
        # A button to insert special symbols
        self.btn_sym = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Symbols')
                                 ,hint     = _('Paste a special symbol')
                                 ,inactive = self.icn_sym
                                 ,active   = self.icn_sym
                                 )
        self.opt_src = sg.OptionMenu (parent = self.frm_btn
                                     ,Combo  = True
                                     ,font   = 'Sans 11'
                                     )
        ''' Configure the option menu at the GUI creation time to avoid
            glitches with the search field.
        '''
        self.opt_src.widget.configure (width = 14
                                      ,font  = 'Sans 11'
                                      )
        # Drop-down lists with languages
        self.opt_lg1 = sg.OptionMenu (parent = self.frm_btn
                                     ,Combo  = True
                                     ,font   = 'Sans 11'
                                     )
        self.opt_lg2 = sg.OptionMenu (parent = self.frm_btn
                                     ,Combo  = True
                                     ,font   = 'Sans 11'
                                     )
        self.opt_col = sg.OptionMenu (parent  = self.frm_btn
                                     ,items   = (1,2,3,4,5,6,7,8,9,10)
                                     ,default = 4
                                     ,Combo   = True
                                     ,font    = 'Sans 11'
                                     )
        ''' The 'height' argument changes a height of the drop-down
            list and not the main widget.
        '''
        self.opt_lg1.widget.config (width  = 11
                                   ,height = 15
                                   )
        self.opt_lg2.widget.config (width  = 11
                                   ,height = 15
                                   )
        self.opt_col.widget.config(width=2)
        # A settings button
        self.btn_set = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Settings')
                                 ,hint     = _('Tune up view settings')
                                 ,inactive = self.icn_set
                                 ,active   = self.icn_set
                                 )
        # A button to change the article view
        self.btn_viw = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Toggle view')
                                 ,hint     = _('Toggle the article view mode')
                                 ,inactive = self.icn_ver
                                 ,active   = self.icn_hor
                                 )
        # A button to toggle dictionary blocking
        self.btn_blk = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Blacklist')
                                 ,hint     = _('Toggle the blacklist')
                                 ,inactive = self.icn_bl0
                                 ,active   = self.icn_bl1
                                 )
        # A button to toggle dictionary prioritization
        self.btn_pri = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Prioritize')
                                 ,hint     = _('Toggle prioritizing')
                                 ,inactive = self.icn_pr0
                                 ,active   = self.icn_pr1
                                 )
        # A button to toggle dictionary alphabetization
        self.btn_alp = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Alphabetize')
                                 ,hint     = _('Toggle alphabetizing')
                                 ,inactive = self.icn_al0
                                 ,active   = self.icn_al1
                                 )
        # A button to move to the previous article
        self.btn_prv = sg.Button (parent   = self.frm_btn
                                 ,text     = '←'
                                 ,hint     = _('Go to the preceding article')
                                 ,inactive = self.icn_bk0
                                 ,active   = self.icn_bk1
                                 )
        # A button to move to the next article
        self.btn_nxt = sg.Button (parent   = self.frm_btn
                                 ,text     = '→'
                                 ,hint     = _('Go to the following article')
                                 ,inactive = self.icn_fw0
                                 ,active   = self.icn_fw1
                                 )
        # A button to toggle and clear history
        self.btn_hst = sg.Button (parent   = self.frm_btn
                                 ,text     = _('History')
                                 ,inactive = self.icn_hst
                                 ,active   = self.icn_hst
                                 )
        # A button to reload the article
        self.btn_rld = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Reload')
                                 ,hint     = _('Reload the article')
                                 ,inactive = self.icn_rld
                                 ,active   = self.icn_rld
                                 )
        # A button to search within the article
        self.btn_ser = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Search')
                                 ,hint     = _('Find in the current article')
                                 ,inactive = self.icn_src
                                 ,active   = self.icn_src
                                 )
        # A button to save the article
        self.btn_sav = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Save')
                                 ,hint     = _('Save the current article')
                                 ,inactive = self.icn_sav
                                 ,active   = self.icn_sav
                                 )
        # A button to open the current article in a browser
        self.btn_brw = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Browse')
                                 ,hint     = _('Open the current article in a browser')
                                 ,inactive = self.icn_brw
                                 ,active   = self.icn_brw
                                 )
        # A button to print the article
        self.btn_prn = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Print')
                                 ,hint     = _('Create a print-ready preview')
                                 ,inactive = self.icn_prn
                                 ,active   = self.icn_prn
                                 )
        # A button to define a term
        self.btn_def = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Define')
                                 ,hint     = _('Define the current term')
                                 ,inactive = self.icn_def
                                 ,active   = self.icn_def
                                 )
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Clipboard')
                                 ,hint     = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                 ,inactive = self.icn_cp0
                                 ,active   = self.icn_cp1
                                 ,fg       = 'red'
                                 )
        # A button to show info about the program
        self.btn_abt = sg.Button (parent   = self.frm_btn
                                 ,text     = _('About')
                                 ,hint     = _('View About')
                                 ,inactive = self.icn_abt
                                 ,active   = self.icn_abt
                                 )
        # A button to quit the program
        self.btn_qit = sg.Button (parent   = self.frm_btn
                                 ,text     = _('Quit')
                                 ,hint     = _('Quit the program')
                                 ,action   = self.close
                                 ,inactive = self.icn_qit
                                 ,active   = self.icn_qit
                                 ,side     = 'right'
                                 )

    def bindings(self):
        ''' We need to bind all buttons (inside 'self.frm_btn') and also
            gaps between them and between top-bottom borders
            ('self.cvs_prm').
        '''
        sg.bind (obj      = self.cvs_prm
                ,bindings = '<Motion>'
                ,action   = self.motion
                )
        sg.bind (obj      = self.obj
                ,bindings = '<Control-q>'
                ,action   = self.close
                )
        for child in self.frm_btn.widget.winfo_children():
            child.bind('<Motion>',self.motion)

    def scrollbars(self):
        sg.Scrollbar (parent = self.frm_ver
                     ,scroll = self
                     )
        sg.Scrollbar (parent = self.frm_btm
                     ,scroll = self
                     ,Horiz  = True
                     )
        
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (sh.objs.pdir().add ('..','resources'
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
        f = '[MClient] gui.WebFrame.width'
        sg.objs.root().widget.update_idletasks()
        '''
        sh.log.append (f,_('DEBUG')
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
        if self.obj.widget.winfo_width() < self.frm_btn.widget.winfo_reqwidth():
            x = self.cvs_prm.widget.winfo_pointerx()
            ''' We read 'canvas' because it should return positive
                values (in comparison with 'self.frm_btn', which is
                movable). 'rootx' should be negative only when 'canvas'
                is partially moved by a user out of screen (but we may
                need this case too).
            '''
            rootx  = self.cvs_prm.widget.winfo_rootx()
            leftx  = max (0,rootx)
            rightx = min (rootx + self.cvs_prm.widget.winfo_width()
                         ,scr_width
                         )
            if x <= leftx + self._border:
                self.scroll_left()
            elif x >= rightx - self._border:
                self.scroll_right()
            
    def scroll_left(self):
        f = '[MClient] gui.WebFrame.scroll_left'
        '''
        sh.log.append (f,_('DEBUG')
                      ,_('Scroll by %d units to left') % self._shift
                      )
        '''
        self.cvs_prm.widget.xview_scroll(-self._shift,'units')
        
    def scroll_right(self):
        f = '[MClient] gui.WebFrame.scroll_right'
        '''
        sh.log.append (f,_('DEBUG')
                      ,_('Scroll by %d units to right') % self._shift
                      )
        '''
        self.cvs_prm.widget.xview_scroll(self._shift,'units')



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
        self._sc_items = (PRODUCT
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
        self.Active      = False

    def update_col1(self):
        f = '[MClient] gui.Settings.update_col1'
        if self.opt_cl1.choice != _('Do not set'):
            if self.opt_cl1.choice in self._allowed:
                self._allowed.remove(self.opt_cl1.choice)
            elif _('Dictionaries') in self._allowed:
                self.opt_cl1.set(_('Dictionaries'))
                self._allowed.remove(_('Dictionaries'))
            elif self._allowed:
                self.opt_cl1.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (f,_('ERROR')
                           ,_('Empty input is not allowed!')
                           )

    def update_col2(self):
        f = '[MClient] gui.Settings.update_col2'
        if self.opt_cl2.choice != _('Do not set'):
            if self.opt_cl2.choice in self._allowed:
                self._allowed.remove(self.opt_cl2.choice)
            elif _('Word forms') in self._allowed:
                self.opt_cl2.set(_('Word forms'))
                self._allowed.remove(_('Word forms'))
            elif self._allowed:
                self.opt_cl2.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (f,_('ERROR')
                           ,_('Empty input is not allowed!')
                           )

    def update_col3(self):
        f = '[MClient] gui.Settings.update_col3'
        if self.opt_cl3.choice != _('Do not set'):
            if self.opt_cl3.choice in self._allowed:
                self._allowed.remove(self.opt_cl3.choice)
            elif _('Parts of speech') in self._allowed:
                self.opt_cl3.set(_('Parts of speech'))
                self._allowed.remove(_('Parts of speech'))
            elif self._allowed:
                self.opt_cl3.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (f,_('ERROR')
                           ,_('Empty input is not allowed!')
                           )

    def update_col4(self):
        f = '[MClient] gui.Settings.update_col4'
        if self.opt_cl4.choice != _('Do not set'):
            if self.opt_cl4.choice in self._allowed:
                self._allowed.remove(self.opt_cl4.choice)
            elif _('Transcription') in self._allowed:
                self.opt_cl4.set(_('Transcription'))
                self._allowed.remove(_('Transcription'))
            elif self._allowed:
                self.opt_cl4.set(self._allowed[0])
                self._allowed.remove(self._allowed[0])
            else:
                sg.Message (f,_('ERROR')
                           ,_('Empty input is not allowed!')
                           )

    def update_sc(self,event=None):
        cond11 = self.opt_cl1.choice == _('Dictionaries')
        cond12 = self.opt_cl1.choice == _('Word forms')
        cond13 = self.opt_cl1.choice == _('Parts of speech')
        cond21 = self.opt_cl2.choice == _('Word forms')
        cond22 = self.opt_cl2.choice == _('Transcription')
        cond31 = self.opt_cl3.choice == _('Transcription')
        cond32 = self.opt_cl3.choice == _('Parts of speech')
        cond33 = self.opt_cl3.choice == _('Do not set')
        cond41 = self.opt_cl4.choice == _('Parts of speech')
        cond42 = self.opt_cl4.choice == _('Dictionaries')
        cond43 = self.opt_cl4.choice == _('Do not set')

        if cond11 and cond21 and cond31 and cond41:
            self.opt_scm.set(PRODUCT)
        elif cond12 and cond22 and cond32 and cond42:
            self.opt_scm.set(_('Multitran'))
        elif cond13 and cond21 and cond31 and cond42:
            self.opt_scm.set(_('Cut to the chase'))
        elif cond13 and cond21 and cond33 and cond43:
            self.opt_scm.set(_('Clearness'))
        else:
            self.opt_scm.set(_('Custom'))

    def update_by_sc(self,event=None):
        f = '[MClient] gui.Settings.update_by_sc'
        if self.opt_scm.choice == PRODUCT:
            self.opt_cl1.set(_('Dictionaries'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Parts of speech'))
        elif self.opt_scm.choice == _('Multitran'):
            self.opt_cl1.set(_('Word forms'))
            self.opt_cl2.set(_('Transcription'))
            self.opt_cl3.set(_('Parts of speech'))
            self.opt_cl4.set(_('Dictionaries'))
        elif self.opt_scm.choice == _('Cut to the chase'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Transcription'))
            self.opt_cl4.set(_('Dictionaries'))
        elif self.opt_scm.choice == _('Clearness'):
            self.opt_cl1.set(_('Parts of speech'))
            self.opt_cl2.set(_('Word forms'))
            self.opt_cl3.set(_('Do not set'))
            self.opt_cl4.set(_('Do not set'))
        elif self.opt_scm.choice == _('Custom'):
            pass
        else:
            sg.Message (f,_('ERROR')
                       ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".')\
                       % (str(self.opt_scm.choice)
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
        f = '[MClient] gui.Settings.block_settings'
        sg.Message (f,_('INFO')
                   ,_('Not implemented yet!')
                   )

    def priority_settings(self,event=None):
        f = '[MClient] gui.Settings.priority_settings'
        sg.Message (f,_('INFO')
                   ,_('Not implemented yet!')
                   )

    def checkboxes(self):
        self.cbx_no1 = sg.CheckBox (parent = self.frm_cb1
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.cbx_no2 = sg.CheckBox (parent = self.frm_cb2
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.cbx_no3 = sg.CheckBox (parent = self.frm_cb3
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.cbx_no4 = sg.CheckBox (parent = self.frm_cb4
                                   ,Active = True
                                   ,side   = 'left'
                                   )
        self.cbx_no5 = sg.CheckBox (parent = self.frm_cb5
                                   ,Active = False
                                   ,side   = 'left'
                                   )
        self.cbx_no6 = sg.CheckBox (parent = self.frm_cb6
                                   ,Active = False
                                   ,side   = 'left'
                                   )

    def reset(self,event=None):
        self.opt_scm.set(PRODUCT)
        self.opt_cl1.set(_('Dictionaries'))
        self.opt_cl2.set(_('Word forms'))
        self.opt_cl3.set(_('Parts of speech'))
        self.opt_cl4.set(_('Transcription'))
        self.opt_sp1.set(_('Noun'))
        self.opt_sp2.set(_('Verb'))
        self.opt_sp3.set(_('Adjective'))
        self.opt_sp4.set(_('Abbreviation'))
        self.opt_sp5.set(_('Adverb'))
        self.opt_sp6.set(_('Preposition'))
        self.opt_sp7.set(_('Pronoun'))
        self.cbx_no1.enable()
        self.cbx_no2.enable()
        self.cbx_no3.enable()
        self.cbx_no4.enable()
        self.cbx_no5.disable()
        self.cbx_no6.disable()

    def buttons(self):
        sg.Button (parent = self.frm_btn
                  ,action = self.reset
                  ,hint   = _('Reset settings')
                  ,text   = _('Reset')
                  ,side   = 'left'
                  )

        self.btn_apl = sg.Button (parent = self.frm_btn
                                 ,hint   = _('Apply settings')
                                 ,text   = _('Apply')
                                 ,side   = 'right'
                                 )
        #todo: elaborate
        '''
        self.btn_blk = sg.Button (parent = self.frm_cb3
                                 ,hint   = _('Tune up blacklisting')
                                 ,text   = _('Add/Remove')
                                 ,side   = 'right'
                                 )
        self.btn_pri = sg.Button (parent = self.frm_cb4
                                 ,hint   = _('Tune up prioritizing')
                                 ,text   = _('Add/Remove')
                                 ,side   = 'right'
                                 )
        '''

    def frames(self):
        self.frm_col = sg.Frame (parent = self.obj
                                ,expand = True
                                ,fill   = 'both'
                                )
        self.frm_spc = sg.Frame (parent = self.obj
                                ,expand = True
                                ,fill   = 'both'
                                )
        self.frm_scm = sg.Frame (parent = self.frm_col
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_cl1 = sg.Frame (parent = self.frm_col
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_cl2 = sg.Frame (parent = self.frm_col
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_cl3 = sg.Frame (parent = self.frm_col
                                ,expand = False
                                ,side   = 'left'
                                ,fill   = 'both'
                                )
        self.frm_cl4 = sg.Frame (parent = self.frm_col
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp1 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp2 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp3 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp4 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp5 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp6 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_sp7 = sg.Frame (parent = self.frm_spc
                                ,side   = 'left'
                                ,expand = False
                                ,fill   = 'both'
                                )
        self.frm_cb1 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cb2 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cb3 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cb4 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cb5 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_cb6 = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                )
        self.frm_btn = sg.Frame (parent = self.obj
                                ,expand = False
                                ,fill   = 'x'
                                ,side   = 'bottom'
                                )

    def labels(self):
        ''' Other possible color schemes:
            font = 'Sans 9 italic', fg = 'khaki4'
        '''
        sg.Label (parent = self.frm_scm
                 ,text   = _('Style:')
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_cl1
                 ,text   = _('Column') + ' 1:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_cl2
                 ,text   = _('Column') + ' 2:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_cl3
                 ,text   = _('Column') + ' 3:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_cl4
                 ,text   = _('Column') + ' 4:'
                 ,font   = 'Sans 9'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        self.lbl_no1 = sg.Label (parent = self.frm_cb1
                                ,text   = _('Sort by each column (if it is set, except for transcription) and order parts of speech')
                                ,side   = 'left'
                                )
        self.lbl_no2 = sg.Label (parent = self.frm_cb2
                                ,text   = _('Alphabetize terms')
                                ,side   = 'left'
                                )
        self.lbl_no3 = sg.Label (parent = self.frm_cb3
                                ,text   = _('Block dictionaries from blacklist')
                                ,side   = 'left'
                                )
        self.lbl_no4 = sg.Label (parent = self.frm_cb4
                                ,text   = _('Prioritize dictionaries')
                                ,side   = 'left'
                                )
        self.lbl_no5 = sg.Label (parent = self.frm_cb5
                                ,text   = _('Vertical view')
                                ,side   = 'left'
                                )
        self.lbl_no6 = sg.Label (parent = self.frm_cb6
                                ,text   = _('Use abbreviations for dictionaries')
                                ,side   = 'left'
                                )
        sg.Label (parent = self.frm_sp1
                 ,text   = _('Part of speech') + ' 1:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp2
                 ,text   = _('Part of speech') + ' 2:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp3
                 ,text   = _('Part of speech') + ' 3:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp4
                 ,text   = _('Part of speech') + ' 4:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp5
                 ,text   = _('Part of speech') + ' 5:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp6
                 ,text   = _('Part of speech') + ' 6:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
        sg.Label (parent = self.frm_sp7
                 ,text   = _('Part of speech') + ' 7:'
                 ,font   = 'Sans 8'
                 ,side   = 'top'
                 ,fill   = 'both'
                 ,expand = True
                 ,fg     = 'PaleTurquoise1'
                 ,bg     = 'RoyalBlue3'
                 )
                 
    def columns(self):
        self.opt_scm = sg.OptionMenu (parent  = self.frm_scm
                                     ,items   = self._sc_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sc
                                     ,default = PRODUCT
                                     )
        self.opt_cl1 = sg.OptionMenu (parent  = self.frm_cl1
                                     ,items   = self._items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_col1
                                     ,default = _('Dictionaries')
                                     )
        self.opt_cl2 = sg.OptionMenu (parent  = self.frm_cl2
                                     ,items   = self._items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_col2
                                     ,default = _('Word forms')
                                     )
        self.opt_cl3 = sg.OptionMenu (parent  = self.frm_cl3
                                     ,items   = self._items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_col3
                                     ,default = _('Transcription')
                                     )
        self.opt_cl4 = sg.OptionMenu (parent  = self.frm_cl4
                                     ,items   = self._items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_col4
                                     ,default = _('Parts of speech')
                                     )
        self.opt_sp1 = sg.OptionMenu (parent  = self.frm_sp1
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp1
                                     ,default = self._sp_items[0]
                                     )
        self.opt_sp2 = sg.OptionMenu (parent  = self.frm_sp2
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp2
                                     ,default = self._sp_items[1]
                                     )
        self.opt_sp3 = sg.OptionMenu (parent  = self.frm_sp3
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp3
                                     ,default = self._sp_items[2]
                                     )
        self.opt_sp4 = sg.OptionMenu (parent  = self.frm_sp4
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp4
                                     ,default = self._sp_items[3]
                                     )
        self.opt_sp5 = sg.OptionMenu (parent  = self.frm_sp5
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp5
                                     ,default = self._sp_items[4]
                                     )
        self.opt_sp6 = sg.OptionMenu (parent  = self.frm_sp6
                                     ,items   = self._sp_items
                                     ,side    = 'bottom'
                                     ,action  = self.update_by_sp6
                                     ,default = self._sp_items[5]
                                     )
        self.opt_sp7 = sg.OptionMenu (parent  = self.frm_sp7
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
        sg.bind (obj      = self.lbl_no1
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no1.toggle
                )
        sg.bind (obj      = self.lbl_no2
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no2.toggle
                )
        sg.bind (obj      = self.lbl_no3
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no3.toggle
                )
        sg.bind (obj      = self.lbl_no4
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no4.toggle
                )
        sg.bind (obj      = self.lbl_no5
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no5.toggle
                )
        sg.bind (obj      = self.lbl_no6
                ,bindings = '<Button-1>'
                ,action   = self.cbx_no6.toggle
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
            self.obj.icon (sh.objs.pdir().add ('..','resources'
                                              ,'icon_64x64_mclient.gif'
                                              )
                          )
    
    def update_sp1(self):
        f = '[MClient] gui.Settings.update_sp1'
        if self.opt_sp1.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp1.choice)
        elif _('Noun') in self._sp_allowed:
            self.opt_sp1.set(_('Noun'))
            self._sp_allowed.remove(_('Noun'))
        elif self._sp_allowed:
            self.opt_sp1.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
    
    def update_sp2(self):
        f = '[MClient] gui.Settings.update_sp2'
        if self.opt_sp2.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp2.choice)
        elif _('Verb') in self._sp_allowed:
            self.opt_sp2.set(_('Verb'))
            self._sp_allowed.remove(_('Verb'))
        elif self._sp_allowed:
            self.opt_sp2.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
                       
    def update_sp3(self):
        f = '[MClient] gui.Settings.update_sp3'
        if self.opt_sp3.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp3.choice)
        elif _('Adjective') in self._sp_allowed:
            self.opt_sp3.set(_('Adjective'))
            self._sp_allowed.remove(_('Adjective'))
        elif self._sp_allowed:
            self.opt_sp3.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
                       
    def update_sp4(self):
        f = '[MClient] gui.Settings.update_sp4'
        if self.opt_sp4.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp4.choice)
        elif _('Abbreviation') in self._sp_allowed:
            self.opt_sp4.set(_('Abbreviation'))
            self._sp_allowed.remove(_('Abbreviation'))
        elif self._sp_allowed:
            self.opt_sp4.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
                       
    def update_sp5(self):
        f = '[MClient] gui.Settings.update_sp5'
        if self.opt_sp5.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp5.choice)
        elif _('Adverb') in self._sp_allowed:
            self.opt_sp5.set(_('Adverb'))
            self._sp_allowed.remove(_('Adverb'))
        elif self._sp_allowed:
            self.opt_sp5.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
                       
    def update_sp6(self):
        f = '[MClient] gui.Settings.update_sp6'
        if self.opt_sp6.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp6.choice)
        elif _('Preposition') in self._sp_allowed:
            self.opt_sp6.set(_('Preposition'))
            self._sp_allowed.remove(_('Preposition'))
        elif self._sp_allowed:
            self.opt_sp6.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )
                       
    def update_sp7(self):
        f = '[MClient] gui.Settings.update_sp7'
        if self.opt_sp7.choice in self._sp_allowed:
            self._sp_allowed.remove(self.opt_sp7.choice)
        elif _('Pronoun') in self._sp_allowed:
            self.opt_sp7.set(_('Pronoun'))
            self._sp_allowed.remove(_('Pronoun'))
        elif self._sp_allowed:
            self.opt_sp7.set(self._sp_allowed[0])
            self._sp_allowed.remove(self._sp_allowed[0])
        else:
            sg.Message (f,_('ERROR')
                       ,_('Empty input is not allowed!')
                       )



class SpecSymbols:

    def __init__(self):
        self.Active = False
        self.gui()
        
    def gui(self):
        self.obj    = sg.objs.new_top()
        self.widget = self.obj.widget
        self.frm_prm  = sg.Frame(self.obj,expand=1)
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
            self.obj.icon (sh.objs.pdir().add ('..','resources'
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



#todo: make this widget reusable
class Suggest:
    
    def __init__(self):
        self.parent = None
        
    def bindings(self):
        sg.bind (obj      = self.parent
                ,bindings = '<Escape>'
                ,action   = self.close
                )
        
    def show(self,lst=['a','b','c'],action=None):
        if not self.parent:
            self.parent = sg.SimpleTop(parent=sg.objs.root())
            self.parent.widget.wm_overrideredirect(1)
            self.lbox = sg.ListBox (parent          = self.parent
                                   ,title           = ''
                                   ,lst             = lst
                                   ,action          = action
                                   ,Composite       = True
                                   ,Scrollbar       = False
                                   ,SelectionCloses = False
                                   )
            self.bindings()
                               
    def close(self):
        if self.parent:
            self.parent.kill()
            self.parent = None



if __name__ == '__main__':
    sg.objs.start()
    WebFrame().show()
    '''
    sources = Sources()
    sources.reset ((_('Offline')
                   ,'multitran.ru'
                   ,'multitran.com'
                   )
                  )
    sources.show()
    '''
    sg.objs.end()
