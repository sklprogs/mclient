#!/usr/bin/python3
#coding=UTF-8
import sys
import os
from time import time, sleep
import re
import codecs
import webbrowser
import tkinter as tk
import tkinter.messagebox as tkmes
import tkinter.filedialog as dialog
from tkinter import ttk
# В Python 3 не работает просто import urllib, импорт должен быть именно такой, как здесь
import urllib.request, urllib.parse
import html.parser
import posixpath
from configparser import SafeConfigParser
import eg_mod as eg
import mes_ru
import mes_en
import platform

__author__ = 'Peter Sklyar'
__copyright__ = 'Copyright 2015, 2016, Peter Sklyar'
__license__ = 'GPL v.3'
__version__ = '4.1'
__email__ = 'skl.progs@gmail.com'

# All third-party modules are the intellectual work of their authors.

license_easygui = '''
EasyGui version0.96
EasyGui version0.95
Copyright (c) 2010, Stephen Raymond Ferg
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer. 

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation and/or 
other materials provided with the distribution. 

3. The name of the author may not be used to endorse or promote products derived 
from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED 
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT 
OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING 
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY 
OF SUCH DAMAGE.
'''

license_tkinterhtml = '''tkinterhtml
https://bitbucket.org/aivarannamaa/tkinterhtml
License: MIT
Copyright (c) <year> aivarannamaa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Нельзя закомментировать, поскольку cur_func нужен при ошибке чтения конфига (которое вне функций)
cur_func = 'MAIN'
gpl3_url_ru = 'http://rusgpl.ru/rusgpl.html'
gpl3_url_en = 'http://www.gnu.org/licenses/gpl.html'
# Данные глобальные переменные оформлены в виде словаря, что позволяет не использовать лишний раз global.
globs = {'AbortAll':False,'LogCount':0,'cur_widget':'ERR_NO_WIDGET_DEFINED','ui_lang':'ru','mes':mes_ru,'license_url':gpl3_url_ru,'mclient_config_root':'mclient.cfg','config_parser':SafeConfigParser(),'_tkhtml_loaded':False,'var':{},'int':{}}
globs['geom_top'] = {'width':0,'height':0}

db = {}
db['search'] = globs['mes'].welcome
# todo: Избавиться
globs['Quit'] = False
db['ShowHistory'] = False

lev_crit = 'CRITICAL'
lev_err = 'ERROR'
lev_warn = 'WARNING'
lev_info = 'INFO'
lev_debug_err = 'DEBUG-ERROR'
lev_debug = 'DEBUG'

# Сообщения
my_email = 'skl.progs@gmail.com'
my_yandex_money = '41001418272280'
# Скрытые сообщения об ошибках
err_mes_unavail = 'CF_UNICODETEXT_UNAVAILABLE'
err_mes_copy = 'CLIPBOARD_COPY_ERROR'
err_mes_paste = 'CLIPBOARD_PASTE_ERROR'
err_wrong_enc = 'WRONG_ENCODING_ERROR'
err_incor_log_mes = 'INCORRECT_LOG_MESSAGE'
cur_widget = 'ERR_NO_WIDGET_DEFINED'
err_mes_no_feature_text = 'ERR_NO_FEATURE_TEXT'
err_mes_no_full_inq_text = 'ERR_NO_FULL_INQ_TEXT'
err_mes_no_inq_path = 'ERR_NO_INQ_PATH'
err_mes_empty_question = 'ERR_EMPTY_QUESTION'
err_mes_empty_warning = 'ERR_EMPTY_WARNING'
err_mes_empty_info = 'ERR_EMPTY_INFO'
err_mes_empty_error = 'ERR_EMPTY_ERROR'
err_mes_empty_input = 'ERR_EMPTY_INPUT'
err_mes_no_selection = 'ERR_NO_SELECTION'
err_mes_selected_not_matched = 'SELECTED_NOT_MATCHED'
err_mes_empty_mes = 'EMPTY_MESSAGE'
err_mes_unsupported_lang = 'ERR_UNSUPPORTED_LANGUAGE'
# Не добавляю cur_widget в cmd_err_mess, поскольку он может меняться
cmd_err_mess = [err_mes_unavail,err_mes_copy,err_mes_paste,err_wrong_enc,err_incor_log_mes,err_mes_no_feature_text,err_mes_no_full_inq_text,err_mes_no_inq_path,err_mes_empty_question,err_mes_empty_warning,err_mes_empty_info,err_mes_empty_error,err_mes_empty_input,err_mes_no_selection,err_mes_selected_not_matched,err_mes_empty_mes,err_mes_unsupported_lang]

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Multitran client-specific variables
'''
ENG => RUS      Англо-русский:  'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s'
DEU => RUS      Нем-рус:        'http://www.multitran.ru/c/m.exe?l1=3&l2=2&s=%s'
SPA => RUS      Исп-рус:        'http://www.multitran.ru/c/m.exe?l1=5&l2=2&s=%s'
FRA => RUS      Франц-рус:      'http://www.multitran.ru/c/m.exe?l1=4&l2=2&s=%s'
NLD => RUS      Нидерл-рус:     'http://www.multitran.ru/c/m.exe?l1=24&l2=2&s=%s'
ITA => RUS      Итал-рус:       'http://www.multitran.ru/c/m.exe?l1=23&l2=2&s=%s'
LAV => RUS      Латыш-рус:      'http://www.multitran.ru/c/m.exe?l1=27&l2=2&s=%s'
EST => RUS      Эстон-рус:      'http://www.multitran.ru/c/m.exe?l1=26&l2=2&s=%s'
AFR => RUS      Африкаанс-рус:  'http://www.multitran.ru/c/m.exe?l1=31&l2=2&s=%s'
EPO => RUS      Эсперанто-рус:  'http://www.multitran.ru/c/m.exe?l1=34&l2=2&s=%s'
RUS => XAL		Рус-калм:		'http://www.multitran.ru/c/m.exe?l1=2&l2=35&s=%s'
XAL => RUS      Калм-рус:       'http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s'
ENG => DEU      Англ-нем:       'http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s'
ENG => EST      Англ-эст:       'http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s'
'''
online_url_root = 'http://www.multitran.ru/c/m.exe?'
online_url_safe = 'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%ED%E5%E2%E5%F0%ED%E0%FF+%F1%F1%FB%EB%EA%E0'
default_pair = 'ENG <=> RUS'
globs['cur_pair'] = default_pair
pairs = ['ENG <=> RUS','DEU <=> RUS','SPA <=> RUS','FRA <=> RUS','NLD <=> RUS','ITA <=> RUS','LAV <=> RUS','EST <=> RUS','AFR <=> RUS','EPO <=> RUS','RUS <=> XAL','XAL <=> RUS','ENG <=> DEU','ENG <=> EST']
online_dic_urls = ['http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=3&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=5&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=4&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=24&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=23&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=27&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=26&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=31&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=34&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=2&l2=35&s=%s','http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s']
assert len(pairs) == len(online_dic_urls)
#globs['var']['online_dic_url'] = online_dic_urls[0]
my_program_title = ''
not_found_online = 'Вы знаете перевод этого слова? Добавьте его в словарь'
sep_words_found = 'найдены отдельные слова'
message_board = 'спросить в форуме'
# 'спросить в форуме' не удается обработать в этом списке, поэтому обрабатываю его отдельно
delete_entries = ['Вход','Регистрация','Сообщить об ошибке','Изменить','Удалить','Добавить']
delete_entries_pos = [0,0,-1,-1,-1,-1]
assert len(delete_entries) == len(delete_entries_pos)
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
# Список символов, которые можно считать за буквы.
allowed_syms = ['°']
sizes = {}
sizes['top'] = {}
sizes['top']['width'] = 0
sizes['top']['height'] = 0

# Разделы конфигурационного файла
'''SectionLinuxSettings = 'Linux settings'
SectionWindowsSettings = 'Windows settings'
SectionMacSettings = 'Mac settings'
'''
SectionVariables = 'Variables'
SectionIntegers = 'Integer Values'
#SectionFloatings = 'Floating Values'
SectionBooleans = 'Boolean'

# Custom
default_encoding = 'utf-8'
# Неразрывный пробел, non-breaking space
nbspace = ' '
dlb = '\n'
wdlb = '\r\n'
tab = '        '
col_limit = 5

root = tk.Tk()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Placeholders
def log(cur_func,level,log_mes,TransFunc=False):
	pass
	#if level == lev_crit or level == lev_debug_err or level == lev_warn or level == lev_err:
	#	print(cur_func,':',level,':',log_mes)
#------------------------------------------------------------------------------
# Placeholder
def decline_nom(words_nf,Decline=False):
	pass
#------------------------------------------------------------------------------
# Placeholder
def check_args(func,arg_list):
	pass
#------------------------------------------------------------------------------
def check_type(*args):
	pass
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Ошибка
def ErrorMessage(cur_func='MAIN',cur_mes=err_mes_empty_error,Critical=True):
	#root.withdraw()
	tkmes.showerror(globs['mes'].err_head,cur_mes)
	if Critical:
		log(cur_func,lev_crit,cur_mes)
		sys.exit()
	else:
		log(cur_func,lev_err,cur_mes)
	root.deiconify()

# В этой функции лог еще не подключен, поэтому отмена всех операций не поддерживается
# Проверить существование файла
def exist(cur_file,Silent=False,Critical=True):
	cur_func = sys._getframe().f_code.co_name
	if os.path.exists(cur_file):
		Success=True
	else:
		Success=False
		mestype(cur_func,globs['mes'].file_not_found % cur_file,Silent=Silent,Critical=Critical)
	# Лог еще не подключен
	return Success
		
# Определить тип ОС
def detect_os():
	#cur_func = sys._getframe().f_code.co_name
	if 'win' in sys.platform:
		par = 'win'
	elif 'lin' in sys.platform:
		par = 'lin'
	elif 'mac' in sys.platform:
		par = 'mac'
	else:
		par = 'unknown'
	# Занесение в лог здесь делать рано, конфиг еще не прочитан
	#log(cur_func,lev_debug,str(par))
	return par

sys_type = detect_os()
if sys_type == 'win':
	sysdiv = '\\'
else:
	sysdiv = '/'
	
# Верно определить каталог по полному пути вне зависимости от ОС
def true_dirname(path,UseLog=True):
	cur_func = sys._getframe().f_code.co_name
	curdir = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		path = path.replace('\\','//')
		#curdir = ntpath.dirname(path)
		curdir = posixpath.dirname(path)
		if sys_type == 'win':
			curdir = curdir.replace('//','\\')
		if UseLog:
			log(cur_func,lev_debug,globs['mes'].full_path2 % (path,curdir))
	return curdir
	
# Вернуть расширение файла с точкой
def get_ext(file,Lower=False):
	cur_func = sys._getframe().f_code.co_name
	func_res = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		func_res = os.path.splitext(file)[1]
		if Lower:
			func_res = func_res.lower()
		log(cur_func,lev_debug,str(func_res))
	return func_res

# Изменить язык графического интерфейса и сообщений
def toggle_ui_lang():
	if globs['ui_lang'] == 'en':
		globs['ui_lang'] = 'ru'
		globs['mes'] = mes_ru
		globs['license_url'] = gpl3_url_ru
	else:
		globs['ui_lang'] = 'en'
		globs['mes'] = mes_en
		globs['license_url'] = gpl3_url_en

# Загрузить конфигурацию по умолчанию
def default_config(config='mclient',Init=True):
	cur_func = sys._getframe().f_code.co_name
	# Ключи, которые, возможно, стоит убрать: pixel_hack, use_format, use_output, mismatch_num, (некоторые в bool), CorrectHTML, UsePaste, DeclineFeatures, DicHints, AlwaysMaximize, TrimEnd, currar, Online
	if Init:
		globs['lin'] = {}
		globs['win'] = {}
		globs['mac'] = {}
		globs['var'] = {}
		globs['int'] = {}
		globs['float'] = {}
		globs['bool'] = {}
	# Эти ключи нужно создавать до чтения конфига
	globs['bin_dir'] = true_dirname(os.path.realpath(sys.argv[0]),UseLog=False)
	globs['mclient_config'] = globs['bin_dir'] + sysdiv + globs['mclient_config_root']
	'''
	CONFIG CHANGES:
	[bool]:
	- TermsColoredSep
	+ CopyTermsOnly
	+ SelectTermsOnly
	[int]:
	+ font_comments_size, font_dics_size, font_terms_size
	[var]:
	- bind_hide_top, color_borders, font_comments, font_dics, font_terms
	+ bind_hide_top, font_comments_family, font_dics_family, font_terms_family
	'''
	if config == 'mclient':
		globs['bool'].update({
			'AlwaysMaximize':True,
			'AutoCloseSpecSymbol':False,
			'AutoHideHistory':False,
			'CopyTermsOnly':True,
			'ExploreMismatch':True,
			'InternalDebug':False,
			'mclientSaveTitle':False,
			'ReadOnlyProtection':False,
			'SelectTermsOnly':True,
			'ShortHistory':False,
			'ShowWallet':True,
			'Spelling':True,
			'TextButtons':False,
			'UnixSelection':False,
			'UseOptionalButtons':True,
							})
		#----------------------------------------------------------------------
		globs['int'].update({
			'default_button_size':36,
			'default_hint_border_width':1,
			'default_hint_delay':800,
			'default_hint_height':40,
			'default_hint_width':280,
			'font_comments_size':3,
			'font_dics_size':4,
			'font_terms_size':4,
			'pixel_hack':18,
			'tab_length':5
							})
		#----------------------------------------------------------------------
		#globs['var'].update({'bind_re_search_article':'<Control-f>','bind_reload_article':'<Control-r>','bind_save_article':'<Control-s>'})
		globs['var'].update({
			'bind_clear_history_alt':'<Control-Shift-Delete>',
			'bind_clear_history':'<ButtonRelease-3>',
			'bind_clear_search_field':'<ButtonRelease-3>',
			'bind_hide_top':'<ButtonRelease-2>',
			'bind_copy_article_url':'<Shift-F7>',
			'bind_copy_history':'<ButtonRelease-3>',
			'bind_copy_sel_alt':'<Control-KP_Enter>',
			'bind_copy_sel_alt2':'<ButtonRelease-3>',
			'bind_copy_sel':'<Control-Return>',
			'bind_copy_url':'<Control-F7>',
			'bind_define':'<Control-d>',
			'bind_get_history':'<Double-Button-1>',
			'bind_go_back':'<Alt-Left>',
			'bind_go_forward':'<Alt-Right>',
			'bind_go_search_alt':'<KP_Enter>',
			'bind_go_search':'<Return>',
			'bind_go_url':'<Button-1>',
			'bind_move_down':'<Down>',
			'bind_move_left':'<Left>',
			'bind_move_line_end':'<End>',
			'bind_move_line_start':'<Home>',
			'bind_move_page_down':'<Next>',
			'bind_move_page_end':'<Shift-End>',
			'bind_move_page_start':'<Shift-Home>',
			'bind_move_page_up':'<Prior>',
			'bind_move_right':'<Right>',
			'bind_move_text_end':'<Control-End>',
			'bind_move_text_start':'<Control-Home>',
			'bind_move_up':'<Up>',
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
			'bind_search_field':'<F6>',
			'bind_show_about':'<F1>',
			'bind_spec_symbol':'<Control-e>',
			'bind_toggle_history_alt':'<Control-h>',
			'bind_toggle_history':'<F4>',
			'bind_toggle_iconify':'<Control-i>',
			'bind_watch_clipboard_alt':'<Control-t>',
			'bind_watch_clipboard':'<F8>',
			'color_comments':'gray',
			'color_dics':'cadet blue',
			'color_terms_sel':'cyan',
			'color_terms':'black',
			'default_hint_background':'#ffffe0',
			'default_hint_border_color':'navy',
			'default_hint_direction':'top',
			'font_comments_family':'Mono',
			'font_dics_family':'Arial',
			'font_history':'Sans 12',
			'font_style':'Sans 14',
			'font_terms_sel':'Sans 14 bold italic',
			'font_terms_family':'Serif',
			'icon_change_ui_lang':'icon_36x36_change_ui_lang.gif',
			'icon_clear_history':'icon_36x36_clear_history.gif',
			'icon_clear_search_field':'icon_36x36_clear_search_field.gif',
			'icon_define':'icon_36x36_define.gif',
			'icon_go_back_off':'icon_36x36_go_back_off.gif',
			'icon_go_back':'icon_36x36_go_back.gif',
			'icon_go_forward_off':'icon_36x36_go_forward_off.gif',
			'icon_go_forward':'icon_36x36_go_forward.gif',
			'icon_go_search':'icon_36x36_go_search.gif',
			'icon_main':'icon_64x64_main.gif',
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
			'icon_watch_clipboard_off':'icon_36x36_watch_clipboard_off.gif',
			'icon_watch_clipboard_on':'icon_36x36_watch_clipboard_on.gif',
			'online_dic_url':'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s',
			'repeat_sign':'!',
			'repeat_sign2':'!!',
			'spec_syms':'àáâäāæßćĉçèéêēëəĝģĥìíîïīĵķļñņòóôõöōœšùúûūŭũüýÿžжҗқңөүұÀÁÂÄĀÆSSĆĈÇÈÉÊĒËƏĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӨҮҰ',
			'web_search_url':'http://www.google.ru/search?ie=UTF-8&oe=UTF-8&sourceid=navclient=1&q=%s',
			'win_encoding':'windows-1251',
			'window_size':'1024x768',
				})
	else:
		ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(config),'mclient'))
		
# Вопрос
def Question(cur_func='MAIN',cur_mes=err_mes_empty_question):
	#root.withdraw()
	par = tkmes.askokcancel(globs['mes'].ques_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_info,cur_mes)
	return par

# Названия такие же, как у модуля PyZenity (кроме List)
# Информация
def InfoMessage(cur_func='MAIN',cur_mes=err_mes_empty_info):
	#root.withdraw()
	tkmes.showinfo(globs['mes'].inf_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_info,cur_mes)

# Предупреждение
def Warning(cur_func='MAIN',cur_mes=err_mes_empty_warning):
	#root.withdraw()
	tkmes.showwarning(globs['mes'].warn_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_warn,cur_mes)
	
# Заменить двойные разрывы строк на одиночные
def delete_double_line_breaks(line,Strip=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Удаляем разрывы строк в случае копирования из табличного процессора
		# Для LO/Gnumeric (даже Win-версий) достаточно \n, для MSO этого недостаточно (нужно \r\n)
		# Без str может дать TypeError: Type str doesn't support the buffer API
		line = str(line)
		while '\r\n' in line:
			line = line.replace('\r\n','\n')
		line = line.replace('\r','\n')
		while '\n\n' in line:
			line = line.replace('\n\n','\n')
		# Удалить пробелы и переносы строк с начала и конца
		if Strip:
			line = line.strip()
		else:
			# Удалять перенос строки с конца текста нужно всегда
			line = line.strip(dlb)
		log(cur_func,lev_debug,str(line))
	return line

# Вставить из буфера обмена
def clipboard_paste(MakePretty=True):
	cur_func = sys._getframe().f_code.co_name
	line = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Иначе происходит зависание в цикле
		root.update()
		try:
			line = root.clipboard_get()
		except:
			line = err_mes_paste
			log(cur_func,lev_debug,str(line))
			Warning(cur_func,globs['mes'].clipboard_paste_failure)
		if MakePretty:
			if not line in cmd_err_mess:
				line = delete_double_line_breaks(line)
			if line.startswith(dlb):
				line = line.replace(dlb,'',1)
			line = line.rstrip(dlb)
		log(cur_func,lev_debug,str(line))
	return line
	
# Создание корректной ссылки в Интернете (URI => URL)
def online_request(base_str,my_request_bytes): #str, bytes
	cur_func = sys._getframe().f_code.co_name
	my_url = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		my_url = base_str % urllib.parse.quote(my_request_bytes)
		log(cur_func,lev_debug,str(my_url))
	return my_url
	
# Открыть заданный адрес в веб-браузере по умолчанию
def browse_url(base_str,search_str):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		request_bytes = bytes(search_str,encoding=default_encoding)
		search_str = online_request(base_str,request_bytes)
		try:
			webbrowser.open(search_str,new=2,autoraise=True)
		except:
			Warning(cur_func,globs['mes'].browser_failure % search_str)

# Показать сообщение определенного типа в зависимости от параметров
def mestype(func,cur_mes,Silent=False,Critical=False,Info=False):
	if Critical and not Info:
		ErrorMessage(func,cur_mes)
	else:
		if Info:
			if Silent:
				log(func,lev_info,cur_mes)
			else:
				InfoMessage(func,cur_mes)
		else:
			if Silent:
				log(func,lev_warn,cur_mes)
			else:
				Warning(func,cur_mes)
				
# Удалить знаки пунктуации
# Это самый простой путь. Заменяет все совпадения (в отличие от использования переменных из punc_array) и не требует regexp (при котором потребуется экранирование)
def delete_punctuation(fragm):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		fragm = fragm.replace(',','')
		fragm = fragm.replace('.','')
		fragm = fragm.replace('!','')
		fragm = fragm.replace('?','')
		fragm = fragm.replace(':','')
		fragm = fragm.replace(';','')
		log(cur_func,lev_debug,str(fragm))
	return fragm
	
# Удалить нумерацию в виде алфавита
def delete_alphabetic_numeration(line):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		my_expr = ' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
		match = re.search(my_expr,line)
		while match:
			replace_what = match.group(0)
			replace_with = match.group(1)
			line = line.replace(replace_what,replace_with)
			match = re.search(my_expr,line)
		log(cur_func,lev_debug,str(line))
	return line

# Преобразовать строку в нижний регистр, удалить пунктуацию и алфавитную нумерацию
def prepare_str(line,Extended=False,Lower=True,PuncOnly=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if Lower:
			line = line.lower()
		line = line.replace('ё','е')
		if PuncOnly:
			line = delete_punctuation(line)
		else:
			line = line.replace('"','')
			line = line.replace('“','')
			line = line.replace('”','')
			line = line.replace('«','')
			line = line.replace('»','')
			line = line.replace('(','')
			line = line.replace(')','')
			line = line.replace('[','')
			line = line.replace(']','')
			line = line.replace('{','')
			line = line.replace('}','')
			line = line.replace('*','')
			line = delete_punctuation(line)
			line = delete_alphabetic_numeration(line)
		if Extended:
			line = re.sub('\d+','',line)
			#line = line.replace('-','')
		#log(cur_func,lev_debug,str(line))
	return line

# Привести в вид, понимаемый виджетом Tk, список вида [sent_no,pos1]
def convert2tk(sent,pos,Even=False):
	cur_func = sys._getframe().f_code.co_name
	tk_str = '1.0'
	check_args(cur_func,[[sent,globs['mes'].type_int],[pos,globs['mes'].type_int],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if Even:
			tk_str = str(sent+1) + '.' + str(pos+1)
		else:
			tk_str = str(sent+1) + '.' + str(pos)
		log(cur_func,lev_debug,str(tk_str))
	return tk_str
	
# Скопировать в буфер обмена
def clipboard_copy(line):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		line = str(line)
		try:
			root.clipboard_clear()
			root.clipboard_append(line)
			# Указать режиму буфера, что переводить измененный буфер не надо
			globs['IgnorePaste'] = True
		except:
			pass
			'''# Иначе в окне не сработают горячие клавиши
			set_keyboard_layout('en')
			text_field(title=globs['mes'].clipboard_copy_failure,user_text=line,SelectAll=True,ReadOnly=True)
			line = err_mes_copy
			log(cur_func,lev_debug,str(line))
			'''
		
# Вернуть веб - страницу онлайн - словаря с термином
def get_online_article(Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# db['search'] требуется всегда, даже если на входе URL
		# Если на входе URL, то читается db['url'], если же на входе строка, то читается db['search'] и создается db['url']
		db['page'] = ''
		db['html'] = ''
		while db['page'] == '':
			Success = False
			# Загружаем страницу
			try:
				# Если загружать страницу с помощью "page=urllib.request.urlopen(my_url)", то в итоге получится HTTPResponse, что полезно только для удаления тэгов JavaScript. Поскольку мы вручную удаляем все лишние тэги, то на выходе нам нужна строка.
				db['page'] = urllib.request.urlopen(db['url']).read()
				log(cur_func,lev_info,globs['mes'].ok % db['search'])
				Success = True
			except:
				log(cur_func,lev_warn,globs['mes'].failed % db['search'])
				#mestype(cur_func,globs['mes'].webpage_unavailable,Silent=Silent,Critical=Critical)
				if not Question(cur_func,globs['mes'].webpage_unavailable_ques):
					sys.exit()
			if Success: # Если страница не загружена, то понятно, что ее кодировку изменить не удастся
				try:
					# Меняем кодировку globs['var']['win_encoding'] на нормальную
					db['page'] = db['page'].decode(globs['var']['win_encoding'])
					db['html'] = db['page']
				except:
					mestype(cur_func,globs['mes'].wrong_html_encoding,Silent=Silent,Critical=Critical)
	
# Конвертировать строку в целое число
def str2int(line):
	cur_func = sys._getframe().f_code.co_name
	par = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			par = int(line)
		except:
			log(cur_func,lev_err,globs['mes'].convert_to_int_failure % line)
		log(cur_func,lev_debug,str(par))
	return par

# Конвертировать строку с позицией Tkinter вида '1.20' в список вида [sent_no,pos_no]
def convertFromTk(line,Even=False):
	cur_func = sys._getframe().f_code.co_name
	lst = [0,0]
	check_args(cur_func,[[line,globs['mes'].type_str],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		num_lst = line.split('.')
		assert len(num_lst) == 2
		sent = str2int(num_lst[0])
		check_type(cur_func,sent,globs['mes'].type_int)
		pos = str2int(num_lst[1])
		check_type(cur_func,pos,globs['mes'].type_int)
		if Even:
			lst = [sent-1,pos-1]
		else:
			lst = [sent-1,pos]
		# Tkinter позволяет выделять так, что конец придется на первый (=нулевой) символ в начале предложения, и из-за Even получится отрицательное число. Компенсируем это.
		for i in range(len(lst)):
			if lst[i] < 0:
				log(cur_func,lev_warn,globs['mes'].negative % lst[i])
				lst[i] = 0
		log(cur_func,lev_debug,str(lst))
	return lst

# Конвертировать числовую позицию формата int в позицию в формате Tkinter
# Пример: 20 = > '1.20'
def pos2tk(text_db,pos,Even=False):
	cur_func = sys._getframe().f_code.co_name
	tk_pos = '1.0'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# < при len = maxi + 1 и <= при len = maxi
		assert pos < text_db['len']
		#elem = text_db['pos_sl'][pos-1]
		elem = text_db['pos_sl'][pos]
		tk_pos = convert2tk(elem[0],elem[1],Even=Even)
		log(cur_func,lev_debug,str('%d => %s' % (pos,tk_pos)))
	return tk_pos

# Конвертировать позицию в формате Tkinter в числовую позицию формата int
# Пример: '1.20' = > 20
def tk2pos(text_db,tk_pos,Even=False):
	cur_func = sys._getframe().f_code.co_name
	found = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Пример: [0,10]
		pos_sl_no = convertFromTk(tk_pos,Even=Even)
		# Выделение в Tkinter может выйти за пределы самого текста, поэтому заранее определяем правую границу.
		found = len(text_db['pos_sl'])
		for i in range(len(text_db['pos_sl'])):
			if pos_sl_no == text_db['pos_sl'][i]:
				found = i
				break
		log(cur_func,lev_debug,str('%s => %s' % (tk_pos,str(found))))
	return found
	
# Выбор одного элемента из списка
def SelectFromList(title,cur_mes,list_array,Insist=False,Silent=False,Critical=True,MakeLower=False):
	cur_func = sys._getframe().f_code.co_name
	log(cur_func,lev_debug,globs['mes'].title % str(title))
	log(cur_func,lev_debug,globs['mes'].mes % str(cur_mes))
	log(cur_func,lev_debug,globs['mes'].lst % str(list_array))
	check_args(cur_func,[[title,globs['mes'].type_str],[cur_mes,globs['mes'].type_str],[list_array,globs['mes'].type_lst]])
	choice = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Если на входе пустой список, на выходе выдаем ''
		if list_array == []:
			log(cur_func,lev_warn,globs['mes'].empty_lists_not_allowed)
		# Если список включает только 1 файл, вывести его сразу
		elif len(list_array)==1:
			choice = list_array[0]
		elif Insist:
			while empty(choice):
				root.withdraw()
				try:
					choice = eg.choicebox(cur_mes,title,list_array) #MakeLower=MakeLower
				except:
					mestype(cur_func,globs['mes'].eg,Silent=Silent,Critical=Critical)
				root.deiconify()
				if empty(choice):
					Warning(cur_func,globs['mes'].force_choice)
		else:
			root.withdraw()
			try:
				choice = eg.choicebox(cur_mes,title,list_array) #MakeLower=MakeLower
			except:
				mestype(cur_func,globs['mes'].eg,Silent=Silent,Critical=Critical)
			root.deiconify()
			if empty(choice) and Critical:
				globs['AbortAll'] = True
		log(cur_func,lev_debug,str(choice))
	return choice

# Удалить файл (но не каталог)
def delete(file,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		if os.path.exists(file):
			try:
				os.remove(file)
				log(cur_func,lev_info,globs['mes'].deleting % file)
			except:
				Success = False
				mestype(cur_func,globs['mes'].file_del_failure2 % file,Silent=Silent,Critical=Critical)
		else:
			Success = False
			mestype(cur_func,globs['mes'].file_del_failure3 % file,Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,str(Success))
	return Success

# Проверить существование файла и выйти в случае отказа от перезаписи
def rewrite(file,Force=False,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		# Существование файла здесь не является критическим параметром, что позволяет использовать 'if rewrite(file):' для несуществующих файлов.
		if os.path.exists(file):
			if Force:
				Warning(cur_func,globs['mes'].rewrite_warning % file)
				# Используется вторая проверка, поскольку пользователь может вручную удалить файл после предупреждения
				if os.path.exists(file):
					Success = delete(file,Silent=False,Critical=Critical)
			else: 
				if Question(cur_func,globs['mes'].rewrite_ques % file):
					if os.path.exists(file):
						Success = delete(file,Silent=False,Critical=Critical)
				else:
					Success = False
		log(cur_func,lev_debug,str(Success))
	return Success

# Записать текст в файл в режиме 'write' или 'append'
# Critical распространяется только на попытку записи файла. Проверка режима обязана быть Critical
def write_file(file,text,mode='w',Silent=False,Critical=False,AskRewrite=True):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	check_type(cur_func,file,globs['mes'].type_str)
	check_type(cur_func,mode,globs['mes'].type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		if mode != 'w' and mode != 'a':
			Success = False
			mestype(cur_func,globs['mes'].wrong_mode % mode,Silent=False,Critical=True)
		# Может создаваться новый файл, поэтому проверку существования не делаем
		if AskRewrite:
			Success = rewrite(file)
		if Success:
			try:
				with open(file,mode,encoding=default_encoding) as f:
					f.write(text)
				log(cur_func,lev_info,globs['mes'].file_written % file)
			except:
				Success = False
				mestype(cur_func,globs['mes'].file_write_failure % file,Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,str(Success))
	return Success

# Удостовериться, что входная строка имеет какую - то ценность
def empty(my_input):
	cur_func = sys._getframe().f_code.co_name
	par = True # При отмене всех задач должно возвращаться True, иначе 'if not empty()' в таких случаях возвращает True!
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if my_input == '' or my_input == None or my_input == [] or my_input == () or my_input == {} or my_input in cmd_err_mess:
			par = True
		else:
			par = False
		log(cur_func,lev_debug,str(par))
	return par

# Диалог сохранения файла
def dialog_save_file(text,filetypes=(),Critical=True):
	cur_func = sys._getframe().f_code.co_name
	file = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if empty(filetypes):
			filetypes=((globs['mes'].plain_text,'.txt'),(globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*'))
		options = {}
		options['initialfile'] = ''
		options['filetypes'] = filetypes
		options['title'] = globs['mes'].save_as
		# Если реализовать выбор файла через EasyGui, получим ошибку при выборе каталога, защищенного от записи, не ловится даже в try - except, получаем "alloc: invalid block: 0xb33c040: c0 b Aborted"
		#file = eg.filesavebox(msg=globs['mes'].select_file,filetypes=mask)
		try:
			file = dialog.asksaveasfilename(**options)
		except:
			mestype(cur_func,globs['mes'].file_sel_failed,Critical=Critical)
		# dialog при пустом выборе возвращает (), который мы заменяем на '', потому что возвращаемое значение должно представлять собой строку, а не кортеж (иначе, например, такие процедуры как exist() будут вылетать)
		if file == ():
			file = ''
		if empty(file):
			if Critical:
				globs['AbortAll'] = True
		else:
			# На Linux добавляется расширение после asksaveasfilename, на Windows - нет. Мы не можем понять, что выбрал пользователь, поскольку asksaveasfilename возвращает только имя файла. Поэтому, если никакого разрешения нет, добавляем '.htm' в надежде, что браузер нормально откроет текстовый файл.
			# ВНИМАНИЕ: это сработает для обычного текста и для веб-страниц, с другими типами могут быть проблемы.
			if empty(get_ext(file)):
				file += '.htm'
			# rewrite (AskRewrite) не задействуем, поскольку наличие файла уже проверяется на этапе asksaveasfilename()
			write_file(file,text,mode='w',Silent=False,Critical=Critical,AskRewrite=False)
	log(cur_func,lev_debug,globs['mes'].writing % str(file))
	return file

# Выделить весь текст в виджете
def select_all(widget,Small=True): # Entry: Small=True; Text: Small=False
	if Small:
		widget.select_clear()
		widget.select_range(0,'end')
	else:
		widget.tag_add('sel','1.0','end')
		widget.mark_set('insert','1.0')
	return 'break'

# Конструктор для создания окна для манипуляции текстом
def text_field(title=None,user_text=err_mes_empty_input,CheckSpelling=False,GoTo='',Insist=False,SelectAll=False,ReadOnly=False,Small=False,TrimEnd=False,CursorTk='1.0',xoffset=0,yoffset=0): # Edit=True равноценно user_text!=err_mes_empty_input
	cur_func = sys._getframe().f_code.co_name
	func_res = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Если правописание (globs['bool']['Spelling']) отключено в конфиге, то отключить и опциональный параметр CheckSpelling
		if not globs['bool']['Spelling']:
			CheckSpelling = False
		top, res = tk.Toplevel(root), [None]
		if globs['bool']['AlwaysMaximize'] and not Small:
			if sys_type == 'lin':
				top.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				top.wm_state(newstate='zoomed')
		def close_top(event):
			top.destroy()
			root.deiconify()
		def callback(event):
			if Small:
				returned = widget.get()
			elif ReadOnly:
				returned = user_text
			else:
				returned = widget.get(1.0,'end')
			# На входе без ошибок (пока) принимаются список и строка
			if get_obj_type(returned,Verbal=True) == globs['mes'].type_str:
				returned = returned.strip(dlb)
			res[0] = returned
			close_top(None)
		root.withdraw()
		if empty(title):
			title = globs['mes'].text
		title += ' ' + my_program_title
		top.title(title)
		top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=globs['var']['icon_main']))
		# Позволяет удалять пробел и пунктуацию с конца, что полезно при некорректной обработке Ctrl + Shift + - >
		if TrimEnd and not Small: # По текущим данным, globs['bool']['UnixSelection'] не работает с Entry
			user_text = delete_end_punc(user_text)
		if Small:
			widget = tk.Entry(top,font=globs['var']['font_style'])
		else:
			scrollbar = tk.Scrollbar(top,jump=0)
			widget = tk.Text(top,height=10,font=globs['var']['font_style'],wrap='word',yscrollcommand=scrollbar.set)
		if not empty(user_text):
			widget.insert('end',user_text)
		if ReadOnly and globs['bool']['ReadOnlyProtection'] and not Small:
			widget.config(state='disabled')
		if not Small:
			# Позволяет использовать мышь для управления скроллбаром
			scrollbar.config(command=widget.yview)
			scrollbar.pack(side='right',fill='y')
		create_binding(widget=widget,bindings=['<Return>','<KP_Enter>'],action=callback)
		if Small:
			widget.pack()
		else:
			widget.pack(expand=1,fill='both')
		# Выход по клику кнопки
		if ReadOnly:
			create_button(parent_widget=top,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=callback,expand=1)
		else:
			create_button(parent_widget=top,text=globs['mes'].save_and_close,hint=globs['mes'].save_and_close,action=callback,expand=1)
		# Выход по нажатию Enter и Пробел на кнопке (навигация по Shift+Tab)
		widget.focus_force()
		if empty(GoTo):
			if Small:
				# todo: tk.Entry: index: Gets the numerical position corresponding to the given index.
				# tk.Entry не поддерживает координаты Tk (поддерживаются только целочисленные позиции и 'end')
				if CursorTk == '1.0':
					widget.icursor(0)
				elif CursorTk == 'end':
					widget.icursor('end')
				else:
					ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(CursorTk),'0-9*, end'))
			else:
				mark_add(widget=widget,mark_name='insert',postk=CursorTk)
		# todo: tk.Entry: index: Gets the numerical position corresponding to the given index.
		# tk.Entry не поддерживает mark_set
		elif not Small:
			try:
				goto_pos = widget.search(GoTo,'1.0','end')
				widget.mark_set('goto',goto_pos)
				widget.mark_set('insert',goto_pos)
				widget.yview('goto')
			except:
				log(cur_func,lev_err,globs['mes'].shift_screen_failure % 'goto')
		if SelectAll:
			select_all(widget,Small=Small)
		# Игнорировать ключ SelectAll и всегда выделять весь текст в tk.Entry
		#elif Small and not ReadOnly:
		#	select_all(widget,Small=True)
		create_binding(widget=widget,bindings='<Control-a>',action=lambda x:select_all(widget,Small=Small))
		globs['cur_widget'] = widget
		if globs['bool']['UnixSelection'] and not Small: # По текущим данным, globs['bool']['UnixSelection'] не работает с Entry
			create_binding(widget=globs['cur_widget'],bindings='<Control-Shift-Left>',action=lambda x: top.after(20, left_sel_mod))
			create_binding(widget=globs['cur_widget'],bindings='<Control-Shift-Right>',action=lambda x: top.after(20, right_sel_mod))
		if Small or ReadOnly:
			create_binding(widget=widget,bindings='<Escape>',action=close_top)
		if xoffset != 0 or yoffset != 0:
			root.geometry('+{0}+{1}'.format(xoffset,yoffset))
		top.wait_window(top)
		func_res = res[0]
		log(cur_func,lev_debug,str(func_res))
		if Insist:
			if empty(func_res):
				ErrorMessage(cur_func,globs['mes'].empty_text)
			# Предотвратить возможные ошибки при глобальной отмене
		if func_res == None:
			func_res = ''
	return func_res
	
# Создать переменные, которые основываются на ключах конфига, но не входят в него
def additional_keys():
	cur_func = sys._getframe().f_code.co_name
	# Это второстепенный ключ, указывать его в конфиге не надо
	globs['IgnorePaste'] = False
	globs['var']['spec_syms'] = list(globs['var']['spec_syms'])

# Загрузить все конфигурационные файлы
def read_configs(Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	total_keys = 0
	changed_keys = 0
	missing_keys = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		# Должен лежать в одном каталоге с программой
		# Руководство питона предлагает использовать разные методы для разных платформ: http://docs.python.org/2/library/os.path.html
		cur_mes = ''
		if not exist(globs['mclient_config'],Silent=Silent,Critical=Critical):
			Success = False
		if Success:
			try:
				globs['config_parser'].readfp(codecs.open(globs['mclient_config'],'r','utf-8'))
			except:
				Success = False
				mestype(cur_func,globs['mes'].invalid_config % globs['mclient_config'],Silent=Silent,Critical=Critical)
			if Success:
				'''if sys_type == 'lin':
					config_section = SectionLinuxSettings
				elif sys_type == 'win':
					config_section = SectionWindowsSettings
				elif sys_type == 'mac':
					config_section = SectionMacSettings
				'''
				# Сокращенное название раздела в globs
				config_section_abbr = sys_type
				#--------------------------------------------------------------
				'''# Загрузка раздела SectionLinuxSettings/SectionWindowsSettings/SectionMacSettings
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[sys_type]:
						total_keys += 1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value = globs['config_parser'].get(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys += 1
								globs[config_section_abbr][config_option] = new_config_value
						else:
							Success = False
							missing_keys += 1
							cur_mes += globs['mes'].no_config_option % (config_option,config_section) + dlb
				else:
					Success = False
					cur_mes += globs['mes'].no_config_section % config_section + dlb
				'''
				#--------------------------------------------------------------
				# Загрузка раздела SectionVariables
				config_section = SectionVariables
				config_section_abbr = 'var'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					#----------------------------------------------------------
					# 'ui_lang' - это единственный параметр 1-го уровня вложенности globs, который можно менять при загрузке конфига (иначе придется создавать globs['var'] раньше, чем хотелось бы)
					config_option = 'ui_lang'
					total_keys += 1
					if globs['config_parser'].has_option(config_section,config_option):
						new_config_value=globs['config_parser'].get(config_section,config_option)
						# Обратить внимание, что раздел указывать не нужно
						if globs[config_option] != new_config_value:
							log(cur_func,lev_info,globs['mes'].key_changed % config_option)
							changed_keys += 1
							toggle_ui_lang()
					else:
						Success = False
						missing_keys += 1
						cur_mes += globs['mes'].no_config_option % (config_option,config_section) + dlb
					#----------------------------------------------------------
					for config_option in globs[config_section_abbr]:
						total_keys += 1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].get(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys += 1
								globs[config_section_abbr][config_option] = new_config_value
						else:
							Success = False
							missing_keys += 1
							cur_mes += globs['mes'].no_config_option % (config_option,config_section) + dlb
				else:
					Success = False
					cur_mes += globs['mes'].no_config_section % config_section + dlb
				#--------------------------------------------------------------
				# Загрузка раздела SectionIntegers
				config_section = SectionIntegers
				config_section_abbr = 'int'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys += 1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value = globs['config_parser'].getint(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys += 1
								globs[config_section_abbr][config_option] = new_config_value
						else:
							Success = False
							missing_keys += 1
							cur_mes += globs['mes'].no_config_option % (config_option,config_section) + dlb
				else:
					Success = False
					cur_mes += globs['mes'].no_config_section % config_section + dlb
				#--------------------------------------------------------------
				'''# Загрузка раздела SectionFloatings
				config_section = SectionFloatings
				config_section_abbr = 'float'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys += 1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].getfloat(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys += 1
								globs[config_section_abbr][config_option] = new_config_value
						else:
							Success = False
							missing_keys += 1
							cur_mes += globs['mes'].no_config_option % (config_option,config_section) + dlb
				else:
					Success = False
					cur_mes += globs['mes'].no_config_section % config_section + dlb
				'''
				#--------------------------------------------------------------
				# Загрузка раздела SectionBooleans
				config_section = SectionBooleans
				config_section_abbr = 'bool'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys += 1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value = globs['config_parser'].getboolean(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys += 1
								globs[config_section_abbr][config_option] = new_config_value
						else:
							Success = False
							missing_keys += 1
							cur_mes = globs['mes'].no_config_option % (config_option,config_section) + dlb
				else:
					Success = False
					cur_mes += globs['mes'].no_config_section % config_section + dlb
		#----------------------------------------------------------------------
		# Данные действия необходимо производить вне зависимости от успеха в чтении конфига и именно после него
		# Эти вспомогательные ключи зависят от основных и не обновляются самостоятельно. Принудительно обновляем их после чтения основных ключей.
		additional_keys()
		for key in globs['var']:
			if key.startswith('icon_'):
				globs['var'][key] = globs['bin_dir'] + sysdiv + globs['var'][key]
		#----------------------------------------------------------------------
		if Critical and not Success:
			sys.exit()
		if not Success:
			cur_mes = globs['mes'].wrong_configs_structure + dlb + dlb + cur_mes
			cur_mes += dlb + globs['mes'].default_config
			text_field(title=globs['mes'].errors,user_text=cur_mes,ReadOnly=True)
		log(cur_func,lev_debug,str(Success))
	log(cur_func,lev_info,globs['mes'].config_stat % (total_keys,changed_keys,missing_keys))
	return Success

# Название типа на русском
def obj_type_verbal(obj_type_str,IgnoreErrors=False):
	cur_func = sys._getframe().f_code.co_name
	obj_type_str = str(obj_type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if obj_type_str == 'str':
			obj_type_str = globs['mes'].type_str
		elif obj_type_str == 'list':
			obj_type_str = globs['mes'].type_lst
		elif obj_type_str == 'dict':
			obj_type_str = globs['mes'].type_dic
		elif obj_type_str == 'tuple':
			obj_type_str = globs['mes'].type_tuple
		elif obj_type_str == 'set' or obj_type_str == 'frozenset':
			obj_type_str = globs['mes'].type_set
		elif obj_type_str == 'int':
			obj_type_str = globs['mes'].type_int
		elif obj_type_str == 'long':
			obj_type = globs['mes'].type_long_int
		elif obj_type_str == 'float':
			obj_type_str = globs['mes'].type_float
		elif obj_type_str == 'complex':
			obj_type_str = globs['mes'].type_complex
		elif obj_type_str == 'bool':
			obj_type_str = globs['mes'].type_bool
		elif IgnoreErrors:
			pass
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (obj_type_str,'str, list, dict, tuple, set, frozenset, int, long, float, complex, bool'))
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str

# Вернуть тип параметра
def get_obj_type(obj,Verbal=True,IgnoreErrors=False):
	cur_func = sys._getframe().f_code.co_name
	obj_type_str = ''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		obj_type_str = str(type(obj))
		obj_type_str = obj_type_str.replace("<class '",'')
		obj_type_str = obj_type_str.replace("'>",'')
		# int, float, str, list, dict, tuple, NoneType
		if Verbal:
			obj_type_str = obj_type_verbal(obj_type_str,IgnoreErrors=IgnoreErrors)
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str
	
# Remove a tag within a range
def tag_remove(widget,tag_name,pos1tk='1.0',pos2tk='end',Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.tag_remove(tag_name,pos1tk,pos2tk)
			log(cur_func,lev_debug,globs['mes'].tag_removed % (tag_name,pos1tk,pos2tk))
		except tk.TclError:
			mestype(cur_func,globs['mes'].tag_remove_failed % (tag_name,str(widget),pos1tk,pos2tk),Silent=Silent,Critical=Critical)
			
# Add a mark
def mark_add(widget,mark_name,postk,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	check_args(cur_func,[[mark_name,globs['mes'].type_str],[postk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.mark_set(mark_name,postk)
			log(cur_func,lev_debug,globs['mes'].mark_added % (mark_name,postk))
		except tk.TclError:
			mestype(cur_func,globs['mes'].mark_addition_failure % (mark_name,postk),Silent=Silent,Critical=Critical)
			
# Remove a mark
def mark_remove(widget,mark_name,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	check_args(cur_func,[[mark_name,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.mark_unset(mark_name)
			log(cur_func,lev_debug,globs['mes'].mark_removed % (mark_name))
		except tk.TclError:
			mestype(cur_func,globs['mes'].mark_removal_failure % mark_name,Silent=Silent,Critical=Critical)

# Remove a tag
# Note: False will be returned if the tag has not been found
def tag_remove(widget,tag_name='tag',pos1tk='1.0',pos2tk='end'):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	check_args(cur_func,[[tag_name,globs['mes'].type_str],[pos1tk,globs['mes'].type_str],[pos2tk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		try:
			widget.tag_remove(tag_name,pos1tk,pos2tk)
		except:
			Success = False
			log(cur_func,lev_warn,globs['mes'].tag_remove_failed % (tag_name,str(widget),pos1tk,pos2tk))
		log(cur_func,lev_debug,str(Success))
	return Success

# Add a tag
def tag_add(widget,tag_name='tag',pos1tk='1.0',pos2tk='end',DeletePrevious=True):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	check_args(cur_func,[[tag_name,globs['mes'].type_str],[pos1tk,globs['mes'].type_str],[pos2tk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		# Предварительно удалить все имеющиеся одноименные тэги из виджета. Полезно, если тэг может иметь только одно текущее выделение.
		if DeletePrevious:
			# Вероятно, неуспех данной операции не должен свидетельствовать об неуспехе всей операции, поскольку при отсутствии тэга выйдет ошибка, но тэг отсутствует в самом начале.
			# Необходимо очистить весь виджет, поэтому диапазон не указываем
			tag_remove(widget=widget,tag_name=tag_name)
		# 1. Установка тэга
		try:
			widget.tag_add(tag_name,pos1tk,pos2tk)
			log(cur_func,lev_debug,globs['mes'].tag_added % (tag_name,pos1tk,pos2tk))
		except:
			Success = False
			log(cur_func,lev_err,globs['mes'].tag_addition_failure % (tag_name,pos1tk,pos2tk))
		log(cur_func,lev_debug,str(Success))
	return Success
	
# Configure an added tag (background, foreground)
def tag_config(widget,tag_name='tag',mode='bg',color='cyan'):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	check_args(cur_func,[[tag_name,globs['mes'].type_str],[mode,globs['mes'].type_str],[color,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		# 2. Настройка тэга
		try:
			if mode == 'bg':
				widget.tag_config(tag_name,background=color)
				log(cur_func,lev_debug,globs['mes'].tag_bg % (tag_name,color))
			elif mode == 'fg':
				widget.tag_config(tag_name,foreground=color)
				log(cur_func,lev_debug,globs['mes'].tag_fg % (tag_name,color))
			else:
				Success = False
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'bg, fg'))
		except:
			Success = False
			if mode == 'fg':
				log(cur_func,lev_err,globs['mes'].tag_fg_failure % tag_name)
			else:
				log(cur_func,lev_err,globs['mes'].tag_bg_failure % tag_name)
		log(cur_func,lev_debug,str(Success))
	return Success

# Add and configure a tag
def tag_add_config(widget,tag_name,pos1tk,pos2tk,mode='bg',color='cyan',DeletePrevious=True):
	cur_func = sys._getframe().f_code.co_name
	Success = False
	check_args(cur_func,[[tag_name,globs['mes'].type_str],[pos1tk,globs['mes'].type_str],[pos2tk,globs['mes'].type_str]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success = True
		Success = tag_add(widget=widget,tag_name=tag_name,pos1tk=pos1tk,pos2tk=pos2tk,DeletePrevious=DeletePrevious)
		if Success:
			Success = tag_config(widget=widget,tag_name=tag_name,mode=mode,color=color)
		log(cur_func,lev_debug,str(Success))
	return Success

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# mclient non-shared code
# Convert HTML entities to UTF-8 and perform other necessary operations
def prepare_page():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			html_parser = html.parser.HTMLParser()
			db['page'] = html_parser.unescape(db['page'])
		except:
			log(cur_func,lev_err,globs['mes'].html_conversion_failure)
		# It is not clear why .replace does not replace all suitable elements
		db['page'] = db['page'].replace('\r\n','')
		db['page'] = db['page'].replace('\n','')
		db['page'] = db['page'].replace('\xa0',' ')
		while '  ' in db['page']:
			db['page'] = db['page'].replace('  ',' ')
		db['page'] = db['page'].replace(nbspace+'<','<')
		db['page'] = db['page'].replace(' <','<')
		db['page'] = db['page'].replace('>'+nbspace,'>')
		db['page'] = db['page'].replace('> ','>')
		#----------------------------------------------------------------------
		# If separate words are found instead of a phrase, prepare those words only
		if sep_words_found in db['page']:
			db['page'] = db['page'].replace(sep_words_found,'')
			if message_board in db['page']:
				board_pos = db['page'].index(message_board)
			else:
				board_pos = - 1
			while tag_pattern11 in db['page']:
				if db['page'].index(tag_pattern11) < board_pos:
					db['page'] = db['page'].replace(tag_pattern11,tag_pattern13)
				else:
					break
			while tag_pattern1 in db['page']:
				tag_pos = db['page'].index(tag_pattern1)
				if tag_pos < board_pos:
					db['page'] = db['page'].replace(tag_pattern1,tag_pattern12,1)
				else:
					break
			# Вставить sep_words_found перед названием 1 - го словаря. Нельзя вставлять его в самое начало ввиду особенностей обработки delete_entries.
			if globs['bool']['ExploreMismatch']:
				db['page'] = db['page'].replace(tag_pattern1,tag_pattern5 + sep_words_found + tag_pattern6 + tag_pattern1,1)
			else:
				db['page'] = db['page'][:board_pos] + tag_pattern7 + tag_pattern5 + sep_words_found + tag_pattern6
			# Поскольку message_board встречается между вхождениями, а не до них или после них, то обрабатываем его вне delete_entries.
			db['page'] = db['page'].replace(message_board,'')
			if globs['bool']['InternalDebug']:
				text_field(title="db['page']",user_text=db['page'],ReadOnly=True)
		#----------------------------------------------------------------------
		# Move the phrases section to the new line
		regexp_obj = re.compile('\d+ фраз')
		phrases_index = - 1
		for x in regexp_obj.finditer(db['page']):
			phrases_index = x.start()
		if phrases_index != - 1:
			if tag_pattern2 in db['page'][:phrases_index]:
				phrases_index = db['page'][:phrases_index].rindex(tag_pattern2)
				db['page'] = db['page'][:phrases_index] + tag_pattern1 + globs['mes'].phrases + tag_pattern8 + db['page'][phrases_index:]
		#----------------------------------------------------------------------
		# Remove tags <p>, </p>, <b> and </b>, because they can be inside hyperlinks
		db['page'] = db['page'].replace('<p>','')
		db['page'] = db['page'].replace('</p>','')
		db['page'] = db['page'].replace('<b>','')
		db['page'] = db['page'].replace('</b>','')
		# Remove symbols '<' and '>' that do not define tags
		db['page'] = list(db['page'])
		i = 0
		TagOpen = False
		while i < len(db['page']):
			if db['page'][i] == '<':
				if TagOpen:
					log(cur_func,lev_debug,globs['mes'].deleting_useless_elem % (i,db['page'][i]))
					if i >= 10 and i < len(db['page'])-10:
						log(cur_func,lev_debug,globs['mes'].context % ''.join(db['page'][i-10:i+10]))
					del db['page'][i]
					i -= 1
				else:
					TagOpen = True
			if db['page'][i] == '>':
				if not TagOpen:
					log(cur_func,lev_info,globs['mes'].deleting_useless_elem % (i,db['page'][i]))
					if i >= 10 and i < len(db['page']) - 10:
						log(cur_func,lev_info,globs['mes'].context % ''.join(db['page'][i-10:i+10]))
					del db['page'][i]
					i -= 1
				else:
					TagOpen = False
			i += 1
		db['page'] = ''.join(db['page'])
		db['len_page'] = len(db['page'])
		log(cur_func,lev_debug,"db['page']: '%s'" % db['page'])
		log(cur_func,lev_debug,"db['len_page']: %d" % db['len_page'])

# Analyse tags and collect the information on them
def analyse_tags():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		start_time = time()
		tags_pos()
		extract_tags()
		remove_useless_tags()
		extract_tag_contents()
		end_time = time()
		log(cur_func,lev_info,globs['mes'].tag_analysis_timer % str(end_time-start_time))
	
# Create a list with positions of signs '<' and '>'
def tags_pos():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		tag_borders = []
		i = 0
		while i < db['len_page']:
			# Signs '<' and '>' as such can cause serious problems since they can occur in invalid cases like "perform >>> conduct >> carry out (vbadalov)". The following algorithm is also not 100% precise but is better.
			if db['page'][i] == '<' or db['page'][i] == '>':
				tag_borders.append(i)
			i += 1
		if len(tag_borders) % 2 != 0:
			log(cur_func,lev_warn,globs['mes'].wrong_tag_num % len(tag_borders))
			if len(tag_borders) > 0:
				del tag_borders[-1]
			else:
				log(cur_func,lev_warn,globs['mes'].tag_borders_empty)
		tmp_borders = []
		i = 0
		while i < len(tag_borders):
			uneven = tag_borders[i]
			i += 1
			even = tag_borders[i]
			i += 1
			tmp_borders += [[uneven,even]]
		db['tag_borders'] = tmp_borders
		db['len_tag_borders'] = len(db['tag_borders'])
		log(cur_func,lev_debug,"db['tag_borders']: %s" % str(db['tag_borders']))
		log(cur_func,lev_debug,"db['len_tag_borders']: %d" % db['len_tag_borders'])
	
# Extract fragments inside signs '<' and '>'
def extract_tags():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['tags'] = []
		for i in range(db['len_tag_borders']):
			# + 1 because of slice peculiarities
			pos1 = db['tag_borders'][i][0]
			pos2 = db['tag_borders'][i][1] + 1
			db['tags'].append(db['page'][pos1:pos2])
			log(cur_func,lev_debug,globs['mes'].extracting_tag % db['tags'][-1])
		db['len_tags'] = len(db['tags'])
		log(cur_func,lev_info,globs['mes'].tags_found % (db['len_tags']))
		log(cur_func,lev_debug,str(db['tags']))
	
# Create a list of on - screen text elements for each useful tag
def extract_tag_contents():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
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
		'''
		db['elem'] = []
		#----------------------------------------------------------------------
		for i in range(db['len_tags']):
			# Если используется шаблон вместо пустого словаря, то нужно обратить внимание на то, что при изменении присвоенных значений будет меняться и сам шаблон!
			db['elem'].append({'url':online_url_safe,'selectable':False,'dic':'','term':'','comment':''})
			EntryMatch = False
			url = online_url_safe
			# Extracting dictionary abbreviations
			if db['tags'][i].startswith(tag_pattern1):
				tmp_str = db['tags'][i]
				tmp_str = tmp_str.replace(tag_pattern1,'',1)
				tmp_str = re.sub('".*','',tmp_str)
				if tmp_str == '' or tmp_str == ' ':
					log(cur_func,lev_warn,globs['mes'].wrong_tag % db['tags'][i])
				else:
					db['elem'][-1]['dic'] = tmp_str
			# Extracting terms
			if db['tags'][i].startswith(tag_pattern2):
				# It is reasonable to bind URLs to terms only, but we want the number of URLs to match the number of article elements, moreover, extra URLs can appear useful.
				if i + 1 < db['len_tags']:
					pos1 = db['tag_borders'][i][1] + 1
					pos2 = db['tag_borders'][i+1][0] - 1
					if pos1 >= db['len_page']:
						log(cur_func,lev_warn,globs['mes'].tag_near_text_end % db['tags'][i])
					else:
						if tag_pattern7 in db['tags'][i+1] or tag_pattern8 in db['tags'][i+1]:
							tmp_str = db['page'][pos1:pos2+1]
							# If we see symbols '<' or '>' there for some reason, then there is a problem in the tag extraction algorithm. We can make manual deletion of '<' and '>' there.
							db['elem'][-1]['term'] = tmp_str
						# Extracting URL
						url = db['tags'][i].replace(tag_pattern2,'',1)
						# We need re because of such cases as "<a href = "m.exe?t = 74188_2_4&s1 = faute">ошибка"
						url = re.sub('\"\>.*','">',url)
						if url.endswith(tag_pattern8):
							url = url.replace(tag_pattern8,'')
							url = online_url_root + url
						else:
							log(cur_func,lev_warn,globs['mes'].url_extraction_failure % url)
				else:
					log(cur_func,lev_warn,globs['mes'].last_tag % db['tags'][i])
			# Extracting comments
			if db['tags'][i] == tag_pattern3 or db['tags'][i] == tag_pattern5 or db['tags'][i] == tag_pattern9:
				pos1 = db['tag_borders'][i][1]+1
				if pos1 >= db['len_page']:
					log(cur_func,lev_warn,globs['mes'].tag_near_text_end % db['tags'][i])
				else:
					if i+1 < db['len_tags']:
						pos2 = db['tag_borders'][i+1][0]-1
					else:
						log(cur_func,lev_warn,globs['mes'].last_tag % db['tags'][i])
						if db['len_tag_borders'] > 0:
							pos2 = db['tag_borders'][-1][1]
						else:
							pos2 = pos1
							log(cur_func,lev_warn,globs['mes'].tag_borders_empty)
					tmp_str = db['page'][pos1:pos2+1]
					# Sometimes, the tag contents is just '('. We remove it, so the final text does not look like '( user_name'
					if tmp_str == '' or tmp_str == ' ' or tmp_str == '|' or tmp_str == '(':
						log(cur_func,lev_warn,globs['mes'].empty_tag_contents % db['tags'][i])
					else:
						db['elem'][-1]['comment'] = tmp_str
			log(cur_func,lev_debug,globs['mes'].adding_url % url)
			db['elem'][-1]['url'] = url
			if not empty(db['elem'][-1]['term']):
				db['elem'][-1]['selectable'] = True
		#----------------------------------------------------------------------
		# Deleting some common entries
		# We can also delete 'g-sort' here
		# todo: remove useless entries by their URL, not by their names
		i = 0
		while i < len(db['elem']):
			if db['elem'][i]['term'] in delete_entries:
				del db['elem'][i]
				i -= 1
			i += 1
		#----------------------------------------------------------------------
		# We do not need empty entries before creating cells, so we delete them (if any)
		i = 0
		while i < len(db['elem']):
			if empty(db['elem'][i]['dic']) and empty(db['elem'][i]['term']) and empty(db['elem'][i]['comment']):
				del db['elem'][i]
				i -= 1
			i += 1
		#----------------------------------------------------------------------
		# Logging
		log(cur_func,lev_debug,"db['elem']: %s" % db['elem'])
		#----------------------------------------------------------------------
		# Human-readable representation
		if globs['bool']['InternalDebug']:
			res_mes = ''
			for i in range(len(db['elem'])):
				res_mes += "i: %d" % i + tab + db['elem'][i]['dic'] + tab + db['elem'][i]['term'] + tab + db['elem'][i]['comment'] + tab + db['elem'][i]['url'] + tab + str(db['elem'][i]['selectable']) + dlb
			text_field(title=globs['mes'].db_all_check,user_text=res_mes,ReadOnly=True)
	
# Adjust positions of entries for pretty viewing
def prepare_search():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Removing unwanted values
		# We assume that a 'dic'-type entry shall be succeeded by a 'term'-type entry, not a 'comment'-type entry. Therefore, we delete 'comment'-type entries after 'dic'-type entries in order to ensure that dictionary abbreviations do not succeed full dictionary titles. We also can delete full dictionary titles and leave abbreviations instead.
		# todo (?)
		#if i > 0:
		#	if db['all']['types'][i-1] == 'dics' and db['all']['types'][i] == 'comments':
		i = 0
		while i < len(db['elem']):
			# todo: Удалять по URL
			if db['elem'][i]['comment'].endswith('.') or 'Макаров' in db['elem'][i]['comment'] or 'Вебстер' in db['elem'][i]['comment'] or 'Webster' in db['elem'][i]['comment'] or 'Майкрософт' in db['elem'][i]['comment'] or 'Microsoft' in db['elem'][i]['comment']:
				log(cur_func,lev_info,globs['mes'].deleting_useless_entry % str(db['elem'][i]))
				del db['elem'][i]
				i -= 1
			i += 1
		# todo: обновить db['page']
		# todo: Проверить, обязательно ли все еще следующее условие: The first element of the 'dic' list must precede the first element of the 'term' list

# Remove tags that are not relevant to the article structure
def remove_useless_tags():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		tags_total = db['len_tags']
		i = 0
		while i < db['len_tags']:
			#if tags[i].startswith(tag_pattern1) or tags[i].startswith(tag_pattern2) or tags[i].startswith(tag_pattern3) or tags[i].startswith(tag_pattern4) or tags[i]==tag_pattern5 or tags[i]==tag_pattern6 or tags[i]==tag_pattern7 or tags[i]==tag_pattern8:
			if tag_pattern1 in db['tags'][i] or tag_pattern2 in db['tags'][i] or tag_pattern3 in db['tags'][i] or tag_pattern4 in db['tags'][i] or tag_pattern5 in db['tags'][i] or tag_pattern6 in db['tags'][i] or tag_pattern7 in db['tags'][i] or tag_pattern8 in db['tags'][i]:
				log(cur_func,lev_debug,globs['mes'].tag_kept % db['tags'][i])
				pass
			else:
				log(cur_func,lev_debug,globs['mes'].deleting_tag % (i,db['tags'][i]))
				del db['tags'][i]
				db['len_tags'] -= 1
				del db['tag_borders'][i]
				db['len_tag_borders'] -= 1
				i -= 1
			i += 1
		# Logging
		log(cur_func,lev_debug,"db['len_tags']: %d" % db['len_tags'])
		log(cur_func,lev_debug,"db['tags']: %s" % str(db['tags']))
		log(cur_func,lev_debug,"db['len_tag_borders']: %d" % db['len_tag_borders'])
		log(cur_func,lev_debug,"db['tag_borders']: %s" % str(db['tag_borders']))
		log(cur_func,lev_info,globs['mes'].tags_stat % (tags_total,db['len_tags'],tags_total-db['len_tags']))
		# Testing
		assert db['len_tags'] == db['len_tag_borders']
	
# Преобразовать координаты заданного виджета из пикселей в Tkinter
def pixels2tk(widget,x,y,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	tk_pos = '1.0'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			tk_pos = widget.index('@%d,%d' % (x,y))
		except:
			mestype(cur_func,globs['mes'].unknown_coor % (str(widget),str(x),str(y)),Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,tk_pos)
	return tk_pos

# Вычислить координаты текста для текущей видимой области
def get_page_coor(page_no):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['coor_db']['pages'][page_no] = {}
		db['coor_db']['pages'][page_no]['up'] = {}
		db['coor_db']['pages'][page_no]['up']['pix'] = {}
		db['coor_db']['pages'][page_no]['down'] = {}
		db['coor_db']['pages'][page_no]['down']['pix'] = {}
		db['coor_db']['pages'][page_no]['up']['pix']['x'] = db['coor_db']['widget'].winfo_x()
		db['coor_db']['pages'][page_no]['up']['pix']['y'] = db['coor_db']['widget'].winfo_y()
		db['coor_db']['pages'][page_no]['down']['pix']['x'] = db['coor_db']['pages'][page_no]['up']['pix']['x']+db['coor_db']['width']
		db['coor_db']['pages'][page_no]['down']['pix']['y'] = db['coor_db']['pages'][page_no]['up']['pix']['y']+db['coor_db']['height']
		db['coor_db']['pages'][page_no]['up']['tk'] = pixels2tk(db['coor_db']['widget'],db['coor_db']['pages'][page_no]['up']['pix']['x'],db['coor_db']['pages'][page_no]['up']['pix']['y'])
		db['coor_db']['pages'][page_no]['down']['tk'] = pixels2tk(db['coor_db']['widget'],db['coor_db']['pages'][page_no]['down']['pix']['x'],db['coor_db']['pages'][page_no]['down']['pix']['y'])
		db['coor_db']['pages'][page_no]['up']['pos'] = tk2pos(db['db_page'],db['coor_db']['pages'][page_no]['up']['tk'],Even=False)
		db['coor_db']['pages'][page_no]['down']['pos'] = tk2pos(db['db_page'],db['coor_db']['pages'][page_no]['down']['tk'],Even=True)
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pix']['x']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pix']['x']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pix']['y']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pix']['y']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pix']['x']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pix']['x']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pix']['y']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pix']['y']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['tk']: %s" % (page_no,db['coor_db']['pages'][page_no]['up']['tk']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['tk']: %s" % (page_no,db['coor_db']['pages'][page_no]['down']['tk']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pos']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pos']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pos']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pos']))

