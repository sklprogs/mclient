#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import calendar
import os
import pickle
import re
import shutil
import subprocess
import sys
import time
import tkinter as tk
import tkinter.messagebox as tkmes
import webbrowser
# import urllib does not in Python 3, importing must be as follows:
import urllib.request, urllib.parse
import difflib

from constants import *



# todo: Timing class functions sometimes shows inadequate results
def timer(func_title,func,args=None): # Use tuple to pass multiple arguments
	start_time = time.time()
	if args:
		func_res = func(args)
		log.append(func_title,lev_info,globs['mes'].operation_completed % float(time.time()-start_time))
	else:
		func_res = func()
		log.append(func_title,lev_info,globs['mes'].operation_completed % float(time.time()-start_time))
	return func_res
		
# We do not put this into File class because we do not need to check existence
def rewrite(dest,AskRewrite=True):
	# We return True so we may proceed with writing if the file has not been found
	Confirmed = True
	# We use AskRewrite just to shorten other procedures (to be able to use 'rewrite' silently in the code without ifs)
	if AskRewrite and os.path.isfile(dest):
		# We don't actually need to force rewriting or delete the file before rewriting
		Confirmed = Message(func='rewrite',type=lev_ques,message=globs['mes'].rewrite_ques % dest).Yes
	return Confirmed
	


class OSSpecific:
	
	def __init__(self):
		self._sys = ''
		self._sep = ''
		self.sys()
		self.sep()
	
	def sys(self):
		if not self._sys:
			self._sys = 'unknown'
			sys_plat = sys.platform
			if 'win' in sys_plat:
				self._sys = 'win'
			elif 'lin' in sys_plat:
				self._sys = 'lin'
			elif 'mac' in sys_plat:
				self._sys = 'mac'
		return self._sys
	
	def sep(self):
		if not self._sep:
			self._sep = os.path.sep
		return self._sep

h_os = OSSpecific()		

if h_os.sys() == 'win':
	#http://mail.python.org/pipermail/python-win32/2012-July/012493.html
	_tz = os.getenv('TZ')
	if _tz is not None and '/' in _tz:
		os.unsetenv('TZ')
	# Импортируем win-only модули 
	import pythoncom
	from win32com.shell import shell, shellcon
	import win32com.client, win32api
	if win32com.client.gencache.is_readonly:
		win32com.client.gencache.is_readonly = False
		# under p2exe/cx_freeze the call in gencache to __init__() does not happen so we use Rebuild() to force the creation of the gen_py folder
		# the contents of library.zip\win32com shall be unpacked to exe.win32 - 3.3\win32com
		# See also the section where EnsureDispatch is called.
		win32com.client.gencache.Rebuild()
# Загружается последним ввиду проблем с TZ (см. выше)
import datetime



class Launch:
	
	def __init__(self,target='',Block=False,Silent=False):
		self.target = target
		self.Block = Block
		self.Silent = Silent
		self.h_path = Path(self.target) # Do not shorten, Path is used further
		self.ext = self.h_path.extension().lower()
		self.custom_app = ''
		self.custom_args = []
		if self.target and os.path.exists(self.target): # We do not use the File class because a target can be a directory
			self.TargetExists = True
		else:
			self.TargetExists = False
		
	def _launch(self):
		if self.custom_args:
			try:
				if self.Block: # Block the script till the called program is closed
					subprocess.call(self.custom_args)
				else:
					subprocess.Popen(self.custom_args)
			except:
				Message(func='Launch._launch',type=lev_err,message=globs['mes'].launch_failure2 % str(self.custom_args))
		else:
			log.append('Launch._launch',lev_err,globs['mes'].not_enough_input_data)
	
	def _lin(self):
		try:
			os.system("xdg-open " + self.h_path.escape() + "&")
		except:
			Message(func='Launch._lin',type=lev_err,message=globs['mes'].ext_prog_failure,Silent=self.Silent)
			
	def _mac(self):
		try:
			os.system("open " + self.target)
		except:
			Message(func='Launch._mac',type=lev_err,message=globs['mes'].ext_prog_failure,Silent=self.Silent)
			
	def _win(self):
		try:
			os.startfile(self.target)
		except:
			Message(func='Launch._win',type=lev_err,message=globs['mes'].ext_prog_failure,Silent=self.Silent)
	
	def app(self,custom_app='',custom_args=[]):
		self.custom_app = custom_app
		self.custom_args = custom_args
		if self.custom_app:
			if self.custom_args and len(self.custom_args) > 0:
				self.custom_args = [self.custom_app,self.custom_args[0]]
			else:
				self.custom_args = [self.custom_app]
		self._launch()
	
	def auto(self):
		if self.TargetExists:
			if self.ext == '.txt' and globs['bool']['ForceAltTXTApp']:
				self.custom_app = globs['var'][h_os.sys()]['txt_app']
				self.custom()
			elif self.ext == '.pdf' and globs['bool']['ForceAltPDFApp']:
				self.custom_app = globs['var'][h_os.sys()]['pdf_app']
				self.custom()
			elif os.path.isdir(self.target) and globs['bool']['ForceAltFileMan']:
				self.custom_app = globs['var'][h_os.sys()]['dir_app']
				self.custom()
			else:
				self.default()
		else:
			log.append('Launch.auto',lev_warn,globs['mes'].canceled)

	def custom(self):
		if self.TargetExists:
			self.custom_args = [self.custom_app,self.target]
			self._launch()
		else:
			log.append('Launch.custom',lev_warn,globs['mes'].canceled)
	
	def default(self):
		if self.TargetExists:
			if h_os.sys() == 'lin':
				self._lin()
			elif h_os.sys() == 'mac':
				self._mac()
			elif h_os.sys() == 'win':
				self._win()
		else:
			log.append('Launch.default',lev_warn,globs['mes'].canceled)



class WriteTextFile:
	
	def __init__(self,file,Silent=False,AskRewrite=True,UseLog=True):
		self.file = file
		self.text = ''
		self.Silent = Silent
		self.AskRewrite = AskRewrite
		self.UseLog = UseLog
		self.Success = True
		if not self.file:
			if self.UseLog:
				Message(func='WriteTextFile.__init__',type=lev_err,message=globs['mes'].not_enough_input_data,Silent=self.Silent)
			else:
				print('WriteTextFile.__init__: Not enough input data!')
			self.Success = False
	
	def _write(self,mode='w'):
		if mode == 'w' or mode == 'a':
			if self.UseLog:
				log.append('WriteTextFile._write',lev_info,globs['mes'].writing % self.file)
			try:
				with open(self.file,mode,encoding='UTF-8') as f:
					f.write(self.text)
			except:
				self.Success = False
				if self.UseLog:
					Message(func='WriteTextFile._write',type=lev_err,message=globs['mes'].file_write_failure % self.file,Silent=self.Silent)
				else:
					print('WriteTextFile._write: Unable to write the file!')
		else:
			if self.UseLog:
				Message(func='WriteTextFile._write',type=lev_err,message=globs['mes'].unknown_mode % (str(mode),'a, w'),Silent=False)
			else:
				print('WriteTextFile._write: An unknown mode!')
			
	def append(self,text=''):
		if self.Success:
			self.text = text
			if self.text:
				# todo: In the append mode the file is created if it does not exist, but should we warn the user that we create it from scratch?
				self._write('a')
			else:
				if self.UseLog:
					Message(func='WriteTextFile.append',type=lev_err,message=globs['mes'].not_enough_input_data,Silent=self.Silent)
				else:
					print('WriteTextFile.append: Not enough input data!')
		else:
			if self.UseLog:
				log.append('WriteTextFile.append',lev_warn,globs['mes'].canceled)
	
	def write(self,text=''):
		if self.Success:
			self.text = text
			if self.text:
				if rewrite(self.file,AskRewrite=self.AskRewrite):
					self._write('w')
			else:
				if self.UseLog:
					Message(func='WriteTextFile.write',type=lev_err,message=globs['mes'].not_enough_input_data,Silent=self.Silent)
				else:
					print('WriteTextFile.write: Not enough input data!')
		else:
			if self.UseLog:
				log.append('WriteTextFile.write',lev_warn,globs['mes'].canceled)



