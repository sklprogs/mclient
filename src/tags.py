#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import copy
import shared as sh
import sharedGUI as sg

transc_orig  = ('[',']','2','3','34','39','40','41','58','65','68','69','73','78','79','80','81','83','84','86','90','97','98','100','101','102','103','104','105','106','107','108','109','110','112','113','114','115','116','117','118','119','120','122')
transc_final = ('[',']','','','ˌ','′','(',')',':','ʌ','ð','ɜ','ı','ŋ','ɔ','ɒ','ɑ','ʃ','θ','ʋ','ʒ','a','b','d','e','f','g','h','i','j','k','l','m','n','p','ə','r','s','t','u','v','w','æ','z')

assert(len(transc_orig) == len(transc_final))


''' Tag patterns:
	•  Dictionary titles:
	     - Multitran:
	         <a title="...">
	     - Stardict:
	         define them manually by the file name
	•  Abbreviations of dictionaries:
	     - Multitran:
	         <a title="Общая лексика" href="m.exe?a=110&t=60148_1_2&sc=0"><i>общ.</i>&nbsp;</a>
	     - Stardict:
	         define them manually by the file name
	•  Terms:
	     - Multitran:
	         <a href="M.exe?..."></a>
	     - Stardict:
	         <dtrn></dtrn>
	         <kref></kref> (in phrases)
	•  Comments:
	     - Multitran:
	         <span STYLE="color:gray"...<
	     - Stardict:
	         <co></co>
	•  Corrections:
	     - Multitran:
	         <span STYLE="color:rgb(60,179,113)">
	•  Users:
	     - Multitran:
	         <a href="M.exe?..."><i>...</i></a>
	           OR without 1st <
	•  Genders:
	     - Multitran:
	         <span STYLE="color:gray"<i>...</i>
	•  Word forms:
	     - Multitran:
	         '<a href="M.exe?a=118&t='
	     - Stardict:
	         <k></k>
	•  Transcription: (a digit in 'width="9"' may vary)
	     - Multitran:
	         '<img SRC="/gif/..." width="9" height="16" align="absbottom">'
	     - Stardict:
	         <tr></tr>
	•  Parts of speech:
	     - Multitran:
	         <em></em>
	     - Stardict:
	         
	'''

# Tag patterns
tag_pattern_del = 	[
						'.exe?a=5&s=AboutMultitran.htm',	# О словаре
						'.exe?a=5&s=FAQ.htm'           ,	# FAQ
						'.exe?a=40'                    ,	# Вход
						'.exe?a=113'                   ,	# Регистрация
						'.exe?a=24&s='                 ,	# Настройки
						'.exe?a=5&s=searches'          ,	# Словари
						'.exe?a=2&l1=1&l2=2'           ,	# Форум
						'.exe?a=44&nadd=1'             ,	# Купить
						'.exe?a=5&s=DownloadFile'      ,	# Скачать
						'.exe?a=45'                    ,	# Отзывы
						'.exe?a=5&s=s_contacts'        ,	# Контакты
						'.exe?a=104&&'                 ,	# Добавить
						'.exe?a=134&s='                ,	# Удалить
						'.exe?a=11&l1='                ,	# Изменить
						'.exe?a=26&&s='                ,	# Сообщить об ошибке
						'.exe?a=136'                   ,	# Оценить сайт
						'&ex=1'                        ,	# только заданная форма слова
						'&order=1'                     ,	# в заданном порядке
						'.exe?a=46&&short_value'       ,	# спросить в форуме
						'.exe?a=5&s=SendPassword'      ,	# я забыл пароль
						'.exe?a=5&s=EnterProblems'			# проблемы со входом или использованием форума?
					]

# Stardict: ST, Multitran: MT
# Full dictionary titles
pdic  = '<a title="'                              # MT

# URLs
purl1 = '<a href="M.exe?'                         # MT
purl2 = '<a href="m.exe?'                         # MT
purl3 = '">'                                      # MT

# Comments
# May also need to look at: '<a href="#start', '<a href="#phrases', '<a href="', '<span STYLE="color:gray"> (ед.ч., мн.ч.)<span STYLE="color:black">'
pcom1 = '<i>'                                     # MT
pcom2 = '<span STYLE="color:gray">'               # MT
pcom3 = '<co>'                                    # ST

