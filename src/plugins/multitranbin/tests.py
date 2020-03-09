#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import struct
import get as gt
import skl_shared.shared as sh
from skl_shared.localize import _


class Tests:
    
    def searchu_glue(self):
        upage = UPage(gt.objs.files().iwalker.get_glue1())
        upage.get_parts()
        upage.searchu(b'\x1b-\x00')
        upage.debug()
    
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
        #pattern = b'abatement'
        
        gt.LANG1 = 'English'
        gt.LANG2 = 'Russian'
        gt.objs.files().reset()
        upage = UPage(gt.objs.files().iwalker.get_stems1())
        upage.searchu(b'abatement')
        print('---------------------------------------------------')
        gt.LANG1 = 'Russian'
        gt.LANG2 = 'English'
        gt.objs.files().reset()
        # Since we swap languages, the needed stems will always be #1
        upage = UPage(gt.objs.files().iwalker.get_stems1())
        upage.searchu(bytes('уборка',gt.ENCODING))
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
    #objs.files().get_stems1().get_limits(20)
    #objs.files().get_stems1().find(b'abasin',1000,9000)
    #Tests().glue_upage()
    #Tests().stems_upage()
    #objs.files().close()
    Tests().searchu_glue()