class Log:
	
	def __init__(self,Use=True,Write=False,Print=True,Short=False,file=None,TransFunc=False): # TransFunc is ommitted for now
		self.Success = True
		self.file = file
		self.func = 'Log.__init__'
		self.level = lev_info
		self.message = 'Test'
		self.count = 0
		self.Write = Write
		self.Print = Print
		self.Short = Short
		if not Use:
			self.Success = False
		if self.Write:
			self.h_write = WriteTextFile(file=self.file,AskRewrite=False,UseLog=False)
			self.Success = self.h_write.Success
			self.clear()
			
	def clear(self):
		if self.Success:
			self.h_write.write(text=globs['mes'].log_start)
	
	def _write(self):
		self.h_write.append(text='\n%d:%s:%s:%s' % (self.count,self.func,self.level,self.message))
	
	def write(self):
		if self.Success and self.Write:
			if self.Short:
				if self.level == lev_warn or self.level == lev_err:
					self._write()
			else:
				self._write()
	
	def print(self):
		if self.Success:
			if self.Print:
				if self.Short:
					if self.level == lev_warn or self.level == lev_err:
						self._print()
				else:
					self._print()
	
	def _print(self):
		print('%d:%s:%s:%s' % (self.count,self.func,self.level,self.message))
		
	def append(self,func='Log.append',level=lev_info,message='Test'):
		if self.Success:
			if func and level and message:
				self.func = func
				self.level = level
				self.message = message
				self.print()
				self.write()
				self.count += 1
				
if h_os == 'win':
	log = Log(Use=True,Write=False,Print=True,Short=False,file=r'C:\Users\pete\AppData\Local\Temp\log')
else:
	log = Log(Use=True,Write=False,Print=True,Short=False,file='/tmp/log')

				
				
				
class Dic:
	
	def __init__(self,file,Silent=False,Sortable=False):
		self.file = file
		self.Silent = Silent
		self.Sortable = Sortable
		self.h_read = ReadTextFile(self.file,Silent=self.Silent)
		self.reset()
		
	# This is might be needed only for those dictionaries that already may contain duplicates (dictionaries with newly added entries do not have duplicates due to new algorithms)
	def _delete_duplicates(self):
		if self.Success:
			if self.Sortable:
				old = self.lines()
				self._list = list(set(self.list()))
				new = self._lines = len(self._list)
				log.append('Dic._delete_duplicates',lev_info,globs['mes'].entries_deleted % (old-new,old,new))
				self.text = '\n'.join(self._list)
				self._split() # Update original and translation
				self.sort() # After using set(), the original order was lost
			else:
				Message(func='Dic._delete_duplicates',type=lev_warn,message=globs['mes'].non_sortable % self.file,Silent=self.Silent)
		else:
			log.append('Dic._delete_duplicates',lev_warn,globs['mes'].canceled)

	# We can use this as an updater, even without relying on Success
	def _join(self):
		if len(self.orig) == len(self.transl):
			self._lines = len(self.orig)
			self._list = []
			for i in range(self._lines):
				self._list.append(self.orig[i]+'\t'+self.transl[i])
			self.text = '\n'.join(self._list)
		else:
			Message(func='Dic._join',type=lev_warn,message=globs['mes'].wrong_input2,Silent=False)

	# We can use this to check integrity and/or update original and translation lists
	def _split(self):
		if self.get():
			self.Success = True
			self.orig = []
			self.transl = []
			# Building lists takes ~0.1 longer without temporary variables (now self._split() takes ~0.256)
			for i in range(self._lines):
				tmp_lst = self._list[i].split('\t')
				if len(tmp_lst) == 2:
					self.orig.append(tmp_lst[0])
					self.transl.append(tmp_lst[1])
				else:
					self.Success = False
					# i+1: Count from 1
					Message(func='Dic._split',type=lev_warn,message=globs['mes'].incorrect_line % (self.file,i+1,self._list[i]),Silent=self.Silent)
		else:
			self.Success = False
			
	# todo: write a dictionary in an append mode after appending to memory
	# todo: skip repetitions
	def append(self,original,translation):
		if self.Success:
			if original and translation:
				self.orig.append(original)
				self.transl.append(translation)
				self._join()
			else:
				Message(func='Dic.append',type=lev_warn,message=globs['mes'].empty_input,Silent=self.Silent)
		else:
			log.append('Dic.append',lev_warn,globs['mes'].canceled)
	
	# todo: fix: an entry which is only one in a dictionary is not deleted
	def delete_entry(self,entry_no): # Count from 1
		if self.Success:
			entry_no -= 1
			if entry_no >= 0 and entry_no < self.lines():
				del self.orig[entry_no]
				del self.transl[entry_no]
				self._join()
			else:
				Message(func='Dic.delete_entry',type=lev_err,message=globs['mes'].condition_failed % ('0 <= ' + str(entry_no) + ' < %d' % self.lines()),Silent=False)
		else:
			log.append('Dic.append',lev_warn,globs['mes'].canceled)
			
	# todo: Add checking orig and transl (where needed) for a wrapper function
	def edit_entry(self,entry_no,orig,transl): # Count from 1
		if self.Success:
			entry_no -= 1
			if entry_no >= 0 and entry_no < self.lines():
				self.orig[entry_no] = orig
				self.transl[entry_no] = transl
				self._join()
			else:
				Message(func='Dic.delete_entry',type=lev_err,message=globs['mes'].condition_failed % ('0 <= ' + str(entry_no) + ' < %d' % self.lines()),Silent=False)
		else:
			log.append('Dic.append',lev_warn,globs['mes'].canceled)
	
	def get(self):
		if not self.text:
			self.text = self.h_read.load()
		return self.text
		
	def lines(self):
		if self._lines == 0:
			self._lines = len(self.list())
		return self._lines

	def list(self):
		if not self._list:
			self._list = self.get().splitlines()
		return self._list
	
	def reset(self):
		self.text = self.h_read.load()
		self.orig = []
		self.transl = []
		self._list = self.get().splitlines()
		self._lines = len(self._list)
		self._split()
	
	# Sort a dictionary with the longest lines going first
	def sort(self):
		if self.Success:
			if self.Sortable:
				tmp_list = []
				for i in range(len(self._list)):
					tmp_list += [[len(self.orig[i]),self.orig[i],self.transl[i]]]
				tmp_list.sort(key=lambda x: x[0],reverse=True)
				for i in range(len(self._list)):
					self.orig[i] = tmp_list[i][1]
					self.transl[i] = tmp_list[i][2]
					self._list[i] = self.orig[i] + '\t' + self.transl[i]
				self.text = '\n'.join(self._list)
			else:
				Message(func='Dic.sort',type=lev_warn,message=globs['mes'].non_sortable % self.file,Silent=self.Silent)
		else:
			log.append('Dic.sort',lev_warn,globs['mes'].canceled)
	
	def tail(self):
		tail_text = ''
		if self.Success:
			tail_len = globs['int']['tail_len']
			if tail_len > self.lines():
				tail_len = self.lines()
			i = self.lines() - tail_len
			# We count from 1, therefore it is < and not <=
			while i < self.lines():
				# i+1 by the same reason
				tail_text += str(i+1) + ':' + '"' + self.list()[i] + '"\n'
				i += 1
		else:
			log.append('Dic.tail',lev_warn,globs['mes'].canceled)
		return tail_text
	
	def write(self):
		if self.Success:
			WriteTextFile(self.file,self.get(),Silent=self.Silent,AskRewrite=False).write()
		else:
			log.append('Dic.write',lev_warn,globs['mes'].canceled)
	
	

