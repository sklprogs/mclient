#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.online import Email, ONLINE
from skl_shared_qt.logic import email, com
from skl_shared_qt.paths import PDIR
from skl_shared_qt.text_file import Read


class ThirdParties:
    
    def send_feedback(self):
        Email(email, _('On MClient')).create()

    def open_license_url(self):
        ONLINE.url = com.license_url
        ONLINE.browse()
    
    def fill(self):
        file = PDIR.add('..', 'resources', 'third parties.txt')
        return Read(file).get()
