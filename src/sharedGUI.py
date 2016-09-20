#!/usr/bin/python3
#coding=UTF-8

import tkinter as tk
import tkinter.filedialog as dialog
import mes_ru as mes
import sys, os

from constants import *
globs['var'].update({'icon_main':'/usr/local/bin/icon_64x64_main.gif'})
from shared import log, Message, WriteTextFile, Text, h_os
#log = Log(Use=True,Write=True,Print=True,Short=False,file='/tmp/log')

# Вернуть тип параметра
def get_obj_type(obj,Verbal=True,IgnoreErrors=False):
	obj_type_str = ''
	obj_type_str = str(type(obj))
	obj_type_str = obj_type_str.replace("<class '",'')
	obj_type_str = obj_type_str.replace("'>",'')
	# int, float, str, list, dict, tuple, NoneType
	if Verbal:
		obj_type_str = obj_type_verbal(obj_type_str,IgnoreErrors=IgnoreErrors)
	#log.append('get_obj_type',lev_debug,obj_type_str)
	return obj_type_str
	
# Название типа на русском
def obj_type_verbal(obj_type_str,IgnoreErrors=False):
	obj_type_str = str(obj_type_str)
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
		Message(func='obj_type_verbal',type=lev_err,message=globs['mes'].unknown_mode % (obj_type_str,'str, list, dict, tuple, set, frozenset, int, long, float, complex, bool'))
	#log.append('obj_type_verbal',lev_debug,obj_type_str)
	return obj_type_str
	


# Класс для оформления root как виджета
class Root:

	def __init__(self):
		self.type = 'Root'
		self.widget = tk.Tk()

	def run(self):
		self.widget.mainloop()

	def show(self):
		self.widget.deiconify()

	def close(self):
		self.widget.withdraw()

	def destroy(self):
		self.widget.destroy()
		
	def update(self):
		self.widget.update()

# Привязать горячие клавиши или кнопки мыши к действию
def create_binding(widget,bindings,action): # widget, list, function
	bindings_type = get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
	if bindings_type == globs['mes'].type_str or bindings_type == globs['mes'].type_lst:
		if bindings_type == globs['mes'].type_str:
			bindings = [bindings]
		for i in range(len(bindings)):
			try:
				widget.bind(bindings[i],action)
			except tk.TclError:
				Message(func='create_binding',type=lev_err,message=globs['mes'].wrong_keybinding % bindings[i])
	else:
		Message(func='create_binding',type=lev_err,message=globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))
			
def confirm_quit(widget,Verbose=False):
	def _quit():
		log.append('_quit',lev_info,globs['mes'].goodbye)
		widget.destroy()
		sys.exit()
	if Verbose:
		if Message(func='confirm_quit',type=lev_ques,message=globs['mes'].close_window).Yes:
			_quit()
	else:
		_quit()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class WidgetShared:
	
	def focus(object):
		object.widget.focus()

	def insert(object,text,pos):
		if object.type == 'TextBox' or object.type == 'Entry':
			try:
				object.widget.insert(pos,text)
			except tk.TclError:
				try:
					object.widget.insert(pos,globs['mes'].insert_failure)
				except tk.TclError:
					Message(func='WidgetShared.insert',type=lev_err,message=globs['mes'].insert_failure)

	def font(object,font='Sans 11'): # font_style, globs['var']['menu_font']
		if object.type == 'TextBox' or object.type == 'Entry':
			object.widget.config(font=font)

	def set_state(object,ReadOnly=False):
		if object.type == 'TextBox' or object.type == 'Entry':
			if ReadOnly:
				object.widget.config(state='disabled')
				object.state = 'disabled'
			else:
				object.widget.config(state='normal')
				object.state = 'normal'
			
	def title(object,title=globs['mes'].text,my_program_title=''): # Родительский виджет
		if object.type == 'Toplevel' or object.type == 'Root':
			object.widget.title(title + my_program_title)
		
	def custom_buttons(object):
		if not object.Composite:
			if object.parent_obj.type == 'Toplevel' or object.parent_obj.type == 'Root':
				if object.state == 'disabled':
					object.parent_obj.close_button.widget.config(text=globs['mes'].btn_x)
				else:
					object.parent_obj.close_button.widget.config(text=globs['mes'].save_and_close)
				
	def icon(object,file): # Родительский объект
		if object.type == 'Toplevel' or object.type == 'Root':
			if file and os.path.exists(file):
				object.widget.tk.call('wm','iconphoto',object.widget._w,tk.PhotoImage(master=object.widget,file=file))
			