class ReadTextFile:
	
	def __init__(self,file,Silent=False):
		self.file = file
		self.text = ''
		self.Silent = Silent
		self.Success = True
		if self.file and os.path.isfile(self.file):
			pass
		elif not self.file:
			self.Success = False
			Message(func='ReadTextFile.__init__',type=lev_err,message=globs['mes'].not_enough_input_data,Silent=self.Silent)
		elif not os.path.exists(self.file):
			self.Success = False
			Message(func='ReadTextFile.__init__',type=lev_warn,message=globs['mes'].file_not_found % self.file,Silent=self.Silent)
		else:
			self.Success = False
			Message(func='ReadTextFile.__init__',type=lev_err,message=globs['mes'].wrong_input2,Silent=self.Silent)
		
	def _read(self,encoding):
		try:
			with open(self.file,'r',encoding=encoding) as f:
				self.text = f.read()
		# We can handle UnicodeDecodeError here, however, we just handle them all (there could be access errors, etc.)
		except:
			pass

	def delete_bom(self):
		self.text = self.text.replace('\N{ZERO WIDTH NO-BREAK SPACE}','')
	
	# Return the text from memory (or load the file first)
	def get(self):
		if not self.text:
			self.load()
		return self.text

	# Return a number of lines in the file. Returns 0 for an empty file.
	def lines(self):
		return len(self.list())

	def list(self):
		return self.get().splitlines()

	def load(self):
		if self.Success:
			log.append('ReadTextFile.load',lev_info,globs['mes'].loading_file % self.file)
			# We can try to define an encoding automatically, however, this often spoils some symbols, so we just proceed with try-except and the most popular encodings
			self._read('UTF-8')
			if not self.text:
				self._read('windows-1251')
			if not self.text:
				self._read('windows-1252')
			if not self.text:
				# The file cannot be read OR the file is empty (we don't need empty files)
				# todo: Update the message
				self.Success = False
				Message(func='ReadTextFile.load',type=lev_err,message=globs['mes'].file_read_failure % self.file)
			self.delete_bom()
		else:
			log.append('ReadTextFile.load',lev_warn,globs['mes'].canceled)
		return self.text



class AnalyseText:

	def __init__(self,text):
		self.dic = {}
		self.dic['text'] = text
		AnalyseText.words.num = AnalyseText.words_num
		AnalyseText.words.nf = AnalyseText.words_nf
		AnalyseText.words.low = AnalyseText.words_low
		AnalyseText.words.nf.low = AnalyseText.words_nf_low

	def words(self,word_no=-1):
		if not 'words' in self.dic:
			self.dic['words'] = self.dic['text'].split()
		if word_no >= 0 and word_no < len(self.dic['words']):
			return self.dic['words'][word_no]
		else:
			return self.dic['words']

	def words_num(self):
		# Is it worth it? Text length must be static
		if not 'words_num' in self.dic:
			self.dic['words_num'] = len(self.words())
		return self.dic['words_num']

	def words_low(self,word_no=-1):
		if not 'words_low' in self.dic:
			self.dic['words_low'] = []
			for i in range(self.words_num()):
				self.dic['words_low'].append('')
		if word_no >= 0 and word_no < self.words_num():
			self.dic['words_low'][word_no] = self.words(word_no).lower()
			return self.dic['words_low'][word_no]
		else:
			return self.dic['words_low']

	def words_nf(self,word_no=-1):
		if not 'words_nf' in self.dic:
			self.dic['words_nf'] = []
			for i in range(self.words_num()):
				self.dic['words_nf'].append('')
		if word_no >= 0 and word_no < self.words_num():
			self.dic['words_nf'][word_no] = self.words(word_no).replace(',','').replace('.','').replace('!','').replace('?','').replace(':','').replace(';','')
			return self.dic['words_nf'][word_no]
		else:
			return self.dic['words_nf']

	def words_nf_low(self,word_no=-1):
		if not 'words_nf_low' in self.dic:
			self.dic['words_nf_low'] = []
			for i in range(self.words_num()):
				self.dic['words_nf_low'].append('')
		if word_no >= 0 and word_no < self.words_num():
			self.dic['words_nf_low'][word_no] = self.words_nf(word_no).lower()
			return self.dic['words_nf_low'][word_no]
		else:
			return self.dic['words_nf_low']
			
			
			
