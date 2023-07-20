#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import config as cf


COLNUM = 6


class Hotkeys:
    
    def __init__(self):
        self.hotkeys = []
    
    def add(self, desc, bindings):
        self.hotkeys.append((desc, bindings))
    
    def _format_desc(self, text):
        return f'<p style="font-family: Sans; font-size: 12pt">{text}</p>'
    
    def _format_hotkeys(self, text):
        return f'<p align="center" style="font-family: Mono; font-size: 11pt; margin-left: 5px; margin-right: 44px">{text}</p>'
    
    def get(self):
        f = '[MClientQt] welcome.logic.Hotkeys.get'
        if not self.hotkeys:
            sh.com.rep_empty(f)
            return []
        rows = []
        hotkeys = '; '.join(self.hotkeys[0][1])
        hotkeys = self._format_hotkeys(hotkeys)
        desc = self._format_desc(self.hotkeys[0][0])
        row = [desc, hotkeys]
        i = 1
        while i < len(self.hotkeys):
            hotkeys = '; '.join(self.hotkeys[i][1])
            hotkeys = self._format_hotkeys(hotkeys)
            desc = self._format_desc(self.hotkeys[i][0])
            row += [desc, hotkeys]
            if i % COLNUM == 0:
                rows.append(row)
                row = []
            i += 1
        if row:
            row += ['' * COLNUM]
            rows.append(row)
        return rows



