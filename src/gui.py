#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinterhtml as th
import skl_shared.shared as sh
from skl_shared.localize import _

PRODUCT = 'MClient'
VERSION = '6.7'
CURYEAR = 2021
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')


class Sources:

    def __init__(self,width=350,height=300):
        self.set_values()
        self.width = width
        self.height = height
        self.parent = sh.Top()
        sh.Geometry(self.parent).set ('%dx%d' % (self.width
                                                ,self.height
                                                )
                                     )
        self.set_gui()
        
    def set_icon(self,path=None):
        if path:
            self.parent.set_icon(path)
        else:
            self.parent.set_icon(ICON)
    
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
        self.cvs_prm.set_top_bindings (top = self.parent
                                      ,Ctrl = False
                                      )
    
    def get_selected(self,event=None):
        active = []
        for i in range(len(self.cboxes)):
            if self.cboxes[i].get():
                active.append(self.lbls[i].text)
        return active
    
    def set_title(self,text=None):
        if not text:
            text = _('Sources')
        self.parent.set_title(text)
    
    def set_region(self):
        f = '[MClient] gui.Sources.set_region'
        if self.frms:
            self.cvs_prm.set_region (x = self.width
                                    ,y = 22 * len(self.frms)
                                    ,xborder = 10
                                    ,yborder = 20
                                    )
            self.cvs_prm.scroll()
        else:
            sh.com.rep_lazy()
        
    def set_values(self):
        self.frms = []
        self.cboxes = []
        self.lbls = []
        
    def set_buttons(self):
        self.btn_tgl = sh.Button (parent = self.frm_btl
                                 ,text = _('Select all')
                                 ,hint = _('Mark/unmark all checkboxes')
                                 ,side = 'left'
                                 ,action = self.toggle
                                 )
        self.btn_rst = sh.Button (parent = self.frm_btl
                                 ,text = _('Reset')
                                 ,hint = _('Reset to default')
                                 ,side = 'right'
                                 )
        self.btn_apl = sh.Button (parent = self.frm_btr
                                 ,text = _('Apply')
                                 ,hint = _('Close & Apply')
                                 ,side = 'right'
                                 )
    
    def widgets(self):
        self.cvs_prm = sh.Canvas(parent=self.frm_cnt)
        self.frm_emb = sh.Frame(parent=self.frm_cnt)
        self.cvs_prm.embed(self.frm_emb)
        self.set_buttons()
        
    def add_row(self,text):
        frm = sh.Frame (parent = self.frm_emb
                       ,expand = False
                       )
        cbx = sh.CheckBox (parent = frm
                          ,side = 'left'
                          )
        lbl = sh.Label (parent = frm
                       ,text = text
                       ,side = 'left'
                       )
        sh.com.bind (obj = lbl
                    ,bindings = '<ButtonRelease-1>'
                    ,action = cbx.toggle
                    )
        self.frms.append(frm)
        self.cboxes.append(cbx)
        self.lbls.append(lbl)
        
    def toggle(self,event=None):
        Marked = False
        for cbox in self.cboxes:
            if cbox.get():
                Marked = True
                break
        if Marked:
            for cbox in self.cboxes:
                cbox.disable()
        else:
            for cbox in self.cboxes:
                cbox.enable()
    
    def reset(self,lst=[]):
        lst = [str(item) for item in lst]
        for frame in self.frms:
            frame.widget.destroy()
        self.set_values()
        for item in lst:
            self.add_row(item)
        self.set_region()
    
    def set_gui(self):
        self.set_frames()
        self.set_widgets()
        self.set_scroll()
        self.set_bindings()
        self.set_title()
        self.btn_apl.focus()
        
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self.parent)
        self.frm_top = sh.Frame (parent = self.frm_prm
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.frm_prm
                                ,side = 'bottom'
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cnt = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                )
        self.frm_ver = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,fill = 'y'
                                ,side = 'right'
                                )
        self.frm_hor = sh.Frame (parent = self.frm_btm
                                ,expand = False
                                ,fill = 'x'
                                ,side = 'top'
                                )
        self.frm_btn = sh.Frame (parent = self.frm_btm
                                ,expand = False
                                ,fill = 'both'
                                ,side = 'bottom'
                                )
        self.frm_btl = sh.Frame (parent = self.frm_btn
                                ,fill = 'both'
                                ,side = 'left'
                                )
        self.frm_btr = sh.Frame (parent = self.frm_btn
                                ,fill = 'both'
                                ,side = 'right'
                                )
        
    def set_scroll(self):
        self.scr_hor = sh.Scrollbar (parent = self.frm_hor
                                    ,scroll = self.cvs_prm
                                    ,Horiz = True
                                    )
        self.scr_ver = sh.Scrollbar (parent = self.frm_ver
                                    ,scroll = self.cvs_prm
                                    )
                                 
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



