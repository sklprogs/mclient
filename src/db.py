#!/usr/bin/python3
# -*- coding: UTF-8 -*-

'''
    We need 'POS1 < POS2' to skip empty blocks; POS1 = POS2 causes
    Moves to work incorrectly
'''

import sqlite3
import shared as sh

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


''' #note: don't forget to change 'self.Selectable', 'self._cols',
    'self.SortTerms' externally
'''
class DB:

    def __init__(self):
        self.values()
        self.reset()
        self.db  = sqlite3.connect(':memory:')
        self.dbc = self.db.cursor()
        self.create_blocks()
        self.create_articles()
        
    def values(self):
        self.Selectable = True
        self._articleid = 0
        
    def create_blocks(self):
        ''' We use integers instead of booleans; -1 means not set.
            Must indicate 'integer' fully before 'primary key 
            autoincrement'.
            31 columns for now.
        '''
        self.dbc.execute (
           'create table if not exists BLOCKS (\
            NO         integer primary   \
                       key autoincrement \
           ,ARTICLEID  integer           \
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
           ,SPEECHPR   integer           \
           ,DICAF      text              \
                                              )'
                         )
                         
    def create_articles(self):
        self.dbc.execute (
            'create table if not exists ARTICLES (\
             ARTICLEID  integer primary   \
                        key autoincrement \
            ,SOURCE     text              \
            ,TITLE      text              \
            ,URL        text              \
            ,BOOKMARK   integer           \
                                                 )'
                         )

    def reset (self,cols=('dic','wform','transc','speech')
              ,SortRows=False,SortTerms=False,ExpandDic=False
              ):
        self.SortTerms = SortTerms
        self.SortRows  = SortRows
        self.ExpandDic = ExpandDic
        self._cols     = cols
        # Prevents None + tuple
        if not self._cols:
            self._cols = ('dic','wform','transc','speech')
            sh.log.append ('DB.reset'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        self._types = self._cols + ('term','phrase','comment'
                                   ,'correction'
                                   )

    def fill_blocks(self,data):
        self.dbc.executemany ('insert into BLOCKS values \
                               (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?\
                               ,?,?,?,?,?,?,?,?,?,?,?\
                               )'
                               ,data
                              )
        
    def fill_articles(self,data):
        self.dbc.execute('insert into ARTICLES values (?,?,?,?,?)',data)

    def fetch(self):
        self.dbc.execute ('select TYPE,TEXT,ROWNO,COLNO from BLOCKS \
                           where ARTICLEID = ? and BLOCK = 0 \
                           and IGNORE = 0 order by CELLNO,NO'
                         ,(self._articleid,)
                         )
        return self.dbc.fetchall()

    def present(self,source,title,url):
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           where SOURCE = ? and TITLE = ? and URL = ?'
                         ,(source,title,url,)
                         )
        result = self.dbc.fetchone()
        if result:
            return result[0]

    def searches(self):
        self.dbc.execute ('select distinct ARTICLEID,TITLE \
                           from ARTICLES order by ARTICLEID desc'
                         )
        return self.dbc.fetchall()

    def prev_id(self,Loop=True):
        if self._articleid:
            self.dbc.execute ('select ARTICLEID from ARTICLES \
                               where ARTICLEID < ? \
                               order by ARTICLEID desc'
                             ,(self._articleid,)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
            elif Loop:
                return self.max_articleid()
        else:
            sh.log.append ('DB.prev_id'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def next_id(self,Loop=True):
        if self._articleid:
            self.dbc.execute ('select ARTICLEID from ARTICLES \
                               where ARTICLEID > ? order by ARTICLEID'
                             ,(self._articleid,)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
            elif Loop:
                return self.min_articleid()
        else:
            sh.log.append ('DB.next_id'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20,mode='BLOCKS'
              ):
        ''' 'self.dbc.description' is 'None' without performing
            'select' first
        '''
        if not Selected:
            if mode == 'BLOCKS':
                self.dbc.execute ('select * from BLOCKS \
                                   order by CELLNO,NO'
                                 )
            elif mode == 'ARTICLES':
                self.dbc.execute ('select * from ARTICLES \
                                   order by ARTICLEID'
                                 )
            else:
                sh.objs.mes (func    = 'DB.print'
                            ,level   = _('ERROR')
                            ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                       % (str(mode),'ARTICLES, BLOCKS')
                            )
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
            sh.objs.mes ('DB.update'
                        ,_('ERROR')
                        ,_('Unable to execute:\n"%s"') \
                        % str(query).replace(';',';\n')
                        )

    # Assign input data for BlockPrioritize
    def assign_bp(self):
        if self._articleid:
            self.dbc.execute ('select NO,TYPE,TEXT,DICA from BLOCKS \
                               where ARTICLEID = ? order by NO'
                             ,(self._articleid,)
                             )
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
                ''' Full dictionary titles and abbreviations can be
                    sorted differently, for example, in case of
                    'файл.расшир.' -> 'Расширение файла'
                '''
                if self.ExpandDic:
                    query.append('LOWER(DICAF)')
                else:
                    query.append('LOWER(DICA)')
            elif item == 'wform':
                query.append('WFORMA')
            elif item == 'speech':
                query.append('SPEECHPR desc')
                query.append('SPEECHA')
            elif item == 'transc':
                # There is no sense to sort by transcription
                pass
            else:
                sh.objs.mes (func    = 'DB.order_query'
                            ,level   = _('ERROR')
                            ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                                       % (str(item)
                                         ,'dic, wform, speech, transc'
                                         )
                            )
        if self.SortTerms:
            query.append('TERMA')
        return ','.join(query)

    # Assign input data for Cells
    def assign_cells(self):
        if self._articleid:
            query = 'select NO,TYPE,TEXT,SAMECELL,'
            if self.ExpandDic:
                query += 'DICAF,'
            else:
                query += 'DICA,'
            query += 'WFORMA,SPEECHA,TRANSCA from BLOCKS \
                      where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                      order by '
            if self.SortRows:
                order = self.order_query()
            else:
                order = None
            if order:
                query += order + ',NO'
            else:
                query += 'NO'
            self.dbc.execute(query,(self._articleid,))
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.assign_cells'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Assign input data for Pos
    def assign_pos(self):
        if self._articleid:
            self.dbc.execute ('select NO,TYPE,TEXT,SAMECELL,ROWNO \
                               from BLOCKS where ARTICLEID = ? \
                               and BLOCK = 0 and IGNORE = 0 \
                               order by CELLNO,NO',(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.assign_pos'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Get 'PhraseDic' before 'Cells' are built when 'PhraseDic' is
        still of a 'phrase' type.
    '''
    def phrase_dic_primary(self):
        if self._articleid:
            self.dbc.execute ('select DICA from BLOCKS \
                               where ARTICLEID = ? and TYPE = ? \
                               order by NO',(self._articleid,'phrase',)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.phrase_dic_primary'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def phrase_dic(self):
        if self._articleid:
            result = self.phrase_dic_primary()
            if result:
                self.dbc.execute ('select POS1,URL,TEXT from BLOCKS \
                                   where ARTICLEID = ? and DICA = ? \
                                   order by NO'
                                 ,(self._articleid,result,)
                                 )
                return self.dbc.fetchone()
            else:
                sh.log.append ('DB.phrase_dic'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('DB.phrase_dic'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def clear(self):
        sh.log.append ('DB.clear'
                      ,_('WARNING')
                      ,_('Delete all records from %s') \
                      % 'ARTICLES, BLOCKS'
                      )
        # VACUUM command is a no-op for in-memory databases
        self.dbc.execute('delete from BLOCKS')
        self.dbc.execute('delete from ARTICLES')

    def clear_cur(self):
        if self._articleid:
            sh.log.append ('DB.clear_cur'
                          ,_('WARNING')
                          ,_('Delete records of article No. %d from %s')\
                          % (self._articleid,'BLOCKS, ARTICLES')
                          )
            self.dbc.execute ('delete from BLOCKS where ARTICLEID = ?'
                             ,(self._articleid,)
                             )
            self.dbc.execute ('delete from ARTICLES where ARTICLEID = ?'
                             ,(self._articleid,)
                             )
        else:
            sh.log.append ('DB.clear_cur'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def block_pos(self,pos):
        if self._articleid:
            if self.Selectable:
                ''' 'POS2 > pos' instead of 'POS2 >= pos' allows to
                    correctly navigate through blocks where separate
                    words have been found
                '''
                self.dbc.execute ('select POS1,POS2,CELLNO,ROWNO,COLNO\
                                  ,NO,TEXT,SELECTABLE,TYPE from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 <= ? \
                                   and POS2 > ? and POS1 < POS2 \
                                   and SELECTABLE = 1'
                                 ,(self._articleid,pos,pos,)
                                 )
            else:
                self.dbc.execute ('select POS1,POS2,CELLNO,ROWNO,COLNO\
                                  ,NO,TEXT,SELECTABLE,TYPE from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 <= ? \
                                   and POS2 > ? and POS1 < POS2'
                                 ,(self._articleid,pos,pos,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.block_pos'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def article(self):
        if self._articleid:
            self.dbc.execute ('select SOURCE,TITLE,URL,BOOKMARK \
                               from ARTICLES where ARTICLEID = ?'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.article'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def url(self,pos):
        if self._articleid:
            self.dbc.execute ('select URL from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 <= ? \
                               and POS2 > ?',(self._articleid,pos,pos,)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.url'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def text(self,pos):
        if self._articleid:
            self.dbc.execute ('select TEXT from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 <= ? \
                               and POS2 > ?'
                             ,(self._articleid,pos,pos,)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.text'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def min_cell(self):
        if self._articleid:
            if self.Selectable:
                ''' This function is made for calculating moves; if we
                    don't take into account types, the first selectable
                    cell may not be reached (e.g., it has 'transc' type)
                '''
                self.dbc.execute ('select CELLNO,NO,POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by CELLNO,NO'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select CELLNO,NO,POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by CELLNO,NO'
                                 ,(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_cell'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def max_cell(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select CELLNO,NO,POS1,BBOX1,BBOX2 \
                                   from BLOCKS where ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and TYPE in ("term","phrase") \
                                   and SELECTABLE = 1 and POS1 < POS2 \
                                   order by CELLNO desc,NO desc'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select CELLNO,NO,POS1,BBOX1,BBOX2 \
                                   from BLOCKS where ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and POS1 < POS2 order by CELLNO desc\
                                   ,NO desc',(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_cell'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Find the maximum available row number for the whole table;
        this might not be the same as ROWNO of 'self.max_cell'
    '''
    def max_row(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by ROWNO desc'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by ROWNO desc'
                                 ,(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_row'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Find the maximum available column number for the whole table;
        this might not be the same as COLNO of 'self.max_cell'
    '''
    def max_col(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select COLNO,NO,BBOX2 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by COLNO desc\
                                  ,NO desc',(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select COLNO,NO,BBOX2 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by COLNO desc,NO desc'
                                 ,(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_col'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    # Find the maximum available row number for the set column
    def max_row_sp(self,col_no):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where COLNO = ? and ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and TYPE in ("term","phrase") \
                                   and SELECTABLE = 1 and POS1 < POS2 \
                                   order by ROWNO desc,NO desc'
                                 ,(col_no,self._articleid,)
                                 )
            else:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where COLNO = ? and ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and POS1 < POS2 order by ROWNO desc\
                                  ,NO desc',(col_no,self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_row_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Find the minimum available column number for the whole table;
        this should be the same as COLNO of 'self.min_cell' but we leave
        it for non-standard tables
    '''
    def min_col(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select COLNO,NO,BBOX1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by COLNO,NO'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select COLNO,NO,BBOX1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by COLNO,NO',(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_col'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    ''' Find the minimum available row number for the set column;
        this might not be the same as ROWNO of 'self.min_cell'
    '''
    def min_row_sp(self,col_no):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where COLNO = ? and ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and TYPE in ("term","phrase") \
                                   and SELECTABLE = 1 and POS1 < POS2 \
                                   order by ROWNO,NO'
                                 ,(col_no,self._articleid,)
                                 )
            else:
                self.dbc.execute ('select ROWNO,NO from BLOCKS \
                                   where COLNO = ? and ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and POS1 < POS2 order by ROWNO,NO'
                                 ,(col_no,self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.min_row_sp'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def selection(self,pos):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select NODE1,NODE2,OFFPOS1,OFFPOS2\
                                  ,BBOX1,BBOX2,BBOY1,BBOY2,ROWNO \
                                   from BLOCKS where ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and SELECTABLE = 1 and POS1 < POS2 \
                                   and POS1 <= ? and POS2 >= ? \
                                   order by COLNO,NO'
                                 ,(self._articleid,pos,pos,)
                                 )
            else:
                self.dbc.execute ('select NODE1,NODE2,OFFPOS1,OFFPOS2\
                                  ,BBOX1,BBOY1,BBOX2,BBOY2,ROWNO \
                                   from BLOCKS where ARTICLEID = ? \
                                   and BLOCK = 0 and IGNORE = 0 \
                                   and POS1 < POS2 and POS1 <= ? \
                                   and POS2 >= ? order by COLNO,NO'
                                 ,(self._articleid,pos,pos,)
                                 )
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

    def blocked(self):
        if self._articleid:
            self.dbc.execute ('select NO from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 1'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.blocked'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def prioritized(self):
        if self._articleid:
            ''' #note: We assume that 'Phrases' section has -1000
                priority and this is always used despite user settings.
            '''
            self.dbc.execute ('select NO from BLOCKS \
                               where ARTICLEID = ? and PRIORITY != 0 \
                               and PRIORITY != -1000'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.prioritized'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def dics(self,Block=False):
        if self._articleid:
            # Do not use 'POS1 < POS2', it might be not set yet
            if Block:
                self.dbc.execute ('select TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE = "dic" \
                                   and TEXT != ""',(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select TEXT from BLOCKS \
                                   where ARTICLEID = ? and TYPE = "dic"\
                                   and TEXT != ""',(self._articleid,)
                                 )
            return self.dbc.fetchall()
        else:
            sh.log.append ('DB.dics'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def search_forward(self,pos,search):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and TEXTLOW like ? and POS1 > ? \
                                   order by CELLNO,NO'
                                 ,(self._articleid
                                  ,'%' + search + '%',pos,
                                  )
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TEXTLOW like ? \
                                   and POS1 > ? order by CELLNO,NO'
                                 ,(self._articleid
                                  ,'%' + search + '%',pos,
                                  )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.search_forward'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def search_backward(self,pos,search):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and TEXTLOW like ? and POS2 < ? \
                                   order by CELLNO desc,NO desc'
                                 ,(self._articleid
                                  ,'%' + search + '%',pos,
                                  )
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TEXTLOW like ? \
                                   and POS2 < ? order by CELLNO desc\
                                  ,NO desc'
                                 ,(self._articleid
                                  ,'%' + search + '%',pos,
                                  )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('DB.search_backward'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def unignore(self):
        self.dbc.execute ('update BLOCKS set IGNORE = 0 \
                           where ARTICLEID = ?',(self._articleid,)
                         )

    def ignore(self):
        self.dbc.execute ('update BLOCKS set IGNORE = 1 \
                           where ARTICLEID = ? and TYPE not in %s' \
                           % (self._types,),(self._articleid,)
                         )
        if 'dic' not in self._types:
            self.dbc.execute ('update BLOCKS set IGNORE = 1 \
                               where ARTICLEID = ? and TYPE = "phrase"'
                             ,(self._articleid,)
                             )
            
    # Get any block with the maximal BBOY2
    def max_bboy(self,limit=0):
        if self._articleid:
            if limit:
                self.dbc.execute ('select BBOY2,NODE1,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   and BBOY2 < ? order by BBOY2 desc'
                                 ,(self._articleid,limit,)
                                 )
            else:
                self.dbc.execute ('select BBOY2,NODE1,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by BBOY2 desc'
                                 ,(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_bboy'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    # Get any block with the maximal BBOX2
    def max_bbox(self,limit=0):
        if self._articleid:
            if limit:
                self.dbc.execute ('select BBOX2,NODE1,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   and BBOX2 < ? order by BBOX2 desc'
                                 ,(self._articleid,limit,)
                                 )
            else:
                self.dbc.execute ('select BBOX2,NODE1,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by BBOX2 desc'
                                 ,(self._articleid,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.max_bbox'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    # Get the minimum BBOY1 and the maximum BBOY2 for the set row number
    def bboy_limits(self,row_no=0):
        if self._articleid:
            self.dbc.execute ('select BBOY1 from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 < POS2 \
                               and ROWNO = ? order by BBOY1'
                             ,(self._articleid,row_no,)
                             )
            min_result = self.dbc.fetchone()
            self.dbc.execute ('select BBOY2 from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 < POS2 \
                               and ROWNO = ? order by BBOY2 desc'
                             ,(self._articleid,row_no,)
                             )
            max_result = self.dbc.fetchone()
            if min_result and max_result:
                return(min_result[0],max_result[0])
            else:
                sh.log.append ('DB.bboy_limits'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('DB.bboy_limits'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    ''' Get the minimum BBOX1 and the maximum BBOX2 for the set column
        number
    '''
    def bbox_limits(self,col_no=0):
        if self._articleid:
            self.dbc.execute ('select BBOX1 from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 < POS2 \
                               and COLNO = ? order by BBOX1'
                             ,(self._articleid,col_no,)
                             )
            min_result = self.dbc.fetchone()
            self.dbc.execute ('select BBOX2 from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and POS1 < POS2 \
                               and COLNO = ? order by BBOX2 desc'
                             ,(self._articleid,col_no,)
                             )
            max_result = self.dbc.fetchone()
            if min_result and max_result:
                return(min_result[0],max_result[0])
            else:
                sh.log.append ('DB.bbox_limits'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('DB.bbox_limits'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def min_articleid(self):
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           order by ARTICLEID'
                         )
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.log.append ('DB.min_articleid'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            # Default minimal autoincrement in SQlite
            return 1
            
    def max_articleid(self):
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           order by ARTICLEID desc'
                         )
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.log.append ('DB.max_articleid'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
            # Default minimal autoincrement in SQlite
            return 1
    
    def block_pos_next(self,pos):
        if self._articleid:
            if self.Selectable:
                ''' 'POS2 > pos' instead of 'POS2 >= pos' allows to
                    correctly navigate through blocks where separate
                    words have been found
                '''
                self.dbc.execute ('select POS1,POS2,CELLNO,ROWNO,COLNO\
                                  ,NO,TEXT,SELECTABLE from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and POS1 >= ? \
                                   and POS1 < POS2 and SELECTABLE = 1 \
                                   order by CELLNO,NO'
                                 ,(self._articleid,pos,)
                                 )
            else:
                self.dbc.execute ('select POS1,POS2,CELLNO,ROWNO,COLNO\
                                  ,NO,TEXT,SELECTABLE from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 >= ? \
                                   and POS1 < POS2 order by CELLNO,NO'
                                 ,(self._articleid,pos,)
                                 )
            return self.dbc.fetchone()
        else:
            sh.log.append ('DB.block_pos_next'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def set_bookmark(self,pos=0):
        if str(pos).isdigit():
            if self._articleid:
                ''' # Too frequent
                sh.log.append ('DB.set_bookmark'
                              ,_('DEBUG')
                              ,_('Set bookmark %d for article #%d') \
                              % (pos,self._articleid)
                              )
                '''
                self.dbc.execute ('update ARTICLES set BOOKMARK = ? \
                                   where ARTICLEID = ?'
                                 ,(pos,self._articleid,)
                                 )
            else:
                sh.log.append ('DB.set_bookmark'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('DB.set_bookmark'
                          ,_('WARNING')
                          ,_('Wrong input data!')
                          )
                          
    def delete_bookmarks(self):
        sh.log.append ('DB.delete_bookmarks'
                      ,_('DEBUG')
                      ,_('Delete bookmarks for all articles')
                      )
        self.dbc.execute('update ARTICLES set BOOKMARK = -1')
        
    def unprioritize_speech(self):
        self.dbc.execute('update BLOCKS set SPEECHPR = 0')



# Separating this class will slow down the program at ~0,027s.
class Moves(DB):

    def __init__(self):
        super().__init__()

    def start(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by CELLNO,NO'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by CELLNO,NO'
                                 ,(self._articleid,)
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.start'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def end(self):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 order by CELLNO desc\
                                  ,NO desc'
                                 ,(self._articleid,)
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   order by CELLNO desc,NO desc'
                                 ,(self._articleid,)
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.end'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def line_start(self,pos):
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    self.dbc.execute ('select POS1 from BLOCKS \
                                       where ARTICLEID = ? \
                                       and BLOCK = 0 and IGNORE = 0 \
                                       and TYPE in ("term","phrase") \
                                       and SELECTABLE = 1 and ROWNO = ?\
                                       and COLNO <= ? and POS1 < POS2 \
                                       order by COLNO,NO'
                                     ,(self._articleid,row_no,col_no,)
                                     )
                else:
                    self.dbc.execute ('select POS1 from BLOCKS \
                                       where ARTICLEID = ? \
                                       and BLOCK = 0 and IGNORE = 0 \
                                       and ROWNO = ? and COLNO <= ? \
                                       and POS1 < POS2 \
                                       order by COLNO,NO'
                                     ,(self._articleid,row_no,col_no,)
                                     )
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
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    self.dbc.execute ('select POS1 from BLOCKS \
                                       where ARTICLEID = ? \
                                       and BLOCK = 0 and IGNORE = 0 \
                                       and TYPE in ("term","phrase") \
                                       and SELECTABLE = 1 and ROWNO = ?\
                                       and COLNO >= ? and POS1 < POS2\
                                       order by COLNO desc,NO desc'
                                     ,(self._articleid,row_no,col_no,)
                                     )
                else:
                    self.dbc.execute ('select POS1 from BLOCKS \
                                       where ARTICLEID = ? \
                                       and BLOCK = 0 and IGNORE = 0 \
                                       and ROWNO = ? and COLNO >= ? \
                                       and POS1 < POS2 \
                                       order by COLNO desc,NO desc'
                                     ,(self._articleid,row_no,col_no,)
                                     )
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
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, no = poses[2], poses[5]
                min_cell = self.min_cell()
                max_cell = self.max_cell()
                if min_cell and max_cell:
                    if no == min_cell[1]:
                        return max_cell[2]
                    elif self.Selectable:
                        self.dbc.execute ('select POS1 from BLOCKS \
                                           where ARTICLEID = ? \
                                           and BLOCK = 0 and IGNORE = 0\
                                           and TYPE in \
                                           ("term","phrase") \
                                           and SELECTABLE = 1 \
                                           and CELLNO <= ? \
                                           and POS1 < ? \
                                           and POS1 < POS2 \
                                           order by CELLNO desc,NO desc'
                                         ,(self._articleid,cell_no,pos,)
                                         )
                    else:
                        self.dbc.execute ('select POS1 from BLOCKS \
                                           where ARTICLEID = ? \
                                           and BLOCK = 0 and IGNORE = 0\
                                           and CELLNO <= ? and POS1 < ?\
                                           and POS1 < POS2 \
                                           order by CELLNO desc,NO desc'
                                         ,(self._articleid,cell_no,pos,)
                                         )
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
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no, no = poses[2], poses[5]
                max_cell = self.max_cell()
                min_cell = self.min_cell()
                if min_cell and max_cell:
                    if no == max_cell[1]:
                        # Loop moves
                        return min_cell[2]
                    elif self.Selectable:
                        self.dbc.execute ('select POS1 from BLOCKS \
                                           where ARTICLEID = ? \
                                           and BLOCK = 0 and IGNORE = 0\
                                           and TYPE in \
                                           ("term","phrase") \
                                           and SELECTABLE = 1 \
                                           and CELLNO >= ? \
                                           and POS1 > ? and POS1 < POS2\
                                           order by CELLNO,NO'
                                         ,(self._articleid,cell_no,pos,)
                                         )
                    else:
                        self.dbc.execute ('select POS1 from BLOCKS \
                                           where ARTICLEID = ? \
                                           and BLOCK = 0 and IGNORE = 0\
                                           and CELLNO >= ? and POS1 > ?\
                                           and POS1 < POS2 \
                                           order by CELLNO,NO'
                                         ,(self._articleid,cell_no,pos,)
                                         )
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
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no = poses[2]
                row_no  = poses[3]
                col_no  = poses[4]
                no      = poses[5]
                min_cell   = self.min_cell()
                min_row_sp = self.min_row_sp(col_no=col_no)
                max_col    = self.max_col()
                if min_cell and max_col and min_row_sp:
                    if no == min_cell[1]:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO = ? \
                                               and POS1 < POS2 \
                                               order by ROWNO desc\
                                              ,NO desc'
                                             ,(self._articleid
                                              ,max_col[0],
                                              )
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS\
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO = ? \
                                               and POS1 < POS2 \
                                               order by ROWNO desc\
                                              ,NO desc'
                                             ,(self._articleid
                                              ,max_col[0],
                                              )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == min_row_sp[1]:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO < ? \
                                               and POS1 < POS2 \
                                               order by COLNO desc\
                                              ,ROWNO desc,NO desc'
                                             ,(self._articleid,col_no,)
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO < ? \
                                               and POS1 < POS2 \
                                               order by COLNO desc\
                                              ,ROWNO desc,NO desc'
                                             ,(self._articleid,col_no,)
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO = ? \
                                               and ROWNO <= ? \
                                               and POS1 < ? \
                                               and POS1 < POS2 \
                                               order by ROWNO desc\
                                              ,NO desc'
                                             ,(self._articleid,col_no
                                              ,row_no,pos,
                                              )
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS\
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO = ? \
                                               and ROWNO <= ? \
                                               and POS1 < ? \
                                               and POS1 < POS2 \
                                               order by ROWNO desc\
                                              ,NO desc'
                                             ,(self._articleid,col_no
                                              ,row_no,pos,
                                              )
                                             )
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
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                cell_no    = poses[2]
                row_no     = poses[3]
                col_no     = poses[4]
                no         = poses[5]
                min_col    = self.min_col()
                max_row_sp = self.max_row_sp(col_no=col_no)
                max_col    = self.max_col()

                if min_col and max_row_sp and max_col:
                    if row_no == max_row_sp[0] and col_no == max_col[0]:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS\
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO = ? \
                                               and POS1 < POS2 \
                                               order by ROWNO,NO'
                                             ,(self._articleid
                                              ,min_col[0],
                                              )
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS\
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO = ? \
                                               and POS1 < POS2 \
                                               order by ROWNO,NO'
                                             ,(self._articleid
                                              ,min_col[0]
                                              ,
                                              )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == max_row_sp[1]:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS\
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO > ? \
                                               and POS1 < POS2 \
                                               order by COLNO,ROWNO,NO'
                                             ,(self._articleid,col_no,)
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO > ? \
                                               and POS1 < POS2 \
                                               order by COLNO,ROWNO,NO'
                                             ,(self._articleid,col_no,)
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and TYPE in \
                                               ("term","phrase") \
                                               and SELECTABLE = 1 \
                                               and COLNO = ? \
                                               and ROWNO >= ? \
                                               and POS1 > ? \
                                               and POS1 < POS2 \
                                               order by ROWNO,NO'
                                             ,(self._articleid,col_no
                                              ,row_no,pos
                                              ,
                                              )
                                             )
                        else:
                            self.dbc.execute ('select POS1 from BLOCKS \
                                               where ARTICLEID = ? \
                                               and BLOCK = 0 \
                                               and IGNORE = 0 \
                                               and COLNO = ? \
                                               and ROWNO >= ? \
                                               and POS1 > ? \
                                               and POS1 < POS2 \
                                               order by ROWNO,NO'
                                             ,(self._articleid,col_no
                                              ,row_no,pos
                                              ,
                                              )
                                             )
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
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 and BBOY1 >= ? \
                                   order by CELLNO,NO'
                                 ,(self._articleid
                                  ,int(bboy / height) * height + height
                                  ,
                                  )
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   and BBOY1 >= ? order by CELLNO,NO'
                                 ,(self._articleid
                                  ,int(bboy / height) * height + height
                                  ,
                                  )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.page_down'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def page_up(self,bboy,height):
        if self._articleid:
            if self.Selectable:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and TYPE in \
                                   ("term","phrase") and SELECTABLE = 1\
                                   and POS1 < POS2 and BBOY1 >= ? \
                                   order by CELLNO,NO'
                                 ,(self._articleid
                                  ,int(bboy / height) * height - height
                                  ,
                                  )
                                 )
            else:
                self.dbc.execute ('select POS1 from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and POS1 < POS2 \
                                   and BBOY1 >= ? order by CELLNO,NO'
                                 ,(self._articleid
                                  ,int(bboy / height) * height - height
                                  ,
                                  )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.log.append ('Moves.page_up'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def first_section(self,col_no=0):
        if self._articleid:
            self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and COLNO = ? \
                               and POS1 < POS2 order by ROWNO,NO'
                             ,(self._articleid,col_no,)
                             )
            return self.dbc.fetchone()
        else:
            sh.log.append ('Moves.first_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def last_section(self,col_no=0):
        if self._articleid:
            self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and COLNO = ? \
                               and POS1 < POS2 order by ROWNO desc,NO'
                             ,(self._articleid,col_no,)
                             )
            return self.dbc.fetchone()
        else:
            sh.log.append ('Moves.last_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def next_section(self,pos,col_no=0,Loop=True):
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and ROWNO > ? \
                                   and COLNO = ? and POS1 < POS2 \
                                   order by CELLNO,NO'
                                 ,(self._articleid,poses[3],col_no,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result
                elif Loop:
                    return self.first_section(col_no=col_no)
            else:
                sh.log.append ('Moves.next_section'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.next_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
                          
    def prev_section(self,pos,col_no=0,Loop=True):
        if self._articleid:
            poses = self.block_pos(pos=pos)
            if poses:
                self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                                   where ARTICLEID = ? and BLOCK = 0 \
                                   and IGNORE = 0 and ROWNO < ? \
                                   and COLNO = ? and POS1 < POS2 \
                                   order by CELLNO desc,NO'
                                 ,(self._articleid,poses[3],col_no,)
                                 )
                result = self.dbc.fetchone()
                if result:
                    return result
                elif Loop:
                    return self.last_section(col_no=col_no)
            else:
                sh.log.append ('Moves.prev_section'
                              ,_('WARNING')
                              ,_('Empty input is not allowed!')
                              )
        else:
            sh.log.append ('Moves.prev_section'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
    
    def next_col(self,row_no=0,col_no=0):
        if self._articleid:
            self.dbc.execute ('select POS1,ROWNO,COLNO,TEXT \
                               from BLOCKS where ARTICLEID = ? \
                               and BLOCK = 0 and IGNORE = 0 \
                               and ROWNO = ? and COLNO >= ? \
                               and POS1 < POS2 order by CELLNO,NO'
                             ,(self._articleid,row_no,col_no,)
                             )
            return self.dbc.fetchone()
        else:
            sh.log.append ('Moves.next_col'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )


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
    articleid  = 0

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

    elems = el.Elems (blocks    = tags._blocks
                     ,articleid = articleid
                     )
    elems.run()

    blocks_db = DB()
    blocks_db.fill_blocks(elems._data)
    
    blocks_db._articleid = articleid

    ph_terma = el.PhraseTerma (dbc       = blocks_db.dbc
                              ,articleid = articleid
                              )
    ph_terma.run()

    data       = blocks_db.assign_bp()
    phrase_dic = blocks_db.phrase_dic ()

    bp = cl.BlockPrioritize (data       = data
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
