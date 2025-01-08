#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.root.controller import ROOT

from config import CONFIG
from manager import PLUGINS
from articles import ARTICLES

from prior_block.gui import Panes as guiPanes


def get_article_subjects():
    f = '[MClient] prior_block.controller.get_article_subjects'
    subjfs = ARTICLES.get_subjf()
    if not subjfs:
        rep.empty(f)
        return {}
    subjfs = sorted(set(subjfs), key=lambda s: s.casefold())
    dic = {}
    for subjf in subjfs:
        dic[subjf] = {}
    return dic


class Panes:
    
    def __init__(self):
        self.Active = False
        self.gui = guiPanes()
        self.set_gui()
    
    def dump1(self):
        return self.gui.tree1.dump()
    
    def toggle(self):
        if self.Active:
            self.close()
        else:
            self.show()
    
    def set_gui(self):
        self.set_bindings()
        self.set_title()
    
    def expand_all(self):
        self.gui.expand_all()
    
    def set_target_right(self):
        f = '[MClient] prior_block.controller.Panes.set_target_right'
        items = self.gui.tree2.find(self.gui.tree1.source)
        if not items:
            rep.empty(f)
            return
        self.gui.tree2.target = items[0]
    
    def set_target_left(self):
        f = '[MClient] prior_block.controller.Panes.set_target_left'
        items = self.gui.tree1.find(self.gui.tree2.source)
        if not items:
            rep.empty(f)
            return
        self.gui.tree1.target = items[0]
    
    def set_target_left_single(self):
        f = '[MClient] prior_block.controller.Panes.set_target_left_single'
        items = self.gui.tree1.find(self.gui.tree1.source)
        if not items:
            rep.empty(f)
            return
        self.gui.tree1.target = items[0]
    
    def set_target_right_single(self):
        f = '[MClient] prior_block.controller.Panes.set_target_right_single'
        items = self.gui.tree2.find(self.gui.tree2.source)
        if not items:
            rep.empty(f)
            return
        self.gui.tree2.target = items[0]

    def move2right(self):
        f = '[MClient] prior_block.controller.Panes.move2right'
        mes = _('Move items from left to right')
        Message(f, mes).show_debug()
        self.set_target_right()
        self.gui.tree2._set_item(self.gui.tree2.target, self.gui.tree1.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.tree2.clear_selection()
    
    def move2left(self):
        f = '[MClient] prior_block.controller.Panes.move2left'
        mes = _('Move items from right to left')
        Message(f, mes).show_debug()
        self.set_target_left()
        self.gui.tree1._set_item(self.gui.tree1.target, self.gui.tree2.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.tree1.clear_selection()
    
    def drop_left(self):
        f = '[MClient] prior_block.controller.Panes.drop_left'
        if self.gui.tree2.source and self.gui.tree1.find(self.gui.tree2.source):
            mes = _('Two-pane mode')
            Message(f, mes).show_debug()
            self.move2left()
        else:
            mes = _('Single-pane mode')
            Message(f, mes).show_debug()
            self.set_target_left_single()
            self.gui.tree1._set_item(self.gui.tree1.target, self.gui.tree1.children)
            #self.gui.tree1.clear_selection()
        self.gui.reset_drop()
    
    def drop_right(self):
        f = '[MClient] prior_block.controller.Panes.drop_right'
        if self.gui.tree1.source and self.gui.tree2.find(self.gui.tree1.source):
            mes = _('Two-pane mode')
            Message(f, mes).show_debug()
            self.move2right()
        else:
            mes = _('Single-pane mode')
            Message(f, mes).show_debug()
            self.set_target_right_single()
            self.gui.tree2._set_item(self.gui.tree2.target, self.gui.tree2.children)
            #self.gui.tree2.clear_selection()
        self.gui.reset_drop()
    
    def set_bindings(self):
        self.gui.bind(('Esc',), self.close)
        self.gui.tree1.sig_drop.connect(self.drop_left)
        self.gui.tree2.sig_drop.connect(self.drop_right)
    
    def close(self):
        self.Active = False
        self.gui.close()
    
    def show(self):
        self.Active = True
        self.gui.show()
    
    def fill(self, dic1, dic2):
        f = '[MClient] prior_block.controller.Panes.fill'
        ''' This workaround allows to drag and drop items onto an empty
            widget. Empty input must be allowed (there are no blocked
            subjects by default).
        '''
        if not dic1:
            dic1 = {'': {}}
        if not dic2:
            dic2 = {'': {}}
        self.gui.fill(dic1, dic2)
    
    def set_title(self, title=''):
        if not title:
            title = _('Prioritization')
        self.gui.set_title(title)



class Block(Panes):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_titles()
        self.add_bindings()
        self.reset()
    
    def set_titles(self):
        self.gui.set_title(_('Blocking'))
        self.gui.tree1.set_header(_('Blocked subjects'))
    
    def toggle_use(self):
        self.gui.cbx_pri.toggle()
        self.save()
    
    def save(self):
        CONFIG.new['subjects']['blocked'] = self.dump1()
        CONFIG.new['BlockSubjects'] = self.gui.cbx_pri.get()
        self.gui.load_article()
    
    def add_bindings(self):
        self.gui.btn_res.set_action(self.reset)
        self.gui.btn_apl.set_action(self.apply)
        self.gui.opt_src.set_action(self.reset)
    
    def set_mode(self):
        f = '[MClient] prior_block.controller.Block.set_mode'
        mode = self.gui.opt_src.get()
        if mode == _('All subjects'):
            self.dic2 = PLUGINS.get_subjects()
        elif mode == _('From the article'):
            self.dic2 = get_article_subjects()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, '; '.join(self.gui.opt_src.items))
            Message(f, mes, True).show_error()
            return
        mes = _('Mode: "{}"').format(mode)
        Message(f, mes).show_debug()
    
    def reset(self):
        f = '[MClient] prior_block.controller.Block.reset'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.dic1 = CONFIG.new['subjects']['blocked']
        self.set_mode()
        #TODO: Elaborate
        self.fill(self.dic1, self.dic2)
    
    def apply(self):
        self.close()
        self.save()



class Priorities(Panes):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bindings()
        self.reset()
    
    def toggle_use(self):
        self.gui.cbx_pri.toggle()
        self.save()
    
    def save(self):
        CONFIG.new['subjects']['prioritized'] = self.dump1()
        CONFIG.new['PrioritizeSubjects'] = self.gui.cbx_pri.get()
        self.gui.load_article()
    
    def add_bindings(self):
        self.gui.btn_res.set_action(self.reset)
        self.gui.btn_apl.set_action(self.apply)
        self.gui.opt_src.set_action(self.reset)
    
    def set_mode(self):
        f = '[MClient] prior_block.controller.Priorities.set_mode'
        mode = self.gui.opt_src.get()
        if mode == _('All subjects'):
            self.dic2 = PLUGINS.get_subjects()
        elif mode == _('From the article'):
            self.dic2 = get_article_subjects()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, '; '.join(self.gui.opt_src.items))
            Message(f, mes, True).show_error()
            return
        mes = _('Mode: "{}"').format(mode)
        Message(f, mes).show_debug()
    
    def reset(self):
        f = '[MClient] prior_block.controller.Priorities.reset'
        if not CONFIG.Success:
            rep.cancel(f)
            return
        self.dic1 = CONFIG.new['subjects']['prioritized']
        self.set_mode()
        #TODO: Elaborate
        self.fill(self.dic1, self.dic2)
    
    def apply(self):
        self.close()
        self.save()


BLOCK = Block()
PRIOR = Priorities()
