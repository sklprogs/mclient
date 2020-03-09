#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import struct
import get               as gt
import skl_shared.shared as sh
from skl_shared.localize import _


class Binary(gt.Binary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fsize  = 0
        self.pages  = []
        self.upages = []
        self.lpages = []
        self.zpages = []
    
    def info(self):
        f = '[MClient] plugins.multitranbin.tests.Binary.info'
        self.get_block_size()
        self.get_file_size()
        self.get_pages()
        if self.Success:
            iwrite = io.StringIO()
            mes = _('File: {}').format(self.file)
            iwrite.write(mes)
            iwrite.write('\n')
            size = sh.com.human_size(self.fsize)
            mes  = _('File size: {}').format(size)
            iwrite.write(mes)
            iwrite.write('\n')
            size = sh.com.figure_commas(self.bsize)
            mes  = _('Block size: {}').format(size)
            iwrite.write(mes)
            iwrite.write('\n\n')
            mes = _('Pages:')
            iwrite.write(mes)
            iwrite.write('\n')
            nos    = []
            types  = []
            poses1 = []
            poses2 = []
            sizes  = []
            for i in range(len(self.pages)):
                # The first page is actually an M area
                nos.append(i+2)
                if self.pages[i] in self.upages:
                    types.append('U')
                elif self.pages[i] in self.lpages:
                    types.append('L')
                elif self.pages[i] in self.zpages:
                    types.append('Z')
                else:
                    types.append(_('N/A'))
                    mes = _('Wrong input data!')
                    sh.objs.mes(f,mes).error()
                # The first page is actually an M area
                poses = self.get_page_limits(i+1)
                if poses:
                    poses1.append(sh.com.figure_commas(poses[0]))
                    poses2.append(sh.com.figure_commas(poses[1]))
                    sizes.append(sh.com.figure_commas(poses[1]-poses[0]))
                else:
                    sh.com.empty(f)
                    poses1.append(_('N/A'))
                    poses2.append(_('N/A'))
                    sizes.append(_('N/A'))
            headers  = ('#','TYPE','POS1','POS2','SIZE')
            iterable = [nos,types,poses1,poses2,sizes]
            mes = sh.FastTable (headers  = headers
                               ,iterable = iterable
                               ).run()
            iwrite.write(mes)
            iwrite.write('\n')
            mes = iwrite.getvalue()
            iwrite.close()
            sh.com.fast_debug(mes)
        else:
            sh.com.cancel(f)
    
    def get_pages(self):
        f = '[MClient] plugins.multitranbin.tests.Binary.get_pages'
        self.get_block_size()
        if self.Success:
            if not self.pages:
                limits = self.get_page_limit()
                if limits:
                    ''' These limits are based on the binary size, so we
                        can read it without fearing an empty input.
                        'if limit' skips 'M' area (page 0).
                    '''
                    limits = [limit * self.bsize \
                              for limit in range(limits) \
                              if limit
                             ]
                    for limit in limits:
                        node = self.read(limit,limit+1)
                        if node == b'U':
                            self.upages.append(limit)
                        elif node == b'L':
                            self.lpages.append(limit)
                        elif node == b'Z':
                            self.zpages.append(limit)
                        else:
                            sub = sh.com.figure_commas(limit)
                            messages = []
                            mes = _('Position: {}').format(sub)
                            messages.append(mes)
                            mes = _('Wrong input data: "{}"!')
                            mes = mes.format(node)
                            messages.append(mes)
                            mes = '\n'.join(messages)
                            sh.objs.mes(f,mes).warning()
                            break
                    upages = [sh.com.figure_commas(item) \
                              for item in self.upages
                             ]
                    lpages = [sh.com.figure_commas(item) \
                              for item in self.lpages
                             ]
                    zpages = [sh.com.figure_commas(item) \
                              for item in self.zpages
                             ]
                    mes = _('U pages: {}').format(upages)
                    sh.objs.mes(f,mes,True).debug()
                    mes = _('L pages: {}').format(lpages)
                    sh.objs.mes(f,mes,True).debug()
                    mes = _('Z pages: {}').format(zpages)
                    sh.objs.mes(f,mes,True).debug()
                    self.pages = self.upages + self.lpages + self.zpages
                    self.pages.sort()
                else:
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)
        return self.pages
    
    def get_page_limit(self):
        f = '[MClient] plugins.multitranbin.tests.Binary.get_page_limit'
        if self.Success:
            val = self.get_file_size() // self.get_block_size()
            mes = sh.com.figure_commas(val)
            sh.objs.mes(f,mes,True).debug()
            return val
        else:
            sh.com.cancel(f)
    
    def get_file_size(self):
        ''' This should be equal to 'sh.File(self.vfile).size()'.
            #NOTE: size = max_pos + 1
        '''
        f = '[MClient] plugins.multitranbin.tests.Binary.get_file_size'
        if self.Success:
            if not self.fsize:
                self.fsize = sh.File(self.file).size()
            mes  = _('File "{}" has the size of {}')
            size = sh.com.human_size(self.fsize)
            mes  = mes.format(self.file,size)
            sh.objs.mes(f,mes,True).debug()
            if not self.fsize:
                self.Success = False
                mes = _('Empty output is not allowed!')
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
        return self.fsize



