#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep

from third_parties.gui import ThirdParties as guiThirdParties
from third_parties.logic import ThirdParties as lgThirdParties


class ThirdParties:
    
    def __init__(self):
        self.gui = guiThirdParties()
        self.logic = lgThirdParties()
        self.set_gui()
    
    def send_feedback(self):
        self.logic.send_feedback()

    def open_license_url(self):
        self.logic.open_license_url()
    
    def fill(self):
        self.gui.fill(self.logic.fill())
    
    def set_title(self, title=_('Third parties')):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.set_bindings()
        self.set_title()
        self.fill()
    
    def show(self):
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.gui.close()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)


THIRD_PARTIES = ThirdParties()
