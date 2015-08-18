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
# В Python 3 не работает просто import urllib, импорт должен быть именно такой, как здесь
import urllib.request, urllib.parse
import html.parser
import posixpath
from configparser import SafeConfigParser
import eg_mod as eg
import mes_ru
import mes_en

# (C) Peter Sklyar, 2015. License: GPL v.3
# All third-party modules are the intellectual work of their authors.

# Нельзя закомментировать, поскольку cur_func нужен при ошибке чтения конфига (которое вне функций)
cur_func='MAIN'
build_ver='3.8 (in progress)'
gpl3_url_ru='http://rusgpl.ru/rusgpl.html'
gpl3_url_en='http://www.gnu.org/licenses/gpl.html'
# Данные глобальные переменные оформлены в виде словаря, что позволяет не использовать лишний раз global.
globs={'AbortAll':False,'LogCount':0,'cur_widget':'ERR_NO_WIDGET_DEFINED','ui_lang':'ru','mes':mes_ru,'license_url':gpl3_url_ru,'mclient_config_root':'mclient.cfg','config_parser':SafeConfigParser()}
globs['top']={}
globs['top'].update({'width':0,'height':0})

lev_crit='CRITICAL'
lev_err='ERROR'
lev_warn='WARNING'
lev_info='INFO'
lev_debug_err='DEBUG-ERROR'
lev_debug='DEBUG'

