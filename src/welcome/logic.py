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
        f = '[MClient] welcome.logic.Hotkeys.get'
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
    
    def _add_hotkeys(self, key):
        self.ihotkeys.add (cf.objs.config.new['actions'][key]['hint']
                          ,cf.objs.config.new['actions'][key]['hotkeys']
                          )
    
    def set_hotkeys(self):
        cf.objs.get_config()
        self.ihotkeys = Hotkeys()
        
        self.ihotkeys.add (_('Translate the current input or selection')
                          ,(_('Left mouse button'), 'Return')
                          )
        
        self.ihotkeys.add (cf.objs.config.new['actions']['copy_sel']['hint']
                          ,[_('Right mouse button')] + cf.objs.config.new['actions']['copy_sel']['hotkeys']
                          )
        
        self.ihotkeys.add(_('Show the program window (system-wide)'), ('Alt+~',))
        
        self.ihotkeys.add (_('Translate selection from an external program')
                          ,('Ctrl+Ins+Ins', 'Ctrl+C+C')
                          )
        
        self.ihotkeys.add(_('Minimize the program window'), ('Esc',))
        
        self.ihotkeys.add (cf.objs.config.new['actions']['quit']['hint']
                          ,['Ctrl+Q'] + cf.objs.config.new['actions']['quit']['hotkeys']
                          )
        
        self._add_hotkeys('copy_url')
        self._add_hotkeys('copy_article_url')
        self._add_hotkeys('col1_up')
        self._add_hotkeys('col1_down')
        self._add_hotkeys('col2_up')
        self._add_hotkeys('col2_down')
        self._add_hotkeys('col3_up')
        self._add_hotkeys('col3_down')
        self._add_hotkeys('define')
        self._add_hotkeys('go_phrases')
        self._add_hotkeys('go_back')
        self._add_hotkeys('go_next')
        self._add_hotkeys('next_lang1')
        self._add_hotkeys('prev_lang1')
        self._add_hotkeys('print')
        self._add_hotkeys('open_in_browser')
        self._add_hotkeys('reload_article')
        self._add_hotkeys('save_article')
        self._add_hotkeys('re_search_article')
        self._add_hotkeys('search_article_forward')
        self._add_hotkeys('search_article_backward')
        self._add_hotkeys('toggle_settings')
        self._add_hotkeys('toggle_about')
        self._add_hotkeys('toggle_spec_symbols')
        self._add_hotkeys('toggle_alphabet')
        self._add_hotkeys('toggle_block')
        self._add_hotkeys('toggle_history')
        self._add_hotkeys('toggle_priority')
        self._add_hotkeys('clear_history')
        self._add_hotkeys('next_lang2')
        self._add_hotkeys('prev_lang2')
        self._add_hotkeys('swap_langs')
        self._add_hotkeys('copy_nominative')
        self._add_hotkeys('toggle_popup')
        
        self.table += self.ihotkeys.get()
    
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