# Вернуть число страниц (видимых областей) в статье
def get_coor_pages(widget):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['coor_db'] = {}
		db['coor_db']['widget'] = widget
		db['coor_db']['widget'].update_idletasks()
		db['coor_db']['width']=db['coor_db']['widget'].winfo_width()
		db['coor_db']['height']=db['coor_db']['widget'].winfo_height()
		if db['coor_db']['height'] > globs['int']['pixel_hack']:
			db['coor_db']['height'] -= globs['int']['pixel_hack']
		if db['coor_db']['width'] > globs['int']['pixel_hack']:
			db['coor_db']['width'] -= globs['int']['pixel_hack']
		log(cur_func,lev_debug,"db['coor_db']['width']: %d" % db['coor_db']['width'])
		log(cur_func,lev_debug,"db['coor_db']['height']: %d" % db['coor_db']['height'])
		db['coor_db']['pages'] = {}
		page_no = 0
		next_page_pos = 0
		prev_tk = '1.0'
		next_page_tk = '1.0'
		widget.yview('1.0')
		while next_page_pos < db['db_page']['len']:
			get_page_coor(page_no)
			next_page_pos = db['coor_db']['pages'][page_no]['down']['pos'] + 1
			if next_page_pos > db['db_page']['len'] - 1:
				break
			else:
				next_page_tk = pos2tk(db['db_page'],next_page_pos,Even=True)
				# В некоторых случаях, несмотря на + 1 в номере символа, его позиция по Tk не меняется, и можно войти в бесконечный цикл.
				while next_page_tk == prev_tk and next_page_pos < db['db_page']['len']-1:
					next_page_pos += 1
					next_page_tk = pos2tk(db['db_page'],next_page_pos,Even=True)
				log(cur_func,lev_debug,'next_page_tk: %s' % next_page_tk)
				if next_page_tk == prev_tk or next_page_pos >= db['db_page']['len'] - 1:
					break
				else:
					widget.yview(next_page_tk)
					page_no += 1
					prev_tk = next_page_tk
		widget.yview('1.0')
		db['coor_db']['pages']['num'] = page_no+1
		if db['mode'] != 'skip':
			db['coor_db']['cur_page_no'] = 0
		db['coor_db']['direction'] = 'right_down'
		log(cur_func,lev_debug,"db['coor_db']['pages']['num']: %d" % db['coor_db']['pages']['num'])
	