class Top:

	def __init__(self,parent_obj,Maximize=False,DestroyRoot=False):
		self.type = 'Toplevel'
		self.parent_obj = parent_obj
		self.count = 0
		# Lock = True - блокировать дальнейшее выполнение программы до попытки закрытия виджета. Lock = False позволяет создать одновременно несколько виджетов на экране. Они будут работать, однако, виджет с Lock = False будет закрыт при закрытии виджета с Lock = True. Кроме того, если ни один из виджетов не имеет Lock = True, то они все будут показаны и тут же закрыты.
		self.Lock = True
		self.widget = tk.Toplevel(self.parent_obj.widget)
		if DestroyRoot:
			self.widget.protocol("WM_DELETE_WINDOW",lambda:confirm_quit(self.parent_obj))
		else:
			self.widget.protocol("WM_DELETE_WINDOW",self.close)
		if Maximize:
			if h_os.sys() == 'lin':
				self.widget.wm_attributes('-zoomed',True)
			# Win, Mac
			else:
				self.widget.wm_state(newstate='zoomed')
		self.tk_trigger = tk.BooleanVar()
	
	def close(self,*args):
		self.widget.withdraw()
		if self.Lock:
			self.tk_trigger.set(True)
	
	def show(self,Lock=True):
		self.count += 1
		self.Lock = Lock
		self.widget.deiconify()
		self.center()
		if self.Lock:
			self.tk_trigger = tk.BooleanVar()
			self.widget.wait_variable(self.tk_trigger)
	
	def title(self,title='Title:'):
		WidgetShared.title(self,title=title)
		
	def icon(self,icon):
		WidgetShared.icon(self,icon)
		
	def center(self):
		# Make child widget always centered at the first time and up to a user's choice any other time (if the widget is reused).
		if self.count == 1:
			self.widget.update_idletasks()
			width = self.widget.winfo_screenwidth()
			height = self.widget.winfo_screenheight()
			size = tuple(int(_) for _ in self.widget.geometry().split('+')[0].split('x'))
			x = width/2 - size[0]/2
			y = height/2 - size[1]/2
			self.widget.geometry("%dx%d+%d+%d" % (size + (x, y)))



