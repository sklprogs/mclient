#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Hotkeys:
    
    def __init__(self):
        self.hotkeys = []
    
    def add(self,desc,bindings):
        self.hotkeys.append((desc,bindings))
    
    def _add_indent(self,text):
        return f'<p align="center" style="margin-left: 15px">{text}</p>'
    
    def get(self):
        f = '[MClientQt] welcome.logic.Hotkeys.get'
        if not self.hotkeys:
            sh.com.rep_empty(f)
            return []
        rows = []
        hotkeys = '; '.join(self.hotkeys[0][1])
        hotkeys = self._add_indent(hotkeys)
        row = [self.hotkeys[0][0],hotkeys,'']
        i = 1
        while i < len(self.hotkeys):
            hotkeys = '; '.join(self.hotkeys[i][1])
            hotkeys = self._add_indent(hotkeys)
            row += [self.hotkeys[i][0],hotkeys,'']
            if i % 6 == 0:
                rows.append(row)
                row = []
            i += 1
        if row:
            row += ['','','','','','','','']
            rows.append(row)
        return rows



class Welcome:

    def __init__ (self,product='MClient'
                 ,version='current'
                 ):
        self.set_values()
        self.product = product
        self.version = version
        self.desc = sh.List (lst1 = [self.product
                                    ,self.version
                                    ]
                            ).space_items()

    def set_values(self):
        self.sources = []
        self.sdstat = 0
        self.mtbstat = 0
        self.lgstat = 0
        self.sdcolor = 'red'
        self.mtbcolor = 'red'
        self.lgcolor = 'red'
        self.product = ''
        self.version = ''
        self.desc = ''
    
    def try_sources(self):
        f = '[MClientQt] welcome.logic.Welcome.try_sources'
        old = objs.get_plugins().source
        if sh.lg.globs['bool']['Ping']:
            dics = objs.plugins.get_online_sources()
            if dics:
                for dic in dics:
                    objs.plugins.set(dic)
                    source = Source()
                    source.title = dic
                    if objs.plugins.is_accessible():
                        source.status = _('running')
                        source.color = 'green'
                    self.sources.append(source)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_lazy(f)
        # Try Stardict
        objs.plugins.set(_('Stardict'))
        self.sdstat = objs.get_plugins().is_accessible()
        if self.sdstat:
            self.sdcolor = 'green'
        # Try local Multitran
        objs.plugins.set(_('Local MT'))
        self.mtbstat = objs.plugins.is_accessible()
        if self.mtbstat:
            self.mtbcolor = 'green'
        # Try DSL
        objs.plugins.set('Lingvo (DSL)')
        self.lgstat = objs.plugins.is_accessible()
        if self.lgstat:
            self.lgcolor = 'green'
        objs.plugins.set(old)

    def gen_source_code(self,title,status,color):
        sub = ' {}'.format(status)
        code = '<b>{}</b><font face="Serif" color="{}" size="6">{}'
        code = code.format(title,color,sub)
        self.istr.write(code)
        code = '</font>.<br>'
        self.istr.write(code)
    
    def gen_hint(self,hint):
        code = '<td align="left" valign="top" col width="200">{}</td>'
        code = code.format(hint)
        self.istr.write(code)
    
    def gen_hotkey(self,hotkey):
        code = '<td align="center" valign="top" col width="100">{}</td>'
        code = code.format(sh.Hotkeys(hotkey).run())
        self.istr.write(code)
    
    def gen_row(self,hint1,hotkey1,hint2,hotkey2):
        self.istr.write('<tr>')
        self.gen_hint(hint1)
        self.gen_hotkey(hotkey1)
        # Suppress useless warnings since the 2nd column may be empty
        if hotkey2:
            self.gen_hint(hint2)
            self.gen_hotkey(hotkey2)
        self.istr.write('</tr>')
    
    def get_hotkeys(self):
        ihotkeys = Hotkeys()
        
        hint = _('Translate the current input or selection')
        hotkeys = (_('Left mouse button'),'Return')
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Copy the current selection')
        hotkeys = (_('Right mouse button'),sh.lg.globs['str']['bind_copy_sel']
                  ,sh.lg.globs['str']['bind_copy_sel_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Show the program window (system-wide)')
        hotkeys = ('Alt+~',)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Translate selection from an external program')
        hotkeys = ('Ctrl+Ins+Ins','Ctrl+C+C')
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Minimize the program window')
        hotkeys = ('Esc',)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Quit the program')
        hotkeys = ('Ctrl+Q',sh.lg.globs['str']['bind_quit'])
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Copy the URL of the selected term')
        hotkeys = (sh.lg.globs['str']['bind_copy_url'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Copy the URL of the current article')
        hotkeys = (sh.lg.globs['str']['bind_copy_article_url'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the previous section of column #{}').format(1)
        hotkeys = (sh.lg.globs['str']['bind_col1_up'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the next section of column #{}').format(1)
        hotkeys = (sh.lg.globs['str']['bind_col1_down'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the previous section of column #{}').format(2)
        hotkeys = (sh.lg.globs['str']['bind_col2_up'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the next section of column #{}').format(2)
        hotkeys = (sh.lg.globs['str']['bind_col2_down'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the previous section of column #{}').format(3)
        hotkeys = (sh.lg.globs['str']['bind_col3_up'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the next section of column #{}').format(3)
        hotkeys = (sh.lg.globs['str']['bind_col3_down'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Open a webpage with a definition of the current term')
        hotkeys = (sh.lg.globs['str']['bind_define'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Look up phrases')
        hotkeys = (sh.lg.globs['str']['bind_go_phrases'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the preceding article')
        hotkeys = (sh.lg.globs['str']['bind_go_back'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Go to the following article')
        hotkeys = (sh.lg.globs['str']['bind_go_forward'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Next source language')
        hotkeys = (sh.lg.globs['str']['bind_next_lang1']
                  ,sh.lg.globs['str']['bind_next_lang1_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Previous source language')
        hotkeys = (sh.lg.globs['str']['bind_prev_lang1']
                  ,sh.lg.globs['str']['bind_prev_lang1_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Create a printer-friendly page')
        hotkeys = (sh.lg.globs['str']['bind_print'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Open the current article in a default browser')
        hotkeys = (sh.lg.globs['str']['bind_open_in_browser']
                  ,sh.lg.globs['str']['bind_open_in_browser_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Reload the current article')
        hotkeys = (sh.lg.globs['str']['bind_reload_article']
                  ,sh.lg.globs['str']['bind_reload_article_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Save or copy the current article')
        hotkeys = (sh.lg.globs['str']['bind_save_article']
                  ,sh.lg.globs['str']['bind_save_article_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Start a new search in the current article')
        hotkeys = (sh.lg.globs['str']['bind_re_search_article'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Search the article forward')
        hotkeys = (sh.lg.globs['str']['bind_search_article_forward'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Search the article backward')
        hotkeys = (sh.lg.globs['str']['bind_search_article_backward'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Show settings')
        hotkeys = (sh.lg.globs['str']['bind_settings']
                  ,sh.lg.globs['str']['bind_settings_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('About the program')
        hotkey = (sh.lg.globs['str']['bind_show_about'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Paste a special symbol')
        hotkeys = (sh.lg.globs['str']['bind_spec_symbol'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle alphabetizing')
        hotkeys = (sh.lg.globs['str']['bind_toggle_alphabet'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle blacklisting')
        hotkeys = (sh.lg.globs['str']['bind_toggle_block'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle History')
        hotkeys = (sh.lg.globs['str']['bind_toggle_history']
                  ,sh.lg.globs['str']['bind_toggle_history_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle prioritizing')
        hotkeys = (sh.lg.globs['str']['bind_toggle_priority'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle terms-only selection')
        hotkeys = (sh.lg.globs['str']['bind_toggle_sel'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Toggle the current article view')
        hotkeys = (sh.lg.globs['str']['bind_toggle_view']
                  ,sh.lg.globs['str']['bind_toggle_view_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Clear History')
        hotkeys = (sh.lg.globs['str']['bind_clear_history'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Next target language')
        hotkeys = (sh.lg.globs['str']['bind_next_lang2']
                  ,sh.lg.globs['str']['bind_next_lang2_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Previous target language')
        hotkeys = (sh.lg.globs['str']['bind_prev_lang2']
                  ,sh.lg.globs['str']['bind_prev_lang2_alt']
                  )
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Swap source and target languages')
        hotkeys = (sh.lg.globs['str']['bind_swap_langs'],)
        ihotkeys.add(hint,hotkeys)
        
        hint = _('Copy the nominative case')
        hotkeys = (sh.lg.globs['str']['bind_copy_nominative'],)
        ihotkeys.add(hint,hotkeys)
        
        return ihotkeys.get()
    
    def generate(self):
        f = '[MClient] logic.Welcome.generate'
        self.istr = io.StringIO()
        sub = _('Welcome to {}!').format(self.desc)
        code = '<html><body><h1>{}</h1><font face="Serif" size="6"><br>'
        code = code.format(sub)
        self.istr.write(code)
        sub = _('This program retrieves translation from online/offline sources.')
        self.istr.write(sub)
        sub = _('Use an entry area below to enter a word/phrase to be translated.')
        code = '<br>{}<br><br>'
        code = code.format(sub)
        self.istr.write(code)
        for source in self.sources:
            self.gen_source_code (title = source.title
                                 ,status = source.status
                                 ,color = source.color
                                 )
        sub1 = _('Offline dictionaries loaded:')
        sub2 = ' Stardict: '
        sub3 = ', Lingvo (DSL): '
        code = '{}{}<font color="{}">{}</font>{}'
        code = code.format(sub1,sub2,self.sdcolor,self.sdstat,sub3)
        self.istr.write(code)
        sub = ', Multitran (Demo): '
        code = '<font color="{}">{}</font>{}<font color="{}'
        code = code.format(self.lgcolor,self.lgstat,sub,self.mtbcolor)
        self.istr.write(code)
        sub1 = _('Main hotkeys')
        sub2 = _('(see documentation for other hotkeys, mouse bindings and functions)')
        code = '">{}</font>{}<br><br><br><br><h1>{}</h1><h2>{}</h2>'
        code = code.format(self.mtbstat,'.',sub1,sub2)
        self.istr.write(code)
        self.set_hotkeys()
        code = '</body></html>'
        self.istr.write(code)
        code = self.istr.getvalue()
        self.istr.close()
        return code

    def run(self):
        '''
        self.try_sources()
        return self.generate()
        '''
        return self.get_hotkeys()
