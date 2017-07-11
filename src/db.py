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
		self._source     = ''
		self._article_id = ''
		self.db          = sqlite3.connect(':memory:')
		self.dbc         = self.db.cursor()
		# We use integers instead of booleans; -1 means not set
		# Must indicate 'integer' fully before 'primary key autoincrement'
		self.dbc.execute (
		            'create table if not exists BLOCKS (\
		            NO                  integer primary key autoincrement    ,\
		            SOURCE              text                                 ,\
		            ARTICLEID           text                                 ,\
		            DICA                text                                 ,\
		            WFORMA              text                                 ,\
		            SPEECHA             text                                 ,\
		            TRANSCA             text                                 ,\
		            TERMA               text                                 ,\
		            TYPE                text                                 ,\
		            TEXT                text                                 ,\
		            URL                 text                                 ,\
		            BLOCK               integer                              ,\
		            PRIORITY            integer                              ,\
		            SELECTABLE          integer                              ,\
		            SAMECELL            integer                              ,\
		            CELLNO              integer                              ,\
		            ROWNO               integer                              ,\
		            COLNO               integer                              ,\
		            POS1                integer                              ,\
		            POS2                integer\
		                                               )'
		                 )

	def fill(self,data):
		self.dbc.executemany('insert into BLOCKS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)

	def sort(self,Fetch=True):
		self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where BLOCK is NOT ? order by DICA,WFORMA,SPEECHA,TERMA,CELLNO,NO',(1,))
		if Fetch:
			return self.dbc.fetchall()
			
	def request(self,source,article_id):
		if source and article_id:
			self._source     = source
			self._article_id = article_id
		else:
			sg.Message('DB.request',sh.lev_warn,sh.globs['mes'].empty_input)
	
	def print(self,Selected=False,Shorten=False,MaxHeader=10,MaxRow=20,MaxRows=20):
		# 'self.dbc.description' is 'None' without performing 'select' first
		if not Selected:
			self.dbc.execute('select * from BLOCKS order by NO')
		headers = [cn[0] for cn in self.dbc.description]
		rows    = self.dbc.fetchall()
		sh.Table (
		            headers             = headers                             ,
		            rows                = rows                                ,
		            Shorten             = Shorten                             ,
		            MaxHeader           = MaxHeader                           ,
		            MaxRow              = MaxRow                              ,
		            MaxRows             = MaxRows
		         ).print()

	def get_cell(self,pos): # Selectable
		# todo: limit by SOURCE, ARTICLEID
		#TEXT,CELLNO
		self.dbc.execute('select CELLNO from BLOCKS where POS1 <= ? and POS2 >= ?',(pos,pos))
		result = self.dbc.fetchall()
		if result and result[0]:
			result = result[0][0]
			sh.log.append('DB.get_cell',sh.lev_debug,'Cell #:%d' % result) # todo: mes
			self.dbc.execute('select POS1,POS2 from BLOCKS where CELLNO=?',(result,))
			return self.dbc.fetchone()
		else:
			return(0,0)

	def update(self,query):
		try:
			self.dbc.executescript(query)
		except sqlite3.OperationalError:
			sg.Message('DB.update',sh.lev_err,'Unable to execute:\n"%s"' % str(query))
			
	def nos(self,source,article_id):
		if self._source and self._article_id:
			self.dbc.execute('select NO from BLOCKS where SOURCE = ? and ARTICLEID = ? order by NO',(self._source,self._article_id))
			result = self.dbc.fetchall()
			if result:
				return [x[0] for x in result]
		else:
			sg.Message('DB.nos',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def nos_nb(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO from BLOCKS where SOURCE = ? and ARTICLEID = ? and BLOCK IS NOT ? order by NO',(self._source,self._article_id,1,))
			result = self.dbc.fetchall()
			if result:
				return [x[0] for x in result]
		else:
			sg.Message('DB.nos_nb',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for BlockPrioritize
	def assign_bp(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO,TYPE,DICA from BLOCKS where SOURCE = ? and ARTICLEID = ? order by NO',(self._source,self._article_id))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_bp',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for Cells
	def assign_cells(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where SOURCE = ? and ARTICLEID = ? and BLOCK is not ? order by NO',(self._source,self._article_id,1,))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_cells',sh.lev_warn,sh.globs['mes'].empty_input)



if __name__ == '__main__':
	import re
	import html
	import time
	import tags as tg
	import elems as el
	import mclient as mc
	
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/star_test').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/sampling.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/test.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/do.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/filter_get').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/добро пожаловать.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/добро.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/рабочая документация.txt').get()
	text = sh.ReadTextFile(file='/home/pete/tmp/ars/martyr.txt').get()

	text = text.replace('\r','')
	text = text.replace('\n','')
	text = text.replace(' <','<')
	text = text.replace('> ','>')
	text = text.replace(sh.nbspace+'<','<')
	text = text.replace('>'+sh.nbspace,'>')

	text = text.replace('>; <','><')
	text = text.replace('> <','><')

	try:
		text = html.unescape(text)
	except:
		sh.log.append('Page.decode_entities',sh.lev_err,sh.globs['mes'].html_conversion_failure)
		
	# An excessive space must be removed after unescaping the page
	text = re.sub(r'\>[\s]{0,1}\<','><',text)

	mc.ConfigMclient ()

	start_time = time.time()
	cur_start  = time.time()
	
	tags = tg.Tags(text)
	tags.run()
	
	sh.log.append('tags',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	cur_start  = time.time()
	
	elems = el.Elems(blocks=tags._blocks)
	elems.run()
	
	sh.log.append('elems',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	
	cur_start  = time.time()
	data = elems.dump()
	sh.log.append('elems: fill + dump',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	
	db = DB()
	cur_start  = time.time()
	db.fill(data)
	db.sort()
	sh.log.append('db.fill, db.sort',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	db.dbc.execute('select TERMA,TYPE,TEXT,SELECTABLE,SAMECELL,CELLNO from BLOCKS')
	db.print(Selected=1)
