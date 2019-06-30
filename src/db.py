#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' We need 'POS1 < POS2' to skip empty blocks; POS1 = POS2 causes
    Moves to work incorrectly.
'''

import sqlite3
import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')


class DB:
    ''' #note: don't forget to change 'self.Selectable', 'self._cols',
        'self.SortTerms' externally.
    '''
    def __init__(self):
        self.values()
        self.reset()
        self.db  = sqlite3.connect(':memory:')
        self.dbc = self.db.cursor()
        self.create_blocks()
        self.create_articles()
        
    def next_dica(self,pos,dica):
        f = '[MClient] db.DB.next_dica'
        if self._articleid:
            self.dbc.execute ('select DICA,DICAF,NO,CELLNO from BLOCKS \
                               where ARTICLEID = ? and POS1 > ? \
                               and not DICA = ? and not DICAF = ? \
                               and BLOCK = 0 and IGNORE = 0 \
                               order by CELLNO,NO'
                             ,(self._articleid,pos,dica,dica,)
                             )
            return self.dbc.fetchone()
        else:
            sh.com.empty(f)
    
    def prev_dica(self,pos,dica):
        f = '[MClient] db.DB.prev_dica'
        if self._articleid:
            self.dbc.execute ('select DICA,DICAF,NO,CELLNO from BLOCKS \
                               where ARTICLEID = ? and POS1 < ? \
                               and not DICA = ? and not DICAF = ? \
                               and BLOCK = 0 and IGNORE = 0 \
                               order by CELLNO desc,NO desc'
                             ,(self._articleid,pos,dica,dica,)
                             )
            return self.dbc.fetchone()
        else:
            sh.com.empty(f)
    
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
        # 7 columns for now
        self.dbc.execute (
            'create table if not exists ARTICLES (\
             ARTICLEID  integer primary   \
                        key autoincrement \
            ,SOURCE     text              \
            ,TITLE      text              \
            ,URL        text              \
            ,LANG1      text              \
            ,LANG2      text              \
            ,BOOKMARK   integer           \
                                                 )'
                         )

    def reset (self,cols=('dic','wform','transc','speech')
              ,SortRows=False,SortTerms=False,ExpandDic=False
              ):
        f = '[MClient] db.DB.reset'
        self.SortTerms = SortTerms
        self.SortRows  = SortRows
        self.ExpandDic = ExpandDic
        self._cols     = cols
        # Prevents None + tuple
        if not self._cols:
            self._cols = ('dic','wform','transc','speech')
            sh.com.empty(f)
        #NOTE: do not forget to add new block types here
        self._types = self._cols + ('term','phrase','comment'
                                   ,'correction','user'
                                   )

    def fill_blocks(self,data):
        self.dbc.executemany ('insert into BLOCKS values \
                               (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?\
                               ,?,?,?,?,?,?,?,?,?,?,?\
                               )'
                               ,data
                              )
        
    def fill_articles(self,data):
        self.dbc.execute ('insert into ARTICLES values (?,?,?,?,?,?,?)'
                         ,data
                         )

    def fetch(self):
        self.dbc.execute ('select TYPE,TEXT,ROWNO,COLNO from BLOCKS \
                           where ARTICLEID = ? and BLOCK = 0 \
                           and IGNORE = 0 order by CELLNO,NO'
                         ,(self._articleid,)
                         )
        return self.dbc.fetchall()

    def present(self,source,title,lang1,lang2):
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           where SOURCE = ? and TITLE = ? and LANG1 = ?\
                           and LANG2 = ?'
                         ,(source,title,lang1,lang2,)
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
        f = '[MClient] db.DB.prev_id'
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
            sh.com.empty(f)

    def next_id(self,Loop=True):
        f = '[MClient] db.DB.next_id'
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
            sh.com.empty(f)

    def print (self,Selected=False,Shorten=False
              ,MaxRow=20,MaxRows=20,mode='BLOCKS'
              ):
        ''' 'self.dbc.description' is 'None' without performing
            'select' first
        '''
        f = '[MClient] db.DB.print'
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
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
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
        f = '[MClient] db.DB.update'
        try:
            self.dbc.executescript(query)
        except sqlite3.OperationalError:
            sh.objs.mes (f,_('ERROR')
                        ,_('Unable to execute:\n"%s"') \
                        % str(query).replace(';',';\n')
                        )

    # Assign input data for BlockPrioritize
    def assign_bp(self):
        f = '[MClient] db.DB.assign_bp'
        if self._articleid:
            self.dbc.execute ('select NO,TYPE,TEXT,DICA from BLOCKS \
                               where ARTICLEID = ? order by NO'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.com.empty(f)

    def order_query(self):
        f = '[MClient] db.DB.order_query'
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
                sh.objs.mes (f,_('ERROR')
                            ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') \
                            % (str(item),'dic, wform, speech, transc')
                            )
        if self.SortTerms:
            query.append('TERMA')
        return ','.join(query)

    # Assign input data for Cells
    def assign_cells(self):
        f = '[MClient] db.DB.assign_cells'
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
            #fix: this will not work for Cyrillic
            query += ' collate nocase'
            self.dbc.execute(query,(self._articleid,))
            return self.dbc.fetchall()
        else:
            sh.com.empty(f)

    # Assign input data for Pos
    def assign_pos(self):
        f = '[MClient] db.DB.assign_pos'
        if self._articleid:
            self.dbc.execute ('select NO,TYPE,TEXT,SAMECELL,ROWNO \
                               from BLOCKS where ARTICLEID = ? \
                               and BLOCK = 0 and IGNORE = 0 \
                               order by CELLNO,NO',(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.com.empty(f)

    def phrase_dic_primary(self):
        ''' Get 'PhraseDic' before 'Cells' are built when 'PhraseDic' is
            still of a 'phrase' type.
        '''
        f = '[MClient] db.DB.phrase_dic_primary'
        if self._articleid:
            self.dbc.execute ('select DICA from BLOCKS \
                               where ARTICLEID = ? and TYPE = ? \
                               order by NO',(self._articleid,'phrase',)
                             )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.empty(f)
                          
    def phrase_dic(self):
        f = '[MClient] db.DB.phrase_dic'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def clear(self):
        f = '[MClient] db.DB.clear'
        sh.log.append (f,_('WARNING')
                      ,_('Delete all records from %s') \
                      % 'ARTICLES, BLOCKS'
                      )
        # VACUUM command is a no-op for in-memory databases
        self.dbc.execute('delete from BLOCKS')
        self.dbc.execute('delete from ARTICLES')

    def clear_cur(self):
        f = '[MClient] db.DB.clear_cur'
        if self._articleid:
            sh.log.append (f,_('WARNING')
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
            sh.com.empty(f)

    def block_pos(self,pos):
        f = '[MClient] db.DB.block_pos'
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
        # Too frequent, especially on the Welcome screen
        #else:
        #    sh.com.empty(f)

    def article(self):
        f = '[MClient] db.DB.article'
        if self._articleid:
            self.dbc.execute ('select SOURCE,TITLE,URL,BOOKMARK,LANG1\
                                     ,LANG2 \
                               from ARTICLES where ARTICLEID = ?'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchone()
        else:
            sh.com.empty(f)

    def url(self,pos):
        f = '[MClient] db.DB.url'
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
            sh.com.empty(f)

    def text(self,pos):
        f = '[MClient] db.DB.text'
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
            sh.com.empty(f)

    def min_cell(self):
        f = '[MClient] db.DB.min_cell'
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
            sh.com.empty(f)

    def max_cell(self):
        f = '[MClient] db.DB.max_cell'
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
            sh.com.empty(f)

    def max_row(self):
        ''' Find the maximum available row number for the whole table;
            this might not be the same as ROWNO of 'self.max_cell'
        '''
        f = '[MClient] db.DB.max_row'
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
            sh.com.empty(f)

    def max_col(self):
        ''' Find the maximum available column number for the whole
            table; this might not be the same as COLNO of
            'self.max_cell'
        '''
        f = '[MClient] db.DB.max_col'
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
            sh.com.empty(f)

    # Find the maximum available row number for the set column
    def max_row_sp(self,col_no):
        f = '[MClient] db.DB.max_row_sp'
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
            sh.com.empty(f)

    def min_col(self):
        ''' Find the minimum available column number for the whole
            table; this should be the same as COLNO of 'self.min_cell'
            but we leave it for non-standard tables.
        '''
        f = '[MClient] db.DB.min_col'
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
            sh.com.empty(f)

    def min_row_sp(self,col_no):
        ''' Find the minimum available row number for the set column;
            this might not be the same as ROWNO of 'self.min_cell'
        '''
        f = '[MClient] db.DB.min_row_sp'
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
            sh.com.empty(f)

    def selection(self,pos):
        f = '[MClient] db.DB.selection'
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
            sh.com.empty(f)
            '''

    def skipped_dicas(self):
        f = '[MClient] db.DB.skipped_dicas'
        if self._articleid:
            self.dbc.execute ('select distinct DICA from BLOCKS \
                               where ARTICLEID = ? \
                               and (BLOCK = 1 or IGNORE = 1)'
                             ,(self._articleid,)
                             )
            result = self.dbc.fetchall()
            if result:
                return [item[0] for item in result]
        else:
            sh.com.empty(f)
    
    def blocked(self):
        f = '[MClient] db.DB.blocked'
        if self._articleid:
            self.dbc.execute ('select NO from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 1'
                             ,(self._articleid,)
                             )
            return self.dbc.fetchall()
        else:
            sh.com.empty(f)

    def prioritized(self):
        f = '[MClient] db.DB.prioritized'
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
            sh.com.empty(f)

    def dics(self,Block=False):
        f = '[MClient] db.DB.dics'
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
            sh.com.empty(f)

    def search_forward(self,pos,search):
        f = '[MClient] db.DB.search_forward'
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
            sh.com.empty(f)

    def search_backward(self,pos,search):
        f = '[MClient] db.DB.search_backward'
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
            sh.com.empty(f)

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
        f = '[MClient] db.DB.max_bboy'
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
            sh.com.empty(f)
    
    # Get any block with the maximal BBOX2
    def max_bbox(self,limit=0):
        f = '[MClient] db.DB.max_bbox'
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
            sh.com.empty(f)
    
    # Get the minimum BBOY1 and the maximum BBOY2 for the set row number
    def bboy_limits(self,row_no=0):
        f = '[MClient] db.DB.bboy_limits'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)
                          
    ''' Get the minimum BBOX1 and the maximum BBOX2 for the set column
        number
    '''
    def bbox_limits(self,col_no=0):
        f = '[MClient] db.DB.bbox_limits'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def min_articleid(self):
        f = '[MClient] db.DB.min_articleid'
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           order by ARTICLEID'
                         )
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.com.empty(f)
            # Default minimal autoincrement in SQlite
            return 1
            
    def max_articleid(self):
        f = '[MClient] db.DB.max_articleid'
        self.dbc.execute ('select ARTICLEID from ARTICLES \
                           order by ARTICLEID desc'
                         )
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.com.empty(f)
            # Default minimal autoincrement in SQlite
            return 1
    
    def block_pos_next(self,pos):
        f = '[MClient] db.DB.block_pos_next'
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
            sh.com.empty(f)
    
    def set_bookmark(self,pos=0):
        f = '[MClient] db.DB.set_bookmark'
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
                sh.com.empty(f)
        else:
            sh.log.append (f,_('WARNING')
                          ,_('Wrong input data!')
                          )
                          
    def delete_bookmarks(self):
        f = '[MClient] db.DB.delete_bookmarks'
        sh.log.append (f,_('DEBUG')
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
        f = '[MClient] db.Moves.start'
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
            sh.com.empty(f)

    def end(self):
        f = '[MClient] db.Moves.end'
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
            sh.com.empty(f)

    def line_start(self,pos):
        f = '[MClient] db.Moves.line_start'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def line_end(self,pos):
        f = '[MClient] db.Moves.line_end'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def left(self,pos):
        f = '[MClient] db.Moves.left'
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
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def right(self,pos):
        f = '[MClient] db.Moves.right'
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
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def up(self,pos):
        f = '[MClient] db.Moves.up'
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
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def down(self,pos):
        f = '[MClient] db.Moves.down'
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
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)

    def page_down(self,bboy,height):
        f = '[MClient] db.Moves.page_down'
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
            sh.com.empty(f)

    def page_up(self,bboy,height):
        f = '[MClient] db.Moves.page_up'
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
            sh.com.empty(f)
                          
    def first_section(self,col_no=0):
        f = '[MClient] db.Moves.first_section'
        if self._articleid:
            self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and COLNO = ? \
                               and POS1 < POS2 order by ROWNO,NO'
                             ,(self._articleid,col_no,)
                             )
            return self.dbc.fetchone()
        else:
            sh.com.empty(f)
                          
    def last_section(self,col_no=0):
        f = '[MClient] db.Moves.last_section'
        if self._articleid:
            self.dbc.execute ('select POS1,ROWNO,TEXT from BLOCKS \
                               where ARTICLEID = ? and BLOCK = 0 \
                               and IGNORE = 0 and COLNO = ? \
                               and POS1 < POS2 order by ROWNO desc,NO'
                             ,(self._articleid,col_no,)
                             )
            return self.dbc.fetchone()
        else:
            sh.com.empty(f)
    
    def next_section(self,pos,col_no=0,Loop=True):
        f = '[MClient] db.Moves.next_section'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)
                          
    def prev_section(self,pos,col_no=0,Loop=True):
        f = '[MClient] db.Moves.prev_section'
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
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def next_col(self,row_no=0,col_no=0):
        f = '[MClient] db.Moves.next_col'
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
            sh.com.empty(f)
