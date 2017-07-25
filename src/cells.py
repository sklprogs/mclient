#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo:
    - selectables: make 'Phrases' DIC cell SELECTABLE
'''

import io
import shared as sh
import sharedGUI as sg


# Extended from tags.Block
class Block:
	
	def __init__(self):
		self._block    = -1
		self.i         = -1
		self.j         = -1
		self._first    = -1
		self._last     = -1
		self._no       = -1
		self._cell_no  = -1 # Applies to non-blocked cells only
		self._same     = -1
		self._priority = -1
		# '_select' is an attribute of a *cell* which is valid if the cell has a non-blocked block of types 'term', 'phrase' or 'transc'
		self._select   = -1
		self._type     = 'comment' # 'wform', 'speech', 'dic', 'phrase', 'term', 'comment', 'correction', 'transc', 'invalid'
		self._text     = ''
		self._dica     = ''
		self._wforma   = ''
		self._speecha  = ''
		self._transca  = ''



# Update Block and Priority in DB before sorting cells
''' This complements DB with values that must be dumped into DB before sorting it
    Needs attributes in blocks: NO, DICA, TYPE, TEXT (test purposes only)
    Modifies attributes:        BLOCK, PRIORITY
'''
class BlockPrioritize:
	
	def __init__(self,data,source,search,blacklist=[],prioritize=[],phrase_dic=None):
		self._data       = data
		self._source     = source
		self._search     = search
		self._blacklist  = blacklist
		self._prioritize = prioritize
		self._phrase_dic = phrase_dic
		self._blocks     = []
		self._query      = ''
		if self._data and self._source and self._search:
			self.Success = True
		else:
			self.Success = False
			sh.log.append('BlockPrioritize.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
	
	def run(self):
		if self.Success:
			self.assign     ()
			self.block      ()
			self.prioritize ()
			self.dump       ()
		else:
			sh.log.append('BlockPrioritize.run',sh.lev_warn,sh.globs['mes'].canceled)
	
	def assign(self):
		for item in self._data:
			block       = Block()
			block._no   = item[0]
			block._type = item[1]
			block._text = item[2]
			block._dica = item[3]
			self._blocks.append(block)
			
	def block(self):
		for block in self._blocks:
			if block._dica in self._blacklist:
				block._block = 1
			else:
				block._block = 0
			
	def prioritize(self):
		if self._phrase_dic:
			for block in self._blocks:
				if self._phrase_dic == block._dica:
					# Set the (presumably) lowest priority for a 'Phrases' dictionary
					block._priority = -10
		for i in range(len(self._prioritize)):
			priority = len(self._prioritize) - i
			for block in self._blocks:
				if self._prioritize[i].lower() == block._dica.lower():
					block._priority = priority
					
	def dump(self):
		tmp = io.StringIO()
		tmp.write('begin;')
		for block in self._blocks:
			tmp.write('update BLOCKS set BLOCK=%d,PRIORITY=%d where NO=%d;' % (block._block,block._priority,block._no))
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()

	def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
		print('\nBlockPrioritize.debug (Non-DB blocks):')
		headers = ['NO'
		          ,'DICA'
		          ,'TYPE'
		          ,'TEXT'
		          ,'BLOCK'
		          ,'PRIORITY'          
		          ]
		rows = []
		for block in self._blocks:
			rows.append ([block._no
			             ,block._dica
			             ,block._type
			             ,block._text
			             ,block._block
			             ,block._priority        
			             ]
			            )
		sh.Table (headers = headers
		         ,rows    = rows
		         ,Shorten = Shorten
		         ,MaxRow  = MaxRow
		         ,MaxRows = MaxRows
		         ).print()



''' This re-assigns DIC, WFORM, SPEECH, TRANSC types
    We assume that sqlite has already sorted DB with 'BLOCK IS NOT 1'
    Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL, DICA, WFORMA, SPEECHA, TRANSCA
    Modifies attributes:        TEXT, ROWNO, COLNO
