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
			
	def fetch(self):
		self.dbc.execute('select TYPE,TEXT,ROWNO,COLNO from BLOCKS where BLOCK is NOT ? order by CELLNO,NO',(1,))
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
			self.dbc.execute('select * from BLOCKS order by CELLNO,NO')
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
		if self._source and self._article_id:
			self.dbc.execute('select NO,CELLNO,TYPE,TEXT,POS1,POS2 from BLOCKS where SOURCE = ? and ARTICLEID = ? and BLOCK = 0 and POS1 <= ? and POS2 >= ?',(self._source,self._article_id,pos,pos,))
			result = self.dbc.fetchone()
			if result:
				#return(result[0],result[1])
				print('NO:\t\t',result[0])
				print('CELLNO:\t\t',result[1])
				print('TYPE:\t\t',result[2])
				print('TEXT:\t\t',result[3])
				print('Range:\t\t%d-%d' % (result[4],result[5]))
				return(result[4],result[5])
		else:
			sg.Message('DB.get_cell',sh.lev_warn,sh.globs['mes'].empty_input)

	def update(self,query):
		try:
			self.dbc.executescript(query)
		except sqlite3.OperationalError:
			sg.Message('DB.update',sh.lev_err,'Unable to execute:\n"%s"' % str(query).replace(';',';\n'))
			
	# Assign input data for BlockPrioritize
	def assign_bp(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO,TYPE,TEXT,DICA from BLOCKS where SOURCE = ? and ARTICLEID = ? order by NO',(self._source,self._article_id))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_bp',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for Cells
	def assign_cells(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where SOURCE = ? and ARTICLEID = ? and BLOCK is not ? order by PRIORITY desc,DICA,WFORMA,SPEECHA,TERMA,NO',(self._source,self._article_id,1,))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_cells',sh.lev_warn,sh.globs['mes'].empty_input)
			
	# Assign input data for Pos
	def assign_pos(self):
		if self._source and self._article_id:
			self.dbc.execute('select NO,TYPE,TEXT,SAMECELL,ROWNO from BLOCKS where SOURCE = ? and ARTICLEID = ? and BLOCK is not ? order by ROWNO,COLNO,NO',(self._source,self._article_id,1,))
			return self.dbc.fetchall()
		else:
			sg.Message('DB.assign_pos',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def phrase_dic(self):
		if self._source and self._article_id:
			self.dbc.execute('select DICA from BLOCKS where SOURCE = ? and ARTICLEID = ? and TYPE = ? order by NO',(self._source,self._article_id,'phrase',))
			result = self.dbc.fetchone()
			if result:
				return result[0]
		else:
			sg.Message('DB.phrase_dic',sh.lev_warn,sh.globs['mes'].empty_input)



if __name__ == '__main__':
	import re
	import html
	import tags    as tg
	import elems   as el
	import cells   as cl
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
	
	collimit   = 10
	source     = 'All'
	article_id = 'martyr.txt'
	#blacklist  = ['Христианство']
	blacklist  = []
	prioritize = ['Религия']

	tags = tg.Tags(text)
	tags.run()
	#tags.debug(MaxRows=40)
	#input('Tags step completed. Press Enter')
	
	elems = el.Elems(blocks=tags._blocks,source=source,article_id=article_id)
	elems.run()
	#elems.debug(MaxRows=40)
	#input('Elems step completed. Press Enter')
	
	blocks_db = DB()
	blocks_db.fill(elems._data)
	
	blocks_db.request(source=source,article_id=article_id)
	data = blocks_db.assign_bp()
	
	bp = cl.BlockPrioritize(data=data,source=source,article_id=article_id,blacklist=blacklist,prioritize=prioritize)
	bp.run()
	#bp.debug(MaxRows=40)
	#input('BlockPrioritize step completed. Press Enter')
	#sg.Message('BlockPrioritize',sh.lev_info,bp._query.replace(';',';\n'))
	blocks_db.update(query=bp._query)
	
	data = blocks_db.assign_cells()
	cells = cl.Cells(data=data,collimit=collimit)
	cells.run()
	#cells.debug(MaxRows=40)
	#input('Cells step completed. Press Enter')
	#sg.Message('Cells',sh.lev_info,cells._query.replace(';',';\n'))
	blocks_db.update(query=cells._query)

	data = blocks_db.assign_pos()
	pos = cl.Pos(data=data)
	pos.run()
	#pos.debug(MaxRows=40)
	#input('Pos step completed. Press Enter')
	#sg.Message('Pos',sh.lev_info,pos._query.replace(';',';\n'))
	blocks_db.update(query=pos._query)
	
	blocks_db.print(Shorten=1,MaxRow=18,MaxRows=150)