# По позиции символа определить ближайший термин слева или справа
def get_adjacent_term(det,direction='right_down'):
	cur_func = sys._getframe().f_code.co_name
	term_num = - 1
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		term = ''
		if direction == 'right_down':
			for i in range(db['terms']['num']):
				if det <= db['terms']['pos'][i][0] or det <= db['terms']['pos'][i][1]:
					term_num = i
					term = db['terms']['phrases'][term_num]
					break
			log(cur_func,lev_debug,globs['mes'].right_term % (term_num,term))
		elif direction == 'left_up':
			i = db['terms']['num'] - 1
			while i >= 0:
				if det >= db['terms']['pos'][i][0] or det >= db['terms']['pos'][i][1]:
					term_num = i
					term = db['terms']['phrases'][term_num]
					break
				i -= 1
			log(cur_func,lev_debug,globs['mes'].left_term % (term_num,term))
	return term_num

# Загрузить картинку кнопки
# top.wm_iconbitmap поддерживает только черно - белый XBM. Через PhotoImage удается загрузить только GIF.
def load_icon(icon_path,parent_widget,width=None,height=None,Silent=False,Critical=True):
	cur_func = sys._getframe().f_code.co_name
	button_img = None
	check_type(cur_func,icon_path,globs['mes'].type_str)
	exist(icon_path,Silent=Silent,Critical=Critical)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if empty(width):
			width = globs['int']['default_button_size']
		if empty(height):
			height = globs['int']['default_button_size']
		try:
			# Нужно указывать виджет: http://stackoverflow.com/questions/23224574/tkinter - create - image - function - error - pyimage1 - does - not - exist
			button_img = tk.PhotoImage(file=icon_path,master=parent_widget,width=width,height=height) # Без 'file=' не сработает!
		except tk.TclError:
			mestype(cur_func,globs['mes'].button_load_failed % icon_path,Silent=Silent,Critical=Critical)
	return button_img
	
