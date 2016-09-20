#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from constants import *
from shared import Message, WriteTextFile, Launch, List, Config, Clipboard, Path, Online, ReadTextFile, Email, timer, log, globs, h_os, CreateInstance, h_lang
from sharedGUI import create_binding, Button, Root, Top, Entry, WidgetShared, Frame, TextBox, ListBox, dialog_save_file, OptionMenu
import copy
# В Python 3 не работает просто import urllib, импорт должен быть именно такой, как здесь
import urllib.request, urllib.parse
import html
import os, sys, platform
import tkinter as tk
from tkinter import ttk
from io import StringIO
import sqlite3
import pickle

class log:
	def append(self,*args):
		pass
		
product = 'MClient'
version = '4.7'



class ConfigMclient(Config):
	
	def __init__(self):
		super().__init__()
		self.sections = [SectionBooleans,SectionIntegers,SectionVariables]
		self.sections_abbr = [SectionBooleans_abbr,SectionIntegers_abbr,SectionVariables_abbr]
		self.sections_func = [config_parser.getboolean,config_parser.getint,config_parser.get]
		self.message = globs['mes'].missing_config + '\n'
		self.total_keys = 0
		self.changed_keys = 0
		self.missing_keys = 0
		self.missing_sections = 0
		# Create these keys before reading the config
		globs['bin_dir'] = Path(os.path.realpath(sys.argv[0])).dirname()
		self.path = globs['bin_dir'] + os.path.sep + 'mclient.cfg'
		self.reset()
		h_read = ReadTextFile(self.path,Silent=self.Silent)
		self.text = h_read.get()
		self.Success = h_read.Success
		self._default()
		if os.path.exists(self.path):
			self.open()
		else:
			self.Success = False
		self.check()
		self.load()
		self.additional_keys()
			
	def _default(self):
		globs['bool'].update({
			'AutoCloseSpecSymbol':False,
			'CopyTermsOnly':True,
			'ExploreMismatch':True,
			'Iconify':True,
			'SelectTermsOnly':True,
			'ShortHistory':False
			             })
		#---------------------------------------------------
		globs['int'].update({
			'default_button_size':36,
			'default_hint_border_width':1,
			'default_hint_delay':800,
			'default_hint_height':40,
			'default_hint_width':280,
			'font_comments_size':3,
			'font_dics_size':4,
			'font_speech_size':4,
			'font_terms_size':4
			              })
		#---------------------------------------------------
		globs['var'].update({
			'bind_add_cell':'<Control-Insert>',
			'bind_clear_history_alt':'<Control-Shift-Delete>',
			'bind_clear_history':'<ButtonRelease-3>',
			'bind_clear_search_field':'<ButtonRelease-3>',
			'bind_copy_article_url':'<Shift-F7>',
			'bind_copy_history':'<ButtonRelease-3>',
			'bind_copy_sel_alt':'<Control-KP_Enter>',
			'bind_copy_sel_alt2':'<ButtonRelease-3>',
			'bind_copy_sel':'<Control-Return>',
			'bind_copy_url':'<Control-F7>',
			'bind_delete_cell':'<Control-Delete>',
			'bind_define':'<Control-d>',
			'bind_go_back':'<Alt-Left>',
			'bind_go_forward':'<Alt-Right>',
			'bind_go_search_alt':'<KP_Enter>',
			'bind_go_search':'<Return>',
			'bind_go_url':'<Button-1>',
			'bind_iconify':'<ButtonRelease-2>',
			'bind_move_down':'<Down>',
			'bind_move_left':'<Left>',
			'bind_move_line_end':'<End>',
			'bind_move_line_start':'<Home>',
			'bind_move_page_down':'<Next>',
			'bind_move_page_up':'<Prior>',
			'bind_move_right':'<Right>',
			'bind_move_text_end':'<Control-End>',
			'bind_move_text_start':'<Control-Home>',
			'bind_move_up':'<Up>',
			'bind_next_pair':'<F8>',
			'bind_next_pair_alt':'<Control-l>',
			'bind_prev_pair':'<Shift-F8>',
			'bind_prev_pair_alt':'<Control-L>',
			'bind_open_in_browser_alt':'<Control-b>',
			'bind_open_in_browser':'<F7>',
			'bind_paste_search_field':'<ButtonRelease-2>',
			'bind_quit_now_alt':'<F10>',
			'bind_quit_now':'<Control-q>',
			'bind_re_search_article':'<Control-F3>',
			'bind_reload_article_alt':'<Control-r>',
			'bind_reload_article':'<F5>',
			'bind_save_article_alt':'<Control-s>',
			'bind_save_article':'<F2>',
			'bind_search_article_backward':'<Shift-F3>',
			'bind_search_article_forward':'<F3>',
			'bind_show_about':'<F1>',
			'bind_spec_symbol':'<Control-e>',
			'bind_toggle_history_alt':'<Control-h>',
			'bind_toggle_history':'<F4>',
			'bind_toggle_view':'<F6>',
			'bind_toggle_view_alt':'<Control-V>',
			'color_comments':'gray',
			'color_dics':'cadet blue',
			'color_speech':'red',
			'color_terms_sel_bg':'cyan',
			'color_terms_sel_fg':'black',
			'color_terms':'black',
			'default_hint_background':'#ffffe0',
			'default_hint_border_color':'navy',
			'default_hint_direction':'top',
			'font_comments_family':'Mono',
			'font_dics_family':'Arial',
			'font_history':'Sans 12',
			'font_speech_family':'Arial',
			'font_style':'Sans 14',
			'font_terms_sel':'Sans 14 bold italic',
			'font_terms_family':'Serif',
			'icon_clear_history':'icon_36x36_clear_history.gif',
			'icon_clear_search_field':'icon_36x36_clear_search_field.gif',
			'icon_define':'icon_36x36_define.gif',
			'icon_go_back_off':'icon_36x36_go_back_off.gif',
			'icon_go_back':'icon_36x36_go_back.gif',
			'icon_go_forward_off':'icon_36x36_go_forward_off.gif',
			'icon_go_forward':'icon_36x36_go_forward.gif',
			'icon_go_search':'icon_36x36_go_search.gif',
			'icon_mclient':'icon_64x64_mclient.gif',
			'icon_open_in_browser':'icon_36x36_open_in_browser.gif',
			'icon_paste':'icon_36x36_paste.gif',
			'icon_quit_now':'icon_36x36_quit_now.gif',
			'icon_reload':'icon_36x36_reload.gif',
			'icon_repeat_sign_off':'icon_36x36_repeat_sign_off.gif',
			'icon_repeat_sign':'icon_36x36_repeat_sign.gif',
			'icon_repeat_sign2_off':'icon_36x36_repeat_sign2_off.gif',
			'icon_repeat_sign2':'icon_36x36_repeat_sign2.gif',
			'icon_save_article':'icon_36x36_save_article.gif',
			'icon_search_article':'icon_36x36_search_article.gif',
			'icon_show_about':'icon_36x36_show_about.gif',
			'icon_spec_symbol':'icon_36x36_spec_symbol.gif',
			'icon_toggle_history':'icon_36x36_toggle_history.gif',
			'icon_toggle_view_hor':'icon_36x36_toggle_view_hor.gif',
			'icon_toggle_view_ver':'icon_36x36_toggle_view_ver.gif',
			'icon_watch_clipboard_off':'icon_36x36_watch_clipboard_off.gif',
			'icon_watch_clipboard_on':'icon_36x36_watch_clipboard_on.gif',
			'repeat_sign':'!',
			'repeat_sign2':'!!',
			'spec_syms':'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ',
			'ui_lang':'ru',
			'web_search_url':'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s',
			'win_encoding':'windows-1251'
				           })
	
	def reset(self):
		globs['bool'] = {}
		globs['float'] = {}
		globs['int'] = {}
		globs['var'] = {}
		
	def additional_keys(self):
		for key in globs['var']:
			if globs['var'][key].endswith('.gif'):
				old_val = globs['var'][key]
				globs['var'][key] = globs['bin_dir'] + os.path.sep + 'resources' + os.path.sep + globs['var'][key]
				log.append('ConfigMclient.additional_keys',lev_debug,'%s -> %s' % (old_val,globs['var'][key]))



ConfigMclient()
h_lang.set()

if h_os.sys() == 'win':
	import kl_mod_win as kl_mod
	import pythoncom
else:
	import kl_mod_lin as kl_mod

globs['_tkhtml_loaded'] = False
# todo: del
globs['bool']['DryRun'] = False # True
globs['dry_count'] = 0
globs['geom_top'] = {}
globs['top'] = {}

online_url_root = 'http://www.multitran.ru/c/m.exe?'
online_url_safe = 'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%ED%E5%E2%E5%F0%ED%E0%FF+%F1%F1%FB%EB%EA%E0'
welcome_url = 'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC%21'
welcome_str = 'Добро пожаловать!'
sep_words_found = 'найдены отдельные слова'
message_board = 'спросить в форуме'
nbspace = ' '

pairs = ('ENG <=> RUS','DEU <=> RUS','SPA <=> RUS','FRA <=> RUS','NLD <=> RUS','ITA <=> RUS','LAV <=> RUS','EST <=> RUS','AFR <=> RUS','EPO <=> RUS','RUS <=> XAL','XAL <=> RUS','ENG <=> DEU','ENG <=> EST')
online_dic_urls = ('http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=3&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=5&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=4&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=24&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=23&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=27&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=26&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=31&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=34&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=2&l2=35&s=%s','http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s')

# Tag patterns
tag_pattern1 = '<a title="'
tag_pattern2 = '<a href="m.exe?'
tag_pattern3 = '<i>'
tag_pattern4 = '</i>'
tag_pattern5 = '<span STYLE="color:gray">'
tag_pattern6 = '<span STYLE="color:black">'
tag_pattern7 = '</a>'
tag_pattern8 = '">'
tag_pattern9 = '<span STYLE="color:rgb(60,179,113)">'
tag_pattern10 = '</td>'
# Возможно '... " href', или '" href', если перевод вмещается полностью
tag_pattern11 = '" href'
tag_pattern12 = '<trash>'
tag_pattern13 = '"</trash><a href'
tag_pattern14 = 'm.exe?a=118&t=' # Части речи # Полностью: '<a href="m.exe?a=118&t='

# 'спросить в форуме' не удается обработать в этом списке, поэтому обрабатываю его отдельно
delete_entries = ['Вход','Регистрация','Сообщить об ошибке','Изменить','Удалить','Добавить']

instances = {}

def init_inst(name):
	if name in instances and instances[name]:
		pass
	elif name == 'root':
		instances[name] = Root()
		instances[name].close()
	elif name == 'top':
		instances[name] = Top(init_inst('root'),Maximize=True) #,DestroyRoot=True
		instances[name].icon(globs['var']['icon_mclient'])
	elif name == 'top_entry':
		instances[name] = Top(init_inst('root'))
		#instances[name].close()
	elif name == 'top_textbox':
		instances[name] = Top(init_inst('root'),Maximize=True)
		instances[name].close()
	elif name == 'entry':
		instances[name] = Entry(init_inst('top_entry'))
		instances[name].icon(globs['var']['icon_mclient'])
		instances[name].title(globs['mes'].search_str)
	elif name == 'textbox':
		instances[name] = TextBox(init_inst('top_textbox'))
	elif name == 'clipboard':
		instances[name] = Clipboard(init_inst('root'))
	elif name == 'online':
		instances[name] = Online()
	elif name == 'about':
		instances[name] = About()
	return instances[name]



class Request:
	
	def __init__(self):
		self.reset()
		
	def reset(self):
		self._online = self._source = self._dic = self._search = self._url = self._collimit = self._priority = self._view = self._cells = self._elems = self._html = self._html_raw = self._text = self._moves = None
	
	def update(self):
		self._cells = self._html = self._text = self._moves = None
	
	def new(self): # A completely new request
		self._cells = self._elems = self._html_raw = self._html = self._text = self._moves = None
	
	def online(self):
		if self._online is None:
			self._online = True
		return self._online
		
	def source(self):
		if self._source is None:
			self._source = 'Multitran'
		return self._source
		
	def dic(self):
		if self._dic is None:
			self._dic = 'Main'
		return self._dic
		
	def search(self):
		if self._search is None:
			self._search = 'Добро пожаловать!'
		return self._search
		
	def url(self):
		if self._url is None:
			self._url = 'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC%21'
		return self._url
		
	def collimit(self):
		if self._collimit is None:
			self._collimit = 5
			# todo: del
			#self._collimit = globs['collimit']
		return self._collimit
		
	def view(self):
		if self._view is None:
			self._view = 0
			# todo: del
			#self._view = globs['view']
		return self._view
		
	def priority(self):
		if self._priority is None:
			self._priority = False
			# todo: del
			#self._priority = globs['priority']
		return self._priority
		
	def cells(self):
		if self._cells is None:
			Cells()
		return self._cells
		
	def elems(self):
		if self._elems is None:
			Elems()
		return self._elems
		
	def html(self):
		if self._html is None:
			HTML()
		return self._html
		
	def html_raw(self):
		if self._html_raw is None:
			Page()
		return self._html_raw
		
	def text(self):
		if self._text is None:
			Page()
		return self._text
		
	# todo: fix: _moves is always not None
	def moves(self):
		if self._moves is None:
			Moves()
		return self._moves



