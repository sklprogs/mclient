#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.time import Timer
from skl_shared.logic import com as shcom
from skl_shared.list import List

from sources.dsl.cleanup import CleanUp
from sources.dsl.get import ALL_DICS
from sources.dsl.tags import Tags
from sources.dsl.elems import Elems
from cells import Elems as cElems

from converters.mdic_shared import Runner as mdRunner, Index as mdIndex
from converters.mdic_shared import Portion as mdPortion


class Portion(mdPortion):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
    def set_blocks(self):
        f = '[MClient] converters.dsl.mdic.Portion.set_blocks'
        if not self.Success:
            rep.cancel(f)
            return
        # We do not want millions of debug messages
        ms.STOP = True
        for article in self.articles:
            code = CleanUp(article).run()
            blocks = Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            blocks = Elems(blocks).run()
            blocks = cElems(blocks).run()
            if blocks:
                self.blocks.append(blocks)
        ms.STOP = False
        if not self.blocks:
            self.Success = False
            rep.empty_output(f)
            return
    
    def run(self):
        self.set_blocks()
        self.set_json()
        self.set_sources()
        self.dump_json()
        self.set_wforms()
        self.set_fragms()
        self.set_body()
        self.save_body()
        self.free_memory()
        # We return tuple in order not to keep in memory this class
        return(self.Success, self.pos)



class Runner(mdRunner):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Success = self.Success and ALL_DICS.Success
    
    def loop_sources(self):
        f = '[MClient] converters.dsl.mdic.Runner.loop_sources'
        if not self.Success:
            rep.cancel(f)
            return
        if self.feed_limit <= 0:
            self.Success = False
            mes = f'{self.feed_limit} > 0'
            rep.condition(f, mes)
            return
        PROGRESS.set_value(0)
        ''' We cannot set the number of articles here since they are
            not processed yet.
        '''
        PROGRESS.set_max(len(ALL_DICS.dics))
        PROGRESS.set_title(_('Process articles'))
        PROGRESS.show()
        pos = 0
        for idic in ALL_DICS.dics:
            idic.run()
            idic.set_articles()
            self.Success = idic.Success
            if not self.Success:
                return
            for articles in List(idic.articles).split_by_len(self.feed_limit):
                mes = _('Dictionary: {}\nArticles processed in total: {}')
                mes = mes.format(idic.fname, self.count)
                PROGRESS.set_info(mes, 69)
                PROGRESS.update()
                self.count += len(articles)
                iportion = Portion(articles, idic.dicname, pos)
                self.Success, pos = iportion.run()
                self.unknown_wforms += iportion.unknown_wforms
                # Free memory
                iportion = None
                if not self.Success:
                    return
            PROGRESS.inc()
            PROGRESS.update()
            idic.free_memory()
        PROGRESS.close()
    
    def report(self, interval):
        f = '[MClient] converters.dsl.mdic.Runner.report'
        interval = shcom.get_human_time(interval)
        if not self.Success:
            mes = _('The operation has failed! Time wasted: {}')
            mes = mes.format(interval)
            Message(f, mes, True).show_error()
            return
        len_ = shcom.set_figure_commas(len(ALL_DICS.dics))
        count = shcom.set_figure_commas(self.count)
        mes = []
        sub = _('Processed in total: dictionaries: {}; articles: {}')
        sub = sub.format(len_, count)
        mes.append(sub)
        sub = _('The operation has taken {}.').format(interval)
        mes.append(sub)
        mes = '\n'.join(mes)
        Message(f, mes, True).show_info()
        if self.unknown_wforms:
            mes = _('Number of articles having no word forms: {}')
            mes = mes.format(self.unknown_wforms)
            Message(f, mes).show_warning()
    
    def run(self):
        f = '[MClient] converters.dsl.mdic.Runner.run'
        timer = Timer(f)
        timer.start()
        self.loop_sources()
        self.Success = self.Success and mdIndex().run()
        self.report(timer.end())