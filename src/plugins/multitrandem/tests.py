#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import struct
from skl_shared.localize import _
import skl_shared.message.controller as ms
from skl_shared.message.controller import Message, rep
from skl_shared.table import Table
from skl_shared.graphics.debug.controller import DEBUG
from skl_shared.logic import com as shcom
from skl_shared.time import Timer
import get as gt


class Commands:
    
    def swap_langs(self):
        gt.LANG1, gt.LANG2 = gt.LANG2, gt.LANG1
        gt.objs.get_files().reset()



class Ending(gt.Ending):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def debug(self):
        f = '[MClient] plugins.multitrandem.tests.Ending.debug'
        if not self.Success:
            rep.cancel(f)
            return
        ends = list(self.ends)
        ends = [str(end) for end in ends]
        headers = ('#', 'ENDINGS')
        iterable = (self.nos, ends)
        mes = Table(iterable=iterable, headers=headers).run()
        sub = _('File: "{}"').format(self.file)
        mes = sub + '\n\n' + mes
        DEBUG.reset(f, mes)
        DEBUG.show()



class Subject(gt.Subject):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def debug(self):
        f = '[MClient] plugins.multitrandem.tests.Subject.debug'
        if not self.Success:
            rep.cancel(f)
            return
        headers = ('#', 'FULL (1)', 'ABBR (1)', 'FULL (2)', 'ABBR (2)')
        iterable = (self.dic_nos, self.en_dicf, self.en_dic, self.ru_dicf
                   ,self.ru_dic)
        mes = Table(headers=headers, iterable=iterable).run()
        sub = _('File: "{}"').format(self.file)
        mes = sub + '\n\n' + mes
        DEBUG.reset(f, mes)
        DEBUG.show()



class Binary(gt.Binary):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []
        self.upages = []
        self.lpages = []
        self.zpages = []
    
    def get_max_limits(self, page_no):
        ''' Return positions of a page based on a block size.
            #NOTE: Seems that 'get.Binary.get_page_limits' which returns
                   a narrower range works fine, so I use the present function
                   for testing purposes only.
        '''
        f = '[MClient] plugins.multitrandem.tests.Binary.get_max_limits'
        if not self.Success:
            rep.cancel(f)
            return
        if page_no is None or not self.get_block_size():
            rep.empty(f)
            return
        mes = _('Page #: {}').format(page_no)
        Message(f, mes).show_debug()
        pos1 = page_no * self.bsize
        pos2 = pos1 + self.bsize
        sub1 = shcom.set_figure_commas(pos1)
        sub2 = shcom.set_figure_commas(pos2)
        mes = _('Page limits: [{}:{}]').format(sub1, sub2)
        Message(f, mes).show_debug()
        return(pos1, pos2)
    
    def show_info(self):
        f = '[MClient] plugins.multitrandem.tests.Binary.show_info'
        self.get_block_size()
        self.get_file_size()
        self.get_pages()
        if not self.Success:
            rep.cancel(f)
            return
        iwrite = io.StringIO()
        mes = _('File: {}').format(self.file)
        iwrite.write(mes)
        iwrite.write('\n')
        size = shcom.get_human_size(self.fsize)
        mes = _('File size: {}').format(size)
        iwrite.write(mes)
        iwrite.write('\n')
        size = shcom.set_figure_commas(self.bsize)
        mes = _('Block size: {}').format(size)
        iwrite.write(mes)
        iwrite.write('\n\n')
        mes = _('Pages:')
        iwrite.write(mes)
        iwrite.write('\n')
        nos = []
        types = []
        poses1 = []
        poses2 = []
        sizes = []
        for i in range(len(self.pages)):
            # Page #0 is actually an M area
            nos.append(i+1)
            if self.pages[i] in self.upages:
                types.append('U')
            elif self.pages[i] in self.lpages:
                types.append('L')
            elif self.pages[i] in self.zpages:
                types.append('Z')
            else:
                types.append(_('N/A'))
                mes = _('Wrong input data!')
                Message(f, mes, True).show_error()
            # The first page is actually an M area
            poses = self.get_page_limits(i+1)
            if poses:
                poses1.append(shcom.set_figure_commas(poses[0]))
                poses2.append(shcom.set_figure_commas(poses[1]))
                delta = poses[1] - poses[0]
                sizes.append(shcom.set_figure_commas(delta))
            else:
                rep.empty(f)
                poses1.append(_('N/A'))
                poses2.append(_('N/A'))
                sizes.append(_('N/A'))
        headers = ('#', 'TYPE', 'POS1', 'POS2', 'SIZE')
        iterable = [nos, types, poses1, poses2, sizes]
        mes = Table(headers=headers, iterable=iterable).run()
        iwrite.write(mes)
        iwrite.write('\n')
        mes = iwrite.getvalue()
        iwrite.close()
        DEBUG.reset(f, mes)
        DEBUG.show()
    
    def get_pages(self):
        f = '[MClient] plugins.multitrandem.tests.Binary.get_pages'
        self.get_block_size()
        if not self.Success:
            rep.cancel(f)
            return self.pages
        if self.pages:
            return self.pages
        limits = self.get_page_limit()
        if not limits:
            rep.empty(f)
            return self.pages
        ''' These limits are based on the binary size, so we can read it
            without fearing an empty input. 'if limit' skips 'M' area (page 0).
        '''
        limits = [limit * self.bsize for limit in range(limits) if limit]
        for limit in limits:
            node = self.read(limit, limit+1)
            if node == b'U':
                self.upages.append(limit)
            elif node == b'L':
                self.lpages.append(limit)
            elif node == b'Z':
                self.zpages.append(limit)
            else:
                sub = shcom.set_figure_commas(limit)
                messages = []
                mes = _('Position: {}').format(sub)
                messages.append(mes)
                mes = _('Wrong input data: "{}"!')
                mes = mes.format(node)
                messages.append(mes)
                mes = '\n'.join(messages)
                Message(f, mes, True).show_warning()
                break
        upages = [shcom.set_figure_commas(item) \
                  for item in self.upages
                 ]
        lpages = [shcom.set_figure_commas(item) \
                  for item in self.lpages
                 ]
        zpages = [shcom.set_figure_commas(item) \
                  for item in self.zpages
                 ]
        mes = _('U pages: {}').format(upages)
        Message(f, mes).show_debug()
        mes = _('L pages: {}').format(lpages)
        Message(f, mes).show_debug()
        mes = _('Z pages: {}').format(zpages)
        Message(f, mes).show_debug()
        self.pages = self.upages + self.lpages + self.zpages
        self.pages.sort()
        return self.pages