# Привязать горячие клавиши или кнопки мыши к действию
def create_binding(widget,bindings,action): # widget, list, function
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		bindings_type = get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
		if bindings_type == globs['mes'].type_str or bindings_type == globs['mes'].type_lst:
			if bindings_type == globs['mes'].type_str:
				bindings = [bindings]
			for i in range(len(bindings)):
				try:
					widget.bind(bindings[i],action)
				except tk.TclError:
					Warning(cur_func,globs['mes'].wrong_keybinding % bindings[i])
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))
		
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Всплывающие подсказки для кнопок
# see also 'calltips'
# based on idlelib.ToolTip
class ToolTipBase:
	def __init__(self,button):
		self.button = button
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
		self._id1 = self.button.bind("<Enter>", self.enter)
		self._id2 = self.button.bind("<Leave>", self.leave)
		self._id3 = self.button.bind("<ButtonPress>", self.leave)
	#----------------------------------------------------------------------
	def enter(self, event=None):
		self.schedule()
	#----------------------------------------------------------------------
	def leave(self, event=None):
		self.unschedule()
		self.hidetip()
	#----------------------------------------------------------------------
	def schedule(self):
		self.unschedule()
		self.id = self.button.after(self.hint_delay, self.showtip)
	#----------------------------------------------------------------------
	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)
	#----------------------------------------------------------------------
	def showtip(self):
		cur_func = sys._getframe().f_code.co_name
		if not 'geom_top' in globs or not 'width' in globs['geom_top'] or not 'height' in globs['geom_top']:
			ErrorMessage(cur_func,globs['mes'].not_enough_input_data)
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if self.tipwindow:
				return
			# The tip window must be completely outside the button; otherwise when the mouse enters the tip window we get a leave event and it disappears, and then we get an enter event and it reappears, and so on forever :-(
			# Координаты подсказки рассчитываются так, чтобы по горизонтали подсказка и кнопка, несмотря на разные размеры, совпадали бы центрами.
			x = self.button.winfo_rootx() + self.button.winfo_width()/2 - self.hint_width/2
			if self.hint_direction == 'bottom':
				y = self.button.winfo_rooty() + self.button.winfo_height() + 1
			elif self.hint_direction == 'top':
				y = self.button.winfo_rooty() - self.hint_height - 1
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(self.hint_direction),'top, bottom'))
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Позиция подсказки корректируется так, чтобы не выходить за пределы экрана
				if x + self.hint_width > globs['geom_top']['width']:
					log(cur_func,lev_info,globs['mes'].wrong_coor % ('x',str(x),str(globs['top']['width'] - self.hint_width)))
					x = globs['geom_top']['width'] - self.hint_width
				if y + self.hint_height > globs['top']['height']:
					log(cur_func,lev_info,globs['mes'].wrong_coor % ('y',str(y),str(globs['top']['height'] - self.hint_height)))
					y = globs['geom_top']['height'] - self.hint_height
				if x < 0:
					log(cur_func,lev_warn,globs['mes'].wrong_coor % ('x',str(x),'0'))
					x = 0
				if y < 0:
					log(cur_func,lev_warn,globs['mes'].wrong_coor % ('y',str(y),'0'))
					y = 0
				self.tipwindow = tw = tk.Toplevel(self.button)
				tw.wm_overrideredirect(1)
				# " + %d + %d" недостаточно!
				log(cur_func,lev_info,globs['mes'].new_geometry % ('tw',self.hint_width,self.hint_height,x,y))
				tw.wm_geometry("%dx%d+%d+%d" % (self.hint_width,self.hint_height,x, y))
				self.showcontents()
	#----------------------------------------------------------------------
	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

class ToolTip(ToolTipBase):
	def __init__(self,button,text='Sample text',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,button_side='left'):
		if empty(hint_delay):
			hint_delay = globs['int']['default_hint_delay']
		if empty(hint_width):
			hint_width = globs['int']['default_hint_width']
		if empty(hint_height):
			hint_height = globs['int']['default_hint_height']
		if empty(hint_background):
			hint_background = globs['var']['default_hint_background']
		if empty(hint_direction):
			hint_direction = globs['var']['default_hint_direction']
		if empty(hint_border_width):
			hint_border_width = globs['int']['default_hint_border_width']
		if empty(hint_border_color):
			hint_border_color = globs['var']['default_hint_border_color']
		self.text = text
		self.hint_delay = hint_delay
		self.hint_direction = hint_direction
		self.hint_background = hint_background
		self.hint_border_color = hint_border_color
		self.hint_height = hint_height
		self.hint_width = hint_width
		self.hint_border_width = hint_border_width
		self.button_side = button_side
		ToolTipBase.__init__(self,button)
	#----------------------------------------------------------------------
	def showcontents(self):
		frame=tk.Frame(self.tipwindow,background=self.hint_border_color,borderwidth=self.hint_border_width)
		frame.pack()
		label=tk.Label(frame,text=self.text,justify='center',background=self.hint_background,width=self.hint_width,height=self.hint_height)
		label.pack() #expand=1,fill='x'
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Создать кнопку с различными параметрами
# expand = 1 - увеличить расстояние между кнопками
# Моментальная упаковка не поддерживается, потому что это действие возвращает вместо виджета None, а мы проводим далее над виджетом другие операции
def create_button(parent_widget,text,hint,action,expand=0,side='left',fg='black',Silent=False,Critical=True,width=None,height=None,bd=0,icon_path='',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,bindings=[]):
	# side: must be 'top, 'bottom', 'left' or 'right'
	cur_func = sys._getframe().f_code.co_name
	button = None
	Success = True # Кнопку удалось инициализировать и упаковать; неудачные привязки не учитываются
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		bindings_type=get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
		if bindings_type == globs['mes'].type_str or bindings_type == globs['mes'].type_lst:
			if bindings_type == globs['mes'].type_str:
				bindings = [bindings]
			if empty(width):
				width = globs['int']['default_button_size']
			if empty(height):
				height = globs['int']['default_button_size']
			if empty(hint_delay):
				hint_delay = globs['int']['default_hint_delay']
			if empty(hint_width):
				hint_width = globs['int']['default_hint_width']
			if empty(hint_height):
				hint_height = globs['int']['default_hint_height']
			if empty(hint_background):
				hint_background = globs['var']['default_hint_background']
			if empty(hint_direction):
				hint_direction = globs['var']['default_hint_direction']
			if empty(hint_border_width):
				hint_border_width = globs['int']['default_hint_border_width']
			if empty(hint_border_color):
				hint_border_color = globs['var']['default_hint_border_color']
			if not empty(bindings):
				# Наличие элемента #0 должно гарантироваться в empty
				hint_expand = dlb + bindings[0].replace('<','').replace('>','')
				i = 1
				while i < len(bindings):
					hint_expand+=', '+bindings[i].replace('<','').replace('>','')
					i += 1
				hint += hint_expand
			try:
				if empty(icon_path) or globs['bool']['TextButtons']:
					button = tk.Button(parent_widget,text=text,fg=fg)
				else:
					button_img = load_icon(icon_path=icon_path,parent_widget=parent_widget,width=width,height=height,Silent=Silent,Critical=Critical)
					button = tk.Button(parent_widget,image=button_img,width=width,height=height,bd=bd)
					button.flag_img = button_img
			except tk.TclError:
				Success = False
				if Critical:
					globs['AbortAll'] = True
			try:
				button.pack(expand=expand,side=side)
			# tk.TclError, AttributeError
			except:
				Success = False
				if Critical:
					globs['AbortAll'] = True
			create_binding(widget=button,bindings=['<Return>','<KP_Enter>','<space>','<ButtonRelease-1>'],action=action)
			if Success:
				ToolTip(button,text=hint,hint_delay=hint_delay,hint_width=hint_width,hint_height=hint_height,hint_background=hint_background,hint_direction=hint_direction,button_side=side)
			log(cur_func,lev_debug,str(Success))
			if not Success:
				mestype(cur_func,globs['mes'].button_create_failed % text,Silent=Silent,Critical=Critical)
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))
	return button

