#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' We need 'POS1 < POS2' to skip empty blocks; POS1 = POS2 causes
    Moves to work incorrectly.
'''

import sqlite3
import skl_shared.shared as sh
from skl_shared.localize import _


class DB:
    ''' #NOTE: don't forget to change 'self.Selectable' and 'self.cols'
        externally.
    '''
    def __init__(self):
        self.set_values()
        self.reset()
        self.db = sqlite3.connect(':memory:')
        self.dbc = self.db.cursor()
        self.create_blocks()
        self.create_articles()
    
    def update_phterm(self):
        f = '[MClient] db.DB.update_phterm'
        if self.artid:
            query = 'update BLOCKS set TERM = ? where ARTICLEID = ?'
            self.dbc.execute(query,('',self.artid,))
        else:
            sh.com.rep_empty(f)
    
    def unblock(self):
        self.dbc.execute('update BLOCKS set BLOCK = 0')
    
    def unprioritize(self):
        self.dbc.execute('update BLOCKS set DICPR = 0')
    
    def get_skipped_terms(self):
        f = '[MClient] db.DB.get_skipped_terms'
        if self.artid:
            query = 'select distinct TERM from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 1 order by TERM'
            self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchall()
            if result:
                return [item[0] for item in result]
        else:
            sh.com.rep_empty(f)
    
    def print_custom(self,maxrow=40,maxrows=1000):
        ''' This allows to quickly debug only needed fields.
            The procedure is orphaned so any fields can be selected.
        '''
        f = '[MClient] db.DB.print_custom'
        query = 'select NO,TYPE,TEXT,DIC,SPEECH,SPEECHPR from BLOCKS \
                 order by CELLNO,NO'
        self.dbc.execute(query)
        rows = self.dbc.fetchall()
        headers = ('NO','TYPE','TEXT','DIC','SPEECH','SPEECHPR')
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ,Transpose = True
                           ).run()
        sh.com.run_fast_debug(f,mes)
    
    def get_wform(self,pos):
        f = '[MClient] db.DB.get_wform'
        if self.artid:
            query = 'select WFORM from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 <= ? \
                     and POS2 > ?'
            self.dbc.execute(query,(self.artid,pos,pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)
    
    def get_next_dic(self,pos,dic):
        f = '[MClient] db.DB.get_next_dic'
        if self.artid:
            query = 'select DIC,DICF,NO,CELLNO from BLOCKS \
                     where ARTICLEID = ? and POS1 > ? and not DIC = ? \
                     and not DICF = ? and BLOCK = 0 and IGNORE = 0 \
                     order by CELLNO,NO'
            self.dbc.execute(query,(self.artid,pos,dic,dic,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    def get_prev_dic(self,pos,dic):
        f = '[MClient] db.DB.prev_dic'
        if self.artid:
            query = 'select DIC,DICF,NO,CELLNO from BLOCKS \
                     where ARTICLEID = ? and POS1 < ? and not DIC = ? \
                     and not DICF = ? and BLOCK = 0 and IGNORE = 0 \
                     order by CELLNO desc,NO desc'
            self.dbc.execute(query,(self.artid,pos,dic,dic,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
        
    def create_blocks(self):
        ''' We use integers instead of booleans; -1 means not set.
            Must indicate 'integer' fully before 'primary key 
            autoincrement'.
            31 columns for now.
        '''
        query = 'create table if not exists BLOCKS (\
                 NO         integer primary key autoincrement \
                ,ARTICLEID  integer \
                ,DIC        text    \
                ,WFORM      text    \
                ,SPEECH     text    \
                ,TRANSC     text    \
                ,TERM       text    \
                ,TYPE       text    \
                ,TEXT       text    \
                ,URL        text    \
                ,BLOCK      integer \
                ,DICPR      integer \
                ,SELECTABLE integer \
                ,SAMECELL   integer \
                ,CELLNO     integer \
                ,ROWNO      integer \
                ,COLNO      integer \
                ,POS1       integer \
                ,POS2       integer \
                ,NODE1      text    \
                ,NODE2      text    \
                ,OFFPOS1    integer \
                ,OFFPOS2    integer \
                ,BBOX1      integer \
                ,BBOX2      integer \
                ,BBOY1      integer \
                ,BBOY2      integer \
                ,TEXTLOW    text    \
                ,IGNORE     integer \
                ,SPEECHPR   integer \
                ,DICF       text    \
                                                   )'
        self.dbc.execute(query)
                         
    def create_articles(self):
        # 7 columns for now
        query = 'create table if not exists ARTICLES (\
                 ARTICLEID integer primary key autoincrement \
                ,SOURCE    text    \
                ,TITLE     text    \
                ,URL       text    \
                ,LANG1     text    \
                ,LANG2     text    \
                ,BOOKMARK  integer \
                                                     )'
        self.dbc.execute(query)

    def reset (self,cols=('dic','wform','transc','speech')
              ,SortRows=False,SortTerms=False,ExpandDic=False
              ,ShowUsers=False
              ):
        f = '[MClient] db.DB.reset'
        self.cols = cols
        self.ExpandDic = ExpandDic
        self.SortRows = SortRows
        self.SortTerms = SortTerms
        self.ShowUsers = ShowUsers
        
        # Prevents None + tuple
        if not self.cols:
            self.cols = ('dic','wform','transc','speech')
            sh.com.rep_empty(f)
        #NOTE: do not forget to add new block types here
        self.types = self.cols + ('term','phrase','comment'
                                 ,'correction','definition'
                                 )
        if self.ShowUsers:
            self.types += ('user',)

    def fill_blocks(self,data):
        query = 'insert into BLOCKS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?\
                                           ,?,?,?,?,?,?,?,?,?,?,?,?,?,?\
                                           ,?,?,?)'
        self.dbc.executemany(query,data)
        
    def fill_articles(self,data):
        query = 'insert into ARTICLES values (?,?,?,?,?,?,?)'
        self.dbc.execute(query,data)

    def fetch(self):
        query = 'select TYPE,TEXT,ROWNO,COLNO from BLOCKS \
                 where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                 order by CELLNO,NO'
        self.dbc.execute(query,(self.artid,))
        return self.dbc.fetchall()

    def is_present(self,source,title,url):
        ''' We also need to pass URL in case History has two phrase
            dictionary titles of the same name.
            URL will be empty for local dictionaries so we need to pass
            TITLE as well.
            #NOTE: add LANG1 and LANG2 when pairs are enabled for local
            dictionaries.
        '''
        query = 'select ARTICLEID from ARTICLES where URL = ? \
                 and SOURCE = ? and TITLE = ?'
        self.dbc.execute(query,(url,source,title,))
        result = self.dbc.fetchone()
        if result:
            return result[0]

    def get_searches(self):
        query = 'select distinct ARTICLEID,TITLE from ARTICLES \
                 order by ARTICLEID desc'
        self.dbc.execute(query)
        return self.dbc.fetchall()

    def get_prev_id(self,Loop=True):
        f = '[MClient] db.DB.get_prev_id'
        if self.artid:
            query = 'select ARTICLEID from ARTICLES where ARTICLEID < ?\
                     order by ARTICLEID desc'
            self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
            elif Loop:
                return self.get_max_artid()
        else:
            sh.com.rep_empty(f)

    def get_next_id(self,Loop=True):
        f = '[MClient] db.DB.get_next_id'
        if self.artid:
            query = 'select ARTICLEID from ARTICLES where ARTICLEID > ?\
                     order by ARTICLEID'
            self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
            elif Loop:
                return self.get_min_artid()
        else:
            sh.com.rep_empty(f)

    def print (self,Selected=False
              ,mode='BLOCKS',maxrow=10
              ,maxrows=1000
              ):
        ''' 'self.dbc.description' is 'None' without performing
            'select' first
        '''
        f = '[MClient] db.DB.print'
        if not Selected:
            if mode == 'BLOCKS':
                query = 'select * from BLOCKS order by CELLNO,NO'
                self.dbc.execute(query)
            elif mode == 'ARTICLES':
                query = 'select * from ARTICLES order by ARTICLEID'
                self.dbc.execute(query)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(mode,'ARTICLES, BLOCKS')
                sh.objs.get_mes(f,mes).show_error()
        headers = [cn[0] for cn in self.dbc.description]
        rows = self.dbc.fetchall()
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ,Transpose = True
                           ).run()
        sh.com.run_fast_debug(f,mes)

    def update(self,query):
        f = '[MClient] db.DB.update'
        try:
            self.dbc.executescript(query)
        except sqlite3.OperationalError:
            sub = str(query).replace(';',';\n')
            mes = _('Unable to execute:\n"{}"').format(sub)
            sh.objs.get_mes(f,mes).show_error()

    # Assign input data for BlockPrioritize
    def assign_bp(self):
        f = '[MClient] db.DB.assign_bp'
        if self.artid:
            query = 'select NO,TYPE,TEXT'
            if self.ExpandDic:
                query += ',DICF'
            else:
                query += ',DIC'
            query += ',SPEECH from BLOCKS where ARTICLEID = ? \
                       order by NO'
            
            self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchall()
        else:
            sh.com.rep_empty(f)

    def order_query(self):
        f = '[MClient] db.DB.order_query'
        query = []
        for item in self.cols:
            if item == 'dic':
                query.append('DICPR desc')
                #TODO: Is sorting by DICPR is enough here?
                ''' Full and short dictionary titles can be
                    sorted differently, for example, in case of
                    'файл.расшир.' -> 'Расширение файла'
                '''
                if self.ExpandDic:
                    query.append('LOWER(DICF)')
                else:
                    query.append('LOWER(DIC)')
            elif item == 'wform':
                query.append('WFORM')
            elif item == 'speech':
                query.append('SPEECHPR')
            elif item == 'transc':
                # Sorting by transcription is useless
                pass
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(item,'dic, wform, speech, transc')
                sh.objs.get_mes(f,mes).show_error()
        if self.SortTerms:
            query.append('TERM')
        return ','.join(query)

    # Assign input data for Cells
    def assign_cells(self):
        f = '[MClient] db.DB.assign_cells'
        if self.artid:
            query = 'select NO,TYPE,TEXT,SAMECELL,'
            if self.ExpandDic:
                query += 'DICF,'
            else:
                query += 'DIC,'
            query += 'WFORM,SPEECH,SPEECHPR,TRANSC from BLOCKS \
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
            #FIX: this will not work for Cyrillic
            query += ' collate nocase'
            self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchall()
        else:
            sh.com.rep_empty(f)

    # Assign input data for Pos
    def assign_pos(self):
        f = '[MClient] db.DB.assign_pos'
        if self.artid:
            query = 'select NO,TYPE,TEXT,SAMECELL,ROWNO from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                     order by CELLNO,NO'
            self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchall()
        else:
            sh.com.rep_empty(f)
                          
    def get_phdic(self):
        f = '[MClient] db.DB.get_phdic'
        if self.artid:
            query = 'select TEXT,POS1,URL from BLOCKS \
                     where ARTICLEID = ? and TYPE = ?'
            self.dbc.execute(query,(self.artid,'phdic',))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def clear(self):
        f = '[MClient] db.DB.clear'
        mes = _('Delete all records from {}').format('ARTICLES, BLOCKS')
        sh.objs.get_mes(f,mes,True).show_warning()
        # VACUUM command is a no-op for in-memory databases
        self.dbc.execute('delete from BLOCKS')
        self.dbc.execute('delete from ARTICLES')

    def clear_cur(self):
        f = '[MClient] db.DB.clear_cur'
        if self.artid:
            mes = _('Delete records of article No. {} from {}')
            mes = mes.format(self.artid,'BLOCKS, ARTICLES')
            sh.objs.get_mes(f,mes,True).show_warning()
            query = 'delete from BLOCKS where ARTICLEID = ?'
            self.dbc.execute(query,(self.artid,))
            query = 'delete from ARTICLES where ARTICLEID = ?'
            self.dbc.execute(query,(self.artid,))
        else:
            sh.com.rep_empty(f)

    def get_block_pos(self,pos):
        f = '[MClient] db.DB.get_block_pos'
        if self.artid:
            if self.Selectable:
                ''' 'POS2 > pos' instead of 'POS2 >= pos' allows to
                    correctly navigate through blocks where separate
                    words have been found
                '''
                query = 'select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT \
                        ,SELECTABLE,TYPE from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 <= ? and POS2 > ? \
                         and POS1 < POS2 and SELECTABLE = 1'
                self.dbc.execute(query,(self.artid,pos,pos,))
            else:
                query = 'select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT \
                               ,SELECTABLE,TYPE from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 <= ? and POS2 > ? \
                         and POS1 < POS2'
                self.dbc.execute(query,(self.artid,pos,pos,))
            return self.dbc.fetchone()
        # Too frequent, especially on the Welcome screen
        #else:
        #    sh.com.rep_empty(f)

    def get_article(self):
        f = '[MClient] db.DB.get_article'
        if self.artid:
            query = 'select SOURCE,TITLE,URL,BOOKMARK,LANG1,LANG2 \
                     from ARTICLES where ARTICLEID = ?'
            self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_url(self,pos):
        f = '[MClient] db.DB.get_url'
        if self.artid:
            query = 'select URL from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 <= ? \
                     and POS2 > ?'
            self.dbc.execute(query,(self.artid,pos,pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def get_text(self,pos):
        f = '[MClient] db.DB.get_text'
        if self.artid:
            query = 'select TEXT from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 <= ? \
                     and POS2 > ?'
            self.dbc.execute(query,(self.artid,pos,pos,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def get_min_cell(self):
        f = '[MClient] db.DB.get_min_cell'
        if self.artid:
            if self.Selectable:
                ''' This function is made for calculating moves;
                    if we don't take into account types, the first
                    selectable cell may not be reached
                    (e.g., it has 'transc' type).
                    #NOTE: 'TYPE in ("term","phrase")' causes bugs.
                '''
                query = 'select CELLNO,NO,POS1 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and TYPE in (?,?) \
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select CELLNO,NO,POS1 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_max_cell(self):
        f = '[MClient] db.DB.get_max_cell'
        if self.artid:
            if self.Selectable:
                query = 'select CELLNO,NO,POS1,BBOX1,BBOX2 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and TYPE in (?,?) \
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by CELLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select CELLNO,NO,POS1,BBOX1,BBOX2 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by CELLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_max_row(self):
        ''' Find the maximum available row number for the whole table;
            this might not be the same as ROWNO of 'self.max_cell'
        '''
        f = '[MClient] db.DB.get_max_row'
        if self.artid:
            if self.Selectable:
                query = 'select ROWNO,NO from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and TYPE in (?,?) \
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by ROWNO desc'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select ROWNO,NO from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by ROWNO desc'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_max_col(self):
        ''' Find the maximum available column number for the whole
            table; this might not be the same as COLNO of
            'self.get_max_cell'
        '''
        f = '[MClient] db.DB.get_max_col'
        if self.artid:
            if self.Selectable:
                query = 'select COLNO,NO,BBOX2 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and TYPE in (?,?) \
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by COLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select COLNO,NO,BBOX2 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by COLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    # Find the maximum available row number for the set column
    def get_max_row_sp(self,col_no):
        f = '[MClient] db.DB.get_max_row_sp'
        if self.artid:
            if self.Selectable:
                query = 'select ROWNO,NO from BLOCKS where COLNO = ? \
                         and ARTICLEID = ? and BLOCK = 0 and IGNORE = 0\
                         and TYPE in (?,?) and SELECTABLE = 1 \
                         and POS1 < POS2 order by ROWNO desc,NO desc'
                self.dbc.execute (query,(col_no,self.artid,'term'
                                        ,'phrase',
                                        )
                                 )
            else:
                query = 'select ROWNO,NO from BLOCKS where COLNO = ? \
                         and ARTICLEID = ? and BLOCK = 0 and IGNORE = 0\
                         and POS1 < POS2 order by ROWNO desc,NO desc'
                self.dbc.execute(query,(col_no,self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_min_col(self):
        ''' Find the minimum available column number for the whole
            table; this should be the same as COLNO of 'self.min_cell'
            but we leave it for non-standard tables.
        '''
        f = '[MClient] db.DB.get_min_col'
        if self.artid:
            if self.Selectable:
                query = 'select COLNO,NO,BBOX1 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and TYPE in (?,?) \
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by COLNO,NO'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select COLNO,NO,BBOX1 from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by COLNO,NO'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_min_row_sp(self,col_no):
        ''' Find the minimum available row number for the set column;
            this might not be the same as ROWNO of 'self.min_cell'
        '''
        f = '[MClient] db.DB.get_min_row_sp'
        if self.artid:
            if self.Selectable:
                query = 'select ROWNO,NO from BLOCKS where COLNO = ? \
                         and ARTICLEID = ? and BLOCK = 0 and IGNORE = 0\
                         and TYPE in (?,?) and SELECTABLE = 1 \
                         and POS1 < POS2 order by ROWNO,NO'
                self.dbc.execute (query,(col_no,self.artid,'term'
                                        ,'phrase',
                                        )
                                 )
            else:
                query = 'select ROWNO,NO from BLOCKS where COLNO = ? \
                         and ARTICLEID = ? and BLOCK = 0 and IGNORE = 0\
                         and POS1 < POS2 order by ROWNO,NO'
                self.dbc.execute(query,(col_no,self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)

    def get_sel(self,pos):
        f = '[MClient] db.DB.get_sel'
        if self.artid:
            if self.Selectable:
                query = 'select NODE1,NODE2,OFFPOS1,OFFPOS2,BBOX1,BBOX2\
                               ,BBOY1,BBOY2,ROWNO from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and SELECTABLE = 1 \
                         and POS1 < POS2 and POS1 <= ? and POS2 >= ? \
                         order by COLNO,NO'
                self.dbc.execute(query,(self.artid,pos,pos,))
            else:
                query = 'select NODE1,NODE2,OFFPOS1,OFFPOS2,BBOX1,BBOY1\
                               ,BBOX2,BBOY2,ROWNO from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 and POS1 <= ? \
                         and POS2 >= ? order by COLNO,NO'
                self.dbc.execute(query,(self.artid,pos,pos,))
            return self.dbc.fetchone()
        else:
            pass
            '''
            # Too frequent
            sh.com.rep_empty(f)
            '''

    def get_skipped_dics(self):
        f = '[MClient] db.DB.get_skipped_dics'
        ''' #NOTE: Both DIC and TEXT can comprise several dic titles.
            Use 'mclient.Commands.get_skipped_dics' to split them.
        '''
        if self.artid:
            query = 'select distinct DICF from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 1'
            self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchall()
            if result:
                return [item[0] for item in result]
        else:
            sh.com.rep_empty(f)
    
    def get_blocked(self):
        f = '[MClient] db.DB.get_blocked'
        if self.artid:
            query = 'select NO from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 1'
            self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchall()
        else:
            sh.com.rep_empty(f)

    def get_prioritized(self):
        f = '[MClient] db.DB.get_prioritized'
        if self.artid:
            ''' #NOTE: We assume that 'Phrases' section has the priority
                of 999-1000 and it is always used despite user settings.
            '''
            query = 'select distinct DICF from BLOCKS \
                     where ARTICLEID = ? and DICPR > 0 and DICPR < 999 \
                     order by DICPR'
            self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchall()
            if result:
                return [item[0] for item in result]
        else:
            sh.com.rep_empty(f)

    def get_dics(self,Block=False):
        f = '[MClient] db.DB.get_dics'
        if self.artid:
            # Do not use 'POS1 < POS2', it might be not set yet
            if Block:
                query = 'select distinct DICF from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0'
                self.dbc.execute(query,(self.artid,))
            else:
                query = 'select distinct DICF from BLOCKS \
                         where ARTICLEID = ?'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchall()
        else:
            sh.com.rep_empty(f)

    def search_next(self,pos,search):
        f = '[MClient] db.DB.search_next'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and TEXTLOW like ? \
                         and POS1 > ? order by CELLNO,NO'
                self.dbc.execute (query,(self.artid,'term','phrase'
                                        ,'%' + search + '%',pos,
                                        )
                                 )
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 \
                         and TEXTLOW like ? and POS1 > ? \
                         order by CELLNO,NO'
                self.dbc.execute (query,(self.artid
                                        ,'%' + search + '%',pos,
                                        )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def search_prev(self,pos,search):
        f = '[MClient] db.DB.search_prev'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and TEXTLOW like ? \
                         and POS2 < ? order by CELLNO desc,NO desc'
                self.dbc.execute (query,(self.artid,'term','phrase'
                                        ,'%' + search + '%',pos,
                                        )
                                 )
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TEXTLOW \
                         like ? and POS2 < ? order by CELLNO desc \
                        ,NO desc'
                self.dbc.execute (query,(self.artid,'%' + search + '%'
                                        ,pos,
                                        )
                                 )
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def unignore(self):
        query = 'update BLOCKS set IGNORE = 0 where ARTICLEID = ?'
        self.dbc.execute(query,(self.artid,))

    def ignore(self):
        query = 'update BLOCKS set IGNORE = 1 where ARTICLEID = ? \
                 and TYPE not in %s'
        self.dbc.execute(query % (self.types,),(self.artid,))
        if 'dic' not in self.types:
            query = 'update BLOCKS set IGNORE = 1 where ARTICLEID = ? \
                     and TYPE = ?'
            self.dbc.execute(query,(self.artid,'phrase',))
            
    # Get any block with the maximal BBOY2
    def get_max_bboy(self,limit=0):
        f = '[MClient] db.DB.get_max_bboy'
        if self.artid:
            if limit:
                query = 'select BBOY2,NODE1,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 and BBOY2 < ? \
                         order by BBOY2 desc'
                self.dbc.execute(query,(self.artid,limit,))
            else:
                query = 'select BBOY2,NODE1,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by BBOY2 desc'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    # Get any block with the maximal BBOX2
    def get_max_bbox(self,limit=0):
        f = '[MClient] db.DB.get_max_bbox'
        if self.artid:
            if limit:
                query = 'select BBOX2,NODE1,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 and BBOX2 < ? \
                         order by BBOX2 desc'
                self.dbc.execute(query,(self.artid,limit,))
            else:
                query = 'select BBOX2,NODE1,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and POS1 < POS2 \
                         order by BBOX2 desc'
                self.dbc.execute(query,(self.artid,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    # Get the minimum BBOY1 and the maximum BBOY2 for the set row number
    def get_bboy_limits(self,row_no=0):
        f = '[MClient] db.DB.get_bboy_limits'
        if self.artid:
            query = 'select BBOY1 from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                     and ROWNO = ? order by BBOY1'
            self.dbc.execute(query,(self.artid,row_no,))
            min_result = self.dbc.fetchone()
            query = 'select BBOY2 from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                     and ROWNO = ? order by BBOY2 desc'
            self.dbc.execute(query,(self.artid,row_no,))
            max_result = self.dbc.fetchone()
            if min_result and max_result:
                return(min_result[0],max_result[0])
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
                          
    def get_bbox_limits(self,col_no=0):
        ''' Get the minimum BBOX1 and the maximum BBOX2 for
            the set column number.
        '''
        f = '[MClient] db.DB.get_bbox_limits'
        if self.artid:
            query = 'select BBOX1 from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                     and COLNO = ? order by BBOX1'
            self.dbc.execute(query,(self.artid,col_no,))
            min_result = self.dbc.fetchone()
            query = 'select BBOX2 from BLOCKS where ARTICLEID = ? \
                     and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                     and COLNO = ? order by BBOX2 desc'
            self.dbc.execute(query,(self.artid,col_no,))
            max_result = self.dbc.fetchone()
            if min_result and max_result:
                return(min_result[0],max_result[0])
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_min_artid(self):
        f = '[MClient] db.DB.get_min_artid'
        query = 'select ARTICLEID from ARTICLES order by ARTICLEID'
        self.dbc.execute(query)
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.com.rep_empty(f)
            # Default minimal autoincrement in SQlite
            return 1
            
    def get_max_artid(self):
        f = '[MClient] db.DB.get_max_artid'
        query = 'select ARTICLEID from ARTICLES order by ARTICLEID desc'
        self.dbc.execute(query)
        result = self.dbc.fetchone()
        if result:
            return result[0]
        else:
            sh.com.rep_empty(f)
            # Default minimal autoincrement in SQlite
            return 1
    
    def get_next_block_pos(self,pos):
        f = '[MClient] db.DB.get_next_block_pos'
        if self.artid:
            if self.Selectable:
                ''' 'POS2 > pos' instead of 'POS2 >= pos' allows to
                    correctly navigate through blocks where separate
                    words have been found
                '''
                query = 'select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT \
                        ,SELECTABLE from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and POS1 >= ? and POS1 < POS2 \
                         and SELECTABLE = 1 order by CELLNO,NO'
                self.dbc.execute (query,(self.artid,'term','phrase',pos
                                        ,
                                        )
                                 )
            else:
                query = 'select POS1,POS2,CELLNO,ROWNO,COLNO,NO,TEXT \
                        ,SELECTABLE from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and POS1 >= ? \
                         and POS1 < POS2 order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,pos,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    def set_bookmark(self,pos=0):
        f = '[MClient] db.DB.set_bookmark'
        if str(pos).isdigit():
            if self.artid:
                ''' # Too frequent
                    mes = _('Set bookmark {} for article #{}')
                    mes = mes.format(pos,self.artid)
                    sh.objs.get_mes(f,mes,True).show_debug()
                '''
                query = 'update ARTICLES set BOOKMARK = ? \
                         where ARTICLEID = ?'
                self.dbc.execute(query,(pos,self.artid,))
            else:
                sh.com.rep_empty(f)
        else:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes,True).show_warning()
                          
    def delete_bookmarks(self):
        f = '[MClient] db.DB.delete_bookmarks'
        mes = _('Delete bookmarks for all articles')
        sh.objs.get_mes(f,mes,True).show_debug()
        self.dbc.execute('update ARTICLES set BOOKMARK = -1')
        
    def unprioritize_speech(self):
        self.dbc.execute('update BLOCKS set SPEECHPR = 0')



# Separating this class will slow down the program for ~0,027s.
class Moves(DB):

    def __init__(self):
        super().__init__()

    def get_start(self):
        f = '[MClient] db.Moves.get_start'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                         order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def get_end(self):
        f = '[MClient] db.Moves.get_end'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and POS1 < POS2 \
                         order by CELLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,'term','phrase',))
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                         order by CELLNO desc,NO desc'
                self.dbc.execute(query,(self.artid,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def get_line_start(self,pos):
        f = '[MClient] db.Moves.get_line_start'
        if self.artid:
            poses = self.get_block_pos(pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    query = 'select POS1 from BLOCKS \
                             where ARTICLEID = ? and BLOCK = 0 \
                             and IGNORE = 0 and TYPE in (?,?) \
                             and SELECTABLE = 1 and ROWNO = ? \
                             and COLNO <= ? and POS1 < POS2 \
                             order by COLNO,NO'
                    self.dbc.execute (query,(self.artid,'term','phrase'
                                            ,row_no,col_no,
                                            )
                                     )
                else:
                    query = 'select POS1 from BLOCKS \
                             where ARTICLEID = ? and BLOCK = 0 \
                             and IGNORE = 0 and ROWNO = ? \
                             and COLNO <= ? and POS1 < POS2 \
                             order by COLNO,NO'
                    self.dbc.execute(query,(self.artid,row_no,col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_line_end(self,pos):
        f = '[MClient] db.Moves.get_line_end'
        if self.artid:
            poses = self.get_block_pos(pos=pos)
            if poses:
                row_no, col_no = poses[3], poses[4]
                if self.Selectable:
                    query = 'select POS1 from BLOCKS \
                             where ARTICLEID = ? and BLOCK = 0 \
                             and IGNORE = 0 and TYPE in (?,?) \
                             and SELECTABLE = 1 and ROWNO = ? \
                             and COLNO >= ? and POS1 < POS2 \
                             order by COLNO desc,NO desc'
                    self.dbc.execute (query,(self.artid,'term','phrase'
                                            ,row_no,col_no,
                                            )
                                     )
                else:
                    query = 'select POS1 from BLOCKS \
                             where ARTICLEID = ? and BLOCK = 0 \
                             and IGNORE = 0 and ROWNO = ? \
                             and COLNO >= ? and POS1 < POS2 \
                             order by COLNO desc,NO desc'
                    self.dbc.execute(query,(self.artid,row_no,col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result[0]
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_left(self,pos):
        f = '[MClient] db.Moves.get_left'
        if self.artid:
            poses = self.get_block_pos(pos=pos)
            if poses:
                cellno, no = poses[2], poses[5]
                min_cell = self.get_min_cell()
                max_cell = self.get_max_cell()
                if min_cell and max_cell:
                    if no == min_cell[1]:
                        return max_cell[2]
                    elif self.Selectable:
                        query = 'select POS1 from BLOCKS \
                                 where ARTICLEID = ? and BLOCK = 0 \
                                 and IGNORE = 0 and TYPE in (?,?) \
                                 and SELECTABLE = 1 and CELLNO <= ? \
                                 and POS1 < ? and POS1 < POS2 \
                                 order by CELLNO desc,NO desc'
                        self.dbc.execute (query,(self.artid,'term'
                                                ,'phrase',cellno,pos,
                                                )
                                         )
                    else:
                        query = 'select POS1 from BLOCKS \
                                 where ARTICLEID = ? and BLOCK = 0 \
                                 and IGNORE = 0 and CELLNO <= ? \
                                 and POS1 < ? and POS1 < POS2 \
                                 order by CELLNO desc,NO desc'
                        self.dbc.execute(query,(self.artid,cellno,pos,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_right(self,pos):
        f = '[MClient] db.Moves.get_right'
        if self.artid:
            poses = self.get_block_pos(pos=pos)
            if poses:
                cellno, no = poses[2], poses[5]
                max_cell = self.get_max_cell()
                min_cell = self.get_min_cell()
                if min_cell and max_cell:
                    if no == max_cell[1]:
                        # Loop moves
                        return min_cell[2]
                    elif self.Selectable:
                        query = 'select POS1 from BLOCKS \
                                 where ARTICLEID = ? and BLOCK = 0 \
                                 and IGNORE = 0 and TYPE in (?,?) \
                                 and SELECTABLE = 1 and CELLNO >= ? \
                                 and POS1 > ? and POS1 < POS2 \
                                 order by CELLNO,NO'
                        self.dbc.execute (query,(self.artid,'term'
                                                ,'phrase',cellno,pos,
                                                )
                                         )
                    else:
                        query = 'select POS1 from BLOCKS \
                                 where ARTICLEID = ? and BLOCK = 0 \
                                 and IGNORE = 0 and CELLNO >= ? \
                                 and POS1 > ? and POS1 < POS2 \
                                 order by CELLNO,NO'
                        self.dbc.execute(query,(self.artid,cellno,pos,))
                    result = self.dbc.fetchone()
                    if result:
                        return result[0]
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_up(self,pos):
        f = '[MClient] db.Moves.get_up'
        if self.artid:
            poses = self.get_block_pos(pos)
            if poses:
                cellno = poses[2]
                row_no = poses[3]
                col_no = poses[4]
                no = poses[5]
                min_cell = self.get_min_cell()
                min_row_sp = self.get_min_row_sp(col_no=col_no)
                max_col = self.get_max_col()
                if min_cell and max_col and min_row_sp:
                    if no == min_cell[1]:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO = ? \
                                     and POS1 < POS2 \
                                     order by ROWNO desc,NO desc'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',max_col[0]
                                                    ,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO = ? \
                                     and POS1 < POS2 \
                                     order by ROWNO desc,NO desc'
                            self.dbc.execute (query,(self.artid
                                                    ,max_col[0]
                                                    ,
                                                    )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == min_row_sp[1]:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO < ? \
                                     and POS1 < POS2 \
                                     order by COLNO desc,ROWNO desc \
                                    ,NO desc'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',col_no
                                                    ,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO < ? \
                                     and POS1 < POS2 \
                                     order by COLNO desc,ROWNO desc \
                                    ,NO desc'
                            self.dbc.execute(query,(self.artid,col_no,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO = ? \
                                     and ROWNO <= ? and POS1 < ? \
                                     and POS1 < POS2 \
                                     order by ROWNO desc,NO desc'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',col_no
                                                    ,row_no,pos,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO = ? \
                                     and ROWNO <= ? and POS1 < ? \
                                     and POS1 < POS2 \
                                     order by ROWNO desc,NO desc'
                            self.dbc.execute (query,(self.artid,col_no
                                                    ,row_no,pos,
                                                    )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_down(self,pos):
        f = '[MClient] db.Moves.get_down'
        if self.artid:
            poses = self.get_block_pos(pos)
            if poses:
                cellno = poses[2]
                row_no = poses[3]
                col_no = poses[4]
                no = poses[5]
                min_col = self.get_min_col()
                max_row_sp = self.get_max_row_sp(col_no)
                max_col = self.get_max_col()

                if min_col and max_row_sp and max_col:
                    if row_no == max_row_sp[0] and col_no == max_col[0]:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO = ? \
                                     and POS1 < POS2 order by ROWNO,NO'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',min_col[0]
                                                    ,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO = ? \
                                     and POS1 < POS2 order by ROWNO,NO'
                            self.dbc.execute (query,(self.artid
                                                    ,min_col[0]
                                                    ,
                                                    )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    elif no == max_row_sp[1]:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO > ? \
                                     and POS1 < POS2 \
                                     order by COLNO,ROWNO,NO'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',col_no
                                                    ,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO > ? \
                                     and POS1 < POS2 \
                                     order by COLNO,ROWNO,NO'
                            self.dbc.execute(query,(self.artid,col_no,))
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                    else:
                        if self.Selectable:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and TYPE in (?,?) \
                                     and SELECTABLE = 1 and COLNO = ? \
                                     and ROWNO >= ? and POS1 > ? \
                                     and POS1 < POS2 order by ROWNO,NO'
                            self.dbc.execute (query,(self.artid,'term'
                                                    ,'phrase',col_no
                                                    ,row_no,pos
                                                    ,
                                                    )
                                             )
                        else:
                            query = 'select POS1 from BLOCKS \
                                     where ARTICLEID = ? and BLOCK = 0 \
                                     and IGNORE = 0 and COLNO = ? \
                                     and ROWNO >= ? and POS1 > ? \
                                     and POS1 < POS2 order by ROWNO,NO'
                            self.dbc.execute (query,(self.artid,col_no
                                                    ,row_no,pos
                                                    ,
                                                    )
                                             )
                        result = self.dbc.fetchone()
                        if result:
                            return result[0]
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)

    def get_page_down(self,bboy,height):
        f = '[MClient] db.Moves.get_page_down'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and POS1 < POS2 \
                         and BBOY1 >= ? order by CELLNO,NO'
                value = int(bboy / height) * height + height
                self.dbc.execute (query,(self.artid,'term','phrase'
                                        ,value
                                        ,
                                 )
                                 )
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                         and BBOY1 >= ? order by CELLNO,NO'
                value = int(bboy / height) * height + height
                self.dbc.execute(query,(self.artid,value,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)

    def get_page_up(self,bboy,height):
        f = '[MClient] db.Moves.get_page_up'
        if self.artid:
            if self.Selectable:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and TYPE in (?,?)\
                         and SELECTABLE = 1 and POS1 < POS2 \
                         and BBOY1 >= ? order by CELLNO,NO'
                value = int(bboy / height) * height - height
                self.dbc.execute (query,(self.artid,'term','phrase'
                                        ,value
                                        ,
                                        )
                                 )
            else:
                query = 'select POS1 from BLOCKS where ARTICLEID = ? \
                         and BLOCK = 0 and IGNORE = 0 and POS1 < POS2 \
                         and BBOY1 >= ? order by CELLNO,NO'
                value = int(bboy / height) * height - height
                self.dbc.execute(query,(self.artid,value,))
            result = self.dbc.fetchone()
            if result:
                return result[0]
        else:
            sh.com.rep_empty(f)
                          
    def get_first_section(self,col_no=0):
        f = '[MClient] db.Moves.get_first_section'
        if self.artid:
            query = 'select POS1,ROWNO,TEXT from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                     and COLNO = ? and POS1 < POS2 order by ROWNO,NO'
            self.dbc.execute(query,(self.artid,col_no,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
                          
    def get_last_section(self,col_no=0):
        f = '[MClient] db.Moves.get_last_section'
        if self.artid:
            query = 'select POS1,ROWNO,TEXT from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                     and COLNO = ? and POS1 < POS2 \
                     order by ROWNO desc,NO'
            self.dbc.execute(query,(self.artid,col_no,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
    
    def get_next_section(self,pos,col_no=0,Loop=True):
        f = '[MClient] db.Moves.get_next_section'
        if self.artid:
            poses = self.get_block_pos(pos=pos)
            if poses:
                query = 'select POS1,ROWNO,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and ROWNO > ? and COLNO = ? \
                         and POS1 < POS2 order by CELLNO,NO'
                self.dbc.execute(query,(self.artid,poses[3],col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result
                elif Loop:
                    return self.get_first_section(col_no=col_no)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
                          
    def get_prev_section(self,pos,col_no=0,Loop=True):
        f = '[MClient] db.Moves.get_prev_section'
        if self.artid:
            poses = self.get_block_pos(pos)
            if poses:
                query = 'select POS1,ROWNO,TEXT from BLOCKS \
                         where ARTICLEID = ? and BLOCK = 0 \
                         and IGNORE = 0 and ROWNO < ? and COLNO = ? \
                         and POS1 < POS2 order by CELLNO desc,NO'
                self.dbc.execute(query,(self.artid,poses[3],col_no,))
                result = self.dbc.fetchone()
                if result:
                    return result
                elif Loop:
                    return self.get_last_section(col_no)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_next_col(self,row_no=0,col_no=0):
        f = '[MClient] db.Moves.get_next_col'
        if self.artid:
            query = 'select POS1,ROWNO,COLNO,TEXT from BLOCKS \
                     where ARTICLEID = ? and BLOCK = 0 and IGNORE = 0 \
                     and ROWNO = ? and COLNO >= ? and POS1 < POS2 \
                     order by CELLNO,NO'
            self.dbc.execute(query,(self.artid,row_no,col_no,))
            return self.dbc.fetchone()
        else:
            sh.com.rep_empty(f)
