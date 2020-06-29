#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared.shared as sh
from skl_shared.localize import _

DEFORDER = (_('Noun'),_('Verb'),_('Adjective'),_('Abbreviation')
           ,_('Adverb'),_('Preposition'),_('Pronoun')
           )


class SpeechPrior:
    
    def __init__(self,order=DEFORDER):
        self.reset(order)
    
    def reset(self,order=DEFORDER):
        self.set_values()
        self.order = order
        self.check()
        self.prioritize()
    
    def debug(self):
        f = '[MClient] speech.SpeechPrior.debug'
        if self.Success:
            full = []
            abbr = []
            prior = []
            i = max(self.prior)
            while i > 0:
                prior.append(i)
                index_ = self.prior.index(i)
                abbr.append(self.abbr[index_])
                full.append(self.full[index_])
                i -= 1
            headers = (_('ABBREVIATION'),_('NAME'),_('PRIORITY'))
            iterable = [abbr,full,prior]
            mes = sh.FastTable(iterable,headers).run()
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def prioritize(self):
        f = '[MClient] speech.SpeechPrior.prioritize'
        if self.Success:
            lst = [i + 1 for i in range(len(self.abbr))]
            lst = lst[::-1]
            for i in range(len(self.order)):
                try:
                    ind = self.full.index(self.order[i])
                    self.prior[ind] = lst[i]
                except ValueError:
                    mes = _('Wrong input data: "{}"!')
                    mes = mes.format(self.order[i])
                    sh.objs.get_mes(f,mes,True).show_warning()
            lst = lst[len(self.order):]
            try:
                ind = self.full.index(_('Phrase'))
                self.prior[ind] = 1
                lst = lst[:-1]
            except ValueError:
                pass
            j = 0
            for i in range(len(self.prior)):
                if self.prior[i] == -1:
                    self.prior[i] = lst[j]
                    j += 1
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] speech.SpeechPrior.check'
        if len(self.abbr):
            if len(self.abbr) == len(self.full):
                if len(self.order) > len(self.abbr):
                    self.Success = False
                    sub = '{} <= {}'.format (len(self.order)
                                            ,len(self.abbr)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    sh.objs.get_mes(f,mes).show_error()
            else:
                self.Success = False
                sub = '{} == {}'.format(len(self.abbr),len(self.full))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_error()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def set_values(self):
        self.abbr = [_('abbr.')
                    ,_('adj')
                    ,_('adv.')
                    ,_('art.')
                    ,_('conj.')
                    ,_('form')
                    ,_('interj.')
                    ,_('n')
                    ,_('num.')
                    ,_('ord.num.')
                    ,_('part.')
                    ,_('phrase')
                    ,_('predic.')
                    ,_('prepos.')
                    ,_('pron')
                    ,_('suf')
                    ,_('v')
                    ]
        self.full = [_('Abbreviation')
                    ,_('Adjective')
                    ,_('Adverb')
                    ,_('Article')
                    ,_('Conjunction')
                    ,_('Form')
                    ,_('Interjection')
                    ,_('Noun')
                    ,_('Numeral')
                    ,_('Ordinal Numeral')
                    ,_('Particle')
                    ,_('Phrase')
                    ,_('Predicative')
                    ,_('Preposition')
                    ,_('Pronoun')
                    ,_('Suffix')
                    ,_('Verb')
                    ]
        self.prior = [-1 for i in range(len(self.abbr))]
        self.Success = True


if __name__ == '__main__':
    ispeech = SpeechPrior()
    ispeech.debug()
