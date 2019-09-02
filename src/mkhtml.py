#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared as sh

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


# Shortened
class Block:

    def __init__(self):
        self._type = ''
        self._text = ''
        self.i     = 0
        self.j     = 0


class HTML:

    def __init__(self):
        self.values()
        self.priority_colors()
        self.blocked_colors()

    # 'collimit' includes fixed blocks
    def reset (self,data,cols,order
              ,collimit=9,Printer=False
              ,Reverse=False,width=0
              ,phdic='',skipped=0
              ,max_syms=30
              ):
        self.values()
        self.order     = order
        self._data     = data
        self._cols     = cols
        self._collimit = collimit
        self._width    = width
        self.Printer   = Printer
        self.Reverse   = Reverse
        self._phdic    = phdic
        self._skipped  = skipped
        ''' Maximum number of symbols in a column. If the column exceeds
            this number and 'self._width' is set - wrap the column.
            #todo: calculate font width to be more precise
        '''
        self._max_syms = max_syms
        
    def run(self):
        self.assign()
        self.html()
        return self._html
    
    def values(self):
        self._blocks  = []
        self._skipped = 0
        self._block   = None
        self._html    = ''
        self._phdic   = ''
        self._script  = '''
        <head>

          <div align="center">
            <!-- A button to print the printable area -->
            <input type="button" onclick="printDiv('printableArea')" value="%s" />
          </div>

          <script type="text/javascript">
            function printDiv(divName) {
              var printContents = document.getElementById(divName).innerHTML;
              var originalContents = document.body.innerHTML;
              document.body.innerHTML = printContents;
              window.print();
              document.body.innerHTML = originalContents;
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
        self._script = self._script % _('Print')
    
    def priority_colors(self):
        default_color = 'red'
        delta         = -76
        # Column 1 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col1']
                                  ,delta = delta
                                  )
        if result:
            self._priority_color1 = result
        else:
            self._priority_color1 = default_color
        # Column 2 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col2']
                                  ,delta = delta
                                  )
        if result:
            self._priority_color2 = result
        else:
            self._priority_color2 = default_color
        # Column 3 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col3']
                                  ,delta = delta
                                  )
        if result:
            self._priority_color3 = result
        else:
            self._priority_color3 = default_color
        # Column 4 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col4']
                                  ,delta = delta
                                  )
        if result:
            self._priority_color4 = result
        else:
            self._priority_color4 = default_color
            
    def blocked_colors(self):
        default_color = 'dim gray'
        delta         = 76
        # Column 1 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col1']
                                  ,delta = delta
                                  )
        if result:
            self._blocked_color1 = result
        else:
            self._blocked_color1 = default_color
        # Column 2 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col2']
                                  ,delta = delta
                                  )
        if result:
            self._blocked_color2 = result
        else:
            self._blocked_color2 = default_color
        # Column 3 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col3']
                                  ,delta = delta
                                  )
        if result:
            self._blocked_color3 = result
        else:
            self._blocked_color3 = default_color
        # Column 4 color
        result = sh.com.mod_color (color = sh.lg.globs['var']['color_col4']
                                  ,delta = delta
                                  )
        if result:
            self._blocked_color4 = result
        else:
            self._blocked_color4 = default_color
    
    def assign(self):
        for item in self._data:
            block       = Block()
            block._type = item[0]
            block._text = item[1]
            block.i     = item[2]
            block.j     = item[3]
            self._blocks.append(block)

    def _dic(self):
        if self._block._type == 'dic' and self._block._text:
            self.output.write('<font face="')
            self.output.write(self._family())
            self.output.write('" color="')
            # Suppress useless error output
            if self._block._text != self._phdic:
                lst         = self.order.get_list(search=self._block._text)
                Blocked     = self.order.is_blocked(lst)
                Prioritized = self.order.is_prioritized(lst)
            else:
                Blocked     = False
                Prioritized = False
            if Blocked:
                self.output.write(self._color_b())
            elif Prioritized:
                self.output.write(self._color_p())
            else:
                self.output.write(self._color())
            self.output.write('" size="')
            self.output.write(str(self._size()))
            self.output.write('"><b>')
            self.output.write(self._block._text)
            self.output.write('</b></font>')

    def _family(self):
        if self._block.xj == 0:
            return sh.lg.globs['var']['font_col1_family']
        elif self._block.xj == 1:
            return sh.lg.globs['var']['font_col2_family']
        elif self._block.xj == 2:
            return sh.lg.globs['var']['font_col3_family']
        elif self._block.xj == 3:
            return sh.lg.globs['var']['font_col4_family']
        else:
            return sh.lg.globs['var']['font_terms_family']
            
    def _size(self):
        if self._block.xj == 0:
            return sh.lg.globs['int']['font_col1_size']
        elif self._block.xj == 1:
            return sh.lg.globs['int']['font_col2_size']
        elif self._block.xj == 2:
            return sh.lg.globs['int']['font_col3_size']
        elif self._block.xj == 3:
            return sh.lg.globs['int']['font_col4_size']
        else:
            return sh.lg.globs['int']['font_terms_size']
            
    def _color_p(self):
        if self._block.xj == 0:
            return self._priority_color1
        elif self._block.xj == 1:
            return self._priority_color2
        elif self._block.xj == 2:
            return self._priority_color3
        elif self._block.xj == 3:
            return self._priority_color4
        else:
            return 'red'
            
    def _color_b(self):
        if self._block.xj == 0:
            return self._blocked_color1
        elif self._block.xj == 1:
            return self._blocked_color2
        elif self._block.xj == 2:
            return self._blocked_color3
        elif self._block.xj == 3:
            return self._blocked_color4
        else:
            return 'dim gray'
    
    def _color(self):
        if self._block.xj == 0:
            return sh.lg.globs['var']['color_col1']
        elif self._block.xj == 1:
            return sh.lg.globs['var']['color_col2']
        elif self._block.xj == 2:
            return sh.lg.globs['var']['color_col3']
        elif self._block.xj == 3:
            return sh.lg.globs['var']['color_col4']
        else:
            return sh.lg.globs['var']['color_terms']
    
    def _wform(self):
        if self._block._type == 'wform':
            self.output.write('<font face="')
            self.output.write(self._family())
            self.output.write('" color="')
            self.output.write(self._color())
            self.output.write('" size="')
            self.output.write(str(self._size()))
            self.output.write('"><b>')
            self.output.write(self._block._text)
            self.output.write('</b></font>')

    def _term(self):
        if self._block._type in ('term','phrase'):
            self.output.write('<font face="')
            self.output.write(sh.lg.globs['var']['font_terms_family'])
            self.output.write('" color="')
            self.output.write(sh.lg.globs['var']['color_terms'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_terms_size']))
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</font>')

    def _speech(self):
        if self._block._type == 'speech':
            self.output.write('<font face="')
            self.output.write(self._family())
            self.output.write('" color="')
            self.output.write(self._color())
            self.output.write('" size="')
            self.output.write(str(self._size()))
            self.output.write('">')
            self.output.write('<i>')
            if self._block.xj == 0:
                self.output.write('<b>')
                self.output.write(self._block._text)
                self.output.write('</b>')
            else:
                self.output.write(self._block._text)
            self.output.write('</i>')
            self.output.write('</font>')
    
    def _comment(self):
        if self._block._type in ('comment','transc','user','definition'):
            self.output.write('<i><font face="')
            self.output.write(sh.lg.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_comments_size']))
            self.output.write('" color="')
            self.output.write(sh.lg.globs['var']['color_comments'])
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</i></font>')

    def _correction(self):
        if self._block._type == 'correction':
            self.output.write('<i><font face="')
            self.output.write(sh.lg.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.lg.globs['int']['font_comments_size']))
            self.output.write('" color="')
            #todo (?): add to config
            self.output.write('green')
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</i></font>')

    def html(self):
        ''' Default Python string concatenation is too slow, so we use
            this module instead.
        '''
        self.output = io.StringIO()
        self.output.write('<html>\n')
        self.output.write('\t<body>\n\t\t<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        if self.Printer:
            self.output.write(self._script)
        #fix: this CSS does not work
        #self.output.write('\n\t\t<style type="text/css">\n\t\t\t.line-separator{border-top: 2px dashed #4f94cd;}\n\t\t\t.indent{padding-bottom: 5px;}\n\t\t</style>')
        if self.Printer:
            self.output.write('\n\t\t<div id="printableArea">')
        if self._blocks:
            self.output.write('\n\t\t\t<table>\n\t\t<tr>')
            if self._width and self.Reverse:
                self.output.write('<td valign="top" col width="')
                self.output.write(str(self._width))
                self.output.write('">')
            else:
                self.output.write('<td align="center" valign="top">')
            i = j = 0
            for self._block in self._blocks:
                while self._block.i > i:
                    self.output.write('</td></tr>\n\t\t<tr>')
                    cond1 = self._width and self.Reverse
                    cond2 = self._width \
                            and len(self._block._text) > self._max_syms
                    if cond1 or cond2:
                        self.output.write('<td align="center" valign="top" col width="')
                        self.output.write(str(self._width))
                        self.output.write('">')
                    else:
                        self.output.write('<td align="center" valign="top">')
                    i = self._block.i
                    j = 0
                while self._block.j > j:
                    self.output.write('</td>\n\t\t\t')
                    # -1 because we define 'td' for the next column here
                    cond1 = self._width and self._block._text
                    cond2 = self._block.j > len(self._cols) - 1 \
                            or self.Reverse
                    cond3 = self._width \
                            and len(self._block._text) > self._max_syms
                    if cond1 and cond2 or cond3:
                        self.output.write('<td valign="top" col width="')
                        self.output.write(str(self._width))
                        self.output.write('">')
                    else:
                        self.output.write('<td valign="top">')
                    j += 1
                if self.Reverse:
                    self._block.xi = self._block.j
                    self._block.xj = self._block.i
                else:
                    self._block.xi = self._block.i
                    self._block.xj = self._block.j
                self._dic()
                self._wform()
                self._speech()
                self._term()
                self._comment()
                self._correction()
            self.output.write('</td></tr>\n\t\t\t</table>\t')
        elif self._skipped:
            self.output.write('<h1>')
            mes = _('Nothing has been found (skipped dictionaries: {}).')
            mes = mes.format(self._skipped)
            self.output.write(mes)
            self.output.write('</h1>')
        else:
            self.output.write('<h1>')
            self.output.write(_('Nothing has been found.'))
            self.output.write('</h1>')
        if self.Printer:
            self.output.write('\n\t</div>')
        self.output.write('\n</body>\n</html>')
        self._html = self.output.getvalue()
        ''' #todo: enhance algorithm, drop this; I tried to monitor j,
            block._text, block.j, but they are all changing.
        '''
        self._html = self._html.replace ('<td valign="top" col width="%d"></td>' \
                                        % self._width
                                        ,'<td valign="top"></td>'
                                        )
        self.output.close()
        return self._html



class Objects:
    
    def __init__(self):
        self._html = None
        
    def html(self):
        if self._html is None:
            self._html = HTML()
        return self._html


objs = Objects()