# Свернуть заданное окно
def iconify(widget=root):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		widget.iconify()

# Определить номера терминов, которые являются пограничными для видимой области
def aggregate_pages():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		for i in range(db['coor_db']['pages']['num']):
			db['coor_db']['pages'][i]['up']['num'] = get_adjacent_term(db['coor_db']['pages'][i]['up']['pos'],direction='right_down')
			db['coor_db']['pages'][i]['down']['num'] = get_adjacent_term(db['coor_db']['pages'][i]['down']['pos'],direction='left_up')
			if db['terms']['num'] > 0:
				log(cur_func,lev_debug,globs['mes'].db_pages_stat % (i,db['coor_db']['pages'][i]['up']['num'],db['terms']['phrases'][db['coor_db']['pages'][i]['up']['num']],db['coor_db']['pages'][i]['down']['num'],db['terms']['phrases'][db['coor_db']['pages'][i]['down']['num']]))
	
def quit_now(*args):
	root.destroy()
	sys.exit()
	
# Пополнить историю и обновить виджет
def add_history():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if db['mode'] != 'skip' and not empty(db['search']):
			if globs['bool']['ShortHistory']:
				if not db['search'] in db['history']:
					db['history'].append(db['search'])
					log(cur_func,lev_info,globs['mes'].adding % str(db['search']))
					db['history_url'].append(db['url'])
					log(cur_func,lev_info,globs['mes'].adding % str(db['url']))
					if 'listbox' in globs and len(db['history']) > 0:
						globs['listbox'].insert(0,db['history'][-1])
			else:
				db['history'].append(db['search'])
				log(cur_func,lev_info,globs['mes'].adding % str(db['search']))
				db['history_url'].append(db['url'])
				log(cur_func,lev_info,globs['mes'].adding % str(db['url']))
				if 'listbox' in globs and len(db['history']) > 0:
					globs['listbox'].insert(0,db['history'][-1])
			db['history_index'] = len(db['history']) - 1

