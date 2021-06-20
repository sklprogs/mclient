#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')
icn_clr = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_clear_selection.gif'
                           )
icn_grb = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_double_back.gif'
                           )
icn_gru = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_double_forward.gif'
                           )
icn_lft = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_go_back.gif'
                           )
icn_rht = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_go_forward.gif'
                           )
icn_rld = sh.objs.pdir.add ('..','resources','buttons'
                           ,'icon_36x36_reload.gif'
                           )


class Blacklist:
    
    def __init__(self):
        self.set_gui()
    
    def get_checkbox(self):
        return self.cbx_blk.get()
    
    def set_checkbox(self,Active=False):
        self.cbx_blk.set(Active)
    
    def set_block(self):
        self.cbx_blk = sh.CheckBox (parent = self.frm_bm2
                                   ,side = 'left'
                                   )
        self.lbl_blk = sh.Label (parent = self.frm_bm2
                                ,text = _('Block subjects')
                                ,side = 'left'
                                )
    
    def set_scrolly(self):
        sh.Scrollbar (parent = self.frm_vr1
                     ,scroll = self.lbx_lft
                     )
        sh.Scrollbar (parent = self.frm_vr2
                     ,scroll = self.lbx_rht
                     )
    
    def select_mult1(self,indexes):
        self.lbx_lft.select_mult(indexes)
    
    def select_mult2(self,indexes):
        self.lbx_rht.select_mult(indexes)
    
    def colorize1(self,i,bg='cyan'):
        self.lbx_lft.widget.itemconfig(i,{'bg':bg})
    
    def colorize2(self,i,bg='cyan'):
        self.lbx_rht.widget.itemconfig(i,{'bg':bg})
    
    def get_index_mult1(self):
        return self.lbx_lft.get_index_mult()
    
    def get_index_mult2(self):
        return self.lbx_rht.get_index_mult()
    
    def get_sel1(self):
        return self.lbx_lft.get()
    
    def get_sel2(self):
        return self.lbx_rht.get()
    
    def clear_sel1(self):
        self.lbx_lft.clear_sel()
    
    def clear_sel2(self):
        self.lbx_rht.clear_sel()
    
    def reset1(self,lst=[]):
        self.lbx_lft.reset(lst)
        self.clear_sel1()
    
    def reset2(self,lst=[]):
        self.lbx_rht.reset(lst)
        self.clear_sel2()
    
    def get1(self):
        return self.lbx_lft.lst
    
    def get2(self):
        return self.lbx_rht.lst
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_frames(self):
        self.frm_top = sh.Frame (parent = self.parent
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,side = 'bottom'
                                ,expand = False
                                )
        self.frm_bm1 = sh.Frame (parent = self.frm_btm
                                ,side = 'left'
                                )
        self.frm_bm2 = sh.Frame (parent = self.frm_btm
                                ,side = 'left'
                                )
        self.frm_bm3 = sh.Frame (parent = self.frm_btm
                                ,side = 'right'
                                ,expand = False
                                )
        self.frm_lft = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,propag = False
                                ,width = 350
                                )
        self.frm_vr1 = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,expand = False
                                ,fill = 'y'
                                )
        self.frm_cnt = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,expand = False
                                )
        self.frm_rht = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                ,propag = False
                                ,width = 350
                                )
        self.frm_vr2 = sh.Frame (parent = self.frm_top
                                ,expand = False
                                ,fill = 'y'
                                ,side = 'left'
                                )
        self.frm_bt1 = sh.Frame (parent = self.frm_cnt
                                ,side = 'top'
                                )
        self.frm_bt2 = sh.Frame (parent = self.frm_cnt
                                ,side = 'top'
                                ,expand = False
                                )
        self.frm_bt3 = sh.Frame (parent = self.frm_cnt
                                ,side = 'bottom'
                                )
    
    def set_listboxes(self):
        self.lbx_lft = sh.ListBox (parent = self.frm_lft
                                  ,Multiple = True
                                  )
        self.lbx_rht = sh.ListBox (parent = self.frm_rht
                                  ,Multiple = True
                                  )
    
    def set_buttons(self):
        self.btn_lft = sh.Button (parent = self.frm_cnt
                                 ,hint = _('Block selection on the right')
                                 ,inactive = icn_lft
                                 ,active = icn_lft
                                 ,text = '←'
                                 ,side = 'top'
                                 ,expand = 0
                                 ,hdir = 'bottom'
                                 )
        self.btn_rht = sh.Button (parent = self.frm_cnt
                                 ,hint = _('Unblock selection on the left')
                                 ,inactive = icn_rht
                                 ,active = icn_rht
                                 ,text = '→'
                                 ,side = 'top'
                                 ,expand = 0
                                 ,hdir = 'bottom'
                                 )
        self.btn_grb = sh.Button (parent = self.frm_cnt
                                 ,hint = _('Block related subjects')
                                 ,inactive = icn_grb
                                 ,active = icn_grb
                                 ,text = '⟸'
                                 ,side = 'top'
                                 ,expand = 0
                                 ,hdir = 'bottom'
                                 )
        self.btn_gru = sh.Button (parent = self.frm_cnt
                                 ,hint = _('Unblock related subjects')
                                 ,inactive = icn_gru
                                 ,active = icn_gru
                                 ,text = '⇒'
                                 ,side = 'top'
                                 ,expand = 0
                                 ,hdir = 'bottom'
                                 )
        self.btn_clr = sh.Button (parent = self.frm_cnt
                                 ,hint = _('Clear selection in both panes')
                                 ,inactive = icn_clr
                                 ,active = icn_clr
                                 ,text = _('Clear')
                                 ,side = 'top'
                                 ,expand = 0
                                 ,hdir = 'bottom'
                                 )
        self.btn_rld = sh.Button (parent = self.frm_cnt
                                 ,text = _('Reload')
                                 ,hint = _('Reload settings')
                                 ,inactive = icn_rld
                                 ,active = icn_rld
                                 ,expand = 0
                                 ,side = 'top'
                                 ,hdir = 'bottom'
                                 )
        self.btn_cls = sh.Button (parent = self.frm_bm1
                                 ,text = _('Close')
                                 ,hint = _('Close this window')
                                 ,expand = 0
                                 ,side = 'left'
                                 ,hdir = 'top'
                                 )
        self.btn_all = sh.Button (parent = self.frm_bm3
                                 ,text = _('All')
                                 ,hint = _('Show all subjects')
                                 ,expand = 0
                                 ,side = 'left'
                                 ,hdir = 'top'
                                 )
        self.btn_art = sh.Button (parent = self.frm_bm3
                                 ,text = _('Article')
                                 ,hint = _('Show subjects from the current article')
                                 ,expand = 0
                                 ,side = 'right'
                                 ,hdir = 'top'
                                 )
    
    def set_widgets(self):
        self.set_frames()
        self.set_listboxes()
        self.set_buttons()
        self.set_block()
    
    def set_gui(self):
        self.parent = sh.Top (icon = ICON
                             ,title = _('Subject blocking')
                             )
        self.widget = self.parent.widget
        sh.Geometry(self.parent).set('800x450')
        self.set_widgets()
        self.set_scrolly()
        self.lbx_lft.focus()


if __name__ == '__main__':
    f = '[MClient] subjects.blacklist.gui.__main__'
    sh.com.start()
    Blacklist().show()
    sh.com.end()
