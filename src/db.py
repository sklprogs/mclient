#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo:
    - DB.reset: reset TEXT for DIC, WFORM, SPEECH, TRANSC; reset BLOCK, PRIORITY, CELLNO, SELECTABLE, ROWNO, COLNO, POS1, POS2
    - Fix Moves.up on 'painting' (SelectTermsOnly=0)
    - Fix Moves on 'рабочая документация' (SelectTermsOnly=0), selects ')' twice, but does not select corrections
'''

'''
    We need 'POS1 < POS2' to skip empty blocks; POS1 = POS2 causes Moves to work incorrectly
'''

import gettext

gettext.install('mclient','./locale')

import sqlite3
import shared as sh
import sharedGUI as sg


# note: don't forget to change 'self.Selectable', 'self._cols', 'self.SortTerms' externally
class DB:

    def __init__(self):
        self._source    = ''
        self._search    = ''
        self.Selectable = True
        self.reset()
        self.db         = sqlite3.connect(':memory:')
        self.dbc        = self.db.cursor()
        # We use integers instead of booleans; -1 means not set
        # Must indicate 'integer' fully before 'primary key autoincrement'
        self.dbc.execute (
                    'create table if not exists BLOCKS (\
                     NO         integer primary   \
                                key autoincrement \
                    ,SOURCE     text              \
                    ,SEARCH     text              \
                    ,URLA       text              \
                    ,DICA       text              \
                    ,WFORMA     text              \
                    ,SPEECHA    text              \
                    ,TRANSCA    text              \
                    ,TERMA      text              \
                    ,TYPE       text              \
                    ,TEXT       text              \
                    ,URL        text              \
                    ,BLOCK      integer           \
                    ,PRIORITY   integer           \
                    ,SELECTABLE integer           \
                    ,SAMECELL   integer           \
                    ,CELLNO     integer           \
                    ,ROWNO      integer           \
                    ,COLNO      integer           \
                    ,POS1       integer           \
                    ,POS2       integer           \
                    ,NODE1      text              \
                    ,NODE2      text              \
                    ,OFFPOS1    integer           \
                    ,OFFPOS2    integer           \
                    ,BBOX1      integer           \
                    ,BBOX2      integer           \
                    ,BBOY1      integer           \
                    ,BBOY2      integer           \
                    ,TEXTLOW    text              \
                    ,IGNORE     integer           \
                                                       )'
                         )

    def reset (self,cols=('dic','wform','transc','speech')
              ,SortRows=False,SortTerms=False
              ):
        self.SortTerms = SortTerms
        self._cols     = cols
        if not self._cols: # Prevents None + tuple
            self._cols = ('dic','wform','transc','speech')
            sh.log.append ('DB.reset'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        self._types    = self._cols + ('term','phrase','comment','correction')

    def fill(self,data):
        self.dbc.executemany('insert into BLOCKS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)

    def fetch(self):
        self.dbc.execute('select TYPE,TEXT,ROWNO,COLNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 order by CELLNO,NO',(self._source,self._search,))
        return self.dbc.fetchall()

    def present(self):
        self.dbc.execute('select NO from BLOCKS where SOURCE = ? and SEARCH = ?',(self._source,self._search,))
        return self.dbc.fetchall()

    def searches(self):
        self.dbc.execute('select distinct SEARCH from BLOCKS order by NO desc')
        result = self.dbc.fetchall()
        if result:
            return [item[0] for item in result]

    def cur_nos(self,Block=True):
        if self._search:
            if Block:
                self.dbc.execute('select NO from BLOCKS where SEARCH = ? and BLOCK = 0 and IGNORE = 0 order by NO',(self._search,))
            else:
                self.dbc.execute('select NO from BLOCKS where SEARCH = ? order by NO',(self._search,))
            result = self.dbc.fetchall()
            if result:
                return(result[0][0],result[-1][0])
        else:
            sh.log.append ('DB.prev_search'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def prev_search(self):
        nos = self.cur_nos()
        if nos:
            self.dbc.execute('select SEARCH from BLOCKS where NO < ? and BLOCK = 0 and IGNORE = 0 order by NO desc',(nos[0],))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.prev_search'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def next_search(self):
        nos = self.cur_nos()
        if nos:
            self.dbc.execute('select SEARCH from BLOCKS where NO > ? and BLOCK = 0 and IGNORE = 0 order by NO',(nos[-1],))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.prev_search'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def request(self,source,search):
        if source and search:
            self._source = source
            self._search = search
        else:
            sh.log.append ('DB.request'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def print(self,Selected=False,Shorten=False,MaxRow=20,MaxRows=20):
        # 'self.dbc.description' is 'None' without performing 'select' first
        if not Selected:
            self.dbc.execute('select * from BLOCKS order by CELLNO,NO')
        headers = [cn[0] for cn in self.dbc.description]
        rows    = self.dbc.fetchall()
        sh.Table (headers = headers
                 ,rows    = rows
                 ,Shorten = Shorten
                 ,MaxRow  = MaxRow
                 ,MaxRows = MaxRows
                 ).print()

    def update(self,query):
        try:
            self.dbc.executescript(query)
        except sqlite3.OperationalError:
            sg.Message ('DB.update'
                       ,_('ERROR')
                       ,_('Unable to execute:\n"%s"') % str(query).replace(';',';\n')
                       )

    # Assign input data for BlockPrioritize
    def assign_bp(self):
        if self._source and self._search:
            self.dbc.execute('select NO,TYPE,TEXT,DICA from BLOCKS where SOURCE = ? and SEARCH = ? order by NO',(self._source,self._search))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.assign_bp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def order_query(self):
        query = []
        for item in self._cols:
            if item == 'dic':
                query.append('PRIORITY desc')
                query.append('DICA')
            elif item == 'wform':
                query.append('WFORMA')
            elif item == 'speech':
                query.append('SPEECHA')
            elif item == 'transc':
                # There is no sense to sort by transcription
                pass
            else:
                sg.Message (func    = 'DB.order_query'
                           ,level   = _('ERROR')
                           ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(item),'dic, wform, speech, transc')
                           )
        if self.SortTerms:
            query.append('TERMA')
        return ','.join(query)

    # Assign input data for Cells
    def assign_cells(self):
        if self._source and self._search:
            query = 'select NO,TYPE,TEXT,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 order by '
            order = self.order_query()
            if order:
                query += order + ',NO'
            else:
                query += 'NO'
            self.dbc.execute(query,(self._source,self._search,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.assign_cells'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Assign input data for Pos
    def assign_pos(self):
        if self._source and self._search:
            self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,ROWNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 order by CELLNO,NO',(self._source,self._search,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.assign_pos'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def phrase_dic(self):
        if self._source and self._search:
            self.dbc.execute('select DICA from BLOCKS where SOURCE = ? and SEARCH = ? and TYPE = ? order by NO',(self._source,self._search,'phrase',))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.phrase_dic'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def clear(self):
        sh.log.append ('DB.clear'
                      ,_('WARNING')
                      ,_('Delete all records from %s') % 'BLOCKS'
                      )
        # VACUUM command is a no-op for in-memory databases
        self.dbc.execute('delete from BLOCKS')

    def clear_cur(self):
        nos = self.cur_nos(Block=0)
        if nos:
            sh.log.append ('DB.clear_cur'
                          ,_('WARNING')
                          ,_('Delete records %d-%d from %s') % (nos[0],nos[1],'BLOCKS')
                          )
            # Sqlite does not warn about '? <= NO >= ?', but this does nothing
            self.dbc.execute('delete from BLOCKS where NO >= ? and NO <= ?',(nos[0],nos[1],))
        else:
            sh.log.append ('DB.clear_cur'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def block_pos(self,pos):
        if self._source and self._search:
            if self.Selectable:
                # 'POS2 > pos' instead of 'POS2 >= pos' allows to correctly navigate through blocks where separate words have been found
                self.dbc.execute('select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT,SELECTABLE from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 <= ? and POS2 > ? and POS1 < POS2 and SELECTABLE = 1',(self._source,self._search,pos,pos,))
            else:
                self.dbc.execute('select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT,SELECTABLE from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 <= ? and POS2 > ? and POS1 < POS2',(self._source,self._search,pos,pos,))
            return self.dbc.fetchone()
        else:
            # Too frequent
            #sh.log.append('DB.block_pos',_('WARNING'),_('Empty input is not allowed!'))
            pass

    def urla(self):
        if self._source and self._search:
            self.dbc.execute('select URLA from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0',(self._source,self._search,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.urla'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def url(self,pos):
        if self._source and self._search:
            self.dbc.execute('select URL from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 <= ? and POS2 > ?',(self._source,self._search,pos,pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def text(self,pos):
        if self._source and self._search:
            self.dbc.execute('select TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 <= ? and POS2 > ?',(self._source,self._search,pos,pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.text'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def min_cell(self):
        if self._source and self._search:
            if self.Selectable:
                # This function is made for calculating moves; if we don't take into account types, the first selectable cell may not be reached (e.g., it has 'transc' type)
                self.dbc.execute('select CELLNO,NO,POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select CELLNO,NO,POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_cell'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def max_cell(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select CELLNO,NO,POS1,BBOX1,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select CELLNO,NO,POS1,BBOX1,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_cell'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the maximum available row number for the whole table; this might not be the same as ROWNO of 'self.max_cell'
    def max_row(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select ROWNO,NO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by ROWNO desc',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select ROWNO,NO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by ROWNO desc',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_row'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the maximum available column number for the whole table; this might not be the same as COLNO of 'self.max_cell'
    def max_col(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select COLNO,NO,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by COLNO desc,NO desc',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select COLNO,NO,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by COLNO desc,NO desc',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_col'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the maximum available row number for the set column
    def max_row_sp(self,col_no):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select ROWNO,NO from BLOCKS where COLNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by ROWNO desc,NO desc',(col_no,self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select ROWNO,NO from BLOCKS where COLNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by ROWNO desc,NO desc',(col_no,self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_row_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the maximum available column number for the set row
    def max_col_sp(self,row_no):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select COLNO,NO,BBOX2 from BLOCKS where ROWNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by COLNO desc,NO desc',(row_no,self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select COLNO,NO,BBOX2 from BLOCKS where ROWNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by COLNO desc,NO desc',(row_no,self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_col_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the minimum available column number for the whole table; this should be the same as COLNO of 'self.min_cell' but we leave it for non-standard tables
    def min_col(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select COLNO,NO,BBOX1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by COLNO,NO',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select COLNO,NO,BBOX1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by COLNO,NO',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_col'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the minimum available row number for the whole table; this should be the same as ROWNO of 'self.min_cell' but we leave it for non-standard tables
    def min_row(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select ROWNO,NO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select ROWNO,NO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_row'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the minimum available row number for the set column; this might not be the same as ROWNO of 'self.min_cell'
    def min_row_sp(self,col_no):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select ROWNO,NO from BLOCKS where COLNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by ROWNO,NO',(col_no,self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select ROWNO,NO from BLOCKS where COLNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by ROWNO,NO',(col_no,self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_row_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the minimum available column number for the set row
    def min_col_sp(self,row_no):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select COLNO,NO,BBOX1 from BLOCKS where ROWNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by COLNO,NO',(row_no,self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select COLNO,NO,BBOX1 from BLOCKS where ROWNO = ? and SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by COLNO,NO',(row_no,self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_col_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def selection(self,pos):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select NODE1,NODE2,OFFPOS1,OFFPOS2,BBOX1,BBOX2,BBOY1,BBOY2,ROWNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 and POS1 <= ? and POS2 >= ? order by COLNO,NO',(self._source,self._search,'term','phrase',pos,pos,))
            else:
                self.dbc.execute('select NODE1,NODE2,OFFPOS1,OFFPOS2,BBOX1,BBOY1,BBOX2,BBOY2,ROWNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and POS1 <= ? and POS2 >= ? order by COLNO,NO',(self._source,self._search,pos,pos,))
            return self.dbc.fetchone()
        else:
            pass
            '''
            # Too frequent
            sh.log.append ('DB.selection'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            '''

    def node_y1(self,bboy):
        if self._source and self._search:
            self.dbc.execute('select NODE1,BBOY1,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and BBOY1 >= ? order by BBOY1',(self._source,self._search,bboy,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.node_y1'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def row(self,row_no):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select BBOX1,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 and ROWNO = ? order by CELLNO,NO',(self._source,self._search,'term','phrase',row_no,))
            else:
                self.dbc.execute('select BBOX1,BBOX2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and ROWNO = ? order by CELLNO,NO',(self._source,self._search,row_no,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.row'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def blocked(self):
        if self._source and self._search:
            self.dbc.execute('select NO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 1',(self._source,self._search,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.blocked'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def prioritized(self):
        if self._source and self._search:
            # note: We assume that 'Phrases' section has -1000 priority and this is always used despite user settings
            self.dbc.execute('select NO from BLOCKS where SOURCE = ? and SEARCH = ? and PRIORITY != 0 and PRIORITY != -1000',(self._source,self._search,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.prioritized'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def dics(self,Block=False):
        if self._source and self._search:
            # Do not use 'POS1 < POS2', it might be not set yet
            if Block:
                self.dbc.execute('select TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and TYPE = ? and TEXT != ?',(self._source,self._search,'dic','',))
            else:
                self.dbc.execute('select TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and TYPE = ? and TEXT != ?',(self._source,self._search,'dic','',))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.dics'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def search_forward(self,pos,search):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and TEXTLOW like ? and POS1 > ? order by CELLNO,NO',(self._source,self._search,'term','phrase','%' + search + '%',pos,))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and TEXTLOW like ? and POS1 > ? order by CELLNO,NO',(self._source,self._search,'%' + search + '%',pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.search_forward'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def search_backward(self,pos,search):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and TEXTLOW like ? and POS2 < ? order by CELLNO desc,NO desc',(self._source,self._search,'term','phrase','%' + search + '%',pos,))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and TEXTLOW like ? and POS2 < ? order by CELLNO desc,NO desc',(self._source,self._search,'%' + search + '%',pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.search_backward'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def unignore(self):
        self.dbc.execute('update BLOCKS set IGNORE = 0 where SOURCE = ? and SEARCH = ?',(self._source,self._search,))

    def ignore(self):
        self.dbc.execute('update BLOCKS set IGNORE = 1 where SOURCE = ? and SEARCH = ? and TYPE not in %s' % (self._types,),(self._source,self._search,))
        if 'dic' not in self._types:
            self.dbc.execute('update BLOCKS set IGNORE = 1 where SOURCE = ? and SEARCH = ? and TYPE = ?',(self._source,self._search,'phrase',))
            
    # Get any block with the minimal BBOY1 for the set column number
    def min_bboy(self,row_no=0):
        if self._source and self._search:
            self.dbc.execute('select BBOY1,BBOY2,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and ROWNO = ? order by BBOY1',(self._source,self._search,row_no,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_bboy'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    # Only a cell number must be on input (in case of a pos, block parameters are returned)
    def cell(self,cell_no=0):
        if self._source and self._search:
            self.dbc.execute('select NODE1,BBOX1,BBOY1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and CELLNO = ? order by NO',(self._source,self._search,cell_no,))
            result1 = self.dbc.fetchone()
            self.dbc.execute('select NODE2,BBOX2,BBOY2 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and CELLNO = ? order by NO desc',(self._source,self._search,cell_no,))
            result2 = self.dbc.fetchone()
            if result1 and result2:
                # NODE1,NODE2,BBOX1,BBOX2,BBOY1,BBOY2
                return(result1[0],result2[0],result1[1],result2[1],result1[2],result2[2])
        else:
            sh.log.append ('DB.cell'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    # Get any block with the maximal BBOY2
    def max_bboy(self,limit=0):
        if self._source and self._search:
            if limit:
                self.dbc.execute('select BBOY2,NODE1,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and BBOY2 < ? order by BBOY2 desc',(self._source,self._search,limit,))
            else:
                self.dbc.execute('select BBOY2,NODE1,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by BBOY2 desc',(self._source,self._search,))
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_bboy'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def zzz(self):
        pass



# Separating this class will slow down the program at ~0,027s.
class Moves(DB):

    def __init__(self):
        super().__init__()

    def start(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.start'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def end(self):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,'term','phrase',))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.end'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def line_start(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and ROWNO = ? and COLNO <= ? and POS1 < POS2 order by COLNO,NO',(self._source,self._search,'term','phrase',row_no,col_no,))
                else:
                    self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and ROWNO = ? and COLNO <= ? and POS1 < POS2 order by COLNO,NO',(self._source,self._search,row_no,col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            else:
                sh.log.append ('Moves.line_start'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.line_start'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def line_end(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and ROWNO = ? and COLNO >= ? and POS1 < POS2 order by COLNO desc,NO desc',(self._source,self._search,'term','phrase',row_no,col_no,))
                else:
                    self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and ROWNO = ? and COLNO >= ? and POS1 < POS2 order by COLNO desc,NO desc',(self._source,self._search,row_no,col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            else:
                sh.log.append ('Moves.line_end'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.line_end'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def left(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, no = poses[2], poses[5]
                min_cell = self.min_cell()
                max_cell = self.max_cell()
                if min_cell and max_cell:
                    if no == min_cell[1]:
                        return max_cell[2]
                    elif self.Selectable:
                        self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and CELLNO <= ? and POS1 < ? and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,'term','phrase',cell_no,pos,))
                    else:
                        self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and CELLNO <= ? and POS1 < ? and POS1 < POS2 order by CELLNO desc,NO desc',(self._source,self._search,cell_no,pos,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                else:
                    sh.log.append ('Moves.left'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Moves.left'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.left'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def right(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, no = poses[2], poses[5]
                max_cell = self.max_cell()
                min_cell = self.min_cell()
                if min_cell and max_cell:
                    if no == max_cell[1]:
                        return min_cell[2] # Loop moves
                    elif self.Selectable:
                        self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and CELLNO >= ? and POS1 > ? and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,'term','phrase',cell_no,pos,))
                    else:
                        self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and CELLNO >= ? and POS1 > ? and POS1 < POS2 order by CELLNO,NO',(self._source,self._search,cell_no,pos,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                else:
                    sh.log.append ('Moves.right'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Moves.right'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.right'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def up(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, row_no, col_no, no = poses[2], poses[3], poses[4], poses[5]
                min_cell   = self.min_cell()
                min_row_sp = self.min_row_sp(col_no=col_no)
                max_col    = self.max_col()
                if min_cell and max_col and min_row_sp:
                    if no == min_cell[1]:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO = ? and POS1 < POS2 order by ROWNO desc,NO desc',(self._source,self._search,'term','phrase',max_col[0],))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO = ? and POS1 < POS2 order by ROWNO desc,NO desc',(self._source,self._search,max_col[0],))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == min_row_sp[1]:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO < ? and POS1 < POS2 order by COLNO desc,ROWNO desc,NO desc',(self._source,self._search,'term','phrase',col_no,))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO < ? and POS1 < POS2 order by COLNO desc,ROWNO desc,NO desc',(self._source,self._search,col_no,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO = ? and ROWNO <= ? and POS1 < ? and POS1 < POS2 order by ROWNO desc,NO desc',(self._source,self._search,'term','phrase',col_no,row_no,pos,))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO = ? and ROWNO <= ? and POS1 < ? and POS1 < POS2 order by ROWNO desc,NO desc',(self._source,self._search,col_no,row_no,pos,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                else:
                    sh.log.append ('Moves.up'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Moves.up'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.up'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def down(self,pos):
        if self._source and self._search:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, row_no, col_no, no = poses[2], poses[3], poses[4], poses[5]
                min_col    = self.min_col()
                max_row_sp = self.max_row_sp(col_no=col_no)
                max_col    = self.max_col()
                if min_col and max_row_sp and max_col:
                    if no == max_row_sp[1] and no == max_col[1]:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO = ? and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,'term','phrase',min_col[0],))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO = ? and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,min_col[0],))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == max_row_sp[1]:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO > ? and POS1 < POS2 order by COLNO,ROWNO,NO',(self._source,self._search,'term','phrase',col_no,))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO > ? and POS1 < POS2 order by COLNO,ROWNO,NO',(self._source,self._search,col_no,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and COLNO = ? and ROWNO >= ? and POS1 > ? and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,'term','phrase',col_no,row_no,pos,))
                        else:
                            self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and COLNO = ? and ROWNO >= ? and POS1 > ? and POS1 < POS2 order by ROWNO,NO',(self._source,self._search,col_no,row_no,pos,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                else:
                    sh.log.append ('Moves.down'
                                  ,_('WARNING')
                                  ,_('Empty input is not allowed!')
                                  )
            else:
                sh.log.append ('Moves.down'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.down'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def page_down(self,bboy,height):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 and BBOY1 >= ? order by CELLNO,NO',(self._source,self._search,'term','phrase',int(bboy / height) * height + height,))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and BBOY1 >= ? order by CELLNO,NO',(self._source,self._search,int(bboy / height) * height + height,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.page_down'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def page_up(self,bboy,height):
        if self._source and self._search:
            if self.Selectable:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 and POS1 < POS2 and BBOY1 >= ? order by CELLNO,NO',(self._source,self._search,'term','phrase',int(bboy / height) * height - height,))
            else:
                self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 and BBOY1 >= ? order by CELLNO,NO',(self._source,self._search,int(bboy / height) * height - height,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.page_up'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def zzz(self):
        pass



if __name__ == '__main__':
    import page    as pg
    import tags    as tg
    import elems   as el
    import cells   as cl
    import mclient as mc

    # Modifiable
    source     = _('Online')
    #search    = 'рабочая документация'
    #search    = 'таратайка'
    search     = 'martyr'
    #file      = '/home/pete/tmp/ars/рабочая документация.txt'
    #file      = '/home/pete/tmp/ars/таратайка.txt'
    file       = '/home/pete/tmp/ars/martyr.txt'
    #file      = None
    collimit   = 10
    blacklist  = []
    prioritize = ['Общая лексика']

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

    tags = tg.Tags(page._page)
    tags.run()

    elems = el.Elems (blocks = tags._blocks
                     ,source = source
                     ,search = search
                     )
    elems.run()

    blocks_db = DB()
    blocks_db.fill(elems._data)
    blocks_db.request(source=source,search=search)

    ph_terma = el.PhraseTerma (dbc    = blocks_db.dbc
                              ,source = source
                              ,search = search
                              )
    ph_terma.run()

    data       = blocks_db.assign_bp()
    phrase_dic = blocks_db.phrase_dic ()

    bp = cl.BlockPrioritize (data       = data
                            ,source     = source
                            ,search     = search
                            ,blacklist  = blacklist
                            ,prioritize = prioritize
                            ,phrase_dic = phrase_dic
                            )
    bp.run()
    blocks_db.update(query=bp._query)

    data = blocks_db.assign_cells()
    cells = cl.Cells (data     = data
                     ,collimit = collimit
                     ,cols     = ('dic','wform','transc','speech')
                     )
    cells.run()
    blocks_db.update(query=cells._query)

    blocks_db.print(Shorten=1,MaxRow=15,MaxRows=150)