# Corrective comments
pcor1 = '<span STYLE="color:rgb(60,179,113)">'    # MT

# Word Forms
pwf1  = '<td bgcolor='                            # MT
pwf2  = '<a href="M.exe?a='                       # MT # Do not shorten
pwf3  = '<a href="m.exe?a='                       # MT # Do not shorten
pwf4  = '<span STYLE=&#34;color:gray&#34;>'       # MT
pwf5  = '&ifp='                                   # MT
pwf6  = '<k>'                                     # ST

# Parts of speech
psp1  = '<em>'                                    # MT

# Terms
ptm1  = 'M.exe?t'                                 # MT # Both terms and word forms
ptm2  = 'm.exe?t'                                 # MT # Both terms and word forms
ptm3  = '<a href="M.exe?&s='                      # MT
ptm4  = '<a href="m.exe?&s='                      # MT
ptm5  = '<a href="M.exe?s='                       # MT
ptm6  = '<a href="m.exe?s='                       # MT
ptm7  = '<dtrn>'                                  # ST

# Terms in the 'Phrases' section
pph1  = '<a href="M.exe?a=3&&s='                  # MT
pph2  = '<a href="m.exe?a=3&&s='                  # MT
pph3  = '<a href="M.exe?a=3&s='                   # MT
pph4  = '<a href="m.exe?a=3&s='                   # MT
pph5  = '<kref>'                                  # ST

# Transcription
ptr1  = '<img SRC="/gif/'                         # MT
ptr2  = '<tr>'                                    # ST
ptr3  = '</tr>'                                   # ST

useful_tags = [pdic,purl1,purl2,pcom1,pcom2,pcom3,pcor1,ptr1,ptr2,pwf6,ptm7,pph5,psp1]



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
		self._urla     = ''
		self._dica     = ''
		self._wforma   = ''
		self._speecha  = ''
		self._transca  = ''
		self._terma    = ''
		self._priority = 0



