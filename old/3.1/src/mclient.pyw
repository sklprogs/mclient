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
# В Python 3 не работает просто import urllib, импорт должен быть именно такой, как здесь
import urllib.request, urllib.parse
import html.parser
import posixpath
from configparser import SafeConfigParser

# (C) Peter Sklyar, 2015. License: GPL v.3
# All third-party modules are the intellectual work of their authors.

# Нельзя закомментировать, поскольку cur_func нужен при ошибке чтения конфига (которое вне функций)
cur_func='MAIN'
build_ver='3.1'
config_file_root='main.cfg'
root=tk.Tk()

ui_lang='ru'
gpl3_url_ru='http://rusgpl.ru/rusgpl.html'
gpl3_url_en='http://www.gnu.org/licenses/gpl.html'
if ui_lang=='ru':
	import mes_ru as mes
	gpl3_url=gpl3_url_ru
else:
	import mes_en as mes
	gpl3_url=gpl3_url_en
mclientSaveTitle=False
	
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
cur_pair=default_pair
pairs=['ENG <=> RUS','DEU <=> RUS','SPA <=> RUS','FRA <=> RUS','NLD <=> RUS','ITA <=> RUS','LAV <=> RUS','EST <=> RUS','AFR <=> RUS','EPO <=> RUS','XAL <=> RUS','ENG <=> DEU','ENG <=> EST']
online_dic_urls=['http://www.multitran.ru/c/m.exe?l1=1&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=3&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=5&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=4&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=24&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=23&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=27&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=26&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=31&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=34&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=35&l2=2&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=3&s=%s','http://www.multitran.ru/c/m.exe?l1=1&l2=26&s=%s']
online_dic_url=online_dic_urls[0]
not_found_online='Вы знаете перевод этого слова? Добавьте его в словарь'
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
#------------------------------------------------------------------------------
# Bool
HistoryEnabled=False
# I removed extra code, InternalDebug=False will not work
InternalDebug=False

# Placeholder
def log(cur_func,level,log_mes,TransFunc=False):
	#print(cur_func,':',level,':',log_mes)
	pass

# Placeholder
def text_field_ro(title=mes.check,array='test',SelectAll=False,GoTo=''):
	#print(title,':',array)
	pass

# Ошибка
def ErrorMessage(cur_func='MAIN',cur_mes=err_mes_empty_error,Critical=True):
	root.withdraw()
	tkmes.showerror(mes.err_head,cur_mes)
	if Critical:
		log(cur_func,lev_crit,cur_mes)
		sys.exit()
	else:
		log(cur_func,lev_err,cur_mes)
	root.deiconify()

# Проверить существование файла
def exist(file):
	cur_func=sys._getframe().f_code.co_name
	if not os.path.exists(file):
		ErrorMessage(cur_func,mes.file_not_found % file)
		
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
	import win32clipboard
	sysdiv='\\'
else:
	import pyperclip # (C) Al Sweigart, al@inventwithpython.com, BSD License
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

parser=SafeConfigParser()
# Должен лежать в одном каталоге с программой
# Руководство питона предлагает использовать разные методы для разных платформ: http://docs.python.org/2/library/os.path.html
bin_dir=true_dirname(os.path.realpath(sys.argv[0]),UseLog=False)
config_file=bin_dir+sysdiv+config_file_root
exist(config_file)
try:
	parser.readfp(codecs.open(config_file,'r','utf-8'))
except:
	ErrorMessage(cur_func,mes.invalid_config % config_file)

# Проверить наличие секции в конфигурационном файле
def check_config_section(config_section):
	cur_func=sys._getframe().f_code.co_name
	if not parser.has_section(config_section):
		ErrorMessage(cur_func,mes.wrong_config_structure+dlb+dlb+mes.no_config_section % config_section)

# Проверить наличие параметра в конфигурационном файле
def check_config_option(config_section,config_option):
	cur_func=sys._getframe().f_code.co_name
	if not parser.has_option(config_section,config_option):
		ErrorMessage(cur_func,mes.wrong_config_structure+dlb+dlb+mes.no_config_option % (config_option,config_section))

# Загрузить параметр типа str из конфигурационного файла
def load_option(config_section,config_option):
	check_config_option(config_section,config_option)
	return parser.get(config_section,config_option)

# Загрузить параметр типа float из конфигурационного файла
def load_option_float(config_section,config_option):
	check_config_option(config_section,config_option)
	return parser.getfloat(config_section,config_option)

# Загрузить параметр типа int из конфигурационного файла
def load_option_int(config_section,config_option):
	check_config_option(config_section,config_option)
	return parser.getint(config_section,config_option)

# Загрузить параметр типа bool из конфигурационного файла
def load_option_bool(config_section,config_option):
	check_config_option(config_section,config_option)
	return parser.getboolean(config_section,config_option)

# Разделы конфигурационного файла
SectionLinuxSettings='Linux settings'
SectionWindowsSettings='Windows settings'
SectionMacSettings='Mac settings'
SectionVariables='Variables'
SectionIntegers='Integer Values'
SectionFloatings='Floating Values'
SectionBooleans='Boolean'
Sections=[SectionLinuxSettings,SectionWindowsSettings,SectionMacSettings,SectionVariables,SectionIntegers,SectionFloatings,SectionBooleans]

# Проверка наличия разделов
i=0
for i in range(len(Sections)):
	check_config_section(Sections[i])

# Custom
win_encoding='windows-1251'
default_encoding='utf-8'
# Неразрывный пробел, non-breaking space
nbspace=' '
font_style='Sans 14'
dlb='\n'
wdlb='\r\n'

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Загрузка раздела [Variables] конфигурационного файла
#color_terms='cyan'
color_terms=load_option(SectionVariables,'color_terms')
# Цвет, которым обозначается выделенный (текущий) термин в окне mclient
#color_terms_sel='cyan'
color_terms_sel=load_option(SectionVariables,'color_terms_sel')
# Цвет, которым обозначаются названия словарей в окне mclient
#color_dics='green'
color_dics=load_option(SectionVariables,'color_dics')
# Цвет, которым обозначаются комментарии и имена пользователей в окне mclient
#color_comments='gray'
color_comments=load_option(SectionVariables,'color_comments')
# Цвет, которым разграничиваются термины в окне mclient
#color_borders='lemon_chiffon'
color_borders=load_option(SectionVariables,'color_borders')
# Шрифт текста в области истории запросов (mclient)
#font_history='Sans 12'
font_history=load_option(SectionVariables,'font_history')
# Шрифт терминов в окне mclient
#font_terms='Sans 14'
font_terms=load_option(SectionVariables,'font_terms')
# Шрифт выделенного (текущего) термина в окне mclient
#font_terms_sel='Sans 14 bold italic'
font_terms_sel=load_option(SectionVariables,'font_terms_sel')
# Шрифт названий словарей в окне mclient
#font_dics='Sans 14'
font_dics=load_option(SectionVariables,'font_dics')
# Шрифт комментариев в окне mclient
#font_comments='Sans 14'
font_comments=load_option(SectionVariables,'font_comments')
# Принудительно задать размер окна (работает только при AlwaysMaximize==False)
#window_size='1024x768'
window_size=load_option(SectionVariables,'window_size')
# Путь к иконке mclient
# icon_mclient='/usr/local/bin/icon_64x64_dic.xbm'
icon_mclient=load_option(SectionVariables,'icon_mclient')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Загрузка раздела [Integers] конфигурационного файла
# Число пикселей с краев окна, текст в области которых считается нечитаемым и должен быть перенесен
# Чтобы отключить, выставьте 0
pixel_hack=load_option_int(SectionIntegers,'pixel_hack')
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Загрузка раздела [Booleans] конфигурационного файла
# Следует ли всегда отображать в окне mclient только название и версию клиента (True), или же отображать текущий запрос (False); при 1-м запросе всегда указывается название и версия клиента
#mclientSaveTitle=False
mclientSaveTitle=load_option_bool(SectionBooleans,'mclientSaveTitle')
# Всегда создавать новое окно на полный экран
#AlwaysMaximize=True
AlwaysMaximize=load_option_bool(SectionBooleans,'AlwaysMaximize')
# mclient: Выделять ли промежуток между терминами цветом color_borders; если нет, то термины будут разделены точкой с запятой
#TermsColoredSep=False
TermsColoredSep=load_option_bool(SectionBooleans,'TermsColoredSep')
#ShowWallet=True
ShowWallet=load_option_bool(SectionBooleans,'ShowWallet')

