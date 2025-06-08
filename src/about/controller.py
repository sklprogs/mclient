#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _

from third_parties.controller import THIRD_PARTIES

from about.gui import About as guiAbout
from about.logic import About as lgAbout


class About:
    
    def __init__(self):
        self.gui = guiAbout()
        self.logic = lgAbout()
        self.Shown = False
        self.set_text()
        self.set_title()
        self.set_bindings()
    
    def get_product(self):
        return self.logic.get_product()
    
    def set_title(self, title=_('About the program')):
        self.gui.set_title(title)
    
    def set_text(self, text=''):
        if not text:
            text = self.logic.set_code()
        self.gui.set_text(text)
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.bind(('F1',), self.toggle)
        self.gui.sig_close.connect(self.close)
        self.gui.btn_thd.set_action(THIRD_PARTIES.show)
        self.gui.btn_lic.set_action(THIRD_PARTIES.open_license_url)
        self.gui.btn_eml.set_action(THIRD_PARTIES.send_feedback)
    
    def centralize(self):
        self.gui.centralize()
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()


ABOUT = About()
