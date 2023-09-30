from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

from . import gui as gi


class Panes:
    
    def __init__(self):
        self.Active = False
        self.gui = gi.Panes()
        self.set_gui()
    
    def toggle(self):
        if self.Active:
            self.Active = False
            self.close()
        else:
            self.Active = True
            self.show()
    
    def set_gui(self):
        self.set_bindings()
        self.set_title()
    
    def expand_all(self):
        self.gui.expand_all()
    
    def set_target_right(self):
        f = '[Trees] controller.Panes.set_target_right'
        items = self.gui.trw_rht.find(self.gui.trw_lft.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.trw_rht.target = items[0]
    
    def set_target_left(self):
        f = '[Trees] controller.Panes.set_target_left'
        items = self.gui.trw_lft.find(self.gui.trw_rht.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.trw_lft.target = items[0]
    
    def set_target_left_single(self):
        f = '[Trees] controller.Panes.set_target_left_single'
        items = self.gui.trw_lft.find(self.gui.trw_lft.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.trw_lft.target = items[0]
    
    def set_target_right_single(self):
        f = '[Trees] controller.Panes.set_target_right_single'
        items = self.gui.trw_rht.find(self.gui.trw_rht.source)
        if not items:
            sh.com.rep_empty(f)
            return
        self.gui.trw_rht.target = items[0]

    def move2right(self):
        f = '[Trees] controller.Panes.move2right'
        mes = _('Move items from left to right')
        sh.objs.get_mes(f, mes, True).show_debug()
        self.set_target_right()
        self.gui.trw_rht._set_item(self.gui.trw_rht.target, self.gui.trw_lft.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.trw_rht.clear_selection()
    
    def move2left(self):
        f = '[Trees] controller.Panes.move2left'
        mes = _('Move items from right to left')
        sh.objs.get_mes(f, mes, True).show_debug()
        self.set_target_left()
        self.gui.trw_lft._set_item(self.gui.trw_lft.target, self.gui.trw_rht.children)
        ''' Wrong order of this procedure or clearing both panes may break
            deleting the source item.
        '''
        self.gui.trw_lft.clear_selection()
    
    def drop_left(self):
        f = '[Trees] controller.Panes.drop_left'
        if self.gui.trw_rht.source and self.gui.trw_lft.find(self.gui.trw_rht.source):
            mes = _('Two-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.move2left()
        else:
            mes = _('Single-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.set_target_left_single()
            self.gui.trw_lft._set_item(self.gui.trw_lft.target, self.gui.trw_lft.children)
            #self.gui.trw_lft.clear_selection()
        self.gui.reset_drop()
    
    def drop_right(self):
        f = '[Trees] controller.Panes.drop_right'
        if self.gui.trw_lft.source and self.gui.trw_rht.find(self.gui.trw_lft.source):
            mes = _('Two-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.move2right()
        else:
            mes = _('Single-pane mode')
            sh.objs.get_mes(f, mes, True).show_debug()
            self.set_target_right_single()
            self.gui.trw_rht._set_item(self.gui.trw_rht.target, self.gui.trw_rht.children)
            #self.gui.trw_rht.clear_selection()
        self.gui.reset_drop()
    
    def set_bindings(self):
        self.gui.bind('Escape', self.close)
        self.gui.trw_lft.sig_drop.connect(self.drop_left)
        self.gui.trw_rht.sig_drop.connect(self.drop_right)
    
    def close(self):
        self.gui.close()
    
    def show(self):
        self.gui.show()
    
    def fill(self, dic1, dic2):
        f = '[Trees] controller.Panes.fill'
        if not dic1 or not dic2:
            sh.com.rep_empty(f)
            return
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