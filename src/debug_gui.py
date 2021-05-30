#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _
import gui as mg

PRODUCT = mg.PRODUCT
VERSION = mg.VERSION
CURYEAR = mg.CURYEAR
ICON = mg.ICON


class About(mg.About):

    def __init__(self):
        super().__init__()



class History(mg.History):

    def __init__(self):
        super().__init__()



class SaveArticle(mg.SaveArticle):

    def __init__(self):
        super().__init__()



class SearchArticle(mg.SearchArticle):

    def __init__(self):
        super().__init__()



class Sources(mg.Sources):

    def __init__(self):
        super().__init__()



class Suggest(mg.Suggest):

    def __init__(self):
        super().__init__()



class ThirdParties(mg.ThirdParties):

    def __init__(self):
        super().__init__()



class Debug:
    
    def init_debug(self):
        self.mes = []
        self.section = ''
    
    def get_section(self,name):
        if name.startswith('lbl'):
            return _('Labels')
        elif name.startswith('cbx'):
            return _('Checkboxes')
        elif name.startswith('opt'):
            return _('Option menus')
        elif name.startswith('btn'):
            return _('Buttons')
        elif name.startswith('ent'):
            return _('Entries')
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



class Settings(mg.Settings,Debug):
    
    def __init__(self):
        super(Settings,self).__init__()
        self.init_debug()
    
    def debug(self):
        f = '[MClient] debug_gui.Settings.debug'
        self.mes = []
        self.add_widgets()
        mes = '\n'.join(self.mes)
        mes = '{}:\n'.format(f) + mes.strip()
        self.close()
        return mes
    
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



class WebFrame(mg.WebFrame,Debug):
    
    def __init__(self):
        super(WebFrame,self).__init__()
        self.init_debug()
    
    def debug(self):
        f = '[MClient] debug_gui.WebFrame.debug'
        self.mes = []
        self.add_widgets()
        mes = '\n'.join(self.mes)
        mes = '{}:\n'.format(f) + mes.strip()
        return mes
    
    def add_widgets(self):
        self.add_widget('ent_src',self.ent_src.get())
        self.add_widget('opt_src',self.opt_src.choice)
        self.add_widget('opt_lg1',self.opt_lg1.choice)
        self.add_widget('opt_lg2',self.opt_lg2.choice)
        self.add_widget('opt_col',self.opt_col.choice)
        self.add_widget('btn_alp',self.btn_alp.Status)
        self.add_widget('btn_blk',self.btn_blk.Status)
        self.add_widget('btn_cap',self.btn_cap.Status)
        self.add_widget('btn_grp',self.btn_grp.Status)
        self.add_widget('btn_pri',self.btn_pri.Status)



if __name__ == '__main__':
    iset = Settings()
    iset.close()
    iset.debug()
    iweb = WebFrame()
    iweb.close()
    iweb.debug()
