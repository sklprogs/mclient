#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo:
    - DB.reset: reset TEXT for DIC, WFORM, SPEECH, TRANSC; reset BLOCK, PRIORITY, CELLNO, SELECTABLE, ROWNO, COLNO, POS1, POS2
'''

import sqlite3
import prettytable
import shared as sh
import sharedGUI as sg


class DB:
	
	def __init__(self):
		self._source = ''
		self._search = ''
		self.db      = sqlite3.connect(':memory:')
		self.dbc     = self.db.cursor()
		# We use integers instead of booleans; -1 means not set
		# Must indicate 'integer' fully before 'primary key autoincrement'
		self.dbc.execute (
		            'create table if not exists BLOCKS (\
		            NO          integer primary   \
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
		                                               )'
		                 )

	def fill(self,data):
		self.dbc.executemany('insert into BLOCKS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)

	def sort(self,Fetch=True):
		self.dbc.execute('select NO,DICA,WFORMA,SPEECHA,TERMA,TYPE,TEXT,SAMECELL,CELLNO,ROWNO,COLNO from BLOCKS where BLOCK is NOT ? order by CELLNO,NO',(1,)) # order by DICA,WFORMA,SPEECHA,TERMA,
		if Fetch:
			return self.dbc.fetchall()
			
	def fetch(self):
		self.dbc.execute('select TYPE,TEXT,ROWNO,COLNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 order by CELLNO,NO',(self._source,self._search,))
		return self.dbc.fetchall()
		
	def present(self):
		self.dbc.execute('select NO from BLOCKS where SOURCE = ? and SEARCH = ?',(self._source,self._search,))
		return self.dbc.fetchall()
		
	def searches(self):
		self.dbc.execute('select SEARCH from BLOCKS order by NO desc')
		result = self.dbc.fetchall()
		if result:
			return set([item[0] for item in result])
			
	def cur_nos(self,Block=True):
		if self._search:
			if Block:
				self.dbc.execute('select NO from BLOCKS where SEARCH = ? and BLOCK < 1 order by NO',(self._search,))
			else:
				self.dbc.execute('select NO from BLOCKS where SEARCH = ? order by NO',(self._search,))
			result = self.dbc.fetchall()
			if result:
				return(result[0][0],result[-1][0])
		else:
			sh.log.append('DB.prev_search',sh.lev_warn,sh.globs['mes'].empty_input)
	
	def prev_search(self):
		nos = self.cur_nos()
		if nos:
			self.dbc.execute('select SEARCH from BLOCKS where NO < ? and BLOCK < 1 order by NO desc',(nos[0],))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.prev_search',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def next_search(self):
		nos = self.cur_nos()
		if nos:
			self.dbc.execute('select SEARCH from BLOCKS where NO > ? and BLOCK < 1 order by NO',(nos[-1],))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.prev_search',sh.lev_warn,sh.globs['mes'].empty_input)

	def request(self,source,search):
		if source and search:
			self._source = source
			self._search = search
		else:
			sg.Message('DB.request',sh.lev_warn,sh.globs['mes'].empty_input)
	
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
			sg.Message('DB.update',sh.lev_err,'Unable to execute:\n"%s"' % str(query).replace(';',';\n'))
			
	# Assign input data for BlockPrioritize
	def assign_bp(self):
		if self._source and self._search:
			self.dbc.execute('select NO,TYPE,TEXT,DICA from BLOCKS where SOURCE = ? and SEARCH = ? order by NO',(self._source,self._search))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_bp',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for Cells
	def assign_cells(self):
		if self._source and self._search:
			self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 order by PRIORITY desc,DICA,WFORMA,SPEECHA,TERMA,NO',(self._source,self._search,))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_cells',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for Pos
	def assign_pos(self):
		if self._source and self._search:
			self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,ROWNO from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 order by ROWNO,COLNO,NO',(self._source,self._search,))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_pos',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def phrase_dic(self):
		if self._source and self._search:
			self.dbc.execute('select DICA from BLOCKS where SOURCE = ? and SEARCH = ? and TYPE = ? order by NO',(self._source,self._search,'phrase',))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sg.Message('DB.phrase_dic',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def clear(self):
		sh.log.append('DB.clear',sh.lev_warn,'Delete all records from BLOCKS') # todo: mes
		# VACUUM command is a no-op for in-memory databases
		self.dbc.execute('delete from BLOCKS')
		
	def clear_cur(self):
		nos = self.cur_nos(Block=0)
		if nos:
			sh.log.append('DB.clear_cur',sh.lev_warn,'Delete records %d-%d from BLOCKS' % (nos[0],nos[1])) # todo: mes
			# Sqlite does not warn about '? <= NO >= ?', but this does nothing
			self.dbc.execute('delete from BLOCKS where NO >= ? and NO <= ?',(nos[0],nos[1],))
		else:
			sh.log.append('DB.clear_cur',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def block_pos(self,pos,Selectable=False):
		if self._source and self._search:
			# We use strict 'POS2 > pos' because the range provided by 'Pos.gen_poses' is non-inclusive (just like in Tkinter)
			if Selectable:
				self.dbc.execute('select POS1,POS2,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 and POS1 <= ? and POS2 > ? and SELECTABLE = 1',(self._source,self._search,pos,pos,))
			else:
				self.dbc.execute('select POS1,POS2,TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 and POS1 <= ? and POS2 > ?',(self._source,self._search,pos,pos,))
			return self.dbc.fetchone()
		else:
			sh.log.append('DB.block_pos',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def urla(self):
		if self._source and self._search:
			self.dbc.execute('select URLA from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1',(self._source,self._search,))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.urla',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def url(self,pos):
		if self._source and self._search:
			self.dbc.execute('select URL from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 and POS1 <= ? and POS2 > ?',(self._source,self._search,pos,pos,))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.url',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def text(self,pos):
		if self._source and self._search:
			self.dbc.execute('select TEXT from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 and POS1 <= ? and POS2 > ?',(self._source,self._search,pos,pos,))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.text',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Get the first term to put a selection on
	def first_term(self):
		if self._source and self._search:
			self.dbc.execute('select POS1 from BLOCKS where SOURCE = ? and SEARCH = ? and BLOCK < 1 and (TYPE = ? or TYPE = ?) and SELECTABLE = 1 order by CELLNO,NO',(self._source,self._search,'term','phrase',))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sh.log.append('DB.first_term',sh.lev_warn,sh.globs['mes'].empty_input)



if __name__ == '__main__':
	import page    as pg
	import tags    as tg
	import elems   as el
	import cells   as cl
	import mclient as mc
	
	# Modifiable
	source     = 'Online'
	search     = 'рабочая документация'
	file       = '/home/pete/tmp/ars/рабочая документация.txt'
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
	
	elems = el.Elems(blocks=tags._blocks,source=source,search=search)
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
	cells = cl.Cells(data=data,collimit=collimit)
	cells.run()
	blocks_db.update(query=cells._query)

	'''
	data = blocks_db.assign_pos()
	pos = cl.Pos(data=data,raw_text='RAW_TEXT')
	pos.run()
	blocks_db.update(query=pos._query)
	'''
	
	blocks_db.print(Shorten=1,MaxRow=18,MaxRows=150)
