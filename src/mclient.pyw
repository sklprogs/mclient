#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' # todo
	- Make transcriptions Selectable
'''

import tkinterhtml as th
import os
import sys
import tkinter     as tk
#from tkinter import ttk # todo (?): del
import shared      as sh
import sharedGUI   as sg
import page        as pg
import tags        as tg
import elems       as el
import cells       as cl
import db
import mkhtml      as mh


product = 'MClient'
version = '5.1'

third_parties = '''
tkinterhtml
https://bitbucket.org/aivarannamaa/tkinterhtml
License: MIT
Copyright (c) <year> aivarannamaa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''



class ConfigMclient(sh.Config):
	
	def __init__(self):
		super().__init__()
		self.sections         = [sh.SectionBooleans,sh.SectionIntegers,sh.SectionVariables]
		self.sections_abbr    = [sh.SectionBooleans_abbr,sh.SectionIntegers_abbr,sh.SectionVariables_abbr]
		self.sections_func    = [sh.config_parser.getboolean,sh.config_parser.getint,sh.config_parser.get]
		self.message          = sh.globs['mes'].missing_config + '\n'
		self.total_keys       = 0
		self.changed_keys     = 0
		self.missing_keys     = 0
		self.missing_sections = 0
		# Create these keys before reading the config
		self.path    = sh.objs.pdir().add('mclient.cfg')
		self.reset()
		h_read       = sh.ReadTextFile(self.path,Silent=self.Silent)
		self.text    = h_read.get()
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
		sh.globs['bool'].update({
			'AutoCloseSpecSymbol':False,
			'CopyTermsOnly':True,
			'Iconify':True
			             })
		#---------------------------------------------------
		sh.globs['int'].update({
			'font_comments_size':3,
			'font_dics_size':4,
			'font_speech_size':4,
			'font_terms_size':4
			              })
		#---------------------------------------------------
		sh.globs['var'].update({
			'bind_add_cell':'<Control-Insert>',
			'bind_clear_history':'<Control-Shift-Delete>',
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
			'bind_toggle_alphabet':'<Alt-a>',
			'bind_toggle_block':'<Alt-b>',
			'bind_toggle_history_alt':'<Control-h>',
			'bind_toggle_history':'<F4>',
			'bind_toggle_priority':'<Alt-p>',
			'bind_toggle_view':'<F6>',
			'bind_toggle_view_alt':'<Alt-v>',
			'color_comments':'gray',
			'color_dics':'cadet blue',
			'color_speech':'red',
			'color_terms_sel_bg':'cyan',
			'color_terms_sel_fg':'black',
			'color_terms':'black',
			'font_comments_family':'Mono',
			'font_dics_family':'Arial',
			'font_history':'Sans 12',
			'font_speech_family':'Arial',
			'font_style':'Sans 14',
			'font_terms_sel':'Sans 14 bold italic',
			'font_terms_family':'Serif',
			'pair_afr_rus':'l1=31&l2=2&s=%s',
			'pair_deu_rus':'l1=3&l2=2&s=%s',
			'pair_eng_deu':'l1=1&l2=3&s=%s',
			'pair_eng_est':'l1=1&l2=26&s=%s',
			'pair_eng_rus':'CL=1&s=%s',
			'pair_epo_rus':'l1=34&l2=2&s=%s',
			'pair_est_rus':'l1=26&l2=2&s=%s',
			'pair_fra_rus':'l1=4&l2=2&s=%s',
			'pair_ita_rus':'l1=23&l2=2&s=%s',
			'pair_lav_rus':'l1=27&l2=2&s=%s',
			'pair_nld_rus':'l1=24&l2=2&s=%s',
			'pair_root':'http://www.multitran.ru/c/M.exe?',
			'pair_rus_xal':'l1=2&l2=35&s=%s',
			'pair_spa_rus':'l1=5&l2=2&s=%s',
			'pair_xal_rus':'l1=35&l2=2&s=%s',
			'repeat_sign':'!',
			'repeat_sign2':'!!',
			'spec_syms':'àáâäāæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ',
			'ui_lang':'ru',
			'web_search_url':'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s',
			'win_encoding':'windows-1251'
				           })
	
	def reset(self):
		sh.globs['bool']  = {}
		sh.globs['float'] = {}
		sh.globs['int']   = {}
		sh.globs['var']   = {}
		
	def additional_keys(self):
		sh.globs['var'].update({
			'icon_alphabet_off':'icon_36x36_alphabet_off.gif',
			'icon_alphabet_on':'icon_36x36_alphabet_on.gif',
			'icon_block_off':'icon_36x36_block_off.gif',
			'icon_block_on':'icon_36x36_block_on.gif',
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
			'icon_priority_off':'icon_36x36_priority_off.gif',
			'icon_priority_on':'icon_36x36_priority_on.gif',
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
			'icon_watch_clipboard_on':'icon_36x36_watch_clipboard_on.gif'
			})
		for key in sh.globs['var']:
			if sh.globs['var'][key].endswith('.gif'):
				old_val = sh.globs['var'][key]
				sh.globs['var'][key] = sh.objs.pdir().add('resources',sh.globs['var'][key])
				sh.log.append('ConfigMclient.additional_keys',sh.lev_debug,'%s -> %s' % (old_val,sh.globs['var'][key]))



ConfigMclient()
sh.h_lang.set()

if __name__ == '__main__':
	if sh.oss.win():
		import kl_mod_win as kl_mod
		import pythoncom
	else:
		import kl_mod_lin as kl_mod

sh.globs['_tkhtml_loaded'] = False
sh.globs['geom_top'] = {}
sh.globs['top'] = {}

online_url_safe = sh.globs['var']['pair_root'] + 'l1=2&l2=1&s=%ED%E5%E2%E5%F0%ED%E0%FF+%F1%F1%FB%EB%EA%E0' # 'неверная ссылка'
sep_words_found = 'найдены отдельные слова'

pairs = ('ENG <=> RUS','DEU <=> RUS','SPA <=> RUS','FRA <=> RUS','NLD <=> RUS','ITA <=> RUS','LAV <=> RUS','EST <=> RUS','AFR <=> RUS','EPO <=> RUS','RUS <=> XAL','XAL <=> RUS','ENG <=> DEU','ENG <=> EST')
online_dic_urls = ( sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_rus'],	# ENG <=> RUS, 'CL=1&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_deu_rus'],	# DEU <=> RUS, 'l1=3&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_spa_rus'],	# SPA <=> RUS, 'l1=5&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_fra_rus'],	# FRA <=> RUS, 'l1=4&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_nld_rus'],	# NLD <=> RUS, 'l1=24&l2=2&s=%s',
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_ita_rus'],	# ITA <=> RUS, 'l1=23&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_lav_rus'],	# LAV <=> RUS, 'l1=27&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_est_rus'],	# EST <=> RUS, 'l1=26&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_afr_rus'],	# AFR <=> RUS, 'l1=31&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_epo_rus'],	# EPO <=> RUS, 'l1=34&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_rus_xal'],	# RUS <=> XAL, 'l1=2&l2=35&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_xal_rus'],	# XAL <=> RUS, 'l1=35&l2=2&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_deu'],	# ENG <=> DEU, 'l1=1&l2=3&s=%s'
					sh.globs['var']['pair_root'] + sh.globs['var']['pair_eng_est']	# ENG <=> EST, 'l1=1&l2=26&s=%s'
				  )
				  
langs           = ( 'English'                                                     , # ENG <=> RUS
					'German'                                                      , # DEU <=> RUS
					'Spanish'                                                     , # SPA <=> RUS
					'French'                                                      , # FRA <=> RUS
					'Dutch'                                                       , # NLD <=> RUS
					'Italian'                                                     ,	# ITA <=> RUS
					'Latvian'                                                     , # LAV <=> RUS
					'Estonian'                                                    ,	# EST <=> RUS
					'Afrikaans'                                                   ,	# AFR <=> RUS
					'Esperanto'                                                   ,	# EPO <=> RUS
					'Kazakh'                                                      ,	# RUS <=> XAL
					'Kazakh'                                                      ,	# XAL <=> RUS
					'German'                                                      ,	# ENG <=> DEU
					'Estonian'                                                  	# ENG <=> EST
				  )

sources = ('All','Online','Offline')



class Objects: # Requires 'article'
	
	def __init__(self):
		self._top = self._entry = self._textbox = self._online_mt = self._online_other = self._about = self._blacklist = self._prioritize = self._parties = self._request = self._ext_dics = self._webframe = self._blocks_db = None
		
	def blocks_db(self):
		if not self._blocks_db:
			self._blocks_db = db.DB()
		return self._blocks_db
	
	def webframe(self):
		if not self._webframe:
			self._webframe = WebFrame()
		return self._webframe
	
	def ext_dics(self):
		if not self._ext_dics:
			self._ext_dics = pg.ExtDics(path=sh.objs.pdir().add('dics'))
		return self._ext_dics
	
	def request(self):
		if not self._request:
			self._request = CurRequest()
		return self._request
	
	def parties(self):
		if not self._parties:
			top = sg.objs.new_top(Maximize=0)
			sg.Geometry(parent_obj=top).set('800x600')
			self._parties = sg.TextBox(parent_obj=top)
			self._parties.icon(sh.globs['var']['icon_mclient'])
			self._parties.title(text=sh.globs['mes'].btn_third_parties+':')
			self._parties.insert(text=third_parties,MoveTop=1)
			self._parties.read_only()
		return self._parties
	
	def top(self):
		if not self._top:
			self._top = sg.Top(sg.objs.root())
			self._top.icon(sh.globs['var']['icon_mclient'])
			sg.Geometry(parent_obj=self._top,title=articles.current().search()).maximize()
		return self._top
			
	def entry(self):
		if not self._entry:
			self._entry = sg.Entry(parent_obj=sg.Top(sg.objs.root()))
			self._entry.icon(sh.globs['var']['icon_mclient'])
			self._entry.title(sh.globs['mes'].search_str)
		return self._entry
		
	def textbox(self):
		if not self._textbox:
			h_top = sg.Top(sg.objs.root())
			self._textbox = sg.TextBox(parent_obj=h_top)
			sg.Geometry(parent_obj=h_top).set('500x400')
			self._textbox.icon(sh.globs['var']['icon_mclient'])
		return self._textbox
		
	def online_mt(self):
		if not self._online_mt:
			self._online_mt = sh.Online(MTSpecific=True)
		return self._online_mt
		
	def online_other(self):
		if not self._online_other:
			self._online_other = sh.Online(MTSpecific=False)
		return self._online_other
		
	def online(self):
		if articles.current().source() == 'Multitran':
			return self.online_mt()
		else:
			return self.online_other()
			
	def about(self):
		if not self._about:
			self._about = About()
		return self._about
		
	def blacklist(self):
		if self._blacklist is None: # Allow empty lists
			self._blacklist = Lists().blacklist()
		return self._blacklist
		
	def prioritize(self):
		if self._prioritize is None: # Allow empty lists
			self._prioritize = Lists().prioritize()
		return self._prioritize