class Tests:
    
    def _parse_upage(self,file):
        upage = UPage(file)
        upage.get_parts()
        upage.debug()
    
    def parse_upage(self):
        file = gt.objs.files().iwalker.get_stems1()
        self._parse_upage(file)
        file = gt.objs.files().iwalker.get_stems2()
        self._parse_upage(file)
        file = gt.objs.files().iwalker.get_glue1()
        self._parse_upage(file)
        file = gt.objs.files().iwalker.get_glue2()
        self._parse_upage(file)
    
    def searchu_glue(self):
        #pattern = b'\x1b-\x00'
        pattern  = b'\x00'
        upage = UPage(gt.objs.files().iwalker.get_glue1())
        upage.get_parts()
        upage.searchu(pattern)
        #upage.debug()
    
    def get_upage_stems(self):
        upage = UPage(gt.objs.files().iwalker.get_stems1())
        upage.get_parts()
        part1  = list(upage.part1)
        part2  = list(upage.part2)
        part1d = [item.decode(gt.ENCODING,'replace') for item in part1]
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h',part2[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part2l.append(unpacked)
            else:
                part2l.append('""')
        header = ('CHUNK1','CP1251','CHUNK2','<h')
        data   = [part1,part1d,part2,part2l]
        mes = sh.FastTable (headers  = header
                           ,iterable = data
                           ,sep      = 3 * ' '
                           ).run()
        sh.com.fast_debug(mes)
    
    def get_upage_glue(self):
        upage = UPage(gt.objs.files().iwalker.get_glue1())
        upage.get_parts()
        part1  = list(upage.part1)
        part2  = list(upage.part2)
        part1l = []
        for i in range(len(part1)):
            if part1[i]:
                unpacked = struct.unpack('<b',part1[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part1l.append(unpacked)
            else:
                part1l.append('""')
        part2l = []
        for i in range(len(part2)):
            if part2[i]:
                unpacked = struct.unpack('<h',part2[i])[0]
                unpacked = '"{}"'.format(unpacked)
                part2l.append(unpacked)
            else:
                part2l.append('""')
        header = ('CHUNK1','<b','CHUNK2','<h')
        data   = [part1,part1l,part2,part2l]
        mes = sh.FastTable (headers  = header
                           ,iterable = data
                           ,sep      = 3 * ' '
                           ).run()
        sh.com.fast_debug(mes)
        '''
        tmp = list(set(part2l))
        tmp.sort()
        sh.com.fast_debug(tmp)
        '''
    
    def searchu_stems(self):
        f = '[MClient] plugins.multitranbin.tests.Tests.searchu_stems'
        timer = sh.Timer(f)
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
        
        gt.LANG1 = 'English'
        gt.LANG2 = 'Russian'
        gt.objs.files().reset()
        upage = UPage(gt.objs.files().iwalker.get_stems1())
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
        pattern  = 'звезда'
        pattern  = bytes(pattern,gt.ENCODING)
        gt.LANG1 = 'Russian'
        gt.LANG2 = 'English'
        gt.objs.files().reset()
        # Since we swap languages, the needed stems will always be #1
        upage = UPage(gt.objs.files().iwalker.get_stems1())
        upage.searchu(pattern)
        timer.end()
        #upage.debug()
    
    def translate_pair(self):
        self.translate('abasin')
        gt.LANG1 = 'Russian'
        gt.LANG2 = 'English'
        gt.objs.files().reset()
        # 'factorage', 'sack' # 2 terms
        self.translate('уборка') # has a comment
    
    def translate_many(self):
        # 'absolute measurements' = 'абсолютный способ измерения'
        '''
        # Successfully processed patterns
        patterns = ['abasin'
                   ,'absolute measurements'
                   ,'baby fish'
                   ,'sack duty'
                   ,'habitable room'
                   ,'a posteriori'
                   ,'abatement of tax'
                   ,'abatement of purchase price'
                   ,'habitable room'
                   ,'absolute distribution'
                   ,'abolishment of a scheme'
                   ,'calcium gallium germanium garnet'
                   ,'daily reports notice'
                   ]
        # Failed patterns
        # No combos:      ['he has not a sou'
                          ,'World Union of Catholic Teachers'
                          ,'Kapteyn transformation'
                          ]
        # Stack overflow: ['Bachelor of Vocational Education'
                          ,'ashlar line'
                          ,'acceleration measured in G'
                          ,'acceleration spectral density'
                          ,'A & E'
                          ,'Abelian equation'
                          ,'deaf as an adder'
                          ,'eristic'
                          ,'курс занятий для студентов последнего курса'
                          ]
        '''
        patterns = ['he has not a sou'
                   ,'Bachelor of Vocational Education'
                   ,'ashlar line'
                   ,'acceleration measured in G'
                   ]
        for pattern in patterns:
            self.translate(pattern)
            input(_('Press any key'))
    
    def translate(self,pattern):
        f = '[MClient] plugins.multitranbin.tests.Tests.translate'
        timer = sh.Timer(f)
        timer.start()
        iget = gt.Get(pattern)
        sh.objs.mes(f,iget.run(),True).debug()
        timer.end()



class UPage(gt.UPage):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def debug(self):
        f = '[MClient] plugins.multitranbin.tests.UPage.debug'
        if self.Success:
            if self.file in (gt.objs.files().iwalker.get_stems1()
                            ,gt.objs._files.iwalker.get_stems2()
                            ):
                self.debug_stems()
            elif self.file in (gt.objs._files.iwalker.get_glue1()
                              ,gt.objs._files.iwalker.get_glue2()
                              ):
                self.debug_glue()
            else:
                mes = _('Not implemented yet!')
                sh.objs.mes(f,mes).info()
        else:
            sh.com.cancel(f)
    
    def debug_glue(self):
        f = '[MClient] plugins.multitranbin.tests.UPage.debug_glue'
        if self.Success:
            if self.part2:
                part1 = [gt.com.get_string(chunk) \
                         for chunk in self.part1
                        ]
                part2 = [struct.unpack('<h',chunk)[0] \
                         for chunk in self.part2
                        ]
                mes = sh.FastTable (headers  = ('STEM','PAGEREF')
                                   ,iterable = (part1,part2)
                                   ,sep      = 3 * ' '
                                   ).run()
                if mes:
                    mes = _('File: {}').format(self.file) + '\n\n' + mes
                    sh.com.fast_debug(mes)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def debug_stems(self):
        f = '[MClient] plugins.multitranbin.tests.UPage.debug_stems'
        if self.Success:
            if self.part2:
                part1 = [chunk.decode(gt.ENCODING,'ignore') \
                         for chunk in self.part1
                        ]
                part2 = [struct.unpack('<h',chunk)[0] \
                         for chunk in self.part2
                        ]
                mes = sh.FastTable (headers  = ('STEM','PAGEREF')
                                   ,iterable = (part1,part2)
                                   ,sep      = 3 * ' '
                                   ).run()
                if mes:
                    mes = _('File: {}').format(self.file) + '\n\n' + mes
                    sh.com.fast_debug(mes)
                else:
                    sh.com.empty(f)
            else:
                sh.com.empty(f)
        else:
            sh.com.cancel(f)


if __name__ == '__main__':
    f = '[MClient] plugins.multitranbin.tests.__main__'
    gt.PATH = '/home/pete/.config/mclient/dics'
    #Tests().searchu()
    #Tests().translate('removal')
    #Tests().translate_many()
    #Tests().translate('Bachelor of Vocational Education')
    #Tests().translate('Kafir')
    #Tests().translate('absolute measurements')
    #Tests().translate('abatement of purchase price')
    #Tests().translate('answer print')
    #LANG1, LANG2 = LANG2, LANG1
    #objs.files().reset()
    '''
    'с большой точностью'
    'уборка'
    'стычка'
    OK: 'садовод'
    '''
    #Tests().translate('boiler')
    #Tests().translate('boiler')
    #Tests().translate_pair()
    #gt.objs.files().get_stems1().get_page_limits(20)
    #objs.files().get_stems1().find(b'abasin',1000,9000)
    #Tests().glue_upage()
    #Tests().stems_upage()
    #objs.files().close()
    #Tests().searchu_stems()
    #Tests().searchu_glue()
    #Tests().parse_upage()
    file = gt.objs.files().iwalker.get_article()
    ibin = Binary(file)
    ibin.info()
