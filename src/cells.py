#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
from skl_shared.localize import _
import skl_shared.shared as sh
import subjects.subjects as sj


# Extended from tags.Block
class Block:
    
    def __init__(self):
        self.block = -1
        # Applies to non-blocked cells only
        self.cellno = -1
        self.dic = ''
        self.dprior = 0
        self.first = -1
        self.Fixed = False
        self.i = -1
        self.j = -1
        self.last = -1
        self.no = -1
        self.same = -1
        self.speech = ''
        self.sprior = -1
        self.text = ''
        self.transc = ''
        ''' 'comment','correction','dic','phcount','phcom','phdic'
           ,'phrase','speech','term','transc','user','wform'
        '''
        self.type_ = 'comment'
        self.wform = ''



class BlockPrioritize:
    ''' Update Block and Priority in DB before sorting cells.
        This complements DB with values that must be dumped into DB
        before sorting it.
        Needs attributes in blocks: NO, DIC, SPEECH*, TYPE, TEXT*
        * (test purposes only).
        Modifies attributes: BLOCK, DICPR, SPEECHPR
    '''
    def __init__(self,data,Block=False,Prioritize=False
                ,phdic=None,Debug=False,maxrows=1000
                ,spdic={}
                ):
        f = '[MClient] cells.BlockPrioritize.__init__'
        self.query = ''
        self.blocks = []
        self.Block = Block
        self.data = data
        self.Debug = Debug
        self.maxrows = maxrows
        self.phdic = phdic
        self.Prioritize = Prioritize
        self.spdic = spdic
        if self.data:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def _debug_blocks(self):
        f = '[MClient] cells.BlockPrioritize._debug_blocks'
        headers = ('NO','TYPE','TEXT','BLOCK','DIC','DICPR','SPEECH'
                  ,'SPEECHPR'
                  )
        rows = []
        for block in self.blocks:
            rows.append ([block.no,block.type_,block.text,block.block
                         ,block.dic,block.dprior,block.speech
                         ,block.sprior
                         ]
                        )
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = 20
                               ,maxrows = self.maxrows
                               ,Transpose = True
                               ).run()
        return f + ':\n' + mes
    
    def prioritize_speech(self):
        f = '[MClient] cells.BlockPrioritize.prioritize_speech'
        # Takes ~0.0038s for 'set' on AMD E-300
        if self.Success:
            ''' It is assumed that we have already reset
                'logic.SpeechPrior' with the required speech order
                before.
            '''
            unknown_prior = []
            if self.spdic:
                for block in self.blocks:
                    sprior = self.spdic.get(block.speech)
                    if sprior:
                        block.sprior = sprior
                    elif not block.speech in unknown_prior:
                        mes = _('A priority of the part of speech "{}" is not defined!')
                        mes = mes.format(block.speech)
                        sh.objs.get_mes(f,mes,True).show_warning()
                        unknown_prior.append(block.speech)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run(self):
        f = '[MClient] cells.BlockPrioritize.run'
        if self.Success:
            self.assign()
            self.block()
            self.prioritize_dics()
            self.prioritize_speech()
            self.dump()
            self.debug()
        else:
            sh.com.cancel(f)
    
    def assign(self):
        for item in self.data:
            block = Block()
            block.no = item[0]
            block.type_ = item[1]
            block.text = item[2]
            block.dic = item[3]
            block.speech = item[4]
            self.blocks.append(block)
            
    def block(self):
        f = '[MClient] cells.BlockPrioritize.block'
        for block in self.blocks:
            Blocked = sj.objs.get_article().is_blocked(block.dic)
            ''' Do not put checking 'self.Block' ahead of the loop
                since we need to assign 'block' to 0 anyway.
            '''
            if self.Block and Blocked:
                block.block = 1
            else:
                block.block = 0
            
    def prioritize_dics(self):
        f = '[MClient] cells.BlockPrioritize.prioritize_dics'
        for block in self.blocks:
            if block.dic:
                if self.phdic == block.dic:
                    ''' - This value should be set irrespectively of
                          'self.Prioritize'.
                        - Set the (presumably) lowest priority for
                          a 'Phrases' subject. This must be
                          quite a small value as not to conflict
                          with other subjects.
                    '''
                    block.dprior = -1000
                elif self.Prioritize:
                    block.dprior = sj.objs.get_article().get_priority(block.dic)

    def dump(self):
        tmp = io.StringIO()
        tmp.write('begin;')
        for block in self.blocks:
            tmp.write ('update BLOCKS set BLOCK=%d,DICPR=%d,SPEECHPR=%d\
                        where NO=%d;' % (block.block,block.dprior
                                        ,block.sprior,block.no
                                        )
                      )
        tmp.write('commit;')
        self.query = tmp.getvalue()
        tmp.close()

    def debug(self):
        f = '[MClient] cells.BlockPrioritize.debug'
        if self.Debug:
            mes = [self._debug_blocks()]
            mes = '\n\n'.join(mes)
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.rep_lazy(f)



