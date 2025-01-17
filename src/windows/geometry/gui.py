#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import win32gui
import win32con


class Geometry:
    
    def enumerate(self, callback, keyword):
        win32gui.EnumWindows(callback, keyword)
    
    def get_title(self, handle):
        return win32gui.GetWindowText(handle)
    
    def get_handle(self, title):
        # Orphaned for now
        return win32gui.FindWindow(None, title)
    
    def activate(self, handle=''):
        ''' It is important to choose the right flag, the window may not
            be shown otherwise.
        '''
        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        elif win32gui.GetWindowPlacement(handle)[1] in (win32con.SW_SHOWMAXIMIZED
                                                       ,win32con.SW_MAXIMIZE):
            win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
        else:
            win32gui.ShowWindow(handle, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(handle)
