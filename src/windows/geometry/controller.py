#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Geometry:
    ''' Window behavior is not uniform through different platforms or even
        through different Windows versions.
    '''
    def __init__(self, keyword=''):
        self.title = ''
        self.handle = ''
        self.keyword = keyword
        self.gui = gi.Geometry()
    
    def find_handle(self):
        f = '[MClient] windows.geometry.controller.Geometry.find_handle'
        try:
            self.gui.enumerate(self.enumerate, self.keyword)
        except Exception as e:
            sh.com.rep_failed(f, e)
    
    def get_title(self, handle):
        f = '[MClient] windows.geometry.controller.Geometry.find_handle'
        try:
            return self.gui.get_title(handle)
        except Exception as e:
            sh.com.rep_failed(f, e)
        return ''
    
    def enumerate(self, handle, arg=None):
        # An extra argument is required by win32gui.EnumWindows
        if self.keyword in self.get_title(handle):
            self.handle = handle
    
    def activate(self):
        f = '[MClient] windows.geometry.controller.Geometry.activate'
        self.find_handle()
        try:
            self.gui.activate(self.handle)
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes, True).show_warning()