class Cells:
    ''' This re-assigns DIC, WFORM, SPEECH, TRANSC types.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1'.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DIC,
                                    WFORM, SPEECH, SPEECHPR, TRANSC
        Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO
        #NOTE: collimit at input: fixed columns are included
    '''
    def __init__ (self,data,cols,collimit=10
                 ,phdic=None,Reverse=False
                 ,spdic={},Debug=False
                 ,maxrows=1000
                 ):
        f = '[MClient] cells.Cells.__init__'
        # Sqlite fetch
        self.blocks = []
        self.unsupsp = []
        self.cols = cols
        self.collimit = collimit
        self.data = data
        self.Debug = Debug
        self.maxrows = maxrows
        self.phdic = phdic
        self.Reverse = Reverse
        self.spdic = spdic
        if self.data:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)

    def set_cols(self):
        ''' #TODO (?): change lg.objs.request.cols and
            lg.objs.request.collimit directly.
        '''
        f = '[MClient] cells.Cells.set_cols'
        fixed = set(block.type_ for block in self.blocks if block.Fixed)
        old_len = len(self.cols)
        self.cols = [col for col in self.cols if col in fixed]
        delta = old_len - len(self.cols)
        if delta > 0:
            if self.collimit > delta:
                self.collimit -= delta
            else:
                pass
        mes = _('Types of actual fixed columns: {}')
        mes = mes.format(', '.join(self.cols))
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Actual column limit: {}').format(self.collimit)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_fixed(self):
        for block in self.blocks:
            #TODO: either add new fixed types here or import a variable
            if block.type_ in ('dic','wform','speech','transc'):
                block.Fixed = True

    def clear_phrases(self):
        ''' The 'Phrases' section comes the latest in MT, therefore,
            it inherits fixed columns of the preceding subject which
            are irrelevant. Here we clear them.
        '''
        if self.phdic:
            for block in self.blocks:
                if block.dic == self.phdic:
                    if block.type_ in ('wform','speech','transc'):
                        block.text = ''

    def clear_fixed(self):
        dic = wform = speech = transc = ''
        for block in self.blocks:
            ''' 'phdic' is reassigned to 'dic' in this module (in order
                to be independent from modes).
            '''
            if block.type_ == 'dic':
                if dic == block.dic:
                    block.text = ''
                else:
                    dic = block.dic
            elif block.type_ == 'wform':
                if wform == block.wform:
                    block.text = ''
                else:
                    wform = block.wform
            elif block.type_ == 'speech':
                if speech == block.speech:
                    block.text = ''
                else:
                    speech = block.speech
            elif block.type_ == 'transc':
                if transc == block.transc:
                    block.text = ''
                else:
                    transc = block.transc

    def run(self):
        f = '[MClient] cells.Cells.run'
        if self.Success:
            self.assign()
            self.restore_fixed()
            self.clear_fixed()
            self.set_fixed()
            self.set_cols()
            self.clear_phrases()
            self.expand_speech()
            self.wrap()
            self.sort_cells()
            self.set_cellno()
            self.debug()
        else:
            sh.com.cancel(f)
        
    def assign(self):
        for item in self.data:
            block = Block()
            block.no = item[0]
            block.type_ = item[1]
            block.text = item[2]
            block.same = item[3]
            block.dic = item[4]
            block.wform = item[5]
            block.speech = item[6]
            block.sprior = item[7]
            block.transc = item[8]
            self.blocks.append(block)
        
    def debug(self):
        f = '[MClient] cells.Cells.debug'
        if self.Debug:
            headers = ('NO','TYPE','FIXED','TEXT','DIC','WFORM','SPEECH'
                      ,'SPEECHPR','ROWNO','COLNO','CELLNO','SAME'
                      )
            rows = []
            for block in self.blocks:
                rows.append ([block.no
                             ,block.type_
                             ,block.Fixed
                             ,block.text
                             ,block.dic
                             ,block.wform
                             ,block.speech
                             ,block.sprior
                             ,block.i
                             ,block.j
                             ,block.cellno
                             ,block.same
                             ]
                            )
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = 15
                               ,maxrows = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
    
    def wrap(self):
        if self.Reverse:
            self.wrap_y()
        else:
            self.wrap_x()
    
    def get_fixed_index(self,type_):
        f = '[MClient] cells.Cells.get_fixed_index'
        try:
            return self.cols.index(type_)
        except ValueError:
            ''' #TODO: Remove the warning about a missing 'dic' type
                (which was 'phdic' before).
            '''
            mes = _('Wrong input data: "{}"!').format(type_)
            sh.objs.get_mes(f,mes,True).show_warning()
        return 0
    
    def wrap_x(self):
        f = '[MClient] cells.Cells.wrap_x'
        i = j = -1
        fixed_num = len(self.cols)
        for block in self.blocks:
            if not block.same:
                if block.Fixed:
                    j = self.get_fixed_index(block.type_)
                    if j == 0:
                        i += 1
                elif j < fixed_num:
                    j = fixed_num
                else:
                    j += 1
                    if j == self.collimit:
                        j = fixed_num
                        i += 1
            block.i = i
            block.j = j
    
    def wrap_y(self):
        ''' Create a vertically reversed view. This differs from
            'wrap_x' in that we do not use 'collimit', so we cannot
            just transpose row numbers to column numbers and vice versa.
        '''
        dic = ''
        i = j = oldi = 0
        for x in range(len(self.blocks)):
            if self.cols and dic != self.blocks[x].dic:
                dic = self.blocks[x].dic
                if x > 0:
                    j += 1
                self.blocks[x].j = j
                self.blocks[x].i = oldi = 0
                i = 1
            elif self.blocks[x].same > 0:
                self.blocks[x].i = oldi = i
                self.blocks[x].j = j
            else:
                self.blocks[x].j = j
                if oldi == i:
                    i += 1
                self.blocks[x].i = oldi = i
    
    def sort_cells(self):
        # This is necessary since fixed columns are interchangeable now
        self.blocks = sorted (self.blocks
                             ,key = lambda block:(block.i
                                                 ,block.j
                                                 ,block.no
                                                 )
                             )
    
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
        query = 'update BLOCKS set TEXT = ?,ROWNO = ?,COLNO = ? \
                       ,CELLNO = ? where NO = ?'
        for block in self.blocks:
            blocksdb.dbc.execute (query,(block.text,block.i,block.j
                                        ,block.cellno,block.no
                                        )
                                 )
        
    def expand_speech(self):
        # Takes ~0.002s on 'set'
        f = '[MClient] cells.Cells.expand_speech'
        if self.spdic:
            for block in self.blocks:
                if block.type_ == 'speech' and block.text:
                    result = self.spdic.get(block.text)
                    if result:
                        block.text = result
                    elif not block.text in self.unsupsp:
                        self.unsupsp.append(block.text)
                        mes = _('An unsupported part of speech: "{}"!')
                        mes = mes.format(block.text)
                        sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_lazy(f)
    
    def restore_fixed(self):
        for block in self.blocks:
            if block.type_ in ('dic','phdic'):
                block.text = block.dic
                ''' Since this module is mode-independent, 'phdic' type
                    is optional and cannot be treated as a fixed type.
                '''
                block.type_ = 'dic'
            elif block.type_ == 'wform':
                block.text = block.wform
            elif block.type_ == 'speech':
                block.text = block.speech
            elif block.type_ == 'transc':
                block.text = block.transc



