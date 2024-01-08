#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import PyQt6.QtCore
import PyQt6.QtWidgets

#from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import gui as gi


class App:
    
    def __init__(self):
        # 'thread' name is OK here, but will override a built-in method in GUI
        self.thread = gi.Thread()
        self.gui = Gui()
        self.set_bindings()
    
    def run_thread(self):
        self.thread.run_thread()
    
    def report(self):
        print('Triggered')
        self.gui.button.setText('SUCCESS')
    
    def set_bindings(self):
        self.thread.bind_catch(self.report)
        self.gui.sig_close.connect(self.thread.end)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()



class Gui(PyQt6.QtWidgets.QWidget):
    
    sig_close = PyQt6.QtCore.pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_gui()
    
    def closeEvent(self, event):
        self.sig_close.emit()
        return super().closeEvent(event)
    
    def report(self):
        print('Triggered')
        self.button.setText('SUCCESS')
    
    def bind(self, hotkeys, action):
        for hotkey in hotkeys:
            PyQt6.QtGui.QShortcut(PyQt6.QtGui.QKeySequence(hotkey), self).activated.connect(action)
    
    def set_gui(self):
        self.button = PyQt6.QtWidgets.QPushButton()
        self.button.setText('Click me!')
        layout_ = PyQt6.QtWidgets.QHBoxLayout()
        layout_.addWidget(self.button)
        self.setLayout(layout_)


if __name__ == '__main__':
    f = '[MClient] keylistener.test.__main__'
    sh.com.start()
    app = App()
    app.show()
    app.run_thread()
    sh.com.end()
