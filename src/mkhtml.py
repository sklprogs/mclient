#!/usr/bin/python3

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','./locale')

import io
import shared as sh
import sharedGUI as sg


# Shortened
class Block:

    def __init__(self):
        self._type = ''
        self._text = ''
        self.i     = 0
        self.j     = 0


class HTML:

    def __init__(self,data,cols,collimit=9
                ,Printer=False,blacklist=[]
                ,prioritize=[],width=0
                ,Reverse=False
                ): # 'collimit' includes fixed blocks
        self._data            = data
        self._cols            = cols
        self._collimit        = collimit
        self.Printer          = Printer
        self._blacklist       = blacklist
        self._prioritize      = prioritize
        self._width           = width
        self.Reverse          = Reverse
        self._blocks          = []
        self._block           = None
        self._html            = ''
        self._script          = '''
        <head>

          <div align="center">
            <!-- A button to print the printable area -->
            <input type="button" onclick="printDiv('printableArea')" value="Print" />
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
        self.assign()
        self.priority_colors()
        self.blocked_colors()
        self.html()

    def priority_colors(self):
        default_color = 'red'
        delta         = -76
        # Column 1 color
        result = sg.mod_color (color = sh.globs['var']['color_col1']
                              ,delta = delta
                              )
        if result:
            self._priority_color1 = result
        else:
            self._priority_color1 = default_color
        # Column 2 color
        result = sg.mod_color (color = sh.globs['var']['color_col2']
                              ,delta = delta
                              )
        if result:
            self._priority_color2 = result
        else:
            self._priority_color2 = default_color
        # Column 3 color
        result = sg.mod_color (color = sh.globs['var']['color_col3']
                              ,delta = delta
                              )
        if result:
            self._priority_color3 = result
        else:
            self._priority_color3 = default_color
        # Column 4 color
        result = sg.mod_color (color = sh.globs['var']['color_col4']
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
        result = sg.mod_color (color = sh.globs['var']['color_col1']
                              ,delta = delta
                              )
        if result:
            self._blocked_color1 = result
        else:
            self._blocked_color1 = default_color
        # Column 2 color
        result = sg.mod_color (color = sh.globs['var']['color_col2']
                              ,delta = delta
                              )
        if result:
            self._blocked_color2 = result
        else:
            self._blocked_color2 = default_color
        # Column 3 color
        result = sg.mod_color (color = sh.globs['var']['color_col3']
                              ,delta = delta
                              )
        if result:
            self._blocked_color3 = result
        else:
            self._blocked_color3 = default_color
        # Column 4 color
        result = sg.mod_color (color = sh.globs['var']['color_col4']
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
        if self._block._type == 'dic':
            self.output.write('<font face="')
            self.output.write(self._family())
            self.output.write('" color="')
            if self._block._text in self._blacklist:
                self.output.write(self._color_b())
            elif self._block._text in self._prioritize:
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
            return sh.globs['var']['font_col1_family']
        elif self._block.xj == 1:
            return sh.globs['var']['font_col2_family']
        elif self._block.xj == 2:
            return sh.globs['var']['font_col3_family']
        elif self._block.xj == 3:
            return sh.globs['var']['font_col4_family']
        else:
            return sh.globs['var']['font_terms_family']
            
    def _size(self):
        if self._block.xj == 0:
            return sh.globs['int']['font_col1_size']
        elif self._block.xj == 1:
            return sh.globs['int']['font_col2_size']
        elif self._block.xj == 2:
            return sh.globs['int']['font_col3_size']
        elif self._block.xj == 3:
            return sh.globs['int']['font_col4_size']
        else:
            return sh.globs['int']['font_terms_size']
            
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
            return sh.globs['var']['color_col1']
        elif self._block.xj == 1:
            return sh.globs['var']['color_col2']
        elif self._block.xj == 2:
            return sh.globs['var']['color_col3']
        elif self._block.xj == 3:
            return sh.globs['var']['color_col4']
        else:
            return sh.globs['var']['color_terms']
    
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
            self.output.write(sh.globs['var']['font_terms_family'])
            self.output.write('" color="')
            self.output.write(sh.globs['var']['color_terms'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_terms_size']))
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
        if self._block._type in ('comment','transc'):
            self.output.write('<i><font face="')
            self.output.write(sh.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_comments_size']))
            self.output.write('" color="')
            self.output.write(sh.globs['var']['color_comments'])
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</i></font>')

    def _correction(self):
        if self._block._type == 'correction':
            self.output.write('<i><font face="')
            self.output.write(sh.globs['var']['font_comments_family'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_comments_size']))
            self.output.write('" color="')
            # todo (?): add to config
            self.output.write('green')
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</i></font>')

    def html(self):
        # Default Python string concatenation is too slow, so we use this module instead
        self.output = io.StringIO()
        self.output.write('<html>\n')
        if self.Printer:
            self.output.write(self._script)
        self.output.write('\t<body>\n\t\t<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        # todo: this CSS does not work
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
                    if self._width and self.Reverse:
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
                    if self._width and self._block._text and (self._block.j > len(self._cols) - 1 or self.Reverse):
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
                self._dic       ()
                self._wform     ()
                self._speech    ()
                self._term      ()
                self._comment   ()
                self._correction()
            self.output.write('</td></tr>\n\t\t\t</table>\t')
        else:
            self.output.write('<h1>')
            self.output.write(_('Nothing has been found.'))
            self.output.write('</h1>')
        if self.Printer:
            self.output.write('\n\t</div>')
        self.output.write('\n</body>\n</html>')
        self._html = self.output.getvalue()
        # todo: enhance algorithm, drop this; I tried to monitor j, block._text, block.j, but they are all changing
        self._html = self._html.replace('<td valign="top" col width="%d"></td>' % self._width,'<td valign="top"></td>')
        self.output.close()



if __name__ == '__main__':
    import page    as pg
    import tags    as tg
    import db
    import elems   as el
    import cells   as cl
    import mclient as mc


    #'/home/pete/tmp/ars/star_test'
    #'/home/pete/tmp/ars/sampling.txt'
    #'/home/pete/tmp/ars/filter_get'
    #'/home/pete/tmp/ars/добро пожаловать.txt'
    #'/home/pete/tmp/ars/добро.txt'
    #'/home/pete/tmp/ars/рабочая документация.txt'
    #'/home/pete/tmp/ars/martyr.txt'
    #'/home/pete/tmp/ars/preceding.txt'

    # Modifiable
    source     = _('Offline')
    search     = 'preceding'
    file       = '/home/pete/tmp/ars/preceding.txt'
    collimit   = 7
    #blacklist = ['Христианство']
    blacklist  = []
    prioritize = ['Общая лексика']
    Debug      = 0
    articleid  = 1
    url        = ''

    timer = sh.Timer(func_title='page, elems')
    timer.start()

    page = pg.Page (source       = source
                   ,lang         = 'English'
                   ,search       = search
                   ,url          = ''
                   ,win_encoding = 'windows-1251'
                   ,ext_dics     = []
                   ,file         = file
                   )
    page.run()

    mc.ConfigMclient()

    timer = sh.Timer(func_title='tags + elems + cells + pos + mkhtml')
    timer.start()

    tags = tg.Tags(page._page)
    tags.run()

    if Debug:
        tags.debug(MaxRows=40)
        input('Tags step completed. Press Enter')

    elems = el.Elems (blocks    = tags._blocks
                     ,articleid = articleid
                     )
    elems.run()

    if Debug:
        elems.debug(MaxRows=40)
        input('Elems step completed. Press Enter')

    blocks_db = db.DB()
    
    data = (None   # (00) ARTICLEID
           ,source # (01) SOURCE
           ,search # (02) TITLE
           ,url    # (03) URL
           ,''     # (04) BOOKMARK
           )
    blocks_db.fill_articles(data=data)
    blocks_db._articleid = blocks_db.max_articleid()
    
    blocks_db.fill_blocks(elems._data)
    
    ph_terma = el.PhraseTerma (dbc       = blocks_db.dbc
                              ,articleid = articleid
                              )
    ph_terma.run()

    phrase_dic = blocks_db.phrase_dic ()
    data       = blocks_db.assign_bp  ()

    bp = cl.BlockPrioritize (data       = data
                            ,blacklist  = blacklist
                            ,prioritize = prioritize
                            ,phrase_dic = phrase_dic
                            )
    bp.run()

    if Debug:
        bp.debug(MaxRows=40)
        input('BlockPrioritize step completed. Press Enter')
        sg.Message ('BlockPrioritize'
                   ,_('INFO')
                   ,bp._query.replace(';',';\n')
                   )

    blocks_db.update(query=bp._query)

    data  = blocks_db.assign_cells()
    cells = cl.Cells (data       = data
                     ,cols       = ('dic','wform','transc','speech')
                     ,collimit   = collimit
                     ,phrase_dic = phrase_dic
                     )
    cells.run()

    if Debug:
        cells.debug(MaxRows=40)
        input('Cells step completed. Press Enter')
        sg.Message ('Cells'
                   ,_('INFO')
                   ,cells._query.replace(';',';\n')
                   )

    blocks_db.update(query=cells._query)

    data = blocks_db.assign_pos()
    pos = cl.Pos(data=data,raw_text='')
    pos.run()
    if Debug:
        pos.debug(MaxRows=40)
        input('Pos step completed. Press Enter')
        sg.Message ('Pos'
                   ,_('INFO')
                   ,pos._query.replace(';',';\n')
                   )

    blocks_db.update(query=pos._query)

    if Debug:
        blocks_db.dbc.execute('select CELLNO,ROWNO,COLNO,TYPE,TEXT from BLOCKS where BLOCK=0 and IGNORE=0 order by CELLNO,NO')
        blocks_db.print(Selected=1,Shorten=1,MaxRows=200,MaxRow=18)
        input('Blocks')

    mkhtml = HTML (data     = blocks_db.fetch()
                  ,cols     = ('dic','wform','transc','speech')
                  ,collimit = collimit
                  ,Printer  = 1
                  )

    timer.end()

    file_w = '/tmp/test.html'
    sh.WriteTextFile(file=file_w,AskRewrite=0).write(text=mkhtml._html)
    sh.Launch(target=file_w).default()

