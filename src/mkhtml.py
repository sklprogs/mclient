#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
from skl_shared.localize import _
import skl_shared.shared as sh
import subjects.subjects as sj


# Shortened
class Block:

    def __init__(self):
        self.i = 0
        self.j = 0
        self.text = ''
        self.type_ = ''


class HTM:

    def __init__(self):
        self.set_values()
        self.set_priority_colors()
        self.set_blocked_colors()
    
    def set_width(self):
        f = '[MClient] mkhtml.HTM.set_width'
        if sh.lg.globs['int']['colnum']:
            self.width = int(80/sh.lg.globs['int']['colnum'])
        else:
            sh.com.rep_empty(f)
    
    def _run_user(self):
        if self.block.type_ == 'user':
            color = sh.lg.globs['str']['color_comments']
            result = sh.com.get_mod_color (color = color
                                          ,delta = 75
                                          )
            if result:
                color = result
            c = '<i><font face="{}" size="{}" color="{}">{}</font></i>'
            c = c.format (sh.lg.globs['str']['font_comments_family']
                         ,sh.lg.globs['int']['font_comments_size']
                         ,color
                         ,self.block.text
                         )
            self.output.write(c)
    
    # 'collimit' includes fixed blocks
    def reset (self,data,cols,collimit=9,Printer=False
              ,Reverse=False,phdic='',skipped=0
              ):
        self.set_values()
        self.collimit = collimit
        self.cols = cols
        self.data = data
        self.phdic = phdic
        self.Printer = Printer
        self.Reverse = Reverse
        self.skipped = skipped
        
    def run(self):
        self.set_width()
        self.assign()
        self.gen_htm()
        return self.htm
    
    def set_values(self):
        self.block = None
        self.blocks = []
        self.htm = ''
        self.phdic = ''
        self.script = '''
        <head>

          <div align="center">
            <!-- A button to print the printable area -->
            <input type="button" onclick="printDiv('printableArea')" value="%s" />
          </div>

          <script type="text/javascript">
            function printDiv(divName) {
              var printContents = document.getElementById(divName).innerHTM;
              var originalContents = document.body.innerHTM;
              document.body.innerHTM = printContents;
              window.print();
              document.body.innerHTM = originalContents;
            }
          </script>

          <!-- Print in a landscape mode -->
          <style type="text/css">
            @page
            {
              size: landscape;
              margin: 1.5cm;
            }
          </style>

          <style type="text/css" media="print">
            @page
            {
              size: landscape;
              margin: 1.5cm;
            }
          </style>

        </head>
        '''
        ''' Either don't use 'format' here or double all curly braces
            in the script.
        '''
        self.script = self.script % _('Print')
        self.skipped = 0
        self.width = 0
    
    def set_priority_colors(self):
        default_color = 'red'
        delta = -76
        # Column 1 color
        result = sh.com.get_mod_color (color = sh.lg.globs['str']['color_col1']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color1 = result
        else:
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
    
    def assign(self):
        for item in self.data:
            block = Block()
            block.type_ = item[0]
            block.text = item[1]
            block.i = item[2]
            block.j = item[3]
            self.blocks.append(block)
    
    def _run_dic(self):
        if self.block.type_ in ('dic','phdic') and self.block.text:
            # Suppress useless error output
            if self.block.text == self.phdic:
                Blocked = False
                Prioritized = False
            else:
                Blocked = sj.objs.get_article().is_blocked(self.block.text)
                Prioritized = sj.objs.article.get_priority(self.block.text) > 0
            if Blocked:
                sub = self._get_color_b()
            elif Prioritized:
                sub = self._get_color_p()
            else:
                sub = self._get_color()
            c = '<font face="{}" color="{}" size="{}"><b>{}</b></font>'
            c = c.format (self._get_family()
                         ,sub
                         ,self._get_size()
                         ,self.block.text
                         )
            self.output.write(c)

    def _get_family(self):
        if self.block.xj == 0:
            return sh.lg.globs['str']['font_col1_family']
        elif self.block.xj == 1:
            return sh.lg.globs['str']['font_col2_family']
        elif self.block.xj == 2:
            return sh.lg.globs['str']['font_col3_family']
        elif self.block.xj == 3:
            return sh.lg.globs['str']['font_col4_family']
        else:
            return sh.lg.globs['str']['font_terms_family']
            
    def _get_size(self):
        if self.block.xj == 0:
            return sh.lg.globs['int']['font_col1_size']
        elif self.block.xj == 1:
            return sh.lg.globs['int']['font_col2_size']
        elif self.block.xj == 2:
            return sh.lg.globs['int']['font_col3_size']
        elif self.block.xj == 3:
            return sh.lg.globs['int']['font_col4_size']
        else:
            return sh.lg.globs['int']['font_terms_size']
            
    def _get_color_p(self):
        if self.block.xj == 0:
            return self.priority_color1
        elif self.block.xj == 1:
            return self.priority_color2
        elif self.block.xj == 2:
            return self.priority_color3
        elif self.block.xj == 3:
            return self.priority_color4
        else:
            return 'red'
            
    def _get_color_b(self):
        if self.block.xj == 0:
            return self.blocked_color1
        elif self.block.xj == 1:
            return self.blocked_color2
        elif self.block.xj == 2:
            return self.blocked_color3
        elif self.block.xj == 3:
            return self.blocked_color4
        else:
            return 'dim gray'
    
    def _get_color(self):
        if self.block.xj == 0:
            return sh.lg.globs['str']['color_col1']
        elif self.block.xj == 1:
            return sh.lg.globs['str']['color_col2']
        elif self.block.xj == 2:
            return sh.lg.globs['str']['color_col3']
        elif self.block.xj == 3:
            return sh.lg.globs['str']['color_col4']
        else:
            return sh.lg.globs['str']['color_terms']
    
    def _run_wform(self):
        if self.block.type_ == 'wform':
            c = '<font face="{}" color="{}" size="{}"><b>{}</b></font>'
            c = c.format (self._get_family()
                         ,self._get_color()
                         ,self._get_size()
                         ,self.block.text
                         )
            self.output.write(c)

    def _run_term(self):
        if self.block.type_ in ('term','phrase'):
            c = '<font face="{}" color="{}" size="{}">{}</font>'
            c = c.format (sh.lg.globs['str']['font_terms_family']
                         ,sh.lg.globs['str']['color_terms']
                         ,sh.lg.globs['int']['font_terms_size']
                         ,self.block.text
                         )
            self.output.write(c)

    def _run_speech(self):
        if self.block.type_ == 'speech':
            if self.block.xj == 0:
                sub = '<b>{}</b>'.format(self.block.text)
            else:
                sub = self.block.text
            c = '<font face="{}" color="{}" size="{}"><i>{}</i></font>'
            c = c.format (self._get_family()
                         ,self._get_color()
                         ,self._get_size()
                         ,sub
                         )
            self.output.write(c)
    
    def _run_comment(self):
        if self.block.type_ in ('comment','transc','phcount','phcom'):
            c = '<i><font face="{}" size="{}" color="{}">{}</font></i>'
            c = c.format (sh.lg.globs['str']['font_comments_family']
                         ,sh.lg.globs['int']['font_comments_size']
                         ,sh.lg.globs['str']['color_comments']
                         ,self.block.text
                         )
            self.output.write(c)

    def _run_correction(self):
        if self.block.type_ == 'correction':
            c = '<i><font face="{}" size="{}" color="{}">{}</font></i>'
            c = c.format (sh.lg.globs['str']['font_comments_family']
                         ,sh.lg.globs['int']['font_comments_size']
                         ,'green'
                         ,self.block.text
                         )
            self.output.write(c)

    def gen_htm(self):
        ''' Default Python string concatenation is too slow, so we use
            this module instead.
        '''
        self.output = io.StringIO()
        self.output.write('<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        if self.Printer:
            self.output.write(self.script)
            self.output.write('<div id="printableArea">')
        if self.blocks:
            ''' Sometimes the right end in a multicolumn view is not
                visible. Setting a table width explicitly allows to
                avoid this problem. The value of 82% is picked up by
                trial and error and is the minimum to show EN-RU,
                'deterrence' properly.
                #TODO: remove extra table properties when using a good
                web engine
            '''
            self.output.write('<table style="width: 82%;table-layout:fixed;">')
            if self.Reverse:
                self.output.write('<tr><td valign="top">')
            elif self.blocks and self.blocks[0].text \
            and self.blocks[0].type_ in ('dic','wform','transc'
                                        ,'speech','phdic'
                                        ):
                self.output.write('<tr><td align="center" valign="top">')
            else:
                self.output.write('<tr><td valign="top">')
            i = j = 0
            for self.block in self.blocks:
                while self.block.i > i:
                    self.output.write('</td></tr><tr>')
                    if self.block.text \
                    and self.block.type_ in ('dic','wform','transc'
                                            ,'speech','phdic'
                                            ):
                        base = '<td align="center" valign="top">'
                    elif self.width and self.block.text:
                        base = '<td valign="top" style="width: {}%">'
                        base = base.format(self.width)
                    else:
                        base = '<td valign="top">'
                    self.output.write(base)
                    i = self.block.i
                    j = 0
                while self.block.j > j:
                    self.output.write('</td>')
                    mes = '<td valign="top"{}>'
                    if self.block.text \
                    and self.block.type_ in ('term','comment','user'
                                            ,'correction','phrase'
                                            ,'phcom','phcount'
                                            ) and self.width:
                        sub = ' style="width: {}%"'.format(self.width)
                    else:
                        sub = ''
                    mes = mes.format(sub)
                    self.output.write(mes)
                    j += 1
                if self.Reverse:
                    self.block.xi = self.block.j
                    self.block.xj = self.block.i
                else:
                    self.block.xi = self.block.i
                    self.block.xj = self.block.j
                self._run_dic()
                self._run_wform()
                self._run_speech()
                self._run_term()
                self._run_comment()
                self._run_user()
                self._run_correction()
            self.output.write('</td></tr></table>')
        elif self.skipped:
            self.output.write('<h1>')
            mes = _('Nothing has been found (skipped subjects: {}).')
            mes = mes.format(self.skipped)
            self.output.write(mes)
            self.output.write('</h1>')
        else:
            self.output.write('<h1>')
            self.output.write(_('Nothing has been found.'))
            self.output.write('</h1>')
        if self.Printer:
            self.output.write('</div>')
        self.output.write('</meta></body></html>')
        self.htm = self.output.getvalue()
        #TODO: Fix the algorithm and drop this workaround
        what = '<td valign="top" style="width: {}%"></td>'
        what = what.format(self.width)
        with_ = '<td valign="top"></td>'
        self.htm = self.htm.replace(what,with_)
        self.output.close()
        return self.htm



class Objects:
    
    def __init__(self):
        self.htm = None
        
    def get_htm(self):
        if self.htm is None:
            self.htm = HTM()
        return self.htm


objs = Objects()