class Welcome:

    def __init__ (self):
        self.table = []
        self.desc = 'Product Current Version'
    
    def set_head(self):
        self.set_heading()
        self.table.append([''])
        self.set_about()
        self.table.append([''])
    
    def set_tail(self):
        self.table.append([''])
        sub = f'<h2>{_("Main hotkeys")}</h2>'
        self.table.append([sub])
        sub = _('(see documentation for other hotkeys, mouse bindings and functions)')
        sub = f'<h3>{sub}</h3>'
        self.table.append([sub])
        self.set_hotkeys()
        self.add_cols()
    
    def run(self):
        # This function is called only during standalone tests
        self.set_heading()
        self.set_about()
        self.set_hotkeys()
        self.add_cols()
        return self.table
    
    def set_hotkeys(self):
        cf.objs.get_config()
        ihotkeys = Hotkeys()
        
        ihotkeys.add (_('Translate the current input or selection')
                     ,(_('Left mouse button'), 'Return')
                     )
        
        ihotkeys.add (_('Copy the current selection')
                     ,[_('Right mouse button')] + cf.objs.config.new['hotkeys']['copy_sel']
                     )
        
        ihotkeys.add(_('Show the program window (system-wide)'), ('Alt+~',))
        
        ihotkeys.add (_('Translate selection from an external program')
                     ,('Ctrl+Ins+Ins', 'Ctrl+C+C')
                     )
        
        ihotkeys.add(_('Minimize the program window'), ('Esc',))
        
        ihotkeys.add (_('Quit the program')
                     ,['Ctrl+Q'] + cf.objs.config.new['hotkeys']['quit']
                     )
        
        ihotkeys.add (_('Copy the URL of the selected term')
                     ,cf.objs.config.new['hotkeys']['copy_url']
                     )
        
        ihotkeys.add (_('Copy the URL of the current article')
                     ,cf.objs.config.new['hotkeys']['copy_article_url']
                     )
        
        ihotkeys.add (_('Go to the previous section of column #{}').format(1)
                     ,cf.objs.config.new['hotkeys']['col1_up']
                     )
        
        ihotkeys.add (_('Go to the next section of column #{}').format(1)
                     ,cf.objs.config.new['hotkeys']['col1_down']
                     )
        
        ihotkeys.add (_('Go to the previous section of column #{}').format(2)
                     ,cf.objs.config.new['hotkeys']['col2_up']
                     )
        
        ihotkeys.add (_('Go to the next section of column #{}').format(2)
                     ,cf.objs.config.new['hotkeys']['col2_down']
                     )
        
        ihotkeys.add (_('Go to the previous section of column #{}').format(3)
                     ,cf.objs.config.new['hotkeys']['col3_up']
                     )
        
        ihotkeys.add (_('Go to the next section of column #{}').format(3)
                     ,cf.objs.config.new['hotkeys']['col3_down']
                     )
        
        ihotkeys.add (_('Open a webpage with a definition of the current term')
                     ,cf.objs.config.new['hotkeys']['define']
                     )
        
        ihotkeys.add (_('Look up phrases')
                     ,cf.objs.config.new['hotkeys']['go_phrases']
                     )
        
        ihotkeys.add (_('Go to the preceding article')
                     ,cf.objs.config.new['hotkeys']['go_back']
                     )
        
        ihotkeys.add (_('Go to the following article')
                     ,cf.objs.config.new['hotkeys']['go_next']
                     )
        
        ihotkeys.add (_('Next source language')
                     ,cf.objs.config.new['hotkeys']['next_lang1']
                     )
        
        ihotkeys.add (_('Previous source language')
                     ,cf.objs.config.new['hotkeys']['prev_lang1']
                     )
        
        ihotkeys.add (_('Create a printer-friendly page')
                     ,cf.objs.config.new['hotkeys']['print']
                     )
        
        ihotkeys.add (_('Open the current article in a default browser')
                     ,cf.objs.config.new['hotkeys']['open_in_browser']
                     )
        
        ihotkeys.add (_('Reload the current article')
                     ,cf.objs.config.new['hotkeys']['reload_article']
                     )
        
        ihotkeys.add (_('Save or copy the current article')
                     ,cf.objs.config.new['hotkeys']['save_article']
                     )
        
        ihotkeys.add (_('Start a new search in the current article')
                     ,cf.objs.config.new['hotkeys']['re_search_article']
                     )
        
        ihotkeys.add (_('Search the article forward')
                     ,cf.objs.config.new['hotkeys']['search_article_forward']
                     )
        
        ihotkeys.add (_('Search the article backward')
                     ,cf.objs.config.new['hotkeys']['search_article_backward']
                     )
        
        ihotkeys.add (_('Show settings')
                     ,cf.objs.config.new['hotkeys']['settings']
                     )
        
        ihotkeys.add (_('About the program')
                     ,cf.objs.config.new['hotkeys']['show_about']
                     )
        
        ihotkeys.add (_('Paste a special symbol')
                     ,cf.objs.config.new['hotkeys']['spec_symbol']
                     )
        
        ihotkeys.add (_('Toggle alphabetizing')
                     ,cf.objs.config.new['hotkeys']['toggle_alphabet']
                     )
        
        ihotkeys.add (_('Toggle blacklisting')
                     ,cf.objs.config.new['hotkeys']['toggle_block']
                     )
        
        ihotkeys.add (_('Toggle History')
                     ,cf.objs.config.new['hotkeys']['toggle_history']
                     )
        
        ihotkeys.add (_('Toggle prioritizing')
                     ,cf.objs.config.new['hotkeys']['toggle_priority']
                     )
        
        ihotkeys.add (_('Clear History')
                     ,cf.objs.config.new['hotkeys']['clear_history']
                     )
        
        ihotkeys.add (_('Next target language')
                     ,cf.objs.config.new['hotkeys']['next_lang2']
                     )
        
        ihotkeys.add (_('Previous target language')
                     ,cf.objs.config.new['hotkeys']['prev_lang2']
                     )
        
        ihotkeys.add (_('Swap source and target languages')
                     ,cf.objs.config.new['hotkeys']['swap_langs']
                     )
        
        ihotkeys.add (_('Copy the nominative case')
                     ,cf.objs.config.new['hotkeys']['copy_nominative']
                     )
        
        ihotkeys.add (_('Show full cell text')
                     ,cf.objs.config.new['hotkeys']['toggle_popup']
                     )
        
        self.table += ihotkeys.get()
    
    def set_font(self, text):
        return f'<p style="font-family: Sans; font-size: 14pt">{text}</p>'
    
    def set_about(self):
        sub = _('This program retrieves translation from online/offline sources.')
        sub = self.set_font(sub)
        self.table.append([sub])
        sub = _('Use an entry area below to enter a word/phrase to be translated.')
        sub = self.set_font(sub)
        self.table.append([sub])

    def set_heading(self):
        mes = _('Welcome to {}!').format(self.desc)
        mes = f'<h1>{mes}</h1>'
        self.table.append([mes])
    
    def add_cols(self):
        for i in range(len(self.table)):
            delta = COLNUM - len(self.table[i])
            if delta > 0:
                for j in range(delta):
                    self.table[i].append('')
