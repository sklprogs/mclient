#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class ThirdParties:
    
    def send_feedback(self):
        sh.Email (email = sh.lg.email
                 ,subject = _('On MClient')
                 ).create()

    def open_license_url(self):
        ionline = sh.Online()
        ionline.url = sh.com.license_url
        ionline.browse()
    
    def fill(self):
        file = sh.objs.get_pdir().add('..','resources','third parties.txt')
        return sh.ReadTextFile(file).get()
