#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared as sh
from skl_shared.localize import _

#TODO: share
abbr     = ['гл.','сущ.','прил.','нареч.','сокр.','предл.','мест.']
expanded = ['Глагол','Существительное','Прилагательное','Наречие'
           ,'Сокращение','Предлог','Местоимение'
           ]


# Extended from tags.Block
class Block:
    
    def __init__(self):
        self.block = -1
        self.i     = -1
        self.j     = -1
        self.first = -1
        self.last  = -1
        self.no    = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.same   = -1
        self.priority = 0
        ''' Block types:
            'wform', 'speech', 'dic', 'phrase', 'term', 'comment',
            'correction', 'user', 'definition', 'transc', 'invalid'
        '''
        self.type_   = 'comment'
        self.text    = ''
        self.dica    = ''
        self.wforma  = ''
        self.speecha = ''
        self.transca = ''



class BlockPrioritize:
    ''' Update Block and Priority in DB before sorting cells.
        This complements DB with values that must be dumped into DB
        before sorting it.
        Needs attributes in blocks: NO, DICA, TYPE, TEXT (test purposes
        only).
        Modifies attributes:        BLOCK, PRIORITY
    '''
    def __init__(self,data,order,Block=False
                ,Prioritize=False,phdic=None
                ,Debug=False,maxrow=20
                ,maxrows=50
                ):
        f = '[MClient] cells.BlockPrioritize.__init__'
        self.blocks     = []
        self.query      = ''
        self.order      = order
        self.phdic      = phdic
        self.data       = data
        self.Block      = Block
        self.Prioritize = Prioritize
        self.Debug      = Debug
        self.maxrow     = maxrow
        self.maxrows    = maxrows
        if self.data:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
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
        for item in self.data:
            block       = Block()
            block.no    = item[0]
            block.type_ = item[1]
            block.text  = item[2]
            block.dica  = item[3]
            self.blocks.append(block)
            
    def block(self):
        for block in self.blocks:
            # Suppress useless error output
            if block.dica and block.dica != self.phdic:
                lst     = self.order.get_list(search=block.dica)
                Blocked = self.order.is_blocked(lst)
            else:
                Blocked = False
            if self.Block and Blocked:
                block.block = 1
            else:
                block.block = 0
            
    def prioritize(self):
        f = '[MClient] cells.BlockPrioritize.prioritize'
        if self.order.Success:
            for block in self.blocks:
                if block.dica:
                    if self.phdic == block.dica:
                        ''' - This value should be set irrespectively of
                              'self.Prioritize'.
                            - Set the (presumably) lowest priority for
                              a 'Phrases' dictionary. This must be
                              quite a small value as not to conflict
                              with other dictionaries.
                        '''
                        block.priority = -1000
                    elif self.Prioritize:
                        block.priority = self.order.get_priority(search=block.dica)
        else:
            sh.com.cancel(f)

    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self.blocks:
            tmp.write ('update BLOCKS set BLOCK=%d,PRIORITY=%d \
                        where NO=%d;' % (block.block,block.priority
                                        ,block.no
                                        )
                      )
        tmp.write('commit;')
        self.query = tmp.getvalue()
        tmp.close()

    def debug(self):
        f = '[MClient] cells.BlockPrioritize.debug'
        if self.Debug:
            headers = ('NO','DICA','TYPE','TEXT','BLOCK','PRIORITY')
            rows = []
            for block in self.blocks:
                rows.append ([block.no
                             ,block.dica
                             ,block.type_
                             ,block.text
                             ,block.block
                             ,block.priority        
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = self.maxrow
                               ,maxrows   = self.maxrows
                               ,Transpose = True
                               ).run()
            mes = f + '\n\n' + mes
            sh.com.run_fast_debug(mes)



class Cells:
    ''' This re-assigns DIC, WFORM, SPEECH, TRANSC types.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1'.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DICA,
                                    WFORMA, SPEECHA, TRANSCA
        Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO
        #NOTE: collimit at input: fixed columns are included
    '''
    def __init__ (self,data,cols,collimit=10
                 ,phdic=None,Reverse=False
                 ,ExpandSp=False,Debug=False
                 ,maxrow=20,maxrows=50
                 ):
        f = '[MClient] cells.Cells.__init__'
        # Sqlite fetch
        self.data     = data
        self.cols     = cols
        self.collimit = collimit
        self.phdic    = phdic
        self.Reverse  = Reverse
        self.ExpandSp = ExpandSp
        self.Debug    = Debug
        self.maxrow   = maxrow
        self.maxrows  = maxrows
        self.blocks   = []
        if self.data:
            self.Success  = True
        else:
            self.Success  = False
            sh.com.rep_empty(f)
        
    def clear_phrases(self):
        ''' The 'Phrases' section comes the latest in MT, therefore,
            it inherits fixed columns of the preceding dictionary which
            are irrelevant. Here we clear them.
        '''
        if self.phdic:
            for block in self.blocks:
                if block.dica == self.phdic:
                    if block.type_ in ('wform','speech','transc'):
                        block.text = ''

    def clear_fixed(self):
        dica = wforma = speecha = transca = ''
        for block in self.blocks:
            if block.type_ == 'dic':
                if dica == block.dica:
                    block.text = ''
                else:
                    dica = block.dica
            if block.type_ == 'wform':
                if wforma == block.wforma:
                    block.text = ''
                else:
                    wforma = block.wforma
            if block.type_ == 'speech':
                if speecha == block.speecha:
                    block.text = ''
                else:
                    speecha = block.speecha
            if block.type_ == 'transc':
                if transca == block.transca:
                    block.text = ''
                else:
                    transca = block.transca

    def run_sep_words(self):
        ''' Reassign COLNO to start with 0 if separate words have been
            found (all fixed columns are empty). This allows to avoid
            the effect when a column with the 1st term is stretched
            owing to empty fixed columns.
        '''
        min_j = len(self.cols)
        for block in self.blocks:
            if block.text and block.j < min_j:
                min_j = block.j
        if min_j == len(self.cols):
            for block in self.blocks:
                block.j -= len(self.cols)
    
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
            self.run_sep_words()
            self.sort_cells()
            self.set_cellno()
            self.debug()
        else:
            sh.com.cancel(f)
        
    def assign(self):
        for item in self.data:
            block         = Block()
            block.no      = item[0]
            block.type_   = item[1]
            block.text    = item[2]
            block.same    = item[3]
            block.dica    = item[4]
            block.wforma  = item[5]
            block.speecha = item[6]
            block.transca = item[7]
            self.blocks.append(block)
        
    def debug(self):
        f = '[MClient] cells.Cells.debug'
        if self.Debug:
            headers = ('NO','TYPE','TEXT','ROWNO','COLNO','CELLNO'
                      ,'SAME'
                      )
            rows = []
            for block in self.blocks:
                rows.append ([block.no
                             ,block.type_
                             ,block.text
                             ,block.i
                             ,block.j
                             ,block.cellno
                             ,block.same
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = self.maxrow
                               ,maxrows   = self.maxrows
                               ,Transpose = True
                               ).run()
            mes = f + '\n\n' + mes
            sh.com.run_fast_debug(mes)
    
    def wrap(self):
        if self.Reverse:
            self.wrap_y()
        else:
            self.wrap_x()
    
    def wrap_x(self):
        i = j = -1
        PrevFixed = False
        for x in range(len(self.blocks)):
            if self.cols and self.blocks[x].type_ == self.cols[0]:
                if PrevFixed:
                    self.blocks[x].i = i
                else:
                    PrevFixed = True
                    i += 1
                    self.blocks[x].i = i
                self.blocks[x].j = 0
                j = len(self.cols) - 1
            elif len(self.cols) > 1 \
            and self.blocks[x].type_ == self.cols[1]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self.blocks[x].i = i
                self.blocks[x].j = 1
                j = len(self.cols) - 1
            elif len(self.cols) > 2 \
            and self.blocks[x].type_ == self.cols[2]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self.blocks[x].i = i
                self.blocks[x].j = 2
                j = len(self.cols) - 1
            elif len(self.cols) > 3 \
            and self.blocks[x].type_ == self.cols[3]:
                if not PrevFixed:
                    PrevFixed = True
                    i += 1
                self.blocks[x].i = i
                self.blocks[x].j = j = len(self.cols) - 1
            elif self.blocks[x].type_ == 'definition':
                try:
                    j = self.cols.index('wform')
                except ValueError:
                    j = len(self.cols)
                self.blocks[x].i = i
                self.blocks[x].j = j
            # Must be before checking '_collimit'
            elif self.blocks[x].same > 0:
                PrevFixed = False
                # This can happen if there are no fixed columns
                if i < 0:
                    i = 0
                if j < len(self.cols):
                    j = len(self.cols)
                self.blocks[x].i = i
                self.blocks[x].j = j
            elif j + 1 == self.collimit:
                PrevFixed = False
                i += 1
                self.blocks[x].i = i
                # Instead of creating empty non-selectable cells
                self.blocks[x].j = j = len(self.cols)
            else:
                PrevFixed = False
                # This can happen if there are no fixed columns
                if i < 0:
                    i = 0
                self.blocks[x].i = i
                if x > 0:
                    j += 1
                    if j < len(self.cols):
                        j = len(self.cols) + 1
                    self.blocks[x].j = j
                else:
                    self.blocks[x].j = len(self.cols)
                    j += 1
                    
    def wrap_y(self):
        ''' Create a vertically reversed view. This generally differs
            from 'wrap' in that we do not use 'collimit'.
        '''
        i = j = 0
        for x in range(len(self.blocks)):
            if self.cols and self.blocks[x].type_ == self.cols[0] \
            and self.blocks[x].text:
                if x > 0:
                    j += 1
                self.blocks[x].j = j
                self.blocks[x].i = 0
                i = 1
            elif self.blocks[x].same > 0:
                self.blocks[x].i = i
                self.blocks[x].j = j
            elif self.blocks[x].text:
                self.blocks[x].j = j
                i += 1
                self.blocks[x].i = i
    
    # This is necessary because fixed columns are interchangeable now
    def sort_cells(self):
        self.blocks = sorted (self.blocks
                              ,key=lambda block:(block.i
                                                ,block.j
                                                ,block.no
                                                )
                              )
    
    def phrases2end(self):
        f = '[MClient] cells.Cells.phrases2end'
        if self.phdic:
            phrases = [block for block in self.blocks \
                       if block.dica == self.phdic
                      ]
            self.blocks = [block for block in self.blocks \
                            if block.dica != self.phdic
                           ]
            self.blocks = self.blocks + phrases
        else:
            sh.com.rep_empty(f)
    
    def set_cellno(self):
        no = 0
        for i in range(len(self.blocks)):
            if self.blocks[i].same > 0:
                self.blocks[i].cellno = no
            # i != no
            elif i > 0:
                no += 1
                self.blocks[i].cellno = no
            else:
                self.blocks[i].cellno = no
        
    def dump(self,blocksdb):
        ''' Do not use 'executescript' to update TEXT field. SQLITE may
            recognize a keyword (e.g., 'block') and replace it with '0'.
            Takes ~0,08s for 'block', ~0,13s for 'set' on AMD E-300.
        '''
        for block in self.blocks:
            blocksdb.dbc.execute ('update BLOCKS \
                                   set    TEXT=?,ROWNO=?,COLNO=?\
                                         ,CELLNO=?\
                                   where  NO=?',(block.text,block.i
                                                ,block.j,block.cellno
                                                ,block.no
                                                )
                                 )
        
    # Takes ~0,0077s on 'set'
    def expand_speech(self):
        if self.ExpandSp:
            for i in range(len(self.blocks)):
                if self.blocks[i].type_ == 'speech':
                    lst = self.blocks[i].text.split(' ')
                    for j in range(len(lst)):
                        if lst[j] in abbr:
                            ind    = abbr.index(lst[j])
                            lst[j] = expanded[ind]
                    self.blocks[i].text = ' '.join(lst)
        # In case of switching back from the 'Cut to the chase' mode
        else:
            for i in range(len(self.blocks)):
                if self.blocks[i].type_ == 'speech':
                    lst = self.blocks[i].text.split(' ')
                    for j in range(len(lst)):
                        if lst[j] in expanded:
                            ind    = expanded.index(lst[j])
                            lst[j] = abbr[ind]
                    self.blocks[i].text = ' '.join(lst)
    
    def restore_fixed(self):
        for block in self.blocks:
            if block.type_ == 'dic':
                block.text = block.dica
            elif block.type_ == 'wform':
                block.text = block.wforma
            elif block.type_ == 'speech':
                block.text = block.speecha
            elif block.type_ == 'transc':
                block.text = block.transca



class Pos:
    ''' This is view-specific and should be recreated each time.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1' and all cell manipulations are completed.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
        Modifies attributes:        POS1, POS2
    '''
    def __init__ (self,data,raw_text
                 ,Debug=False,maxrow=70
                 ,maxrows=50
                 ):
        f = '[MClient] cells.Pos.__init__'
        self.blocks = []
        self.query  = ''
        # Sqlite fetch
        self.data = data
        # Retrieved from the TkinterHTM widget
        self.rawtext = raw_text
        self.Debug   = Debug
        self.maxrow  = maxrow
        self.maxrows = maxrows
        if self.data and self.rawtext:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
        
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
        for item in self.data:
            block       = Block()
            block.no    = item[0]
            block.type_ = item[1]
            block.text  = item[2]
            block.same  = item[3]
            block.i     = item[4]
            self.blocks.append(block)
        
    def debug(self):
        f = '[MClient] cells.Pos.debug'
        if self.Debug:
            headers = ('NO','TYPE','TEXT','POS1','POS2')
            rows = []
            for block in self.blocks:
                rows.append ([block.no
                             ,block.type_
                             ,block.text
                             ,block.first
                             ,block.last
                             ]
                            )
            mes = sh.FastTable (headers   = headers
                               ,iterable  = rows
                               ,maxrow    = self.maxrow
                               ,maxrows   = self.maxrows
                               ,Transpose = True
                               ).run()
            mes = f + '\n\n' + mes
            sh.com.run_fast_debug(mes)
    
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
        last = 0
        not_found = []
        for block in self.blocks:
            text = sh.Text(text=block.text.strip()).delete_duplicate_spaces()
            if text:
                search = sh.Search (text    = self.rawtext
                                   ,pattern = text
                                   )
                search.i = last
                result = sh.Input(f,search.get_next()).get_integer()
                if result >= last:
                    block.first = result
                else:
                    block.first = last
                    not_found.append(text)
            else:
                block.first = last
            block.last = block.first + len(text)
            last = block.last
        if not_found:
            not_found = ['"' + item + '"' for item in not_found]
            not_found = '\n' + '\n'.join(not_found)
            mes = _('Unable to find: {}').format(not_found)
            sh.objs.get_mes(f,mes).show_error()
            
    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self.blocks:
            tmp.write ('update BLOCKS set POS1=%d,POS2=%d where NO=%d;'\
                      % (block.first,block.last,block.no)
                      )
        tmp.write('commit;')
        self.query = tmp.getvalue()
        tmp.close()
        return self.query



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
        self.query  = ''
        self.obj    = obj
        self.blocks = blocks
        self.Debug  = Debug
        if self.blocks and self.obj and hasattr(self.obj,'widget') \
        and hasattr(self.obj,'bbox'):
            self.Success = True
            self.widget = self.obj.widget
        else:
            self.Success = False
            sh.com.rep_empty(f)
        
    def create_index(self):
        f = '[MClient] cells.Pages.create_index'
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self.blocks:
            index_ = self.widget.text('index',block.first,block.last)
            if index_:
                bbox = self.obj.bbox(index_[0])
                if bbox:
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
                               % (index_[0],index_[2],index_[1]
                                 ,index_[3],bbox[0],bbox[2],bbox[1]
                                 ,bbox[3],block.no
                                 )
                              )
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        tmp.write('commit;')
        self.query = tmp.getvalue()
        tmp.close()
        return self.query
            
    def debug(self):
        f = '[MClient] cells.Pages.debug'
        if self.Debug:
            mes = self.query.replace(';',';\n')
            sh.objs.get_mes(f,mes).show_debug()
    
    def run(self):
        f = '[MClient] cells.Pages.run'
        if self.Success:
            self.create_index()
            self.debug()
        else:
            sh.com.cancel(f)