class DB: # Requires h_request global
	
	def __init__(self):
		self.db_con = sqlite3.connect(':memory:')
		self.db = self.db_con.cursor()
		self.reset()
		
	def reset(self):
		self._count = 0
		self._id = -1
		self.db.executescript('drop table if exists INFO;')
		self.db.execute('create table INFO (ONLINE bool,SOURCE text,DIC text,SEARCH text,URL text,ID integer,COLLIMIT integer,VIEW integer,PRIORITY integer,ELEMS pickle,CELLS pickle,HTML text,HTML_RAW text,TEXT text,MOVES pickle)')
		
	def index_add(self):
		if self._id < self._count - 1:
			self._id += 1
		else:
			self._id = 0
	
	def index_subtract(self):
		if self._id > 0:
			self._id -= 1
		else:
			self._id = self._count - 1
		
	# orphant, equivalent of '_count'
	def len(self):
		self.db.execute('select Count(*) from INFO')
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def searches(self):
		self.db.execute('select SEARCH from INFO order by ID')
		searches = self.db.fetchall()
		for i in range(len(searches)):
			searches[i] = searches[i][0]
		return searches
	
	def copy(self):
		h_request._online = self.online()
		h_request._source = self.source()
		h_request._dic = self.dic()
		h_request._search = self.search()
		h_request._url = self.url()
		h_request._collimit = self.collimit()
		h_request._view = self.view()
		h_request._priority = self.priority()
		h_request._html_raw = self.html_raw()
		h_request._elems = self.elems()
		h_request._cells = self.cells()
		h_request._moves = self.moves()
		h_request._html = self.html()
		h_request._text = self.text()
		
	def copy_ahead(self):
		h_request._search = self.search()
		h_request._url = self.url()
		h_request._html_raw = self.html_raw() # Do not re-download the page
		h_request._elems = self.elems()
	
	def collimit(self):
		self.db.execute('select COLLIMIT from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def view(self):
		self.db.execute('select VIEW from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def priority(self):
		self.db.execute('select PRIORITY from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def online(self):
		self.db.execute('select ONLINE from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def url(self):
		self.db.execute('select URL from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def search(self):
		self.db.execute('select SEARCH from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def dic(self):
		self.db.execute('select DIC from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def source(self):
		self.db.execute('select SOURCE from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def moves(self):
		self.db.execute('select MOVES from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return pickle.loads(result)
	
	def cells(self):
		self.db.execute('select CELLS from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return pickle.loads(result)
	
	def elems(self):
		self.db.execute('select ELEMS from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return pickle.loads(result)
	
	def text(self):
		self.db.execute('select TEXT from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def html_raw(self):
		self.db.execute('select HTML_RAW from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def html(self):
		self.db.execute('select HTML from INFO where ID=?',(self._id,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def add(self):
		self.db.execute('insert into INFO values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[h_request.online(),h_request.source(),h_request.dic(),h_request.search(),h_request.url(),self._count,h_request.collimit(),h_request.view(),h_request.priority(),pickle.dumps(h_request.elems()),pickle.dumps(h_request.cells()),h_request.html(),h_request.html_raw(),h_request.text(),pickle.dumps(h_request.moves())])
		self.db_con.commit()
		self._id += 1
		self._count += 1
	
	def prev(self):
		self.db.execute('select SEARCH from INFO where ID=?',(self._count - 1,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
			
	def preprev(self):
		self.db.execute('select SEARCH from INFO where ID=?',(self._count - 2,))
		result = self.db.fetchone()
		if result:
			result = result[0]
			return result
	
	def search_full(self):
		if h_request.online():
			self.db.execute('select ID from INFO where ONLINE=? and SOURCE=? and DIC=? and URL=? and COLLIMIT=? and VIEW=? and PRIORITY=?',(h_request.online(),h_request.source(),h_request.dic(),h_request.url(),h_request.collimit(),h_request.view(),h_request.priority(),))
		else:
			self.db.execute('select ID from INFO where ONLINE=? and SOURCE=? and DIC=? and SEARCH=? and COLLIMIT=? and VIEW=? and PRIORITY=?',(h_request.online(),h_request.source(),h_request.dic(),h_request.search(),h_request.collimit(),h_request.view(),h_request.priority(),))
		result = self.db.fetchone()
		if result:
			self._id = result[0]
			log.append('DB.search_full',lev_info,globs['mes'].id_full_match % self._id)
			self.copy()
			return True
	
	def search_part(self):
		if not self.search_full():
			if h_request.online():
				self.db.execute('select ID from INFO where ONLINE=? and SOURCE=? and DIC=? and URL=?',(h_request.online(),h_request.source(),h_request.dic(),h_request.url(),))
			else:
				self.db.execute('select ID from INFO where ONLINE=? and SOURCE=? and DIC=? and SEARCH=?',(h_request.online(),h_request.source(),h_request.dic(),h_request.search(),))
			result = self.db.fetchone()
			if result:
				self._id = result[0]
				log.append('DB.search_part',lev_info,globs['mes'].id_match % self._id)
				self.copy_ahead()
			else:
				self.add()
			
	def print(self):
		self.db.execute("select * from INFO")
		print(self.db.fetchall())
		
	def close(self):
		self.db_con.close()



class HTML:
	
	def __init__(self):
		if h_request._html:
			log.append('HTML.__init__',lev_debug,globs['mes'].action_not_required)
		else:
			log.append('HTML.__init__',lev_info,globs['mes'].create_object)
			Cells()
			self.html()
	
	def _comment(self):
		if h_request._cells[self.i][self.j].comment:
			self.output.write('<i><font face="')
			self.output.write(globs['var']['font_comments_family'])
			self.output.write('" size="')
			self.output.write(str(globs['int']['font_comments_size']))
			self.output.write('" color="')
			self.output.write(globs['var']['color_comments'])
			self.output.write('">')
			self.output.write(h_request._cells[self.i][self.j].comment)
			self.output.write('</i></font></td>')
	
	def _speech(self):
		if h_request._cells[self.i][self.j].speech:
			self.output.write('<font face="')
			self.output.write(globs['var']['font_speech_family'])
			self.output.write('" color="')
			self.output.write(globs['var']['color_speech'])
			self.output.write('" size="')
			self.output.write(str(globs['int']['font_speech_size']))
			self.output.write('"><b>')
			self.output.write(h_request._cells[self.i][self.j].speech)
			self.output.write('</b></font>')
		
	def _dic(self):
		if h_request._cells[self.i][self.j].dic:
			self.output.write('<font face="')
			self.output.write(globs['var']['font_dics_family'])
			self.output.write('" color="')
			self.output.write(globs['var']['color_dics'])
			self.output.write('" size="')
			self.output.write(str(globs['int']['font_dics_size']))
			self.output.write('"><b>')
			self.output.write(h_request._cells[self.i][self.j].dic)
			self.output.write('</b></font>')
		
	def _term(self):
		if h_request._cells[self.i][self.j].term:
			self.output.write('<font face="')
			self.output.write(globs['var']['font_terms_family'])
			self.output.write('" color="')
			self.output.write(globs['var']['color_terms'])
			self.output.write('" size="')
			self.output.write(str(globs['int']['font_terms_size']))
			self.output.write('">')
			self.output.write(h_request._cells[self.i][self.j].term)
			self.output.write('</font>')
	
	def html(self):
		# Default Python string concatenation is too slow, so we use this module instead
		self.output = StringIO()
		self.output.write('<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"><table>')
		for i in range(len(h_request._cells)):
			self.i = i
			# todo: this doesn't work, why?
			self.output.write('<col width="130">')
			self.output.write('<tr>')
			for j in range(len(h_request._cells[i])):
				self.j = j
				if h_request._cells[i][j].dic:
					self.output.write('<td align="center">')
				else:
					self.output.write('<td>')
				self._speech()
				self._dic()
				self._term()
				self._comment()
			self.output.write('</tr>')
		self.output.write('</table></body></html>')
		h_request._html = self.output.getvalue()
		self.output.close()
		
		

class Page:
	
	def __init__(self):
		self._page = ''
		if globs['bool']['DryRun']:
			if globs['dry_count'] == 0:
				self.example()
			elif globs['dry_count'] == 1:
				self.example2()
			else:
				self.example3()
			globs['dry_count'] += 1
		else:
			self.get()
		self.decode_entities() # HTML specific
		self.common_replace() # HTML specific
		self.article_not_found() # HTML specific
		
	def article_not_found(self): # HTML specific
		# If separate words are found instead of a phrase, prepare those words only
		if sep_words_found in self._page:
			self._page = self._page.replace(sep_words_found,'')
			if message_board in self._page:
				board_pos = self._page.index(message_board)
			else:
				board_pos = -1
			while tag_pattern11 in self._page:
				if self._page.index(tag_pattern11) < board_pos:
					self._page = self._page.replace(tag_pattern11,tag_pattern13)
				else:
					break
			while tag_pattern1 in self._page:
				tag_pos = self._page.index(tag_pattern1)
				if tag_pos < board_pos:
					self._page = self._page.replace(tag_pattern1,tag_pattern12,1)
				else:
					break
			# Вставить sep_words_found перед названием 1-го словаря. Нельзя вставлять его в самое начало ввиду особенностей обработки delete_entries.
			if globs['bool']['ExploreMismatch']:
				self._page = self._page.replace(tag_pattern1,tag_pattern5 + sep_words_found + tag_pattern6 + tag_pattern1,1)
			else:
				self._page = self._page[:board_pos] + tag_pattern7 + tag_pattern5 + sep_words_found + tag_pattern6
			# Поскольку message_board встречается между вхождениями, а не до них или после них, то обрабатываем его вне delete_entries.
			self._page = self._page.replace(message_board,'')
	
	def example_class(self):
		self._page = '''<!DOCTYPE html>
<html manifest="mt.appcache">
<head>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1251">
<script>
if (top.location != self.location) { top.location = self.location; }
</script>
<script type="text/javascript" src="http://www.multitran.ru/adfox.asyn.code.ver3.js"></script>
<title>сцеживать</title> 
<meta http-equiv="Content-Language" Content="en"/>
<meta name="Keywords" Content="сцеживать"/>
<meta name="revisit-after" content="15 days"/>
<meta name="rating" content="safe for kids"/>
<meta property="og:title" content="сцеживать"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="http://www.multitran.ru/c/m.exe?l1=2&l2=1&s=сцеживать"/>
<meta property="og:image" content="http://www.multitran.ru/gif/logo.gif"/>
<meta property="og:site_name" content="Словарь Мультитран"/>
<meta name="ROBOTS" content="ALL"/>
<link rel="TOC" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="index" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="contents" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link type="application/opensearchdescription+xml" rel="search" href="http://www.multitran.ru/osdd.xml">
<link rel="shortcut icon" href="/gif/favicon.ico">
<meta name="keywords" content="словарь, англо-русский словарь, немецко-русский словарь, электронный словарь, автоматический словарь, перевод, форум переводчиков">
<meta name="description" content="англо-русский словарь">
<link rel="stylesheet" href="/style3.css" type="text/css">

<script type="text/javascript">

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-2913236-1']);
_gaq.push(['_trackPageview']);

(function() {
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
</script>

</head>
<body>
<a name="start"></a>
<table border="0" cellspacing="0" cellpadding="0"><tr><td></td><td>
<table border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td><table border="0" cellspacing="0" cellpadding="0"><tr><td><table width>
  <tr>
    <td>
<a href="../c/m.exe?a=5&amp;s=AboutMultitran.htm">О словаре</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=5&amp;s=FAQ.htm">FAQ</a></span></span>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;</td>
    <td ><a href="m.exe?a=116&UserName=denton">denton</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=150">Выход</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=24&amp;s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&amp;action=0">Настройки</a></td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=1"><img src="../j/logo.gif"
    alt="Словарь Мультитран" width="252" height="90"></a>
</td>
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 728x90 N33 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:728px;height:90px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="1674328017"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=5&amp;s=searches"><img src="../j/dict_active.gif" alt="Dicts"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=2&amp;l1=2&amp;l2=1"><img
    border="0" src="../j/forum.gif" alt="Forum" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=44&amp;nadd=1"><img src="../j/buy.gif" alt="Buy" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=5&amp;s=DownloadFile"><img src="../j/download.gif" alt="Download"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=45"><img src="../j/guestbook.gif"
    alt="Guestbook" width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=5&amp;s=s_contacts"><img
    src="../j/contacts.gif" alt="Contacts" width="83" height="27"></a></td>
    <td align="center" valign="middle">
<a target="_blank" href=http://www.multitran.com> в тестовом режиме открыт новый сайт Мультитрана</a>
</td>
  </tr>
</table>
</td></tr><tr><td>
<table border="0" cellspacing="0" cellpadding="0"><tr><td width=170>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 160x600 N44 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:160px;height:600px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="2373948248"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td><td>
<table width="700"><tr><td></td></tr></table><form id="translation" name="translation" action="/c/m.exe" method="get">
      <input type="hidden" name="l1" value="2"><input type="hidden" name="l2"
      value="1">
    
<table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" cellpadding="0" id="AutoNumber1" width="100%">
  <tr>
    <td><span style="position:relative;"><input id="s" type="text" name="s" autocomplete="off"
          value="сцеживать" size="45" tabindex="1">&nbsp;</span><input type="submit"
          value="Поиск" tabindex="2">&nbsp;
Eng&nbsp;<br><div id="suggest"></div></td>
    <td>
    
</td>
</tr>
</table>
      <script><!--
document.translation.s.select()
document.translation.s.focus() 
// --></script>
    </form>
<div></div>
<script>
createAutoComplete();
</script>
    
<table border="0" cellspacing="0" cellpadding="0"><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?a=118&t=65945_2_1">сцеживать</a> <em>гл.</em>&nbsp;<a href="#phrases"><FONT SIZE=2>фразы</FONT></a></a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=65945_2_1&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=65945_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">decant</a><span STYLE="color:gray"> (вино)<span STYLE="color:black">;  <a href="m.exe?t=662264_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">emulge</a>;  <a href="m.exe?t=3978793_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">rack</a><span STYLE="color:gray"> (вино, сидр; часто rack off)<span STYLE="color:black"></td><tr><td >&nbsp;&nbsp;<a title="Акушерство" href="m.exe?a=110&t=6817233_2_1&sc=145"><i>акуш.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=6817233_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">express</a><span STYLE="color:gray"> (молоко <a href="m.exe?a=116&&UserName=dms"><i>dms</i></a>)<span STYLE="color:black"></td><tr><td >&nbsp;&nbsp;<a title="Макаров" href="m.exe?a=110&t=3129579_2_1&sc=517"><i>Макаров</i>&nbsp;</a>
</td><td> <a href="m.exe?t=3129579_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">rack</a><span STYLE="color:gray"> (вино, сидр)<span STYLE="color:black">;  <a href="m.exe?t=3129594_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">rack off</a><span STYLE="color:gray"> (вино, сидр)<span STYLE="color:black"></td><tr><td >&nbsp;&nbsp;<a title="Медицина" href="m.exe?a=110&t=353857_2_1&sc=8"><i>мед.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=353857_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">rack</a></td><tr><td >&nbsp;&nbsp;<a title="Сельское хозяйство" href="m.exe?a=110&t=2952872_2_1&sc=30"><i>с.-х.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=2952872_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">drain off</a>;  <a href="m.exe?t=3185152_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">strain off</a></td><tr><td >&nbsp;&nbsp;<a title="Техника" href="m.exe?a=110&t=2328922_2_1&sc=28"><i>тех.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=2328922_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">elutriate</a>;  <a href="m.exe?t=2333980_1_2&s1=%F1%F6%E5%E6%E8%E2%E0%F2%FC">filter off</a></td></tr></table><a name="phrases"></a>

<table cellspacing="0" border="0">
<tr><td width="25%"><img border="0" src="gif/empty5.gif" width="1" height="8"></td><td width="25%"></td><td width="25%"></td><td width="25%"></td></tr>
<tr><td width="700" colspan="4" bgcolor="#DBDBDB">&nbsp;сцеживать: <a href="m.exe?a=3&&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&l1=2&l2=1">3 фразы</a> в 2 тематиках&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="#start"><FONT SIZE=2>в начало</FONT></a></td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&sc=145&l1=2&l2=1">Акушерство</a></td><td width="25%">2</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&sc=0&l1=2&l2=1">Общая&nbsp;лексика</a></td><td width="25%">1</td></tr>
</table>
<form id="translation" name="translation" action="/c/m.exe" method="get">
      <input type="hidden" name="l1" value="2"><input type="hidden" name="l2"
      value="1">
    
<table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" cellpadding="0" id="AutoNumber1" width="100%">
  <tr>
    <td><span style="position:relative;"><input id="s" type="text" name="s" autocomplete="off"
          value="сцеживать" size="45" tabindex="1">&nbsp;</span><input type="submit"
          value="Поиск" tabindex="2">&nbsp;
Eng&nbsp;<br><div id="suggest"></div></td>
    <td>
    
</td>
</tr>
</table>
      <script><!--
document.translation.s.select()
document.translation.s.focus() 
// --></script>
    </form>
<div></div>
<script>
createAutoComplete();
</script>
    
</td><td>&nbsp;&nbsp;&nbsp;</td><td width="240">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 240*400 N35 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:240px;height:400px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8916963057"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>

</td></tr></table></td></tr></table><table border="0" cellpadding="0" cellspacing="0" width="100%">
 <tr>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
  </tr>
 <tr bgcolor="#DBDBDB">
    <td><font size="2">&nbsp;<a href="m.exe?a=104&&l1=2&l2=1&s2=%F1%F6%E5%E6%E8%E2%E0%F2%FC">Добавить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=134&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&l1=2&l2=1">Удалить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=11&l1=2&l2=1&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC">Изменить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=26&&s=%F1%F6%E5%E6%E8%E2%E0%F2%FC&l1=2&l2=1">Сообщить&nbsp;об&nbsp;ошибке</a>&nbsp;<span STYLE</font></td>
   
<td>    
<g:plusone size="small"></g:plusone>
<script type="text/javascript">
  window.___gcfg = {lang: 'ru'};
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
</script>
</td>
    
    <td align="right">
</td>
  </tr>
 <tr>
    <td colspan="3">&nbsp;</td>
   
  </tr>
 <tr>
    <td>
    <p align="center">&nbsp;</td>
   
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 300x250 N36 Abroad -->
<ins class="adsbygoogle"
 style="display:block"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8153379056"
 data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
   
    <td>&nbsp;</td>
   
  </tr>
</table>
</td></tr></table></td><td>&nbsp;</td></tr></table>

</body>
</html>'''
	
	def example2(self):
		'''
		<!DOCTYPE html>
<html manifest="mt.appcache">
<head>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1251">
<script>
if (top.location != self.location) { top.location = self.location; }
</script>
<script type="text/javascript" src="http://www.multitran.ru/adfox.asyn.code.ver3.js"></script>
<title>welcome aboard</title> 
<meta http-equiv="Content-Language" Content="ru"/>
<meta name="Keywords" Content="welcome aboard"/>
<meta name="revisit-after" content="15 days"/>
<meta name="rating" content="safe for kids"/>
<meta property="og:title" content="welcome aboard"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=welcome aboard"/>
<meta property="og:image" content="http://www.multitran.ru/gif/logo.gif"/>
<meta property="og:site_name" content="Словарь Мультитран"/>
<meta name="ROBOTS" content="ALL"/>
<link rel="TOC" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="index" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="contents" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link type="application/opensearchdescription+xml" rel="search" href="http://www.multitran.ru/osdd.xml">
<link rel="shortcut icon" href="/gif/favicon.ico">
<meta name="keywords" content="словарь, англо-русский словарь, немецко-русский словарь, электронный словарь, автоматический словарь, перевод, форум переводчиков">
<meta name="description" content="англо-русский словарь">
<link rel="stylesheet" href="/style3.css" type="text/css">

<script type="text/javascript">

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-2913236-1']);
_gaq.push(['_trackPageview']);

(function() {
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
</script>

<script type="text/javascript" src="script.js"> </script>
<script type="text/javascript">
var urlgo="m.exe?l1=1&l2=2&s=";
var url="ms.exe?l1=1&l2=2&s=";
var strclosesug="close";
</script>
</head>
<body>
<a name="start"></a>
<table border="0" cellspacing="0" cellpadding="0"><tr><td></td><td>
<table border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td><table border="0" cellspacing="0" cellpadding="0"><tr><td><table width>
  <tr>
    <td>
<a href="../c/m.exe?a=5&amp;s=AboutMultitran.htm">О словаре</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=5&amp;s=FAQ.htm">FAQ</a></span></span>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;</td>
    <td ><a href="m.exe?a=40">Вход</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=113">Регистрация</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=24&amp;s=welcome%20aboard&amp;action=0">Настройки</a></td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=1"><img src="../j/logo.gif"
    alt="Словарь Мультитран" width="252" height="90"></a>
</td>
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 728x90 N33 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:728px;height:90px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="1674328017"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=5&amp;s=searches"><img src="../j/dict_active.gif" alt="Dicts"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=2&amp;l1=1&amp;l2=2"><img
    border="0" src="../j/forum.gif" alt="Forum" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=44&amp;nadd=1"><img src="../j/buy.gif" alt="Buy" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=5&amp;s=DownloadFile"><img src="../j/download.gif" alt="Download"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=45"><img src="../j/guestbook.gif"
    alt="Guestbook" width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=5&amp;s=s_contacts"><img
    src="../j/contacts.gif" alt="Contacts" width="83" height="27"></a></td>
    <td align="center" valign="middle">
<a target="_blank" href=http://www.multitran.com> в тестовом режиме открыт новый сайт Мультитрана</a>
</td>
  </tr>
</table>
</td></tr><tr><td>
<table border="0" cellspacing="0" cellpadding="0"><tr><td width=170>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 160x600 N44 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:160px;height:600px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="2373948248"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td><td>
<table width="700"><tr><td></td></tr></table><form id="translation" name="translation" action="/c/m.exe" method="get">
      <input type="hidden" name="l1" value="1"><input type="hidden" name="l2"
      value="2">
    
<table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" cellpadding="0" id="AutoNumber1" width="100%">
  <tr>
    <td><span style="position:relative;"><input id="s" type="text" name="s" autocomplete="off"
          value="welcome aboard" size="45" tabindex="1">&nbsp;</span><input type="submit"
          value="Поиск" tabindex="2">&nbsp;
Eng&nbsp;<br><div id="suggest"></div></td>
    <td>
    
</td>
</tr>
</table>
      <script><!--
document.translation.s.select()
document.translation.s.focus() 
// --></script>
    </form>
<div></div>
<script>
createAutoComplete();
</script>
    
<table border="0" cellspacing="0" cellpadding="0"><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=6900382_1_2&ifp=1&s1=welcome%20aboard">welcome aboard</a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=6900382_1_2&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=6900382_2_1&s1=welcome%20aboard">добро пожаловать</a><span STYLE="color:gray"> (к нашему шалашу <a href="m.exe?a=116&&UserName=Miha4406"><i>Miha4406</i></a>)<span STYLE="color:black">;  <a href="m.exe?t=200866_2_1&s1=welcome%20aboard">приветствуем вас на борту самолёта</a><span STYLE="color:gray"> (обращение стюардессы к пассажирам)<span STYLE="color:black"><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=3375858_1_2&ifp=1&s1=welcome%20aboard!">welcome aboard!</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="#start"><FONT SIZE=2>в начало</FONT></a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=3375858_1_2&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=3375858_2_1&s1=welcome%20aboard!">приветствуем вас на борту нашего самолёта</a><span STYLE="color:gray"> (обращение стюардессы)<span STYLE="color:black"></td><tr><td >&nbsp;&nbsp;<a title="Риторика" href="m.exe?a=110&t=7057959_1_2&sc=110"><i>ритор.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=7057959_2_1&s1=welcome%20aboard!">приветствую вас на нашей палубе!</a><span STYLE="color:gray"> (<a href="m.exe?a=116&&UserName=Alex_Odeychuk"><i>Alex_Odeychuk</i></a>)<span STYLE="color:black">;  <a href="m.exe?t=7057958_2_1&s1=welcome%20aboard!">добро пожаловать к нашему шалашу!</a><span STYLE="color:gray"> (<a href="m.exe?a=116&&UserName=Alex_Odeychuk"><i>Alex_Odeychuk</i></a>)<span STYLE="color:black"></td></tr></table><a name="phrases"></a>
</td><td>&nbsp;&nbsp;&nbsp;</td><td width="240">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 240*400 N35 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:240px;height:400px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8916963057"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>

</td></tr></table></td></tr></table><table border="0" cellpadding="0" cellspacing="0" width="100%">
 <tr>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
  </tr>
 <tr bgcolor="#DBDBDB">
    <td><font size="2">&nbsp;<a href="m.exe?a=104&&l1=1&l2=2&s1=welcome%20aboard">Добавить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=134&s=welcome%20aboard&l1=1&l2=2">Удалить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=11&l1=1&l2=2&s=welcome%20aboard">Изменить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=26&&s=welcome%20aboard&l1=1&l2=2">Сообщить&nbsp;об&nbsp;ошибке</a>&nbsp;<span STYLE</font></td>
   
<td>    
<g:plusone size="small"></g:plusone>
<script type="text/javascript">
  window.___gcfg = {lang: 'ru'};
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
</script>
</td>
    
    <td align="right">
</td>
  </tr>
 <tr>
    <td colspan="3">&nbsp;</td>
   
  </tr>
 <tr>
    <td>
    <p align="center">&nbsp;</td>
   
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 300x250 N36 Abroad -->
<ins class="adsbygoogle"
 style="display:block"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8153379056"
 data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
   
    <td>&nbsp;</td>
   
  </tr>
</table>
</td></tr></table></td><td>&nbsp;</td></tr></table>

</body>
</html>
		'''
		
	def example3(self):
		'''
		<!DOCTYPE html>
<html manifest="mt.appcache">
<head>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1251">
<script>
if (top.location != self.location) { top.location = self.location; }
</script>
<script type="text/javascript" src="http://www.multitran.ru/adfox.asyn.code.ver3.js"></script>
<title>приветствуем вас на борту самолёта</title> 
<meta http-equiv="Content-Language" Content="en"/>
<meta name="Keywords" Content="приветствуем вас на борту самолёта"/>
<meta name="revisit-after" content="15 days"/>
<meta name="rating" content="safe for kids"/>
<meta property="og:title" content="приветствуем вас на борту самолёта"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="http://www.multitran.ru/c/m.exe?l1=2&l2=1&s=приветствуем вас на борту самолёта"/>
<meta property="og:image" content="http://www.multitran.ru/gif/logo.gif"/>
<meta property="og:site_name" content="Словарь Мультитран"/>
<meta name="ROBOTS" content="ALL"/>
<link rel="TOC" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="index" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="contents" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link type="application/opensearchdescription+xml" rel="search" href="http://www.multitran.ru/osdd.xml">
<link rel="shortcut icon" href="/gif/favicon.ico">
<meta name="keywords" content="словарь, англо-русский словарь, немецко-русский словарь, электронный словарь, автоматический словарь, перевод, форум переводчиков">
<meta name="description" content="англо-русский словарь">
<link rel="stylesheet" href="/style3.css" type="text/css">

<script type="text/javascript">

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-2913236-1']);
_gaq.push(['_trackPageview']);

(function() {
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
</script>

<script type="text/javascript" src="script.js"> </script>
<script type="text/javascript">
var urlgo="m.exe?l1=2&l2=1&s=";
var url="ms.exe?l1=2&l2=1&s=";
var strclosesug="close";
</script>
</head>
<body>
<a name="start"></a>
<table border="0" cellspacing="0" cellpadding="0"><tr><td></td><td>
<table border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td><table border="0" cellspacing="0" cellpadding="0"><tr><td><table width>
  <tr>
    <td>
<a href="../c/m.exe?a=5&amp;s=AboutMultitran.htm">О словаре</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=5&amp;s=FAQ.htm">FAQ</a></span></span>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;</td>
    <td ><a href="m.exe?a=40">Вход</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=113">Регистрация</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=24&amp;s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0&amp;action=0">Настройки</a></td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=1"><img src="../j/logo.gif"
    alt="Словарь Мультитран" width="252" height="90"></a>
</td>
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 728x90 N33 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:728px;height:90px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="1674328017"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=5&amp;s=searches"><img src="../j/dict_active.gif" alt="Dicts"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=2&amp;l1=2&amp;l2=1"><img
    border="0" src="../j/forum.gif" alt="Forum" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=44&amp;nadd=1"><img src="../j/buy.gif" alt="Buy" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=5&amp;s=DownloadFile"><img src="../j/download.gif" alt="Download"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=45"><img src="../j/guestbook.gif"
    alt="Guestbook" width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=5&amp;s=s_contacts"><img
    src="../j/contacts.gif" alt="Contacts" width="83" height="27"></a></td>
    <td align="center" valign="middle">
<a target="_blank" href=http://www.multitran.com> в тестовом режиме открыт новый сайт Мультитрана</a>
</td>
  </tr>
</table>
</td></tr><tr><td>
<table border="0" cellspacing="0" cellpadding="0"><tr><td width=170>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 160x600 N44 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:160px;height:600px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="2373948248"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td><td>
<table width="700"><tr><td></td></tr></table><form id="translation" name="translation" action="/c/m.exe" method="get">
      <input type="hidden" name="l1" value="2"><input type="hidden" name="l2"
      value="1">
    
<table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" cellpadding="0" id="AutoNumber1" width="100%">
  <tr>
    <td><span style="position:relative;"><input id="s" type="text" name="s" autocomplete="off"
          value="приветствуем вас на борту самолёта" size="45" tabindex="1">&nbsp;</span><input type="submit"
          value="Поиск" tabindex="2">&nbsp;
Eng&nbsp;<br><div id="suggest"></div></td>
    <td>
    
</td>
</tr>
</table>
      <script><!--
document.translation.s.select()
document.translation.s.focus() 
// --></script>
    </form>
<div></div>
<script>
createAutoComplete();
</script>
    
<table border="0" cellspacing="0" cellpadding="0"><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=200866_2_1&ifp=1&s1=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0">приветствуем вас на борту самолёта</a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=200866_2_1&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=200866_1_2&s1=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0">welcome aboard</a><span STYLE="color:gray"> (обращение стюардессы к пассажирам)<span STYLE="color:black"></td></tr></table><a name="phrases"></a>

<table cellspacing="0" border="0">
<tr><td width="25%"><img border="0" src="gif/empty5.gif" width="1" height="8"></td><td width="25%"></td><td width="25%"></td><td width="25%"></td></tr>
<tr><td width="700" colspan="4" bgcolor="#DBDBDB">&nbsp;приветствуем вас на борту самолёта: <a href="m.exe?a=3&&s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0&l1=2&l2=1">2 фразы</a> в 1 тематике</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0&sc=0&l1=2&l2=1">Общая&nbsp;лексика</a></td><td width="25%">2</td><td width="25%"></td><td width="25%"></td></tr>
</table>
</td><td>&nbsp;&nbsp;&nbsp;</td><td width="240">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 240*400 N35 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:240px;height:400px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8916963057"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>

</td></tr></table></td></tr></table><table border="0" cellpadding="0" cellspacing="0" width="100%">
 <tr>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
  </tr>
 <tr bgcolor="#DBDBDB">
    <td><font size="2">&nbsp;<a href="m.exe?a=104&&l1=2&l2=1&s2=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0">Добавить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=134&s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0&l1=2&l2=1&t=200866">Удалить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=11&l1=2&l2=1&t=200866&s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0">Изменить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=26&&s=%EF%F0%E8%E2%E5%F2%F1%F2%E2%F3%E5%EC%20%E2%E0%F1%20%ED%E0%20%E1%EE%F0%F2%F3%20%F1%E0%EC%EE%EB%B8%F2%E0&l1=2&l2=1">Сообщить&nbsp;об&nbsp;ошибке</a>&nbsp;<span STYLE</font></td>
   
<td>    
<g:plusone size="small"></g:plusone>
<script type="text/javascript">
  window.___gcfg = {lang: 'ru'};
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
</script>
</td>
    
    <td align="right">
</td>
  </tr>
 <tr>
    <td colspan="3">&nbsp;</td>
   
  </tr>
 <tr>
    <td>
    <p align="center">&nbsp;</td>
   
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 300x250 N36 Abroad -->
<ins class="adsbygoogle"
 style="display:block"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8153379056"
 data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
   
    <td>&nbsp;</td>
   
  </tr>
</table>
</td></tr></table></td><td>&nbsp;</td></tr></table>

</body>
</html>
		'''
	
	def example(self):
		self._page = '''<!DOCTYPE html>
<html manifest="mt.appcache">
<head>
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1251">
<script>
if (top.location != self.location) { top.location = self.location; }
</script>
<script type="text/javascript" src="http://www.multitran.ru/adfox.asyn.code.ver3.js"></script>
<title>Добро пожаловать!</title> 
<meta http-equiv="Content-Language" Content="ru"/>
<meta name="Keywords" Content="Добро пожаловать!"/>
<meta name="revisit-after" content="15 days"/>
<meta name="rating" content="safe for kids"/>
<meta property="og:title" content="Добро пожаловать!"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=Добро пожаловать!"/>
<meta property="og:image" content="http://www.multitran.ru/gif/logo.gif"/>
<meta property="og:site_name" content="Словарь Мультитран"/>
<meta name="ROBOTS" content="ALL"/>
<link rel="TOC" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="index" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link rel="contents" href="http://www.multitran.ru/c/m.exe?a=5&s=searches"/>
<link type="application/opensearchdescription+xml" rel="search" href="http://www.multitran.ru/osdd.xml">
<link rel="shortcut icon" href="/gif/favicon.ico">
<meta name="keywords" content="словарь, англо-русский словарь, немецко-русский словарь, электронный словарь, автоматический словарь, перевод, форум переводчиков">
<meta name="description" content="англо-русский словарь">
<meta HTTP-EQUIV="Set-Cookie" CONTENT="langs=1 2;EXPIRES=Friday, 01-Jan-2020 23:59:59 GMT;PATH=/">
<link rel="stylesheet" href="/style3.css" type="text/css">

<script type="text/javascript">

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-2913236-1']);
_gaq.push(['_trackPageview']);

(function() {
var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();
</script>

<script type="text/javascript" src="script.js"> </script>
<script type="text/javascript">
var urlgo="m.exe?l1=1&l2=2&s=";
var url="ms.exe?l1=1&l2=2&s=";
var strclosesug="close";
</script>
</head>
<body>
<a name="start"></a>
<table border="0" cellspacing="0" cellpadding="0"><tr><td></td><td>
<table border="0" cellspacing="0" cellpadding="0" width="100%"><tr><td><table border="0" cellspacing="0" cellpadding="0"><tr><td><table width>
  <tr>
    <td>
<a href="../c/m.exe?a=5&amp;s=AboutMultitran.htm">О словаре</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=5&amp;s=FAQ.htm">FAQ</a></span></span>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;</td>
    <td ><a href="m.exe?a=40">Вход</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=113">Регистрация</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;
<a href="../c/m.exe?a=24&amp;s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&amp;action=0">Настройки</a></td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=1"><img src="../j/logo.gif"
    alt="Словарь Мультитран" width="252" height="90"></a>
</td>
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 728x90 N33 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:728px;height:90px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="1674328017"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
  </tr>
</table>
<table>
  <tr>
    <td><a href="../c/m.exe?a=5&amp;s=searches"><img src="../j/dict_active.gif" alt="Dicts"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=2&amp;l1=1&amp;l2=2"><img
    border="0" src="../j/forum.gif" alt="Forum" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=44&amp;nadd=1"><img src="../j/buy.gif" alt="Buy" width="83" height="27"></a>&nbsp;<a
    href="../c/m.exe?a=5&amp;s=DownloadFile"><img src="../j/download.gif" alt="Download"
    width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=45"><img src="../j/guestbook.gif"
    alt="Guestbook" width="83" height="27"></a>&nbsp;<a href="../c/m.exe?a=5&amp;s=s_contacts"><img
    src="../j/contacts.gif" alt="Contacts" width="83" height="27"></a></td>
    <td align="center" valign="middle">
<a target="_blank" href=http://www.multitran.com> в тестовом режиме открыт новый сайт Мультитрана</a>
</td>
  </tr>
</table>
</td></tr><tr><td>
<table border="0" cellspacing="0" cellpadding="0"><tr><td width=170>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 160x600 N44 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:160px;height:600px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="2373948248"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td><td>
<table width="700"><tr><td></td></tr></table><form id="translation" name="translation" action="/c/m.exe" method="get">
      <input type="hidden" name="l1" value="2"><input type="hidden" name="l2"
      value="1">
    
<table border="0" cellspacing="0" style="border-collapse: collapse" bordercolor="#111111" cellpadding="0" id="AutoNumber1" width="100%">
  <tr>
    <td><span style="position:relative;"><input id="s" type="text" name="s" autocomplete="off"
          value="Добро пожаловать!" size="45" tabindex="1">&nbsp;</span><input type="submit"
          value="Поиск" tabindex="2">&nbsp;
Eng&nbsp;<br><div id="suggest"></div></td>
    <td>
    
</td>
</tr>
</table>
      <script><!--
document.translation.s.select()
document.translation.s.focus() 
// --></script>
    </form>
<div></div>
<script>
createAutoComplete();
</script>
    
<table border="0" cellspacing="0" cellpadding="0"><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=13454_2_1&ifp=1&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">добро пожаловать</a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=13454_2_1&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=13454_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">welcome</a>;  <a href="m.exe?t=244928_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">you are welcome</a>;  <a href="m.exe?t=6900382_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">welcome aboard</a><span STYLE="color:gray"> (к нашему шалашу <a href="m.exe?a=116&&UserName=Miha4406"><i>Miha4406</i></a>)<span STYLE="color:black"></td><tr><td >&nbsp;&nbsp;<a title="Устаревшее слово" href="m.exe?a=110&t=238922_2_1&sc=17"><i>уст.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=238922_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">well met</a></td><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=813384_2_1&ifp=1&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">добро пожаловать!</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="#start"><FONT SIZE=2>в начало</FONT></a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Общая лексика" href="m.exe?a=110&t=813384_2_1&sc=0"><i>общ.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=813384_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">welcome</a></td><tr><td >&nbsp;&nbsp;<a title="Итальянский язык" href="m.exe?a=110&t=642393_2_1&sc=90"><i>итал.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=642393_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">ben venuto!</a></td><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=6453625_2_1&ifp=1&s1=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">Добро пожаловать</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="#start"><FONT SIZE=2>в начало</FONT></a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Американизм" href="m.exe?a=110&t=6453625_2_1&sc=13"><i>амер.</i>&nbsp;</a>
</td><td> <a href="m.exe?t=6453625_1_2&s1=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC">Welcome to the club</a><span STYLE="color:gray"> (Вы не один такой <a href="m.exe?a=116&&UserName=Val_Ships"><i>Val_Ships</i></a>)<span STYLE="color:black"></td><tr><td bgcolor="#DBDBDB" colspan="2" width="700">&nbsp;<a href="m.exe?t=2144703_2_1&ifp=1&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">добро пожаловать!</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="#start"><FONT SIZE=2>в начало</FONT></a>
</td></tr><tr><td >&nbsp;&nbsp;<a title="Пословица" href="m.exe?a=110&t=2144703_2_1&sc=310"><i>посл.</i>&nbsp;</a>
</td><td> <span STYLE="color:gray">you are<span STYLE="color:black"> <a href="m.exe?t=2144703_1_2&s1=%E4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">welcome!</a></td></tr></table><a name="phrases"></a>

<table cellspacing="0" border="0">
<tr><td width="25%"><img border="0" src="gif/empty5.gif" width="1" height="8"></td><td width="25%"></td><td width="25%"></td><td width="25%"></td></tr>
<tr><td width="700" colspan="4" bgcolor="#DBDBDB">&nbsp;Добро пожаловать!: <a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&l1=2&l2=1">20 фраз</a> в 12 тематиках</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=13&l1=2&l2=1">Американизм</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=0&l1=2&l2=1">Общая&nbsp;лексика</a></td><td width="25%">9</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=84&l1=2&l2=1">Дипломатический&nbsp;термин</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=310&l1=2&l2=1">Пословица</a></td><td width="25%">1</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=15&l1=2&l2=1">Ироническое&nbsp;выражение</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=357&l1=2&l2=1">Программирование</a></td><td width="25%">1</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=90&l1=2&l2=1">Итальянский&nbsp;язык</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=110&l1=2&l2=1">Риторика</a></td><td width="25%">1</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=1&l1=2&l2=1">Компьютерная&nbsp;техника</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=136&l1=2&l2=1">Сленг</a></td><td width="25%">1</td></tr>
<tr><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=847&l1=2&l2=1">Майкрософт</a></td><td width="25%">1</td><td width="25%">&nbsp;&nbsp;<a href="m.exe?a=3&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&sc=17&l1=2&l2=1">Устаревшее&nbsp;слово</a></td><td width="25%">1</td></tr>
</table>
</td><td>&nbsp;&nbsp;&nbsp;</td><td width="240">
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 240*400 N35 -->
<ins class="adsbygoogle"
 style="display:inline-block;width:240px;height:400px"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8916963057"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>

</td></tr></table></td></tr></table><table border="0" cellpadding="0" cellspacing="0" width="100%">
 <tr>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
    <td height="3">&nbsp;</td>
  </tr>
 <tr bgcolor="#DBDBDB">
    <td><font size="2">&nbsp;<a href="m.exe?a=104&&l1=2&l2=1&s2=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">Добавить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=134&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&l1=2&l2=1">Удалить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=11&l1=2&l2=1&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!">Изменить</a>&nbsp;<span STYLE="color:gray">|<span STYLE="color:black">&nbsp;<a href="m.exe?a=26&&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC!&l1=2&l2=1">Сообщить&nbsp;об&nbsp;ошибке</a>&nbsp;<span STYLE</font></td>
   
<td>    
<g:plusone size="small"></g:plusone>
<script type="text/javascript">
  window.___gcfg = {lang: 'ru'};
  (function() {
    var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
    po.src = 'https://apis.google.com/js/plusone.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
  })();
</script>
</td>
    
    <td align="right">
</td>
  </tr>
 <tr>
    <td colspan="3">&nbsp;</td>
   
  </tr>
 <tr>
    <td>
    <p align="center">&nbsp;</td>
   
    <td>
<script async src="//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- 300x250 N36 Abroad -->
<ins class="adsbygoogle"
 style="display:block"
 data-ad-client="ca-pub-3245380208650914"
 data-ad-slot="8153379056"
 data-ad-format="auto"></ins>
<script>
(adsbygoogle = window.adsbygoogle || []).push({});
</script>
</td>
   
    <td>&nbsp;</td>
   
  </tr>
</table>
</td></tr></table></td><td>&nbsp;</td></tr></table>

</body>
</html>
		'''
	
	def common_replace(self): # HTML specific
		self._page = self._page.replace('\r\n','')
		self._page = self._page.replace('\n','')
		self._page = self._page.replace('\xa0',' ')
		while '  ' in self._page:
			self._page = self._page.replace('  ',' ')
		self._page = self._page.replace(nbspace+'<','<')
		self._page = self._page.replace(' <','<')
		self._page = self._page.replace('>'+nbspace,'>')
		self._page = self._page.replace('> ','>')
	
	# Convert HTML entities to a human readable format, e.g., '&copy;' -> '©'
	def decode_entities(self): # HTML specific
		try:
			self._page = html.unescape(self._page)
		except:
			log.append('Page.decode_entities',lev_err,globs['mes'].html_conversion_failure)
	
	def get(self):
		if not self._page:
			''' # todo: Paste globs['mes'].wait into search_field before loading a page and clear search_field after the page has been processed. The problem: tkinter does not update when neccessary. Print supports this.
			h_table.paste_search_field(text=globs['mes'].wait)
			h_table.clear_search_field()
			'''
			while self._page == '':
				Success = False
				# Загружаем страницу
				try:
					# Если загружать страницу с помощью "page=urllib.request.urlopen(my_url)", то в итоге получится HTTPResponse, что полезно только для удаления тэгов JavaScript. Поскольку мы вручную удаляем все лишние тэги, то на выходе нам нужна строка.
					self._page = urllib.request.urlopen(h_request.url()).read()
					log.append('Page.get',lev_info,globs['mes'].ok % h_request.search())
					Success = True
				except:
					log.append('Page.get',lev_warn,globs['mes'].failed % h_request.search())
					if not Message(func='Page.get',type=lev_ques,message=globs['mes'].webpage_unavailable_ques).Yes:
						break
				if Success: # Если страница не загружена, то понятно, что ее кодировку изменить не удастся
					try:
						# Меняем кодировку globs['var']['win_encoding'] на нормальную
						self._page = self._page.decode(globs['var']['win_encoding'])
					except:
						Message(func='Page.get',type=lev_err,message=globs['mes'].wrong_html_encoding)
					h_request._html_raw = self._page
		return self._page



class Tags:
	
	def __init__(self):
		self._page = ''
		self._borders = []
		self._elems = []
		self._tags = []
		self.url = '' # Only a current URL for a tag
	
	# Create a list with positions of signs '<' and '>'
	def borders(self):
		if not self._borders:
			self._page = self.page()
			if self._page:
				tmp_borders = []
				i = 0
				while i < len(self._page):
					# Signs '<' and '>' as such can cause serious problems since they can occur in invalid cases like "perform >>> conduct >> carry out (vbadalov)". The following algorithm is also not 100% precise but is better.
					if self._page[i] == '<' or self._page[i] == '>':
						tmp_borders.append(i)
					i += 1
				if len(tmp_borders) % 2 != 0:
					log.append('Tags.pos',lev_warn,globs['mes'].wrong_tag_num % len(tmp_borders))
					if len(tmp_borders) > 0:
						del tmp_borders[-1]
					else:
						log.append('Tags.pos',lev_warn,globs['mes'].tmp_borders_empty)
				i = 0
				while i < len(tmp_borders):
					uneven = tmp_borders[i]
					i += 1
					even = tmp_borders[i]
					i += 1
					self._borders += [[uneven,even]]
		return self._borders
		
	# Extract a dictionary abbreviation
	def _dic(self,i=0):
		if self._tags[i].startswith(tag_pattern1):
			tmp_str = self._tags[i]
			tmp_str = tmp_str.replace(tag_pattern1,'',1)
			tmp_str = re.sub('".*','',tmp_str)
			if tmp_str == '' or tmp_str == ' ':
				log.append('Tags._dic',lev_warn,globs['mes'].wrong_tag % self._tags[i])
			else:
				self._elems[-1].dic = tmp_str
				
	# Extract a term
	def _term(self,i=0):
		if self._tags[i].startswith(tag_pattern2):
			# It is reasonable to bind URLs to terms only, but we want the number of URLs to match the number of article elements, moreover, extra URLs can appear useful.
			if i + 1 < len(self._tags):
				pos1 = self._borders[i][1] + 1
				pos2 = self._borders[i+1][0] - 1
				if pos1 >= len(self._page):
					log.append('Tags._term',lev_warn,globs['mes'].tag_near_text_end % self._tags[i])
				else:
					if tag_pattern7 in self._tags[i+1] or tag_pattern8 in self._tags[i+1]:
						tmp_str = self._page[pos1:pos2+1]
						# If we see symbols '<' or '>' there for some reason, then there is a problem in the tag extraction algorithm. We can make manual deletion of '<' and '>' there.
						# Draft such cases as '23 фраз' as dictionary titles, not terms
						# todo: Make this selectable
						match = re.search('\d+ фраз',tmp_str)
						if match:
							self._elems[-1].dic = tmp_str
						else:
							self._elems[-1].term = tmp_str
					self._url(i)
			else:
				log.append('Tags._term',lev_warn,globs['mes'].last_tag % self._tags[i])
				
	# Extract URL
	def _url(self,i=0):
		self.url = self._tags[i].replace(tag_pattern2,'',1)
		# We need re because of such cases as "<a href = "m.exe?t = 74188_2_4&s1 = faute">ошибка"
		self.url = re.sub('\"\>.*','">',self.url)
		if self.url.endswith(tag_pattern8):
			self.url = self.url.replace(tag_pattern8,'')
			self.url = online_url_root + self.url
		else:
			log.append('Tags._url',lev_warn,globs['mes'].url_extraction_failure % self.url)
		
	# Extract a comment
	def _comment(self,i):
		if self._tags[i] == tag_pattern3 or self._tags[i] == tag_pattern5 or self._tags[i] == tag_pattern9:
			pos1 = self._borders[i][1] + 1
			if pos1 >= len(self._page):
				log.append('Tags._comment',lev_warn,globs['mes'].tag_near_text_end % self._tags[i])
			else:
				if i + 1 < len(self._tags):
					pos2 = self._borders[i+1][0] - 1
				else:
					log.append('Tags._comment',lev_warn,globs['mes'].last_tag % self._tags[i])
					if len(self._borders) > 0:
						pos2 = self._borders[-1][1]
					else:
						pos2 = pos1
						log.append('Tags._comment',lev_warn,globs['mes'].tag_borders_empty)
				tmp_str = self._page[pos1:pos2+1]
				# Sometimes, the tag contents is just '('. We remove it, so the final text does not look like '( user_name'
				if tmp_str == '' or tmp_str == ' ' or tmp_str == '|' or tmp_str == '(':
					log.append('Tags._comment',lev_warn,globs['mes'].empty_tag_contents % self._tags[i])
				else:
					self._elems[-1].comment = tmp_str
	
	# Delete some common entries
	def _common(self):
		# We can also delete 'g-sort' here
		# todo: remove useless entries by their URL, not by their names
		i = 0
		while i < len(self._elems):
			if self._elems[i].term in delete_entries:
				del self._elems[i]
				i -= 1
			i += 1
	
	# We do not need empty entries before creating cells, so we delete them (if any)
	def _empty(self):
		i = 0
		while i < len(self._elems):
			if not self._elems[i].speech and not self._elems[i].dic and not self._elems[i].term and not self._elems[i].comment:
				del self._elems[i]
				i -= 1
			i += 1
	
	# Create a list of on-screen text elements for each useful tag
	def elems(self):
		if not self._elems:
			''' Tag patterns:
			1) Abbreviations of dictionaries:
			<a title="...">
			2) Users
			<a href="m.exe?..."><i>...</i></a> OR without 1st <
			3) Terms:
			<a href="m.exe?..."></a>
			4) Genders:
			<span STYLE="color:gray"<i>...</i>
			5) Comments:
			<span STYLE="color:gray"...<
			6) Parts of speech (will be processed later):
			'<a href="m.exe?a=118&t='
			'''
			self._tags = self.tags()
			for i in range(len(self._tags)):
				# Если используется шаблон вместо пустого словаря, то нужно обратить внимание на то, что при изменении присвоенных значений будет меняться и сам шаблон!
				self._elems.append(Cell())
				EntryMatch = False
				self._dic(i)
				self._term(i)
				self._comment(i)
				log.append('Tags.elems',lev_debug,globs['mes'].adding_url % self.url)
				self._elems[i].url = self.url
			self._common()
			self._empty()
		return self._elems
		
	def invalid(self): # Delete tags that impede the tag analysis
		# todo: проверить, учитывает ли парсер '>' в качестве закрывающего символа, или только '/>'
		# Мой парсер по какой-то причине пропускает эти тэги, а tkhtml их удаляет, поэтому возникают проблемы с границами.
		self._page = self._page.replace('<eq>','')
		self._page = self._page.replace('<amp>','')
		# Remove tags <p>, </p>, <b> and </b>, because they can be inside hyperlinks
		self._page = self._page.replace('<p>','')
		self._page = self._page.replace('</p>','')
		self._page = self._page.replace('<b>','')
		self._page = self._page.replace('</b>','')
		
	def open_close(self): # Remove symbols '<' and '>' that do not define tags
		self._page = list(self._page)
		i = 0
		TagOpen = False
		while i < len(self._page):
			if self._page[i] == '<':
				if TagOpen:
					log.append('Tags.open_close',lev_debug,globs['mes'].deleting_useless_elem % (i,self._page[i]))
					if i >= 10 and i < len(self._page) - 10:
						log.append('Tags.open_close',lev_debug,globs['mes'].context % ''.join(self._page[i-10:i+10]))
					del self._page[i]
					i -= 1
				else:
					TagOpen = True
			if self._page[i] == '>':
				if not TagOpen:
					log.append('Tags.open_close',lev_info,globs['mes'].deleting_useless_elem % (i,self._page[i]))
					if i >= 10 and i < len(self._page) - 10:
						log.append('Tags.open_close',lev_info,globs['mes'].context % ''.join(self._page[i-10:i+10]))
					del self._page[i]
					i -= 1
				else:
					TagOpen = False
			i += 1
		self._page = ''.join(self._page)
		
	def page(self):
		if not self._page:
			self._page = Page().get()
			# todo: Move this to __init__?
			self.invalid()
			self.open_close()
			self._non_tags()
		return self._page
	
	def _non_tags(self):
		self._page = list(self._page)
		i = 0
		while i < len(self._page):
			# todo: check: Почему-то при 'not in lat_alphabet' удаляет почти всю статью
			if i < len(self._page) - 1 and self._page[i] == '<' and self._page[i+1] in ru_alphabet:
				del self._page[i]
				i -= 1
			if i > 0 and self._page[i] == '>' and self._page[i-1] in ru_alphabet:
				del self._page[i]
				i -= 1
			i += 1
		# todo: "Expected str instance, int found" error if failed to convert encoding
		self._page = ''.join(self._page)
		
	def _extract(self):
		self._borders = self.borders()
		for i in range(len(self._borders)):
			# + 1 because of slice peculiarities
			pos1 = self._borders[i][0]
			pos2 = self._borders[i][1] + 1
			self._tags.append(self._page[pos1:pos2])
			log.append('Tags._extract',lev_debug,globs['mes'].extracting_tag % self._tags[-1])
		log.append('Tags._extract',lev_info,globs['mes'].tags_found % (len(self._tags)))
		log.append('Tags._extract',lev_debug,str(self._tags))
		
	# Remove tags that are not relevant to the article structure
	def _useless(self):
		old_total = len(self._tags)
		i = 0
		while i < len(self._tags):
			if tag_pattern1 in self._tags[i] or tag_pattern2 in self._tags[i] or tag_pattern3 in self._tags[i] or tag_pattern4 in self._tags[i] or tag_pattern5 in self._tags[i] or tag_pattern6 in self._tags[i] or tag_pattern7 in self._tags[i] or tag_pattern8 in self._tags[i]:
				log.append('Tags._useless',lev_debug,globs['mes'].tag_kept % self._tags[i])
			else:
				log.append('Tags._useless',lev_debug,globs['mes'].deleting_tag % (i,self._tags[i]))
				del self._tags[i]
				del self._borders[i]
				i -= 1
			i += 1
		log.append('Tags._useless',lev_info,globs['mes'].tags_stat % (old_total,len(self._tags),old_total-len(self._tags)))
		# Testing
		assert len(self._tags) == len(self._borders)		
		
	# Extract fragments inside signs '<' and '>'
	def tags(self):
		if not self._tags:
			self._extract()
			self._useless()
		return self._tags



class Elems:
	
	def __init__(self):
		if h_request._elems:
			log.append('Elems.__init__',lev_debug,globs['mes'].action_not_required)
		else:
			log.append('Elems.__init__',lev_info,globs['mes'].create_object)
			h_request._elems = Tags().elems()
			self.useless()
			self.speech()
			self.unite_comments()
			# todo: debug
			#self.unite_by_url()
			self.define_selectables()
			
	def useless(self):
		# We assume that a 'dic'-type entry shall be succeeded by a 'term'-type entry, not a 'comment'-type entry. Therefore, we delete 'comment'-type entries after 'dic'-type entries in order to ensure that dictionary abbreviations do not succeed full dictionary titles. We also can delete full dictionary titles and leave abbreviations instead.
		i = 0
		while i < len(h_request._elems):
			# todo: Удалять по URL
			# Чтобы не удалить случайно длинный комментарий с точкой на конце, ограничиваю его длину 12 (выбрано условно)
			if h_request._elems[i].comment.endswith('.') and len(h_request._elems[i].comment) < 12 or 'Макаров' in h_request._elems[i].comment or 'Вебстер' in h_request._elems[i].comment or 'Webster' in h_request._elems[i].comment or 'Майкрософт' in h_request._elems[i].comment or 'Microsoft' in h_request._elems[i].comment:
				log.append('Elems.useless',lev_info,globs['mes'].deleting_useless_entry % str(h_request._elems[i].comment))
				del h_request._elems[i]
				i -= 1
			i += 1
		# todo (?): обновить self._page
		# todo (?): Проверить, обязательно ли все еще следующее условие: The first element of the 'dic' list must precede the first element of the 'term' list
		
	# Определить части речи и пометить их как названия словарей (чтобы выносились на новую строку)
	def speech(self):
		for i in range(len(h_request._elems)):
			if tag_pattern14 in h_request._elems[i].url:
				if not h_request._elems[i].speech:
					h_request._elems[i].speech = h_request._elems[i].term
					h_request._elems[i].term = ''
					
	# Unite multiple comments using a separator ' | '. Delete comments-only entries.
	def unite_comments(self):
		# Remove comments-only cells
		i = len(h_request._elems) - 1
		while i >= 0:
			if h_request._elems[i].dic == '' and h_request._elems[i].term == '' and h_request._elems[i].comment != '':
				h_request._elems[i-1].comment = h_request._elems[i-1].comment + ' | ' + h_request._elems[i].comment
				del h_request._elems[i]
			i -= 1
		# Delete comments separators where they are not necessary
		for i in range(len(h_request._elems)):
			if h_request._elems[i].comment.startswith(' | '):
				h_request._elems[i].comment = h_request._elems[i].comment.replace(' | ',' ',1)
				
	# Объединить элементы, которые должны входить в одну ячейку
	def unite_by_url(self):
		''' Правила такие:
			1) URL последующего элемента совпадает с URL предыдущего элемента
			2) URL последующего элемента представляет собой URL предыдущего элемента плюс конструкция '&s1=*')
			3) В URL содержится 'UserName', т.е. элемент на самом деле относится к комментариям (хотя в Мультитране идет как самостоятельная ссылка)
		'''
		i = 0
		while i < len(h_request._elems):
			if i > 0:
				if h_request._elems[i].url and h_request._elems[i-1].url == h_request._elems[i].url or h_request._elems[i-1].url + '&s1=' in h_request._elems[i].url or '&UserName=' in h_request._elems[i].url:
					# В настоящее время в ячейке жестко заданы сначала название словаря, потом термин, потом комментарий, поэтому "хвост", который первоначально относился к последующей ячейке, лучше добавить к комментарию, иначе будет потерян смысл
					h_request._elems[i-1].comment = List([h_request._elems[i-1].comment,h_request._elems[i].dic,h_request._elems[i].term,h_request._elems[i].comment]).space_items()
					del h_request._elems[i]
					i -= 1
			i += 1
			
	# Назначить выделяемые ячейки
	def define_selectables(self):
		# Выделяемые ячейки надо назначать как минимум после этой процедуры
		for i in range(len(h_request._elems)):
			if h_request._elems[i].term:
				h_request._elems[i].Selectable = True



def Cell():
	obj = CreateInstance()
	obj.Selectable = False
	obj.speech = ''
	obj.dic = ''
	obj.term = ''
	obj.comment = ''
	obj.url = ''
	return obj

	
	
class Cells:
	
	def __init__(self):
		if h_request._cells:
			log.append('Cells.__init__',lev_debug,globs['mes'].action_not_required)
		else:
			log.append('Cells.__init__',lev_info,globs['mes'].create_object)
			h_request.collimit()
			h_request.view()
			h_request._cells = []
			Elems()
			if h_request._view == 1:
				self.view1()
			elif h_request._view == 2:
				self.view2()
			else:
				self.view0()

	def view0(self):
		row = []
		for i in range(len(h_request._elems)):
			if h_request._elems[i].dic != '':
				if len(row) > 0:
					while len(row) < h_request._collimit:
						row.append(Cell())
					h_request._cells.append(row)
					row = [h_request._elems[i]]
				else:
					row.append(h_request._elems[i])
			elif h_request._elems[i].speech != '':
				if len(row) > 0:
					while len(row) < h_request._collimit:
						row.append(Cell())
					h_request._cells.append(row)
					# todo: Speech position is hardcoded. Should we enhance this?
					if h_request._collimit >= 2:
						row = [Cell(),h_request._elems[i]]
					else:
						row = [h_request._elems[i]]
				else:
					row.append(h_request._elems[i])
			elif len(row) == h_request._collimit:
				h_request._cells.append(row)
				row = [Cell()]
				row.append(h_request._elems[i])
			else:
				row.append(h_request._elems[i])
			if i == len(h_request._elems) - 1: # Last element
				while len(row) < h_request._collimit:
					row.append(Cell())
				h_request._cells.append(row)
				
	def view1(self):
		columns = []
		column = []
		for i in range(len(h_request._elems)):
			if h_request._elems[i].dic != '':
				if column:
					columns.append(column)
				column = []
				column.append(h_request._elems[i])
			else:
				column.append(h_request._elems[i])
		if column: # Add the last column
			columns.append(column)
		max_cols = 0
		for i in range(len(columns)):
			if len(columns[i]) > max_cols:
				max_cols = len(columns[i])
		for i in range(max_cols):
			row = []
			for j in range(len(columns)):
				if i >= len(columns[j]):
					columns[j].append(Cell())
				row.append(columns[j][i])
			h_request._cells.append(row)

	def view2(self):
		Message('Cells.view',lev_err,globs['mes'].not_implemented)



# Свернуть заданное окно
def iconify(obj):
	if obj and hasattr(obj,'widget'):
		obj.widget.iconify()
	else:
		Message(func='iconify',type=lev_warn,message=globs['mes'].not_enough_input_data)

# Развернуть заданное окно и установить на нем фокус
def deiconify(obj,Silent=False,TakeFocus=True):
	if obj and hasattr(obj,'widget'):
		obj.widget.deiconify()
		# Activates the window in Openbox
		obj.widget.lift()
		# Do not use .focus_set twice on different widgets
		if TakeFocus:
			obj.widget.focus_set()
		if h_os.sys() == 'win':
			obj.widget.wm_attributes('-topmost',1)
			obj.widget.wm_attributes('-topmost',0)
			# Иначе нажатие кнопки будет вызывать переход по ссылке там, где это не надо
			if self.MouseClicked:
				import ctypes
				# Уродливый хак, но иначе никак не поставить фокус на виджет (в Linux/Windows XP обходимся без этого, в Windows 8 - необходимо)
				# Cимулируем нажатие кнопки мыши
				ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left mouse button down
				ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left mouse button up
	else:
		Message(func='deiconify',type=lev_err,message=globs['mes'].not_enough_input_data,Silent=Silent)

# Перехватить нажатие Control-c-c
def timed_update():
	if h_table.CaptureHotkey and kl_mod.result():
		# Позволяет предотвратить зависание потока в версиях Windows старше XP
		if h_os.sys() == 'win':
			kl_mod.keylistener.cancel()
			kl_mod.keylistener.restart()
		h_table.MouseClicked = True
		new_clipboard = init_inst('clipboard').paste()
		if new_clipboard:
			h_table.search = new_clipboard
			h_table.search_online()
		# Использовать то же сочетание клавиш для вызова окна
		deiconify(init_inst('top'),TakeFocus=False)
		# In case of .focus_set() *first* Control-c-c can call an inactive widget
		h_table.search_field.widget.focus_force()
	else:
		h_table.MouseClicked = False
	# We need to have .after in the same function for it to work
	h_quit._id = init_inst('root').widget.after(300,timed_update)
	h_quit.now()



class Quit:
	
	def __init__(self):
		self.Quit = False
		self._id = None # This must be changed externally
	
	def wait(self,*args):
		self.Quit = True
		init_inst('top').close()
		
	def now(self,*args):
		if self.Quit:
			log.append('Quit.now',lev_info,globs['mes'].goodbye)
			kl_mod.keylistener.cancel()
			init_inst('top').widget.destroy()
			init_inst('root').widget.after_cancel(self._id)
			init_inst('root').destroy()
			sys.exit()



class About:
	
	def __init__(self):
		self.Active = False
		self.type = 'About'
		self.parent_obj = Top(init_inst('root'))
		self.widget = self.parent_obj.widget
		self.parent_obj.icon(globs['var']['icon_mclient'])
		self.parent_obj.title(globs['mes'].about)
		frame1 = Frame(self,expand=1,fill='both',side='top')
		frame2 = Frame(self,expand=1,fill='both',side='left')
		frame3 = Frame(self,expand=1,fill='both',side='right')
		label = tk.Label(frame1.widget,font=globs['var']['font_style'],text=globs['mes'].about_text % version)
		label.pack()
		# Лицензия
		Button(frame2,text=globs['mes'].btn_third_parties,hint=globs['mes'].hint_license,action=self.show_third_parties,side='left')
		Button(frame3,text=globs['mes'].btn_license,hint=globs['mes'].hint_license,action=self.open_license_url,side='left')
		# Отправить письмо автору
		Button(frame3,text=globs['mes'].btn_email_author,hint=globs['mes'].hint_email_author,action=self.response_back,side='right')
		self.widget.focus_set()
		create_binding(widget=self.widget,bindings=globs['var']['bind_show_about'],action=self.toggle)
		create_binding(widget=self.widget,bindings='<Escape>',action=self.close)
		self.close()
	
	def close(self,*args):
		self.parent_obj.close()
		self.Active = False
		
	def show(self,*args):
		self.parent_obj.show()
		self.Active = True
	
	def toggle(self,*args):
		if self.Active:
			self.close()
		else:
			self.show()
	
	# Написать письмо автору
	def response_back(self,*args):
		Email(email=email,subject=globs['mes'].program_subject % product).create()

	# Открыть веб-страницу с лицензией
	def open_license_url(self,*args):
		init_inst('online')._url = globs['license_url']
		init_inst('online').browse()

	# Отобразить информацию о лицензии третьих сторон
	def show_third_parties(self,*args):
		init_inst('textbox').update(title=globs['mes'].btn_third_parties+':',text=third_parties,ReadOnly=True,icon=globs['var']['icon_mclient'])
		# todo: Maximize key does not work outside sharedGUI
		init_inst('top_textbox').show()


		
class SaveArticle:
	
	def __init__(self):
		self.type = 'SaveArticle'
		self.parent_obj = Top(init_inst('root'))
		self.obj = ListBox(parent_obj=self.parent_obj,Multiple=False,lst=[globs['mes'].save_view_as_html,globs['mes'].save_article_as_html,globs['mes'].save_article_as_txt,globs['mes'].copy_article_html,globs['mes'].copy_article_txt],title=globs['mes'].select_action,icon=globs['var']['icon_mclient'])
		self.widget = self.obj.widget
		self.custom_bindings()
		self.close()
		
	def custom_bindings(self):
		create_binding(widget=self.parent_obj.widget,bindings=['<Escape>',globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']],action=self.close)
		create_binding(widget=self.widget,bindings=['<Escape>',globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']],action=self.close)
		
	def close(self,*args):
		self.obj.close()
		
	def show(self,*args):
		self.obj.show()
		
	def select(self,*args):
		self.show()
		opt = self.obj.get()
		if opt:
			if opt == globs['mes'].save_view_as_html:
				self.view_as_html()
			elif opt == globs['mes'].save_article_as_html:
				self.raw_as_html()
			elif opt == globs['mes'].save_article_as_txt:
				self.view_as_txt()
			elif opt == globs['mes'].copy_article_html:
				self.copy_raw()
			elif opt == globs['mes'].copy_article_txt:
				self.copy_view()
	
	def view_as_html(self):
		file = dialog_save_file(filetypes=((globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*')))
		if file:
			# We disable AskRewrite because the confirmation is already built in the internal dialog
			WriteTextFile(file,AskRewrite=False).write(h_request._html)
			
	def raw_as_html(self):
		# Ключ 'html' может быть необходим для записи файла, которая производится в кодировке UTF-8, поэтому, чтобы полученная веб-страница нормально читалась, меняем кодировку вручную.
		# Также меняем сокращенные гиперссылки на полные, чтобы они работали и в локальном файле.
		file = dialog_save_file(filetypes=((globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*')))
		if file:
			# todo: fix remaining links to localhost
			WriteTextFile(file,AskRewrite=False).write(h_request._html_raw.replace('charset=windows-1251"','charset=utf-8"').replace('<a href="m.exe?','<a href="'+online_url_root).replace('../c/m.exe?',online_url_root))
		
	def view_as_txt(self):
		file = dialog_save_file(filetypes=((globs['mes'].plain_text,'.txt'),(globs['mes'].all_files,'*')))
		if file:
			WriteTextFile(file,AskRewrite=False).write(h_request._text)
			
	def copy_raw(self):
		init_inst('clipboard').copy(h_request._html_raw)
			
	def copy_view(self):
		init_inst('clipboard').copy(h_request._text)

	

# Search IN an article
class SearchArticle:
	
	def __init__(self):
		self.type = 'SearchArticle'
		self.obj = init_inst('entry')
		self.widget = self.obj.widget
		self.parent_obj = init_inst('top_entry')
		self.parent_obj.icon(globs['var']['icon_mclient'])
		self.parent_obj.title(globs['mes'].search_word)
		create_binding(widget=self.widget,bindings=globs['var']['bind_search_article_forward'],action=self.close)
		create_binding(widget=self.widget,bindings='<Escape>',action=self.close)
		self.widget.focus_set()
		self.close()
		self.reset()
	
	def reset(self):
		self._list = []
		self._pos = -1
		self._search = ''
		# Plus: keeping old input
		# Minus: searching old input after cancelling the search and searching again
		#self.clear()
	
	def clear(self,*args):
		self.obj.clear_text()
	
	def close(self,*args):
		self.parent_obj.close()
		
	def show(self,*args):
		self.parent_obj.show()
		self.obj.select_all()
			
	# Create a list of all matches in the article
	def matches(self):
		if self.search():
			for i in range(len(h_request.cells())):
				for j in range(len(h_request._cells[i])):
					# todo: Для всех вхождений, а не только терминов
					if h_request._cells[i][j].Selectable and self._search in h_request._cells[i][j].term.lower():
						self._list.append((i,j))
	
	def search(self):
		if not self._search:
			self.show()
			self._search = self.widget.get().strip(' ').strip('\n').lower()
		return self._search
	
	def list(self):
		if not self._list:
			self.matches()
		return self._list
	
	def forward(self):
		if self._pos + 1 < len(self.list()):
			self._pos += 1
		else:
			Message(func='SearchArticle.forward',type=lev_info,message=globs['mes'].search_from_start)
			self._pos = 0
	
	def backward(self):
		if self._pos > 0:
			self._pos -= 1
		else:
			Message(func='SearchArticle.backward',type=lev_info,message=globs['mes'].search_from_end)
			self._pos = len(self.list()) - 1

	
	
# Search FOR an article
class SearchField:
	
	def __init__(self,parent_obj,side='left',ipady=5):
		self.type = 'SearchField'
		self.parent_obj = parent_obj
		# Поле ввода поисковой строки
		self.widget = tk.Entry(self.parent_obj.widget)
		# Подгоняем высоту поисковой строки под высоту графических кнопок; значение 5 подобрано опытным путем
		self.widget.pack(side=side,ipady=ipady)
		
	def clear(self,*args):
		self.widget.delete(0,'end')
		self.widget.selection_clear()
		
	# Очистить строку поиска и вставить в нее заданный текст или содержимое буфера обмена
	def paste(self,text=None):
		self.clear()
		if text:
			self.widget.insert(0,text)
		else:
			self.widget.insert(0,init_inst('clipboard').paste())
		return 'break'
		
	# Вставить предыдущий запрос
	def insert_repeat_sign(self,*args):
		if h_db._count > 0:
			init_inst('clipboard').copy(str(h_db.prev()))
			self.paste()

	# Вставить запрос до предыдущего
	def insert_repeat_sign2(self,*args):
		if h_db._count > 1:
			init_inst('clipboard').copy(str(h_db.preprev()))
			self.paste()
			
			
			
class SpecSymbols:
	
	def __init__(self):
		self.obj = Top(init_inst('root'))
		self.widget = self.obj.widget
		self.obj.icon(globs['var']['icon_mclient'])
		self.obj.title(globs['mes'].paste_spec_symbol)
		self.frame = Frame(self.obj,expand=1)
		for i in range(len(globs['var']['spec_syms'])):
			if i % 10 == 0:
				self.frame = Frame(self.obj,expand=1)
			# lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
			# width и height нужны для Windows
			self.button = tk.Button(self.frame.widget,text=globs['var']['spec_syms'][i],command=lambda i=i:h_table.insert_sym(globs['var']['spec_syms'][i]),width=2,height=2).pack(side='left',expand=1)
		self.custom_bindings()
		self.close()
		
	def custom_bindings(self):
		create_binding(widget=self.widget,bindings=['<Escape>',globs['var']['bind_spec_symbol']],action=self.close)
	
	def show(self,*args):
		self.obj.show()
		
	def close(self,*args):
		self.obj.close()
		
		
		
class History:
	
	def __init__(self):
		self.parent_obj = Top(init_inst('root'))
		self.parent_obj.widget.geometry('250x350')
		self._title = globs['mes'].btn_history
		self._icon = globs['var']['icon_mclient']
		self.obj = ListBox(parent_obj=self.parent_obj,title=self._title,icon=self._icon,SelectFirst=False,SelectionCloses=False,SingleClick=False,Composite=True,user_function=self.go)
		self.widget = self.obj.widget
		self.Active = False
		create_binding(widget=self.parent_obj.widget,bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history_alt'],'<Escape>'],action=self.toggle)
		create_binding(widget=self.parent_obj.widget,bindings=globs['var']['bind_clear_history_alt'],action=self.clear)
		self.close()
	
	def autoselect(self):
		self.obj._index = h_db._id
		self.obj.select()
	
	def show(self,*args):
		self.Active = True
		self.fill()
		self.parent_obj.show()
		self.widget.focus_set()
		
	def close(self,*args):
		self.Active = False
		self.parent_obj.close()
		
	def fill(self):
		self.obj.reset(lst=h_db.searches(),title=self._title,icon=self._icon)
	
	def update(self):
		self.fill()
		self.autoselect()
		
	def clear(self,*args):
		self.obj.clear()
		h_request.reset()
		h_db.reset()
		h_db.search_part()
		h_table.load_article()
		self.update()
	
	def toggle(self,*args):
		if self.Active:
			self.close()
		else:
			self.show()
			
	def go(self,*args):
		h_db._id = self.obj.index()
		h_db.copy()
		h_table.load_article()
		
	# Скопировать элемент истории
	def copy(self,*args):
		init_inst('clipboard').copy(h_request.search())



class Moves:
	
	def __init__(self):
		if h_request._moves:
			log.append('Moves.__init__',lev_debug,globs['mes'].action_not_required)
		else:
			log.append('Moves.__init__',lev_info,globs['mes'].create_object)
			Cells()
			h_request._moves = {'_move_right':[],'_move_left':[],'_move_down':[],'_move_up':[],'_move_line_start':[],'_move_line_end':[],'_move_text_start':[],'_move_text_end':[]}
			self.text_start()
			self.text_end()
			self.right()
			self.left()
			self.down()
			self.up()
			self.line_start()
			self.line_end()
		
	# Вернуть первую выделяемую ячейку по вертикали в направлении сверху вниз
	def get_vert_selectable(self,cur_i=0,cur_j=0,GetNext=True):
		func_res = (cur_i,cur_j)
		i = cur_i
		while i < len(h_request._cells):
			# todo: Алгоритм для globs['bool']['SelectTermsOnly']
			if h_request._cells[i][cur_j].Selectable:
				if GetNext:
					if i != cur_i:
						func_res = (i,cur_j)
						break
				else:
					func_res = (i,cur_j)
					break
			i += 1
		#log.append('TkinterHtmlMod.get_vert_selectable',lev_debug,str(func_res))
		return func_res
		
	# Вернуть первую выделяемую ячейку по вертикали в направлении снизу вверх
	def get_vert_selectable_backwards(self,cur_i=0,cur_j=0,GetPrevious=True,Silent=False,Critical=False):
		func_res = (cur_i,cur_j)
		i = cur_i
		while i >= 0:
			# todo: Алгоритм для globs['bool']['SelectTermsOnly']
			if h_request._cells[i][cur_j].Selectable:
				if GetPrevious:
					if i != cur_i:
						func_res = (i,cur_j)
						break
				else:
					func_res = (i,cur_j)
					break
			i -= 1
		#log.append('TkinterHtmlMod.get_vert_selectable_backwards',lev_debug,str(func_res))
		return func_res

	# Список ячеек, выбираемых слева направо
	def right(self):
		if not h_request._moves['_move_right']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					tmp_lst += [self.get_selectable(i,j)]
				h_request._moves['_move_right'] += [tmp_lst]
		return h_request._moves['_move_right']
	
	# Список ячеек, выбираемых справа налево
	def left(self): # Просто перевернуть self._move_right оказывается недостаточным
		if not h_request._moves['_move_left']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					tmp_lst += [self.get_selectable_backwards(i,j)]
				h_request._moves['_move_left'] += [tmp_lst]
		return h_request._moves['_move_left']

	# Список для перехода на первые выделяемые ячейки
	def line_start(self):
		if not h_request._moves['_move_line_start']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					tmp_lst += [self.get_selectable(i,0,False)]
				h_request._moves['_move_line_start'] += [tmp_lst]
		return h_request._moves['_move_line_start']

	# Список для перехода на последние выделяемые ячейки
	def line_end(self):
		if not h_request._moves['_move_line_end']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					# Алгоритм не принимает -1, необходимо точно указывать позицию
					tmp_lst += [self.get_selectable_backwards(i,len(h_request._cells[i])-1,False)]
				h_request._moves['_move_line_end'] += [tmp_lst]
		return h_request._moves['_move_line_end']

	# Первая выделяемая ячейка
	def text_start(self):
		# todo: Почему не удается использовать 'move_left', 'move_up'?
		if not h_request._moves['_move_text_start']:
			h_request._moves['_move_text_start'] = self.get_selectable(0,0,False)
		return h_request._moves['_move_text_start']
		
	# Последняя выделяемая ячейка
	def text_end(self):
		# todo: Почему не удается использовать 'move_right', 'move_down'?
		if not h_request._moves['_move_text_end']:
			h_request._moves['_move_text_end'] = self.get_selectable_backwards(len(h_request._cells)-1,len(h_request._cells[-1])-1,False)
		return h_request._moves['_move_text_end']
		
	# Логика 'move_up' и 'move_down': идем вверх/вниз по тому же столбцу. Если на текущей строке нет выделяемой ячейки в нужном столбце, тогда пропускаем ее. Если дошли до конца столбца, переходим на первую/последнюю строку последующего/предыдущего столбца.
	def down(self):
		if not h_request._moves['_move_down']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					# Номер строки, на которой находится конечная выделяемая ячейка при навигации сверху вниз. Обратить внимание, что это не обязательно последняя строка в статье!
					# Возможно, имеет смысл вынести max_i в отдельный список, чтобы не вычислять его лишний раз. Но будет ли это быстрее?
					max_i = self.get_vert_selectable_backwards(len(h_request._cells)-1,j,GetPrevious=False)[0]
					cell = self.get_vert_selectable(i,j)
					# Просто == не работает
					if i >= max_i:
						# Если достигнут конец текущего столбца, перейти на первую выделяемую ячейку следующего столбца
						if j < len(h_request._cells[i]) - 1:
							tmp_lst.append(self.get_vert_selectable(0,j+1,GetNext=False))
						else:
							tmp_lst.append((i,j))
					elif cell == (i,j):
						tmp_lst.append(self.get_selectable(i,0))
					else:
						tmp_lst.append(cell)
				h_request._moves['_move_down'] += [tmp_lst]
		return h_request._moves['_move_down']
	
	def up(self):
		if not h_request._moves['_move_up']:
			for i in range(len(h_request._cells)):
				tmp_lst = []
				for j in range(len(h_request._cells[i])):
					# Номер строки, на которой находится первая выделяемая ячейка при навигации снизу вверх. Обратить внимание, что это не обязательно первая строка в статье!
					# Возможно, имеет смысл вынести min_i в отдельный список, чтобы не вычислять его лишний раз. Но будет ли это быстрее?
					min_i = self.get_vert_selectable(0,j,GetNext=False)[0]
					cell = self.get_vert_selectable_backwards(i,j)
					# Просто == не работает
					if i <= min_i:
						# Если достигнута самая первая выделяемая ячейка, не продолжать с последнего столбца статьи. Для 'move_down' такая проверка почему-то не обязательна.
						if i == h_request._moves['_move_text_start'][0] and j == h_request._moves['_move_text_start'][1]:
							tmp_lst.append((i,j))
						# Если достигнут конец текущего столбца, перейти на последнюю выделяемую ячейку предыдущего столбца
						elif j > 0:
							tmp_lst.append(self.get_vert_selectable_backwards(len(h_request._cells)-1,j-1,GetPrevious=False))
						else:
							tmp_lst.append((i,j))
					elif cell == (i,j):
						tmp_lst.append(self.get_selectable_backwards(i,0))
					else:
						tmp_lst.append(cell)
				h_request._moves['_move_up'] += [tmp_lst]
		return h_request._moves['_move_up']

	# Определить следующую (+1,+1) ячейку, которую можно выделить
	''' Если выделить можно любую ячейку, то будет выбрана следующая по очереди. Обратить внимание: в конце таблицы, там, где выделяемых ячеек уже нет, будет возвращаться текущая ячейка. Это логично, если выбрать можно любую ячейку, но не совсем логично, если выбирать только помеченные ячейки. Впрочем, если указано использование помеченных ячеек, а ячейка не помечена, то переход на нее осуществлен не будет, поэтому и ссылка в ней использована не будет.
	'''
	def get_selectable(self,cur_i=0,cur_j=0,GetNext=True):
		Found = False
		i = sel_i = cur_i
		j = sel_j = cur_j
		while i < len(h_request._cells):
			while j < len(h_request._cells[i]):
				if globs['bool']['SelectTermsOnly']:
					if h_request._cells[i][j].Selectable:
						# Позволяет вернуть последнюю ячейку, которую можно выделить, если достигнут конец таблицы
						sel_i, sel_j = i, j
						# Если указаная ячейка уже может быть выбрана, то игнорировать ее и искать следующую
						if GetNext:
							if cur_i != i or cur_j != j:
								Found = True
								break
						else:
							Found = True
							break
				else:
					sel_i, sel_j = i, j
					if cur_i != i or cur_j != j:
						Found = True
						break
				j += 1
			if Found:
				break
			j = 0
			i += 1
		#log.append('TkinterHtmlMod.get_selectable',lev_debug,str((sel_i,sel_j)))
		return(sel_i,sel_j)
		
	# Определить предыдущую (-1,-1) ячейку, которую можно выделить
	def get_selectable_backwards(self,cur_i,cur_j,GetPrevious=True):
		Found = False
		i = sel_i = cur_i
		j = sel_j = cur_j
		while i >= 0:
			while j >= 0:
				if globs['bool']['SelectTermsOnly']:
					if h_request._cells[i][j].Selectable:
						# Позволяет вернуть последнюю ячейку, которую можно выделить, если достигнут конец таблицы
						sel_i = i
						sel_j = j
						# Если указаная ячейка уже может быть выбрана, то игнорировать ее и искать следующую
						if GetPrevious:
							if cur_i != i or cur_j != j:
								Found = True
								break
						else:
							Found = True
							break
				else:
					sel_i, sel_j = i, j
					if cur_i != i or cur_j != j:
						Found = True
						break
				j -= 1
			if Found:
				break
			i -= 1
			j = len(h_request._cells[i]) - 1
		#log.append('TkinterHtmlMod.get_selectable_backwards',lev_debug,str((sel_i,sel_j)))
		return(sel_i,sel_j)



"""Wrapper for the Tkhtml widget from http://tkhtml.tcl.tk/tkhtml.html"""
class TkinterHtmlMod(tk.Widget):

	def __init__(self,master,cfg={},**kw):
		self.i = 0
		self.j = 0
		self.pos2cell = []
		self._node = None
		self.index = None
		self._offset = None
		self._selection_end_node = None
		self._selection_end_offset = None
		self.mouse_index = -1 # self.mouse_index (int) != self.index (tuple)
		self._search_list = []
		self._search_article_pos = 0
		self.CaptureHotkey = True
		self.MouseClicked = False
		self.event = None
		self.url = h_request._url
		self.search = h_request._search
		
		self.master = master
		self.location = self.get_tkhtml_folder()
		self.load_tkhtml()
		self.widget = tk.Widget
		self.obj = self.widget.__init__(self,master,'html',cfg,kw)
		self.vsb = ttk.Scrollbar(self.obj,orient=tk.VERTICAL)
		self.hsb = ttk.Scrollbar(self.obj,orient=tk.HORIZONTAL)
		self.widget.configure(self,yscrollcommand=self.vsb.set)
		self.widget.configure(self,xscrollcommand=self.hsb.set)
		self.vsb.config(command=self.yview)
		self.hsb.config(command=self.xview)
		
		self.search_article = SearchArticle()
		self.spec_symbols = SpecSymbols()
		self.save_article = SaveArticle()
		
		# todo: The same does not work when imported from sharedGUI for some reason
		if h_os.sys() == 'lin':
			init_inst('top').widget.wm_attributes('-zoomed',True)
		# Win, Mac
		else:
			init_inst('top').widget.wm_state(newstate='zoomed')
		self.history = History()
		self.create_frame_panel()
		self.search_field.widget.focus_set()
		create_binding(widget=self,bindings=globs['var']['bind_go_url'],action=self.go_url)
		self.bind("<Motion>",self.mouse_sel,True)
		# ВНИМАНИЕ: По непонятной причине, не работает привязка горячих клавиш (только мышь) для данного виджета, работает только для основного виджета!
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_copy_sel'],globs['var']['bind_copy_sel_alt'],globs['var']['bind_copy_sel_alt2']],action=self.copy_cell)
		# По неясной причине в одной и той же Windows ИНОГДА не удается включить '<KP_Delete>'
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_delete_cell'],action=self.delete_cell)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_add_cell'],action=self.add_cell)
		self.widget_width = 0
		self.widget_height = 0
		self.widget_offset_x = 0
		self.widget_offset_y = 0
		self.top_bbox = 0
		self.bottom_bbox = 0
		
	def get_url(self):
		# Note: encoding must be UTF-8 here
		init_inst('online').reset(self.get_pair(),self.search)
		self.url = init_inst('online').url()
		log.append('TkinterHtmlMod.get_url',lev_debug,"self.url: %s" % str(self.url))
	
	# todo: move 'move_*' procedures to Moves class
	# Перейти на 1-й термин текущей строки	
	def move_line_start(self,*args):
		if len(h_request._moves['_move_line_start']) > self.i and len(h_request._moves['_move_line_start'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_line_start'][self.i][self.j]
			self.set_cell()
		else:
			log.append('TkinterHtmlMod.move_line_start',lev_err,globs['mes'].wrong_input2)

	# Перейти на последний термин текущей строки
	def move_line_end(self,*args):
		if len(h_request._moves['_move_line_end']) > self.i and len(h_request._moves['_move_line_end'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_line_end'][self.i][self.j]
			self.set_cell()

	# Перейти на 1-й термин статьи
	def move_text_start(self,*args):
		self.i, self.j = h_request._moves['_move_text_start']
		self.set_cell()

	# Перейти на последний термин статьи
	def move_text_end(self,*args):
		self.i, self.j = h_request._moves['_move_text_end']
		self.set_cell()

	# Перейти на страницу вверх
	def move_page_up(self,event=None):
		if event:
			self.event = event
		self.yview_scroll(-1,'pages')
		self.mouse_sel()

	# Перейти на страницу вверх
	def move_page_down(self,event=None):
		if event:
			self.event = event
		self.yview_scroll(1,'pages')
		self.mouse_sel()

	# Перейти на предыдущий термин
	def move_left(self,*args):
		if len(h_request._moves['_move_left']) > self.i and len(h_request._moves['_move_left'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_left'][self.i][self.j]
			self.set_cell()
		else:
			log.append('TkinterHtmlMod.move_left',lev_err,globs['mes'].wrong_input2)

	# Перейти на следующий термин
	def move_right(self,*args):
		if len(h_request._moves['_move_right']) > self.i and len(h_request._moves['_move_right'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_right'][self.i][self.j]
			self.set_cell()
		else:
			log.append('TkinterHtmlMod.move_right',lev_err,globs['mes'].wrong_input2)

	# Перейти на строку вниз
	def move_down(self,*args):
		if len(h_request._moves['_move_down']) > self.i and len(h_request._moves['_move_down'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_down'][self.i][self.j]
			self.set_cell()
		else:
			log.append('TkinterHtmlMod.move_down',lev_err,globs['mes'].wrong_input2)

	# Перейти на строку вверх
	def move_up(self,*args):
		if len(h_request._moves['_move_up']) > self.i and len(h_request._moves['_move_up'][self.i]) > self.j:
			self.i, self.j = h_request._moves['_move_up'][self.i][self.j]
			self.set_cell()
		else:
			log.append('TkinterHtmlMod.move_up',lev_err,globs['mes'].wrong_input2)
	
	# Задействование колеса мыши для пролистывания экрана
	def mouse_wheel(self,event):
		self.event = event
		# В Windows XP delta == -120, однако, в других версиях оно другое
		if self.event.num == 5 or self.event.delta < 0:
			self.move_page_down()
		# В Windows XP delta == 120, однако, в других версиях оно другое
		if self.event.num == 4 or self.event.delta > 0:
			self.move_page_up()
		return 'break'
	
	# Следить за буфером обмена
	def watch_clipboard(self,*args):
		if self.CaptureHotkey:
			self.CaptureHotkey = False
		else:
			self.CaptureHotkey = True
		self.update_buttons()
	
	# Открыть URL текущей статьи в браузере
	def open_in_browser(self,*args):
		init_inst('online')._url = h_request._url
		init_inst('online').browse()
	
	# Скопировать URL текущей статьи или выделения
	def copy_url(self,obj,mode='article'):
		cur_url = online_url_safe
		if mode == 'term':
			# Скопировать URL текущего термина. URL 1-го термина не совпадает с URL статьи!
			cur_url = h_request._cells[self.i][self.j].url
			if globs['bool']['Iconify']:
				iconify(obj)
		elif mode == 'article':
			# Скопировать URL статьи
			cur_url = h_request._url
			if globs['bool']['Iconify']:
				iconify(obj)
		else:
			Message(func='TkinterHtmlMod.copy_url',type=lev_err,message=globs['mes'].unknown_mode % (str(mode),'article, term'))
		init_inst('clipboard').copy(cur_url)

	# Открыть веб-страницу с определением текущего термина
	def define(self,Selected=True): # Selected: True: Выделенный термин; False: Название статьи
		# cur
		if Selected:
			search_str = 'define:' + h_request._cells[self.i][self.j].term
		else:
			search_str = 'define:' + h_request._search
		init_inst('online').reset(base_str=globs['var']['web_search_url'],search_str=search_str)
		init_inst('online').browse()
	
	# Обновить рисунки на кнопках
	def update_buttons(self):
		if h_db._count > 0:
			self.btn_repeat_sign.active()
		else:
			self.btn_repeat_sign.inactive()

		if h_db._count > 1:
			self.btn_repeat_sign2.active()
		else:
			self.btn_repeat_sign2.inactive()

		if h_db._id > 0:
			self.btn_prev.active()
		else:
			self.btn_prev.inactive()

		if h_db._count > 1 and h_db._id < h_db._count - 1:
			self.btn_next.active()
		else:
			self.btn_next.inactive()

		if self.CaptureHotkey:
			self.btn_clipboard.active()
		else:
			self.btn_clipboard.inactive()
			
		# todo: Change active/inactive button logic in case of creating three or more views
		if h_request.view() == 0:
			self.btn_toggle_view.active()
		else:
			self.btn_toggle_view.inactive()
			
	# Перейти на предыдущий запрос
	def go_back(self,*args):
		old_index = h_db._id
		h_db.index_subtract()
		if old_index != h_db._id:
			h_db.copy()
			self.load_article()

	# Перейти на следующий запрос
	def go_forward(self,*args):
		old_index = h_db._id
		h_db.index_add()
		if old_index != h_db._id:
			h_db.copy()
			self.load_article()

	def control_length(self): # Confirm too long requests
		Confirmed = True
		if len(self.search) >= 150:
			if not Message(func='TkinterHtmlMod.control_length',type=lev_ques,message=globs['mes'].long_request % len(self.search)).Yes:
				Confirmed = False
		return Confirmed
	
	def drag_search(self):
		if self.search_article.list():
			self.i, self.j = self.search_article._list[self.search_article._pos]
			self.set_cell()
			if len(self.index) > 0:
				self.yview_name(self.index[0])
	
	def search_reset(self,*args): # SearchArticle
		self.search_article.reset()
		self.search_forward()
	
	def search_backward(self,*args): # SearchArticle
		self.search_article.backward()
		self.drag_search()
	
	def search_forward(self,*args): # SearchArticle
		self.search_article.forward()
		self.drag_search()
	
	def search_online(self):
		if self.control_length():
			self.get_url()
			h_request._url = self.url
			h_request._search = self.search
			h_request.new()
			h_db.search_part()
			log.append('TkinterHtmlMod._go_search',lev_debug,h_request._search)
			self.load_article()
	
	# Search the selected term online using the entry widget (search field)
	def go_search(self,*args):
		self.search = self.search_field.widget.get().strip('\n').strip(' ')
		# Allows to use the same hotkeys for the search field and the article field
		if self.search == '':
			self.go_url()
		else:
			# Скопировать предпоследний запрос в буфер и вставить его в строку поиска (например, для перехода на этот запрос еще раз)
			if self.search == globs['var']['repeat_sign2']:
				self.search_field.insert_repeat_sign2()
			# Скопировать последний запрос в буфер и вставить его в строку поиска (например, для корректировки)
			elif self.search == globs['var']['repeat_sign']:
				self.search_field.insert_repeat_sign()
			else:
				self.search_online()
					
	# Создание каркаса с полем ввода, кнопкой выбора направления перевода и кнопкой выхода
	def create_frame_panel(self):
		self.frame_panel = Frame(init_inst('top'),expand=0,fill='x',side='bottom')
		# Поле ввода поисковой строки
		self.search_field = SearchField(parent_obj=self.frame_panel)
		self.draw_buttons()
		if self.CaptureHotkey:
			self.btn_clipboard.active()
		else:
			self.btn_clipboard.inactive()
		self.hotkeys()
		
	def get_pair(self):
		return online_dic_urls[self.option_menu.index]
	
	# Создать кнопки
	def draw_buttons(self):
		# Кнопка для "чайников", заменяет Enter в search_field
		Button(self.frame_panel,text=globs['mes'].btn_translate,hint=globs['mes'].btn_translate,action=self.go_search,inactive_image_path=globs['var']['icon_go_search'],active_image_path=globs['var']['icon_go_search'],bindings=[globs['var']['bind_go_search'],globs['var']['bind_go_search_alt']]) # В данном случае btn = hint
		# Кнопка очистки строки поиска
		Button(self.frame_panel,text=globs['mes'].btn_clear,hint=globs['mes'].hint_clear_search_field,action=self.search_field.clear,inactive_image_path=globs['var']['icon_clear_search_field'],active_image_path=globs['var']['icon_clear_search_field'],bindings=[globs['var']['bind_clear_search_field']])
		# Кнопка вставки
		Button(self.frame_panel,text=globs['mes'].btn_paste,hint=globs['mes'].hint_paste_clipboard,action=self.search_field.paste,inactive_image_path=globs['var']['icon_paste'],active_image_path=globs['var']['icon_paste'],bindings=['<Control-v>'])
		# Кнопка вставки текущего запроса
		self.btn_repeat_sign = Button(self.frame_panel,text=globs['mes'].btn_repeat_sign,hint=globs['mes'].hint_paste_cur_request,action=self.search_field.insert_repeat_sign,inactive_image_path=globs['var']['icon_repeat_sign_off'],active_image_path=globs['var']['icon_repeat_sign'],bindings=globs['var']['repeat_sign'])
		# Кнопка вставки предыдущего запроса
		self.btn_repeat_sign2 = Button(self.frame_panel,text=globs['mes'].btn_repeat_sign2,hint=globs['mes'].hint_paste_prev_request,action=self.search_field.insert_repeat_sign2,inactive_image_path=globs['var']['icon_repeat_sign2_off'],active_image_path=globs['var']['icon_repeat_sign2'],bindings=globs['var']['repeat_sign2'])
		# Кнопка для вставки спец. символов
		Button(self.frame_panel,text=globs['mes'].btn_symbols,hint=globs['mes'].hint_symbols,action=self.spec_symbols.show,inactive_image_path=globs['var']['icon_spec_symbol'],active_image_path=globs['var']['icon_spec_symbol'],bindings=globs['var']['bind_spec_symbol'])
		# Выпадающий список с вариантами направлений перевода
		self.option_menu = OptionMenu(parent_obj=self.frame_panel,items=pairs)
		# Кнопка изменения вида статьи
		# todo: Change active/inactive button logic in case of creating three or more views
		self.btn_toggle_view = Button(self.frame_panel,text=globs['mes'].btn_toggle_view,hint=globs['mes'].hint_toggle_view,action=self.toggle_view,inactive_image_path=globs['var']['icon_toggle_view_ver'],active_image_path=globs['var']['icon_toggle_view_hor'],bindings=[globs['var']['bind_toggle_view'],globs['var']['bind_toggle_view_alt']])
		# Кнопка перехода на предыдущую статью
		self.btn_prev = Button(self.frame_panel,text=globs['mes'].btn_prev,hint=globs['mes'].hint_preceding_article,action=self.go_back,inactive_image_path=globs['var']['icon_go_back_off'],active_image_path=globs['var']['icon_go_back'],bindings=globs['var']['bind_go_back'])
		# Кнопка перехода на следующую статью
		self.btn_next = Button(self.frame_panel,text=globs['mes'].btn_next,hint=globs['mes'].hint_following_article,action=self.go_forward,inactive_image_path=globs['var']['icon_go_forward_off'],active_image_path=globs['var']['icon_go_forward'],bindings=globs['var']['bind_go_forward'])
		# Кнопка включения/отключения истории
		self.button = Button(self.frame_panel,text=globs['mes'].btn_history,hint=globs['mes'].hint_history,action=self.history.toggle,inactive_image_path=globs['var']['icon_toggle_history'],active_image_path=globs['var']['icon_toggle_history'],bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history_alt']])
		create_binding(widget=self.button.widget,bindings=globs['var']['bind_clear_history'],action=self.history.clear)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_clear_history_alt'],action=self.history.clear)
		# Кнопка очистки истории
		Button(self.frame_panel,text=globs['mes'].btn_clear_history,hint=globs['mes'].hint_clear_history,action=self.history.clear,inactive_image_path=globs['var']['icon_clear_history'],active_image_path=globs['var']['icon_clear_history'],bindings=globs['var']['bind_clear_history_alt'])
		# Кнопка перезагрузки статьи
		Button(self.frame_panel,text=globs['mes'].btn_reload,hint=globs['mes'].hint_reload_article,action=self.reload,inactive_image_path=globs['var']['icon_reload'],active_image_path=globs['var']['icon_reload'],bindings=[globs['var']['bind_reload_article'],globs['var']['bind_reload_article_alt']])
		# Кнопка "Поиск в статье"
		Button(self.frame_panel,text=globs['mes'].btn_search,hint=globs['mes'].hint_search_article,action=self.search_reset,inactive_image_path=globs['var']['icon_search_article'],active_image_path=globs['var']['icon_search_article'],bindings=globs['var']['bind_re_search_article'])
		# Кнопка "Сохранить"
		Button(self.frame_panel,text=globs['mes'].btn_save,hint=globs['mes'].hint_save_article,action=self.save_article.select,inactive_image_path=globs['var']['icon_save_article'],active_image_path=globs['var']['icon_save_article'],bindings=[globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']])
		# Кнопка "Открыть в браузере"
		Button(self.frame_panel,text=globs['mes'].btn_in_browser,hint=globs['mes'].hint_in_browser,action=self.open_in_browser,inactive_image_path=globs['var']['icon_open_in_browser'],active_image_path=globs['var']['icon_open_in_browser'],bindings=[globs['var']['bind_open_in_browser'],globs['var']['bind_open_in_browser_alt']])
		# Кнопка толкования термина. Сделана вспомогательной ввиду нехватки места
		Button(self.frame_panel,text=globs['mes'].btn_define,hint=globs['mes'].hint_define,action=lambda:self.define(Selected=False),inactive_image_path=globs['var']['icon_define'],active_image_path=globs['var']['icon_define'],bindings=globs['var']['bind_define'])
		# Кнопка "Перехват Ctrl-c-c"
		self.btn_clipboard = Button(self.frame_panel,text=globs['mes'].btn_clipboard,hint=globs['mes'].hint_watch_clipboard,action=self.watch_clipboard,inactive_image_path=globs['var']['icon_watch_clipboard_off'],active_image_path=globs['var']['icon_watch_clipboard_on'],fg='red',bindings=[])
		# Кнопка "О программе"
		Button(self.frame_panel,text=globs['mes'].btn_about,hint=globs['mes'].hint_about,action=init_inst('about').show,inactive_image_path=globs['var']['icon_show_about'],active_image_path=globs['var']['icon_show_about'],bindings=globs['var']['bind_show_about'])
		# Кнопка выхода
		Button(self.frame_panel,text=globs['mes'].btn_x,hint=globs['mes'].hint_x,action=h_quit.wait,inactive_image_path=globs['var']['icon_quit_now'],active_image_path=globs['var']['icon_quit_now'],side='right',bindings=[globs['var']['bind_quit_now'],globs['var']['bind_quit_now_alt']])

	def hotkeys(self):
		# Привязки: горячие клавиши и кнопки мыши
		create_binding(widget=self.history.widget,bindings=globs['var']['bind_copy_history'],action=self.history.copy)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_go_search'],globs['var']['bind_go_search_alt']],action=self.go_search)
		# todo: do not iconify at <ButtonRelease-3>
		create_binding(widget=self.search_field.widget,bindings=globs['var']['bind_clear_search_field'],action=self.search_field.clear)
		create_binding(widget=self.search_field.widget,bindings=globs['var']['bind_paste_search_field'],action=lambda e:self.search_field.paste())
		if h_os.sys() == 'win' or h_os.sys() == 'mac':
			create_binding(widget=init_inst('top').widget,bindings='<MouseWheel>',action=self.mouse_wheel)
		else:
			create_binding(widget=init_inst('top').widget,bindings=['<Button 4>','<Button 5>'],action=self.mouse_wheel)
		# Перейти на предыдущую/следующую статью
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_go_back'],action=self.go_back)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_go_forward'],action=self.go_forward)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_left'],action=self.move_left)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_right'],action=self.move_right)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_down'],action=self.move_down)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_up'],action=self.move_up)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_line_start'],action=self.move_line_start)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_line_end'],action=self.move_line_end)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_text_start'],action=self.move_text_start)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_text_end'],action=self.move_text_end)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_page_up'],action=self.move_page_up)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_move_page_down'],action=self.move_page_down)
		create_binding(widget=init_inst('top').widget,bindings='<Escape>',action=lambda e:iconify(init_inst('top')))
		create_binding(widget=self,bindings=globs['var']['bind_iconify'],action=lambda e:iconify(init_inst('top')))
		# Дополнительные горячие клавиши
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_quit_now'],globs['var']['bind_quit_now_alt']],action=h_quit.wait)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_search_article_forward'],action=self.search_forward)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_search_article_backward'],action=self.search_backward)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_re_search_article'],action=self.search_reset)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_reload_article'],globs['var']['bind_reload_article_alt']],action=self.reload)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']],action=self.save_article.select)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_show_about'],action=init_inst('about').show)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history']],action=self.history.toggle)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history_alt']],action=self.history.toggle)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_open_in_browser'],globs['var']['bind_open_in_browser_alt']],action=self.open_in_browser)
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_copy_url'],action=lambda e:self.copy_url(init_inst('top'),mode='term'))
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_copy_article_url'],action=lambda e:self.copy_url(init_inst('top'),mode='article'))
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_spec_symbol']],action=self.spec_symbols.show)
		create_binding(widget=self.search_field.widget,bindings='<Control-a>',action=lambda e:select_all(self.search_field.widget,Small=True))
		create_binding(widget=init_inst('top').widget,bindings=globs['var']['bind_define'],action=lambda e:self.define(Selected=True))
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_prev_pair'],globs['var']['bind_prev_pair_alt']],action=self.option_menu.set_prev)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_next_pair'],globs['var']['bind_next_pair_alt']],action=self.option_menu.set_next)
		create_binding(widget=init_inst('top').widget,bindings=[globs['var']['bind_toggle_view'],globs['var']['bind_toggle_view_alt']],action=self.toggle_view)
		
	def show(self):
		self.vsb.pack(side='right',fill='y')
		self.hsb.pack(side='bottom',fill='x')
		self.pack(expand=1,fill='both')
		
	# Загрузить библиотеку tkhtml
	def load_tkhtml(self):
		if self.location:
			self.master.tk.eval('global auto_path; lappend auto_path {%s}' % self.location)
		self.master.tk.eval('package require Tkhtml')

	# Вернуть местоположение библиотеки tkhtml
	def get_tkhtml_folder(self):
		# globs['bin_dir']
		return os.path.join (Path(os.path.abspath(sys.argv[0])).dirname(),
							 "tkhtml",
							 platform.system().replace("Darwin", "MacOSX"),
							 "64-bit" if sys.maxsize > 2**32 else "32-bit")
							 
	def get_cell(self,index):
		if len(self.pos2cell) > index:
			parts = self.pos2cell[index]
		else:
			parts = (0,0)
			log.append('TkinterHtmlMod.get_cell',lev_err,globs['mes'].wrong_input2)
		if globs['bool']['SelectTermsOnly']:
			if len(h_request._cells) > parts[0] and len(h_request._cells[self.i]) > parts[1]:
				if h_request._cells[parts[0]][parts[1]].Selectable:
					self.i, self.j = parts
		else:
			self.i, self.j = parts
	
	def node(self, *arguments):
		return self.tk.call(self._w, "node", *arguments)

	def parse(self, *args):
		self.tk.call(self._w, "parse", *args)

	def reset(self):
		return self.tk.call(self._w, "reset")

	def tag(self, subcommand, tag_name, *arguments):
		return self.tk.call(self._w, "tag", subcommand, tag_name, *arguments)

	def text(self, *args):
		return self.tk.call(self._w, "text", *args)

	def xview(self, *args):
		"Used to control horizontal scrolling."
		if args: return self.tk.call(self._w, "xview", *args)
		coords = map(float, self.tk.call(self._w, "xview").split())
		return tuple(coords)

	def xview_moveto(self, fraction):
		"""Adjusts horizontal position of the widget so that fraction
		of the horizontal span of the document is off-screen to the left.
		"""
		return self.xview("moveto", fraction)

	def xview_scroll(self, number, what):
		"""Shifts the view in the window according to number and what;
		number is an integer, and what is either 'units' or 'pages'.
		"""
		return self.xview("scroll", number, what)

	def yview(self, *args):
		"Used to control the vertical position of the document."
		if args: return self.tk.call(self._w, "yview", *args)
		#coords = map(float, self.tk.call(self._w, "yview").split())
		coords = map(float, self.tk.call(self._w, "yview"))
		return tuple(coords)

	# Сместить экран до заданного узла
	def yview_name(self, name):
		''' Пример использования:
			self.index = self.text('index',term_first_pos,term_last_pos)
			self.yview_name(self.index[0])
		'''
		return self.yview(name)

	def yview_moveto(self, fraction):
		"""Adjust the vertical position of the document so that fraction of
		the document is off-screen above the visible region.
		Example:
		self.yview('moveto',20.0)
		"""
		return self.yview("moveto", fraction)

	def yview_scroll(self, number, what):
		"""Shifts the view in the window up or down, according to number and
		what. 'number' is an integer, and 'what' is either 'units' or 'pages'.
		"""
		return self.yview("scroll", number, what)

	def bbox(self,*args): # nodeHandle
		return self.tk.call(self._w, "bbox", *args)
	
	def get_nearest_page_up(self):
		while self.page_no > 0:
			if self.page_no in self.top_indexes:
				break
			else:
				self.page_no -= 1
	
	# Сместить экран так, чтобы была видна текущая выделенная ячейка
	def shift_screen(self):
		init_inst('root').widget.update_idletasks()
		cur_widget_width = globs['geom_top']['width'] = self.winfo_width()
		cur_widget_height = globs['geom_top']['height'] = self.winfo_height()
		cur_widget_offset_x = self.winfo_rootx()
		cur_widget_offset_y = self.winfo_rooty()
		if cur_widget_width != self.widget_width or cur_widget_height != self.widget_height or cur_widget_offset_x != self.widget_offset_x or cur_widget_offset_y != self.widget_offset_y:
			self.widget_width = cur_widget_width
			self.widget_height = cur_widget_height
			self.widget_offset_x = cur_widget_offset_x
			self.widget_offset_y = cur_widget_offset_y
			log.append('TkinterHtmlMod.shift_screen',lev_debug,globs['mes'].geometry % (self.widget_width,self.widget_height,self.widget_offset_x,self.widget_offset_y))
			self.top_indexes = {}
			self.page_no = 0
			# todo: check this
			self.i, self.j = h_request._moves['_move_text_start']
		# Иначе экран будет смещаться до 1-й выделяемой ячейки, а не до верхнего края
		if self.page_no == 0 and not 0 in self.top_indexes:
			self.top_indexes[0] = self.text('index',0)[0]
		self.top_bbox = self.widget_height * self.page_no
		self.bottom_bbox = self.top_bbox + self.widget_height
		try:
			cur_top_bbox = self.bbox(self.index[0])[1]
			cur_bottom_bbox = self.bbox(self.index[0])[3]
		except tk.TclError:
			log.append('TkinterHtmlMod.shift_screen',lev_debug,globs['mes'].wrong_input2)
			cur_top_bbox = 0
			cur_bottom_bbox = 0
		if cur_top_bbox < self.top_bbox:
			if self.page_no > 0:
				self.page_no -= 1
			if len(self.top_indexes) > 0:
				self.get_nearest_page_up()
				self.yview_name(self.top_indexes[self.page_no])
			# todo: check this
			'''if self.page_no in self.top_indexes:
				self.yview_name(self.top_indexes[self.page_no])
			else:
				self.yview_scroll(cur_top_bbox-self.top_bbox,'units')
			'''
			log.append('TkinterHtmlMod.shift_screen',lev_info,globs['mes'].cur_page_no % self.page_no)
		elif cur_bottom_bbox > self.bottom_bbox:
			self.yview(self.index[0])
			self.page_no += 1
			log.append('TkinterHtmlMod.shift_screen',lev_info,globs['mes'].cur_page_no % self.page_no)
			self.top_indexes[self.page_no] = self.index[0]
		else:
			#log.append('TkinterHtmlMod.shift_screen',lev_info,globs['mes'].shift_screen_not_required)
			pass

	# Выделить ячейку
	def set_cell(self,View=True): # View=True будет всегда сдвигать экран до текущей ячейки при навигации с клавиатуры
		self.tag("delete", "selection")
		self.index = None
		# todo: Здесь иногда получаем ошибку с индексами
		if len(h_request._cells) > self.i and len(h_request._cells[self.i]) > self.j:
			if globs['bool']['SelectTermsOnly']:
				self.index = self.text('index',h_request._cells[self.i][self.j].first,h_request._cells[self.i][self.j].last_term)
			else:
				self.index = self.text('index',h_request._cells[self.i][self.j].first,h_request._cells[self.i][self.j].last)
		else:
			log.append('TkinterHtmlMod.set_cell',globs['mes'].wrong_input2)
		if self.index:
			#log.append('TkinterHtmlMod.set_cell',lev_debug,globs['mes'].cur_node % self.index[0])
			# В крайнем случае можно делать так:
			#self.tag("add", "selection",self._node,0,self._node,300)
			try:
				self.tag('add','selection',self.index[0],self.index[1],self.index[2],self.index[3])
			# При удалении или вставке ячеек может возникнуть ошибка, поскольку текущий узел изменился
			except tk.TclError:
				log.append('TkinterHtmlMod.set_cell',lev_warn,globs['mes'].tag_addition_failure % ('selection',self.index[0],self.index[3]))
			self.tag('configure','selection','-background',globs['var']['color_terms_sel_bg'])
			self.tag('configure','selection','-foreground',globs['var']['color_terms_sel_fg'])
			if View:
				self.shift_screen()

	# Изменить ячейку при движении мышью
	def mouse_sel(self,event=None):
		if event:
			self.event = event
			# Если ячейку определить не удалось, либо ее выделять нельзя (согласно настройкам), то возвращается предыдущая ячейка. Это позволяет всегда иметь активное выделение.
			try:
				self._node, self._offset = self.node(True,self.event.x,self.event.y)
				self.mouse_index = self.text("offset",self._node,self._offset)
			except ValueError:
				# Это сообщение появляется так часто, что не ставлю тут ничего.
				#log.append('TkinterHtmlMod.mouse_sel',lev_warn,globs['mes'].unknown_cell)
				pass
			if self.mouse_index > 0:
				self.get_cell(self.mouse_index)
				self.set_cell(View=False)

	# Скопировать термин текущей ячейки (или полное ее содержимое)
	def copy_cell(self,*args):
		#self.set_cell()
		if globs['bool']['CopyTermsOnly']:
			selected_text = h_request._cells[self.i][self.j].term
		else:
			selected_text = List([h_request._cells[self.i][self.j].dic,h_request._cells[self.i][self.j].term,h_request._cells[self.i][self.j].comment]).space_items()
		init_inst('clipboard').copy(selected_text)
		if globs['bool']['Iconify']:
			iconify(init_inst('top'))

	# Удалить ячейку и перекомпоновать статью
	def delete_cell(self,*args):
		Found = False
		# Предполагаем, что h_request._elems уже прошло стадию объединения комментариев
		for i in range(len(h_request._elems)):
			# todo: Уточнить и упростить алгоритм
			if h_request._elems[i] == h_request._cells[self.i][self.j]:
				Found = True
				break
		if Found:
			del h_request._elems[i]
			h_request.update()
			self.load_article()
		else:
			Message(func='TkinterHtmlMod.delete_cell',type=lev_warn,message=globs['mes'].wrong_input2,Silent=self.Silent)

	# Добавить пустую ячейку и перекомпоновать статью
	def add_cell(self,*args):
		Found = False
		# Предполагаем, что h_request._elems уже прошло стадию объединения комментариев
		for i in range(len(h_request._elems)):
			# todo: Уточнить и упростить алгоритм
			if h_request._elems[i] == h_request._cells[self.i][self.j]:
				Found = True
				break
		if Found:
			h_request._elems.insert(i,Cell())
			h_request.update()
			self.load_article()

	def load_article(self,*args):
		self.reset()
		self.parse(h_request.html())
		h_request._text = self.text('text')
		self.top_indexes = {}
		self.gen_poses()
		self.gen_pos2cell()
		Moves()
		self.move_text_start()
		init_inst('top').widget.title(h_request.search())
		self.history.update()
		self.update_buttons()
		self.search_article.reset()
	
	# Перейти по URL текущей ячейки
	def go_url(self,*args):
		#self.set_cell()
		if self.MouseClicked:
			pass
		else:
			log.append('TkinterHtmlMod.go_url',lev_debug,globs['mes'].cur_cell % (self.i,self.j))
			h_request._search = h_request._cells[self.i][self.j].term
			h_request._url = h_request._cells[self.i][self.j].url
			h_request.new()
			h_db.search_part()
			log.append('TkinterHtmlMod.go_url',lev_info,globs['mes'].opening_link % h_request._url)
			self.load_article()
				
	def gen_pos2cell(self):
		# 1-й символ всегда соответствует 1-й ячейке
		self.pos2cell = [[0,0]]
		cur_index = 1 # Starts with '\n'
		for i in range(len(h_request._cells)):
			# Число столбцов в таблице должно быть одинаковым!
			for j in range(len(h_request._cells[i])):
				if h_request._cells[i][j].speech:
					tmp_str = h_request._cells[i][j].speech.strip() + '\n'
					h_request._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					h_request._cells[i][j].last_term = h_request._cells[i][j].first + len(h_request._cells[i][j].term)
					h_request._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
				if h_request._cells[i][j].dic:
					tmp_str = h_request._cells[i][j].dic.strip() + '\n'
					h_request._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					h_request._cells[i][j].last_term = h_request._cells[i][j].first + len(h_request._cells[i][j].term)
					h_request._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
				if h_request._cells[i][j].term + h_request._cells[i][j].comment:
					tmp_str = (h_request._cells[i][j].term + h_request._cells[i][j].comment).strip() + '\n'
					tmp_str = tmp_str.replace('  ',' ')
					h_request._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					h_request._cells[i][j].last_term = h_request._cells[i][j].first + len(h_request._cells[i][j].term)
					h_request._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
	#assert len(h_request._text) == len(self.pos2cell)
				
	def gen_poses(self):
		cur_index = 1 # Starts with '\n'
		for i in range(len(h_request._cells)):
			for j in range(len(h_request._cells[i])):
				tmp_str = List([h_request._cells[i][j].speech,h_request._cells[i][j].dic,h_request._cells[i][j].term,h_request._cells[i][j].comment]).space_items()
				h_request._cells[i][j].first = cur_index
				h_request._cells[i][j].last_term = cur_index + len(h_request._cells[i][j].term)
				h_request._cells[i][j].last = cur_index + len(tmp_str)
				cur_index += len(tmp_str)
				cur_index += 1
	
	def reload(self,*args):
		h_request._html = h_request._text = h_request._cells = h_request._elems = None
		self.load_article()
		
	# Вставить спец. символ в строку поиска
	def insert_sym(self,sym):
		self.search_field.widget.insert('end',sym)
		if globs['bool']['AutoCloseSpecSymbol']:
			self.spec_symbols.close()
			
	def toggle_view(self,*args):
		if h_request.view() == 0:
			h_request._view = 1
		elif h_request._view == 1:
			#h_request._view = 2
			h_request._view = 0
		elif h_request._view == 2:
			h_request._view = 0
		log.append('TkinterHtmlMod.toggle_view',lev_info,globs['mes'].new_view_mode % h_request._view)
		# todo: why move_right and move_left are so slow to be calculated?
		# todo: do not recreate 'cells' each time
		h_request.update()
		h_db.search_part()
		log.append('TkinterHtmlMod.go_url',lev_info,globs['mes'].opening_link % h_request._url)
		self.load_article()
	
	def zzz(self): # Only needed to move quickly to the end of the class
		pass



if  __name__ == '__main__':
	h_request = Request()
	h_db = DB()
	h_quit = Quit()
	h_table = TkinterHtmlMod(init_inst('top').widget)
	init_inst('top').widget.protocol("WM_DELETE_WINDOW",h_quit.wait)
	timed_update() # Do not wrap this function. Change this carefully.
	h_db.search_part()
	h_table.load_article()
	h_table.show()
	init_inst('top').show()
	init_inst('root').run()
