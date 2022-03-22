#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

VERSION = '6.13.2 (equal_columns branch)'
CURYEAR = 2022
ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_mclient.gif')


class About:

    def __init__(self):
        self.set_gui()
        
    def set_gui(self):
        self.obj = self.parent = sh.Top()
        self.widget = self.obj.widget
        self.set_frames()
        self.set_labels()
        self.set_buttons()
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
    
    def close(self,event=None):
        self.obj.close()

    def show(self,event=None):
        self.obj.show()
