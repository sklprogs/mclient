#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' This module prepares blocks after extracting tags for permanently storing in DB
    Needs attributes in blocks: TYPE, DICA, WFORMA, SPEECHA, TRANSCA, TERMA, SAMECELL
    Modifies attributes:        TYPE, TEXT, DICA, WFORMA, SPEECHA, TRANSCA, TERMA, SAMECELL
    SAMECELL is based on Tags and TYPE and is filled fully
    SELECTABLE cannot be filled because it depends on CELLNO which is created in Cells; Cells modifies TEXT of DIC, WFORM, SPEECH, TRANSC types, and we do not need to make empty cells SELECTABLE, so we calculate SELECTABLE fully in Cells
'''

''' # todo:
    - Check that _same of the 1st cell is always True (or fix such behavior)
	- clean up
	- unite cells if (?) the url is the same or similar. Example: 'sampling' -> Робототехника -> проведение выборочных замеров
'''

import shared as sh
import sharedGUI as sg



# A copy of Tags.Block
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
		# '_select' is an attribute of a *cell* which is valid if the cell has a non-blocked block of types 'term', 'phrase' or 'transc'
		self._select   = -1
		self._type     = 'comment' # 'wform', 'speech', 'dic', 'phrase', 'term', 'comment', 'correction', 'transc', 'invalid'
		self._text     = ''
		self._url      = ''
		self._dica     = ''
		self._wforma   = ''
		self._speecha  = ''
		self._transca  = ''
		self._terma    = ''
		self._priority = -1



# Process blocks before dumping to DB
''' About filling 'terma':
    - We fill 'terma' from the start in order to ensure the correct 'terma' value for blocks having '_same == 1'
	- We fill 'terma' from the end in order to ensure that 'terma' of blocks of non-selectable types will have the value of the 'term' AFTER those blocks
	- We fill 'terma' from the end in order to ensure that 'terma' is also filled for blocks having '_same == 0'
	- When filling 'terma' from the start to the end, in order to set a default 'terma' value, we also search for blocks of the 'phrase' type (just to be safe in such cases when 'phrase' blocks anticipate 'term' blocks). However, we fill 'terma' for 'phrase' blocks from the end to the start because we want the 'phrase' dictionary to have the 'terma' value of the first 'phrase' block AFTER it
