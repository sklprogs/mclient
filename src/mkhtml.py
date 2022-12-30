#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
import subjects.subjects as sj


class Font:
    
    def __init__ (self,block,blocked_color1='dim gray'
                 ,blocked_color2='dim gray',blocked_color3='dim gray'
                 ,blocked_color4='dim gray',priority_color1='red'
                 ,priority_color2='red',priority_color3='red'
                 ,priority_color4='red'
                 ):
        self.set_values()
        self.block = block
        self.blocked_color1 = blocked_color1
        self.blocked_color2 = blocked_color2
        self.blocked_color3 = blocked_color3
        self.blocked_color4 = blocked_color4
        self.priority_color1 = priority_color1
        self.priority_color2 = priority_color2
        self.priority_color3 = priority_color3
        self.priority_color4 = priority_color4
    
    def set_values(self):
        self.Success = True
        self.text = ''
        self.family = 'Serif'
        self.color = 'black'
        self.size = 4
        self.Bold = False
        self.Italic = False
        self.rowno = 0
        self.colno = 0
        self.col_width = 0
    
    def run(self):
        self.check()
        self.set_text()
        self.set_pos()
        self.set_family()
        self.set_size()
        self.set_color()
        self.set_bold()
        self.set_italic()
    
    def set_pos(self):
        f = '[MClient] mkhtml.Font.set_pos'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.rowno = self.block.i
        self.colno = self.block.j
    
    def _set_color(self):
        if self.block.Fixed:
            if self.colno == 0:
                self.color = sh.lg.globs['str']['color_col1']
            elif self.colno == 1:
                self.color = sh.lg.globs['str']['color_col2']
            elif self.colno == 2:
                self.color = sh.lg.globs['str']['color_col3']
            elif self.colno == 3:
                self.color = sh.lg.globs['str']['color_col4']
        elif self.block.type_ in ('phrase','term'):
            self.color = sh.lg.globs['str']['color_terms']
        elif self.block.type_ in ('comment','phcom','phcount','transc'):
            self.color = sh.lg.globs['str']['color_comments']
        elif self.block.type_ == 'correction':
            self.color = 'green'
        elif self.block.type_ == 'user':
            color = sh.lg.globs['str']['color_comments']
            result = sh.com.get_mod_color (color = color
                                          ,delta = 75
                                          )
            if result:
                color = result
            self.color = color
    
    def _set_color_p(self):
        if self.block.Fixed:
            if self.colno == 0:
                self.color = self.priority_color1
            elif self.colno == 1:
                self.color = self.priority_color2
            elif self.colno == 2:
                self.color = self.priority_color3
            elif self.colno == 3:
                self.color = self.priority_color4
        else:
            self.color = self.priority_color1
    
    def _set_color_b(self):
        if self.block.Fixed:
            if self.colno == 0:
                self.color = self.blocked_color1
            elif self.colno == 1:
                self.color = self.blocked_color2
            elif self.colno == 2:
                self.color = self.blocked_color3
            elif self.colno == 3:
                self.color = self.blocked_color4
        else:
            self.color = 'dim gray'
    
    def set_bold(self):
        f = '[MClient] mkhtml.Font.set_bold'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.colno == 0 and self.block.Fixed \
        or self.block.type_ in ('dic','phdic','wform'):
            self.Bold = True
    
    def set_italic(self):
        f = '[MClient] mkhtml.Font.set_italic'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.type_ in ('comment','correction','phcom'
                               ,'phcount','speech','transc','user'
                               ):
            self.Italic = True
    
    def set_color(self):
        f = '[MClient] mkhtml.Font.set_color'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' We need to determine whether a block is blockable or
            prioritizable irrespectively of its state in a current view,
            so we do not rely on 'block' values.
        '''
        if sj.objs.get_article().is_blocked(self.block.text):
            self._set_color_b()
        elif sj.objs.article.get_priority(self.block.text) > 0:
            self._set_color_p()
        else:
            self._set_color()
    
    def set_text(self):
        f = '[MClient] mkhtml.Font.set_text'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.text = self.block.text
    
    def check(self):
        f = '[MClient] mkhtml.Font.check'
        if self.block and self.blocked_color1 and self.blocked_color2 \
        and self.blocked_color3 and self.blocked_color4 \
        and self.priority_color1 and self.priority_color2 \
        and self.priority_color3 and self.priority_color4:
            pass
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_family(self):
        f = '[MClient] mkhtml.Font.set_family'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.Fixed:
            if self.colno == 0:
                self.family = sh.lg.globs['str']['font_col1_family']
            elif self.colno == 1:
                self.family = sh.lg.globs['str']['font_col2_family']
            elif self.colno == 2:
                self.family = sh.lg.globs['str']['font_col3_family']
            elif self.colno == 3:
                self.family = sh.lg.globs['str']['font_col4_family']
        elif self.block.type_ in ('comment','correction','phcom'
                                 ,'phcount','transc','user'
                                 ):
            self.family = sh.lg.globs['str']['font_comments_family']
        elif self.block.type_ in ('phrase','term'):
            self.family = sh.lg.globs['str']['font_terms_family']
    
    def set_size(self):
        f = '[MClient] mkhtml.Font.set_size'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.block.Fixed:
            if self.colno == 0:
                self.size = sh.lg.globs['int']['font_col1_size']
            elif self.colno == 1:
                self.size = sh.lg.globs['int']['font_col2_size']
            elif self.colno == 2:
                self.size = sh.lg.globs['int']['font_col3_size']
            elif self.colno == 3:
                self.size = sh.lg.globs['int']['font_col4_size']
        elif self.block.type_ in ('comment','correction','phcom'
                                 ,'phcount','transc','user'
                                 ):
            self.size = sh.lg.globs['int']['font_comments_size']
        elif self.block.type_ in ('phrase','term'):
            self.size = sh.lg.globs['int']['font_terms_size']



class Fonts:
    
    def __init__(self,Debug=False,maxrows=1000):
        self.set_values()
        self.set_blocked_colors()
        self.set_priority_colors()
        self.Debug = Debug
        self.maxrows = maxrows
    
    def _get_col_width(self,colno):
        f = '[MClient] mkhtml.Fonts._get_col_width'
        for column in self.columns:
            if column.no == colno:
                return column.width
        modes = sorted(set(str(column.no) for column in self.columns))
        modes = '; '.join(modes)
        mes = _('Argument "{}" is not covered by the range of "{}"!')
        mes = mes.format(colno,modes)
        sh.objs.get_mes(f,mes,True).show_warning()
        return 0
    
    def set_column_width(self):
        f = '[MClient] mkhtml.Fonts.set_column_width'
        if not self.Success:
            sh.com.cancel(f)
            return
        for ifont in self.fonts:
            ifont.col_width = self._get_col_width(ifont.colno)
    
    def debug(self):
        f = '[MClient] mkhtml.Fonts.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        nos = [i + 1 for i in range(len(self.fonts))]
        texts = []
        families = []
        colors = []
        sizes = []
        bolds = []
        italics = []
        rownos = []
        colnos = []
        col_widths = []
        for ifont in self.fonts:
            texts.append(ifont.text)
            families.append(ifont.family)
            colors.append(ifont.color)
            sizes.append(ifont.size)
            bolds.append(ifont.Bold)
            italics.append(ifont.Italic)
            rownos.append(ifont.rowno)
            colnos.append(ifont.colno)
            col_widths.append(ifont.col_width)
        headers = (_('#'),_('ROW #'),_('COLUMN #'),_('COLUMN WIDTH (%)')
                  ,_('TEXT'),_('COLOR'),_('FAMILY'),_('SIZE'),_('BOLD')
                  ,_('ITALIC')
                  )
        iterable = [nos,rownos,colnos,col_widths,texts,colors,families
                   ,sizes,bolds,italics
                   ]
        # 10'' screen: 20 symbols
        mes = sh.FastTable (headers = headers
                           ,iterable = iterable
                           ,maxrow = 20
                           ,maxrows = self.maxrows
                           ).run()
        sh.com.run_fast_debug(f,mes)
    
    def reset(self,blocks,columns):
        self.set_values()
        self.blocks = blocks
        self.columns = columns
    
    def set_values(self):
        self.Success = True
        self.fonts = []
        self.blocks = []
        self.columns = []
    
    def set_priority_colors(self):
        delta = -76
        # Column 1 color
        default_color = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col1']
                                             ,delta = delta
                                             )
        if not default_color:
            default_color = 'red'
        
        self.priority_color1 = default_color
        # Column 2 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col2']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color2 = result
        else:
            self.priority_color2 = default_color
        # Column 3 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col3']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color3 = result
        else:
            self.priority_color3 = default_color
        # Column 4 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col4']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color4 = result
        else:
            self.priority_color4 = default_color
            
    def set_blocked_colors(self):
        default_color = 'dim gray'
        delta = 76
        # Column 1 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col1']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color1 = result
        else:
            self.blocked_color1 = default_color
        # Column 2 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col2']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color2 = result
        else:
            self.blocked_color2 = default_color
        # Column 3 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col3']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color3 = result
        else:
            self.blocked_color3 = default_color
        # Column 4 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col4']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color4 = result
        else:
            self.blocked_color4 = default_color
    
    def check(self):
        f = '[MClient] mkhtml.Fonts.check'
        if not self.blocks or not self.columns:
            self.Success = False
            sh.com.rep_empty(f)
    
    def fill(self):
        f = '[MClient] mkhtml.Fonts.fill'
        if not self.Success:
            sh.com.cancel(f)
            return
        for block in self.blocks:
            ifont = Font (block = block
                         ,blocked_color1 = self.blocked_color1
                         ,blocked_color2 = self.blocked_color2
                         ,blocked_color3 = self.blocked_color3
                         ,blocked_color4 = self.blocked_color4
                         ,priority_color1 = self.priority_color1
                         ,priority_color2 = self.priority_color2
                         ,priority_color3 = self.priority_color3
                         ,priority_color4 = self.priority_color4
                         )
            ifont.run()
            self.fonts.append(ifont)
    
    def run(self):
        self.check()
        self.fill()
        self.set_column_width()
        self.debug()
        return self.fonts



class Block:
    # Shortened
    def __init__(self):
        self.i = 0
        self.j = 0
        self.text = ''
        self.type_ = ''


class HTM:

    def __init__(self):
        self.set_values()
    
    def reset(self,fonts,Printer=False,skipped=0,tab_width=0):
        # 'collimit' includes fixed blocks
        self.set_values()
        self.fonts = fonts
        self.Printer = Printer
        self.skipped = skipped
        self.tab_width = tab_width
        
    def set_landscape(self):
        f = '[MClient] mkhtml.HTM.set_landscape'
        if self.Printer:
            file = sh.objs.get_pdir().add ('..','resources'
                                          ,'landscape.html'
                                          )
            code = sh.ReadTextFile(file).get()
            if code:
                ''' Either don't use 'format' here or double all curly
                    braces in the script.
                '''
                self.landscape = code % _('Print')
            else:
                sh.com.rep_empty(f)
    
    def run(self):
        self.set_landscape()
        self.gen_htm()
        return self.htm
    
    def set_values(self):
        self.htm = ''
        self.landscape = ''
        self.skipped = 0
        self.Printer = False
    
    def gen_htm(self):
        ''' #NOTE: mismatch in opening/closing tags may fail finding
            text and thereby the algorithm for setting positions.
        '''
        f = '[MClient] mkhtml.HTM.gen_htm'
        code = []
        code.append('<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        if self.Printer:
            code.append(self.landscape)
            code.append('<div id="printableArea">')
        if self.fonts:
            code.append('<table>')
            old_colno = -1
            old_rowno = -1
            for ifont in self.fonts:
                if old_rowno != ifont.rowno:
                    if ifont.rowno > 0:
                        code.append('</td></tr>')
                    code.append('<tr>')
                ''' #NOTE: Without checking a row number here finding
                    text may fail in the vertical mode when 2 cells
                    have a different row number but the same column
                    number.
                '''
                if old_rowno != ifont.rowno or old_colno != ifont.colno:
                    if ifont.colno > 0 and old_rowno == ifont.rowno:
                        code.append('</td>')
                    if old_rowno == ifont.rowno:
                        delta = ifont.colno - old_colno - 1
                    else:
                        delta = ifont.colno
                    for i in range(delta):
                        col_width = objs.get_fonts()._get_col_width(i)
                        sub = '<td width="{}"/>'
                        sub = sub.format(col_width)
                        code.append(sub)
                    sub = '<td{} valign="top"{}>'
                    if ifont.block.Fixed:
                        sub1 = ' align="center"'
                    else:
                        sub1 = ''
                    if ifont.col_width:
                        sub2 = ' width="{}"'
                        sub2 = sub2.format(ifont.col_width)
                    else:
                        sub2 = ''
                    sub = sub.format(sub1,sub2)
                    code.append(sub)
                    old_colno = ifont.colno
                ''' Cannot be modified immediately after a new row was
                    discovered since 'rowno' is used after that.
                '''
                if old_rowno != ifont.rowno:
                    old_rowno = ifont.rowno
                if ifont.Bold:
                    sub1 = '<b>'
                    sub4 = '</b>'
                else:
                    sub1 = sub4 = ''
                if ifont.Italic:
                    sub2 = '<i>'
                    sub3 = '</i>'
                else:
                    sub2 = sub3 = ''
                sub = '{}{}<font face="{}" color="{}" size="{}">{}</font>{}{}'
                sub = sub.format (sub1,sub2,ifont.family,ifont.color
                                 ,ifont.size,html.escape(ifont.text)
                                 ,sub3,sub4
                                 )
                code.append(sub)
            code.append('</td></tr></table>')
        elif self.skipped:
            code.append('<h1>')
            mes = _('Nothing has been found (skipped subjects: {}).')
            mes = mes.format(self.skipped)
            code.append(mes)
            code.append('</h1>')
        else:
            code.append('<h1>')
            code.append(_('Nothing has been found.'))
            code.append('</h1>')
        if self.Printer:
            code.append('</div>')
        code.append('</meta></body></html>')
        self.htm = ''.join(code)
        return self.htm



class Objects:
    
    def __init__(self):
        self.htm = self.fonts = None
        
    def get_htm(self):
        if self.htm is None:
            self.htm = HTM()
        return self.htm
    
    def get_fonts(self,Debug=False,maxrows=1000):
        if self.fonts is None:
            self.fonts = Fonts(Debug,maxrows)
        return self.fonts


objs = Objects()