class About:

    def __init__(self):
        self.type = 'About'
        self.set_gui()
        
    def set_gui(self):
        self.obj = self.parent = sh.Top()
        self.widget = self.obj.widget
        self.set_frames()
        self.set_labels()
        self.set_buttons()
        self.set_bindings()
        self.set_icon()
        self.set_title()
        self.widget.focus_set()
        
    def set_title(self,text=None):
        if not text:
            text = _('About')
        self.obj.set_title(text)
    
    def set_icon(self,path=None):
        if path:
            self.obj.set_icon(path)
        else:
            self.obj.set_icon(ICON)
        
    def set_labels(self):
        text = _('Programming: Peter Sklyar, 2015-{}.\nVersion: {}\n\nThis program is free and opensource. You can use and modify it freely\nwithin the scope of the provisions set forth in GPL v.3 and the active legislation.\n\nIf you have any questions, requests, etc., please do not hesitate to contact me.\n')
        text = text.format(CURYEAR,VERSION)
        self.lbl_abt = sh.Label (parent = self.frm_prm
                                ,text = text
                                ,font = 'Sans 14'
                                )
        
    def set_frames(self):
        self.frm_prm = sh.Frame (parent = self
                                ,expand = 1
                                ,fill = 'both'
                                ,side = 'top'
                                )
        self.frm_sec = sh.Frame (parent = self
                                ,expand = 1
                                ,fill = 'both'
                                ,side = 'left'
                                )
        self.frm_ter = sh.Frame (parent = self
                                ,expand = 1
                                ,fill = 'both'
                                ,side = 'right'
                                )
    def set_buttons(self):
        # Show the license
        self.btn_thd = sh.Button (parent = self.frm_sec
                                 ,text = _('Third parties')
                                 ,hint = _('Third-party licenses')
                                 ,side = 'left'
                                 )
        self.btn_lic = sh.Button (parent = self.frm_ter
                                 ,text = _('License')
                                 ,hint = _('View the license')
                                 ,side = 'left'
                                 )
        # Send mail to the author
        self.btn_eml = sh.Button (parent = self.frm_ter
                                 ,text = _('Contact the author')
                                 ,hint = _('Draft an email to the author')
                                 ,side = 'right'
                                 )
    
    def set_bindings(self):
        sh.com.bind (obj = self.obj
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )

    def close(self,event=None):
        self.obj.close()

    def show(self,event=None):
        self.obj.show()



class ThirdParties:
    
    def __init__(self):
        self.set_gui()
        
    def set_bindings(self):
        sh.com.bind (obj = self.obj
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
    
    def set_gui(self):
        title = _('Third parties') + ':'
        self.obj = sh.TextBoxRO (title = title
                                ,icon = ICON
                                )
        self.parent = self.obj.parent
        sh.Geometry(self.parent).set('800x600')
        self.set_bindings()
        self.obj.focus()
    
    def show(self,event=None):
        self.obj.show()
    
    def close(self,event=None):
        self.obj.close()



class SearchArticle:
    
    def __init__(self):
        self.set_gui()
    
    def insert(self,pattern=''):
        self.parent.insert(pattern)
    
    def focus(self):
        self.parent.focus()
        
    def center(self):
        self.parent.parent.center()
    
    def set_gui(self):
        self.parent = sh.EntryC (title = _('Enter a string to search:')
                                ,icon = ICON
                                )
        self.widget = self.parent.widget
        self.set_bindings()
        self.parent.focus()
    
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.parent.close
                    )
                             
    def show(self,event=None):
        self.parent.select_all()
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class SaveArticle:

    def __init__(self):
        self.type = 'SaveArticle'
        self.items = [_('Save the current view as a web-page (*.htm)')
                      ,_('Save the original article as a web-page (*.htm)')
                      ,_('Save the article as plain text in UTF-8 (*.txt)')
                      ,_('Copy HTML code of the article to clipboard')
                      ,_('Copy the text of the article to clipboard')
                      ]
        self.set_gui()
        
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
    
    def set_gui(self):
        self.parent = sh.ListBoxC (lst = self.items
                                  ,title = _('Select an action:')
                                  ,icon = ICON
                                  )
        self.widget = self.parent.widget
        self.set_bindings()

    def close(self,event=None):
        self.parent.close()

    def show(self,event=None):
        self.parent.show()



class History:

    def __init__(self):
        self.set_gui()

    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('History')
                             )
        self.obj = sh.ListBox(self.parent)
        sh.Geometry(self.parent).set('250x350')
        self.widget = self.obj.widget
        self.set_bindings()

    def set_bindings(self):
        sh.com.bind (obj = self
                    ,bindings = '<ButtonRelease-3>'
                    ,action = self.copy
                    )
        sh.com.bind (obj = self.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )

    def show(self,event=None):
        self.obj.focus()
        self.parent.show()

    def close(self,event=None):
        self.parent.close()

    # Скопировать элемент истории
    def copy(self,event=None):
        sh.Clipboard().copy(self.obj.get())



