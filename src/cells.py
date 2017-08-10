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
		# '_select' is an attribute of a *cell* which is valid if the cell has a non-blocked block of types 'term', 'phrase' or 'transc'
		self._select   = -1
		self._priority = 0
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
    Modifies attributes:        TEXT, ROWNO, COLNO, CELLNO, SELECTABLE
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
						block._text = ''
	
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
			self.cell_no       ()
			self.selectables   ()
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
		          ,'CELLNO'
		          ,'SELECTABLE'
		          ]
		rows = []
		for block in self._blocks:
			rows.append ([block._no
			             ,block._type
			             ,block._text
			             ,block.i
			             ,block.j
			             ,block._cell_no
			             ,block._select
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
					
	def selectables(self):
		nos = [block._no for block in self._blocks if block._type in ('phrase','term','transc') and block._text]
		for block in self._blocks:
			if block._no in nos:
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
			# We do not want to mess around with screening quotes that can fail the query
			if block._text:
				tmp.write('update BLOCKS set ROWNO=%d,COLNO=%d,CELLNO=%d,SELECTABLE=%s where NO=%d;' % (block.i,block.j,block._cell_no,block._select,block._no))
			else:
				tmp.write('update BLOCKS set TEXT="%s",ROWNO=%d,COLNO=%d,CELLNO=%d,SELECTABLE=%s where NO=%d;' % (block._text,block.i,block.j,block._cell_no,block._select,block._no))
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()
		return self._query



# This is view-specific and should be recreated each time
''' We assume that sqlite has already sorted DB with 'BLOCK IS NOT 1' and all cell manipulations are completed
    Needs attributes in blocks: NO, TYPE, TEXT, SAMECELL
    Modifies attributes:        POS1, POS2
'''
class Pos:
	
	def __init__(self,data,raw_text):
		self._data     = data     # Sqlite fetch
		self._raw_text = raw_text # Retrieved from the TkinterHTML widget
		self._blocks   = []
		self._query    = ''
		if self._data and self._raw_text:
			self.Success = True
		else:
			self.Success = False
			sh.log.append('Pos.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	def run(self):
		if self.Success:
			self.assign   ()
			self.gen_poses()
			self.dump     ()
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
		          ,'POS1'
		          ,'POS2'
		          ]
		rows = []
		for block in self._blocks:
			rows.append ([block._no
			             ,block._type
			             ,block._text
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
	
	''' We generate positions here according to the text produced by 
	    TkinterHtml's 'widget.text()' command.
	    Peculiarities of the retrieved text:
	    - TkinterHtml adds some empty lines from the top and the bottom;
	      the number of these lines varies each time (and we don't know
	      the rule according to which they are generated)
	    - Each cell occupies a single line
	    - Blocks within a cell are spaced with a single space (except
	      for the blocks having such text as '(')
	    - Each line is stripped
	    - Pos2 of the previous cell and pos1 of the next cell are
	      sometimes equal; this corresponds to the position system
	      used by Tkinter
	    - Duplicate spaces are removed
	'''
	def gen_poses(self):
		last = 0
		for block in self._blocks:
			text = sh.Text(text=block._text.strip()).delete_duplicate_spaces()
			if text:
				search   = sh.Search(text=self._raw_text,search=text)
				search.i = last
				result   = sh.Input(val=search.next(),func_title='Pos.gen_poses').integer()
				if result >= last:
					block._first = result
				else:
					sg.Message('WebFrame.gen_poses',sh.lev_err,'Unable to find "%s"!' % str(text)) # todo: mes
					block._first = last
			else:
				block._first = last
			block._last = block._first + len(text)
			last        = block._last
			
	def dump(self):
		tmp = io.StringIO()
		tmp.write('begin;')
		for block in self._blocks:
			tmp.write('update BLOCKS set POS1=%d,POS2=%d where NO=%d;' % (block._first,block._last,block._no))
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()
		return self._query



''' Creating a selection requires 4 parameters to be calculated:
"self.widget.tag('add','selection',node1,pos1,node2,pos2)"
'node1' usually equals to 'node2' (for a single block this is 
always true because it represents a single tag and therefore 
lies within a single node).
The current node can be calculated using:
"node1,node2 = self.widget.node(True,event.x,event.y)"
The main catch here is that the remaining pos1 and pos2 
are not equal for some reason to positions calculated
for the text generated by 'widget.text()' (_index[1], 
_index[3]). Therefore, we need an additional 'index' 
command.
'''
class Pages:
	
	def __init__(self,obj,blocks):
		self.obj     = obj
		self._blocks = blocks
		self._query  = ''
		if self._blocks and self.obj and hasattr(self.obj,'widget') and hasattr(self.obj,'bbox'):
			self.Success = True
			self.widget = self.obj.widget
		else:
			self.Success = False
			sh.log.append('Pages.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	def create_index(self):
		tmp = io.StringIO()
		tmp.write('begin;')
		for block in self._blocks:
			_index = self.widget.text('index',block._first,block._last)
			if _index:
				_bbox  = self.obj.bbox(_index[0])
				if _bbox:
					# BBOX: man says: The first two integers are the x and y coordinates of the top-left corner of the bounding-box, the later two are the x and y coordinates of the bottom-right corner of the same box. If the node does not generate content, then an empty string is returned.
					tmp.write('update BLOCKS set NODE1="%s",NODE2="%s",OFFPOS1=%d,OFFPOS2=%d,BBOX1=%d,BBOX2=%d,BBOY1=%d,BBOY2=%d where NO=%d;' % (_index[0],_index[2],_index[1],_index[3],_bbox[0],_bbox[2],_bbox[1],_bbox[3],block._no))
				else:
					sh.log.append('Pages.create_index',sh.lev_warn,sh.globs['mes'].empty_input)
			else:
				sh.log.append('Pages.create_index',sh.lev_warn,sh.globs['mes'].empty_input)
		tmp.write('commit;')
		self._query = tmp.getvalue()
		tmp.close()
		return self._query
			
	def debug(self):
		sg.Message('Pages.debug',sh.lev_info,self._query.replace(';',';\n'))
	
	def run(self):
		if self.Success:
			self.create_index()
		else:
			sh.log.append('Pages.run',sh.lev_warn,sh.globs['mes'].canceled)



if __name__ == '__main__':
	import db
	import page    as pg
	import tags    as tg
	import elems   as el
	import mclient as mc
	
	# Modifiable
	source     = 'Online'
	search     = 'working documentation'
	url        = ''
	file       = '/home/pete/tmp/ars/working documentation.txt'
	blacklist  = []
	prioritize = ['Общая лексика']
	collimit   = 10
	file_raw   = '/home/pete/tmp/ars/working documentation - extracted text'
	
	raw_text = sh.ReadTextFile(file=file_raw).get()
	
	timer = sh.Timer(func_title='page, tags, elems, ph_terma, cells')
	timer.start()
	
	mc.ConfigMclient ()
	
	page = pg.Page (source       = source
	               ,lang         = 'English'
	               ,search       = search
	               ,url          = url
	               ,win_encoding = 'windows-1251'
	               ,ext_dics     = []
	               ,file         = file)
	page.run()
	
	tags = tg.Tags(source=source,text=page._page)
	tags.run()
	
	elems = el.Elems (blocks = tags._blocks
	                 ,source = source
	                 ,search = search)
	elems.run()
	
	blocks_db = db.DB()
	blocks_db.fill(elems._data)
	
	blocks_db.request(source=source,search=search)
	
	ph_terma = el.PhraseTerma (dbc    = blocks_db.dbc
	                          ,source = source
	                          ,search = search)
	ph_terma.run()
	
	data       = blocks_db.assign_bp()
	phrase_dic = blocks_db.phrase_dic ()
	
	bp = BlockPrioritize (data       = data
	                     ,source     = source
	                     ,search     = search
	                     ,blacklist  = blacklist
	                     ,prioritize = prioritize
	                     ,phrase_dic = phrase_dic
	                     )
	bp.run()
	blocks_db.update(query=bp._query)
	
	data = blocks_db.assign_cells()
	cells = Cells(data=data,collimit=collimit)
	cells.run()
	blocks_db.update(query=cells._query)
	
	data = blocks_db.assign_pos()
	pos  = Pos(data=data,raw_text=raw_text)
	pos.run()
	blocks_db.update(query=pos._query)
	
	timer.end()
	
	blocks_db.dbc.execute('select NO,DICA,TYPE,TEXT,SAMECELL,PRIORITY,CELLNO,POS1,POS2,SELECTABLE from BLOCKS order by CELLNO,NO')
	blocks_db.print(Selected=1,Shorten=1,MaxRows=200,MaxRow=18)
