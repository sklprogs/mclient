#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

#todo: share
abbr     = ['гл.','сущ.','прил.','нареч.','сокр.','предл.','мест.']
expanded = ['Глагол','Существительное','Прилагательное','Наречие'
           ,'Сокращение','Предлог','Местоимение'
           ]


# Extended from tags.Block
class Block:
    
    def __init__(self):
        self._block    = -1
        self.i         = -1
        self.j         = -1
        self._first    = -1
        self._last     = -1
        self._no       = -1
        # Applies to non-blocked cells only
        self._cell_no  = -1
        self._same     = -1
        self._priority = 0
        ''' 'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'user', 'transc', 'invalid'
        '''
        self._type     = 'comment'
        self._text     = ''
        self._dica     = ''
        self._wforma   = ''
        self._speecha  = ''
        self._transca  = ''



class BlockPrioritize:
    ''' Update Block and Priority in DB before sorting cells.
        This complements DB with values that must be dumped into DB
        before sorting it.
        Needs attributes in blocks: NO, DICA, TYPE, TEXT (test purposes
        only).
        Modifies attributes:        BLOCK, PRIORITY
    '''
    def __init__(self,data,order,Block=False
                ,Prioritize=False,phrase_dic=None
                ,Debug=False,Shorten=True
                ,MaxRow=20,MaxRows=50
                ):
        f = '[MClient] cells.BlockPrioritize.__init__'
        self._blocks     = []
        self._query      = ''
        self.order       = order
        self._phrase_dic = phrase_dic
        self._data       = data
        self.Block       = Block
        self.Prioritize  = Prioritize
        self.Debug       = Debug
        self.Shorten     = Shorten
        self.MaxRow      = MaxRow
        self.MaxRows     = MaxRows
        if self._data:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
    
    def run(self):
        f = '[MClient] cells.BlockPrioritize.run'
        if self.Success:
            self.assign()
            self.block()
            self.prioritize()
            self.dump()
            self.debug()
        else:
            sh.com.cancel(f)
    
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
            # Suppress useless error output
            if block._dica and block._dica != self._phrase_dic:
                lst     = self.order.get_list(search=block._dica)
                Blocked = self.order.is_blocked(lst)
            else:
                Blocked = False
            if self.Block and Blocked:
                block._block = 1
            else:
                block._block = 0
            
    def prioritize(self):
        f = '[MClient] cells.BlockPrioritize.prioritize'
        if self.order.Success:
            for block in self._blocks:
                if block._dica:
                    if self._phrase_dic == block._dica:
                        ''' - This value should be set irrespectively of
                              'self.Prioritize'.
                            - Set the (presumably) lowest priority for
                              a 'Phrases' dictionary. This must be
                              a quite small value as not to conflict
                              with other dictionaries.
                        '''
                        block._priority = -1000
                    elif self.Prioritize:
                        block._priority = self.order.priority(search=block._dica)
        else:
            sh.com.cancel(f)

    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            tmp.write ('update BLOCKS set BLOCK=%d,PRIORITY=%d \
                        where NO=%d;' % (block._block,block._priority
                                        ,block._no
                                        )
                      )
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()

    def debug(self):
        f = '[MClient] cells.BlockPrioritize.debug'
        if self.Debug:
            sh.log.append (f,_('INFO')
                          ,_('Debug table:')
                          )
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
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()