class CurRequest:
	
	def __init__(self):
		self.reset()
		
	def reset(self):
		self._view       = 0
		#self._collimit   = 8
		self._collimit   = 7
		self._source     = 'All'
		#self._source    = 'Offline'
		#self._source    = 'Online'
		#self._search    = 'Добро пожаловать!'
		#self._search    = 'filter'
		#self._search    = 'counterpart'
		#self._search     = 'compensate'
		#self._search    = 'computer'
		#self._search     = 'martyr'
		#self._search      = 'balance'
		#self._search      = 'do'
		#self._search     = 'слово'
		#self._search      = 'башмак'
		self._search     = 'preceding'
		#self._search      = 'дерево' # DE
		self._lang       = 'English'
		#self._url       = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC%21'
		#self._url       = sh.globs['var']['pair_root'] + 'CL=1&s=filter&l1=1'
		#self._url        = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=martyr'
		#self._url        = sh.globs['var']['pair_root'] + 'CL=1&s=counterpart&l1=1'
		#self._url        = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=compensate'
		#self._url         = sh.globs['var']['pair_root'] + 't=3502039_1_2&s1=%F3%F0%E0%E2%ED%EE%E2%E5%F1%E8%F2%FC'
		#self._url          = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=do'
		#self._url          = sh.globs['var']['pair_root'] + 'l1=4&l2=2&s=%F1%EB%EE%E2%EE'
		#self._url         = sh.globs['var']['pair_root'] + 'l1=3&l2=2&s=%F1%EB%EE%E2%EE'
		#self._url          = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=%E1%E0%F8%EC%E0%EA'
		self._url           = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=preceding&l1=1&l2=2&s=preceding'
		# 'дерево', DE
		#self._url           = sh.globs['var']['pair_root'] + 'l1=3&l2=2&s=%E4%E5%F0%E5%E2%EE'
		self._article_id = self._search + ' (' + self._url + ')'
		# Toggling blacklisting should not depend on a number of blocked dictionaries (otherwise, it is not clear how blacklisting should be toggled)
		self.Block       = True
		self.Prioritize  = True
		self.SortTerms   = True
		# *Temporary* turn off prioritizing and terms sorting for articles with 'sep_words_found' and in phrases; use previous settings for new articles
		self.SpecialPage = False
		self._page       = ''
		self._html       = ''
		self._html_raw   = ''



class Article:
	
	def __init__(self):
		self.reset()
		
	def reset(self):
		self._source = self._search = self._url = self._cells = self._elems = self._html = self._html_raw = self._text = self._moves = self._page = self._tags = self._block = self._prioritize = None
	
	def update(self):
		self._cells = self._html = self._text = self._moves = None
	
	# todo: drop in favor of 'reset'
	def new(self): # A completely new request
		self._cells = self._elems = self._html_raw = self._html = self._text = self._moves = self._block = self._prioritize = None
	
	def source(self):
		if self._source is None:
			self._source = objs.request()._source
		return self._source
		
	def search(self):
		if self._search is None:
			self._search = 'Добро пожаловать!'
		return self._search
		
	def url(self):
		if self._url is None:
			self._url = sh.globs['var']['pair_root'] + 'l1=1&l2=2&s=%C4%EE%E1%F0%EE%20%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC%21'
		return self._url
		
	def cells(self):
		if self._cells is None:
			self._cells = Cells(elems=self.elems())._cells
		return self._cells
		
	def tags(self):
		if self._tags is None:
			_tags = tg.Tags(text=self.text())
			_tags.tags()
			self._tags = _tags.blocks()
		return self._tags
	
	def elems(self):
		if self._elems is None:
			# todo: check when text=None
			self._elems = Elems(lst=self.tags()).elems()
		return self._elems
		
	def html(self):
		if self._html is None:
			self._html = HTML(cells=self.cells())._html
		return self._html
		
	def page(self):
		if self._page is None:
			self._page = pg.Page(source=self.source(),lang=objs.request()._lang,search=self.search(),url=self.url(),win_encoding=sh.globs['var']['win_encoding'],ext_dics=objs.ext_dics())
			self._page.run()
		return self._page
	
	def html_raw(self):
		if self._html_raw is None:
			self._html_raw = self.page()._html_raw
		return self._html_raw
		
	def text(self):
		if self._text is None:
			self._text = self.page()._page
		return self._text
		
	# todo: fix: _moves is always not None
	def moves(self):
		if self._moves is None:
			self._moves = Moves(cells=self.cells())._moves
		return self._moves
		
	def block(self):
		if self._block is None: # Allow an empty list
			self.elems()
		return self._block
		
	def prioritize(self):
		if self._prioritize is None: # Allow an empty list
			self.elems() # fix: rework output
		return self._prioritize



class Articles: # Requires 'request'
	
	def __init__(self):
		self.reset()
		
	def reset(self):
		self._articles = []
		self._no = 0
		if not self._articles:
			self.add()
			
	def len(self):
		return len(self._articles)
	
	def add(self):
		self._articles.append(Article())
		self._no = self.len() - 1
		
	def current(self):
		return self._articles[self._no]
		
	def search_article(self):
		Found = False
		for i in range(self.len()):
			if self._articles[i]._source == objs.request()._source and self._articles[i]._url == objs._request._url:
				self._no = i
				Found = True
				articles.current().update()
				break
		if not Found:
			self.add()
			self.current()._source = objs.request()._source
			self.current()._url    = objs._request._url
			self.current()._search = objs._request._search
			
	def index_add(self):
		if self._no < self.len() - 1:
			self._no += 1
		else:
			self._no = 0
			
	def index_subtract(self):
		if self._no > 0:
			self._no -= 1
		else:
			self._no = self.len() - 1
			
	def searches(self):
		return [str(x._search) for x in self._articles]
		
	def prev(self):
		if self._no > 0:
			return self._articles[self._no-1].search()
			
	def debug(self): # orphan
		old = self._no
		message = ''
		for i in range(self.len()):
			self._no = i
			message += '#%d:\n'         % i
			message += 'Source: "%s"\n' % str(self.current()._source)
			message += 'Search: "%s"\n' % str(self.current()._search)
			message += 'URL: "%s"\n'    % str(self.current()._url)
			message += '\n\n'
		self._no = old
		sg.Message(func='Articles.debug',level=sh.lev_info,message=message)



def call_app():
	# Использовать то же сочетание клавиш для вызова окна
	sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).activate(MouseClicked=h_table.MouseClicked)
	# In case of .focus_set() *first* Control-c-c can call an inactive widget
	h_table.search_field.widget.focus_force()

# Перехватить нажатие Control-c-c
def timed_update():
	h_table.MouseClicked = False
	check = kl_mod.keylistener.check()
	if check:
		if check == 1 and h_table.CaptureHotkey:
			# Позволяет предотвратить зависание потока в версиях Windows старше XP
			if sh.oss.win():
				kl_mod.keylistener.cancel()
				kl_mod.keylistener.restart()
			h_table.MouseClicked = True
			new_clipboard = sg.Clipboard().paste()
			if new_clipboard:
				h_table.search = new_clipboard
				h_table.search_sources()
		if check == 2 or h_table.CaptureHotkey:
			call_app()
	# We need to have .after in the same function for it to work
	h_quit._id = sg.objs.root().widget.after(300,timed_update)
	h_quit.now()



class Quit:
	
	def __init__(self):
		self.Quit = False
		self._id  = None # This must be changed externally
	
	def wait(self,*args):
		self.Quit = True
		objs.top().close()
		
	def now(self,*args):
		if self.Quit:
			sh.log.append('Quit.now',sh.lev_info,sh.globs['mes'].goodbye)
			kl_mod.keylistener.cancel()
			objs.top().widget.destroy()
			sg.objs.root().widget.after_cancel(self._id)
			sg.objs.root().destroy()
			sys.exit()



