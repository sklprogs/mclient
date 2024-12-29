#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.clipboard.controller import CLIPBOARD
from skl_shared_qt.paths import Path
from skl_shared_qt.text_file import Write
from skl_shared_qt.pretty_html import make_pretty

from config import CONFIG
from logic import HTM
from manager import PLUGINS
from articles import ARTICLES
from save.gui import Save as guiSave, TableModel


class Save:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
        self.add_bindings()
        self.fill_model()
    
    def set_gui(self):
        self.gui = guiSave()
        self.set_title()
        self.set_bindings()
        self.change_font_size(2)
    
    def get(self):
        f = '[MClient] save.controller.Save.get'
        if not self.model.items:
            rep.lazy(f)
            return
        return self.model.items[self.gui.get_row()]
    
    def go_start(self):
        f = '[MClient] save.controller.Save.go_start'
        if not self.model.items:
            rep.lazy(f)
            return
        self._go_row(0)
    
    def go_end(self):
        f = '[MClient] save.controller.Save.go_end'
        if not self.model.items:
            rep.lazy(f)
            return
        rowno = len(self.model.items) - 1
        self._go_row(rowno)
    
    def go_down(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] save.controller.Save.go_down'
        if not self.model.items:
            rep.empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == len(self.model.items) - 1:
            rowno = -1
        rowno += 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old, rowno)
        Message(f, mes).show_debug()
    
    def go_up(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] save.controller.Save.go_up'
        if not self.model.items:
            rep.empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == 0:
            rowno = len(self.model.items)
        rowno -= 1
        self._go_row(rowno)
        mes = _('Change row number: {} → {}').format(old, rowno)
        Message(f, mes).show_debug()
    
    def change_font_size(self, delta=1):
        f = '[MClient] save.controller.Save.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            rep.empty(f)
            return
        if size + delta <= 0:
            rep.condition(f, f'{size} + {delta} > 0')
            return
        self.gui.set_font_size(size+delta)
    
    def fill_model(self):
        ''' Do not assign 'TableModel' externally, this will not change
            the actual model.
        '''
        self.model = TableModel()
        self.gui.set_model(self.model)
        if self.model.items:
            self._go_row(0)
    
    def _go_row(self, rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno, 0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def set_title(self, title=_('Save article')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.bind(('Down',), self.go_down)
        self.gui.bind(('Up',), self.go_up)
        self.gui.bind(('Home',), self.go_start)
        self.gui.bind(('End',), self.go_end)
        self.gui.bind(('Ctrl+Home',), self.go_start)
        self.gui.bind(('Ctrl+End',), self.go_end)
        self.gui.bind(CONFIG.new['actions']['save_article']['hotkeys'], self.toggle)
        self.gui.sig_close.connect(self.close)
    
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
    
    def _get_text(self):
        f = '[MClient] save.controller.Save._get_text'
        text = []
        text_row = []
        cells = ARTICLES.get_table()
        if not cells:
            rep.empty(f)
            return ''
        for row in cells:
            for cell in row:
                if not cell.text.strip():
                    continue
                if cell.colno == 0 and cell.fixed_block:
                    if text_row:
                        text_row = ''.join(text_row)
                        # Removing '; ' before subject-related cells
                        text.append(text_row[:-2])
                        text_row = []
                text_row.append(cell.text)
                if cell.colno == 0 and cell.fixed_block:
                    text_row.append(': ')
                else:
                    text_row.append('; ')
        if text_row:
            # Removing '; ' before subject-related cells
            text_row = ''.join(text_row)
            text.append(text_row[:-2])
        return '\n\n'.join(text)
    
    def add_bindings(self):
        self.gui.save.clicked.connect(self.select)
        self.gui.bind(('Return',), self.select)
        self.gui.bind(('Enter',), self.select)
    
    def select(self):
        f = '[MClient] save.controller.Save.select'
        opt = self.get()
        if not opt:
            rep.empty(f)
            return
        self.close()
        if opt == _('Save the current view as a web-page (*.htm)'):
            self.save_view_as_htm()
        elif opt == _('Save the original article as a web-page (*.htm)'):
            self.save_raw_as_htm()
        elif opt == _('Save the article as plain text in UTF-8 (*.txt)'):
            self.save_view_as_txt()
        elif opt == _('Copy the code of the article to clipboard'):
            self.copy_raw()
        elif opt == _('Copy the text of the article to clipboard'):
            self.copy_view()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(opt, '; '.join(self.model.items))
            Message(f, mes, True).show_error()

    def _add_web_ext(self):
        if not Path(self.file).get_ext_low() in ('.htm', '.html'):
            self.file += '.htm'
    
    def save_view_as_htm(self):
        f = '[MClient] save.controller.Save.save_view_as_htm'
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        if not self.file:
            rep.empty(f)
            return
        # Can be an empty list
        cells = ARTICLES.get_table()
        #TODO: elaborate
        skipped = []
        #skipped = com.get_skipped_terms()
        code = HTM(cells, skipped).run()
        if not code:
            rep.empty(f)
            return
        self._add_web_ext()
        # Takes ~0.47s for 'set' on Intel Atom, do not call in 'load_article'
        code = make_pretty(code)
        Write(self.file).write(code)

    def save_raw_as_htm(self):
        f = '[MClient] mclient.Save.save_raw_as_htm'
        ''' Key 'html' may be needed to write a file in the UTF-8 encoding,
            therefore, in order to ensure that the web-page is read correctly,
            we change the encoding manually. We also replace abbreviated
            hyperlinks with full ones in order to ensure that they are also
            valid in the local file.
        '''
        self.gui.ask.filter = _('Web-pages (*.htm, *.html)')
        self.file = self.gui.ask.save()
        code = ARTICLES.get_raw_code()
        if not self.file or not code:
            rep.empty(f)
            return
        self._add_web_ext()
        code = PLUGINS.fix_raw_htm(code)
        Write(self.file).write(code)

    def save_view_as_txt(self):
        f = '[MClient] mclient.Save.save_view_as_txt'
        self.gui.ask.filter = _('Plain text (*.txt)')
        self.file = self.gui.ask.save()
        text = self._get_text()
        if not self.file or not text:
            rep.empty(f)
            return
        if not Path(self.file).get_ext_low() == '.txt':
            self.file += '.txt'
        Write(self.file).write(text)

    def copy_raw(self):
        CLIPBOARD.copy(ARTICLES.get_raw_code())

    def copy_view(self):
        CLIPBOARD.copy(self._get_text())