'''
class Cells:
	
	def __init__(self,data,collimit=10,phrase_dic=None): # Including fixed columns
		self._data       = data # Sqlite fetch
		self._collimit   = collimit
		self._phrase_dic = phrase_dic
		self._blocks     = []
		self._query      = ''
		if self._data:
			self.Success = True
		else:
			self.Success = False
			sh.log.append('Cells.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	# The 'Phrases' section comes the latest in MT, therefore, it inherits fixed columns of the preceding dictionary which are irrelevant. Here we clear them.
	def clear_phrases(self):
		if self._phrase_dic:
			for block in self._blocks:
				if block._dica == self._phrase_dic:
					if block._type == 'wform' or block._type == 'speech' or block._type == 'transc':
						block._text  = ''
	
	def clear_fixed(self):
		dica = wforma = speecha = transca = ''
		for block in self._blocks:
			if block._type == 'dic':
				if dica == block._dica:
					block._text = ''
				else:
					dica = block._dica
			if block._type == 'wform':
				if wforma == block._wforma:
					block._text = ''
				else:
					wforma = block._wforma
			if block._type == 'speech':
				if speecha == block._speecha:
					block._text = ''
				else:
					speecha = block._speecha
			if block._type == 'transc':
				if transca == block._transca:
					block._text = ''
				else:
					transca = block._transca
					
	def run(self):
		if self.Success:
			self.assign        ()
			self.clear_fixed   ()
			self.clear_phrases ()
			self.wrap          ()
			self.dump          ()
		else:
			sh.log.append('Cells.run',sh.lev_warn,sh.globs['mes'].canceled)
		
	def assign(self):
		for item in self._data:
			block          = Block()
			block._no      = item[0]
			block._type    = item[1]
			block._text    = item[2]
			block._same    = item[3]
			block._dica    = item[4]
			block._wforma  = item[5]
			block._speecha = item[6]
			block._transca = item[7]
			self._blocks.append(block)
		
	def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
		print('\nCells.debug (Non-DB blocks):')
		headers = ['NO'
		          ,'TYPE'
		          ,'TEXT'
		          ,'ROWNO'
		          ,'COLNO'             
		          ]
		rows = []
		for block in self._blocks:
			rows.append ([block._no
			             ,block._type
			             ,block._text
			             ,block.i
			             ,block.j             
			             ]
			            )
		sh.Table (headers = headers
		         ,rows    = rows
		         ,Shorten = Shorten
		         ,MaxRow  = MaxRow
		         ,MaxRows = MaxRows
		         ).print()
	
	def wrap(self): # Dic-Wform-Transc-Speech
		i = j = 0
		for x in range(len(self._blocks)):
			if self._blocks[x]._type == 'dic':
				if x > 0:
					i += 1
					self._blocks[x].i = i
				else:
					self._blocks[x].i = i
					i += 1
				self._blocks[x].j = 0
				j = 3
			elif self._blocks[x]._type == 'wform':
				self._blocks[x].i = i
				self._blocks[x].j = j = 1
			elif self._blocks[x]._type == 'transc':
				self._blocks[x].i = i
				self._blocks[x].j = j = 2
			elif self._blocks[x]._type == 'speech':
				self._blocks[x].i = i
				self._blocks[x].j = j = 3
			elif self._blocks[x]._same > 0: # Must be before checking '_collimit'
				self._blocks[x].i = i
				self._blocks[x].j = j
			elif j + 1 == self._collimit:
				i += 1
				self._blocks[x].i = i
				self._blocks[x].j = j = 4 # Instead of creating empty non-selectable cells
			else:
				self._blocks[x].i = i
				if x > 0:
					j += 1
					self._blocks[x].j = j
				else:
					self._blocks[x].j = 4
					j += 1
		
	def dump(self):
		tmp = io.StringIO()
		tmp.write('begin;')
		for block in self._blocks:
			# We do not want to mess around with screening quotes that can fail the query
			if block._text:
				tmp.write('update BLOCKS set ROWNO=%d,COLNO=%d where NO=%d;' % (block.i,block.j,block._no))
			else:
				tmp.write('update BLOCKS set TEXT="%s",ROWNO=%d,COLNO=%d where NO=%d;' % (block._text,block.i,block.j,block._no))
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()
		return self._query



# This is view-specific and should be recreated each time
''' We assume that sqlite has already sorted DB with 'BLOCK IS NOT 1'
    Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
    Modifies attributes:        SELECTABLE, CELLNO, POS1, POS2
