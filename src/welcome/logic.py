#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


COLNUM = 6


class Hotkeys:
    
    def __init__(self):
        self.hotkeys = []
    
    def add(self,desc,bindings):
        self.hotkeys.append((desc,bindings))
    
    def _format_hotkeys(self,text):
        return f'<p align="center" style="font-family: Mono; font-size: 11pt; margin-left: 5px; margin-right: 44px">{text}</p>'
    
    def get(self):
        f = '[MClientQt] welcome.logic.Hotkeys.get'
        if not self.hotkeys:
            sh.com.rep_empty(f)
            return []
        rows = []
        hotkeys = '; '.join(self.hotkeys[0][1])
        hotkeys = self._format_hotkeys(hotkeys)
        row = [self.hotkeys[0][0],hotkeys]
        i = 1
        while i < len(self.hotkeys):
            hotkeys = '; '.join(self.hotkeys[i][1])
            hotkeys = self._format_hotkeys(hotkeys)
            row += [self.hotkeys[i][0],hotkeys]
            if i % COLNUM == 0:
                rows.append(row)
                row = []
            i += 1
        if row:
            row += ['' * COLNUM]
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
        self.table = []
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
    
    def run(self):
        self.set_heading()
        self.set_about()
        self.set_hotkeys()
        self.add_cols()
        return self.table
    
    def set_hotkeys(self):
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
        
        self.table += ihotkeys.get()
    
    def set_about(self):
        sub = [_('This program retrieves translation from online/offline sources.')]
        self.table.append(sub)
        sub = [_('Use an entry area below to enter a word/phrase to be translated.')]
        self.table.append(sub)

    def set_heading(self):
        row = [f'<h2>Welcome to {self.desc}!</h2>']
        self.table.append(row)
    
    def add_cols(self):
        f = '[MClient] logic.Welcome.add_cols'
        for i in range(len(self.table)):
            delta = COLNUM - len(self.table[i])
            if delta > 0:
                for j in range(delta):
                    self.table[i].append('')
