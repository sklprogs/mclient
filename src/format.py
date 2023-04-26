#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.shared as sh

import subjects.subjects as sj


class Block:
    
    def __init__(self, block, colno):
        self.colors_bl = (objs.get_colors().b1, objs.colors.b2, objs.colors.b3
                         ,objs.colors.b4
                         )
        self.colors_pr = (objs.get_colors().p1, objs.colors.p2, objs.colors.p3
                         ,objs.colors.p4
                         )
        self.code = ''
        self.block = block
        self.colno = colno
    
    def _is_phrase_prior(self):
        if self.block.type_ == 'phrase':
            return sj.objs.get_order().is_prioritized(self.block.text)
    
    def _is_phrase_blocked(self):
        if self.block.type_ == 'phrase':
            return sj.objs.get_order().is_blocked(self.block.text)
    
    def _is_subj_prior(self):
        # 'phsubj' cannot be prioritized or blocked
        if self.block.type_ == 'subj':
            return sj.objs.get_order().is_prioritized(self.block.text)
    
    def _is_subj_blocked(self):
        # 'phsubj' cannot be prioritized or blocked
        if self.block.type_ == 'subj':
            return sj.objs.get_order().is_blocked(self.block.text)
    
    def get_color(self):
        if self._is_phrase_prior():
            return objs.get_colors().php
        if self._is_phrase_blocked():
            return objs.get_colors().phb
        if self.block.type_ in ('phrase', 'term'):
            return sh.lg.globs['str']['color_terms']
        if self.block.type_ in ('comment', 'phcount', 'transc'):
            return sh.lg.globs['str']['color_comments']
        if self.block.type_ == 'user':
            return objs.get_colors().user
        if self.block.type_ == 'correction':
            return objs.get_colors().correction
        if self._is_subj_blocked():
            return self.colors_bl[self.colno]
        if self._is_subj_prior():
            return self.colors_pr[self.colno]
        if self.colno == 0:
            return sh.lg.globs['str']['color_col1']
        if self.colno == 1:
            return sh.lg.globs['str']['color_col2']
        if self.colno == 2:
            return sh.lg.globs['str']['color_col3']
        if self.colno == 3:
            return sh.lg.globs['str']['color_col4']
        # Qt accepts empty color names
        return ''
    
    def set_italic(self):
        if self.block.type_ in ('comment', 'user', 'correction', 'phcount'
                               ,'speech', 'transc'
                               ):
            self.code = '<i>' + self.code + '</i>'
    
    def set_bold(self):
        if self.colno == 0:
            self.code = '<b>' + self.code + '</b>'
    
    def get_family(self):
        if self.block.type_ in ('phrase', 'term'):
            return sh.lg.globs['str']['font_terms_family']
        if self.block.type_ in ('comment', 'correction', 'phcount', 'transc'
                               ,'user'
                               ):
            return sh.lg.globs['str']['font_comments_family']
        if self.colno == 0:
            return sh.lg.globs['str']['font_col1_family']
        if self.colno == 1:
            return sh.lg.globs['str']['font_col2_family']
        if self.colno == 2:
            return sh.lg.globs['str']['font_col3_family']
        if self.colno == 3:
            return sh.lg.globs['str']['font_col4_family']
        return 'Sans'
    
    def get_size(self):
        if self.block.type_ in ('phrase', 'term'):
            return sh.lg.globs['int']['font_terms_size']
        if self.block.type_ in ('comment', 'correction', 'phcount', 'transc'
                               ,'user'
                               ):
            return sh.lg.globs['int']['font_comments_size']
        if self.colno == 0:
            return sh.lg.globs['int']['font_col1_size']
        if self.colno == 1:
            return sh.lg.globs['int']['font_col2_size']
        if self.colno == 2:
            return sh.lg.globs['int']['font_col3_size']
        if self.colno == 3:
            return sh.lg.globs['int']['font_col4_size']
        return 11

    def set_style(self):
        family = self.get_family()
        size = self.get_size()
        color = self.get_color()
        # Color name must be put in single quotes
        sub = '''<span style="font-family:{}; font-size:{}pt; color:'{}';">{}</span>'''
        self.code = sub.format(family, size, color, self.block.text)
    
    def run(self):
        if not self.block.text:
            return ''
        self.set_style()
        self.set_bold()
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
        self.php = sh.Color('red').get_hex()
        self.phb = sh.Color('gray').get_hex()
        self.correction = sh.Color('green').get_hex()
    
    def set_tints(self):
        ''' Config values should be converted to HEX since they are further
            used to generate a web-page when saving an article, and browsers,
            unlike Qt, may not understand colors like 'cadet blue' (with or
            without quotes).
        '''
        # color_terms
        icolor = sh.Color(sh.lg.globs['str']['color_terms'])
        sh.lg.globs['str']['color_terms'] = icolor.get_hex()
        
        # color_comments
        icolor = sh.Color(sh.lg.globs['str']['color_comments'])
        sh.lg.globs['str']['color_comments'] = icolor.get_hex()
        darker, self.user = icolor.modify(self.factor)
        
        # color_col1
        icolor = sh.Color(sh.lg.globs['str']['color_col1'])
        sh.lg.globs['str']['color_col1'] = icolor.get_hex()
        self.p1, self.b1 = icolor.modify(self.factor)
        
        # color_col2
        icolor = sh.Color(sh.lg.globs['str']['color_col2'])
        sh.lg.globs['str']['color_col2'] = icolor.get_hex()
        self.p2, self.b2 = icolor.modify(self.factor)
        
        # color_col3
        icolor = sh.Color(sh.lg.globs['str']['color_col3'])
        sh.lg.globs['str']['color_col3'] = icolor.get_hex()
        self.p3, self.b3 = icolor.modify(self.factor)
        
        # color_col4
        icolor = sh.Color(sh.lg.globs['str']['color_col4'])
        sh.lg.globs['str']['color_col4'] = icolor.get_hex()
        self.p4, self.b4 = icolor.modify(self.factor)



class Objects:
    
    def __init__(self):
        self.colors = None
    
    def get_colors(self):
        if self.colors is None:
            self.colors = Colors()
        return self.colors


objs = Objects()
