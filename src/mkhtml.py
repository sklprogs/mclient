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


# Shortened
class Block:
	
	def __init__(self):
		self._type = ''
		self._text = ''
		self.i     = 0
		self.j     = 0


class HTML:
	
	def __init__(self,data,collimit=9): # 'collimit' includes fixed blocks
		self._data     = data
		self._collimit = collimit
		self._blocks   = []
		self._block    = None
		self._html     = ''
		if self._data:
			self.assign ()
			self.html   ()
		else:
			sh.log.append('HTML.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
			
	def assign(self):
		for item in self._data:
			block       = Block()
			block._type = item[0]
			block._text = item[1]
			block.i     = item[2]
			block.j     = item[3]
			self._blocks.append(block)
		
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
		self.output.write('<html>\n  <body>\n    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n      <table>')
		i = j = 0
		self.output.write('\n        <tr><td>')
		for self._block in self._blocks:
			while self._block.i > i:
				self.output.write('</td></tr>\n        <tr><td align="center">')
				i = self._block.i
				j = 0
			while self._block.j > j:
				self.output.write('</td>\n          <td>')
				j += 1
			self._dic        ()
			self._wform      ()
			self._term       ()
			self._comment    ()
			self._correction ()
		self.output.write('</td></tr>\n      </table>  \n</body>\n</html>')
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

	timer = sh.Timer(func_title='tags + elems + cells + pos + mkhtml')
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
	
	blocks_db.print(Shorten=1,MaxRows=100,MaxRow=18)
	
	mkhtml = HTML(data=blocks_db.fetch(),collimit=collimit)
	
	timer.end()
	
	file_w = '/tmp/test.html'
	sh.WriteTextFile(file=file_w,AskRewrite=0).write(text=mkhtml._html)
	sh.Launch(target=file_w).default()
	
