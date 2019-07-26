#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')

import random
import shared as sh


class Commands:
    
    def __init__(self):
        pass
    
    def textboxc(self):
        #file  = '/home/pete/base/[unmusic] corrupted tags.txt'
        file  = '/tmp/test.txt'
        text  = sh.lg.ReadTextFile(file).get()
        words = sh.lg.Words (text = text
                            ,Auto = True
                            )
        words.sent_nos()
        itxt = sh.TextBoxC (SpReturn = True
                           ,Maximize = False
                           ,title    = 'TextBoxC with Selection and Search'
                           ,icon     = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
                           ,words    = words
                           )
        itxt.insert(text)
        itxt.spelling()
        itxt.focus()
        itxt.show()
        result = sh.lg.Text(itxt.get()).shorten(max_len=20)
        print('Output: "{}"'.format(result))
    
    def panes(self):
        file   = '/home/pete/base/[unmusic] corrupted tags.txt'
        text   = sh.lg.ReadTextFile(file).get()
        words  = sh.lg.Words (text = text
                             ,Auto = True
                             )
        words.sent_nos()
        ipanes = sh.Panes (bg       = 'old lace'
                          ,Extended = True
                          )
        '''
        ipanes = sh.Panes (bg       = 'old lace'
                          ,Extended = True
                          ,words1   = words
                          ,words2   = words
                          ,words3   = words
                          ,words4   = words
                          )
        '''
        ipanes.reset(words,words,words,words)
        ipanes.show()
    
    def textbox(self):
        file   = '/home/pete/base/[unmusic] corrupted tags.txt'
        text   = sh.lg.ReadTextFile(file).get()
        words  = sh.lg.Words (text = text
                             ,Auto = True
                             )
        words.sent_nos()
        parent = sh.Top()
        parent.title('TextBox with Selection and Search')
        itxt = sh.TextBox (parent  = parent
                          ,expand  = 1
                          ,side    = None
                          ,fill    = 'both'
                          ,words   = words
                          ,font    = 'Serif 14'
                          ,ScrollX = True
                          ,ScrollY = True
                          ,wrap    = 'word'
                          )
        itxt.insert(text)
        itxt.focus()
        parent.show()
        result = sh.lg.Text(itxt.get()).shorten(max_len=20)
        print('Output: "{}"'.format(result))
    
    def entryc(self):
        ient = sh.EntryC (title = 'This is an Entry'
                         ,icon  = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
                         )
        ient.show()
        print('Output: "{}"'.format(ient.get()))
    
    def entry(self):
        parent = sh.Top()
        ient = sh.Entry (parent  = parent
                        ,side    = 'left'
                        ,ipadx   = 5
                        ,ipady   = 5
                        ,fill    = 'x'
                        ,width   = 10
                        ,expand  = None
                        ,font    = 'Sans 11'
                        ,bg      = 'blue'
                        ,fg      = 'red'
                        ,justify = 'right'
                        )
        ient.focus()
        ient.insert('Anything')
        ient.disable()
        parent.show()
    
    def multcboxesc(self):
        text = '\n'.join([str(i+1) for i in range(100)])
        imult = sh.MultCBoxesC (text    = text
                               ,width   = 550
                               ,height  = 400
                               ,font    = 'Sans 11'
                               ,MarkAll = False
                               ,icon    = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
                               )
        imult.show()
        print(imult.selected())
    
    def multcboxes(self):
        parent = sh.Top()
        imult = sh.MultCBoxes (parent  = parent
                              ,text    = 'Hello\nBye\nHello again'
                              ,font    = 'Sans 11'
                              ,MarkAll = False
                              )
        parent.show()
    
    def trigger_cbox(self,event=None):
        print('Output: "{}"'.format(self.cbx.get()))
    
    def checkbox(self):
        parent = sh.Top()
        sh.Geometry(parent).set('100x100')
        parent.title('CheckBox')
        self.cbx = sh.CheckBox (parent = parent
                               ,Active = False
                               ,side   = 'left'
                               ,action = self.trigger_cbox
                               )
        self.lbl = sh.Label (parent = parent
                            ,text   = 'Label'
                            ,side   = 'left'
                            )
        sh.com.bind (obj      = self.lbl
                    ,bindings = '<ButtonRelease-1>'
                    ,action   = self.trigger_cbox
                    )
        parent.show()
    
    def progressbar(self):
        top   = sh.Top(AutoCr=False)
        iprog = sh.ProgressBar (width   = 750
                               ,height  = 200
                               ,YScroll = True
                               ,title   = 'Load dictionaries'
                               ,icon    = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
                               )
        for i in range(10):
            iprog.add()
        iprog.show()
        top.show()
    
    def progressbaritem(self):
        parent = sh.Top()
        iprog  = sh.ProgressBarItem (parent = parent
                                    ,orient = 'horizontal'
                                    ,length = 100
                                    ,mode   = 'determinate'
                                    )
        parent.show()
    
    def canvas(self):
        parent = sh.Top()
        parent.title('Canvas')
        icanvas = sh.Canvas (parent = parent
                            ,expand = True
                            ,side   = None
                            ,region = None
                            ,width  = None
                            ,height = None
                            ,fill   = 'both'
                            )
        sh.Geometry(parent=parent).set('1024x768')
        frame  = sh.Frame (parent = parent)
        # This frame must be created after the bottom frame
        frame1 = sh.Frame (parent = frame)
        canvas = sh.Canvas(parent = frame1)

        label  = sh.Label (parent = frame1
                          ,expand = True
                          ,fill   = 'both'
                          ,text   = 'Hello, Canvas!'
                          ,fg     = 'white'
                          ,bg     = 'blue'
                          )

        icanvas.embed(frame)
        icanvas.focus()
        icanvas.top_bindings(top=parent)
        parent.show()
    
    def clipboard(self):
        iclip = sh.Clipboard(Silent=True)
        #iclip.copy('Hello, this is очень классный лент!')
        print('Output: "{}"'.format(iclip.paste()))
    
    def symbol_map(self):
        imap = sh.SymbolMap (items = 'àáâäāãæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңәөүұÀÁÂÄĀÃÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӘӨҮҰ'
                            ,title = ''
                            ,icon  = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
                            )
        imap.show()
        print('Your input: "{}"'.format(imap.get()))
    
    def optionmenu_trigger(self,event=None):
        print('Your input: "{}"'.format(self.opt_prm.choice))
    
    def optionmenu(self):
        f = '[shared] tests.Commands.optionmenu'
        parent = sh.Top()
        sh.Geometry(parent).set('300x40')
        parent.title('OptionMenu')
        self.opt_prm = sh.OptionMenu (parent  = parent
                                     ,items   = None
                                     ,side    = 'left'
                                     ,anchor  = 'center'
                                     ,action  = self.optionmenu_trigger
                                     ,tfocus  = 1
                                     ,default = None
                                     ,Combo   = True
                                     ,expand  = False
                                     ,fill    = None
                                     ,font    = 'Sans 11'
                                     )
        parent.show()
        parent.title(_('New settings'))
        self.opt_prm.reset (items   = (33,34,345,345)
                           ,default = 345
                           ,action  = self.optionmenu_trigger
                           )
        parent.show()
    
    def listboxc(self):
        f = '[shared] tests.Commands.listboxc'
        lst = [i for i in range(15)]
        self.lbx_prm = sh.ListBoxC (Multiple = False
                                   ,lst      = lst
                                   ,action   = None
                                   ,side     = None
                                   ,expand   = True
                                   ,fill     = 'both'
                                   ,title    = 'ListBox (All)'
                                   ,icon     = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
                                   ,SelQuits = True
                                   ,ScrollX  = True
                                   ,ScrollY  = True
                                   )
        self.lbx_prm.show()
        print('Your final selection: "{}"'.format(self.lbx_prm.get()))
        self.lbx_prm.reset (lst   = (_('Mexico'),_('Canada'),_('Russia'))
                           ,title = _('New settings')
                           ,icon  = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
                           )
        self.lbx_prm.show()
        print('Your final selection: "{}"'.format(self.lbx_prm.get()))
    
    def lbx_trigger(self,event=None):
        text = self.lbx_prm.get()
        print('Your input: "{}"'.format(text))
    
    def listbox(self):
        f = '[shared] tests.Commands.listbox'
        parent = sh.Top()
        parent.title('ListBox')
        lst = [i for i in range(15)]
        self.lbx_prm = sh.ListBox (parent   = parent
                                  ,Multiple = False
                                  ,lst      = lst
                                  ,action   = self.lbx_trigger
                                  ,side     = None
                                  ,expand   = True
                                  ,fill     = 'both'
                                  )
        self.lbx_prm.focus()
        parent.show()
    
    def scrollbar(self):
        f = '[shared] tests.Commands.scrollbar'
        text = '\n'.join([('('+str(i)+')'+f+' ')*(i+1) for i in range(100)])
        parent = sh.Top()
        parent.title('Y Scrollbar')
        ''' #note: when the widget width is <580, the scrollbar will not
            be visible.
        '''
        sh.Geometry(parent).set('600x400')
        
        frm_prm = sh.Frame (parent = parent
                           ,side   = 'left'
                           )
        frm_ver = sh.Frame (parent = parent
                           ,side   = 'right'
                           ,expand = False
                           ,fill   = 'y'
                           )
        frm_txt = sh.Frame (parent = frm_prm
                           ,side   = 'top'
                           )
        frm_hor = sh.Frame (parent = frm_prm
                           ,side   = 'bottom'
                           ,expand = False
                           ,fill   = 'x'
                           )
        
        #todo: use 'TextBox'
        import tkinter as tk
        widget = tk.Text(frm_txt.widget,wrap='none')
        widget.pack(expand=True,fill='both')
        widget.insert('1.0',text)
        txt = sh.gi.WidgetObject(widget)
        txt.widget.focus_set()
        
        sh.Scrollbar (parent = frm_hor
                     ,scroll = txt
                     ,Horiz  = True
                     )
        sh.Scrollbar (parent = frm_ver
                     ,scroll = txt
                     ,Horiz  = False
                     )
        parent.show()
    
    def waitbox(self):
        f = '[shared] tests.Commands.waitbox'
        import time
        icon1 = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
        icon2 = '/home/pete/bin/Yatube/resources/icon_64x64_yatube.gif'
        sh.objs.waitbox().icon(icon1)
        sh.objs.waitbox()
        sh.objs._waitbox.reset (func    = f
                               ,message = None
                               )
        sh.objs._waitbox.show()
        time.sleep(3)
        sh.objs._waitbox.close()
        
        sh.objs._waitbox.icon(icon2)
        sh.objs._waitbox.reset (func    = f
                               ,message = 'Hello! I\'m still here!'
                               )
        sh.objs._waitbox.show()
        time.sleep(3)
        sh.objs._waitbox.close()
    
    def button_trigger(self,event=None):
        f = '[shared] tests.Commands.button_trigger'
        ''' #todo: this works partially: silent messages do not pass
            here, label colors are changed when the mouse pointer is not
            over them (when using mouse).
        '''
        mes = _('The event has been triggered!')
        sh.Message(f,mes,True)
        if self.btn_img.Status:
            self.btn_trg.widget.config (bg = 'green'
                                       ,fg = 'black'
                                       )
            self.btn_img.inactive()
        else:
            self.btn_trg.widget.config (bg = 'yellow'
                                       ,fg = 'red'
                                       )
            self.btn_img.active()
    
    def button(self):
        parent  = sh.Top()
        parent.title(_('Button'))
        self.btn_trg = sh.Button (parent      = parent
                                 ,side        = 'top'
                                 ,action      = self.button_trigger
                                 ,text        = _('Trigger an event')
                                 ,font        = 'Sans 14 bold'
                                 )
        self.btn_img = sh.Button (parent      = parent
                                 ,action      = None
                                 ,hint        = 'This is a hint'
                                 ,inactive    = '/home/pete/bin/mclient/resources/buttons/icon_36x36_watch_clipboard_off.gif'
                                 ,active      = '/home/pete/bin/mclient/resources/buttons/icon_36x36_watch_clipboard_on.gif'
                                 ,text        = 'Press me'
                                 ,height      = 36
                                 ,width       = 36
                                 ,side        = 'top'
                                 ,expand      = 0
                                 ,bg          = None
                                 ,bg_focus    = None
                                 ,fg          = None
                                 ,fg_focus    = None
                                 ,bd          = 0
                                 ,hint_delay  = 800
                                 ,hint_bg     = '#ffffe0'
                                 ,hint_dir    = 'top'
                                 ,hint_bwidth = 1
                                 ,hint_bcolor = 'navy'
                                 ,bindings    = []
                                 ,fill        = 'both'
                                 ,TakeFocus   = True
                                 ,font        = None
                                 )
        parent.show()
    
    def frame(self):
        iframe = sh.Frame (parent = sh.Top()
                          ,expand = 1
                          ,fill   = 'both'
                          ,side   = None
                          ,padx   = 10
                          ,pady   = 10
                          ,ipadx  = None
                          ,ipady  = None
                          ,bd     = 2
                          ,bg     = 'blue'
                          ,width  = 200
                          ,height = 200
                          ,propag = False
                          )
        iframe.title('Frame')
        sh.Label (parent = iframe
                 ,text   = 'Label'
                 ,bg     = 'red'
                 ,fg     = 'orange'
                 )
        iframe.show()
    
    def random_coor(self,w,h):
        f = '[shared] tests.Commands.random_coor'
        x = 0
        y = 0
        max_x, max_y = sh.objs.root().resolution()
        x = random.randint(0,max_x)
        y = random.randint(0,max_y)
        mes = _('Screen resolution: {}x{}').format(max_x,max_y)
        sh.Message(f,mes,True).debug()
        if w + x > max_x:
            x = max_x - w
        if h + y > max_y:
            y = max_y - h
        mes = _('Random coordinates: x: {}; y: {}').format(x,y)
        sh.Message(f,mes,True).debug()
        return(x,y)
    
    def size_range(self,event=None):
        v1 = 0
        v2 = 0
        while abs(v1-v2) <= 40:
            v1 = random.randint(90,250)
            v2 = random.randint(90,250)
        return(v1,v2)
    
    def frameless(self):
        top  = sh.Top()
        top1 = sh.Top (AutoCr = False
                      ,Lock   = False
                      )
        top2 = sh.Top (AutoCr = False
                      ,Lock   = False
                      )
        top.title('Host')
        sh.Geometry(top).set('150x150')
        
        top1.widget.wm_overrideredirect(1)
        top2.widget.wm_overrideredirect(1)
        
        sh.Label (parent = top
                 ,text   = 'HOST'
                 ,bg     = 'black'
                 ,fg     = 'red'
                 ,expand = True
                 ,fill   = 'both'
                 )
        sh.Label (parent = top1
                 ,text   = 'TOP1'
                 ,bg     = 'green'
                 ,fg     = 'orange'
                 ,expand = True
                 ,fill   = 'both'
                 )
        sh.Label (parent = top2
                 ,text   = 'TOP2'
                 ,bg     = 'red'
                 ,fg     = 'orange'
                 ,expand = True
                 ,fill   = 'both'
                 )
        
        w1, w2 = com.size_range()
        h1, h2 = com.size_range()
        
        x1, y1 = com.random_coor(h1,w1)
        x2, y2 = com.random_coor(h2,w2)
        
        geom = sh.Geometry(parent=top1)
        geom._geom = '%dx%d+%d+%d' % (w1,h1,x1,y1)
        geom.restore()
        
        geom = sh.Geometry(parent=top2)
        geom._geom = '%dx%d+%d+%d' % (w2,h2,x2,y2)
        geom.restore()
        
        top1.show()
        top2.show()
        top.show()
    
    def label(self):
        lbl = sh.Label (parent  = sh.Top()
                       ,text    = 'Hello! It\'s me again'
                       ,font    = 'Sans 14'
                       ,side    = 'right'
                       ,fill    = 'both'
                       ,expand  = False
                       ,ipadx   = 30
                       ,ipady   = 10
                       ,image   = None
                       ,fg      = 'orange'
                       ,bg      = 'green'
                       ,anchor  = None
                       ,width   = None
                       ,height  = None
                       ,justify = 'left'
                       )
        lbl.title('Label test')
        lbl.show()
    
    def simple_top(self):
        icon_path = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
        itop = sh.Top(Lock=False)
        itop.title('Welcome to shared')
        itop.icon(icon_path)
        itop.show()
        itop.center()
        import time
        time.sleep(2)
    
    def geometry(self):
        import time
        parent = sh.Top(Lock=False)
        igeo = sh.Geometry(parent)
        igeo.set('340x250')
        parent.idle()
        time.sleep(3)
        igeo.minimize()
        parent.idle()
        time.sleep(3)
        igeo.focus()
        igeo.foreground()
        igeo.lift()
        igeo.activate()
        igeo.restore()
        igeo.maximize()
        igeo.update()
        print('Window handle:',igeo.hwnd())
        igeo.save()
        parent.show()
    
    def top(self):
        icon_path = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
        itop = sh.Top (Maximize = False
                      ,AutoCr   = True
                      ,Lock     = True
                      ,ForceCr  = False
                      )
        itop.title('Welcome to shared')
        itop.icon(icon_path)
        itop.show()
    
    def messages(self):
        func    = '[shared] tests.Commands.messages'
        # debug
        message = 'This is a GUI DEBUG message'
        sh.Message (func    = func
                   ,message = message
                   ).debug()
        # info
        message = 'This is a GUI INFO message'
        sh.Message (func    = func
                   ,message = message
                   ).info()
        # question
        message = 'This is a GUI QUESTION message'
        answer = sh.Message (func    = func
                            ,message = message
                            ).question()
        if answer:
            print('You answered Yes')
        else:
            print('You answered No')
        # warning
        message = 'This is a GUI WARNING message'
        sh.Message (func    = func
                   ,message = message
                   ).warning()
        # error
        message = 'This is a GUI ERROR message'
        sh.Message (func    = func
                   ,message = message
                   ).error()
        # debug, silent
        message = 'This is a CLI DEBUG message'
        sh.Message (func    = func
                   ,message = message
                   ,Silent  = True
                   ).debug()
        # info, silent
        message = 'This is a CLI INFO message'
        sh.Message (func    = func
                   ,message = message
                   ,Silent  = True
                   ).info()
        # question, silent
        message = 'This is a CLI QUESTION message'
        answer = sh.Message (func    = func
                            ,message = message
                            ,Silent  = True
                            ).question()
        if answer:
            print('You answered Yes')
        else:
            print('You answered No')
        # warning, silent
        message = 'This is a CLI WARNING message'
        sh.Message (func    = func
                   ,message = message
                   ,Silent  = True
                   ).warning()
        # error, silent
        message = 'This is a CLI ERROR message'
        sh.Message (func    = func
                   ,message = message
                   ,Silent  = True
                   ).error()
    
    def font(self):
        ifont = sh.Font('Serif 11')
        ifont.set_text('Hello, I am here and here!')
        ifont.gui.font('Sans',11)
        width  = ifont.width()
        height = ifont.height()
        print('Font size: {}x{}'.format(width,height))
    
    def free_space(self):
        print('Test #1')
        print('Empty input. 0B is expected')
        path = None
        size = sh.Path(path).free_space()
        print(sh.com.human_size(size))
        print('Test #2')
        print('/. LargeOnly=1. 8,3G is expected')
        path = '/'
        size = sh.Path(path).free_space()
        print(sh.com.human_size(size,LargeOnly=1))
        print('Test #3')
        print('/home/pete/tmp/. 32G is expected')
        path = '/home/pete/tmp/'
        size = sh.Path(path).free_space()
        print(sh.com.human_size(size))
    
    def size(self):
        print('Test #1')
        my_dir = '/home/pete/base/Изображения'
        print('Object: directory; expected result: 975M')
        size = sh.Directory(my_dir).size(Follow=1)
        print(sh.com.human_size(size,LargeOnly=0))
        print('Test #2')
        my_dir = '/home/pete/base/docs'
        print('Object: directory; expected result: 8,7G')
        size = sh.Directory(my_dir).size(Follow=1)
        print(sh.com.human_size(size,LargeOnly=0))
        print('Test #3')
        file = '/boot/initrd.img-4.9.0-9-686'
        print('Object: file; expected result: 21M')
        size = sh.File(file).size()
        print(sh.com.human_size(size,LargeOnly=0))
        print('Test #4')
        file = '/home/pete/main/dist/manjaro-xfce-15.12-i686.iso'
        print('Object: file; LargeOnly=1; expected result: 1,3G')
        size = sh.File(file).size()
        print(sh.com.human_size(size,LargeOnly=1))
        print('Test #5')
        file = '/home/pete/bin/examples/gettext_windows.py'
        print('Object: file; Follow=0; expected result: 0')
        size = sh.File(file).size(Follow=0)
        print(sh.com.human_size(size,LargeOnly=1))

    def progressbar0(self):
        pb = sh.ProgressBar()
        for i in range(100):
            item     = pb.add()
            file     = 'File #%d' % i
            total    = random.randint(1,100)
            cur_size = random.randint(0,total)
            rate     = random.randint(1,5000)
            eta      = int((total*1000)/rate)
            item.text (file     = file
                      ,cur_size = cur_size
                      ,total    = total
                      ,rate     = rate
                      ,eta      = eta
                      )
        pb.show()



