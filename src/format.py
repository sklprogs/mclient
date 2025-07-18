#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.graphics.color.controller import Color

from config import CONFIG
from subjects import SUBJECTS


class Block:
    
    def __init__(self, block, colno, Select=False):
        self.colors_bl = (objs.get_colors().b1, objs.colors.b2, objs.colors.b3
                         ,objs.colors.b4)
        self.colors_pr = (objs.colors.p1, objs.colors.p2, objs.colors.p3
                         ,objs.colors.p4)
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
            return objs.get_colors().php
        if self._is_phrase_blocked():
            return objs.get_colors().phb
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['color']
        if self.block.type in ('comment', 'phcount', 'transc'):
            return CONFIG.new['comments']['font']['color']
        if self.block.type == 'user':
            return objs.get_colors().user
        if self.block.type == 'correction':
            return objs.get_colors().correction
        if self._is_subj_blocked():
            return self.colors_bl[self.colno]
        if self._is_subj_prior():
            return self.colors_pr[self.colno]
        if self.colno == 0:
            return CONFIG.new['columns']['1']['font']['color']
        if self.colno == 1:
            return CONFIG.new['columns']['2']['font']['color']
        if self.colno == 2:
            return CONFIG.new['columns']['3']['font']['color']
        if self.colno == 3:
            return CONFIG.new['columns']['4']['font']['color']
        # Qt accepts empty color names
        return ''
    
    def set_italic(self):
        if self.block.type in ('comment', 'user', 'correction', 'phcount'
                              ,'speech', 'transc'):
            self.code = '<i>' + self.code + '</i>'
    
    def set_fixed(self):
        if self.colno == 0:
            self.code = f'''<b><div align="{CONFIG.new['columns']['1']['font']['align']}">{self.code}</div></b>'''
        elif self.colno == 1:
            self.code = f'''<b><div align="{CONFIG.new['columns']['2']['font']['align']}">{self.code}</div></b>'''
        elif self.colno == 2:
            self.code = f'''<div align="{CONFIG.new['columns']['3']['font']['align']}">{self.code}</div>'''
        elif self.colno == 3:
            self.code = f'''<div align="{CONFIG.new['columns']['4']['font']['align']}">{self.code}</div>'''
    
    def get_family(self):
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['family']
        if self.block.type in ('comment', 'correction', 'phcount', 'transc'
                              ,'user'):
            return CONFIG.new['comments']['font']['family']
        if self.colno == 0:
            return CONFIG.new['columns']['1']['font']['family']
        if self.colno == 1:
            return CONFIG.new['columns']['2']['font']['family']
        if self.colno == 2:
            return CONFIG.new['columns']['3']['font']['family']
        if self.colno == 3:
            return CONFIG.new['columns']['4']['font']['family']
        return 'Sans'
    
    def get_size(self):
        if self.block.type in ('phrase', 'term'):
            return CONFIG.new['terms']['font']['size']
        if self.block.type in ('comment', 'correction', 'phcount', 'transc'
                              ,'user'):
            return CONFIG.new['comments']['font']['size']
        if self.colno == 0:
            return CONFIG.new['columns']['1']['font']['size']
        if self.colno == 1:
            return CONFIG.new['columns']['2']['font']['size']
        if self.colno == 2:
            return CONFIG.new['columns']['3']['font']['size']
        if self.colno == 3:
            return CONFIG.new['columns']['4']['font']['size']
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
        self.set_values()
        self.set_constants()
        self.set_tints()
    
    def set_values(self):
        self.factor = 140
        # No need to set default colors, Qt ignores empty names at input
        self.p1 = self.p2 = self.p3 = self.p4 = self.b1 = self.b2 = self.b3 \
        = self.b4 = self.user = self.php = self.phb = ''
    
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



class Objects:
    
    def __init__(self):
        self.colors = None
    
    def get_colors(self):
        if self.colors is None:
            self.colors = Colors()
        return self.colors


objs = Objects()