# Вопрос
def Question(cur_func='MAIN',cur_mes=err_mes_empty_question):
	root.withdraw()
	par=tkmes.askokcancel(mes.ques_head,cur_mes)
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
	tkmes.showwarning(mes.warn_head,cur_mes)
	root.deiconify()
	log(cur_func,lev_warn,cur_mes)
	
# Вставить из буфера обмена
def clipboard_paste():
	cur_func=sys._getframe().f_code.co_name
	if sys_type=='win':
		#set_keyboard_layout('ru')
		try:
			win32clipboard.OpenClipboard()
			if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
				line=win32clipboard.GetClipboardData()
			else:
				line=err_mes_unavail
				Warning(cur_func,mes.cf_text_failure)
			win32clipboard.CloseClipboard()
			line=str(line)
			if line==None:
				line=''
		except:
			line=err_mes_paste
			log(cur_func,lev_debug,str(line))
			Warning(cur_func,mes.clipboard_paste_failure)
		#set_keyboard_layout('en')
	else:
		try:
			line=pyperclip.paste()
		except:
			line=err_mes_paste
	# Возможно, здесь ему не лучшее место
	#if not line in cmd_err_mess:
	#	line=delete_double_line_breaks(line)
	log(cur_func,lev_debug,str(line))
	return line
	
# Создание корректной ссылки в Интернете (URI => URL)
def online_request(base_str,my_request_bytes): #str, bytes
	cur_func=sys._getframe().f_code.co_name
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
	start_time=time()
	#check_args(cur_func,[[text,mes.type_str],[Truncate,mes.type_bool]])
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
				if word.isalpha():			
					first_syms_nf+=[i]
					first_syms_nf_sl+=[k]
				elif i+1 < len(text):
					delta=i+1
					kdelta=k+1
					while delta < len(text) and not text[delta].isalpha():
						delta+=1
						kdelta+=1
					first_syms_nf+=[delta]
					first_syms_nf_sl+=[kdelta]
					log(cur_func,lev_info,mes.first_syms_cor % (i,delta))
				else:
					first_syms_nf+=[i]
					first_syms_nf_sl+=[k]
					log(cur_func,lev_warn,mes.first_syms_failure)
		k+=1
	# Добавление последнего слова
	if word!='' and word!=dlb:
		words.append(word)
	maxi=i
	words_num=len(words)
	sent_no=0
	for i in range(words_num):
		words_nf.append(prepare_str(words[i],Extended=True))
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
			log(cur_func,lev_warn,mes.zero_len_sent % i)
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
	#detailed_declined=decline_nom(words_nf,Decline=Decline)
	detailed_declined=[]
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
	log(cur_func,lev_info,mes.analysis_finished % str(end_time-start_time))
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
	# Проверка целостности входных данных
	#check_type(cur_func,lst,mes.type_lst)
	#for i in range(len(lst)):
	#	check_type(cur_func,lst[i],mes.type_lst)
	#	assert(len(lst[i])==4)
	#	check_args(cur_func,[[lst[i][0],mes.type_int],[lst[i][1],mes.type_int],[lst[i][2],mes.type_int],[lst[i][3],mes.type_int]])
	tk_lst=[]
	for i in range(len(lst)):
		tk_lst+=[[convert2tk(lst[i][0],lst[i][1],Even=False),convert2tk(lst[i][2],lst[i][3],Even=True)]]
	log(cur_func,lev_debug,str(tk_lst))
	return tk_lst

# Привести в вид, понимаемый виджетом Tk, список вида [sent_no,pos1]
def convert2tk(sent,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
	#check_args(cur_func,[[sent,mes.type_int],[pos,mes.type_int],[Even,mes.type_bool]])
	if Even:
		tk_str=str(sent+1)+'.'+str(pos+1)
	else:
		tk_str=str(sent+1)+'.'+str(pos)
	log(cur_func,lev_debug,str(tk_str))
	return tk_str
	
# Скопировать в буфер обмена
def clipboard_copy(line):
	cur_func=sys._getframe().f_code.co_name
	line=str(line)
	if sys_type=='win':
		#set_keyboard_layout('ru')
		try:
			win32clipboard.OpenClipboard()
			win32clipboard.EmptyClipboard()
			win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT,line)
			win32clipboard.CloseClipboard()
		except:
			# Иначе в окне не сработают горячие клавиши
			#set_keyboard_layout('en')
			text_field_ro(mes.clipboard_copy_failure,line,SelectAll=True)
			line=err_mes_copy
			log(cur_func,lev_debug,str(line))
		# Иначе скрипт останется на ru
		#set_keyboard_layout('en')
	else:
		pyperclip.copy(line)
		