class Tests:
    
    def suggest(self):
        #pattern = 'acid'
        pattern = 'кислот'
        com.swap_langs()
        timer = Timer()
        timer.start()
        gt.objs.get_files().get_typein1().search(pattern)
        timer.end()
    
    def get_speech(self, pattern):
        ''' 'absolut'  -> 176     -> 32
            'absolute' -> 31,123  -> 2 ('absolutely')
            'absolute' -> 188,481 -> 67
            'measurement': [916, 3, 67, 80760, 20, 32, 223439, 3, 66]
        '''
        get = gt.Get(pattern)
        get.run()
        stemnos = get.stemnos
        stemnos = [gt.com.unpack(no) for no in stemnos]
        stemnos = [shcom.set_figure_commas(no) for no in stemnos]
        Message(f, stemnos).show_debug()
        mes = f'"{get.speech};{get.spabbr}"'
        Message(f, mes).show_debug()
    
    def run_ending(self):
        subj = Ending(gt.objs.get_files().iwalker.get_ending())
        subj.debug()
    
    def run_subject(self):
        subj = Subject(gt.objs.get_files().iwalker.get_subject())
        subj.debug()
    
    def _parse_upage(self, file):
        upage = UPage(file)
        upage.get_parts()
        upage.debug()
    
    def searchu_article(self):
        #pattern = b'\x00'
        #pattern = b'\x01\x02\x03'
        #pattern = b'\x02\x01\x03'
        #pattern = b'A'
        #pattern = b'\x02'
        #pattern = b'\x03'
        #pattern = b'\x04'
        #pattern = b':'
        #pattern = b'\xfc'
        pattern = b'\xfd'
        upage = UPage(gt.objs.get_files().iwalker.get_article())
        upage.get_parts()
        upage.searchu(pattern)
        #upage.debug()
    
    def parse_upage(self):
        file = gt.objs.get_files().iwalker.get_stems1()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_stems2()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_glue1()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_glue2()
        self._parse_upage(file)
        file = gt.objs.get_files().iwalker.get_article()
        self._parse_upage(file)
    
    def searchu_glue(self):
        #pattern = b'\x1b-\x00'
        pattern = b'\x00'
        upage = UPage(gt.objs.get_files().iwalker.get_glue1())
        upage.get_parts()
        upage.searchu(pattern)
        #upage.debug()
    
    def get_upage_stems(self):
        f = '[MClient] plugins.multitrandem.tests.Tests.get_upage_stems'
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.get_parts()
        part1 = list(upage.part1)
        part2 = list(upage.part2)
        part1d = [item.decode(gt.CODING, 'replace') for item in part1]
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h', part2[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part2l.append(unpacked)
            else:
                part2l.append('""')
        header = ('CHUNK1', 'CP1251', 'CHUNK2', '<h')
        data = [part1, part1d, part2, part2l]
        mes = Table(headers=header, iterable=data, sep=3 * ' ').run()
        DEBUG.reset(f, mes)
        DEBUG.show()
    
    def get_upage_glue(self):
        f = '[MClient] plugins.multitrandem.tests.Tests.get_upage_glue'
        upage = UPage(gt.objs.get_files().iwalker.get_glue1())
        upage.get_parts()
        part1 = list(upage.part1)
        part2 = list(upage.part2)
        part1l = []
        for i in range(len(part1)):
            if part1[i]:
                unpacked = struct.unpack('<b', part1[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part1l.append(unpacked)
            else:
                part1l.append('""')
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h', part2[i])[0]
                part2l.append(f'"{unpacked}"')
            else:
                part2l.append('""')
        header = ('CHUNK1', '<b', 'CHUNK2', '<h')
        data = [part1, part1l, part2, part2l]
        mes = Table(headers=header, iterable=data, sep=3 * ' ').run()
        DEBUG.reset(f, mes)
        DEBUG.show()
    
    def searchu_stems(self):
        f = '[MClient] plugins.multitrandem.tests.Tests.searchu_stems'
        timer = Timer(f)
        timer.start()
        #pattern = b'wol'
        #pattern = b'zero'
        #pattern = b'wi'
        #pattern = b'wifi'
        #pattern = b'willing'
        #pattern = b'vh'
        #pattern = b'ace'
        #pattern = b'a'
        #pattern = b'algorithm'
        #pattern = b'wol'
        #pattern = b'acf'
        #pattern = b'volume'
        pattern = b'abatement'
        
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.searchu(pattern)
        print('---------------------------------------------------')
        #pattern = 'уборка'
        #pattern = 'эт'
        #pattern = 'аж'
        #pattern = 'ажиотаж'
        #pattern = 'аккордеон'
        #pattern = 'ан'
        #pattern = 'анорексия'
        #pattern = 'ас'
        #pattern = 'асс'
        #pattern = 'язык'
        #pattern = 'этот'
        #pattern = 'железобетонный принцип'
        #pattern = 'з'
        #pattern = 'задеть'
        #pattern = 'зашуганный'
        pattern = 'звезда'
        pattern = bytes(pattern, gt.CODING)
        com.swap_langs()
        # Since we swap languages, the needed stems will always be #1
        upage = UPage(gt.objs.get_files().iwalker.get_stems1())
        upage.searchu(pattern)
        timer.end()
        #upage.debug()
    
    def translate_pair(self):
        self.translate('abasin')
        com.swap_langs()
        # 'factorage', 'sack' # 2 terms
        self.translate('уборка') # has a comment
    
    def translate_many(self):
        f = '[MClient] plugins.multitrandem.tests.Tests.translate_many'
        ''' MISSING IN MT DEMO:
            'преобразование случайной величины X, имеющей асимметричное распределение, в нормально распределённую величину Z'
        '''
        timer = Timer()
        timer.start()
        ms.STOP = True
        en_patterns = ['A & E'
                      ,'a posteriori'
                      ,'abasin'
                      ,'abatement of purchase price'
                      ,'abatement of tax'
                      ,'abbrmate'
                      ,'absolute measurements'
                      ,'acceleration measured in G'
                      ,'acceleration spectral density'
                      ,'ashlar line'
                      ,'baby fish'
                      ,'Bachelor of Vocational Education'
                      ,'calcium gallium germanium garnet'
                      ,'daily reports notice'
                      ,'deaf as an adder'
                      ,'eristic'
                      ,'habitable room'
                      ,'he has not a sou'
                      ,'Kapteyn transformation'
                      ,'law and equity'
                      ,'loadable system'
                      ,'palletbox'
                      ,'sack duty'
                      ,'work'
                      ,'World Union of Catholic Teachers'
                      ,'Zebra time'
                      ]
        ru_patterns = ['абонентское устройство для совместной передачи речи и данных'
                      ,'абсолютный способ измерения'
                      ,'Всемирный союз преподавателей-католиков'
                      ,'курс занятий для студентов последнего курса'
                      ,'с большой точностью'
                      ,'уборка'
                      ,'у него нет ни гроша'
                      ,'ячейка решётки'
                      ,'ящичный поддон'
                      ]
        failed = 0
        total = len(en_patterns) + len(ru_patterns)
        for pattern in en_patterns:
            if not self.translate(pattern):
                failed += 1
        com.swap_langs()
        for pattern in ru_patterns:
            if not self.translate(pattern):
                failed += 1
        ms.STOP = False
        timer.end()
        messages = []
        mes = _('Total: {}').format(total)
        messages.append(mes)
        mes = _('Successful: {}').format(total-failed)
        messages.append(mes)
        mes = _('Failed: {}').format(failed)
        messages.append(mes)
        mes = '\n' + '\n'.join(messages)
        Message(f, mes).show_debug()
    
    def translate(self, pattern):
        f = '[MClient] plugins.multitrandem.tests.Tests.translate'
        timer = Timer(f)
        timer.start()
        result = gt.Get(pattern).run()
        Message(f, result).show_debug()
        timer.end()
        return result



class UPage(gt.UPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def debug(self):
        f = '[MClient] plugins.multitrandem.tests.UPage.debug'
        if not self.Success:
            rep.cancel(f)
            return
        if self.file in (gt.objs.get_files().iwalker.get_stems1()
                        ,gt.objs.files.iwalker.get_stems2()
                        ):
            self.debug_stems()
        else:
            self.debug_glue()
    
    def debug_glue(self):
        f = '[MClient] plugins.multitrandem.tests.UPage.debug_glue'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.part2:
            rep.empty(f)
            return
        part1 = [gt.com.get_string(chunk) for chunk in self.part1]
        part2 = [struct.unpack('<h', chunk)[0] for chunk in self.part2]
        mes = Table(headers=('STEM', 'PAGEREF'), iterable=(part1, part2)
                   ,sep = 3 * ' ').run()
        if not mes:
            rep.empty(f)
            return
        mes = _('File: {}').format(self.file) + '\n\n' + mes
        DEBUG.reset(f, mes)
        DEBUG.show()
    
    def debug_stems(self):
        f = '[MClient] plugins.multitrandem.tests.UPage.debug_stems'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.part2:
            rep.empty(f)
            return
        part1 = [chunk.decode(gt.CODING, 'ignore') for chunk in self.part1]
        part2 = [struct.unpack('<h', chunk)[0] for chunk in self.part2]
        mes = Table(headers=('STEM', 'PAGEREF'), iterable=(part1, part2)
                   ,sep = 3 * ' ').run()
        if not mes:
            rep.empty(f)
            return
        mes = _('File: {}').format(self.file) + '\n\n' + mes
        DEBUG.reset(f, mes)
        DEBUG.show()


com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.multitrandem.tests.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    ''' Currently failing translations:
        "work"
        "совковая лопата с суживающимся полотном с прямолинейной кромкой"
        "собирать и содержать в определённом месте потерявшихся домашних животных или автомобили"
    '''
    #Tests().get_speech('DARE')
    #Tests().translate('DARE')
    #Binary(gt.objs.get_files().iwalker.get_glue1()).show_info()
    gt.DEBUG = True
    gt.com.overflowh(-1841)
