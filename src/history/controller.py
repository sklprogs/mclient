#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep

from history.gui import History as guiHistory, TableModel


class History:
    
    def __init__(self):
        self.Shown = False
        self.set_gui()
        self.fill_model()
    
    def set_gui(self):
        self.gui = guiHistory()
        self.set_title()
        self.set_bindings()
    
    def change_row(self):
        f = '[MClient] history.controller.History.change_row'
        ''' We should either calculate a row number by the mouse click event or
            load the new article twice when the history window is opened.
        '''
        if not self.Shown:
            rep.lazy(f)
            return
        rowno = self.gui.get_row()
        try:
            id_ = self.model.items[rowno][0]
        except IndexError:
            rep.wrong_input(f, rowno)
            return
        self.gui.sig_go.emit(int(id_) - 1)
    
    def fill_model(self, table=[[]]):
        ''' Do not assign 'gui.TableModel' externally, this will not change
            the actual model.
        '''
        self.model = TableModel(table)
        self.gui.set_model(self.model)
        # Must be done only after setting a model
        self.gui.history.selectionModel().selectionChanged.connect(self.change_row)
    
    def _go_row(self, rowno):
        self.gui.clear_selection()
        index_ = self.model.index(rowno, 0)
        self.gui.set_index(index_)
        self.gui.select_row(index_)
    
    def go_down(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] history.controller.History.go_down'
        if not self.model.items or not self.model.items[0]:
            rep.empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == len(self.model.items) - 1:
            rowno = -1
        rowno += 1
        self._go_row(rowno)
    
    def go_up(self):
        # Qt already goes down/up, but without looping
        f = '[MClient] history.controller.History.go_up'
        if not self.model.items or not self.model.items[0]:
            rep.empty(f)
            return
        old = rowno = self.gui.get_row()
        if rowno == 0:
            rowno = len(self.model.items)
        rowno -= 1
        self._go_row(rowno)
    
    def _find_id(self, id_):
        for i in range(len(self.model.items)):
            if self.model.items[i] and self.model.items[i][0] == id_:
                return i
    
    def add_row(self, id_, source, lang1, lang2, search):
        f = '[MClient] history.controller.History.add_row'
        if not self.model.items:
            rep.empty(f)
            return
        # Avoid getting out of bounds, since our table is initially [[]]
        if self.model.items[0] == []:
            del self.model.items[0]
        rowno = self._find_id(str(id_ + 1))
        if rowno is None:
            row = [str(id_ + 1), source, lang1, lang2, search]
            self.model.items.append(row)
            self.model.update()
            self._go_row(len(self.model.items)-1)
        else:
            self._go_row(rowno)
    
    def set_title(self, title=_('History')):
        self.gui.set_title(title)
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.bind(('Down', 'Right', 'Alt+Right'), self.go_down)
        self.gui.bind(('Up', 'Left', 'Alt+Left'), self.go_up)
    
    def show(self):
        self.Shown = True
        self.gui.show()
        self.gui.centralize()
    
    def close(self):
        self.Shown = False
        self.gui.close()
    
    def toggle(self):
        if self.Shown:
            self.close()
        else:
            self.show()
