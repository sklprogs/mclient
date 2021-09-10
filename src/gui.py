#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinterhtml as th
from skl_shared.localize import _
import skl_shared.shared as sh

PRODUCT = 'MClient'
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')


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
                      ,_('Copy the code of the article to clipboard')
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

    def get_item(self):
        return self.lbx.get()
    
    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('History')
                             )
        self.widget = self.parent.widget
        self.lbx = sh.ListBox(self.parent)
        sh.Geometry(self.parent).set('250x350')

    def show(self,event=None):
        self.lbx.focus()
        self.parent.show()

    def close(self,event=None):
        self.parent.close()



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
        self.obj.widget.protocol('WM_DELETE_WINDOW',self.close)

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
        self.set_buttons()
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

    def set_buttons(self):
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
        # A button to toggle subject blocking
        self.btn_blk = sh.Button (parent = self.frm_btn
                                 ,text = _('Blacklist')
                                 ,hint = _('Configure blacklisting')
                                 ,inactive = self.icn_bl0
                                 ,active = self.icn_bl1
                                 )
        # A button to toggle subject prioritization
        self.btn_pri = sh.Button (parent = self.frm_btn
                                 ,text = _('Prioritize')
                                 ,hint = _('Configure prioritization')
                                 ,inactive = self.icn_pr0
                                 ,active = self.icn_pr1
                                 )
        # A button to toggle subject alphabetization
        self.btn_alp = sh.Button (parent = self.frm_btn
                                 ,text = _('Alphabetize')
                                 ,hint = _('Toggle alphabetizing')
                                 ,inactive = self.icn_al0
                                 ,active = self.icn_al1
                                 )
        # A button to change the article view
        self.btn_viw = sh.Button (parent = self.frm_btn
                                 ,text = _('Toggle view')
                                 ,hint = _('Toggle the article view mode')
                                 ,inactive = self.icn_ver
                                 ,active = self.icn_hor
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



if __name__ == '__main__':
    sh.com.start()
    WebFrame().show()
    sh.com.end()
