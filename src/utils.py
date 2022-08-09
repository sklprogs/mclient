#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sqlite3

from skl_shared.localize import _
import skl_shared.shared as sh

import mkhtml as mh


class Subjects:
    
    def compile(self):
        import plugins.multitrancom.utils.subjects.compile as us
        us.Compile(1).run()
    
    def check(self):
        import plugins.multitrancom.utils.subjects.check as us
        us.Check().run()
    
    def run_missing(self):
        import plugins.multitrancom.utils.subjects.compile as us
        us.Missing(1).run()



class FontsDB:
    
    def __init__(self):
        self.db = sqlite3.connect('/home/pete/tmp/set.db')
        self.dbc = self.db.cursor()
        self.create_fonts()
    
    def create_fonts(self):
        # 9 columns for now
        query = 'create table if not exists FONTS (       \
                 NO     integer primary key autoincrement \
                ,ROWNO  integer                           \
                ,COLNO  integer                           \
                ,TEXT   text                              \
                ,COLOR  text                              \
                ,FAMILY text                              \
                ,SIZE   integer                           \
                ,BOLD   boolean                           \
                ,ITALIC boolean                           \
                                                  )'
        self.dbc.execute(query)
    
    def fill(self,data):
        query = 'insert into FONTS values (?,?,?,?,?,?,?,?,?)'
        self.dbc.execute(query,data)
    
    def save(self):
        self.db.commit()
    
    def close(self):
        self.dbc.close()



class Fonts(mh.Fonts):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def export(self):
        f = '[MClient] utils.Fonts.export'
        ''' Non-silent so as to be sure that the procedure runs only once and
            we get final results.
        '''
        if not self.Success:
            sh.com.cancel(f)
            return
        mes = _('Export Fonts to DB')
        sh.objs.get_mes(f,mes).show_info()
        for i in range(len(self.fonts)):
            ifont = self.fonts[i]
            row = (i + 1,ifont.rowno,ifont.colno,ifont.text,ifont.color
                  ,ifont.family,ifont.size,ifont.Bold,ifont.Italic
                  )
            objs.get_db().fill(row)
        objs.get_db().save()
        objs.db.close()
    
    def run(self):
        self.check()
        self.fill()
        self.set_column_width()
        self.debug()
        self.export()
        return self.fonts



class Objects:
    
    def __init__(self):
        self.db = None
    
    def get_db(self):
        if self.db is None:
            self.db = FontsDB()
        return self.db



class Commands:
    
    def export_fonts(self):
        f = '[MClient] utils.Commands.export_fonts'
        import plugins.multitrancom.run as mc
        import mclient
        import logic as lg
        mh.Fonts = Fonts
        lg.objs.get_plugins(Debug=False,maxrows=1000)
        lg.objs.get_default('MClient')
        if lg.objs.default.Success:
            mclient.objs.get_webframe().reset()
            mclient.objs.webframe.show()
            lg.objs.plugins.quit()
        else:
            mes = _('Unable to continue due to an invalid configuration.')
            sh.objs.get_mes(f,mes).show_warning()
        lg.objs.get_order().save()
        lg.com.save_config()
        mes = _('Goodbye!')
        sh.objs.get_mes(f,mes,True).show_debug()
        


com = Commands()
objs = Objects()


if __name__ == '__main__':
    f = '[MClient] utils.__main__'
    sh.com.start()
    com.export_fonts()
    sh.com.end()
                
