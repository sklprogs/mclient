#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

import instance as ic


class Elems:

    def __init__(self, blocks):
        f = '[MClient] plugins.stardict.elems.Elems.__init__'
        self.dicurls = {}
        self.blocks = blocks
        if self.blocks:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)

    def expand_dic(self):
        #TODO (?): implement
        pass
    
    def run(self):
        f = '[MClient] plugins.stardict.elems.Elems.run'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.set_phrases()
        self.delete_straight_line()
        self.run_comments()
        ''' These 2 procedures should not be combined (otherwise, corrections
            will have the same color as comments)
        '''
        self.unite_comments()
        self.set_com_same()
        self.add_space()
        self.fill()
        self.remove_fixed()
        self.insert_fixed()
        self.expand_dic()
        return self.blocks
    
    def debug(self, maxrow=20, maxrows=1000):
        f = '[MClient] plugins.stardict.elems.Elems.debug'
        headers = ('NO','CELLNO', 'SUBJ', 'WFORM', 'SPEECH', 'TRANSC', 'TYPE'
                  ,'TEXT'
                  )
        rows = []
        for i in range(len(self.blocks)):
            rows.append ([i + 1
                         ,self.blocks[i].cellno
                         ,self.blocks[i].subj
                         ,self.blocks[i].wform
                         ,self.blocks[i].speech
                         ,self.blocks[i].transc
                         ,self.blocks[i].type
                         ,self.blocks[i].text
                         ]
                        )
        mes = sh.FastTable (headers = headers
                           ,iterable = rows
                           ,maxrow = maxrow
                           ,maxrows = maxrows
                           ,Transpose = True
                           ).run()
        return f'{f}:\n{mes}'
        
    def unite_comments(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i].type == 'comment' \
            and self.blocks[i-1].cellno == self.blocks[i].cellno:
                if i > 0 and self.blocks[i-1].type == 'comment':
                    self.blocks[i-1].text \
                            = sh.List (lst1 = [self.blocks[i-1].text
                                      ,self.blocks[i].text
                                      ]
                                      ).space_items()
                    del self.blocks[i]
                    i -= 1
            i += 1
            
    def delete_straight_line(self):
        self.blocks = [block for block in self.blocks \
                       if block.text.strip() != '|'
                      ]
    
    def run_comments(self):
        i = 0
        cellno = -1
        while i < len(self.blocks):
            if self.blocks[i].type in ('comment', 'correction'):
                text_str = self.blocks[i].text.strip()
                ''' Delete comments that are just ';' or ',' (we don't need
                    them, we have a table view). We delete instead of
                    assigning Block attribute because we may need to unblock
                    blocked subjects later.
                '''
                if text_str == ';' or text_str == ',':
                    del self.blocks[i]
                    i -= 1
                elif self.blocks[i].cellno == cellno:
                    # For the following cases: "23 фраз в 9 тематиках"
                    if i > 0 and self.blocks[i-1].type == 'phrase':
                        self.blocks[i].cellno = cellno
                    # Move the comment to the preceding cell
                    if text_str.startswith(',') or text_str.startswith(';') \
                    or text_str.startswith('(') or text_str.startswith(')') \
                    or text_str.startswith('|'):
                        self.blocks[i].cellno = cellno
                        # Mark the next block as a start of a new cell
                        if i < len(self.blocks) - 1 and self.blocks[i+1].type \
                        not in ('comment', 'correction'):
                            cellno += 1
                            self.blocks[i+1].cellno = cellno
            i += 1
            
    def set_com_same(self):
        ''' Sometimes sources do not provide sufficient information on
            SAMECELL blocks, and the tag parser cannot handle sequences
            such as 'any type (not same) -> comment (not same) ->
            any type (not same)'.
            Rules:
            1) (Should be always correct)
                'i >= 0 -> correction (not same)
                    =>
                'i >= 0 -> correction (same)
            2) (Preferable)
                'term (not same) -> comment (not same) -> any type
                (not same)'
                    =>
                'term (not same) -> comment (same) -> any type
                (not same)'
            3) (Generally correct before removing fixed columns)
                'dic/wform/speech/transc -> comment (not same) -> term
                (not same)'
                    =>
                'dic/wform/speech/transc -> comment (not same) -> term
                (same)'
            4) (By guess, check only after ##2&3)
                'any type (same) -> comment (not same) -> any type
                (not same)'
                    =>
                'any type (same) -> comment (same) -> any type
                (not same)'
            5) (Always correct)
                'any type -> comment/correction (not same) -> END'
                    =>
                'any type -> comment/correction (same) -> END'
            6) (Do this in the end of the loop + Readability improvement
               ("в 42 тематиках"))
                'any type (not same) -> comment (not same) -> any type
                (not same)'
                    =>
                'any type (not same) -> comment (same) -> any type
                (not same)'
        '''
        if not self.blocks:
            return
        i = 3
        while i < len(self.blocks):
            cond1 = self.blocks[i].type == 'correction'
            cond2 = False
            if self.blocks[i-1].cellno != self.blocks[i].cellno:
                cond2 = True
            cond3 = self.blocks[i-1].type == 'comment' \
                    and self.blocks[i-2].cellno == self.blocks[i-1].cellno
            cond4 = self.blocks[i-2].type == 'term' \
                    and self.blocks[i-3].cellno == self.blocks[i-2].cellno
            cond5 = self.blocks[i-3].cellno == self.blocks[i-2].cellno
            cond6 = self.blocks[i].type == 'term'
            cond7a = self.blocks[i-2].type == 'subj'
            cond7b = self.blocks[i-2].type == 'wform'
            cond7c = self.blocks[i-2].type == 'speech'
            cond7d = self.blocks[i-2].type == 'transc'
            cond7 = cond7a or cond7b or cond7c or cond7d
            # Rule 1
            if cond1 and cond2:
                self.blocks[i].same = 1
            # Rule 2
            elif cond4 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 3
            elif cond7 and cond3 and cond6 and cond2:
                self.blocks[i].same = 1
            # Rule 4:
            elif cond5 and cond3 and cond2:
                self.blocks[i-1].same = 1
            # Rule 6:
            elif cond5 and cond3 and cond2:
                self.blocks[i-1].same = 1
            i += 1
        # Rule 5
        # After exiting the loop, the last block
        i = len(self.blocks) - 1
        cond1 = self.blocks[i].type in ('comment', 'correction')
        cond2 = self.blocks[i-1].cellno == self.blocks[i].cellno
        if cond1 and cond2:
            self.blocks[i].cellno = self.blocks[i-1].cellno
    
    def add_space(self):
        i = 1
        while i < len(self.blocks):
            if self.blocks[i-1].cellno == self.blocks[i].cellno:
                cond = False
                if i > 0:
                    if self.blocks[i-1].text[-1] in ['(', '[', '{']:
                        cond = True
                if self.blocks[i].text \
                  and not self.blocks[i].text[0].isspace() \
                  and not self.blocks[i].text[0] in sh.lg.punc_array \
                  and not self.blocks[i].text[0] in [')', ']', '}'] \
                  and not cond:
                    self.blocks[i].text = ' ' + self.blocks[i].text
            i += 1

    def set_phrases(self):
        for block in self.blocks:
            if block.type == 'phrase':
                block.type = 'subj'
                block.subj = block.text.strip()
                break
                
    def fill(self):
        dic = wform = speech = transc = term = ''
        
        # Find first non-empty values and set them as default
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.text
                break
        for block in self.blocks:
            if block.type == 'wform':
                wform = block.text
                break
        for block in self.blocks:
            if block.type == 'speech':
                speech = block.text
                break
        for block in self.blocks:
            if block.type == 'transc':
                transc = block.text
                break
        for block in self.blocks:
            if block.type == 'term' or block.type == 'phrase':
                term = block.text
                break
        
        for block in self.blocks:
            if block.type == 'subj':
                dic = block.text
            elif block.type == 'wform':
                wform = block.text
            elif block.type == 'speech':
                speech = block.text
            elif block.type == 'transc':
                transc = block.text
                ''' #TODO: Is there a difference if we use both term/phrase
                    here or the term only?
                '''
            elif block.type in ('term', 'phrase'):
                term = block.text
            block.subj = dic.strip()
            block.wform = wform
            block.speech = speech
            block.transc = transc
    
    def insert_fixed(self):
        dic = wform = speech = ''
        i = 0
        while i < len(self.blocks):
            if dic != self.blocks[i].subj \
            or wform != self.blocks[i].wform \
            or speech != self.blocks[i].speech:
                
                block = ic.Block()
                block.type = 'speech'
                block.text = self.blocks[i].speech
                block.subj = self.blocks[i].subj
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'transc'
                block.text = self.blocks[i].transc
                block.subj = self.blocks[i].subj
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)

                block = ic.Block()
                block.type = 'wform'
                block.text = self.blocks[i].wform
                block.subj = self.blocks[i].subj
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                block = ic.Block()
                block.type = 'subj'
                block.text = self.blocks[i].subj
                block.subj = self.blocks[i].subj
                block.wform = self.blocks[i].wform
                block.speech = self.blocks[i].speech
                block.transc = self.blocks[i].transc
                self.blocks.insert(i, block)
                
                dic = self.blocks[i].subj
                wform = self.blocks[i].wform
                speech = self.blocks[i].speech
                i += 4
            i += 1
            
    def remove_fixed(self):
        self.blocks = [block for block in self.blocks if block.type \
                       not in ('subj', 'wform', 'transc', 'speech')
                      ]