class Text:
	
	def __init__(self,text,Auto=True):
		self.text = text
		# This can be useful in many cases, e.g. after OCR
		if Auto:
			self.strip_lines()
			self.delete_duplicate_line_breaks()
			self.tabs2spaces()
			self.delete_duplicate_spaces()
			self.yo()
			self.fix_degree_sign()
			self.text = self.text.replace('· ','').replace('• ','') # Getting rid of some useless symbols
			self.delete_space_with_punctuation()
			self.text = self.text.strip() # This is necessary even if we do strip for each line (we need to strip '\n' at the beginning/end)
		
	# todo: check
	def delete_alphabetic_numeration(self):
		my_expr = ' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
		match = re.search(my_expr,self.text)
		while match:
			self.text = self.text.replace(match.group(0),match.group(1))
			match = re.search(my_expr,self.text)
		return self.text
			
	def delete_autotranslate_markers(self):
		self.text = self.text.replace('[[','').replace(']]','').replace('{','').replace('}','').replace('_','')
		return self.text
	
	def delete_embraced_text(self,opening_sym='{',closing_sym='}'):
		opening_parentheses = []
		closing_parentheses = []
		for i in range(len(self.text)):
			if self.text[i] == opening_sym:
				opening_parentheses.append(i)
			elif self.text[i] == closing_sym:
				closing_parentheses.append(i)

		min_val = min(len(opening_parentheses),len(closing_parentheses))

		opening_parentheses = opening_parentheses[::-1]
		closing_parentheses = closing_parentheses[::-1]

		# Ignore non-matching parentheses
		i = 0
		while i < min_val:
			if opening_parentheses[i] >= closing_parentheses[i]:
				del closing_parentheses[i]
				i -= 1
				min_val -= 1
			i += 1

		self.text = list(self.text)
		for i in range(min_val):
			if opening_parentheses[i] < closing_parentheses[i]:
				self.text = self.text[0:opening_parentheses[i]] + self.text[closing_parentheses[i]+1:]
		self.text = ''.join(self.text)
		# Further steps: self.delete_duplicate_spaces(), self.text.strip()
		return self.text
	
	def delete_line_breaks(self): # Use splitlines() first to get rid of Windows- and MacOS-like line breaks
		self.text = self.text.replace('\n',' ')
		return self.text
	
	def delete_duplicate_line_breaks(self):
		while '\n\n' in self.text:
			self.text = self.text.replace('\n\n','\n')
		return self.text
			
	def delete_duplicate_spaces(self):
		while '  ' in self.text:
			self.text = self.text.replace('  ',' ')
		return self.text
			
	# Delete a space and punctuation marks in the end of a line (useful when extracting features with CompareField)
	def delete_end_punc(self,Extended=False):
		if len(self.text) > 0:
			if Extended:
				while self.text[-1] == ' ' or self.text[-1] in punc_array or self.text[-1] in punc_ext_array:
					self.text = self.text[:-1]
			else:
				while self.text[-1] == ' ' or self.text[-1] in punc_array:
					self.text = self.text[:-1]
		else:
			log.append('Text.delete_end_punc',lev_warn,globs['mes'].empty_str_not_supported)
		return self.text
			
	def delete_figures(self):
		self.text = re.sub('\d+','',self.text)
		return self.text
	
	def delete_punctuation(self):
		for i in range(len(punc_array)):
			self.text = self.text.replace(punc_array[i],'')
		for i in range(len(punc_ext_array)):
			self.text = self.text.replace(punc_ext_array[i],'')
		return self.text
		
	def delete_space_with_punctuation(self):
		# Delete duplicate spaces first
		for i in range(len(punc_array)):
			self.text = self.text.replace(' '+punc_array[i],punc_array[i])
		self.text = self.text.replace('“ ','“')
		self.text = self.text.replace(' ”','”')
		self.text = self.text.replace('( ','(')
		self.text = self.text.replace(' )',')')
		self.text = self.text.replace('[ ','[')
		self.text = self.text.replace(' ]',']')
		self.text = self.text.replace('{ ','{')
		self.text = self.text.replace(' }','}')
	
	# Fix possible misprints and OCR errors in the text where a degree sign can be witnessed
	def fix_degree_sign(self):
		my_expr = '[\s]{0,1}[°o][\s]{0,1}[CС](\W)'
		match = re.search(my_expr,self.text)
		while match:
			old = self.text
			self.text = self.text.replace(match.group(0),'°C'+match.group(1))
			match = re.search(my_expr,self.text)
			if old == self.text:
				match = False
		return self.text
	
	# Shorten a title up to a max length
	def prepare_title(self,max_title_len=20,Enclose=True):
		if len(self.text) > max_title_len:
			self.text = self.text[0:max_title_len] + '...'
		if Enclose:
			self.text = '"' + self.text + '"' #'[' + self.text + ']'
		return self.text
	
	# Replace commas or semicolons with line breaks or line breaks with commas
	def split_by_comma(self):
		if (';' in self.text or ',' in self.text) and '\n' in self.text:
			Message(func='Text.split_by_comma',type=lev_warn,message=globs['mes'].comma_ambiguous)
		elif ';' in self.text or ',' in self.text:
			self.text = self.text.replace(',','\n')
			self.text = self.text.replace(';','\n')
			self.strip_lines()
		elif '\n' in self.text:
			self.delete_duplicate_line_breaks()
			self.text.strip() # Delete a line break at the beginning/end
			self.text = self.text.splitlines()
			for i in range(len(self.text)):
				self.text[i] = self.text[i].strip()
			self.text = ', '.join(self.text)
			if self.text.endswith(', '):
				self.text = self.text.strip(', ')
		return self.text
				
	def str2int(self):
		par = 0
		try:
			par = int(self.text)
		except(ValueError,TypeError):
			log.append('Text.str2int',lev_err,globs['mes'].convert_to_int_failure % str(self.text))
		return par
		
	def str2float(self):
		par = 0.0
		try:
			par = float(self.text)
		except(ValueError,TypeError):
			log.append('Text.str2float',lev_err,globs['mes'].convert_to_float_failure % str(self.text))
		return par
	
	def strip_lines(self):
		self.text = self.text.splitlines()
		for i in range(len(self.text)):
			self.text[i] = self.text[i].strip()
		self.text = '\n'.join(self.text)
		return self.text
	
	def tabs2spaces(self):
		self.text = self.text.replace('\t',' ')
		return self.text
		
	def yo(self): # This allows to shorten dictionaries
		self.text = self.text.replace('Ё','Е')
		self.text = self.text.replace('ё','е')
		return self.text

		

class List:
	
	def __init__(self,lst1=[],lst2=[],Silent=False):
		self.lst1 = list(lst1)
		self.lst2 = list(lst2)
		self.Silent = Silent
		
	def lst_in_lst(self,lst1=[],lst2=[]):
		# Local lists are more convenient because of lst_in_lst_loop()
		if not lst1 and not lst2:
			lst1 = list(self.lst1)
			lst2 = list(self.lst2)
		par = [x for x in range(len(lst1)) if lst1[x:x+len(lst2)] == lst2]
		# Пустой список имеет длину 0
		if len(par) > 0:
			par = par[0]
		else:
			par = None
		log.append('List.lst_in_lst',lev_debug,str(par))
		return par
		
	# todo: Is it enough to add up len?
	# Вернуть все координаты списка 2 в списке 1 (строгое совпадение)
	def lst_in_lst_loop(self):
		found_lst = []
		delta = 0
		while True:
			if delta < len(self.lst1):
				par = self.lst_in_lst(self.lst1[delta:],self.lst2)
			else:
				break
			if par == None:
				break
			else:
				pos1 = delta + par
				pos2 = delta + par + len(self.lst2) - 1
				found_lst += [[pos1,pos2]]
				delta = pos2 + 1
		log.append('List.lst_in_lst_loop',lev_debug,str(found_lst))
		return found_lst
	
	# Add a space where necessary and convert to a string
	def space_items(self):
		text = ''
		for i in range(len(self.lst1)):
			if not self.lst1[i] == '':
				if text == '':
					text += self.lst1[i]
				else:
					text += ' ' + self.lst1[i]
		return text
		
	# Сделать списки, указанные на входе, одинаковой длины
	def equalize(self):
		max_range = max(len(self.lst1),len(self.lst2))
		if max_range == len(self.lst1):
			for i in range(len(self.lst1)-len(self.lst2)):
				self.lst2.append('')
		else:
			for i in range(len(self.lst2)-len(self.lst1)):
				self.lst1.append('')
		return(self.lst1,self.lst2)


		