# Отобразить окно со словарной статьей
class ShowArticle:
	cur_func = sys._getframe().f_code.co_name
	# Инициализация
	def first_run(self):
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			globs['top'] = tk.Toplevel(root)
			root.withdraw()
			if globs['bool']['AlwaysMaximize']:
				if sys_type == 'lin':
					globs['top'].wm_attributes('-zoomed',True)
				# Win, Mac
				else:
					globs['top'].wm_state(newstate='zoomed')
			else:
				globs['top'].geometry(globs['var']['window_size'])
			# Назначение заголовка окна (первичное). В __init__ это происходит единожды, поэтому далее мы отдельно вызываем данную процедуру при каждой загрузке статьи.
			self.update_title()
			# Only black-and-white icons of XBM format
			#globs['top'].wm_iconbitmap(bitmap='@'+globs['var']['icon_mclient'])
			# Иконку надо определять здесь, поскольку запуск может быть не Standalone
			globs['top'].tk.call('wm','iconphoto',globs['top']._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
			globs['top'].protocol("WM_DELETE_WINDOW",quit_now)
			# tmp
			globs['top'].update_idletasks()
			globs['geom_top']['width'] = globs['top'].winfo_width()
			globs['geom_top']['height'] = globs['top'].winfo_height()
			log(cur_func,lev_info,globs['mes'].widget_sizes % ('top',globs['geom_top']['width'],globs['geom_top']['height']))
			root.protocol("WM_DELETE_WINDOW",quit_now)
			self.create_frame_history()
			self.web_frame = tk.Frame(globs['top'])
			self.web_frame.pack(expand=1,fill='both')
			globs['web_widget'] = create_web_widget(self.web_frame)
			set_page()
			self.create_frame_panel()
			globs['top'].wait_window()
	#--------------------------------------------------------------------------
	# Создание каркаса с предыдущими поисковыми запросами
	def create_frame_history(self):
		self.frame_history = tk.Frame(globs['top'])
		if db['ShowHistory'] == True:
			self.frame_history.pack(expand=0,side='left',fill='both')
		# Предыдущие поисковые запросы
		self.listbox = tk.Listbox(self.frame_history,font=globs['var']['font_history'])
		if db['ShowHistory'] == True:
			self.listbox.pack(expand=1,side='top',fill='both')
		for i in range(len(db['history'])):
			self.listbox.insert(0,db['history'][i])
		globs['listbox'] = self.listbox
		globs['frame_history'] = self.frame_history
	#--------------------------------------------------------------------------
	# Создание каркаса с полем ввода, кнопкой выбора направления перевода и кнопкой выхода
	def create_frame_panel(self):
		self.frame_panel = tk.Frame(globs['top'])
		self.frame_panel.pack(expand=0,fill='x',side='bottom')
		# Поле ввода поисковой строки
		self.search_field = tk.Entry(self.frame_panel)
		if globs['bool']['TextButtons']:
			self.search_field.pack(side='left')
		else:
			# Подгоняем высоту поисковой строки под высоту графических кнопок; значение 5 подобрано опытным путем
			self.search_field.pack(side='left',ipady=5)
		# Для перевода в области терминов используем кнопки мыши, но не альтернативные комбинации клавиш, поскольку предполагаются, что они для удобства совпадают с комбинациями клавиш для перевода в области поиска.
		self.search_field.focus_force()
		self.draw_buttons()
		self.hotkeys()
		globs['frame_panel'] = self.frame_panel
	#--------------------------------------------------------------------------
	# Обновить заголовок окна
	def update_title(self):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if 'top' in globs:
				if globs['bool']['mclientSaveTitle']:
					globs['top'].title(globs['mes'].mclient % __version__)
				else:
					if db['FirstLaunch']:
						globs['top'].title(globs['mes'].mclient % __version__)
					else:
						globs['top'].title(db['search'])
	#--------------------------------------------------------------------------
	# Вставить предыдущий запрос
	def insert_repeat_sign(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['history']) > 0:
				clipboard_copy(db['history'][-1])
				self.paste_search_field(None)
	#--------------------------------------------------------------------------
	# Вставить запрос до предыдущего
	def insert_repeat_sign2(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['history']) > 1:
				clipboard_copy(db['history'][-2])
				self.paste_search_field(None)
	#--------------------------------------------------------------------------
	# Search the selected term online using the entry widget (search field)
	def go_search(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			search_str = self.search_field.get().strip(dlb).strip(' ')
			# Allows to use the same hotkeys for the search field and the article field
			if search_str == '':
				globs['web_widget'].go_url(event)
			else:
				db['search'] = search_str
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
				get_url()
				db['mode'] = 'url'
				# Скопировать предпоследний запрос в буфер и вставить его в строку поиска (например, для перехода на этот запрос еще раз)
				if db['search'] == globs['var']['repeat_sign2']:
					self.insert_repeat_sign2(event)
				# Скопировать последний запрос в буфер и вставить его в строку поиска (например, для корректировки)
				elif db['search'] == globs['var']['repeat_sign']:
					self.insert_repeat_sign(event)
				else:
					self.clear_search_field(event)
					loop_page()
					self.update_title()
	#--------------------------------------------------------------------------
	# Задействование колеса мыши для пролистывания экрана
	def mouse_wheel(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# В Windows XP delta == - 120, однако, в других версиях оно другое
			if event.num == 5 or event.delta < 0:
				self.move_page_down(event)
			# В Windows XP delta == 120, однако, в других версиях оно другое
			if event.num == 4 or event.delta > 0:
				self.move_page_up(event)
			return 'break'
	#----------------------------------------------------------------------
	# todo
	# Рассчитать координаты ползунка в зависимости от числа страниц
	def scrollbar_poses(self):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			delim = 1/db['coor_db']['pages']['num']
			# Минимальный шаг, который разграничивает координаты 2 соседних экранов
			step = 0.000000001
			last_val = 0
			db['scroll_poses'] = []
			for i in range(db['coor_db']['pages']['num']):
				if i == 0:
					db['scroll_poses'] += [[last_val,last_val+delim]]
				else:
					db['scroll_poses'] += [[last_val+step,last_val+delim]]
				last_val += delim
			log(cur_func,lev_debug,str(db['scroll_poses']))
			assert len(db['scroll_poses']) == db['coor_db']['pages']['num']
	#----------------------------------------------------------------------
	# todo
	# Вернуть номер страницы в зависимости от координат ползунка
	def detect_page(self,mode='coor'): # 'coor', 'term_no'
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# Инициализируем i, иначе при i = 0 далее возникнет ошибка присваивания
			i = 0
			if mode == 'coor':
				for i in range(db['coor_db']['pages']['num']):
					if db['cur_scroll_pos'] >= db['scroll_poses'][i][0] and db['cur_scroll_pos'] <= db['scroll_poses'][i][1]:
						break
			elif mode == 'term_no':
				for i in range(db['coor_db']['pages']['num']):
					if res[0] >= db['coor_db']['pages'][i]['up']['num'] and res[0] <= db['coor_db']['pages'][i]['down']['num']:
						break
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'coor, term_no'))
			db['coor_db']['cur_page_no'] = i
			log(cur_func,lev_debug,str(db['coor_db']['cur_page_no']))
	#----------------------------------------------------------------------
	# todo
	# Задействование ползунка
	def custom_scroll(self,*args):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# Если сдвигается сам ползунок, то Tkinter передаст 2 параметра: 'moveto' и offset (оба имеющие тип 'строка', однако, второй параметр на самом деле float).
			# Если же используются стрелки ползунка, то 1-м параметром будет 'scroll', а 2-м - '1' (направление вниз) или '-1' (направление вверх).
			def add_page(self):
				cur_func = sys._getframe().f_code.co_name
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					if db['coor_db']['cur_page_no'] < db['coor_db']['pages']['num']-1:
						log(cur_func,lev_info,"db['coor_db']['cur_page_no']: %d -> %d" % (db['coor_db']['cur_page_no'],db['coor_db']['cur_page_no']+1))
						db['coor_db']['cur_page_no'] += 1
			def subtract_page(self):
				cur_func = sys._getframe().f_code.co_name
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					if db['coor_db']['cur_page_no'] > 0:
						log(cur_func,lev_info,"db['coor_db']['cur_page_no']: %d -> %d" % (db['coor_db']['cur_page_no'],db['coor_db']['cur_page_no']-1))
						db['coor_db']['cur_page_no'] -= 1
			action = args[0]
			log(cur_func,lev_info,globs['mes'].action % action)
			offset = self.scrollbar.get()[0]
			if offset < 0:
				offset = 0
			elif offset > 1:
				offset = 1
			log(cur_func,lev_info,globs['mes'].scrollbar_pos % str(offset))
			if not 'prev_scroll_pos' in db:
				db['prev_scroll_pos'] = 0
				db['cur_scroll_pos'] = 0
				db['coor_db']['cur_page_no'] = 0
			db['prev_scroll_pos'] = db['cur_scroll_pos']
			db['cur_scroll_pos'] = offset
			log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
			log(cur_func,lev_info,"db['cur_scroll_pos']: %s" % str(db['cur_scroll_pos']))
			# Определяем текущую страницу
			self.detect_page()
			log(cur_func,lev_info,globs['mes'].cur_page_no % db['coor_db']['cur_page_no'])
			if action == 'scroll':
				offset = args[1]
				if offset == '1':
					self.add_page()
				elif offset == ' - 1':
					self.subtract_page()
				else:
					log(cur_func,lev_err,globs['mes'].unknown_args % (str(offset),'-1, 1'))
			elif action == 'moveto':
				if db['cur_scroll_pos'] < 0:
					log(cur_func,lev_info,globs['mes'].cor_scroll % (db['cur_scroll_pos'],0))
					db['cur_scroll_pos'] = 0
				elif db['cur_scroll_pos'] > 1:
					log(cur_func,lev_info,globs['mes'].cor_scroll % (db['cur_scroll_pos'],1))
					db['cur_scroll_pos'] = 1
				if db['cur_scroll_pos'] > db['prev_scroll_pos']:
					self.add_page()
				#elif db['cur_scroll_pos'] < db['prev_scroll_pos']:
				#	self.subtract_page()
				else:
					log(cur_func,lev_info,globs['mes'].scrollbar_still)
			else:
				Warning(cur_func,globs['mes'].unknown_args % (action,'scroll, move_to'))
			db['prev_scroll_pos'] = db['cur_scroll_pos']
			db['cur_scroll_pos'] = db['scroll_poses'][db['coor_db']['cur_page_no']][0]
			log(cur_func,lev_info,globs['mes'].new_values)
			log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
			log(cur_func,lev_info,"db['cur_scroll_pos']: %s" % str(db['cur_scroll_pos']))
			# Изменяем текущую страницу в соответствии с предыдущими корректировками
			self.detect_page()
			log(cur_func,lev_info,globs['mes'].cur_page_no % db['coor_db']['cur_page_no'])
			self.shift_screen(mode='still')
			db['cur_scroll_pos'] = db['scroll_poses'][db['coor_db']['cur_page_no']][0]
			scroll_pos1 = db['cur_scroll_pos']
			scroll_pos2 = db['scroll_poses'][db['coor_db']['cur_page_no']][1]
			if scroll_pos1 < 0:
				scroll_pos1 = 0
			elif scroll_pos1 > 1:
				scroll_pos1 = 1
			if scroll_pos2 < 0:
				scroll_pos2 = 0
			elif scroll_pos2 > 1:
				scroll_pos2 = 1
			self.scrollbar.set(scroll_pos1,scroll_pos2)
			self.select_term()
			db['prev_scroll_pos'] = db['cur_scroll_pos']
			log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
			return 'break'
	#----------------------------------------------------------------------
	# todo
	# Определить, входит ли текущий термин в видимую часть экрана
	def fits_screen(self):
		cur_func = sys._getframe().f_code.co_name
		# Вернуть True, если смещение экрана не требуется (ввиду названия функции)
		Success = True
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# Если терминов нет, то смещать экран бесполезно
			if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
				if not 'cur_page_no' in db['coor_db']:
					db['coor_db']['cur_page_no'] = 0
				if db['terms']['pos'][res[0]][0] >= db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['pos'] and db['terms']['pos'][res[0]][-1] <= db['coor_db']['pages'][db['coor_db']['cur_page_no']]['down']['pos']:
					pass
				else:
					Success = False
		return Success
	#----------------------------------------------------------------------
	# todo
	# Обеспечить удобное пролистывание экрана
	# mode='normal': смещать экран согласно fits_screen()
	# mode='change': изменить номер страницы даже в том случае, если текущий термин находится в видимой области (необходимо для move_page_up/_down)
	# mode='still': не изменять номер страницы (необходимо для move_page_start/_end)
	def shift_screen(self,mode='normal'):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			DragScreen = False
			# Вставляю проверку в самом начале, чтобы в случае ошибки не проводить дополнительные операции. Все равно если терминов нет, то смещать экран бесполезно
			if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
				if mode == 'normal':
					if self.fits_screen():
						DragScreen = False
					else:
						DragScreen = True
				elif mode == 'change':
					DragScreen = True
				elif mode == 'still':
					DragScreen = False
				else:
					ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'normal, change, still'))
				if DragScreen:
					log(cur_func,lev_info,globs['mes'].shift_screen_required)
					if db['coor_db']['direction'] == 'right_down':
						if db['coor_db']['cur_page_no'] < db['coor_db']['pages']['num']-1:
							db['coor_db']['cur_page_no'] += 1
					elif db['coor_db']['direction'] == 'left_up':
						if db['coor_db']['cur_page_no'] > 0:
							db['coor_db']['cur_page_no'] -= 1
					else:
						ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(db['coor_db']['direction']),'left_up, right_down'))
				else:
					log(cur_func,lev_info,globs['mes'].shift_screen_not_required)
				# Фактически, экран нужно смещать всегда
				yview_tk = db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['tk']
				# Смещение экрана до заданного термина
				# Алгоритм работает только, если метка называется 'insert'
				try:
					txt.mark_set('insert',yview_tk)
					txt.yview('insert')
					log(cur_func,lev_info,globs['mes'].shift_screen % ('insert',yview_tk))
				except:
					log(cur_func,lev_err,globs['mes'].shift_screen_failure % 'insert')
	#--------------------------------------------------------------------------
	# Перейти на 1 - й термин текущей строки	
	def move_line_start(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# Перейти на последний термин текущей строки
	def move_line_end(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# Перейти на 1 - й термин статьи
	def move_text_start(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			assign_cur_cell(db['move_start'])
			globs['web_widget'].set_cell()
	#--------------------------------------------------------------------------
	# Перейти на последний термин статьи
	def move_text_end(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# Можно также брать db['move_down'][-1]
			assign_cur_cell(db['move_end'])
			globs['web_widget'].set_cell()
	#--------------------------------------------------------------------------
	# todo
	# Перейти на страницу вверх
	def move_page_up(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# todo
	# Перейти на страницу вверх
	def move_page_down(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# todo
	# Перейти на 1 - й термин текущей страницы
	def move_page_start(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# todo
	# Перейти на последний термин текущей страницы
	def move_page_end(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# Перейти на предыдущий термин
	def move_left(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['move_left']) > db['cur_cell']['i'] and len(db['move_left'][db['cur_cell']['i']]) > db['cur_cell']['j']:
				assign_cur_cell(db['move_left'][db['cur_cell']['i']][db['cur_cell']['j']])
				globs['web_widget'].set_cell()
			else:
				log(cur_func,lev_err,globs['mes'].wrong_input2)
	#--------------------------------------------------------------------------
	# Перейти на следующий термин
	def move_right(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['move_right']) > db['cur_cell']['i'] and len(db['move_right'][db['cur_cell']['i']]) > db['cur_cell']['j']:
				assign_cur_cell(db['move_right'][db['cur_cell']['i']][db['cur_cell']['j']])
				globs['web_widget'].set_cell()
			else:
				log(cur_func,lev_err,globs['mes'].wrong_input2)
	#--------------------------------------------------------------------------
	# Перейти на строку вниз
	def move_down(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['move_down']) > db['cur_cell']['i'] and len(db['move_down'][db['cur_cell']['i']]) > db['cur_cell']['j']:
				assign_cur_cell(db['move_down'][db['cur_cell']['i']][db['cur_cell']['j']])
				globs['web_widget'].set_cell()
			else:
				log(cur_func,lev_err,globs['mes'].wrong_input2)
	#--------------------------------------------------------------------------
	# Перейти на строку вверх
	def move_up(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			pass
	#--------------------------------------------------------------------------
	# Изменить направление (язык) перевода
	def change_pair(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			try:
				selected_pair = self.var.get()
			except:
				log(cur_func,lev_err,globs['mes'].lang_pair_undefined)
				selected_pair = globs['cur_pair']
			log(cur_func,lev_debug,globs['mes'].got_value % str(selected_pair))
			Found = False
			for i in range(len(pairs)):
				if selected_pair == pairs[i]:
					Found = True
					break
			if Found:
				globs['var']['online_dic_url'] = online_dic_urls[i]
			log(cur_func,lev_info,globs['mes'].lang_pair % selected_pair)
			log(cur_func,lev_debug,'URL: %s' % globs['var']['online_dic_url'])
			globs['cur_pair'] = selected_pair
	#--------------------------------------------------------------------------
	# Отобразить/скрыть историю запросов онлайн
	def toggle_history(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if db['ShowHistory']:
				db['ShowHistory'] = False
				if 'frame_history' in globs and 'listbox' in globs:
					globs['listbox'].pack_forget()
					globs['frame_history'].pack_forget()
			else:
				db['ShowHistory'] = True
				if 'frame_history' in globs and 'listbox' in globs:
					globs['frame_history'].pack(expand=1,side='top',fill='both')
					globs['listbox'].pack(expand=1,side='top',fill='both')
					#globs['listbox'].pack(expand=1,side='top',fill='both')
			#db['mode'] = 'skip'
			# Запоминаем позицию выделения, чтобы она не сбрасывалась при переключении отображения Истории. Запомнить позицию выделения можно только на первой странице.
			# todo
			#db['last_cell'] = db['cur_cell']
			#loop_page()
	#--------------------------------------------------------------------------
	# Написать письмо автору
	def response_back(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			try:
				webbrowser.open('mailto:%s' % my_email)
			except:
				Warning(cur_func,globs['mes'].email_agent_failure)
	#--------------------------------------------------------------------------
	# Скопировать номер кошелька
	def copy_wallet_no(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			clipboard_copy(my_yandex_money)
			InfoMessage(cur_func,globs['mes'].wallet_no_copied)
			root.withdraw()
	#--------------------------------------------------------------------------
	# Открыть веб-страницу с лицензией
	def open_license_url(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			try:
				webbrowser.open(globs['license_url'])
			except:
				Warning(cur_func,globs['mes'].browser_failure % globs['license_url'])
	#--------------------------------------------------------------------------
	# Окно "О программе"
	def show_about(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			about_top = tk.Toplevel(root)
			about_top.tk.call('wm','iconphoto',about_top._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
			about_top.title(globs['mes'].about)
			frame1 = tk.Frame(about_top)
			frame1.pack(expand=1,fill='both',side='top')
			frame2 = tk.Frame(about_top)
			frame2.pack(expand=1,fill='both',side='left')
			frame3 = tk.Frame(about_top)
			frame3.pack(expand=1,fill='both',side='right')
			if globs['bool']['ShowWallet']:
				label = tk.Label(frame1,font=globs['var']['font_style'],text=globs['mes'].about_text)
			else:
				label = tk.Label(frame1,font=globs['var']['font_style'],text=globs['mes'].about_text_no_wallet)
			label.pack()
			if globs['bool']['ShowWallet']:
				# Номер электронного кошелька
				create_button(parent_widget=frame2,text=globs['mes'].btn_wallet_no,hint=globs['mes'].hint_wallet_no,action=self.copy_wallet_no,side='left')
				# Лицензия
				create_button(parent_widget=frame3,text=globs['mes'].btn_license,hint=globs['mes'].hint_license,action=self.open_license_url,side='left')
			else:
				# Лицензия
				create_button(parent_widget=frame2,text=globs['mes'].btn_license,hint=globs['mes'].hint_license,action=self.open_license_url,side='left')
			# Отправить письмо автору
			create_button(parent_widget=frame3,text=globs['mes'].btn_email_author,hint=globs['mes'].hint_email_author,action=self.response_back,side='right')
			about_top.focus_set()
			about_top.wait_window()
	#--------------------------------------------------------------------------
	# Перейти на элемент истории
	def get_history(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			# При выборе пункта возвращается кортеж с номером пункта
			selection = self.listbox.curselection()
			# ВНИМАНИЕ: В Python 3.4 selection[0] является числом, в более старших интерпретаторах, а также в сборках на их основе - строкой. Для совместимости преобразуем в число.
			#db['search'] = self.listbox.get(selection[0])
			sel_no = len(db['history']) - int(selection[0]) - 1
			if sel_no < len(db['history']) and sel_no < len(db['history_url']):
				db['search'] = db['history'][sel_no]
				# Список истории запросов идет в обратном порядке, поэтому необходимо синхронизировать
				db['url'] = db['history_url'][sel_no]
				log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
				log(cur_func,lev_debug,globs['mes'].history_elem_selected % db['search'])
				db['mode'] = 'url'
				loop_page()
				if globs['bool']['AutoHideHistory']:
					self.toggle_history(None)
				# todo: Требуется ли это теперь?
				# Выносим в самый конец, чтобы нейтрализовать режим 'skip' в toggle_history()
				db['mode'] = 'url'
	#--------------------------------------------------------------------------
	# Скопировать элемент истории
	def copy_history(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			selection = err_mes_copy
			selection = self.listbox.get(self.listbox.curselection()[0])
			log(cur_func,lev_debug,globs['mes'].history_elem_selected % selection)
			clipboard_copy(selection)
			if globs['bool']['AutoHideHistory']:
				self.toggle_history(None)
	#--------------------------------------------------------------------------
	# Очистить Историю
	def clear_history(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if len(db['history']) > 0:
				i = len(db['history']) - 1
				while i >= 0:
					self.listbox.delete(i)
					i -= 1
			db['mode'] = 'skip'
			db['search'] = globs['mes'].welcome
			db['history'] = []
			db['history_url'] = []
			db['history_index'] = 0
			self.frame_panel.destroy()
			self.create_frame_panel()
	#--------------------------------------------------------------------------
	# Очистить строку поиска
	def clear_search_field(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.search_field.delete(0,'end')
	#--------------------------------------------------------------------------
	# Очистить строку поиска и вставить в нее содержимое буфера обмена
	def paste_search_field(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.search_field.delete(0,'end')
			self.search_field.selection_clear()
			self.search_field.insert(0,clipboard_paste())
			return 'break'
	#--------------------------------------------------------------------------
	# Следить за буфером обмена
	def watch_clipboard(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if db['TrackClipboard']:
				db['TrackClipboard'] = False
				db['mode'] = 'url'
			else:
				db['TrackClipboard'] = True
				db['mode'] = 'clipboard'
			globs['top'].iconify()
			loop_page()
			globs['top'].title(db['search'])
			globs['top'].deiconify()
	#--------------------------------------------------------------------------
	# Открыть URL текущей статьи в браузере
	def open_in_browser(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if not 'url' in db:
				if db['terms']['num'] > 0:
					db['url'] = db['terms']['url'][0]
				else:
					db['url'] = online_url_safe
				log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
			try:
				webbrowser.open(db['url'])
			except:
				Warning(cur_func,globs['mes'].browser_failure % db['url'])
	#--------------------------------------------------------------------------
	# Скопировать URL текущей статьи или выделения
	def copy_url(self,widget,mode='article'):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			cur_url = online_url_safe
			if mode == 'term':
				# Скопировать URL текущего термина. URL 1-го термина не совпадает с URL статьи!
				cur_url = db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['url']
				if db['Iconify']:
					iconify(widget=widget)
			elif mode == 'article':
				# Скопировать URL статьи
				cur_url = db['url']
				if db['Iconify']:
					iconify(widget=widget)
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'article, term'))
			log(cur_func,lev_debug,"cur_url: %s" % str(cur_url))
			clipboard_copy(cur_url)
	#--------------------------------------------------------------------------
	# Открыть веб-страницу с определением текущего термина
	def define(self,Selected=True): # Selected: True: Выделенный термин; False: Название статьи
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if Selected:
				browse_url(globs['var']['web_search_url'],'define:' + db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['term'])
			else:
				browse_url(globs['var']['web_search_url'],'define:'+db['search'])
	#--------------------------------------------------------------------------
	# Переключить язык интерфейса с русского на английский и наоборот
	def change_ui_lang(self,event):
		cur_func = sys._getframe().f_code.co_name
		# Если включить проверку, будем все время получать SyntaxWarning
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			toggle_ui_lang()
			self.frame_panel.destroy()
			self.create_frame_panel()
	#--------------------------------------------------------------------------
	# Перейти на предыдущий запрос
	def go_back(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if not 'history_index' in db:
				db['history_index'] = len(db['history'])
			if db['history_index'] > 0:
				db['history_index'] -= 1
				db['mode'] = 'url'
				db['search'] = db['history'][db['history_index']]
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
				db['url'] = db['history_url'][db['history_index']]
				log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
				loop_page(AddHistory=False)
	#--------------------------------------------------------------------------
	# Перейти на следующий запрос
	def go_forward(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if not 'history_index' in db:
				db['history_index'] = len(db['history'])
			if db['history_index'] < len(db['history']) - 1:
				db['history_index'] += 1
				db['mode'] = 'url'
				db['search'] = db['history'][db['history_index']]
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
				db['url'] = db['history_url'][db['history_index']]
				log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
				loop_page(AddHistory=False)
	#--------------------------------------------------------------------------
	# Найти слово/слова в статье
	def search_article(self,direction='forward'): # clear, forward, backward
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if direction == 'clear': # Начать поиск заново
				if 'search_list' in db:
					del db['search_list']
				direction = 'forward'
			elif direction != 'forward' and direction != 'backward':
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(direction),'clear, forward, backward'))
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Создаем начальные значения
				if not 'search_list' in db:
					search_str = text_field(title=globs['mes'].search_str,Small=True) #search_field.get()
					search_str = search_str.strip(' ').strip(dlb).lower()
					root.withdraw()
					if not empty(search_str):
						# Создать список позиций всех совпадений по поиску в статье
						db['search_list'] = []
						for i in range(len(db['cells'])):
							for j in range(len(db['cells'][0])):
								# todo: Для всех вхождений, а не только терминов
								if db['cells'][i][j]['selectable'] and search_str in db['cells'][i][j]['term'].lower():
									db['search_list'].append((i,j))
						if len(db['search_list']) > 0:
							if direction == 'forward':
								# Номер текущего выделенного совпадения ('search_article_pos') в списке совпадений ('search_list')
								db['search_article_pos'] = -1
							elif direction == 'backward':
								db['search_article_pos'] = len(db['search_list'])
				if 'search_list' in db:
					# Продолжаем поиск с предыдущего места
					if len(db['search_list']) > 0:
						if direction == 'forward':
							if db['search_article_pos'] + 1 < len(db['search_list']):
								db['search_article_pos'] += 1
							else:
								db['search_article_pos'] = 0
						elif direction == 'backward':
							if db['search_article_pos'] > 0:
								db['search_article_pos'] -= 1
							else:
								db['search_article_pos'] = len(db['search_list']) - 1
						assign_cur_cell(db['search_list'][db['search_article_pos']])
						globs['web_widget'].set_cell()
	#--------------------------------------------------------------------------
	# Сохранить статью на диск
	def save_article(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			opt = SelectFromList(globs['mes'].select_action,globs['mes'].actions,[globs['mes'].save_article_as_html,globs['mes'].save_article_as_txt,globs['mes'].copy_article_html,globs['mes'].copy_article_txt],Insist=False,Critical=False)
			if not empty(opt):
				if opt == globs['mes'].save_article_as_html:
					# Ключ 'html' может быть необходим для записи файла, которая производится в кодировке UTF-8, поэтому, чтобы полученная веб-страница нормально читалась, меняем кодировку вручную.
					# Также меняем сокращенные гиперссылки на полные, чтобы они работали и в локальном файле.
					dialog_save_file(db['html'].replace('charset=windows-1251"','charset=utf-8"').replace('<a href="m.exe?','<a href="'+online_url_root).replace('../c/m.exe?',online_url_root),filetypes=((globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*')),Critical=False)
				elif opt == globs['mes'].save_article_as_txt:
					dialog_save_file(db['plain_text'],filetypes=((globs['mes'].plain_text,'.txt'),(globs['mes'].all_files,'*')),Critical=False)
				elif opt == globs['mes'].copy_article_html:
					# Копирование веб - кода в буфер обмена полезно разве что в целях отладки, поэтому никак не меняем этот код.
					clipboard_copy(db['html'])
				elif opt == globs['mes'].copy_article_txt:
					clipboard_copy(db['plain_text'])
			root.withdraw()
	#--------------------------------------------------------------------------
	# Вставить спец. символ в строку поиска
	def insert_sym(self,sym):
		self.search_field.insert('end',sym)
		if globs['bool']['AutoCloseSpecSymbol']:
			self.symbols_top.destroy()
	def spec_symbol(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.symbols_top = tk.Toplevel(root)
			self.symbols_top.title(globs['mes'].paste_spec_symbol)
			btn_frame = tk.Frame(self.symbols_top)
			btn_frame.pack(expand=1)
			for i in range(len(globs['var']['spec_syms'])):
				if i % 10 == 0:
					btn_frame = tk.Frame(self.symbols_top)
					btn_frame.pack(expand=1)
				# lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
				# width и height нужны для Windows
				btn = tk.Button(btn_frame,text=globs['var']['spec_syms'][i],command=lambda i=i:self.insert_sym(globs['var']['spec_syms'][i]),width=2,height=2).pack(side='left',expand=1)
			# В Windows окно может оказаться на заднем плане
			self.symbols_top.focus_set()
			self.symbols_top.wait_window()
	#--------------------------------------------------------------------------
	# todo: Убрать режим 'close' (?)
	# Вернуть режим буфера обмена при закрытии окна спец. комбинацией или при копировании в буфер. В других случаях режим буфер не удастся отличить от других режимов даже при наличии спец. флага.
	# Нельзя присваивать комбинации по типу (...,action=toggle_clipboard_mode), поскольку в этом случае эта процедура примет event за mode
	def toggle_clipboard_mode(self,mode='close'): # close, copy
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if db['TrackClipboard']:
				db['mode'] = 'clipboard'
				loop_page()
			elif mode == 'close':
				loop_page()
			elif mode == 'copy':
				if db['Iconify']:
					iconify(widget = top)
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'close, copy'))
	#--------------------------------------------------------------------------
	# Временно включить или отключить сворачивание окна при операциях копирования
	def toggle_iconify(self,event):
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if db['Iconify']:
				db['Iconify'] = False
			else:
				db['Iconify'] = True
	#--------------------------------------------------------------------------
	# Создать кнопки
	def draw_buttons(self):
		# Кнопка для "чайников", заменяет Enter в search_field
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_translate,hint=globs['mes'].btn_translate,action=self.go_search,icon_path=globs['var']['icon_go_search'],bindings=[globs['var']['bind_go_search'],globs['var']['bind_go_search_alt']]) # В данном случае btn = hint
		# Если кнопки только текстовые, то все они не поместятся на экране, поэтому в текстовом режиме вспомогательные кнопки можно скрыть
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка очистки строки поиска
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_clear,hint=globs['mes'].hint_clear_search_field,action=self.clear_search_field,icon_path=globs['var']['icon_clear_search_field'],bindings=[globs['var']['bind_clear_search_field']])
			# Вспомогательная кнопка вставки
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_paste,hint=globs['mes'].hint_paste_clipboard,action=self.paste_search_field,icon_path=globs['var']['icon_paste'],bindings=['<Control-v>'])
			# Вспомогательная кнопка вставки текущего запроса
			if 'history' in db and len(db['history']) > 0:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_repeat_sign,hint=globs['mes'].hint_paste_cur_request,action=self.insert_repeat_sign,icon_path=globs['var']['icon_repeat_sign'],bindings=globs['var']['repeat_sign'])
			else:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_repeat_sign,hint=globs['mes'].hint_paste_cur_request,action=self.insert_repeat_sign,icon_path=globs['var']['icon_repeat_sign_off'],bindings=globs['var']['repeat_sign'])
			# Вспомогательная кнопка вставки предыдущего запроса
			if 'history' in db and len(db['history']) > 1:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_repeat_sign2,hint=globs['mes'].hint_paste_prev_request,action=self.insert_repeat_sign2,icon_path=globs['var']['icon_repeat_sign2'],bindings=globs['var']['repeat_sign2'])
			else:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_repeat_sign2,hint=globs['mes'].hint_paste_prev_request,action=self.insert_repeat_sign2,icon_path=globs['var']['icon_repeat_sign2_off'],bindings=globs['var']['repeat_sign2'])
		# Кнопка для вставки спец. символов
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_symbols,hint=globs['mes'].hint_symbols,action=self.spec_symbol,icon_path=globs['var']['icon_spec_symbol'],bindings=globs['var']['bind_spec_symbol'])
		# Выпадающий список с вариантами направлений перевода
		self.var = tk.StringVar(globs['top'])
		self.var.set(globs['cur_pair'])
		self.option_menu = tk.OptionMenu(self.frame_panel,self.var,*pairs,command=self.change_pair).pack(side='left',anchor='center')
		# Выпадающий список для вставки спец. символов
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка перехода на предыдущую статью
			if 'history_index' in db and 'history' in db and db['history_index'] > 0:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_prev,hint=globs['mes'].hint_preceding_article,action=self.go_back,icon_path=globs['var']['icon_go_back'],bindings=globs['var']['bind_go_back'])
			else:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_prev,hint=globs['mes'].hint_preceding_article,action=self.go_back,icon_path=globs['var']['icon_go_back_off'],bindings=globs['var']['bind_go_back'])
			# Вспомогательная кнопка перехода на следующую статью
			if 'history_index' in db and db['history_index'] < len(db['history']) - 1:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_next,hint=globs['mes'].hint_following_article,action=self.go_forward,icon_path=globs['var']['icon_go_forward'],bindings=globs['var']['bind_go_forward'])
			else:
				create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_next,hint=globs['mes'].hint_following_article,action=self.go_forward,icon_path=globs['var']['icon_go_forward_off'],bindings=globs['var']['bind_go_forward'])
		# Кнопка включения/отключения истории
		self.button = create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_history,hint=globs['mes'].hint_history,action=self.toggle_history,icon_path=globs['var']['icon_toggle_history'],bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history_alt']])
		create_binding(widget=self.button,bindings=globs['var']['bind_clear_history'],action=self.clear_history)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_clear_history_alt'],action=self.clear_history)
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка очистки истории
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_clear_history,hint=globs['mes'].hint_clear_history,action=self.clear_history,icon_path=globs['var']['icon_clear_history'],bindings=globs['var']['bind_clear_history_alt'])
			# Вспомогательная кнопка перезагрузки статьи
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_reload,hint=globs['mes'].hint_reload_article,action=loop_page,icon_path=globs['var']['icon_reload'],bindings=[globs['var']['bind_reload_article'],globs['var']['bind_reload_article_alt']])
		# Кнопка "Поиск в статье"
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_search,hint=globs['mes'].hint_search_article,action=lambda e:self.search_article(direction='clear'),icon_path=globs['var']['icon_search_article'],bindings=globs['var']['bind_re_search_article'])
		# Кнопка "Сохранить"
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_save,hint=globs['mes'].hint_save_article,action=self.save_article,icon_path=globs['var']['icon_save_article'],bindings=[globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']])
		# Кнопка "Открыть в браузере"
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_in_browser,hint=globs['mes'].hint_in_browser,action=self.open_in_browser,icon_path=globs['var']['icon_open_in_browser'],bindings=[globs['var']['bind_open_in_browser'],globs['var']['bind_open_in_browser_alt']])
		if globs['bool']['UseOptionalButtons']:
			# Кнопка толкования термина. Сделана вспомогательной ввиду нехватки места
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_define,hint=globs['mes'].hint_define,action=lambda x:self.define(Selected=False),icon_path=globs['var']['icon_define'],bindings=globs['var']['bind_define'])
		# Кнопка "Буфер обмена"
		if 'TrackClipboard' in db and db['TrackClipboard']:
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_clipboard,hint=globs['mes'].hint_watch_clipboard,action=self.watch_clipboard,icon_path=globs['var']['icon_watch_clipboard_on'],fg='red',bindings=[globs['var']['bind_watch_clipboard'],globs['var']['bind_watch_clipboard_alt']])
		else:
			create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_clipboard,hint=globs['mes'].hint_watch_clipboard,action=self.watch_clipboard,icon_path=globs['var']['icon_watch_clipboard_off'],bindings=[globs['var']['bind_watch_clipboard'],globs['var']['bind_watch_clipboard_alt']])
		# Кнопка переключения языка интерфейса
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_ui_lang,hint=globs['mes'].hint_ui_lang,action=self.change_ui_lang,icon_path=globs['var']['icon_change_ui_lang'])
		# Кнопка "О программе"
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_about,hint=globs['mes'].hint_about,action=self.show_about,icon_path=globs['var']['icon_show_about'],bindings=globs['var']['bind_show_about'])
		# Кнопка выхода
		create_button(parent_widget=self.frame_panel,text=globs['mes'].btn_x,hint=globs['mes'].hint_x,action=quit_now,icon_path=globs['var']['icon_quit_now'],side='right',bindings=[globs['var']['bind_quit_now'],globs['var']['bind_quit_now_alt']])
		#----------------------------------------------------------------------
	def hotkeys(self):
		# Привязки: горячие клавиши и кнопки мыши
		create_binding(widget=self.listbox,bindings=[globs['var']['bind_get_history'],'<Return>','<KP_Enter>','<space>'],action=self.get_history) # При просто <Button-1> выделение еще не будет выбрано
		create_binding(widget=self.listbox,bindings=globs['var']['bind_copy_history'],action=self.copy_history)
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_go_search'],globs['var']['bind_go_search_alt']],action=self.go_search)
		create_binding(widget=self.search_field,bindings=globs['var']['bind_clear_search_field'],action=self.clear_search_field)
		create_binding(widget=self.search_field,bindings=globs['var']['bind_paste_search_field'],action=self.paste_search_field)
		# Перейти на предыдущую/следующую статью
		create_binding(widget=globs['top'],bindings=globs['var']['bind_go_back'],action=self.go_back)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_go_forward'],action=self.go_forward)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_left'],action=self.move_left)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_right'],action=self.move_right)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_down'],action=self.move_down)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_up'],action=self.move_up)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_line_start'],action=self.move_line_start)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_line_end'],action=self.move_line_end)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_text_start'],action=self.move_text_start)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_text_end'],action=self.move_text_end)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_page_start'],action=self.move_page_start)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_page_end'],action=self.move_page_end)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_page_up'],action=self.move_page_up)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_move_page_down'],action=self.move_page_down)
		# Для выхода нельзя использовать Return, поскольку это конфликтует с Shift - Enter. Поэтому оставляем только Escape.
		if 'TrackClipboard' in db and db['TrackClipboard']:
			create_binding(widget=globs['top'],bindings=['<Escape>','<Control-w>','<Alt-F4>'],action=lambda x:self.toggle_clipboard_mode(mode='close'))
		else:
			create_binding(widget=globs['top'],bindings='<Escape>',action=lambda e: iconify(widget=globs['top']))
		if sys_type == 'win' or sys_type == 'mac':
			create_binding(widget=globs['top'],bindings='<MouseWheel>',action=self.mouse_wheel)
		else:
			create_binding(widget=globs['top'],bindings=['<Button 4>','<Button 5>'],action=self.mouse_wheel)
		if 'TrackClipboard' in db and db['TrackClipboard']:
			create_binding(widget=globs['web_widget'],bindings=globs['var']['bind_hide_top'],action=lambda x:self.toggle_clipboard_mode(mode='close'))
		else:
			create_binding(widget=globs['web_widget'],bindings=globs['var']['bind_hide_top'],action=lambda x:iconify(widget=globs['top']))
		# Дополнительные горячие клавиши
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_quit_now'],globs['var']['bind_quit_now_alt']],action=quit_now)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_search_article_forward'],action=lambda e:self.search_article(direction='forward'))
		create_binding(widget=globs['top'],bindings=globs['var']['bind_search_article_backward'],action=lambda e:self.search_article(direction='backward'))
		create_binding(widget=globs['top'],bindings=globs['var']['bind_re_search_article'],action=lambda e:self.search_article(direction='clear'))
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_reload_article'],globs['var']['bind_reload_article_alt']],action=loop_page)
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_save_article'],globs['var']['bind_save_article_alt']],action=self.save_article)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_search_field'],action=lambda e:self.search_field.focus_force())
		create_binding(widget=globs['top'],bindings=globs['var']['bind_show_about'],action=self.show_about)
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_toggle_history'],globs['var']['bind_toggle_history_alt']],action=self.toggle_history)
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_open_in_browser'],globs['var']['bind_open_in_browser_alt']],action=self.open_in_browser)
		create_binding(widget=globs['top'],bindings=globs['var']['bind_copy_url'],action=lambda x:self.copy_url(widget=globs['top'],mode='term'))
		create_binding(widget=globs['top'],bindings=globs['var']['bind_copy_article_url'],action=lambda x:self.copy_url(widget=globs['top'],mode='article'))
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_watch_clipboard'],globs['var']['bind_watch_clipboard_alt']],action=self.watch_clipboard)
		create_binding(widget=globs['top'],bindings=[globs['var']['bind_spec_symbol']],action=self.spec_symbol)
		create_binding(widget=self.search_field,bindings='<Control-a>',action=lambda x:self.select_all(self.search_field,Small=True))
		create_binding(widget=globs['top'],bindings=globs['var']['bind_define'],action=lambda x:self.define(Selected=True))
		create_binding(widget=globs['top'],bindings=globs['var']['bind_toggle_iconify'],action=self.toggle_iconify)
		#----------------------------------------------------------------------

