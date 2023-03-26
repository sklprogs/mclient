#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import gui as gi


class App:
    
    def __init__(self):
        # 'thread' name is OK here, but will override a built-in method in GUI
        self.thread = gi.Thread()
        self.gui = gi.App()
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


if __name__ == '__main__':
    f = '__main__'
    sh.com.start()
    app = App()
    app.show()
    app.run_thread()
    sh.com.end()