class Time: # We constantly recalculate each value because they depend on each other
	
	def __init__(self,_timestamp=None,pattern='%Y-%m-%d',MondayWarning=True,Silent=False):
		self.reset(_timestamp=_timestamp,pattern=pattern,MondayWarning=MondayWarning,Silent=Silent)
	
	def reset(self,_timestamp=None,pattern='%Y-%m-%d',MondayWarning=True,Silent=False):
		self.Success = True
		self.Silent = Silent
		self.pattern = pattern
		self.MondayWarning = MondayWarning
		self._timestamp = _timestamp
		self._date = self._instance = self._date = self._year = self._month_abbr = self._month_name = ''
		if self._timestamp or self._timestamp == 0: # Prevent recursion
			self.instance()
		else:
			self.todays_date()
	
	def add_days(self,days_delta):
		if self.Success:
			if not self._instance:
				self.instance()
			try:
				self._instance += datetime.timedelta(days=days_delta)
			except:
				self.Success = False
				Message(func='Time.instance',type=lev_warn,message=globs['mes'].time_error)
			self.monday_warning()
		else:
			log.append('Time.add_days',lev_warn,globs['mes'].canceled)

	def date(self):
		if self.Success:
			if not self._instance:
				self.instance()
			try:
				self._date = self._instance.strftime(self.pattern)
			except:
				self.Success = False
				Message(func='Time.instance',type=lev_warn,message=globs['mes'].time_error)
		else:
			log.append('Time.date',lev_warn,globs['mes'].canceled)
		return self._date
		
	def instance(self):
		if self.Success:
			if not self._timestamp:
				self.timestamp()
			try:
				self._instance = datetime.datetime.fromtimestamp(self._timestamp)
			except:
				self.Success = False
				Message(func='Time.instance',type=lev_warn,message=globs['mes'].time_error)
		else:
			log.append('Time.instance',lev_warn,globs['mes'].canceled)
		return self._instance
	
	def timestamp(self):
		if self.Success:
			if not self._date:
				self.date()
			try:
				self._timestamp = time.mktime(datetime.datetime.strptime(self._date,self.pattern).timetuple())
			except:
				self.Success = False
				Message(func='Time.timestamp',type=lev_warn,message=globs['mes'].time_error)
		else:
			log.append('Time.timestamp',lev_warn,globs['mes'].canceled)
		return self._timestamp

	def monday_warning(self):
		if self.Success:
			if not self._instance:
				self.instance()
			if self.MondayWarning and datetime.datetime.weekday(self._instance) == 0:
				Message(func='Time.monday_warning',type=lev_info,message=globs['mes'].monday,Silent=self.Silent)
		else:
			log.append('Time.monday_warning',lev_warn,globs['mes'].canceled)
				
	def month_name(self):
		if self.Success:
			if not self._instance:
				self.instance()
			self._month_name = calendar.month_name[Text(self._instance.strftime("%m"),Auto=False).str2int()]
		else:
			log.append('Time.month_local',lev_warn,globs['mes'].canceled)
		return self._month_name
	
	def month_abbr(self):
		if self.Success:
			if not self._instance:
				self.instance()
			self._month_abbr = calendar.month_abbr[Text(self._instance.strftime("%m"),Auto=False).str2int()]
		else:
			log.append('Time.month_abbr',lev_warn,globs['mes'].canceled)
		return self._month_abbr
	
	def todays_date(self):
		self._instance = datetime.datetime.today()
		
	def year(self):
		if self.Success:
			if not self._instance:
				self.instance()
			try:
				self._year = self._instance.strftime("%Y")
			except:
				self.Success = False
				Message(func='Time.instance',type=lev_warn,message=globs['mes'].time_error)
		else:
			log.append('Time.year',lev_warn,globs['mes'].canceled)
		return self._year
		


class File:
	
	def __init__(self,file,dest=None,Silent=False,AskRewrite=True):
		self.Success = True
		self.Silent = Silent
		self.AskRewrite = AskRewrite
		self.file = file
		self.dest = dest
		if not self.dest: # This will allow to skip some checks for destination
			self.dest = self.file
		self.atime = ''
		self.mtime = ''
		if self.file and os.path.isfile(self.file): # This already checks existence
			if os.path.isdir(self.dest): # If the destination directory does not exist, this will be caught in try-except while copying/moving
				self.dest += os.path.sep + Path(self.file).basename()
		elif not self.file:
			self.Success = False
			Message(func='File.__init__',type=lev_err,message=globs['mes'].empty_input,Silent=self.Silent)
		elif not os.path.exists(self.file):
			self.Success = False
			Message(func='File.__init__',type=lev_warn,message=globs['mes'].file_not_found % self.file,Silent=self.Silent)
		else:
			self.Success = False
			Message(func='File.__init__',type=lev_warn,message=globs['mes'].not_file % self.file,Silent=self.Silent)
			
	def _copy(self):
		Success = True
		log.append('File._copy',lev_info,globs['mes'].copying % (self.file,self.dest))
		try:
			shutil.copyfile(self.file,self.dest)
		except:
			Success = False
			Message(func='File._copy',type=lev_err,message=globs['mes'].file_copy_failure % (self.file,self.dest),Silent=self.Silent)
		return Success
		
	def _move(self):
		Success = True
		log.append('File._move',lev_info,globs['mes'].moving % (self.file,self.dest))
		try:
			shutil.move(self.file,self.dest)
		except:
			Success = False
			Message(func='File._move',type=lev_err,message=globs['mes'].move_failure % (self.file,self.dest),Silent=self.Silent)
		return Success
	
	def access_time(self):
		if self.Success:
			try:
				self.atime = os.path.getatime(self.file)
				# Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
			except:
				Message(func='File.access_time',type=lev_warn,message=globs['mes'].file_date_failure % self.file,Silent=self.Silent)
		else:
			log.append('File.access_time',lev_warn,globs['mes'].canceled)

	def copy(self):
		Success = True
		if self.Success:
			if self.file.lower() == self.dest.lower():
				Message(func='File.copy',type=lev_err,message=globs['mes'].file_copy_failure2 % self.file,Silent=self.Silent)
			elif rewrite(selt.dest,AskRewrite=self.AskRewrite):
				Success = self._copy()
			else:
				log.append('File.copy',lev_info,globs['mes'].canceled_by_user)
		else:
			log.append('File.copy',lev_warn,globs['mes'].canceled)
		return Success
		
	def delete(self):
		Success = True
		if self.Success:
			log.append('File.delete',lev_info,globs['mes'].deleting % self.file)
			try:
				os.remove(self.file)
			except:
				Success = False
				Message(func='File.delete',type=lev_warn,message=globs['mes'].file_del_failure % self.file,Silent=self.Silent)
		else:
			log.append('File.delete',lev_warn,globs['mes'].canceled)
		return Success
		
	def delete_wait(self):
		if self.Success:
			while os.path.exists(self.file) and not self.delete():
				time.sleep(0.3)
		else:
			log.append('File.delete_wait',lev_warn,globs['mes'].canceled)
			
	def modification_time(self):
		if self.Success:
			try:
				self.mtime = os.path.getmtime(self.file)
				# Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
			except:
				Message(func='File.modification_time',type=lev_warn,message=globs['mes'].file_date_failure % self.file,Silent=self.Silent)
		else:
			log.append('File.modification_time',lev_warn,globs['mes'].canceled)
			
	def move(self):
		Success = True
		if self.Success:
			if self.file.lower() == self.dest.lower():
				Message(func='File.move',type=lev_err,message=globs['mes'].move_failure3,Silent=self.Silent)
			elif rewrite(selt.dest,AskRewrite=self.AskRewrite):
				Success = self._move()
			else:
				log.append('File.move',lev_info,globs['mes'].canceled_by_user)
		else:
			log.append('File.move',lev_warn,globs['mes'].canceled)
		return Success
			
	def set_time(self):
		if self.Success:
			if self.atime and self.mtime:
				log.append('File.set_time',lev_info,globs['mes'].file_time_change % (self.file,str((self.atime,self.mtime))))
				try:
					os.utime(self.file,(self.atime,self.mtime))
				except:
					Message(func='File.set_time',type=lev_warn,message=globs['mes'].file_time_change_failure % (self.file,str((self.atime,self.mtime))),Silent=self.Silent)
		else:
			log.append('File.set_time',lev_warn,globs['mes'].canceled)
			
			
			
