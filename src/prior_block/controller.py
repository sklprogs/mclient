from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Panes:
    
    def __init__(self):
        self.Active = False
        self.gui = gi.Panes()
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
        f = '[MClientQt] prior_block.controller.Panes.set_target_right'
        items = self.gui.tree2.find(self.gui.tree1.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.tree2.target = items[0]
    
    def set_target_left(self):
        f = '[MClientQt] prior_block.controller.Panes.set_target_left'
        items = self.gui.tree1.find(self.gui.tree2.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.tree1.target = items[0]
    
    def set_target_left_single(self):
        f = '[MClientQt] prior_block.controller.Panes.set_target_left_single'
        items = self.gui.tree1.find(self.gui.tree1.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.tree1.target = items[0]
    
    def set_target_right_single(self):
        f = '[MClientQt] prior_block.controller.Panes.set_target_right_single'
        items = self.gui.tree2.find(self.gui.tree2.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.tree2.target = items[0]

    def move2right(self):
        f = '[MClientQt] prior_block.controller.Panes.move2right'
        mes = _('Move items from left to right')
        sh.objs.get_mes(f, mes, True).show_debug()
        self.set_target_right()
        self.gui.tree2._set_item(self.gui.tree2.target, self.gui.tree1.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.tree2.clear_selection()
    
    def move2left(self):
        f = '[MClientQt] prior_block.controller.Panes.move2left'
        mes = _('Move items from right to left')
        sh.objs.get_mes(f, mes, True).show_debug()
        self.set_target_left()
        self.gui.tree1._set_item(self.gui.tree1.target, self.gui.tree2.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.tree1.clear_selection()
    
    def drop_left(self):
        f = '[MClientQt] prior_block.controller.Panes.drop_left'
        if self.gui.tree2.source and self.gui.tree1.find(self.gui.tree2.source):
            mes = _('Two-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.move2left()
        else:
            mes = _('Single-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.set_target_left_single()
            self.gui.tree1._set_item(self.gui.tree1.target, self.gui.tree1.children)
            #self.gui.tree1.clear_selection()
        self.gui.reset_drop()
    
    def drop_right(self):
        f = '[MClientQt] prior_block.controller.Panes.drop_right'
        if self.gui.tree1.source and self.gui.tree2.find(self.gui.tree1.source):
            mes = _('Two-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.move2right()
        else:
            mes = _('Single-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.set_target_right_single()
            self.gui.tree2._set_item(self.gui.tree2.target, self.gui.tree2.children)
            #self.gui.tree2.clear_selection()
        self.gui.reset_drop()
    
    def set_bindings(self):
        self.gui.bind('Escape', self.close)
        self.gui.tree1.sig_drop.connect(self.drop_left)
        self.gui.tree2.sig_drop.connect(self.drop_right)
    
    def close(self):
        self.Active = False
        self.gui.close()
    
    def show(self):
        self.Active = True
        self.gui.show()
    
    def fill(self, dic1, dic2):
        f = '[MClientQt] prior_block.controller.Panes.fill'
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


if __name__ == '__main__':
    dic1 = {'LeftRoot':
               {'LeftLevel1':
                   {'LeftLevel1_item1': {}
                   ,'LeftLevel1_item2': {}
                   ,'LeftLevel1_item3': {}
                   }
               ,'LeftLevel2':
                   {'LeftLevel2_SubLevel1':
                       {'LeftLevel2_SubLevel1_item1': {}
                       ,'LeftLevel2_SubLevel1_item2': {}
                       ,'LeftLevel2_SubLevel1_item3': {}
                       }
                   ,'LeftLevel2_SubLevel2':
                       {'LeftLevel2_SubLevel2_item1': {}
                       ,'LeftLevel2_SubLevel2_item2': {}
                       ,'LeftLevel2_SubLevel2_item3': {}
                       }
                   }
               ,'LeftLevel3':
                   {'LeftLevel3_item1': {}
                   ,'LeftLevel3_item2': {}
                   ,'LeftLevel3_item3': {}
                   }
               }
           }
    dic2 = {'RightRoot':
               {'RightLevel1':
                   {'RightLevel1_item1': {}
                   ,'RightLevel1_item2': {}
                   ,'RightLevel1_item3': {}
                   }
               ,'RightLevel2':
                   {'RightLevel2_SubLevel1':
                       {'RightLevel2_SubLevel1_item1': {}
                       ,'RightLevel2_SubLevel1_item2': {}
                       ,'RightLevel2_SubLevel1_item3': {}
                       }
                   ,'RightLevel2_SubLevel2':
                       {'RightLevel2_SubLevel2_item1': {}
                       ,'RightLevel2_SubLevel2_item2': {}
                       ,'RightLevel2_SubLevel2_item3': {}
                       }
                   }
               ,'RightLevel3':
                   {'RightLevel3_item1': {}
                   ,'RightLevel3_item2': {}
                   ,'RightLevel3_item3': {}
                   }
               }
           }
    
    sh.com.start()
    panes = Panes()
    panes.fill(dic1, dic2)
    # For some reason, this does not work when run within Panes
    panes.expand_all()
    panes.show()
    sh.com.end()
