#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import re
# В Python 3 не работает просто import urllib, импорт должен быть именно такой, как здесь
import urllib.request, urllib.parse
import html
import pystardict as pd
import shared as sh
import sharedGUI as sg

sep_words_found = 'найдены отдельные слова'
message_board   = 'спросить в форуме'

p1 = '" href'
p2 = '<trash>'
p3 = '"</trash><a href'
p4 = '<a title="'
p5 = '</a>'
p6 = '<span STYLE="color:gray">'
p7 = '<span STYLE="color:black">'
p8 = '">'


class ExtDic:
	
	def __init__(self,path,lang='English',name='External',Block=False,Silent=False):
		self.Silent = Silent
		# Full path without extension (as managed by pystardict)
		self._path  = path
		self._lang  = lang
		self._name  = name
		self.Block  = Block
		self._dic   = None
		self.load()
	
	def load(self):
		sh.log.append('ExtDic.load',sh.lev_info,'Load "%s"' % self._path) # todo: mes
		try:
			self._dic = pd.Dictionary(self._path)
		except:
			sg.Message('ExtDic.load',sh.lev_warn,'Failed to load "%s"!' % self._path,self.Silent) # todo: mes
			
	def get(self,search):
		result = ''
		if self._dic:
			try:
				result = self._dic.get(k=search)
			except:
				sg.Message('ExtDic.get',sh.lev_warn,'Failed to parse "%s"!' % self._path,self.Silent) # todo: mes
		else:
			sh.log.append('ExtDic.get',sh.lev_warn,sh.globs['mes'].empty_input)
		return result



class ExtDics:
	
	def __init__(self,path):
		self._dics    = []
		self._dics_en = []
		self._dics_de = []
		self._dics_es = []
		self._dics_it = []
		self._dics_fr = []
		self._path    = path
		self.dir      = sh.Directory(path=self._path)
		self._files   = self.dir.files()
		self.Success  = self.dir.Success
		self._list()
		self.load()
		
	def get(self,lang='English',search=''):
		if self.Success:
			dics = [dic for dic in self._dics if dic._lang == lang and not dic.Block]
			lst  = []
			for dic in dics:
				tmp = dic.get(search=search)
				if tmp:
					# Set offline dictionary title
					lst.append(p4 + dic._name + p8 + tmp)
			return '\n'.join(lst)
		else:
			sh.log.append('ExtDics.get',sh.lev_warn,sh.globs['mes'].canceled)
	
	def load(self):
		if self.Success:
			sg.objs.waitbox().reset(func_title='ExtDic.load',message='Load offline dictionaries') # todo: mes
			sg.objs._waitbox.show()
			for elem in self._en:
				path = os.path.join(self._path,elem)
				self._dics.append(ExtDic(path=path,lang='English',name=elem))
			for elem in self._de:
				path = os.path.join(self._path,elem)
				self._dics.append(ExtDic(path=path,lang='German',name=elem))
			for elem in self._es:
				path = os.path.join(self._path,elem)
				self._dics.append(ExtDic(path=path,lang='Spanish',name=elem))
			for elem in self._it:
				path = os.path.join(self._path,elem)
				self._dics.append(ExtDic(path=path,lang='Italian',name=elem))
			for elem in self._fr:
				path = os.path.join(self._path,elem)
				self._dics.append(ExtDic(path=path,lang='French',name=elem))
			sg.objs._waitbox.close()
			# Leave only those dictionaries that were successfully loaded
			self._dics = [x for x in self._dics if x._dic]
			sh.log.append('ExtDics.load',sh.lev_info,'%d offline dictionaries have been loaded' % len(self._dics)) # todo: mes
		else:
			sh.log.append('ExtDics.load',sh.lev_warn,sh.globs['mes'].canceled)
	
	def _list(self):
		if self._files:
			self._filenames = set([sh.Path(file).filename().replace('.dict','') for file in self._files])
			# todo: elaborate (make automatical, use language codes)
			# todo: forget 'Ru', check for 1st upper and 2nd lower letters
			self._en        = [elem for elem in self._filenames if 'RuEn' in elem or 'EnRu' in elem]
			self._de        = [elem for elem in self._filenames if 'RuDe' in elem or 'DeRu' in elem]
			self._es        = [elem for elem in self._filenames if 'RuEs' in elem or 'EsRu' in elem]
			self._it        = [elem for elem in self._filenames if 'RuIt' in elem or 'ItRu' in elem]
			self._fr        = [elem for elem in self._filenames if 'RuFr' in elem or 'FrRu' in elem]
		else:
			self._filenames = []
			self._en        = []
			self._de        = []
			self._es        = []
			self._it        = []
			self._fr        = []
	
	def debug(self):
		message = 'English:\n'
		message += '\n'.join(self._en) + '\n\n'
		message += 'German:\n'
		message += '\n'.join(self._de) + '\n\n'
		message += 'French:\n'
		message += '\n'.join(self._fr) + '\n\n'
		message += 'Spanish:\n'
		message += '\n'.join(self._es) + '\n\n'
		message += 'Italian:\n'
		message += '\n'.join(self._it) + '\n\n'
		sg.Message(func='ExtDics.debug',level=sh.lev_info,message=message)