class Path:
	
	def __init__(self,path):
		self.reset(path)
		
	def _splitpath(self):
		if not self._split:
			self._split = os.path.splitext(self.basename())
		return self._split

	def basename(self):
		if not self._basename:
			self._basename = os.path.basename(self.path)
		return self._basename
		
	def create(self): # This will recursively (by design) create self.path
		Success = True # We actually don't need to fail the class globally
		if self.path:
			if os.path.exists(self.path):
				if os.path.isdir(self.path):
					log.append('Path.create',lev_info,globs['mes'].dir_exists % self.path)
				else:
					Success = False
					Message(func='Path.create',type=lev_warn,message=globs['mes'].invalid_path % self.path)
			else:
				log.append('Path.create',lev_info,globs['mes'].creating_dir % self.path)
				try:
					os.makedirs(self.path)
				except:
					Success = False
					Message(func='Path.create',type=lev_err,message=globs['mes'].dir_creation_failure % self.path)
		else:
			Success = False
			Message(func='Path.create',type=lev_err,message=globs['mes'].not_enough_input_data)
		return Success
	
	def delete_inappropriate_symbols(self): # These symbols may pose a problem while opening files # todo: check whether this is really necessary
		return self.filename().replace("'",'').replace("&",'')
	
	def dirname(self):
		if not self._dirname:
			self._dirname = os.path.dirname(self.path)
		return self._dirname
		
	def escape(self): # In order to use xdg-open, we need to escape spaces first
		return self.path.replace(' ','\ ').replace('(','\(').replace(')','\)')
	
	def extension(self): # with a dot
		if not self._extension:
			if len(self._splitpath()) > 1:
				self._extension = self._splitpath()[1]
		return self._extension
		
	def extract_date(self): # Only for pattern '(YYYY-MM-DD)'
		if not self._date:
			expr = '\((\d\d\d\d-\d\d-\d\d)\)'
			match = re.search(expr,self.filename())
			if match:
				self._date = match.group(1)
		return self._date

	def filename(self):
		if not self._filename:
			if len(self._splitpath()) >= 1:
				self._filename = self._splitpath()[0]
		return self._filename
	
	def reset(self,path,Silent=False):
		self.path = path
		# Unescaped Windows paths must be preceeded with r, e.g., r'C:\1.txt', which will be automatically converted to 'C:\\1.txt'.
		# We can import ntpath, posixpath instead
		# todo: check if paths with \\ are always valid in Windows (do we need to replace this back)
		self.path = self.path.replace('\\','//')
		# We remove a separator from the end, because basename and dirname work differently in this case ('' and the last directory, correspondingly)
		self.path = self.path.rstrip('//')
		self._basename = self._dirname = self._extension = self._filename = self._split = self._date = ''
		self.parts = []
		self.Silent = Silent
		
	def split(self):
		if not self.parts:
			self.parts = self.path.split(h_os.sep())
			i = 0
			tmp_str = ''
			while i < len(self.parts):
				if self.parts[i]:
					self.parts[i] = tmp_str + self.parts[i]
					tmp_str = ''
				else:
					tmp_str += h_os.sep()
					del self.parts[i]
					i -= 1
				i += 1
		return self.parts
		
		

class WriteBinary:
	def __init__(self,file,obj,Silent=False,AskRewrite=False):
		self.Success = True
		self.file = file
		self.Silent = Silent
		self.AskRewrite = AskRewrite
		self.obj = obj
		self.fragm = None
		
	def _write(self,mode='w+b'):
		log.append('WriteBinary._write',lev_info,globs['mes'].writing % self.file)
		if mode == 'w+b' or mode == 'a+b':
			try:
				with open(self.file,mode) as f:
					if mode == 'w+b':
						pickle.dump(self.obj,f)
					elif mode == 'a+b':
						pickle.dump(self.fragm,f)
			except:
				self.Success = False
				Message(func='WriteBinary._write',type=lev_err,message=globs['mes'].file_write_failure % self.file,Silent=self.Silent)
		else:
			Message(func='WriteTextFile._write',type=lev_err,message=globs['mes'].unknown_mode % (str(mode),'w+b, a+b'),Silent=False)
			
	def append(self,fragm):
		self.fragm = fragm
		if self.fragm:
			self._write(mode='a+b')
		else:
			Message(func='WriteBinary.append',type=lev_err,message=globs['mes'].empty_input,Silent=self.Silent)
	
	def write(self):
		if self.obj:
			if rewrite(self.file,AskRewrite=self.AskRewrite):
				self._write(mode='w+b')
			else:
				log.append('WriteBinary.write',lev_info,globs['mes'].canceled_by_user)
		else:
			Message(func='WriteBinary.write',type=lev_err,message=globs['mes'].empty_input,Silent=self.Silent)



class ReadBinary:
	
	def __init__(self,file,Silent=False):
		self.file = file
		self.Silent = Silent
		self.obj = None
		h_file = File(self.file,Silent=self.Silent)
		self.Success = h_file.Success
		
	def _load(self):
		log.append('ReadBinary._load',lev_info,globs['mes'].loading_file % self.file)
		try:
			# AttributeError means that a module using _load does not have a class that was defined while creating the binary
			with open(self.file,'r+b') as f:
				self.obj = pickle.load(f)
		except:
			self.Success = False
			Message(func='ReadBinary._load',type=lev_err,message=globs['mes'].file_read_failure % self.file,Silent=self.Silent)
			
	# todo: load fragments appended to a binary
	def load(self):
		if self.Success:
			self._load()
		else:
			log.append('ReadBinary.load',lev_warn,globs['mes'].canceled)
		return self.obj
			
	def get(self):
		if not self.obj:
			self.load()
		return self.obj



