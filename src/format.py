#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.graphics.color.controller import Color

from config import CONFIG
from subjects import SUBJECTS


class Block:
    
    def __init__(self, block, colno, Select=False):
        self.colors_bl = (COLORS.b1, COLORS.b2, COLORS.b3, COLORS.b4, COLORS.b5
                         ,COLORS.b6)
        self.colors_pr = (COLORS.p1, COLORS.p2, COLORS.p3, COLORS.p4, COLORS.p5
                         ,COLORS.p6)
        self.code = ''
        self.block = block
        self.colno = colno
        self.Select = Select
    
    def _is_phrase_prior(self):
        if self.block.type == 'phrase':
            return SUBJECTS.is_phrase_prior(self.block.text)
    
    def _is_phrase_blocked(self):
        if self.block.type == 'phrase':
            return SUBJECTS.is_phrase_blocked(self.block.text)
    
    def _is_subj_prior(self):
        # 'phsubj' cannot be prioritized or blocked
        if self.block.type == 'subj':
            return SUBJECTS.is_prioritized(self.block.text)
    
    def _is_subj_blocked(self):
        # 'phsubj' cannot be prioritized or blocked
        if self.block.type == 'subj':
            return SUBJECTS.is_blocked(self.block.text)
    
    def get_color(self):
        if self._is_phrase_prior():
            return COLORS.php
        if self._is_phrase_blocked():
            return COLORS.phb
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['color']
        if self.block.type in ('comment', 'phcount', 'transc'):
            return CONFIG.new['comments']['font']['color']
        if self.block.type == 'user':
            return COLORS.user
        if self.block.type == 'correction':
            return COLORS.correction
        if self._is_subj_blocked():
            return self.colors_bl[self.colno]
        if self._is_subj_prior():
            return self.colors_pr[self.colno]
        try:
            return CONFIG.new['columns'][str(self.colno + 1)]['font']['color']
        except KeyError:
            # Qt accepts empty color names
            return ''
    
    def set_italic(self):
        if self.block.type in ('comment', 'user', 'correction', 'phcount'
                              ,'speech', 'transc'):
            self.code = '<i>' + self.code + '</i>'
    
    def _get_weight(self):
        try:
            weight = CONFIG.new['columns'][str(self.colno + 1)]['font']['weight']
        except KeyError:
            return ('', '')
        match weight:
            case 'bold':
                return ('<b>', '</b>')
            case 'italic':
                return ('<i>', '</i>')
        return ('', '')
    
    def _get_align(self):
        try:
            return CONFIG.new['columns'][str(self.colno + 1)]['font']['align']
        except KeyError:
            return 'left'
    
    def set_fixed(self):
        weight1, weight2 = self._get_weight()
        align = self._get_align()
        self.code = f'''{weight1}<div align="{align}">{self.code}</div>{weight2}'''
    
    def get_family(self):
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['family']
        if self.block.type in ('comment', 'correction', 'phcount', 'transc'
                              ,'user'):
            return CONFIG.new['comments']['font']['family']
        try:
            return CONFIG.new['columns'][str(self.colno + 1)]['font']['family']
        except KeyError:
            return 'Sans'
    
    def get_size(self):
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['size']
        if self.block.type in ('comment', 'correction', 'phcount', 'transc'
                              ,'user'):
            return CONFIG.new['comments']['font']['size']
        try:
            return CONFIG.new['columns'][str(self.colno + 1)]['font']['size']
        except KeyError:
            return 11

    def set_style(self):
        family = self.get_family()
        size = self.get_size()
        color = self.get_color()
        if self.Select:
            ''' I had to put color values in single quotes in Qt5 to work in
                the app (however, quotes had to be removed before saving HTML).
                This is not required now.
            '''
            sub = '''<span style="font-family:{}; font-size:{}pt; color:{}; background-color:{};">{}</span>'''
            self.code = sub.format(family, size, color
                                  ,CONFIG.new['selection']['block']
                                  ,self.block.text)
        else:
            sub = '''<span style="font-family:{}; font-size:{}pt; color:{};">{}</span>'''
            self.code = sub.format(family, size, color, self.block.text)
    
    def run(self):
        if not self.block.text:
            return ''
        self.set_style()
        self.set_fixed()
        self.set_italic()
        return self.code



class Colors:
    
    def __init__(self):
        self.factor = 140
        # No need to set default colors, Qt ignores empty names at input
        self.p1 = self.p2 = self.p3 = self.p4 = self.p5 = self.p6 = self.b1 \
                = self.b2 = self.b3 = self.b4 = self.b5 = self.b6 = self.user \
                = self.php = self.phb = ''
        self.set_constants()
        self.set_tints()
    
    def set_constants(self):
        self.correction = Color('green').get_hex()
    
    def set_tints(self):
        ''' Config values should be converted to HEX since they are further
            used to generate a web-page when saving an article, and browsers,
            unlike Qt, may not understand colors like 'cadet blue' (with or
            without quotes).
        '''
        # color_terms
        icolor = Color(CONFIG.new['terms']['font']['color'])
        CONFIG.new['terms']['font']['color'] = icolor.get_hex()
        
        # color_comments
        icolor = Color(CONFIG.new['comments']['font']['color'])
        CONFIG.new['comments']['font']['color'] = icolor.get_hex()
        darker, self.user = icolor.modify(self.factor)
        
        # color_col1
        icolor = Color(CONFIG.new['columns']['1']['font']['color'])
        CONFIG.new['columns']['1']['font']['color'] = icolor.get_hex()
        self.p1, self.b1 = icolor.modify(self.factor)
        self.php = self.p1
        self.phb = self.b1
        
        # color_col2
        icolor = Color(CONFIG.new['columns']['2']['font']['color'])
        CONFIG.new['columns']['2']['font']['color'] = icolor.get_hex()
        self.p2, self.b2 = icolor.modify(self.factor)
        
        # color_col3
        icolor = Color(CONFIG.new['columns']['3']['font']['color'])
        CONFIG.new['columns']['3']['font']['color'] = icolor.get_hex()
        self.p3, self.b3 = icolor.modify(self.factor)
        
        # color_col4
        icolor = Color(CONFIG.new['columns']['4']['font']['color'])
        CONFIG.new['columns']['4']['font']['color'] = icolor.get_hex()
        self.p4, self.b4 = icolor.modify(self.factor)
        
        # color_col5
        icolor = Color(CONFIG.new['columns']['5']['font']['color'])
        CONFIG.new['columns']['5']['font']['color'] = icolor.get_hex()
        self.p5, self.b5 = icolor.modify(self.factor)
        
        # color_col6
        icolor = Color(CONFIG.new['columns']['6']['font']['color'])
        CONFIG.new['columns']['6']['font']['color'] = icolor.get_hex()
        self.p6, self.b6 = icolor.modify(self.factor)


COLORS = Colors()