class Cells:
    ''' This re-assigns DIC, WFORM, SPEECH, TRANSC types.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1'.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DICA,
                                    WFORMA, SPEECHA, TRANSCA
        Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO
        #note: collimit at input: fixed columns are included
    '''
    def __init__ (self,data,cols,collimit=10
                 ,phrase_dic=None,Reverse=False
                 ,ExpandSpeech=False,Debug=False
                 ,Shorten=True,MaxRow=20,MaxRows=50
                 ):
        f = '[MClient] cells.Cells.__init__'
        # Sqlite fetch
        self._data        = data
        self._cols        = cols
        self._collimit    = collimit
        self._phrase_dic  = phrase_dic
        self.Reverse      = Reverse
        self.ExpandSpeech = ExpandSpeech
        self.Debug        = Debug
        self.Shorten      = Shorten
        self.MaxRow       = MaxRow
        self.MaxRows      = MaxRows
        self._blocks      = []
        if self._data:
            self.Success  = True
        else:
            self.Success  = False
            sh.com.empty(f)
        
    def clear_phrases(self):
        ''' The 'Phrases' section comes the latest in MT, therefore,
            it inherits fixed columns of the preceding dictionary which
            are irrelevant. Here we clear them.
        '''
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

    def sep_words(self):
        ''' Reassign COLNO to start with 0 if separate words have been
            found (all fixed columns are empty). This allows to avoid
            the effect when a column with the 1st term is stretched
            owing to empty fixed columns.
        '''
        min_j = len(self._cols)
        for block in self._blocks:
            if block._text and block.j < min_j:
                min_j = block.j
        if min_j == len(self._cols):
            for block in self._blocks:
                block.j -= len(self._cols)
    
    def run(self):
        f = '[MClient] cells.Cells.run'
        if self.Success:
            self.assign()
            self.restore_fixed()
            self.clear_fixed()
            self.clear_phrases()
            self.expand_speech()
            self.phrases2end()
            self.wrap()
            self.sep_words()
            self.sort_cells()
            self.cell_no()
            self.debug()
        else:
            sh.com.cancel(f)
        
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
        
    def debug(self):
        f = '[MClient] cells.Cells.debug'
        if self.Debug:
            sh.log.append (f,_('INFO')
                          ,_('Debug table:')
                          )
            headers = ['NO'
                      ,'TYPE'
                      ,'TEXT'
                      ,'ROWNO'
                      ,'COLNO'
                      ,'CELLNO'
                      ,'SAME'
                      ]
            rows = []
            for block in self._blocks:
                rows.append ([block._no
                             ,block._type
                             ,block._text
                             ,block.i
                             ,block.j
                             ,block._cell_no
                             ,block._same
                             ]
                            )
            sh.Table (headers = headers
                     ,rows    = rows
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
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
            elif len(self._cols) > 1 \
            and self._blocks[x]._type == self._cols[1]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = 1
                j = len(self._cols) - 1
            elif len(self._cols) > 2 \
            and self._blocks[x]._type == self._cols[2]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = 2
                j = len(self._cols) - 1
            elif len(self._cols) > 3 \
            and self._blocks[x]._type == self._cols[3]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self._blocks[x].i = i
                self._blocks[x].j = j = len(self._cols) - 1
            # Must be before checking '_collimit'
            elif self._blocks[x]._same > 0:
                PrevFixed = False
                # This can happen if there are no fixed columns
                if i < 0:
                    i = 0
                if j < len(self._cols):
                    j = len(self._cols)
                self._blocks[x].i = i
                self._blocks[x].j = j
            elif j + 1 == self._collimit:
                PrevFixed = False
                i += 1
                self._blocks[x].i = i
                # Instead of creating empty non-selectable cells
                self._blocks[x].j = j = len(self._cols)
            else:
                PrevFixed = False
                # This can happen if there are no fixed columns
                if i < 0:
                    i = 0
                self._blocks[x].i = i
                if x > 0:
                    j += 1
                    if j < len(self._cols):
                        j = len(self._cols) + 1
                    self._blocks[x].j = j
                else:
                    self._blocks[x].j = len(self._cols)
                    j += 1
                    
    def wrap_y(self):
        ''' Create a vertically reversed view. This generally differs
            from 'wrap' in that we do not use 'collimit'.
        '''
        i = j = 0
        for x in range(len(self._blocks)):
            if self._cols and self._blocks[x]._type == self._cols[0] \
            and self._blocks[x]._text:
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
        self._blocks = sorted (self._blocks
                              ,key=lambda block:(block.i
                                                ,block.j
                                                ,block._no
                                                )
                              )
    
    def phrases2end(self):
        f = '[MClient] cells.Cells.phrases2end'
        if self._phrase_dic:
            phrases = [block for block in self._blocks \
                       if block._dica == self._phrase_dic
                      ]
            self._blocks = [block for block in self._blocks \
                            if block._dica != self._phrase_dic
                           ]
            self._blocks = self._blocks + phrases
        else:
            sh.com.empty(f)
    
    def cell_no(self):
        no = 0
        for i in range(len(self._blocks)):
            if self._blocks[i]._same > 0:
                self._blocks[i]._cell_no = no
            # i != no
            elif i > 0:
                no += 1
                self._blocks[i]._cell_no = no
            else:
                self._blocks[i]._cell_no = no
        
    def dump(self,blocks_db):
        ''' Do not use 'executescript' to update TEXT field. SQLITE may
            recognize a keyword (e.g., 'block') and replace it with '0'.
            Takes ~0,08s for 'block', ~0,13s for 'set' on AMD E-300.
        '''
        for block in self._blocks:
            blocks_db.dbc.execute ('update BLOCKS \
                                    set    TEXT=?,ROWNO=?,COLNO=?\
                                          ,CELLNO=?\
                                    where  NO=?',(block._text,block.i
                                                 ,block.j,block._cell_no
                                                 ,block._no
                                                 )
                                  )
        
    # Takes ~0,0077s on 'set'
    def expand_speech(self):
        if self.ExpandSpeech:
            for i in range(len(self._blocks)):
                if self._blocks[i]._type == 'speech':
                    lst = self._blocks[i]._text.split(' ')
                    for j in range(len(lst)):
                        if lst[j] in abbr:
                            ind    = abbr.index(lst[j])
                            lst[j] = expanded[ind]
                    self._blocks[i]._text = ' '.join(lst)
        # In case of switching back from the 'Cut to the chase' mode
        else:
            for i in range(len(self._blocks)):
                if self._blocks[i]._type == 'speech':
                    lst = self._blocks[i]._text.split(' ')
                    for j in range(len(lst)):
                        if lst[j] in expanded:
                            ind    = expanded.index(lst[j])
                            lst[j] = abbr[ind]
                    self._blocks[i]._text = ' '.join(lst)
    
    def restore_fixed(self):
        for block in self._blocks:
            if block._type == 'dic':
                block._text = block._dica
            elif block._type == 'wform':
                block._text = block._wforma
            elif block._type == 'speech':
                block._text = block._speecha
            elif block._type == 'transc':
                block._text = block._transca



class Pos:
    ''' This is view-specific and should be recreated each time.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1' and all cell manipulations are completed.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
        Modifies attributes:        POS1, POS2
    '''
    def __init__ (self,data,raw_text
                 ,Debug=False,Shorten=True
                 ,MaxRow=70,MaxRows=50
                 ):
        f = '[MClient] cells.Pos.__init__'
        self._blocks   = []
        self._query    = ''
        # Sqlite fetch
        self._data     = data
        # Retrieved from the TkinterHTML widget
        self._raw_text = raw_text
        self.Debug     = Debug
        self.Shorten   = Shorten
        self.MaxRow    = MaxRow
        self.MaxRows   = MaxRows
        if self._data and self._raw_text:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
        
    def run(self):
        f = '[MClient] cells.Pos.run'
        if self.Success:
            self.assign()
            self.gen_poses()
            self.dump()
            self.debug()
        else:
            sh.com.cancel(f)
        
    def assign(self):
        for item in self._data:
            block       = Block()
            block._no   = item[0]
            block._type = item[1]
            block._text = item[2]
            block._same = item[3]
            block.i     = item[4]
            self._blocks.append(block)
        
    def debug(self):
        f = '[MClient] cells.Pos.debug'
        if self.Debug:
            sh.log.append (f,_('INFO')
                          ,_('Debug table:')
                          )
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
                     ,Shorten = self.Shorten
                     ,MaxRow  = self.MaxRow
                     ,MaxRows = self.MaxRows
                     ).print()
    
    def gen_poses(self):
        ''' We generate positions here according to the text produced by 
            TkinterHtml's 'widget.text()' command.
            Peculiarities of the retrieved text:
            - TkinterHtml adds some empty lines from the top and
              the bottom;
            - The number of these lines varies each time (and we don't
              know the rule according to which they are generated)
            - Each cell occupies a single line
            - Blocks within a cell are spaced with a single space
              (except for the blocks having such text as '(')
            - Each line is stripped
            - Pos2 of the previous cell and pos1 of the next cell are
              sometimes equal; this corresponds to the position system
              used by Tkinter
            - Duplicate spaces are removed
        '''
        f = '[MClient] cells.Pos.gen_poses'
        last      = 0
        not_found = []
        for block in self._blocks:
            text = sh.Text(text=block._text.strip()).delete_duplicate_spaces()
            if text:
                search = sh.Search (text   = self._raw_text
                                   ,search = text
                                   )
                search.i = last
                result = sh.Input (title = f
                                  ,value = search.next()
                                  ).integer()
                if result >= last:
                    block._first = result
                else:
                    block._first = last
                    not_found.append(text)
            else:
                block._first = last
            block._last = block._first + len(text)
            last        = block._last
        if not_found:
            not_found = ['"' + item + '"' for item in not_found]
            not_found = '\n' + '\n'.join(not_found)
            sh.objs.mes (f,_('ERROR')
                        ,_('Unable to find: %s') % not_found
                        )
            
    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            tmp.write ('update BLOCKS set POS1=%d,POS2=%d where NO=%d;'\
                      % (block._first,block._last,block._no)
                      )
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()
        return self._query