class Message:
	
	def __init__(self,func='MAIN',type=lev_warn,message='Message',Silent=False):
		self.Success = True
		self.Yes = False
		self.func = func
		self.message = message
		self.type = type
		self.Silent = Silent
		if not self.func or not self.message:
			self.Success = False
			log.append('Message.__init__',lev_err,globs['mes'].not_enough_input_data)
		if self.type == lev_info:
			self.info()
		elif self.type == lev_warn:
			self.warning()
		elif self.type == lev_err:
			self.error()
		elif self.type == lev_ques:
			self.question()
		else:
			log.append('Message.__init__',lev_err,globs['mes'].unknown_mode % (str(self.type),lev_info + ', ' + lev_warn + ', ' + lev_err + ', ' + lev_ques))
			
	def error(self):
		if self.Success:
			if not self.Silent:
				tkmes.showerror(self.func+':',self.message) # globs['mes'].err_head
			log.append(self.func,lev_err,self.message)
		else:
			log.append('Message.error',lev_err,globs['mes'].canceled)
			
	def info(self):
		if self.Success:
			if not self.Silent:
				tkmes.showinfo(self.func+':',self.message) # globs['mes'].inf_head
			log.append(self.func,lev_info,self.message)
		else:
			log.append('Message.info',lev_info,globs['mes'].canceled)
	
	def question(self):
		if self.Success:
			self.Yes = tkmes.askokcancel(self.func+':',self.message) # globs['mes'].ques_head
			log.append(self.func,lev_ques,self.message)
		else:
			log.append('Message.question',lev_ques,globs['mes'].canceled)
	
	def warning(self):
		if self.Success:
			if not self.Silent:
				tkmes.showwarning(self.func+':',self.message) # globs['mes'].warn_head
			log.append(self.func,lev_warn,self.message)
		else:
			log.append('Message.warning',lev_warn,globs['mes'].canceled)



class Clipboard:
	
	def __init__(self,root_obj,Silent=False):
		self.h_root = root_obj
		self.Silent = Silent
	
	def copy(self,text,CopyEmpty=True):
		text = str(text)
		if text or CopyEmpty:
			try:
				self.h_root.widget.clipboard_clear()
				self.h_root.widget.clipboard_append(text)
			except tk.TclError:
				# todo: Show a window to manually copy from
				Message(func='Clipboard.copy',type=lev_err,message=globs['mes'].clipboard_failure,Silent=self.Silent)
				
	def paste(self):
		text = ''
		try:
			text = self.h_root.widget.clipboard_get()
		except tk.TclError:
			Message(func='Clipboard.copy',type=lev_err,message=globs['mes'].clipboard_paste_failure,Silent=self.Silent)
		# Further actions: strip, delete double line breaks
		return text



# Do not forget to import this class if it was used to pickle an object
class CreateInstance:
	pass



class Directory:
	
	def __init__(self,path,dest='',Silent=False):
		self.Success = True
		self.Silent = Silent
		if dir:
			self.dir = Path(path).path # Removes trailing slashes if necessary
		else:
			self.dir = ''
		if dest:
			self.dest = Path(dest).path
		else:
			self.dest = self.dir
		self._list = []
		if not os.path.isdir(self.dir):
			self.Success = False
			Message(func='Directory.__init__',type=lev_warn,message=globs['mes'].wrong_input2,Silent=self.Silent)
			
	def delete(self):
		if self.Success:
			log.append('Directory.delete',lev_info,globs['mes'].deleting % self.dir)
			try:
				shutil.rmtree(self.dir)
			except:
				Message(func='Directory.delete',type=lev_warn,message=globs['mes'].dir_del_failure % str(self.dir))
		else:
			log.append('Directory.delete',lev_warn,globs['mes'].canceled)
			
	def list(self):
		if self.Success:
			if not self._list:
				self._list = os.listdir(self.dir)
		else:
			log.append('Directory.list',lev_warn,globs['mes'].canceled)
		return self._list
		
	def copy(self):
		if self.Success:
			if self.dir.lower() == self.dest.lower():
				Message(func='Directory.copy',type=lev_err,message=globs['mes'].copy_failure2 % self.dir,Silent=self.Silent)
			elif os.path.isdir(self.dest):
				Message(func='Directory.copy',type=lev_info,message=globs['mes'].dir_exists % self.dest,Silent=self.Silent)
			else:
				self._copy()
		else:
			log.append('Directory.copy',lev_warn,globs['mes'].canceled)
		
	def _copy(self):
		log.append('Directory._copy',lev_info,globs['mes'].copying % (self.dir,self.dest))
		try:
			shutil.copytree(self.dir,self.dest)
		except:
			self.Success = False
			Message(func='Directory._copy',type=lev_err,message=globs['mes'].copy_failure % (self.dir,self.dest),Silent=self.Silent)



class Config:
	
	def __init__(self,Silent=False):
		self.Success = True
		self.Silent = Silent
	
	def load(self):
		if self.Success:
			for i in range(len(self.sections)):
				for option in globs[self.sections_abbr[i]]:
					new_val = self.sections_func[i](self.sections[i],option)
					if globs[self.sections_abbr[i]][option] != new_val:
						log.append('Config.load_section',lev_info,globs['mes'].key_changed % option)
						self.changed_keys += 1
						globs[self.sections_abbr[i]][option] = new_val
			log.append('Config.load',lev_info,globs['mes'].config_stat % (self.total_keys,self.changed_keys))
		else:
			log.append('Config.load',lev_warn,globs['mes'].canceled)
	
	def check(self):
		if self.Success:
			for i in range(len(self.sections)):
				if config_parser.has_section(self.sections[i]):
					for option in globs[self.sections_abbr[i]]:
						self.total_keys += 1
						if not config_parser.has_option(self.sections[i],option):
							self.Success = False
							self.missing_keys += 1
							self.message += option + '; '
				else:
					self.Success = False
					self.missing_sections += 1
					self.message += self.sections[i] + '; '
			if not self.Success:
				self.message += '\n' + globs['mes'].missing_sections % self.missing_sections
				self.message += '\n' + globs['mes'].missing_keys % self.missing_keys
				self.message += '\n' + globs['mes'].default_config
				Message(func='Config.check',type=lev_warn,message=self.message)
				self._default()
		else:
			log.append('Config.check',lev_warn,globs['mes'].canceled)
	
	def open(self):
		if self.Success:
			try:
				config_parser.read(self.path,'utf-8')
			except:
				Success = False
				Message(func='Config.open',type=lev_warn,message=globs['mes'].invalid_config % self.path,Silent=self.Silent)
		else:
			log.append('Config.open',lev_warn,globs['mes'].canceled)
			