class TextBox:
	
	def __init__(self,parent_obj,Composite=False,side='top'):
		self.type = 'TextBox'
		self.Composite = Composite
		self.state = 'normal' # 'disabled' - отключить редактирование
		self.SpecialReturn = True
		self.Save = False
		self.tags = []
		self.marks = []
		self.parent_obj = parent_obj
		if self.parent_obj.type == 'Toplevel' or self.parent_obj.type == 'Root':
			self.widget = tk.Text(self.parent_obj.widget,font='Serif 14',wrap='word',height=1) #globs['var']['font_style']
		else:
			self.widget = tk.Text(self.parent_obj.widget,font='Serif 14',wrap='word') #globs['var']['font_style']
		self.widget.pack(expand=1,fill='both',side=side)
		self.scrollbar = tk.Scrollbar(self.widget,jump=0)
		self.widget.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.widget.yview)
		create_binding(widget=self.widget,bindings='<Control-a>',action=self.select_all)
		self.scrollbar.pack(side='right',fill='y')
		if not self.Composite and not hasattr(self.parent_obj,'close_button'):
			if self.parent_obj.type == 'Toplevel' or self.parent_obj.type == 'Root':
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
		WidgetShared.custom_buttons(self)
		self.custom_bindings()
		
	def close(self,*args):
		self.Save = True
		self.parent_obj.close()
		return 'break'
	
	# Только для несоставных виджетов
	def custom_bindings(self):
		if not self.Composite:
			self.widget.unbind('<Return>')
			if self.state == 'disabled' or self.SpecialReturn:
				# Разрешать считывать текст после нажатия Escape (в Entry запрещено)
				create_binding(widget=self.widget,bindings=['<Return>','<KP_Enter>','<Escape>'],action=self.close)
			else:
				create_binding(widget=self.widget,bindings=['<Escape>'],action=self.close)
	
	def get(self,Strip=True):
		if Strip:
			return self.widget.get('1.0','end').strip()
		else:
			return self.widget.get('1.0','end').strip('\n')

	def insert(self,text='text',pos='1.0'):
		WidgetShared.insert(self,text=text,pos=pos)

	def select_all(self,*args):
		self.tag_add()
		self.mark_add()
		return 'break'

	def tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
		try:
			self.widget.tag_remove(tag_name,pos1tk,pos2tk)
		except tk.TclError:
			log.append('TextBox.tag_remove',lev_warn,globs['mes'].tag_remove_failed % (tag_name,str(widget),pos1tk,pos2tk))
		if self.tags:
			try:
				self.tags.remove(tag_name)
			except ValueError:
				# todo: Что тут не работает?
				log.append('TextBox.tag_remove',lev_debug_err,globs['mes'].element_not_found % (tag_name,str(self.tags)))

	# Tk.Entry не поддерживает тэги и метки
	def tag_add(self,tag_name='sel',pos1tk='1.0',pos2tk='end',DeletePrevious=True):
		if DeletePrevious:
			self.tag_remove(tag_name)
		try:
			self.widget.tag_add(tag_name,pos1tk,pos2tk)
		except tk.TclError:
			log.append('TextBox.tag_add',lev_err,globs['mes'].tag_addition_failure % (tag_name,pos1tk,pos2tk))
		self.tags.append(tag_name)
	
	# Tk.Entry не поддерживает тэги и метки
	def mark_add(self,mark_name='insert',postk='1.0'):
		try:
			self.widget.mark_set(mark_name,postk)
			# todo: mes: adding mark
			log.append('TextBox.mark_add',lev_debug,globs['mes'].mark_added % (mark_name,postk))
		except tk.TclError:
			log.append('TextBox.tag_add',lev_err,globs['mes'].mark_addition_failure % (mark_name,postk))
		self.marks.append(mark_name)
	
	def mark_remove(self,mark_name='insert'):
		try:
			self.widget.mark_unset(mark_name)
			# todo: mes: removing mark
			log.append('TextBox.mark_remove',lev_debug,globs['mes'].mark_removed % (mark_name))
		except tk.TclError:
			log.append('TextBox.mark_remove',lev_err,globs['mes'].mark_removal_failure % mark_name)
		try:
			self.marks.remove(mark_name)
		except ValueError:
			log.append('TextBox.mark_remove',lev_err,globs['mes'].element_not_found % (mark_name,str(self.marks)))
			
	def clear_text(self):
		self.widget.delete('1.0','end')
		
	def clear_tags(self):
		i = len(self.tags) - 1
		while i >= 0:
			self.tag_remove(self.tags[i])
			i -= 1
	
	def clear_marks(self):
		i = len(self.marks) - 1
		while i >= 0:
			self.mark_remove(self.marks[i])
			i -= 1
	
	def goto(self,GoTo=''):
		if GoTo:
			try:
				goto_pos = self.widget.search(GoTo,'1.0','end')
				self.mark_add('goto',goto_pos)
				self.mark_add('insert',goto_pos)
				self.widget.yview('goto')
			except:
				log.append('TextBox.goto',lev_err,globs['mes'].shift_screen_failure % 'goto')
				
	# Сместить экран до позиции tkinter или до метки (тэги не работают)
	def scroll(self,mark):
		try:
			self.widget.yview(mark)
		except tk.TclError:
			log.append('TextBox.scroll',lev_warn,globs['mes'].shift_screen_failure % str(mark))
			
	# Сместить экран до позиции tkinter или до метки, если они не видны (тэги не работают)
	def autoscroll(self,mark):
		if not self.visible(mark):
			self.scroll(mark)
	
	def title(self,title='Title:'):
		WidgetShared.title(self.parent_obj,title)
		
	def icon(self,icon):
		WidgetShared.icon(self.parent_obj,icon)
	
	# Только для несоставных виджетов (ввиду custom_bindings)
	def update(self,title='Title:',text='Text:',GoTo='',SelectAll=False,ReadOnly=False,CursorPos='1.0',icon='',SpecialReturn=True):
		self.Save = False
		self.SpecialReturn = SpecialReturn
		# Операции над главным виджетом
		self.icon(icon=icon)
		self.title(title=title)
		# Иначе обновление текста не сработает. Необходимо делать до любых операций по обновлению текста.
		WidgetShared.set_state(self,ReadOnly=False)
		self.reset()
		# Присвоение аргументов
		self.insert(text=text)
		# Перейти в указанное место
		self.mark_add(mark_name='insert',postk=CursorPos)
		self.widget.yview(CursorPos)
		# Изменение статуса "Только чтение" поддерживается только виджетами tk.Text, tk.Entry и не поддерживается tk.Toplevel
		WidgetShared.set_state(self,ReadOnly=ReadOnly)
		WidgetShared.custom_buttons(self)
		if SelectAll:
			self.select_all()
		self.goto(GoTo=GoTo)
		self.widget.focus_set()
		# Только для несоставных виджетов
		self.custom_bindings()
		
	def visible(self,tk_pos):
		if self.widget.bbox(tk_pos):
			return True
		else:
			return False
			
	# Очистка текста, тэгов, меток
	def reset(self):
		self.clear_text()
		self.clear_tags()
		self.clear_marks()
		
		
		
