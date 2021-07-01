#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
from . import gui as gi


class About:

    def __init__(self):
        self.Active = False
        self.gui = None
    
    def toggle(self,event=None):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def close(self):
        self.Active = False
        self.get_gui().close()
    
    def show(self):
        self.Active = True
        self.get_gui().show()
    
    def set_gui(self):
        self.gui = gi.About()
        self.set_bindings()
        self.gui.lbl_abt.set_font(sh.lg.globs['str']['font_style'])
        
    def set_bindings(self):
        sh.com.bind (obj = self.get_gui().obj
                    ,bindings = sh.lg.globs['str']['bind_show_about']
                    ,action = self.toggle
                    )
        self.gui.btn_thd.action = self.show_third_parties
        self.gui.btn_lic.action = self.open_license_url
        self.gui.btn_eml.action = self.send_feedback

    def send_feedback(self,event=None):
        # Compose an email to the author
        sh.Email (email = sh.lg.email
                 ,subject = _('On {}').format(gi.PRODUCT)
                 ).create()

    def open_license_url(self,event=None):
        # Open a license web-page
        ionline = sh.Online()
        ionline.url = sh.lg.globs['license_url']
        ionline.browse()

    def show_third_parties(self,event=None):
        # Show info about third-party licenses
        pass
