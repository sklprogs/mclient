#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.progress_bar.controller import PROGRESS
from skl_shared.time import Timer
from skl_shared.logic import com as shcom

from plugins.dsl.cleanup import CleanUp
from plugins.dsl.get import ALL_DICS
from plugins.dsl.tags import Tags
from plugins.dsl.elems import Elems


class Parser:
    
    def __init__(self, idic):
        self.idic = idic
        self.Success = self.idic.Success
        self.cells = []
    
    def set_articles(self):
        f = '[MClient] converters.dsl.shared.Parser.set_articles'
        if not self.Success:
            rep.cancel(f)
            return
        self.idic.set_articles()
        # Reclaim memory
        self.idic.lst = []
        self.idic.poses = []
        self.idic.index_ = []
        self.Success = self.idic.Success and self.idic.articles
    
    def _add_wform(self, article):
        f = '[MClient] converters.dsl.shared.Parser._add_wform'
        if not article:
            rep.empty(f)
            return
        article = article.splitlines()
        article[0] = '[wform]' + article[0] + '[/wform]'
        return '\n'.join(article)
    
    def set_cells(self):
        f = '[MClient] converters.dsl.shared.Parser.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        for article in self.idic.articles:
            blocks = []
            article = self._add_wform(article)
            code = CleanUp(article).run()
            blocks += Tags(code).run()
            if not blocks:
                rep.empty(f)
                continue
            ''' When exporting to Odict XML, we do not care about cell or row
                numbers, so we do not need plugins.fora.run.Plugin._join_cells.
            '''
            self.cells += Elems(blocks).run()
        # Reclaim memory
        self.idic.articles = []
        if not self.cells:
            self.Success = False
            rep.empty_output(f)
            return
    
    def run(self):
        # We do not want millions of debug messages
        ms.STOP = True
        self.set_articles()
        self.set_cells()
        ms.STOP = False
        return self.cells



class Runner:
    
    def __init__(self):
        self.cells = []
        self.Success = ALL_DICS.Success

    def set_cells(self):
        f = '[MClient] converters.dsl.shared.Runner.set_cells'
        if not self.Success:
            rep.cancel(f)
            return
        PROGRESS.set_title(_('DSL Dictionary Converter'))
        PROGRESS.show()
        PROGRESS.set_value(0)
        PROGRESS.set_max(len(ALL_DICS.dics))
        for i in range(len(ALL_DICS.dics)):
            PROGRESS.update()
            mes = _('Process {} ({}/{})')
            mes = mes.format(ALL_DICS.dics[i].fname, i + 1, len(ALL_DICS.dics))
            PROGRESS.set_info(mes)
            iparse = Parser(ALL_DICS.dics[i])
            self.cells += iparse.run()
            self.Success = iparse.Success
            if not self.Success:
                break
            PROGRESS.inc()
        PROGRESS.close()
        self.cells = [cell for cell in self.cells if cell]
        mes = _('Cells have been created')
        Message(f, mes).show_info()
    
    def run(self):
        f = '[MClient] converters.dsl.shared.Runner.run'
        timer = Timer(f)
        timer.start()
        self.set_cells()
        sub = shcom.get_human_time(timer.end())
        mes = _('The operation has taken {}.').format(sub)
        Message(f, mes, True).show_info()
