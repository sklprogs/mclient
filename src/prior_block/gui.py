#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QTreeWidget, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.button.controller import Button
from skl_shared_qt.graphics.checkbox.controller import CheckBox
from skl_shared_qt.graphics.option_menu.controller import OptionMenu
from skl_shared_qt.graphics.root.controller import ROOT


class TreeWidget(QTreeWidget):
    
    sig_drop = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = ''
        self.target = None
        self.children = {}
        self.setColumnCount(1)
    
    def reset_drop(self):
        self.source = ''
        self.target = None
    
    def find(self, text):
        return self.findItems(text, Qt.MatchFlag.MatchContains | Qt.MatchFlag.MatchRecursive, 0)
    
    def clear_selection(self):
        self.selectionModel().clearSelection()
        if self.target:
            self.target.setSelected(True)
    
    def get_target_parent(self):
        parent = self.target.parent()
        if parent is None:
            parent = self.invisibleRootItem()
        return parent
    
    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.MouseButton.LeftButton:
            return
        self.startDrag(Qt.DropAction.MoveAction)
    
    def dragEnterEvent(self, event):
        f = '[MClient] prior_block.gui.TreeWidget.dragEnterEvent'
        index_ = self.indexAt(event.position().toPoint())
        item = self.itemFromIndex(index_)
        if not item:
            rep.empty(f)
            return
        self.source = item.text(0)
        self.children = self._dump(item)
        super(QTreeWidget, self).dragEnterEvent(event)
        event.accept()
    
    def dropEvent(self, event):
        super(QTreeWidget, self).dropEvent(event)
        event.accept()
        self.sig_drop.emit()
    
    def collapse_all(self):
        self.collapseAll()
    
    def expand_all(self):
        self.expandAll()
    
    def set_header(self, title):
        self.setHeaderLabel(title)
    
    def _dump(self, parent):
        dic = {}
        for row in range(parent.childCount()):
            child = parent.child(row)
            dic[child.text(0)] = self._dump(child)
        return dic
    
    def dump(self):
        return self._dump(self.invisibleRootItem())
    
    def _set_item(self, parent, section):
        f = '[MClient] prior_block.gui.TreeWidget._set_item'
        if not isinstance(section, dict):
            mes = _('Unexpected type: {}').format(type(section))
            Message(f, mes).show_warning()
            return
        for key, value in section.items():
            item = QTreeWidgetItem([key])
            if parent is None:
                self.addTopLevelItem(item)
            else:
                parent.addChild(item)
            self._set_item(item, value)
    
    def fill(self, dic):
        self.clear()
        self._set_item(None, dic)



class Panes(QWidget):
    
    sig_close = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.set_gui()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def reset_drop(self):
        self.tree1.reset_drop()
        self.tree2.reset_drop()
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def expand_all(self):
        self.tree1.expand_all()
        self.tree2.expand_all()
    
    def fill(self, dic1, dic2):
        self.tree1.fill(dic1)
        self.tree2.fill(dic2)
    
    def set_widgets(self):
        self.tree1 = TreeWidget()
        self.tree2 = TreeWidget()
        self.btn_res = Button(text = _('Reset')
                             ,hint = _('Reject changes and reload subjects'))
        self.cbx_pri = CheckBox(_('Enable'))
        sources = (_('All subjects'), _('From the article'))
        self.opt_src = OptionMenu(sources)
        self.btn_apl = Button(text = _('Apply')
                             ,hint = _('Apply changes and close the window'))
    
    def configure(self):
        self.tree1.set_header(_('Prioritized subjects'))
        self.tree2.set_header(_('Available subjects'))
        self.tree1.setAcceptDrops(True)
        self.tree2.setAcceptDrops(True)
        self.tree1.setDragEnabled(True)
        self.tree2.setDragEnabled(True)
        self.tree1.setAlternatingRowColors(True)
        self.tree2.setAlternatingRowColors(True)
        self.grid.setContentsMargins(4, 0, 4, 3)
        self.setMinimumSize(700, 500)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def set_gui(self):
        self.set_widgets()
        self.set_layout()
        self.configure()
        self.centralize()
    
    def set_layout(self):
        self.grid = QGridLayout()
        self.grid.addWidget(self.tree1, 0, 0, 1, 4)
        self.grid.addWidget(self.tree2, 0, 4, 1, 4)
        self.grid.addWidget(self.btn_res.widget, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.cbx_pri.widget, 1, 2, 1, 4, Qt.AlignmentFlag.AlignCenter)
        self.grid.addWidget(self.opt_src.widget, 1, 6, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.grid.addWidget(self.btn_apl.widget, 1, 7, 1, 1, Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.grid)
    
    def centralize(self):
        self.move(ROOT.get_root().primaryScreen().geometry().center() - self.rect().center())