class WebFrame:

    def __init__(self):
        self.set_values()
        self.set_gui()
        
    def paste_search(self,event=None,text=None):
        ''' Clear the search field and insert set text or
            clipboard contents.
        '''
        self.ent_src.clear_text()
        if text:
            self.ent_src.insert(text=text)
        else:
            self.ent_src.insert(text=sh.Clipboard().paste())
        return 'break'

    def set_values(self):
        self.shift = 1
        self.border = 24
        self.icn_al0 = sh.objs.get_pdir().add ('..','resources'
                                              ,'buttons'
                                              ,'icon_36x36_alphabet_off.gif'
                                              )
        self.icn_al1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_alphabet_on.gif'
                                        )
        self.icn_bl0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_block_off.gif'
                                        )
        self.icn_bl1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_block_on.gif'
                                        )
        self.icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_clear_search_field.gif'
                                        )
        self.icn_def = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_define.gif'
                                        )
        self.icn_bk0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_go_back_off.gif'
                                        )
        self.icn_bk1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_go_back.gif'
                                        )
        self.icn_fw0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_go_forward_off.gif'
                                        )
        self.icn_fw1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_go_forward.gif'
                                        )
        self.icn_ret = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_go_search.gif'
                                        )
        self.icn_brw = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_open_in_browser.gif'
                                        )
        self.icn_ins = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_paste.gif'
                                        )
        self.icn_prn = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_print.gif'
                                        )
        self.icn_pr0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_priority_off.gif'
                                        )
        self.icn_pr1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_priority_on.gif'
                                        )
        self.icn_qit = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_quit_now.gif'
                                        )
        self.icn_rld = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_reload.gif'
                                        )
        self.icn_rp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_repeat_sign_off.gif'
                                        )
        self.icn_rp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_repeat_sign.gif'
                                        )
        self.icn_r20 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_repeat_sign2_off.gif'
                                        )
        self.icn_r21 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_repeat_sign2.gif'
                                        )
        self.icn_sav = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_save_article.gif'
                                        )
        self.icn_src = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_search_article.gif'
                                        )
        self.icn_set = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_settings.gif'
                                        )
        self.icn_abt = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_show_about.gif'
                                        )
        self.icn_sym = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_spec_symbol.gif'
                                        )
        self.icn_hst = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_toggle_history.gif'
                                        )
        self.icn_hor = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_toggle_view_hor.gif'
                                        )
        self.icn_ver = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_toggle_view_ver.gif'
                                        )
        self.icn_cp0 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_watch_clipboard_off.gif'
                                        )
        self.icn_cp1 = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_watch_clipboard_on.gif'
                                        )
        self.icn_swp = sh.objs.pdir.add ('..','resources','buttons'
                                        ,'icon_36x36_swap_langs.gif'
                                        )

    def set_gui(self):
        self.obj = sh.Top(Maximize=True)
        self.frm_prm = sh.Frame (parent = self.obj
                                ,expand = 1
                                )
        self.frm_btm = sh.Frame (parent = self.frm_prm
                                ,expand = 0
                                ,side = 'bottom'
                                )
        self.frm_ver = sh.Frame (parent = self.frm_prm
                                ,expand = 0
                                ,fill = 'y'
                                ,side = 'right'
                                )
        self.widget = th.TkinterHtml(self.frm_prm.widget)
        self.widget.pack(expand='1',fill='both')
        self.set_scroll()
        self.set_frame_panel()
        self.set_icon()
        self.set_title()
        self.set_bindings()
        self.ent_src.focus()
        self.obj.widget.protocol("WM_DELETE_WINDOW",self.close)

    def set_frame_panel(self):
        ''' Do not mix 'self.frm_pnl' and 'self.frm_btm', otherwise,
            they may overlap each other.
        '''
        self.frm_pnl = sh.Frame (parent = self.frm_btm
                                ,expand = 0
                                ,fill = 'x'
                                )
        # Canvas should be created within a frame
        self.cvs_prm = sh.Canvas (parent = self.frm_pnl
                                 ,expand = 0
                                 )
        self.frm_btn = sh.Frame (parent = self.frm_pnl
                                ,expand = 0
                                )
        # A search entry field
        self.ent_src = sh.Entry (parent = self.frm_btn
                                ,side = 'left'
                                ,ipady = 5
                                )
        self.draw_buttons()
        self.cvs_prm.embed(obj=self.frm_btn)
        ''' #TODO: Updating idletasks will show the AllDic 'Please wait'
            message for too long, however, we need to update in order to
            set canvas dimensions correctly.
        '''
        sh.objs.get_root().update_idle()
        height = self.frm_btn.get_height()
        width = self.frm_btn.get_width()
        self.cvs_prm.widget.config(width=self.obj.get_resolution()[0])
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
        self.btn_trn = sh.Button (parent = self.frm_btn
                                 ,text = _('Translate')
                                 ,hint = _('Translate')
                                 ,inactive = self.icn_ret
                                 ,active = self.icn_ret
                                 )

        # A button to clear the search field
        self.btn_clr = sh.Button (parent = self.frm_btn
                                 ,text = _('Clear')
                                 ,hint = _('Clear search field')
                                 ,inactive = self.icn_clr
                                 ,active = self.icn_clr
                                 )

        # A button to insert text into the search field
        self.btn_ins = sh.Button (parent = self.frm_btn
                                 ,text = _('Paste')
                                 ,hint = _('Paste text from clipboard')
                                 ,inactive = self.icn_ins
                                 ,active = self.icn_ins
                                 )
        # A button to insert a current search
        self.btn_rp1 = sh.Button (parent = self.frm_btn
                                 ,text = '!'
                                 ,hint = _('Paste current request')
                                 ,inactive = self.icn_rp0
                                 ,active = self.icn_rp1
                                 )
        # A button to insert a previous search
        self.btn_rp2 = sh.Button (parent = self.frm_btn
                                 ,text = '!!'
                                 ,hint = _('Paste previous request')
                                 ,inactive = self.icn_r20
                                 ,active = self.icn_r21
                                 )
        # A button to insert special symbols
        self.btn_sym = sh.Button (parent = self.frm_btn
                                 ,text = _('Symbols')
                                 ,hint = _('Paste a special symbol')
                                 ,inactive = self.icn_sym
                                 ,active = self.icn_sym
                                 )
        self.opt_src = sh.OptionMenu (parent = self.frm_btn
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        ''' Configure the option menu at the GUI creation time to avoid
            glitches with the search field.
        '''
        self.opt_src.widget.configure (width = 14
                                      ,font = 'Sans 11'
                                      )
        # Drop-down lists with languages
        self.opt_lg1 = sh.OptionMenu (parent = self.frm_btn
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        self.btn_swp = sh.Button (parent = self.frm_btn
                                 ,hint = _('Swap source and target languages')
                                 ,inactive = self.icn_swp
                                 ,active = self.icn_swp
                                 ,text = _('Swap')
                                 )
        self.opt_lg2 = sh.OptionMenu (parent = self.frm_btn
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        self.opt_col = sh.OptionMenu (parent = self.frm_btn
                                     ,items = (1,2,3,4,5,6,7,8,9,10)
                                     ,default = 4
                                     ,Combo = True
                                     ,font = 'Sans 11'
                                     )
        ''' The 'height' argument changes a height of the drop-down
            list and not the main widget.
        '''
        self.opt_lg1.widget.config (width = 11
                                   ,height = 15
                                   )
        self.opt_lg2.widget.config (width = 11
                                   ,height = 15
                                   )
        self.opt_col.widget.config(width=2)
        # A settings button
        self.btn_set = sh.Button (parent = self.frm_btn
                                 ,text = _('Settings')
                                 ,hint = _('Tune up view settings')
                                 ,inactive = self.icn_set
                                 ,active = self.icn_set
                                 )
        # A button to change the article view
        self.btn_viw = sh.Button (parent = self.frm_btn
                                 ,text = _('Toggle view')
                                 ,hint = _('Toggle the article view mode')
                                 ,inactive = self.icn_ver
                                 ,active = self.icn_hor
                                 )
        # A button to toggle dictionary blocking
        self.btn_blk = sh.Button (parent = self.frm_btn
                                 ,text = _('Blacklist')
                                 ,hint = _('Toggle the blacklist')
                                 ,inactive = self.icn_bl0
                                 ,active = self.icn_bl1
                                 )
        # A button to toggle dictionary prioritization
        self.btn_pri = sh.Button (parent = self.frm_btn
                                 ,text = _('Prioritize')
                                 ,hint = _('Toggle prioritizing')
                                 ,inactive = self.icn_pr0
                                 ,active = self.icn_pr1
                                 )
        # A button to toggle dictionary alphabetization
        self.btn_alp = sh.Button (parent = self.frm_btn
                                 ,text = _('Alphabetize')
                                 ,hint = _('Toggle alphabetizing')
                                 ,inactive = self.icn_al0
                                 ,active = self.icn_al1
                                 )
        # A button to move to the previous article
        self.btn_prv = sh.Button (parent = self.frm_btn
                                 ,text = '←'
                                 ,hint = _('Go to the preceding article')
                                 ,inactive = self.icn_bk0
                                 ,active = self.icn_bk1
                                 )
        # A button to move to the next article
        self.btn_nxt = sh.Button (parent = self.frm_btn
                                 ,text = '→'
                                 ,hint = _('Go to the following article')
                                 ,inactive = self.icn_fw0
                                 ,active = self.icn_fw1
                                 )
        # A button to toggle and clear history
        self.btn_hst = sh.Button (parent = self.frm_btn
                                 ,text = _('History')
                                 ,inactive = self.icn_hst
                                 ,active = self.icn_hst
                                 )
        # A button to reload the article
        self.btn_rld = sh.Button (parent = self.frm_btn
                                 ,text = _('Reload')
                                 ,hint = _('Reload the article')
                                 ,inactive = self.icn_rld
                                 ,active = self.icn_rld
                                 )
        # A button to search within the article
        self.btn_ser = sh.Button (parent = self.frm_btn
                                 ,text = _('Search')
                                 ,hint = _('Find in the current article')
                                 ,inactive = self.icn_src
                                 ,active = self.icn_src
                                 )
        # A button to save the article
        self.btn_sav = sh.Button (parent = self.frm_btn
                                 ,text = _('Save')
                                 ,hint = _('Save the current article')
                                 ,inactive = self.icn_sav
                                 ,active = self.icn_sav
                                 )
        # A button to open the current article in a browser
        self.btn_brw = sh.Button (parent = self.frm_btn
                                 ,text = _('Browse')
                                 ,hint = _('Open the current article in a browser')
                                 ,inactive = self.icn_brw
                                 ,active = self.icn_brw
                                 )
        # A button to print the article
        self.btn_prn = sh.Button (parent = self.frm_btn
                                 ,text = _('Print')
                                 ,hint = _('Create a print-ready preview')
                                 ,inactive = self.icn_prn
                                 ,active = self.icn_prn
                                 )
        # A button to define a term
        self.btn_def = sh.Button (parent = self.frm_btn
                                 ,text = _('Define')
                                 ,hint = _('Define the current term')
                                 ,inactive = self.icn_def
                                 ,active = self.icn_def
                                 )
        # A button to toggle capturing Ctrl-c-c and Ctrl-Ins-Ins
        self.btn_cap = sh.Button (parent = self.frm_btn
                                 ,text = _('Clipboard')
                                 ,hint = _('Capture Ctrl-c-c and Ctrl-Ins-Ins')
                                 ,inactive = self.icn_cp0
                                 ,active = self.icn_cp1
                                 ,fg = 'red'
                                 )
        # A button to show info about the program
        self.btn_abt = sh.Button (parent = self.frm_btn
                                 ,text = _('About')
                                 ,hint = _('View About')
                                 ,inactive = self.icn_abt
                                 ,active = self.icn_abt
                                 )
        # A button to quit the program
        self.btn_qit = sh.Button (parent = self.frm_btn
                                 ,text = _('Quit')
                                 ,hint = _('Quit the program')
                                 ,action = self.close
                                 ,inactive = self.icn_qit
                                 ,active = self.icn_qit
                                 ,side = 'right'
                                 )

    def set_bindings(self):
        ''' We need to bind all buttons (inside 'self.frm_btn') and also
            gaps between them and between top-bottom borders
            ('self.cvs_prm').
        '''
        sh.com.bind (obj = self.cvs_prm
                    ,bindings = '<Motion>'
                    ,action = self.set_motion
                    )
        sh.com.bind (obj = self.obj
                    ,bindings = '<Control-q>'
                    ,action = self.close
                    )
        for child in self.frm_btn.widget.winfo_children():
            child.bind('<Motion>',self.set_motion)

    def set_scroll(self):
        sh.Scrollbar (parent = self.frm_ver
                     ,scroll = self
                     )
        sh.Scrollbar (parent = self.frm_btm
                     ,scroll = self
                     ,Horiz = True
                     )
        
    def set_icon(self,path=None):
        if path:
            self.obj.set_icon(path)
        else:
            self.obj.set_icon(ICON)
                          
    def set_title(self,text=None):
        if not text:
            text = 'MClient'
        self.obj.set_title(text)

    def get_height(self):
        sh.objs.get_root().update_idle()
        return self.widget.winfo_height()

    def get_width(self):
        f = '[MClient] gui.WebFrame.get_width'
        sh.objs.get_root().update_idle()
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
        
    def set_motion(self,event=None):
        scr_width = self.obj.get_resolution()[0]
        # Do not move button frame if it is entirely visible
        if self.obj.widget.winfo_width() < self.frm_btn.widget.winfo_reqwidth():
            x = self.cvs_prm.widget.winfo_pointerx()
            ''' We read 'canvas' because it should return positive
                values (in comparison with 'self.frm_btn', which is
                movable). 'rootx' should be negative only when 'canvas'
                is partially moved by a user out of screen (but we may
                need this case too).
            '''
            rootx = self.cvs_prm.widget.winfo_rootx()
            leftx = max (0,rootx)
            rightx = min (rootx + self.cvs_prm.widget.winfo_width()
                         ,scr_width
                         )
            if x <= leftx + self.border:
                self.scroll_left()
            elif x >= rightx - self.border:
                self.scroll_right()
            
    def scroll_left(self):
        f = '[MClient] gui.WebFrame.scroll_left'
        '''
        mes = _('Scroll by {} units to the left').format(self.shift)
        sh.objs.get_mes(f,mes,True).show_debug()
        '''
        self.cvs_prm.widget.xview_scroll(-self.shift,'units')
        
    def scroll_right(self):
        f = '[MClient] gui.WebFrame.scroll_right'
        '''
        mes = _('Scroll by {} units to the right').format(self.shift)
        sh.objs.get_mes(f,mes,True).show_debug()
        '''
        self.cvs_prm.widget.xview_scroll(self.shift,'units')



class Settings:

    def __init__(self):
        self.set_values()
        self.set_gui()

    def set_values(self):
        self.items = (_('Dictionaries')
                     ,_('Word forms')
                     ,_('Transcription')
                     ,_('Parts of speech')
                     ,_('Do not set')
                     )
        self.scitems = (PRODUCT
                       ,_('Multitran')
                       ,_('Cut to the chase')
                       ,_('Clearness')
                       ,_('Custom')
                       )
        self.spitems = (_('Noun'),_('Verb'),_('Adjective')
                       ,_('Abbreviation'),_('Adverb'),_('Preposition')
                       ,_('Pronoun')
                       )
        self.allowed = []
        self.spallow = []

    def update_col1(self):
        f = '[MClient] gui.Settings.update_col1'
        if self.opt_cl1.choice != _('Do not set'):
            if self.opt_cl1.choice in self.allowed:
                self.allowed.remove(self.opt_cl1.choice)
            elif _('Dictionaries') in self.allowed:
                self.opt_cl1.set(_('Dictionaries'))
                self.allowed.remove(_('Dictionaries'))
            elif self.allowed:
                self.opt_cl1.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col2(self):
        f = '[MClient] gui.Settings.update_col2'
        if self.opt_cl2.choice != _('Do not set'):
            if self.opt_cl2.choice in self.allowed:
                self.allowed.remove(self.opt_cl2.choice)
            elif _('Word forms') in self.allowed:
                self.opt_cl2.set(_('Word forms'))
                self.allowed.remove(_('Word forms'))
            elif self.allowed:
                self.opt_cl2.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col3(self):
        f = '[MClient] gui.Settings.update_col3'
        if self.opt_cl3.choice != _('Do not set'):
            if self.opt_cl3.choice in self.allowed:
                self.allowed.remove(self.opt_cl3.choice)
            elif _('Parts of speech') in self.allowed:
                self.opt_cl3.set(_('Parts of speech'))
                self.allowed.remove(_('Parts of speech'))
            elif self.allowed:
                self.opt_cl3.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

    def update_col4(self):
        f = '[MClient] gui.Settings.update_col4'
        if self.opt_cl4.choice != _('Do not set'):
            if self.opt_cl4.choice in self.allowed:
                self.allowed.remove(self.opt_cl4.choice)
            elif _('Transcription') in self.allowed:
                self.opt_cl4.set(_('Transcription'))
                self.allowed.remove(_('Transcription'))
            elif self.allowed:
                self.opt_cl4.set(self.allowed[0])
                self.allowed.remove(self.allowed[0])
            else:
                mes = _('Empty input is not allowed!')
                sh.objs.get_mes(f,mes).show_error()

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
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.opt_scm.choice,self.scitems)
            sh.objs.get_mes(f,mes).show_error()

    def update_by_col1(self,event=None):
        self.allowed = list(self.items)
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col2(self,event=None):
        self.allowed = list(self.items)
        self.update_col2()
        self.update_col1()
        self.update_col3()
        self.update_col4()
        self.update_sc()

    def update_by_col3(self,event=None):
        self.allowed = list(self.items)
        self.update_col3()
        self.update_col1()
        self.update_col2()
        self.update_col4()
        self.update_sc()

    def update_by_col4(self,event=None):
        self.allowed = list(self.items)
        self.update_col4()
        self.update_col1()
        self.update_col2()
        self.update_col3()
        self.update_sc()
        
    def update_by_sp1(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp2(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp2()
        self.update_sp1()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp3(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp3()
        self.update_sp1()
        self.update_sp2()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp4(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp4()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp5()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp5(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp5()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp6()
        self.update_sp7()
        
    def update_by_sp6(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp6()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp7()
        
    def update_by_sp7(self,event=None):
        self.spallow = list(self.spitems)
        self.update_sp7()
        self.update_sp1()
        self.update_sp2()
        self.update_sp3()
        self.update_sp4()
        self.update_sp5()
        self.update_sp6()

    def set_gui(self):
        self.obj = self.parent = sh.Top(AutoCr=True)
        self.set_title()
        self.set_frames()
        self.set_cboxes()
        self.set_labels()
        self.set_columns()
        self.set_buttons()
        self.set_bindings()
        self.set_icon()

    def block_settings(self,event=None):
        f = '[MClient] gui.Settings.block_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def get_priority_settings(self,event=None):
        f = '[MClient] gui.Settings.get_priority_settings'
        mes = _('Not implemented yet!')
        sh.objs.get_mes(f,mes).show_info()

    def set_cboxes(self):
        self.cbx_no1 = sh.CheckBox (parent = self.frm_cb1
                                   ,side = 'left'
                                   )
        self.cbx_no2 = sh.CheckBox (parent = self.frm_cb2
                                   ,side = 'left'
                                   )
        self.cbx_no3 = sh.CheckBox (parent = self.frm_cb3
                                   ,side = 'left'
                                   )
        self.cbx_no4 = sh.CheckBox (parent = self.frm_cb4
                                   ,side = 'left'
                                   )
        self.cbx_no5 = sh.CheckBox (parent = self.frm_cb5
                                   ,side = 'left'
                                   )
        self.cbx_no6 = sh.CheckBox (parent = self.frm_cb6
                                   ,side = 'left'
                                   )
        self.cbx_no7 = sh.CheckBox (parent = self.frm_cb7
                                   ,side = 'left'
                                   )
        self.cbx_no8 = sh.CheckBox (parent = self.frm_cb8
                                   ,side = 'left'
                                   )
        self.cbx_no9 = sh.CheckBox (parent = self.frm_cb9
                                   ,side = 'left'
                                   )
        self.cbx_no10 = sh.CheckBox (parent = self.frm_cb10
                                    ,side = 'left'
                                    )
        self.cbx_no11 = sh.CheckBox (parent = self.frm_cb11
                                    ,side = 'left'
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
        self.cbx_no7.disable()
        self.cbx_no8.enable()
        self.cbx_no9.enable()
        self.cbx_no10.enable()
        self.cbx_no11.enable()

    def set_buttons(self):
        sh.Button (parent = self.frm_btn
                  ,action = self.reset
                  ,hint = _('Reset settings')
                  ,text = _('Reset')
                  ,side = 'left'
                  )

        self.btn_apl = sh.Button (parent = self.frm_btn
                                 ,hint = _('Apply settings')
                                 ,text = _('Apply')
                                 ,side = 'right'
                                 )
        #TODO: elaborate
        '''
        self.btn_blk = sh.Button (parent = self.frm_cb3
                                 ,hint = _('Tune up blacklisting')
                                 ,text = _('Add/Remove')
                                 ,side = 'right'
                                 )
        self.btn_pri = sh.Button (parent = self.frm_cb4
                                 ,hint = _('Tune up prioritizing')
                                 ,text = _('Add/Remove')
                                 ,side = 'right'
                                 )
        '''

    def set_frames(self):
        self.frm_col = sh.Frame (parent = self.obj
                                ,expand = True
                                ,fill = 'both'
                                )
        self.frm_spc = sh.Frame (parent = self.obj
                                ,expand = True
                                ,fill = 'both'
                                )
        self.frm_scm = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl1 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl2 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cl3 = sh.Frame (parent = self.frm_col
                                ,expand = False
                                ,side = 'left'
                                ,fill = 'both'
                                )
        self.frm_cl4 = sh.Frame (parent = self.frm_col
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp1 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp2 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp3 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp4 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp5 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp6 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_sp7 = sh.Frame (parent = self.frm_spc
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'both'
                                )
        self.frm_cb1 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb2 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb3 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb4 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb5 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb6 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb7 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb8 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb9 = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                )
        self.frm_cb10 = sh.Frame (parent = self.obj
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_cb11 = sh.Frame (parent = self.obj
                                 ,expand = False
                                 ,fill = 'x'
                                 )
        self.frm_btn = sh.Frame (parent = self.obj
                                ,expand = False
                                ,fill = 'x'
                                ,side = 'bottom'
                                )

    def set_labels(self):
        ''' Other possible color schemes:
            font = 'Sans 9 italic', fg = 'khaki4'
        '''
        sh.Label (parent = self.frm_scm
                 ,text = _('Style:')
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl1
                 ,text = _('Column') + ' 1:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl2
                 ,text = _('Column') + ' 2:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl3
                 ,text = _('Column') + ' 3:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_cl4
                 ,text = _('Column') + ' 4:'
                 ,font = 'Sans 9'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        self.lbl_no1 = sh.Label (parent = self.frm_cb1
                                ,text = _('Sort by each column (if it is set, except for transcription) and order parts of speech')
                                ,side = 'left'
                                )
        self.lbl_no2 = sh.Label (parent = self.frm_cb2
                                ,text = _('Alphabetize terms')
                                ,side = 'left'
                                )
        self.lbl_no3 = sh.Label (parent = self.frm_cb3
                                ,text = _('Block dictionaries from blacklist')
                                ,side = 'left'
                                )
        self.lbl_no4 = sh.Label (parent = self.frm_cb4
                                ,text = _('Prioritize dictionaries')
                                ,side = 'left'
                                )
        self.lbl_no5 = sh.Label (parent = self.frm_cb5
                                ,text = _('Vertical view')
                                ,side = 'left'
                                )
        self.lbl_no6 = sh.Label (parent = self.frm_cb6
                                ,text = _('Shorten dictionary titles')
                                ,side = 'left'
                                )
        self.lbl_no7 = sh.Label (parent = self.frm_cb7
                                ,text = _('Shorten parts of speech')
                                ,side = 'left'
                                )
        self.lbl_no8 = sh.Label (parent = self.frm_cb8
                                ,text = _('Show user names')
                                ,side = 'left'
                                )
        self.lbl_no9 = sh.Label (parent = self.frm_cb9
                                ,text = _('Select terms only')
                                ,side = 'left'
                                )
        self.lbl_no10 = sh.Label (parent = self.frm_cb10
                                 ,text = _('Iconify the program window after copying')
                                 ,side = 'left'
                                 )
        self.lbl_no11 = sh.Label (parent = self.frm_cb11
                                 ,text = _('Show suggestions on input')
                                 ,side = 'left'
                                 )
        sh.Label (parent = self.frm_sp1
                 ,text = _('Part of speech') + ' 1:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp2
                 ,text = _('Part of speech') + ' 2:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp3
                 ,text = _('Part of speech') + ' 3:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp4
                 ,text = _('Part of speech') + ' 4:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp5
                 ,text = _('Part of speech') + ' 5:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp6
                 ,text = _('Part of speech') + ' 6:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
        sh.Label (parent = self.frm_sp7
                 ,text = _('Part of speech') + ' 7:'
                 ,font = 'Sans 8'
                 ,side = 'top'
                 ,fill = 'both'
                 ,expand = True
                 ,fg = 'PaleTurquoise1'
                 ,bg = 'RoyalBlue3'
                 )
                 
    def set_columns(self):
        self.opt_scm = sh.OptionMenu (parent = self.frm_scm
                                     ,items = self.scitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sc
                                     ,default = PRODUCT
                                     )
        self.opt_cl1 = sh.OptionMenu (parent = self.frm_cl1
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col1
                                     ,default = _('Dictionaries')
                                     )
        self.opt_cl2 = sh.OptionMenu (parent = self.frm_cl2
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col2
                                     ,default = _('Word forms')
                                     )
        self.opt_cl3 = sh.OptionMenu (parent = self.frm_cl3
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col3
                                     ,default = _('Transcription')
                                     )
        self.opt_cl4 = sh.OptionMenu (parent = self.frm_cl4
                                     ,items = self.items
                                     ,side = 'bottom'
                                     ,action = self.update_by_col4
                                     ,default = _('Parts of speech')
                                     )
        self.opt_sp1 = sh.OptionMenu (parent = self.frm_sp1
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp1
                                     ,default = self.spitems[0]
                                     )
        self.opt_sp2 = sh.OptionMenu (parent = self.frm_sp2
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp2
                                     ,default = self.spitems[1]
                                     )
        self.opt_sp3 = sh.OptionMenu (parent = self.frm_sp3
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp3
                                     ,default = self.spitems[2]
                                     )
        self.opt_sp4 = sh.OptionMenu (parent = self.frm_sp4
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp4
                                     ,default = self.spitems[3]
                                     )
        self.opt_sp5 = sh.OptionMenu (parent = self.frm_sp5
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp5
                                     ,default = self.spitems[4]
                                     )
        self.opt_sp6 = sh.OptionMenu (parent = self.frm_sp6
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp6
                                     ,default = self.spitems[5]
                                     )
        self.opt_sp7 = sh.OptionMenu (parent = self.frm_sp7
                                     ,items = self.spitems
                                     ,side = 'bottom'
                                     ,action = self.update_by_sp7
                                     ,default = self.spitems[6]
                                     )

    def set_bindings(self):
        sh.com.bind (obj = self.obj
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.close
                    )
        sh.com.bind (obj = self.lbl_no1
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no1.toggle
                    )
        sh.com.bind (obj = self.lbl_no2
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no2.toggle
                    )
        sh.com.bind (obj = self.lbl_no3
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no3.toggle
                    )
        sh.com.bind (obj = self.lbl_no4
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no4.toggle
                    )
        sh.com.bind (obj = self.lbl_no5
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no5.toggle
                    )
        sh.com.bind (obj = self.lbl_no6
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no6.toggle
                    )
        sh.com.bind (obj = self.lbl_no7
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no7.toggle
                    )
        sh.com.bind (obj = self.lbl_no8
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no8.toggle
                    )
        sh.com.bind (obj = self.lbl_no9
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no9.toggle
                    )
        sh.com.bind (obj = self.lbl_no10
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no10.toggle
                    )
        sh.com.bind (obj = self.lbl_no11
                    ,bindings = '<Button-1>'
                    ,action = self.cbx_no11.toggle
                    )

    def set_title(self,text=_('View Settings')):
        self.obj.set_title(text=text)

    def show(self,event=None):
        self.obj.show()

    def close(self,event=None):
        self.obj.close()

    def set_icon(self,path=None):
        if path:
            self.obj.set_icon(path)
        else:
            self.obj.set_icon(ICON)
    
    def update_sp1(self):
        f = '[MClient] gui.Settings.update_sp1'
        if self.opt_sp1.choice in self.spallow:
            self.spallow.remove(self.opt_sp1.choice)
        elif _('Noun') in self.spallow:
            self.opt_sp1.set(_('Noun'))
            self.spallow.remove(_('Noun'))
        elif self.spallow:
            self.opt_sp1.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
    
    def update_sp2(self):
        f = '[MClient] gui.Settings.update_sp2'
        if self.opt_sp2.choice in self.spallow:
            self.spallow.remove(self.opt_sp2.choice)
        elif _('Verb') in self.spallow:
            self.opt_sp2.set(_('Verb'))
            self.spallow.remove(_('Verb'))
        elif self.spallow:
            self.opt_sp2.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp3(self):
        f = '[MClient] gui.Settings.update_sp3'
        if self.opt_sp3.choice in self.spallow:
            self.spallow.remove(self.opt_sp3.choice)
        elif _('Adjective') in self.spallow:
            self.opt_sp3.set(_('Adjective'))
            self.spallow.remove(_('Adjective'))
        elif self.spallow:
            self.opt_sp3.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp4(self):
        f = '[MClient] gui.Settings.update_sp4'
        if self.opt_sp4.choice in self.spallow:
            self.spallow.remove(self.opt_sp4.choice)
        elif _('Abbreviation') in self.spallow:
            self.opt_sp4.set(_('Abbreviation'))
            self.spallow.remove(_('Abbreviation'))
        elif self.spallow:
            self.opt_sp4.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp5(self):
        f = '[MClient] gui.Settings.update_sp5'
        if self.opt_sp5.choice in self.spallow:
            self.spallow.remove(self.opt_sp5.choice)
        elif _('Adverb') in self.spallow:
            self.opt_sp5.set(_('Adverb'))
            self.spallow.remove(_('Adverb'))
        elif self.spallow:
            self.opt_sp5.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp6(self):
        f = '[MClient] gui.Settings.update_sp6'
        if self.opt_sp6.choice in self.spallow:
            self.spallow.remove(self.opt_sp6.choice)
        elif _('Preposition') in self.spallow:
            self.opt_sp6.set(_('Preposition'))
            self.spallow.remove(_('Preposition'))
        elif self.spallow:
            self.opt_sp6.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()
                       
    def update_sp7(self):
        f = '[MClient] gui.Settings.update_sp7'
        if self.opt_sp7.choice in self.spallow:
            self.spallow.remove(self.opt_sp7.choice)
        elif _('Pronoun') in self.spallow:
            self.opt_sp7.set(_('Pronoun'))
            self.spallow.remove(_('Pronoun'))
        elif self.spallow:
            self.opt_sp7.set(self.spallow[0])
            self.spallow.remove(self.spallow[0])
        else:
            mes = _('Empty input is not allowed!')
            sh.objs.get_mes(f,mes).show_error()



#TODO: make this widget reusable
class Suggest:
    
    def __init__(self):
        self.parent = None
        
    def set_bindings(self):
        sh.com.bind (obj = self.parent
                    ,bindings = '<Escape>'
                    ,action = self.close
                    )
        
    def show(self,lst=['a','b','c'],action=None):
        if not self.parent:
            self.parent = sh.Top(Lock=False)
            self.parent.widget.wm_overrideredirect(1)
            self.lbox = sh.ListBox (parent = self.parent
                                   ,lst = lst
                                   ,action = action
                                   )
            self.set_bindings()
                               
    def close(self):
        if self.parent:
            self.parent.kill()
            self.parent = None



if __name__ == '__main__':
    sh.com.start()
    #WebFrame().show()
    Settings().show()
    sh.com.end()
