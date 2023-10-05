import PyQt5
import PyQt5.QtWidgets
import PyQt5.QtCore
import PyQt5.QtGui

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class TreeWidget(PyQt5.QtWidgets.QTreeWidget):
    
    sig_drop = PyQt5.QtCore.pyqtSignal()
    
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
        return self.findItems(text, PyQt5.QtCore.Qt.MatchContains | PyQt5.QtCore.Qt.MatchRecursive, 0)
    
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
        if event.buttons() != PyQt5.QtCore.Qt.LeftButton:
            return
        self.startDrag(PyQt5.QtCore.Qt.MoveAction)
    
    def dragEnterEvent(self, event):
        f = '[MClientQt] prior_block.gui.TreeWidget.dragEnterEvent'
        index_ = self.indexAt(event.pos())
        item = self.itemFromIndex(index_)
        if not item:
            sh.com.rep_empty(f)
            return
        self.source = item.text(0)
        self.children = self._dump(item)
        super(PyQt5.QtWidgets.QTreeWidget, self).dragEnterEvent(event)
        event.accept()
    
    def dropEvent(self, event):
        super(PyQt5.QtWidgets.QTreeWidget, self).dropEvent(event)
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
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        for key, value in section.items():
            item = PyQt5.QtWidgets.QTreeWidgetItem([key])
            if parent is None:
                self.addTopLevelItem(item)
            else:
                parent.addChild(item)
            self._set_item(item, value)
    
    def fill(self, dic):
        self.clear()
        self._set_item(None, dic)



class Panes(PyQt5.QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        self.set_gui()
    
    def reset_drop(self):
        self.trw_lft.reset_drop()
        self.trw_rht.reset_drop()
    
    def bind(self, hotkey, action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def expand_all(self):
        self.trw_lft.expand_all()
        self.trw_rht.expand_all()
    
    def fill(self, dic1, dic2):
        self.trw_lft.fill(dic1)
        self.trw_rht.fill(dic2)
    
    def set_widgets(self):
        self.trw_lft = TreeWidget()
        self.trw_rht = TreeWidget()
        self.btn_res = sh.Button (text = _('Reset')
                                 ,hint = _('Forget changes and reload subjects')
                                 )
        self.cbx_pri = sh.CheckBox(_('Enable'))
        sources = (_('All subjects'), _('From the article'))
        self.opt_src = sh.OptionMenu(sources)
    
    def configure(self):
        self.trw_lft.set_header(_('Prioritized subjects'))
        self.trw_rht.set_header(_('Available subjects'))
        self.trw_lft.setAcceptDrops(True)
        self.trw_rht.setAcceptDrops(True)
        self.trw_lft.setDragEnabled(True)
        self.trw_rht.setDragEnabled(True)
        self.trw_lft.setAlternatingRowColors(True)
        self.trw_rht.setAlternatingRowColors(True)
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
        self.grid = PyQt5.QtWidgets.QGridLayout()
        self.grid.addWidget(self.trw_lft, 0, 0, 1, 3)
        self.grid.addWidget(self.trw_rht, 0, 3, 1, 3)
        self.grid.addWidget(self.btn_res.widget, 1, 0, 1, 2, PyQt5.QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.cbx_pri.widget, 1, 2, 1, 2, PyQt5.QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.opt_src.widget, 1, 4, 1, 2, PyQt5.QtCore.Qt.AlignRight)
        self.setLayout(self.grid)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())
