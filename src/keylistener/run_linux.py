#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import time
import PyQt5.QtCore
import PyQt5.QtWidgets

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import gui as gi


class App:
    
    def __init__(self):
        self.gui = gi.App()
    
    def report(self):
        print('Triggered')
        self.gui.button.setText('SUCCESS')
    
    def run_thread(self):
        self.gui.run_thread()
        self.gui.catcher.bind_catch(self.report)
        self.gui.ithread.start()
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = App()
    app.show()
    app.run_thread()
    sh.com.end()