def get_url():
	cur_func = sys._getframe().f_code.co_name
	db['url'] = online_url_safe
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Поскольку Multitran использует кодировку windows-1251, необходимо использовать ее. Поскольку некоторые символы не кодируются в globs['var']['win_encoding'] корректно, оставляем для них кодировку UTF-8.
		try:
			request_encoded = db['search'].encode(globs['var']['win_encoding'])
		except:
			request_encoded = bytes(db['search'],encoding=default_encoding)
		# Некоторые версии питона принимают 'encode('windows-1251')', но не 'encode(encoding='windows-1251')'
		db['url'] = online_request(globs['var']['online_dic_url'],request_encoded)
		log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))

# Создать веб-страницу из ячеек и провести другие необходимые операции
# Вынесено в отдельную процедуру для обеспечения быстрой перекомпоновки ячеек
def process_cells():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['cells'] = split_by_columms(db['elem'])
		#db['cells'] = distribute_columns(db['cells'])
		#span_cells = create_span(db['cells'])
		generate_simple_page()
		generate_tkhtml_text()
		assign_cur_cell(get_selectable(0,0,GetNext=False))
		if globs['bool']['SelectTermsOnly']:
			db['move_start'] = get_selectable(0,0,GetNext=False)
			db['move_end'] = get_selectable_backwards(len(db['cells'])-1,len(db['cells'][0])-1,GetPrevious=False)
		else:
			db['move_start'] = (0,0)
			db['move_end'] = (-1,-1)
		move_events()

# Подготовить всю необходимую информацию для отображения GUI
def get_article():
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
		#----------------------------------------------------------------------
		# Воссоздаем значения, если они отсутствуют
		if not 'history' in db:
			db['history'] = []
			db['history_url'] = []
		if not 'mode' in db:
			db['mode'] = 'url' # 'clipboard', 'skip'
		if not 'url' in db:
			db['url'] = 'http://www.multitran.ru/c/m.exe?CL=1&s=%C4%EE%E1%F0%EE+%EF%EE%E6%E0%EB%EE%E2%E0%F2%FC%21&l1=1'
		if not 'TrackClipboard' in db:
			db['TrackClipboard'] = False
		if not 'Iconify' in db:
			db['Iconify'] = True
		if not 'search' in db:
			db['search'] = globs['mes'].welcome
			log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
		if not 'ShowHistory' in db:
			db['ShowHistory'] = False
		if not 'FirstLaunch' in db:
			db['FirstLaunch'] = True
		if 'search_list' in db:
			del db['search_list']
		#----------------------------------------------------------------------
		if globs['Quit']:
			log(cur_func,lev_info,globs['mes'].goodbye)
			root.destroy()
			sys.exit()
		#elif db['mode'] == 'clipboard':
		elif db['TrackClipboard']:
			old_clipboard = clipboard_paste()
			new_clipboard = old_clipboard
			#root.withdraw()
			while old_clipboard == new_clipboard:
				sleep(1)
				if globs['Quit']:
					log(cur_func,lev_info,globs['mes'].goodbye)
					sys.exit()
				new_clipboard = clipboard_paste()
				# Игнорировать URL, скопированные в буфер обмена
				if 'http://' in new_clipboard or 'www.' in new_clipboard or globs['IgnorePaste']:
					new_clipboard = old_clipboard
				globs['IgnorePaste'] = False
			db['search'] = new_clipboard
			get_url()
			log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
		get_online_article()
		# Предполагаем, что режим может быть 'skip' только после создания БД хотя бы для 1 статьи
		if db['mode'] != 'skip':
			prepare_page()
			if not_found_online in db['page']:
				Warning(cur_func,globs['mes'].term_not_found % db['search'])
				db['search'] = '' # Do not put here anything besides '' because globs['mes'].welcome or any other is not translated for all languages, and we do not obligatory have 'en-ru' pair here, so this can enter an infinite loop
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
			analyse_tags()
			prepare_search()
			db['elem'] = unite_comments(db['elem'])
			process_cells()
		db['FirstLaunch'] = False

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<	
# Unite multiple comments using a separator ' | '. Delete comments-only entries.
def unite_comments(db_elem):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Remove comments-only cells
		i = len(db_elem) - 1
		while i >= 0:
			if db_elem[i]['dic'] == '' and db_elem[i]['term'] == '' and db_elem[i]['comment'] != '':
				db_elem[i-1]['comment'] = db_elem[i-1]['comment']+' | '+db_elem[i]['comment']
				del db_elem[i]
			i -= 1
		# Delete comments separators where they are not necessary
		for i in range(len(db_elem)):
			if db_elem[i]['comment'].startswith(' | '):
				db_elem[i]['comment'] = db_elem[i]['comment'].replace(' | ',' ',1)
	return db_elem
	
# Split selectables according to a predefined number of columns (col_limit)
def split_selectables(selectables):
	cur_func = sys._getframe().f_code.co_name
	split_sel = []
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		row = []
		for i in range(len(selectables)):
			if not empty(selectables[i]):
				if len(row) > 0:
					while len(row) < col_limit:
						row.append([])
					split_sel += [row]
					row = [selectables[i]]
				else:
					row.append(selectables[i])
			elif len(row) == col_limit:
				split_sel += [row]
				row = []
				row.append(selectables[i])
			else:
				row.append(selectables[i])
			# Last element
			if i == len(selectables) - 1:
				while len(row) < col_limit:
					row.append([])
				split_sel += [row]
			log(cur_func,lev_debug,globs['mes'].line_no % (i,str(row)))
		log(cur_func,lev_debug,str(split_sel))
	return split_sel

