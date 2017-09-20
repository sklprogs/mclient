#!/usr/bin/python3

''' # todo:
'''

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

    def __init__(self,data,cols,collimit=9,Printer=False,blacklist=[]
                ,prioritize=[],blocked_color='gray',priority_color='red'
                ,width=0,Reverse=False
                ): # 'collimit' includes fixed blocks
        self._data           = data
        self._cols           = cols
        self._collimit       = collimit
        self.Printer         = Printer
        self._blacklist      = blacklist
        self._prioritize     = prioritize
        self._blocked_color  = blocked_color
        self._priority_color = priority_color
        self._width          = width
        self.Reverse         = Reverse
        self._blocks         = []
        self._block          = None
        self._html           = ''
        self._script         = '''
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
        self.html  ()

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
            self.output.write(sh.globs['var']['font_dics_family'])
            self.output.write('" color="')
            if self._block._text in self._blacklist:
                self.output.write(self._blocked_color)
            elif self._block._text in self._prioritize:
                self.output.write(self._priority_color)
            else:
                self.output.write(sh.globs['var']['color_dics'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_dics_size']))
            self.output.write('"><b>')
            self.output.write(self._block._text)
            self.output.write('</b></font>')

    def _wform(self):
        if self._block._type == 'wform':
            self.output.write('<font face="')
            self.output.write(sh.globs['var']['font_speech_family'])
            self.output.write('" color="')
            self.output.write(sh.globs['var']['color_speech'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_speech_size']))
            self.output.write('"><b>')
            self.output.write(self._block._text)
            self.output.write('</b></font>')

    def _term(self):
        if self._block._type == 'term' or self._block._type == 'phrase':
            self.output.write('<font face="')
            self.output.write(sh.globs['var']['font_terms_family'])
            self.output.write('" color="')
            self.output.write(sh.globs['var']['color_terms'])
            self.output.write('" size="')
            self.output.write(str(sh.globs['int']['font_terms_size']))
            self.output.write('">')
            self.output.write(self._block._text)
            self.output.write('</font>')

    def _comment(self):
        if self._block._type == 'comment' or self._block._type == 'speech' or self._block._type == 'transc':
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
            #self.output.write(sh.globs['var']['color_comments'])
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
        self.output.write('  <body>\n    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">')
        if self.Printer:
            self.output.write('\n    <div id="printableArea">')
        if self._blocks:
            self.output.write('\n      <table>\n    <tr>')
            if self._width and self.Reverse:
                self.output.write('<td col width="')
                self.output.write(str(self._width))
                self.output.write('">')
            else:
                self.output.write('<td>')
            i = j = 0
            for self._block in self._blocks:
                while self._block.i > i:
                    self.output.write('</td></tr>\n    <tr>')
                    if self._width and self.Reverse:
                        self.output.write('<td align="center" col width="')
                        self.output.write(str(self._width))
                        self.output.write('">')
                    else:
                        self.output.write('<td align="center">')
                    i = self._block.i
                    j = 0
                while self._block.j > j:
                    self.output.write('</td>\n      ')
                    # -1 because we define 'td' for the next column here
                    if self._width and self._block._text and (self._block.j > len(self._cols) - 1 or self.Reverse):
                        self.output.write('<td col width="')
                        self.output.write(str(self._width))
                        self.output.write('">')
                    else:
                        self.output.write('<td>')
                    j += 1
                self._dic       ()
                self._wform     ()
                self._term      ()
                self._comment   ()
                self._correction()
            self.output.write('</td></tr>\n      </table>  ')
        else:
            self.output.write('<h1>')
            self.output.write(_('Nothing has been found.'))
            self.output.write('</h1>')
        if self.Printer:
            self.output.write('\n  </div>')
        self.output.write('\n</body>\n</html>')
        self._html = self.output.getvalue()
        # todo: enhance algorithm, drop this; I tried to monitor j, block._text, block.j, but they are all changing
        self._html = self._html.replace('<td col width="%d"></td>' % self._width,'<td></td>')
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

    mc.ConfigMclient ()

    timer = sh.Timer(func_title='tags + elems + cells + pos + mkhtml')
    timer.start()

    tags = tg.Tags(page._page)
    tags.run()

    if Debug:
        tags.debug(MaxRows=40)
        input('Tags step completed. Press Enter')

    elems = el.Elems (blocks = tags._blocks
                     ,source = source
                     ,search = search
                     )
    elems.run()

    if Debug:
        elems.debug(MaxRows=40)
        input('Elems step completed. Press Enter')

    blocks_db = db.DB()
    blocks_db.fill(elems._data)

    blocks_db.request (source = source
                      ,search = search
                      )
    ph_terma = el.PhraseTerma (dbc = blocks_db.dbc
                              ,source = source
                              ,search = search
                              )
    ph_terma.run()

    phrase_dic = blocks_db.phrase_dic ()
    data       = blocks_db.assign_bp  ()

    bp = cl.BlockPrioritize (data       = data
                            ,source     = source
                            ,search     = search
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
    pos = cl.Pos(data=data)
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
        blocks_db.print(Shorten=1,MaxRows=100,MaxRow=18)
        input('Return.')

    mkhtml = HTML (data     = blocks_db.fetch()
                  ,cols     = ('dic','wform','transc','speech')
                  ,collimit = collimit
                  ,Printer  = 1
                  )

    timer.end()

    file_w = '/tmp/test.html'
    sh.WriteTextFile(file=file_w,AskRewrite=0).write(text=mkhtml._html)
    sh.Launch(target=file_w).default()