# Сообщения
my_email='skl.progs@gmail.com'
my_yandex_money='41001418272280'
# Скрытые сообщения об ошибках
err_mes_unavail='CF_UNICODETEXT_UNAVAILABLE'
err_mes_copy='CLIPBOARD_COPY_ERROR'
err_mes_paste='CLIPBOARD_PASTE_ERROR'
err_wrong_enc='WRONG_ENCODING_ERROR'
err_incor_log_mes='INCORRECT_LOG_MESSAGE'
cur_widget='ERR_NO_WIDGET_DEFINED'
err_mes_no_feature_text='ERR_NO_FEATURE_TEXT'
err_mes_no_full_inq_text='ERR_NO_FULL_INQ_TEXT'
err_mes_no_inq_path='ERR_NO_INQ_PATH'
err_mes_empty_question='ERR_EMPTY_QUESTION'
err_mes_empty_warning='ERR_EMPTY_WARNING'
err_mes_empty_info='ERR_EMPTY_INFO'
err_mes_empty_error='ERR_EMPTY_ERROR'
err_mes_empty_input='ERR_EMPTY_INPUT'
err_mes_no_selection='ERR_NO_SELECTION'
err_mes_selected_not_matched='SELECTED_NOT_MATCHED'
err_mes_empty_mes='EMPTY_MESSAGE'
err_mes_unsupported_lang='ERR_UNSUPPORTED_LANGUAGE'
# cur_widget может меняться, поэтому не добавляю его в cmd_err_mess
cmd_err_mess=[err_mes_unavail,err_mes_copy,err_mes_paste,err_wrong_enc,err_incor_log_mes,err_mes_no_feature_text,err_mes_no_full_inq_text,err_mes_no_inq_path,err_mes_empty_question,err_mes_empty_warning,err_mes_empty_info,err_mes_empty_error,err_mes_empty_input,err_mes_no_selection,err_mes_selected_not_matched,err_mes_empty_mes,err_mes_unsupported_lang]

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
XAL => RUS      Калм-рус:       'http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s'
ENG => DEU      Англ-нем:       'http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s'
ENG => EST      Англ-эст:       'http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s'
'''
online_url_root='http://www.multitran.ru/c/m.exe?'
online_url_safe='http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%ED%E5%E2%E5%F0%ED%E0%FF+%F1%F1%FB%EB%EA%E0'
default_pair='ENG <=> RUS'
globs['cur_pair']=default_pair
pairs=['ENG <=> RUS','DEU <=> RUS','SPA <=> RUS','FRA <=> RUS','NLD <=> RUS','ITA <=> RUS','LAV <=> RUS','EST <=> RUS','AFR <=> RUS','EPO <=> RUS','XAL <=> RUS','ENG <=> DEU','ENG <=> EST']
online_dic_urls=['http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=3&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=5&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=4&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=24&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=23&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=27&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=26&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=31&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=34&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s']
not_found_online='Вы знаете перевод этого слова? Добавьте его в словарь'
my_program_title=''
#------------------------------------------------------------------------------
# Tag patterns
tag_pattern1='<a title="'
tag_pattern2='<a href="m.exe?'
tag_pattern3='<i>'
tag_pattern4='</i>'
tag_pattern5='<span STYLE="color:gray">'
tag_pattern6='<span STYLE="color:black">'
tag_pattern7='</a>'
tag_pattern8='">'
tag_pattern9='<span STYLE="color:rgb(60,179,113)">'
tag_pattern10='</td>'
#------------------------------------------------------------------------------
# Список символов, которые можно считать за буквы.
allowed_syms=['°']
sizes={}
sizes['top']={}
sizes['top']['width']=0
sizes['top']['height']=0

# Разделы конфигурационного файла
SectionLinuxSettings='Linux settings'
SectionWindowsSettings='Windows settings'
SectionMacSettings='Mac settings'
SectionVariables='Variables'
SectionIntegers='Integer Values'
SectionFloatings='Floating Values'
SectionBooleans='Boolean'
Sections=[SectionLinuxSettings,SectionWindowsSettings,SectionMacSettings,SectionVariables,SectionIntegers,SectionFloatings,SectionBooleans]

# Custom
default_encoding='utf-8'
# Неразрывный пробел, non-breaking space
nbspace=' '
dlb='\n'
wdlb='\r\n'

root=tk.Tk()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Placeholders
def log(cur_func,level,log_mes,TransFunc=False):
	#print(cur_func,':',level,':',log_mes)
	pass
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
	root.withdraw()
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
	cur_func=sys._getframe().f_code.co_name
	if os.path.exists(cur_file):
		Success=True
	else:
		Success=False
		mestype(cur_func,globs['mes'].file_not_found % cur_file,Silent=Silent,Critical=Critical)
	# Лог еще не подключен
	return Success
		
# Определить тип ОС
def detect_os():
	#cur_func=sys._getframe().f_code.co_name
	if 'win' in sys.platform:
		par='win'
	elif 'lin' in sys.platform:
		par='lin'
	elif 'mac' in sys.platform:
		par='mac'
	else:
		par='unknown'
	# Занесение в лог здесь делать рано, конфиг еще не прочитан
	#log(cur_func,lev_debug,str(par))
	return par

sys_type=detect_os()
if sys_type=='win':
	sysdiv='\\'
else:
	sysdiv='/'
	
# Верно определить каталог по полному пути вне зависимости от ОС
def true_dirname(path,UseLog=True):
	cur_func=sys._getframe().f_code.co_name
	path=path.replace('\\','//')
	#curdir=ntpath.dirname(path)
	curdir=posixpath.dirname(path)
	if sys_type=='win':
		curdir=curdir.replace('//','\\')
	if UseLog:
		log(cur_func,lev_debug,mes.full_path2 % (path,curdir))
	return curdir
	
# Вернуть расширение файла с точкой
def get_ext(file):
	cur_func=sys._getframe().f_code.co_name
	if AbortAll==[True]:
		log(cur_func,lev_warn,mes.abort_func % cur_func)
		return ''
	else:
		func_res=os.path.splitext(file)[1]
		log(cur_func,lev_debug,str(func_res))
		return func_res

# Изменить язык графического интерфейса и сообщений
def toggle_ui_lang():
	if globs['ui_lang']=='en':
		globs['ui_lang']='ru'
		globs['mes']=mes_ru
		globs['secret']=secret_ru
		globs['license_url']=gpl3_url_ru
	else:
		globs['ui_lang']='en'
		globs['mes']=mes_en
		globs['secret']=secret_en
		globs['license_url']=gpl3_url_en

# Загрузить конфигурацию по умолчанию
def default_config(config='mclient',Init=True):
	cur_func=sys._getframe().f_code.co_name
	# Ключи, которые, возможно, стоит убрать: pixel_hack, use_format, use_output, mismatch_num, (некоторые в bool), CorrectHTML, UsePaste, DeclineFeatures, DicHints, AlwaysMaximize, TrimEnd, currar, Online
	if Init:
		globs['lin']={}
		globs['win']={}
		globs['mac']={}
		globs['var']={}
		globs['int']={}
		globs['float']={}
		globs['bool']={}
	# Эти ключи нужно создавать до чтения конфига
	globs['bin_dir']=true_dirname(os.path.realpath(sys.argv[0]),UseLog=False)
	globs['mclient_config']=globs['bin_dir']+sysdiv+globs['mclient_config_root']
	if config=='mclient':
		#globs['var'].update({'bind_re_search_article':'<Control-f>','bind_reload_article':'<Control-r>','bind_save_article':'<Control-s>'})
		globs['var'].update({'online_dic_url':'http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s','color_terms':'black','color_terms_sel':'cyan','color_dics':'cadet blue','color_comments':'gray','color_borders':'azure2','font_history':'Sans 12','font_terms':'Sans 14','font_terms_sel':'Sans 14 bold italic','font_dics':'Sans 14','font_comments':'Sans 14','window_size':'1024x768','repeat_sign':'!','repeat_sign2':'!!','default_hint_background':'#ffffe0','default_hint_direction':'top','default_hint_border_color':'navy','bind_get_history':'<Double-Button-1>','bind_copy_history':'<ButtonRelease-3>','bind_clear_search_field':'<ButtonRelease-3>','bind_paste_search_field':'<ButtonRelease-2>','bind_go_back':'<Alt-Left>','bind_go_forward':'<Alt-Right>','bind_move_left':'<Left>','bind_move_right':'<Right>','bind_move_down':'<Down>','bind_move_up':'<Up>','bind_move_line_start':'<Home>','bind_move_line_end':'<End>','bind_move_text_start':'<Control-Home>','bind_move_text_end':'<Control-End>','bind_move_page_start':'<Shift-Home>','bind_move_page_end':'<Shift-End>','bind_move_page_up':'<Prior>','bind_move_page_down':'<Next>','bind_go_url':'<Button-1>','bind_copy_sel':'<Control-Return>','bind_copy_sel_alt':'<Control-KP_Enter>','bind_copy_sel_alt2':'<ButtonRelease-3>','bind_go_search':'<Return>','bind_go_search_alt':'<KP_Enter>','bind_clear_history':'<ButtonRelease-3>','bind_close_top':'<ButtonRelease-2>','bind_quit_now':'<Control-q>','bind_search_article_forward':'<F3>','bind_search_article_backward':'<Shift-F3>','bind_re_search_article':'<Control-F3>','bind_reload_article':'<F5>','bind_save_article':'<F2>','bind_search_field':'<F6>','bind_show_about':'<F1>','icon_main':'icon_64x64_main.gif','icon_mclient':'icon_64x64_mclient.gif','icon_go_search':'icon_36x36_go_search.gif','icon_toggle_history':'icon_36x36_toggle_history.gif','icon_watch_clipboard_on':'icon_36x36_watch_clipboard_on.gif','icon_watch_clipboard_off':'icon_36x36_watch_clipboard_off.gif','icon_open_in_browser':'icon_36x36_open_in_browser.gif','icon_change_ui_lang':'icon_36x36_change_ui_lang.gif','icon_show_about':'icon_36x36_show_about.gif','icon_save_article':'icon_36x36_save_article.gif','icon_search_article':'icon_36x36_search_article.gif','icon_quit_now':'icon_36x36_quit_now.gif','icon_go_back':'icon_36x36_go_back.gif','icon_go_back_off':'icon_36x36_go_back_off.gif','icon_go_forward':'icon_36x36_go_forward.gif','icon_go_forward_off':'icon_36x36_go_forward_off.gif','icon_clear_search_field':'icon_36x36_clear_search_field.gif','icon_clear_history':'icon_36x36_clear_history.gif','icon_paste':'icon_36x36_paste.gif','icon_reload':'icon_36x36_reload.gif','icon_repeat_sign':'icon_36x36_repeat_sign.gif','icon_repeat_sign_off':'icon_36x36_repeat_sign_off.gif','icon_repeat_sign2':'icon_36x36_repeat_sign2.gif','icon_repeat_sign2_off':'icon_36x36_repeat_sign2_off.gif','font_style':'Sans 14','win_encoding':'windows-1251'})
		globs['int'].update({'pixel_hack':18,'default_button_size':36,'default_hint_delay':800,'default_hint_width':280,'default_hint_height':30,'default_hint_border_width':2})
		globs['bool'].update({'mclientSaveTitle':False,'AlwaysMaximize':True,'TermsColoredSep':False,'ShowWallet':True,'TextButtons':False,'UseOptionalButtons':True,'ReadOnlyProtection':False,'InternalDebug':False,'ShortHistory':True,'AutoHideHistory':True})
	else:
		ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(config),'mclient'))
		
# Вопрос
def Question(cur_func='MAIN',cur_mes=err_mes_empty_question):
	root.withdraw()
	par=tkmes.askokcancel(globs['mes'].ques_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_info,cur_mes)
	return par

# Названия такие же, как у модуля PyZenity (кроме List)
# Информация
def InfoMessage(cur_func='MAIN',cur_mes=err_mes_empty_info):
	root.withdraw()
	tkmes.showinfo(mes.inf_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_info,cur_mes)

# Предупреждение
def Warning(cur_func='MAIN',cur_mes=err_mes_empty_warning):
	root.withdraw()
	tkmes.showwarning(globs['mes'].warn_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_warn,cur_mes)
	
# Заменить двойные разрывы строк на одиночные
def delete_double_line_breaks(line,Strip=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Удаляем разрывы строк в случае копирования из табличного процессора
		# Для LO/Gnumeric (даже Win-версий) достаточно \n, для MSO этого недостаточно (нужно \r\n)
		# Без str может дать TypeError: Type str doesn't support the buffer API
		line=str(line)
		while '\r\n' in line:
			line=line.replace('\r\n','\n')
		line=line.replace('\r','\n')
		while '\n\n' in line:
			line=line.replace('\n\n','\n')
		# Удалить пробелы и переносы строк с начала и конца
		if Strip:
			line=line.strip()
		else:
			# Удалять перенос строки с конца текста нужно всегда
			line=line.strip(dlb)
		log(cur_func,lev_debug,str(line))
	return line

# Вставить из буфера обмена
def clipboard_paste(MakePretty=True):
	cur_func=sys._getframe().f_code.co_name
	line=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Иначе происходит зависание в цикле
		root.update()
		try:
			line=root.clipboard_get()
		except:
			line=err_mes_paste
			log(cur_func,lev_debug,str(line))
			Warning(cur_func,globs['mes'].clipboard_paste_failure)
		if MakePretty:
			if not line in cmd_err_mess:
				line=delete_double_line_breaks(line)
			if line.startswith(dlb):
				line=line.replace(dlb,'',1)
			line=line.rstrip(dlb)
		log(cur_func,lev_debug,str(line))
	return line
	
# Создание корректной ссылки в Интернете (URI => URL)
def online_request(base_str,my_request_bytes): #str, bytes
	cur_func=sys._getframe().f_code.co_name
	my_url=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		my_url=base_str % urllib.parse.quote(my_request_bytes)
		log(cur_func,lev_debug,str(my_url))
	return my_url

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
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		fragm=fragm.replace(',','')
		fragm=fragm.replace('.','')
		fragm=fragm.replace('!','')
		fragm=fragm.replace('?','')
		fragm=fragm.replace(':','')
		fragm=fragm.replace(';','')
		log(cur_func,lev_debug,str(fragm))
	return fragm
	
# Удалить нумерацию в виде алфавита
def delete_alphabetic_numeration(line):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		my_expr=' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
		match=re.search(my_expr,line)
		while match:
			replace_what=match.group(0)
			replace_with=match.group(1)
			line=line.replace(replace_what,replace_with)
			match=re.search(my_expr,line)
		log(cur_func,lev_debug,str(line))
	return line

# Преобразовать строку в нижний регистр, удалить пунктуацию и алфавитную нумерацию
def prepare_str(line,Extended=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		line=line.lower()
		line=line.replace('ё','е')
		line=line.replace('"','')
		line=line.replace('“','')
		line=line.replace('”','')
		line=line.replace('«','')
		line=line.replace('»','')
		line=line.replace('(','')
		line=line.replace(')','')
		line=line.replace('[','')
		line=line.replace(']','')
		line=line.replace('{','')
		line=line.replace('}','')
		line=line.replace('*','')
		line=delete_punctuation(line)
		line=delete_alphabetic_numeration(line)
		if Extended:
			line=re.sub('\d+','',line)
			#line=line.replace('-','')
		#log(cur_func,lev_debug,str(line))
	return line

# Проанализировать текст и вернуть информацию о нем
def analyse_text(text,Truncate=True,Decline=False):
	cur_func=sys._getframe().f_code.co_name
	text_db={}
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		start_time=time()
		check_args(cur_func,[[text,globs['mes'].type_str],[Truncate,globs['mes'].type_bool]])
		# Нотация: lst = general list, clst = char list, wlst = word list, slst = sentence list
		first_syms=[] # позиции первых букв слов
		first_syms_sl=[] # позиции первых букв слов (отсчет от начала текущей строки)
		first_syms_nf=[]
		first_syms_nf_sl=[]
		words=[] # список слов
		# Для dlbs и nls делать _sl бессмысленно
		dlbs=[] # позиции dlb
		nls=[] # номера слов, с которых начинается новая строка
		spaces=[] # позиции пробелов
		spaces_sl=[] # позиции пробелов (отсчет от начала текущей строки)
		last_syms=[] # позиции последних букв слов
		last_syms_sl=[] # позиции последних букв слов (отсчет от начала текущей строки)
		last_syms_nf=[] # позиции последних букв слов без пунктуации
		last_syms_nf_sl=[] # позиции последних букв слов без пунктуации (отсчет от начала текущей строки)
		sent_nos=[] # список номеров строк для каждого слова
		words_nf=[] # список слов без пунктуации
		sents_sym_len=[] # Длина предложений в символах
		sents_word_len=[] # Список количеств слов в предложениях
		sents_text=[] # Список предложений с сохранением лишних пробелов и пунктуации
		sents_text_nf=[] # Список предложений с сохранением лишних пробелов без пунктуации
		# Пример: [[[0, 2], [4, 8], [10, 17]], [[34, 34], [36, 38], [40, 43]]]
		sents_pos=[] # Список позиций символов начала и конца слов, разбитый по предложениям
		sents_pos_sl=[] # Тот же список, но номера идут от начала строки
		sents_pos_nf=[] # Тот же список, но без учета пунктуации
		sents_pos_nf_sl=[] # Тот же список, но номера идут от начала строки без учета пунктуации
		#--------------------------------------------------------------------------
		# Truncate - удалить лишние пробелы, переносы строк. Однако, strip по строкам не делается.
		if Truncate:
			text=tr_str(text)
		else:
			text=text.replace(wdlb,dlb)
		#--------------------------------------------------------------------------
		word=''
		k=0
		# В принципе, текст не должен быть пуст, но мы на всякий случай инициализируем i, чтобы не возникло ошибки при maxi=i
		i=0
		for i in range(len(text)):
			if text[i]==dlb:
				dlbs+=[i]
				# Проверка защищает от двойных dlb и пробелов
				if word!='':
					words.append(word)
				word=''
				nls+=[len(words)]
				k=-1
			# Необходимо разделять слова с неразрывным пробелом тоже, иначе фраза будет восприниматься как единое слово
			elif text[i].isspace():
				spaces+=[i]
				spaces_sl+=[k]
				if word!='':
					words.append(word)
				word=''
			else:
				word+=text[i]
				if len(word)==1:
					first_syms+=[i]
					first_syms_sl+=[k]
					if word.isdigit() or word.isalpha() or word in allowed_syms:
						first_syms_nf+=[i]
						first_syms_nf_sl+=[k]
					elif i+1 < len(text):
						delta=i+1
						kdelta=k+1
						while delta < len(text) and not text[delta].isalpha() and not text[delta].isdigit() and not text[delta] in allowed_syms:
							delta+=1
							kdelta+=1
						first_syms_nf+=[delta]
						first_syms_nf_sl+=[kdelta]
						log(cur_func,lev_debug,globs['mes'].first_syms_cor % (i,delta))
					else:
						first_syms_nf+=[i]
						first_syms_nf_sl+=[k]
						log(cur_func,lev_warn,globs['mes'].first_syms_failure)
			k+=1
		# Добавление последнего слова
		if word!='' and word!=dlb:
			words.append(word)
		maxi=i
		words_num=len(words)
		sent_no=0
		for i in range(words_num):
			words_nf.append(prepare_str(words[i],Extended=False)) # Ключ Extended=True удалит цифры
			last_syms+=[first_syms[i]+len(words[i])-1]
			last_syms_nf+=[first_syms_nf[i]+len(words_nf[i])-1]
			last_syms_sl+=[first_syms_sl[i]+len(words[i])-1]
			last_syms_nf_sl+=[first_syms_nf_sl[i]+len(words_nf[i])-1]
			if i in nls:
				sent_no+=1
			sent_nos+=[sent_no]
		#--------------------------------------------------------------------------	
		sent_no=0
		j=0
		pos_sl=[] # Список позиций всех символов в тексте в формате [[0,0],[0,1]...[n,n]]
		for i in range(maxi+1):
			pos_sl+=[[sent_no,j]]
			if i in dlbs:
				sent_no+=1
				j=0
			else:
				j+=1
		#--------------------------------------------------------------------------
		sents=[]
		sents_nf=[]
		old_sent_no=-1
		cur_sent=[]
		cur_sent_nf=[]
		cur_pos=[]
		cur_pos_nf=[]
		cur_pos_sl=[]
		cur_pos_nf_sl=[]
		for i in range(len(sent_nos)):
			sent_no=sent_nos[i]
			if sent_no!=old_sent_no:
				if cur_sent!=[]:
					sents+=[cur_sent]
				if cur_sent_nf!=[]:
					sents_nf+=[cur_sent_nf]
				if cur_pos!=[]:
					sents_pos+=[cur_pos]
				if cur_pos_nf!=[]:
					sents_pos_nf+=[cur_pos_nf]
				if cur_pos_sl!=[]:
					sents_pos_sl+=[cur_pos_sl]
				if cur_pos_nf_sl!=[]:
					sents_pos_nf_sl+=[cur_pos_nf_sl]
				cur_sent=[]
				cur_sent_nf=[]
				cur_pos=[]
				cur_pos_nf=[]
				cur_pos_sl=[]
				cur_pos_nf_sl=[]
				old_sent_no=sent_no
			cur_sent+=[words[i]]
			cur_sent_nf+=[words_nf[i]]
			cur_pos+=[[first_syms[i],last_syms[i]]]
			cur_pos_sl+=[[first_syms_sl[i],last_syms_sl[i]]]
			cur_pos_nf+=[[first_syms_nf[i],last_syms_nf[i]]]
			cur_pos_nf_sl+=[[first_syms_nf_sl[i],last_syms_nf_sl[i]]]
		#--------------------------------------------------------------------------
		# Добавление последнего предложения
		if cur_sent!=[]:
			sents+=[cur_sent]
		if cur_sent_nf!=[]:
			sents_nf+=[cur_sent_nf]
		if cur_pos!=[]:
			sents_pos+=[cur_pos]
		if cur_pos_nf!=[]:
			sents_pos_nf+=[cur_pos_nf]
		if cur_pos_sl!=[]:
			sents_pos_sl+=[cur_pos_sl]
		if cur_pos_nf_sl!=[]:
			sents_pos_nf_sl+=[cur_pos_nf_sl]
		#--------------------------------------------------------------------------
		# +1 к номеру последнего предложения
		sents_num=len(sents)
		#--------------------------------------------------------------------------
		for i in range(sents_num):
			if len(sents_pos_sl[i]) > 0:
				sents_sym_len+=[sents_pos_sl[i][-1][1]]
			else:
				sents_sym_len+=[0]
				log(cur_func,lev_warn,globs['mes'].zero_len_sent % i)
		#--------------------------------------------------------------------------
		# +1 к номеру последнего слова в предложении
		for i in range(sents_num):
			sents_word_len+=[len(sents_pos[i])]
		#--------------------------------------------------------------------------
		for i in range(sents_num):
			if sents_sym_len[i] > 0:
				dummy=' '*(sents_sym_len[i]-1)
			else:
				dummy=''
			dummy=list(dummy)
			dummy_nf=list(dummy)
			for j in range(sents_word_len[i]):
				pos1=sents_pos_sl[i][j][0]
				pos1_nf=sents_pos_nf_sl[i][j][0]
				pos2=sents_pos_sl[i][j][1]
				pos2_nf=sents_pos_nf_sl[i][j][1]
				dummy[pos1:pos2+1]=sents[i][j]
				dummy_nf[pos1_nf:pos2_nf+1]=sents_nf[i][j]
			sents_text+=[''.join(dummy)]
			sents_text_nf+=[''.join(dummy_nf)]
		#--------------------------------------------------------------------------
		detailed_declined=decline_nom(words_nf,Decline=Decline)
		#--------------------------------------------------------------------------
		assert(words_num==len(words))
		assert(words_num==len(words_nf))
		assert(words_num==len(first_syms))
		assert(words_num==len(first_syms_sl))
		assert(words_num==len(first_syms_nf))
		assert(words_num==len(first_syms_nf_sl))
		assert(words_num==len(last_syms))
		assert(words_num==len(last_syms_sl))
		assert(words_num==len(last_syms_nf))
		assert(words_num==len(last_syms_nf_sl))
		assert(sents_num==len(sents))
		assert(sents_num==len(sents_nf))
		assert(sents_num==len(sents_pos))
		assert(sents_num==len(sents_pos_nf))
		assert(sents_num==len(sents_pos_sl))
		assert(sents_num==len(sents_pos_nf_sl))
		assert(sents_num==len(sents_text))
		assert(sents_num==len(sents_text_nf))
		#--------------------------------------------------------------------------
		end_time=time()
		log(cur_func,lev_info,globs['mes'].analysis_finished % str(end_time-start_time))
		#--------------------------------------------------------------------------
		log(cur_func,lev_debug,'len (=maxi+1): %d' % (maxi+1))
		log(cur_func,lev_debug,'words: %s' % str(words))
		log(cur_func,lev_debug,'words_nf: %s' % str(words_nf))
		log(cur_func,lev_debug,'nls: %s' % str(nls))
		log(cur_func,lev_debug,'dlbs: %s' % str(dlbs))
		log(cur_func,lev_debug,'spaces: %s' % str(spaces))
		log(cur_func,lev_debug,'spaces_sl: %s' % str(spaces_sl))
		log(cur_func,lev_debug,'first_syms: %s' % str(first_syms))
		log(cur_func,lev_debug,'first_syms_sl: %s' % str(first_syms_sl))
		log(cur_func,lev_debug,'first_syms_nf: %s' % str(first_syms_nf))
		log(cur_func,lev_debug,'first_syms_nf_sl: %s' % str(first_syms_nf_sl))
		log(cur_func,lev_debug,'last_syms: %s' % str(last_syms))
		log(cur_func,lev_debug,'last_syms_sl: %s' % str(last_syms_sl))
		log(cur_func,lev_debug,'last_syms_nf: %s' % str(last_syms_nf))
		log(cur_func,lev_debug,'last_syms_nf_sl: %s' % str(last_syms_nf_sl))
		log(cur_func,lev_debug,'sent_nos: %s' % str(sent_nos))
		log(cur_func,lev_debug,'words_num: %d' % words_num)
		log(cur_func,lev_debug,'pos_sl: %s' % str(pos_sl))
		log(cur_func,lev_debug,'sents_num: %d' % sents_num)
		log(cur_func,lev_debug,'sents: %s' % str(sents))
		log(cur_func,lev_debug,'sents_nf: %s' % str(sents_nf))
		log(cur_func,lev_debug,'sents_pos: %s' % str(sents_pos))
		log(cur_func,lev_debug,'sents_pos_nf: %s' % str(sents_pos_nf))
		log(cur_func,lev_debug,'sents_pos_sl: %s' % str(sents_pos_sl))
		log(cur_func,lev_debug,'sents_pos_nf_sl: %s' % str(sents_pos_nf_sl))
		log(cur_func,lev_debug,'sents_sym_len: %s' % str(sents_sym_len))
		log(cur_func,lev_debug,'sents_word_len: %s' % str(sents_word_len))
		log(cur_func,lev_debug,'sents_text: %s' % str(sents_text))
		log(cur_func,lev_debug,'sents_text_nf: %s' % str(sents_text_nf))
		log(cur_func,lev_debug,'detailed_declined: %s' % str(detailed_declined))
		#--------------------------------------------------------------------------
		text_db={'len':maxi+1,'words_num':words_num,'words':words,'words_nf':words_nf,
				'first_syms':first_syms,'first_syms_nf':first_syms_nf,'first_syms_sl':first_syms_sl,
				'first_syms_nf_sl':first_syms_nf_sl,'last_syms':last_syms,'last_syms_sl':last_syms_sl,
				'last_syms_nf':last_syms_nf,'last_syms_nf_sl':last_syms_nf_sl,'nls':nls,'dlbs':dlbs,
				'spaces':spaces,'spaces_sl':spaces_sl,'sent_nos':sent_nos,'pos_sl':pos_sl,'text':text,
				'sents_num':sents_num,'sents_pos':sents_pos,'sents_pos_nf':sents_pos_nf,'sents':sents,
				'sents_nf':sents_nf,'sents_pos_sl':sents_pos_sl,'sents_pos_nf_sl':sents_pos_nf_sl,
				'sents_sym_len':sents_sym_len,'sents_word_len':sents_word_len,'sents_text':sents_text,
				'sents_text_nf':sents_text_nf,'declined':detailed_declined}
		return text_db
				
# Привести список вида [[sent_no,pos1,sent_no,pos2]] к виду, понимаемому Tk
def list2tk(lst):
	cur_func=sys._getframe().f_code.co_name
	tk_lst=[]
	# Проверка целостности входных данных
	check_type(cur_func,lst,globs['mes'].type_lst)
	for i in range(len(lst)):
		check_type(cur_func,lst[i],globs['mes'].type_lst)
		assert(len(lst[i])==4)
		check_args(cur_func,[[lst[i][0],globs['mes'].type_int],[lst[i][1],globs['mes'].type_int],[lst[i][2],globs['mes'].type_int],[lst[i][3],globs['mes'].type_int]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		for i in range(len(lst)):
			tk_lst+=[[convert2tk(lst[i][0],lst[i][1],Even=False),convert2tk(lst[i][2],lst[i][3],Even=True)]]
		log(cur_func,lev_debug,str(tk_lst))
	return tk_lst

# Привести в вид, понимаемый виджетом Tk, список вида [sent_no,pos1]
def convert2tk(sent,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	tk_str='1.0'
	check_args(cur_func,[[sent,globs['mes'].type_int],[pos,globs['mes'].type_int],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if Even:
			tk_str=str(sent+1)+'.'+str(pos+1)
		else:
			tk_str=str(sent+1)+'.'+str(pos)
		log(cur_func,lev_debug,str(tk_str))
	return tk_str
	
# Скопировать в буфер обмена
def clipboard_copy(line):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		line=str(line)
		try:
			root.clipboard_clear()
			root.clipboard_append(line)
			# Указать режиму буфера, что переводить измененный буфер не надо
			globs['IgnorePaste']=True
		except:
			# Иначе в окне не сработают горячие клавиши
			set_keyboard_layout('en')
			text_field(title=globs['mes'].clipboard_copy_failure,user_text=line,SelectAll=True,ReadOnly=True)
			line=err_mes_copy
			log(cur_func,lev_debug,str(line))
		
# Вернуть веб-страницу онлайн-словаря с термином
def get_online_article(db,IsURL=False,Silent=False,Critical=False,Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# db['search'] требуется всегда, даже если на входе URL
		# Если на входе URL, то читается db['url'], если же на входе строка, то читается db['search'] и создается db['url']
		if not IsURL:
			# Поскольку Multitran использует кодировку windows-1251, необходимо использовать ее. Поскольку некоторые символы не кодируются в globs['var']['win_encoding'] корректно, оставляем для них кодировку UTF-8.
			try:
				request_encoded=db['search'].encode(globs['var']['win_encoding'])
			except:
				request_encoded=bytes(db['search'],encoding=default_encoding)
			# Некоторые версии питона принимают 'encode('windows-1251')', но не 'encode(encoding='windows-1251')'
			db['url']=online_request(globs['var']['online_dic_url'],request_encoded)
		db['page']=''
		db['html']=''
		while db['page']=='':
			Success=False
			# Загружаем страницу
			try:
				# Если загружать страницу с помощью "page=urllib.request.urlopen(my_url)", то в итоге получится HTTPResponse, что полезно только для удаления тэгов JavaScript. Поскольку мы вручную удаляем все лишние тэги, то на выходе нам нужна строка.
				db['page']=urllib.request.urlopen(db['url']).read()
				log(cur_func,lev_info,globs['mes'].ok % db['search'])
				Success=True
			except:
				log(cur_func,lev_warn,globs['mes'].failed % db['search'])
				#mestype(cur_func,globs['mes'].webpage_unavailable,Silent=Silent,Critical=Critical)
				if not Question(cur_func,globs['mes'].webpage_unavailable_ques):
					if Standalone:
						sys.exit()
					else:
						break
			if Success: # Если страница не загружена, то понятно, что ее кодировку изменить не удастся
				try:
					# Меняем кодировку globs['var']['win_encoding'] на нормальную
					db['page']=db['page'].decode(globs['var']['win_encoding'])
					db['html']=db['page']
				except:
					mestype(cur_func,globs['mes'].wrong_html_encoding,Silent=Silent,Critical=Critical)
	return db
	
# Конвертировать строку в целое число
def str2int(line):
	cur_func=sys._getframe().f_code.co_name
	par=0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			par=int(line)
		except:
			log(cur_func,lev_err,globs['mes'].convert_to_int_failure % line)
		log(cur_func,lev_debug,str(par))
	return par

# Конвертировать строку с позицией Tkinter вида '1.20' в список вида [sent_no,pos_no]
def convertFromTk(line,Even=False):
	cur_func=sys._getframe().f_code.co_name
	lst=[0,0]
	check_args(cur_func,[[line,globs['mes'].type_str],[Even,globs['mes'].type_bool]])
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		num_lst=line.split('.')
		assert(len(num_lst)==2)
		sent=str2int(num_lst[0])
		check_type(cur_func,sent,globs['mes'].type_int)
		pos=str2int(num_lst[1])
		check_type(cur_func,pos,globs['mes'].type_int)
		if Even:
			lst=[sent-1,pos-1]
		else:
			lst=[sent-1,pos]
		# Tkinter позволяет выделять так, что конец придется на первый (=нулевой) символ в начале предложения, и из-за Even получится отрицательное число. Компенсируем это.
		for i in range(len(lst)):
			if lst[i] < 0:
				log(cur_func,lev_warn,globs['mes'].negative % lst[i])
				lst[i]=0
		log(cur_func,lev_debug,str(lst))
	return lst

# Конвертировать числовую позицию формата int в позицию в формате Tkinter
# Пример: 20 => '1.20'
def pos2tk(text_db,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	tk_pos='1.0'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# < при len=maxi+1 и <= при len=maxi
		assert(pos < text_db['len'])
		#elem=text_db['pos_sl'][pos-1]
		# 2014-11-15 11:52
		elem=text_db['pos_sl'][pos]
		tk_pos=convert2tk(elem[0],elem[1],Even=Even)
		log(cur_func,lev_debug,str('%d => %s' % (pos,tk_pos)))
	return tk_pos

# Конвертировать позицию в формате Tkinter в числовую позицию формата int
# Пример: '1.20' => 20
def tk2pos(text_db,tk_pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	found=0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Пример: [0,10]
		pos_sl_no=convertFromTk(tk_pos,Even=Even)
		# Выделение в Tkinter может выйти за пределы самого текста, поэтому заранее определяем правую границу.
		found=len(text_db['pos_sl'])
		for i in range(len(text_db['pos_sl'])):
			if pos_sl_no==text_db['pos_sl'][i]:
				found=i
				break
		log(cur_func,lev_debug,str('%s => %s' % (tk_pos,str(found))))
	return found
	
# Выбор одного элемента из списка
def SelectFromList(title,cur_mes,list_array,Insist=False,Silent=False,Critical=True,MakeLower=False):
	cur_func=sys._getframe().f_code.co_name
	log(cur_func,lev_debug,globs['mes'].title % str(title))
	log(cur_func,lev_debug,globs['mes'].mes % str(cur_mes))
	log(cur_func,lev_debug,globs['mes'].lst % str(list_array))
	check_args(cur_func,[[title,globs['mes'].type_str],[cur_mes,globs['mes'].type_str],[list_array,globs['mes'].type_lst]])
	choice=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Если на входе пустой список, на выходе выдаем ''
		if list_array==[]:
			log(cur_func,lev_warn,globs['mes'].empty_lists_not_allowed)
		# Если список включает только 1 файл, вывести его сразу
		elif len(list_array)==1:
			choice=list_array[0]
		elif Insist:
			while empty(choice):
				root.withdraw()
				try:
					choice=eg.choicebox(cur_mes,title,list_array) #MakeLower=MakeLower
				except:
					mestype(cur_func,globs['mes'].eg,Silent=Silent,Critical=Critical)
				root.deiconify()
				if empty(choice):
					Warning(cur_func,globs['mes'].force_choice)
		else:
			root.withdraw()
			try:
				choice=eg.choicebox(cur_mes,title,list_array) #MakeLower=MakeLower
			except:
				mestype(cur_func,globs['mes'].eg,Silent=Silent,Critical=Critical)
			root.deiconify()
			if empty(choice) and Critical:
				globs['AbortAll']=True
		log(cur_func,lev_debug,str(choice))
	return choice

# Удалить файл (но не каталог)
def delete(file,Silent=False,Critical=False):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		if os.path.exists(file):
			try:
				os.remove(file)
				log(cur_func,lev_info,globs['mes'].deleting % file)
			except:
				Success=False
				mestype(cur_func,globs['mes'].file_del_failure2 % file,Silent=Silent,Critical=Critical)
		else:
			Success=False
			mestype(cur_func,globs['mes'].file_del_failure3 % file,Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,str(Success))
	return Success

# Проверить существование файла и выйти в случае отказа от перезаписи
def rewrite(file,Force=False,Silent=False,Critical=False):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		# Существование файла здесь не является критическим параметром, что позволяет использовать 'if rewrite(file):' для несуществующих файлов.
		if os.path.exists(file):
			if Force:
				Warning(cur_func,globs['mes'].rewrite_warning % file)
				# Используется вторая проверка, поскольку пользователь может вручную удалить файл после предупреждения
				if os.path.exists(file):
					Success=delete(file,Silent=False,Critical=Critical)
			else: 
				if Question(cur_func,globs['mes'].rewrite_ques % file):
					if os.path.exists(file):
						Success=delete(file,Silent=False,Critical=Critical)
				else:
					Success=False
		log(cur_func,lev_debug,str(Success))
	return Success

# Записать текст в файл в режиме 'write' или 'append'
# Critical распространяется только на попытку записи файла. Проверка режима обязана быть Critical
def write_file(file,text,mode='w',Silent=False,Critical=False,AskRewrite=True):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	check_type(cur_func,file,globs['mes'].type_str)
	check_type(cur_func,mode,globs['mes'].type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		if mode!='w' and mode!='a':
			Success=False
			mestype(cur_func,globs['mes'].wrong_mode % mode,Silent=False,Critical=True)
		# Может создаваться новый файл, поэтому проверку существования не делаем
		if AskRewrite:
			Success=rewrite(file)
		if Success:
			try:
				with open(file,mode,encoding=default_encoding) as f:
					f.write(text)
				log(cur_func,lev_info,globs['mes'].file_written % file)
			except:
				Success=False
				mestype(cur_func,globs['mes'].file_write_failure % file,Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,str(Success))
	return Success

# Удостовериться, что входная строка имеет какую-то ценность
def empty(my_input):
	cur_func=sys._getframe().f_code.co_name
	par=True # При отмене всех задач должно возвращаться True, иначе 'if not empty()' в таких случаях возвращает True!
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if my_input=='' or my_input==None or my_input==[] or my_input==() or my_input=={} or my_input in cmd_err_mess:
			par=True
		else:
			par=False
		log(cur_func,lev_debug,str(par))
	return par

# Диалог сохранения файла
def dialog_save_file(text,filetypes=((globs['mes'].plain_text,'.txt'),(globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*')),Critical=True):
	cur_func=sys._getframe().f_code.co_name
	file=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		options={}
		options['initialfile']=''
		options['filetypes']=filetypes
		options['title']=globs['mes'].save_as
		# Если реализовать выбор файла через EasyGui, получим ошибку при выборе каталога, защищенного от записи, не ловится даже в try-except, получаем "alloc: invalid block: 0xb33c040: c0 b Aborted"
		#file=eg.filesavebox(msg=globs['mes'].select_file,filetypes=mask)
		try:
			file=dialog.asksaveasfilename(**options)
		except:
			mestype(cur_func,globs['mes'].file_sel_failed,Critical=Critical)
		# dialog при пустом выборе возвращает (), который мы заменяем на '', потому что возвращаемое значение должно представлять собой строку, а не кортеж (иначе, например, такие процедуры как exist() будут вылетать)
		if file==():
			file=''
		if empty(file):
			if Critical:
				globs['AbortAll']=True
		else:
			# На Linux добавляется расширение после asksaveasfilename, на Windows - нет. Мы не можем понять, что выбрал пользователь, поскольку asksaveasfilename возвращает только имя файла. Поэтому, если никакого разрешения нет, добавляем '.htm' в надежде, что браузер нормально откроет текстовый файл.
			# ВНИМАНИЕ: это сработает для обычного текста и для веб-страниц, с другими типами могут быть проблемы.
			if empty(get_ext(file)):
				file+='.htm'
			# rewrite (AskRewrite) не задействуем, поскольку наличие файла уже проверяется на этапе asksaveasfilename()
			write_file(file,text,mode='w',Silent=False,Critical=Critical,AskRewrite=False)
	log(cur_func,lev_debug,globs['mes'].writing % str(file))
	return file

# Конструктор для создания окна для манипуляции текстом
def text_field(title=globs['mes'].text,user_text=err_mes_empty_input,CheckSpelling=False,GoTo='',Insist=False,SelectAll=False,ReadOnly=False,Small=False,TrimEnd=False): # Edit=True равноценно user_text!=err_mes_empty_input
	cur_func=sys._getframe().f_code.co_name
	func_res=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		top, res = tk.Toplevel(root), [None]
		if globs['bool']['AlwaysMaximize'] and not Small:
			if sys_type=='lin':
				top.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				top.wm_state(newstate='zoomed')
		def close_top(event):
			top.destroy()
			root.deiconify()
		def callback(event):
			if Small:
				returned=widget.get()
			elif ReadOnly:
				returned=user_text
			else:
				returned=widget.get(1.0,'end')
			# На входе без ошибок (пока) принимаются список и строка
			if get_obj_type(returned,Verbal=True)==globs['mes'].type_str:
				returned=returned.strip(dlb)
			res[0]=returned
			close_top(None)
		def select_all(event):
			if Small:
				widget.select_clear()
				widget.select_range(0,'end')
			else:
				widget.tag_add('sel','1.0','end')
				widget.mark_set('insert','1.0')
			return 'break'
		root.withdraw()
		title+=' '+my_program_title
		top.title(title)
		top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=globs['var']['icon_main']))
		# Позволяет удалять пробел и пунктуацию с конца, что полезно при некорректной обработке Ctrl+Shift+->
		if TrimEnd and not Small:
			user_text=delete_end_punc(user_text)
		if Small:
			widget=tk.Entry(top,font=globs['var']['font_style'])
		else:
			scrollbar=tk.Scrollbar(top,jump=0)
			widget=tk.Text(top,height=10,font=globs['var']['font_style'],wrap='word',yscrollcommand=scrollbar.set)
		if not empty(user_text):
			widget.insert('end',user_text)
		if ReadOnly and globs['bool']['ReadOnlyProtection'] and not Small:
			widget.config(state='disabled')
		if not Small:
			# Позволяет использовать мышь для управления скроллбаром
			scrollbar.config(command=widget.yview)
			scrollbar.pack(side='right',fill='y')
		create_binding(widget=widget,binding='<Return>',action=callback)
		create_binding(widget=widget,binding='<KP_Enter>',action=callback)
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
		if GoTo!='' and not Small:
			try:
				goto_pos=widget.search(GoTo,'1.0','end')
				widget.mark_set('goto',goto_pos)
				widget.mark_set('insert',goto_pos)
				widget.yview('goto')
			except:
				log(cur_func,lev_err,globs['mes'].shift_screen_failure % 'goto')
		else:
			try:
				widget.mark_set('insert','1.0')
			except:
				log(cur_func,lev_err,globs['mes'].cursor_insert_failure)
		if SelectAll:
			select_all(None)
		elif Small and not ReadOnly:
			select_all(None)
		create_binding(widget=widget,binding='<Control-a>',action=select_all)
		create_binding(widget=widget,binding='<Control-A>',action=select_all)
		globs['cur_widget']=widget
		if Small or ReadOnly:
			create_binding(widget=widget,binding='<Escape>',action=close_top)
		top.wait_window(top)
		func_res=res[0]
		log(cur_func,lev_debug,str(func_res))
		if Insist:
			if empty(func_res):
				ErrorMessage(cur_func,globs['mes'].empty_text)
			# Предотвратить возможные ошибки при глобальной отмене
		if func_res==None:
			func_res=''
	return func_res
	
# Создать переменные, которые основываются на ключах конфига, но не входят в него
def additional_keys():
	cur_func=sys._getframe().f_code.co_name
	# Это второстепенный ключ, указывать его в конфиге не надо
	globs['IgnorePaste']=False

# Загрузить все конфигурационные файлы
def read_configs(Silent=False,Critical=False):
	cur_func=sys._getframe().f_code.co_name
	Success=False
	total_keys=0
	changed_keys=0
	missing_keys=0
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		Success=True
		# Должен лежать в одном каталоге с программой
		# Руководство питона предлагает использовать разные методы для разных платформ: http://docs.python.org/2/library/os.path.html
		cur_mes=''
		if not exist(globs['mclient_config'],Silent=Silent,Critical=Critical):
			Success=False
		if Success:
			try:
				globs['config_parser'].readfp(codecs.open(globs['mclient_config'],'r','utf-8'))
			except:
				Success=False
				mestype(cur_func,globs['mes'].invalid_config % globs['mclient_config'],Silent=Silent,Critical=Critical)
			if Success:
				if sys_type=='lin':
					config_section=SectionLinuxSettings
				elif sys_type=='win':
					config_section=SectionWindowsSettings
				elif sys_type=='mac':
					config_section=SectionMacSettings
				# Сокращенное название раздела в globs
				config_section_abbr=sys_type
				#--------------------------------------------------------------
				# Загрузка раздела SectionLinuxSettings/SectionWindowsSettings/SectionMacSettings
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[sys_type]:
						total_keys+=1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].get(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys+=1
								globs[config_section_abbr][config_option]=new_config_value
						else:
							Success=False
							missing_keys+=1
							cur_mes+=globs['mes'].no_config_option % (config_option,config_section)+dlb
				else:
					Success=False
					cur_mes+=globs['mes'].no_config_section % config_section+dlb
				#--------------------------------------------------------------
				# Загрузка раздела SectionVariables
				config_section=SectionVariables
				config_section_abbr='var'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					#----------------------------------------------------------
					# 'ui_lang' - это единственный параметр 1-го уровня вложенности globs, который можно менять при загрузке конфига (иначе придется создавать globs['var'] раньше, чем хотелось бы)
					config_option='ui_lang'
					total_keys+=1
					if globs['config_parser'].has_option(config_section,config_option):
						new_config_value=globs['config_parser'].get(config_section,config_option)
						# Обратить внимание, что раздел указывать не нужно
						if globs[config_option] != new_config_value:
							log(cur_func,lev_info,globs['mes'].key_changed % config_option)
							changed_keys+=1
							toggle_ui_lang()
					else:
						Success=False
						missing_keys+=1
						cur_mes+=globs['mes'].no_config_option % (config_option,config_section)+dlb
					#----------------------------------------------------------
					for config_option in globs[config_section_abbr]:
						total_keys+=1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].get(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys+=1
								globs[config_section_abbr][config_option]=new_config_value
						else:
							Success=False
							missing_keys+=1
							cur_mes+=globs['mes'].no_config_option % (config_option,config_section)+dlb
				else:
					Success=False
					cur_mes+=globs['mes'].no_config_section % config_section+dlb
				#--------------------------------------------------------------
				# Загрузка раздела SectionIntegers
				config_section=SectionIntegers
				config_section_abbr='int'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys+=1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].getint(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys+=1
								globs[config_section_abbr][config_option]=new_config_value
						else:
							Success=False
							missing_keys+=1
							cur_mes+=globs['mes'].no_config_option % (config_option,config_section)+dlb
				else:
					Success=False
					cur_mes+=globs['mes'].no_config_section % config_section+dlb
				#--------------------------------------------------------------
				# Загрузка раздела SectionFloatings
				config_section=SectionFloatings
				config_section_abbr='float'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys+=1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].getfloat(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys+=1
								globs[config_section_abbr][config_option]=new_config_value
						else:
							Success=False
							missing_keys+=1
							cur_mes+=globs['mes'].no_config_option % (config_option,config_section)+dlb
				else:
					Success=False
					cur_mes+=globs['mes'].no_config_section % config_section+dlb
				#--------------------------------------------------------------
				# Загрузка раздела SectionBooleans
				config_section=SectionBooleans
				config_section_abbr='bool'
				if globs['config_parser'].has_section(config_section):
					log(cur_func,lev_info,globs['mes'].section_keys % (config_section,len(globs[config_section_abbr])))
					for config_option in globs[config_section_abbr]:
						total_keys+=1
						if globs['config_parser'].has_option(config_section,config_option):
							# Обновить параметр по умолчанию на параметр из конфигурационного файла
							new_config_value=globs['config_parser'].getboolean(config_section,config_option)
							if globs[config_section_abbr][config_option] != new_config_value:
								log(cur_func,lev_info,globs['mes'].key_changed % config_option)
								changed_keys+=1
								globs[config_section_abbr][config_option]=new_config_value
						else:
							Success=False
							missing_keys+=1
							cur_mes=globs['mes'].no_config_option % (config_option,config_section)+dlb
				else:
					Success=False
					cur_mes+=globs['mes'].no_config_section % config_section+dlb
		#----------------------------------------------------------------------
		# Данные действия необходимо производить вне зависимости от успеха в чтении конфига и именно после него
		# Эти вспомогательные ключи зависят от основных и не обновляются самостоятельно. Принудительно обновляем их после чтения основных ключей.
		additional_keys()
		for key in globs['var']:
			if key.startswith('icon_'):
				globs['var'][key]=globs['bin_dir']+sysdiv+globs['var'][key]
		#----------------------------------------------------------------------
		if Critical and not Success:
			sys.exit()
		if not Success:
			cur_mes=globs['mes'].wrong_configs_structure+dlb+dlb+cur_mes
			cur_mes+=dlb+globs['mes'].default_config
			text_field(title=globs['mes'].errors,user_text=cur_mes,ReadOnly=True)
		log(cur_func,lev_debug,str(Success))
	log(cur_func,lev_info,globs['mes'].config_stat % (total_keys,changed_keys,missing_keys))
	return Success

# Название типа на русском
def obj_type_verbal(obj_type_str,IgnoreErrors=False):
	cur_func=sys._getframe().f_code.co_name
	obj_type_str=str(obj_type_str)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if obj_type_str=='str':
			obj_type_str=globs['mes'].type_str
		elif obj_type_str=='list':
			obj_type_str=globs['mes'].type_lst
		elif obj_type_str=='dict':
			obj_type_str=globs['mes'].type_dic
		elif obj_type_str=='tuple':
			obj_type_str=globs['mes'].type_tuple
		elif obj_type_str=='set' or obj_type_str=='frozenset':
			obj_type_str=globs['mes'].type_set
		elif obj_type_str=='int':
			obj_type_str=globs['mes'].type_int
		elif obj_type_str=='long':
			obj_type=globs['mes'].type_long_int
		elif obj_type_str=='float':
			obj_type_str=globs['mes'].type_float
		elif obj_type_str=='complex':
			obj_type_str=globs['mes'].type_complex
		elif obj_type_str=='bool':
			obj_type_str=globs['mes'].type_bool
		elif IgnoreErrors:
			pass
		else:
			ErrorMessage(cur_func,globs['mes'].unknown_mode % (obj_type_str,'str, list, dict, tuple, set, frozenset, int, long, float, complex, bool'))
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str

# Вернуть тип параметра
def get_obj_type(obj,Verbal=True,IgnoreErrors=False):
	cur_func=sys._getframe().f_code.co_name
	obj_type_str=''
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		obj_type_str=str(type(obj))
		obj_type_str=obj_type_str.replace("<class '",'')
		obj_type_str=obj_type_str.replace("'>",'')
		# int, float, str, list, dict, tuple, NoneType
		if Verbal:
			obj_type_str=obj_type_verbal(obj_type_str,IgnoreErrors=IgnoreErrors)
		#log(cur_func,lev_debug,obj_type_str)
	return obj_type_str

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# mclient non-shared code
# Convert HTML entities to UTF-8 and perform other necessary operations
def prepare_page(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			html_parser = html.parser.HTMLParser()
			db['page']=html_parser.unescape(db['page'])
		except:
			log(cur_func,lev_err,globs['mes'].html_conversion_failure)
		# It is not clear why .replace does not replace all suitable elements
		db['page']=db['page'].replace('\r\n','')
		db['page']=db['page'].replace('\n','')
		db['page']=db['page'].replace('\xa0',' ')
		while '  ' in db['page']:
			db['page']=db['page'].replace('  ',' ')
		db['page']=db['page'].replace(nbspace+'<','<')
		db['page']=db['page'].replace(' <','<')
		db['page']=db['page'].replace('>'+nbspace,'>')
		db['page']=db['page'].replace('> ','>')
		# Remove tags <p>, </p>, <b> and </b>, because they can be inside hyperlinks
		db['page']=db['page'].replace('<p>','')
		db['page']=db['page'].replace('</p>','')
		db['page']=db['page'].replace('<b>','')
		db['page']=db['page'].replace('</b>','')
		# Remove symbols '<' and '>' that do not define tags
		db['page']=list(db['page'])
		i=0
		TagOpen=False
		while i < len(db['page']):
			if db['page'][i]=='<':
				if TagOpen:
					log(cur_func,lev_debug,globs['mes'].deleting_useless_elem % (i,db['page'][i]))
					if i >= 10 and i < len(db['page'])-10:
						log(cur_func,lev_debug,globs['mes'].context % ''.join(db['page'][i-10:i+10]))
					del db['page'][i]
					i-=1
				else:
					TagOpen=True
			if db['page'][i]=='>':
				if not TagOpen:
					log(cur_func,lev_info,globs['mes'].deleting_useless_elem % (i,db['page'][i]))
					if i >= 10 and i < len(db['page'])-10:
						log(cur_func,lev_info,globs['mes'].context % ''.join(db['page'][i-10:i+10]))
					del db['page'][i]
					i-=1
				else:
					TagOpen=False
			i+=1
		db['page']=''.join(db['page'])
		db['len_page']=len(db['page'])
		log(cur_func,lev_debug,"db['page']: '%s'" % db['page'])
		log(cur_func,lev_debug,"db['len_page']: %d" % db['len_page'])
	return db

# Analyse tags and collect the information on them
def analyse_tags(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		start_time=time()
		db=tags_pos(db)
		db=extract_tags(db)
		db=remove_useless_tags(db)
		db=extract_tag_contents(db)
		end_time=time()
		log(cur_func,lev_info,globs['mes'].tag_analysis_timer % str(end_time-start_time))
	return db
	
# Create a list with positions of signs '<' and '>'
def tags_pos(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		tag_borders=[]
		i=0
		while i < db['len_page']:
			# Signs '<' and '>' as such can cause serious problems since they can occur in invalid cases like "perform >>> conduct >> carry out (vbadalov)". The following algorithm is also not 100% precise but is better.
			if db['page'][i]=='<' or db['page'][i]=='>':
				tag_borders.append(i)
			i+=1
		if len(tag_borders) % 2 != 0:
			log(cur_func,lev_warn,globs['mes'].wrong_tag_num % len(tag_borders))
			if len(tag_borders) > 0:
				del tag_borders[-1]
			else:
				log(cur_func,lev_warn,globs['mes'].tag_borders_empty)
		tmp_borders=[]
		i=0
		while i < len(tag_borders):
			uneven=tag_borders[i]
			i+=1
			even=tag_borders[i]
			i+=1
			tmp_borders+=[[uneven,even]]
		db['tag_borders']=tmp_borders
		db['len_tag_borders']=len(db['tag_borders'])
		log(cur_func,lev_debug,"db['tag_borders']: %s" % str(db['tag_borders']))
		log(cur_func,lev_debug,"db['len_tag_borders']: %d" % db['len_tag_borders'])
	return db
	
# Extract fragments inside signs '<' and '>'
def extract_tags(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['tags']=[]
		for i in range(db['len_tag_borders']):
			# +1 because of slice peculiarities
			pos1=db['tag_borders'][i][0]
			pos2=db['tag_borders'][i][1]+1
			db['tags'].append(db['page'][pos1:pos2])
			log(cur_func,lev_debug,globs['mes'].extracting_tag % db['tags'][-1])
		db['len_tags']=len(db['tags'])
		log(cur_func,lev_info,globs['mes'].tags_found % (db['len_tags']))
		log(cur_func,lev_debug,str(db['tags']))
	return db
	
# Create a list of on-screen text elements for each useful tag
def extract_tag_contents(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		#--------------------------------------------------------------------------
		# Assigning initial values
		# It is much easier to debug results if we separate types just before showing them in tkinter
		db['all']={}
		db['all']['phrases']=[]
		db['all']['types']=[]
		db['all']['pos']=[]
		db['all']['url']=[]
		#--------------------------------------------------------------------------
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
		#--------------------------------------------------------------------------
		for i in range(db['len_tags']):
			EntryMatch=False
			url=online_url_safe
			# Extracting dictionary abbreviations
			if db['tags'][i].startswith(tag_pattern1):
				tmp_str=db['tags'][i]
				tmp_str=tmp_str.replace(tag_pattern1,'',1)
				tmp_str=re.sub('".*','',tmp_str)
				if tmp_str=='' or tmp_str==' ':
					log(cur_func,lev_warn,globs['mes'].wrong_tag % db['tags'][i])
				else:
					db['all']['phrases'].append(tmp_str)
					db['all']['types'].append('dics')
					pos1=db['tag_borders'][i][0]+len(tag_pattern1)-1
					pos2=pos1+len(tmp_str)-1
					db['all']['pos']+=[[pos1,pos2]]
					EntryMatch=True
			# Extracting terms
			if db['tags'][i].startswith(tag_pattern2):
				# It is reasonable to bind URLs to terms only, but we want the number of URLs to match db['all']['num'], moreover, extra URLs can appear useful.
				if i+1 < db['len_tags']:
					TermMatch=True
					pos1=db['tag_borders'][i][1]+1
					pos2=db['tag_borders'][i+1][0]-1
					if pos1 >= db['len_page']:
						log(cur_func,lev_warn,globs['mes'].tag_near_text_end % db['tags'][i])
					else:
						if tag_pattern7 in db['tags'][i+1] or tag_pattern8 in db['tags'][i+1]:
							tmp_str=db['page'][pos1:pos2+1]
							# If we see symbols '<' or '>' there for some reason, then there is a problem in the tag extraction algorithm. We can make manual deletion of '<' and '>' there.
							if tmp_str=='' or tmp_str==' ':
								TermMatch=False
								log(cur_func,lev_warn,globs['mes'].empty_tag_contents % db['tags'][i])
							if TermMatch:
								db['all']['phrases'].append(tmp_str)
								db['all']['types'].append('terms')
								db['all']['pos']+=[[pos1,pos2]]
								EntryMatch=True
						else:
							TermMatch=False
						# Extracting URL
						url=db['tags'][i].replace(tag_pattern2,'',1)
						# We need re because of such cases as "<a href="m.exe?t=74188_2_4&s1=faute">ошибка"
						url=re.sub('\"\>.*','">',url)
						if url.endswith(tag_pattern8):
							url=url.replace(tag_pattern8,'')
							url=online_url_root+url
						else:
							log(cur_func,lev_warn,globs['mes'].url_extraction_failure % url)
						if not TermMatch:
							log(cur_func,lev_warn,globs['mes'].useless_url % url)
				else:
					log(cur_func,lev_warn,globs['mes'].last_tag % db['tags'][i])
					TermMatch=False
			# Extracting comments
			if db['tags'][i]==tag_pattern3 or db['tags'][i]==tag_pattern5 or db['tags'][i]==tag_pattern9:
				pos1=db['tag_borders'][i][1]+1
				if pos1 >= db['len_page']:
					log(cur_func,lev_warn,globs['mes'].tag_near_text_end % db['tags'][i])
				else:
					if i+1 < db['len_tags']:
						pos2=db['tag_borders'][i+1][0]-1
					else:
						log(cur_func,lev_warn,globs['mes'].last_tag % db['tags'][i])
						if db['len_tag_borders'] > 0:
							pos2=db['tag_borders'][-1][1]
						else:
							pos2=pos1
							log(cur_func,lev_warn,globs['mes'].tag_borders_empty)
					tmp_str=db['page'][pos1:pos2+1]
					# Sometimes, the tag contents is just '('. We remove it, so the final text does not look like '( user_name'
					if tmp_str=='' or tmp_str==' ' or tmp_str=='|' or tmp_str=='(':
						log(cur_func,lev_warn,globs['mes'].empty_tag_contents % db['tags'][i])
					else:
						db['all']['phrases'].append(tmp_str)
						db['all']['types'].append('comments')
						db['all']['pos']+=[[pos1,pos2]]
						EntryMatch=True
			if EntryMatch:
				log(cur_func,lev_debug,globs['mes'].adding_url % url)
				db['all']['url'].append(url)
		db['all']['num']=len(db['all']['phrases'])
		#--------------------------------------------------------------------------
		# Deleting some common entries
		# We can also delete 'g-sort' here
		# ATTENTION: All types must be removed: 'phrases', 'types', 'pos', 'url'!
		if db['all']['num'] > 0:
			if db['all']['phrases'][0]=='Вход':
				del db['all']['phrases'][0]
				del db['all']['types'][0]
				del db['all']['pos'][0]
				del db['all']['url'][0]
				db['all']['num']-=1
			if db['all']['phrases'][0]=='Регистрация':
				del db['all']['phrases'][0]
				del db['all']['types'][0]
				del db['all']['pos'][0]
				del db['all']['url'][0]
				db['all']['num']-=1
			if db['all']['num'] > 0:
				if db['all']['phrases'][-1]=='Сообщить об ошибке':
					del db['all']['phrases'][-1]
					del db['all']['types'][-1]
					del db['all']['pos'][-1]
					del db['all']['url'][-1]
					db['all']['num']-=1
			if db['all']['num'] > 0:
				if db['all']['phrases'][-1]=='Изменить':
					del db['all']['phrases'][-1]
					del db['all']['types'][-1]
					del db['all']['pos'][-1]
					del db['all']['url'][-1]
					db['all']['num']-=1
			if db['all']['num'] > 0:
				if db['all']['phrases'][-1]=='Удалить':
					del db['all']['phrases'][-1]
					del db['all']['types'][-1]
					del db['all']['pos'][-1]
					del db['all']['url'][-1]
					db['all']['num']-=1
			if db['all']['num'] > 0:
				if db['all']['phrases'][-1]=='Добавить':
					del db['all']['phrases'][-1]
					del db['all']['types'][-1]
					del db['all']['pos'][-1]
					del db['all']['url'][-1]
					db['all']['num']-=1
		else:
			log(cur_func,lev_warn,globs['mes'].entries_terms_empty)
		#--------------------------------------------------------------------------
		# Logging
		log(cur_func,lev_debug,"db['all']['num']: %d" % db['all']['num'])
		log(cur_func,lev_debug,"db['all']['phrases']: %s" % str(db['all']['phrases']))
		log(cur_func,lev_debug,"db['all']['types']: %s" % str(db['all']['types']))
		log(cur_func,lev_debug,"db['all']['pos']: %s" % str(db['all']['pos']))
		log(cur_func,lev_debug,"db['all']['url']: %s" % str(db['all']['url']))
		#--------------------------------------------------------------------------
		# Testing
		assert(db['all']['num']==len(db['all']['phrases']))
		assert(db['all']['num']==len(db['all']['types']))
		assert(db['all']['num']==len(db['all']['pos']))
		assert(db['all']['num']==len(db['all']['url']))
		# Human-readable representation
		if globs['bool']['InternalDebug']:
			res_mes=''
			for i in range(db['all']['num']):
				res_mes+="i: %d" % i+tab+db['all']['types'][i]+tab+db['all']['phrases'][i]+tab+str(db['all']['pos'][i])+tab+db['all']['url'][i]+dlb
			text_field(title=globs['mes'].db_all_check,user_text=res_mes,ReadOnly=True)
	return db
	
# Adjust positions of entries for pretty viewing
def prepare_search(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		# Removing unwanted values
		# We assume that a 'dic'-type entry shall be succeeded by a 'term'-type entry, not a 'comment'-type entry. Therefore, we delete 'comment'-type entries after 'dic'-type entries in order to ensure that dictionary abbreviations do not succeed full dictionary titles. We also can delete full dictionary titles and leave abbreviations instead.
		i=0
		while i < db['all']['num']:
			if i > 0:
				if db['all']['types'][i-1]=='dics' and db['all']['types'][i]=='comments':
					if '.' in db['all']['phrases'][i] or 'Макаров' in db['all']['phrases'][i] or 'Вебстер' in db['all']['phrases'][i] or 'Webster' in db['all']['phrases'][i] or 'Майкрософт' in db['all']['phrases'][i] or 'Microsoft' in db['all']['phrases'][i]:
						pos1=db['all']['pos'][i][0]
						pos2=db['all']['pos'][i][1]
						log(cur_func,lev_info,globs['mes'].deleting_useless_entry % db['page'][pos1:pos2+1])
						del db['all']['phrases'][i]
						del db['all']['types'][i]
						del db['all']['pos'][i]
						del db['all']['url'][i]
						db['all']['num']-=1
						i-=1
			i+=1
		#--------------------------------------------------------------------------
		# Adjusting values
		if db['all']['num'] > 0:
			delta=db['all']['pos'][0][0]
			delta_i=db['all']['pos'][0][1]-delta
			if delta_i < 0:
				log(cur_func,lev_err,globs['mes'].wrong_delta % (db['all']['pos'][0][1],delta))
				delta_i=abs(delta_i)
			db['all']['pos'][0]=[0,db['all']['pos'][0][1]-delta]
		else:
			log(cur_func,lev_warn,globs['mes'].db_all_empty)
		for i in range(db['all']['num']):
			if i > 0:
				delta=db['all']['pos'][i][0]-db['all']['pos'][i-1][1]
				if delta < 2:
					log(cur_func,lev_err,globs['mes'].intersection % (db['all']['pos'][i-1][0],db['all']['pos'][i-1][1],db['all']['pos'][i][0],db['all']['pos'][i][1]))
				delta_i=db['all']['pos'][i][1]-db['all']['pos'][i][0]
				if delta_i < 0:
					log(cur_func,lev_err,globs['mes'].wrong_delta % (db['all']['pos'][i][1],db['all']['pos'][i][0]))
					delta_i=abs(delta_i)
				db['all']['pos'][i][0]=db['all']['pos'][i-1][1]+2
				db['all']['pos'][i][1]=db['all']['pos'][i][0]+delta_i
		log(cur_func,lev_debug,"db['all']['pos']: %s" % str(db['all']['pos']))
		assert(db['all']['num']==len(db['all']['pos']))
		#--------------------------------------------------------------------------
		# Creating the final text
		# We update db['page'] there!
		if db['len_page'] > 0 and db['all']['num'] > 0:
			# Not "db['page']=' '*(db['len_page']-1)", because we have already shifted positions
			db['len_page']=db['all']['pos'][-1][1]
		else:
			log(cur_func,lev_warn,globs['mes'].no_entries)
		db['page']=' '*(db['len_page']-1)
		db['page']=list(db['page'])
		db['all']['sent_nos']=[]
		# Длина не привязана к db['all']['num']!
		db['all']['dlbs']={}
		db['all']['dlbs']['pos']=[]
		cur_sent=0
		for i in range(db['all']['num']):
			pos1=db['all']['pos'][i][0]
			pos2=db['all']['pos'][i][1]
			db['page'][pos1:pos2+1]=db['all']['phrases'][i]
			if db['all']['types'][i]=='dics' and pos1 > 0:
				db['page'][pos1-1]=dlb
				db['all']['dlbs']['pos'].append(pos1-1)
				cur_sent+=1
			db['all']['sent_nos'].append(cur_sent)
		db['page']=''.join(db['page'])
		db['len_page']=len(db['page'])
		assert(db['all']['num']==len(db['all']['sent_nos']))
		db['all']['dlbs']['num']=len(db['all']['dlbs']['pos'])
		log(cur_func,lev_debug,"db['all']['dlbs']['num']: %d" % db['all']['dlbs']['num'])
		log(cur_func,lev_debug,"db['all']['dlbs']['pos']: %s" % str(db['all']['dlbs']['pos']))
		if globs['bool']['InternalDebug']:
			res_mes=[]
			for i in range(db['all']['num']):
				pos1=db['all']['pos'][i][0]
				pos2=db['all']['pos'][i][1]
				res_mes.append(db['page'][pos1:pos2+1])
			res_mes=str(res_mes)
			res_mes+=dlb+dlb+"db['all']['pos']:"+dlb+str(db['all']['pos'])
			text_field(title=globs['mes'].db_check1,user_text=res_mes,ReadOnly=True)
			text_field(title=globs['mes'].db_check2,user_text=str(db['all']['dlbs']['pos']),ReadOnly=True)
		#--------------------------------------------------------------------------
		# Two adjacent terms are either separated with a coloured space, or with a semicolumn
		if not globs['bool']['TermsColoredSep']:
			# Separating terms with semicolumn instead of coloured background
			db['page']=list(db['page'])
			for i in range(db['all']['num']):
				if i < db['all']['num']-1:
					if db['all']['types'][i]=='terms' and db['all']['types'][i+1]=='terms':
						cur_pos=db['all']['pos'][i][1]+1
						db['page'].insert(cur_pos,';')
						j=i+1
						while j < db['all']['num']:
							db['all']['pos'][j][0]+=1
							db['all']['pos'][j][1]+=1
							j+=1
						for j in range(db['all']['dlbs']['num']):
							if db['all']['dlbs']['pos'][j] >= cur_pos:
								db['all']['dlbs']['pos'][j]+=1
			db['page']=''.join(db['page'])
			db['len_page']=len(db['page'])
			log(cur_func,lev_debug,"db['page']: %s" % db['page'])
			if globs['bool']['InternalDebug']:
				text_field(title="db['page']:",user_text=db['page'],ReadOnly=True)
		#--------------------------------------------------------------------------
		# Creating tkinter-specific values
		# list() is not enough!
		db['all']['pos_sl']=[]
		delta=0
		for i in range(db['all']['num']):
			if db['all']['pos'][i][0]-1 in db['all']['dlbs']['pos']:
				delta=db['all']['pos'][i][0]
			db['all']['pos_sl']+=[[db['all']['pos'][i][0]-delta,db['all']['pos'][i][1]-delta]]
			log(cur_func,lev_debug,globs['mes'].db_conv % (db['all']['pos'][i][0],db['all']['pos'][i][1],db['all']['pos_sl'][i][0],db['all']['pos_sl'][i][1]))
		log(cur_func,lev_debug,"db['all']['pos_sl']: %s" % str(db['all']['pos_sl']))
		assert(db['all']['num']==len(db['all']['pos_sl']))
		if db['all']['pos'] == db['all']['pos_sl']:
			log(cur_func,lev_warn,globs['mes'].db_alg)
		#--------------------------------------------------------------------------
		db['all']['tk']=[]
		for i in range(db['all']['num']):
			pos1=db['all']['pos_sl'][i][0]
			pos2=db['all']['pos_sl'][i][1]
			db['all']['tk']+=[[db['all']['sent_nos'][i],pos1,db['all']['sent_nos'][i],pos2]]
		db['all']['tk']=list2tk(db['all']['tk'])
		log(cur_func,lev_debug,"db['all']['tk']: %s" % str(db['all']['tk']))
		assert(db['all']['num']==len(db['all']['tk']))
		#--------------------------------------------------------------------------
		# In comparison with the last globs['bool']['InternalDebug']: +str(db['all']['tk'][i])
		if globs['bool']['InternalDebug']:
			res_mes=''
			for i in range(db['all']['num']):
				res_mes+="i: %d" % i+tab+db['all']['types'][i]+tab+db['all']['phrases'][i]+tab+str(db['all']['pos'][i])+tab+str(db['all']['pos_sl'][i])+tab+str(db['all']['tk'][i])+tab+db['all']['url'][i]+dlb
			text_field(title=globs['mes'].db_check3,user_text=res_mes,ReadOnly=True)
		#--------------------------------------------------------------------------
		# Mark terms borders for easy reading
		db['borders']=[]
		for i in range(db['all']['num']):
			if i > 0:
				if db['all']['types'][i-1]=='terms' and db['all']['types'][i]=='terms':
					sent_no1=db['all']['sent_nos'][i-1]
					sent_no2=db['all']['sent_nos'][i]
					pos1=db['all']['pos_sl'][i-1][1]+1
					pos2=db['all']['pos_sl'][i][0]-1
					db['borders']+=[[sent_no1,pos1,sent_no2,pos2]]
		if db['borders']!=[]:
			db['borders']=list2tk(db['borders'])
		log(cur_func,lev_debug,"db['borders']: %s" % str(db['borders']))
		#--------------------------------------------------------------------------
		# Create separate keys for article entries. Please note that they are NOT interconnected with db['all'] anymore and should be created just before showing an article.
		db['dics']={}
		db['dics']['phrases']=[]
		db['dics']['pos']=[]
		db['dics']['tk']=[]
		db['terms']={}
		db['terms']['phrases']=[]
		db['terms']['pos']=[]
		db['terms']['tk']=[]
		db['terms']['url']=[]
		db['comments']={}
		db['comments']['phrases']=[]
		db['comments']['pos']=[]
		db['comments']['tk']=[]
		for i in range(db['all']['num']):
			if db['all']['types'][i]=='dics':
				db['dics']['phrases'].append(db['all']['phrases'][i])
				db['dics']['pos'].append(db['all']['pos'][i])
				db['dics']['tk'].append(db['all']['tk'][i])
			elif db['all']['types'][i]=='terms':
				db['terms']['phrases'].append(db['all']['phrases'][i])
				db['terms']['pos'].append(db['all']['pos'][i])
				db['terms']['tk'].append(db['all']['tk'][i])
				db['terms']['url'].append(db['all']['url'][i])
			elif db['all']['types'][i]=='comments':
				db['comments']['phrases'].append(db['all']['phrases'][i])
				db['comments']['pos'].append(db['all']['pos'][i])
				db['comments']['tk'].append(db['all']['tk'][i])
			else:
				log(cur_func,lev_err,globs['mes'].unknown_type % str(db['all']['types'][i]))
		db['dics']['num']=len(db['dics']['phrases'])
		db['terms']['num']=len(db['terms']['phrases'])
		db['comments']['num']=len(db['comments']['phrases'])
		# Logging
		log(cur_func,lev_debug,"db['dics']['phrases']: %s" % str(db['dics']['phrases']))
		log(cur_func,lev_debug,"db['dics']['pos']: %s" % str(db['dics']['pos']))
		log(cur_func,lev_debug,"db['dics']['tk']: %s" % str(db['dics']['tk']))
		log(cur_func,lev_debug,"db['dics']['num']: %s" % str(db['terms']['num']))
		log(cur_func,lev_debug,"db['terms']['phrases']: %s" % str(db['terms']['phrases']))
		log(cur_func,lev_debug,"db['terms']['pos']: %s" % str(db['terms']['pos']))
		log(cur_func,lev_debug,"db['terms']['tk']: %s" % str(db['terms']['tk']))
		log(cur_func,lev_debug,"db['terms']['url']: %s" % str(db['terms']['url']))
		log(cur_func,lev_debug,"db['terms']['num']: %s" % str(db['terms']['num']))
		log(cur_func,lev_debug,"db['comments']['phrases']: %s" % str(db['comments']['phrases']))
		log(cur_func,lev_debug,"db['comments']['pos']: %s" % str(db['comments']['pos']))
		log(cur_func,lev_debug,"db['comments']['tk']: %s" % str(db['comments']['tk']))
		log(cur_func,lev_debug,"db['comments']['num']: %s" % str(db['comments']['num']))
		if globs['bool']['InternalDebug']:
			res_mes="db['dics']['num']:"+dlb+str(db['dics']['num'])+dlb+dlb
			res_mes+="db['dics']['phrases']:"+dlb+str(db['dics']['phrases'])+dlb+dlb
			res_mes+="db['dics']['pos']:"+dlb+str(db['dics']['pos'])+dlb+dlb
			res_mes+="db['dics']['tk']:"+dlb+str(db['dics']['tk'])+dlb+dlb
			res_mes+="db['terms']['num']:"+dlb+str(db['terms']['num'])+dlb+dlb
			res_mes+="db['terms']['phrases']:"+dlb+str(db['terms']['phrases'])+dlb+dlb
			res_mes+="db['terms']['pos']:"+dlb+str(db['terms']['pos'])+dlb+dlb
			res_mes+="db['terms']['tk']:"+dlb+str(db['terms']['tk'])+dlb+dlb
			res_mes+="db['terms']['url']:"+dlb+str(db['terms']['url'])+dlb+dlb
			res_mes+="db['comments']['num']:"+dlb+str(db['comments']['num'])+dlb+dlb
			res_mes+="db['comments']['phrases']:"+dlb+str(db['comments']['phrases'])+dlb+dlb
			res_mes+="db['comments']['pos']:"+dlb+str(db['comments']['pos'])+dlb+dlb
			res_mes+="db['comments']['tk']:"+dlb+str(db['comments']['tk'])
			text_field(title=globs['mes'].db_check4,user_text=res_mes,ReadOnly=True)
			res_mes=''
			debug_lst=[]
			for i in range(db['dics']['num']):
				pos1=db['dics']['pos'][i][0]
				pos2=db['dics']['pos'][i][1]
				debug_lst.append(db['page'][pos1:pos2+1])
			res_mes+='dics:'+dlb+str(debug_lst)+dlb+dlb
			debug_lst=[]
			for i in range(db['terms']['num']):
				pos1=db['terms']['pos'][i][0]
				pos2=db['terms']['pos'][i][1]
				debug_lst.append(db['page'][pos1:pos2+1])
			res_mes+='terms:'+dlb+str(debug_lst)+dlb+dlb
			debug_lst=[]
			for i in range(db['comments']['num']):
				pos1=db['comments']['pos'][i][0]
				pos2=db['comments']['pos'][i][1]
				debug_lst.append(db['page'][pos1:pos2+1])
			res_mes+='comments:'+dlb+str(debug_lst)
			text_field(title=globs['mes'].db_check5,user_text=res_mes,ReadOnly=True)
		#--------------------------------------------------------------------------
		# The first element of the 'dic' list must precede the first element of the 'term' list. We create a new dic list in order not to change the existing one.
		new_dic=[]
		for i in range(db['dics']['num']):
			new_dic.append(db['dics']['pos'][i][0])
		if len(new_dic) > 0:
			if new_dic[0]!='0':
				new_dic.insert(0,0)
		else:
			# To prevent program crash
			new_dic.insert(0,0)
			log(cur_func,lev_warn,globs['mes'].no_line_breaks_in_article)
		len_new_dic=len(new_dic)
		#--------------------------------------------------------------------------
		# Collect the information for easy move-up/-down/-left/-right, etc. actions
		# 'Move down' event
		db['move_down']=[]
		dic_no=0
		dic_pos=0
		for i in range(db['terms']['num']):
			term_no=i
			for j in range(len_new_dic):
				if new_dic[j] > db['terms']['pos'][i][0]:
					break
				else:
					dic_pos=new_dic[j]
					dic_no=j
			if len_new_dic-1 > dic_no:
				dic_no+=1
			dic_pos=new_dic[dic_no]
			for j in range(db['terms']['num']):
				if db['terms']['pos'][j][0] >= dic_pos:
					term_no=j
					break
			#db['move_down']+=[[db['terms']['tk'][term_no]]]
			db['move_down'].append(term_no)
		assert(db['terms']['num']==len(db['move_down']))
		log(cur_func,lev_debug,"db['move_down']: %s" % str(db['move_down']))
		#--------------------------------------------------------------------------
		# 'End' event
		# Весьма топорный алгоритм. Возможно, лучше создать db_page на раннем этапе и делать анализ 'end' на его основе
		db['end']=list(db['move_down'])
		# На предыдущем этапе мы делали проверку того, что длина списка терминов равна длине 'move_down'
		for i in range(db['terms']['num']):
			# Если элемент является 1-м элементом новой строки, то предыдущий элемент будет последним элементом предыдущей строки
			db['end'][i]-=1
		# Компенсируем различия с алгоритмом 'move_down'. Не очень красиво, но логично: в списке 'move_down' все элементы в последней строке будут ссылаться на одно и то же значение. В случае с 'end', все элементы последней строки должны ссылаться на номер последнего термина.
		# Проверка нужна для last_elem
		if db['terms']['num'] > 0:
			max_terms=db['terms']['num']-1
			max_all=db['all']['num']-1
			last_elem=db['end'][-1]
			while max_terms >= 0:
				if db['end'][max_terms] == last_elem:
					if max_all > 0:
						if db['all']['types'][max_all-1]=='terms':
							db['end'][max_terms]=db['terms']['num']-1
						else:
							# Вносим также 1-й элемент строки
							db['end'][max_terms]=db['terms']['num']-1
							break
				else:
					break
				max_terms-=1
				max_all-=1
		# Мы изначально брали равный по длине список, но оставляем проверку на случай усложнения алгоритма.
		assert(db['terms']['num']==len(db['end']))
		log(cur_func,lev_debug,"db['end']: %s" % str(db['end']))
		#--------------------------------------------------------------------------
		# 'Move up' event
		db['move_up']=[]
		dic_no=0
		dic_pos=0
		for i in range(db['terms']['num']):
			term_no=i
			j=len_new_dic-1
			while j >= 0:
				if db['terms']['pos'][i][0] > new_dic[j]:
					dic_pos=new_dic[j]
					dic_no=j
					break
				j-=1
			if dic_no > 0:
				dic_no-=1
			dic_pos=new_dic[dic_no]
			for j in range(db['terms']['num']):
				if db['terms']['pos'][j][0] >= dic_pos:
					term_no=j
					break
			#db['move_up']+=[[db['terms']['tk'][term_no]]]
			db['move_up'].append(term_no)
		assert(db['terms']['num']==len(db['move_up']))
		log(cur_func,lev_debug,"db['move_up']: %s" % str(db['move_up']))
		#--------------------------------------------------------------------------
		# 'Home' event
		db['home']=[]
		dic_no=0
		dic_pos=0
		for i in range(db['terms']['num']):
			term_no=i
			j=len_new_dic-1
			while j >= 0:
				if db['terms']['pos'][i][0] > new_dic[j]:
					dic_pos=new_dic[j]
					dic_no=j
					break
				j-=1
			dic_pos=new_dic[dic_no]
			for j in range(db['terms']['num']):
				if db['terms']['pos'][j][0] >= dic_pos:
					term_no=j
					break
			db['home'].append(term_no)
		assert(db['terms']['num']==len(db['home']))
		log(cur_func,lev_debug,"db['home']: %s" % str(db['home']))
		#--------------------------------------------------------------------------
		# 'Move left' event
		db['move_left']=[]
		for i in range(db['terms']['num']):
			term_no=i
			if i > 0:
				term_no-=1
			#db['move_left']+=[[db['terms']['tk'][term_no]]]
			db['move_left'].append(term_no)
		assert(db['terms']['num']==len(db['move_left']))
		log(cur_func,lev_debug,"db['move_left']: %s" % str(db['move_left']))
		#--------------------------------------------------------------------------
		# 'Move right' event
		db['move_right']=[]
		for i in range(db['terms']['num']):
			term_no=i
			if i < db['terms']['num']-1:
				term_no+=1
			#db['move_right']+=[[db['terms']['tk'][term_no]]]
			db['move_right'].append(term_no)
		#--------------------------------------------------------------------------
		assert(db['terms']['num']==len(db['move_right']))
		log(cur_func,lev_debug,"db['move_right']: %s" % str(db['move_right']))
		if globs['bool']['InternalDebug']:
			res_mes="db['move_up']:"+dlb+str(db['move_up'])+dlb+dlb
			res_mes+="db['move_down']:"+dlb+str(db['move_down'])+dlb+dlb
			res_mes+="db['move_left']:"+dlb+str(db['move_left'])+dlb+dlb
			res_mes+="db['move_right']:"+dlb+str(db['move_right'])+dlb+dlb
			text_field(title=globs['mes'].db_check6,user_text=res_mes,ReadOnly=True)
	return db

# Remove tags that are not relevant to the article structure
def remove_useless_tags(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		tags_total=db['len_tags']
		i=0
		while i < db['len_tags']:
			#if tags[i].startswith(tag_pattern1) or tags[i].startswith(tag_pattern2) or tags[i].startswith(tag_pattern3) or tags[i].startswith(tag_pattern4) or tags[i]==tag_pattern5 or tags[i]==tag_pattern6 or tags[i]==tag_pattern7 or tags[i]==tag_pattern8:
			if tag_pattern1 in db['tags'][i] or tag_pattern2 in db['tags'][i] or tag_pattern3 in db['tags'][i] or tag_pattern4 in db['tags'][i] or tag_pattern5 in db['tags'][i] or tag_pattern6 in db['tags'][i] or tag_pattern7 in db['tags'][i] or tag_pattern8 in db['tags'][i]:
				log(cur_func,lev_debug,globs['mes'].tag_kept % db['tags'][i])
				pass
			else:
				log(cur_func,lev_debug,globs['mes'].deleting_tag % (i,db['tags'][i]))
				del db['tags'][i]
				db['len_tags']-=1
				del db['tag_borders'][i]
				db['len_tag_borders']-=1
				i-=1
			i+=1
		# Logging
		log(cur_func,lev_debug,"db['len_tags']: %d" % db['len_tags'])
		log(cur_func,lev_debug,"db['tags']: %s" % str(db['tags']))
		log(cur_func,lev_debug,"db['len_tag_borders']: %d" % db['len_tag_borders'])
		log(cur_func,lev_debug,"db['tag_borders']: %s" % str(db['tag_borders']))
		log(cur_func,lev_info,globs['mes'].tags_stat % (tags_total,db['len_tags'],tags_total-db['len_tags']))
		# Testing
		assert(db['len_tags']==db['len_tag_borders'])
	return db
	
# Преобразовать координаты заданного виджета из пикселей в Tkinter
def pixels2tk(widget,x,y,Silent=False,Critical=False):
	cur_func=sys._getframe().f_code.co_name
	tk_pos='1.0'
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			tk_pos=widget.index('@%d,%d' % (x,y))
		except:
			mestype(cur_func,'Не удается преобразовать координаты виджета "%s" из пикселей в Tkinter для координат (%s,%s)' % (str(widget),str(x),str(y)),Silent=Silent,Critical=Critical)
		log(cur_func,lev_debug,tk_pos)
	return tk_pos

# Вычислить координаты текста для текущей видимой области
def get_page_coor(db,page_no):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['coor_db']['pages'][page_no]={}
		db['coor_db']['pages'][page_no]['up']={}
		db['coor_db']['pages'][page_no]['up']['pix']={}
		db['coor_db']['pages'][page_no]['down']={}
		db['coor_db']['pages'][page_no]['down']['pix']={}
		db['coor_db']['pages'][page_no]['up']['pix']['x']=db['coor_db']['widget'].winfo_x()
		db['coor_db']['pages'][page_no]['up']['pix']['y']=db['coor_db']['widget'].winfo_y()
		db['coor_db']['pages'][page_no]['down']['pix']['x']=db['coor_db']['pages'][page_no]['up']['pix']['x']+db['coor_db']['width']
		db['coor_db']['pages'][page_no]['down']['pix']['y']=db['coor_db']['pages'][page_no]['up']['pix']['y']+db['coor_db']['height']
		db['coor_db']['pages'][page_no]['up']['tk']=pixels2tk(db['coor_db']['widget'],db['coor_db']['pages'][page_no]['up']['pix']['x'],db['coor_db']['pages'][page_no]['up']['pix']['y'])
		db['coor_db']['pages'][page_no]['down']['tk']=pixels2tk(db['coor_db']['widget'],db['coor_db']['pages'][page_no]['down']['pix']['x'],db['coor_db']['pages'][page_no]['down']['pix']['y'])
		db['coor_db']['pages'][page_no]['up']['pos']=tk2pos(db['db_page'],db['coor_db']['pages'][page_no]['up']['tk'],Even=False)
		db['coor_db']['pages'][page_no]['down']['pos']=tk2pos(db['db_page'],db['coor_db']['pages'][page_no]['down']['tk'],Even=True)
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pix']['x']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pix']['x']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pix']['y']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pix']['y']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pix']['x']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pix']['x']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pix']['y']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pix']['y']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['tk']: %s" % (page_no,db['coor_db']['pages'][page_no]['up']['tk']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['tk']: %s" % (page_no,db['coor_db']['pages'][page_no]['down']['tk']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['up']['pos']: %d" % (page_no,db['coor_db']['pages'][page_no]['up']['pos']))
		log(cur_func,lev_debug,"db['coor_db']['pages'][%d]['down']['pos']: %d" % (page_no,db['coor_db']['pages'][page_no]['down']['pos']))
	return db

# Вернуть число страниц (видимых областей) в статье
def get_coor_pages(widget,db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		db['coor_db']={}
		db['coor_db']['widget']=widget
		db['coor_db']['widget'].update_idletasks()
		db['coor_db']['width']=db['coor_db']['widget'].winfo_width()
		db['coor_db']['height']=db['coor_db']['widget'].winfo_height()
		if db['coor_db']['height'] > globs['int']['pixel_hack']:
			db['coor_db']['height']-=globs['int']['pixel_hack']
		if db['coor_db']['width'] > globs['int']['pixel_hack']:
			db['coor_db']['width']-=globs['int']['pixel_hack']
		log(cur_func,lev_debug,"db['coor_db']['width']: %d" % db['coor_db']['width'])
		log(cur_func,lev_debug,"db['coor_db']['height']: %d" % db['coor_db']['height'])
		db['coor_db']['pages']={}
		page_no=0
		next_page_pos=0
		prev_tk='1.0'
		next_page_tk='1.0'
		widget.yview('1.0')
		while next_page_pos < db['db_page']['len']:
			db=get_page_coor(db,page_no)
			next_page_pos=db['coor_db']['pages'][page_no]['down']['pos']+1
			if next_page_pos > db['db_page']['len']-1:
				break
			else:
				next_page_tk=pos2tk(db['db_page'],next_page_pos,Even=True)
				# В некоторых случаях, несмотря на +1 в номере символа, его позиция по Tk не меняется, и можно войти в бесконечный цикл.
				while next_page_tk==prev_tk and next_page_pos < db['db_page']['len']-1:
					next_page_pos+=1
					next_page_tk=pos2tk(db['db_page'],next_page_pos,Even=True)
				log(cur_func,lev_debug,'next_page_tk: %s' % next_page_tk)
				if next_page_tk==prev_tk or next_page_pos >= db['db_page']['len']-1:
					break
				else:
					widget.yview(next_page_tk)
					page_no+=1
					prev_tk=next_page_tk
		widget.yview('1.0')
		db['coor_db']['pages']['num']=page_no+1
		if db['mode']!='skip':
			db['coor_db']['cur_page_no']=0
		db['coor_db']['direction']='right_down'
		log(cur_func,lev_debug,"db['coor_db']['pages']['num']: %d" % db['coor_db']['pages']['num'])
	return db
	
# По позиции символа определить ближайший термин слева или справа
def get_adjacent_term(db,det,direction='right_down'):
	cur_func=sys._getframe().f_code.co_name
	term_num=-1
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		term=''
		if direction=='right_down':
			for i in range(db['terms']['num']):
				if det <= db['terms']['pos'][i][0] or det <= db['terms']['pos'][i][1]:
					term_num=i
					term=db['terms']['phrases'][term_num]
					break
			log(cur_func,lev_debug,globs['mes'].right_term % (term_num,term))
		elif direction=='left_up':
			i=db['terms']['num']-1
			while i >= 0:
				if det >= db['terms']['pos'][i][0] or det >= db['terms']['pos'][i][1]:
					term_num=i
					term=db['terms']['phrases'][term_num]
					break
				i-=1
			log(cur_func,lev_debug,globs['mes'].left_term % (term_num,term))
	return term_num

# Загрузить картинку кнопки
# top.wm_iconbitmap поддерживает только черно-белый XBM. Через PhotoImage удается загрузить только GIF.
def load_icon(icon_path,parent_widget,width=None,height=None,Silent=False,Critical=True):
	cur_func=sys._getframe().f_code.co_name
	button_img=None
	check_type(cur_func,icon_path,globs['mes'].type_str)
	exist(icon_path,Silent=Silent,Critical=Critical)
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if empty(width):
			width=globs['int']['default_button_size']
		if empty(height):
			height=globs['int']['default_button_size']
		try:
			# Нужно указывать виджет: http://stackoverflow.com/questions/23224574/tkinter-create-image-function-error-pyimage1-does-not-exist
			button_img=tk.PhotoImage(file=icon_path,master=parent_widget,width=width,height=height) # Без 'file=' не сработает!
		except tk.TclError:
			mestype(cur_func,globs['mes'].button_load_failed % icon_path,Silent=Silent,Critical=Critical)
	return button_img
	
# Привязать горячие клавиши или кнопки мыши к действию
def create_binding(widget,binding,action):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		try:
			widget.bind(binding,action)
		except tk.TclError:
			Warning(cur_func,globs['mes'].wrong_keybinding % binding)
		
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
	#--------------------------------------------------------------------------
	def enter(self, event=None):
		self.schedule()
	#--------------------------------------------------------------------------
	def leave(self, event=None):
		self.unschedule()
		self.hidetip()
	#--------------------------------------------------------------------------
	def schedule(self):
		self.unschedule()
		self.id = self.button.after(self.hint_delay, self.showtip)
	#--------------------------------------------------------------------------
	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)
	#--------------------------------------------------------------------------
	def showtip(self):
		cur_func=sys._getframe().f_code.co_name
		if not 'top' in globs or not 'width' in globs['top'] or not 'height' in globs['top']:
			ErrorMessage(cur_func,globs['mes'].not_enough_input_data)
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			if self.tipwindow:
				return
			# The tip window must be completely outside the button; otherwise when the mouse enters the tip window we get a leave event and it disappears, and then we get an enter event and it reappears, and so on forever :-(
			# Координаты подсказки рассчитываются так, чтобы по горизонтали подсказка и кнопка, несмотря на разные размеры, совпадали бы центрами.
			x = self.button.winfo_rootx() + self.button.winfo_width()/2 - self.hint_width/2
			if self.hint_direction=='bottom':
				y = self.button.winfo_rooty() + self.button.winfo_height() + 1
			elif self.hint_direction=='top':
				y = self.button.winfo_rooty() - self.hint_height - 1
			else:
				ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(self.hint_direction),'top, bottom'))
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Позиция подсказки корректируется так, чтобы не выходить за пределы экрана
				if x + self.hint_width > globs['top']['width']:
					log(cur_func,lev_info,globs['mes'].wrong_coor % ('x',str(x),str(globs['top']['width'] - self.hint_width)))
					x = globs['top']['width'] - self.hint_width
				if y + self.hint_height > globs['top']['height']:
					log(cur_func,lev_info,globs['mes'].wrong_coor % ('y',str(y),str(globs['top']['height'] - self.hint_height)))
					y = globs['top']['height'] - self.hint_height
				if x < 0:
					log(cur_func,lev_warn,globs['mes'].wrong_coor % ('x',str(x),'0'))
					x=0
				if y < 0:
					log(cur_func,lev_warn,globs['mes'].wrong_coor % ('y',str(y),'0'))
					y=0
				self.tipwindow = tw = tk.Toplevel(self.button)
				tw.wm_overrideredirect(1)
				# "+%d+%d" недостаточно!
				log(cur_func,lev_info,globs['mes'].new_geometry % ('tw',self.hint_width,self.hint_height,x,y))
				tw.wm_geometry("%dx%d+%d+%d" % (self.hint_width,self.hint_height,x, y))
				self.showcontents()
	#--------------------------------------------------------------------------
	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()

class ToolTip(ToolTipBase):
	def __init__(self,button,text='Sample text',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,button_side='left'):
		if empty(hint_delay):
			hint_delay=globs['int']['default_hint_delay']
		if empty(hint_width):
			hint_width=globs['int']['default_hint_width']
		if empty(hint_height):
			hint_height=globs['int']['default_hint_height']
		if empty(hint_background):
			hint_background=globs['var']['default_hint_background']
		if empty(hint_direction):
			hint_direction=globs['var']['default_hint_direction']
		if empty(hint_border_width):
			hint_border_width=globs['int']['default_hint_border_width']
		if empty(hint_border_color):
			hint_border_color=globs['var']['default_hint_border_color']
		self.text=text
		self.hint_delay=hint_delay
		self.hint_direction=hint_direction
		self.hint_background=hint_background
		self.hint_border_color=hint_border_color
		self.hint_height=hint_height
		self.hint_width=hint_width
		self.hint_border_width=hint_border_width
		self.button_side=button_side
		ToolTipBase.__init__(self,button)
	#--------------------------------------------------------------------------
	def showcontents(self):
		frame=tk.Frame(self.tipwindow,background=self.hint_border_color,borderwidth=self.hint_border_width)
		frame.pack()
		label=tk.Label(frame,text=self.text,justify='center',background=self.hint_background,width=self.hint_width,height=self.hint_height)
		label.pack() #expand=1,fill='x'
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Создать кнопку с различными параметрами
# expand=1 - увеличить расстояние между кнопками
def create_button(parent_widget,text,hint,action,expand=0,side='left',fg='black',Silent=False,Critical=True,width=None,height=None,bd=0,icon_path='',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None):
	# side: must be 'top, 'bottom', 'left' or 'right'
	cur_func=sys._getframe().f_code.co_name
	button=None
	Success=True # Кнопку удалось инициализировать и упаковать; неудачные привязки не учитываются
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		if empty(width):
			width=globs['int']['default_button_size']
		if empty(height):
			height=globs['int']['default_button_size']
		if empty(hint_delay):
			hint_delay=globs['int']['default_hint_delay']
		if empty(hint_width):
			hint_width=globs['int']['default_hint_width']
		if empty(hint_height):
			hint_height=globs['int']['default_hint_height']
		if empty(hint_background):
			hint_background=globs['var']['default_hint_background']
		if empty(hint_direction):
			hint_direction=globs['var']['default_hint_direction']
		if empty(hint_border_width):
			hint_border_width=globs['int']['default_hint_border_width']
		if empty(hint_border_color):
			hint_border_color=globs['var']['default_hint_border_color']
		try:
			if empty(icon_path) or globs['bool']['TextButtons']:
				button=tk.Button(parent_widget,text=text,fg=fg)
			else:
				button_img=load_icon(icon_path=icon_path,parent_widget=parent_widget,width=width,height=height,Silent=Silent,Critical=Critical)
				button=tk.Button(parent_widget,image=button_img,width=width,height=height,bd=bd)
				button.flag_img=button_img
		except tk.TclError:
			Success=False
			if Critical:
				globs['AbortAll']=True
		create_binding(button,'<Return>',action)
		create_binding(button,'<KP_Enter>',action)
		create_binding(button,'<space>',action)
		create_binding(button,'<ButtonRelease-1>',action)
		try:
			button.pack(expand=expand,side=side)
		# tk.TclError, AttributeError
		except:
			Success=False
			if Critical:
				globs['AbortAll']=True
		if Success:
			ToolTip(button,text=hint,hint_delay=hint_delay,hint_width=hint_width,hint_height=hint_height,hint_background=hint_background,hint_direction=hint_direction,button_side=side)
		log(cur_func,lev_debug,str(Success))
		if not Success:
			mestype(cur_func,globs['mes'].button_create_failed % text,Silent=Silent,Critical=Critical)
	return button

# Свернуть заданное окно
def iconify(widget=root):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		widget.iconify()

# Определить номера терминов, которые являются пограничными для видимой области
def aggregate_pages(db):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		for i in range(db['coor_db']['pages']['num']):
			db['coor_db']['pages'][i]['up']['num']=get_adjacent_term(db,db['coor_db']['pages'][i]['up']['pos'],direction='right_down')
			db['coor_db']['pages'][i]['down']['num']=get_adjacent_term(db,db['coor_db']['pages'][i]['down']['pos'],direction='left_up')
			if db['terms']['num'] > 0:
				log(cur_func,lev_debug,globs['mes'].db_pages_stat % (i,db['coor_db']['pages'][i]['up']['num'],db['terms']['phrases'][db['coor_db']['pages'][i]['up']['num']],db['coor_db']['pages'][i]['down']['num'],db['terms']['phrases'][db['coor_db']['pages'][i]['down']['num']]))
	return db
	
# Отобразить окно со словарной статьей
def article_field(db,Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		top=tk.Toplevel(root)
		res=[0]
		root.withdraw()
		if not 'search' in db:
			db['search']=globs['mes'].welcome
			log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
		if not 'mode' in db:
			db['mode']='search'
		if not 'ShowHistory' in db:
			db['ShowHistory']=False
		if not 'FirstLaunch' in db:
			db['FirstLaunch']=True
		if not 'history' in db:
			db['history']=[]
			db['history_url']=[]
		#----------------------------------------------------------------------
		# Закрыть текущее окно mclient без выхода из самой программы
		def close_top(event):
			top.destroy()
			root.deiconify()
		#----------------------------------------------------------------------
		# Go to the URL of the current selection
		def go_url(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['search']=db['terms']['phrases'][res[0]]
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
				db['url']=db['terms']['url'][res[0]]
				log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
				db['mode']='url'
				db['history_index']=len(db['history'])
				close_top(event)
		#----------------------------------------------------------------------
		def insert_repeat_sign(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if len(db['history']) > 0:
					clipboard_copy(db['history'][-1])
					paste_search_field(None)
		#----------------------------------------------------------------------
		def insert_repeat_sign2(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if len(db['history']) > 1:
					clipboard_copy(db['history'][-2])
					paste_search_field(None)
		#----------------------------------------------------------------------
		# Search the selected term online using the entry widget (search field)
		def go_search(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				search_str=search_field.get().strip(dlb).strip(' ')
				# Allows to use the same hotkeys for the search field and the article field
				if search_str=='':
					go_url(None)
				else:
					db['search']=search_str
					log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
					# Необходимо вовремя вернуть db['url'], чтобы он был занесен в историю
					# Поскольку Multitran использует кодировку windows-1251, необходимо использовать ее. Поскольку некоторые символы не кодируются в globs['var']['win_encoding'] корректно, оставляем для них кодировку UTF-8.
					# tmp, todo: Не получилось сделать этот блок в виде отдельной процедуры
					try:
						request_encoded=db['search'].encode(globs['var']['win_encoding'])
					except:
						request_encoded=bytes(db['search'],encoding=default_encoding)
					# Некоторые версии питона принимают 'encode('windows-1251')', но не 'encode(encoding='windows-1251')'
					db['url']=online_request(globs['var']['online_dic_url'],request_encoded)
					log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
					db['mode']='search'
					#db['mode']='url'
					# Скопировать предпоследний запрос в буфер и вставить его в строку поиска (например, для перехода на этот запрос еще раз)
					if db['search']==globs['var']['repeat_sign2']:
						insert_repeat_sign2(event)
					# Скопировать последний запрос в буфер и вставить его в строку поиска (например, для корректировки)
					elif db['search']==globs['var']['repeat_sign']:
						insert_repeat_sign(event)
					else:
						# Обновляем индекс текущего запроса при добавлении элемента для поиска
						db['history_index']=len(db['history'])
						close_top(event)
		#----------------------------------------------------------------------		
		# Copy to clipboard
		def copy_sel(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				clipboard_copy(db['terms']['phrases'][res[0]])
				log(cur_func,lev_info,globs['mes'].copied_to_clipboard % str(db['terms']['phrases'][res[0]]))
				if db['mode']=='clipboard':
					close_top(event)
				else:
					top.iconify()
		#----------------------------------------------------------------------
		# Close the root window without errors
		def quit_now(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['Quit']=True
				close_top(event)
		#----------------------------------------------------------------------
		# Запрос на выход
		def quit_top(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if db['mode']!='clipboard':
					#if Question(cur_func,globs['mes'].ques_exit):
					#	log(cur_func,lev_info,globs['mes'].goodbye)
						db['Quit']=True
				close_top(None)
		#----------------------------------------------------------------------
		# Определение текущего термина по координатам указателя
		def mouse_sel(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				tk_pos=pixels2tk(txt,event.x,event.y,Silent=False,Critical=False)
				pos=tk2pos(db['db_page'],tk_pos)
				res[0]=get_adjacent_term(db,pos)
				select_term(ForceScreenFit=True)
		#----------------------------------------------------------------------
		# Задействование колеса мыши для пролистывания экрана
		def mouse_wheel(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# В Windows XP delta==-120, однако, в других версиях оно другое
				if event.num==5 or event.delta < 0:
					move_page_down(event)
				# В Windows XP delta==120, однако, в других версиях оно другое
				if event.num==4 or event.delta > 0:
					move_page_up(event)
				return 'break'
		#----------------------------------------------------------------------
		# Рассчитать координаты ползунка в зависимости от числа страниц
		def scrollbar_poses(db):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				delim=1/db['coor_db']['pages']['num']
				# Минимальный шаг, который разграничивает координаты 2 соседних экранов
				step=0.000000001
				last_val=0
				db['scroll_poses']=[]
				for i in range(db['coor_db']['pages']['num']):
					if i==0:
						db['scroll_poses']+=[[last_val,last_val+delim]]
					else:
						db['scroll_poses']+=[[last_val+step,last_val+delim]]
					last_val+=delim
				log(cur_func,lev_debug,str(db['scroll_poses']))
				assert(len(db['scroll_poses'])==db['coor_db']['pages']['num'])
		#----------------------------------------------------------------------
		# Вернуть номер страницы в зависимости от координат ползунка
		def detect_page(mode='coor'): # 'coor', 'term_no'
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Инициализируем i, иначе при i=0 далее возникнет ошибка присваивания
				i=0
				if mode=='coor':
					for i in range(db['coor_db']['pages']['num']):
						if db['cur_scroll_pos'] >= db['scroll_poses'][i][0] and db['cur_scroll_pos'] <= db['scroll_poses'][i][1]:
							break
				elif mode=='term_no':
					for i in range(db['coor_db']['pages']['num']):
						if res[0] >= db['coor_db']['pages'][i]['up']['num'] and res[0] <= db['coor_db']['pages'][i]['down']['num']:
							break
				else:
					ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'coor, term_no'))
				db['coor_db']['cur_page_no']=i
				log(cur_func,lev_debug,str(db['coor_db']['cur_page_no']))
		#----------------------------------------------------------------------
		# Задействование ползунка
		def custom_scroll(*args):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Если сдвигается сам ползунок, то Tkinter передаст 2 параметра: 'moveto' и offset (оба имеющие тип 'строка', однако, второй параметр на самом деле float).
				# Если же используются стрелки ползунка, то 1-м параметром будет 'scroll', а 2-м - '1' (направление вниз) или '-1' (направление вверх).
				def add_page():
					cur_func=sys._getframe().f_code.co_name
					if globs['AbortAll']:
						log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
					else:
						if db['coor_db']['cur_page_no'] < db['coor_db']['pages']['num']-1:
							log(cur_func,lev_info,"db['coor_db']['cur_page_no']: %d -> %d" % (db['coor_db']['cur_page_no'],db['coor_db']['cur_page_no']+1))
							db['coor_db']['cur_page_no']+=1
				def subtract_page():
					cur_func=sys._getframe().f_code.co_name
					if globs['AbortAll']:
						log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
					else:
						if db['coor_db']['cur_page_no'] > 0:
							log(cur_func,lev_info,"db['coor_db']['cur_page_no']: %d -> %d" % (db['coor_db']['cur_page_no'],db['coor_db']['cur_page_no']-1))
							db['coor_db']['cur_page_no']-=1
				action=args[0]
				log(cur_func,lev_info,globs['mes'].action % action)
				offset=scrollbar.get()[0]
				if offset < 0:
					offset=0
				elif offset > 1:
					offset=1
				log(cur_func,lev_info,globs['mes'].scrollbar_pos % str(offset))
				if not 'prev_scroll_pos' in db:
					db['prev_scroll_pos']=0
					db['cur_scroll_pos']=0
					db['coor_db']['cur_page_no']=0
				db['prev_scroll_pos']=db['cur_scroll_pos']
				db['cur_scroll_pos']=offset
				log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
				log(cur_func,lev_info,"db['cur_scroll_pos']: %s" % str(db['cur_scroll_pos']))
				# Определяем текущую страницу
				detect_page()
				log(cur_func,lev_info,globs['mes'].cur_page_no % db['coor_db']['cur_page_no'])
				if action=='scroll':
					offset=args[1]
					if offset=='1':
						add_page()
					elif offset=='-1':
						subtract_page()
					else:
						log(cur_func,lev_err,globs['mes'].unknown_args % (str(offset),'-1, 1'))
				elif action=='moveto':
					if db['cur_scroll_pos'] < 0:
						log(cur_func,lev_info,globs['mes'].cor_scroll % (db['cur_scroll_pos'],0))
						db['cur_scroll_pos']=0
					elif db['cur_scroll_pos'] > 1:
						log(cur_func,lev_info,globs['mes'].cor_scroll % (db['cur_scroll_pos'],1))
						db['cur_scroll_pos']=1
					if db['cur_scroll_pos'] > db['prev_scroll_pos']:
						add_page()
					#elif db['cur_scroll_pos'] < db['prev_scroll_pos']:
					#	subtract_page()
					else:
						log(cur_func,lev_info,globs['mes'].scrollbar_still)
				else:
					Warning(cur_func,globs['mes'].unknown_args % (action,'scroll, move_to'))
				db['prev_scroll_pos']=db['cur_scroll_pos']
				db['cur_scroll_pos']=db['scroll_poses'][db['coor_db']['cur_page_no']][0]
				log(cur_func,lev_info,globs['mes'].new_values)
				log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
				log(cur_func,lev_info,"db['cur_scroll_pos']: %s" % str(db['cur_scroll_pos']))
				# Изменяем текущую страницу в соответствии с предыдущими корректировками
				detect_page()
				log(cur_func,lev_info,globs['mes'].cur_page_no % db['coor_db']['cur_page_no'])
				shift_screen(mode='still')
				db['cur_scroll_pos']=db['scroll_poses'][db['coor_db']['cur_page_no']][0]
				scroll_pos1=db['cur_scroll_pos']
				scroll_pos2=db['scroll_poses'][db['coor_db']['cur_page_no']][1]
				if scroll_pos1 < 0:
					scroll_pos1=0
				elif scroll_pos1 > 1:
					scroll_pos1=1
				if scroll_pos2 < 0:
					scroll_pos2=0
				elif scroll_pos2 > 1:
					scroll_pos2=1
				scrollbar.set(scroll_pos1,scroll_pos2)
				select_term()
				db['prev_scroll_pos']=db['cur_scroll_pos']
				log(cur_func,lev_info,"db['prev_scroll_pos']: %s" % str(db['prev_scroll_pos']))
				return 'break'
		#----------------------------------------------------------------------
		# Выделение терминов
		def select_term(ForceScreenFit=True):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
					if ForceScreenFit:
						if not fits_screen():
							log(cur_func,lev_warn,globs['mes'].visible_selection)
							if db['coor_db']['direction']=='right_down':
								res[0]=get_adjacent_term(db,db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['pos'],db['coor_db']['direction'])
							elif db['coor_db']['direction']=='left_up':
								res[0]=get_adjacent_term(db,db['coor_db']['pages'][db['coor_db']['cur_page_no']]['down']['pos'],db['coor_db']['direction'])
					pos1=db['terms']['pos'][res[0]][0]
					pos2=db['terms']['pos'][res[0]][1]
					pos1=pos2tk(db['db_page'],pos1)
					pos2=pos2tk(db['db_page'],pos2,Even=True)
					# Только 1 термин должен быть выделен, поэтому предварительно удаляем тэг выделения по всему тексту.
					try:
						txt.tag_remove('cur_term','1.0','end')
					except:
						log(cur_func,lev_err,'Не удалось удалить тэг "%s" в диапазоне %s-%s!' % ('cur_term','1.0','end'))
					try:
						txt.tag_add('cur_term',pos1,pos2)
						log(cur_func,lev_debug,globs['mes'].tag_added % ('cur_term',pos1,pos2))
					except:
						mestype(cur_func,globs['mes'].tag_addition_failure % ('cur_term',pos1,pos2),Silent=False,Critical=False)
				else:
					log(cur_func,lev_warn,globs['mes'].not_enough_input_data)
				# 2. Настройка тэга
				try:
					txt.tag_config('cur_term',background=globs['var']['color_terms_sel'],font=globs['var']['font_terms_sel'])
					log(cur_func,lev_debug,globs['mes'].tag_config % ('cur_term',globs['var']['color_terms_sel'],globs['var']['font_terms_sel']))
				except:
					mestype(cur_func,globs['mes'].tag_config_failure % ('cur_term',globs['var']['color_terms_sel'],globs['var']['font_terms_sel']),Silent=False,Critical=False)
		#----------------------------------------------------------------------
		# Определить, входит ли текущий термин в видимую часть экрана
		def fits_screen():
			cur_func=sys._getframe().f_code.co_name
			# Вернуть True, если смещение экрана не требуется (ввиду названия функции)
			Success=True
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				# Если терминов нет, то смещать экран бесполезно
				if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
					if not 'cur_page_no' in db['coor_db']:
						db['coor_db']['cur_page_no']=0
					if db['terms']['pos'][res[0]][0] >= db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['pos'] and db['terms']['pos'][res[0]][-1] <= db['coor_db']['pages'][db['coor_db']['cur_page_no']]['down']['pos']:
						pass
					else:
						Success=False
			return Success
		#----------------------------------------------------------------------
		# Обеспечить удобное пролистывание экрана
		# mode='normal': смещать экран согласно fits_screen()
		# mode='change': изменить номер страницы даже в том случае, если текущий термин находится в видимой области (необходимо для move_page_up/_down)
		# mode='still': не изменять номер страницы (необходимо для move_page_start/_end)
		def shift_screen(mode='normal'):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				DragScreen=False
				# Вставляю проверку в самом начале, чтобы в случае ошибки не проводить дополнительные операции. Все равно если терминов нет, то смещать экран бесполезно
				if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
					if mode=='normal':
						if fits_screen():
							DragScreen=False
						else:
							DragScreen=True
					elif mode=='change':
						DragScreen=True
					elif mode=='still':
						DragScreen=False
					else:
						ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(mode),'normal, change, still'))
					if DragScreen:
						log(cur_func,lev_info,globs['mes'].shift_screen_required)
						if db['coor_db']['direction']=='right_down':
							if db['coor_db']['cur_page_no'] < db['coor_db']['pages']['num']-1:
								db['coor_db']['cur_page_no']+=1
						elif db['coor_db']['direction']=='left_up':
							if db['coor_db']['cur_page_no'] > 0:
								db['coor_db']['cur_page_no']-=1
						else:
							ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(db['coor_db']['direction']),'left_up, right_down'))
					else:
						log(cur_func,lev_info,globs['mes'].shift_screen_not_required)
					# Фактически, экран нужно смещать всегда
					yview_tk=db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['tk']
					# Смещение экрана до заданного термина
					# Алгоритм работает только, если метка называется 'insert'
					try:
						txt.mark_set('insert',yview_tk)
						txt.yview('insert')
						log(cur_func,lev_info,globs['mes'].shift_screen % ('insert',yview_tk))
					except:
						log(cur_func,lev_err,globs['mes'].shift_screen_failure % 'insert')
		#----------------------------------------------------------------------
		# Перейти на 1-й термин текущей строки	
		def move_line_start(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='left_up'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['home'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на последний термин текущей строки
		def move_line_end(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='right_down'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['end'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на 1-й термин статьи
		def move_text_start(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='left_up'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=0
				db['coor_db']['cur_page_no']=0
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на последний термин статьи
		def move_text_end(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='right_down'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['terms']['num']-1
				db['coor_db']['cur_page_no']=db['coor_db']['pages']['num']-1
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на страницу вверх
		def move_page_up(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				db['coor_db']['direction']='left_up'
				if db['coor_db']['cur_page_no'] > 0:
					res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']-1]['up']['num']
				else:
					res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['num']
				shift_screen(mode='change')
				select_term(ForceScreenFit=False)
				return "break"
		#----------------------------------------------------------------------
		# Перейти на страницу вверх
		def move_page_down(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				db['coor_db']['direction']='right_down'
				if db['coor_db']['cur_page_no'] < db['coor_db']['pages']['num']-1:
					res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']+1]['up']['num']
				else:
					res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['num']
				shift_screen(mode='change')
				select_term(ForceScreenFit=False)
				return "break"
		#----------------------------------------------------------------------
		# Перейти на 1-й термин текущей страницы
		def move_page_start(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				# Направление указывается для того, чтобы в любом случае не менять текущую страницу
				db['coor_db']['direction']='left_up'
				res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']]['up']['num']
				shift_screen(mode='still')
				select_term(ForceScreenFit=False)
				# Поскольку привязка идет по Shift, то tkinter может также осуществлять другие действия по Shift, например, выделение. "break" блокирует это поведение.
				return "break"
		#----------------------------------------------------------------------
		# Перейти на последний термин текущей страницы
		def move_page_end(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				# Направление указывается для того, чтобы в любом случае не менять текущую страницу
				db['coor_db']['direction']='left_up'
				res[0]=db['coor_db']['pages'][db['coor_db']['cur_page_no']]['down']['num']
				shift_screen(mode='still')
				select_term(ForceScreenFit=False)
				# Поскольку привязка идет по Shift, то tkinter может также осуществлять другие действия по Shift, например, выделение. "break" блокирует это поведение.
				return "break"
		#----------------------------------------------------------------------
		# Перейти на предыдущий термин
		def move_left(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='left_up'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['move_left'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на следующий термин
		def move_right(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='right_down'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['move_right'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на строку вниз
		def move_down(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='right_down'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['move_down'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Перейти на строку вверх
		def move_up(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['coor_db']['direction']='left_up'
				txt.tag_remove('cur_term','1.0','end')
				log(cur_func,lev_debug,globs['mes'].tag_removed % ('cur_term','1.0','end'))
				res[0]=db['move_up'][res[0]]
				shift_screen()
				select_term()
		#----------------------------------------------------------------------
		# Изменить направление (язык) перевода
		def change_pair(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				try:
					selected_pair=var.get()
				except:
					log(cur_func,lev_err,globs['mes'].lang_pair_undefined)
					selected_pair=globs['cur_pair']
				log(cur_func,lev_debug,globs['mes'].got_value % str(selected_pair))
				Found=False
				for i in range(len(pairs)):
					if selected_pair==pairs[i]:
						Found=True
						break
				if Found:
					globs['var']['online_dic_url']=online_dic_urls[i]
				log(cur_func,lev_info,globs['mes'].lang_pair % selected_pair)
				log(cur_func,lev_debug,'URL: %s' % globs['var']['online_dic_url'])
				globs['cur_pair']=selected_pair
		#----------------------------------------------------------------------
		# Отобразить/скрыть историю запросов онлайн
		def toggle_history(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if db['ShowHistory']:
					db['ShowHistory']=False
				else:
					db['ShowHistory']=True
				db['mode']='skip'
				# Запоминаем позицию выделения, чтобы она не сбрасывалась при переключении отображения Истории. Запомнить позицию выделения можно только на первой странице.
				db['last_sel']=res[0]
				close_top(event)
		#----------------------------------------------------------------------
		# Окно "О программе"
		def show_about(event):
			# Написать письмо автору
			def response_back(event):
				cur_func=sys._getframe().f_code.co_name
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					try:
						webbrowser.open('mailto:%s' % my_email)
					except:
						Warning(cur_func,globs['mes'].email_agent_failure)
			# Скопировать номер кошелька
			def copy_wallet_no(event):
				cur_func=sys._getframe().f_code.co_name
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					clipboard_copy(my_yandex_money)
					InfoMessage(cur_func,globs['mes'].wallet_no_copied)
					root.withdraw()
			# Открыть веб-страницу с лицензией
			def open_license_url(event):
				cur_func=sys._getframe().f_code.co_name
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					try:
						webbrowser.open(globs['license_url'])
					except:
						Warning(cur_func,browser_failure % globs['license_url'])
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				top=tk.Toplevel(root)
				top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
				top.title(globs['mes'].about)
				frame1=tk.Frame(top)
				frame1.pack(expand=1,fill='both',side='top')
				frame2=tk.Frame(top)
				frame2.pack(expand=1,fill='both',side='left')
				frame3=tk.Frame(top)
				frame3.pack(expand=1,fill='both',side='right')
				if globs['bool']['ShowWallet']:
					label=tk.Label(frame1,font=globs['var']['font_style'],text=globs['mes'].about_text)
				else:
					label=tk.Label(frame1,font=globs['var']['font_style'],text=globs['mes'].about_text_no_wallet)
				label.pack()
				if globs['bool']['ShowWallet']:
					# Номер электронного кошелька
					create_button(parent_widget=frame2,text=globs['mes'].btn_wallet_no,hint=globs['mes'].hint_wallet_no,action=copy_wallet_no,side='left')
					# Лицензия
					create_button(parent_widget=frame3,text=globs['mes'].btn_license,hint=globs['mes'].hint_license,action=open_license_url,side='left')
				else:
					# Лицензия
					create_button(parent_widget=frame2,text=globs['mes'].btn_license,hint=globs['mes'].hint_license,action=open_license_url,side='left')
				# Отправить письмо автору
				create_button(parent_widget=frame3,text=globs['mes'].btn_email_author,hint=globs['mes'].hint_email_author,action=response_back,side='right')
				top.wait_window()
		#----------------------------------------------------------------------
		# Перейти на элемент истории
		def get_history(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				try:
					# При выборе пункта возвращается кортеж с номером пункта
					selection=listbox.curselection()
					# ВНИМАНИЕ: В Python 3.4 selection[0] является числом, в более старших интерпретаторах, а также в сборках на их основе - строкой. Для совместимости преобразуем в число.
					#db['search']=listbox.get(selection[0])
					db['history_index']=len(db['history'])-int(selection[0])-1
					db['search']=db['history'][db['history_index']]
					# Список истории запросов идет в обратном порядке, поэтому необходимо синхронизировать
					db['url']=db['history_url'][db['history_index']]
					log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
					log(cur_func,lev_debug,globs['mes'].history_elem_selected % db['search'])
				except:
					# По непонятным пока причинам после переключения интерфейса на английский может возникнуть ошибка globs['mes'].history_failure.
					#Warning(cur_func,globs['mes'].history_failure)
					log(cur_func,lev_warn,globs['mes'].history_failure)
				if globs['bool']['AutoHideHistory']:
					# Уже содержит close_top()
					toggle_history(None)
				else:
					close_top(event)
				# Выносим в самый конец, чтобы нейтрализовать режим 'skip' в toggle_history()
				db['mode']='url'
		#----------------------------------------------------------------------
		# Скопировать элемент истории
		def copy_history(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				selection=err_mes_copy
				try:
					selection=listbox.get(listbox.curselection()[0])
					log(cur_func,lev_debug,globs['mes'].history_elem_selected % selection)
				except:
					# По непонятным пока причинам после переключения интерфейса на английский может возникнуть ошибка globs['mes'].history_failure.
					#Warning(cur_func,globs['mes'].history_failure)
					log(cur_func,lev_warn,globs['mes'].history_failure)
				clipboard_copy(selection)
				if globs['bool']['AutoHideHistory']:
					toggle_history(None)
		#----------------------------------------------------------------------
		# Очистить строку поиска
		def clear_search_field(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				search_field.delete(0,'end')
		#----------------------------------------------------------------------
		# Очистить строку поиска и вставить в нее содержимое буфера обмена
		def paste_search_field(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				search_field.delete(0,'end')
				search_field.selection_clear()
				if Standalone:
					search_field.insert(0,clipboard_paste())
				else:
					search_field.insert(0,apply_autocor(clipboard_paste(),Auto=True))
				return 'break'
		#----------------------------------------------------------------------
		# Очистить Историю
		def clear_history(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				db['mode']='search'
				db['search']=globs['mes'].welcome
				log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
				db['history']=[]
				db['history_url']=[]
				db['history_index']=0
				close_top(event)
		#----------------------------------------------------------------------
		# Следить за буфером обмена
		def watch_clipboard(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if db['mode']=='clipboard':
					db['mode']='search'
				else:
					db['mode']='clipboard'
				top.destroy()
				root.deiconify()
		#----------------------------------------------------------------------
		# Открыть URL текущей статьи в браузере
		def open_in_browser(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if not 'url' in db:
					if db['terms']['num'] > 0:
						db['url']=db['terms']['url'][0]
					else:
						db['url']=online_url_safe
					log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
				try:
					webbrowser.open(db['url'])
				except:
					Warning(cur_func,globs['mes'].browser_failure % db['url'])
		#----------------------------------------------------------------------
		# Переключить язык интерфейса с русского на английский и наоборот
		def change_ui_lang(event):
			cur_func=sys._getframe().f_code.co_name
			# Если включить проверку, будем все время получать SyntaxWarning
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				toggle_ui_lang()
				close_top(event)
		#----------------------------------------------------------------------
		# Перейти на предыдущий запрос
		def go_back(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if not 'history_index' in db:
					db['history_index']=len(db['history'])
				if db['history_index'] > 0:
					db['history_index']-=1
					if db['mode']!='url':
						db['mode']='url'
					db['search']=db['history'][db['history_index']]
					log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
					db['url']=db['history_url'][db['history_index']]
					log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
					close_top(event)
		#----------------------------------------------------------------------
		# Перейти на следующий запрос
		def go_forward(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if not 'history_index' in db:
					db['history_index']=len(db['history'])
				if db['history_index'] < len(db['history'])-1:
					db['history_index']+=1
					if db['mode']!='url':
						db['mode']='url'
					db['search']=db['history'][db['history_index']]
					log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
					db['url']=db['history_url'][db['history_index']]
					log(cur_func,lev_debug,"db['url']: %s" % str(db['url']))
					close_top(event)
		#----------------------------------------------------------------------
		# Найти слово/слова в статье
		def search_article(direction='forward'): # clear, forward, backward
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				if direction=='clear': # Начать поиск заново
					if 'search_list' in db:
						del db['search_list']
					direction='forward'
				elif direction!='forward' and direction!='backward':
					ErrorMessage(cur_func,globs['mes'].unknown_mode % (str(direction),'clear, forward, backward'))
				if globs['AbortAll']:
					log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
				else:
					# Создаем начальные значения
					if not 'search_list' in db:
						search_str=text_field(title=globs['mes'].search_str,Small=True) #search_field.get()
						search_str=search_str.strip(' ').strip(dlb)
						root.withdraw()
						if not empty(search_str):
							# Создать список позиций всех совпадений по поиску в статье
							db['search_list']=[]
							i=0
							while i < db['terms']['num']:
								if search_str in db['terms']['phrases'][i].lower():
									db['search_list'].append(i)
								i+=1
							if len(db['search_list']) > 0:
								if direction=='forward':
									# Номер текущего выделенного совпадения ('search_article_pos') в списке совпадений ('search_list')
									db['search_article_pos']=-1
								elif direction=='backward':
									db['search_article_pos']=len(db['search_list'])
					if 'search_list' in db:
						# Продолжаем поиск с предыдущего места
						if len(db['search_list']) > 0:
							if direction=='forward':
								if db['search_article_pos']+1 < len(db['search_list']):
									db['search_article_pos']+=1
								else:
									db['search_article_pos']=0
							elif direction=='backward':
								if db['search_article_pos'] > 0:
									db['search_article_pos']-=1
								else:
									db['search_article_pos']=len(db['search_list'])-1
							res[0]=db['search_list'][db['search_article_pos']]
							# Нужно дополнительно определять страницу, shift_screen + select_term работают неточно без указания доп. параметров, некоторые из которых, я, похоже, указать забыл
							detect_page(mode='term_no')
							shift_screen(mode='still')
							select_term(ForceScreenFit=False)
		#----------------------------------------------------------------------
		# Сохранить статью на диск
		def save_article(event):
			cur_func=sys._getframe().f_code.co_name
			if globs['AbortAll']:
				log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
			else:
				opt=SelectFromList(globs['mes'].select_action,globs['mes'].actions,[globs['mes'].save_article_as_html,globs['mes'].save_article_as_txt,globs['mes'].copy_article_html,globs['mes'].copy_article_txt],Insist=False,Critical=False)
				if not empty(opt):
					if opt==globs['mes'].save_article_as_html:
						# Ключ 'html' может быть необходим для записи файла, которая производится в кодировке UTF-8, поэтому, чтобы полученная веб-страница нормально читалась, меняем кодировку вручную.
						# Также меняем сокращенные гиперссылки на полные, чтобы они работали и в локальном файле.
						dialog_save_file(db['html'].replace('charset=windows-1251"','charset=utf-8"').replace('<a href="m.exe?','<a href="'+online_url_root).replace('../c/m.exe?',online_url_root),filetypes=((globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*')),Critical=False)
					elif opt==globs['mes'].save_article_as_txt:
						dialog_save_file(db['page'],filetypes=((globs['mes'].plain_text,'.txt'),(globs['mes'].all_files,'*')),Critical=False)
					elif opt==globs['mes'].copy_article_html:
						# Копирование веб-кода в буфер обмена полезно разве что в целях отладки, поэтому никак не меняем этот код.
						clipboard_copy(db['html'])
					elif opt==globs['mes'].copy_article_txt:
						clipboard_copy(db['page'])
				root.withdraw()
		#--------------------------------------------------------------------------
		if globs['bool']['AlwaysMaximize']:
			if sys_type=='lin':
				top.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				top.wm_state(newstate='zoomed')
		else:
			top.geometry(globs['var']['window_size'])
		if globs['bool']['mclientSaveTitle']:
			top.title(globs['mes'].mclient % build_ver)
		else:
			if db['FirstLaunch']:
				top.title(globs['mes'].mclient % build_ver)
			else:
				top.title(db['search'])
		# Only black-and-white icons of XBM format
		#top.wm_iconbitmap(bitmap='@'+globs['var']['icon_mclient'])
		# Иконку надо определять здесь, поскольку запуск может быть не Standalone
		top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
		top.protocol("WM_DELETE_WINDOW", lambda: quit_top(None))
		# tmp
		top.update_idletasks()
		globs['top']['width']=top.winfo_width()
		globs['top']['height']=top.winfo_height()
		log(cur_func,lev_info,globs['mes'].widget_sizes % ('top',globs['top']['width'],globs['top']['height']))
		#root.protocol("WM_DELETE_WINDOW",quit_now)
		# Создание каркаса с предыдущими поисковыми запросами
		frame_history=tk.Frame(top)
		if db['ShowHistory']==True:
			frame_history.pack(expand=1,side='left',fill='both')
		# Предыдущие поисковые запросы
		listbox=tk.Listbox(frame_history,font=globs['var']['font_history'])
		if db['ShowHistory']==True:
			listbox.pack(expand=1,side='top',fill='both')
		for i in range(len(db['history'])):
			listbox.insert(0,db['history'][i])
		# Создание каркаса с полем ввода, кнопкой выбора направления перевода и кнопкой выхода
		frame_panel=tk.Frame(top)
		frame_panel.pack(expand=0,fill='both',side='bottom')
		# Поле ввода поисковой строки
		search_field=tk.Entry(frame_panel)
		if globs['bool']['TextButtons']:
			search_field.pack(side='left')
		else:
			# Подгоняем высоту поисковой строки под высоту графических кнопок; значение 5 подобрано опытным путем
			search_field.pack(side='left',ipady=5)
		if db['FirstLaunch'] and not Standalone:
			paste_search_field(None)
		# Кнопка для "чайников", заменяет Enter в search_field
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_translate,hint=globs['mes'].btn_translate,action=go_search,icon_path=globs['var']['icon_go_search']) # В данном случае btn = hint
		# Если кнопки только текстовые, то все они не поместятся на экране, поэтому в текстовом режиме вспомогательные кнопки можно скрыть
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка очистки строки поиска
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_clear,hint=globs['mes'].hint_clear_search_field,action=clear_search_field,icon_path=globs['var']['icon_clear_search_field'])
			# Вспомогательная кнопка вставки
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_paste,hint=globs['mes'].hint_paste_clipboard,action=paste_search_field,icon_path=globs['var']['icon_paste'])
			# Вспомогательная кнопка вставки текущего запроса
			if 'history' in db and len(db['history']) > 0:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_repeat_sign,hint=globs['mes'].hint_paste_cur_request,action=insert_repeat_sign,icon_path=globs['var']['icon_repeat_sign'])
			else:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_repeat_sign,hint=globs['mes'].hint_paste_cur_request,action=insert_repeat_sign,icon_path=globs['var']['icon_repeat_sign_off'])
			# Вспомогательная кнопка вставки предыдущего запроса
			if 'history' in db and len(db['history']) > 1:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_repeat_sign2,hint=globs['mes'].hint_paste_prev_request,action=insert_repeat_sign2,icon_path=globs['var']['icon_repeat_sign2'])
			else:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_repeat_sign2,hint=globs['mes'].hint_paste_prev_request,action=insert_repeat_sign2,icon_path=globs['var']['icon_repeat_sign2_off'])
		# Выпадающий список с вариантами направлений перевода
		var=tk.StringVar(top)
		var.set(globs['cur_pair'])
		option_menu=tk.OptionMenu(frame_panel,var,*pairs,command=change_pair).pack(side='left',anchor='center')
		# Выпадающий список для вставки спец. символов
		
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка перехода на предыдущую статью
			if 'history_index' in db and 'history' in db and db['history_index'] > 0:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_prev,hint=globs['mes'].hint_preceding_article,action=go_back,icon_path=globs['var']['icon_go_back'])
			else:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_prev,hint=globs['mes'].hint_preceding_article,action=go_back,icon_path=globs['var']['icon_go_back_off'])
			# Вспомогательная кнопка перехода на следующую статью
			if 'history_index' in db and db['history_index'] < len(db['history'])-1:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_next,hint=globs['mes'].hint_following_article,action=go_forward,icon_path=globs['var']['icon_go_forward'])
			else:
				create_button(parent_widget=frame_panel,text=globs['mes'].btn_next,hint=globs['mes'].hint_following_article,action=go_forward,icon_path=globs['var']['icon_go_forward_off'])
		# Кнопка включения/отключения истории
		button=create_button(parent_widget=frame_panel,text=globs['mes'].btn_history,hint=globs['mes'].hint_history,action=toggle_history,icon_path=globs['var']['icon_toggle_history'])
		create_binding(button,globs['var']['bind_clear_history'],clear_history)
		if globs['bool']['UseOptionalButtons']:
			# Вспомогательная кнопка очистки истории
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_clear_history,hint=globs['mes'].hint_clear_history,action=clear_history,icon_path=globs['var']['icon_clear_history'])
			# Вспомогательная кнопка перезагрузки статьи
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_reload,hint=globs['mes'].hint_reload_article,action=close_top,icon_path=globs['var']['icon_reload'])
		# Кнопка "Поиск в статье"
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_search,hint=globs['mes'].hint_search_article,action=lambda e:search_article(direction='clear'),icon_path=globs['var']['icon_search_article'])
		# Кнопка "Сохранить"
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_save,hint=globs['mes'].hint_save_article,action=save_article,icon_path=globs['var']['icon_save_article'])
		# Кнопка "Открыть в браузере"
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_in_browser,hint=globs['mes'].hint_in_browser,action=open_in_browser,icon_path=globs['var']['icon_open_in_browser'])
		# Кнопка "Буфер обмена"
		if 'mode' in db and db['mode']=='clipboard':
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_clipboard,hint=globs['mes'].hint_watch_clipboard,action=watch_clipboard,icon_path=globs['var']['icon_watch_clipboard_on'],fg='red')
		else:
			create_button(parent_widget=frame_panel,text=globs['mes'].btn_clipboard,hint=globs['mes'].hint_watch_clipboard,action=watch_clipboard,icon_path=globs['var']['icon_watch_clipboard_off'])
		# Кнопка переключения языка интерфейса
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_ui_lang,hint=globs['mes'].hint_ui_lang,action=change_ui_lang,icon_path=globs['var']['icon_change_ui_lang'])
		# Кнопка "О программе"
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_about,hint=globs['mes'].hint_about,action=show_about,icon_path=globs['var']['icon_show_about'])
		# Кнопка выхода
		create_button(parent_widget=frame_panel,text=globs['mes'].btn_x,hint=globs['mes'].hint_x,action=quit_now,icon_path=globs['var']['icon_quit_now'],side='right')
		frame=tk.Frame(top)
		frame.pack(expand=1,fill='both')
		#scrollbar=tk.Scrollbar(frame,repeatinterval=1000,jump=1,repeatdelay=1000)
		scrollbar=tk.Scrollbar(frame,jump=1)
		txt=tk.Text(frame,height=7,font=globs['var']['font_style'],wrap='word',yscrollcommand=scrollbar.set)
		txt.insert('1.0',db['page'])
		#--------------------------------------------------------------------------
		# Установка курсора в начало
		try:
			txt.mark_set('insert','1.0')
		except:
			mestype(cur_func,globs['mes'].cursor_insert_failure,Silent=False,Critical=False)
		#--------------------------------------------------------------------------
		# Выделение элементов
		# 1. Установка тэгов
		for i in range(db['all']['num']):
			pos1=db['all']['tk'][i][0]
			pos2=db['all']['tk'][i][-1]
			tag_type=db['all']['types'][i]
			try:
				txt.tag_add(tag_type,pos1,pos2)
				log(cur_func,lev_debug,globs['mes'].tag_added % (db['all']['types'][i],pos1,pos2))
			except:
				mestype(cur_func,globs['mes'].tag_addition_failure % (db['all']['types'][i],pos1,pos2),Silent=False,Critical=False)
		if globs['bool']['TermsColoredSep']:
			for i in range(len(db['borders'])):
				pos1=db['borders'][i][0]
				pos2=db['borders'][i][-1]
				try:
					txt.tag_add('borders',pos1,pos2)
					log(cur_func,lev_debug,globs['mes'].tag_added % ('borders',pos1,pos2))
				except:
					mestype(cur_func,globs['mes'].tag_addition_failure % ('borders',pos1,pos2),Silent=False,Critical=False)
		# 2. Настройка тэгов
		try:
			txt.tag_config('terms',foreground=globs['var']['color_terms'],font=globs['var']['font_terms'])
			log(cur_func,lev_debug,globs['mes'].tag_config % ('terms',globs['var']['color_terms'],globs['var']['font_terms']))
		except:
			mestype(cur_func,globs['mes'].tag_config_failure % ('terms',globs['var']['color_terms'],globs['var']['font_terms']),Silent=False,Critical=False)
		try:
			txt.tag_config('dics',foreground=globs['var']['color_dics'],font=globs['var']['font_dics'])
			log(cur_func,lev_debug,globs['mes'].tag_config % ('dics',globs['var']['color_dics'],globs['var']['font_dics']))
		except:
			mestype(cur_func,globs['mes'].tag_config_failure % ('dics',globs['var']['color_dics'],globs['var']['font_dics']),Silent=False,Critical=False)
		try:
			txt.tag_config('comments',foreground=globs['var']['color_comments'],font=globs['var']['font_comments'])
			log(cur_func,lev_debug,globs['mes'].tag_config % ('comments',globs['var']['color_comments'],globs['var']['font_comments']))
		except:
			mestype(cur_func,globs['mes'].tag_config_failure % ('coments',globs['var']['color_comments'],globs['var']['font_comments']),Silent=False,Critical=False)
		if globs['bool']['TermsColoredSep']:
			try:
				txt.tag_config('borders',background=globs['var']['color_borders'])
				log(cur_func,lev_debug,globs['mes'].tag_bg % ('borders',globs['var']['color_borders']))
			except:
				mestype(cur_func,globs['mes'].tag_bg_failure % 'borders',Silent=False,Critical=False)
		#--------------------------------------------------------------------------
		scrollbar.pack(side='right',fill='y')
		txt.config(state='disabled')
		txt.pack(expand=1,fill='both')
		#--------------------------------------------------------------------------
		# Возможно, здесь можно оптимизировать алгоритм
		# db['all']['pos'] и db['all']['pos_sl'] включают позиции начала и конца вхождений в статью, в отличие от результата text_analyse(), где ['first_syms_nf'], ['last_syms_nf'] и ['pos_sl'] прописаны для каждого символа, поэтому tk2pos надо делать на основе новой БД, а не db['all']
		if db['mode']!='skip':
			db['db_page']=analyse_text(db['page'],Truncate=False,Decline=False)
		# Поскольку область Истории изменяет размеры области терминов, то пересоздаем БД координат даже в режиме 'skip'
		db=get_coor_pages(txt,db)
		db=aggregate_pages(db)
		scrollbar_poses(db)
		#--------------------------------------------------------------------------
		scrollbar.config(command=custom_scroll)
		#--------------------------------------------------------------------------
		# Привязки: горячие клавиши и кнопки мыши
		create_binding(widget=listbox,binding=globs['var']['bind_get_history'],action=get_history) # При просто <Button-1> выделение еще не будет выбрано
		create_binding(widget=listbox,binding='<Return>',action=get_history)
		create_binding(widget=listbox,binding='<KP_Enter>',action=get_history)
		create_binding(widget=listbox,binding='<space>',action=get_history)
		create_binding(widget=listbox,binding=globs['var']['bind_copy_history'],action=copy_history)
		create_binding(widget=top,binding=globs['var']['bind_go_search'],action=go_search)
		create_binding(widget=top,binding=globs['var']['bind_go_search_alt'],action=go_search)
		create_binding(widget=search_field,binding=globs['var']['bind_clear_search_field'],action=clear_search_field)
		create_binding(widget=search_field,binding=globs['var']['bind_paste_search_field'],action=paste_search_field)
		# Перейти на предыдущую/следующую статью
		create_binding(widget=top,binding=globs['var']['bind_go_back'],action=go_back)
		create_binding(widget=top,binding=globs['var']['bind_go_forward'],action=go_forward)
		create_binding(widget=top,binding=globs['var']['bind_move_left'],action=move_left)
		create_binding(widget=top,binding=globs['var']['bind_move_right'],action=move_right)
		create_binding(widget=top,binding=globs['var']['bind_move_down'],action=move_down)
		create_binding(widget=top,binding=globs['var']['bind_move_up'],action=move_up)
		create_binding(widget=top,binding=globs['var']['bind_move_line_start'],action=move_line_start)
		create_binding(widget=top,binding=globs['var']['bind_move_line_end'],action=move_line_end)
		create_binding(widget=top,binding=globs['var']['bind_move_text_start'],action=move_text_start)
		create_binding(widget=top,binding=globs['var']['bind_move_text_end'],action=move_text_end)
		create_binding(widget=top,binding=globs['var']['bind_move_page_start'],action=move_page_start)
		create_binding(widget=top,binding=globs['var']['bind_move_page_end'],action=move_page_end)
		create_binding(widget=top,binding=globs['var']['bind_move_page_up'],action=move_page_up)
		create_binding(widget=top,binding=globs['var']['bind_move_page_down'],action=move_page_down)
		# Для перевода в области терминов используем кнопки мыши, но не альтернативные комбинации клавиш, поскольку предполагаются, что они для удобства совпадают с комбинациями клавиш для перевода в области поиска.
		# ВНИМАНИЕ: widget - только txt. Если поставить top, то кнопки во frame_panel не будут нормально работать.
		create_binding(widget=txt,binding=globs['var']['bind_go_url'],action=go_url)
		search_field.focus_force()
		if not Standalone:
			# Для выхода нельзя использовать Return, поскольку это конфликтует с Shift-Enter. Поэтому оставляем только Escape.
			create_binding(widget=top,binding='<Escape>',action=quit_now)
		create_binding(widget=top,binding=globs['var']['bind_copy_sel'],action=copy_sel)
		create_binding(widget=top,binding=globs['var']['bind_copy_sel_alt'],action=copy_sel)
		create_binding(widget=txt,binding=globs['var']['bind_copy_sel_alt2'],action=copy_sel)
		if sys_type=='win' or sys_type=='mac':
			create_binding(widget=top,binding='<MouseWheel>',action=mouse_wheel)
		else:
			create_binding(widget=top,binding='<Button 4>',action=mouse_wheel)
			create_binding(widget=top,binding='<Button 5>',action=mouse_wheel)
		create_binding(widget=txt,binding='<Motion>',action=mouse_sel)
		# Закрывать текущее окно с последующей перезагрузкой статьи в обычном режиме бессмысленно, поэтому, прямо указываем режим Буфера
		if 'mode' in db:
			if db['mode']=='clipboard':
				# Привязка к top может конфликтовать со строкой поиска
				create_binding(widget=txt,binding=globs['var']['bind_close_top'],action=close_top)
			elif Standalone:
				create_binding(widget=txt,binding=globs['var']['bind_close_top'],action=lambda e: iconify(widget=top))
			else:
				create_binding(widget=txt,binding=globs['var']['bind_close_top'],action=quit_top)
		create_binding(widget=top,binding=globs['var']['bind_quit_now'],action=quit_now)
		create_binding(widget=top,binding=globs['var']['bind_search_article_forward'],action=lambda e:search_article(direction='forward'))
		create_binding(widget=top,binding=globs['var']['bind_search_article_backward'],action=lambda e:search_article(direction='backward'))
		create_binding(widget=top,binding=globs['var']['bind_re_search_article'],action=lambda e:search_article(direction='clear'))
		create_binding(widget=top,binding=globs['var']['bind_reload_article'],action=close_top)
		create_binding(widget=top,binding=globs['var']['bind_save_article'],action=save_article)
		create_binding(widget=top,binding='Alt-F4',action=quit_top)
		create_binding(widget=top,binding=globs['var']['bind_search_field'],action=lambda e:search_field.focus_force())
		create_binding(widget=top,binding=globs['var']['bind_show_about'],action=show_about)
		#--------------------------------------------------------------------------
		# Выделение первого признака
		if 'mode' in db and db['mode']=='skip':
			if 'last_sel' in db:
				res[0]=db['last_sel']
			else:
				res[0]=0
		select_term()
		top.wait_window()
	return db

# Запустить article_field в виде встроенной функции или в виде отдельного приложения
def article_loop(Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	if globs['AbortAll']:
		log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
	else:
		root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file=globs['var']['icon_mclient']))
		db={}
		db['search']=globs['mes'].welcome
		log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
		if globs['AbortAll']:
			log(cur_func,lev_warn,globs['mes'].abort_func % cur_func)
		else:
			db['history']=[]
			db['history_url']=[]
			db['mode']='search' # 'url', 'clipboard', 'skip'
			db['Quit']=False
			db['ShowHistory']=False
			while True:
				if 'search_list' in db:
					del db['search_list']
				if db['Quit']:
					if Standalone:
						log(cur_func,lev_info,globs['mes'].goodbye)
						sys.exit()
					else:
						# Возвращаемся в основную программу и меняем пиктограмму на основную
						root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file=globs['var']['icon_main']))
						break
				elif db['mode']=='clipboard': # Переход на режимы 'search' и 'url' отключит режим 'clipboard'. Если создать дополнительную переменную для слежения за буфером, то не понятно, какому режиму отдавать предпочтение: если считать более приоритетным 'clipboard', то ручной переход на другие статьи не сработает
					old_clipboard=clipboard_paste()
					new_clipboard=old_clipboard
					root.withdraw()
					while old_clipboard==new_clipboard:
						sleep(1)
						if db['Quit'] and Standalone:
							log(cur_func,lev_info,globs['mes'].goodbye)
							sys.exit()
						new_clipboard=clipboard_paste()
						# Игнорировать URL, скопированные в буфер обмена
						if 'http://' in new_clipboard or 'www.' in new_clipboard or globs['IgnorePaste']:
							new_clipboard=old_clipboard
						globs['IgnorePaste']=False
					db['search']=new_clipboard
					log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
					db=get_online_article(db,IsURL=False,Standalone=Standalone)
					if globs['bool']['ShortHistory']:
						if not db['search'] in db['history']:
							db['history'].append(db['search'])
							log(cur_func,lev_info,globs['mes'].adding % str(db['search']))
							db['history_url'].append(db['url'])
							log(cur_func,lev_info,globs['mes'].adding % str(db['url']))
					else:
						db['history'].append(db['search'])
						log(cur_func,lev_info,globs['mes'].adding % str(db['search']))
						db['history_url'].append(db['url'])
						log(cur_func,lev_info,globs['mes'].adding % str(db['url']))
					db['history_index']=len(db['history'])
				elif db['mode']=='url':
					db=get_online_article(db,IsURL=True,Standalone=Standalone)
				elif db['mode']=='search':
					db=get_online_article(db,IsURL=False,Standalone=Standalone)
				# Предполагаем, что режим может быть 'skip' только после создания БД хотя бы для 1 статьи
				if db['mode']!='skip':
					db=prepare_page(db)
					if not_found_online in db['page']:
						Warning(cur_func,globs['mes'].term_not_found % db['search'])
						db['search']='' # Do not put here anything besides '' because globs['mes'].welcome or any other is not translated for all languages, and we do not obligatory have 'en-ru' pair here, so this can enter an infinite loop
						log(cur_func,lev_debug,"db['search']: %s" % str(db['search']))
					db=analyse_tags(db)
					db=prepare_search(db)
				db=article_field(db,Standalone=Standalone)
				if db['mode']!='skip' and not empty(db['search']):
					if globs['bool']['ShortHistory']:
						if not db['search'] in db['history']:
							db['history'].append(db['search'])
							db['history_url'].append(db['url'])
					else:
						db['history'].append(db['search'])
						db['history_url'].append(db['url'])
				db['FirstLaunch']=False
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<	

default_config(config='mclient',Init=True)
read_configs()
# I removed extra code, Standalone=False will not work
article_loop(Standalone=True)
