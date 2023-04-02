#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh
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
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' It is assumed that we have already reset 'logic.SpeechPrior' with
            the required speech order before.
        '''
        unknown_prior = []
        if not self.spdic:
            sh.com.rep_empty(f)
            return
        for block in self.blocks:
            sprior = self.spdic.get(block.speech)
            if sprior:
                block.sprior = sprior
            elif not block.speech in unknown_prior:
                mes = _('A priority of the part of speech "{}" is not defined!')
                mes = mes.format(block.speech)
                sh.objs.get_mes(f,mes,True).show_warning()
                unknown_prior.append(block.speech)
    
    def run(self):
        f = '[MClient] cells.BlockPrioritize.run'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.assign()
        self.block()
        self.prioritize_dics()
        self.prioritize_speech()
        self.dump()
        self.debug()
    
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
            if not block.dic:
                continue
            if self.phdic == block.dic:
                ''' - This value should be set irrespectively of
                      'self.Prioritize'.
                    - Set the (presumably) lowest priority for a 'Phrases'
                      subject. This must be quite a small value as not to
                      conflict with other subjects.
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
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        mes = [self._debug_blocks()]
        mes = '\n\n'.join(mes)
        sh.com.run_fast_debug(f,mes)



class Cells:
    ''' This re-assigns DIC, WFORM, SPEECH, TRANSC types. We assume that sqlite
        has already sorted DB with 'BLOCK IS NOT 1'.
        Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DIC, WFORM
                                   ,SPEECH, SPEECHPR, TRANSC.
        Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO
        #NOTE: collimit at input: fixed columns are included.
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
                sub = '{} > {} - {}'.format (self.collimit
                                            ,old_len
                                            ,len(self.cols)
                                            )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_warning()
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
        if not self.phdic:
            return
        for block in self.blocks:
            if block.dic == self.phdic \
            and block.type_ in ('wform','speech','transc'):
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

    def move_phrases_end(self):
        f = '[MClient] cells.Cells.move_phrases_end'
        if not self.phdic:
            sh.com.rep_empty(f)
            return
        phrases = [block for block in self.blocks if block.dic == self.phdic]
        blocks = [block for block in self.blocks if block.dic != self.phdic]
        self.blocks = blocks + phrases
    
    def run(self):
        f = '[MClient] cells.Cells.run'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.assign()
        self.restore_fixed()
        self.clear_fixed()
        self.set_fixed()
        self.set_cols()
        self.clear_phrases()
        self.expand_speech()
        self.move_phrases_end()
        self.wrap()
        self.sort_cells()
        self.set_cellno()
        self.debug()
        
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
        if not self.Debug:
            sh.com.rep_lazy(f)
            return
        headers = ('NO','TYPE','FIXED','TEXT','DIC','WFORM','SPEECH','SPEECHPR'
                  ,'ROWNO','COLNO','CELLNO','SAME'
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
        mes = f + '\n' + mes
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
            ''' The warning about a missing 'dic' type (which was 'phdic'
                before) is natural.
            '''
            if type_ != 'dic':
                mes = _('Wrong input data: "{}"!').format(type_)
                sh.objs.get_mes(f,mes,True).show_warning()
        return 0
    
    def wrap_x(self):
        ''' #NOTE: orders of fixed columns in 'elems' and 'cells' can be
            different, so blocks should not be processed sequentially.
        '''
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
        if not self.spdic:
            sh.com.rep_lazy(f)
            return
        for block in self.blocks:
            if not (block.type_ == 'speech' and block.text):
                continue
            result = self.spdic.get(block.text)
            if result:
                block.text = result
            elif not block.text in self.unsupsp:
                self.unsupsp.append(block.text)
                mes = _('An unsupported part of speech: "{}"!')
                mes = mes.format(block.text)
                sh.objs.get_mes(f,mes,True).show_warning()
    
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
