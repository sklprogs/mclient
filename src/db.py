#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3
import prettytable
import shared as sh
import sharedGUI as sg


class DB:
	
	def __init__(self):
		self.db  = sqlite3.connect(':memory:')
		self.dbc = self.db.cursor()
		# Must use 'integer' fully before 'primary key autoincrement'
		self.dbc.execute('create table if not exists BLOCKS (NO integer primary key autoincrement,ARTICLEID text,SOURCE text,DICA text,WFORMA text,SPEECHA text,TRANSCA text,TERMA text,TYPE text,TEXT text,SELECTABLE bool,SAMECELL bool,CELLNO integer,ROWNO integer,COLNO integer,POS1 integer,POS2 integer,BLOCK boolean)')
		
	def fill(self,data):
		self.dbc.executemany('insert into BLOCKS values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',data)
	
	def sort(self):
		#self.dbc.execute('select * from BLOCKS order by DICA,WFORMA,NO,TERMA')
		#self.dbc.execute('select TYPE,TEXT,SELECTABLE,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where TYPE in ("term","comment","correction","phrase") order by DICA,WFORMA,CELLNO,TERMA,NO')
		self.dbc.execute('select TYPE,TEXT,SELECTABLE,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where TYPE in ("term","comment","correction","phrase") order by DICA,WFORMA,TERMA,CELLNO,NO')
		#self.dbc.execute('select TYPE,TEXT,SELECTABLE,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA from BLOCKS where TYPE in ("term","comment","correction","phrase") order by NO') # cur
		#return self.dbc.fetchall()
	
	def shorten(self,rows):
		for i in range(len(rows)):
			if isinstance(rows[i],tuple):
				rows[i] = list(rows[i])
			for j in range(len(rows[i])):
				if isinstance(rows[i][j],str):
					if len(rows[i][j]) > 20:
						rows[i][j] = rows[i][j][0:20]
		return rows
	
	def print(self,Selected=False):
		# 'self.dbc.description' is 'None' without performing 'select' first
		if not Selected:
			self.dbc.execute('select * from BLOCKS')
		col_names = [cn[0] for cn in self.dbc.description]
		rows = self.dbc.fetchall()
		rows = self.shorten(rows)
		x = prettytable.PrettyTable(col_names)
		for row in rows:
			x.add_row(row)
		print(x)
		
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
