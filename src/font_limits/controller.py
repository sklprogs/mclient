#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from font_limits.gui import FontLimits as guiFontLimits


class FontLimits:
    
    def __init__(self, family, size, Bold=False, Italic=False):
        self.set_values()
        self.family = family
        self.size = size
        self.Bold = Bold
        self.Italic = Italic
        self.gui = guiFontLimits()
        self.set_font()
    
    def set_values(self):
        self.family = 'Sans'
        self.text = ''
        self.font = None
        self.size = 0
        self.Bold = False
        self.Italic = False
    
    def set_text(self, text):
        self.text = str(text)
    
    def set_font(self):
        # 400 is normal, 700 - bold
        if self.Bold:
            weight = 700
        else:
            weight = 400
        self.font = self.gui.get_font(self.family
                                     ,size = self.size
                                     ,weight = weight
                                     ,italic = self.Italic)
    
    def get_space(self):
        space = self.gui.get_space(self.text, self.font)
        #mes = _('Space: {}').format(space)
        #Message(f, mes).show_debug()
        return space