class Entry:
	
	def __init__(self,parent_obj,Composite=False,side=None,ipady=None):
		self.type = 'Entry'
		self.Composite = Composite
		self.state = 'normal' # 'disabled' - отключить редактирование
		self.Save = False
		self.parent_obj = parent_obj
		self.widget = tk.Entry(self.parent_obj.widget,font='Sans 11') #globs['var']['menu_font']
		create_binding(widget=self.widget,bindings='<Control-a>',action=self.select_all)
		if side and ipady:
			self.widget.pack(side=side,ipady=ipady)
		elif side:
			self.widget.pack(side=side)
		elif ipady:
			self.widget.pack(ipady=ipady)
		else:
			self.widget.pack()
		if not self.Composite:
			# Тип родительского виджета может быть любым
			if not hasattr(self.parent_obj,'close_button'):
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
			WidgetShared.custom_buttons(self)
		self.custom_bindings()
	
	def custom_bindings(self):
		if not self.Composite:
			create_binding(widget=self.widget,bindings=['<Return>','<KP_Enter>'],action=self.close)
			create_binding(widget=self.widget,bindings='<Escape>',action=self.parent_obj.close)

	def show(self,*args):
		self.parent_obj.show()
	
	def close(self,*args):
		self.Save = True
		self.parent_obj.close()
	
	def get(self,Strip=False):
		if Strip:
			return self.widget.get().strip()
		else:
			return self.widget.get().strip('\n')

	def insert(self,text='text',pos=0):
		WidgetShared.insert(self,text=text,pos=pos)

	def select_all(self,*args):
		self.widget.select_clear()
		self.widget.select_range(0,'end')
		return 'break'

	def clear_text(self):
		self.widget.delete(0,'end')
		
	# GoTo работает только в tk.Text и оставлено для совместимости с ним (как и SpecialReturn)
	def update(self,title='Title:',text='',SelectAll=True,ReadOnly=False,CursorPos=0,icon='',GoTo='',SpecialReturn=False):
		self.Save = False
		# Операции над главным виджетом
		self.icon(icon=icon)
		self.title(title=title)
		# Иначе обновление текста не сработает. Необходимо делать до любых операций по обновлению текста.
		WidgetShared.set_state(self,ReadOnly=False)
		# Очистка текста
		self.clear_text()
		# Присвоение аргументов
		self.insert(text=text)
		# Перейти в указанное место
		self.widget.icursor(CursorPos) # int, 'end'
		# Изменение статуса "Только чтение" поддерживается только виджетами tk.Text, tk.Entry и не поддерживается tk.Toplevel
		WidgetShared.set_state(self,ReadOnly=ReadOnly)
		WidgetShared.custom_buttons(self)
		if SelectAll:
			self.select_all()
		self.widget.focus_set()
		
	def icon(self,icon):
		WidgetShared.icon(self.parent_obj,icon)
		
	def title(self,title='Title:'):
		WidgetShared.title(self.parent_obj,title)
		