'''
class Pos:
	
	def __init__(self,data):
		self._data       = data # Sqlite fetch
		self._blocks     = []
		self._query      = ''
		if self._data:
			self.Success = True
		else:
			self.Success = False
			sh.log.append('Pos.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	def run(self):
		if self.Success:
			self.assign      ()
			self.gen_poses   ()
			self.cell_no     ()
			self.selectables ()
			self.dump        ()
		else:
			sh.log.append('Pos.run',sh.lev_warn,sh.globs['mes'].canceled)
		
	def assign(self):
		for item in self._data:
			block       = Block()
			block._no   = item[0]
			block._type = item[1]
			block._text = item[2]
			block._same = item[3]
			block.i     = item[4]
			self._blocks.append(block)
		
	def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
		print('\nPos.debug (Non-DB blocks):')
		headers = ['NO'
		          ,'TYPE'
		          ,'TEXT'
		          ,'SELECTABLE'
		          ,'CELLNO'
		          ,'POS1'
		          ,'POS2'
		          ]
		rows = []
		for block in self._blocks:
			rows.append ([block._no
			             ,block._type
			             ,block._text
			             ,block._select
			             ,block._cell_no
			             ,block._first
			             ,block._last
			             ]
			            )
		sh.Table (headers = headers
		         ,rows    = rows
		         ,Shorten = Shorten
		         ,MaxRow  = MaxRow
		         ,MaxRows = MaxRows
		         ).print()
	
	def gen_poses(self): # todo: elaborate
		last = 0
		for block in self._blocks:
			block._first = last + 1
			block._last  = block._first + len(block._text)
			last         = block._last
		
	def selectables(self):
		cell_nos = []
		for block in self._blocks:
			if block._type == 'phrase' or block._type == 'term' or block._type == 'transc':
				# There is no need to select empty cells
				if block._text:
					cell_nos.append(block._cell_no)
		for block in self._blocks:
			if block._cell_no in cell_nos:
				block._select = 1
			else:
				block._select = 0

	def cell_no(self):
		no = 0
		for i in range(len(self._blocks)):
			if self._blocks[i]._same > 0:
				self._blocks[i]._cell_no = no
			elif i > 0: # i != no
				no += 1
				self._blocks[i]._cell_no = no
			else:
				self._blocks[i]._cell_no = no
		
	def dump(self):
		tmp = io.StringIO()
		tmp.write('begin;')
		for block in self._blocks:
			tmp.write('update BLOCKS set SELECTABLE=%d,CELLNO=%d,POS1=%d,POS2=%d where NO=%d;' % (block._select,block._cell_no,block._first,block._last,block._no))
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()
		return self._query



if __name__ == '__main__':
	import re
	import html
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
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/martyr.txt').get()
	text = sh.ReadTextFile(file='/home/pete/tmp/ars/preceding.txt').get()

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
	
	source     = 'All'
	search     = 'martyr.txt'
	blacklist  = ['Австралийский сленг','Архаизм','Бранное выражение','Грубое выражение','Диалект','Жаргон','Презрительное выражение','Просторечие','Разговорное выражение','Расширение файла','Редкое выражение','Ругательство','Сленг','Табу','Табуированная лексика','Тюремный жаргон','Устаревшее слово','Фамильярное выражение','Шутливое выражение','Эвфемизм']
	prioritize = ['Общая лексика','Техника']
	
	Debug = 0

	tags = tg.Tags(text)
	tags.run()
	if Debug:
		tags.debug(MaxRows=40)
		input('Tags step completed. Press Enter')
	
	elems = el.Elems(blocks=tags._blocks,source=source,search=search)
	elems.run()
	if Debug:
		elems.debug(MaxRows=40)
		input('Elems step completed. Press Enter')
	
	blocks_db = db.DB()
	blocks_db.fill(elems._data)
	
	blocks_db.request(source=source,search=search)
	phrase_dic = blocks_db.phrase_dic()
	data = blocks_db.assign_bp()
	
	bp = BlockPrioritize(data=data,source=source,search=search,blacklist=blacklist,prioritize=prioritize,phrase_dic=phrase_dic)
	bp.run()
	if Debug:
		bp.debug(MaxRows=40)
		input('BlockPrioritize step completed. Press Enter')
		sg.Message('BlockPrioritize',sh.lev_info,bp._query.replace(';',';\n'))
	blocks_db.update(query=bp._query)
	
	data = blocks_db.assign_cells()
	cells = Cells(data=data,collimit=10,phrase_dic=phrase_dic)
	cells.run()
	if Debug:
		cells.debug(MaxRows=40)
		input('Cells step completed. Press Enter')
		sg.Message('Cells',sh.lev_info,cells._query.replace(';',';\n'))
	blocks_db.update(query=cells._query)
	
	data = blocks_db.assign_pos()
	pos = Pos(data=data)
	pos.run()
	if Debug:
		pos.debug(MaxRows=40)
		input('Pos step completed. Press Enter')
		sg.Message('Pos',sh.lev_info,pos._query.replace(';',';\n'))
	blocks_db.update(query=pos._query)

	if Debug:
		blocks_db.print(Shorten=1,MaxRow=15,MaxRows=100)
		#blocks_db.dbc.execute('select * from BLOCKS where BLOCK=0 order by CELLNO,NO')
		#blocks_db.print(Selected=1,Shorten=1,MaxRow=18,MaxRows=100)
		
	#blocks_db.dbc.execute('select * from BLOCKS where BLOCK=0 order by NO')
	#blocks_db.print(Selected=1,Shorten=1,MaxRow=15,MaxRows=100)
	blocks_db.print(Shorten=1,MaxRow=15,MaxRows=100)
	
