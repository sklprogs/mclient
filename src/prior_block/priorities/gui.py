#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# This module uses third-party code, license: resources/third parties.txt
# See https://github.com/jimmykuu/PyQt-PySide-Cookbook/blob/master/tree/drop_indicator.md

import PyQt5
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

icn_btm = sh.objs.get_pdir().add('..', 'resources', 'buttons', 'bottom.png')
icn_dwn = sh.objs.pdir.add('..', 'resources', 'buttons', 'down.png')
icn_lft = sh.objs.pdir.add('..', 'resources', 'buttons', 'go_back.png')
icn_rht = sh.objs.pdir.add('..', 'resources', 'buttons', 'go_next.png')
icn_top = sh.objs.pdir.add('..', 'resources', 'buttons', 'top.png')
icn_up1 = sh.objs.pdir.add('..', 'resources', 'buttons', 'up.png')


class View(PyQt5.QtWidgets.QTreeView):

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.dropIndicatorRect = PyQt5.QtCore.QRect()

    def paintEvent(self, event):
        painter = PyQt5.QtGui.QPainter(self.viewport())
        self.drawTree(painter, event.region())
        # Originally it calls the inline function paintDropIndicator here
        self.paintDropIndicator(painter)

    def paintDropIndicator(self, painter):
        if self.state() == PyQt5.QtWidgets.QAbstractItemView.DraggingState:
            opt = PyQt5.QtWidgets.QStyleOption()
            opt.initFrom(self)
            opt.rect = self.dropIndicatorRect
            rect = opt.rect

            brush = PyQt5.QtGui.QBrush(PyQt5.QtGui.QColor(PyQt5.QtCore.Qt.black))

            if rect.height() == 0:
                pen = PyQt5.QtGui.QPen(brush, 2, PyQt5.QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(rect.topLeft(), rect.topRight())
            else:
                pen = PyQt5.QtGui.QPen(brush, 2, PyQt5.QtCore.Qt.SolidLine)
                painter.setPen(pen)
                painter.drawRect(rect)



class TreeWidget(PyQt5.QtWidgets.QTreeWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _dump(self, parent):
        dic = {}
        for row in range(parent.childCount()):
            child = parent.child(row)
            dic[child.text(0)] = self._dump(child)
        return dic
    
    def dump(self):
        return self._dump(self.invisibleRootItem())
    
    def _set_item(self, parent, section):
        f = '[MClient] prior_block.priorities.gui.TreeWidget._set_item'
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
        self.setColumnCount(1)
        self._set_item(None, dic)



class Tree(TreeWidget, View):

    def fill(self, dic):
        TreeWidget.fill(self, dic)
    
    def startDrag(self, supportedActions):
        listsQModelIndex = self.selectedIndexes()
        if listsQModelIndex:
            dataQMimeData = self.model().mimeData(listsQModelIndex)
            dragQDrag = PyQt5.QtGui.QDrag(self)
            dragQDrag.setMimeData(dataQMimeData)
            defaultDropAction = PyQt5.QtCore.Qt.IgnoreAction
            if ((supportedActions & PyQt5.QtCore.Qt.CopyAction) \
            and (self.dragDropMode() != PyQt5.QtWidgets.QAbstractItemView.InternalMove)):
                defaultDropAction = PyQt5.QtCore.Qt.CopyAction
            dragQDrag.exec_(supportedActions, defaultDropAction)

    def dragMoveEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)
        if not item:
            return
        # This always gets default column 0 index
        index = self.indexFromItem(item)

        rect = self.visualRect(index)
        rect_left = self.visualRect(index.sibling(index.row(), 0))
        # In case the section has been moved
        rect_right = self.visualRect (index.sibling(index.row()
                                     ,self.header().logicalIndex(self.columnCount() - 1))
                                     )

        self.dropIndicatorPosition = self.position(event.pos(), rect, index)

        if self.dropIndicatorPosition == self.AboveItem:
            self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                  ,rect_left.top()
                                                  ,rect_right.right() - rect_left.left()
                                                  ,0
                                                  )
            event.accept()
        elif self.dropIndicatorPosition == self.BelowItem:
            self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                        ,rect_left.bottom()
                                                        ,rect_right.right() - rect_left.left()
                                                        ,0
                                                        )
            event.accept()
        elif self.dropIndicatorPosition == self.OnItem:
            self.dropIndicatorRect = PyQt5.QtCore.QRect (rect_left.left()
                                                        ,rect_left.top()
                                                        ,rect_right.right() - rect_left.left()
                                                        ,rect.height()
                                                        )
            event.accept()
        else:
            self.dropIndicatorRect = PyQt5.QtCore.QRect()

        self.model().setData (index, self.dropIndicatorPosition
                             ,PyQt5.QtCore.Qt.UserRole
                             )

        # This is necessary or else the previously drawn rect won't be erased
        self.viewport().update()

    def dropEvent(self, event):
        pos = event.pos()
        item = self.itemAt(pos)

        if item is self.currentItem():
            TreeWidget.dropEvent(self, event)
            event.accept()
            return

        if item:
            index = self.indexFromItem(item)
            self.model().setData(index, 0, PyQt5.QtCore.Qt.UserRole)

        cond1 = event.source != self or event.dropAction() != PyQt5.QtCore.Qt.MoveAction
        cond2 = self.dragDropMode() != PyQt5.QtWidgets.QAbstractItemView.InternalMove
        if cond1 and cond2:
            return
        topIndex = PyQt5.QtCore.QModelIndex()
        col = -1
        row = -1
        lst = [event, row, col, topIndex]
        if not self.dropOn(lst):
            return
        event, row, col, topIndex = lst
        idxs = self.selectedIndexes()
        indexes = []
        existing_rows = set()
        for i in idxs:
            if i.row() not in existing_rows:
                indexes.append(i)
                existing_rows.add(i.row())

        if topIndex in indexes:
            return

        dropRow = self.model().index(row, col, topIndex)
        taken = []

        indexes_reverse = indexes[:]
        indexes_reverse.reverse()
        i = 0
        for index in indexes_reverse:
            parent = self.itemFromIndex(index)
            if not parent or not parent.parent():
                '''
                if not parent or not isinstance (parent.parent()
                                                ,PyQt5.QtWidgets.QTreeWidgetItem
                                                ):
                '''
                taken.append(self.takeTopLevelItem(index.row()))
            else:
                taken.append(parent.parent().takeChild(index.row()))

            i += 1
            # break

        taken.reverse()

        for index in indexes:
            if row == -1:
                if topIndex.isValid():
                    parent = self.itemFromIndex(topIndex)
                    parent.insertChild(parent.childCount(), taken[0])
                    taken = taken[1:]

                else:
                    self.insertTopLevelItem (self.topLevelItemCount()
                                            ,taken[0]
                                            )
                    taken = taken[1:]
            else:
                r = dropRow.row() if dropRow.row() >= 0 else row
                if topIndex.isValid():
                    parent = self.itemFromIndex(topIndex)
                    parent.insertChild (min(r, parent.childCount())
                                       ,taken[0]
                                       )
                    taken = taken[1:]
                else:
                    self.insertTopLevelItem (min(r, self.topLevelItemCount())
                                            ,taken[0]
                                            )
                    taken = taken[1:]

        event.accept()

        TreeWidget.dropEvent(self, event)
        self.expandAll()

    def position(self, pos, rect, index):
        r = PyQt5.QtWidgets.QAbstractItemView.OnViewport
        ''' margin*2 must be smaller than row height, or the drop onItem rect
            will no show up.
        '''
        margin = 10
        if pos.y() - rect.top() < margin:
            r = PyQt5.QtWidgets.QAbstractItemView.AboveItem
        elif rect.bottom() - pos.y() < margin:
            r = PyQt5.QtWidgets.QAbstractItemView.BelowItem

        # This rect is always the first column rect
        # elif rect.contains(pos, True):
        elif pos.y() - rect.top() > margin and rect.bottom() - pos.y() > margin:
            r = PyQt5.QtWidgets.QAbstractItemView.OnItem

        return r

    def dropOn(self, lst):

        event, row, col, index = lst

        root = self.rootIndex()

        if self.viewport().rect().contains(event.pos()):
            index = self.indexAt(event.pos())
            if not index.isValid() or not self.visualRect(index).contains(event.pos()):
                index = root

        if index != root:
            '''
            dropIndicatorPosition = self.position (event.pos()
                                                  ,self.visualRect(index)
                                                  ,index
                                                  )
            '''
            self.position(event.pos(), self.visualRect(index), index)
            if self.dropIndicatorPosition == self.AboveItem:
                print('dropon above')
                row = index.row()
                col = index.column()
                index = index.parent()

            elif self.dropIndicatorPosition == self.BelowItem:
                print('dropon below')
                row = index.row() + 1
                col = index.column()
                index = index.parent()

            elif self.dropIndicatorPosition == self.OnItem:
                print('dropon onItem')
                pass
            elif self.dropIndicatorPosition == self.OnViewport:
                pass
            else:
                pass

        else:
            self.dropIndicatorPosition = self.OnViewport

        lst[0], lst[1], lst[2], lst[3] = event, row, col, index

        #if not self.droppingOnItself(event, index):
        return True