class Frame:
	
	def __init__(self,parent_obj,expand=1,fill='both',side=None):
		self.type = 'Frame'
		self.parent_obj = parent_obj
		self.widget = tk.Frame(self.parent_obj.widget)
		if side:
			self.widget.pack(expand=expand,fill=fill,side=side)
		else:
			self.widget.pack(expand=expand,fill=fill)
			


# todo: Нужно ли на входе ,bindings=[]?
class Button:
	
	def __init__(self,parent_obj,action,hint='<Hint>',inactive_image_path=None,active_image_path=None,text='Press me',height=36,width=36,side='left',expand=0,fg='black',bd=0,hint_delay=800,hint_width=280,hint_height=40,hint_background='#ffffe0',hint_direction='top',hint_border_width=1,hint_border_color='navy',bindings=[],fill='both',TakeFocus=False):
		self.parent_obj = parent_obj
		self.action = action
		self.Status = False
		self.height = height
		self.width = width
		self.side = side
		self.expand = expand
		self.fill = fill
		self.inactive_image = self.image(inactive_image_path)
		self.active_image = self.image(active_image_path)
		if self.inactive_image:
			self.widget = tk.Button(self.parent_obj.widget,image=self.inactive_image,height=self.height,width=self.width,bd=bd,fg=fg)
		else:
			# В большинстве случаев текстовая кнопка не требует задания высоты и ширины по умолчанию, они определяются автоматически. Также в большинстве случаев для текстовых кнопок следует использовать рамку.
			self.widget = tk.Button(self.parent_obj.widget,bd=1,fg=fg)
		self.title(button_text=text)
		if bindings:
			hint_extended = hint + '\n' + str(bindings).replace('[','').replace(']','').replace('<','').replace('>','').replace("'",'')
		else:
			hint_extended = hint
		ToolTip(self.widget,text=hint_extended,hint_delay=hint_delay,hint_width=hint_width,hint_height=hint_height,hint_background=hint_background,hint_direction=hint_direction,button_side=side)
		self.show()
		create_binding(widget=self.widget,bindings=['<ButtonRelease-1>','<space>','<Return>','<KP_Enter>'],action=self.click)
		if TakeFocus:
			self.widget.focus_set()
	
	def title(self,button_text='Press me'):
		if button_text:
			self.widget.config(text=button_text)
	
	def image(self,button_image_path=None):
		# Без 'file=' не сработает!
		if button_image_path and os.path.exists(button_image_path):
			button_image = tk.PhotoImage(file=button_image_path,master=self.parent_obj.widget,width=self.width,height=self.height)
		else:
			button_image = None
		return button_image
	
	def click(self,*args):
		self.action()
	
	def active(self):
		if not self.Status:
			self.Status = True
			if self.active_image:
				self.widget.config(image=self.active_image)
				self.widget.flag_img = self.active_image
			#self.widget.config(text="I'm Active")
	
	def inactive(self):
		if self.Status:
			self.Status = False
			if self.inactive_image:
				self.widget.config(image=self.inactive_image)
				self.widget.flag_img = self.inactive_image
			#self.widget.config(text="I'm Inactive")
			
	def show(self):
		self.widget.pack(expand=self.expand,side=self.side,fill=self.fill)
	
	def close(self):
		self.widget.pack_forget()
	
def button_test(button):
	if button.Status:
		button.title('I am active')
	else:
		button.title('I am passive')
		


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

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.button.after(self.hint_delay, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)

	def showtip(self):
		if not 'geom_top' in globs or not 'width' in globs['geom_top'] or not 'height' in globs['geom_top']:
			log.append('ToolTipBase.showtip',lev_err,globs['mes'].not_enough_input_data)
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
			Message(func='ToolTipBase.showtip',type=lev_err,message=globs['mes'].unknown_mode % (str(self.hint_direction),'top, bottom'))
		if 'geom_top' in globs and 'width' in globs['geom_top'] and 'height' in globs['geom_top']:
			self.tipwindow = tw = tk.Toplevel(self.button)
			tw.wm_overrideredirect(1)
			# "+%d+%d" is not enough!
			log.append('ToolTipBase.showtip',lev_info,globs['mes'].new_geometry % ('tw',self.hint_width,self.hint_height,x,y))
			tw.wm_geometry("%dx%d+%d+%d" % (self.hint_width,self.hint_height,x, y))
			self.showcontents()

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()