class About:
	
	def __init__(self):
		self.Active = False
		self.type   = 'About'
		self.obj    = sg.Top(sg.objs.root())
		self.widget = self.obj.widget
		self.obj.icon (sh.globs['var']['icon_mclient'])
		self.obj.title(sh.globs['mes'].about)
		frame1 = sg.Frame (
		            parent_obj          = self                                ,
		            expand              = 1                                   ,
		            fill                = 'both'                              ,
		            side                = 'top'
		                  )
		frame2 = sg.Frame (
		            parent_obj          = self                                ,
		            expand              = 1                                   ,
		            fill                = 'both'                              ,
		            side                = 'left'
		                  )
		frame3 = sg.Frame (
		            parent_obj          = self                                ,
		            expand              = 1                                   ,
		            fill                = 'both'                              ,
		            side                = 'right'
		                  )
		label  = sg.Label (
		            parent_obj          = frame1                              ,
		            text                = sh.globs['mes'].about_text % version,
		            font                = sh.globs['var']['font_style']
		                  )
		# Лицензия
		sg.Button (
		            parent_obj          = frame2                              ,
		            text                = sh.globs['mes'].btn_third_parties   ,
		            hint                = sh.globs['mes'].hint_license        ,
		            action              = self.show_third_parties             ,
		            side                = 'left'
		          )
		sg.Button (
		            parent_obj          = frame3                              ,
		            text                = sh.globs['mes'].btn_license         ,
		            hint                = sh.globs['mes'].hint_license        ,
		            action              = self.open_license_url               ,
		            side                = 'left'
		          )
		# Отправить письмо автору
		sg.Button (
		            parent_obj          = frame3                              ,
		            text                = sh.globs['mes'].btn_email_author    ,
		            hint                = sh.globs['mes'].hint_email_author   ,
		            action              = self.response_back                  ,
		            side                = 'right'
		          )
		self.widget.focus_set()
		sg.bind (
		            obj                 = self.obj                            ,
		            bindings            = sh.globs['var']['bind_show_about']  ,
		            action              = self.toggle
		        )
		sg.bind (
		            obj                 = self.obj                            ,
		            bindings            = '<Escape>'                          ,
		            action              = self.close
		        )
		self.close()
	
	def close(self,*args):
		self.obj.close()
		self.Active = False
		
	def show(self,*args):
		self.obj.show()
		self.Active = True
	
	def toggle(self,*args):
		if self.Active:
			self.close()
		else:
			self.show()
	
	# Написать письмо автору
	def response_back(self,*args):
		sh.Email (
		            email               = sh.email                            ,
		            subject             = sh.globs['mes'].program_subject % product
		         ).create()

	# Открыть веб-страницу с лицензией
	def open_license_url(self,*args):
		objs.online()._url = sh.globs['license_url']
		objs.online().browse()

	# Отобразить информацию о лицензии третьих сторон
	def show_third_parties(self,*args):
		objs.parties().show()


		
class SaveArticle:
	
	def __init__(self):
		self.type       = 'SaveArticle'
		self.parent_obj = sg.Top(sg.objs.root())
		self.obj        = sg.ListBox (
		            parent_obj          = self.parent_obj                     ,
		            Multiple            = False                               ,
		            lst                 = [sh.globs['mes'].save_view_as_html  ,
		                                  sh.globs['mes'].save_article_as_html,
		                                  sh.globs['mes'].save_article_as_txt ,
		                                  sh.globs['mes'].copy_article_html   ,
		                                  sh.globs['mes'].copy_article_txt]   ,
		            title               = sh.globs['mes'].select_action       ,
		            icon                = sh.globs['var']['icon_mclient']
		                             )
		self.widget = self.obj.widget
		# Use this instead of 'close' because there is no selection yet
		self.obj.interrupt()
		self.file = ''
		
	def close(self,*args):
		self.obj.close()
		
	def show(self,*args):
		self.obj.show()
		
	# Fix an extension for Windows
	def fix_ext(self,ext='.htm'):
		if not self.file.endswith(ext):
			self.file += ext
			
	def select(self,*args):
		self.show()
		opt = self.obj._get
		if opt:
			if opt == sh.globs['mes'].save_view_as_html:
				self.view_as_html()
			elif opt == sh.globs['mes'].save_article_as_html:
				self.raw_as_html()
			elif opt == sh.globs['mes'].save_article_as_txt:
				self.view_as_txt()
			elif opt == sh.globs['mes'].copy_article_html:
				self.copy_raw()
			elif opt == sh.globs['mes'].copy_article_txt:
				self.copy_view()
	
	def view_as_html(self):
		self.file = sg.dialog_save_file (
		            filetypes           = ((sh.globs['mes'].webpage,'.htm')   ,
		                                   (sh.globs['mes'].webpage,'.html')  ,
		                                   (sh.globs['mes'].all_files,'*')
		                                  )
		                                )
		if self.file:
			self.fix_ext(ext='.htm')
			# We disable AskRewrite because the confirmation is already built in the internal dialog
			sh.WriteTextFile(self.file,AskRewrite=False).write(articles.current().html())
			
	def raw_as_html(self):
		# Ключ 'html' может быть необходим для записи файла, которая производится в кодировке UTF-8, поэтому, чтобы полученная веб-страница нормально читалась, меняем кодировку вручную.
		# Также меняем сокращенные гиперссылки на полные, чтобы они работали и в локальном файле.
		self.file = sg.dialog_save_file (
		            filetypes           = ((sh.globs['mes'].webpage,'.htm')   ,
		                                   (sh.globs['mes'].webpage,'.html')  ,
		                                   (sh.globs['mes'].all_files,'*')
		                                  )
		                                )
		if self.file:
			self.fix_ext(ext='.htm')
			# todo: fix remaining links to localhost
			sh.WriteTextFile(self.file,AskRewrite=False).write(articles.current().html_raw().replace('charset=windows-1251"','charset=utf-8"').replace('<a href="M.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/M.exe?',sh.globs['var']['pair_root']).replace('<a href="m.exe?','<a href="'+sh.globs['var']['pair_root']).replace('../c/m.exe?',sh.globs['var']['pair_root']))
		
	def view_as_txt(self):
		self.file = sg.dialog_save_file (
		            filetypes           = ((sh.globs['mes'].plain_text,'.txt'),
		                                   (sh.globs['mes'].all_files,'*')
		                                  )
		                                )
		if self.file:
			self.fix_ext(ext='.txt')
			sh.WriteTextFile(self.file,AskRewrite=False).write(articles.current()._text)
			
	def copy_raw(self):
		sg.Clipboard().copy(articles.current().html_raw())
			
	def copy_view(self):
		sg.Clipboard().copy(articles.current()._text)

	

# Search IN an article
class SearchArticle:
	
	def __init__(self):
		self.type   = 'SearchArticle'
		self.obj    = objs.entry()
		self.obj.title(sh.globs['mes'].search_word)
		self.widget = self.obj.widget
		sg.bind (
		            obj                 = self.obj                            ,
		            bindings            = sh.globs['var']['bind_search_article_forward'],
		            action              = self.close
		        )
		sg.bind (
		            obj                 = self.obj                            ,
		            bindings            = '<Escape>'                          ,
		            action              = self.close
		        )
		self.obj.select_all()
		self.obj.focus()
		self.close()
		self.reset()
	
	def reset(self):
		self._list   = []
		self._pos    = -1
		self._search = ''
		# Plus: keeping old input
		# Minus: searching old input after cancelling the search and searching again
		#self.clear()
	
	def clear(self,*args):
		self.obj.clear_text()
	
	def close(self,*args):
		self.obj.close()
		
	def show(self,*args):
		self.obj.show()
		self.obj.select_all()
	
	# Create a list of all matches in the article
	def matches(self):
		if self.search():
			for i in range(len(articles.current().cells())):
				for j in range(len(articles.current()._cells[i])):
					# todo: Для всех вхождений, а не только терминов
					if articles.current()._cells[i][j].Selectable and self._search in articles.current()._cells[i][j].term.lower():
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
			sg.Message (
			        func                = 'SearchArticle.forward'             ,
			        level               = sh.lev_info                         ,
			        message             = sh.globs['mes'].search_from_start
			           )
			self._pos = 0
	
	def backward(self):
		if self._pos > 0:
			self._pos -= 1
		else:
			sg.Message (
			        func                = 'SearchArticle.backward'            ,
			        level               = sh.lev_info                         ,
			        message             = sh.globs['mes'].search_from_end
			           )
			self._pos = len(self.list()) - 1

	
	
# Search FOR an article
class SearchField:
	
	def __init__(self,parent_obj,side='left',ipady=5):
		self.type       = 'SearchField'
		self.parent_obj = parent_obj
		# Поле ввода поисковой строки
		self.widget     = tk.Entry(self.parent_obj.widget)
		# Подгоняем высоту поисковой строки под высоту графических кнопок; значение 5 подобрано опытным путем
		self.widget.pack(side=side,ipady=ipady)
		
	def clear(self,*args):
		self.widget.delete(0,'end')
		self.widget.selection_clear()
		
	# Очистить строку поиска и вставить в нее заданный текст или содержимое буфера обмена
	def paste(self,event=None,text=None):
		self.clear()
		if text:
			self.widget.insert(0,text)
		else:
			self.widget.insert(0,sg.Clipboard().paste())
		return 'break'
		
	# Вставить текущий запрос	
	def insert_repeat_sign(self,*args):
		if articles.len() > 0:
			sg.Clipboard().copy(str(articles.current().search()))
			self.paste()

	# Вставить предыдущий запрос
	def insert_repeat_sign2(self,*args):
		if articles.len() > 1:
			sg.Clipboard().copy(str(articles.prev()))
			self.paste()



class SpecSymbols:
	
	def __init__(self):
		self.obj    = sg.Top(sg.objs.root())
		self.widget = self.obj.widget
		self.obj.icon (sh.globs['var']['icon_mclient'])
		self.obj.title(sh.globs['mes'].paste_spec_symbol)
		self.frame  = sg.Frame(self.obj,expand=1)
		for i in range(len(sh.globs['var']['spec_syms'])):
			if i % 10 == 0:
				self.frame = sg.Frame(self.obj,expand=1)
			# lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
			# width и height нужны для Windows
			self.button = tk.Button(self.frame.widget,text=sh.globs['var']['spec_syms'][i],command=lambda i=i:h_table.insert_sym(sh.globs['var']['spec_syms'][i]),width=2,height=2).pack(side='left',expand=1)
		self.bindings()
		self.close()
		
	def bindings(self):
		sg.bind (
		            obj                 = self.obj                            ,
		            bindings            = ['<Escape>',sh.globs['var']['bind_spec_symbol']],
		            action              = self.close
		        )
	
	def show(self,*args):
		self.obj.show()
		
	def close(self,*args):
		self.obj.close()



