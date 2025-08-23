#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep

from config import CONFIG
from manager import PLUGINS
from logic import Source

from about.controller import ABOUT

from welcome.gui import Welcome as guiWelcome, TableModel as guiTableModel
from welcome.logic import Welcome as lgWelcome, COLNUM


class Welcome:
    
    def __init__(self):
        self.gui = guiWelcome()
        self.logic = lgWelcome()
        self.logic.desc = ABOUT.get_product()
        self.sources = []
    
    def get_width(self):
        return self.gui.width()
    
    def get_height(self):
        return self.gui.height()
    
    def hide(self):
        self.gui.hide()
    
    def loop_online_sources(self):
        code = []
        for source in self.sources:
            if source.Online:
                desc = self.gen_online_source(title = source.title
                                             ,status = source.status
                                             ,color = source.color)
                code.append(desc)
        code = ', '.join(code) + '.'
        code = self.set_font(code)
        self.logic.table.append([code])
    
    def loop_offline_sources(self):
        code = []
        for source in self.sources:
            if not source.Online:
                desc = self.gen_offline_source(title = source.title
                                              ,status = source.status
                                              ,color = source.color)
                code.append(desc)
        code = _('Offline dictionaries loaded: ') + ', '.join(code) + '.'
        code = self.set_font(code)
        self.logic.table.append([code])
    
    def gen_online_source(self, title, status, color):
        return f'<b>{title} <font color="{color}">{status}</font></b>'
    
    def gen_offline_source(self, title, status, color):
        return f'{title}: <font color="{color}">{status}</font>'
    
    def set_online_sources(self):
        f = '[MClient] welcome.controller.Welcome.set_online_sources'
        if not CONFIG.new['Ping']:
            rep.lazy(f)
            return
        old = PLUGINS.source
        dics = PLUGINS.get_online_sources()
        if not dics:
            rep.empty(f)
            return
        for dic in dics:
            PLUGINS.set(dic)
            isource = Source()
            isource.title = dic
            isource.Online = True
            if PLUGINS.count_valid():
                isource.status = _('running')
                isource.color = 'green'
            self.sources.append(isource)
        PLUGINS.set(old)
    
    def set_offline_sources(self):
        f = '[MClient] welcome.controller.Welcome.set_offline_sources'
        dics = PLUGINS.get_offline_sources()
        if not dics:
            rep.empty(f)
            return
        old = PLUGINS.source
        for dic in dics:
            PLUGINS.set(dic)
            isource = Source()
            isource.title = dic
            dic_num = PLUGINS.count_valid()
            isource.status = dic_num
            if dic_num:
                isource.color = 'green'
            self.sources.append(isource)
        PLUGINS.set(old)
    
    def set_sources(self):
        self.set_online_sources()
        self.set_offline_sources()

    def set_middle(self):
        self.set_sources()
        self.loop_online_sources()
        self.loop_offline_sources()
    
    def run(self):
        self.set_head()
        self.set_middle()
        self.set_tail()
        return self.logic.table
    
    def hide_rows(self, rownos):
        self.gui.hide_rows(rownos)
    
    def show_rows(self, rownos):
        self.gui.show_rows(rownos)
    
    def set_font(self, text):
        return self.logic.set_font(text)
    
    def set_head(self):
        self.logic.set_head()
    
    def set_tail(self):
        self.logic.set_tail()
    
    def set_model(self, model):
        self.gui.set_model(model)
    
    def set_spans(self):
        for i in range(10):
            self.gui.set_span(i, 0, 1, COLNUM)
    
    def set_col_widths(self):
        for i in range(COLNUM):
            self.gui.set_col_width(i, 166)
    
    def resize_rows(self):
        ''' Create the table and fill the model before resizing rows, otherwise
            the latter will not work as expected and can cause segfaults.
            This strange workaround allows to avoid too much space caused by
            spanning rows and resizing them to contents.
            https://stackoverflow.com/questions/52166539/qtablewidget-respect-span-when-sizing-to-contents
        '''
        self.set_col_widths()
        self.set_spans()
        self.hide_rows((0, 1, 2, 3, 4, 5, 6, 7, 8))
        self.gui.resize_rows()
        self.show_rows((0, 1, 2, 3, 4, 5, 6, 7, 8))
    
    def reset(self):
        #self.set_col_widths()
        self.fill()
    
    def fill(self):
        #model = guiTableModel(self.logic.run())
        model = guiTableModel(self.run())
        self.set_model(model)


WELCOME = Welcome()
