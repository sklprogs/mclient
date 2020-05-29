#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared as sh
from skl_shared.localize import _


# Shortened
class Block:

    def __init__(self):
        self.type_ = ''
        self.text  = ''
        self.i     = 0
        self.j     = 0


class HTM:

    def __init__(self):
        self.set_values()
        self.set_priority_colors()
        self.set_blocked_colors()

    def fix(self):
        ''' It is a common case when an opening bracket, a phrase and 
            a closing bracket are 3 separate blocks. Tkinter (unlike
            popular web browsers) wraps these blocks after ')'.
            We just fix this behavior.
        '''
        self.htm = self.htm.replace('<i><font face="Mono" size="3" color="gray"> (</i></font><i><font face="Mono" size="3" color="gray">','<i><font face="Mono" size="3" color="gray"> (')
    
    # 'collimit' includes fixed blocks
    def reset (self,data,cols,order
              ,collimit=9,Printer=False
              ,Reverse=False,width=0
              ,phdic='',skipped=0
              ,max_syms=30
              ):
        self.set_values()
        self.order = order
        self.data = data
        self.cols = cols
        self.collimit = collimit
        self.width = width
        self.Printer = Printer
        self.Reverse = Reverse
        self.phdic = phdic
        self.skipped = skipped
        ''' Maximum number of symbols in a column. If the column exceeds
            this number and 'self.width' is set - wrap the column.
            #TODO: calculate font width to be more precise
        '''
        self.maxsyms = max_syms
        
    def run(self):
        self.assign()
        self.gen_htm()
        self.fix()
        return self.htm
    
    def set_values(self):
        self.blocks = []
        self.skipped = 0
        self.block = None
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
    
    def set_priority_colors(self):
        default_color = 'red'
        delta         = -76
        # Column 1 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col1']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color1 = result
        else:
            self.priority_color1 = default_color
        # Column 2 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col2']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color2 = result
        else:
            self.priority_color2 = default_color
        # Column 3 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col3']
                                      ,delta = delta
                                      )
        if result:
            self.priority_color3 = result
        else:
            self.priority_color3 = default_color
        # Column 4 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col4']
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
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col1']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color1 = result
        else:
            self.blocked_color1 = default_color
        # Column 2 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col2']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color2 = result
        else:
            self.blocked_color2 = default_color
        # Column 3 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col3']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color3 = result
        else:
            self.blocked_color3 = default_color
        # Column 4 color
        result = sh.com.get_mod_color (color = sh.lg.globs['var']['color_col4']
                                      ,delta = delta
                                      )
        if result:
            self.blocked_color4 = result
        else:
            self.blocked_color4 = default_color
    
    def assign(self):
        for item in self.data:
            block       = Block()
            block.type_ = item[0]
            block.text  = item[1]
            block.i     = item[2]
            block.j     = item[3]
            self.blocks.append(block)

    def _run_dic(self):
        if self.block.type_ == 'dic' and self.block.text:
            self.output.write('<font face="')
            self.output.write(self._get_family())
            self.output.write('" color="')
            # Suppress useless error output
            if self.block.text != self.phdic:
                lst         = self.order.get_list(search=self.block.text)
                Blocked     = self.order.is_blocked(lst)
                Prioritized = self.order.is_prioritized(lst)
            else:
                Blocked     = False
                Prioritized = False
            if Blocked:
                self.output.write(self._get_color_b())
            elif Prioritized:
                self.output.write(self._get_color_p())
            else:
                self.output.write(self._get_color())
            self.output.write('" size="')
            self.output.write(str(self._get_size()))
            self.output.write('"><b>')
            self.output.write(self.block.text)
            self.output.write('</b></font>')

    def _get_family(self):
        if self.block.xj == 0:
            return sh.lg.globs['var']['font_col1_family']
        elif self.block.xj == 1:
            return sh.lg.globs['var']['font_col2_family']
        elif self.block.xj == 2:
            return sh.lg.globs['var']['font_col3_family']
        elif self.block.xj == 3:
            return sh.lg.globs['var']['font_col4_family']
        else:
            return sh.lg.globs['var']['font_terms_family']
            
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
            return sh.lg.globs['var']['color_col1']
        elif self.block.xj == 1:
            return sh.lg.globs['var']['color_col2']
        elif self.block.xj == 2:
            return sh.lg.globs['var']['color_col3']
        elif self.block.xj == 3:
            return sh.lg.globs['var']['color_col4']
        else:
            return sh.lg.globs['var']['color_terms']
    
    def _run_wform(self):
        if self.block.type_ == 'wform':
            self.output.write('<font face="')
            self.output.write(self._get_family())
            self.output.write('" color="')
            self.output.write(self._get_color())
            self.output.write('" size="')
            self.output.write(str(self._get_size()))
            self.output.write('"><b>')
            self.output.write(self.block.text)
            self.output.write('</b></font>')

    def _run_term(self):
        if self.block.type_ in ('term','phrase'):
            self.output.write('<font face="')
            self.output.write(sh.lg.globs['var']['font_terms_family'])
            self.output.write('" color="')
            self.output.write(sh.lg.globs['var']['color_terms'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_terms_size']))
            self.output.write('">')
            self.output.write(self.block.text)
            self.output.write('</font>')

    def _run_speech(self):
        if self.block.type_ == 'speech':
            self.output.write('<font face="')
            self.output.write(self._get_family())
            self.output.write('" color="')
            self.output.write(self._get_color())
            self.output.write('" size="')
            self.output.write(str(self._get_size()))
            self.output.write('">')
            self.output.write('<i>')
            if self.block.xj == 0:
                self.output.write('<b>')
                self.output.write(self.block.text)
                self.output.write('</b>')
            else:
                self.output.write(self.block.text)
            self.output.write('</i>')
            self.output.write('</font>')
    
    def _run_comment(self):
        if self.block.type_ in ('comment','transc','user','definition'):
            self.output.write('<i><font face="')
            self.output.write(sh.lg.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_comments_size']))
            self.output.write('" color="')
            self.output.write(sh.lg.globs['var']['color_comments'])
            self.output.write('">')
            self.output.write(self.block.text)
            self.output.write('</i></font>')

    def _run_correction(self):
        if self.block.type_ == 'correction':
            self.output.write('<i><font face="')
            self.output.write(sh.lg.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_comments_size']))
            self.output.write('" color="')
            #TODO (?): add to config
            self.output.write('green')
            self.output.write('">')
            self.output.write(self.block.text)
            self.output.write('</i></font>')

    def gen_htm(self):
        ''' Default Python string concatenation is too slow, so we use
            this module instead.
        '''
        self.output = io.StringIO()
        self.output.write('<html>\n')
        self.output.write('\t<body>\n\t\t<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        if self.Printer:
            self.output.write(self.script)
        #FIX: this CSS does not work
        #self.output.write('\n\t\t<style type="text/css">\n\t\t\t.line-separator{border-top: 2px dashed #4f94cd;}\n\t\t\t.indent{padding-bottom: 5px;}\n\t\t</style>')
        if self.Printer:
            self.output.write('\n\t\t<div id="printableArea">')
        if self.blocks:
            self.output.write('\n\t\t\t<table>\n\t\t<tr>')
            if self.width and self.Reverse:
                self.output.write('<td valign="top" col width="')
                self.output.write(str(self.width))
                self.output.write('">')
            elif self.blocks and self.blocks[0].text \
            and self.blocks[0].type_ in ('dic','wform','transc'
                                        ,'speech'
                                        ):
                self.output.write('<td align="center" valign="top">')
            else:
                self.output.write('<td valign="top">')
            i = j = 0
            for self.block in self.blocks:
                while self.block.i > i:
                    self.output.write('</td></tr>\n\t\t<tr>')
                    cond1 = self.width and self.Reverse
                    cond2 = self.width \
                            and len(self.block.text) > self.maxsyms
                    if self.block.text and self.block.type_ in \
                    ('dic','wform','transc','speech'):
                        base = '<td align="center" valign="top"'
                    else:
                        base = '<td valign="top"'
                    if cond1 or cond2:
                        self.output.write(base+' col width="')
                        self.output.write(str(self.width))
                        self.output.write('">')
                    else:
                        self.output.write(base+'>')
                    i = self.block.i
                    j = 0
                while self.block.j > j:
                    self.output.write('</td>\n\t\t\t')
                    # -1 because we define 'td' for the next column here
                    cond1 = self.width and self.block.text
                    cond2 = self.block.j > len(self.cols) - 1 \
                            or self.Reverse
                    cond3 = self.width \
                            and len(self.block.text) > self.maxsyms
                    if cond1 and cond2 or cond3:
                        self.output.write('<td valign="top" col width="')
                        self.output.write(str(self.width))
                        self.output.write('">')
                    else:
                        self.output.write('<td valign="top">')
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
                self._run_correction()
            self.output.write('</td></tr>\n\t\t\t</table>\t')
        elif self.skipped:
            self.output.write('<h1>')
            mes = _('Nothing has been found (skipped dictionaries: {}).')
            mes = mes.format(self.skipped)
            self.output.write(mes)
            self.output.write('</h1>')
        else:
            self.output.write('<h1>')
            self.output.write(_('Nothing has been found.'))
            self.output.write('</h1>')
        if self.Printer:
            self.output.write('\n\t</div>')
        self.output.write('\n</body>\n</html>')
        self.htm = self.output.getvalue()
        ''' #TODO: enhance algorithm, drop this; I tried to monitor j,
            block.text, block.j, but they are all changing.
        '''
        self.htm = self.htm.replace ('<td valign="top" col width="%d"></td>' \
                                    % self.width
                                    ,'<td valign="top"></td>'
                                    )
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