class History:
	
	def __init__(self):
		self._title = sh.globs['mes'].btn_history
		self._icon  = sh.globs['var']['icon_mclient']
		self.Active = False
		self.gui()
		
	def gui(self):
		self.parent_obj = sg.Top(sg.objs.root())
		self.parent_obj.widget.geometry('250x350')
		self.obj = sg.ListBox (
		            parent_obj          = self.parent_obj                     ,
		            title               = self._title                         ,
		            icon                = self._icon                          ,
		            SelectionCloses     = False                               ,
		            SingleClick         = False                               ,
		            Composite           = True                                ,
		            user_function       = self.go
		                      )
		self.widget = self.obj.widget
		self.bindings()
		self.close()
		
	def bindings(self):
		sg.bind (
		            obj                 = self.parent_obj                     ,
		            bindings            = [sh.globs['var']['bind_toggle_history'],
		                                   sh.globs['var']['bind_toggle_history_alt'],
		                                   '<Escape>'
		                                  ]                                   ,
		            action              = self.toggle
		        )
		sg.bind(obj=self.parent_obj,bindings='<ButtonRelease-3>',action=self.clear)
	
	def autoselect(self):
		self.obj._index = articles._no
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
		self.obj.reset(lst=articles.searches(),title=self._title)
	
	def update(self):
		self.fill()
		self.autoselect()
		
	def clear(self,*args):
		self.obj.clear()
		h_table.search_article.obj.clear_text()
		articles.reset()
		articles.search_article()
		h_table.load_article()
		self.update()
	
	def toggle(self,*args):
		if self.Active:
			self.close()
		else:
			self.show()
			
	def go(self,*args):
		articles._no = self.obj.index()
		h_table.load_article()
		
	# Скопировать элемент истории
	def copy(self,*args):
		sg.Clipboard().copy(articles.current().search())



class WebFrame:
	
	def __init__(self):
		self.values()
		self.gui()
	
	def values(self):
		self.event       = None
		self._node       = None
		self.index       = None
		self._offset     = None
		self.mouse_index = -1 # self.mouse_index (int) != self.index (tuple)
	
	def gui(self):
		self.obj    = sg.objs.new_top(Maximize=1)
		self.widget = th.TkinterHtml(self.obj.widget)
		self.widget.pack(expand='1',fill='both')
		self.bindings()
		self.title()
		
	def title(self,arg=None):
		if not arg:
			arg = sh.List(lst1=[product,version]).space_items()
		self.obj.title(arg)
		
	def text(self,event=None):
		return self.widget.text('text')
		
	def bindings(self):
		self.widget.bind("<Motion>",self.mouse_sel,True)
		
	# Изменить ячейку при движении мышью
	def mouse_sel(self,event=None):
		if event:
			self.event = event
			# Если ячейку определить не удалось, либо ее выделять нельзя (согласно настройкам), то возвращается предыдущая ячейка. Это позволяет всегда иметь активное выделение.
			try:
				self._node, self._offset = self.widget.node(True,self.event.x,self.event.y)
				self.mouse_index         = self.widget.text("offset",self._node,self._offset)
			except ValueError:
				# Это сообщение появляется так часто, что не ставлю тут ничего.
				#sh.log.append('WebFrame.mouse_sel',sh.lev_warn,sh.globs['mes'].unknown_cell)
				pass
			if self.mouse_index > 0:
				#self.get_cell(self.mouse_index)
				#self.set_cell(View=False)
				#print(self.mouse_index)
				self.set_cell(pos=self.mouse_index)
				# cur
	
	# Выделить ячейку
	def set_cell(self,pos,View=True): # View=True будет всегда сдвигать экран до текущей ячейки при навигации с клавиатуры
		print() # todo: del
		print('mouse_index:',self.mouse_index) # todo: del
		self.widget.tag("delete", "selection")
		result = objs.blocks_db().get_cell(pos=pos)
		if result:
			pos1, pos2 = result
		else:
			pos1, pos2 = 0, 0
		#print('pos1:',pos1) # todo: del # cur
		#print('pos2:',pos2) # todo: del
		self.index = self.widget.text('index',pos1,pos2)
		print('index:',self.index) # todo: del
		print('index[0]:',self.index[0]) # todo: del
		print('index[1]:',self.index[1]) # todo: del
		print('index[2]:',self.index[2]) # todo: del
		print('index[3]:',self.index[3]) # todo: del
		if self.index:
			try:
				self.widget.tag('add','selection',self.index[0],self.index[1],self.index[2],self.index[3])
			# При удалении или вставке ячеек может возникнуть ошибка, поскольку текущий узел изменился
			except tk.TclError:
				sh.log.append('WebFrame.set_cell',sh.lev_warn,sh.globs['mes'].tag_addition_failure % ('selection',self.index[0],self.index[3]))
			self.widget.tag('configure','selection','-background',sh.globs['var']['color_terms_sel_bg'])
			self.widget.tag('configure','selection','-foreground',sh.globs['var']['color_terms_sel_fg'])
			#if View:
			#	self.shift_screen()
	
	def fill(self,code='<html><body><h1>Nothing has been loaded yet.</h1></body></html>'):
		self.widget.reset()
		self.widget.parse(code)
		
	def show(self,*args):
		self.obj.show()
		
	def close(self,*args):
		self.obj.close()