class Online:
	
	def __init__(self,base_str='',search_str='',encoding='UTF-8'):
		self.reset(base_str=base_str,search_str=search_str,encoding=encoding)

	def bytes(self):
		if not self._bytes:
			self._bytes = bytes(self.search_str,encoding=self.encoding)
		return self._bytes 
	
	def browse(self): # Open a URL in a default browser
		try:
			webbrowser.open(self.url(),new=2,autoraise=True)
		except:
			Message(func='Online.browse',type=lev_err,message=globs['mes'].browser_failure % self._url)
				
	# Create a correct online link (URI => URL)
	def url(self):
		if not self._url:
			self._url = self.base_str % urllib.parse.quote(self.bytes())
			log.append('Online.url',lev_debug,str(self._url))
		return self._url
		
	def reset(self,base_str='',search_str='',encoding='UTF-8'):
		self.encoding = encoding
		self.base_str = base_str
		self.search_str = search_str
		self._bytes = self._url = None



class Diff:
	
	def __init__(self,Silent=False):
		self.Silent = Silent
		self.Custom = False
		self.wda_html = globs[h_os.sys()]['tmp_folder'] + h_os.sep() + 'wda.html'
		self.h_wda_write = WriteTextFile(self.wda_html,AskRewrite=False,Silent=self.Silent)
	
	def reset(self,text1,text2,file=None):
		self._diff = ''
		self.text1 = text1
		self.text2 = text2
		if file:
			self.Custom = True
			self.file = file
			self._header = ''
			self.h_write = WriteTextFile(self.file,AskRewrite=True,Silent=self.Silent)
			self.h_path = Path(self.file)
		else:
			self.Custom = False
			self.file = self.wda_html
			self._header = globs['mes'].title_diff
			self.h_write = self.h_wda_write
			
	def diff(self):
		self.text1 = self.text1.split(' ')
		self.text2 = self.text2.split(' ')
		self._diff = difflib.HtmlDiff().make_file(self.text1,self.text2)
		# Avoid a bug in HtmlDiff()
		self._diff = self._diff.replace('charset=ISO-8859-1','charset=UTF-8')
	
	def header(self):
		if self.Custom:
			self._header = self.h_path.basename().replace(self.h_path.extension(),'')
			self._header = '<title>' + self._header + '</title>'
		self._diff = self._diff.replace('<title></title>',self._header) + '\n'
		
	def compare(self):
		self.diff()
		self.header()
		self.h_write.write(self._diff)
		if self.h_write.Success:
			# Cannot reuse the class instance because the temporary file might be missing
			Launch(target=self.file).default()



class Shortcut:
	
	def __init__(self,symlink='',path='',Silent=False):
		self.Success = True
		self.Silent = Silent
		self.path = path
		self.symlink = symlink
		if not self.path and not self.symlink:
			self.Success = False
			Message(func='Shortcut.__init__',type=lev_warn,message=globs['mes'].wrong_input2,Silent=self.Silent)
		
	# http://timgolden.me.uk/python/win32_how_do_i/read-a-shortcut.html
	def _get_win(self):
		link = pythoncom.CoCreateInstance(shell.CLSID_ShellLink,None,pythoncom.CLSCTX_INPROC_SERVER,shell.IID_IShellLink)
		link.QueryInterface(pythoncom.IID_IPersistFile).Load(self.symlink)
		'''	GetPath returns the name and a WIN32_FIND_DATA structure which we're ignoring. The parameter indicates whether shortname, UNC or the "raw path" are to be returned. Bizarrely, the docs indicate that the flags can be combined.
		'''
		self.path,_=link.GetPath(shell.SLGP_UNCPRIORITY)
			
	def _get_unix(self):
		self.path = os.path.realpath(self.symlink)
		
	def get(self):
		if self.Success and not self.path:
			if h_os.sys() == 'win':
				self._get_win()
			else:
				self._get_unix()
		return self.path
		
	def _delete(self):
		log.append('Shortcut._delete',lev_info,globs['mes'].deleting_symlink % self.symlink)
		try:
			os.unlink(symlink)
		except:
			Message(func='Shortcut._delete',type=lev_warn,message=globs['mes'].symlink_removal_failure % self.symlink)
	
	def delete(self):
		if self.Success:
			if os.path.islink(self.symlink):
				self._delete()
		else:
			log.append('Shortcut.delete',lev_warn,globs['mes'].canceled)
	
	def _create_unix(self):
		log.append('Shortcut._create_unix',lev_info,globs['mes'].creating_symlink % self.symlink)
		try:
			os.symlink(self.path,self.symlink)
		except:
			Message(func='Shortcut._create_unix',type=lev_err,message=globs['mes'].symlink_creation_failure % self.symlink)
	
	def create_unix(self):
		self.delete()
		if os.path.exists(self.symlink):
			if os.path.islink(symlink):
				log.append('Shortcut.create_unix',globs['mes'].action_not_required)
			else:
				self.Success = False
				Message(func='Shortcut.create_unix',type=lev_warn,message=globs['mes'].wrong_input2,Silent=self.Silent)
		else:
			self._create_unix()
			
	def _create_win(self):
		log.append('Shortcut._create_win',lev_info,globs['mes'].creating_symlink % self.symlink)
		try:
			# The code will automatically add '.lnk' if necessary
			shell = win32com.client.Dispatch("WScript.Shell")
			shortcut = shell.CreateShortCut(self.symlink)
			shortcut.Targetpath = self.path
			shortcut.save()
		except:
			Message(func='Shortcut._create_win',type=lev_err,message=globs['mes'].symlink_creation_failure % self.symlink)
	
	def create_win(self):
		# Using python 3 and windows (since 2009) it is possible to create a symbolic link, however, this will not be the same as a shortcut (.lnk). Therefore, in case the shortcut is used, os.path.islink() will always return False (not supported) (must use os.path.exists()), however, os.unlink() will work as expected.
		# Do not forget: windows paths must have a double backslash!
		if self.Success:
			if not Path(self.symlink).extension().lower() == '.lnk':
				self.symlink += '.lnk'
			self.delete()
			if os.path.exists(self.symlink):
				log.append('Shortcut.create_win',globs['mes'].action_not_required)
			else:
				self._create_win()
		else:
			log.append('Shortcut.create_win',lev_warn,globs['mes'].canceled)
	
	def create(self):
		if self.Success:
			if h_os.sys() == 'win':
				self.create_win()
			else:
				self.create_unix()
		else:
			log.append('Shortcut.create',lev_warn,globs['mes'].canceled)



class Email:
	
	def __init__(self,email,subject='',message=''):
		self._sep = ',' # Not all mail agents support ';'
		self._email = email # A single address or multiple comma-separated addresses
		self._subject = subject
		self._message = message
		
	def create(self):
		try:
			webbrowser.open('mailto:%s?subject=%s&body=%s' % (self._email,self._subject,self._message))
		except:
			Message(func='TkinterHtmlMod.response_back',type=lev_err,message=globs['mes'].email_agent_failure)