class Page:
	
	def __init__(self,source='All',lang='English',search='SEARCH',url='',win_encoding='windows-1251',ext_dics=[],file=None):
		self._html_raw     = self._page = ''
		self._source       = source
		self._lang         = lang
		self._search       = search
		self._url          = url
		self._win_encoding = win_encoding
		self.ext_dics      = ext_dics
		self._file         = file
		self.Success       = True
		if not self._source or not self._lang or not self._search or not self._win_encoding:
			self.Success   = False
			sh.log.append('Page.__init__',sh.lev_warn,sh.globs['mes'].empty_input)
		
	def run(self):
		self.get                ()
		self.decode_entities    () # HTML specific
		self.invalid            ()
		# An excessive space must be removed after unescaping the page
		self.mt_specific_replace()
		self.common_replace     () # HTML specific
		self.article_not_found  () # HTML specific
		return self._page
		
	# This is due to technical limitations and should be corrected
	def invalid(self):
		# Do this before 'common_replace'. Splitting terms is hindered without this.
		self._page = self._page.replace('</a>;  <a','</a><a')
	
	def article_not_found(self): # HTML specific
		if self._source == 'All' or self._source == 'Online':
			# If separate words are found instead of a phrase, prepare those words only
			if sep_words_found in self._page:
				self._page = self._page.replace(sep_words_found,'')
				if message_board in self._page:
					board_pos = self._page.index(message_board)
				else:
					board_pos = -1
				while p1 in self._page:
					if self._page.index(p1) < board_pos:
						self._page = self._page.replace(p1,p3)
					else:
						break
				while p4 in self._page:
					tag_pos = self._page.index(p4)
					if tag_pos < board_pos:
						self._page = self._page.replace(p4,p2,1)
					else:
						break
				# Вставить sep_words_found перед названием 1-го словаря. Нельзя вставлять его в самое начало ввиду особенностей обработки delete_entries.
				self._page = self._page[:board_pos] + p5 + p6 + sep_words_found + p7
				# Поскольку message_board встречается между вхождениями, а не до них или после них, то обрабатываем его вне delete_entries.
				self._page = self._page.replace(message_board,'')
	
	def common_replace(self): # HTML specific
		self._page = self._page.replace('\r\n','')
		self._page = self._page.replace('\n','')
		self._page = self._page.replace('\xa0',' ')
		while '  ' in self._page:
			self._page = self._page.replace('  ',' ')
		self._page = re.sub(r'\>[\s]{0,1}\<','><',self._page)
		
	def mt_specific_replace(self):
		if self._source == 'All' or self._source == 'Online':
			self._page = self._page.replace('&nbsp;Вы знаете перевод этого выражения? Добавьте его в словарь:','').replace('&nbsp;Вы знаете перевод этого слова? Добавьте его в словарь:','').replace('&nbsp;Требуется авторизация<br>&nbsp;Пожалуйста, войдите на сайт под Вашим именем','').replace('Термины, содержащие ','')
			self._page = re.sub('все формы слов[а]{0,1} \(\d+\)','',self._page)
	
	# Convert HTML entities to a human readable format, e.g., '&copy;' -> '©'
	def decode_entities(self): # HTML specific
		# todo: do we need to check this?
		if self._source == 'All' or self._source == 'Online':
			try:
				self._page = html.unescape(self._page)
			except:
				sh.log.append('Page.decode_entities',sh.lev_err,sh.globs['mes'].html_conversion_failure)
	
	def _get_online(self):
		Got = False
		while not self._page:
			try:
				sh.log.append('Page._get_online',sh.lev_info,'Get online: "%s"' % self._search) # todo: mes
				# Если загружать страницу с помощью "page=urllib.request.urlopen(my_url)", то в итоге получится HTTPResponse, что полезно только для удаления тэгов JavaScript. Поскольку мы вручную удаляем все лишние тэги, то на выходе нам нужна строка.
				self._page = urllib.request.urlopen(self._url).read()
				sh.log.append('Page._get_online',sh.lev_info,sh.globs['mes'].ok % self._search)
				Got = True
			# Too many possible exceptions
			except:
				sh.log.append('Page._get_online',sh.lev_warn,sh.globs['mes'].failed % self._search)
				# For some reason, 'break' does not work here
				if not sg.Message(func='Page._get_online',level=sh.lev_ques,message=sh.globs['mes'].webpage_unavailable_ques).Yes:
					self._page = 'CANCELED'
		if self._page == 'CANCELED':
			self._page = ''
		if Got: # Если страница не загружена, то понятно, что ее кодировку изменить не удастся
			try:
				# Меняем кодировку sh.globs['var']['win_encoding'] на нормальную
				self._page = self._page.decode(self._win_encoding)
			except:
				sg.Message(func='Page._get_online',level=sh.lev_err,message=sh.globs['mes'].wrong_html_encoding)
	
	def _get_offline(self):
		if self.ext_dics:
			self._page = self.ext_dics.get(lang=self._lang,search=self._search)
	
	def disamb_mt(self):
		# This is done to speed up and eliminate tag disambiguation
		try:
			self._page = self._page.replace('<tr>','').replace('</tr>','')
		except TypeError: # Encoding has failed
			self._page = ''
		
	def disamb_sd(self):
		# This is done to speed up and eliminate tag disambiguation
		try:
			self._page = self._page.replace('<i>','').replace('</i>','')
		except TypeError: # Encoding has failed
			self._page = ''
	
	def get(self):
		if not self._page:
			if self._file:
				read = sh.ReadTextFile(file=self._file)
				self._page   = read.get()
				self.Success = read.Success
				self.disamb_sd()
			else:
				page = ''
				if self._source == 'All': # todo: mes
					self._get_online()
					self.disamb_mt()
					page = self._page
					self._get_offline()
					self.disamb_sd()
				elif self._source == 'Online':
					self._get_online()
					self.disamb_mt()
				elif self._source == 'Offline':
					self._get_offline()
					self.disamb_sd()
				else:
					sg.Message('Page.get',sh.lev_err,sh.globs['mes'].unknown_mode % (str(self._source),';'.join(sources)))
				if self._page is None:
					self._page = ''
				if page and self._page:
					self._page += page
				elif page:
					self._page = page
			self._html_raw = self._page
		return self._page


if __name__ == '__main__':
	from time import time
	start_time = time()
	#page = Page(search='filter',url='https://www.multitran.ru/c/M.exe?CL=1&s=filter&l1=1')
	page = Page(search='do',url='https://www.multitran.ru/c/M.exe?CL=1&s=filter&l1=1')
	page.run()
	text = page._page
	sh.log.append('__main__',sh.lev_info,sh.globs['mes'].operation_completed % float(time()-start_time))
	text = text.replace('windows-1251','UTF-8')
	sh.WriteTextFile(file='/home/pete/tmp/ars/do.txt',AskRewrite=0).write(text=text)