class Moves:
	
	def __init__(self,pos):
		self._pos = sh.Input(func_title='Moves.__init__',val=pos).integer()
	
	def get_cell(self):
		# cur
		pass



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
		self.MouseClicked = False
		self.CaptureHotkey = True
		self.event = None
		self.url = objs.request()._url
		self.search = objs._request._search
		
		self.master = master
		self.location = self.get_tkhtml_folder()
		self.load_tkhtml()
		self.widget = tk.Widget
		self.widget.__init__(self,master,'html',cfg,kw)
		self.vsb = ttk.Scrollbar(objs.top().widget,orient=tk.VERTICAL)
		self.hsb = ttk.Scrollbar(self.master,orient=tk.HORIZONTAL)
		self.widget.configure(self,yscrollcommand=self.vsb.set)
		self.widget.configure(self,xscrollcommand=self.hsb.set)
		self.vsb.config(command=self.yview)
		self.hsb.config(command=self.xview)
		
		self.search_article = SearchArticle()
		self.spec_symbols = SpecSymbols()
		self.save_article = SaveArticle()
		
		# todo: The same does not work when imported from sharedGUI for some reason
		if sh.oss.lin():
			objs.top().widget.wm_attributes('-zoomed',True)
		# Win, Mac
		else:
			objs.top().widget.wm_state(newstate='zoomed')
		self.history = History()
		self.create_frame_panel()
		# The very place for packing the vertical scrollbar. If we pack it earlier, it will fill an extra space, if later - it will be too small.
		self.vsb.pack(side='right',fill='y')
		self.search_field.widget.focus_set()
		self.bind(sh.globs['var']['bind_go_url'],self.go_url)
		self.bind("<Motion>",self.mouse_sel,True)
		# todo: fix: ВНИМАНИЕ: По непонятной причине, не работает привязка горячих клавиш (только мышь) для данного виджета, работает только для основного виджета!
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_copy_sel'],sh.globs['var']['bind_copy_sel_alt'],sh.globs['var']['bind_copy_sel_alt2']],action=self.copy_cell)
		# По неясной причине в одной и той же Windows ИНОГДА не удается включить '<KP_Delete>'
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_delete_cell'],action=self.delete_cell)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_add_cell'],action=self.add_cell)
		self.widget_width = 0
		self.widget_height = 0
		self.widget_offset_x = 0
		self.widget_offset_y = 0
		self.top_bbox = 0
		self.bottom_bbox = 0
		
	def get_url(self):
		# Note: encoding must be UTF-8 here
		if objs.request()._source == 'Offline':
			objs.online().reset(self.get_pair(),self.search,MTSpecific=False)
			# note # todo: elaborate
			self.url = self.search
		else:
			objs.online().reset(self.get_pair(),self.search,MTSpecific=True)
			self.url = objs.online().url()
		sh.log.append('TkinterHtmlMod.get_url',sh.lev_debug,"self.url: %s" % str(self.url))
	
	# todo: move 'move_*' procedures to Moves class
	# Перейти на 1-й термин текущей строки	
	def move_line_start(self,*args):
		if len(articles.current()._moves['_move_line_start']) > self.i and len(articles.current()._moves['_move_line_start'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_line_start'][self.i][self.j]
			self.set_cell()
		else:
			sh.log.append('TkinterHtmlMod.move_line_start',sh.lev_err,sh.globs['mes'].wrong_input2)

	# Перейти на последний термин текущей строки
	def move_line_end(self,*args):
		if len(articles.current()._moves['_move_line_end']) > self.i and len(articles.current()._moves['_move_line_end'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_line_end'][self.i][self.j]
			self.set_cell()

	# Перейти на 1-й термин статьи
	def move_text_start(self,*args):
		if articles.current()._moves['_move_text_start']:
			self.i, self.j = articles.current()._moves['_move_text_start']
		else:
			self.i, self.j = 0, 0
		self.set_cell()

	# Перейти на последний термин статьи
	def move_text_end(self,*args):
		self.i, self.j = articles.current()._moves['_move_text_end']
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
		if len(articles.current()._moves['_move_left']) > self.i and len(articles.current()._moves['_move_left'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_left'][self.i][self.j]
			self.set_cell()
		else:
			sh.log.append('TkinterHtmlMod.move_left',sh.lev_err,sh.globs['mes'].wrong_input2)

	# Перейти на следующий термин
	def move_right(self,*args):
		if len(articles.current()._moves['_move_right']) > self.i and len(articles.current()._moves['_move_right'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_right'][self.i][self.j]
			self.set_cell()
		else:
			sh.log.append('TkinterHtmlMod.move_right',sh.lev_err,sh.globs['mes'].wrong_input2)

	# Перейти на строку вниз
	def move_down(self,*args):
		if len(articles.current()._moves['_move_down']) > self.i and len(articles.current()._moves['_move_down'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_down'][self.i][self.j]
			self.set_cell()
		else:
			sh.log.append('TkinterHtmlMod.move_down',sh.lev_err,sh.globs['mes'].wrong_input2)

	# Перейти на строку вверх
	def move_up(self,*args):
		if len(articles.current()._moves['_move_up']) > self.i and len(articles.current()._moves['_move_up'][self.i]) > self.j:
			self.i, self.j = articles.current()._moves['_move_up'][self.i][self.j]
			self.set_cell()
		else:
			sh.log.append('TkinterHtmlMod.move_up',sh.lev_err,sh.globs['mes'].wrong_input2)
	
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
		objs.online()._url = articles.current()._url
		objs.online().browse()
	
	# Скопировать URL текущей статьи или выделения
	def copy_url(self,obj,mode='article'):
		cur_url = online_url_safe
		if mode == 'term':
			# Скопировать URL текущего термина. URL 1-го термина не совпадает с URL статьи!
			cur_url = articles.current()._cells[self.i][self.j].url
			if sh.globs['bool']['Iconify']:
				sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).minimize()
		elif mode == 'article':
			# Скопировать URL статьи
			cur_url = articles.current()._url
			if sh.globs['bool']['Iconify']:
				sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).minimize()
		else:
			sg.Message(func='TkinterHtmlMod.copy_url',level=sh.lev_err,message=sh.globs['mes'].unknown_mode % (str(mode),'article, term'))
		sg.Clipboard().copy(cur_url)

	# Открыть веб-страницу с определением текущего термина
	def define(self,Selected=True): # Selected: True: Выделенный термин; False: Название статьи
		if Selected:
			search_str = 'define:' + articles.current()._cells[self.i][self.j].term
		else:
			search_str = 'define:' + articles.current()._search
		objs.online().reset(base_str=sh.globs['var']['web_search_url'],search_str=search_str)
		objs.online().browse()
	
	# Обновить рисунки на кнопках
	def update_buttons(self):
		if articles.len() > 0:
			self.btn_repeat_sign.active()
		else:
			self.btn_repeat_sign.inactive()

		if articles.len() > 1:
			self.btn_repeat_sign2.active()
		else:
			self.btn_repeat_sign2.inactive()

		if articles._no > 0:
			self.btn_prev.active()
		else:
			self.btn_prev.inactive()

		if articles.len() > 1 and articles._no < articles.len() - 1:
			self.btn_next.active()
		else:
			self.btn_next.inactive()

		if self.CaptureHotkey:
			self.btn_clipboard.active()
		else:
			self.btn_clipboard.inactive()
			
		# todo: Change active/inactive button logic in case of creating three or more views
		if objs.request()._view == 0:
			self.btn_toggle_view.active()
		else:
			self.btn_toggle_view.inactive()
			
		if not objs.request().SpecialPage and objs._request.SortTerms:
			self.btn_toggle_alphabet.active()
		else:
			self.btn_toggle_alphabet.inactive()
		
		if objs._request.Block and articles.current().block():
			self.btn_toggle_block.active()
		else:
			self.btn_toggle_block.inactive()
			
		if not objs._request.SpecialPage and objs._request.Prioritize and articles.current().prioritize():
			self.btn_toggle_priority.active()
		else:
			self.btn_toggle_priority.inactive()
			
	# Перейти на предыдущий запрос
	def go_back(self,*args):
		old_index = articles._no
		articles.index_subtract()
		if old_index != articles._no:
			self.load_article()

	# Перейти на следующий запрос
	def go_forward(self,*args):
		old_index = articles._no
		articles.index_add()
		if old_index != articles._no:
			self.load_article()

	def control_length(self): # Confirm too long requests
		Confirmed = True
		if len(self.search) >= 150:
			if not sg.Message(func='TkinterHtmlMod.control_length',level=sh.lev_ques,message=sh.globs['mes'].long_request % len(self.search)).Yes:
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
	
	def search_sources(self):
		if self.control_length():
			self.get_url()
			objs.request()._url    = self.url
			objs._request._search  = self.search
			articles.search_article()
			sh.log.append('TkinterHtmlMod.search_sources',sh.lev_debug,articles.current()._search)
			self.load_article()
	
	# Search the selected term online using the entry widget (search field)
	def go_search(self,*args):
		self.search = self.search_field.widget.get().strip('\n').strip(' ')
		# Allows to use the same hotkeys for the search field and the article field
		if self.search == '':
			self.go_url()
		else:
			# Скопировать предпоследний запрос в буфер и вставить его в строку поиска (например, для перехода на этот запрос еще раз)
			if self.search == sh.globs['var']['repeat_sign2']:
				self.search_field.insert_repeat_sign2()
			# Скопировать последний запрос в буфер и вставить его в строку поиска (например, для корректировки)
			elif self.search == sh.globs['var']['repeat_sign']:
				self.search_field.insert_repeat_sign()
			else:
				self.search_sources()
					
	# Создание каркаса с полем ввода, кнопкой выбора направления перевода и кнопкой выхода
	def create_frame_panel(self):
		self.frame_panel = sg.Frame(objs.top(),expand=0,fill='x',side='bottom')
		# Поле ввода поисковой строки
		self.search_field = SearchField(parent_obj=self.frame_panel)
		self.draw_buttons()
		if self.CaptureHotkey:
			self.btn_clipboard.active()
		else:
			self.btn_clipboard.inactive()
		self.hotkeys()
		
	def set_lang(self,*args):
		objs.request()._lang = langs[self.menu_pairs.index]
		sh.log.append('TkinterHtmlMod.set_lang',sh.lev_info,'Set language to "%s"' % objs._request._lang)
		
	def set_source(self,*args):
		objs.request()._source = sources[self.menu_sources.index]
		sh.log.append('TkinterHtmlMod.set_source',sh.lev_info,'Set source to "%s"' % objs._request._source)
		self.load_article()
	
	def get_pair(self):
		return online_dic_urls[self.menu_pairs.index]
	
	def set_columns(self,*args):
		sh.log.append('TkinterHtmlMod.set_columns',sh.lev_info,str(self.menu_columns.choice))
		objs.request()._collimit = self.menu_columns.choice
		articles.current().update()
		self.load_article()
	
	# Создать кнопки
	# Bindings are indicated here only to set hints. In order to set bindings, use 'self.hotkeys'.
	def draw_buttons(self):
		# Кнопка для "чайников", заменяет Enter в search_field
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_translate,hint=sh.globs['mes'].btn_translate,action=self.go_search,inactive_image_path=sh.globs['var']['icon_go_search'],active_image_path=sh.globs['var']['icon_go_search'],bindings=[sh.globs['var']['bind_go_search'],sh.globs['var']['bind_go_search_alt']]) # В данном случае btn = hint
		# Кнопка очистки строки поиска
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_clear,hint=sh.globs['mes'].hint_clear_search_field,action=self.search_field.clear,inactive_image_path=sh.globs['var']['icon_clear_search_field'],active_image_path=sh.globs['var']['icon_clear_search_field'],bindings=[sh.globs['var']['bind_clear_search_field']])
		# Кнопка вставки
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_paste,hint=sh.globs['mes'].hint_paste_clipboard,action=self.search_field.paste,inactive_image_path=sh.globs['var']['icon_paste'],active_image_path=sh.globs['var']['icon_paste'],bindings=['<Control-v>'])
		# Кнопка вставки текущего запроса
		self.btn_repeat_sign = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_repeat_sign,hint=sh.globs['mes'].hint_paste_cur_request,action=self.search_field.insert_repeat_sign,inactive_image_path=sh.globs['var']['icon_repeat_sign_off'],active_image_path=sh.globs['var']['icon_repeat_sign'],bindings=sh.globs['var']['repeat_sign'])
		# Кнопка вставки предыдущего запроса
		self.btn_repeat_sign2 = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_repeat_sign2,hint=sh.globs['mes'].hint_paste_prev_request,action=self.search_field.insert_repeat_sign2,inactive_image_path=sh.globs['var']['icon_repeat_sign2_off'],active_image_path=sh.globs['var']['icon_repeat_sign2'],bindings=sh.globs['var']['repeat_sign2'])
		# Кнопка для вставки спец. символов
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_symbols,hint=sh.globs['mes'].hint_symbols,action=self.spec_symbols.show,inactive_image_path=sh.globs['var']['icon_spec_symbol'],active_image_path=sh.globs['var']['icon_spec_symbol'],bindings=sh.globs['var']['bind_spec_symbol'])
		self.menu_sources  = sg.OptionMenu(parent_obj=self.frame_panel,items=sources,command=self.set_source) # todo: mes
		# Выпадающий список с вариантами направлений перевода
		self.menu_pairs  = sg.OptionMenu(parent_obj=self.frame_panel,items=pairs,command=self.set_lang)
		self.menu_columns = sg.OptionMenu(parent_obj=self.frame_panel,items=(1,2,3,4,5,6,7,8,9,10),command=self.set_columns,default=4)
		# Кнопка изменения вида статьи
		# todo: Change active/inactive button logic in case of creating three or more views
		self.btn_toggle_view = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_toggle_view,hint=sh.globs['mes'].hint_toggle_view,action=self.toggle_view,inactive_image_path=sh.globs['var']['icon_toggle_view_ver'],active_image_path=sh.globs['var']['icon_toggle_view_hor'],bindings=[sh.globs['var']['bind_toggle_view'],sh.globs['var']['bind_toggle_view_alt']])
		# Кнопка включения/отключения режима блокировки словарей
		self.btn_toggle_block = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_toggle_block,hint=sh.globs['mes'].hint_toggle_block,action=self.toggle_block,inactive_image_path=sh.globs['var']['icon_block_off'],active_image_path=sh.globs['var']['icon_block_on'],bindings=sh.globs['var']['bind_toggle_block'])
		# Кнопка включения/отключения режима приоритезации словарей
		self.btn_toggle_priority = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_toggle_priority,hint=sh.globs['mes'].hint_toggle_priority,action=self.toggle_priority,inactive_image_path=sh.globs['var']['icon_priority_off'],active_image_path=sh.globs['var']['icon_priority_on'],bindings=sh.globs['var']['bind_toggle_priority'])
		# Кнопка включения/отключения сортировки словарей по алфавиту
		self.btn_toggle_alphabet = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_toggle_alphabet,hint=sh.globs['mes'].hint_toggle_alphabet,action=self.toggle_alphabet,inactive_image_path=sh.globs['var']['icon_alphabet_off'],active_image_path=sh.globs['var']['icon_alphabet_on'],bindings=sh.globs['var']['bind_toggle_alphabet'])
		# Кнопка перехода на предыдущую статью
		self.btn_prev = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_prev,hint=sh.globs['mes'].hint_preceding_article,action=self.go_back,inactive_image_path=sh.globs['var']['icon_go_back_off'],active_image_path=sh.globs['var']['icon_go_back'],bindings=sh.globs['var']['bind_go_back'])
		# Кнопка перехода на следующую статью
		self.btn_next = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_next,hint=sh.globs['mes'].hint_following_article,action=self.go_forward,inactive_image_path=sh.globs['var']['icon_go_forward_off'],active_image_path=sh.globs['var']['icon_go_forward'],bindings=sh.globs['var']['bind_go_forward'])
		# Кнопка включения/отключения и очистки истории
		# todo: fix: do not iconify on RMB (separate button frame from main frame)
		# We may hardcore 'bind_clear_history_alt' because this is bound to the button
		bind_clear_history_alt = '<ButtonRelease-3>'
		hint_history = sh.globs['mes'].hint_history + '\n' + sh.globs['var']['bind_toggle_history'] + ', ' + sh.globs['var']['bind_toggle_history_alt'] + '\n\n' + sh.globs['mes'].hint_clear_history + '\n' + sh.globs['var']['bind_clear_history'] + ', ' + bind_clear_history_alt
		self.button = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_history,hint=hint_history,action=self.history.toggle,inactive_image_path=sh.globs['var']['icon_toggle_history'],active_image_path=sh.globs['var']['icon_toggle_history'],hint_height=80)
		sg.bind(obj=self.button,bindings=bind_clear_history_alt,action=self.history.clear)
		# Кнопка перезагрузки статьи
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_reload,hint=sh.globs['mes'].hint_reload_article,action=self.reload,inactive_image_path=sh.globs['var']['icon_reload'],active_image_path=sh.globs['var']['icon_reload'],bindings=[sh.globs['var']['bind_reload_article'],sh.globs['var']['bind_reload_article_alt']])
		# Кнопка "Поиск в статье"
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_search,hint=sh.globs['mes'].hint_search_article,action=self.search_reset,inactive_image_path=sh.globs['var']['icon_search_article'],active_image_path=sh.globs['var']['icon_search_article'],bindings=sh.globs['var']['bind_re_search_article'])
		# Кнопка "Сохранить"
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_save,hint=sh.globs['mes'].hint_save_article,action=self.save_article.select,inactive_image_path=sh.globs['var']['icon_save_article'],active_image_path=sh.globs['var']['icon_save_article'],bindings=[sh.globs['var']['bind_save_article'],sh.globs['var']['bind_save_article_alt']])
		# Кнопка "Открыть в браузере"
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_in_browser,hint=sh.globs['mes'].hint_in_browser,action=self.open_in_browser,inactive_image_path=sh.globs['var']['icon_open_in_browser'],active_image_path=sh.globs['var']['icon_open_in_browser'],bindings=[sh.globs['var']['bind_open_in_browser'],sh.globs['var']['bind_open_in_browser_alt']])
		# Кнопка толкования термина. Сделана вспомогательной ввиду нехватки места
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_define,hint=sh.globs['mes'].hint_define,action=lambda:self.define(Selected=False),inactive_image_path=sh.globs['var']['icon_define'],active_image_path=sh.globs['var']['icon_define'],bindings=sh.globs['var']['bind_define'])
		# Кнопка "Перехват Ctrl-c-c"
		self.btn_clipboard = sg.Button(self.frame_panel,text=sh.globs['mes'].btn_clipboard,hint=sh.globs['mes'].hint_watch_clipboard,action=self.watch_clipboard,inactive_image_path=sh.globs['var']['icon_watch_clipboard_off'],active_image_path=sh.globs['var']['icon_watch_clipboard_on'],fg='red',bindings=[])
		# Кнопка "О программе"
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_about,hint=sh.globs['mes'].hint_about,action=objs.about().show,inactive_image_path=sh.globs['var']['icon_show_about'],active_image_path=sh.globs['var']['icon_show_about'],bindings=sh.globs['var']['bind_show_about'])
		# Кнопка выхода
		sg.Button(self.frame_panel,text=sh.globs['mes'].btn_x,hint=sh.globs['mes'].hint_x,action=h_quit.wait,inactive_image_path=sh.globs['var']['icon_quit_now'],active_image_path=sh.globs['var']['icon_quit_now'],side='right',bindings=[sh.globs['var']['bind_quit_now'],sh.globs['var']['bind_quit_now_alt']])

	def hotkeys(self):
		# Привязки: горячие клавиши и кнопки мыши
		sg.bind(obj=self.history,bindings=sh.globs['var']['bind_copy_history'],action=self.history.copy)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_go_search'],sh.globs['var']['bind_go_search_alt']],action=self.go_search)
		# todo: do not iconify at <ButtonRelease-3>
		sg.bind(obj=self.search_field,bindings=sh.globs['var']['bind_clear_search_field'],action=self.search_field.clear)
		sg.bind(obj=self.search_field,bindings=sh.globs['var']['bind_paste_search_field'],action=lambda e:self.search_field.paste())
		if sh.oss.win() or sh.oss.mac():
			sg.bind(obj=objs.top(),bindings='<MouseWheel>',action=self.mouse_wheel)
		else:
			sg.bind(obj=objs.top(),bindings=['<Button 4>','<Button 5>'],action=self.mouse_wheel)
		# Перейти на предыдущую/следующую статью
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_go_back'],action=self.go_back)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_go_forward'],action=self.go_forward)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_left'],action=self.move_left)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_right'],action=self.move_right)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_down'],action=self.move_down)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_up'],action=self.move_up)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_line_start'],action=self.move_line_start)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_line_end'],action=self.move_line_end)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_text_start'],action=self.move_text_start)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_text_end'],action=self.move_text_end)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_page_up'],action=self.move_page_up)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_move_page_down'],action=self.move_page_down)
		sg.bind(obj=objs.top(),bindings='<Escape>',action=sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).minimize)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_iconify'],action=sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).minimize)
		# Дополнительные горячие клавиши
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_quit_now'],sh.globs['var']['bind_quit_now_alt']],action=h_quit.wait)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_search_article_forward'],action=self.search_forward)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_search_article_backward'],action=self.search_backward)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_re_search_article'],action=self.search_reset)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_reload_article'],sh.globs['var']['bind_reload_article_alt']],action=self.reload)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_save_article'],sh.globs['var']['bind_save_article_alt']],action=self.save_article.select)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_show_about'],action=objs.about().show)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_toggle_history'],sh.globs['var']['bind_toggle_history']],action=self.history.toggle)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_toggle_history'],sh.globs['var']['bind_toggle_history_alt']],action=self.history.toggle)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_open_in_browser'],sh.globs['var']['bind_open_in_browser_alt']],action=self.open_in_browser)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_copy_url'],action=lambda e:self.copy_url(objs.top(),mode='term'))
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_copy_article_url'],action=lambda e:self.copy_url(objs.top(),mode='article'))
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_spec_symbol']],action=self.spec_symbols.show)
		sg.bind(obj=self.search_field,bindings='<Control-a>',action=lambda e:select_all(self.search_field.widget,Small=True))
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_define'],action=lambda e:self.define(Selected=True))
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_prev_pair'],sh.globs['var']['bind_prev_pair_alt']],action=self.menu_pairs.set_prev)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_next_pair'],sh.globs['var']['bind_next_pair_alt']],action=self.menu_pairs.set_next)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_toggle_view'],sh.globs['var']['bind_toggle_view_alt']],action=self.toggle_view)
		sg.bind(obj=objs.top(),bindings=[sh.globs['var']['bind_toggle_history'],sh.globs['var']['bind_toggle_history_alt']],action=self.history.toggle)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_clear_history'],action=self.history.clear)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_toggle_alphabet'],action=self.toggle_alphabet)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_toggle_block'],action=self.toggle_block)
		sg.bind(obj=objs.top(),bindings=sh.globs['var']['bind_toggle_priority'],action=self.toggle_priority)
		
	def show(self):
		self.pack(expand=1,fill='both')
		self.hsb.pack(side='bottom',fill='x')
		
	# Загрузить библиотеку tkhtml
	def load_tkhtml(self):
		if self.location:
			self.master.tk.eval('global auto_path; lappend auto_path {%s}' % self.location)
		self.master.tk.eval('package require Tkhtml')

	# Вернуть местоположение библиотеки tkhtml
	def get_tkhtml_folder(self):
		return os.path.join (sh.Path(os.path.abspath(sys.argv[0])).dirname(),
							 "tkhtml",
							 platform.system().replace("Darwin", "MacOSX"),
							 "64-bit" if sys.maxsize > 2**32 else "32-bit")
							 
	def get_cell(self,index):
		if len(self.pos2cell) > index:
			parts = self.pos2cell[index]
		else:
			parts = (0,0)
			sh.log.append('TkinterHtmlMod.get_cell',sh.lev_err,sh.globs['mes'].wrong_input2)
		if articles.current()._cells and len(articles.current()._cells) > parts[0] and len(articles.current()._cells[self.i]) > parts[1]:
			if articles.current()._cells[parts[0]][parts[1]].Selectable:
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
		sg.objs.root().widget.update_idletasks()
		cur_widget_width = sh.globs['geom_top']['width'] = self.winfo_width()
		cur_widget_height = sh.globs['geom_top']['height'] = self.winfo_height()
		cur_widget_offset_x = self.winfo_rootx()
		cur_widget_offset_y = self.winfo_rooty()
		if cur_widget_width != self.widget_width or cur_widget_height != self.widget_height or cur_widget_offset_x != self.widget_offset_x or cur_widget_offset_y != self.widget_offset_y:
			self.widget_width = cur_widget_width
			self.widget_height = cur_widget_height
			self.widget_offset_x = cur_widget_offset_x
			self.widget_offset_y = cur_widget_offset_y
			sh.log.append('TkinterHtmlMod.shift_screen',sh.lev_debug,sh.globs['mes'].geometry % (self.widget_width,self.widget_height,self.widget_offset_x,self.widget_offset_y))
			self.top_indexes = {}
			self.page_no = 0
			# todo: check this
			self.i, self.j = articles.current()._moves['_move_text_start']
		# Иначе экран будет смещаться до 1-й выделяемой ячейки, а не до верхнего края
		if self.page_no == 0 and not 0 in self.top_indexes:
			self.top_indexes[0] = self.text('index',0)[0]
		self.top_bbox = self.widget_height * self.page_no
		self.bottom_bbox = self.top_bbox + self.widget_height
		try:
			cur_top_bbox = self.bbox(self.index[0])[1]
			cur_bottom_bbox = self.bbox(self.index[0])[3]
		except tk.TclError:
			sh.log.append('TkinterHtmlMod.shift_screen',sh.lev_debug,sh.globs['mes'].wrong_input2)
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
			sh.log.append('TkinterHtmlMod.shift_screen',sh.lev_info,sh.globs['mes'].cur_page_no % self.page_no)
		elif cur_bottom_bbox > self.bottom_bbox:
			self.yview(self.index[0])
			self.page_no += 1
			sh.log.append('TkinterHtmlMod.shift_screen',sh.lev_info,sh.globs['mes'].cur_page_no % self.page_no)
			self.top_indexes[self.page_no] = self.index[0]
		else:
			#sh.log.append('TkinterHtmlMod.shift_screen',sh.lev_info,sh.globs['mes'].shift_screen_not_required)
			pass

	# Выделить ячейку
	def set_cell(self,View=True): # View=True будет всегда сдвигать экран до текущей ячейки при навигации с клавиатуры
		self.tag("delete", "selection")
		self.index = None
		# todo: Здесь иногда получаем ошибку с индексами
		if articles.current()._cells and len(articles.current()._cells) > self.i and len(articles.current()._cells[self.i]) > self.j:
			self.index = self.text('index',articles.current()._cells[self.i][self.j].first,articles.current()._cells[self.i][self.j].last_term)
		else:
			sh.log.append('TkinterHtmlMod.set_cell',sh.globs['mes'].wrong_input2)
		if self.index:
			#sh.log.append('TkinterHtmlMod.set_cell',sh.lev_debug,sh.globs['mes'].cur_node % self.index[0])
			# В крайнем случае можно делать так:
			#self.tag("add", "selection",self._node,0,self._node,300)
			try:
				self.tag('add','selection',self.index[0],self.index[1],self.index[2],self.index[3])
			# При удалении или вставке ячеек может возникнуть ошибка, поскольку текущий узел изменился
			except tk.TclError:
				sh.log.append('TkinterHtmlMod.set_cell',sh.lev_warn,sh.globs['mes'].tag_addition_failure % ('selection',self.index[0],self.index[3]))
			self.tag('configure','selection','-background',sh.globs['var']['color_terms_sel_bg'])
			self.tag('configure','selection','-foreground',sh.globs['var']['color_terms_sel_fg'])
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
				#sh.log.append('TkinterHtmlMod.mouse_sel',sh.lev_warn,sh.globs['mes'].unknown_cell)
				pass
			if self.mouse_index > 0:
				self.get_cell(self.mouse_index)
				self.set_cell(View=False)

	# Скопировать термин текущей ячейки (или полное ее содержимое)
	def copy_cell(self,*args):
		#self.set_cell()
		if sh.globs['bool']['CopyTermsOnly']:
			selected_text = articles.current()._cells[self.i][self.j].term
		else:
			selected_text = sh.List([articles.current()._cells[self.i][self.j].dic,articles.current()._cells[self.i][self.j].term,articles.current()._cells[self.i][self.j].comment]).space_items()
		sg.Clipboard().copy(selected_text)
		if sh.globs['bool']['Iconify']:
			sg.Geometry(parent_obj=objs.top(),title=articles.current().search()).minimize()

	# Удалить ячейку и перекомпоновать статью
	def delete_cell(self,*args):
		Found = False
		# Предполагаем, что articles.current()._elems уже прошло стадию объединения комментариев
		for i in range(len(articles.current()._elems)):
			# todo: Уточнить и упростить алгоритм
			if articles.current()._elems[i] == articles.current()._cells[self.i][self.j]:
				Found = True
				break
		if Found:
			del articles.current()._elems[i]
			articles.current().update()
			self.load_article()
		else:
			sg.Message(func='TkinterHtmlMod.delete_cell',level=sh.lev_warn,message=sh.globs['mes'].wrong_input2,Silent=self.Silent)

	# Добавить пустую ячейку и перекомпоновать статью
	def add_cell(self,*args):
		Found = False
		# Предполагаем, что articles.current()._elems уже прошло стадию объединения комментариев
		for i in range(len(articles.current()._elems)):
			# todo: Уточнить и упростить алгоритм
			if articles.current()._elems[i] == articles.current()._cells[self.i][self.j]:
				Found = True
				break
		if Found:
			articles.current()._elems.insert(i,Elem())
			articles.current().update()
			self.load_article()

	def load_article(self,*args):
		self.reset()
		# Do this before calling 'html()'
		if sep_words_found in articles.current().text() or re.search('\d+\sфраз',articles.current().search()):
			objs.request().SpecialPage = True
		else:
			objs.request().SpecialPage = False
		self.parse(articles.current().html())
		articles.current()._text = self.text('text')
		self.top_indexes = {}
		self.gen_poses()
		self.gen_pos2cell()
		articles.current().moves()
		self.move_text_start()
		objs.top().widget.title(articles.current().search())
		self.history.update()
		self.update_buttons()
		self.search_article.reset()
		self.search_field.clear()
	
	# Перейти по URL текущей ячейки
	def go_url(self,*args):
		if not self.MouseClicked:
			sh.log.append('TkinterHtmlMod.go_url',sh.lev_debug,sh.globs['mes'].cur_cell % (self.i,self.j))
			objs.request()._search = articles.current()._cells[self.i][self.j].terms() # fix
			objs._request._url     = articles.current()._cells[self.i][self.j].url()
			articles.search_article()
			sh.log.append('TkinterHtmlMod.go_url',sh.lev_info,sh.globs['mes'].opening_link % articles.current()._url)
			self.load_article()
				
	def gen_pos2cell(self):
		# 1-й символ всегда соответствует 1-й ячейке
		self.pos2cell = [[0,0]]
		cur_index = 1 # Starts with '\n'
		for i in range(len(articles.current().cells())):
			# Число столбцов в таблице должно быть одинаковым!
			for j in range(len(articles.current()._cells[i])):
				#if articles.current()._cells[i][j].dic_print: # fix
				if articles.current()._cells[i][j].dic():
					#tmp_str = articles.current()._cells[i][j].dic_print.strip() + '\n'
					tmp_str = articles.current()._cells[i][j].dic().strip() + '\n'
					articles.current()._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					#articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].term)
					articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].terms()) # fix
					articles.current()._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
				#if articles.current()._cells[i][j].speech_print:
				if articles.current()._cells[i][j].wforms():
					#tmp_str = articles.current()._cells[i][j].speech_print.strip() + '\n'
					tmp_str = articles.current()._cells[i][j].wforms().strip() + '\n'
					articles.current()._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					#articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].term)
					articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].terms())
					articles.current()._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
				#if articles.current()._cells[i][j].transc_print:
				if articles.current()._cells[i][j].transc():
					#tmp_str = articles.current()._cells[i][j].transc_print.strip() + '\n'
					tmp_str = articles.current()._cells[i][j].transc().strip() + '\n'
					articles.current()._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					#articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].term)
					articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].terms()) # fix
					articles.current()._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
				#if articles.current()._cells[i][j].term + articles.current()._cells[i][j].comment:
				if articles.current()._cells[i][j].terms() + articles.current()._cells[i][j].comments():
					#tmp_str = (articles.current()._cells[i][j].term + articles.current()._cells[i][j].comment).strip() + '\n'
					tmp_str = (articles.current()._cells[i][j].terms() + articles.current()._cells[i][j].comments()).strip() + '\n'
					tmp_str = tmp_str.replace('  ',' ')
					articles.current()._cells[i][j].first = cur_index
					cur_index += len(tmp_str)
					#articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].term)
					articles.current()._cells[i][j].last_term = articles.current()._cells[i][j].first + len(articles.current()._cells[i][j].terms())
					articles.current()._cells[i][j].last = cur_index
					for k in range(len(tmp_str)):
						self.pos2cell.append([i,j])
	#assert len(articles.current()._text) == len(self.pos2cell)
				
	def gen_poses(self):
		cur_index = 1 # Starts with '\n'
		for i in range(len(articles.current().cells())):
			for j in range(len(articles.current()._cells[i])):
				# fix
				#tmp_str = sh.List([articles.current()._cells[i][j].speech_print,articles.current()._cells[i][j].dic_print,articles.current()._cells[i][j].term,articles.current()._cells[i][j].comment]).space_items()
				tmp_str = articles.current()._cells[i][j].wforms() + articles.current()._cells[i][j].dic() + articles.current()._cells[i][j].terms() + articles.current()._cells[i][j].comments()
				articles.current()._cells[i][j].first     = cur_index
				articles.current()._cells[i][j].last_term = cur_index + len(articles.current()._cells[i][j].terms()) # fix
				articles.current()._cells[i][j].last      = cur_index + len(tmp_str)
				cur_index += len(tmp_str)
				cur_index += 1
	
	def reload(self,*args):
		articles.current().new()
		self.load_article()
		
	# Вставить спец. символ в строку поиска
	def insert_sym(self,sym):
		self.search_field.widget.insert('end',sym)
		if sh.globs['bool']['AutoCloseSpecSymbol']:
			self.spec_symbols.close()
			
	def toggle_view(self,*args):
		if objs.request()._view == 0:
			objs._request._view = 1
		elif objs._request._view == 1:
			objs._request._view = 0
		else:
			sg.Message(func='TkinterHtmlMod.toggle_view',level=sh.lev_err,message=sh.globs['mes'].unknown_mode % (str(objs._request._view),'0, 1'))
		sh.log.append('TkinterHtmlMod.toggle_view',sh.lev_info,sh.globs['mes'].new_view_mode % objs._request._view)
		# todo: why move_right and move_left are so slow to be calculated?
		# todo: store views to reload them without reloading everything
		articles.current().update()
		self.load_article()
		
	def toggle_alphabet(self,*args):
		if objs.request().SortTerms:
			objs._request.SortTerms = False
		else:
			objs._request.SortTerms = True
		articles.current().update()
		self.load_article()
	
	def toggle_block(self,*args):
		if objs.request().Block:
			objs._request.Block = False
			#sg.Message(func='TkinterHtmlMod.toggle_block',level=sh.lev_info,message='Blacklisting is now OFF.') # todo: mes
		else:
			objs._request.Block = True
			if objs._blacklist:
				#sg.Message(func='TkinterHtmlMod.toggle_block',level=sh.lev_info,message='Blacklisting is now ON.')  # todo: mes
				pass
			else:
				sg.Message(func='TkinterHtmlMod.toggle_block',level=sh.lev_warn,message='No dictionaries have been provided for blacklisting!') # todo: mes
		articles.current().update()
		self.load_article()
		
	def toggle_priority(self,*args):
		if objs.request().Prioritize:
			objs._request.Prioritize = False
			#sg.Message(func='TkinterHtmlMod.toggle_priority',level=sh.lev_info,message='Prioritizing is now OFF.') # todo: mes
		else:
			objs._request.Prioritize = True
			if objs._prioritize:
				#sg.Message(func='TkinterHtmlMod.toggle_priority',level=sh.lev_info,message='Prioritizing is now ON.')  # todo: mes
				pass
			else:
				sg.Message(func='TkinterHtmlMod.toggle_priority',level=sh.lev_warn,message='No dictionaries have been provided for prioritizing!') # todo: mes
		articles.current().update()
		self.load_article()
	
	def zzz(self): # Only needed to move quickly to the end of the class
		pass