class AnalyzeTag:
	
	def __init__(self,tag,source='All',pair_root='http://www.multitran.ru/c/M.exe?'):
		self._tag       = tag
		self._pair_root = pair_root
		self._source    = source
		self._cur       = Block()
		self._blocks    = []
		self._elems     = []
		self._block     = ''
		
	def analyze(self):
		self.split()
		self._blocks = [block for block in self._blocks if block.strip()]
		for self._block in self._blocks:
			if self._block.startswith('<'):
				if self.useful() and not self.useless():
					self.phrases ()
					# Phrases and word forms have conflicting tags
					if self._cur._type != 'phrase':
						self.wform()
					self.dic     ()
					self.term    ()
					self.speech  ()
					self.comment ()
					self.url     ()
					self.transc  ()
				else:
					self._cur._type = 'invalid'
			else:
				self.plain()

	def useless(self):
		for tag in tag_pattern_del:
			if tag in self._block:
				return True
				
	def useful(self):
		for tag in useful_tags:
			if tag in self._block:
				return True
	
	def plain(self):
		self._cur._text = self._block
		#note: The analysis must be reset after '</', otherwise, plain text following it will be marked as 'invalid' rather than 'comment'
		if self._cur._type != 'invalid':
			self._elems.append(copy.copy(self._cur))
	
	# Use custom split because we need to preserve delimeters (cannot distinguish tags and contents otherwise)
	def split(self):
		tmp = ''
		for sym in self._tag:
			if sym == '>':
				tmp += sym
				self._blocks.append(tmp)
				tmp = ''
			elif sym == '<':
				if tmp:
					self._blocks.append(tmp)
				tmp = sym
			else:
				tmp += sym
		if tmp:
			self._blocks.append(tmp)
	
	def _comment_mt(self):
		if self._block.startswith(pcom1) or self._block.startswith(pcom2):
			self._cur._type = 'comment'
			
	def _cor_comment_mt(self):
		if self._block.startswith(pcor1):
			self._cur._type = 'correction'
			
	def _comment_sd(self):
		if self._block.startswith(pcom3):
			self._cur._type = 'comment'
			
	def comment(self):
		# The tag has a different meaning in online and offline sources, so we must check the source first
		if self._source == 'All':
			# todo: analyze pages from different sources separately
			self._comment_mt()
			self._comment_sd()
			self._cor_comment_mt()
		elif self._source == 'Online':
			self._comment_mt()
			self._cor_comment_mt()
		elif self._source == 'Offline':
			self._comment_sd()
		else:
			sg.Message('AnalyzeTag.transc',sh.lev_err,sh.globs['mes'].unknown_mode % (str(self._source),'All, Online, Offline'))
	
	def dic(self):
		if self._block.startswith(pdic):
			tmp = self._block.replace(pdic,'',1)
			tmp = re.sub('".*','',tmp)
			if tmp == '' or tmp == ' ':
				sh.log.append('AnalyzeTag.dic',sh.lev_warn,sh.globs['mes'].wrong_tag % tmp)
			else:
				self._cur._type = 'dic'
				self._cur._text = tmp
				self._elems.append(copy.copy(self._cur))
				
	def wform(self):
		cond1 = pwf1 in self._block
		cond2 = pwf2 in self._block and not 'UserName' in self._block
		cond3 = pwf3 in self._block and not 'UserName' in self._block
		cond4 = pwf4 in self._block
		cond5 = pwf5 in self._block and ptm1 in self._block
		cond6 = pwf5 in self._block and ptm2 in self._block
		cond7 = pwf6 in self._block
		if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7:
			self._cur._type  = 'wform'
			
	def phrases(self):
		# Old algorithm: 'startswith'
		cond1 = pph1 in self._block
		cond2 = pph2 in self._block
		cond3 = pph3 in self._block
		cond4 = pph4 in self._block
		cond5 = pph5 in self._block
		if cond1 or cond2 or cond3 or cond4 or cond5:
			self._cur._type = 'phrase'
			
	def term(self):
		cond1 = ptm1 in self._block
		cond2 = ptm2 in self._block
		cond3 = ptm3 in self._block
		cond4 = ptm4 in self._block
		cond5 = ptm5 in self._block
		cond6 = ptm6 in self._block
		cond7 = ptm7 in self._block
		if cond1 or cond2 or cond3 or cond4 or cond5 or cond6 or cond7:
			self._cur._type = 'term'
			
	def url(self):
		cond1 = self._source == 'All'    and self._cur._type == 'term'
		cond2 = self._source == 'All'    and self._cur._type == 'phrase'
		cond3 = self._source == 'Online' and self._cur._type == 'term'
		cond4 = self._source == 'Online' and self._cur._type == 'phrase'
		#note: these additional checks can be shortened if we create a sub-source (e.g., 'Multitran') and check for it
		cond5 = purl1 in self._block
		cond6 = purl2 in self._block
		
		if cond1 or cond2 or cond3 or cond4:
			if cond5 or cond6: # Otherwise, 'self._block' will be returned when there is no match
				self._cur._url = self._block.replace(purl1,'',1).replace(purl2,'',1)
				if self._cur._url.endswith(purl3):
					self._cur._url = self._cur._url.replace(purl3,'')
					#note: adding a non-Multitran online source will require code modification
					self._cur._url = self._pair_root + self._cur._url
				else:
					self._cur._url = ''
				
	def transc(self): # Transcription
		# '<tr>' has a different meaning in online and offline sources, so we must check the source first
		if self._source == 'All':
			self._transc_mt()
			self._transc_sd()
		elif self._source == 'Online':
			self._transc_mt()
		elif self._source == 'Offline':
			self._transc_sd()
		else:
			sg.Message('AnalyzeTag.transc',sh.lev_err,sh.globs['mes'].unknown_mode % (str(self._source),'All, Online, Offline'))
			
			
	def _transc_sd(self): # Stardict
		if ptr2 in self._block:
			_type = 'transc'
			_text = self._block.replace(ptr2,'',1).replace(ptr3,'',1)
			if _text: # Will be empty for non-Stardict sources
				self._cur._type, self._cur._text = _type, _text
				self._elems.append(copy.copy(self._cur))
	
	def _transc_mt(self):
		# Extract a phonetic sign (Multitran-only)
		if ptr1 in self._block:
			tmp = re.sub(r'\.gif.*','',self._block)
			tmp = tmp.replace(ptr1,'')
			if tmp:
				self._cur._type = 'transc'
				try:
					ind = transc_orig.index(tmp)
					self._cur._text = transc_final[ind]
					self._elems.append(copy.copy(self._cur))
				except ValueError:
					sh.log.append('Tags._transc_mt',sh.lev_warn,sh.globs['mes'].wrong_input3 % tmp)
			else:
				log.append('Tags._transc_mt',sh.lev_warn,sh.globs['mes'].empty_input)
				
	def speech(self):
		if psp1 in self._block:
			self._cur._type = 'speech'



