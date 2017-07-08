#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import shared as sh
import sharedGUI as sg


# Extended from tags.Block
class Block:
	
	def __init__(self):
		self._type      = 'comment' # 'wform', 'speech', 'dic', 'phrase', 'term', 'comment', 'correction', 'transc', 'invalid'
		self._text      = self._url = ''
		self._cell_no   = 0 # Applies to non-blocked cells only
		self.Block      = self.SameCell = False
		# 'Selectable' is an attribute of a *cell* which is valid if the cell has a non-blocked block of types 'term', 'phrase' or 'transc'
		self.Selectable = False
		self.i          = 0
		self.j          = 0



# This is view-specific and should be recreated each time
class Cells:
	
	def __init__(self,data,collimit=10): # Including non-selectable columns
		# 'data' is a 'fetchall' result of the following columns: TYPE,TEXT,SELECTABLE,SAMECELL,DICA,WFORMA,SPEECHA,TRANSCA
		self._data     = data
		self._collimit = collimit
		self._blocks   = []
		
	def assign(self):
		for item in self._data:
			block            = Block()
			block._type      = item[0]
			block._text      = item[1]
			block.Selectable = item[2]
			block.SameCell   = item[3]
			block._dica      = item[4]
			block._wforma    = item[5]
			block._speecha   = item[6]
			block._transca   = item[7]
			self._blocks.append(block)
			
	def fill(self): # Dic-Wform-Speech-Transc
		dica = wforma = ''
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._dica != dica:
				block            = Block()
				block.Selectable = self._blocks[i].Selectable
				block.SameCell   = False
				block._type      = 'dic'
				block._text      = self._blocks[i]._dica
				dica             = self._blocks[i]._dica
				self._blocks.insert(i,block)
				i += 1
			if self._blocks[i]._wforma != wforma:
				# Add 'wform'
				block            = Block()
				block.Selectable = self._blocks[i].Selectable
				block.SameCell   = False
				block._type      = 'wform'
				block._text      = self._blocks[i]._wforma
				wforma           = self._blocks[i]._wforma
				self._blocks.insert(i,block)
				i += 1
				# Add 'transc'
				block            = Block()
				block.Selectable = self._blocks[i].Selectable
				block.SameCell   = False
				block._type      = 'transc'
				block._text      = self._blocks[i]._transca
				self._blocks.insert(i,block)
				i += 1
				# Add 'speech'
				block            = Block()
				block.Selectable = self._blocks[i].Selectable
				block.SameCell   = False
				block._type      = 'speech'
				block._text      = self._blocks[i]._speecha
				self._blocks.insert(i,block)
				i += 1
			i += 1
			
	def run(self):
		self.assign    ()
		self.fill      ()
		self.wrap      ()
		self.gen_poses ()
		self.cell_no   ()
		#self.debug    ()
		
	def debug(self):
		message = ''
		for i in range(len(self._blocks)):
			message += '%d: Type\t\t: "%s"\n'        % ( i,self._blocks[i]._type      )
			message += '%d: Text\t\t: "%s"\n'        % ( i,self._blocks[i]._text      )
			#message += '%d: URL\t\t: "%s"\n'        % ( i,self._blocks[i]._url       )
			message += '%d: Selectable\t\t: "%s"\n'  % ( i,self._blocks[i].Selectable )
			message += '%d: SameCell\t\t: "%s"\n'    % ( i,self._blocks[i].SameCell   )
			if hasattr(self._blocks[i],'_dica'):
				message += '%d: DICA\t\t: "%s"\n'    % ( i,self._blocks[i]._dica      )
				message += '%d: WFORMA\t\t: "%s"\n'  % ( i,self._blocks[i]._wforma    )
				message += '%d: SPEECHA\t\t: "%s"\n' % ( i,self._blocks[i]._speecha   )
				message += '%d: TRANSCA\t\t: "%s"\n' % ( i,self._blocks[i]._transca   )
			if hasattr(self._blocks[i],'i'):
				message += '%d: i\t\t: %d\n'         % ( i,self._blocks[i].i          )
				message += '%d: j\t\t: %d\n'         % ( i,self._blocks[i].j          )
			if hasattr(self._blocks[i],'_first'):
				message += '%d: _first\t\t: %d\n'    % ( i,self._blocks[i]._first     )
				message += '%d: _last\t\t: %d\n'     % ( i,self._blocks[i]._last      )
			message += '\n'
		sg.Message('Cells.debug',sh.lev_info,message)
	
	def wrap(self): # Dic-Wform-Speech-Transc
		i = j = -1
		prev_type = None
		for block in self._blocks:
			if block._type == 'dic':
				prev_type = block._type
				i += 1
				block.i = i
				block.j = 0
				j = 3
			elif block._type == 'wform':
				if not prev_type == 'dic':
					i += 1
				prev_type = block._type
				block.i = i
				block.j = j = 1
			elif block._type == 'transc':
				if not prev_type == 'wform':
					i += 1
				prev_type = block._type
				block.i = i
				block.j = j = 2
			elif block._type == 'speech':
				if not prev_type == 'transc':
					i += 1
				prev_type = block._type
				block.i = i
				block.j = j = 3
			elif block.SameCell: # Must be before checking '_collimit'
				block.i = i
				block.j = j
			elif j + 1 == self._collimit:
				prev_type = block._type
				i += 1
				block.i = i
				block.j = j = 4 # Instead of creating empty non-selectable cells
			else:
				prev_type = block._type
				block.i = i
				j += 1
				block.j = j
				
	def gen_poses(self):
		last = -1
		for block in self._blocks:
			if not block.Block:
				block._first = last + 1
				block._last  = block._first + len(block._text)
				last         = block._last
				# 'block._last+1' if there are spaces between words
				# tmp.write(' ') if there are spaces between words
		
	# Identical to 'Elems.cell_no'
	def cell_no(self):
		no = 0
		for i in range(len(self._blocks)):
			if self._blocks[i].SameCell:
				self._blocks[i]._cell_no = no
			elif i > 0: # i != no
				no += 1
			self._blocks[i]._cell_no = no
		
	def dump(self,min_no=1): # Autoincrement starts with 1
		# todo: 'min_no' is the autoincremented number with which the first block of a new article starts; it should be recalculated each time we load an article
		tmp = io.StringIO()
		tmp.write('begin;')
		i = min_no
		for block in self._blocks:
			if block.Block:
				tmp.write('update BLOCKS set BLOCK=1 where NO=%d;' % i)
			else:
				#NO integer primary key autoincrement,ARTICLEID text,SOURCE text,DICA text,WFORMA text,SPEECHA text,TRANSCA text,TERMA text,TYPE text,TEXT text,SELECTABLE bool,SAMECELL bool,CELLNO integer,ROWNO integer,COLNO integer,POS1 integer,POS2 integer,BLOCK boolean
				tmp.write('update BLOCKS set SAMECELL=%d,CELLNO=%d, ROWNO=%d, COLNO=%d, POS1=%d, POS2=%d, BLOCK=0 where NO=%d;' % (block.SameCell,block._cell_no,block.i,block.j,block._first,block._last,i))
			i += 1
		tmp.write('commit;')
		query = tmp.getvalue()
		tmp.close()
		return query



if __name__ == '__main__':
	import re
	import html
	import time
	import tags as tg
	import elems as el
	import mclient as mc
	import db
	
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
	
	cur_start = time.time()
	data = elems.dump()
	sh.log.append('elems: fill + dump',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	
	blocks_db = db.DB()
	cur_start = time.time()
	blocks_db.fill(data)
	blocks_db.sort()
	sh.log.append('blocks_db.fill, blocks_db.sort',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-cur_start))
	#blocks_db.print()
	
	data = blocks_db.dbc.fetchall()
	
	cells = Cells(data=data)
	cells.run()
	#cells.debug()
	
	blocks_db.update(query=cells.dump())

	blocks_db.dbc.execute('select TERMA,TYPE,TEXT,SELECTABLE,SAMECELL,CELLNO,ROWNO,COLNO from BLOCKS')
	blocks_db.print(Selected=True)
