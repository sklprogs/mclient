#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.list import List


class About:
    
    def __init__(self):
        self.product = 'MClient'
        self.version = '7.1.6'
        self.curyear = 2025
        self.code = []
    
    def get_product(self):
        return List([self.product, self.version]).space_items()
    
    def set_code(self):
        self.set_group()
        self.set_license()
        self.set_contact()
        self.code = '<br>'.join(self.code)
        self.code = '<span style="font-family: Serif; font-size:{}pt">{}</span>'.format(12, self.code)
        return self.code
    
    def set_group(self):
        sub = _('Programming: Peter Sklyar, 2015-{}.').format(self.curyear)
        sub = sub.format(self.curyear, self.version)
        sub2 = _('Version: {}').format(self.version)
        text = sub + '<br>' + sub2
        text = '<div align="center">{}</div>'.format(text)
        self.code.append(text)
    
    def set_license(self):
        text = _('This program is free and opensource. You can use and modify it freely')
        self.code.append(text)
        text = _('within the scope of the provisions set forth in GPL v.3 and the active legislation.')
        self.code.append(text)
    
    def set_contact(self):
        text = _('If you have any questions, requests, etc., please do not hesitate to contact me.')
        self.code.append(text)
