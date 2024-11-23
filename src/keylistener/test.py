#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QShortcut, QKeySequence

from skl_shared_qt.graphics.root.controller import ROOT

from keylistener.gui import Thread


class App:
    
    def __init__(self):
        # 'thread' name is OK here, but will override a built-in method in GUI
        self.thread = Thread()
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



class Gui(QWidget):
    
    sig_close = pyqtSignal()
    
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
            QShortcut(QKeySequence(hotkey), self).activated.connect(action)
    
    def set_gui(self):
        self.button = QPushButton()
        self.button.setText('Click me!')
        layout_ = QHBoxLayout()
        layout_.addWidget(self.button)
        self.setLayout(layout_)


if __name__ == '__main__':
    f = '[MClient] keylistener.test.__main__'
    app = App()
    app.show()
    app.run_thread()
    ROOT.end()