class Paths:
	
	def __init__(self):
		self.dir = sh.Directory(path=sh.objs.pdir().add('dics'))
		self.Success = self.dir.Success
		
	def blacklist(self):
		if self.Success:
			instance = sh.File(file=os.path.join(self.dir.dir,'block.txt'))
			self.Success = instance.Success
			if self.Success:
				return instance.file
			else:
				sh.log.append('Paths.blacklist',sh.lev_warn,sh.globs['mes'].canceled)
		else:
			sh.log.append('Paths.blacklist',sh.lev_warn,sh.globs['mes'].canceled)
			
	def prioritize(self):
		if self.Success:
			instance = sh.File(file=os.path.join(self.dir.dir,'prioritize.txt'))
			self.Success = instance.Success
			if self.Success:
				return instance.file
			else:
				sh.log.append('Paths.prioritize',sh.lev_warn,sh.globs['mes'].canceled)
		else:
			sh.log.append('Paths.prioritize',sh.lev_warn,sh.globs['mes'].canceled)



# Read the blocklist and the prioritize list
class Lists:
	
	def __init__(self):
		paths            = Paths()
		self._blacklist  = paths.blacklist()
		self._prioritize = paths.prioritize()
		self.Success     = paths.Success
		
	def blacklist(self):
		if self.Success:
			text = sh.ReadTextFile(file=self._blacklist,Silent=1).get()
			text = sh.Text(text=text,Auto=1).text
			return text.splitlines()
		else:
			sh.log.append('Lists.blacklist',sh.lev_warn,sh.globs['mes'].canceled)
			
	def prioritize(self):
		if self.Success:
			text = sh.ReadTextFile(file=self._prioritize,Silent=1).get()
			text = sh.Text(text=text,Auto=1).text
			return text.splitlines()
		else:
			sh.log.append('Lists.prioritize',sh.lev_warn,sh.globs['mes'].canceled)


