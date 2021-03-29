#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import gui as gi


class Settings(gi.Settings):
    
    def __init__(self):
        super().__init__()
        self.mes = []
        self.section = ''
    
    def debug(self):
        f = '[MClient] debug_gui.Settings.debug'
        self.add_widgets()
        mes = '\n'.join(self.mes)
        mes = mes.strip()
        sh.com.run_fast_debug(f,mes)
    
    def get_section(self,name):
        if name.startswith('lbl'):
            return _('Labels')
        elif name.startswith('cbx'):
            return _('Checkboxes')
        elif name.startswith('opt'):
            return _('Option menus')
        elif name.startswith('btn'):
            return _('Buttons')
        else:
            return _('UNKNOWN')
    
    def add_section(self,name):
        section = self.get_section(name)
        if section != self.section:
            self.mes.append('')
            self.mes.append('[{}]'.format(section))
            self.section = section
    
    def add_widget(self,name,value):
        self.add_section(name)
        self.mes.append('{}: {}'.format(name,value))
    
    def add_widgets(self):
        self.add_widget('lbl_no1',self.lbl_no1.text)
        self.add_widget('lbl_no2',self.lbl_no2.text)
        self.add_widget('lbl_no3',self.lbl_no3.text)
        self.add_widget('lbl_no4',self.lbl_no4.text)
        self.add_widget('lbl_no5',self.lbl_no5.text)
        self.add_widget('lbl_no6',self.lbl_no6.text)
        self.add_widget('lbl_no7',self.lbl_no7.text)
        self.add_widget('lbl_no8',self.lbl_no8.text)
        self.add_widget('lbl_no9',self.lbl_no9.text)
        self.add_widget('lbl_no10',self.lbl_no10.text)
        self.add_widget('lbl_no11',self.lbl_no11.text)
        self.add_widget('lbl_no12',self.lbl_no12.text)
        self.add_widget('lbl_no13',self.lbl_no13.text)
        self.add_widget('cbx_no1',self.cbx_no1.get())
        self.add_widget('cbx_no2',self.cbx_no2.get())
        self.add_widget('cbx_no3',self.cbx_no3.get())
        self.add_widget('cbx_no4',self.cbx_no4.get())
        self.add_widget('cbx_no5',self.cbx_no5.get())
        self.add_widget('cbx_no6',self.cbx_no6.get())
        self.add_widget('cbx_no7',self.cbx_no7.get())
        self.add_widget('cbx_no8',self.cbx_no8.get())
        self.add_widget('cbx_no9',self.cbx_no9.get())
        self.add_widget('cbx_no10',self.cbx_no10.get())
        self.add_widget('cbx_no11',self.cbx_no11.get())
        self.add_widget('cbx_no12',self.cbx_no12.get())
        self.add_widget('cbx_no13',self.cbx_no13.get())
        self.add_widget('opt_scm',self.opt_scm.choice)
        self.add_widget('opt_cl1',self.opt_cl1.choice)
        self.add_widget('opt_cl2',self.opt_cl2.choice)
        self.add_widget('opt_cl3',self.opt_cl3.choice)
        self.add_widget('opt_cl4',self.opt_cl4.choice)
        self.add_widget('opt_sp1',self.opt_sp1.choice)
        self.add_widget('opt_sp2',self.opt_sp2.choice)
        self.add_widget('opt_sp3',self.opt_sp3.choice)
        self.add_widget('opt_sp4',self.opt_sp4.choice)
        self.add_widget('opt_sp5',self.opt_sp5.choice)
        self.add_widget('opt_sp6',self.opt_sp6.choice)
        self.add_widget('opt_sp7',self.opt_sp7.choice)


if __name__ == '__main__':
    iset = Settings()
    iset.close()
    iset.debug()