class Priorities(PyQt5.QtWidgets.QWidget):

    sig_close = PyQt5.QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree_style = '''
                          QTreeView {
                              show-decoration-selected: 1;
                          }

                          QTreeView::item:hover {
                              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e7effd, stop: 1 #cbdaf1);
                          }

                          QTreeView::item:selected:active{
                              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6ea1f1, stop: 1 #567dbc);
                          }

                          QTreeView::item:selected:!active {
                              background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #6b9be8, stop: 1 #577fbf);
                          }
                          '''
        self.set_gui()
    
    def set_gui(self):
        self.set_title(_('Prioritization'))
        self.set_icon()
        self.set_layouts()
        self.set_widgets()
        self.set_buttons()
        self.add_widgets()
        self.add_buttons()
        self.set_headers()
        self.customize()
        self.resize(800, 450)
        self.centralize()
    
    def set_headers(self):
        self.tree1.setHeaderLabel(_('Prioritized subjects'))
        self.tree2.setHeaderLabel(_('Available subjects'))
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def get_index(self):
        #TODO: is this orphant?
        return self.lbx_lft.selectionModel().currentIndex()
    
    def get_row(self):
        #TODO: is this orphant?
        index_ = self.get_index()
        return(index_.row(), index_.column())
    
    def bind(self, hotkey, action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def add_buttons(self):
        #NOTE: If run directly, this module will not find icons owing to paths
        self.lay_btn.addWidget(self.btn_lft.widget)
        self.lay_btn.addWidget(self.btn_rht.widget)
        self.lay_btn.addWidget(self.btn_up1.widget)
        self.lay_btn.addWidget(self.btn_dwn.widget)
        self.lay_btn.addWidget(self.btn_top.widget)
        self.lay_btn.addWidget(self.btn_btm.widget)
    
    def set_buttons(self):
        self.btn_lft = sh.Button (hint = _('Prioritize selection on the right')
                                 ,inactive = icn_lft
                                 ,active = icn_lft
                                 )
        self.btn_rht = sh.Button (hint = _('Unprioritize selection on the left')
                                 ,inactive = icn_rht
                                 ,active = icn_rht
                                 )
        self.btn_up1 = sh.Button (hint = _('Increase priority')
                                 ,inactive = icn_up1
                                 ,active = icn_up1
                                 )
        self.btn_dwn = sh.Button (hint = _('Decrease priority')
                                 ,inactive = icn_dwn
                                 ,active = icn_dwn
                                 )
        self.btn_top = sh.Button (hint = _('Move to the top')
                                 ,inactive = icn_top
                                 ,active = icn_top
                                 )
        self.btn_btm = sh.Button (hint = _('Move to the bottom')
                                 ,inactive = icn_btm
                                 ,active = icn_btm
                                 )
        self.btn_res = sh.Button (text = _('Reset')
                                 ,hint = _('Reload subjects')
                                 )
        self.btn_apl = sh.Button (text = _('Apply')
                                 ,hint = _('Save and close')
                                 )
    
    def set_icon(self):
        # Does not accent None
        self.setWindowIcon(sh.gi.objs.get_icon())
    
    def customize(self):
        #self.lay_prm.setContentsMargins(0, 0, 0, 0)
        self.lay_sec.setContentsMargins(0, 0, 0, 0)
        self.lay_btn.setContentsMargins(4, 4, 4, 4)
        self.lay_ter.setContentsMargins(2, 4, 2, 0)
        self.lay_rht.setContentsMargins(0, 0, 0, 0)
        self.tree1.setSelectionMode(PyQt5.QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree2.setSelectionMode(PyQt5.QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree1.setDragDropMode(PyQt5.QtWidgets.QAbstractItemView.InternalMove)
        self.tree2.setDragDropMode(PyQt5.QtWidgets.QAbstractItemView.InternalMove)
        self.tree1.setStyleSheet(self.tree_style)
        self.tree2.setStyleSheet(self.tree_style)
        self.setStyleSheet('QTreeWidget::item{ height: 30px;  }')
    
    def set_layouts(self):
        self.lay_prm = PyQt5.QtWidgets.QVBoxLayout()
        self.lay_sec = PyQt5.QtWidgets.QGridLayout()
        self.lay_ter = PyQt5.QtWidgets.QGridLayout()
        self.lay_btn = PyQt5.QtWidgets.QVBoxLayout()
        self.lay_rht = PyQt5.QtWidgets.QHBoxLayout()
    
    def set_widgets(self):
        self.lbx_lft = View()
        self.lbx_rht = View()
        self.prm_sec = PyQt5.QtWidgets.QWidget()
        self.prm_ter = PyQt5.QtWidgets.QWidget()
        self.prm_btn = PyQt5.QtWidgets.QWidget()
        self.prm_rht = PyQt5.QtWidgets.QWidget()
        self.cbx_pri = sh.CheckBox(_('Enable'))
        sources = (_('All subjects'), _('Main'), _('From the article'))
        self.opt_src = sh.OptionMenu(sources)
        self.tree1 = Tree()
        self.tree2 = Tree()
    
    def add_widgets(self):
        self.lay_prm.addWidget(self.prm_sec)
        self.lay_prm.addWidget(self.prm_ter)
        self.lay_sec.addWidget(self.lbx_lft, 0, 0)
        self.lay_sec.addWidget(self.tree1, 0, 0)
        self.lay_sec.addWidget(self.prm_btn, 0, 1)
        self.lay_sec.addWidget(self.lbx_rht, 0, 2)
        self.lay_sec.addWidget(self.tree2, 0, 2)
        self.lay_ter.addWidget(self.btn_res.widget, 0, 1, PyQt5.QtCore.Qt.AlignLeft)
        self.lay_ter.addWidget(self.cbx_pri.widget, 0, 2, PyQt5.QtCore.Qt.AlignCenter)
        self.lay_ter.addWidget(self.prm_rht, 0, 3, PyQt5.QtCore.Qt.AlignRight)
        self.lay_rht.addWidget(self.opt_src.widget)
        self.lay_rht.addWidget(self.btn_apl.widget)
        self.prm_sec.setLayout(self.lay_sec)
        self.prm_btn.setLayout(self.lay_btn)
        self.prm_ter.setLayout(self.lay_ter)
        self.prm_rht.setLayout(self.lay_rht)
        self.setLayout(self.lay_prm)
    
    def fill1(self, dic):
        self.tree1.fill(dic)
    
    def fill2(self, dic):
        self.tree2.fill(dic)
    
    def set_title(self, title):
        self.setWindowTitle(title)
    
    def centralize(self):
        self.move(sh.objs.get_root().desktop().screen().rect().center() - self.rect().center())

    


if __name__ == '__main__':
    f = '[MClient] prior_block.priorities.gui.__main__'
    sh.com.start()
    iprior = Priorities()
    iprior.show()
    iprior.resize(800, 450)
    iprior.centralize()
    sh.com.end()