'''
class Elems:
	
	def __init__(self,blocks,source,article_id):
		self._blocks     = blocks
		self._source     = source
		self._article_id = article_id
		self._data       = []
		if self._blocks and self._source and self._article_id:
			self.Success = True
		else:
			self.Success = False
			sh.log.append('Elems.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	def run(self):
		if self.Success:
			self.transc            ()
			self.phrases           ()
			self.comments          ()
			self.add_space         ()
			# These 2 procedures should not be combined (otherwise, corrections will have the same color as comments)
			self.unite_comments    ()
			self.unite_corrections ()
			self.speech            ()
			self.fill              ()
			self.fill_terma        ()
			self.remove_fixed      ()
			self.insert_fixed      ()
			self.dump              ()
		else:
			sh.log.append('Elems.run',sh.lev_warn,sh.globs['mes'].canceled)
	
	def debug(self,Shorten=1,MaxHeader=10,MaxRow=20,MaxRows=20):
		print('\nElems.debug (Non-DB blocks):')
		headers = [
		            'DICA'              ,
		            'WFORMA'            ,
		            'SPEECHA'           ,
		            'TRANSCA'           ,
		            'TYPE'              ,
		            'TEXT'              ,
		            'SAMECELL'          
		          ]
		rows = []
		for block in self._blocks:
			rows.append (
			              [
			        block._dica         ,
			        block._wforma       ,
			        block._speecha      ,
			        block._transca      ,
			        block._type         ,
			        block._text         ,
			        block._same         
			              ]
			            )
		sh.Table (
		            headers             = headers                             ,
		            rows                = rows                                ,
		            Shorten             = Shorten                             ,
		            MaxHeader           = MaxHeader                           ,
		            MaxRow              = MaxRow                              ,
		            MaxRows             = MaxRows
		         ).print()
		
	# 'speech' blocks have '_same = True' when analyzing MT because they are within a single tag. We fix it here, not in Tags, because Tags are assumed to output the result 'as is'.
	def speech(self):
		for i in range(len(self._blocks)):
			if self._blocks[i]._type == 'speech':
				self._blocks[i]._same = 0
				if i < len(self._blocks) - 1:
					self._blocks[i+1]._same = 0
	
	def transc(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'transc' and self._blocks[i]._same > 0:
				if i > 0 and self._blocks[i-1]._type == 'transc':
					self._blocks[i-1]._text += self._blocks[i]._text
					del self._blocks[i]
					i -= 1
			i += 1
							
	def unite_comments(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'comment' and self._blocks[i]._same > 0:
				if i > 0 and self._blocks[i-1]._type == 'comment':
					self._blocks[i-1]._text += self._blocks[i]._text
					del self._blocks[i]
					i -= 1
			i += 1
			
	def unite_corrections(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'correction' and self._blocks[i]._same > 0:
				if i > 0 and self._blocks[i-1]._type == 'correction':
					self._blocks[i-1]._text += self._blocks[i]._text
					del self._blocks[i]
					i -= 1
			i += 1
			
	def comments(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'comment' or self._blocks[i]._type == 'correction':
				text_str = self._blocks[i]._text.strip()
				# Delete comments that are just ';' or ',' (we don't need them, we have a table view)
				# We delete instead of assigning Block attribute because we may need to unblock blocked dictionaries later
				if text_str == ';' or text_str == ',':
					del self._blocks[i]
					i -= 1
				# We suppose that these are abbreviations of dictionary titles. If the full dictionary title is not preceding (this can happen if the whole article is occupied by the 'Phrases' section), we keep these abbreviations as comments.
				elif i > 0 and self._blocks[i-1]._type == 'dic' and self._blocks[i]._same > 0:
					del self._blocks[i]
					i -= 1
				elif i == 0 and text_str == '|':
					del self._blocks[i]
					i -= 1
				elif i > 0 and text_str == '|' and self._blocks[i-1]._type != 'comment' and self._blocks[i-1]._type != 'correction':
					del self._blocks[i]
					i -= 1
				elif i > 0 and self._blocks[i]._text == self._blocks[i-1]._text == '|':
					del self._blocks[i]
					i -= 1
				elif i == len(self._blocks) and text_str == '|':
					del self._blocks[i]
					i -= 1
				elif not self._blocks[i]._same > 0:
					# For the following cases: "23 фраз в 9 тематиках"
					if i > 0 and self._blocks[i-1]._type == 'phrase':
						self._blocks[i]._same = 1
					# Move the comment to the preceding cell
					if text_str.startswith(',') or text_str.startswith(';') or text_str.startswith('(') or text_str.startswith(')') or text_str.startswith('|'):
						self._blocks[i]._same = 1
						# Mark the next block as a start of a new cell
						if i < len(self._blocks) - 1 and self._blocks[i+1]._type != 'comment' and self._blocks[i+1]._type != 'correction':
							self._blocks[i+1]._same = 0
			i += 1
	
	def add_space(self):
		for i in range(len(self._blocks)):
			if self._blocks[i]._same > 0:
				cond = False
				if i > 0:
					if self._blocks[i-1]._text[-1] in ['(','[','{']:
						cond = True
				if self._blocks[i]._text and not self._blocks[i]._text[0].isspace() and not self._blocks[i]._text[0] in sh.punc_array and not self._blocks[i]._text[0] in [')',']','}'] and not cond:
					self._blocks[i]._text = ' ' + self._blocks[i]._text

	def phrases(self):
		for block in self._blocks:
			if block._type == 'phrase':
				block._type = 'dic'
				block._select = True
				break
				
	def fill(self):
		dica = wforma = speecha = transca = terma = ''
		
		# Find first non-empty values and set them as default
		for block in self._blocks:
			if block._type == 'dic':
				dica = block._text
				break
		for block in self._blocks:
			if block._type == 'wform':
				wforma = block._text
				break
		for block in self._blocks:
			if block._type == 'speech':
				speecha = block._text
				break
		for block in self._blocks:
			if block._type == 'transc':
				transca = block._text
				break
		for block in self._blocks:
			if block._type == 'term' or block._type == 'phrase':
				terma = block._text
				break
		
		for block in self._blocks:
			if block._type == 'dic':
				dica = block._text
			elif block._type == 'wform':
				wforma = block._text
			elif block._type == 'speech':
				speecha = block._text
			elif block._type == 'transc':
				transca = block._text
			elif block._type == 'term':
				terma = block._text
			block._dica    = dica
			block._wforma  = wforma
			block._speecha = speecha
			block._transca = transca
			if block._same > 0:
				block._terma = terma
	
	def fill_terma(self):
		terma = ''
		i = len(self._blocks) - 1
		while i >= 0:
			if self._blocks[i]._type == 'term' or self._blocks[i]._type == 'phrase':
				terma = self._blocks[i]._text
				break
			i -= 1
		i = len(self._blocks) - 1
		while i >= 0:
			if self._blocks[i]._type == 'term' or self._blocks[i]._type == 'phrase':
				terma = self._blocks[i]._text
			if not self._blocks[i]._same > 0:
				self._blocks[i]._terma = terma
			i -= 1
			
	def insert_fixed(self):
		dica = wforma = speecha = ''
		i = 0
		while i < len(self._blocks):
			if dica != self._blocks[i]._dica or wforma != self._blocks[i]._wforma or speecha != self._blocks[i]._speecha:
				block          = Block()
				block._type    = 'dic'
				block._text    = self._blocks[i]._dica
				block._dica    = self._blocks[i]._dica
				block._wforma  = self._blocks[i]._wforma
				block._speecha = self._blocks[i]._speecha
				block._transca = self._blocks[i]._transca
				block._terma   = self._blocks[i]._terma
				block._same    = 0
				self._blocks.insert(i,block)
				block          = Block()
				block._type    = 'wform'
				block._text    = self._blocks[i]._wforma
				block._dica    = self._blocks[i]._dica
				block._wforma  = self._blocks[i]._wforma
				block._speecha = self._blocks[i]._speecha
				block._transca = self._blocks[i]._transca
				block._terma   = self._blocks[i]._terma
				block._same    = 0
				self._blocks.insert(i,block)
				block          = Block()
				block._type    = 'transc'
				block._text    = self._blocks[i]._transca
				block._dica    = self._blocks[i]._dica
				block._wforma  = self._blocks[i]._wforma
				block._speecha = self._blocks[i]._speecha
				block._transca = self._blocks[i]._transca
				block._terma   = self._blocks[i]._terma
				block._same    = 0
				self._blocks.insert(i,block)
				block          = Block()
				block._type    = 'speech'
				block._text    = self._blocks[i]._speecha
				block._dica    = self._blocks[i]._dica
				block._wforma  = self._blocks[i]._wforma
				block._speecha = self._blocks[i]._speecha
				block._transca = self._blocks[i]._transca
				block._terma   = self._blocks[i]._terma
				block._same    = 0
				self._blocks.insert(i,block)
				dica    = self._blocks[i]._dica
				wforma  = self._blocks[i]._wforma
				speecha = self._blocks[i]._speecha
				i += 4
			i += 1
		
	def remove_fixed(self):
		self._blocks = [block for block in self._blocks if block._type not in ['dic','wform','transc','speech']]
	
	def dump(self):
		for block in self._blocks:
			self._data.append (
			              (
			        None                , # (00) Skips the autoincrement
			        self._source        , # (01) SOURCE
			        self._article_id    , # (02) ARTICLEID
			        block._dica         , # (03) DICA
			        block._wforma       , # (04) WFORMA
			        block._speecha      , # (05) SPEECHA
			        block._transca      , # (06) TRANSCA
			        block._terma        , # (07) TERMA
			        block._type         , # (08) TYPE
			        block._text         , # (09) TEXT
			        block._url          , # (10) URL
			        block._block        , # (11) BLOCK
			        block._priority     , # (12) PRIORITY
			        block._select       , # (13) SELECTABLE
			        block._same         , # (14) SAMECELL
			        block._cell_no      , # (15) CELLNO
			        -1                  , # (16) ROWNO
			        -1                  , # (17) COLNO
			        -1                  , # (18) POS1
			        -1                    # (19) POS2
			            )
			              )



if __name__ == '__main__':
	import re
	import html
	import tags as tg
	import mclient as mc
	
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/star_test').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/sampling.txt').get()
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
	
	source     = 'All'
	article_id = 'martyr.txt'

	try:
		text = html.unescape(text)
	except:
		sh.log.append('Page.decode_entities',sh.lev_err,sh.globs['mes'].html_conversion_failure)
		
	# An excessive space must be removed after unescaping the page
	text = re.sub(r'\>[\s]{0,1}\<','><',text)

	mc.ConfigMclient ()

	tags = tg.Tags(text)
	tags.run()
	
	elems = Elems(blocks=tags._blocks,source=source,article_id=article_id)
	elems.run   ()
	elems.debug ()
