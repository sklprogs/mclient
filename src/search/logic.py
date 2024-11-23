#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.message.controller import rep


class Search:

    def __init__(self, text=None, pattern=None):
        self.Success = False
        self.i = 0
        self.nextloop = []
        self.prevloop = []
        if text and pattern:
            self.reset(text, pattern)

    def reset(self, text, pattern):
        f = '[SharedQt] search.logic.Search.reset'
        self.Success = True
        self.i = 0
        self.nextloop = []
        self.prevloop = []
        self.text = text
        self.pattern = pattern
        if not self.pattern or not self.text:
            self.Success = False
            rep.wrong_input(f)

    def add(self):
        f = '[SharedQt] search.logic.Search.add'
        if not self.Success:
            rep.cancel(f)
            return
        if len(self.text) > self.i + len(self.pattern) - 1:
            self.i += len(self.pattern)

    def get_next(self):
        f = '[SharedQt] search.logic.Search.get_next'
        if not self.Success:
            rep.cancel(f)
            return
        result = self.text.find(self.pattern, self.i)
        if result != -1:
            self.i = result
            self.add()
            # Do not allow -1 as output
            return result

    def get_prev(self):
        f = '[SharedQt] search.logic.Search.get_prev'
        if not self.Success:
            rep.cancel(f)
            return
        ''' rfind, unlike find, does not include limits, so we can use it to
            search backwards.
        '''
        result = self.text.rfind(self.pattern, 0, self.i)
        if result != -1:
            self.i = result
        return result

    def get_next_loop(self):
        f = '[SharedQt] search.logic.Search.get_next_loop'
        if not self.Success:
            rep.cancel(f)
            return self.nextloop
        if self.nextloop:
            return self.nextloop
        self.i = 0
        while True:
            result = self.get_next()
            if result is None:
                break
            else:
                self.nextloop.append(result)
        return self.nextloop

    def get_prev_loop(self):
        f = '[SharedQt] search.logic.Search.get_prev_loop'
        if not self.Success:
            rep.cancel(f)
            return self.prevloop
        if self.prevloop:
            return self.prevloop
        self.i = len(self.text)
        while True:
            result = self.get_prev()
            if result is None:
                break
            else:
                self.prevloop.append(result)
        return self.prevloop
