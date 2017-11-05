#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','./locale')

import io
import shared as sh
import sharedGUI as sg


# Extended from tags.Block
class Block:
    
    def __init__(self):
        self._block    = -1
        self.i         = -1
        self.j         = -1
        self._first    = -1
        self._last     = -1
        self._no       = -1
        self._cell_no  = -1 # Applies to non-blocked cells only
        self._same     = -1
        self._priority = 0
        self._type     = 'comment' # 'wform', 'speech', 'dic', 'phrase', 'term', 'comment', 'correction', 'transc', 'invalid'
        self._text     = ''
        self._dica     = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''



# Update Block and Priority in DB before sorting cells
''' This complements DB with values that must be dumped into DB before sorting it
    Needs attributes in blocks: NO, DICA, TYPE, TEXT (test purposes only)
    Modifies attributes:        BLOCK, PRIORITY
'''
class BlockPrioritize:
    
    def __init__(self,data,blacklist=[]
                ,prioritize=[],Block=False
                ,Prioritize=False,phrase_dic=None
                ):
        self._data       = data
        self._blacklist  = blacklist
        self._prioritize = prioritize
        self.Block       = Block
        self.Prioritize  = Prioritize
        self._phrase_dic = phrase_dic
        self._blocks     = []
        self._query      = ''
        if self._data:
            self.Success = True
        else:
            self.Success = False
            sh.log.append ('BlockPrioritize.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def run(self):
        if self.Success:
            self.assign    ()
            self.block     ()
            self.prioritize()
            self.dump      ()
        else:
            sh.log.append ('BlockPrioritize.run'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
    
    def assign(self):
        for item in self._data:
            block       = Block()
            block._no   = item[0]
            block._type = item[1]
            block._text = item[2]
            block._dica = item[3]
            self._blocks.append(block)
            
    def block(self):
        for block in self._blocks:
            if self.Block and block._dica in self._blacklist:
                block._block = 1
            else:
                block._block = 0
            
    def prioritize(self):
        if self._phrase_dic:
            for block in self._blocks:
                if self._phrase_dic == block._dica:
                    # Set the (presumably) lowest priority for a 'Phrases' dictionary. This must be a quite small value as not to conflict with other dictionaries.
                    block._priority = -1000
        if self.Prioritize:
            for i in range(len(self._prioritize)):
                priority = len(self._prioritize) - i
                for block in self._blocks:
                    if self._prioritize[i].lower() == block._dica.lower():
                        block._priority = priority
                    
    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            tmp.write('update BLOCKS set BLOCK=%d,PRIORITY=%d where NO=%d;' % (block._block,block._priority,block._no))
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()

    def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
        print('\nBlockPrioritize.debug (Non-DB blocks):')
        headers = ['NO'
                  ,'DICA'
                  ,'TYPE'
                  ,'TEXT'
                  ,'BLOCK'
                  ,'PRIORITY'          
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._no
                         ,block._dica
                         ,block._type
                         ,block._text
                         ,block._block
                         ,block._priority        
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = Shorten
                 ,MaxRow  = MaxRow
                 ,MaxRows = MaxRows
                 ).print()



''' This re-assigns DIC, WFORM, SPEECH, TRANSC types
    We assume that sqlite has already sorted DB with 'BLOCK IS NOT 1'
    Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DICA, WFORMA, SPEECHA, TRANSCA
    Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO
'''
class Cells:
    
    def __init__ (self,data,cols,collimit=10
                 ,phrase_dic=None,Reverse=False
                 ): # Including fixed columns
        self._data       = data # Sqlite fetch
        self._cols       = cols
        self._collimit   = collimit
        self._phrase_dic = phrase_dic
        self.Reverse     = Reverse
        self._blocks     = []
        self._query      = ''
        if self._data:
            self.Success = True
        else:
            self.Success = False
            sh.log.append ('Cells.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    # The 'Phrases' section comes the latest in MT, therefore, it inherits fixed columns of the preceding dictionary which are irrelevant. Here we clear them.
    def clear_phrases(self):
        if self._phrase_dic:
            for block in self._blocks:
                if block._dica == self._phrase_dic:
                    if block._type in ('wform','speech','transc'):
                        block._text = ''
    
    def clear_fixed(self):
        dica = wforma = speecha = transca = ''
        for block in self._blocks:
            if block._type == 'dic':
                if dica == block._dica:
                    block._text = ''
                else:
                    dica = block._dica
            if block._type == 'wform':
                if wforma == block._wforma:
                    block._text = ''
                else:
                    wforma = block._wforma
            if block._type == 'speech':
                if speecha == block._speecha:
                    block._text = ''
                else:
                    speecha = block._speecha
            if block._type == 'transc':
                if transca == block._transca:
                    block._text = ''
                else:
                    transca = block._transca
                    
    # Reassign COLNO to start with 0 if separate words have been found (all fixed columns are empty). This allows to avoid the effect when a column with the 1st term is stretched owing to empty fixed columns.
    def sep_words(self):
        min_j = len(self._cols)
        for block in self._blocks:
            if block._text and block.j < min_j:
                min_j = block.j
        if min_j == len(self._cols):
            for i in range(len(self._blocks)):
                self._blocks[i].j -= len(self._cols)
    
    def run(self):
        if self.Success:
            self.assign       ()
            self.clear_fixed  ()
            self.clear_phrases()
            self.wrap         ()
            self.sep_words    ()
            self.sort_cells   ()
            self.cell_no      ()
            self.dump         ()
        else:
            sh.log.append ('Cells.run'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def assign(self):
        for item in self._data:
            block          = Block()
            block._no      = item[0]
            block._type    = item[1]
            block._text    = item[2]
            block._same    = item[3]
            block._dica    = item[4]
            block._wforma  = item[5]
            block._speecha = item[6]
            block._transca = item[7]
            self._blocks.append(block)
        
    def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
        print('\nCells.debug (Non-DB blocks):')
        headers = ['NO'
                  ,'TYPE'
                  ,'TEXT'
                  ,'ROWNO'
                  ,'COLNO'
                  ,'CELLNO'
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._no
                         ,block._type
                         ,block._text
                         ,block.i
                         ,block.j
                         ,block._cell_no
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = Shorten
                 ,MaxRow  = MaxRow
                 ,MaxRows = MaxRows
                 ).print()
    
    def wrap(self):
        if self.Reverse:
            self.wrap_y()
        else:
            self.wrap_x()
    
    def wrap_x(self):
        i = j = -1
        PrevFixed = False
        for x in range(len(self._blocks)):
            if self._cols and self._blocks[x]._type == self._cols[0]:
                if PrevFixed:
                    self._blocks[x].i = i
                else:
                    PrevFixed = True
                    i += 1
                    self._blocks[x].i = i
                self._blocks[x].j = 0
                j = len(self._cols) - 1
            elif len(self._cols) > 1 and self._blocks[x]._type == self._cols[1]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = 1
                j = len(self._cols) - 1
            elif len(self._cols) > 2 and self._blocks[x]._type == self._cols[2]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = 2
                j = len(self._cols) - 1
            elif len(self._cols) > 3 and self._blocks[x]._type == self._cols[3]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = j = len(self._cols) - 1
            elif self._blocks[x]._same > 0: # Must be before checking '_collimit'
                PrevFixed = False
                self._blocks[x].i = i
                self._blocks[x].j = j
            elif j + 1 == self._collimit:
                PrevFixed = False
                i += 1
                self._blocks[x].i = i
                self._blocks[x].j = j = len(self._cols) # Instead of creating empty non-selectable cells
            else:
                PrevFixed = False
                self._blocks[x].i = i
                if x > 0:
                    j += 1
                    if j < len(self._cols):
                        j = len(self._cols) + 1
                    self._blocks[x].j = j
                else:
                    self._blocks[x].j = len(self._cols)
                    j += 1
                    
    # Create a vertically reversed view. This generally differs from 'wrap' in that we do not use 'collimit'.
    def wrap_y(self):
        i = j = 0
        for x in range(len(self._blocks)):
            if self._cols and self._blocks[x]._type == self._cols[0] and self._blocks[x]._text:
                if x > 0:
                    j += 1
                self._blocks[x].j = j
                self._blocks[x].i = 0
                i = 1
            elif self._blocks[x]._same > 0:
                self._blocks[x].i = i
                self._blocks[x].j = j
            elif self._blocks[x]._text:
                self._blocks[x].j = j
                i += 1
                self._blocks[x].i = i
    
    # This is necessary because fixed columns are interchangeable now
    def sort_cells(self):
        self._blocks = sorted(self._blocks,key=lambda block:(block.i,block.j,block._no))
    
    def cell_no(self):
        no = 0
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                self._blocks[i]._cell_no = no
            elif i > 0: # i != no
                no += 1
                self._blocks[i]._cell_no = no
            else:
                self._blocks[i]._cell_no = no
        
    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            # We do not want to mess around with screening quotes that can fail the query
            if block._text:
                tmp.write('update BLOCKS set ROWNO=%d,COLNO=%d,CELLNO=%d where NO=%d;' % (block.i,block.j,block._cell_no,block._no))
            else:
                tmp.write('update BLOCKS set TEXT="%s",ROWNO=%d,COLNO=%d,CELLNO=%d where NO=%d;' % (block._text,block.i,block.j,block._cell_no,block._no))
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()
        return self._query
        
# This is view-specific and should be recreated each time
''' We assume that sqlite has already sorted DB with 'BLOCK IS NOT 1' and all cell manipulations are completed
    Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
    Modifies attributes:        POS1, POS2
'''
class Pos:
    
    def __init__(self,data,raw_text):
        self._data     = data     # Sqlite fetch
        self._raw_text = raw_text # Retrieved from the TkinterHTML widget
        self._blocks   = []
        self._query    = ''
        if self._data and self._raw_text:
            self.Success = True
        else:
            self.Success = False
            sh.log.append ('Pos.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def run(self):
        if self.Success:
            self.assign   ()
            self.gen_poses()
            self.dump     ()
        else:
            sh.log.append ('Pos.run'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        
    def assign(self):
        for item in self._data:
            block       = Block()
            block._no   = item[0]
            block._type = item[1]
            block._text = item[2]
            block._same = item[3]
            block.i     = item[4]
            self._blocks.append(block)
        
    def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
        print('\nPos.debug (Non-DB blocks):')
        headers = ['NO'
                  ,'TYPE'
                  ,'TEXT'
                  ,'POS1'
                  ,'POS2'
                  ]
        rows = []
        for block in self._blocks:
            rows.append ([block._no
                         ,block._type
                         ,block._text
                         ,block._first
                         ,block._last
                         ]
                        )
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = Shorten
                 ,MaxRow  = MaxRow
                 ,MaxRows = MaxRows
                 ).print()
    
    ''' We generate positions here according to the text produced by 
        TkinterHtml's 'widget.text()' command.
        Peculiarities of the retrieved text:
        - TkinterHtml adds some empty lines from the top and the bottom;
          the number of these lines varies each time (and we don't know
          the rule according to which they are generated)
        - Each cell occupies a single line
        - Blocks within a cell are spaced with a single space (except
          for the blocks having such text as '(')
        - Each line is stripped
        - Pos2 of the previous cell and pos1 of the next cell are
          sometimes equal; this corresponds to the position system
          used by Tkinter
        - Duplicate spaces are removed
    '''
    def gen_poses(self):
        last = 0
        for block in self._blocks:
            text = sh.Text(text=block._text.strip()).delete_duplicate_spaces()
            if text:
                search   = sh.Search(text=self._raw_text,search=text)
                search.i = last
                result   = sh.Input (val        = search.next()
                                    ,func_title = 'Pos.gen_poses'
                                    ).integer()
                if result >= last:
                    block._first = result
                else:
                    sg.Message ('Pos.gen_poses'
                               ,_('ERROR')
                               ,_('Unable to find "%s"!') % str(text)
                               )
                    block._first = last
            else:
                block._first = last
            block._last = block._first + len(text)
            last        = block._last
            
    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            tmp.write('update BLOCKS set POS1=%d,POS2=%d where NO=%d;' % (block._first,block._last,block._no))
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()
        return self._query



''' Creating a selection requires 4 parameters to be calculated:
"self.widget.tag('add','selection',node1,pos1,node2,pos2)"
'node1' usually equals to 'node2' (for a single block this is 
always true because it represents a single tag and therefore 
lies within a single node).
The current node can be calculated using:
"node1,node2 = self.widget.node(True,event.x,event.y)"
The main catch here is that the remaining pos1 and pos2 
are not equal for some reason to positions calculated
for the text generated by 'widget.text()' (_index[1], 
_index[3]). Therefore, we need an additional 'index' 
command.
'''
class Pages:
    
    def __init__(self,obj,blocks):
        self.obj     = obj
        self._blocks = blocks
        self._query  = ''
        if self._blocks and self.obj and hasattr(self.obj,'widget') and hasattr(self.obj,'bbox'):
            self.Success = True
            self.widget = self.obj.widget
        else:
            self.Success = False
            sh.log.append ('Pages.__init__'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        
    def create_index(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            _index = self.widget.text('index',block._first,block._last)
            if _index:
                _bbox  = self.obj.bbox(_index[0])
                if _bbox:
                    # BBOX: man says: The first two integers are the x and y coordinates of the top-left corner of the bounding-box, the later two are the x and y coordinates of the bottom-right corner of the same box. If the node does not generate content, then an empty string is returned.
                    tmp.write('update BLOCKS set NODE1="%s",NODE2="%s",OFFPOS1=%d,OFFPOS2=%d,BBOX1=%d,BBOX2=%d,BBOY1=%d,BBOY2=%d where NO=%d;' % (_index[0],_index[2],_index[1],_index[3],_bbox[0],_bbox[2],_bbox[1],_bbox[3],block._no))
                else:
                    sh.log.append ('Pages.create_index'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Pages.create_index'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()
        return self._query
            
    def debug(self):
        sg.Message ('Pages.debug'
                   ,_('INFO')
                   ,self._query.replace(';',';\n')
                   )
    
    def run(self):
        if self.Success:
            self.create_index()
        else:
            sh.log.append ('Pages.run'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



if __name__ == '__main__':
    import db
    import page    as pg
    import tags    as tg
    import elems   as el
    import mclient as mc
    
    # Modifiable
    source     = _('Online')
    search     = 'working documentation'
    url        = ''
    file       = '/home/pete/tmp/ars/working documentation.txt'
    blacklist  = []
    prioritize = ['Общая лексика']
    collimit   = 10
    file_raw   = '/home/pete/tmp/ars/working documentation - extracted text'
    articleid  = 1
    
    raw_text = sh.ReadTextFile(file=file_raw).get()
    
    timer = sh.Timer(func_title='page, tags, elems, ph_terma, cells')
    timer.start()
    
    mc.ConfigMclient ()
    
    page = pg.Page (source       = source
                   ,lang         = 'English'
                   ,search       = search
                   ,url          = url
                   ,win_encoding = 'windows-1251'
                   ,ext_dics     = []
                   ,file         = file)
    page.run()
    
    tags = tg.Tags (source = source
                   ,text   = page._page
                   )
    tags.run()
    
    elems = el.Elems (blocks    = tags._blocks
                     ,articleid = articleid
                     )
    elems.run()
    
    blocks_db = db.DB()
    blocks_db.fill_blocks(elems._data)
    
    data = (None   # (00) ARTICLEID
           ,source # (01) SOURCE
           ,search # (02) TITLE
           ,url    # (03) URL
           ,''     # (04) BOOKMARK
           )
    blocks_db.fill_articles(data=data)
    
    blocks_db._articleid = articleid
    
    ph_terma = el.PhraseTerma (dbc       = blocks_db.dbc
                              ,articleid = articleid
                              )
    ph_terma.run()
    
    data       = blocks_db.assign_bp()
    phrase_dic = blocks_db.phrase_dic ()
    
    bp = BlockPrioritize (data       = data
                         ,blacklist  = blacklist
                         ,prioritize = prioritize
                         ,phrase_dic = phrase_dic
                         )
    bp.run()
    blocks_db.update(query=bp._query)
    
    data = blocks_db.assign_cells()
    cells = Cells (data     = data
                  ,cols     = ('dic','wform','transc','speech')
                  ,collimit = collimit
                  )
    cells.run()
    blocks_db.update(query=cells._query)
    
    data = blocks_db.assign_pos()
    pos  = Pos (data     = data
               ,raw_text = raw_text
               )
    pos.run()
    blocks_db.update(query=pos._query)
    
    timer.end()
    
    blocks_db.print(Shorten=0,mode='ARTICLES')
    print()
    
    blocks_db.dbc.execute('select NO,DICA,TYPE,TEXT,SAMECELL,PRIORITY,CELLNO,POS1,POS2,SELECTABLE from BLOCKS order by CELLNO,NO')
    blocks_db.print(Selected=1,Shorten=1,MaxRows=200,MaxRow=18)