# Вернуть веб-страницу онлайн-словаря с термином
def get_online_article(db,IsURL=False,Silent=False,Critical=False,Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	# db['search'] требуется всегда, даже если на входе URL
	# Если на входе URL, то читается db['url'], если же на входе строка, то читается db['search'] и создается db['url']
	if not IsURL:
		# Поскольку Multitran использует кодировку windows-1251, необходимо использовать ее. Поскольку некоторые символы не кодируются в win_encoding корректно, оставляем для них кодировку UTF-8.
		try:
			request_encoded=db['search'].encode(win_encoding)
		except:
			request_encoded=bytes(db['search'],encoding=default_encoding)
		# Некоторые версии питона принимают 'encode('windows-1251')', но не 'encode(encoding='windows-1251')'
		db['url']=online_request(online_dic_url,request_encoded)
	db['page']=''
	while db['page']=='':
		Success=False
		# Загружаем страницу
		try:
			# Если загружать страницу с помощью "page=urllib.request.urlopen(my_url)", то в итоге получится HTTPResponse, что полезно только для удаления тэгов JavaScript. Поскольку мы вручную удаляем все лишние тэги, то на выходе нам нужна строка.
			db['page']=urllib.request.urlopen(db['url']).read()
			log(cur_func,lev_info,mes.ok % db['search'])
			Success=True
		except:
			db['page']=''
			log(cur_func,lev_warn,mes.failed % db['search'])
			#mestype(cur_func,mes.webpage_unavailable,Silent=Silent,Critical=Critical)
			if not Question(cur_func,mes.webpage_unavailable_ques):
				if Standalone:
					sys.exit()
				else:
					break
		if Success: # Если страница не загружена, то понятно, что ее кодировку изменить не удастся
			try:
				# Меняем кодировку win_encoding на нормальную
				db['page']=db['page'].decode(win_encoding)
			except:
				mestype(cur_func,mes.wrong_html_encoding,Silent=Silent,Critical=Critical)
	return db
	
# Convert HTML entities to UTF-8 and perform other necessary operations
def prepare_page(db):
	cur_func=sys._getframe().f_code.co_name
	try:
		html_parser = html.parser.HTMLParser()
		db['page']=html_parser.unescape(db['page'])
	except:
		log(cur_func,lev_err,mes.html_conversion_failure)
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
				log(cur_func,lev_debug,mes.deleting_useless_elem % (i,db['page'][i]))
				if i >= 10 and i < len(db['page'])-10:
					log(cur_func,lev_debug,mes.context % ''.join(db['page'][i-10:i+10]))
				del db['page'][i]
				i-=1
			else:
				TagOpen=True
		if db['page'][i]=='>':
			if not TagOpen:
				log(cur_func,lev_info,mes.deleting_useless_elem % (i,db['page'][i]))
				if i >= 10 and i < len(db['page'])-10:
					log(cur_func,lev_info,mes.context % ''.join(db['page'][i-10:i+10]))
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
	start_time=time()
	db=tags_pos(db)
	db=extract_tags(db)
	db=remove_useless_tags(db)
	db=extract_tag_contents(db)
	end_time=time()
	log(cur_func,lev_info,mes.tag_analysis_timer % str(end_time-start_time))
	return db
	
# Create a list with positions of signs '<' and '>'
def tags_pos(db):
	cur_func=sys._getframe().f_code.co_name
	tag_borders=[]
	i=0
	while i < db['len_page']:
		# Signs '<' and '>' as such can cause serious problems since they can occur in invalid cases like "perform >>> conduct >> carry out (vbadalov)". The following algorithm is also not 100% precise but is better.
		if db['page'][i]=='<' or db['page'][i]=='>':
			tag_borders.append(i)
		i+=1
	if len(tag_borders) % 2 != 0:
		log(cur_func,lev_warn,mes.wrong_tag_num % len(tag_borders))
		if len(tag_borders) > 0:
			del tag_borders[-1]
		else:
			log(cur_func,lev_warn,mes.tag_borders_empty)
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
	db['tags']=[]
	for i in range(db['len_tag_borders']):
		# +1 because of slice peculiarities
		pos1=db['tag_borders'][i][0]
		pos2=db['tag_borders'][i][1]+1
		db['tags'].append(db['page'][pos1:pos2])
		log(cur_func,lev_debug,mes.extracting_tag % db['tags'][-1])
	db['len_tags']=len(db['tags'])
	log(cur_func,lev_info,mes.tags_found % (db['len_tags']))
	log(cur_func,lev_debug,str(db['tags']))
	return db
	
# Create a list of on-screen text elements for each useful tag
def extract_tag_contents(db):
	cur_func=sys._getframe().f_code.co_name
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
				log(cur_func,lev_warn,mes.wrong_tag % db['tags'][i])
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
					log(cur_func,lev_warn,mes.tag_near_text_end % db['tags'][i])
				else:
					if tag_pattern7 in db['tags'][i+1] or tag_pattern8 in db['tags'][i+1]:
						tmp_str=db['page'][pos1:pos2+1]
						# If we see symbols '<' or '>' there for some reason, then there is a problem in the tag extraction algorithm. We can make manual deletion of '<' and '>' there.
						if tmp_str=='' or tmp_str==' ':
							TermMatch=False
							log(cur_func,lev_warn,mes.empty_tag_contents % db['tags'][i])
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
						log(cur_func,lev_warn,mes.url_extraction_failure % url)
					if not TermMatch:
						log(cur_func,lev_warn,mes.useless_url % url)
			else:
				log(cur_func,lev_warn,mes.last_tag % db['tags'][i])
				TermMatch=False
		# Extracting comments
		if db['tags'][i]==tag_pattern3 or db['tags'][i]==tag_pattern5:
			pos1=db['tag_borders'][i][1]+1
			if pos1 >= db['len_page']:
				log(cur_func,lev_warn,mes.tag_near_text_end % db['tags'][i])
			else:
				if i+1 < db['len_tags']:
					pos2=db['tag_borders'][i+1][0]-1
				else:
					log(cur_func,lev_warn,mes.last_tag % db['tags'][i])
					if db['len_tag_borders'] > 0:
						pos2=db['tag_borders'][-1][1]
					else:
						pos2=pos1
						log(cur_func,lev_warn,mes.tag_borders_empty)
				tmp_str=db['page'][pos1:pos2+1]
				# Sometimes, the tag contents is just '('. We remove it, so the final text does not look like '( user_name'
				if tmp_str=='' or tmp_str==' ' or tmp_str=='|' or tmp_str=='(':
					log(cur_func,lev_warn,mes.empty_tag_contents % db['tags'][i])
				else:
					db['all']['phrases'].append(tmp_str)
					db['all']['types'].append('comments')
					db['all']['pos']+=[[pos1,pos2]]
					EntryMatch=True
		if EntryMatch:
			log(cur_func,lev_debug,mes.adding_url % url)
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
		log(cur_func,lev_warn,mes.entries_terms_empty)
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
	if InternalDebug:
		res_mes=''
		for i in range(db['all']['num']):
			res_mes+="i: %d" % i+tab+db['all']['types'][i]+tab+db['all']['phrases'][i]+tab+str(db['all']['pos'][i])+tab+db['all']['url'][i]+dlb
		text_field_ro(mes.db_all_check,res_mes)	
	return db
	
# Remove tags that are not relevant to the article structure
def remove_useless_tags(db):
	cur_func=sys._getframe().f_code.co_name
	tags_total=db['len_tags']
	i=0
	while i < db['len_tags']:
		#if tags[i].startswith(tag_pattern1) or tags[i].startswith(tag_pattern2) or tags[i].startswith(tag_pattern3) or tags[i].startswith(tag_pattern4) or tags[i]==tag_pattern5 or tags[i]==tag_pattern6 or tags[i]==tag_pattern7 or tags[i]==tag_pattern8:
		if tag_pattern1 in db['tags'][i] or tag_pattern2 in db['tags'][i] or tag_pattern3 in db['tags'][i] or tag_pattern4 in db['tags'][i] or tag_pattern5 in db['tags'][i] or tag_pattern6 in db['tags'][i] or tag_pattern7 in db['tags'][i] or tag_pattern8 in db['tags'][i]:
			log(cur_func,lev_debug,mes.tag_kept % db['tags'][i])
			pass
		else:
			log(cur_func,lev_debug,mes.deleting_tag % (i,db['tags'][i]))
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
	log(cur_func,lev_info,mes.tags_stat % (tags_total,db['len_tags'],tags_total-db['len_tags']))
	# Testing
	assert(db['len_tags']==db['len_tag_borders'])
	return db

# Adjust positions of entries for pretty viewing
def prepare_search(db):
	cur_func=sys._getframe().f_code.co_name
	# Removing unwanted values
	# We assume that a 'dic'-type entry shall be succeeded by a 'term'-type entry, not a 'comment'-type entry. Therefore, we delete 'comment'-type entries after 'dic'-type entries in order to ensure that dictionary abbreviations do not succeed full dictionary titles. We also can delete full dictionary titles and leave abbreviations instead.
	i=0
	while i < db['all']['num']:
		if i > 0:
			if db['all']['types'][i-1]=='dics' and db['all']['types'][i]=='comments':
				if '.' in db['all']['phrases'][i] or 'Макаров' in db['all']['phrases'][i] or 'Вебстер' in db['all']['phrases'][i] or 'Webster' in db['all']['phrases'][i] or 'Майкрософт' in db['all']['phrases'][i] or 'Microsoft' in db['all']['phrases'][i]:
					pos1=db['all']['pos'][i][0]
					pos2=db['all']['pos'][i][1]
					log(cur_func,lev_info,mes.deleting_useless_entry % db['page'][pos1:pos2+1])
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
			log(cur_func,lev_err,mes.wrong_delta % (db['all']['pos'][0][1],delta))
			delta_i=abs(delta_i)
		db['all']['pos'][0]=[0,db['all']['pos'][0][1]-delta]
	else:
		log(cur_func,lev_warn,mes.db_all_empty)
	for i in range(db['all']['num']):
		if i > 0:
			delta=db['all']['pos'][i][0]-db['all']['pos'][i-1][1]
			if delta < 2:
				log(cur_func,lev_err,mes.intersection % (db['all']['pos'][i-1][0],db['all']['pos'][i-1][1],db['all']['pos'][i][0],db['all']['pos'][i][1]))
			delta_i=db['all']['pos'][i][1]-db['all']['pos'][i][0]
			if delta_i < 0:
				log(cur_func,lev_err,mes.wrong_delta % (db['all']['pos'][i][1],db['all']['pos'][i][0]))
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
		log(cur_func,lev_warn,mes.no_entries)
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
	if InternalDebug:
		res_mes=[]
		for i in range(db['all']['num']):
			pos1=db['all']['pos'][i][0]
			pos2=db['all']['pos'][i][1]
			res_mes.append(db['page'][pos1:pos2+1])
		res_mes=str(res_mes)
		res_mes+=dlb+dlb+"db['all']['pos']:"+dlb+str(db['all']['pos'])
		text_field_ro(mes.db_check1,res_mes)
		text_field_ro(mes.db_check2,str(db['all']['dlbs']['pos']))
	#--------------------------------------------------------------------------
	# Two adjacent terms are either separated with a coloured space, or with a semicolumn
	if not TermsColoredSep:
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
		if InternalDebug:
			text_field_ro("db['page']:",db['page'])
	#--------------------------------------------------------------------------
	# Creating tkinter-specific values
	# list() is not enough!
	db['all']['pos_sl']=[]
	delta=0
	for i in range(db['all']['num']):
		if db['all']['pos'][i][0]-1 in db['all']['dlbs']['pos']:
			delta=db['all']['pos'][i][0]
		db['all']['pos_sl']+=[[db['all']['pos'][i][0]-delta,db['all']['pos'][i][1]-delta]]
		log(cur_func,lev_debug,mes.db_conv % (db['all']['pos'][i][0],db['all']['pos'][i][1],db['all']['pos_sl'][i][0],db['all']['pos_sl'][i][1]))
	log(cur_func,lev_debug,"db['all']['pos_sl']: %s" % str(db['all']['pos_sl']))
	assert(db['all']['num']==len(db['all']['pos_sl']))
	if db['all']['pos'] == db['all']['pos_sl']:
		log(cur_func,lev_warn,mes.db_alg)
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
	# In comparison with the last InternalDebug: +str(db['all']['tk'][i])
	if InternalDebug:
		res_mes=''
		for i in range(db['all']['num']):
			res_mes+="i: %d" % i+tab+db['all']['types'][i]+tab+db['all']['phrases'][i]+tab+str(db['all']['pos'][i])+tab+str(db['all']['pos_sl'][i])+tab+str(db['all']['tk'][i])+tab+db['all']['url'][i]+dlb
		text_field_ro(mes.db_check3,res_mes)
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
			log(cur_func,lev_err,mes.unknown_type % str(db['all']['types'][i]))
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
	if InternalDebug:
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
		text_field_ro(mes.db_check4,res_mes)
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
		text_field_ro(mes.db_check5,res_mes)
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
		log(cur_func,lev_warn,mes.no_line_breaks_in_article)
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
	if InternalDebug:
		res_mes="db['move_up']:"+dlb+str(db['move_up'])+dlb+dlb
		res_mes+="db['move_down']:"+dlb+str(db['move_down'])+dlb+dlb
		res_mes+="db['move_left']:"+dlb+str(db['move_left'])+dlb+dlb
		res_mes+="db['move_right']:"+dlb+str(db['move_right'])+dlb+dlb
		text_field_ro(mes.db_check6,res_mes)
	return db
	
# Конвертировать строку в целое число
def str2int(line):
	cur_func=sys._getframe().f_code.co_name
	par=None
	try:
		par=int(line)
	except:
		log(cur_func,lev_err,mes.convert_to_int_failure % line)
	log(cur_func,lev_debug,str(par))
	return par

# Конвертировать строку с позицией Tkinter вида '1.20' в список вида [sent_no,pos_no]
def convertFromTk(line,Even=False):
	cur_func=sys._getframe().f_code.co_name
	#check_args(cur_func,[[line,mes.type_str],[Even,mes.type_bool]])
	num_lst=line.split('.')
	assert(len(num_lst)==2)
	sent=str2int(num_lst[0])
	#check_type(cur_func,sent,mes.type_int)
	pos=str2int(num_lst[1])
	#check_type(cur_func,pos,mes.type_int)
	if Even:
		lst=[sent-1,pos-1]
	else:
		lst=[sent-1,pos]
	# Tkinter позволяет выделять так, что конец придется на первый (=нулевой) символ в начале предложения, и из-за Even получится отрицательное число. Компенсируем это.
	for i in range(len(lst)):
		if lst[i] < 0:
			log(cur_func,lev_warn,mes.negative % lst[i])
			lst[i]=0
	log(cur_func,lev_debug,str(lst))
	return lst

# Конвертировать числовую позицию формата int в позицию в формате Tkinter
# Пример: 20 => '1.20'
def pos2tk(text_db,pos,Even=False):
	cur_func=sys._getframe().f_code.co_name
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

# Преобразовать координаты заданного виджета из пикселей в Tkinter
def pixels2tk(widget,x,y,Silent=False,Critical=False):
	cur_func=sys._getframe().f_code.co_name
	try:
		tk_pos=widget.index('@%d,%d' % (x,y))
	except:
		tk_pos='1.0'
		mestype(cur_func,'Не удается преобразовать координаты виджета "%s" из пикселей в Tkinter для координат (%s,%s)' % (str(widget),str(x),str(y)),Silent=Silent,Critical=Critical)
	log(cur_func,lev_debug,tk_pos)
	return tk_pos
	
# Вычислить координаты текста для текущей видимой области
def get_page_coor(text_db,coor_db,page_no):
	cur_func=sys._getframe().f_code.co_name
	coor_db['pages'][page_no]={}
	coor_db['pages'][page_no]['up']={}
	coor_db['pages'][page_no]['up']['pix']={}
	coor_db['pages'][page_no]['down']={}
	coor_db['pages'][page_no]['down']['pix']={}
	coor_db['pages'][page_no]['up']['pix']['x']=coor_db['widget'].winfo_x()
	coor_db['pages'][page_no]['up']['pix']['y']=coor_db['widget'].winfo_y()
	coor_db['pages'][page_no]['down']['pix']['x']=coor_db['pages'][page_no]['up']['pix']['x']+coor_db['width']
	coor_db['pages'][page_no]['down']['pix']['y']=coor_db['pages'][page_no]['up']['pix']['y']+coor_db['height']
	coor_db['pages'][page_no]['up']['tk']=pixels2tk(coor_db['widget'],coor_db['pages'][page_no]['up']['pix']['x'],coor_db['pages'][page_no]['up']['pix']['y'])
	coor_db['pages'][page_no]['down']['tk']=pixels2tk(coor_db['widget'],coor_db['pages'][page_no]['down']['pix']['x'],coor_db['pages'][page_no]['down']['pix']['y'])
	coor_db['pages'][page_no]['up']['pos']=tk2pos(text_db,coor_db['pages'][page_no]['up']['tk'],Even=False)
	coor_db['pages'][page_no]['down']['pos']=tk2pos(text_db,coor_db['pages'][page_no]['down']['tk'],Even=True)
	log(cur_func,lev_debug,"coor_db['pages'][%d]['up']['pix']['x']: %d" % (page_no,coor_db['pages'][page_no]['up']['pix']['x']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['up']['pix']['y']: %d" % (page_no,coor_db['pages'][page_no]['up']['pix']['y']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['down']['pix']['x']: %d" % (page_no,coor_db['pages'][page_no]['down']['pix']['x']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['down']['pix']['y']: %d" % (page_no,coor_db['pages'][page_no]['down']['pix']['y']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['up']['tk']: %s" % (page_no,coor_db['pages'][page_no]['up']['tk']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['down']['tk']: %s" % (page_no,coor_db['pages'][page_no]['down']['tk']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['up']['pos']: %d" % (page_no,coor_db['pages'][page_no]['up']['pos']))
	log(cur_func,lev_debug,"coor_db['pages'][%d]['down']['pos']: %d" % (page_no,coor_db['pages'][page_no]['down']['pos']))
	return coor_db

# В зависимости от размеров окна вычислить координаты текста для каждой видимой области
def get_coor_pages(widget,text_db):
	cur_func=sys._getframe().f_code.co_name
	coor_db={}
	coor_db['widget']=widget
	coor_db['widget'].update_idletasks()
	coor_db['width']=coor_db['widget'].winfo_width()
	coor_db['height']=coor_db['widget'].winfo_height()
	if coor_db['height'] > pixel_hack:
		coor_db['height']-=pixel_hack
	if coor_db['width'] > pixel_hack:
		coor_db['width']-=pixel_hack
	log(cur_func,lev_debug,"coor_db['width']: %d" % coor_db['width'])
	log(cur_func,lev_debug,"coor_db['height']: %d" % coor_db['height'])
	coor_db['pages']={}
	page_no=0
	next_page_pos=0
	widget.yview('1.0')
	while next_page_pos < text_db['len']:
		coor_db=get_page_coor(text_db,coor_db,page_no)
		next_page_pos=coor_db['pages'][page_no]['down']['pos']+1
		if next_page_pos > text_db['len']-1:
			break
		else:
			next_page_tk=pos2tk(text_db,next_page_pos,Even=True)
			log(cur_func,lev_debug,'next_page_tk: %s' % next_page_tk)
			widget.yview(next_page_tk)
			page_no+=1
	widget.yview('1.0')
	coor_db['pages']['num']=page_no+1
	coor_db['cur_page_no']=0
	coor_db['direction']='right_down'
	log(cur_func,lev_debug,"coor_db['pages']['num']: %d" % coor_db['pages']['num'])
	return coor_db
	
# По позиции символа определить ближайший термин слева или справа
def get_adjacent_term(db,det,direction='right_down'):
	cur_func=sys._getframe().f_code.co_name
	term=''
	term_num=-1
	if direction=='right_down':
		for i in range(db['terms']['num']):
			if det <= db['terms']['pos'][i][0] or det <= db['terms']['pos'][i][1]:
				term_num=i
				term=db['terms']['phrases'][term_num]
				break
		log(cur_func,lev_debug,mes.right_term % (term_num,term))
	elif direction=='left_up':
		i=db['terms']['num']-1
		while i >= 0:
			if det >= db['terms']['pos'][i][0] or det >= db['terms']['pos'][i][1]:
				term_num=i
				term=db['terms']['phrases'][term_num]
				break
			i-=1
		log(cur_func,lev_debug,mes.left_term % (term_num,term))
	return term_num
	
# Определить номера терминов, которые являются пограничными для видимой области
def aggregate_pages(db,coor_db):
	cur_func=sys._getframe().f_code.co_name
	for i in range(coor_db['pages']['num']):
		coor_db['pages'][i]['up']['num']=get_adjacent_term(db,coor_db['pages'][i]['up']['pos'],direction='right_down')
		coor_db['pages'][i]['down']['num']=get_adjacent_term(db,coor_db['pages'][i]['down']['pos'],direction='left_up')
		if db['terms']['num'] > 0:
			log(cur_func,lev_debug,mes.db_pages_stat % (i,coor_db['pages'][i]['up']['num'],db['terms']['phrases'][coor_db['pages'][i]['up']['num']],coor_db['pages'][i]['down']['num'],db['terms']['phrases'][coor_db['pages'][i]['down']['num']]))
	return coor_db

# Отобразить окно со словарной статьей
def article_field(db,Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	top=tk.Toplevel(root)
	res=[0]
	root.withdraw()
	if not 'search' in db:
		db['search']=mes.welcome
	if not 'mode' in db:
		db['mode']='search'
	if not 'first_launch' in db:
		if Standalone:
			db['first_launch']=True
		else:
			db['first_launch']=False
	if Standalone:
		global HistoryEnabled
		if not 'history' in db:
			db['history']=[]
	# Search the selected term online
	def go_sel(event):
		cur_func=sys._getframe().f_code.co_name
		db['search']=db['terms']['phrases'][res[0]]
		db['mode']='search'
		top.destroy()
		root.deiconify()
	# Go to the URL of the current search
	def go_url(event):
		cur_func=sys._getframe().f_code.co_name
		db['search']=db['terms']['phrases'][res[0]]
		db['url']=db['terms']['url'][res[0]]
		db['mode']='url'
		db['history_index']=len(db['history'])
		top.destroy()
		root.deiconify()
	# Search the selected term online using the entry widget
	def go_search(event):
		cur_func=sys._getframe().f_code.co_name
		search_str=search_field.get()
		db['search']=search_str.strip(dlb)
		db['search']=search_str.strip(' ')
		db['mode']='search'
		# Обновляем индекс текущего запроса при добавлении элемента для поиска
		db['history_index']=len(db['history'])
		top.destroy()
		root.deiconify()
	# Copy to clipboard
	def copy_sel(event):
		cur_func=sys._getframe().f_code.co_name
		clipboard_copy(db['terms']['phrases'][res[0]])
		log(cur_func,lev_info,mes.copied_to_clipboard % str(db['terms']['phrases'][res[0]]))
		if db['mode']=='clipboard':
			top.destroy()
			root.deiconify()
		elif Standalone:
			top.iconify()
		else:
			top.destroy()
			root.deiconify()
			db['quit']=True
	# Close the root window without errors
	# Please note that quit_now() should have 1 argument, quit_top() - none of them
	def quit_now(event):
		cur_func=sys._getframe().f_code.co_name
		db['quit']=True
		top.destroy()
		root.deiconify()
	# Запрос на выход
	def quit_top():
		cur_func=sys._getframe().f_code.co_name
		if db['mode']!='clipboard':
			#if Question(cur_func,mes.ques_exit):
			#	log(cur_func,lev_info,mes.goodbye)
				db['quit']=True
		top.destroy()
		root.deiconify()
	# Определение текущего термина по координатам указателя
	def mouse_sel(event):
		cur_func=sys._getframe().f_code.co_name
		tk_pos=pixels2tk(txt,event.x,event.y,Silent=False,Critical=False)
		pos=tk2pos(db_page,tk_pos)
		res[0]=get_adjacent_term(db,pos)
		select_term(ForceScreenFit=True)
	# Выделение терминов
	def select_term(ForceScreenFit=True):
		cur_func=sys._getframe().f_code.co_name
		if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
			if ForceScreenFit:
				if not fits_screen():
					log(cur_func,lev_warn,mes.visible_selection)
					if coor_db['direction']=='right_down':
						res[0]=get_adjacent_term(db,coor_db['pages'][coor_db['cur_page_no']]['up']['pos'],coor_db['direction'])
					elif coor_db['direction']=='left_up':
						res[0]=get_adjacent_term(db,coor_db['pages'][coor_db['cur_page_no']]['down']['pos'],coor_db['direction'])
			pos1=db['terms']['pos'][res[0]][0]
			pos2=db['terms']['pos'][res[0]][1]
			pos1=pos2tk(db_page,pos1)
			pos2=pos2tk(db_page,pos2,Even=True)
			# Только 1 термин должен быть выделен, поэтому предварительно удаляем тэг выделения по всему тексту.
			try:
				txt.tag_remove('cur_term','1.0','end')
			except:
				log(cur_func,lev_err,'Не удалось удалить тэг "%s" в диапазоне %s-%s!' % ('cur_term','1.0','end'))
			try:
				txt.tag_add('cur_term',pos1,pos2)
				log(cur_func,lev_debug,mes.tag_added % ('cur_term',pos1,pos2))
			except:
				mestype(cur_func,mes.tag_addition_failure % ('cur_term',pos1,pos2),Silent=False,Critical=False)
		else:
			log(cur_func,lev_warn,mes.not_enough_input_data)
		# 2. Настройка тэга
		try:
			txt.tag_config('cur_term',background=color_terms_sel,font=font_terms_sel)
			log(cur_func,lev_debug,mes.tag_config % ('cur_term',color_terms_sel,font_terms_sel))
		except:
			mestype(cur_func,mes.tag_config_failure % ('cur_term',color_terms_sel,font_terms_sel),Silent=False,Critical=False)
	# Определить, входит ли текущий термин в видимую часть экрана
	def fits_screen():
		cur_func=sys._getframe().f_code.co_name
		# Вернуть True, если смещение экрана не требуется (ввиду названия функции)
		Success=True
		# Если терминов нет, то смещать экран бесполезно
		if db['terms']['num'] > 0 and db['terms']['num'] > res[0]:
			if db['terms']['pos'][res[0]][0] >= coor_db['pages'][coor_db['cur_page_no']]['up']['pos'] and db['terms']['pos'][res[0]][-1] <= coor_db['pages'][coor_db['cur_page_no']]['down']['pos']:
				pass
			else:
				Success=False
		return Success
	# Обеспечить удобное пролистывание экрана
	# mode='normal': смещать экран согласно fits_screen()
	# mode='change': изменить номер страницы даже в том случае, если текущий термин находится в видимой области (необходимо для move_page_up/_down)
	# mode='still': не изменять номер страницы (необходимо для move_page_start/_end)
	def shift_screen(mode='normal'):
		cur_func=sys._getframe().f_code.co_name
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
				ErrorMessage(cur_func,mes.unknown_mode % (str(mode),'normal, change, still'))
			if DragScreen:
				log(cur_func,lev_info,mes.shift_screen_required)
				if coor_db['direction']=='right_down':
					if coor_db['cur_page_no'] < coor_db['pages']['num']-1:
						coor_db['cur_page_no']+=1
				elif coor_db['direction']=='left_up':
					if coor_db['cur_page_no'] > 0:
						coor_db['cur_page_no']-=1
				else:
					ErrorMessage(cur_func,mes.unknown_mode % (str(coor_db['direction']),'left_up, right_down'))
			else:
				log(cur_func,lev_info,mes.shift_screen_not_required)
			# Фактически, экран нужно смещать всегда
			yview_tk=coor_db['pages'][coor_db['cur_page_no']]['up']['tk']
			# Смещение экрана до заданного термина
			# Алгоритм работает только, если метка называется 'insert'
			try:
				txt.mark_set('insert',yview_tk)
				txt.yview('insert')
				log(cur_func,lev_info,mes.shift_screen % ('insert',yview_tk))
			except:
				log(cur_func,lev_err,mes.shift_screen_failure % 'insert')
	# Перейти на 1-й термин текущей строки	
	def move_line_start(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='left_up'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['home'][res[0]]
		shift_screen()
		select_term()
	# Перейти на последний термин текущей строки
	def move_line_end(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='right_down'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['end'][res[0]]
		shift_screen()
		select_term()
	# Перейти на 1-й термин статьи
	def move_text_start(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='left_up'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=0
		coor_db['cur_page_no']=0
		shift_screen()
		select_term()
	# Перейти на последний термин статьи
	def move_text_end(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='right_down'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['terms']['num']-1
		coor_db['cur_page_no']=coor_db['pages']['num']-1
		shift_screen()
		select_term()
	# Перейти на страницу вверх
	def move_page_up(event):
		cur_func=sys._getframe().f_code.co_name
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		coor_db['direction']='left_up'
		if coor_db['cur_page_no'] > 0:
			res[0]=coor_db['pages'][coor_db['cur_page_no']-1]['up']['num']
		else:
			res[0]=coor_db['pages'][coor_db['cur_page_no']]['up']['num']
		shift_screen(mode='change')
		select_term(ForceScreenFit=False)
		return "break"
	# Перейти на страницу вверх
	def move_page_down(event):
		cur_func=sys._getframe().f_code.co_name
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		coor_db['direction']='right_down'
		if coor_db['cur_page_no'] < coor_db['pages']['num']-1:
			res[0]=coor_db['pages'][coor_db['cur_page_no']+1]['up']['num']
		else:
			res[0]=coor_db['pages'][coor_db['cur_page_no']]['up']['num']
		shift_screen(mode='change')
		select_term(ForceScreenFit=False)
		return "break"
	# Перейти на 1-й термин текущей страницы
	def move_page_start(event):
		cur_func=sys._getframe().f_code.co_name
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		# Направление указывается для того, чтобы в любом случае не менять текущую страницу
		coor_db['direction']='left_up'
		res[0]=coor_db['pages'][coor_db['cur_page_no']]['up']['num']
		shift_screen(mode='still')
		select_term(ForceScreenFit=False)
		# Поскольку привязка идет по Shift, то tkinter может также осуществлять другие действия по Shift, например, выделение. "break" блокирует это поведение.
		return "break"
	# Перейти на последний термин текущей страницы
	def move_page_end(event):
		cur_func=sys._getframe().f_code.co_name
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		# Направление указывается для того, чтобы в любом случае не менять текущую страницу
		coor_db['direction']='left_up'
		res[0]=coor_db['pages'][coor_db['cur_page_no']]['down']['num']
		shift_screen(mode='still')
		select_term(ForceScreenFit=False)
		# Поскольку привязка идет по Shift, то tkinter может также осуществлять другие действия по Shift, например, выделение. "break" блокирует это поведение.
		return "break"
	# Перейти на предыдущий термин
	def move_left(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='left_up'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['move_left'][res[0]]
		shift_screen()
		select_term()
	# Перейти на следующий термин
	def move_right(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='right_down'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['move_right'][res[0]]
		shift_screen()
		select_term()
	# Перейти на строку вниз
	def move_down(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='right_down'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['move_down'][res[0]]
		shift_screen()
		select_term()
	# Перейти на строку вверх
	def move_up(event):
		cur_func=sys._getframe().f_code.co_name
		coor_db['direction']='left_up'
		txt.tag_remove('cur_term','1.0','end')
		log(cur_func,lev_debug,mes.tag_removed % ('cur_term','1.0','end'))
		res[0]=db['move_up'][res[0]]
		shift_screen()
		select_term()
	# Изменить направление (язык) перевода
	def change_pair(event):
		cur_func=sys._getframe().f_code.co_name
		global online_dic_url
		global cur_pair
		try:
			selected_pair=var.get()
		except:
			log(cur_func,lev_err,mes.lang_pair_undefined)
			selected_pair=cur_pair
		log(cur_func,lev_debug,mes.got_value % str(selected_pair))
		Found=False
		for i in range(len(pairs)):
			if selected_pair==pairs[i]:
				Found=True
				break
		if Found:
			online_dic_url=online_dic_urls[i]
		log(cur_func,lev_info,mes.lang_pair % selected_pair)
		log(cur_func,lev_debug,'URL: %s' % online_dic_url)
		cur_pair=selected_pair
	# Отобразить/скрыть историю запросов онлайн
	def toggle_history(event):
		cur_func=sys._getframe().f_code.co_name
		global HistoryEnabled
		if HistoryEnabled:
			log(cur_func,lev_info,mes.history_off)
			HistoryEnabled=False
			frame_history.pack_forget()
			listbox.pack_forget()
		else:
			log(cur_func,lev_info,mes.history_on)
			HistoryEnabled=True
			# Maybe there is a better way, update() or something, but I use the method that worked
			# Forget about all widgets except option_menu (which was packed directly after declaration)
			frame_history.pack_forget()
			listbox.pack_forget()
			frame_panel.pack_forget()
			search_field.pack_forget()
			button_search.pack_forget()
			PackOptionMenu=True
			try:
				option_menu.pack_forget()
			except:
				PackOptionMenu=False
			button_history.pack_forget()
			button_clipboard.pack_forget()
			button_browser.pack_forget()
			button_ui_lang.pack_forget()
			button_about.pack_forget()
			button_quit.pack_forget()
			frame.pack_forget()
			scrollbar.pack_forget()
			txt.pack_forget()
			# Pack widgets again
			frame_history.pack(expand=1,side='left',fill='both')
			listbox.pack(expand=1,side='top',fill='both')
			frame_panel.pack(expand=0,fill='both',side='bottom')
			search_field.pack(side='left')
			button_search.pack(side='left')
			# Иначе будет несколько OptionMenu
			if PackOptionMenu:
				option_menu=tk.OptionMenu(frame_panel,var,*pairs,command=change_pair).pack(side='left',anchor='center')
			button_history.pack(side='left')
			button_clipboard.pack(side='left')
			button_browser.pack(side='left')
			button_ui_lang.pack(side='left')
			button_about.pack(side='left')
			button_quit.pack(side='right')
			frame.pack(expand=1,fill='both')
			scrollbar.pack(side='right',fill='y')
			txt.pack(expand=1,fill='both')
	# Окно "О программе"
	def show_about(event):
		def response_back(event):
			cur_func=sys._getframe().f_code.co_name
			try:
				webbrowser.open('mailto:%s' % my_email)
			except:
				Warning(cur_func,mes.email_agent_failure)
		def copy_wallet_no(event):
			clipboard_copy(my_yandex_money)
			InfoMessage(cur_func,mes.wallet_no_copied)
			root.withdraw()
		def open_license_url(event):
			try:
				webbrowser.open(gpl3_url)
			except:
				Warning(cur_func,browser_failure % gpl3_url)
		top=tk.Toplevel(root)
		top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=icon_mclient))
		top.title(mes.about)
		frame1=tk.Frame(top)
		frame1.pack(expand=1,fill='both',side='top')
		frame2=tk.Frame(top)
		frame2.pack(expand=1,fill='both',side='left')
		frame3=tk.Frame(top)
		frame3.pack(expand=1,fill='both',side='right')
		if ShowWallet:
			label=tk.Label(frame1,font=font_style,text=mes.about_text)
		else:
			label=tk.Label(frame1,font=font_style,text=mes.about_text_no_wallet)
		label.pack()
		if ShowWallet:
			# Номер электронного кошелька
			button_money=tk.Button(frame2,text=mes.wallet_no)
			button_money.pack(side='left')
			button_money.bind('<Return>',copy_wallet_no)
			button_money.bind('<KP_Enter>',copy_wallet_no)
			button_money.bind('<space>',copy_wallet_no)
			button_money.bind('<Button-1>',copy_wallet_no)
		# Лицензия
		if ShowWallet:
			button_license=tk.Button(frame3,text=mes.view_license)
		else:
			button_license=tk.Button(frame2,text=mes.view_license)
		button_license.pack(side='left')
		button_license.bind('<Return>',open_license_url)
		button_license.bind('<KP_Enter>',open_license_url)
		button_license.bind('<space>',open_license_url)
		button_license.bind('<Button-1>',open_license_url)
		# Отправить письмо автору
		button_email=tk.Button(frame3,text=mes.email_author)
		button_email.pack(side='right')
		button_email.bind('<Return>',response_back)
		button_email.bind('<KP_Enter>',response_back)
		button_email.bind('<space>',response_back)
		button_email.bind('<Button-1>',response_back)
		top.wait_window()
	# Перейти на элемент истории
	def get_history(event):
		cur_func=sys._getframe().f_code.co_name
		try:
			# При выборе пункта, возвращается кортеж с номером пункта
			selection=listbox.curselection()
			db['search']=listbox.get(selection[0])
			db['mode']='search'
			log(cur_func,lev_debug,mes.history_elem_selected % db['search'])
		except:
			# По непонятным пока причинам после переключения интерфейса на английский может возникнуть ошибка mes.history_failure.
			#Warning(cur_func,mes.history_failure)
			log(cur_func,lev_warn,mes.history_failure)
		top.destroy()
		root.deiconify()
	# Очистить строку поиска
	def clear_search_field(event):
		cur_func=sys._getframe().f_code.co_name
		search_field.delete(0,'end')
	# Очистить строку поиска и вставить в нее содержимое буфера обмена
	def paste_search_field(event):
		cur_func=sys._getframe().f_code.co_name
		search_field.delete(0,'end')
		search_field.insert(0,clipboard_paste())
	# Очистить Историю
	def clear_history(event):
		cur_func=sys._getframe().f_code.co_name
		db['mode']='search'
		db['search']=mes.welcome
		db['history']=[]
		db['history_index']=0
		top.destroy()
		root.deiconify()
	# Следить за буфером обмена
	def watch_clipboard(event):
		cur_func=sys._getframe().f_code.co_name
		if db['mode']=='clipboard':
			db['mode']='search'
		else:
			db['mode']='clipboard'
		top.destroy()
		root.deiconify()
	# Открыть URL текущей статьи в браузере
	def open_in_browser(event):
		if not 'url' in db:
			if db['terms']['num'] > 0:
				db['url']=db['terms']['url'][0]
			else:
				db['url']=online_url_safe
		try:
			webbrowser.open(db['url'])
		except:
			Warning(cur_func,mes.browser_failure % db['url'])
	# Переключить язык интерфейса с русского на английский и наоборот
	def change_ui_lang(event):
		cur_func=sys._getframe().f_code.co_name
		global ui_lang
		global mes
		global gpl3_url
		if ui_lang=='en':
			ui_lang='ru'
			import mes_ru as mes
			gpl3_url=gpl3_url_ru
		else:
			ui_lang='en'
			import mes_en as mes
			gpl3_url=gpl3_url_en
		top.destroy()
		root.deiconify()
	# Перейти на предыдущий запрос
	def go_back(event):
		cur_func=sys._getframe().f_code.co_name
		if not 'history_index' in db:
			db['history_index']=len(db['history'])
		if db['history_index'] > 0:
			db['history_index']-=1
			if db['mode']!='search':
				db['mode']='search'
			db['search']=db['history'][db['history_index']]
			top.destroy()
			root.deiconify()
	# Перейти на следующий запрос
	def go_forward(event):
		cur_func=sys._getframe().f_code.co_name
		if not 'history_index' in db:
			db['history_index']=len(db['history'])
		if db['history_index'] < len(db['history'])-1:
			db['history_index']+=1
			if db['mode']!='search':
				db['mode']='search'
			db['search']=db['history'][db['history_index']]
			top.destroy()
			root.deiconify()
	#--------------------------------------------------------------------------
	if AlwaysMaximize:
		if sys_type=='lin':
			top.wm_attributes('-zoomed',True)
		# Win, Mac
		else:
			top.wm_state(newstate='zoomed')
	else:
		top.geometry(window_size)
	if mclientSaveTitle:
		top.title(mes.mclient % build_ver)
	else:
		if db['first_launch']:
			top.title(mes.mclient % build_ver)
			db['first_launch']=False
		else:
			top.title(db['search'])
	# Only black-and-white icons of XBM format
	#top.wm_iconbitmap(bitmap='@'+icon_mclient)
	# Иконку надо определять здесь, поскольку запуск может быть не Standalone
	top.tk.call('wm','iconphoto',top._w,tk.PhotoImage(file=icon_mclient))
	top.protocol("WM_DELETE_WINDOW",quit_top)
	#root.protocol("WM_DELETE_WINDOW",quit_now)
	if Standalone:
		# Создание каркаса с предыдущими поисковыми запросами
		frame_history=tk.Frame(top)
		if HistoryEnabled:
			frame_history.pack(expand=1,side='left',fill='both')
		# Предыдущие поисковые запросы
		listbox=tk.Listbox(frame_history,font=font_history)
		if HistoryEnabled:
			listbox.pack(expand=1,side='top',fill='both')
		for i in range(len(db['history'])):
			listbox.insert(0,db['history'][i])
		listbox.bind('<ButtonRelease-1>',get_history) # При просто <Button 1> выделение еще не будет выбрано
		listbox.bind('<Return>',get_history)
		listbox.bind('<KP_Enter>',get_history)
		listbox.bind('<space>',get_history)
		# Создание каркаса с полем ввода, кнопкой выбора направления перевода и кнопкой выхода
		frame_panel=tk.Frame(top)
		frame_panel.pack(expand=0,fill='both',side='bottom')
		# Поле ввода поисковой строки
		search_field=tk.Entry(frame_panel)
		search_field.pack(side='left')
		top.bind('<Return>',go_search)
		top.bind('<KP_Enter>',go_search)
		search_field.bind('<Button 3>',clear_search_field)
		search_field.bind('<Button 2>',paste_search_field)
		# Кнопка для "чайников", заменяет Enter в search_field
		button_search=tk.Button(frame_panel,text=mes.search)
		button_search.bind('<Return>',go_search)
		button_search.bind('<KP_Enter>',go_search)
		button_search.bind('<space>',go_search)
		button_search.bind('<Button 1>',go_search)
		button_search.pack(side='left')
		# Выпадающий список с вариантами направлений перевода
		var=tk.StringVar(top)
		var.set(cur_pair)
		option_menu=tk.OptionMenu(frame_panel,var,*pairs,command=change_pair).pack(side='left',anchor='center')
		# Кнопка включения/отключения истории
		button_history=tk.Button(frame_panel,text=mes.history)
		button_history.bind('<Button 1>',toggle_history)
		button_history.bind('<Return>',toggle_history)
		button_history.bind('<KP_Enter>',toggle_history)
		button_history.bind('<space>',toggle_history)
		button_history.pack(side='left')
		button_history.bind('<Button 3>',clear_history)
		# Кнопка "Буфер обмена"
		if db['mode']=='clipboard':
			button_clipboard=tk.Button(frame_panel,text=mes.watch_clipboard,fg='red')
		else:
			button_clipboard=tk.Button(frame_panel,text=mes.watch_clipboard)
		button_clipboard.bind('<Button 1>',watch_clipboard)
		button_clipboard.bind('<Return>',watch_clipboard)
		button_clipboard.bind('<KP_Enter>',watch_clipboard)
		button_clipboard.bind('<space>',watch_clipboard)
		button_clipboard.pack(side='left')
		# Кнопка "Открыть в браузере"
		button_browser=tk.Button(frame_panel,text=mes.in_browser)
		button_browser.bind('<Button 1>',open_in_browser)
		button_browser.bind('<Return>',open_in_browser)
		button_browser.bind('<KP_Enter>',open_in_browser)
		button_browser.bind('<space>',open_in_browser)
		button_browser.pack(side='left')
		# Кнопка переключения языка интерфейса
		button_ui_lang=tk.Button(frame_panel,text=mes.ui_lang)
		button_ui_lang.bind('<Button 1>',change_ui_lang)
		button_ui_lang.bind('<Return>',change_ui_lang)
		button_ui_lang.bind('<KP_Enter>',change_ui_lang)
		button_ui_lang.bind('<space>',change_ui_lang)
		button_ui_lang.pack(side='left')
		# Кнопка "О программе"
		button_about=tk.Button(frame_panel,text=mes.about,command=show_about)
		button_about.bind('<Button 1>',show_about) 
		button_about.bind('<Return>',show_about)
		button_about.bind('<KP_Enter>',show_about)
		button_about.bind('<space>',show_about)
		button_about.pack(side='left')
		# Кнопка выхода
		button_quit=tk.Button(frame_panel,text=mes.x,command=quit_now)
		button_quit.bind('<Button 1>',quit_now) 
		button_quit.bind('<Return>',quit_now)
		button_quit.bind('<KP_Enter>',quit_now)
		button_quit.bind('<space>',quit_now)
		button_quit.pack(side='right')
		# Перейти на предыдущую/следующую статью
		top.bind('<Control-Left>',go_back)
		top.bind('<Control-Right>',go_forward)
	frame=tk.Frame(top)
	frame.pack(expand=1,fill='both')
	scrollbar=tk.Scrollbar(frame)
	txt=tk.Text(frame,height=7,font=font_style,wrap='word',yscrollcommand=scrollbar.set)
	txt.insert('1.0',db['page'])
	#--------------------------------------------------------------------------
	# Установка курсора в начало
	try:
		txt.mark_set('insert','1.0')
	except:
		mestype(cur_func,mes.cursor_insert_failure,Silent=False,Critical=False)
	#--------------------------------------------------------------------------
	# Выделение элементов
	# 1. Установка тэгов
	for i in range(db['all']['num']):
		pos1=db['all']['tk'][i][0]
		pos2=db['all']['tk'][i][-1]
		tag_type=db['all']['types'][i]
		try:
			txt.tag_add(tag_type,pos1,pos2)
			log(cur_func,lev_debug,mes.tag_added % (db['all']['types'][i],pos1,pos2))
		except:
			mestype(cur_func,mes.tag_addition_failure % (db['all']['types'][i],pos1,pos2),Silent=False,Critical=False)
	if TermsColoredSep:
		for i in range(len(db['borders'])):
			pos1=db['borders'][i][0]
			pos2=db['borders'][i][-1]
			try:
				txt.tag_add('borders',pos1,pos2)
				log(cur_func,lev_debug,mes.tag_added % ('borders',pos1,pos2))
			except:
				mestype(cur_func,mes.tag_addition_failure % ('borders',pos1,pos2),Silent=False,Critical=False)
	# 2. Настройка тэгов
	try:
		txt.tag_config('terms',foreground=color_terms,font=font_terms)
		log(cur_func,lev_debug,mes.tag_config % ('terms',color_terms,font_terms))
	except:
		mestype(cur_func,mes.tag_config_failure % ('terms',color_terms,font_terms),Silent=False,Critical=False)
	try:
		txt.tag_config('dics',foreground=color_dics,font=font_dics)
		log(cur_func,lev_debug,mes.tag_config % ('dics',color_dics,font_dics))
	except:
		mestype(cur_func,mes.tag_config_failure % ('dics',color_dics,font_dics),Silent=False,Critical=False)
	try:
		txt.tag_config('comments',foreground=color_comments,font=font_comments)
		log(cur_func,lev_debug,mes.tag_config % ('comments',color_comments,font_comments))
	except:
		mestype(cur_func,mes.tag_config_failure % ('coments',color_comments,font_comments),Silent=False,Critical=False)
	if TermsColoredSep:
		try:
			txt.tag_config('borders',background=color_borders)
			log(cur_func,lev_debug,mes.tag_bg % ('borders',color_borders))
		except:
			mestype(cur_func,mes.tag_bg_failure % 'borders',Silent=False,Critical=False)
	scrollbar.config(command=txt.yview)
	scrollbar.pack(side='right',fill='y')
	txt.config(state='disabled')
	txt.pack(expand=1,fill='both')
	#--------------------------------------------------------------------------
	# Возможно, здесь можно оптимизировать алгоритм
	# db['all']['pos'] и db['all']['pos_sl'] включают позиции начала и конца вхождений в статью, в отличие от результата text_analyse(), где ['first_syms_nf'], ['last_syms_nf'] и ['pos_sl'] прописаны для каждого символа, поэтому tk2pos надо делать на основе новой БД, а не db['all']
	db_page=analyse_text(db['page'],Truncate=False,Decline=False)
	coor_db=get_coor_pages(txt,db_page)
	coor_db=aggregate_pages(db,coor_db)
	#--------------------------------------------------------------------------
	top.bind('<Left>',move_left)
	top.bind('<Right>',move_right)
	top.bind('<Down>',move_down)
	top.bind('<Up>',move_up)
	top.bind('<Home>',move_line_start)
	top.bind('<End>',move_line_end)
	top.bind('<Control-Home>',move_text_start)
	top.bind('<Control-End>',move_text_end)
	top.bind('<Shift-Home>',move_page_start)
	top.bind('<Shift-End>',move_page_end)
	top.bind('<Prior>',move_page_up)
	top.bind('<Next>',move_page_down)
	if Standalone:
		top.bind('<Shift-Return>',go_url)
		top.bind('<Shift-KP_Enter>',go_url)
		txt.bind('<Button-1>',go_url)
		search_field.focus_force()
	else:
		txt.bind('<Return>',quit_now)
		txt.bind('<KP_Enter>',quit_now)
		txt.bind('<Shift-Return>',quit_now)
		txt.bind('<Shift-KP_Enter>',quit_now)
		top.bind('<Escape>',quit_now)
		txt.focus_force()
	top.bind('<Control-Return>',copy_sel)
	# ПКМ используется еще для очистки Истории, поэтому нельзя использовать top
	txt.bind('<Button 3>',copy_sel)
	top.bind('<Control-KP_Enter>',copy_sel)
	top.bind('<Button 4>',move_page_up)
	top.bind('<Button 5>',move_page_down)
	txt.bind('<Motion>',mouse_sel)
	# Выделение первого признака
	select_term()
	top.wait_window()
	return db

# Запустить article_field в виде встроенной функции или в виде отдельного приложения
def article_loop(Standalone=False):
	cur_func=sys._getframe().f_code.co_name
	root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file=icon_mclient))
	db={}
	if Standalone:
		db['first_launch']=True
		db['search']=mes.welcome
	else:
		db['first_launch']=False
		# Копирование из окна в Linux провоцирует зависание программы
		if UsePaste:
			db['search']=persist(text_field_small_edit,[mes.search_word,clipboard_paste()])
		else:
			db['search']=persist(text_field_small,[mes.search_word])
		db['search']=apply_autocor(db['search'])
		clipboard_copy(db['search'])
		root.title(mes.searching)
		root.update()
	db['history']=[]
	db['mode']='search' # 'url', 'clipboard'
	while True:
		if db['mode']=='clipboard': # Переход на режимы 'search' и 'url' отключит режим 'clipboard'. Если создать дополнительную переменную для слежения за буфером, то не понятно, какому режиму отдавать предпочтение: если считать более приоритетным 'clipboard', то ручной переход на другие статьи не сработает
			old_buffer=clipboard_paste()
			while True:
				root.withdraw()
				sleep(1)
				if 'quit' in db:
					if db['quit']:
						if Standalone:
							log(cur_func,lev_info,mes.goodbye)
							sys.exit()
				new_buffer=clipboard_paste()
				# Игнорировать URL, скопированные в буфер обмена
				if 'http://' in new_buffer or 'www.' in new_buffer:
					new_buffer=old_buffer
				if new_buffer!=old_buffer:
					break
			db['search']=new_buffer
			if not db['search'] in db['history']:
				db['history'].append(db['search'])
			db['history_index']=len(db['history'])
		if db['mode']=='url':
			db=get_online_article(db,IsURL=True,Standalone=Standalone)
		else:
			db=get_online_article(db,IsURL=False,Standalone=Standalone)
		db=prepare_page(db)
		if not_found_online in db['page']:
			Warning(cur_func,mes.term_not_found % db['search'])
			db['search']='' # Do not put here anything besides '' because mes.welcome or any other is not translated for all languages, and we do not obligatory have 'en-ru' pair here, so this can enter an infinite loop
		else:
			if 'quit' in db:
				if db['quit']:
					if Standalone:
						log(cur_func,lev_info,mes.goodbye)
						sys.exit()
					else:
						root.tk.call('wm','iconphoto',root._w,tk.PhotoImage(file=icon_main))
						break
			db=analyse_tags(db)
			db=prepare_search(db)
			db=article_field(db,Standalone=Standalone)
			if Standalone:
				if not db['search'] in db['history']:
					db['history'].append(db['search'])

# I removed extra code, Standalone=False will not work
article_loop(Standalone=True)
