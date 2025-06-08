#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.online import Email, ONLINE
from skl_shared.logic import email, com
from skl_shared.paths import PDIR
from skl_shared.text_file import Read


class ThirdParties:
    
    def send_feedback(self):
        Email(email, _('On MClient')).create()

    def open_license_url(self):
        ONLINE.url = com.license_url
        ONLINE.browse()
    
    def fill(self):
        file = PDIR.add('..', 'resources', 'third parties.txt')
        return Read(file).get()
