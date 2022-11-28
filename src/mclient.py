#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import sqlite3

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import logic as lg
import gui as gi

import cells as cl
import subjects.priorities.controller as pr
import subjects.blacklist.controller as bl
import subjects.subjects as sj
import settings.controller as st
import suggest.controller as sg


DEBUG = False


class Table:

    def __init__(self):
        self.set_values()
        self.logic = lg.Table()
        self.gui = gi.Table()
        self.search = SearchArticle()
        self.set_gui()
    
    def insert_repeat_sign(self):
        pass
    
    def insert_repeat_sign2(self):
        pass
    
    def close_search_next(self):
        self.search.close()
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno,colno)
    
    def reset_search(self):
        rowno, colno = self.get_cell()
        self.search.reset(self.logic.cells,self.logic.plain,rowno,colno)
    
    def search_next(self):
        self.reset_search()
        rowno, colno = self.search.search_next()
        self.select(rowno,colno)
    
    def search_prev(self):
        self.reset_search()
        rowno, colno = self.search.search_prev()
        self.select(rowno,colno)
    
    def set_values(self):
        self.coords = {}
        self.row_height = 42
    
    def go_url(self):
        #TODO: implement
        f = '[MClientQt] mclient.Table.go_url'
        print(f)
    
    def go_end(self):
        rowno, colno = self.logic.get_end()
        self.select(rowno,colno)
    
    def go_start(self):
        rowno, colno = self.logic.get_start()
        self.select(rowno,colno)
    
    def go_down(self):
        ''' #NOTE: This should run only after the event since Qt returns dummy
            geometry values right after startup.
        '''
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_row(rowno,colno)
        self.select(rowno,colno)
        self.scroll_top()
    
    def select(self,rowno,colno,Mouse=False):
        if Mouse and self.search.Shown:
            return
        self.model.update(self.gui.get_index())
        new_index = self.model.index(rowno,colno)
        if Mouse:
            self.gui.set_index(new_index)
        else:
            self.gui.set_cur_index(new_index)
        self.model.update(new_index)
    
    def go_up(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_row(rowno,colno)
        self.select(rowno,colno)
    
    def go_line_start(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_start(rowno)
        self.select(rowno,colno)
    
    def go_line_end(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_line_end(rowno)
        self.select(rowno,colno)
    
    def go_left(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_prev_col(rowno,colno)
        self.select(rowno,colno)
    
    def go_right(self):
        rowno, colno = self.get_cell()
        rowno, colno = self.logic.get_next_col(rowno,colno)
        self.select(rowno,colno)
    
    def scroll_top(self):
        f = '[MClientQt] mclient.Table.scroll_top'
        if not self.coords:
            sh.com.rep_empty(f)
            return
        rowno, colno = self.gui.get_cell()
        index_ = self.model.index(self.coords[rowno],colno)
        self.gui.scroll2index(index_)
    
    def get_cell(self):
        f = '[MClientQt] mclient.Table.get_cell'
        try:
            return self.gui.get_cell()
        except Exception as e:
            sh.com.rep_third_party(f,e)
            return(0,0)
    
    def copy_cell(self):
        f = '[MClientQt] mclient.Table.copy_cell'
        rowno, colno = self.gui.get_cell()
        mes = '"' + self.logic.plain[rowno][colno] + '"'
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def clear(self):
        self.gui.clear()
    
    def set_row_height(self,height=42):
        for no in range(self.logic.rownum):
            self.gui.set_row_height(no,height)
    
    def set_col_width(self):
        # For some reason, this works only after filling cells
        f = '[MClientQt] mclient.Table.set_col_width'
        mes = _('Number of columns: {}').format(self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        #TODO: Rework, number of fixed columns can be different
        for no in range(self.logic.colnum):
            if no == 0:
                width = 140
            elif no == 1:
                width = sh.lg.globs['int']['fixed_col_width']
            elif no in (2,3):
                width = 63
            else:
                width = sh.lg.globs['int']['term_col_width']
            self.gui.set_col_width(no,width)
    
    def reset(self,cells):
        f = '[MClientQt] mclient.Table.reset'
        if not cells:
            sh.com.rep_empty(f)
            return
        self.clear()
        self.logic.reset(cells)
        self.model = gi.TableModel(self.logic.table)
        self.fill()
        self.set_col_width()
        self.set_row_height(self.row_height)
        self.show_borders(False)
        #self.set_long()
        self.go_start()
    
    def set_long(self):
        ''' This is slow ('set' on Intel Atom without debugging: ~2.68s with
            default sizeHint and ~5.57s with custom sizeHint.
        '''
        f = '[MClient] mclient.Table.set_long'
        timer = sh.Timer(f)
        timer.start()
        self.gui.delegate.long = []
        for rowno in range(self.logic.rownum):
            for colno in range(self.logic.colnum):
                index_ = self.model.index(rowno,colno)
                height = self.gui.get_cell_hint(index_)
                #mes = 'Row #{}. Column #{}. Size hint: {}'
                #mes = mes.format(rowno,colno,height)
                #sh.objs.get_mes(f,mes,True).show_debug()
                #if height > self.row_height:
                if height > 380:
                    self.gui.delegate.long.append(index_)
        timer.end()
        mes = _('Number of cells: {}').format(self.logic.rownum*self.logic.colnum)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Number of long cells: {}').format(len(self.gui.delegate.long))
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def set_coords(self,event=None):
        f = '[MClientQt] mclient.Table.set_coords'
        ''' Calculating Y is very fast (~0.05s for 'set' on Intel Atom). We
            need None since this procedure overrides
            self.gui.parent.resizeEvent.
        '''
        height = self.gui.get_height()
        mes = _('Window height: {}').format(height)
        sh.objs.get_mes(f,mes,True).show_debug()
        for rowno in range(self.logic.rownum):
            y = self.gui.get_cell_y(rowno) + self.gui.get_row_height(rowno)
            pageno = int(y / height)
            page_y = pageno * height
            page_rowno = self.gui.get_row_by_y(page_y)
            self.coords[rowno] = page_rowno
    
    def fill(self):
        f = '[MClientQt] mclient.Table.fill'
        timer = sh.Timer(f)
        timer.start()
        self.gui.set_model(self.model)
        timer.end()
    
    def set_max_row_height(self,height=150):
        self.gui.set_max_row_height(height)
    
    def set_max_col_width(self):
        constraints = []
        for cell in self.logic.cells:
            #TODO: elaborate
            if cell.no < 5:
                value = 63
            else:
                value = 221
            constraints.append(self.gui.get_constraint(value))
        self.gui.set_max_col_width(constraints)
    
    def show_borders(self,Show=False):
        self.gui.show_borders(Show)
    
    def set_gui(self):
        self.gui.clicked.connect(self.go_url)
        self.gui.click_right = self.copy_cell
        self.gui.select = self.select
        self.search.gui.ent_src.bind('Return',self.close_search_next)
        self.search.gui.btn_srp.action = self.search_prev
        self.search.gui.btn_srn.action = self.search_next
        self.search.gui.btn_srp.set_action()
        self.search.gui.btn_srn.set_action()
        #self.set_max_row_height()



class DB:
    
    def __init__(self):
        self.set_values()
        self.db = sqlite3.connect(self.path)
        self.dbc = self.db.cursor()
    
    def set_values(self):
        self.artid = 0
        self.Selectable = True
        self.path = '/home/pete/tmp/set.db'
    
    def fetch(self):
        query = 'select NO,ROWNO,COLNO,TEXT,COLOR,FAMILY,SIZE,BOLD,ITALIC \
                 from FONTS order by NO'
        self.dbc.execute(query,)
        return self.dbc.fetchall()
    
    def close(self):
        f = '[MClient] mclient.DB.close'
        mes = _('Close "{}"').format(self.path)
        #sh.objs.get_mes(f,mes,True).show_info()
        print(mes)
        self.dbc.close()
    
    def get_max_col_no(self):
        ''' This is a less advanced alternative to 'self.get_max_col'
            for cases when positions are not set yet.
        '''
        f = '[MClient] mclient.DB.get_max_col_no'
        query = 'select COLNO from FONTS order by COLNO desc'
        self.dbc.execute(query,)
        col_no = self.dbc.fetchone()
        if col_no:
            return col_no[0]
    
    def get_max_row_no(self):
        f = '[MClient] mclient.DB.get_max_row_no'
        query = 'select ROWNO from FONTS order by ROWNO desc'
        self.dbc.execute(query,)
        result = self.dbc.fetchone()
        if result:
            return result[0]



class App:
    
    def __init__(self):
        self.gui = gi.App()
        self.set_gui()
        self.update_ui()
    
    def load_article(self):
        f = '[MClientQt] mclient.App.load_article'
        ''' #NOTE: each time the contents of the current page is changed
            (e.g., due to prioritizing), bookmarks must be deleted.
        '''
        # Suppress useless error output
        if not lg.objs.get_request().search:
            return
        timer = sh.Timer(f)
        #timer.start()
        # Do not allow selection positions from previous articles
        self.pos = -1
        '''
        order = objs.get_settings().get_speech_prior()
        lg.objs.get_speech_prior().reset(order)
        '''
        artid = lg.objs.get_blocksdb().is_present (source = sh.lg.globs['str']['source']
                                                  ,title = lg.objs.request.search
                                                  ,url = lg.objs.request.url
                                                  )
        if artid:
            mes = _('Load article No. {} from memory').format(artid)
            sh.objs.get_mes(f,mes,True).show_info()
            lg.objs.blocksdb.artid = artid
            #self.get_bookmark()
        else:
            blocks = lg.objs.get_plugins().request (search = lg.objs.request.search
                                                   ,url = lg.objs.request.url
                                                   )
            # 'None' skips the autoincrement
            data = (None                              # (00) ARTICLEID
                   ,sh.lg.globs['str']['source']      # (01) SOURCE
                   ,lg.objs.request.search            # (02) TITLE
                   ,lg.objs.request.url               # (03) URL
                   ,lg.objs.get_plugins().get_lang1() # (04) LANG1
                   ,lg.objs.plugins.get_lang2()       # (05) LANG2
                   ,self.pos                          # (06) BOOKMARK
                   ,lg.objs.plugins.get_htm()         # (07) CODE
                   )
            lg.objs.blocksdb.fill_articles(data)
            lg.objs.blocksdb.artid = lg.objs.blocksdb.get_max_artid()
            data = lg.com.dump_elems (blocks = blocks
                                     ,artid = lg.objs.blocksdb.artid
                                     )
            if data:
                lg.objs.blocksdb.fill_blocks(data)
            
            lg.objs.blocksdb.update_phterm()
            
        timer.start()
        self.phdic = lg.objs.blocksdb.get_phdic()
        if self.phdic:
            if sh.lg.globs['bool']['ShortSubjects']:
                self.phdic = self.phdic[0]
            else:
                self.phdic = self.phdic[1]
        else:
            self.phdic = ''
        
        old_special = lg.objs.request.SpecialPage
        if self.phdic:
            lg.objs.request.SpecialPage = False
        else:
            # Otherwise, 'SpecialPage' will be inherited
            lg.objs.request.SpecialPage = True
        lg.objs.request.NewPageType = old_special != lg.objs.request.SpecialPage
        #self.update_columns()
        
        SortTerms = sh.lg.globs['bool']['AlphabetizeTerms'] \
                    and not lg.objs.request.SpecialPage
        ''' We must reset DB as early as possible after setting 'elems',
            otherwise, real and loaded settings may not coincide, which,
            in turn, may lead to a data loss, see, for example, RU-EN:
            "цепь: провод".
        '''
        lg.objs.blocksdb.reset (cols = lg.objs.request.cols
                               ,SortRows = sh.lg.globs['bool']['SortByColumns']
                               ,SortTerms = SortTerms
                               ,ExpandDic = not sh.lg.globs['bool']['ShortSubjects']
                               ,ShowUsers = sh.lg.globs['bool']['ShowUserNames']
                               ,PhraseCount = sh.lg.globs['bool']['PhraseCount']
                               )
        sj.objs.get_article().reset (pairs = lg.objs.blocksdb.get_dic_pairs()
                                    ,Debug = lg.objs.get_plugins().Debug
                                    )
        sj.objs.article.run()
        data = lg.objs.blocksdb.assign_bp()
        spdic = lg.objs.get_speech_prior().get_all2prior()
        bp = cl.BlockPrioritize (data = data
                                ,Block = sh.lg.globs['bool']['BlockSubjects']
                                ,Prioritize = sh.lg.globs['bool']['PrioritizeSubjects']
                                ,phdic = self.phdic
                                ,spdic = spdic
                                ,Debug = lg.objs.plugins.Debug
                                ,maxrows = lg.objs.plugins.maxrows
                                )
        bp.run()
        lg.objs.blocksdb.update(bp.query)
        
        lg.objs.blocksdb.unignore()
        lg.objs.blocksdb.ignore()
        
        data = lg.objs.blocksdb.assign_cells()

        if sh.lg.globs['bool']['ShortSpeech']:
            spdic = {}
        else:
            spdic = lg.objs.speech_prior.get_abbr2full()
        
        cells = cl.Cells (data = data
                         ,cols = lg.objs.request.cols
                         ,collimit = lg.objs.request.collimit
                         ,phdic = self.phdic
                         ,spdic = spdic
                         ,Reverse = sh.lg.globs['bool']['VerticalView']
                         ,Debug = lg.objs.plugins.Debug
                         ,maxrows = lg.objs.plugins.maxrows
                         )
        cells.run()
        cells.dump(lg.objs.blocksdb)
        
        lg.objs.get_column_width().reset()
        lg.objs.column_width.run()
        
        blocks = lg.com.assign_blocks(lg.objs.blocksdb.fetch())
        
        blocks = lg.com.add_formatting(blocks)
        
        ''' Empty article is not added either to DB or history, so we
            just do not clear the search field to be able to correct
            the typo.
        '''
        '''
        if pages.blocks or com.get_skipped_terms():
            self.gui.ent_src.clear_text()
        '''
        #objs.get_suggest().close()
        #self.update_buttons()
        timer.end()
        #self.run_final_debug()
        #self.debug_settings()
        return blocks
    
    def toggle_about(self):
        self.about.toggle()
    
    def go_keyboard(self):
        #f = '[MClientQt] mclient.Table.go_keyboard'
        search = self.panel.ent_src.get().strip()
        if search == '':
            self.table.go_url()
        elif search == sh.lg.globs['str']['repeat_sign']:
            self.insert_repeat_sign()
        elif search == sh.lg.globs['str']['repeat_sign2']:
            self.insert_repeat_sign2()
        else:
            lg.objs.get_request().search = search
            self.go_search()
    
    def go_search(self):
        if lg.objs.get_request().search is None:
            lg.objs.request.search = ''
        lg.objs.request.search = lg.objs.request.search.strip()
        if lg.com.control_length():
            '''
            self.update_lang1()
            self.update_lang2()
            self.auto_swap()
            '''
            lg.com.get_url()
            mes = '"{}"'.format(lg.objs.request.search)
            sh.objs.get_mes(f,mes,True).show_debug()
            self.load_article()
    
    def clear_search_field(self):
        #TODO: implement
        #objs.get_suggest().get_gui().close()
        self.panel.ent_src.clear()
    
    def reset(self,cells):
        f = '[MClientQt] mclient.App.reset'
        self.table.reset(cells)
    
    def minimize(self):
        self.gui.minimize()
    
    def update_ui(self):
        ''' #NOTE: Focusing on the entry will disable left-right arrow keys
            since the table must have a focus for these keys to work. This
            happens owing to that Qt already has internal left-right
            arrow bindings for the entry, and we need to subclass the entry
            and override these bindings.
        '''
        self.gui.panel.ent_src.focus()
        #TODO: load from logic
        sources = (_('Multitran'),_('Stardict'),'Lingvo (DSL)',_('Local MT'))
        self.gui.panel.opt_src.reset(sources)
        self.gui.panel.opt_col.reset((1,2,3,4,5,6,7,8,9,10),4)
        #TODO: load from logic
        langs1 = (_('English'),_('Russian'),_('French'))
        langs2 = (_('Russian'),_('English'),_('French'))
        self.gui.panel.opt_lg1.reset(langs1)
        self.gui.panel.opt_lg2.reset(langs2)
    
    def show(self,event=None):
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def set_bindings(self):
        # Mouse buttons cannot be bound
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.minimize)
        self.gui.bind('Down',self.table.go_down)
        self.gui.bind('Up',self.table.go_up)
        self.gui.bind('Ctrl+Home',self.table.go_start)
        self.gui.bind('Ctrl+End',self.table.go_end)
        self.gui.bind('Home',self.table.go_line_start)
        self.gui.bind('End',self.table.go_line_end)
        self.gui.bind('Left',self.table.go_left)
        self.gui.bind('Right',self.table.go_right)
        self.gui.bind('F1',self.toggle_about)
        self.gui.bind('F3',self.table.search_next)
        self.gui.bind('Shift+F3',self.table.search_prev)
        self.gui.bind('Ctrl+F',self.table.search.show)
        self.gui.bind('Return',self.go_keyboard)
        self.table.gui.click_middle = self.minimize
        ''' Recalculate pages each time the main window is resized. This allows
            to save resources and avoid getting dummy geometry which will be
            returned before the window is shown.
        '''
        self.gui.parent.resizeEvent = self.table.set_coords
        self.panel.btn_trn.action = self.go_keyboard
        self.panel.btn_clr.action = self.clear_search_field
        self.panel.btn_abt.action = self.toggle_about
        self.panel.btn_abt.set_action()
        self.panel.btn_trn.set_action()
        self.panel.btn_clr.set_action()
        self.panel.ent_src.widget.act_on_home = self.table.go_line_start
        self.panel.ent_src.widget.act_on_end = self.table.go_line_end
        self.panel.ent_src.widget.act_on_ctrl_home = self.table.go_start
        self.panel.ent_src.widget.act_on_ctrl_end = self.table.go_end
        self.panel.ent_src.widget.act_on_left = self.table.go_left
        self.panel.ent_src.widget.act_on_right = self.table.go_right
    
    def set_title(self,title='MClientQt'):
        self.gui.set_title(title)
    
    def set_gui(self):
        self.table = Table()
        self.panel = gi.Panel()
        self.about = About()
        self.gui.set_gui(self.table.gui,self.panel)
        self.set_title()
        self.set_bindings()



class SearchArticle:
    
    def __init__(self):
        self.Shown = False
        self.logic = lg.SearchArticle()
        self.gui = gi.SearchArticle()
        self.set_bindings()
        self.gui.ent_src.focus()
    
    def clear(self):
        self.gui.clear()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def show(self):
        self.Shown = True
        self.gui.show()
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
        self.gui.btn_cls.action = self.close
        self.gui.btn_clr.action = self.clear
        self.gui.btn_cls.set_action()
        self.gui.btn_clr.set_action()
    
    def reset(self,cells,plain,rowno,colno):
        self.pattern = self.gui.ent_src.get()
        Case = self.gui.cbx_cas.get()
        self.logic.reset(cells,plain,self.pattern,rowno,colno,Case)
    
    def search_next(self):
        f = '[MClientQt] mclient.SearchArticle.search_next'
        rowno, colno = self.logic.search_next()
        if rowno < self.logic.rowno:
            mes = _('The end has been reached. Searching from the start.')
            sh.objs.get_mes(f,mes).show_info()
        elif rowno == self.logic.rowno and colno == self.logic.colno:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()
        return(rowno,colno)
    
    def search_prev(self):
        f = '[MClientQt] mclient.SearchArticle.search_prev'
        rowno, colno = self.logic.search_prev()
        if rowno > self.logic.rowno:
            mes = _('The start has been reached. Searching from the end.')
            sh.objs.get_mes(f,mes).show_info()
        elif rowno == self.logic.rowno and colno == self.logic.colno:
            mes = _('No matches!')
            sh.objs.get_mes(f,mes).show_info()
        return(rowno,colno)



class About:
    
    def __init__(self):
        self.Shown = False
        self.logic = lg.About()
        self.gui = gi.About()
        self.set_text()
        self.gui.set_title()
        self.set_bindings()
    
    def set_text(self,text=''):
        if not text:
            text = self.logic.set_code()
        self.gui.set_text(text)
    
    def set_bindings(self):
        self.gui.bind('Ctrl+Q',self.close)
        self.gui.bind('Esc',self.close)
        self.gui.bind('F1',self.toggle)
    
    def centralize(self):
        self.gui.centralize()
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()


if __name__ == '__main__':
    f = '[MClient] mclient.__main__'
    sh.com.start()
    lg.objs.get_plugins(Debug=False,maxrows=1000)
    '''
    db = DB()
    data = db.fetch()
    blocks = lg.com.set_blocks(data)
    '''
    lg.objs.get_request().search = 'h'
    timer = sh.Timer(f + ': Showing GUI')
    timer.start()
    app = App()
    ''' We can get a constant mouse hovering response only if we install
        the filter like this.
    '''
    sh.objs.get_root().installEventFilter(app.gui.table)
    sh.objs.get_root().installEventFilter(app.gui.panel)
    lg.com.get_url()
    blocks = app.load_article()
    cells = lg.Cells(blocks).run()
    app.reset(cells)
    timer.end()
    app.show()
    #db.close()
    sh.com.end()