class ToolTip(ToolTipBase):

	def __init__(self,button,text='Sample text',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,button_side='left'):
		if not hint_delay:
			hint_delay = 800 #globs['int']['default_hint_delay']
		if not hint_width:
			hint_width = 280 #globs['int']['default_hint_width']
		if not hint_height:
			hint_height = 40 #globs['int']['default_hint_height']
		if not hint_background:
			hint_background = '#ffffe0' #globs['var']['default_hint_background']
		if not hint_direction:
			hint_direction = 'top' #globs['var']['default_hint_direction']
		if not hint_border_width:
			hint_border_width = 1 #globs['int']['default_hint_border_width']
		if not hint_border_color:
			hint_border_color = 'navy' #globs['var']['default_hint_border_color']
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

	def showcontents(self):
		frame = tk.Frame(self.tipwindow,background=self.hint_border_color,borderwidth=self.hint_border_width)
		frame.pack()
		label = tk.Label(frame,text=self.text,justify='center',background=self.hint_background,width=self.hint_width,height=self.hint_height)
		label.pack() #expand=1,fill='x'
		


class ListBox:
	
	# todo: configure a font
	def __init__(self,parent_obj,Multiple=False,lst=[],title='Title:',icon=None,SelectionCloses=True,SelectFirst=True,Composite=False,SingleClick=True,user_function=None):
		# (1) Initializing variables
		self.parent_obj = parent_obj
		self.scrollbar = tk.Scrollbar(self.parent_obj.widget)
		self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
		self.Multiple = Multiple
		self.SelectFirst = SelectFirst
		self.Composite = Composite
		self.SelectionCloses = SelectionCloses
		self.SingleClick = SingleClick
		# A user-defined function that is run when pressing Up/Down arrow keys and LMB. There is a problem binding it externally, so we bind it here.
		self.user_function = user_function
		self._index = 0
		self.state = 'normal'
		# (2) Creating the widget
		if self.Multiple:
			self.widget = tk.Listbox(self.parent_obj.widget,exportselection=0,selectmode=tk.MULTIPLE)
		else:
			self.widget = tk.Listbox(self.parent_obj.widget,exportselection=0,selectmode=tk.SINGLE)
		self.reset(lst=lst,title=title,icon=icon,SelectFirst=self.SelectFirst)
		self.widget.pack(expand=1,fill='both')
		self._resize()
		self.scrollbar.config(command=self.widget.yview)
		self.widget.config(yscrollcommand=self.scrollbar.set)
		self.widget.focus_set()
		# (3) Setting bindings
		# todo: test <KP_Enter> in Windows
		if self.user_function:
			create_binding(self.widget,'<<ListboxSelect>>',self.user_function) # Binding just to '<Button-1>' does not work. We do not need binding Return/space/etc. because the function will be called each time the selection is changed. However, we still need to bind Up/Down.
		elif self.SelectionCloses:
			create_binding(self.widget,['<Return>','<KP_Enter>','<Double-Button-1>'],self.close)
			if self.SingleClick and not self.Multiple:
				create_binding(self.widget,'<Button-1>',self.close)
		if not self.Composite:
			# Тип родительского виджета может быть любым
			if not hasattr(self.parent_obj,'close_button'):
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
			WidgetShared.custom_buttons(self)
		if not self.Multiple:
			create_binding(self.widget,'<Up>',self.move_up)
			create_binding(self.widget,'<Down>',self.move_down)
		
	def _resize(self):
		# Autofit to contents
		self.widget.config(width=0)
		self.widget.config(height=0)
	
	def activate(self):
		self.widget.activate(self._index)
	
	def clear(self):
		self.widget.delete(0,tk.END)
		
	def clear_selection(self):
		self.widget.selection_clear(0,tk.END)
	
	def reset(self,lst=[],title='Title:',icon=None,SelectFirst=True):
		self.SelectFirst = SelectFirst
		self.clear()
		self.lst = list(lst)
		self.icon(icon=icon)
		self.title(title=title)
		self.fill()
		self._resize()
		self._index = 0
		if self.SelectFirst:
			self.select()
		else:
			self.clear_selection()
		self.IQuit = False
	
	def select(self):
		self.clear_selection()
		self.widget.selection_set(self._index)
		self.widget.see(self._index)
	
	def show(self):
		self.parent_obj.show()

	def close(self,*args):
		self.IQuit = True
		self.parent_obj.close()
	
	def fill(self):
		for i in range(len(self.lst)):
			self.widget.insert(tk.END,self.lst[i])
			
	def title(self,title='Title:'):
		self.parent_obj.title(title=title)
		
	def icon(self,icon):
		WidgetShared.icon(self.parent_obj,icon)
		
	def index(self):
		selection = self.widget.curselection()
		if selection and len(selection) > 0:
			# ATTENTION: selection[0] is a number in Python 3.4, however, in older interpreters and builds based on them it is a string. In order to preserve compatibility, we convert it to a number.
			self._index = int(selection[0])
			return self._index
		else:
			return 0
			
	def index_add(self):
		if self.index() < len(self.lst) - 1:
			self._index += 1
		else:
			self._index = 0
	
	def index_subtract(self):
		if self.index() > 0:
			self._index -= 1
		else:
			self._index = len(self.lst) - 1
	
	def _get(self): # Call this externally to get results *before* closing the widget
		result = [self.widget.get(idx) for idx in self.widget.curselection()]
		if self.Multiple:
			return result
		else:
			if len(result) > 0:
				return result[0]
	
	def get(self):
		if self.SelectionCloses:
			# Return a result if the user has selected anything or None otherwise
			if self.IQuit:
				return self._get()
		else:
			return self._get()
			
	def move_down(self,*args):
		self.index_add()
		self.select()
		if self.user_function:
			self.user_function()
		
	def move_up(self,*args):
		self.index_subtract()
		self.select()
		if self.user_function:
			self.user_function()



