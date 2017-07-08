#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo:
    - Check that SameCell of the 1st cell is always True (or fix such behavior)
	- clean up
	- unite cells if (?) the url is the same or similar. Example: 'sampling' -> Робототехника -> проведение выборочных замеров
'''

import shared as sh
import sharedGUI as sg


# Process blocks before dumping to DB
class Elems:
	
	def __init__(self,blocks):
		self._blocks = blocks
		
	def run(self):
		self.transc            ()
		self.phrases           ()
		self.comments          ()
		self.add_space         ()
		# These 2 procedures should not be combined (otherwise, corrections will have the same color as comments)
		self.unite_comments    ()
		self.unite_corrections ()
		self.speech            ()
		self.cell_no           ()
		self.selectables       ()
		''' About filling 'terma':
		    - We fill 'terma' from the start in order to ensure the correct 'terma' value for blocks having 'SameCell == True'
		    - We fill 'terma' from the end in order to ensure that 'terma' of blocks of non-selectable types will have the value of the 'term' AFTER those blocks
		    - We fill 'terma' from the end in order to ensure that 'terma' is also filled for blocks having 'SameCell == False'
		    - When filling 'terma' from the start to the end, in order to set a default 'terma' value, we also search for blocks of the 'phrase' type (just to be safe in such cases when 'phrase' blocks anticipate 'term' blocks). However, we fill 'terma' for 'phrase' blocks from the end to the start because we want the 'phrase' dictionary to have the 'terma' value of the first 'phrase' block AFTER it
		'''
		self.fill              ()
		self.fill_terma        ()
		#self.debug            ()
	
	# Almost identical to Tags.debug_blocks
	def debug(self):
		message = ''
		count = 0
		for block in self._blocks:
			# fix: search does not work
			message += '%d: Type\t\t: "%s"\n'       % ( count,block._type    )
			message += '%d: Text\t\t: "%s"\n'       % ( count,block._text    )
			message += '%d: URL\t\t: "%s"\n'        % ( count,block._url     )
			message += '%d: Block\t\t: "%s"\n'      % ( count,block.Block    )
			message += '%d: SameCell\t\t: "%s"\n'   % ( count,block.SameCell )
			message += '%d: Cell #\t\t: %d\n\n'     % ( count,block._cell_no )
			count += 1
		#sg.Message('Elems.debug',sh.lev_info,message)
		words = sh.Words(text=message,OrigCyr=1,Auto=0)
		words.sent_nos()
		sg.objs.txt(words=words).reset_data()
		sg.objs._txt.title('Elems.debug:')
		sg.objs._txt.insert(text=message)
		sg.objs._txt.show()
		
	# 'speech' blocks have 'SameCell = True' when analyzing MT because they are within a single tag. We fix it here, not in Tags, because Tags are assumed to output the result 'as is'.
	def speech(self):
		for i in range(len(self._blocks)):
			if self._blocks[i]._type == 'speech':
				self._blocks[i].SameCell = False
				if i < len(self._blocks) - 1:
					self._blocks[i+1].SameCell = False
	
	def transc(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'transc' and self._blocks[i].SameCell:
				if i > 0 and self._blocks[i-1]._type == 'transc':
					self._blocks[i-1]._text += self._blocks[i]._text
					del self._blocks[i]
					i -= 1
			i += 1
							
	def unite_comments(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'comment' and self._blocks[i].SameCell:
				if i > 0 and self._blocks[i-1]._type == 'comment':
					self._blocks[i-1]._text += self._blocks[i]._text
					del self._blocks[i]
					i -= 1
			i += 1
			
	def unite_corrections(self):
		i = 0
		while i < len(self._blocks):
			if self._blocks[i]._type == 'correction' and self._blocks[i].SameCell:
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
				elif i > 0 and self._blocks[i-1]._type == 'dic' and self._blocks[i].SameCell:
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
				elif not self._blocks[i].SameCell:
					# For the following cases: "23 фраз в 9 тематиках"
					if i > 0 and self._blocks[i-1]._type == 'phrase':
						self._blocks[i].SameCell = True
					# Move the comment to the preceding cell
					if text_str.startswith(',') or text_str.startswith(';') or text_str.startswith('(') or text_str.startswith(')') or text_str.startswith('|'):
						self._blocks[i].SameCell = True
						# Mark the next block as a start of a new cell
						if i < len(self._blocks) - 1 and self._blocks[i+1]._type != 'comment' and self._blocks[i+1]._type != 'correction':
							self._blocks[i+1].SameCell = False
			i += 1
	
	def add_space(self):
		for i in range(len(self._blocks)):
			if self._blocks[i].SameCell:
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
				block.Selectable = True
				break
				
	def selectables(self):
		for block in self._blocks:
			if not block.Selectable:
				if block._type == 'phrase' or block._type == 'term' or block._type == 'transc':
					cell_no = block._cell_no
					for block in self._blocks:
						if block._cell_no == cell_no:
							block.Selectable = True
							
	def cell_no(self):
		no = 0
		for i in range(len(self._blocks)):
			if self._blocks[i].SameCell:
				self._blocks[i]._cell_no = no
			elif i > 0: # i != no
				no += 1
			self._blocks[i]._cell_no = no
				
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
			if block.SameCell:
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
			if not self._blocks[i].SameCell:
				self._blocks[i]._terma = terma
			i -= 1
	
	def dump(self):
		data = []
		for block in self._blocks:
			# todo: set ARTICLEID, SOURCE
			# 'None' skips the autoincrement
			data.append((None,'TEST_ID','ALL',block._dica,block._wforma,block._speecha,block._transca,block._terma,block._type,block._text,block.Selectable,block.SameCell,block._cell_no,-1,-1,-1,-1,False))
		return data



if __name__ == '__main__':
	import re
	import html
	import tags as tg
	import mclient as mc
	import time
	import mkhtml as mh
	
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/star_test').get()
	text = sh.ReadTextFile(file='/home/pete/tmp/ars/sampling.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/filter_get').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/добро пожаловать.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/добро.txt').get()
	#text = sh.ReadTextFile(file='/home/pete/tmp/ars/рабочая документация.txt').get()

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
	
	tags = tg.Tags(text)
	tags.run()
	
	elems = Elems(blocks=tags._blocks)
	elems.run()
	#elems.debug      ()
	
	mkhtml = mh.HTML(blocks=elems._blocks)
	
	sh.log.append('tags, elems, mkhtml',sh.lev_info,sh.globs['mes'].operation_completed % float(time.time()-start_time))
	
	file_w = '/tmp/test.html'
	sh.WriteTextFile(file=file_w,AskRewrite=0).write(text=mkhtml._html)
	sh.Launch(target=file_w).default()