# Split the list of article elements according to a predefined number of columns (col_limit)
# todo: Если вынести {'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False} как empty_elem, то он будет меняться, поэтому указываю пока явно.
def split_by_columms(db_elem):
	cur_func = sys._getframe().f_code.co_name
	'''Разбить список вхождений статьи по столбцам
	Возможные виды:
	1: 1-й столбец содержит название словаря или пуст, всего столбцов указанное количество
	2: название словаря занимает всю строчку, 1-й столбец содержит термин или комментарий
	3: источник (Мультитран, Лингво и пр.) занимает всю строчку, далее как в виде 1 или 2
	4: всего столбцов: 2. 1-й столбец содержит название словаря или пуст, 2-й столбец содержит термины и комментарии в сплошном порядке.
	'''
	cells = []
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Текущий вид: 1
		# Текст ячеек. Термины и комментарии объединены.
		row = []
		for i in range(len(db_elem)):
			if db_elem[i]['dic'] != '':
				if len(row) > 0:
					while len(row) < col_limit:
						row.append({'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False})
					cells += [row]
					row = [db_elem[i]]
				else:
					row.append(db_elem[i])
			elif len(row) == col_limit:
				cells += [row]
				# A dic title is in the 1st column
				row = [{'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False}]
				row.append(db_elem[i])
			else:
				row.append(db_elem[i])
			# Last element
			if i == len(db_elem) - 1:
				while len(row) < col_limit:
					row.append({'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False})
				cells += [row]
			log(cur_func,lev_debug,globs['mes'].line_no % (i,str(row)))
		log(cur_func,lev_debug,str(cells))
	return cells

# Вернуть режим распределения свободного пространства для столбцов разной длины: без распределения (none), распределить на максимально длинный столбец (max), распределить равномерно и, при необходимости, добавить остаток к максимально длинному столбцу (all)
def distribute_mode(len_empty,non_empty,max_pos=-1):
	cur_func = sys._getframe().f_code.co_name
	mode = 'none' # 'none', 'max', 'all'
	# List of integer ratios
	proportions = []
	# Sum of all elements of the 'proportions' list
	props = 0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if len_empty == 0:
			mode = 'none'
		elif len_empty == 1:
			mode = 'max'
			# First column is occupied by a dictionary title, thus, it is max_pos and not max_pos-1.
			for i in range(max_pos):
				proportions.append(0)
			proportions.append(1)
		else:
			total = 0
			for i in range(len(non_empty)):
				total += non_empty[i]
			#---------------------------------------------------------------
			min_prop = total/len_empty
			#---------------------------------------------------------------
			for i in range(len(non_empty)):
				proportions.append(round(non_empty[i]/min_prop))
			#---------------------------------------------------------------
			for i in range(len(proportions)):
				if proportions[i] > 0:
					props += proportions[i]
			#---------------------------------------------------------------
			if props > len_empty or len([x for x in proportions if x > 0])==1:
				mode = 'max'
			else:
				mode = 'all'
		if mode == 'none':
			log(cur_func,lev_info,globs['mes'].distribute_nothing)
		elif mode == 'max':
			log(cur_func,lev_info,globs['mes'].distribute_max)
		elif mode == 'all':
			log(cur_func,lev_info,globs['mes'].distribute_equally)
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'none, max, all'))
		log(cur_func,lev_debug,globs['mes'].ratios % str(proportions))
		log(cur_func,lev_debug,globs['mes'].for_distribution % str(props))
	return(mode,proportions,props)

# Assign empty columns to table columns according to the text length
# todo: Если вынести {'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False} как empty_elem, то он будет меняться, поэтому указываю пока явно.
def distribute_columns(cells,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if len(cells) > 0:
			if col_limit >= min_col_limit:
				for i in range(len(cells)):
					row = [] # Text-only list of article entries
					row_elem = [] # List of dictionaries describing article entries
					# The mode when the first column is assigned for dictionary titles
					j = 1
					len_empty = 0
					# Collect some info on empty columns
					while j < len(cells[i]):
						if cells[i][j]['selectable']:
							row.append(cells[i][j]['dic']+cells[i][j]['term']+cells[i][j]['comment'])
							row_elem.append(cells[i][j])
						else:
							len_empty += 1
						#	row.append('')
						j += 1
					lst_len_ne = []
					for j in range(len(row)):
						lst_len_ne.append(len(row[j]))
					# Cannot max on an empty list
					if len(lst_len_ne) > 0:
						max_pos=lst_len_ne.index(max(lst_len_ne))
					else:
						max_pos = -1
					# (column_no,number of columns to add)
					res_lst = distribute_mode(len_empty,lst_len_ne,max_pos)[1]
					indexes = []
					nos = []
					for j in range(len(res_lst)):
						indexes.append(j)
						nos.append(res_lst[j])
					res_lst = res_lst[::-1]
					indexes = indexes[::-1]
					nos = nos[::-1]
					# Assign empty columns to columns with longest text
					# It is OK to assign empty cells even if we plan to merge them because Qt does not actually merge them, it just hides their contents. So, if due to an error we get a merged cell that is not visible, it will always be empty and unselectable.
					for j in range(len(res_lst)):
						for k in range(nos[j]):
							# Ensure that the number of cells will be not greater than col_limit
							# For some reason, at col_limit > 5 the number of elements in row_elem can exceed col_limit (adding columns on the basis of ratios without checking?)
							# -1 since with will further need to add a dictionary title as the first column
							if len(row_elem) < col_limit - 1:
								row_elem.insert(indexes[j]+1,{'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False})
					# Return the 1st column assigned for dictionary titles
					if len(cells[i]) > 0:
						row_elem.insert(0,cells[i][0])
					# Ensure that the number of cells will be not less than col_limit (adding empty cells on the basis of the ratios is not enough).
					delta = col_limit - len(row_elem)
					for j in range(delta):
						row_elem.insert(-1,{'dic':'','term':'','comment':'','url':online_url_safe,'selectable':False})
					log(cur_func,lev_debug,globs['mes'].line_no % (i,str(row_elem)))
					if len(row_elem) != col_limit:
						mestype(cur_func,globs['mes'].inconsistent_columns % (i,len(row_elem),col_limit),Silent=Silent,Critical=Critical)
					cells[i] = row_elem
			else:
				mestype(cur_func,globs['mes'].min_col_limit % (min_col_limit,col_limit),Silent=Silent,Critical=Critical)
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	return cells
	
# Create a list indicating a number of empty elements in succession and a position preceding to them
def prepare_span(lst): # A list of dictionaries characterizing article entries
	cur_func = sys._getframe().f_code.co_name
	col_info = []
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		i = len(lst) - 1
		last_empty_pos = -1
		first_empty_pos = -1
		owner = -1
		while i >= 0:
			if i != 0 and not lst[i]['selectable']:
				if i < len(lst)-1:
					if lst[i+1]['selectable']:
						last_empty_pos = i
				else:
					last_empty_pos = i
			elif last_empty_pos != -1:
				if i < len(lst) - 1:
					first_empty_pos = i + 1
					owner = i
					col_info += [[owner,last_empty_pos-first_empty_pos+1]]
					first_empty_pos = -1
					last_empty_pos = -1
			i -= 1
		col_info = col_info[::-1]
		log(cur_func,lev_debug,str(col_info))
	return col_info
	
# Create a list of cells to be merged compatible with QT setSpan
def create_span(cells):
	cur_func = sys._getframe().f_code.co_name
	# (row No, column No, number of rows, number of columns (to merge))
	span_cells = []
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		for i in range(len(cells)):
			# Example: [[1,1],[3,1]] ([pos_of_elem,nos_of_cells_to_merge])
			tmp_lst = prepare_span(cells[i])
			for j in range(len(tmp_lst)):
				# We need to add 1 (a column to be merged + empty columns)
				span_cells += [[i,tmp_lst[j][0],1,tmp_lst[j][1]+1]]
		log(cur_func,lev_debug,str(span_cells))
	return span_cells
	
# Создать простой и быстрый при отображении html, не перегруженный JavaScript и ненужными тэгами
def generate_simple_page(Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	db['simple_html'] = '<html><body></body></html>'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cells' in db and len(db['cells']) > 0:
			db['simple_html'] = '<html><body><table>'
			# Форматирование текста ячеек тэгами
			for i in range(len(db['cells'])):
				db['simple_html'] += '<tr>'
				# Число столбцов в таблице должно быть одинаковым!
				for j in range(len(db['cells'][0])):
					# Названия словарей
					db['simple_html'] += '<td align="center"><font face="'
					db['simple_html'] += globs['var']['font_dics_family']
					db['simple_html'] += '" color="'
					db['simple_html'] += globs['var']['color_dics']
					db['simple_html'] += '" size="'
					db['simple_html'] += str(globs['int']['font_dics_size'])
					db['simple_html'] += '"><b>' + db['cells'][i][j]['dic'] + '</b></font></td>'
					# Термины
					db['simple_html'] += '<td><font face="'
					db['simple_html'] += globs['var']['font_terms_family']
					db['simple_html'] += '" color="'
					db['simple_html'] += globs['var']['color_terms']
					db['simple_html'] += '" size="'
					db['simple_html'] += str(globs['int']['font_terms_size'])
					db['simple_html'] += '">' + db['cells'][i][j]['term'] + '</font>'
					# Комментарии
					db['simple_html'] += '<i><font face="'
					db['simple_html'] += globs['var']['font_comments_family']
					db['simple_html'] += '" size="'
					db['simple_html'] += str(globs['int']['font_comments_size'])
					db['simple_html'] += '" color="'
					db['simple_html'] += globs['var']['color_comments']
					db['simple_html'] += '">' + db['cells'][i][j]['comment'] + '</i></font></td>'
				db['simple_html'] += '</tr>'
			db['simple_html'] += '</table></body></html>'
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	
# Загрузить библиотеку tkhtml
def load_tkhtml(master, location=None):
	if not '_tkhtml_loaded' in globs or not globs['_tkhtml_loaded']:
		if location:
			master.tk.eval('global auto_path; lappend auto_path {%s}' % location)
		master.tk.eval('package require Tkhtml')
		globs['_tkhtml_loaded'] = True        

# Вернуть местоположение библиотеки tkhtml
def get_tkhtml_folder():
	# globs['bin_dir']
	return os.path.join (true_dirname(os.path.abspath(sys.argv[0])),
						 "tkhtml",
						 platform.system().replace("Darwin", "MacOSX"),
						 "64-bit" if sys.maxsize > 2**32 else "32-bit")
	
# Подготовить данные, необходимые для выделения в виджете tkhtml и отобразить статью в нем
def set_page(Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cells' in db:
			globs['web_widget'].reset()
			globs['web_widget'].parse(db['simple_html'])
			# cur
			#assert db['plain_text'] == globs['web_widget'].text('text')
			if db['plain_text'] != globs['web_widget'].text('text'):
				log(cur_func,lev_err,globs['mes'].different_texts)
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
		
# Проверить входные данные и назначить текущую и прошлую ячейки
def assign_cur_cell(parts,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cur_cell' in db and 'i' in db['cur_cell'] and 'j' in db['cur_cell']:
			db['last_cell'] = {'i':db['cur_cell']['i'],'j':db['cur_cell']['j']}
		else:
			# Для сохранения структуры при назначении parts
			db['cur_cell'] = {'i':0,'j':0}
		if len(parts) >= 2:
			db['cur_cell']['i'] = parts[0]
			db['cur_cell']['j'] = parts[1]
		else:
			mestype(cur_func,globs['mes'].wrong_input2,Silent=Silent,Critical=Critical)

# Вернуть номер ячейки (номер строки и номер столбца), которой соответствует позиция, возвращаемая виджетом tkhtml в соответствии с простым текстом, возвращаемым этим виджетом.
# Если ячейку выделить нельзя (согласно настройкам), то возвращается предыдущая ячейка
def get_cell(index,Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	check_type(cur_func,index,globs['mes'].type_int)
	if 'cur_cell' not in db:
		get_selectable(GetNext=False)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'pos2cell' in db:
			parts = db['pos2cell'][index]
			if globs['bool']['SelectTermsOnly']:
				if db['cells'][parts[0]][parts[1]]['selectable']:
					assign_cur_cell(parts)
			else:
				assign_cur_cell(parts)
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
			
# Получить текст в том виде, как он будет представлен в tkhtml, а также сгенерировать индексы ячеек на основе этого текста.
'''Недостаток данного способа в том, что алгоритм, по которому tkhtml формирует простой текст, до конца не ясен, однако, критически важно, чтобы текст был угадан правильно. Плюс данного в способа в том, что можно будет разделить GUI и вычисления, а также в том, что индексы ячеек вычислить проще и быстрее.
Несмотря на большую длину списков, выполнение процедуры завершается за 0,01 с. (AMD E-300)
'''
def generate_tkhtml_text(Silent=False,Critical=False):
	cur_func = sys._getframe().f_code.co_name
	# db['page'], очищенный от тэгов, может не совпадать с db['plain_text'], который возвращается tkhtml.
	db['plain_text'] = '' # Текст, соответствующий возвращаемому методом globs['web_widget'].text('text')
	db['pos2cell'] = [] # По позиции символа из tkhtml вернуть координаты соответствующей ячейки (номер строки и номер столбца)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Такая конструкция безопасна. Если 1-е условие ложно, то 2-е проверяться не будет.
		if 'cells' in db and len(db['cells']) > 0:
			db['plain_text'] = '\n'
			# 1-й символ всегда соответствует 1-й ячейке
			db['pos2cell'].append([0,0])
			for i in range(len(db['cells'])):
				# Число столбцов в таблице должно быть одинаковым!
				for j in range(len(db['cells'][0])):
					if not empty(db['cells'][i][j]['dic']):
						tmp_str = db['cells'][i][j]['dic'].strip() + '\n'
						db['cells'][i][j]['first'] = len(db['plain_text'])
						db['plain_text'] += tmp_str
						db['cells'][i][j]['last_term'] = db['cells'][i][j]['first'] + len(db['cells'][i][j]['term'])
						db['cells'][i][j]['last'] = len(db['plain_text'])
						for k in range(len(tmp_str)):
							db['pos2cell'].append([i,j])
					if not empty(db['cells'][i][j]['term']+db['cells'][i][j]['comment']):
						tmp_str = (db['cells'][i][j]['term'] + db['cells'][i][j]['comment']).strip() + '\n'
						db['cells'][i][j]['first'] = len(db['plain_text'])
						db['plain_text'] += tmp_str
						db['cells'][i][j]['last_term'] = db['cells'][i][j]['first'] + len(db['cells'][i][j]['term'])
						db['cells'][i][j]['last'] = len(db['plain_text'])
						for k in range(len(tmp_str)):
							db['pos2cell'].append([i,j])
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	log(cur_func,lev_debug,"len(db['plain_text']): %d" % len(db['plain_text']))
	log(cur_func,lev_debug,"len(db['pos2cell']): %d" % len(db['pos2cell']))
	assert len(db['plain_text']) == len(db['pos2cell'])
	
# Prepare the information on move up, down, left, right, etc. events
def move_events():
	cur_func = sys._getframe().f_code.co_name
	db['move_right'] = []
	db['move_left'] = []
	db['move_down'] = []
	db['move_up'] = []
	if not 'cur_cell' in db:
		db['cur_cell'] = {'i':0,'j':0}
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cells' in db and len(db['cells']) > 0 and len(db['cells'][0]) > 0:
			# todo
			
			# 'Move down' event
			
			#------------------------------------------------------------------
			# 'End' event
			#db['end'] = db['move_down'][-1]
			#------------------------------------------------------------------
			# 'Move up' event
			
			#------------------------------------------------------------------
			# 'Home' event
			
			#------------------------------------------------------------------
			# 'Move left' event
			
			#------------------------------------------------------------------
			# Список ячеек, выбираемых слева направо
			db['move_right'] = []
			for i in range(len(db['cells'])):
				tmp_lst = []
				for j in range(len(db['cells'][i])):
					tmp_lst += [get_selectable(i,j)]
				db['move_right'] += [tmp_lst]
			#------------------------------------------------------------------
			# Список ячеек, выбираемых справа налево
			# Просто перевернуть db['move_right'] оказывается недостаточным
			db['move_left'] = []
			for i in range(len(db['cells'])):
				tmp_lst = []
				for j in range(len(db['cells'][i])):
					tmp_lst += [get_selectable_backwards(i,j)]
				db['move_left'] += [tmp_lst]
			#------------------------------------------------------------------
			# Список первых выбираемых ячеек сверху-вниз
			# db['move_down'] = []
			#------------------------------------------------------------------
			# Список первых выбираемых ячеек снизу-вверх
			# db['move_up'] = []
			#------------------------------------------------------------------
			log(cur_func,lev_debug,"db['move_right']: %s" % str(db['move_right']))
			log(cur_func,lev_debug,"db['move_left']: %s" % str(db['move_left']))
			if globs['bool']['InternalDebug']:
				res_mes = "db['move_up']:" + dlb + str(db['move_up']) + dlb + dlb
				res_mes += "db['move_down']:" + dlb + str(db['move_down']) + dlb + dlb
				res_mes += "db['move_left']:" + dlb + str(db['move_left']) + dlb + dlb
				res_mes += "db['move_right']:" + dlb + str(db['move_right']) + dlb + dlb
				text_field(title=globs['mes'].db_check6,user_text=res_mes,ReadOnly=True)
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)

# Определить следующую (+1,+1) ячейку, которую можно выделить
''' Если выделить можно любую ячейку, то будет выбрана следующая по очереди. Обратить внимание: в конце таблицы, там, где выделяемых ячеек уже нет, будет возвращаться текущая ячейка. Это логично, если выбрать можно любую ячейку, но не совсем логично, если выбирать только помеченные ячейки. Впрочем, если указано использование помеченных ячеек, а ячейка не помечена, то переход на нее осуществлен не будет, поэтому и ссылка в ней использована не будет.
'''
def get_selectable(cur_i=0,cur_j=0,GetNext=True):
	cur_func = sys._getframe().f_code.co_name
	Found = False
	i = sel_i = cur_i
	j = sel_j = cur_j
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cells' in db:
			while i < len(db['cells']):
				while j < len(db['cells'][i]):
					if globs['bool']['SelectTermsOnly']:
						if db['cells'][i][j]['selectable']:
							# Позволяет вернуть последнюю ячейку, которую можно выделить, если достигнут конец таблицы
							sel_i = i
							sel_j = j
							# Если указаная ячейка уже может быть выбрана, то игнорировать ее и искать следующую
							if GetNext:
								if cur_i != i or cur_j != j:
									Found = True
									break
							else:
								Found = True
								break
					else:
						sel_i = i
						sel_j = j
						if cur_i != i or cur_j != j:
							Found = True
							break
					j += 1
				if Found:
					break
				j = 0
				i += 1
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	log(cur_func,lev_debug,str((sel_i,sel_j)))
	return(sel_i,sel_j)
	
# Определить предыдущую (-1,-1) ячейку, которую можно выделить
def get_selectable_backwards(cur_i,cur_j,GetPrevious=True):
	cur_func = sys._getframe().f_code.co_name
	Found = False
	i = sel_i = cur_i
	j = sel_j = cur_j
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if 'cells' in db:
			while i >= 0:
				while j >= 0:
					if globs['bool']['SelectTermsOnly']:
						if db['cells'][i][j]['selectable']:
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
						sel_i = i
						sel_j = j
						if cur_i != i or cur_j != j:
							Found = True
							break
					j -= 1
				if Found:
					break
				i -= 1
				j = len(db['cells'][i]) - 1
		else:
			mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	log(cur_func,lev_debug,str((sel_i,sel_j)))
	return(sel_i,sel_j)

# Инициализировать виджет tkhtml
def create_web_widget(parent):
	cur_func = sys._getframe().f_code.co_name
	web_widget = None
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		web_widget = TkinterHtmlMod(parent)
		vsb = ttk.Scrollbar(parent,orient=tk.VERTICAL)
		hsb = ttk.Scrollbar(parent,orient=tk.HORIZONTAL)
		web_widget.configure(yscrollcommand=vsb.set)
		web_widget.configure(xscrollcommand=hsb.set)
		vsb.config(command=web_widget.yview)
		hsb.config(command=web_widget.xview)
		vsb.pack(side='right',fill='y')
		hsb.pack(side='bottom',fill='x')
		web_widget.pack(expand=1,fill='both')
	return web_widget
	
"""Wrapper for the Tkhtml widget from http://tkhtml.tcl.tk/tkhtml.html"""
class TkinterHtmlMod(tk.Widget):
	def __init__(self, master, cfg={}, **kw):
		load_tkhtml(master, get_tkhtml_folder())
		tk.Widget.__init__(self, master, 'html', cfg, kw)
		# make selection and copying possible
		self._node = None
		self._offset = None
		self._selection_end_node = None
		self._selection_end_offset = None
		self.new_url = None
		create_binding(widget=self,bindings=globs['var']['bind_go_url'],action=self.go_url)
		self.bind("<Motion>",self.mouse_sel,True)
		# ВНИМАНИЕ: По непонятной причине, не работает привязка горячих клавиш (только мышь) для данного виджета, работает только для основного виджета!
		if 'top' in globs:
			create_binding(widget=globs['top'],bindings=[globs['var']['bind_copy_sel'],globs['var']['bind_copy_sel_alt'],globs['var']['bind_copy_sel_alt2']],action=self.copy_cell)
			# По неясной причине в одной и той же Windows ИНОГДА не удается включить '<KP_Delete>'
			create_binding(widget=globs['top'],bindings='<Delete>',action=self.del_cell)
		# todo: Получаю здесь ошибку сегментирования
		# Выделить первую выделяемую ячейку
		#self.set_cell()
	#--------------------------------------------------------------------------
	def node(self, *arguments):
		return self.tk.call(self._w, "node", *arguments)
	#--------------------------------------------------------------------------
	def parse(self, *args):
		self.tk.call(self._w, "parse", *args)
	#--------------------------------------------------------------------------
	def reset(self):
		return self.tk.call(self._w, "reset")
	#--------------------------------------------------------------------------
	def tag(self, subcommand, tag_name, *arguments):
		return self.tk.call(self._w, "tag", subcommand, tag_name, *arguments)
	#--------------------------------------------------------------------------
	def text(self, *args):
		return self.tk.call(self._w, "text", *args)
	#--------------------------------------------------------------------------
	def xview(self, *args):
		"Used to control horizontal scrolling."
		if args: return self.tk.call(self._w, "xview", *args)
		coords = map(float, self.tk.call(self._w, "xview").split())
		return tuple(coords)
	#--------------------------------------------------------------------------
	def xview_moveto(self, fraction):
		"""Adjusts horizontal position of the widget so that fraction
		of the horizontal span of the document is off-screen to the left.
		"""
		return self.xview("moveto", fraction)
	#--------------------------------------------------------------------------
	def xview_scroll(self, number, what):
		"""Shifts the view in the window according to number and what;
		number is an integer, and what is either 'units' or 'pages'.
		"""
		return self.xview("scroll", number, what)
	#--------------------------------------------------------------------------
	def yview(self, *args):
		"Used to control the vertical position of the document."
		if args: return self.tk.call(self._w, "yview", *args)
		coords = map(float, self.tk.call(self._w, "yview").split())
		return tuple(coords)
	#--------------------------------------------------------------------------
	def yview_name(self, name):
		"""Adjust the vertical position of the document so that the tag
		<a name=NAME...> is visible and preferably near the top of the window.
		"""
		return self.yview(name)
	#--------------------------------------------------------------------------
	def yview_moveto(self, fraction):
		"""Adjust the vertical position of the document so that fraction of
		the document is off-screen above the visible region.
		"""
		return self.yview("moveto", fraction)
	#--------------------------------------------------------------------------
	def yview_scroll(self, number, what):
		"""Shifts the view in the window up or down, according to number and
		what. 'number' is an integer, and 'what' is either 'units' or 'pages'.
		"""
		return self.yview("scroll", number, what)
	#--------------------------------------------------------------------------
	# Выделить ячейку
	def set_cell(self,Silent=False,Critical=False):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.tag("delete", "selection")
			if 'cur_cell' in db and 'i' in db['cur_cell'] and 'j' in db['cur_cell']:
				if globs['bool']['SelectTermsOnly']:
					# todo: Проверка наличия 'first'
					index = self.text('index',db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['first'],db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['last_term'])
				else:
					index = self.text('index',db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['first'],db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['last'])
				self.tag("add", "selection",index[0],index[1],index[2],index[3])
				self.tag('configure','selection','-background',globs['var']['color_terms_sel'])
			else:
				mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	#--------------------------------------------------------------------------
	# Изменить ячейку при движении мышью
	def mouse_sel(self,event):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			index = -1
			# Если ячейку определить не удалось, либо ее выделять нельзя (согласно настройкам), то возвращается предыдущая ячейка. Это позволяет всегда иметь активное выделение.
			try:
				self._node, self._offset = self.node(True, event.x, event.y)
				index = self.text("offset", self._node, self._offset)
			except ValueError:
				# Это сообщение появляется так часто, что не ставлю тут ничего.
				#log(cur_func,lev_warn,globs['mes'].unknown_cell)
				pass
			if index >= 0:
				get_cell(index)
				self.set_cell()
	#--------------------------------------------------------------------------
	# Скопировать термин текущей ячейки (или полное ее содержимое)
	def copy_cell(self,event=None,Silent=False,Critical=False):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.set_cell(event)
			if 'cur_cell' in db:
				log(cur_func,lev_debug,globs['mes'].cur_cell % (db['cur_cell']['i'],db['cur_cell']['j']))
				if globs['bool']['CopyTermsOnly']:
					selected_text = db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['term']
				else:
					selected_text = db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['dic'] + ' ' + db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['term'] + db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['comment']
				clipboard_copy(selected_text)
				if db['Iconify']:
					iconify(widget=globs['top'])
			else:
				mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	#--------------------------------------------------------------------------
	# Удалить ячейку и перекомпоновать статью
	def del_cell(self,event,Silent=False,Critical=False):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if 'cur_cell' in db and 'i' in db['cur_cell'] and 'j' in db['cur_cell']:
				Found = False
				# Предполагаем, что db['elem'] уже прошло стадию объединения комментариев
				for i in range(len(db['elem'])):
					# todo: Уточнить и упростить алгоритм
					if db['elem'][i] == db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]:
						Found = True
						break
				if Found:
					del db['elem'][i]
					process_cells()
					set_page()
					if 'last_cell' in db and 'i' in db['last_cell'] and 'j' in db['last_cell'] and 'cells' in db and len(db['cells']) > 0 and db['last_cell']['i'] < len(db['cells']) and db['last_cell']['j'] < len(db['cells'][0]):
						assign_cur_cell((db['last_cell']['i'],db['last_cell']['j']))
					self.set_cell(event)
				else:
					mestype(cur_func,globs['mes'].wrong_input2,Silent=Silent,Critical=Critical)
			else:
				mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
	#--------------------------------------------------------------------------
	# Перейти по URL текущей ячейки
	def go_url(self,event=None,Silent=False,Critical=False):
		cur_func = sys._getframe().f_code.co_name
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			self.set_cell(event)
			if 'cur_cell' in db:
				log(cur_func,lev_debug,globs['mes'].cur_cell % (db['cur_cell']['i'],db['cur_cell']['j']))
				# Используем более короткий ключ для простоты
				db['url'] = db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['url']
				log(cur_func,lev_info,globs['mes'].opening_link % db['url'])
				db['search'] = db['cells'][db['cur_cell']['i']][db['cur_cell']['j']]['term']
				db['mode'] = 'url'
				loop_page()
				globs['top'].title(db['search'])
			else:
				mestype(cur_func,globs['mes'].not_enough_input_data,Silent=Silent,Critical=Critical)
				
# Отобразить новую статью
def loop_page(AddHistory=True,*args):
	cur_func = sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		while True:
			if 'ShowArticle' in globs:
				globs['ShowArticle'].change_pair(None)
			get_article()
			if AddHistory:
				add_history()
			set_page()
			if 'frame_panel' in globs and 'ShowArticle' in globs:
				globs['frame_panel'].destroy()
				globs['ShowArticle'].create_frame_panel()
			if 'top' in globs:
				globs['top'].deiconify()
			if not 'TrackClipboard' in db or not db['TrackClipboard']:
				break
				
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

default_config(config='mclient',Init=True)
read_configs()
get_article()
globs['ShowArticle'] = ShowArticle()
globs['ShowArticle'].first_run()
root.mainloop()
