#!/usr/bin/python3

''' # todo:
	- this doesn't work, why?
	  self.output.write('<col width="130">')
	- fix </td>, <td align=>
	- clean up
'''

import io
import shared as sh
import sharedGUI as sg


class HTML:
	
	def __init__(self,blocks=[],collimit=9): # 'collimit' includes fixed blocks
		self._blocks   = blocks
		self._collimit = collimit
		self._html     = ''
		self._block    = None
		self.html()
		
	def _dic(self):
		if self._block._type == 'dic':
			#self.output.write('<td align="left">') # cur
			self.output.write('<font face="')
			self.output.write(sh.globs['var']['font_dics_family'])
			self.output.write('" color="')
			'''
			# todo (?): add to the config
			if self._block._text in articles.current().block():
				self.output.write('gray')
			elif self._block._text in articles.current().prioritize():
				self.output.write('red')
			else:
				self.output.write(sh.globs['var']['color_dics'])
			'''
			self.output.write(sh.globs['var']['color_dics'])
			self.output.write('" size="')
			self.output.write(str(sh.globs['int']['font_dics_size']))
			self.output.write('"><b>')
			self.output.write(self._block._text)
			self.output.write('</b></font>')
			#self.output.write('<td align="left">')
	
	def _wform(self):
		if self._block._type == 'wform':
			#self.output.write('<td align="center">')
			#self.output.write('<td align="left">')
			self.output.write('<font face="')
			self.output.write(sh.globs['var']['font_speech_family'])
			self.output.write('" color="')
			self.output.write(sh.globs['var']['color_speech'])
			self.output.write('" size="')
			self.output.write(str(sh.globs['int']['font_speech_size']))
			self.output.write('"><b>')
			self.output.write(self._block._text)
			self.output.write('</b></font>')
			#self.output.write('</td>')
		
	def _term(self):
		if self._block._type == 'term' or self._block._type == 'phrase':
			#self.output.write('<td align="left">')
			self.output.write('<font face="')
			self.output.write(sh.globs['var']['font_terms_family'])
			self.output.write('" color="')
			self.output.write(sh.globs['var']['color_terms'])
			self.output.write('" size="')
			self.output.write(str(sh.globs['int']['font_terms_size']))
			self.output.write('">')
			self.output.write(self._block._text)
			self.output.write('</font>')
	
	def _comment(self):
		if self._block._type == 'comment' or self._block._type == 'speech' or self._block._type == 'transc':
			'''
			if self._block._type == 'speech' or self._block._type == 'transc':
				#self.output.write('<td align="center">')
				self.output.write('<td align="left">')
			#else:
			#	self.output.write('<td align="left">')
			'''
			#self.output.write('<td align="left">')
			self.output.write('<i><font face="')
			self.output.write(sh.globs['var']['font_comments_family'])
			self.output.write('" size="')
			self.output.write(str(sh.globs['int']['font_comments_size']))
			self.output.write('" color="')
			self.output.write(sh.globs['var']['color_comments'])
			self.output.write('">')
			self.output.write(self._block._text)
			self.output.write('</i></font>')
			#if self._block._type == 'speech' or self._block._type == 'transc':
			#	self.output.write('</td align="left">')
			
	def _correction(self):
		if self._block._type == 'correction':
			self.output.write('<i><font face="')
			self.output.write(sh.globs['var']['font_comments_family'])
			self.output.write('" size="')
			self.output.write(str(sh.globs['int']['font_comments_size']))
			self.output.write('" color="')
			#self.output.write(sh.globs['var']['color_comments'])
			# todo (?): add to config
			self.output.write('green')
			self.output.write('">')
			self.output.write(self._block._text)
			self.output.write('</i></font>')

	def html(self):
		# Default Python string concatenation is too slow, so we use this module instead
		self.output = io.StringIO()
		self.output.write('<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"><table>')
		i = j = 0
		self.output.write('<tr>')
		for self._block in self._blocks:
			''' Just draw a table on a sheet of paper and count a number of empty cells. From this, we come to
			    self._collimit - j + 1 + (self._block.i - i - 1) * self._collimit + self._block.j,
			    which results in:
			    delta = self._collimit * (self._block.i - i) + self._block.j - j - 1.
			    The number of tabs to be inserted is the number of empty cells + 1. So:
			'''
			delta = self._collimit * (self._block.i - i) + self._block.j - j
			for x in range(delta):
				if j == self._collimit - 1:
					j = 0
					#self.output.write('</td>')
					self.output.write('</tr><tr>')
					#self.output.write('</td></tr><tr><td>')
					i += 1
				else:
					j += 1
				self.output.write('<td>')
				#self.output.write('<td>')
				#self.output.write('<td align="left">')
				#self.output.write('</td>')
			#if not self._block.SameCell:
			#self.output.write('<td>')
			self._dic        ()
			self._wform      ()
			self._term       ()
			self._comment    ()
			self._correction ()
			#if not self._block.SameCell:
			#self.output.write('</td>')
			#for x in range(delta):
			#	self.output.write('</td>')
		self.output.write('</tr>')
		self.output.write('</table></body></html>')
		self._html = self.output.getvalue()
		self.output.close()



if __name__ == '__main__':
	import re
	import html
	import tags    as tg
	import db
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

	timer = sh.Timer(func_title='tags + elems + cells')
	timer.start()
	
	tags = tg.Tags(text)
	tags.run()
	#tags.debug(MaxRows=40)
	#input('Tags step completed. Press Enter')
	
	elems = el.Elems(blocks=tags._blocks,source=source,article_id=article_id)
	elems.run()
	#elems.debug(MaxRows=40)
	#input('Elems step completed. Press Enter')
	
	blocks_db = db.DB()
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
	cells = cl.Cells(data=data,nos=blocks_db.nos_nb(),collimit=collimit)
	cells.run()
	#cells.debug(MaxRows=40)
	#input('Cells step completed. Press Enter')
	#sg.Message('Cells',sh.lev_info,cells._query.replace(';',';\n'))
	blocks_db.update(query=cells._query)

	#blocks_db.print(Shorten=1,MaxRow=18,MaxRows=100)
	#blocks_db.dbc.execute('select * from BLOCKS where BLOCK=0 order by CELLNO,NO')
	#blocks_db.print(Selected=1,Shorten=1,MaxRow=18,MaxRows=100)
	
	mkhtml = HTML(blocks=cells._blocks,collimit=collimit)
	
	timer.end()
	
	file_w = '/tmp/test.html'
	sh.WriteTextFile(file=file_w,AskRewrite=0).write(text=mkhtml._html)
	sh.Launch(target=file_w).default()
	