def load_article():
	timer = sh.Timer(func_title='Page')
	timer.start()
	
	page = pg.Page (
	                source              = objs.request()._source              ,
	                lang                = objs._request._lang                 ,
	                search              = objs._request._search               ,
	                url                 = objs._request._url                  ,
	                win_encoding        = sh.globs['var']['win_encoding']     ,
	                ext_dics            = objs.ext_dics()
	               )
	               
	page.run()
	objs._request._page     = page._page
	objs._request._html_raw = page._html_raw
	
	timer.end()

	
	Debug = 1
	
	#blacklist  = ['Австралийский сленг','Архаизм','Бранное выражение','Грубое выражение','Диалект','Жаргон','Презрительное выражение','Просторечие','Разговорное выражение','Расширение файла','Редкое выражение','Ругательство','Сленг','Табу','Табуированная лексика','Тюремный жаргон','Устаревшее слово','Фамильярное выражение','Шутливое выражение','Эвфемизм']
	
	blacklist = []
	
	prioritize = ['Общая лексика','Техника']
	#prioritize = [] # cur

	timer = sh.Timer(func_title='tags + elems + cells + pos + mkhtml')
	timer.start()
	
	tags = tg.Tags(text=objs._request._page,source=objs._request._source,pair_root=sh.globs['var']['pair_root'])
	tags.run()
	if Debug:
		tags.debug(MaxRows=100)
		input('Tags step completed. Press Enter')
	
	# Костыль # cur
	for i in range(len(tags._blocks)):
		if tags._blocks[i]._type == 'term' and tags._blocks[i]._text == 'впереди' and tags._blocks[i]._same == 1:
			sg.Message('__main__',sh.lev_info,'Term found!')
			tags._blocks[i]._same = 0
	
	elems = el.Elems(blocks=tags._blocks,source=objs._request._source,article_id=objs._request._article_id)
	elems.run()
	if Debug:
		elems.debug(Shorten=1,MaxRows=100)
		input('Elems step completed. Press Enter')
	
	objs.blocks_db().fill(elems._data)
	
	objs._blocks_db.request(source=objs._request._source,article_id=objs._request._article_id)
	phrase_dic = objs._blocks_db.phrase_dic()
	data = objs._blocks_db.assign_bp()
	
	bp = cl.BlockPrioritize(data=data,source=objs._request._source,article_id=objs._request._article_id,blacklist=blacklist,prioritize=prioritize,phrase_dic=phrase_dic)
	bp.run()
	if Debug:
		bp.debug(Shorten=1,MaxRows=100)
		input('BlockPrioritize step completed. Press Enter')
		sg.Message('BlockPrioritize',sh.lev_info,bp._query.replace(';',';\n'))
	objs._blocks_db.update(query=bp._query)
	
	if Debug:
		objs._blocks_db.print(Shorten=1,MaxRows=100,MaxRow=15)
		input('After-BP DB created. Press Enter')
	
	data = objs._blocks_db.assign_cells()
	cells = cl.Cells(data=data,collimit=objs._request._collimit,phrase_dic=phrase_dic)
	cells.run()
	if Debug:
		cells.debug(MaxRows=40)
		input('Cells step completed. Press Enter')
		sg.Message('Cells',sh.lev_info,cells._query.replace(';',';\n'))
	objs._blocks_db.update(query=cells._query)
	
	if Debug:
		objs._blocks_db.print(Shorten=1,MaxRows=100,MaxRow=15)
		input('After-Cells DB created. Press Enter')

	#objs._blocks_db.print(Shorten=1,MaxRow=18,MaxRows=100)
	#objs._blocks_db.dbc.execute('select * from BLOCKS where BLOCK=0 order by CELLNO,NO')
	#objs._blocks_db.print(Selected=1,Shorten=1,MaxRow=18,MaxRows=100)
	
	data = objs._blocks_db.assign_pos()
	pos = cl.Pos(data=data)
	pos.run()
	if Debug:
		pos.debug(MaxRows=40)
		input('Pos step completed. Press Enter')
		sg.Message('Pos',sh.lev_info,pos._query.replace(';',';\n'))
	objs._blocks_db.update(query=pos._query)
	
	if Debug:
		objs._blocks_db.print(Shorten=1,MaxRows=1000,MaxRow=15)
	
	get_html = mh.HTML(data=objs._blocks_db.fetch(),collimit=objs._request._collimit)
	objs._request._html = get_html._html
	
	timer.end()
	
	if Debug:
		input('Return.')
	
	objs.webframe().fill(code=objs._request._html)



objs = Objects()


if  __name__ == '__main__':
	sg.objs.start()
	
	ConfigMclient()

	load_article()
	objs.webframe().show()
	
	kl_mod.keylistener.cancel() # todo (?): del
	
	sg.objs.end()
	
	'''
	articles = Articles()
	h_quit   = Quit()
	h_table  = TkinterHtmlMod(objs.top().widget)
	objs.top().widget.protocol("WM_DELETE_WINDOW",h_quit.wait)
	# 'OptionMenu' is updated when the user selects an item. There is a need to update it manually only in case of different default 'request' values.
	h_table.menu_columns.set(request._collimit)
	h_table.menu_sources.set(request._source)
	timed_update() # Do not wrap this function. Change this carefully.
	articles.search_article()
	h_table.load_article()
	h_table.show()
	objs.top().show()
	sg.objs.root().run()
	'''