class Anchors:
    
    def __init__(self):
        self.count   = 0
        self.anchors = ('N' ,'NE','NW','E' 
                       ,'EN','ES','S' ,'SE'
                       ,'SW','W','WN','WS'
                       )
        self.anchor = self.anchors[0]
    
    def adjust(self,event=None):
        if self.count % 2:
            self.next_anchor()
            self.attach()
            mes = _('Press Return to place widgets randomly')
            self.lbl_top.text(mes)
        else:
            self.place_widgets()
            mes = _('Anchor: {}\nPress Return to adjust Widget 2').format(self.anchor)
            self.lbl_top.text(mes)
        self.count += 1
    
    def next_anchor(self):
        ind = self.anchors.index(self.anchor)
        if ind + 1 == len(self.anchors):
            self.anchor = self.anchors[0]
        else:
            self.anchor = self.anchors[ind+1]
    
    def run(self,event=None):
        f = '[shared] tests.Anchors.run'

        self.top  = sh.Top()
        self.top1 = sh.Top (AutoCr = False
                           ,Lock   = False
                           )
        self.top2 = sh.Top (AutoCr = False
                           ,Lock   = False
                           )
        self.top.title('HOST')
        sh.Geometry(self.top).set('550x150')
        
        # Strict order: 'wm_overrideredirect' -> 'show' -> 'center'
        self.top1.widget.wm_overrideredirect(1)
        self.top2.widget.wm_overrideredirect(1)
        
        mes = _('Press Return to place widgets randomly')
        self.lbl_top = sh.Label (parent = self.top
                                ,text   = mes
                                ,expand = True
                                ,fill   = 'both'
                                )
        sh.Label (parent = self.top1
                 ,text   = 'WIDGET1'
                 ,bg     = 'green'
                 ,fg     = 'orange'
                 ,expand = True
                 ,fill   = 'both'
                 )
        sh.Label (parent = self.top2
                 ,text   = 'WIDGET2'
                 ,bg     = 'red'
                 ,fg     = 'orange'
                 ,expand = True
                 ,fill   = 'both'
                 )
        
        self.place_widgets()
        
        mes = _('Anchor: {}').format(self.anchor)
        sh.Message(f,mes,True).info()
        
        sh.com.bind (obj      = self.top
                    ,bindings = '<Return>'
                    ,action   = self.adjust
                    )
        sh.com.bind (obj      = self.top1
                    ,bindings = '<Return>'
                    ,action   = self.adjust
                    )
        sh.com.bind (obj      = self.top2
                    ,bindings = '<Return>'
                    ,action   = self.adjust
                    )
        
        self.top1.show()
        self.top2.show()
        self.top.show()
    
    def place_widgets(self,event=None):
        w1, w2 = com.size_range()
        h1, h2 = com.size_range()
        
        x1, y1 = com.random_coor(h1,w1)
        x2, y2 = com.random_coor(h2,w2)
        
        geom = sh.Geometry(parent=self.top1)
        geom._geom = '%dx%d+%d+%d' % (w1,h1,x1,y1)
        geom.restore()
        
        geom = sh.Geometry(parent=self.top2)
        geom._geom = '%dx%d+%d+%d' % (w2,h2,x2,y2)
        geom.restore()
    
    def attach(self,event=None):
        sh.AttachWidget (obj1   = self.top1
                        ,obj2   = self.top2
                        ,anchor = self.anchor
                        ).run()


com = Commands()


if __name__ == '__main__':
    f = '[shared] tests.__main__'
    sh.com.start()
    #com.textboxc()
    com.progressbar()
    sh.com.end()