class Pos:
    ''' This is view-specific and should be recreated each time.
        We assume that sqlite has already sorted DB with
        'BLOCK IS NOT 1' and all cell manipulations are completed.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
        Modifies attributes:        POS1, POS2
    '''
    def __init__ (self,data,raw_text
                 ,Debug=False,maxrows=50
                 ):
        f = '[MClient] cells.Pos.__init__'
        self.blocks = []
        self.query = ''
        # Sqlite fetch
        self.data = data
        self.Debug = Debug
        self.maxrows = maxrows
        # Retrieved from the TkinterHTM widget
        self.rawtext = raw_text
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
            block = Block()
            block.no = item[0]
            block.type_ = item[1]
            block.text = item[2]
            block.same = item[3]
            block.i = item[4]
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
            mes = sh.FastTable (headers = headers
                               ,iterable = rows
                               ,maxrow = 70
                               ,maxrows = self.maxrows
                               ,Transpose = True
                               ).run()
            sh.com.run_fast_debug(f,mes)
    
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
            text = sh.Text(block.text.strip()).delete_duplicate_spaces()
            if text:
                search = sh.Search (text = self.rawtext
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
        ''' This may be caused by the following:
            a) Missing types in db.DB.types
            b) Defective HTML generation algorithm
        '''
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
        self.blocks = blocks
        self.Debug = Debug
        self.obj = obj
        self.query = ''
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