class Tags:
	
	def __init__(self,text,source='All',pair_root='http://www.multitran.ru/c/M.exe?'):
		self._text      = text
		self._source    = source
		self._pair_root = pair_root
		self._tags      = []
		self._blocks    = []
		
	# Split the text by closing tags
	# To speed up, we remove closing tags right away
	def tags(self):
		if not self._tags:
			Ignore = False
			tmp = ''
			for i in range(len(self._text)):
				if self._text[i] == '<':
					if i < len(self._text) - 1 and self._text[i+1] == '/':
						Ignore = True
						if tmp:
							self._tags.append(tmp)
							tmp = ''
					else:
						tmp += self._text[i]
				elif self._text[i] == '>':
					if Ignore:
						Ignore = False
					else:
						tmp += self._text[i]
				elif not Ignore:
					tmp += self._text[i]
			# Should be needed only for broken tags
			if tmp:
				self._tags.append(tmp)
		return self._tags
			
	def debug_tags(self):
		message = ''
		for i in range(len(self._tags)):
			message += '%d:%s\n' % (i,self._tags[i])
		#sg.Message('Tags.debug_tags',sh.lev_info,message)
		words = sh.Words(text=message,OrigCyr=1,Auto=0)
		words.sent_nos()
		sg.objs.txt(words=words).reset_data()
		sg.objs._txt.title('Tags.debug_tags:')
		sg.objs._txt.insert(text=message)
		sg.objs._txt.show()
		
	def debug_blocks(self,Shorten=1,MaxRow=20,MaxRows=20):
		print('\nTags.debug_blocks (Non-DB blocks):')
		headers = [
		            'TYPE'              ,
		            'TEXT'              ,
		            'URL'               ,
		            'SAMECELL'          
		          ]
		rows = []
		for block in self._blocks:
			rows.append (
			              [
			        block._type         ,
			        block._text         ,
			        block._url          ,
			        block._same         
			              ]
			            )
		sh.Table (
		            headers             = headers                             ,
		            rows                = rows                                ,
		            Shorten             = Shorten                             ,
		            MaxRow              = MaxRow                              ,
		            MaxRows             = MaxRows
		         ).print()
		
	def debug(self,Shorten=1,MaxRow=20,MaxRows=20):
		self.debug_tags   ()
		self.debug_blocks (Shorten=Shorten,MaxRow=MaxRow,MaxRows=MaxRows)
		
	def blocks(self):
		if not self._blocks:
			for tag in self._tags:
				analyze = AnalyzeTag (tag       = tag
				                     ,source    = self._source
				                     ,pair_root = self._pair_root
				                     )
				analyze.analyze()
				lst = analyze._elems
				for i in range(len(lst)):
					if i > 0:
						lst[i]._same = 1
					else:
						lst[i]._same = 0
				self._blocks += lst
		return self._blocks
		
	def run(self):
		self.tags          ()
		self.blocks        ()
		#self.debug_tags   ()
		#self.debug_blocks ()



if __name__ == '__main__':
	import page as pg
	
	# Modifiable
	source = 'Online'
	search = 'preceding'
	file   = '/home/pete/tmp/ars/preceding.txt'
	
	page = pg.Page (source = source
	               ,search = search
	               ,file   = file
	               )
	page.run()
	
	timer = sh.Timer(func_title='Page')
	timer.start()
	tags = Tags(source=source,text=page._page)
	tags.run()
	timer.end()
	#tags.debug_tags   ()
	tags.debug_blocks (MaxRow=30,MaxRows=100)