def dialog_save_file(filetypes=()):
	file = ''
	if not filetypes:
		filetypes = ((globs['mes'].plain_text,'.txt'),(globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*'))
	options = {}
	options['initialfile'] = ''
	options['filetypes'] = filetypes
	options['title'] = globs['mes'].save_as
	#try:
	file = dialog.asksaveasfilename(**options)
	#except:
	#	Message(func='dialog_save_file',type=lev_err,message=globs['mes'].file_sel_failed)
	return file



class OptionMenu:
	
	def __init__(self,parent_obj,items=(1,2,3,4,5),side='left',anchor='center'):
		self.parent_obj = parent_obj
		self.items = items
		self.choice = None
		self.index = 0
		self.var = tk.StringVar(self.parent_obj.widget)
		self.widget = tk.OptionMenu(self.parent_obj.widget,self.var,*self.items,command=self._get)
		self.widget.pack(side=side,anchor=anchor)
		self.default_set()
		
	def default_set(self):
		if len(self.items) > 0:
			self.var.set(self.items[0])
	
	def fill(self):
		self.widget['menu'].delete(0,'end')
		for item in self.items:
			self.widget['menu'].add_command(label=item,command=lambda v=self.var,l=item:v.set(l))
	
	def reset(self,items=(1,2,3,4,5)):
		self.items = items
		self.fill()
		self.default_set()
		
	def _get(self,*args): # Auto updated (after selecting an item)
		self.choice = self.var.get()
		self.index = self.items.index(self.choice)
		
	def set_prev(self,*args):
		if self.index == 0:
			self.index = len(self.items) - 1
		else:
			self.index -= 1
		self.var.set(self.items[self.index])
		
	def set_next(self,*args):
		if self.index == len(self.items) - 1:
			self.index = 0
		else:
			self.index += 1
		self.var.set(self.items[self.index])