class Pages:
    ''' Creating a selection requires 4 parameters to be calculated:
        "self.widget.tag('add','selection',node1,pos1,node2,pos2)"
        'node1' usually equals to 'node2' (for a single block this is
        always true because it represents a single tag and therefore 
        lies within a single node).
        The current node can be calculated using:
        "node1,node2 = self.widget.node(True,event.x,event.y)"
        The main catch here is that the remaining pos1 and pos2 are not
        equal for some reason to positions calculated for the text
        generated by 'widget.text()' (_index[1], _index[3]). Therefore,
        we need an additional 'index' command.
    '''
    def __init__ (self,obj,blocks
                 ,Debug=False
                 ):
        f = '[MClient] cells.Pages.__init__'
        self._query  = ''
        self.obj     = obj
        self._blocks = blocks
        self.Debug   = Debug
        if self._blocks and self.obj and hasattr(self.obj,'widget') \
        and hasattr(self.obj,'bbox'):
            self.Success = True
            self.widget = self.obj.widget
        else:
            self.Success = False
            sh.com.empty(f)
        
    def create_index(self):
        f = '[MClient] cells.Pages.create_index'
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self._blocks:
            _index = self.widget.text('index',block._first,block._last)
            if _index:
                _bbox  = self.obj.bbox(_index[0])
                if _bbox:
                    ''' BBOX: man says: The first two integers are the x
                        and y coordinates of the top-left corner of
                        the bounding-box, the later two are the x and y
                        coordinates of the bottom-right corner of
                        the same box. If the node does not generate
                        content, then an empty string is returned.
                    '''
                    tmp.write ('update BLOCKS \
                                set NODE1="%s",NODE2="%s",OFFPOS1=%d\
                                   ,OFFPOS2=%d,BBOX1=%d,BBOX2=%d\
                                   ,BBOY1=%d,BBOY2=%d where NO=%d;' \
                               % (_index[0],_index[2],_index[1]
                                 ,_index[3],_bbox[0],_bbox[2],_bbox[1]
                                 ,_bbox[3],block._no
                                 )
                              )
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        tmp.write('commit;')
        self._query = tmp.getvalue()
        tmp.close()
        return self._query
            
    def debug(self):
        f = '[MClient] cells.Pages.debug'
        if self.Debug:
            sh.objs.mes (f,_('INFO')
                        ,self._query.replace(';',';\n')
                        )
    
    def run(self):
        f = '[MClient] cells.Pages.run'
        if self.Success:
            self.create_index()
            self.debug()
        else:
            sh.com.cancel(f)
