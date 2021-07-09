#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import locale

from skl_shared.localize import _
import skl_shared.shared as sh

SUBJECTS = {'AI.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'AI.'
                   ,'title': 'Artificial intelligence'
                   }
               ,'ru':
                   {'short': 'ИИ.'
                   ,'title': 'Искусственный интеллект'
                   }
               ,'de':
                   {'short': 'AI.'
                   ,'title': 'Artificial intelligence'
                   }
               ,'es':
                   {'short': 'AI.'
                   ,'title': 'Artificial intelligence'
                   }
               ,'uk':
                   {'short': 'шт.інтел.'
                   ,'title': 'Штучний інтелект'
                   }
               }
           ,'AIDS.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'AIDS.'
                   ,'title': 'AIDS'
                   }
               ,'ru':
                   {'short': 'СПИД.'
                   ,'title': 'СПИД'
                   }
               ,'de':
                   {'short': 'AIDS.'
                   ,'title': 'AIDS'
                   }
               ,'es':
                   {'short': 'AIDS.'
                   ,'title': 'AIDS'
                   }
               ,'uk':
                   {'short': 'СНІД'
                   ,'title': 'СНІД'
                   }
               }
           ,'AMEX.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'AMEX.'
                   ,'title': 'American stock exchange'
                   }
               ,'ru':
                   {'short': 'AMEX.'
                   ,'title': 'Американская фондовая биржа'
                   }
               ,'de':
                   {'short': 'AMEX.'
                   ,'title': 'American stock exchange'
                   }
               ,'es':
                   {'short': 'AMEX.'
                   ,'title': 'American stock exchange'
                   }
               ,'uk':
                   {'short': 'AMEX'
                   ,'title': 'Американська фондова біржа'
                   }
               }
           ,'ASCII.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'ASCII.'
                   ,'title': 'ASCII'
                   }
               ,'ru':
                   {'short': 'ASCII.'
                   ,'title': 'ASCII'
                   }
               ,'de':
                   {'short': 'ASCII'
                   ,'title': 'ASCII'
                   }
               ,'es':
                   {'short': 'ASCII.'
                   ,'title': 'ASCII'
                   }
               ,'uk':
                   {'short': 'ASCII'
                   ,'title': 'ASCII'
                   }
               }
           ,'Alg.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Alg.'
                   ,'title': 'Algeria'
                   }
               ,'ru':
                   {'short': 'Алж.'
                   ,'title': 'Алжир'
                   }
               ,'de':
                   {'short': 'Alg.'
                   ,'title': 'Algeria'
                   }
               ,'es':
                   {'short': 'Alg.'
                   ,'title': 'Algeria'
                   }
               ,'uk':
                   {'short': 'Алж.'
                   ,'title': 'Алжир'
                   }
               }
           ,'AmE':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'AmE'
                   ,'title': 'American English'
                   }
               ,'ru':
                   {'short': 'ам.англ.'
                   ,'title': 'Американский вариант английского языка'
                   }
               ,'de':
                   {'short': 'am.Engl.'
                   ,'title': 'amerikanisches Englisch'
                   }
               ,'es':
                   {'short': 'AmE'
                   ,'title': 'American English'
                   }
               ,'uk':
                   {'short': 'ам.англ.'
                   ,'title': 'Американський варіант англійської мови'
                   }
               }
           ,'Ant.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Ant.'
                   ,'title': 'Antilles'
                   }
               ,'ru':
                   {'short': 'Ант.'
                   ,'title': 'Антильские острова'
                   }
               ,'de':
                   {'short': 'Ant.'
                   ,'title': 'Antilles'
                   }
               ,'es':
                   {'short': 'Ant.'
                   ,'title': 'Antilles'
                   }
               ,'uk':
                   {'short': 'Ант.остр.'
                   ,'title': 'Антильські острови'
                   }
               }
           ,'Apollo-Soyuz':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'Apollo-Soyuz'
                   ,'title': 'Apollo-Soyuz'
                   }
               ,'ru':
                   {'short': 'Союз-Апол.'
                   ,'title': 'Союз-Аполлон'
                   }
               ,'de':
                   {'short': 'Apollo-Soyuz'
                   ,'title': 'Apollo-Soyuz'
                   }
               ,'es':
                   {'short': 'Apollo-Soyuz'
                   ,'title': 'Apollo-Soyuz'
                   }
               ,'uk':
                   {'short': 'Союз-Аполлон'
                   ,'title': 'Союз-Аполлон'
                   }
               }
           ,'Arag.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Arag.'
                   ,'title': 'Aragon'
                   }
               ,'ru':
                   {'short': 'Араг.'
                   ,'title': 'Арагон'
                   }
               ,'de':
                   {'short': 'Arag.'
                   ,'title': 'Aragon'
                   }
               ,'es':
                   {'short': 'Arag.'
                   ,'title': 'Aragon'
                   }
               ,'uk':
                   {'short': 'Араг.'
                   ,'title': 'Арагон'
                   }
               }
           ,'Arg.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Arg.'
                   ,'title': 'Argentina'
                   }
               ,'ru':
                   {'short': 'Арг.'
                   ,'title': 'Аргентина'
                   }
               ,'de':
                   {'short': 'Arg.'
                   ,'title': 'Argentina'
                   }
               ,'es':
                   {'short': 'Arg.'
                   ,'title': 'Argentina'
                   }
               ,'uk':
                   {'short': 'Арген.'
                   ,'title': 'Аргентина'
                   }
               }
           ,'Australia':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Australia'
                   ,'title': 'Australia'
                   }
               ,'ru':
                   {'short': 'Австрал.'
                   ,'title': 'Австралия'
                   }
               ,'de':
                   {'short': 'Austral.'
                   ,'title': 'Australien'
                   }
               ,'es':
                   {'short': 'Australia'
                   ,'title': 'Australia'
                   }
               ,'uk':
                   {'short': 'Австралія'
                   ,'title': 'Австралія'
                   }
               }
           ,'Austria':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Austria'
                   ,'title': 'Austria'
                   }
               ,'ru':
                   {'short': 'Австрия.'
                   ,'title': 'Австрия'
                   }
               ,'de':
                   {'short': 'Österr.'
                   ,'title': 'Österreich'
                   }
               ,'es':
                   {'short': 'Austria'
                   ,'title': 'Austria'
                   }
               ,'uk':
                   {'short': 'Австр.'
                   ,'title': 'Австрія'
                   }
               }
           ,'Belar.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Belar.'
                   ,'title': 'Belarus'
                   }
               ,'ru':
                   {'short': 'Белар.'
                   ,'title': 'Беларусь'
                   }
               ,'de':
                   {'short': 'Bel.'
                   ,'title': 'Belarus'
                   }
               ,'es':
                   {'short': 'Belar.'
                   ,'title': 'Belarus'
                   }
               ,'uk':
                   {'short': 'Білор.'
                   ,'title': 'Білорусь'
                   }
               }
           ,'BrE':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'BrE'
                   ,'title': 'British English'
                   }
               ,'ru':
                   {'short': 'бр.англ.'
                   ,'title': 'Британский вариант английского языка'
                   }
               ,'de':
                   {'short': 'brit. engl.'
                   ,'title': 'Britisches Englisch'
                   }
               ,'es':
                   {'short': 'ingl.brit.'
                   ,'title': 'Inglés británico'
                   }
               ,'uk':
                   {'short': 'бр.англ.'
                   ,'title': 'Британський варіант англійської мови'
                   }
               }
           ,'Braz.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Braz.'
                   ,'title': 'Brazil'
                   }
               ,'ru':
                   {'short': 'Браз.'
                   ,'title': 'Бразилия'
                   }
               ,'de':
                   {'short': 'Braz.'
                   ,'title': 'Brazil'
                   }
               ,'es':
                   {'short': 'Braz.'
                   ,'title': 'Brazil'
                   }
               ,'uk':
                   {'short': 'Браз.'
                   ,'title': 'Бразилія'
                   }
               }
           ,'C.-R.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'C.-R.'
                   ,'title': 'Costa Rica'
                   }
               ,'ru':
                   {'short': 'К.-Р.'
                   ,'title': 'Коста-Рика'
                   }
               ,'de':
                   {'short': 'C.-R.'
                   ,'title': 'Costa Rica'
                   }
               ,'es':
                   {'short': 'C.-R.'
                   ,'title': 'Costa Rica'
                   }
               ,'uk':
                   {'short': 'К.-Р.'
                   ,'title': 'Коста-Рика'
                   }
               }
           ,'CNC':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               ,'ru':
                   {'short': 'ЧПУ.'
                   ,'title': 'Числовое программное управление'
                   }
               ,'de':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               ,'es':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               ,'uk':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               }
           ,'CRT':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'CRT'
                   ,'title': 'Cathode-ray tubes'
                   }
               ,'ru':
                   {'short': 'ЭЛТ.'
                   ,'title': 'Электронно-лучевые трубки'
                   }
               ,'de':
                   {'short': 'CRT'
                   ,'title': 'Kathodenstrahlröhre'
                   }
               ,'es':
                   {'short': 'CRT'
                   ,'title': 'Cathode-ray tubes'
                   }
               ,'uk':
                   {'short': 'ЕПТ'
                   ,'title': 'Електронно-променеві трубки'
                   }
               }
           ,'CT':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'CT'
                   ,'title': 'Computer tomography'
                   }
               ,'ru':
                   {'short': 'КТ.'
                   ,'title': 'Компьютерная томография'
                   }
               ,'de':
                   {'short': 'CT'
                   ,'title': 'Computer tomography'
                   }
               ,'es':
                   {'short': 'CT'
                   ,'title': 'Computer tomography'
                   }
               ,'uk':
                   {'short': 'КТ'
                   ,'title': "Комп'ютерна томографія"}}, 'Canada':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Canada'
                   ,'title': 'Canada'
                   }
               ,'ru':
                   {'short': 'Канада.'
                   ,'title': 'Канада'
                   }
               ,'de':
                   {'short': 'Kanada.'
                   ,'title': 'Kanada'
                   }
               ,'es':
                   {'short': 'Canada'
                   ,'title': 'Canada'
                   }
               ,'uk':
                   {'short': 'Канада'
                   ,'title': 'Канада'
                   }
               }
           ,'Centr.Am.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Centr.Am.'
                   ,'title': 'Central America'
                   }
               ,'ru':
                   {'short': 'Ц.-Ам.'
                   ,'title': 'Центральная Америка'
                   }
               ,'de':
                   {'short': 'Centr.Am.'
                   ,'title': 'Central America'
                   }
               ,'es':
                   {'short': 'Centr.Am.'
                   ,'title': 'Central America'
                   }
               ,'uk':
                   {'short': 'Ц.Ам.'
                   ,'title': 'Центральна Америка'
                   }
               }
           ,'Chil.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Chil.'
                   ,'title': 'Chile'
                   }
               ,'ru':
                   {'short': 'Чили.'
                   ,'title': 'Чили'
                   }
               ,'de':
                   {'short': 'Chil.'
                   ,'title': 'Chile'
                   }
               ,'es':
                   {'short': 'Chil.'
                   ,'title': 'Chile'
                   }
               ,'uk':
                   {'short': 'Чилі'
                   ,'title': 'Чилі'
                   }
               }
           ,'China':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'China'
                   ,'title': 'China'
                   }
               ,'ru':
                   {'short': 'Китай.'
                   ,'title': 'Китай'
                   }
               ,'de':
                   {'short': 'Chin.'
                   ,'title': 'China'
                   }
               ,'es':
                   {'short': 'China'
                   ,'title': 'China'
                   }
               ,'uk':
                   {'short': 'Китай'
                   ,'title': 'Китай'
                   }
               }
           ,'Col.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Col.'
                   ,'title': 'Columbia'
                   }
               ,'ru':
                   {'short': 'Кол.'
                   ,'title': 'Колумбия'
                   }
               ,'de':
                   {'short': 'Col.'
                   ,'title': 'Columbia'
                   }
               ,'es':
                   {'short': 'Col.'
                   ,'title': 'Columbia'
                   }
               ,'uk':
                   {'short': 'Колум.'
                   ,'title': 'Колумбія'
                   }
               }
           ,'Cuba':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Cuba'
                   ,'title': 'Cuba'
                   }
               ,'ru':
                   {'short': 'Куба.'
                   ,'title': 'Куба'
                   }
               ,'de':
                   {'short': 'Cuba'
                   ,'title': 'Cuba'
                   }
               ,'es':
                   {'short': 'Cuba'
                   ,'title': 'Cuba'
                   }
               ,'uk':
                   {'short': 'Куба.'
                   ,'title': 'Куба'
                   }
               }
           ,'Cypr.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Cypr.'
                   ,'title': 'Cyprus'
                   }
               ,'ru':
                   {'short': 'Кипр.'
                   ,'title': 'Кипр'
                   }
               ,'de':
                   {'short': 'Cypr.'
                   ,'title': 'Cyprus'
                   }
               ,'es':
                   {'short': 'Cypr.'
                   ,'title': 'Cyprus'
                   }
               ,'uk':
                   {'short': 'Кіпр'
                   ,'title': 'Кіпр'
                   }
               }
           ,'Dutch':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'Dutch'
                   ,'title': 'Dutch'
                   }
               ,'ru':
                   {'short': 'голл.'
                   ,'title': 'Голландский (нидерландский) язык'
                   }
               ,'de':
                   {'short': 'Niederl.'
                   ,'title': 'Niederländisch'
                   }
               ,'es':
                   {'short': 'holand.'
                   ,'title': 'Holandés'
                   }
               ,'uk':
                   {'short': 'голл.'
                   ,'title': 'Голландська (нідерландська) мова'
                   }
               }
           ,'EBRD':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'EBRD'
                   ,'title': 'European Bank for Reconstruction and Development'
                   }
               ,'ru':
                   {'short': 'ЕБРР.'
                   ,'title': 'Европейский банк реконструкции и развития'
                   }
               ,'de':
                   {'short': 'EBWE'
                   ,'title': 'Europäische Bank für Wiederaufbau und Entwicklung'
                   }
               ,'es':
                   {'short': 'EBRD'
                   ,'title': 'European Bank for Reconstruction and Development'
                   }
               ,'uk':
                   {'short': 'ЄБРР'
                   ,'title': 'Європейський банк реконструкції та розвитку'
                   }
               }
           ,'EU.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'EU.'
                   ,'title': 'European Union'
                   }
               ,'ru':
                   {'short': 'ЕС.'
                   ,'title': 'Евросоюз'
                   }
               ,'de':
                   {'short': 'EU.'
                   ,'title': 'European Union'
                   }
               ,'es':
                   {'short': 'EU.'
                   ,'title': 'European Union'
                   }
               ,'uk':
                   {'short': 'ЄС'
                   ,'title': 'Європейський Союз'
                   }
               }
           ,'Ecuad.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'Ecuad.'
                   ,'title': 'Ecuador'
                   }
               ,'ru':
                   {'short': 'Эквад.'
                   ,'title': 'Эквадор'
                   }
               ,'de':
                   {'short': 'Ecuad.'
                   ,'title': 'Ecuador'
                   }
               ,'es':
                   {'short': 'Ecuad.'
                   ,'title': 'Ecuador'
                   }
               ,'uk':
                   {'short': 'Еквад.'
                   ,'title': 'Еквадор'
                   }
               }
           ,'FBI.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'FBI.'
                   ,'title': 'Federal Bureau of Investigation'
                   }
               ,'ru':
                   {'short': 'ФБР.'
                   ,'title': 'Федеральное бюро расследований'
                   }
               ,'de':
                   {'short': 'FBI.'
                   ,'title': 'Federal Bureau of Investigation'
                   }
               ,'es':
                   {'short': 'FBI.'
                   ,'title': 'Federal Bureau of Investigation'
                   }
               ,'uk':
                   {'short': 'ФБР'
                   ,'title': 'Федеральне бюро розслідувань'
                   }
               }
           ,'GDR':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'GDR'
                   ,'title': 'East Germany'
                   }
               ,'ru':
                   {'short': 'ист., ГДР'
                   ,'title': 'Термин времен ГДР'
                   }
               ,'de':
                   {'short': 'DDR.'
                   ,'title': 'Ostdeutschland (Geschichte)'
                   }
               ,'es':
                   {'short': 'GDR'
                   ,'title': 'East Germany'
                   }
               ,'uk':
                   {'short': 'іст., НДР'
                   ,'title': 'Термін часів НДР'
                   }
               }
           ,'Germ.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Germ.'
                   ,'title': 'Germany'
                   }
               ,'ru':
                   {'short': 'Герман.'
                   ,'title': 'Германия'
                   }
               ,'de':
                   {'short': 'Deutschl.'
                   ,'title': 'Deutschland'
                   }
               ,'es':
                   {'short': 'Germ.'
                   ,'title': 'Germany'
                   }
               ,'uk':
                   {'short': 'Німеч.'
                   ,'title': 'Німеччина'
                   }
               }
           ,'Gruzovik':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik'
                   ,'title': 'General'
                   }
               ,'ru':
                   {'short': 'Gruzovik'
                   ,'title': 'Общая лексика'
                   }
               ,'de':
                   {'short': 'Gruzovik'
                   ,'title': 'Allgemeine Lexik'
                   }
               ,'es':
                   {'short': 'Gruzovik'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'Gruzovik'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'Gruzovik, GOST.':
               {'is_valid': False
               ,'major_en': 'Quality control and standards'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, GOST.'
                   ,'title': 'GOST'
                   }
               ,'ru':
                   {'short': 'Gruzovik, ГОСТ.'
                   ,'title': 'ГОСТ'
                   }
               ,'de':
                   {'short': 'Gruzovik, GOST.'
                   ,'title': 'GOST'
                   }
               ,'es':
                   {'short': 'Gruzovik, GOST.'
                   ,'title': 'GOST'
                   }
               ,'uk':
                   {'short': 'Gruzovik, станд.'
                   ,'title': 'Стандарти'
                   }
               }
           ,'Gruzovik, IT':
               {'is_valid': False
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Information technology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, ИТ.'
                   ,'title': 'Информационные технологии'
                   }
               ,'de':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Informationstechnik'
                   }
               ,'es':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Інформаційні технології'
                   }
               }
           ,'Gruzovik, abbr.':
               {'is_valid': False
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, abbr.'
                   ,'title': 'Abbreviation'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сокр.'
                   ,'title': 'Сокращение'
                   }
               ,'de':
                   {'short': 'Gruzovik, Abkürz.'
                   ,'title': 'Abkürzung'
                   }
               ,'es':
                   {'short': 'Gruzovik, abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'Gruzovik, abbr., IT':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, abbr., IT'
                   ,'title': 'Abbreviation, Information technology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сокр., ИТ.'
                   ,'title': 'Сокращение, Информационные технологии'
                   }
               ,'de':
                   {'short': 'Gruzovik, Abkürz., IT'
                   ,'title': 'Abkürzung, Informationstechnik'
                   }
               ,'es':
                   {'short': 'Gruzovik, abrev., IT'
                   ,'title': 'Abreviatura, Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., IT'
                   ,'title': 'Абревіатура, Інформаційні технології'
                   }
               }
           ,'Gruzovik, abbr., account.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, abbr., account.'
                   ,'title': 'Abbreviation, Accounting'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сокр., бухг.'
                   ,'title': 'Сокращение, Бухгалтерский учет (кроме аудита)'
                   }
               ,'de':
                   {'short': 'Gruzovik, Abkürz., Buchhalt.'
                   ,'title': 'Abkürzung, Buchhaltung'
                   }
               ,'es':
                   {'short': 'Gruzovik, abrev., cont.'
                   ,'title': 'Abreviatura, Contabilidad'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., бухг.'
                   ,'title': 'Абревіатура, Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'Gruzovik, abbr., bank.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, abbr., bank.'
                   ,'title': 'Abbreviation, Banking'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сокр., банк.'
                   ,'title': 'Сокращение, Банки и банковское дело'
                   }
               ,'de':
                   {'short': 'Gruzovik, Abkürz., Bank.'
                   ,'title': 'Abkürzung, Bankwesen'
                   }
               ,'es':
                   {'short': 'Gruzovik, abrev., bank.'
                   ,'title': 'Abreviatura, Banking'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., банк.'
                   ,'title': 'Абревіатура, Банки та банківська справа'
                   }
               }
           ,'Gruzovik, adm.law.':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'ru':
                   {'short': 'Gruzovik, админ.прав.'
                   ,'title': 'Административное право'
                   }
               ,'de':
                   {'short': 'Gruzovik, adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'es':
                   {'short': 'Gruzovik, adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'uk':
                   {'short': 'Gruzovik, адмін.пр.'
                   ,'title': 'Адміністративне право'
                   }
               }
           ,'Gruzovik, adv.':
               {'is_valid': False
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, adv.'
                   ,'title': 'Advertising'
                   }
               ,'ru':
                   {'short': 'Gruzovik, рекл.'
                   ,'title': 'Реклама'
                   }
               ,'de':
                   {'short': 'Gruzovik, Werb.'
                   ,'title': 'Werbung'
                   }
               ,'es':
                   {'short': 'Gruzovik, adv.'
                   ,'title': 'Advertising'
                   }
               ,'uk':
                   {'short': 'Gruzovik, рекл.'
                   ,'title': 'Реклама'
                   }
               }
           ,'Gruzovik, aer.phot.':
               {'is_valid': False
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'ru':
                   {'short': 'Gruzovik, аэрофот.'
                   ,'title': 'Аэрофотосъемка и топография'
                   }
               ,'de':
                   {'short': 'Gruzovik, aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'es':
                   {'short': 'Gruzovik, aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, аерофот.'
                   ,'title': 'Аерофозйомка та топографія'
                   }
               }
           ,'Gruzovik, agric.':
               {'is_valid': False
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, agric.'
                   ,'title': 'Agriculture'
                   }
               ,'ru':
                   {'short': 'Gruzovik, с/х.'
                   ,'title': 'Сельское хозяйство'
                   }
               ,'de':
                   {'short': 'Gruzovik, landwirt.'
                   ,'title': 'Landwirtschaft'
                   }
               ,'es':
                   {'short': 'Gruzovik, agric.'
                   ,'title': 'Agricultura'
                   }
               ,'uk':
                   {'short': 'Gruzovik, с/г.'
                   ,'title': 'Сільське господарство'
                   }
               }
           ,'Gruzovik, ballist.':
               {'is_valid': False
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, ballist.'
                   ,'title': 'Ballistics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, бал.'
                   ,'title': 'Баллистика'
                   }
               ,'de':
                   {'short': 'Gruzovik, ballist.'
                   ,'title': 'Ballistics'
                   }
               ,'es':
                   {'short': 'Gruzovik, ballist.'
                   ,'title': 'Ballistics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, баліст.'
                   ,'title': 'Балістика'
                   }
               }
           ,'Gruzovik, biogeogr.':
               {'is_valid': False
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, biogeogr.'
                   ,'title': 'Biogeography'
                   }
               ,'ru':
                   {'short': 'Gruzovik, биогеогр.'
                   ,'title': 'Биогеография'
                   }
               ,'de':
                   {'short': 'Gruzovik, biogeogr.'
                   ,'title': 'Biogeography'
                   }
               ,'es':
                   {'short': 'Gruzovik, biogeogr.'
                   ,'title': 'Biogeography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, біогеогр.'
                   ,'title': 'Біогеографія'
                   }
               }
           ,'Gruzovik, bot.':
               {'is_valid': False
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, bot.'
                   ,'title': 'Botany'
                   }
               ,'ru':
                   {'short': 'Gruzovik, бот.'
                   ,'title': 'Ботаника'
                   }
               ,'de':
                   {'short': 'Gruzovik, Bot.'
                   ,'title': 'Botanik'
                   }
               ,'es':
                   {'short': 'Gruzovik, bot.'
                   ,'title': 'Botánica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, бот.'
                   ,'title': 'Ботаніка'
                   }
               }
           ,'Gruzovik, cloth.':
               {'is_valid': False
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'ru':
                   {'short': 'Gruzovik, одеж.'
                   ,'title': 'Одежда'
                   }
               ,'de':
                   {'short': 'Gruzovik, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'es':
                   {'short': 'Gruzovik, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'Gruzovik, comp.':
               {'is_valid': False
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, comp.'
                   ,'title': 'Computing'
                   }
               ,'ru':
                   {'short': 'Gruzovik, комп.'
                   ,'title': 'Компьютеры'
                   }
               ,'de':
                   {'short': 'Gruzovik, Comp.'
                   ,'title': 'Computertechnik'
                   }
               ,'es':
                   {'short': 'Gruzovik, comp.'
                   ,'title': 'Computadores'
                   }
               ,'uk':
                   {'short': 'Gruzovik, комп.'
                   ,'title': "Комп'ютери"}}, 'Gruzovik, cryptogr.':
               {'is_valid': False
               ,'major_en': 'Security systems'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'ru':
                   {'short': 'Gruzovik, криптогр.'
                   ,'title': 'Криптография'
                   }
               ,'de':
                   {'short': 'Gruzovik, cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'es':
                   {'short': 'Gruzovik, cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, крипт.'
                   ,'title': 'Криптографія'
                   }
               }
           ,'Gruzovik, dial.':
               {'is_valid': False
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, dial.'
                   ,'title': 'Dialectal'
                   }
               ,'ru':
                   {'short': 'Gruzovik, диал.'
                   ,'title': 'Диалектизм'
                   }
               ,'de':
                   {'short': 'Gruzovik, Dial.'
                   ,'title': 'Dialekt'
                   }
               ,'es':
                   {'short': 'Gruzovik, dial.'
                   ,'title': 'Dialecto'
                   }
               ,'uk':
                   {'short': 'Gruzovik, діал.'
                   ,'title': 'Діалектизм'
                   }
               }
           ,'Gruzovik, econ.':
               {'is_valid': False
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, econ.'
                   ,'title': 'Economy'
                   }
               ,'ru':
                   {'short': 'Gruzovik, эк.'
                   ,'title': 'Экономика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Wirtsch.'
                   ,'title': 'Wirtschaft'
                   }
               ,'es':
                   {'short': 'Gruzovik, econ.'
                   ,'title': 'Economía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ек.'
                   ,'title': 'Економіка'
                   }
               }
           ,'Gruzovik, el.':
               {'is_valid': False
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, el.'
                   ,'title': 'Electronics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, эл.'
                   ,'title': 'Электроника'
                   }
               ,'de':
                   {'short': 'Gruzovik, el.'
                   ,'title': 'Elektronik'
                   }
               ,'es':
                   {'short': 'Gruzovik, electr.'
                   ,'title': 'Electrónica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ел.'
                   ,'title': 'Електроніка'
                   }
               }
           ,'Gruzovik, electric.':
               {'is_valid': False
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, electric.'
                   ,'title': 'Electricity'
                   }
               ,'ru':
                   {'short': 'Gruzovik, электрич.'
                   ,'title': 'Электричество'
                   }
               ,'de':
                   {'short': 'Gruzovik, electric.'
                   ,'title': 'Electricity'
                   }
               ,'es':
                   {'short': 'Gruzovik, electric.'
                   ,'title': 'Electricity'
                   }
               ,'uk':
                   {'short': 'Gruzovik, електр.'
                   ,'title': 'Електричний струм'
                   }
               }
           ,'Gruzovik, email':
               {'is_valid': False
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, email'
                   ,'title': 'E-mail'
                   }
               ,'ru':
                   {'short': 'Gruzovik, эл.почт.'
                   ,'title': 'Электронная почта'
                   }
               ,'de':
                   {'short': 'Gruzovik, E-Mail'
                   ,'title': 'E-Mail'
                   }
               ,'es':
                   {'short': 'Gruzovik, email'
                   ,'title': 'E-mail'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ел.пошт.'
                   ,'title': 'Електронна пошта'
                   }
               }
           ,'Gruzovik, expl.':
               {'is_valid': False
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, expl.'
                   ,'title': 'Explosives'
                   }
               ,'ru':
                   {'short': 'Gruzovik, ВВ.'
                   ,'title': 'Взрывчатые вещества'
                   }
               ,'de':
                   {'short': 'Gruzovik, expl.'
                   ,'title': 'Explosives'
                   }
               ,'es':
                   {'short': 'Gruzovik, expl.'
                   ,'title': 'Explosives'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вибух.'
                   ,'title': 'Вибухові речовини'
                   }
               }
           ,'Gruzovik, fig.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, fig.'
                   ,'title': 'Figurative'
                   }
               ,'ru':
                   {'short': 'Gruzovik, перен.'
                   ,'title': 'Переносный смысл'
                   }
               ,'de':
                   {'short': 'Gruzovik, übertr.'
                   ,'title': 'übertragen'
                   }
               ,'es':
                   {'short': 'Gruzovik, fig.'
                   ,'title': 'Figuradamente'
                   }
               ,'uk':
                   {'short': 'Gruzovik, перен.'
                   ,'title': 'Переносний сенс'
                   }
               }
           ,'Gruzovik, footwear':
               {'is_valid': False
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, footwear'
                   ,'title': 'Footwear'
                   }
               ,'ru':
                   {'short': 'Gruzovik, обув.'
                   ,'title': 'Обувь'
                   }
               ,'de':
                   {'short': 'Gruzovik, footwear'
                   ,'title': 'Footwear'
                   }
               ,'es':
                   {'short': 'Gruzovik, footwear'
                   ,'title': 'Footwear'
                   }
               ,'uk':
                   {'short': 'Gruzovik, взут.'
                   ,'title': 'Взуття'
                   }
               }
           ,'Gruzovik, fr.':
               {'is_valid': False
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, fr.'
                   ,'title': 'French'
                   }
               ,'ru':
                   {'short': 'Gruzovik, фр.'
                   ,'title': 'Французский язык'
                   }
               ,'de':
                   {'short': 'Gruzovik, Franz. Sp.'
                   ,'title': 'Französisch'
                   }
               ,'es':
                   {'short': 'Gruzovik, fr.'
                   ,'title': 'Francés'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фр.'
                   ,'title': 'Французька мова'
                   }
               }
           ,'Gruzovik, garden.':
               {'is_valid': False
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, garden.'
                   ,'title': 'Gardening'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сад.'
                   ,'title': 'Садоводство'
                   }
               ,'de':
                   {'short': 'Gruzovik, Garten.'
                   ,'title': 'Gartenarbeit'
                   }
               ,'es':
                   {'short': 'Gruzovik, garden.'
                   ,'title': 'Gardening'
                   }
               ,'uk':
                   {'short': 'Gruzovik, садівн.'
                   ,'title': 'Садівництво'
                   }
               }
           ,'Gruzovik, glac.':
               {'is_valid': False
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, glac.'
                   ,'title': 'Glaciology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, гляц.'
                   ,'title': 'Гляциология'
                   }
               ,'de':
                   {'short': 'Gruzovik, glac.'
                   ,'title': 'Glaciology'
                   }
               ,'es':
                   {'short': 'Gruzovik, glac.'
                   ,'title': 'Glaciology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, гляц.'
                   ,'title': 'Гляціологія'
                   }
               }
           ,'Gruzovik, horse.breed.':
               {'is_valid': False
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'ru':
                   {'short': 'Gruzovik, кон.'
                   ,'title': 'Коневодство'
                   }
               ,'de':
                   {'short': 'Gruzovik, horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'es':
                   {'short': 'Gruzovik, horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'uk':
                   {'short': 'Gruzovik, кон.'
                   ,'title': 'Конярство'
                   }
               }
           ,'Gruzovik, hunt.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, hunt.'
                   ,'title': 'Hunting'
                   }
               ,'ru':
                   {'short': 'Gruzovik, охот.'
                   ,'title': 'Охота и охотоведение'
                   }
               ,'de':
                   {'short': 'Gruzovik, Jagd.'
                   ,'title': 'Jagd'
                   }
               ,'es':
                   {'short': 'Gruzovik, caza'
                   ,'title': 'Caza y cinegética'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мислив.'
                   ,'title': 'Мисливство та мисливствознавство'
                   }
               }
           ,'Gruzovik, inform.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, inform.'
                   ,'title': 'Informal'
                   }
               ,'ru':
                   {'short': 'Gruzovik, разг.'
                   ,'title': 'Разговорная лексика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Umg.'
                   ,'title': 'Umgangssprache'
                   }
               ,'es':
                   {'short': 'Gruzovik, inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'Gruzovik, розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'Gruzovik, law':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, law'
                   ,'title': 'Law'
                   }
               ,'ru':
                   {'short': 'Gruzovik, юр.'
                   ,'title': 'Юридическая лексика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Recht.'
                   ,'title': 'Recht'
                   }
               ,'es':
                   {'short': 'Gruzovik, jur.'
                   ,'title': 'Jurídico'
                   }
               ,'uk':
                   {'short': 'Gruzovik, юр.'
                   ,'title': 'Юридична лексика'
                   }
               }
           ,'Gruzovik, mach.mech.':
               {'is_valid': False
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mach.mech.'
                   ,'title': 'Machinery and mechanisms'
                   }
               ,'ru':
                   {'short': 'Gruzovik, маш.мех.'
                   ,'title': 'Машины и механизмы'
                   }
               ,'de':
                   {'short': 'Gruzovik, mach.mech.'
                   ,'title': 'Machinery and mechanisms'
                   }
               ,'es':
                   {'short': 'Gruzovik, mach.mech.'
                   ,'title': 'Machinery and mechanisms'
                   }
               ,'uk':
                   {'short': 'Gruzovik, маш.мех.'
                   ,'title': 'Машини та механізми'
                   }
               }
           ,'Gruzovik, magn.':
               {'is_valid': False
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, magn.'
                   ,'title': 'Magnetics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, магн.'
                   ,'title': 'Магнетизм'
                   }
               ,'de':
                   {'short': 'Gruzovik, Magnet.'
                   ,'title': 'Magnetismus'
                   }
               ,'es':
                   {'short': 'Gruzovik, magn.'
                   ,'title': 'Magnetics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, магн.'
                   ,'title': 'Магнетизм'
                   }
               }
           ,'Gruzovik, math.':
               {'is_valid': False
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, math.'
                   ,'title': 'Mathematics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, мат.'
                   ,'title': 'Математика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Math.'
                   ,'title': 'Mathematik'
                   }
               ,'es':
                   {'short': 'Gruzovik, mat.'
                   ,'title': 'Matemáticas'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мат.'
                   ,'title': 'Математика'
                   }
               }
           ,'Gruzovik, med.':
               {'is_valid': False
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, med.'
                   ,'title': 'Medical'
                   }
               ,'ru':
                   {'short': 'Gruzovik, мед.'
                   ,'title': 'Медицина'
                   }
               ,'de':
                   {'short': 'Gruzovik, Med.'
                   ,'title': 'Medizin'
                   }
               ,'es':
                   {'short': 'Gruzovik, med.'
                   ,'title': 'Medicina'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мед.'
                   ,'title': 'Медицина'
                   }
               }
           ,'Gruzovik, media.':
               {'is_valid': False
               ,'major_en': 'Mass media'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, media.'
                   ,'title': 'Mass media'
                   }
               ,'ru':
                   {'short': 'Gruzovik, СМИ.'
                   ,'title': 'Средства массовой информации'
                   }
               ,'de':
                   {'short': 'Gruzovik, Massenmed.'
                   ,'title': 'Massenmedien'
                   }
               ,'es':
                   {'short': 'Gruzovik, media.'
                   ,'title': 'Mass media'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ЗМІ'
                   ,'title': 'Засоби масової інформації'
                   }
               }
           ,'Gruzovik, met.phys.':
               {'is_valid': False
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, met.phys.'
                   ,'title': 'Metal physics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, физ.мет.'
                   ,'title': 'Физика металлов'
                   }
               ,'de':
                   {'short': 'Gruzovik, Metphsk.'
                   ,'title': 'Metallphysik'
                   }
               ,'es':
                   {'short': 'Gruzovik, met.phys.'
                   ,'title': 'Metal physics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фіз.мет.'
                   ,'title': 'Фізика металів'
                   }
               }
           ,'Gruzovik, mil.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mil.'
                   ,'title': 'Military'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен.'
                   ,'title': 'Военный термин'
                   }
               ,'de':
                   {'short': 'Gruzovik, Mil.'
                   ,'title': 'Militär'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'Gruzovik, mil., air.def.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mil., air.def.'
                   ,'title': 'Air defense'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен., ПВО.'
                   ,'title': 'Противовоздушная оборона'
                   }
               ,'de':
                   {'short': 'Gruzovik, mil., air.def.'
                   ,'title': 'Air defense'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil., air.def.'
                   ,'title': 'Air defense'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., ППО'
                   ,'title': 'Протиповітряна оборона'
                   }
               }
           ,'Gruzovik, mil., arm.veh.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен., брон.'
                   ,'title': 'Бронетехника'
                   }
               ,'de':
                   {'short': 'Gruzovik, mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., брон.'
                   ,'title': 'Бронетехніка'
                   }
               }
           ,'Gruzovik, mil., artil.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mil., artil.'
                   ,'title': 'Artillery'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен., арт.'
                   ,'title': 'Артиллерия'
                   }
               ,'de':
                   {'short': 'Gruzovik, Artil.'
                   ,'title': 'Artillerie'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil.,artill.'
                   ,'title': 'Artillería'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., арт.'
                   ,'title': 'Артилерія'
                   }
               }
           ,'Gruzovik, mil., avia.':
               {'is_valid': False
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен., авиац.'
                   ,'title': 'Военная авиация'
                   }
               ,'de':
                   {'short': 'Gruzovik, mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., авіац.'
                   ,'title': 'Військова авіація'
                   }
               }
           ,'Gruzovik, mycol.':
               {'is_valid': False
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, mycol.'
                   ,'title': 'Mycology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, микол.'
                   ,'title': 'Микология'
                   }
               ,'de':
                   {'short': 'Gruzovik, mycol.'
                   ,'title': 'Mycology'
                   }
               ,'es':
                   {'short': 'Gruzovik, mycol.'
                   ,'title': 'Mycology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мікол.'
                   ,'title': 'Мікологія'
                   }
               }
           ,'Gruzovik, myth.':
               {'is_valid': False
               ,'major_en': 'Mythology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, myth.'
                   ,'title': 'Mythology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, миф.'
                   ,'title': 'Мифология'
                   }
               ,'de':
                   {'short': 'Gruzovik, Myth.'
                   ,'title': 'Mythologie'
                   }
               ,'es':
                   {'short': 'Gruzovik, mitol.'
                   ,'title': 'Mitología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, міф.'
                   ,'title': 'Міфологія'
                   }
               }
           ,'Gruzovik, nautic.':
               {'is_valid': False
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, nautic.'
                   ,'title': 'Nautical'
                   }
               ,'ru':
                   {'short': 'Gruzovik, мор.'
                   ,'title': 'Морской термин'
                   }
               ,'de':
                   {'short': 'Gruzovik, Mar.'
                   ,'title': 'Marine'
                   }
               ,'es':
                   {'short': 'Gruzovik, náut.'
                   ,'title': 'Náutico'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мор.'
                   ,'title': 'Морський термін'
                   }
               }
           ,'Gruzovik, obs.':
               {'is_valid': False
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, obs.'
                   ,'title': 'Obsolete / dated'
                   }
               ,'ru':
                   {'short': 'Gruzovik, уст.'
                   ,'title': 'Устаревшее'
                   }
               ,'de':
                   {'short': 'Gruzovik, veralt.'
                   ,'title': 'Veraltet'
                   }
               ,'es':
                   {'short': 'Gruzovik, antic.'
                   ,'title': 'Anticuado'
                   }
               ,'uk':
                   {'short': 'Gruzovik, застар.'
                   ,'title': 'Застаріле'
                   }
               }
           ,'Gruzovik, ocean.':
               {'is_valid': False
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'ru':
                   {'short': 'Gruzovik, океан.'
                   ,'title': 'Океанология (океанография)'
                   }
               ,'de':
                   {'short': 'Gruzovik, Ozeanogr.'
                   ,'title': 'Ozeanographie'
                   }
               ,'es':
                   {'short': 'Gruzovik, ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'uk':
                   {'short': 'Gruzovik, океан.'
                   ,'title': 'Океанологія (океанографія)'
                   }
               }
           ,'Gruzovik, paraglid.':
               {'is_valid': False
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, paraglid.'
                   ,'title': 'Paragliding'
                   }
               ,'ru':
                   {'short': 'Gruzovik, параплан.'
                   ,'title': 'Парапланеризм'
                   }
               ,'de':
                   {'short': 'Gruzovik, paraglid.'
                   ,'title': 'Paragliding'
                   }
               ,'es':
                   {'short': 'Gruzovik, paraglid.'
                   ,'title': 'Paragliding'
                   }
               ,'uk':
                   {'short': 'Gruzovik, параплан.'
                   ,'title': 'Парапланеризм'
                   }
               }
           ,'Gruzovik, philolog.':
               {'is_valid': False
               ,'major_en': 'Philology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, philolog.'
                   ,'title': 'Philology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, филол.'
                   ,'title': 'Филология'
                   }
               ,'de':
                   {'short': 'Gruzovik, Philol.'
                   ,'title': 'Philologie'
                   }
               ,'es':
                   {'short': 'Gruzovik, philolog.'
                   ,'title': 'Philology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, філол.'
                   ,'title': 'Філологія'
                   }
               }
           ,'Gruzovik, phonet.':
               {'is_valid': False
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, phonet.'
                   ,'title': 'Phonetics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, фон.'
                   ,'title': 'Фонетика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Phonet.'
                   ,'title': 'Phonetik'
                   }
               ,'es':
                   {'short': 'Gruzovik, fonét.'
                   ,'title': 'Fonética'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фон.'
                   ,'title': 'Фонетика'
                   }
               }
           ,'Gruzovik, photo.':
               {'is_valid': False
               ,'major_en': 'Photography'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, photo.'
                   ,'title': 'Photography'
                   }
               ,'ru':
                   {'short': 'Gruzovik, фото.'
                   ,'title': 'Фотография'
                   }
               ,'de':
                   {'short': 'Gruzovik, Foto.'
                   ,'title': 'Foto'
                   }
               ,'es':
                   {'short': 'Gruzovik, fotogr.'
                   ,'title': 'Fotografía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фото'
                   ,'title': 'Фотографія'
                   }
               }
           ,'Gruzovik, poetic':
               {'is_valid': False
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, poetic'
                   ,'title': 'Poetic'
                   }
               ,'ru':
                   {'short': 'Gruzovik, поэт.'
                   ,'title': 'Поэтический язык'
                   }
               ,'de':
                   {'short': 'Gruzovik, Poet.'
                   ,'title': 'Poetisch'
                   }
               ,'es':
                   {'short': 'Gruzovik, poét.'
                   ,'title': 'Poético'
                   }
               ,'uk':
                   {'short': 'Gruzovik, поет.'
                   ,'title': 'Поетична мова'
                   }
               }
           ,'Gruzovik, polit.':
               {'is_valid': False
               ,'major_en': 'Politics'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, polit.'
                   ,'title': 'Politics'
                   }
               ,'ru':
                   {'short': 'Gruzovik, полит.'
                   ,'title': 'Политика'
                   }
               ,'de':
                   {'short': 'Gruzovik, Polit.'
                   ,'title': 'Politik'
                   }
               ,'es':
                   {'short': 'Gruzovik, polít.'
                   ,'title': 'Política'
                   }
               ,'uk':
                   {'short': 'Gruzovik, політ.'
                   ,'title': 'Політика'
                   }
               }
           ,'Gruzovik, polygr.':
               {'is_valid': False
               ,'major_en': 'Publishing'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, polygr.'
                   ,'title': 'Polygraphy'
                   }
               ,'ru':
                   {'short': 'Gruzovik, полигр.'
                   ,'title': 'Полиграфия'
                   }
               ,'de':
                   {'short': 'Gruzovik, Polygr.'
                   ,'title': 'Polygraphie'
                   }
               ,'es':
                   {'short': 'Gruzovik, poligr.'
                   ,'title': 'Poligrafía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, полігр.'
                   ,'title': 'Поліграфія'
                   }
               }
           ,'Gruzovik, prof.jarg.':
               {'is_valid': False
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, prof.jarg.'
                   ,'title': 'Professional jargon'
                   }
               ,'ru':
                   {'short': 'Gruzovik, проф.жарг.'
                   ,'title': 'Профессиональный жаргон'
                   }
               ,'de':
                   {'short': 'Gruzovik, Fachj.'
                   ,'title': 'Fachjargon'
                   }
               ,'es':
                   {'short': 'Gruzovik, profesion.'
                   ,'title': 'Jerga profesional'
                   }
               ,'uk':
                   {'short': 'Gruzovik, проф.жарг.'
                   ,'title': 'Професійний жаргон'
                   }
               }
           ,'Gruzovik, prop.&figur.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'ru':
                   {'short': 'Gruzovik, прям.перен.'
                   ,'title': 'Прямой и переносный смысл'
                   }
               ,'de':
                   {'short': 'Gruzovik, prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'es':
                   {'short': 'Gruzovik, prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'uk':
                   {'short': 'Gruzovik, прям.перен.'
                   ,'title': 'Прямий і переносний сенс'
                   }
               }
           ,'Gruzovik, radio':
               {'is_valid': False
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, radio'
                   ,'title': 'Radio'
                   }
               ,'ru':
                   {'short': 'Gruzovik, радио.'
                   ,'title': 'Радио'
                   }
               ,'de':
                   {'short': 'Gruzovik, Radio.'
                   ,'title': 'Radio'
                   }
               ,'es':
                   {'short': 'Gruzovik, radio'
                   ,'title': 'Radio'
                   }
               ,'uk':
                   {'short': 'Gruzovik, радіо'
                   ,'title': 'Радіо'
                   }
               }
           ,'Gruzovik, rel., jud.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, rel., jud.'
                   ,'title': 'Judaism'
                   }
               ,'ru':
                   {'short': 'Gruzovik, рел., иуд.'
                   ,'title': 'Иудаизм'
                   }
               ,'de':
                   {'short': 'Gruzovik, rel., jud.'
                   ,'title': 'Judaism'
                   }
               ,'es':
                   {'short': 'Gruzovik, rel., jud.'
                   ,'title': 'Judaism'
                   }
               ,'uk':
                   {'short': 'Gruzovik, юд.'
                   ,'title': 'Юдаїзм'
                   }
               }
           ,'Gruzovik, row.':
               {'is_valid': False
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, row.'
                   ,'title': 'Rowing'
                   }
               ,'ru':
                   {'short': 'Gruzovik, греб.'
                   ,'title': 'Гребной спорт'
                   }
               ,'de':
                   {'short': 'Gruzovik, row.'
                   ,'title': 'Rowing'
                   }
               ,'es':
                   {'short': 'Gruzovik, row.'
                   ,'title': 'Rowing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, весл.'
                   ,'title': 'Веслування'
                   }
               }
           ,'Gruzovik, sail.':
               {'is_valid': False
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, sail.'
                   ,'title': 'Sailing'
                   }
               ,'ru':
                   {'short': 'Gruzovik, парусн.сп.'
                   ,'title': 'Парусный спорт'
                   }
               ,'de':
                   {'short': 'Gruzovik, sail.'
                   ,'title': 'Sailing'
                   }
               ,'es':
                   {'short': 'Gruzovik, sail.'
                   ,'title': 'Sailing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вітр.спорт'
                   ,'title': 'Вітрильний спорт'
                   }
               }
           ,'Gruzovik, scient.':
               {'is_valid': False
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, scient.'
                   ,'title': 'Scientific'
                   }
               ,'ru':
                   {'short': 'Gruzovik, науч.'
                   ,'title': 'Научный термин'
                   }
               ,'de':
                   {'short': 'Gruzovik, Wissensch.'
                   ,'title': 'Wissenschaftlicher Ausdruck'
                   }
               ,'es':
                   {'short': 'Gruzovik, scient.'
                   ,'title': 'Scientific'
                   }
               ,'uk':
                   {'short': 'Gruzovik, науков.'
                   ,'title': 'Науковий термін'
                   }
               }
           ,'Gruzovik, sculp.':
               {'is_valid': False
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, sculp.'
                   ,'title': 'Sculpture'
                   }
               ,'ru':
                   {'short': 'Gruzovik, скульп.'
                   ,'title': 'Скульптура'
                   }
               ,'de':
                   {'short': 'Gruzovik, sculp.'
                   ,'title': 'Sculpture'
                   }
               ,'es':
                   {'short': 'Gruzovik, sculp.'
                   ,'title': 'Sculpture'
                   }
               ,'uk':
                   {'short': 'Gruzovik, скульп.'
                   ,'title': 'Скульптура'
                   }
               }
           ,'Gruzovik, slang':
               {'is_valid': False
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, slang'
                   ,'title': 'Slang'
                   }
               ,'ru':
                   {'short': 'Gruzovik, сл.'
                   ,'title': 'Сленг'
                   }
               ,'de':
                   {'short': 'Gruzovik, Slang.'
                   ,'title': 'Slang'
                   }
               ,'es':
                   {'short': 'Gruzovik, jerg.'
                   ,'title': 'Jerga'
                   }
               ,'uk':
                   {'short': 'Gruzovik, сленг'
                   ,'title': 'Сленг'
                   }
               }
           ,'Gruzovik, slavon.':
               {'is_valid': False
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, slavon.'
                   ,'title': 'Slavonic'
                   }
               ,'ru':
                   {'short': 'Gruzovik, славянск.'
                   ,'title': 'Славянское выражение'
                   }
               ,'de':
                   {'short': 'Gruzovik, slavon.'
                   ,'title': 'Slavonic'
                   }
               ,'es':
                   {'short': 'Gruzovik, slavon.'
                   ,'title': 'Slavonic'
                   }
               ,'uk':
                   {'short': 'Gruzovik, слов’ян.'
                   ,'title': 'Слов’янський вираз'
                   }
               }
           ,'Gruzovik, social.sc.':
               {'is_valid': False
               ,'major_en': 'Education'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, social.sc.'
                   ,'title': 'Social science'
                   }
               ,'ru':
                   {'short': 'Gruzovik, обществ.'
                   ,'title': 'Обществоведение'
                   }
               ,'de':
                   {'short': 'Gruzovik, social.sc.'
                   ,'title': 'Social science'
                   }
               ,'es':
                   {'short': 'Gruzovik, social.sc.'
                   ,'title': 'Social science'
                   }
               ,'uk':
                   {'short': 'Gruzovik, суспільс.'
                   ,'title': 'Суспільствознавство'
                   }
               }
           ,'Gruzovik, spin.':
               {'is_valid': False
               ,'major_en': 'Crafts'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, spin.'
                   ,'title': 'Spinning'
                   }
               ,'ru':
                   {'short': 'Gruzovik, пряд.'
                   ,'title': 'Прядение'
                   }
               ,'de':
                   {'short': 'Gruzovik, spin.'
                   ,'title': 'Spinning'
                   }
               ,'es':
                   {'short': 'Gruzovik, spin.'
                   ,'title': 'Spinning'
                   }
               ,'uk':
                   {'short': 'Gruzovik, пряд.'
                   ,'title': 'Прядіння'
                   }
               }
           ,'Gruzovik, sport.':
               {'is_valid': False
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, sport.'
                   ,'title': 'Sports'
                   }
               ,'ru':
                   {'short': 'Gruzovik, спорт.'
                   ,'title': 'Спорт'
                   }
               ,'de':
                   {'short': 'Gruzovik, Sport.'
                   ,'title': 'Sport'
                   }
               ,'es':
                   {'short': 'Gruzovik, dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'Gruzovik, спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'Gruzovik, sport.goods':
               {'is_valid': False
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, sport.goods'
                   ,'title': 'Sporting goods'
                   }
               ,'ru':
                   {'short': 'Gruzovik, спорт.тов.'
                   ,'title': 'Спорттовары'
                   }
               ,'de':
                   {'short': 'Gruzovik, sport.goods'
                   ,'title': 'Sporting goods'
                   }
               ,'es':
                   {'short': 'Gruzovik, sport.goods'
                   ,'title': 'Sporting goods'
                   }
               ,'uk':
                   {'short': 'Gruzovik, спорт.тов.'
                   ,'title': 'Спорттовари'
                   }
               }
           ,'Gruzovik, surv.':
               {'is_valid': False
               ,'major_en': 'Sociology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, surv.'
                   ,'title': 'Survey'
                   }
               ,'ru':
                   {'short': 'Gruzovik, соц.опр.'
                   ,'title': 'Социологический опрос'
                   }
               ,'de':
                   {'short': 'Gruzovik, surv.'
                   ,'title': 'Survey'
                   }
               ,'es':
                   {'short': 'Gruzovik, surv.'
                   ,'title': 'Survey'
                   }
               ,'uk':
                   {'short': 'Gruzovik, соц.опит.'
                   ,'title': 'Соціологічне опитування'
                   }
               }
           ,'Gruzovik, tech.':
               {'is_valid': False
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, tech.'
                   ,'title': 'Technology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, тех.'
                   ,'title': 'Техника'
                   }
               ,'de':
                   {'short': 'Gruzovik, Tech.'
                   ,'title': 'Technik'
                   }
               ,'es':
                   {'short': 'Gruzovik, tec.'
                   ,'title': 'Tecnología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, техн.'
                   ,'title': 'Техніка'
                   }
               }
           ,'Gruzovik, tel.':
               {'is_valid': False
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, tel.'
                   ,'title': 'Telephony'
                   }
               ,'ru':
                   {'short': 'Gruzovik, тлф.'
                   ,'title': 'Телефония'
                   }
               ,'de':
                   {'short': 'Gruzovik, Telef.'
                   ,'title': 'Telefonie'
                   }
               ,'es':
                   {'short': 'Gruzovik, tel.'
                   ,'title': 'Telephony'
                   }
               ,'uk':
                   {'short': 'Gruzovik, тлф.'
                   ,'title': 'Телефонія'
                   }
               }
           ,'Gruzovik, terat.':
               {'is_valid': False
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, terat.'
                   ,'title': 'Teratology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, терат.'
                   ,'title': 'Тератология'
                   }
               ,'de':
                   {'short': 'Gruzovik, Teratol.'
                   ,'title': 'Teratologie'
                   }
               ,'es':
                   {'short': 'Gruzovik, terat.'
                   ,'title': 'Teratología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, терат.'
                   ,'title': 'Тератологія'
                   }
               }
           ,'Gruzovik, topogr.':
               {'is_valid': False
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, topogr.'
                   ,'title': 'Topography'
                   }
               ,'ru':
                   {'short': 'Gruzovik, топогр.'
                   ,'title': 'Топография'
                   }
               ,'de':
                   {'short': 'Gruzovik, Topogr.'
                   ,'title': 'Topographie'
                   }
               ,'es':
                   {'short': 'Gruzovik, topogr.'
                   ,'title': 'Topografía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, топ.'
                   ,'title': 'Топографія'
                   }
               }
           ,'Gruzovik, typewrit.':
               {'is_valid': False
               ,'major_en': 'Records management'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, typewrit.'
                   ,'title': 'Typewriters and typewriting'
                   }
               ,'ru':
                   {'short': 'Gruzovik, пиш.маш.'
                   ,'title': 'Пишущие машинки, машинопись'
                   }
               ,'de':
                   {'short': 'Gruzovik, typewrit.'
                   ,'title': 'Typewriters and typewriting'
                   }
               ,'es':
                   {'short': 'Gruzovik, typewrit.'
                   ,'title': 'Typewriters and typewriting'
                   }
               ,'uk':
                   {'short': 'Gruzovik, друк.маш.'
                   ,'title': 'Друкарські машинки та машинопис'
                   }
               }
           ,'Gruzovik, vent.':
               {'is_valid': False
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, vent.'
                   ,'title': 'Ventilation'
                   }
               ,'ru':
                   {'short': 'Gruzovik, вент.'
                   ,'title': 'Вентиляция'
                   }
               ,'de':
                   {'short': 'Gruzovik, vent.'
                   ,'title': 'Ventilation'
                   }
               ,'es':
                   {'short': 'Gruzovik, vent.'
                   ,'title': 'Ventilation'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вент.'
                   ,'title': 'Вентиляція'
                   }
               }
           ,'Gruzovik, weav.':
               {'is_valid': False
               ,'major_en': 'Crafts'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, weav.'
                   ,'title': 'Weaving'
                   }
               ,'ru':
                   {'short': 'Gruzovik, ткач.'
                   ,'title': 'Ткачество'
                   }
               ,'de':
                   {'short': 'Gruzovik, weav.'
                   ,'title': 'Weaving'
                   }
               ,'es':
                   {'short': 'Gruzovik, weav.'
                   ,'title': 'Weaving'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ткац.'
                   ,'title': 'Ткацтво'
                   }
               }
           ,'Gruzovik, written':
               {'is_valid': False
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, written'
                   ,'title': 'Written'
                   }
               ,'ru':
                   {'short': 'Gruzovik, письм.'
                   ,'title': 'Письменная речь'
                   }
               ,'de':
                   {'short': 'Gruzovik, written'
                   ,'title': 'Written'
                   }
               ,'es':
                   {'short': 'Gruzovik, written'
                   ,'title': 'Written'
                   }
               ,'uk':
                   {'short': 'Gruzovik, письм.'
                   ,'title': 'Письмове мовлення'
                   }
               }
           ,'Gruzovik, zool.':
               {'is_valid': False
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'Gruzovik, zool.'
                   ,'title': 'Zoology'
                   }
               ,'ru':
                   {'short': 'Gruzovik, зоол.'
                   ,'title': 'Зоология'
                   }
               ,'de':
                   {'short': 'Gruzovik, Zool.'
                   ,'title': 'Zoologie'
                   }
               ,'es':
                   {'short': 'Gruzovik, zool.'
                   ,'title': 'Zoología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, зоол.'
                   ,'title': 'Зоологія'
                   }
               }
           ,'Guatem.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Guatem.'
                   ,'title': 'Guatemala'
                   }
               ,'ru':
                   {'short': 'Гват.'
                   ,'title': 'Гватемала'
                   }
               ,'de':
                   {'short': 'Guatem.'
                   ,'title': 'Guatemala'
                   }
               ,'es':
                   {'short': 'Guatem.'
                   ,'title': 'Guatemala'
                   }
               ,'uk':
                   {'short': 'Гват.'
                   ,'title': 'Гватемала'
                   }
               }
           ,'HF.electr.':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'HF.electr.'
                   ,'title': 'High frequency electronics'
                   }
               ,'ru':
                   {'short': 'ВЧ.эл.'
                   ,'title': 'Высокочастотная электроника'
                   }
               ,'de':
                   {'short': 'HF.electr.'
                   ,'title': 'High frequency electronics'
                   }
               ,'es':
                   {'short': 'HF.electr.'
                   ,'title': 'High frequency electronics'
                   }
               ,'uk':
                   {'short': 'ВЧ.ел.'
                   ,'title': 'Високочастотна електроніка'
                   }
               }
           ,'HR':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'HR'
                   ,'title': 'Human resources'
                   }
               ,'ru':
                   {'short': 'кадр.'
                   ,'title': 'Кадры'
                   }
               ,'de':
                   {'short': 'HR'
                   ,'title': 'Human resources'
                   }
               ,'es':
                   {'short': 'HR'
                   ,'title': 'Human resources'
                   }
               ,'uk':
                   {'short': 'кадри'
                   ,'title': 'Кадри'
                   }
               }
           ,'IMF.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'IMF.'
                   ,'title': 'International Monetary Fund'
                   }
               ,'ru':
                   {'short': 'МВФ.'
                   ,'title': 'Международный валютный фонд'
                   }
               ,'de':
                   {'short': 'IMF.'
                   ,'title': 'International Monetary Fund'
                   }
               ,'es':
                   {'short': 'IMF.'
                   ,'title': 'International Monetary Fund'
                   }
               ,'uk':
                   {'short': 'МВФ'
                   ,'title': 'Міжнародний валютний фонд'
                   }
               }
           ,'IT':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'IT'
                   ,'title': 'Information technology'
                   }
               ,'ru':
                   {'short': 'ИТ.'
                   ,'title': 'Информационные технологии'
                   }
               ,'de':
                   {'short': 'IT'
                   ,'title': 'Informationstechnik'
                   }
               ,'es':
                   {'short': 'IT'
                   ,'title': 'Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'IT'
                   ,'title': 'Інформаційні технології'
                   }
               }
           ,'India':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'India'
                   ,'title': 'India'
                   }
               ,'ru':
                   {'short': 'инд.'
                   ,'title': 'Индия'
                   }
               ,'de':
                   {'short': 'India'
                   ,'title': 'India'
                   }
               ,'es':
                   {'short': 'India'
                   ,'title': 'India'
                   }
               ,'uk':
                   {'short': 'Індія'
                   ,'title': 'Індія'
                   }
               }
           ,'Indones.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'Indones.'
                   ,'title': 'Indonesian'
                   }
               ,'ru':
                   {'short': 'индонез.'
                   ,'title': 'Индонезийское выражение'
                   }
               ,'de':
                   {'short': 'Indones.'
                   ,'title': 'Indonesian'
                   }
               ,'es':
                   {'short': 'Indones.'
                   ,'title': 'Indonesian'
                   }
               ,'uk':
                   {'short': 'індонез.'
                   ,'title': 'Індонезійський вираз'
                   }
               }
           ,'Iran':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Iran'
                   ,'title': 'Iran'
                   }
               ,'ru':
                   {'short': 'Иран.'
                   ,'title': 'Иран'
                   }
               ,'de':
                   {'short': 'Iran.'
                   ,'title': 'Iran'
                   }
               ,'es':
                   {'short': 'Iran'
                   ,'title': 'Iran'
                   }
               ,'uk':
                   {'short': 'Іран'
                   ,'title': 'Іран'
                   }
               }
           ,'Kazakh.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Kazakh.'
                   ,'title': 'Kazakhstan'
                   }
               ,'ru':
                   {'short': 'Казах.'
                   ,'title': 'Казахстан'
                   }
               ,'de':
                   {'short': 'Kazakh.'
                   ,'title': 'Kazakhstan'
                   }
               ,'es':
                   {'short': 'Kazakh.'
                   ,'title': 'Kazakhstan'
                   }
               ,'uk':
                   {'short': 'Казах.'
                   ,'title': 'Казахстан'
                   }
               }
           ,'Kyrgyz.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Kyrgyz.'
                   ,'title': 'Kyrgyzstan'
                   }
               ,'ru':
                   {'short': 'Кыргыз.'
                   ,'title': 'Кыргызстан'
                   }
               ,'de':
                   {'short': 'Kyrgyz.'
                   ,'title': 'Kyrgyzstan'
                   }
               ,'es':
                   {'short': 'Kyrgyz.'
                   ,'title': 'Kyrgyzstan'
                   }
               ,'uk':
                   {'short': 'Киргиз.'
                   ,'title': 'Киргизстан'
                   }
               }
           ,'LP.play.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'LP.play.'
                   ,'title': 'LP players'
                   }
               ,'ru':
                   {'short': 'проигр.вин.'
                   ,'title': 'Проигрыватели виниловых дисков'
                   }
               ,'de':
                   {'short': 'LP.play.'
                   ,'title': 'LP players'
                   }
               ,'es':
                   {'short': 'LP.play.'
                   ,'title': 'LP players'
                   }
               ,'uk':
                   {'short': 'прогр.вініл.'
                   ,'title': 'Програвачі вінілових дисків'
                   }
               }
           ,'MSDS':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'MSDS'
                   ,'title': 'Material safety data sheet'
                   }
               ,'ru':
                   {'short': 'ПБВ.'
                   ,'title': 'Паспорт безопасности вещества'
                   }
               ,'de':
                   {'short': 'MSDS'
                   ,'title': 'Material-Sicherheitsdatenblatt'
                   }
               ,'es':
                   {'short': 'MSDS'
                   ,'title': 'Material safety data sheet'
                   }
               ,'uk':
                   {'short': 'ПБР'
                   ,'title': 'Паспорт безпеки речовини'
                   }
               }
           ,'Makarov.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Makarov.'
                   ,'title': 'Makarov'
                   }
               ,'ru':
                   {'short': 'Макаров.'
                   ,'title': 'Макаров'
                   }
               ,'de':
                   {'short': 'Makarow.'
                   ,'title': 'Makarow'
                   }
               ,'es':
                   {'short': 'Makarov.'
                   ,'title': 'Makarov'
                   }
               ,'uk':
                   {'short': 'Макаров'
                   ,'title': 'Макаров'
                   }
               }
           ,'Makarov., inform., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Makarov., inform., amer.usg.'
                   ,'title': 'Makarov, Informal, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'Макаров., разг., амер.'
                   ,'title': 'Макаров, Разговорная лексика, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Makarow., Umg., Amerik.'
                   ,'title': 'Makarow, Umgangssprache, Amerikanisch'
                   }
               ,'es':
                   {'short': 'Makarov., inf., amer.'
                   ,'title': 'Makarov, Informal, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'Макаров, розмовн., амер.вир.'
                   ,'title': 'Макаров, Розмовна лексика, Американський вираз (не варыант мови)'
                   }
               }
           ,'Moroc.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Moroc.'
                   ,'title': 'Morocco'
                   }
               ,'ru':
                   {'short': 'Марок.'
                   ,'title': 'Марокко'
                   }
               ,'de':
                   {'short': 'Moroc.'
                   ,'title': 'Morocco'
                   }
               ,'es':
                   {'short': 'Moroc.'
                   ,'title': 'Morocco'
                   }
               ,'uk':
                   {'short': 'Марок.'
                   ,'title': 'Марокко'
                   }
               }
           ,'N.Ireland.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'N.Ireland.'
                   ,'title': 'Northern Ireland'
                   }
               ,'ru':
                   {'short': 'сев.ирл.'
                   ,'title': 'Северная Ирландия'
                   }
               ,'de':
                   {'short': 'N.Ireland.'
                   ,'title': 'Northern Ireland'
                   }
               ,'es':
                   {'short': 'N.Ireland.'
                   ,'title': 'Northern Ireland'
                   }
               ,'uk':
                   {'short': 'Півн.Ірл.'
                   ,'title': 'Північна Ірландія'
                   }
               }
           ,'NASA':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'NASA'
                   ,'title': 'NASA'
                   }
               ,'ru':
                   {'short': 'НАСА.'
                   ,'title': 'НАСА'
                   }
               ,'de':
                   {'short': 'NASA.'
                   ,'title': 'NASA'
                   }
               ,'es':
                   {'short': 'NASA'
                   ,'title': 'NASA'
                   }
               ,'uk':
                   {'short': 'НАСА'
                   ,'title': 'НАСА'
                   }
               }
           ,'NATO':
               {'is_valid': True
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'NATO'
                   ,'title': 'NATO'
                   }
               ,'ru':
                   {'short': 'НАТО.'
                   ,'title': 'НАТО'
                   }
               ,'de':
                   {'short': 'NATO'
                   ,'title': 'NATO'
                   }
               ,'es':
                   {'short': 'NATO'
                   ,'title': 'NATO'
                   }
               ,'uk':
                   {'short': 'НАТО'
                   ,'title': 'НАТО'
                   }
               }
           ,'NGO':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'NGO'
                   ,'title': 'Non-governmental organizations'
                   }
               ,'ru':
                   {'short': 'общ.орг.'
                   ,'title': 'Общественные организации'
                   }
               ,'de':
                   {'short': 'NGO'
                   ,'title': 'Non-governmental organizations'
                   }
               ,'es':
                   {'short': 'NGO'
                   ,'title': 'Non-governmental organizations'
                   }
               ,'uk':
                   {'short': 'гром.орг.'
                   ,'title': 'Громадські організації'
                   }
               }
           ,'NYSE.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'NYSE.'
                   ,'title': 'New York Stock Exchange'
                   }
               ,'ru':
                   {'short': 'NYSE.'
                   ,'title': 'Нью-Йоркская фондовая биржа'
                   }
               ,'de':
                   {'short': 'NYSE.'
                   ,'title': 'New York Stock Exchange'
                   }
               ,'es':
                   {'short': 'NYSE.'
                   ,'title': 'New York Stock Exchange'
                   }
               ,'uk':
                   {'short': 'NYSE'
                   ,'title': 'Нью-Йоркська фондова біржа'
                   }
               }
           ,'Nasdaq':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'Nasdaq'
                   ,'title': 'NASDAQ'
                   }
               ,'ru':
                   {'short': 'Nasdaq.'
                   ,'title': 'NASDAQ'
                   }
               ,'de':
                   {'short': 'Nasdaq'
                   ,'title': 'NASDAQ'
                   }
               ,'es':
                   {'short': 'Nasdaq'
                   ,'title': 'NASDAQ'
                   }
               ,'uk':
                   {'short': 'НАСДАК'
                   ,'title': 'НАСДАК'
                   }
               }
           ,'Netherl., law, court':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Netherl., law, court'
                   ,'title': 'Netherlands, Court (law)'
                   }
               ,'ru':
                   {'short': 'Нидерл., юр., суд.'
                   ,'title': 'Нидерланды, Судебная лексика'
                   }
               ,'de':
                   {'short': 'Netherl., law, court'
                   ,'title': 'Netherlands, Court (law)'
                   }
               ,'es':
                   {'short': 'Netherl., law, court'
                   ,'title': 'Netherlands, Court (law)'
                   }
               ,'uk':
                   {'short': 'Нідерл., юр., суд.'
                   ,'title': 'Нідерланди, Судова лексика'
                   }
               }
           ,'O&G':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': True
               ,'en':
                   {'short': 'O&G'
                   ,'title': 'Oil and gas'
                   }
               ,'ru':
                   {'short': 'нефт.газ.'
                   ,'title': 'Нефть и газ'
                   }
               ,'de':
                   {'short': 'O&G'
                   ,'title': 'Oil and gas'
                   }
               ,'es':
                   {'short': 'O&G'
                   ,'title': 'Oil and gas'
                   }
               ,'uk':
                   {'short': 'нафт.газ'
                   ,'title': 'Нафта і газ'
                   }
               }
           ,'O&G, casp.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, casp.'
                   ,'title': 'Caspian'
                   }
               ,'ru':
                   {'short': 'нефт.газ., касп.'
                   ,'title': 'Каспий'
                   }
               ,'de':
                   {'short': 'O&G, casp.'
                   ,'title': 'Caspian'
                   }
               ,'es':
                   {'short': 'O&G, casp.'
                   ,'title': 'Caspian'
                   }
               ,'uk':
                   {'short': 'нафт.газ., касп.'
                   ,'title': 'Каспій'
                   }
               }
           ,'O&G, karach.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, karach.'
                   ,'title': 'Karachaganak'
                   }
               ,'ru':
                   {'short': 'нефт.газ., карач.'
                   ,'title': 'Карачаганак'
                   }
               ,'de':
                   {'short': 'O&G, karach.'
                   ,'title': 'Karachaganak'
                   }
               ,'es':
                   {'short': 'O&G, karach.'
                   ,'title': 'Karachaganak'
                   }
               ,'uk':
                   {'short': 'нафт.газ., карач.'
                   ,'title': 'Карачаганак'
                   }
               }
           ,'O&G, molikpaq.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, molikpaq.'
                   ,'title': 'Molikpaq'
                   }
               ,'ru':
                   {'short': 'нефт.газ., моликп.'
                   ,'title': 'Моликпак'
                   }
               ,'de':
                   {'short': 'O&G, molikpaq.'
                   ,'title': 'Molikpaq'
                   }
               ,'es':
                   {'short': 'O&G, molikpaq.'
                   ,'title': 'Molikpaq'
                   }
               ,'uk':
                   {'short': 'нафт.газ., молікп.'
                   ,'title': 'Молікпак'
                   }
               }
           ,'O&G, oilfield.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, oilfield.'
                   ,'title': 'Oilfields'
                   }
               ,'ru':
                   {'short': 'нефтепром.'
                   ,'title': 'Нефтепромысловый'
                   }
               ,'de':
                   {'short': 'Erdölind.'
                   ,'title': 'Erdölindustrie'
                   }
               ,'es':
                   {'short': 'O&G, oilfield.'
                   ,'title': 'Oilfields'
                   }
               ,'uk':
                   {'short': 'нафтопром.'
                   ,'title': 'Нафтопромисловий'
                   }
               }
           ,'O&G, sahk.r.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, sahk.r.'
                   ,'title': 'Sakhalin R'
                   }
               ,'ru':
                   {'short': 'нефт.газ., сахал.р.'
                   ,'title': 'Сахалин Р'
                   }
               ,'de':
                   {'short': 'Sachal.R'
                   ,'title': 'Sachalin R'
                   }
               ,'es':
                   {'short': 'O&G, sahk.r.'
                   ,'title': 'Sakhalin R'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.р.'
                   ,'title': 'Сахалін Р'
                   }
               }
           ,'O&G, sahk.s.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, sahk.s.'
                   ,'title': 'Sakhalin S'
                   }
               ,'ru':
                   {'short': 'нефт.газ., сахал.ю.'
                   ,'title': 'Сахалин Ю'
                   }
               ,'de':
                   {'short': 'Sachal.Yu'
                   ,'title': 'Sachalin Yu'
                   }
               ,'es':
                   {'short': 'O&G, sahk.s.'
                   ,'title': 'Sakhalin S'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.ю.'
                   ,'title': 'Сахалін Ю'
                   }
               }
           ,'O&G, sakh.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, sakh.'
                   ,'title': 'Sakhalin'
                   }
               ,'ru':
                   {'short': 'нефт.газ., сахал.'
                   ,'title': 'Сахалин'
                   }
               ,'de':
                   {'short': 'Sachal.'
                   ,'title': 'Sachalin'
                   }
               ,'es':
                   {'short': 'O&G, sakh.'
                   ,'title': 'Sakhalin'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.'
                   ,'title': 'Сахалін'
                   }
               }
           ,'O&G, sakh., geol.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, sakh., geol.'
                   ,'title': 'Sakhalin, Geology'
                   }
               ,'ru':
                   {'short': 'нефт.газ., сахал., геол.'
                   ,'title': 'Сахалин, Геология'
                   }
               ,'de':
                   {'short': 'Sachal., Geol.'
                   ,'title': 'Sachalin, Geologie'
                   }
               ,'es':
                   {'short': 'O&G, sakh., geol.'
                   ,'title': 'Sakhalin, Geología'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал., геолог.'
                   ,'title': 'Сахалін, Геологія'
                   }
               }
           ,'O&G, sakh.a.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, sakh.a.'
                   ,'title': 'Sakhalin A'
                   }
               ,'ru':
                   {'short': 'нефт.газ., сахал.а.'
                   ,'title': 'Сахалин А'
                   }
               ,'de':
                   {'short': 'SachalA'
                   ,'title': 'Sachalin A'
                   }
               ,'es':
                   {'short': 'O&G, sakh.a.'
                   ,'title': 'Sakhalin A'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.а.'
                   ,'title': 'Сахалін А'
                   }
               }
           ,'O&G, tengiz.':
               {'is_valid': False
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G, tengiz.'
                   ,'title': 'Tengiz'
                   }
               ,'ru':
                   {'short': 'нефт.газ., тенгиз.'
                   ,'title': 'Тенгизшевройл'
                   }
               ,'de':
                   {'short': 'O&G, tengiz.'
                   ,'title': 'Tengiz'
                   }
               ,'es':
                   {'short': 'O&G, tengiz.'
                   ,'title': 'Tengiz'
                   }
               ,'uk':
                   {'short': 'нафт.газ., тенгіз.'
                   ,'title': 'Тенгізшевройл'
                   }
               }
           ,'O&G. tech.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'O&G. tech.'
                   ,'title': 'Oil and gas technology'
                   }
               ,'ru':
                   {'short': 'нефт.газ.тех.'
                   ,'title': 'Нефтегазовая техника'
                   }
               ,'de':
                   {'short': 'Öl- u. Gastechnik'
                   ,'title': 'Erdöl- und Erdgastechnik'
                   }
               ,'es':
                   {'short': 'O&G. tech.'
                   ,'title': 'Oil and gas technology'
                   }
               ,'uk':
                   {'short': 'нафт.газ.тех.'
                   ,'title': 'Нафтогазова техніка'
                   }
               }
           ,'OHS':
               {'is_valid': True
               ,'major_en': 'Occupational health & safety'
               ,'is_major': True
               ,'en':
                   {'short': 'OHS'
                   ,'title': 'Occupational health & safety'
                   }
               ,'ru':
                   {'short': 'ОТиТБ.'
                   ,'title': 'Охрана труда и техника безопасности'
                   }
               ,'de':
                   {'short': 'Arb.schutz'
                   ,'title': 'Arbeitsschutz'
                   }
               ,'es':
                   {'short': 'OHS'
                   ,'title': 'Occupational health & safety'
                   }
               ,'uk':
                   {'short': 'ОПіТБ'
                   ,'title': 'Охорона праці та техніка безпеки'
                   }
               }
           ,'PCB':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'PCB'
                   ,'title': 'Printed circuit boards'
                   }
               ,'ru':
                   {'short': 'печ.плат.'
                   ,'title': 'Печатные платы'
                   }
               ,'de':
                   {'short': 'PCB'
                   ,'title': 'Printed circuit boards'
                   }
               ,'es':
                   {'short': 'PCB'
                   ,'title': 'Printed circuit boards'
                   }
               ,'uk':
                   {'short': 'друк.пл.'
                   ,'title': 'Друковані плати'
                   }
               }
           ,'PPE':
               {'is_valid': True
               ,'major_en': 'Occupational health & safety'
               ,'is_major': False
               ,'en':
                   {'short': 'PPE'
                   ,'title': 'Personal protective equipment'
                   }
               ,'ru':
                   {'short': 'ср.защ.'
                   ,'title': 'Средства индивидуальной защиты'
                   }
               ,'de':
                   {'short': 'PPE'
                   ,'title': 'Personal protective equipment'
                   }
               ,'es':
                   {'short': 'PPE'
                   ,'title': 'Personal protective equipment'
                   }
               ,'uk':
                   {'short': 'зас.зах.'
                   ,'title': 'Засоби індивідуального захисту'
                   }
               }
           ,'PR':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'PR'
                   ,'title': 'Public relations'
                   }
               ,'ru':
                   {'short': 'пиар.'
                   ,'title': 'Паблик рилейшнз'
                   }
               ,'de':
                   {'short': 'PR'
                   ,'title': 'Public relations'
                   }
               ,'es':
                   {'short': 'PR'
                   ,'title': 'Public relations'
                   }
               ,'uk':
                   {'short': 'піар.'
                   ,'title': 'Паблік рілейшнз'
                   }
               }
           ,'PSP':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'PSP'
                   ,'title': 'Power system protection'
                   }
               ,'ru':
                   {'short': 'РЗА'
                   ,'title': 'Релейная защита и автоматика'
                   }
               ,'de':
                   {'short': 'PSP'
                   ,'title': 'Power system protection'
                   }
               ,'es':
                   {'short': 'PSP'
                   ,'title': 'Power system protection'
                   }
               ,'uk':
                   {'short': 'РЗА'
                   ,'title': 'Релейний захист і автоматика'
                   }
               }
           ,'Panam.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Panam.'
                   ,'title': 'Panama'
                   }
               ,'ru':
                   {'short': 'Панам.'
                   ,'title': 'Панама'
                   }
               ,'de':
                   {'short': 'Panam.'
                   ,'title': 'Panama'
                   }
               ,'es':
                   {'short': 'Panam.'
                   ,'title': 'Panama'
                   }
               ,'uk':
                   {'short': 'Панама'
                   ,'title': 'Панама'
                   }
               }
           ,'Peru.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Peru.'
                   ,'title': 'Peru'
                   }
               ,'ru':
                   {'short': 'Перу.'
                   ,'title': 'Перу'
                   }
               ,'de':
                   {'short': 'Peru.'
                   ,'title': 'Peru'
                   }
               ,'es':
                   {'short': 'Peru.'
                   ,'title': 'Peru'
                   }
               ,'uk':
                   {'short': 'Перу'
                   ,'title': 'Перу'
                   }
               }
           ,'Philipp.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Philipp.'
                   ,'title': 'Philippines'
                   }
               ,'ru':
                   {'short': 'Фил.'
                   ,'title': 'Филиппины'
                   }
               ,'de':
                   {'short': 'Philipp.'
                   ,'title': 'Philippines'
                   }
               ,'es':
                   {'short': 'Philipp.'
                   ,'title': 'Philippines'
                   }
               ,'uk':
                   {'short': 'Філ.'
                   ,'title': 'Філіппіни'
                   }
               }
           ,'R&D.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'R&D.'
                   ,'title': 'Research and development'
                   }
               ,'ru':
                   {'short': 'науч.-ис.'
                   ,'title': 'Научно-исследовательская деятельность'
                   }
               ,'de':
                   {'short': 'R&D.'
                   ,'title': 'Research and development'
                   }
               ,'es':
                   {'short': 'R&D.'
                   ,'title': 'Research and development'
                   }
               ,'uk':
                   {'short': 'наук.-досл.'
                   ,'title': 'Науково-дослідницька діяльність'
                   }
               }
           ,'Russia':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Russia'
                   ,'title': 'Russia'
                   }
               ,'ru':
                   {'short': 'Россия.'
                   ,'title': 'Россия'
                   }
               ,'de':
                   {'short': 'Russl.'
                   ,'title': 'Russland'
                   }
               ,'es':
                   {'short': 'Russia'
                   ,'title': 'Russia'
                   }
               ,'uk':
                   {'short': 'Росія'
                   ,'title': 'Росія'
                   }
               }
           ,'S.Amer.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'S.Amer.'
                   ,'title': 'South America'
                   }
               ,'ru':
                   {'short': 'Юж.Ам.'
                   ,'title': 'Южная Америка'
                   }
               ,'de':
                   {'short': 'S.Amer.'
                   ,'title': 'South America'
                   }
               ,'es':
                   {'short': 'S.Amer.'
                   ,'title': 'South America'
                   }
               ,'uk':
                   {'short': 'Півд.Ам.'
                   ,'title': 'Південна Америка'
                   }
               }
           ,'SAP.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'SAP.'
                   ,'title': 'SAP'
                   }
               ,'ru':
                   {'short': 'SAP.'
                   ,'title': 'SAP'
                   }
               ,'de':
                   {'short': 'SAP.'
                   ,'title': 'SAP'
                   }
               ,'es':
                   {'short': 'SAP.'
                   ,'title': 'SAP'
                   }
               ,'uk':
                   {'short': 'SAP'
                   ,'title': 'SAP'
                   }
               }
           ,'SAP.fin.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'SAP.fin.'
                   ,'title': 'SAP finance'
                   }
               ,'ru':
                   {'short': 'SAP.фин.'
                   ,'title': 'SAP финансы'
                   }
               ,'de':
                   {'short': 'SAP.fin.'
                   ,'title': 'SAP finance'
                   }
               ,'es':
                   {'short': 'SAP.fin.'
                   ,'title': 'SAP finance'
                   }
               ,'uk':
                   {'short': 'SAP фін.'
                   ,'title': 'SAP фінанси'
                   }
               }
           ,'SAP.tech.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'SAP.tech.'
                   ,'title': 'SAP tech.'
                   }
               ,'ru':
                   {'short': 'SAP.тех.'
                   ,'title': 'SAP технические термины'
                   }
               ,'de':
                   {'short': 'SAP.tech.'
                   ,'title': 'SAP tech.'
                   }
               ,'es':
                   {'short': 'SAP.tech.'
                   ,'title': 'SAP tech.'
                   }
               ,'uk':
                   {'short': 'SAP тех.'
                   ,'title': 'SAP технічні терміни'
                   }
               }
           ,'Scotl.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Scotl.'
                   ,'title': 'Scotland'
                   }
               ,'ru':
                   {'short': 'Шотл.'
                   ,'title': 'Шотландия'
                   }
               ,'de':
                   {'short': 'Schottl.'
                   ,'title': 'Schottland'
                   }
               ,'es':
                   {'short': 'Escoc.'
                   ,'title': 'Escocia'
                   }
               ,'uk':
                   {'short': 'Шотл.'
                   ,'title': 'Шотландія'
                   }
               }
           ,'Spain':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Spain'
                   ,'title': 'Spain'
                   }
               ,'ru':
                   {'short': 'Испан.'
                   ,'title': 'Испания'
                   }
               ,'de':
                   {'short': 'Spa.'
                   ,'title': 'Spanien'
                   }
               ,'es':
                   {'short': 'Spain'
                   ,'title': 'Spain'
                   }
               ,'uk':
                   {'short': 'Іспан.'
                   ,'title': 'Іспанія'
                   }
               }
           ,'TV':
               {'is_valid': True
               ,'major_en': 'Mass media'
               ,'is_major': False
               ,'en':
                   {'short': 'TV'
                   ,'title': 'Television'
                   }
               ,'ru':
                   {'short': 'тлв.'
                   ,'title': 'Телевидение'
                   }
               ,'de':
                   {'short': 'TV'
                   ,'title': 'Fernsehen'
                   }
               ,'es':
                   {'short': 'TV'
                   ,'title': 'Televisión'
                   }
               ,'uk':
                   {'short': 'тлб.'
                   ,'title': 'Телебачення'
                   }
               }
           ,'UK':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'UK'
                   ,'title': 'United Kingdom'
                   }
               ,'ru':
                   {'short': 'Брит.'
                   ,'title': 'Великобритания'
                   }
               ,'de':
                   {'short': 'UK'
                   ,'title': 'United Kingdom'
                   }
               ,'es':
                   {'short': 'UK'
                   ,'title': 'United Kingdom'
                   }
               ,'uk':
                   {'short': 'Брит.'
                   ,'title': 'Велика Британія'
                   }
               }
           ,'UN':
               {'is_valid': True
               ,'major_en': 'United Nations'
               ,'is_major': True
               ,'en':
                   {'short': 'UN'
                   ,'title': 'United Nations'
                   }
               ,'ru':
                   {'short': 'ООН.'
                   ,'title': 'ООН (Организация Объединенных Наций)'
                   }
               ,'de':
                   {'short': 'UN'
                   ,'title': 'United Nations'
                   }
               ,'es':
                   {'short': 'UN'
                   ,'title': 'United Nations'
                   }
               ,'uk':
                   {'short': 'ООН'
                   ,'title': "Організація Об'єднаних Націй"}}, 'USA':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'USA'
                   ,'title': 'United States'
                   }
               ,'ru':
                   {'short': 'США.'
                   ,'title': 'США'
                   }
               ,'de':
                   {'short': 'USA'
                   ,'title': 'United States'
                   }
               ,'es':
                   {'short': 'USA'
                   ,'title': 'United States'
                   }
               ,'uk':
                   {'short': 'США'
                   ,'title': 'Сполучені Штати Америки'
                   }
               }
           ,'Ukraine':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Ukraine'
                   ,'title': 'Ukraine'
                   }
               ,'ru':
                   {'short': 'Украина.'
                   ,'title': 'Украина'
                   }
               ,'de':
                   {'short': 'Ukraine'
                   ,'title': 'Ukraine'
                   }
               ,'es':
                   {'short': 'Ukraine'
                   ,'title': 'Ukraine'
                   }
               ,'uk':
                   {'short': 'Україна'
                   ,'title': 'Україна'
                   }
               }
           ,'Venezuel.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'Venezuel.'
                   ,'title': 'Venezuela'
                   }
               ,'ru':
                   {'short': 'Венесуэл.'
                   ,'title': 'Венесуэла'
                   }
               ,'de':
                   {'short': 'Venezuel.'
                   ,'title': 'Venezuela'
                   }
               ,'es':
                   {'short': 'Venezuel.'
                   ,'title': 'Venezuela'
                   }
               ,'uk':
                   {'short': 'Венес.'
                   ,'title': 'Венесуела'
                   }
               }
           ,'WTO.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'WTO.'
                   ,'title': 'World trade organization'
                   }
               ,'ru':
                   {'short': 'ВТО.'
                   ,'title': 'Всемирная торговая организация'
                   }
               ,'de':
                   {'short': 'WTO.'
                   ,'title': 'World trade organization'
                   }
               ,'es':
                   {'short': 'WTO.'
                   ,'title': 'World trade organization'
                   }
               ,'uk':
                   {'short': 'СОТ'
                   ,'title': 'Світова організація торгівлі'
                   }
               }
           ,'abbr.':
               {'is_valid': True
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'abbr.'
                   ,'title': 'Abbreviation'
                   }
               ,'ru':
                   {'short': 'сокр.'
                   ,'title': 'Сокращение'
                   }
               ,'de':
                   {'short': 'Abkürz.'
                   ,'title': 'Abkürzung'
                   }
               ,'es':
                   {'short': 'abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'abbr., O&G, casp.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, casp.'
                   ,'title': 'Abbreviation, Caspian'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., касп.'
                   ,'title': 'Сокращение, Каспий'
                   }
               ,'de':
                   {'short': 'Abkürz., O&G, casp.'
                   ,'title': 'Abkürzung, Caspian'
                   }
               ,'es':
                   {'short': 'abrev., O&G, casp.'
                   ,'title': 'Abreviatura, Caspian'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., касп.'
                   ,'title': 'Абревіатура, Каспій'
                   }
               }
           ,'abbr., O&G, karach.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, karach.'
                   ,'title': 'Abbreviation, Karachaganak'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., карач.'
                   ,'title': 'Сокращение, Карачаганак'
                   }
               ,'de':
                   {'short': 'Abkürz., O&G, karach.'
                   ,'title': 'Abkürzung, Karachaganak'
                   }
               ,'es':
                   {'short': 'abrev., O&G, karach.'
                   ,'title': 'Abreviatura, Karachaganak'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., карач.'
                   ,'title': 'Абревіатура, Карачаганак'
                   }
               }
           ,'abbr., O&G, sahk.r.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, sahk.r.'
                   ,'title': 'Abbreviation, Sakhalin R'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., сахал.р.'
                   ,'title': 'Сокращение, Сахалин Р'
                   }
               ,'de':
                   {'short': 'Abkürz., Sachal.R'
                   ,'title': 'Abkürzung, Sachalin R'
                   }
               ,'es':
                   {'short': 'abrev., O&G, sahk.r.'
                   ,'title': 'Abreviatura, Sakhalin R'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.р.'
                   ,'title': 'Абревіатура, Сахалін Р'
                   }
               }
           ,'abbr., O&G, sahk.s.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, sahk.s.'
                   ,'title': 'Abbreviation, Sakhalin S'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., сахал.ю.'
                   ,'title': 'Сокращение, Сахалин Ю'
                   }
               ,'de':
                   {'short': 'Abkürz., Sachal.Yu'
                   ,'title': 'Abkürzung, Sachalin Yu'
                   }
               ,'es':
                   {'short': 'abrev., O&G, sahk.s.'
                   ,'title': 'Abreviatura, Sakhalin S'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.ю.'
                   ,'title': 'Абревіатура, Сахалін Ю'
                   }
               }
           ,'abbr., O&G, sakh.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, sakh.'
                   ,'title': 'Abbreviation, Sakhalin'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., сахал.'
                   ,'title': 'Сокращение, Сахалин'
                   }
               ,'de':
                   {'short': 'Abkürz., Sachal.'
                   ,'title': 'Abkürzung, Sachalin'
                   }
               ,'es':
                   {'short': 'abrev., O&G, sakh.'
                   ,'title': 'Abreviatura, Sakhalin'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.'
                   ,'title': 'Абревіатура, Сахалін'
                   }
               }
           ,'abbr., O&G, sakh.a.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., O&G, sakh.a.'
                   ,'title': 'Abbreviation, Sakhalin A'
                   }
               ,'ru':
                   {'short': 'сокр., нефт.газ., сахал.а.'
                   ,'title': 'Сокращение, Сахалин А'
                   }
               ,'de':
                   {'short': 'Abkürz., SachalA'
                   ,'title': 'Abkürzung, Sachalin A'
                   }
               ,'es':
                   {'short': 'abrev., O&G, sakh.a.'
                   ,'title': 'Abreviatura, Sakhalin A'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.а.'
                   ,'title': 'Абревіатура, Сахалін А'
                   }
               }
           ,'abbr., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., amer.usg.'
                   ,'title': 'Abbreviation, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'сокр., амер.'
                   ,'title': 'Сокращение, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Abkürz., Amerik.'
                   ,'title': 'Abkürzung, Amerikanisch'
                   }
               ,'es':
                   {'short': 'abrev., amer.'
                   ,'title': 'Abreviatura, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'абрев., амер.вир.'
                   ,'title': 'Абревіатура, Американський вираз (не варыант мови)'
                   }
               }
           ,'abbr., amer.usg., slang':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., amer.usg., slang'
                   ,'title': 'Abbreviation, American (usage, not AmE), Slang'
                   }
               ,'ru':
                   {'short': 'сокр., амер., сл.'
                   ,'title': 'Сокращение, Американское выражение (не вариант языка), Сленг'
                   }
               ,'de':
                   {'short': 'Abkürz., Amerik., Slang.'
                   ,'title': 'Abkürzung, Amerikanisch, Slang'
                   }
               ,'es':
                   {'short': 'abrev., amer., jerg.'
                   ,'title': 'Abreviatura, Americano (uso), Jerga'
                   }
               ,'uk':
                   {'short': 'абрев., амер.вир., сленг'
                   ,'title': 'Абревіатура, Американський вираз (не варыант мови), Сленг'
                   }
               }
           ,'abbr., avia., avia., ICAO':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., avia., avia., ICAO'
                   ,'title': 'Abbreviation, Aviation, ICAO'
                   }
               ,'ru':
                   {'short': 'сокр., авиац., авиац., ИКАО'
                   ,'title': 'Сокращение, Авиация, ИКАО'
                   }
               ,'de':
                   {'short': 'Abkürz., Luftf., ICAO'
                   ,'title': 'Abkürzung, Luftfahrt, ICAO'
                   }
               ,'es':
                   {'short': 'abrev., avia., avia., ICAO'
                   ,'title': 'Abreviatura, Aviación, ICAO'
                   }
               ,'uk':
                   {'short': 'абрев., авіац., авіац., ІКАО'
                   ,'title': 'Абревіатура, Авіація, ІКАО'
                   }
               }
           ,'abbr., avia., med.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., avia., med.'
                   ,'title': 'Abbreviation, Aviation medicine'
                   }
               ,'ru':
                   {'short': 'сокр., авиац., мед.'
                   ,'title': 'Сокращение, Авиационная медицина'
                   }
               ,'de':
                   {'short': 'Abkürz., Luft.med.'
                   ,'title': 'Abkürzung, Luftfahrtmedizin'
                   }
               ,'es':
                   {'short': 'abrev., avia., med.'
                   ,'title': 'Abreviatura, Aviation medicine'
                   }
               ,'uk':
                   {'short': 'абрев., авіац., мед.'
                   ,'title': 'Абревіатура, Авіаційна медицина'
                   }
               }
           ,'abbr., comp., MS':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., comp., MS'
                   ,'title': 'Abbreviation, Microsoft'
                   }
               ,'ru':
                   {'short': 'сокр., комп., Майкр.'
                   ,'title': 'Сокращение, Майкрософт'
                   }
               ,'de':
                   {'short': 'Abkürz., comp., MS'
                   ,'title': 'Abkürzung, Microsoft'
                   }
               ,'es':
                   {'short': 'abrev., comp., MS'
                   ,'title': 'Abreviatura, Microsoft'
                   }
               ,'uk':
                   {'short': 'абрев., комп., Майкр.'
                   ,'title': 'Абревіатура, Майкрософт'
                   }
               }
           ,'abbr., comp., net.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., comp., net.'
                   ,'title': 'Abbreviation, Computer networks'
                   }
               ,'ru':
                   {'short': 'сокр., комп., сет.'
                   ,'title': 'Сокращение, Компьютерные сети'
                   }
               ,'de':
                   {'short': 'Abkürz., Comp., Netzw.'
                   ,'title': 'Abkürzung, Computernetzwerke'
                   }
               ,'es':
                   {'short': 'abrev., comp., net.'
                   ,'title': 'Abreviatura, Computer networks'
                   }
               ,'uk':
                   {'short': 'абрев., комп., мереж.'
                   ,'title': "Абревіатура, Комп'ютерні мережі"}}, 'abbr., comp., net., IT':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., comp., net., IT'
                   ,'title': 'Abbreviation, Computer networks, Information technology'
                   }
               ,'ru':
                   {'short': 'сокр., комп., сет., ИТ.'
                   ,'title': 'Сокращение, Компьютерные сети, Информационные технологии'
                   }
               ,'de':
                   {'short': 'Abkürz., Comp., Netzw., IT'
                   ,'title': 'Abkürzung, Computernetzwerke, Informationstechnik'
                   }
               ,'es':
                   {'short': 'abrev., comp., net., IT'
                   ,'title': 'Abreviatura, Computer networks, Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'абрев., комп., мереж., IT'
                   ,'title': "Абревіатура, Комп'ютерні мережі, Інформаційні технології"}}, 'abbr., fant./sci-fi.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., fant./sci-fi.'
                   ,'title': 'Abbreviation, Fantasy and science fiction'
                   }
               ,'ru':
                   {'short': 'сокр., фант.'
                   ,'title': 'Сокращение, Фантастика, фэнтези'
                   }
               ,'de':
                   {'short': 'Abkürz., fant./sci-fi.'
                   ,'title': 'Abkürzung, Fantasy and science fiction'
                   }
               ,'es':
                   {'short': 'abrev., fant./sci-fi.'
                   ,'title': 'Abreviatura, Fantasy and science fiction'
                   }
               ,'uk':
                   {'short': 'абрев., фант.'
                   ,'title': 'Абревіатура, Фантастика, фентезі'
                   }
               }
           ,'abbr., law, ADR':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., law, ADR'
                   ,'title': 'Abbreviation, Alternative dispute resolution'
                   }
               ,'ru':
                   {'short': 'сокр., юр., АУС'
                   ,'title': 'Сокращение, Альтернативное урегулирование споров'
                   }
               ,'de':
                   {'short': 'Abkürz., law, ADR'
                   ,'title': 'Abkürzung, Alternative dispute resolution'
                   }
               ,'es':
                   {'short': 'abrev., jur.,SAC'
                   ,'title': 'Abreviatura, Solución alternativa de controversias'
                   }
               ,'uk':
                   {'short': 'абрев., юр., АВС'
                   ,'title': 'Абревіатура, Альтернативне врегулювання спорів'
                   }
               }
           ,'abbr., law, copyr.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., law, copyr.'
                   ,'title': 'Abbreviation, Copyright'
                   }
               ,'ru':
                   {'short': 'сокр., юр., автор.'
                   ,'title': 'Сокращение, Авторское право'
                   }
               ,'de':
                   {'short': 'Abkürz., Urheberrecht'
                   ,'title': 'Abkürzung, Urheberrecht'
                   }
               ,'es':
                   {'short': 'abrev., law, copyr.'
                   ,'title': 'Abreviatura, Copyright'
                   }
               ,'uk':
                   {'short': 'абрев., юр., автор.'
                   ,'title': 'Абревіатура, Авторське право'
                   }
               }
           ,'abbr., mil., WMD':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., mil., WMD'
                   ,'title': 'Abbreviation, Weapons of mass destruction'
                   }
               ,'ru':
                   {'short': 'сокр., воен., ОМП.'
                   ,'title': 'Сокращение, Оружие массового поражения'
                   }
               ,'de':
                   {'short': 'Abkürz., mil., WMD'
                   ,'title': 'Abkürzung, Weapons of mass destruction'
                   }
               ,'es':
                   {'short': 'abrev., mil., WMD'
                   ,'title': 'Abreviatura, Weapons of mass destruction'
                   }
               ,'uk':
                   {'short': 'абрев., військ., ЗМУ'
                   ,'title': 'Абревіатура, Зброя масового ураження'
                   }
               }
           ,'abbr., mil., artil.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., mil., artil.'
                   ,'title': 'Abbreviation, Artillery'
                   }
               ,'ru':
                   {'short': 'сокр., воен., арт.'
                   ,'title': 'Сокращение, Артиллерия'
                   }
               ,'de':
                   {'short': 'Abkürz., Artil.'
                   ,'title': 'Abkürzung, Artillerie'
                   }
               ,'es':
                   {'short': 'abrev., mil.,artill.'
                   ,'title': 'Abreviatura, Artillería'
                   }
               ,'uk':
                   {'short': 'абрев., військ., арт.'
                   ,'title': 'Абревіатура, Артилерія'
                   }
               }
           ,'abbr., mil., navy':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., mil., navy'
                   ,'title': 'Abbreviation, Navy'
                   }
               ,'ru':
                   {'short': 'сокр., воен., мор.'
                   ,'title': 'Сокращение, Военно-морской флот'
                   }
               ,'de':
                   {'short': 'Abkürz., mil., navy'
                   ,'title': 'Abkürzung, Navy'
                   }
               ,'es':
                   {'short': 'abrev., mil., navy'
                   ,'title': 'Abreviatura, Navy'
                   }
               ,'uk':
                   {'short': 'абрев., військ., мор.'
                   ,'title': 'Абревіатура, Військово-морський флот'
                   }
               }
           ,'abbr., patents.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., patents.'
                   ,'title': 'Abbreviation, Patents'
                   }
               ,'ru':
                   {'short': 'сокр., юр., пат.'
                   ,'title': 'Сокращение, Патенты'
                   }
               ,'de':
                   {'short': 'Abkürz., Patent.'
                   ,'title': 'Abkürzung, Patente'
                   }
               ,'es':
                   {'short': 'abrev., patents.'
                   ,'title': 'Abreviatura, Patents'
                   }
               ,'uk':
                   {'short': 'абрев., юр., пат.'
                   ,'title': 'Абревіатура, Патенти'
                   }
               }
           ,'abbr., sport, bask.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'abbr., sport, bask.'
                   ,'title': 'Abbreviation, Basketball'
                   }
               ,'ru':
                   {'short': 'сокр., баск.'
                   ,'title': 'Сокращение, Баскетбол'
                   }
               ,'de':
                   {'short': 'Abkürz., sport, bask.'
                   ,'title': 'Abkürzung, Basketball'
                   }
               ,'es':
                   {'short': 'abrev., sport, bask.'
                   ,'title': 'Abreviatura, Basketball'
                   }
               ,'uk':
                   {'short': 'абрев., спорт, баск.'
                   ,'title': 'Абревіатура, Баскетбол'
                   }
               }
           ,'account.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'account.'
                   ,'title': 'Accounting'
                   }
               ,'ru':
                   {'short': 'бухг.'
                   ,'title': 'Бухгалтерский учет (кроме аудита)'
                   }
               ,'de':
                   {'short': 'Buchhalt.'
                   ,'title': 'Buchhaltung'
                   }
               ,'es':
                   {'short': 'cont.'
                   ,'title': 'Contabilidad'
                   }
               ,'uk':
                   {'short': 'бухг.'
                   ,'title': 'Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'accum.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'accum.'
                   ,'title': 'Accumulators'
                   }
               ,'ru':
                   {'short': 'акк.'
                   ,'title': 'Аккумуляторы'
                   }
               ,'de':
                   {'short': 'accum.'
                   ,'title': 'Accumulators'
                   }
               ,'es':
                   {'short': 'accum.'
                   ,'title': 'Accumulators'
                   }
               ,'uk':
                   {'short': 'акум.'
                   ,'title': 'Акумулятори'
                   }
               }
           ,'acoust.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'acoust.'
                   ,'title': 'Acoustics'
                   }
               ,'ru':
                   {'short': 'акуст.'
                   ,'title': 'Акустика (раздел физики)'
                   }
               ,'de':
                   {'short': 'Akus.'
                   ,'title': 'Akustik'
                   }
               ,'es':
                   {'short': 'acoust.'
                   ,'title': 'Acoustics'
                   }
               ,'uk':
                   {'short': 'акуст.'
                   ,'title': 'Акустика'
                   }
               }
           ,'acrid.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'acrid.'
                   ,'title': 'Acridology'
                   }
               ,'ru':
                   {'short': 'акрид.'
                   ,'title': 'Акридология'
                   }
               ,'de':
                   {'short': 'acrid.'
                   ,'title': 'Acridology'
                   }
               ,'es':
                   {'short': 'acrid.'
                   ,'title': 'Acridology'
                   }
               ,'uk':
                   {'short': 'акрід.'
                   ,'title': 'Акрідологія'
                   }
               }
           ,'acrob.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'acrob.'
                   ,'title': 'Acrobatics'
                   }
               ,'ru':
                   {'short': 'акроб.'
                   ,'title': 'Акробатика'
                   }
               ,'de':
                   {'short': 'acrob.'
                   ,'title': 'Acrobatics'
                   }
               ,'es':
                   {'short': 'acrob.'
                   ,'title': 'Acrobatics'
                   }
               ,'uk':
                   {'short': 'акроб.'
                   ,'title': 'Акробатика'
                   }
               }
           ,'acup.':
               {'is_valid': True
               ,'major_en': 'Medicine - Alternative medicine'
               ,'is_major': False
               ,'en':
                   {'short': 'acup.'
                   ,'title': 'Acupuncture'
                   }
               ,'ru':
                   {'short': 'акуп.'
                   ,'title': 'Акупунктура'
                   }
               ,'de':
                   {'short': 'acup.'
                   ,'title': 'Acupuncture'
                   }
               ,'es':
                   {'short': 'acup.'
                   ,'title': 'Acupuncture'
                   }
               ,'uk':
                   {'short': 'акуп.'
                   ,'title': 'Акупунктура'
                   }
               }
           ,'addit.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'addit.'
                   ,'title': 'Additive manufacturing & 3D printing'
                   }
               ,'ru':
                   {'short': 'аддит.'
                   ,'title': 'Аддитивные технологии и 3D-печать'
                   }
               ,'de':
                   {'short': 'addit.'
                   ,'title': 'Additive manufacturing & 3D printing'
                   }
               ,'es':
                   {'short': 'addit.'
                   ,'title': 'Additive manufacturing & 3D printing'
                   }
               ,'uk':
                   {'short': 'адит.тех.'
                   ,'title': 'Адитивні технології та 3D-друк'
                   }
               }
           ,'adm.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'ru':
                   {'short': 'админ.прав.'
                   ,'title': 'Административное право'
                   }
               ,'de':
                   {'short': 'adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'es':
                   {'short': 'adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'uk':
                   {'short': 'адмін.пр.'
                   ,'title': 'Адміністративне право'
                   }
               }
           ,'admin.geo.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'admin.geo.'
                   ,'title': 'Administrative geography'
                   }
               ,'ru':
                   {'short': 'адм.дел.'
                   ,'title': 'Административное деление'
                   }
               ,'de':
                   {'short': 'admin.geo.'
                   ,'title': 'Administrative geography'
                   }
               ,'es':
                   {'short': 'admin.geo.'
                   ,'title': 'Administrative geography'
                   }
               ,'uk':
                   {'short': 'адм.под.'
                   ,'title': 'Адміністративний поділ'
                   }
               }
           ,'adv.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'adv.'
                   ,'title': 'Advertising'
                   }
               ,'ru':
                   {'short': 'рекл.'
                   ,'title': 'Реклама'
                   }
               ,'de':
                   {'short': 'Werb.'
                   ,'title': 'Werbung'
                   }
               ,'es':
                   {'short': 'adv.'
                   ,'title': 'Advertising'
                   }
               ,'uk':
                   {'short': 'рекл.'
                   ,'title': 'Реклама'
                   }
               }
           ,'aer.phot.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'ru':
                   {'short': 'аэрофот.'
                   ,'title': 'Аэрофотосъемка и топография'
                   }
               ,'de':
                   {'short': 'aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'es':
                   {'short': 'aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'uk':
                   {'short': 'аерофот.'
                   ,'title': 'Аерофозйомка та топографія'
                   }
               }
           ,'aerodyn.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'aerodyn.'
                   ,'title': 'Aerodynamics'
                   }
               ,'ru':
                   {'short': 'аэродин.'
                   ,'title': 'Аэродинамика'
                   }
               ,'de':
                   {'short': 'aerodyn.'
                   ,'title': 'Aerodynamics'
                   }
               ,'es':
                   {'short': 'aerodyn.'
                   ,'title': 'Aerodynamics'
                   }
               ,'uk':
                   {'short': 'аеродин.'
                   ,'title': 'Аеродинаміка'
                   }
               }
           ,'aerohydr.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'aerohydr.'
                   ,'title': 'Aerohydrodynamics'
                   }
               ,'ru':
                   {'short': 'аэрогидр.'
                   ,'title': 'Аэрогидродинамика'
                   }
               ,'de':
                   {'short': 'aerohydr.'
                   ,'title': 'Aerohydrodynamics'
                   }
               ,'es':
                   {'short': 'aerohydr.'
                   ,'title': 'Aerohydrodynamics'
                   }
               ,'uk':
                   {'short': 'аерогідр.'
                   ,'title': 'Аерогідродинаміка'
                   }
               }
           ,'aeron.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'aeron.'
                   ,'title': 'Aeronautics'
                   }
               ,'ru':
                   {'short': 'возд.'
                   ,'title': 'Воздухоплавание'
                   }
               ,'de':
                   {'short': 'Luftschiff.'
                   ,'title': 'Luftschifffahrt'
                   }
               ,'es':
                   {'short': 'aeron.'
                   ,'title': 'Aeronautics'
                   }
               ,'uk':
                   {'short': 'повітр.'
                   ,'title': 'Повітроплавання'
                   }
               }
           ,'affect.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'affect.'
                   ,'title': 'Affectionate'
                   }
               ,'ru':
                   {'short': 'ласкат.'
                   ,'title': 'Ласкательно'
                   }
               ,'de':
                   {'short': 'affect.'
                   ,'title': 'Affectionate'
                   }
               ,'es':
                   {'short': 'affect.'
                   ,'title': 'Affectionate'
                   }
               ,'uk':
                   {'short': 'пестл.'
                   ,'title': 'Пестливо'
                   }
               }
           ,'afghan.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'afghan.'
                   ,'title': 'Afghanistan'
                   }
               ,'ru':
                   {'short': 'афган.'
                   ,'title': 'Афганистан'
                   }
               ,'de':
                   {'short': 'afghan.'
                   ,'title': 'Afghanistan'
                   }
               ,'es':
                   {'short': 'afghan.'
                   ,'title': 'Afghanistan'
                   }
               ,'uk':
                   {'short': 'афган.'
                   ,'title': 'Афганістан'
                   }
               }
           ,'afr.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'afr.'
                   ,'title': 'Africa'
                   }
               ,'ru':
                   {'short': 'афр.'
                   ,'title': 'Африка'
                   }
               ,'de':
                   {'short': 'afr.'
                   ,'title': 'Africa'
                   }
               ,'es':
                   {'short': 'afr.'
                   ,'title': 'Africa'
                   }
               ,'uk':
                   {'short': 'афр.'
                   ,'title': 'Африка'
                   }
               }
           ,'african.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'african.'
                   ,'title': 'African'
                   }
               ,'ru':
                   {'short': 'африк.выр.'
                   ,'title': 'Африканское выражение'
                   }
               ,'de':
                   {'short': 'african.'
                   ,'title': 'African'
                   }
               ,'es':
                   {'short': 'african.'
                   ,'title': 'African'
                   }
               ,'uk':
                   {'short': 'афр.вир.'
                   ,'title': 'Африканський вираз'
                   }
               }
           ,'agr.':
               {'is_valid': False
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'agr.'
                   ,'title': 'Agronomy'
                   }
               ,'ru':
                   {'short': 'с/х., агр.'
                   ,'title': 'Агрономия'
                   }
               ,'de':
                   {'short': 'agr.'
                   ,'title': 'Agronomy'
                   }
               ,'es':
                   {'short': 'agr.'
                   ,'title': 'Agronomy'
                   }
               ,'uk':
                   {'short': 'агрон.'
                   ,'title': 'Агрономія'
                   }
               }
           ,'agric.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': True
               ,'en':
                   {'short': 'agric.'
                   ,'title': 'Agriculture'
                   }
               ,'ru':
                   {'short': 'с/х.'
                   ,'title': 'Сельское хозяйство'
                   }
               ,'de':
                   {'short': 'landwirt.'
                   ,'title': 'Landwirtschaft'
                   }
               ,'es':
                   {'short': 'agric.'
                   ,'title': 'Agricultura'
                   }
               ,'uk':
                   {'short': 'с/г.'
                   ,'title': 'Сільське господарство'
                   }
               }
           ,'agrochem.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'agrochem.'
                   ,'title': 'Agrochemistry'
                   }
               ,'ru':
                   {'short': 'агрохим.'
                   ,'title': 'Агрохимия'
                   }
               ,'de':
                   {'short': 'agrochem.'
                   ,'title': 'Agrochemistry'
                   }
               ,'es':
                   {'short': 'agrochem.'
                   ,'title': 'Agrochemistry'
                   }
               ,'uk':
                   {'short': 'агрохім.'
                   ,'title': 'Агрохімія'
                   }
               }
           ,'aikido.':
               {'is_valid': True
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': False
               ,'en':
                   {'short': 'aikido.'
                   ,'title': 'Aikido'
                   }
               ,'ru':
                   {'short': 'айкидо.'
                   ,'title': 'Айкидо'
                   }
               ,'de':
                   {'short': 'aikido.'
                   ,'title': 'Aikido'
                   }
               ,'es':
                   {'short': 'aikido.'
                   ,'title': 'Aikido'
                   }
               ,'uk':
                   {'short': 'айкідо.'
                   ,'title': 'Айкідо'
                   }
               }
           ,'airccon.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'airccon.'
                   ,'title': 'Air conditioners'
                   }
               ,'ru':
                   {'short': 'кондиц.'
                   ,'title': 'Кондиционеры'
                   }
               ,'de':
                   {'short': 'airccon.'
                   ,'title': 'Air conditioners'
                   }
               ,'es':
                   {'short': 'airccon.'
                   ,'title': 'Air conditioners'
                   }
               ,'uk':
                   {'short': 'кондиц.'
                   ,'title': 'Кондиціонери'
                   }
               }
           ,'airports':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'airports'
                   ,'title': 'Airports and air traffic control'
                   }
               ,'ru':
                   {'short': 'аэроп.'
                   ,'title': 'Аэропорты и управление водзушным движением'
                   }
               ,'de':
                   {'short': 'airports'
                   ,'title': 'Airports and air traffic control'
                   }
               ,'es':
                   {'short': 'airports'
                   ,'title': 'Airports and air traffic control'
                   }
               ,'uk':
                   {'short': 'аероп.'
                   ,'title': 'Аеропорти та керування повітряним рухом'
                   }
               }
           ,'airsh.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'airsh.'
                   ,'title': 'Airships'
                   }
               ,'ru':
                   {'short': 'дир.'
                   ,'title': 'Дирижабли'
                   }
               ,'de':
                   {'short': 'airsh.'
                   ,'title': 'Airships'
                   }
               ,'es':
                   {'short': 'airsh.'
                   ,'title': 'Airships'
                   }
               ,'uk':
                   {'short': 'држбл'
                   ,'title': 'Дирижаблі'
                   }
               }
           ,'alg.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'alg.'
                   ,'title': 'Algebra'
                   }
               ,'ru':
                   {'short': 'алг.'
                   ,'title': 'Алгебра'
                   }
               ,'de':
                   {'short': 'Alg.'
                   ,'title': 'Algebra'
                   }
               ,'es':
                   {'short': 'alg.'
                   ,'title': 'Algebra'
                   }
               ,'uk':
                   {'short': 'алг.'
                   ,'title': 'Алгебра'
                   }
               }
           ,'alk.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'alk.'
                   ,'title': 'Alkaloids'
                   }
               ,'ru':
                   {'short': 'алк.'
                   ,'title': 'Алкалоиды'
                   }
               ,'de':
                   {'short': 'alk.'
                   ,'title': 'Alkaloids'
                   }
               ,'es':
                   {'short': 'alk.'
                   ,'title': 'Alkaloids'
                   }
               ,'uk':
                   {'short': 'алкал.'
                   ,'title': 'Алкалоїди'
                   }
               }
           ,'allergol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'allergol.'
                   ,'title': 'Allergology'
                   }
               ,'ru':
                   {'short': 'аллерг.'
                   ,'title': 'Аллергология'
                   }
               ,'de':
                   {'short': 'allerg.'
                   ,'title': 'Allergologie'
                   }
               ,'es':
                   {'short': 'alergol.'
                   ,'title': 'Alergología'
                   }
               ,'uk':
                   {'short': 'алерг.'
                   ,'title': 'Алергологія'
                   }
               }
           ,'alp.ski.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'alp.ski.'
                   ,'title': 'Alpine skiing'
                   }
               ,'ru':
                   {'short': 'горн.лыж.'
                   ,'title': 'Горные лыжи'
                   }
               ,'de':
                   {'short': 'alp.ski.'
                   ,'title': 'Alpine skiing'
                   }
               ,'es':
                   {'short': 'alp.ski.'
                   ,'title': 'Alpine skiing'
                   }
               ,'uk':
                   {'short': 'гір.лиж.'
                   ,'title': 'Гірські лижі'
                   }
               }
           ,'alum.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'alum.'
                   ,'title': 'Aluminium industry'
                   }
               ,'ru':
                   {'short': 'алюм.'
                   ,'title': 'Алюминиевая промышленность'
                   }
               ,'de':
                   {'short': 'alum.'
                   ,'title': 'Aluminium industry'
                   }
               ,'es':
                   {'short': 'alum.'
                   ,'title': 'Aluminium industry'
                   }
               ,'uk':
                   {'short': 'алюм.'
                   ,'title': 'Алюмінієва промисловість'
                   }
               }
           ,'amer.usg.':
               {'is_valid': False
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'amer.usg.'
                   ,'title': 'American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'амер.'
                   ,'title': 'Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Amerik.'
                   ,'title': 'Amerikanisch'
                   }
               ,'es':
                   {'short': 'amer.'
                   ,'title': 'Americano (uso)'
                   }
               ,'uk':
                   {'short': 'амер.вир.'
                   ,'title': 'Американський вираз (не варыант мови)'
                   }
               }
           ,'amer.usg., Makarov.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'amer.usg., Makarov.'
                   ,'title': 'American (usage, not AmE), Makarov'
                   }
               ,'ru':
                   {'short': 'амер., Макаров.'
                   ,'title': 'Американское выражение (не вариант языка), Макаров'
                   }
               ,'de':
                   {'short': 'Amerik., Makarow.'
                   ,'title': 'Amerikanisch, Makarow'
                   }
               ,'es':
                   {'short': 'amer., Makarov.'
                   ,'title': 'Americano (uso), Makarov'
                   }
               ,'uk':
                   {'short': 'амер.вир., Макаров'
                   ,'title': 'Американський вираз (не варыант мови), Макаров'
                   }
               }
           ,'amer.usg., account.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'amer.usg., account.'
                   ,'title': 'American (usage, not AmE), Accounting'
                   }
               ,'ru':
                   {'short': 'амер., бухг.'
                   ,'title': 'Американское выражение (не вариант языка), Бухгалтерский учет (кроме аудита)'
                   }
               ,'de':
                   {'short': 'Amerik., Buchhalt.'
                   ,'title': 'Amerikanisch, Buchhaltung'
                   }
               ,'es':
                   {'short': 'amer., cont.'
                   ,'title': 'Americano (uso), Contabilidad'
                   }
               ,'uk':
                   {'short': 'амер.вир., бухг.'
                   ,'title': 'Американський вираз (не варыант мови), Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'anaesthes.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'anaesthes.'
                   ,'title': 'Anesthesiology'
                   }
               ,'ru':
                   {'short': 'анест.'
                   ,'title': 'Анестезиология'
                   }
               ,'de':
                   {'short': 'anäst.'
                   ,'title': 'Anästhesiologie'
                   }
               ,'es':
                   {'short': 'anestes.'
                   ,'title': 'Anestesiología'
                   }
               ,'uk':
                   {'short': 'анест.'
                   ,'title': 'Анестезіологія'
                   }
               }
           ,'anat.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'anat.'
                   ,'title': 'Anatomy'
                   }
               ,'ru':
                   {'short': 'анат.'
                   ,'title': 'Анатомия'
                   }
               ,'de':
                   {'short': 'Anat.'
                   ,'title': 'Anatomie'
                   }
               ,'es':
                   {'short': 'anat.'
                   ,'title': 'Anatomía'
                   }
               ,'uk':
                   {'short': 'анат.'
                   ,'title': 'Анатомія'
                   }
               }
           ,'anc.fr.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'anc.fr.'
                   ,'title': 'Ancient French'
                   }
               ,'ru':
                   {'short': 'старофр.'
                   ,'title': 'Старофранцузский'
                   }
               ,'de':
                   {'short': 'Altfranzös.'
                   ,'title': 'Altfranzösisch'
                   }
               ,'es':
                   {'short': 'anc.fr.'
                   ,'title': 'Ancient French'
                   }
               ,'uk':
                   {'short': 'старофр.'
                   ,'title': 'Старофранцузька мова'
                   }
               }
           ,'anc.gr.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'anc.gr.'
                   ,'title': 'Ancient Greek'
                   }
               ,'ru':
                   {'short': 'др.греч.'
                   ,'title': 'Древнегреческий язык'
                   }
               ,'de':
                   {'short': 'Altgr.Sp.'
                   ,'title': 'Altgriechische Sprache'
                   }
               ,'es':
                   {'short': 'gr.ant.'
                   ,'title': 'Griego antiguo'
                   }
               ,'uk':
                   {'short': 'давн.грец.'
                   ,'title': 'Давньогрецька мова'
                   }
               }
           ,'anc.hebr.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'anc.hebr.'
                   ,'title': 'Ancient Hebrew'
                   }
               ,'ru':
                   {'short': 'др.евр.'
                   ,'title': 'Древнееврейский язык'
                   }
               ,'de':
                   {'short': 'Althebr.'
                   ,'title': 'Althebräisch'
                   }
               ,'es':
                   {'short': 'anc.hebr.'
                   ,'title': 'Ancient Hebrew'
                   }
               ,'uk':
                   {'short': 'давн.євр.'
                   ,'title': 'Давньоєврейська мова'
                   }
               }
           ,'angl.':
               {'is_valid': True
               ,'major_en': 'Hobbies and pastimes'
               ,'is_major': False
               ,'en':
                   {'short': 'angl.'
                   ,'title': 'Angling (hobby)'
                   }
               ,'ru':
                   {'short': 'рыбал.'
                   ,'title': 'Рыбалка (хобби)'
                   }
               ,'de':
                   {'short': 'angl.'
                   ,'title': 'Angling (hobby)'
                   }
               ,'es':
                   {'short': 'angl.'
                   ,'title': 'Angling (hobby)'
                   }
               ,'uk':
                   {'short': 'рибол.'
                   ,'title': 'Риболовля (хобі)'
                   }
               }
           ,'anim.husb.':
               {'is_valid': False
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'anim.husb.'
                   ,'title': 'Animal husbandry'
                   }
               ,'ru':
                   {'short': 'с/х., животн.'
                   ,'title': 'Животноводство'
                   }
               ,'de':
                   {'short': 'landwirt.'
                   ,'title': 'Landwirtschaft'
                   }
               ,'es':
                   {'short': 'anim.husb.'
                   ,'title': 'Animal husbandry'
                   }
               ,'uk':
                   {'short': 'тварин.'
                   ,'title': 'Тваринництво'
                   }
               }
           ,'animat.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'animat.'
                   ,'title': 'Animation and animated films'
                   }
               ,'ru':
                   {'short': 'мульт.'
                   ,'title': 'Мультфильмы и мультипликация'
                   }
               ,'de':
                   {'short': 'animat.'
                   ,'title': 'Animation and animated films'
                   }
               ,'es':
                   {'short': 'animat.'
                   ,'title': 'Animation and animated films'
                   }
               ,'uk':
                   {'short': 'мульт.'
                   ,'title': 'Мультфільми та мультиплікація'
                   }
               }
           ,'antarct.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'antarct.'
                   ,'title': 'Antarctic'
                   }
               ,'ru':
                   {'short': 'антаркт.'
                   ,'title': 'Антарктика'
                   }
               ,'de':
                   {'short': 'antarct.'
                   ,'title': 'Antarctic'
                   }
               ,'es':
                   {'short': 'antarct.'
                   ,'title': 'Antarctic'
                   }
               ,'uk':
                   {'short': 'антаркт.'
                   ,'title': 'Антарктика'
                   }
               }
           ,'antenn.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'antenn.'
                   ,'title': 'Antennas and waveguides'
                   }
               ,'ru':
                   {'short': 'антенн.'
                   ,'title': 'Антенны и волноводы'
                   }
               ,'de':
                   {'short': 'antenn.'
                   ,'title': 'Antennas and waveguides'
                   }
               ,'es':
                   {'short': 'antenn.'
                   ,'title': 'Antennas and waveguides'
                   }
               ,'uk':
                   {'short': 'антен.'
                   ,'title': 'Антени і хвилеводи'
                   }
               }
           ,'anthr.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'anthr.'
                   ,'title': 'Anthropology'
                   }
               ,'ru':
                   {'short': 'антр.'
                   ,'title': 'Антропология'
                   }
               ,'de':
                   {'short': 'Anthropol.'
                   ,'title': 'Anthropologie'
                   }
               ,'es':
                   {'short': 'anthr.'
                   ,'title': 'Anthropology'
                   }
               ,'uk':
                   {'short': 'антроп.'
                   ,'title': 'Антропологія'
                   }
               }
           ,'antitrust.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'antitrust.'
                   ,'title': 'Antitrust law'
                   }
               ,'ru':
                   {'short': 'антимон.'
                   ,'title': 'Антимонопольное законодательство'
                   }
               ,'de':
                   {'short': 'antitrust.'
                   ,'title': 'Antitrust law'
                   }
               ,'es':
                   {'short': 'antitrust.'
                   ,'title': 'Antitrust law'
                   }
               ,'uk':
                   {'short': 'антимон.'
                   ,'title': 'Антимонопольне законодавство'
                   }
               }
           ,'appl.math.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'appl.math.'
                   ,'title': 'Applied mathematics'
                   }
               ,'ru':
                   {'short': 'прикл.мат.'
                   ,'title': 'Прикладная математика'
                   }
               ,'de':
                   {'short': 'Wahrsch. Theor.'
                   ,'title': 'Wahrscheinlichkeitstheorie'
                   }
               ,'es':
                   {'short': 'appl.math.'
                   ,'title': 'Applied mathematics'
                   }
               ,'uk':
                   {'short': 'прикл.мат.'
                   ,'title': 'Прикладна математика'
                   }
               }
           ,'arabic':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'arabic'
                   ,'title': 'Arabic language'
                   }
               ,'ru':
                   {'short': 'араб.'
                   ,'title': 'Арабский язык'
                   }
               ,'de':
                   {'short': 'Arab.'
                   ,'title': 'Arabisch'
                   }
               ,'es':
                   {'short': 'árab.'
                   ,'title': 'Árabe'
                   }
               ,'uk':
                   {'short': 'араб.'
                   ,'title': 'Арабська мова'
                   }
               }
           ,'arch.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'arch.'
                   ,'title': 'Archaic'
                   }
               ,'ru':
                   {'short': 'арх.'
                   ,'title': 'Архаизм'
                   }
               ,'de':
                   {'short': 'Arch.'
                   ,'title': 'Archaisch'
                   }
               ,'es':
                   {'short': 'arch.'
                   ,'title': 'Archaic'
                   }
               ,'uk':
                   {'short': 'арх.'
                   ,'title': 'Архаїзм'
                   }
               }
           ,'archer.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'archer.'
                   ,'title': 'Archery'
                   }
               ,'ru':
                   {'short': 'лук.'
                   ,'title': 'Стрельба из лука'
                   }
               ,'de':
                   {'short': 'archer.'
                   ,'title': 'Archery'
                   }
               ,'es':
                   {'short': 'archer.'
                   ,'title': 'Archery'
                   }
               ,'uk':
                   {'short': 'стр.лук.'
                   ,'title': 'Стрільба з лука'
                   }
               }
           ,'archit.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'archit.'
                   ,'title': 'Architecture'
                   }
               ,'ru':
                   {'short': 'архит.'
                   ,'title': 'Архитектура'
                   }
               ,'de':
                   {'short': 'Architek.'
                   ,'title': 'Architektur'
                   }
               ,'es':
                   {'short': 'arquit.'
                   ,'title': 'Arquitectura'
                   }
               ,'uk':
                   {'short': 'архіт.'
                   ,'title': 'Архітектура'
                   }
               }
           ,'archive.':
               {'is_valid': True
               ,'major_en': 'Records management'
               ,'is_major': False
               ,'en':
                   {'short': 'archive.'
                   ,'title': 'Archiving'
                   }
               ,'ru':
                   {'short': 'архив.'
                   ,'title': 'Архивное дело'
                   }
               ,'de':
                   {'short': 'archive.'
                   ,'title': 'Archiving'
                   }
               ,'es':
                   {'short': 'archive.'
                   ,'title': 'Archiving'
                   }
               ,'uk':
                   {'short': 'архів.'
                   ,'title': 'Архівна справа'
                   }
               }
           ,'arts.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'arts.'
                   ,'title': 'Art'
                   }
               ,'ru':
                   {'short': 'иск.'
                   ,'title': 'Искусство'
                   }
               ,'de':
                   {'short': 'Kunst.'
                   ,'title': 'Kunst'
                   }
               ,'es':
                   {'short': 'arte'
                   ,'title': 'Arte'
                   }
               ,'uk':
                   {'short': 'мист.'
                   ,'title': 'Мистецтво'
                   }
               }
           ,'astr.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'astr.'
                   ,'title': 'Astronomy'
                   }
               ,'ru':
                   {'short': 'астр.'
                   ,'title': 'Астрономия'
                   }
               ,'de':
                   {'short': 'Astron.'
                   ,'title': 'Astronomie'
                   }
               ,'es':
                   {'short': 'astr.'
                   ,'title': 'Astronomía'
                   }
               ,'uk':
                   {'short': 'астр.'
                   ,'title': 'Астрономія'
                   }
               }
           ,'astrol.':
               {'is_valid': True
               ,'major_en': 'Parasciences'
               ,'is_major': False
               ,'en':
                   {'short': 'astrol.'
                   ,'title': 'Astrology'
                   }
               ,'ru':
                   {'short': 'астрол.'
                   ,'title': 'Астрология'
                   }
               ,'de':
                   {'short': 'astrol.'
                   ,'title': 'Astrology'
                   }
               ,'es':
                   {'short': 'astrol.'
                   ,'title': 'Astrology'
                   }
               ,'uk':
                   {'short': 'астрол.'
                   ,'title': 'Астрологія'
                   }
               }
           ,'astrometr.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'astrometr.'
                   ,'title': 'Astrometry'
                   }
               ,'ru':
                   {'short': 'амт.'
                   ,'title': 'Астрометрия'
                   }
               ,'de':
                   {'short': 'astrometr.'
                   ,'title': 'Astrometry'
                   }
               ,'es':
                   {'short': 'astrometr.'
                   ,'title': 'Astrometry'
                   }
               ,'uk':
                   {'short': 'астром.'
                   ,'title': 'Астрометрія'
                   }
               }
           ,'astronaut.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'astronaut.'
                   ,'title': 'Astronautics'
                   }
               ,'ru':
                   {'short': 'космон.'
                   ,'title': 'Космонавтика'
                   }
               ,'de':
                   {'short': 'Astro.'
                   ,'title': 'Astronautik'
                   }
               ,'es':
                   {'short': 'astronaut.'
                   ,'title': 'Astronautics'
                   }
               ,'uk':
                   {'short': 'космон.'
                   ,'title': 'Космонавтика'
                   }
               }
           ,'astrophys.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'astrophys.'
                   ,'title': 'Astrophysics'
                   }
               ,'ru':
                   {'short': 'астрофиз.'
                   ,'title': 'Астрофизика'
                   }
               ,'de':
                   {'short': 'astrophys.'
                   ,'title': 'Astrophysics'
                   }
               ,'es':
                   {'short': 'astrophys.'
                   ,'title': 'Astrophysics'
                   }
               ,'uk':
                   {'short': 'астрофіз.'
                   ,'title': 'Астрофізика'
                   }
               }
           ,'astrospectr.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'astrospectr.'
                   ,'title': 'Astrospectroscopy'
                   }
               ,'ru':
                   {'short': 'асп.'
                   ,'title': 'Астроспектроскопия'
                   }
               ,'de':
                   {'short': 'astrospectr.'
                   ,'title': 'Astrospectroscopy'
                   }
               ,'es':
                   {'short': 'astrospectr.'
                   ,'title': 'Astrospectroscopy'
                   }
               ,'uk':
                   {'short': 'астроспек.'
                   ,'title': 'Астроспектроскопія'
                   }
               }
           ,'athlet.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'athlet.'
                   ,'title': 'Athletics'
                   }
               ,'ru':
                   {'short': 'л.атл.'
                   ,'title': 'Легкая атлетика'
                   }
               ,'de':
                   {'short': 'athlet.'
                   ,'title': 'Athletics'
                   }
               ,'es':
                   {'short': 'athlet.'
                   ,'title': 'Athletics'
                   }
               ,'uk':
                   {'short': 'л.атл.'
                   ,'title': 'Легка атлетика'
                   }
               }
           ,'atring.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'atring.'
                   ,'title': 'Astringents'
                   }
               ,'ru':
                   {'short': 'вяж.'
                   ,'title': 'Вяжущие вещества'
                   }
               ,'de':
                   {'short': 'atring.'
                   ,'title': 'Astringents'
                   }
               ,'es':
                   {'short': 'atring.'
                   ,'title': 'Astringents'
                   }
               ,'uk':
                   {'short': 'в’яж.реч.'
                   ,'title': 'В’яжучі речовини'
                   }
               }
           ,'audio.el.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'audio.el.'
                   ,'title': 'Audio electronics'
                   }
               ,'ru':
                   {'short': 'аудиотех.'
                   ,'title': 'Аудиотехника'
                   }
               ,'de':
                   {'short': 'audio.el.'
                   ,'title': 'Audio electronics'
                   }
               ,'es':
                   {'short': 'audio.el.'
                   ,'title': 'Audio electronics'
                   }
               ,'uk':
                   {'short': 'аудіотех.'
                   ,'title': 'Аудіотехніка'
                   }
               }
           ,'austral.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'austral.'
                   ,'title': 'Australian'
                   }
               ,'ru':
                   {'short': 'австрал.'
                   ,'title': 'Австралийское выражение'
                   }
               ,'de':
                   {'short': 'Austr. Slang'
                   ,'title': 'Australischer Slang'
                   }
               ,'es':
                   {'short': 'austral.'
                   ,'title': 'Australiano (sólo uso)'
                   }
               ,'uk':
                   {'short': 'австрал.'
                   ,'title': 'Австралійський вираз'
                   }
               }
           ,'austrian':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'austrian'
                   ,'title': 'Austrian (usage)'
                   }
               ,'ru':
                   {'short': 'австр.выр.'
                   ,'title': 'Австрийское выражение'
                   }
               ,'de':
                   {'short': 'Öster.'
                   ,'title': 'Österreichisch'
                   }
               ,'es':
                   {'short': 'austrian'
                   ,'title': 'Austrian (usage)'
                   }
               ,'uk':
                   {'short': 'австрійськ.'
                   ,'title': 'Австрійський вираз'
                   }
               }
           ,'auto.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'auto.'
                   ,'title': 'Automobiles'
                   }
               ,'ru':
                   {'short': 'авто.'
                   ,'title': 'Автомобили'
                   }
               ,'de':
                   {'short': 'Autoind.'
                   ,'title': 'Autoindustrie'
                   }
               ,'es':
                   {'short': 'automóv.'
                   ,'title': 'Automóviles'
                   }
               ,'uk':
                   {'short': 'авто.'
                   ,'title': 'Автомобілі'
                   }
               }
           ,'auto.ctrl.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'auto.ctrl.'
                   ,'title': 'Automatic control'
                   }
               ,'ru':
                   {'short': 'рег.'
                   ,'title': 'Автоматическое регулирование'
                   }
               ,'de':
                   {'short': 'auto.ctrl.'
                   ,'title': 'Automatic control'
                   }
               ,'es':
                   {'short': 'auto.ctrl.'
                   ,'title': 'Automatic control'
                   }
               ,'uk':
                   {'short': 'автом.рег.'
                   ,'title': 'Автоматичне регулювання'
                   }
               }
           ,'automat.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'automat.'
                   ,'title': 'Automated equipment'
                   }
               ,'ru':
                   {'short': 'автомат.'
                   ,'title': 'Автоматика'
                   }
               ,'de':
                   {'short': 'Autom.'
                   ,'title': 'Automatik'
                   }
               ,'es':
                   {'short': 'automat.'
                   ,'title': 'Automated equipment'
                   }
               ,'uk':
                   {'short': 'автомат.'
                   ,'title': 'Автоматика'
                   }
               }
           ,'avia.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': True
               ,'en':
                   {'short': 'avia.'
                   ,'title': 'Aviation'
                   }
               ,'ru':
                   {'short': 'авиац.'
                   ,'title': 'Авиация'
                   }
               ,'de':
                   {'short': 'Luftf.'
                   ,'title': 'Luftfahrt'
                   }
               ,'es':
                   {'short': 'avia.'
                   ,'title': 'Aviación'
                   }
               ,'uk':
                   {'short': 'авіац.'
                   ,'title': 'Авіація'
                   }
               }
           ,'avia., avia., ICAO':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'avia., avia., ICAO'
                   ,'title': 'Aviation, ICAO'
                   }
               ,'ru':
                   {'short': 'авиац., авиац., ИКАО'
                   ,'title': 'Авиация, ИКАО'
                   }
               ,'de':
                   {'short': 'Luftf., ICAO'
                   ,'title': 'Luftfahrt, ICAO'
                   }
               ,'es':
                   {'short': 'avia., avia., ICAO'
                   ,'title': 'Aviación, ICAO'
                   }
               ,'uk':
                   {'short': 'авіац., авіац., ІКАО'
                   ,'title': 'Авіація, ІКАО'
                   }
               }
           ,'avia., med.':
               {'is_valid': False
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'avia., med.'
                   ,'title': 'Aviation medicine'
                   }
               ,'ru':
                   {'short': 'авиац., мед.'
                   ,'title': 'Авиационная медицина'
                   }
               ,'de':
                   {'short': 'Luft.med.'
                   ,'title': 'Luftfahrtmedizin'
                   }
               ,'es':
                   {'short': 'avia., med.'
                   ,'title': 'Aviation medicine'
                   }
               ,'uk':
                   {'short': 'авіац., мед.'
                   ,'title': 'Авіаційна медицина'
                   }
               }
           ,'avunc.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'avunc.'
                   ,'title': 'Avuncular'
                   }
               ,'ru':
                   {'short': 'фам.'
                   ,'title': 'Фамильярное выражение'
                   }
               ,'de':
                   {'short': 'Salopp'
                   ,'title': 'Salopp'
                   }
               ,'es':
                   {'short': 'avunc.'
                   ,'title': 'Avuncular'
                   }
               ,'uk':
                   {'short': 'фам.'
                   ,'title': 'Фамільярний вираз'
                   }
               }
           ,'bacteriol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'bacteriol.'
                   ,'title': 'Bacteriology'
                   }
               ,'ru':
                   {'short': 'бакт.'
                   ,'title': 'Бактериология'
                   }
               ,'de':
                   {'short': 'Bakter.'
                   ,'title': 'Bakteriologie'
                   }
               ,'es':
                   {'short': 'bact.'
                   ,'title': 'Bacteriología'
                   }
               ,'uk':
                   {'short': 'бакт.'
                   ,'title': 'Бактеріологія'
                   }
               }
           ,'baker.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'baker.'
                   ,'title': 'Bakery'
                   }
               ,'ru':
                   {'short': 'хлеб.'
                   ,'title': 'Хлеб и хлебопечение'
                   }
               ,'de':
                   {'short': 'baker.'
                   ,'title': 'Bakery'
                   }
               ,'es':
                   {'short': 'baker.'
                   ,'title': 'Bakery'
                   }
               ,'uk':
                   {'short': 'хліб.'
                   ,'title': 'Хліб та хлібопечення'
                   }
               }
           ,'ball.bear.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'ball.bear.'
                   ,'title': 'Ball bearings'
                   }
               ,'ru':
                   {'short': 'шарик.'
                   ,'title': 'Шарикоподшипники'
                   }
               ,'de':
                   {'short': 'ball.bear.'
                   ,'title': 'Ball bearings'
                   }
               ,'es':
                   {'short': 'ball.bear.'
                   ,'title': 'Ball bearings'
                   }
               ,'uk':
                   {'short': 'кульк.підш.'
                   ,'title': 'Кулькові підшипники'
                   }
               }
           ,'ballet.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'ballet.'
                   ,'title': 'Ballet'
                   }
               ,'ru':
                   {'short': 'балет.'
                   ,'title': 'Балет'
                   }
               ,'de':
                   {'short': 'ballet.'
                   ,'title': 'Ballet'
                   }
               ,'es':
                   {'short': 'ballet.'
                   ,'title': 'Ballet'
                   }
               ,'uk':
                   {'short': 'балет'
                   ,'title': 'Балет'
                   }
               }
           ,'bank.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'bank.'
                   ,'title': 'Banking'
                   }
               ,'ru':
                   {'short': 'банк.'
                   ,'title': 'Банки и банковское дело'
                   }
               ,'de':
                   {'short': 'Bank.'
                   ,'title': 'Bankwesen'
                   }
               ,'es':
                   {'short': 'bank.'
                   ,'title': 'Banking'
                   }
               ,'uk':
                   {'short': 'банк.'
                   ,'title': 'Банки та банківська справа'
                   }
               }
           ,'baseb.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'baseb.'
                   ,'title': 'Baseball'
                   }
               ,'ru':
                   {'short': 'бейсб.'
                   ,'title': 'Бейсбол'
                   }
               ,'de':
                   {'short': 'Baseball'
                   ,'title': 'Baseball'
                   }
               ,'es':
                   {'short': 'baseb.'
                   ,'title': 'Baseball'
                   }
               ,'uk':
                   {'short': 'бейсб.'
                   ,'title': 'Бейсбол'
                   }
               }
           ,'beekeep.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'beekeep.'
                   ,'title': 'Beekeeping'
                   }
               ,'ru':
                   {'short': 'пчел.'
                   ,'title': 'Пчеловодство'
                   }
               ,'de':
                   {'short': 'Imker.'
                   ,'title': 'Imkerei'
                   }
               ,'es':
                   {'short': 'beekeep.'
                   ,'title': 'Beekeeping'
                   }
               ,'uk':
                   {'short': 'бджіл.'
                   ,'title': 'Бджільництво'
                   }
               }
           ,'belg.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'belg.'
                   ,'title': 'Belgian (usage)'
                   }
               ,'ru':
                   {'short': 'бельг.выр.'
                   ,'title': 'Бельгийское выражение'
                   }
               ,'de':
                   {'short': 'belg.'
                   ,'title': 'Belgian (usage)'
                   }
               ,'es':
                   {'short': 'belg.'
                   ,'title': 'Belgian (usage)'
                   }
               ,'uk':
                   {'short': 'бельг.вир.'
                   ,'title': 'Бельгійський вираз'
                   }
               }
           ,'bev.':
               {'is_valid': True
               ,'major_en': 'Cooking'
               ,'is_major': False
               ,'en':
                   {'short': 'bev.'
                   ,'title': 'Beverages'
                   }
               ,'ru':
                   {'short': 'напит.'
                   ,'title': 'Напитки'
                   }
               ,'de':
                   {'short': 'bev.'
                   ,'title': 'Beverages'
                   }
               ,'es':
                   {'short': 'bev.'
                   ,'title': 'Beverages'
                   }
               ,'uk':
                   {'short': 'напої.'
                   ,'title': 'Напої'
                   }
               }
           ,'bible.term.':
               {'is_valid': True
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'bible.term.'
                   ,'title': 'Bible'
                   }
               ,'ru':
                   {'short': 'библ.'
                   ,'title': 'Библия'
                   }
               ,'de':
                   {'short': 'bibl.'
                   ,'title': 'Bibel'
                   }
               ,'es':
                   {'short': 'bibl.'
                   ,'title': 'Biblia'
                   }
               ,'uk':
                   {'short': 'бібл.'
                   ,'title': 'Біблія'
                   }
               }
           ,'bibliogr.':
               {'is_valid': True
               ,'major_en': 'Records management'
               ,'is_major': False
               ,'en':
                   {'short': 'bibliogr.'
                   ,'title': 'Bibliography'
                   }
               ,'ru':
                   {'short': 'библиогр.'
                   ,'title': 'Библиография'
                   }
               ,'de':
                   {'short': 'bibliogr.'
                   ,'title': 'Bibliography'
                   }
               ,'es':
                   {'short': 'bibliogr.'
                   ,'title': 'Bibliography'
                   }
               ,'uk':
                   {'short': 'бібліогр.'
                   ,'title': 'Бібліографія'
                   }
               }
           ,'bill.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'bill.'
                   ,'title': 'Bills'
                   }
               ,'ru':
                   {'short': 'вексел.'
                   ,'title': 'Вексельное право'
                   }
               ,'de':
                   {'short': 'Wechselrecht'
                   ,'title': 'Wechselrecht'
                   }
               ,'es':
                   {'short': 'bill.'
                   ,'title': 'Bills'
                   }
               ,'uk':
                   {'short': 'векс.'
                   ,'title': 'Вексельне право'
                   }
               }
           ,'billiar.':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'billiar.'
                   ,'title': 'Billiards'
                   }
               ,'ru':
                   {'short': 'бильярд.'
                   ,'title': 'Бильярд'
                   }
               ,'de':
                   {'short': 'billiar.'
                   ,'title': 'Billiards'
                   }
               ,'es':
                   {'short': 'billiar.'
                   ,'title': 'Billiards'
                   }
               ,'uk':
                   {'short': 'більярд'
                   ,'title': 'Більярд'
                   }
               }
           ,'bioacoust.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'bioacoust.'
                   ,'title': 'Bioacoustics'
                   }
               ,'ru':
                   {'short': 'биоакуст.'
                   ,'title': 'Биоакустика'
                   }
               ,'de':
                   {'short': 'bioacoust.'
                   ,'title': 'Bioacoustics'
                   }
               ,'es':
                   {'short': 'bioacoust.'
                   ,'title': 'Bioacoustics'
                   }
               ,'uk':
                   {'short': 'біоакуст.'
                   ,'title': 'Біоакустика'
                   }
               }
           ,'biochem.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'biochem.'
                   ,'title': 'Biochemistry'
                   }
               ,'ru':
                   {'short': 'биохим.'
                   ,'title': 'Биохимия'
                   }
               ,'de':
                   {'short': 'Biochem.'
                   ,'title': 'Biochemie'
                   }
               ,'es':
                   {'short': 'bioq.'
                   ,'title': 'Bioquímica'
                   }
               ,'uk':
                   {'short': 'біохім.'
                   ,'title': 'Біохімія'
                   }
               }
           ,'bioenerg.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'bioenerg.'
                   ,'title': 'Bioenergy'
                   }
               ,'ru':
                   {'short': 'биоэнерг.'
                   ,'title': 'Биоэнергетика'
                   }
               ,'de':
                   {'short': 'bioenerg.'
                   ,'title': 'Bioenergy'
                   }
               ,'es':
                   {'short': 'bioenerg.'
                   ,'title': 'Bioenergy'
                   }
               ,'uk':
                   {'short': 'біоенерг.'
                   ,'title': 'Біоенергетика'
                   }
               }
           ,'biol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': True
               ,'en':
                   {'short': 'biol.'
                   ,'title': 'Biology'
                   }
               ,'ru':
                   {'short': 'биол.'
                   ,'title': 'Биология'
                   }
               ,'de':
                   {'short': 'Biol.'
                   ,'title': 'Biologie'
                   }
               ,'es':
                   {'short': 'biol.'
                   ,'title': 'Biología'
                   }
               ,'uk':
                   {'short': 'біол.'
                   ,'title': 'Біологія'
                   }
               }
           ,'biom.':
               {'is_valid': True
               ,'major_en': 'Security systems'
               ,'is_major': False
               ,'en':
                   {'short': 'biom.'
                   ,'title': 'Biometry'
                   }
               ,'ru':
                   {'short': 'биом.'
                   ,'title': 'Биометрия'
                   }
               ,'de':
                   {'short': 'biom.'
                   ,'title': 'Biometry'
                   }
               ,'es':
                   {'short': 'biom.'
                   ,'title': 'Biometry'
                   }
               ,'uk':
                   {'short': 'біом.'
                   ,'title': 'Біометрія'
                   }
               }
           ,'bion.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'bion.'
                   ,'title': 'Bionics'
                   }
               ,'ru':
                   {'short': 'бион.'
                   ,'title': 'Бионика'
                   }
               ,'de':
                   {'short': 'bion.'
                   ,'title': 'Bionics'
                   }
               ,'es':
                   {'short': 'bion.'
                   ,'title': 'Bionics'
                   }
               ,'uk':
                   {'short': 'біон.'
                   ,'title': 'Біоніка'
                   }
               }
           ,'biophys.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'biophys.'
                   ,'title': 'Biophysics'
                   }
               ,'ru':
                   {'short': 'биофиз.'
                   ,'title': 'Биофизика'
                   }
               ,'de':
                   {'short': 'biophys.'
                   ,'title': 'Biophysik'
                   }
               ,'es':
                   {'short': 'biofís.'
                   ,'title': 'Biofísica'
                   }
               ,'uk':
                   {'short': 'біофіз.'
                   ,'title': 'Біофізика'
                   }
               }
           ,'biotaxy.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'biotaxy.'
                   ,'title': 'Biotaxy'
                   }
               ,'ru':
                   {'short': 'сист.орг.'
                   ,'title': 'Систематика организмов'
                   }
               ,'de':
                   {'short': 'biotaxy.'
                   ,'title': 'Biotaxy'
                   }
               ,'es':
                   {'short': 'biotaxy.'
                   ,'title': 'Biotaxy'
                   }
               ,'uk':
                   {'short': 'сист.орг.'
                   ,'title': 'Систематика організмів'
                   }
               }
           ,'biotechn.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'biotechn.'
                   ,'title': 'Biotechnology'
                   }
               ,'ru':
                   {'short': 'биотех.'
                   ,'title': 'Биотехнология'
                   }
               ,'de':
                   {'short': 'Biotech.'
                   ,'title': 'Biotechnologie'
                   }
               ,'es':
                   {'short': 'biotechn.'
                   ,'title': 'Biotechnology'
                   }
               ,'uk':
                   {'short': 'біот.'
                   ,'title': 'Біотехнологія'
                   }
               }
           ,'black.sl.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'black.sl.'
                   ,'title': 'Black slang'
                   }
               ,'ru':
                   {'short': 'негр.'
                   ,'title': 'Негритянский жаргон'
                   }
               ,'de':
                   {'short': 'Neg.Slang'
                   ,'title': 'Negerslang'
                   }
               ,'es':
                   {'short': 'black.sl.'
                   ,'title': 'Black slang'
                   }
               ,'uk':
                   {'short': 'негр.'
                   ,'title': 'Негритянський жаргон'
                   }
               }
           ,'bodybuild.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'bodybuild.'
                   ,'title': 'Bodybuilding'
                   }
               ,'ru':
                   {'short': 'бодибилд.'
                   ,'title': 'Бодибилдинг'
                   }
               ,'de':
                   {'short': 'bodybuild.'
                   ,'title': 'Bodybuilding'
                   }
               ,'es':
                   {'short': 'bodybuild.'
                   ,'title': 'Bodybuilding'
                   }
               ,'uk':
                   {'short': 'бодібілд.'
                   ,'title': 'Бодібілдинг'
                   }
               }
           ,'book.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'book.'
                   ,'title': 'Bookish / literary'
                   }
               ,'ru':
                   {'short': 'книжн.'
                   ,'title': 'Книжное/литературное выражение'
                   }
               ,'de':
                   {'short': 'Lit. Stil'
                   ,'title': 'Literarischer Stil'
                   }
               ,'es':
                   {'short': 'lib.'
                   ,'title': 'Libresco/literario'
                   }
               ,'uk':
                   {'short': 'книжн.'
                   ,'title': 'Книжний / літературний вираз'
                   }
               }
           ,'book.bind.':
               {'is_valid': True
               ,'major_en': 'Publishing'
               ,'is_major': False
               ,'en':
                   {'short': 'book.bind.'
                   ,'title': 'Book binding'
                   }
               ,'ru':
                   {'short': 'перепл.'
                   ,'title': 'Переплётное дело'
                   }
               ,'de':
                   {'short': 'book.bind.'
                   ,'title': 'Book binding'
                   }
               ,'es':
                   {'short': 'book.bind.'
                   ,'title': 'Book binding'
                   }
               ,'uk':
                   {'short': 'палітурн.'
                   ,'title': 'Палітурна справа'
                   }
               }
           ,'bot.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'bot.'
                   ,'title': 'Botany'
                   }
               ,'ru':
                   {'short': 'бот.'
                   ,'title': 'Ботаника'
                   }
               ,'de':
                   {'short': 'Bot.'
                   ,'title': 'Botanik'
                   }
               ,'es':
                   {'short': 'bot.'
                   ,'title': 'Botánica'
                   }
               ,'uk':
                   {'short': 'бот.'
                   ,'title': 'Ботаніка'
                   }
               }
           ,'box.':
               {'is_valid': True
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': False
               ,'en':
                   {'short': 'box.'
                   ,'title': 'Boxing'
                   }
               ,'ru':
                   {'short': 'бокс.'
                   ,'title': 'Бокс'
                   }
               ,'de':
                   {'short': 'box.'
                   ,'title': 'Boxing'
                   }
               ,'es':
                   {'short': 'box.'
                   ,'title': 'Boxing'
                   }
               ,'uk':
                   {'short': 'бокс'
                   ,'title': 'Бокс'
                   }
               }
           ,'brew.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'brew.'
                   ,'title': 'Brewery'
                   }
               ,'ru':
                   {'short': 'пив.'
                   ,'title': 'Пивоварение'
                   }
               ,'de':
                   {'short': 'Bierbrau'
                   ,'title': 'Bierbrauerei'
                   }
               ,'es':
                   {'short': 'brew.'
                   ,'title': 'Brewery'
                   }
               ,'uk':
                   {'short': 'пив.'
                   ,'title': 'Пивоваріння'
                   }
               }
           ,'bricks':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'bricks'
                   ,'title': 'Bricks'
                   }
               ,'ru':
                   {'short': 'кирпич.'
                   ,'title': 'Кирпич'
                   }
               ,'de':
                   {'short': 'Ziegel.'
                   ,'title': 'Ziegelproduktion'
                   }
               ,'es':
                   {'short': 'bricks'
                   ,'title': 'Bricks'
                   }
               ,'uk':
                   {'short': 'цегл.'
                   ,'title': 'Цегла'
                   }
               }
           ,'bridg.constr.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'bridg.constr.'
                   ,'title': 'Bridge construction'
                   }
               ,'ru':
                   {'short': 'мост.'
                   ,'title': 'Мостостроение'
                   }
               ,'de':
                   {'short': 'bridg.constr.'
                   ,'title': 'Bridge construction'
                   }
               ,'es':
                   {'short': 'bridg.constr.'
                   ,'title': 'Bridge construction'
                   }
               ,'uk':
                   {'short': 'мост.'
                   ,'title': 'Мостобудування'
                   }
               }
           ,'brit.usg.':
               {'is_valid': False
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'brit.usg.'
                   ,'title': 'British (usage, not BrE)'
                   }
               ,'ru':
                   {'short': 'брит.'
                   ,'title': 'Британское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Brit.'
                   ,'title': 'Britische Redensart (Usus)'
                   }
               ,'es':
                   {'short': 'brit.usg.'
                   ,'title': 'British (usage, not BrE)'
                   }
               ,'uk':
                   {'short': 'брит.вир.'
                   ,'title': 'Британський вираз (не варіант мови)'
                   }
               }
           ,'brit.usg., austral.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'brit.usg., austral.'
                   ,'title': 'British (usage, not BrE), Australian'
                   }
               ,'ru':
                   {'short': 'брит., австрал.'
                   ,'title': 'Британское выражение (не вариант языка), Австралийское выражение'
                   }
               ,'de':
                   {'short': 'Brit., Austr. Slang'
                   ,'title': 'Britische Redensart (Usus), Australischer Slang'
                   }
               ,'es':
                   {'short': 'brit.usg., austral.'
                   ,'title': 'British (usage, not BrE), Australiano (sólo uso)'
                   }
               ,'uk':
                   {'short': 'брит.вир., австрал.'
                   ,'title': 'Британський вираз (не варіант мови), Австралійський вираз'
                   }
               }
           ,'build.mat.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': True
               ,'en':
                   {'short': 'build.mat.'
                   ,'title': 'Building materials'
                   }
               ,'ru':
                   {'short': 'стр.мт.'
                   ,'title': 'Строительные материалы'
                   }
               ,'de':
                   {'short': 'build.mat.'
                   ,'title': 'Building materials'
                   }
               ,'es':
                   {'short': 'build.mat.'
                   ,'title': 'Building materials'
                   }
               ,'uk':
                   {'short': 'буд.мат.'
                   ,'title': 'Будівельні матеріали'
                   }
               }
           ,'build.struct.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'build.struct.'
                   ,'title': 'Building structures'
                   }
               ,'ru':
                   {'short': 'констр.'
                   ,'title': 'Строительные конструкции'
                   }
               ,'de':
                   {'short': 'build.struct.'
                   ,'title': 'Building structures'
                   }
               ,'es':
                   {'short': 'build.struct.'
                   ,'title': 'Building structures'
                   }
               ,'uk':
                   {'short': 'буд.констр.'
                   ,'title': 'Будівельні конструкції'
                   }
               }
           ,'bus.styl.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'bus.styl.'
                   ,'title': 'Business style'
                   }
               ,'ru':
                   {'short': 'делов.'
                   ,'title': 'Деловая лексика'
                   }
               ,'de':
                   {'short': 'Geschäftsspr.'
                   ,'title': 'Geschäftssprache'
                   }
               ,'es':
                   {'short': 'bus.styl.'
                   ,'title': 'Business style'
                   }
               ,'uk':
                   {'short': 'ділов.'
                   ,'title': 'Ділова лексика'
                   }
               }
           ,'busin.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': True
               ,'en':
                   {'short': 'busin.'
                   ,'title': 'Business'
                   }
               ,'ru':
                   {'short': 'бизн.'
                   ,'title': 'Бизнес'
                   }
               ,'de':
                   {'short': 'Geschäftsvokab.'
                   ,'title': 'Geschäftsvokabular'
                   }
               ,'es':
                   {'short': 'busin.'
                   ,'title': 'Business'
                   }
               ,'uk':
                   {'short': 'бізн.'
                   ,'title': 'Бізнес'
                   }
               }
           ,'cables':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'cables'
                   ,'title': 'Cables and cable production'
                   }
               ,'ru':
                   {'short': 'каб.'
                   ,'title': 'Кабели и кабельное производство'
                   }
               ,'de':
                   {'short': 'Kabel'
                   ,'title': 'Kabelproduktion'
                   }
               ,'es':
                   {'short': 'cables'
                   ,'title': 'Cables and cable production'
                   }
               ,'uk':
                   {'short': 'каб.'
                   ,'title': 'Кабелі та кабельне виробництво'
                   }
               }
           ,'calligr.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'calligr.'
                   ,'title': 'Calligraphy'
                   }
               ,'ru':
                   {'short': 'каллигр.'
                   ,'title': 'Каллиграфия'
                   }
               ,'de':
                   {'short': 'calligr.'
                   ,'title': 'Calligraphy'
                   }
               ,'es':
                   {'short': 'calligr.'
                   ,'title': 'Calligraphy'
                   }
               ,'uk':
                   {'short': 'калігр.'
                   ,'title': 'Каліграфія'
                   }
               }
           ,'can.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'can.'
                   ,'title': 'Canning'
                   }
               ,'ru':
                   {'short': 'конс.'
                   ,'title': 'Консервирование'
                   }
               ,'de':
                   {'short': 'Konserv.'
                   ,'title': 'Konservierung'
                   }
               ,'es':
                   {'short': 'can.'
                   ,'title': 'Canning'
                   }
               ,'uk':
                   {'short': 'конс.'
                   ,'title': 'Консервування'
                   }
               }
           ,'canad.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'canad.'
                   ,'title': 'Canadian'
                   }
               ,'ru':
                   {'short': 'канад.'
                   ,'title': 'Канадское выражение'
                   }
               ,'de':
                   {'short': 'kand.Ausdr.'
                   ,'title': 'kanadischer Ausdruck'
                   }
               ,'es':
                   {'short': 'canad.'
                   ,'title': 'Canadian'
                   }
               ,'uk':
                   {'short': 'канад.'
                   ,'title': 'Канадський вираз'
                   }
               }
           ,'carcin.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'carcin.'
                   ,'title': 'Carcinology'
                   }
               ,'ru':
                   {'short': 'карц.'
                   ,'title': 'Карцинология'
                   }
               ,'de':
                   {'short': 'carcin.'
                   ,'title': 'Carcinology'
                   }
               ,'es':
                   {'short': 'carcin.'
                   ,'title': 'Carcinology'
                   }
               ,'uk':
                   {'short': 'карц.'
                   ,'title': 'Карцинологія'
                   }
               }
           ,'cardiol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'cardiol.'
                   ,'title': 'Cardiology'
                   }
               ,'ru':
                   {'short': 'кард.'
                   ,'title': 'Кардиология'
                   }
               ,'de':
                   {'short': 'kardiol.'
                   ,'title': 'Kardiologie'
                   }
               ,'es':
                   {'short': 'cardiol.'
                   ,'title': 'Cardiología'
                   }
               ,'uk':
                   {'short': 'кард.'
                   ,'title': 'Кардіологія'
                   }
               }
           ,'cards':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'cards'
                   ,'title': 'Card games'
                   }
               ,'ru':
                   {'short': 'карт.'
                   ,'title': 'Карточные игры'
                   }
               ,'de':
                   {'short': 'Kart.'
                   ,'title': 'Kartenspiel'
                   }
               ,'es':
                   {'short': 'cart.'
                   ,'title': 'Juego de cartas'
                   }
               ,'uk':
                   {'short': 'карти'
                   ,'title': 'Картярські ігри'
                   }
               }
           ,'cartogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'cartogr.'
                   ,'title': 'Cartography'
                   }
               ,'ru':
                   {'short': 'картогр.'
                   ,'title': 'Картография'
                   }
               ,'de':
                   {'short': 'Kartogr.'
                   ,'title': 'Kartografie'
                   }
               ,'es':
                   {'short': 'cartogr.'
                   ,'title': 'Cartography'
                   }
               ,'uk':
                   {'short': 'картогр.'
                   ,'title': 'Картографія'
                   }
               }
           ,'cartogr., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'cartogr., amer.usg.'
                   ,'title': 'Cartography, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'картогр., амер.'
                   ,'title': 'Картография, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Kartogr., Amerik.'
                   ,'title': 'Kartografie, Amerikanisch'
                   }
               ,'es':
                   {'short': 'cartogr., amer.'
                   ,'title': 'Cartography, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'картогр., амер.вир.'
                   ,'title': 'Картографія, Американський вираз (не варыант мови)'
                   }
               }
           ,'cel.mech.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'cel.mech.'
                   ,'title': 'Celestial mechanics'
                   }
               ,'ru':
                   {'short': 'нмх.'
                   ,'title': 'Небесная механика'
                   }
               ,'de':
                   {'short': 'cel.mech.'
                   ,'title': 'Celestial mechanics'
                   }
               ,'es':
                   {'short': 'cel.mech.'
                   ,'title': 'Celestial mechanics'
                   }
               ,'uk':
                   {'short': 'неб.мех.'
                   ,'title': 'Небесна механіка'
                   }
               }
           ,'cem.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'cem.'
                   ,'title': 'Cement'
                   }
               ,'ru':
                   {'short': 'цем.'
                   ,'title': 'Цемент'
                   }
               ,'de':
                   {'short': 'cem.'
                   ,'title': 'Cement'
                   }
               ,'es':
                   {'short': 'cem.'
                   ,'title': 'Cement'
                   }
               ,'uk':
                   {'short': 'цем.'
                   ,'title': 'Цемент'
                   }
               }
           ,'ceram.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'ceram.'
                   ,'title': 'Ceramics'
                   }
               ,'ru':
                   {'short': 'керам.'
                   ,'title': 'Керамика'
                   }
               ,'de':
                   {'short': 'ceram.'
                   ,'title': 'Ceramics'
                   }
               ,'es':
                   {'short': 'ceram.'
                   ,'title': 'Ceramics'
                   }
               ,'uk':
                   {'short': 'керам.'
                   ,'title': 'Кераміка'
                   }
               }
           ,'ceram.tile.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'ceram.tile.'
                   ,'title': 'Ceramic tiles'
                   }
               ,'ru':
                   {'short': 'керам.плит.'
                   ,'title': 'Керамическая плитка'
                   }
               ,'de':
                   {'short': 'ceram.tile.'
                   ,'title': 'Ceramic tiles'
                   }
               ,'es':
                   {'short': 'ceram.tile.'
                   ,'title': 'Ceramic tiles'
                   }
               ,'uk':
                   {'short': 'керам.пл.'
                   ,'title': 'Керамічна плитка'
                   }
               }
           ,'chalcid.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'chalcid.'
                   ,'title': 'Chalcidology'
                   }
               ,'ru':
                   {'short': 'хальцид.'
                   ,'title': 'Хальцидология'
                   }
               ,'de':
                   {'short': 'chalcid.'
                   ,'title': 'Chalcidology'
                   }
               ,'es':
                   {'short': 'chalcid.'
                   ,'title': 'Chalcidology'
                   }
               ,'uk':
                   {'short': 'халькід.'
                   ,'title': 'Халькідологія'
                   }
               }
           ,'charit.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'charit.'
                   ,'title': 'Charities'
                   }
               ,'ru':
                   {'short': 'благотв.'
                   ,'title': 'Благотворительные организации'
                   }
               ,'de':
                   {'short': 'charit.'
                   ,'title': 'Charities'
                   }
               ,'es':
                   {'short': 'charit.'
                   ,'title': 'Charities'
                   }
               ,'uk':
                   {'short': 'благод.'
                   ,'title': 'Благодійні організації'
                   }
               }
           ,'chat.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'chat.'
                   ,'title': 'Chat and Internet slang'
                   }
               ,'ru':
                   {'short': 'чат.'
                   ,'title': 'Чаты и интернет-жаргон'
                   }
               ,'de':
                   {'short': 'Chat.'
                   ,'title': 'Chat- und Internetslang'
                   }
               ,'es':
                   {'short': 'chat.'
                   ,'title': 'Chat and Internet slang'
                   }
               ,'uk':
                   {'short': 'чат.'
                   ,'title': 'Чати та інтернет-жаргон'
                   }
               }
           ,'chech.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'chech.'
                   ,'title': 'Czech'
                   }
               ,'ru':
                   {'short': 'чеш.'
                   ,'title': 'Чешский язык'
                   }
               ,'de':
                   {'short': 'Tschech.'
                   ,'title': 'Tschechisch'
                   }
               ,'es':
                   {'short': 'chech.'
                   ,'title': 'Czech'
                   }
               ,'uk':
                   {'short': 'чеськ.'
                   ,'title': 'Чеська мова'
                   }
               }
           ,'checkers.':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'checkers.'
                   ,'title': 'Checkers'
                   }
               ,'ru':
                   {'short': 'шашк.'
                   ,'title': 'Шашки'
                   }
               ,'de':
                   {'short': 'checkers.'
                   ,'title': 'Checkers'
                   }
               ,'es':
                   {'short': 'checkers.'
                   ,'title': 'Checkers'
                   }
               ,'uk':
                   {'short': 'шашк.'
                   ,'title': 'Шашки'
                   }
               }
           ,'cheese':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'cheese'
                   ,'title': 'Cheesemaking (caseiculture)'
                   }
               ,'ru':
                   {'short': 'сыр.'
                   ,'title': 'Сыроварение'
                   }
               ,'de':
                   {'short': 'cheese'
                   ,'title': 'Cheesemaking (caseiculture)'
                   }
               ,'es':
                   {'short': 'cheese'
                   ,'title': 'Cheesemaking (caseiculture)'
                   }
               ,'uk':
                   {'short': 'сир.'
                   ,'title': 'Сироваріння'
                   }
               }
           ,'chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': True
               ,'en':
                   {'short': 'chem.'
                   ,'title': 'Chemistry'
                   }
               ,'ru':
                   {'short': 'хим.'
                   ,'title': 'Химия'
                   }
               ,'de':
                   {'short': 'Chem.'
                   ,'title': 'Chemie'
                   }
               ,'es':
                   {'short': 'quím.'
                   ,'title': 'Química'
                   }
               ,'uk':
                   {'short': 'хім.'
                   ,'title': 'Хімія'
                   }
               }
           ,'chem.comp.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'chem.comp.'
                   ,'title': 'Chemical compounds'
                   }
               ,'ru':
                   {'short': 'хим.соед.'
                   ,'title': 'Химические соединения'
                   }
               ,'de':
                   {'short': 'chem.comp.'
                   ,'title': 'Chemical compounds'
                   }
               ,'es':
                   {'short': 'chem.comp.'
                   ,'title': 'Chemical compounds'
                   }
               ,'uk':
                   {'short': 'хім.спол.'
                   ,'title': 'Хімічні сполуки'
                   }
               }
           ,'chem.fib.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'chem.fib.'
                   ,'title': 'Chemical fibers'
                   }
               ,'ru':
                   {'short': 'хим.волокн.'
                   ,'title': 'Химические волокна'
                   }
               ,'de':
                   {'short': 'chem.fib.'
                   ,'title': 'Chemical fibers'
                   }
               ,'es':
                   {'short': 'chem.fib.'
                   ,'title': 'Chemical fibers'
                   }
               ,'uk':
                   {'short': 'хім.волок.'
                   ,'title': 'Хімічні волокна'
                   }
               }
           ,'chem.ind.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': True
               ,'en':
                   {'short': 'chem.ind.'
                   ,'title': 'Chemical industry'
                   }
               ,'ru':
                   {'short': 'хим.пром.'
                   ,'title': 'Химическая промышленность'
                   }
               ,'de':
                   {'short': 'chem.ind.'
                   ,'title': 'Chemical industry'
                   }
               ,'es':
                   {'short': 'chem.ind.'
                   ,'title': 'Chemical industry'
                   }
               ,'uk':
                   {'short': 'хім.пром.'
                   ,'title': 'Хімічна промисловість'
                   }
               }
           ,'chem.nomencl.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'chem.nomencl.'
                   ,'title': 'Chemical nomenclature'
                   }
               ,'ru':
                   {'short': 'хим.номенкл.'
                   ,'title': 'Химическая номенклатура'
                   }
               ,'de':
                   {'short': 'chem.nomencl.'
                   ,'title': 'Chemical nomenclature'
                   }
               ,'es':
                   {'short': 'chem.nomencl.'
                   ,'title': 'Chemical nomenclature'
                   }
               ,'uk':
                   {'short': 'хім.номенкл.'
                   ,'title': 'Хімічна номенклатура'
                   }
               }
           ,'chess.term.':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'chess.term.'
                   ,'title': 'Chess'
                   }
               ,'ru':
                   {'short': 'шахм.'
                   ,'title': 'Шахматы'
                   }
               ,'de':
                   {'short': 'Schach.'
                   ,'title': 'Schach'
                   }
               ,'es':
                   {'short': 'ajedr.'
                   ,'title': 'Ajedrez'
                   }
               ,'uk':
                   {'short': 'шах.'
                   ,'title': 'Шахи'
                   }
               }
           ,'child.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'child.'
                   ,'title': 'Childish'
                   }
               ,'ru':
                   {'short': 'детск.'
                   ,'title': 'Детская речь'
                   }
               ,'de':
                   {'short': 'Kinderspr.'
                   ,'title': 'Kindersprache'
                   }
               ,'es':
                   {'short': 'infant.'
                   ,'title': 'Infantil'
                   }
               ,'uk':
                   {'short': 'дит.'
                   ,'title': 'Дитяче мовлення'
                   }
               }
           ,'chinese.lang.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'chinese.lang.'
                   ,'title': 'Chinese'
                   }
               ,'ru':
                   {'short': 'кит.'
                   ,'title': 'Китайский язык'
                   }
               ,'de':
                   {'short': 'chin.'
                   ,'title': 'Chinesische Sprache'
                   }
               ,'es':
                   {'short': 'chin.'
                   ,'title': 'Chino'
                   }
               ,'uk':
                   {'short': 'кит.'
                   ,'title': 'Китайська мова'
                   }
               }
           ,'choreogr.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'choreogr.'
                   ,'title': 'Choreography'
                   }
               ,'ru':
                   {'short': 'хореогр.'
                   ,'title': 'Хореография'
                   }
               ,'de':
                   {'short': 'choreogr.'
                   ,'title': 'Choreography'
                   }
               ,'es':
                   {'short': 'choreogr.'
                   ,'title': 'Choreography'
                   }
               ,'uk':
                   {'short': 'хореогр.'
                   ,'title': 'Хореографія'
                   }
               }
           ,'chromat.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'chromat.'
                   ,'title': 'Chromatography'
                   }
               ,'ru':
                   {'short': 'хроматогр.'
                   ,'title': 'Хроматография'
                   }
               ,'de':
                   {'short': 'chromat.'
                   ,'title': 'Chromatography'
                   }
               ,'es':
                   {'short': 'chromat.'
                   ,'title': 'Chromatography'
                   }
               ,'uk':
                   {'short': 'хроматогр.'
                   ,'title': 'Хроматографія'
                   }
               }
           ,'cinema':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': True
               ,'en':
                   {'short': 'cinema'
                   ,'title': 'Cinematography'
                   }
               ,'ru':
                   {'short': 'кино.'
                   ,'title': 'Кинематограф'
                   }
               ,'de':
                   {'short': 'Film'
                   ,'title': 'Film'
                   }
               ,'es':
                   {'short': 'cine'
                   ,'title': 'Cinematógrafo'
                   }
               ,'uk':
                   {'short': 'кіно'
                   ,'title': 'Кінематограф'
                   }
               }
           ,'cinema.equip.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'cinema.equip.'
                   ,'title': 'Cinema equipment'
                   }
               ,'ru':
                   {'short': 'кинотех.'
                   ,'title': 'Кинотехника'
                   }
               ,'de':
                   {'short': 'cinema.equip.'
                   ,'title': 'Cinema equipment'
                   }
               ,'es':
                   {'short': 'cinema.equip.'
                   ,'title': 'Cinema equipment'
                   }
               ,'uk':
                   {'short': 'кінотех.'
                   ,'title': 'Кінотехніка'
                   }
               }
           ,'circus':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'circus'
                   ,'title': 'Circus'
                   }
               ,'ru':
                   {'short': 'цирк.'
                   ,'title': 'Цирк'
                   }
               ,'de':
                   {'short': 'circus'
                   ,'title': 'Circus'
                   }
               ,'es':
                   {'short': 'circus'
                   ,'title': 'Circus'
                   }
               ,'uk':
                   {'short': 'цирк'
                   ,'title': 'Цирк'
                   }
               }
           ,'civ.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'civ.law.'
                   ,'title': 'Civil law'
                   }
               ,'ru':
                   {'short': 'гражд.прав.'
                   ,'title': 'Гражданское право'
                   }
               ,'de':
                   {'short': 'civ.law.'
                   ,'title': 'Civil law'
                   }
               ,'es':
                   {'short': 'civ.law.'
                   ,'title': 'Civil law'
                   }
               ,'uk':
                   {'short': 'цив.пр.'
                   ,'title': 'Цивільне право'
                   }
               }
           ,'civ.proc.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'civ.proc.'
                   ,'title': 'Civil procedure'
                   }
               ,'ru':
                   {'short': 'гражд.-проц.прав.'
                   ,'title': 'Гражданско-процессуальное право'
                   }
               ,'de':
                   {'short': 'civ.proc.'
                   ,'title': 'Civil procedure'
                   }
               ,'es':
                   {'short': 'civ.proc.'
                   ,'title': 'Civil procedure'
                   }
               ,'uk':
                   {'short': 'цив.проц.пр.'
                   ,'title': 'Цивільно-процесуальне право'
                   }
               }
           ,'clas.ant.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'clas.ant.'
                   ,'title': 'Classical antiquity (excl. mythology)'
                   }
               ,'ru':
                   {'short': 'антич.'
                   ,'title': 'Античность (кроме мифологии)'
                   }
               ,'de':
                   {'short': 'Altröm.'
                   ,'title': 'Altrömisch'
                   }
               ,'es':
                   {'short': 'antig.'
                   ,'title': 'Antigüedad (sin mitología)'
                   }
               ,'uk':
                   {'short': 'антич.'
                   ,'title': 'Античність'
                   }
               }
           ,'cleric.':
               {'is_valid': True
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'cleric.'
                   ,'title': 'Clerical'
                   }
               ,'ru':
                   {'short': 'церк.'
                   ,'title': 'Церковный термин'
                   }
               ,'de':
                   {'short': 'Kirchw.'
                   ,'title': 'Kirchenwesen'
                   }
               ,'es':
                   {'short': 'ecles.'
                   ,'title': 'Eclesiástico'
                   }
               ,'uk':
                   {'short': 'церк.'
                   ,'title': 'Церковний термін'
                   }
               }
           ,'clich.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'clich.'
                   ,'title': 'Cliche'
                   }
               ,'ru':
                   {'short': 'клиш.'
                   ,'title': 'Клише'
                   }
               ,'de':
                   {'short': 'clich.'
                   ,'title': 'Cliche'
                   }
               ,'es':
                   {'short': 'clich.'
                   ,'title': 'Cliche'
                   }
               ,'uk':
                   {'short': 'кліше'
                   ,'title': 'Кліше'
                   }
               }
           ,'clim.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'clim.'
                   ,'title': 'Climatology'
                   }
               ,'ru':
                   {'short': 'клим.'
                   ,'title': 'Климатология'
                   }
               ,'de':
                   {'short': 'clim.'
                   ,'title': 'Climatology'
                   }
               ,'es':
                   {'short': 'clim.'
                   ,'title': 'Climatology'
                   }
               ,'uk':
                   {'short': 'клім.'
                   ,'title': 'Кліматологія'
                   }
               }
           ,'clin.trial.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'clin.trial.'
                   ,'title': 'Clinical trial'
                   }
               ,'ru':
                   {'short': 'клин.иссл.'
                   ,'title': 'Клинические исследования'
                   }
               ,'de':
                   {'short': 'clin.trial.'
                   ,'title': 'Clinical trial'
                   }
               ,'es':
                   {'short': 'clin.trial.'
                   ,'title': 'Clinical trial'
                   }
               ,'uk':
                   {'short': 'клін.досл.'
                   ,'title': 'Клінічні дослідження'
                   }
               }
           ,'cloth.':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'cloth.'
                   ,'title': 'Clothing'
                   }
               ,'ru':
                   {'short': 'одеж.'
                   ,'title': 'Одежда'
                   }
               ,'de':
                   {'short': 'cloth.'
                   ,'title': 'Clothing'
                   }
               ,'es':
                   {'short': 'cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'coal.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'coal.'
                   ,'title': 'Coal'
                   }
               ,'ru':
                   {'short': 'уголь.'
                   ,'title': 'Уголь'
                   }
               ,'de':
                   {'short': 'coal.'
                   ,'title': 'Coal'
                   }
               ,'es':
                   {'short': 'coal.'
                   ,'title': 'Coal'
                   }
               ,'uk':
                   {'short': 'вуг.'
                   ,'title': 'Вугілля'
                   }
               }
           ,'cockney':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'cockney'
                   ,'title': 'Cockney rhyming slang'
                   }
               ,'ru':
                   {'short': 'кокни.'
                   ,'title': 'Кокни (рифмованный сленг)'
                   }
               ,'de':
                   {'short': 'Cockney.'
                   ,'title': 'Cockney'
                   }
               ,'es':
                   {'short': 'cockney'
                   ,'title': 'Cockney rhyming slang'
                   }
               ,'uk':
                   {'short': 'кокні'
                   ,'title': 'Кокні (римований сленг)'
                   }
               }
           ,'coff.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'coff.'
                   ,'title': 'Coffee'
                   }
               ,'ru':
                   {'short': 'кофе.'
                   ,'title': 'Кофе'
                   }
               ,'de':
                   {'short': 'coff.'
                   ,'title': 'Coffee'
                   }
               ,'es':
                   {'short': 'coff.'
                   ,'title': 'Coffee'
                   }
               ,'uk':
                   {'short': 'кава'
                   ,'title': 'Кава'
                   }
               }
           ,'coll.':
               {'is_valid': True
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'coll.'
                   ,'title': 'Collective'
                   }
               ,'ru':
                   {'short': 'собир.'
                   ,'title': 'Собирательно'
                   }
               ,'de':
                   {'short': 'Verallgem.'
                   ,'title': 'Verallgemeinernd'
                   }
               ,'es':
                   {'short': 'colect.'
                   ,'title': 'Colectivo'
                   }
               ,'uk':
                   {'short': 'збірн.'
                   ,'title': 'Збірне поняття'
                   }
               }
           ,'collect.':
               {'is_valid': True
               ,'major_en': 'Collecting'
               ,'is_major': True
               ,'en':
                   {'short': 'collect.'
                   ,'title': 'Collecting'
                   }
               ,'ru':
                   {'short': 'коллекц.'
                   ,'title': 'Коллекционирование'
                   }
               ,'de':
                   {'short': 'Samm.'
                   ,'title': 'Sammeln'
                   }
               ,'es':
                   {'short': 'collect.'
                   ,'title': 'Collecting'
                   }
               ,'uk':
                   {'short': 'колекц.'
                   ,'title': 'Колекціонування'
                   }
               }
           ,'college.vern.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'college.vern.'
                   ,'title': 'College vernacular'
                   }
               ,'ru':
                   {'short': 'студ.'
                   ,'title': 'Студенческая речь'
                   }
               ,'de':
                   {'short': 'Student.Sp.'
                   ,'title': 'Studentensprache'
                   }
               ,'es':
                   {'short': 'college.vern.'
                   ,'title': 'College vernacular'
                   }
               ,'uk':
                   {'short': 'студ.сл.'
                   ,'title': 'Студентський сленг'
                   }
               }
           ,'colloid.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'colloid.chem.'
                   ,'title': 'Colloid chemistry'
                   }
               ,'ru':
                   {'short': 'коллоид.'
                   ,'title': 'Коллоидная химия'
                   }
               ,'de':
                   {'short': 'colloid.chem.'
                   ,'title': 'Colloid chemistry'
                   }
               ,'es':
                   {'short': 'colloid.chem.'
                   ,'title': 'Colloid chemistry'
                   }
               ,'uk':
                   {'short': 'колоїд.'
                   ,'title': 'Колоїдна хімія'
                   }
               }
           ,'combust.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'combust.'
                   ,'title': 'Combustion gas turbines'
                   }
               ,'ru':
                   {'short': 'газ.турб.'
                   ,'title': 'Газовые турбины'
                   }
               ,'de':
                   {'short': 'combust.'
                   ,'title': 'Combustion gas turbines'
                   }
               ,'es':
                   {'short': 'combust.'
                   ,'title': 'Combustion gas turbines'
                   }
               ,'uk':
                   {'short': 'газ.турб.'
                   ,'title': 'Газові турбіни'
                   }
               }
           ,'comic.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'comic.'
                   ,'title': 'Comics'
                   }
               ,'ru':
                   {'short': 'комикс.'
                   ,'title': 'Комиксы'
                   }
               ,'de':
                   {'short': 'comic.'
                   ,'title': 'Comics'
                   }
               ,'es':
                   {'short': 'comic.'
                   ,'title': 'Comics'
                   }
               ,'uk':
                   {'short': 'комікси'
                   ,'title': 'Комікси'
                   }
               }
           ,'commer.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'commer.'
                   ,'title': 'Commerce'
                   }
               ,'ru':
                   {'short': 'торг.'
                   ,'title': 'Торговля'
                   }
               ,'de':
                   {'short': 'Hand.'
                   ,'title': 'Handel'
                   }
               ,'es':
                   {'short': 'com.'
                   ,'title': 'Comercio'
                   }
               ,'uk':
                   {'short': 'торг.'
                   ,'title': 'Торгівля'
                   }
               }
           ,'commun.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': True
               ,'en':
                   {'short': 'commun.'
                   ,'title': 'Communications'
                   }
               ,'ru':
                   {'short': 'связь.'
                   ,'title': 'Связь'
                   }
               ,'de':
                   {'short': 'Kommunik.'
                   ,'title': 'Kommunikation'
                   }
               ,'es':
                   {'short': 'commun.'
                   ,'title': 'Communications'
                   }
               ,'uk':
                   {'short': 'зв’яз.'
                   ,'title': 'Зв’язок'
                   }
               }
           ,'comp.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': True
               ,'en':
                   {'short': 'comp.'
                   ,'title': 'Computing'
                   }
               ,'ru':
                   {'short': 'комп.'
                   ,'title': 'Компьютеры'
                   }
               ,'de':
                   {'short': 'Comp.'
                   ,'title': 'Computertechnik'
                   }
               ,'es':
                   {'short': 'comp.'
                   ,'title': 'Computadores'
                   }
               ,'uk':
                   {'short': 'комп.'
                   ,'title': "Комп'ютери"}}, 'comp., MS':
               {'is_valid': False
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'comp., MS'
                   ,'title': 'Microsoft'
                   }
               ,'ru':
                   {'short': 'комп., Майкр.'
                   ,'title': 'Майкрософт'
                   }
               ,'de':
                   {'short': 'comp., MS'
                   ,'title': 'Microsoft'
                   }
               ,'es':
                   {'short': 'comp., MS'
                   ,'title': 'Microsoft'
                   }
               ,'uk':
                   {'short': 'комп., Майкр.'
                   ,'title': 'Майкрософт'
                   }
               }
           ,'comp., net.':
               {'is_valid': False
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'comp., net.'
                   ,'title': 'Computer networks'
                   }
               ,'ru':
                   {'short': 'комп., сет.'
                   ,'title': 'Компьютерные сети'
                   }
               ,'de':
                   {'short': 'Comp., Netzw.'
                   ,'title': 'Computernetzwerke'
                   }
               ,'es':
                   {'short': 'comp., net.'
                   ,'title': 'Computer networks'
                   }
               ,'uk':
                   {'short': 'комп., мереж.'
                   ,'title': "Комп'ютерні мережі"}}, 'comp., net., abbr.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'comp., net., abbr.'
                   ,'title': 'Computer networks, Abbreviation'
                   }
               ,'ru':
                   {'short': 'комп., сет., сокр.'
                   ,'title': 'Компьютерные сети, Сокращение'
                   }
               ,'de':
                   {'short': 'Comp., Netzw., Abkürz.'
                   ,'title': 'Computernetzwerke, Abkürzung'
                   }
               ,'es':
                   {'short': 'comp., net., abrev.'
                   ,'title': 'Computer networks, Abreviatura'
                   }
               ,'uk':
                   {'short': 'комп., мереж., абрев.'
                   ,'title': "Комп'ютерні мережі, Абревіатура"}}, 'comp.games.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'comp.games.'
                   ,'title': 'Computer games'
                   }
               ,'ru':
                   {'short': 'комп.игр.'
                   ,'title': 'Компьютерные игры'
                   }
               ,'de':
                   {'short': 'comp.games.'
                   ,'title': 'Computer games'
                   }
               ,'es':
                   {'short': 'comp.games.'
                   ,'title': 'Computer games'
                   }
               ,'uk':
                   {'short': 'комп.ігри'
                   ,'title': 'Комп’ютерні ігри'
                   }
               }
           ,'comp.graph.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'comp.graph.'
                   ,'title': 'Computer graphics'
                   }
               ,'ru':
                   {'short': 'комп.граф.'
                   ,'title': 'Компьютерная графика'
                   }
               ,'de':
                   {'short': 'comp.graph.'
                   ,'title': 'Computer graphics'
                   }
               ,'es':
                   {'short': 'comp.graph.'
                   ,'title': 'Computer graphics'
                   }
               ,'uk':
                   {'short': 'комп.граф.'
                   ,'title': 'Комп’ютерна графіка'
                   }
               }
           ,'comp.name.':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': False
               ,'en':
                   {'short': 'comp.name.'
                   ,'title': 'Company name'
                   }
               ,'ru':
                   {'short': 'назв.комп.'
                   ,'title': 'Название компании'
                   }
               ,'de':
                   {'short': 'Firm.name.'
                   ,'title': 'Firmenname'
                   }
               ,'es':
                   {'short': 'comp.name.'
                   ,'title': 'Company name'
                   }
               ,'uk':
                   {'short': 'назв.комп.'
                   ,'title': 'Назва компанії'
                   }
               }
           ,'comp.sec.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'comp.sec.'
                   ,'title': 'Computer security'
                   }
               ,'ru':
                   {'short': 'комп.защ.'
                   ,'title': 'Компьютерная защита'
                   }
               ,'de':
                   {'short': 'comp.sec.'
                   ,'title': 'Computer security'
                   }
               ,'es':
                   {'short': 'comp.sec.'
                   ,'title': 'Computer security'
                   }
               ,'uk':
                   {'short': 'комп.зах.'
                   ,'title': 'Комп’ютерний захист'
                   }
               }
           ,'comp.sl., humor.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'comp.sl., humor.'
                   ,'title': 'Computing slang, Humorous / Jocular'
                   }
               ,'ru':
                   {'short': 'комп., жарг., шутл.'
                   ,'title': 'Компьютерный жаргон, Шутливое выражение'
                   }
               ,'de':
                   {'short': 'Comp.sl., scherzh.'
                   ,'title': 'Computerslang, Scherzhafter Ausdruck'
                   }
               ,'es':
                   {'short': 'comp.sl., humor.'
                   ,'title': 'Computing slang, Humorístico'
                   }
               ,'uk':
                   {'short': 'комп.жар., жарт.'
                   ,'title': 'Комп’ютерний жаргон, Жартівливий вираз'
                   }
               }
           ,'compr.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               ,'ru':
                   {'short': 'компр.'
                   ,'title': 'Компрессоры'
                   }
               ,'de':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               ,'es':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               ,'uk':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               }
           ,'concr.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'concr.'
                   ,'title': 'Concrete'
                   }
               ,'ru':
                   {'short': 'бет.'
                   ,'title': 'Бетон'
                   }
               ,'de':
                   {'short': 'Bet.'
                   ,'title': 'Beton'
                   }
               ,'es':
                   {'short': 'concr.'
                   ,'title': 'Concrete'
                   }
               ,'uk':
                   {'short': 'бетон.'
                   ,'title': 'Бетонне виробництво'
                   }
               }
           ,'confect.':
               {'is_valid': True
               ,'major_en': 'Cooking'
               ,'is_major': False
               ,'en':
                   {'short': 'confect.'
                   ,'title': 'Confectionery'
                   }
               ,'ru':
                   {'short': 'конд.'
                   ,'title': 'Кондитерские изделия'
                   }
               ,'de':
                   {'short': 'Feingeb.'
                   ,'title': 'Feingebäck'
                   }
               ,'es':
                   {'short': 'confect.'
                   ,'title': 'Confectionery'
                   }
               ,'uk':
                   {'short': 'солод.'
                   ,'title': 'Солодощі'
                   }
               }
           ,'construct.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': True
               ,'en':
                   {'short': 'construct.'
                   ,'title': 'Construction'
                   }
               ,'ru':
                   {'short': 'стр.'
                   ,'title': 'Строительство'
                   }
               ,'de':
                   {'short': 'Bauw.'
                   ,'title': 'Bauwesen'
                   }
               ,'es':
                   {'short': 'constr.'
                   ,'title': 'Construcción'
                   }
               ,'uk':
                   {'short': 'буд.'
                   ,'title': 'Будівництво'
                   }
               }
           ,'consult.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'consult.'
                   ,'title': 'Consulting'
                   }
               ,'ru':
                   {'short': 'консалт.'
                   ,'title': 'Консалтинг'
                   }
               ,'de':
                   {'short': 'Berat.'
                   ,'title': 'Beratung'
                   }
               ,'es':
                   {'short': 'consult.'
                   ,'title': 'Consulting'
                   }
               ,'uk':
                   {'short': 'консалт.'
                   ,'title': 'Консалтинг'
                   }
               }
           ,'contempt.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'contempt.'
                   ,'title': 'Contemptuous'
                   }
               ,'ru':
                   {'short': 'презр.'
                   ,'title': 'Презрительно'
                   }
               ,'de':
                   {'short': 'Verächt.'
                   ,'title': 'Verächtlich'
                   }
               ,'es':
                   {'short': 'despect.'
                   ,'title': 'Despectivamente'
                   }
               ,'uk':
                   {'short': 'презирл.'
                   ,'title': 'Презирливий вираз'
                   }
               }
           ,'context.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'context.'
                   ,'title': 'Contextual meaning'
                   }
               ,'ru':
                   {'short': 'конт.'
                   ,'title': 'Контекстуальное значение'
                   }
               ,'de':
                   {'short': 'context.'
                   ,'title': 'Contextual meaning'
                   }
               ,'es':
                   {'short': 'context.'
                   ,'title': 'Contextual meaning'
                   }
               ,'uk':
                   {'short': 'конт.'
                   ,'title': 'Контекстуальне значення'
                   }
               }
           ,'conv.ind.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'conv.ind.'
                   ,'title': 'Converter industry'
                   }
               ,'ru':
                   {'short': 'конв.'
                   ,'title': 'Конвертерное производство'
                   }
               ,'de':
                   {'short': 'Knvbtb.'
                   ,'title': 'Konverterbetrieb'
                   }
               ,'es':
                   {'short': 'conv.ind.'
                   ,'title': 'Converter industry'
                   }
               ,'uk':
                   {'short': 'конв.'
                   ,'title': 'Конвертерне виробництво'
                   }
               }
           ,'conv.notation.':
               {'is_valid': True
               ,'major_en': 'Subjects for Chinese dictionaries (container)'
               ,'is_major': False
               ,'en':
                   {'short': 'conv.notation.'
                   ,'title': 'Conventional notation'
                   }
               ,'ru':
                   {'short': 'усл.'
                   ,'title': 'Условное обозначение'
                   }
               ,'de':
                   {'short': 'conv.notation.'
                   ,'title': 'Conventional notation'
                   }
               ,'es':
                   {'short': 'conv.notation.'
                   ,'title': 'Conventional notation'
                   }
               ,'uk':
                   {'short': 'умов.'
                   ,'title': 'Умовне позначення'
                   }
               }
           ,'cook.':
               {'is_valid': True
               ,'major_en': 'Cooking'
               ,'is_major': True
               ,'en':
                   {'short': 'cook.'
                   ,'title': 'Cooking'
                   }
               ,'ru':
                   {'short': 'кул.'
                   ,'title': 'Кулинария'
                   }
               ,'de':
                   {'short': 'Gastron.'
                   ,'title': 'Gastronomie'
                   }
               ,'es':
                   {'short': 'cocina'
                   ,'title': 'Cocina'
                   }
               ,'uk':
                   {'short': 'кул.'
                   ,'title': 'Кулінарія'
                   }
               }
           ,'coop.':
               {'is_valid': True
               ,'major_en': 'Crafts'
               ,'is_major': False
               ,'en':
                   {'short': 'coop.'
                   ,'title': 'Cooperage'
                   }
               ,'ru':
                   {'short': 'бонд.'
                   ,'title': 'Бондарное производство'
                   }
               ,'de':
                   {'short': 'coop.'
                   ,'title': 'Cooperage'
                   }
               ,'es':
                   {'short': 'coop.'
                   ,'title': 'Cooperage'
                   }
               ,'uk':
                   {'short': 'бонд.'
                   ,'title': 'Бондарство'
                   }
               }
           ,'corp.gov.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'corp.gov.'
                   ,'title': 'Corporate governance'
                   }
               ,'ru':
                   {'short': 'корп.упр.'
                   ,'title': 'Корпоративное управление'
                   }
               ,'de':
                   {'short': 'corp.gov.'
                   ,'title': 'Corporate governance'
                   }
               ,'es':
                   {'short': 'corp.gov.'
                   ,'title': 'Corporate governance'
                   }
               ,'uk':
                   {'short': 'корп.упр.'
                   ,'title': 'Корпоративне управління'
                   }
               }
           ,'corrupt.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'corrupt.'
                   ,'title': 'Combating corruption'
                   }
               ,'ru':
                   {'short': 'коррупц.'
                   ,'title': 'Борьба с коррупцией'
                   }
               ,'de':
                   {'short': 'corrupt.'
                   ,'title': 'Combating corruption'
                   }
               ,'es':
                   {'short': 'corrupt.'
                   ,'title': 'Combating corruption'
                   }
               ,'uk':
                   {'short': 'корупц.'
                   ,'title': 'Боротьба з корупцією'
                   }
               }
           ,'cosmet.':
               {'is_valid': True
               ,'major_en': 'Wellness'
               ,'is_major': False
               ,'en':
                   {'short': 'cosmet.'
                   ,'title': 'Cosmetics and cosmetology'
                   }
               ,'ru':
                   {'short': 'космет.'
                   ,'title': 'Косметика и косметология'
                   }
               ,'de':
                   {'short': 'cosmet.'
                   ,'title': 'Cosmetics and cosmetology'
                   }
               ,'es':
                   {'short': 'cosmet.'
                   ,'title': 'Cosmetics and cosmetology'
                   }
               ,'uk':
                   {'short': 'космет.'
                   ,'title': 'Косметика і косметологія'
                   }
               }
           ,'crim.jarg.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'crim.jarg.'
                   ,'title': 'Criminal jargon'
                   }
               ,'ru':
                   {'short': 'угол.жарг.'
                   ,'title': 'Уголовный жаргон'
                   }
               ,'de':
                   {'short': 'Krim.jarg.'
                   ,'title': 'Kriminaljargon'
                   }
               ,'es':
                   {'short': 'crim.jarg.'
                   ,'title': 'Criminal jargon'
                   }
               ,'uk':
                   {'short': 'крим.жарг.'
                   ,'title': 'Кримінальний жаргон'
                   }
               }
           ,'crim.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'crim.law.'
                   ,'title': 'Criminal law'
                   }
               ,'ru':
                   {'short': 'угол.'
                   ,'title': 'Уголовное право'
                   }
               ,'de':
                   {'short': 'Strafrecht'
                   ,'title': 'Strafrecht'
                   }
               ,'es':
                   {'short': 'crim.law.'
                   ,'title': 'Criminal law'
                   }
               ,'uk':
                   {'short': 'крим.пр.'
                   ,'title': 'Кримінальне право'
                   }
               }
           ,'cryptogr.':
               {'is_valid': True
               ,'major_en': 'Security systems'
               ,'is_major': False
               ,'en':
                   {'short': 'cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'ru':
                   {'short': 'криптогр.'
                   ,'title': 'Криптография'
                   }
               ,'de':
                   {'short': 'cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'es':
                   {'short': 'cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'uk':
                   {'short': 'крипт.'
                   ,'title': 'Криптографія'
                   }
               }
           ,'crystall.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'crystall.'
                   ,'title': 'Crystallography'
                   }
               ,'ru':
                   {'short': 'крист.'
                   ,'title': 'Кристаллография'
                   }
               ,'de':
                   {'short': 'Kristallogr.'
                   ,'title': 'Kristallographie'
                   }
               ,'es':
                   {'short': 'crystall.'
                   ,'title': 'Crystallography'
                   }
               ,'uk':
                   {'short': 'крист.'
                   ,'title': 'Кристалографія'
                   }
               }
           ,'cultur.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'cultur.'
                   ,'title': 'Cultural studies'
                   }
               ,'ru':
                   {'short': 'культур.'
                   ,'title': 'Культурология'
                   }
               ,'de':
                   {'short': 'cultur.'
                   ,'title': 'Cultural studies'
                   }
               ,'es':
                   {'short': 'cultur.'
                   ,'title': 'Cultural studies'
                   }
               ,'uk':
                   {'short': 'культур.'
                   ,'title': 'Культурологія'
                   }
               }
           ,'curr.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'curr.'
                   ,'title': 'Currencies and monetary policy'
                   }
               ,'ru':
                   {'short': 'валют.'
                   ,'title': 'Валюты и монетарная политика (кроме форекс)'
                   }
               ,'de':
                   {'short': 'Währ.'
                   ,'title': 'Währungen und monetäre Politik'
                   }
               ,'es':
                   {'short': 'curr.'
                   ,'title': 'Currencies and monetary policy'
                   }
               ,'uk':
                   {'short': 'валют.'
                   ,'title': 'Валюти та монетарна політика (окрім форекс)'
                   }
               }
           ,'cust.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'cust.'
                   ,'title': 'Customs'
                   }
               ,'ru':
                   {'short': 'тамож.'
                   ,'title': 'Таможенное дело'
                   }
               ,'de':
                   {'short': 'Zoll.'
                   ,'title': 'Zollwesen'
                   }
               ,'es':
                   {'short': 'cust.'
                   ,'title': 'Customs'
                   }
               ,'uk':
                   {'short': 'митн.'
                   ,'title': 'Митна справа'
                   }
               }
           ,'cyber.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'cyber.'
                   ,'title': 'Cybernetics'
                   }
               ,'ru':
                   {'short': 'киб.'
                   ,'title': 'Кибернетика'
                   }
               ,'de':
                   {'short': 'Kybernet.'
                   ,'title': 'Kybernetik'
                   }
               ,'es':
                   {'short': 'cyber.'
                   ,'title': 'Cybernetics'
                   }
               ,'uk':
                   {'short': 'кіб.'
                   ,'title': 'Кібернетика'
                   }
               }
           ,'cyc.sport':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'cyc.sport'
                   ,'title': 'Cycle sport'
                   }
               ,'ru':
                   {'short': 'вело.спорт.'
                   ,'title': 'Велоспорт'
                   }
               ,'de':
                   {'short': 'cyc.sport'
                   ,'title': 'Cycle sport'
                   }
               ,'es':
                   {'short': 'cyc.sport'
                   ,'title': 'Cycle sport'
                   }
               ,'uk':
                   {'short': 'вел.спорт'
                   ,'title': 'Велоспорт'
                   }
               }
           ,'cycl.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'cycl.'
                   ,'title': 'Cycling (other than sport)'
                   }
               ,'ru':
                   {'short': 'вело.'
                   ,'title': 'Велосипеды (кроме спорта)'
                   }
               ,'de':
                   {'short': 'cycl.'
                   ,'title': 'Cycling (other than sport)'
                   }
               ,'es':
                   {'short': 'cycl.'
                   ,'title': 'Cycling (other than sport)'
                   }
               ,'uk':
                   {'short': 'вело.'
                   ,'title': 'Велосипеди (крім спорту)'
                   }
               }
           ,'cytog.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'cytog.'
                   ,'title': 'Cytogenetics'
                   }
               ,'ru':
                   {'short': 'цитоген.'
                   ,'title': 'Цитогенетика'
                   }
               ,'de':
                   {'short': 'cytog.'
                   ,'title': 'Cytogenetics'
                   }
               ,'es':
                   {'short': 'cytog.'
                   ,'title': 'Cytogenetics'
                   }
               ,'uk':
                   {'short': 'цитоген.'
                   ,'title': 'Цитогенетика'
                   }
               }
           ,'cytol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'cytol.'
                   ,'title': 'Cytology'
                   }
               ,'ru':
                   {'short': 'цитол.'
                   ,'title': 'Цитология'
                   }
               ,'de':
                   {'short': 'Zellbiol.'
                   ,'title': 'Zellbiologie'
                   }
               ,'es':
                   {'short': 'citol.'
                   ,'title': 'Citología'
                   }
               ,'uk':
                   {'short': 'цитол.'
                   ,'title': 'Цитологія'
                   }
               }
           ,'d.b..':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'd.b..'
                   ,'title': 'Databases'
                   }
               ,'ru':
                   {'short': 'б.д.'
                   ,'title': 'Базы данных'
                   }
               ,'de':
                   {'short': 'd.b..'
                   ,'title': 'Databases'
                   }
               ,'es':
                   {'short': 'd.b..'
                   ,'title': 'Databases'
                   }
               ,'uk':
                   {'short': 'БД'
                   ,'title': 'Бази даних'
                   }
               }
           ,'dactyl.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'dactyl.'
                   ,'title': 'Dactyloscopy'
                   }
               ,'ru':
                   {'short': 'дактил.'
                   ,'title': 'Дактилоскопия'
                   }
               ,'de':
                   {'short': 'dactyl.'
                   ,'title': 'Dactyloscopy'
                   }
               ,'es':
                   {'short': 'dactyl.'
                   ,'title': 'Dactyloscopy'
                   }
               ,'uk':
                   {'short': 'дактил.'
                   ,'title': 'Дактилоскопія'
                   }
               }
           ,'dam.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'dam.'
                   ,'title': 'Dams'
                   }
               ,'ru':
                   {'short': 'дамб.'
                   ,'title': 'Дамбы'
                   }
               ,'de':
                   {'short': 'dam.'
                   ,'title': 'Dams'
                   }
               ,'es':
                   {'short': 'dam.'
                   ,'title': 'Dams'
                   }
               ,'uk':
                   {'short': 'дамб.'
                   ,'title': 'Дамби'
                   }
               }
           ,'dan.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'dan.'
                   ,'title': 'Danish'
                   }
               ,'ru':
                   {'short': 'датск.'
                   ,'title': 'Датский язык'
                   }
               ,'de':
                   {'short': 'Dän.'
                   ,'title': 'Dänisch'
                   }
               ,'es':
                   {'short': 'dan.'
                   ,'title': 'Danish'
                   }
               ,'uk':
                   {'short': 'дан.'
                   ,'title': 'Данська мова'
                   }
               }
           ,'danc.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'danc.'
                   ,'title': 'Dancing'
                   }
               ,'ru':
                   {'short': 'танц.'
                   ,'title': 'Танцы'
                   }
               ,'de':
                   {'short': 'danc.'
                   ,'title': 'Dancing'
                   }
               ,'es':
                   {'short': 'danc.'
                   ,'title': 'Dancing'
                   }
               ,'uk':
                   {'short': 'танц.'
                   ,'title': 'Танці'
                   }
               }
           ,'dat.proc.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'dat.proc.'
                   ,'title': 'Data processing'
                   }
               ,'ru':
                   {'short': 'обр.дан.'
                   ,'title': 'Обработка данных'
                   }
               ,'de':
                   {'short': 'Datenverarb.'
                   ,'title': 'Datenverarbeitung'
                   }
               ,'es':
                   {'short': 'dat.proc.'
                   ,'title': 'Data processing'
                   }
               ,'uk':
                   {'short': 'обр.дан.'
                   ,'title': 'Обробка даних'
                   }
               }
           ,'deaf.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'deaf.'
                   ,'title': 'Deafblindness'
                   }
               ,'ru':
                   {'short': 'глух.'
                   ,'title': 'Слепоглухота'
                   }
               ,'de':
                   {'short': 'deaf.'
                   ,'title': 'Deafblindness'
                   }
               ,'es':
                   {'short': 'deaf.'
                   ,'title': 'Deafblindness'
                   }
               ,'uk':
                   {'short': 'сліпоглух.'
                   ,'title': 'Сліпоглухота'
                   }
               }
           ,'demogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'demogr.'
                   ,'title': 'Demography'
                   }
               ,'ru':
                   {'short': 'демогр.'
                   ,'title': 'Демография'
                   }
               ,'de':
                   {'short': 'Demograf.'
                   ,'title': 'Demografie'
                   }
               ,'es':
                   {'short': 'demogr.'
                   ,'title': 'Demography'
                   }
               ,'uk':
                   {'short': 'демогр.'
                   ,'title': 'Демографія'
                   }
               }
           ,'dent.impl.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'dent.impl.'
                   ,'title': 'Dental implantology'
                   }
               ,'ru':
                   {'short': 'зуб.импл.'
                   ,'title': 'Зубная имплантология'
                   }
               ,'de':
                   {'short': 'dent.impl.'
                   ,'title': 'Dental implantology'
                   }
               ,'es':
                   {'short': 'dent.impl.'
                   ,'title': 'Dental implantology'
                   }
               ,'uk':
                   {'short': 'зуб.імп.'
                   ,'title': 'Зубна імплантологія'
                   }
               }
           ,'dentist.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'dentist.'
                   ,'title': 'Dentistry'
                   }
               ,'ru':
                   {'short': 'стом.'
                   ,'title': 'Стоматология'
                   }
               ,'de':
                   {'short': 'Zahnmed.'
                   ,'title': 'Zahnmedizin'
                   }
               ,'es':
                   {'short': 'odont.'
                   ,'title': 'Odontología'
                   }
               ,'uk':
                   {'short': 'стом.'
                   ,'title': 'Стоматологія'
                   }
               }
           ,'derbet.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'derbet.'
                   ,'title': 'Derbet language'
                   }
               ,'ru':
                   {'short': 'дербет.'
                   ,'title': 'Дербетский диалект'
                   }
               ,'de':
                   {'short': 'derbet.'
                   ,'title': 'Derbet language'
                   }
               ,'es':
                   {'short': 'derbet.'
                   ,'title': 'Derbet language'
                   }
               ,'uk':
                   {'short': 'дербет.'
                   ,'title': 'Дербетський діалект'
                   }
               }
           ,'dermat.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'dermat.'
                   ,'title': 'Dermatology'
                   }
               ,'ru':
                   {'short': 'дерм.'
                   ,'title': 'Дерматология'
                   }
               ,'de':
                   {'short': 'Dermatol.'
                   ,'title': 'Dermatologie'
                   }
               ,'es':
                   {'short': 'dermat.'
                   ,'title': 'Dermatología'
                   }
               ,'uk':
                   {'short': 'дерм.'
                   ,'title': 'Дерматологія'
                   }
               }
           ,'derog.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'derog.'
                   ,'title': 'Derogatory'
                   }
               ,'ru':
                   {'short': 'пренебр.'
                   ,'title': 'Пренебрежительно'
                   }
               ,'de':
                   {'short': 'derog.'
                   ,'title': 'Derogatory'
                   }
               ,'es':
                   {'short': 'derog.'
                   ,'title': 'Derogatory'
                   }
               ,'uk':
                   {'short': 'зневаж.'
                   ,'title': 'Зневажливо'
                   }
               }
           ,'desert.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               ,'ru':
                   {'short': 'пустын.'
                   ,'title': 'Наука о пустынях'
                   }
               ,'de':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               ,'es':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               ,'uk':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               }
           ,'design.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'design.'
                   ,'title': 'Design'
                   }
               ,'ru':
                   {'short': 'диз.'
                   ,'title': 'Дизайн'
                   }
               ,'de':
                   {'short': 'design.'
                   ,'title': 'Design'
                   }
               ,'es':
                   {'short': 'design.'
                   ,'title': 'Design'
                   }
               ,'uk':
                   {'short': 'диз.'
                   ,'title': 'Дизайн'
                   }
               }
           ,'dial.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': True
               ,'en':
                   {'short': 'dial.'
                   ,'title': 'Dialectal'
                   }
               ,'ru':
                   {'short': 'диал.'
                   ,'title': 'Диалектизм'
                   }
               ,'de':
                   {'short': 'Dial.'
                   ,'title': 'Dialekt'
                   }
               ,'es':
                   {'short': 'dial.'
                   ,'title': 'Dialecto'
                   }
               ,'uk':
                   {'short': 'діал.'
                   ,'title': 'Діалектизм'
                   }
               }
           ,'dialys.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'dialys.'
                   ,'title': 'Dyalysis'
                   }
               ,'ru':
                   {'short': 'диализ.'
                   ,'title': 'Диализ'
                   }
               ,'de':
                   {'short': 'dialys.'
                   ,'title': 'Dyalysis'
                   }
               ,'es':
                   {'short': 'dialys.'
                   ,'title': 'Dyalysis'
                   }
               ,'uk':
                   {'short': 'діаліз'
                   ,'title': 'Діаліз'
                   }
               }
           ,'diet.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'diet.'
                   ,'title': 'Dietology'
                   }
               ,'ru':
                   {'short': 'диет.'
                   ,'title': 'Диетология'
                   }
               ,'de':
                   {'short': 'diet.'
                   ,'title': 'Dietology'
                   }
               ,'es':
                   {'short': 'diet.'
                   ,'title': 'Dietology'
                   }
               ,'uk':
                   {'short': 'дієтол.'
                   ,'title': 'Дієтологія'
                   }
               }
           ,'dig.curr.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'dig.curr.'
                   ,'title': 'Digital and cryptocurrencies'
                   }
               ,'ru':
                   {'short': 'цифр.вал.'
                   ,'title': 'Цифровые и криптовалюты'
                   }
               ,'de':
                   {'short': 'dig.curr.'
                   ,'title': 'Digital and cryptocurrencies'
                   }
               ,'es':
                   {'short': 'dig.curr.'
                   ,'title': 'Digital and cryptocurrencies'
                   }
               ,'uk':
                   {'short': 'цифр.вал.'
                   ,'title': 'Цифрові та криптовалюти'
                   }
               }
           ,'dimin.':
               {'is_valid': True
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'dimin.'
                   ,'title': 'Diminutive'
                   }
               ,'ru':
                   {'short': 'уменьш.'
                   ,'title': 'Уменьшительно'
                   }
               ,'de':
                   {'short': 'Dimin.'
                   ,'title': 'Diminutiv'
                   }
               ,'es':
                   {'short': 'dimin.'
                   ,'title': 'Diminutive'
                   }
               ,'uk':
                   {'short': 'зменш.'
                   ,'title': 'Зменшувально'
                   }
               }
           ,'dipl.':
               {'is_valid': True
               ,'major_en': 'Foreign affairs'
               ,'is_major': False
               ,'en':
                   {'short': 'dipl.'
                   ,'title': 'Diplomacy'
                   }
               ,'ru':
                   {'short': 'дип.'
                   ,'title': 'Дипломатия'
                   }
               ,'de':
                   {'short': 'Dipl.'
                   ,'title': 'Diplomatie'
                   }
               ,'es':
                   {'short': 'dipl.'
                   ,'title': 'Diplomacia'
                   }
               ,'uk':
                   {'short': 'дип.'
                   ,'title': 'Дипломатія'
                   }
               }
           ,'dipl., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'dipl., amer.usg.'
                   ,'title': 'Diplomacy, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'дип., амер.'
                   ,'title': 'Дипломатия, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Dipl., Amerik.'
                   ,'title': 'Diplomatie, Amerikanisch'
                   }
               ,'es':
                   {'short': 'dipl., amer.'
                   ,'title': 'Diplomacia, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'дип., амер.вир.'
                   ,'title': 'Дипломатія, Американський вираз (не варыант мови)'
                   }
               }
           ,'disappr.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'disappr.'
                   ,'title': 'Disapproving'
                   }
               ,'ru':
                   {'short': 'неодобр.'
                   ,'title': 'Неодобрительно'
                   }
               ,'de':
                   {'short': 'mißbill.'
                   ,'title': 'Mißbilligend'
                   }
               ,'es':
                   {'short': 'desaprob.'
                   ,'title': 'Desaprobadoramente'
                   }
               ,'uk':
                   {'short': 'несхв.'
                   ,'title': 'Несхвально'
                   }
               }
           ,'disast.':
               {'is_valid': True
               ,'major_en': 'Politics'
               ,'is_major': False
               ,'en':
                   {'short': 'disast.'
                   ,'title': 'Disaster recovery'
                   }
               ,'ru':
                   {'short': 'авар.'
                   ,'title': 'Аварийное восстановление'
                   }
               ,'de':
                   {'short': 'disast.'
                   ,'title': 'Disaster recovery'
                   }
               ,'es':
                   {'short': 'disast.'
                   ,'title': 'Disaster recovery'
                   }
               ,'uk':
                   {'short': 'авар.'
                   ,'title': 'Аварійне відновлення'
                   }
               }
           ,'distil.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'distil.'
                   ,'title': 'Distillation'
                   }
               ,'ru':
                   {'short': 'дистил.'
                   ,'title': 'Дистилляция'
                   }
               ,'de':
                   {'short': 'distil.'
                   ,'title': 'Distillation'
                   }
               ,'es':
                   {'short': 'distil.'
                   ,'title': 'Distillation'
                   }
               ,'uk':
                   {'short': 'дистил.'
                   ,'title': 'Дистиляція'
                   }
               }
           ,'dog.':
               {'is_valid': True
               ,'major_en': 'Companion animals'
               ,'is_major': False
               ,'en':
                   {'short': 'dog.'
                   ,'title': 'Dog breeding'
                   }
               ,'ru':
                   {'short': 'собак.'
                   ,'title': 'Собаководство (кинология)'
                   }
               ,'de':
                   {'short': 'dog.'
                   ,'title': 'Dog breeding'
                   }
               ,'es':
                   {'short': 'dog.'
                   ,'title': 'Dog breeding'
                   }
               ,'uk':
                   {'short': 'собак.'
                   ,'title': 'Собаківництво'
                   }
               }
           ,'dominic.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'dominic.'
                   ,'title': 'Dominican Republic'
                   }
               ,'ru':
                   {'short': 'доминик.'
                   ,'title': 'Доминиканская Республика'
                   }
               ,'de':
                   {'short': 'dominic.'
                   ,'title': 'Dominican Republic'
                   }
               ,'es':
                   {'short': 'dominic.'
                   ,'title': 'Dominican Republic'
                   }
               ,'uk':
                   {'short': 'домінік.'
                   ,'title': 'Домініканська Республіка'
                   }
               }
           ,'dril.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'dril.'
                   ,'title': 'Drilling'
                   }
               ,'ru':
                   {'short': 'бур.'
                   ,'title': 'Бурение'
                   }
               ,'de':
                   {'short': 'Bohr.'
                   ,'title': 'Bohren'
                   }
               ,'es':
                   {'short': 'dril.'
                   ,'title': 'Drilling'
                   }
               ,'uk':
                   {'short': 'бур.'
                   ,'title': 'Буріння'
                   }
               }
           ,'drug.name':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'drug.name'
                   ,'title': 'Drug name'
                   }
               ,'ru':
                   {'short': 'назв.лек.'
                   ,'title': 'Название лекарственного средства'
                   }
               ,'de':
                   {'short': 'drug.name'
                   ,'title': 'Drug name'
                   }
               ,'es':
                   {'short': 'drug.name'
                   ,'title': 'Drug name'
                   }
               ,'uk':
                   {'short': 'назв.лік.'
                   ,'title': 'Назва лікарського засобу'
                   }
               }
           ,'drugs':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'drugs'
                   ,'title': 'Drugs and addiction medicine'
                   }
               ,'ru':
                   {'short': 'нарк.'
                   ,'title': 'Наркотики и наркология'
                   }
               ,'de':
                   {'short': 'drugs'
                   ,'title': 'Drugs and addiction medicine'
                   }
               ,'es':
                   {'short': 'drugs'
                   ,'title': 'Drugs and addiction medicine'
                   }
               ,'uk':
                   {'short': 'нарк.'
                   ,'title': 'Наркотики та наркологія'
                   }
               }
           ,'drv.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'drv.'
                   ,'title': 'Drives'
                   }
               ,'ru':
                   {'short': 'прив.'
                   ,'title': 'Приводы'
                   }
               ,'de':
                   {'short': 'drv.'
                   ,'title': 'Drives'
                   }
               ,'es':
                   {'short': 'drv.'
                   ,'title': 'Drives'
                   }
               ,'uk':
                   {'short': 'прив.'
                   ,'title': 'Привод'
                   }
               }
           ,'drw.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'drw.'
                   ,'title': 'Drawing'
                   }
               ,'ru':
                   {'short': 'черч.'
                   ,'title': 'Черчение'
                   }
               ,'de':
                   {'short': 'drw.'
                   ,'title': 'Drawing'
                   }
               ,'es':
                   {'short': 'drw.'
                   ,'title': 'Drawing'
                   }
               ,'uk':
                   {'short': 'крес.'
                   ,'title': 'Креслення'
                   }
               }
           ,'drywall':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'drywall'
                   ,'title': 'Drywall'
                   }
               ,'ru':
                   {'short': 'гипсокарт.'
                   ,'title': 'Гипсокартон и сис-мы сухого строительства'
                   }
               ,'de':
                   {'short': 'gipskart.'
                   ,'title': 'Gipskarton u. Trockenbausysteme'
                   }
               ,'es':
                   {'short': 'drywall'
                   ,'title': 'Drywall'
                   }
               ,'uk':
                   {'short': 'гіпсокарт.'
                   ,'title': 'Гипсокартон та сис-ми сухого будівництва'
                   }
               }
           ,'dye.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'dye.'
                   ,'title': 'Dyes'
                   }
               ,'ru':
                   {'short': 'крас.'
                   ,'title': 'Красители'
                   }
               ,'de':
                   {'short': 'dye.'
                   ,'title': 'Dyes'
                   }
               ,'es':
                   {'short': 'dye.'
                   ,'title': 'Dyes'
                   }
               ,'uk':
                   {'short': 'барвн.'
                   ,'title': 'Барвники'
                   }
               }
           ,'ecol.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': False
               ,'en':
                   {'short': 'ecol.'
                   ,'title': 'Ecology'
                   }
               ,'ru':
                   {'short': 'экол.'
                   ,'title': 'Экология'
                   }
               ,'de':
                   {'short': 'Ökol.'
                   ,'title': 'Ökologie'
                   }
               ,'es':
                   {'short': 'ecol.'
                   ,'title': 'Ecology'
                   }
               ,'uk':
                   {'short': 'екол.'
                   ,'title': 'Екологія'
                   }
               }
           ,'econ.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': True
               ,'en':
                   {'short': 'econ.'
                   ,'title': 'Economy'
                   }
               ,'ru':
                   {'short': 'эк.'
                   ,'title': 'Экономика'
                   }
               ,'de':
                   {'short': 'Wirtsch.'
                   ,'title': 'Wirtschaft'
                   }
               ,'es':
                   {'short': 'econ.'
                   ,'title': 'Economía'
                   }
               ,'uk':
                   {'short': 'ек.'
                   ,'title': 'Економіка'
                   }
               }
           ,'econ., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'econ., amer.usg.'
                   ,'title': 'Economy, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'эк., амер.'
                   ,'title': 'Экономика, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Wirtsch., Amerik.'
                   ,'title': 'Wirtschaft, Amerikanisch'
                   }
               ,'es':
                   {'short': 'econ., amer.'
                   ,'title': 'Economía, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ек., амер.вир.'
                   ,'title': 'Економіка, Американський вираз (не варыант мови)'
                   }
               }
           ,'econ.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'econ.law.'
                   ,'title': 'Economic law'
                   }
               ,'ru':
                   {'short': 'хоз.прав.'
                   ,'title': 'Хозйственное (предпринимательское) право'
                   }
               ,'de':
                   {'short': 'econ.law.'
                   ,'title': 'Economic law'
                   }
               ,'es':
                   {'short': 'econ.law.'
                   ,'title': 'Economic law'
                   }
               ,'uk':
                   {'short': 'госп.пр.'
                   ,'title': 'Господарське право'
                   }
               }
           ,'econometr.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'econometr.'
                   ,'title': 'Econometrics'
                   }
               ,'ru':
                   {'short': 'эконометр.'
                   ,'title': 'Эконометрика'
                   }
               ,'de':
                   {'short': 'econometr.'
                   ,'title': 'Econometrics'
                   }
               ,'es':
                   {'short': 'econometr.'
                   ,'title': 'Econometrics'
                   }
               ,'uk':
                   {'short': 'економетр.'
                   ,'title': 'Економетрика'
                   }
               }
           ,'ed.':
               {'is_valid': True
               ,'major_en': 'Education'
               ,'is_major': True
               ,'en':
                   {'short': 'ed.'
                   ,'title': 'Education'
                   }
               ,'ru':
                   {'short': 'обр.'
                   ,'title': 'Образование'
                   }
               ,'de':
                   {'short': 'Ausbild.'
                   ,'title': 'Ausbildung'
                   }
               ,'es':
                   {'short': 'ed.'
                   ,'title': 'Education'
                   }
               ,'uk':
                   {'short': 'осв.'
                   ,'title': 'Освіта'
                   }
               }
           ,'ed., subj.':
               {'is_valid': False
               ,'major_en': 'Education'
               ,'is_major': False
               ,'en':
                   {'short': 'ed., subj.'
                   ,'title': 'School and university subjects'
                   }
               ,'ru':
                   {'short': 'обр., предм.'
                   ,'title': 'Названия учебных предметов'
                   }
               ,'de':
                   {'short': 'ed., subj.'
                   ,'title': 'School and university subjects'
                   }
               ,'es':
                   {'short': 'ed., subj.'
                   ,'title': 'School and university subjects'
                   }
               ,'uk':
                   {'short': 'осв., предм.'
                   ,'title': 'Назви навчальних предметів'
                   }
               }
           ,'egypt.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'egypt.'
                   ,'title': 'Egyptology'
                   }
               ,'ru':
                   {'short': 'египт.'
                   ,'title': 'Египтология'
                   }
               ,'de':
                   {'short': 'Ägyptol.'
                   ,'title': 'Ägyptologie'
                   }
               ,'es':
                   {'short': 'egypt.'
                   ,'title': 'Egyptology'
                   }
               ,'uk':
                   {'short': 'єгипт.'
                   ,'title': 'Єгиптологія'
                   }
               }
           ,'el.':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': True
               ,'en':
                   {'short': 'el.'
                   ,'title': 'Electronics'
                   }
               ,'ru':
                   {'short': 'эл.'
                   ,'title': 'Электроника'
                   }
               ,'de':
                   {'short': 'el.'
                   ,'title': 'Elektronik'
                   }
               ,'es':
                   {'short': 'electr.'
                   ,'title': 'Electrónica'
                   }
               ,'uk':
                   {'short': 'ел.'
                   ,'title': 'Електроніка'
                   }
               }
           ,'el.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'el.chem.'
                   ,'title': 'Electrochemistry'
                   }
               ,'ru':
                   {'short': 'элхим.'
                   ,'title': 'Электрохимия'
                   }
               ,'de':
                   {'short': 'el.chem.'
                   ,'title': 'Electrochemistry'
                   }
               ,'es':
                   {'short': 'el.chem.'
                   ,'title': 'Electrochemistry'
                   }
               ,'uk':
                   {'short': 'ел.хім.'
                   ,'title': 'Електрохімія'
                   }
               }
           ,'el.com.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'el.com.'
                   ,'title': 'Electronic commerce'
                   }
               ,'ru':
                   {'short': 'эл.торг.'
                   ,'title': 'Электронная торговля'
                   }
               ,'de':
                   {'short': 'el.com.'
                   ,'title': 'Electronic commerce'
                   }
               ,'es':
                   {'short': 'el.com.'
                   ,'title': 'Electronic commerce'
                   }
               ,'uk':
                   {'short': 'ел.торг.'
                   ,'title': 'Електронна торгівля'
                   }
               }
           ,'el.gen.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'el.gen.'
                   ,'title': 'Electricity generation'
                   }
               ,'ru':
                   {'short': 'произв.эл.'
                   ,'title': 'Производство электроэнергии'
                   }
               ,'de':
                   {'short': 'Elektr.erz.'
                   ,'title': 'Elektrizitätserzeugung'
                   }
               ,'es':
                   {'short': 'el.gen.'
                   ,'title': 'Electricity generation'
                   }
               ,'uk':
                   {'short': 'виробн.електр.'
                   ,'title': 'Виробництво електроенергії'
                   }
               }
           ,'el.mach.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'el.mach.'
                   ,'title': 'Electric machinery'
                   }
               ,'ru':
                   {'short': 'эл.маш.'
                   ,'title': 'Электрические машины'
                   }
               ,'de':
                   {'short': 'el.mach.'
                   ,'title': 'Electric machinery'
                   }
               ,'es':
                   {'short': 'el.mach.'
                   ,'title': 'Electric machinery'
                   }
               ,'uk':
                   {'short': 'ел.маш.'
                   ,'title': 'Електричні машини'
                   }
               }
           ,'el.med.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'el.med.'
                   ,'title': 'Electromedicine'
                   }
               ,'ru':
                   {'short': 'элмед.'
                   ,'title': 'Электромедицина'
                   }
               ,'de':
                   {'short': 'el.med.'
                   ,'title': 'Electromedicine'
                   }
               ,'es':
                   {'short': 'el.med.'
                   ,'title': 'Electromedicine'
                   }
               ,'uk':
                   {'short': 'ел.мед.'
                   ,'title': 'Електромедицина'
                   }
               }
           ,'el.met.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'el.met.'
                   ,'title': 'Electrometallurgy'
                   }
               ,'ru':
                   {'short': 'элмет.'
                   ,'title': 'Электрометаллургия'
                   }
               ,'de':
                   {'short': 'el.met.'
                   ,'title': 'Electrometallurgy'
                   }
               ,'es':
                   {'short': 'el.met.'
                   ,'title': 'Electrometallurgy'
                   }
               ,'uk':
                   {'short': 'елмет.'
                   ,'title': 'Електрометалургія'
                   }
               }
           ,'el.mot.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'el.mot.'
                   ,'title': 'Electric motors'
                   }
               ,'ru':
                   {'short': 'эл.двиг.'
                   ,'title': 'Электродвигатели'
                   }
               ,'de':
                   {'short': 'El.mot.'
                   ,'title': 'Elektromotoren'
                   }
               ,'es':
                   {'short': 'el.mot.'
                   ,'title': 'Electric motors'
                   }
               ,'uk':
                   {'short': 'ел.двиг.'
                   ,'title': 'Електродвигуни'
                   }
               }
           ,'el.therm.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'el.therm.'
                   ,'title': 'Electrothermy'
                   }
               ,'ru':
                   {'short': 'элтерм.'
                   ,'title': 'Электротермия'
                   }
               ,'de':
                   {'short': 'el.therm.'
                   ,'title': 'Electrothermy'
                   }
               ,'es':
                   {'short': 'el.therm.'
                   ,'title': 'Electrothermy'
                   }
               ,'uk':
                   {'short': 'елтерм.'
                   ,'title': 'Електротермія'
                   }
               }
           ,'el.tract.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'el.tract.'
                   ,'title': 'Electric traction'
                   }
               ,'ru':
                   {'short': 'тяг.'
                   ,'title': 'Электротяга'
                   }
               ,'de':
                   {'short': 'el.tract.'
                   ,'title': 'Electric traction'
                   }
               ,'es':
                   {'short': 'el.tract.'
                   ,'title': 'Electric traction'
                   }
               ,'uk':
                   {'short': 'ел.тяга'
                   ,'title': 'Електротяга'
                   }
               }
           ,'elect.':
               {'is_valid': True
               ,'major_en': 'Politics'
               ,'is_major': False
               ,'en':
                   {'short': 'elect.'
                   ,'title': 'Elections'
                   }
               ,'ru':
                   {'short': 'выб.'
                   ,'title': 'Выборы'
                   }
               ,'de':
                   {'short': 'elect.'
                   ,'title': 'Elections'
                   }
               ,'es':
                   {'short': 'elect.'
                   ,'title': 'Elections'
                   }
               ,'uk':
                   {'short': 'вибори'
                   ,'title': 'Вибори'
                   }
               }
           ,'electr.eng.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': True
               ,'en':
                   {'short': 'electr.eng.'
                   ,'title': 'Electrical engineering'
                   }
               ,'ru':
                   {'short': 'эл.тех.'
                   ,'title': 'Электротехника'
                   }
               ,'de':
                   {'short': 'electr.eng.'
                   ,'title': 'Electrical engineering'
                   }
               ,'es':
                   {'short': 'electr.eng.'
                   ,'title': 'Electrical engineering'
                   }
               ,'uk':
                   {'short': 'ел.тех.'
                   ,'title': 'Електротехніка'
                   }
               }
           ,'electric.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'electric.'
                   ,'title': 'Electricity'
                   }
               ,'ru':
                   {'short': 'электрич.'
                   ,'title': 'Электричество'
                   }
               ,'de':
                   {'short': 'electric.'
                   ,'title': 'Electricity'
                   }
               ,'es':
                   {'short': 'electric.'
                   ,'title': 'Electricity'
                   }
               ,'uk':
                   {'short': 'електр.'
                   ,'title': 'Електричний струм'
                   }
               }
           ,'electrophor.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'electrophor.'
                   ,'title': 'Electrophoresis'
                   }
               ,'ru':
                   {'short': 'электроф.'
                   ,'title': 'Электрофорез'
                   }
               ,'de':
                   {'short': 'electrophor.'
                   ,'title': 'Electrophoresis'
                   }
               ,'es':
                   {'short': 'electrophor.'
                   ,'title': 'Electrophoresis'
                   }
               ,'uk':
                   {'short': 'електроф.'
                   ,'title': 'Електрофорез'
                   }
               }
           ,'elev.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'elev.'
                   ,'title': 'Elevators'
                   }
               ,'ru':
                   {'short': 'лифт.'
                   ,'title': 'Лифты'
                   }
               ,'de':
                   {'short': 'elev.'
                   ,'title': 'Elevators'
                   }
               ,'es':
                   {'short': 'elev.'
                   ,'title': 'Elevators'
                   }
               ,'uk':
                   {'short': 'ліфти'
                   ,'title': 'Ліфти'
                   }
               }
           ,'els.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'els.'
                   ,'title': 'Electrolysis'
                   }
               ,'ru':
                   {'short': 'элз.'
                   ,'title': 'Электролиз'
                   }
               ,'de':
                   {'short': 'els.'
                   ,'title': 'Electrolysis'
                   }
               ,'es':
                   {'short': 'els.'
                   ,'title': 'Electrolysis'
                   }
               ,'uk':
                   {'short': 'електрлз'
                   ,'title': 'Електроліз'
                   }
               }
           ,'embryol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'embryol.'
                   ,'title': 'Embryology'
                   }
               ,'ru':
                   {'short': 'эмбриол.'
                   ,'title': 'Эмбриология'
                   }
               ,'de':
                   {'short': 'embryol.'
                   ,'title': 'Embryologie'
                   }
               ,'es':
                   {'short': 'embriol.'
                   ,'title': 'Embriología'
                   }
               ,'uk':
                   {'short': 'ембр.'
                   ,'title': 'Ембріологія'
                   }
               }
           ,'emerg.care':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'emerg.care'
                   ,'title': 'Emergency medical care'
                   }
               ,'ru':
                   {'short': 'скор.пом.'
                   ,'title': 'Скорая медицинская помощь'
                   }
               ,'de':
                   {'short': 'Krank.dienst.'
                   ,'title': 'Krankenbereitschaftsdienst'
                   }
               ,'es':
                   {'short': 'emerg.care'
                   ,'title': 'Emergency medical care'
                   }
               ,'uk':
                   {'short': 'невідкл.доп.'
                   ,'title': 'Невідкладна медична допомога'
                   }
               }
           ,'emotive':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'emotive'
                   ,'title': 'Emotive'
                   }
               ,'ru':
                   {'short': 'эмоц.'
                   ,'title': 'Эмоциональное выражение'
                   }
               ,'de':
                   {'short': 'Emot.Ausdr.'
                   ,'title': 'Emotionsausdruck'
                   }
               ,'es':
                   {'short': 'emotive'
                   ,'title': 'Emotive'
                   }
               ,'uk':
                   {'short': 'емоц.'
                   ,'title': 'Емоційний вираз'
                   }
               }
           ,'empl.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'empl.'
                   ,'title': 'Employment'
                   }
               ,'ru':
                   {'short': 'занят.'
                   ,'title': 'Занятость'
                   }
               ,'de':
                   {'short': 'empl.'
                   ,'title': 'Employment'
                   }
               ,'es':
                   {'short': 'empl.'
                   ,'title': 'Employment'
                   }
               ,'uk':
                   {'short': 'зайн.'
                   ,'title': 'Зайнятість'
                   }
               }
           ,'endocr.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'endocr.'
                   ,'title': 'Endocrinology'
                   }
               ,'ru':
                   {'short': 'энд.'
                   ,'title': 'Эндокринология'
                   }
               ,'de':
                   {'short': 'Endokrin.'
                   ,'title': 'Endokrinologie'
                   }
               ,'es':
                   {'short': 'endocr.'
                   ,'title': 'Endocrinology'
                   }
               ,'uk':
                   {'short': 'ендокр.'
                   ,'title': 'Ендокринологія'
                   }
               }
           ,'energ.distr.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'energ.distr.'
                   ,'title': 'Energy distribution'
                   }
               ,'ru':
                   {'short': 'распр.'
                   ,'title': 'Распределение энергии'
                   }
               ,'de':
                   {'short': 'energ.distr.'
                   ,'title': 'Energy distribution'
                   }
               ,'es':
                   {'short': 'energ.distr.'
                   ,'title': 'Energy distribution'
                   }
               ,'uk':
                   {'short': 'розпод.ен.'
                   ,'title': 'Розподіл енергії'
                   }
               }
           ,'energ.ind.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': True
               ,'en':
                   {'short': 'energ.ind.'
                   ,'title': 'Energy industry'
                   }
               ,'ru':
                   {'short': 'энерг.'
                   ,'title': 'Энергетика'
                   }
               ,'de':
                   {'short': 'Energiewirts.'
                   ,'title': 'Energiewirtschaft'
                   }
               ,'es':
                   {'short': 'energ.ind.'
                   ,'title': 'Energy industry'
                   }
               ,'uk':
                   {'short': 'енерг.'
                   ,'title': 'Енергетика'
                   }
               }
           ,'energ.syst.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'energ.syst.'
                   ,'title': 'Energy system'
                   }
               ,'ru':
                   {'short': 'эн.сист.'
                   ,'title': 'Энергосистемы'
                   }
               ,'de':
                   {'short': 'energ.syst.'
                   ,'title': 'Energy system'
                   }
               ,'es':
                   {'short': 'energ.syst.'
                   ,'title': 'Energy system'
                   }
               ,'uk':
                   {'short': 'ен.сист.'
                   ,'title': 'Енергосистеми'
                   }
               }
           ,'eng.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': True
               ,'en':
                   {'short': 'eng.'
                   ,'title': 'Engineering'
                   }
               ,'ru':
                   {'short': 'инж.'
                   ,'title': 'Инженерное дело'
                   }
               ,'de':
                   {'short': 'Ing.'
                   ,'title': 'Ingenieurwesen'
                   }
               ,'es':
                   {'short': 'eng.'
                   ,'title': 'Engineering'
                   }
               ,'uk':
                   {'short': 'інж.'
                   ,'title': 'Інженерна справа'
                   }
               }
           ,'eng.geol.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'eng.geol.'
                   ,'title': 'Engineering geology'
                   }
               ,'ru':
                   {'short': 'инж.геол.'
                   ,'title': 'Инженерная геология'
                   }
               ,'de':
                   {'short': 'eng.geol.'
                   ,'title': 'Engineering geology'
                   }
               ,'es':
                   {'short': 'eng.geol.'
                   ,'title': 'Engineering geology'
                   }
               ,'uk':
                   {'short': 'інж.геол.'
                   ,'title': 'Інженерна геологія'
                   }
               }
           ,'engin.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'engin.'
                   ,'title': 'Engines'
                   }
               ,'ru':
                   {'short': 'ДВС.'
                   ,'title': 'Двигатели внутреннего сгорания'
                   }
               ,'de':
                   {'short': 'Verbr. Motor'
                   ,'title': 'Verbrennungsmotor'
                   }
               ,'es':
                   {'short': 'engin.'
                   ,'title': 'Engines'
                   }
               ,'uk':
                   {'short': 'двиг.вн.зг.'
                   ,'title': 'Двигуни внутрішнього згоряння'
                   }
               }
           ,'engl.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'engl.'
                   ,'title': 'English'
                   }
               ,'ru':
                   {'short': 'англ.'
                   ,'title': 'Английский язык'
                   }
               ,'de':
                   {'short': 'engl.'
                   ,'title': 'English'
                   }
               ,'es':
                   {'short': 'engl.'
                   ,'title': 'English'
                   }
               ,'uk':
                   {'short': 'англ.'
                   ,'title': 'Англійська мова'
                   }
               }
           ,'entomol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'entomol.'
                   ,'title': 'Entomology'
                   }
               ,'ru':
                   {'short': 'энт.'
                   ,'title': 'Энтомология'
                   }
               ,'de':
                   {'short': 'Entomol.'
                   ,'title': 'Entomologie'
                   }
               ,'es':
                   {'short': 'entomol.'
                   ,'title': 'Entomologia'
                   }
               ,'uk':
                   {'short': 'ентом.'
                   ,'title': 'Ентомологія'
                   }
               }
           ,'environ.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': False
               ,'en':
                   {'short': 'environ.'
                   ,'title': 'Environment'
                   }
               ,'ru':
                   {'short': 'окруж.'
                   ,'title': 'Окружающая среда'
                   }
               ,'de':
                   {'short': 'Umwelt'
                   ,'title': 'Umwelt'
                   }
               ,'es':
                   {'short': 'environ.'
                   ,'title': 'Environment'
                   }
               ,'uk':
                   {'short': 'довк.'
                   ,'title': 'Довкілля'
                   }
               }
           ,'epist.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'epist.'
                   ,'title': 'Epistolary'
                   }
               ,'ru':
                   {'short': 'эпист.'
                   ,'title': 'Эпистолярный жанр'
                   }
               ,'de':
                   {'short': 'Brief.'
                   ,'title': 'Briefstil'
                   }
               ,'es':
                   {'short': 'epist.'
                   ,'title': 'Epistolary'
                   }
               ,'uk':
                   {'short': 'епіст.'
                   ,'title': 'Епістолярний жанр'
                   }
               }
           ,'equestr.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'equestr.'
                   ,'title': 'Equestrianism'
                   }
               ,'ru':
                   {'short': 'кон. спорт.'
                   ,'title': 'Конный спорт'
                   }
               ,'de':
                   {'short': 'equestr.'
                   ,'title': 'Equestrianism'
                   }
               ,'es':
                   {'short': 'equestr.'
                   ,'title': 'Equestrianism'
                   }
               ,'uk':
                   {'short': 'кінн.сп.'
                   ,'title': 'Кінний спорт'
                   }
               }
           ,'eskim.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'eskim.'
                   ,'title': 'Eskimo (usage)'
                   }
               ,'ru':
                   {'short': 'эскимос.'
                   ,'title': 'Эскимосское выражение'
                   }
               ,'de':
                   {'short': 'Eskim.'
                   ,'title': 'Eskimosprache'
                   }
               ,'es':
                   {'short': 'esquim.'
                   ,'title': 'Esquimal'
                   }
               ,'uk':
                   {'short': 'еск.'
                   ,'title': 'Ескімоська мова'
                   }
               }
           ,'esot.':
               {'is_valid': True
               ,'major_en': 'Parasciences'
               ,'is_major': False
               ,'en':
                   {'short': 'esot.'
                   ,'title': 'Esoterics'
                   }
               ,'ru':
                   {'short': 'эзот.'
                   ,'title': 'Эзотерика'
                   }
               ,'de':
                   {'short': 'esot.'
                   ,'title': 'Esoterics'
                   }
               ,'es':
                   {'short': 'esot.'
                   ,'title': 'Esoterics'
                   }
               ,'uk':
                   {'short': 'езот.'
                   ,'title': 'Езотерика'
                   }
               }
           ,'esper.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'esper.'
                   ,'title': 'Esperanto'
                   }
               ,'ru':
                   {'short': 'эспер.'
                   ,'title': 'Эсперанто'
                   }
               ,'de':
                   {'short': 'esper.'
                   ,'title': 'Esperanto'
                   }
               ,'es':
                   {'short': 'esper.'
                   ,'title': 'Esperanto'
                   }
               ,'uk':
                   {'short': 'еспер.'
                   ,'title': 'Есперанто'
                   }
               }
           ,'ethnogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'ethnogr.'
                   ,'title': 'Ethnography'
                   }
               ,'ru':
                   {'short': 'этн.'
                   ,'title': 'Этнография'
                   }
               ,'de':
                   {'short': 'ethn.'
                   ,'title': 'Ethnographie'
                   }
               ,'es':
                   {'short': 'etnogr.'
                   ,'title': 'Etnografía'
                   }
               ,'uk':
                   {'short': 'етн.'
                   ,'title': 'Етнографія'
                   }
               }
           ,'ethnol.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'ethnol.'
                   ,'title': 'Ethnology'
                   }
               ,'ru':
                   {'short': 'этнол.'
                   ,'title': 'Этнология'
                   }
               ,'de':
                   {'short': 'ethnol.'
                   ,'title': 'Ethnology'
                   }
               ,'es':
                   {'short': 'ethnol.'
                   ,'title': 'Ethnology'
                   }
               ,'uk':
                   {'short': 'етнол.'
                   ,'title': 'Етнологія'
                   }
               }
           ,'ethnopsychol.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': False
               ,'en':
                   {'short': 'ethnopsychol.'
                   ,'title': 'Ethnopsychology'
                   }
               ,'ru':
                   {'short': 'этнопсихол.'
                   ,'title': 'Этнопсихология'
                   }
               ,'de':
                   {'short': 'ethnopsychol.'
                   ,'title': 'Ethnopsychology'
                   }
               ,'es':
                   {'short': 'ethnopsychol.'
                   ,'title': 'Ethnopsychology'
                   }
               ,'uk':
                   {'short': 'етнопсихол.'
                   ,'title': 'Етнопсихологія'
                   }
               }
           ,'ethol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'ethol.'
                   ,'title': 'Ethology'
                   }
               ,'ru':
                   {'short': 'этол.'
                   ,'title': 'Этология'
                   }
               ,'de':
                   {'short': 'ethol.'
                   ,'title': 'Ethology'
                   }
               ,'es':
                   {'short': 'ethol.'
                   ,'title': 'Ethology'
                   }
               ,'uk':
                   {'short': 'етол.'
                   ,'title': 'Етологія'
                   }
               }
           ,'euph.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'euph.'
                   ,'title': 'Euphemistic'
                   }
               ,'ru':
                   {'short': 'эвф.'
                   ,'title': 'Эвфемизм'
                   }
               ,'de':
                   {'short': 'euph.'
                   ,'title': 'Euphemismus'
                   }
               ,'es':
                   {'short': 'eufem.'
                   ,'title': 'Eufemismo'
                   }
               ,'uk':
                   {'short': 'евф.'
                   ,'title': 'Евфемізм'
                   }
               }
           ,'evol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'evol.'
                   ,'title': 'Evolution'
                   }
               ,'ru':
                   {'short': 'эвол.'
                   ,'title': 'Эволюция'
                   }
               ,'de':
                   {'short': 'evol.'
                   ,'title': 'Evolution'
                   }
               ,'es':
                   {'short': 'evol.'
                   ,'title': 'Evolution'
                   }
               ,'uk':
                   {'short': 'евол.'
                   ,'title': 'Еволюція'
                   }
               }
           ,'excl.':
               {'is_valid': True
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'excl.'
                   ,'title': 'Exclamation'
                   }
               ,'ru':
                   {'short': 'воскл.'
                   ,'title': 'Восклицание'
                   }
               ,'de':
                   {'short': 'excl.'
                   ,'title': 'Exclamation'
                   }
               ,'es':
                   {'short': 'excl.'
                   ,'title': 'Exclamation'
                   }
               ,'uk':
                   {'short': 'оклик'
                   ,'title': 'Оклик'
                   }
               }
           ,'exhib.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'exhib.'
                   ,'title': 'Exhibitions'
                   }
               ,'ru':
                   {'short': 'выст.'
                   ,'title': 'Выставки'
                   }
               ,'de':
                   {'short': 'exhib.'
                   ,'title': 'Exhibitions'
                   }
               ,'es':
                   {'short': 'exhib.'
                   ,'title': 'Exhibitions'
                   }
               ,'uk':
                   {'short': 'вист.'
                   ,'title': 'Виставки'
                   }
               }
           ,'explan.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'explan.'
                   ,'title': 'Explanatory translation'
                   }
               ,'ru':
                   {'short': 'поясн.'
                   ,'title': 'Пояснительный вариант перевода'
                   }
               ,'de':
                   {'short': 'explan.'
                   ,'title': 'Explanatory translation'
                   }
               ,'es':
                   {'short': 'explan.'
                   ,'title': 'Explanatory translation'
                   }
               ,'uk':
                   {'short': 'поясн.'
                   ,'title': 'Пояснювальний варіант перекладу'
                   }
               }
           ,'extr.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'extr.'
                   ,'title': 'Extrusion'
                   }
               ,'ru':
                   {'short': 'экстр.'
                   ,'title': 'Экструзия'
                   }
               ,'de':
                   {'short': 'Extr.'
                   ,'title': 'Extrusion'
                   }
               ,'es':
                   {'short': 'extr.'
                   ,'title': 'Extrusion'
                   }
               ,'uk':
                   {'short': 'екструз.'
                   ,'title': 'Екструзія'
                   }
               }
           ,'f.trade.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'f.trade.'
                   ,'title': 'Foreign trade'
                   }
               ,'ru':
                   {'short': 'внеш.торг.'
                   ,'title': 'Внешняя торговля'
                   }
               ,'de':
                   {'short': 'Außenhand.'
                   ,'title': 'Außenhandel'
                   }
               ,'es':
                   {'short': 'f.trade.'
                   ,'title': 'Foreign trade'
                   }
               ,'uk':
                   {'short': 'зовн. торг.'
                   ,'title': 'Зовнішня торгівля'
                   }
               }
           ,'facil.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'facil.'
                   ,'title': 'Facilities'
                   }
               ,'ru':
                   {'short': 'произв.помещ.'
                   ,'title': 'Производственные помещения'
                   }
               ,'de':
                   {'short': 'facil.'
                   ,'title': 'Facilities'
                   }
               ,'es':
                   {'short': 'facil.'
                   ,'title': 'Facilities'
                   }
               ,'uk':
                   {'short': 'вир.приміщ.'
                   ,'title': 'Виробничі приміщення'
                   }
               }
           ,'fant./sci-fi., abbr.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'fant./sci-fi., abbr.'
                   ,'title': 'Fantasy and science fiction, Abbreviation'
                   }
               ,'ru':
                   {'short': 'фант., сокр.'
                   ,'title': 'Фантастика, фэнтези, Сокращение'
                   }
               ,'de':
                   {'short': 'fant./sci-fi., Abkürz.'
                   ,'title': 'Fantasy and science fiction, Abkürzung'
                   }
               ,'es':
                   {'short': 'fant./sci-fi., abrev.'
                   ,'title': 'Fantasy and science fiction, Abreviatura'
                   }
               ,'uk':
                   {'short': 'фант., абрев.'
                   ,'title': 'Фантастика, фентезі, Абревіатура'
                   }
               }
           ,'fash.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'fash.'
                   ,'title': 'Fashion'
                   }
               ,'ru':
                   {'short': 'мод.'
                   ,'title': 'Мода'
                   }
               ,'de':
                   {'short': 'fash.'
                   ,'title': 'Fashion'
                   }
               ,'es':
                   {'short': 'fash.'
                   ,'title': 'Fashion'
                   }
               ,'uk':
                   {'short': 'мод.'
                   ,'title': 'Мода'
                   }
               }
           ,'faux ami':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'faux ami'
                   ,'title': "Translator's false friend"}, 'ru': {'short': 'ложн.друг.'
                   ,'title': 'Ложный друг переводчика'
                   }
               ,'de':
                   {'short': 'faux ami'
                   ,'title': "Translator's false friend"}, 'es': {'short': 'faux ami'
                   ,'title': "Translator's false friend"}, 'uk': {'short': 'хибн.друг'
                   ,'title': 'Хибний друг перекладача'
                   }
               }
           ,'felin.':
               {'is_valid': True
               ,'major_en': 'Companion animals'
               ,'is_major': False
               ,'en':
                   {'short': 'felin.'
                   ,'title': 'Felinology'
                   }
               ,'ru':
                   {'short': 'фелин.'
                   ,'title': 'Фелинология'
                   }
               ,'de':
                   {'short': 'Felin.'
                   ,'title': 'Felinologie'
                   }
               ,'es':
                   {'short': 'felin.'
                   ,'title': 'Felinology'
                   }
               ,'uk':
                   {'short': 'фелін.'
                   ,'title': 'Фелінологія'
                   }
               }
           ,'fenc.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'fenc.'
                   ,'title': 'Fencing'
                   }
               ,'ru':
                   {'short': 'фехт.'
                   ,'title': 'Фехтование'
                   }
               ,'de':
                   {'short': 'fenc.'
                   ,'title': 'Fencing'
                   }
               ,'es':
                   {'short': 'fenc.'
                   ,'title': 'Fencing'
                   }
               ,'uk':
                   {'short': 'фехт.'
                   ,'title': 'Фехтування'
                   }
               }
           ,'ferm.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'ferm.'
                   ,'title': 'Fermentation'
                   }
               ,'ru':
                   {'short': 'ферм.'
                   ,'title': 'Ферментация'
                   }
               ,'de':
                   {'short': 'ferm.'
                   ,'title': 'Fermentation'
                   }
               ,'es':
                   {'short': 'ferm.'
                   ,'title': 'Fermentation'
                   }
               ,'uk':
                   {'short': 'ферм.'
                   ,'title': 'Ферментація'
                   }
               }
           ,'fert.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'fert.'
                   ,'title': 'Fertilizers'
                   }
               ,'ru':
                   {'short': 'удобр.'
                   ,'title': 'Удобрения'
                   }
               ,'de':
                   {'short': 'fert.'
                   ,'title': 'Fertilizers'
                   }
               ,'es':
                   {'short': 'fert.'
                   ,'title': 'Fertilizers'
                   }
               ,'uk':
                   {'short': 'добр.'
                   ,'title': 'Добрива'
                   }
               }
           ,'fib.optic':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'fib.optic'
                   ,'title': 'Fiber optic'
                   }
               ,'ru':
                   {'short': 'опт.вол.'
                   ,'title': 'Оптическое волокно'
                   }
               ,'de':
                   {'short': 'Fas.opt.'
                   ,'title': 'Faseroptik'
                   }
               ,'es':
                   {'short': 'fib.optic'
                   ,'title': 'Fiber optic'
                   }
               ,'uk':
                   {'short': 'опт.вол.'
                   ,'title': 'Оптичне волокно'
                   }
               }
           ,'fig.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'fig.'
                   ,'title': 'Figurative'
                   }
               ,'ru':
                   {'short': 'перен.'
                   ,'title': 'Переносный смысл'
                   }
               ,'de':
                   {'short': 'übertr.'
                   ,'title': 'übertragen'
                   }
               ,'es':
                   {'short': 'fig.'
                   ,'title': 'Figuradamente'
                   }
               ,'uk':
                   {'short': 'перен.'
                   ,'title': 'Переносний сенс'
                   }
               }
           ,'fig.of.sp.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'fig.of.sp.'
                   ,'title': 'Figure of speech'
                   }
               ,'ru':
                   {'short': 'образн.'
                   ,'title': 'Образное выражение'
                   }
               ,'de':
                   {'short': 'Bild. Ausdr.'
                   ,'title': 'Bildlicher Ausdruck'
                   }
               ,'es':
                   {'short': 'fig.of.sp.'
                   ,'title': 'Figure of speech'
                   }
               ,'uk':
                   {'short': 'образн.'
                   ,'title': 'Образний вислів'
                   }
               }
           ,'fig.skat.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'fig.skat.'
                   ,'title': 'Figure skating'
                   }
               ,'ru':
                   {'short': 'фиг.кат.'
                   ,'title': 'Фигурное катание'
                   }
               ,'de':
                   {'short': 'fig.skat.'
                   ,'title': 'Figure skating'
                   }
               ,'es':
                   {'short': 'fig.skat.'
                   ,'title': 'Figure skating'
                   }
               ,'uk':
                   {'short': 'фіг.кат.'
                   ,'title': 'Фігурне катання'
                   }
               }
           ,'file.ext.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'file.ext.'
                   ,'title': 'File extension'
                   }
               ,'ru':
                   {'short': 'ф.расш.'
                   ,'title': 'Расширение файла'
                   }
               ,'de':
                   {'short': 'file.ext.'
                   ,'title': 'File extension'
                   }
               ,'es':
                   {'short': 'file.ext.'
                   ,'title': 'File extension'
                   }
               ,'uk':
                   {'short': 'розшир.ф.'
                   ,'title': 'Розширення файла'
                   }
               }
           ,'film.equip.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'film.equip.'
                   ,'title': 'Filming equipment'
                   }
               ,'ru':
                   {'short': 'кин.ап.'
                   ,'title': 'Киносъёмочная аппаратура'
                   }
               ,'de':
                   {'short': 'film.equip.'
                   ,'title': 'Filming equipment'
                   }
               ,'es':
                   {'short': 'film.equip.'
                   ,'title': 'Filming equipment'
                   }
               ,'uk':
                   {'short': 'кіноап.'
                   ,'title': 'Кінознімальна апаратура'
                   }
               }
           ,'film.light.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'film.light.'
                   ,'title': 'Film lighting equipment'
                   }
               ,'ru':
                   {'short': 'осв.'
                   ,'title': 'Киноосветительная аппаратура'
                   }
               ,'de':
                   {'short': 'film.light.'
                   ,'title': 'Film lighting equipment'
                   }
               ,'es':
                   {'short': 'film.light.'
                   ,'title': 'Film lighting equipment'
                   }
               ,'uk':
                   {'short': 'к.осв.'
                   ,'title': 'Кіноосвітлювальна апаратура'
                   }
               }
           ,'film.proc.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'film.proc.'
                   ,'title': 'Film processing'
                   }
               ,'ru':
                   {'short': 'обр.кино.'
                   ,'title': 'Обработка кинофотоматериалов'
                   }
               ,'de':
                   {'short': 'film.proc.'
                   ,'title': 'Film processing'
                   }
               ,'es':
                   {'short': 'film.proc.'
                   ,'title': 'Film processing'
                   }
               ,'uk':
                   {'short': 'обр.кіноф.мат.'
                   ,'title': 'Обробка кінофотоматеріалів'
                   }
               }
           ,'fin.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': True
               ,'en':
                   {'short': 'fin.'
                   ,'title': 'Finances'
                   }
               ,'ru':
                   {'short': 'фин.'
                   ,'title': 'Финансы'
                   }
               ,'de':
                   {'short': 'Fin.'
                   ,'title': 'Finanzen'
                   }
               ,'es':
                   {'short': 'fin.'
                   ,'title': 'Finanzas'
                   }
               ,'uk':
                   {'short': 'фін.'
                   ,'title': 'Фінанси'
                   }
               }
           ,'finn.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'finn.'
                   ,'title': 'Finnish language'
                   }
               ,'ru':
                   {'short': 'финск.'
                   ,'title': 'Финский язык'
                   }
               ,'de':
                   {'short': 'finn.'
                   ,'title': 'Finnish language'
                   }
               ,'es':
                   {'short': 'finn.'
                   ,'title': 'Finnish language'
                   }
               ,'uk':
                   {'short': 'фінськ.'
                   ,'title': 'Фінська мова'
                   }
               }
           ,'fire.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'fire.'
                   ,'title': 'Firefighting and fire-control systems'
                   }
               ,'ru':
                   {'short': 'пож.'
                   ,'title': 'Пожарное дело и системы пожаротушения'
                   }
               ,'de':
                   {'short': 'fire.'
                   ,'title': 'Firefighting and fire-control systems'
                   }
               ,'es':
                   {'short': 'fire.'
                   ,'title': 'Firefighting and fire-control systems'
                   }
               ,'uk':
                   {'short': 'пожеж.'
                   ,'title': 'Пожежна справа та системи пожежогасіння'
                   }
               }
           ,'fish.farm.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'fish.farm.'
                   ,'title': 'Fish farming (pisciculture)'
                   }
               ,'ru':
                   {'short': 'рыб.'
                   ,'title': 'Рыбоводство'
                   }
               ,'de':
                   {'short': 'Fischz.'
                   ,'title': 'Fischzucht'
                   }
               ,'es':
                   {'short': 'fish.farm.'
                   ,'title': 'Fish farming (pisciculture)'
                   }
               ,'uk':
                   {'short': 'риб.'
                   ,'title': 'Рибництво'
                   }
               }
           ,'fishery':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'fishery'
                   ,'title': 'Fishery (fishing industry)'
                   }
               ,'ru':
                   {'short': 'рыбол.'
                   ,'title': 'Рыболовство (промысловое)'
                   }
               ,'de':
                   {'short': 'fishery'
                   ,'title': 'Fishery (fishing industry)'
                   }
               ,'es':
                   {'short': 'fishery'
                   ,'title': 'Fishery (fishing industry)'
                   }
               ,'uk':
                   {'short': 'риболов.'
                   ,'title': 'Риболовство (промислове)'
                   }
               }
           ,'flor.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'flor.'
                   ,'title': 'Floriculture'
                   }
               ,'ru':
                   {'short': 'цвет.'
                   ,'title': 'Цветоводство'
                   }
               ,'de':
                   {'short': 'flor.'
                   ,'title': 'Floriculture'
                   }
               ,'es':
                   {'short': 'flor.'
                   ,'title': 'Floriculture'
                   }
               ,'uk':
                   {'short': 'квіт.'
                   ,'title': 'Квітникарство'
                   }
               }
           ,'flour.prod.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'flour.prod.'
                   ,'title': 'Flour production'
                   }
               ,'ru':
                   {'short': 'мук.'
                   ,'title': 'Мучное производство'
                   }
               ,'de':
                   {'short': 'flour.prod.'
                   ,'title': 'Flour production'
                   }
               ,'es':
                   {'short': 'flour.prod.'
                   ,'title': 'Flour production'
                   }
               ,'uk':
                   {'short': 'борош.'
                   ,'title': 'Борошняне виробництво'
                   }
               }
           ,'flow.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'flow.'
                   ,'title': 'Flow measurement'
                   }
               ,'ru':
                   {'short': 'расход.'
                   ,'title': 'Расходометрия'
                   }
               ,'de':
                   {'short': 'flow.'
                   ,'title': 'Flow measurement'
                   }
               ,'es':
                   {'short': 'flow.'
                   ,'title': 'Flow measurement'
                   }
               ,'uk':
                   {'short': 'витрат.'
                   ,'title': 'Витратометрія'
                   }
               }
           ,'fodd.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'fodd.'
                   ,'title': 'Fodder'
                   }
               ,'ru':
                   {'short': 'корм.'
                   ,'title': 'Корма'
                   }
               ,'de':
                   {'short': 'fodd.'
                   ,'title': 'Fodder'
                   }
               ,'es':
                   {'short': 'fodd.'
                   ,'title': 'Fodder'
                   }
               ,'uk':
                   {'short': 'корми'
                   ,'title': 'Корми'
                   }
               }
           ,'foil.ships':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'foil.ships'
                   ,'title': 'Foil ships'
                   }
               ,'ru':
                   {'short': 'СПК.'
                   ,'title': 'Суда на подводных крыльях'
                   }
               ,'de':
                   {'short': 'Tragflügelsch.'
                   ,'title': 'Tragflügelschiff'
                   }
               ,'es':
                   {'short': 'foil.ships'
                   ,'title': 'Foil ships'
                   }
               ,'uk':
                   {'short': 'СПК'
                   ,'title': 'Судна на підводних крилах'
                   }
               }
           ,'folk.':
               {'is_valid': True
               ,'major_en': 'Folklore'
               ,'is_major': True
               ,'en':
                   {'short': 'folk.'
                   ,'title': 'Folklore'
                   }
               ,'ru':
                   {'short': 'фольк.'
                   ,'title': 'Фольклор'
                   }
               ,'de':
                   {'short': 'Folkl.'
                   ,'title': 'Folklore'
                   }
               ,'es':
                   {'short': 'folk.'
                   ,'title': 'Folklore'
                   }
               ,'uk':
                   {'short': 'фольк.'
                   ,'title': 'Фольклор'
                   }
               }
           ,'food.ind.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': True
               ,'en':
                   {'short': 'food.ind.'
                   ,'title': 'Food industry'
                   }
               ,'ru':
                   {'short': 'пищ.'
                   ,'title': 'Пищевая промышленность'
                   }
               ,'de':
                   {'short': 'Nahrungsind.'
                   ,'title': 'Nahrungsindustrie'
                   }
               ,'es':
                   {'short': 'food.ind.'
                   ,'title': 'Food industry'
                   }
               ,'uk':
                   {'short': 'харч.'
                   ,'title': 'Харчова промисловість'
                   }
               }
           ,'food.serv.':
               {'is_valid': True
               ,'major_en': 'Service industry'
               ,'is_major': False
               ,'en':
                   {'short': 'food.serv.'
                   ,'title': 'Food service and catering'
                   }
               ,'ru':
                   {'short': 'общ.пит.'
                   ,'title': 'Общественное питание'
                   }
               ,'de':
                   {'short': 'food.serv.'
                   ,'title': 'Food service and catering'
                   }
               ,'es':
                   {'short': 'food.serv.'
                   ,'title': 'Food service and catering'
                   }
               ,'uk':
                   {'short': 'гр.харч.'
                   ,'title': 'Громадське харчування'
                   }
               }
           ,'footb.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'footb.'
                   ,'title': 'Football'
                   }
               ,'ru':
                   {'short': 'футб.'
                   ,'title': 'Футбол'
                   }
               ,'de':
                   {'short': 'Fußb.'
                   ,'title': 'Fußball'
                   }
               ,'es':
                   {'short': 'footb.'
                   ,'title': 'Football'
                   }
               ,'uk':
                   {'short': 'футб.'
                   ,'title': 'Футбол'
                   }
               }
           ,'footwear':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'footwear'
                   ,'title': 'Footwear'
                   }
               ,'ru':
                   {'short': 'обув.'
                   ,'title': 'Обувь'
                   }
               ,'de':
                   {'short': 'footwear'
                   ,'title': 'Footwear'
                   }
               ,'es':
                   {'short': 'footwear'
                   ,'title': 'Footwear'
                   }
               ,'uk':
                   {'short': 'взут.'
                   ,'title': 'Взуття'
                   }
               }
           ,'for.chem.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'for.chem.'
                   ,'title': 'Forest chemistry'
                   }
               ,'ru':
                   {'short': 'лесохим.'
                   ,'title': 'Лесохимия'
                   }
               ,'de':
                   {'short': 'for.chem.'
                   ,'title': 'Forest chemistry'
                   }
               ,'es':
                   {'short': 'for.chem.'
                   ,'title': 'Forest chemistry'
                   }
               ,'uk':
                   {'short': 'лісохім.'
                   ,'title': 'Лісохімія'
                   }
               }
           ,'for.pol.':
               {'is_valid': True
               ,'major_en': 'Foreign affairs'
               ,'is_major': False
               ,'en':
                   {'short': 'for.pol.'
                   ,'title': 'Foreign policy'
                   }
               ,'ru':
                   {'short': 'внеш.полит.'
                   ,'title': 'Внешняя политика'
                   }
               ,'de':
                   {'short': 'for.pol.'
                   ,'title': 'Foreign policy'
                   }
               ,'es':
                   {'short': 'for.pol.'
                   ,'title': 'Foreign policy'
                   }
               ,'uk':
                   {'short': 'зовн.політ.'
                   ,'title': 'Зовнішня політика'
                   }
               }
           ,'foreig.aff.':
               {'is_valid': True
               ,'major_en': 'Foreign affairs'
               ,'is_major': True
               ,'en':
                   {'short': 'foreig.aff.'
                   ,'title': 'Foreign affairs'
                   }
               ,'ru':
                   {'short': 'ин.дел.'
                   ,'title': 'Иностранные дела'
                   }
               ,'de':
                   {'short': 'foreig.aff.'
                   ,'title': 'Foreign affairs'
                   }
               ,'es':
                   {'short': 'foreig.aff.'
                   ,'title': 'Foreign affairs'
                   }
               ,'uk':
                   {'short': 'МЗС'
                   ,'title': 'Міністерство закордонних справ'
                   }
               }
           ,'forens.med.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'forens.med.'
                   ,'title': 'Forensic medicine'
                   }
               ,'ru':
                   {'short': 'суд.мед.'
                   ,'title': 'Судебная медицина'
                   }
               ,'de':
                   {'short': 'R.Med.'
                   ,'title': 'Rechtsmedizin'
                   }
               ,'es':
                   {'short': 'forens.med.'
                   ,'title': 'Forensic medicine'
                   }
               ,'uk':
                   {'short': 'суд.мед.'
                   ,'title': 'Судова медицина'
                   }
               }
           ,'forestr.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': False
               ,'en':
                   {'short': 'forestr.'
                   ,'title': 'Forestry'
                   }
               ,'ru':
                   {'short': 'лес.'
                   ,'title': 'Лесоводство'
                   }
               ,'de':
                   {'short': 'Forst'
                   ,'title': 'Forstbau'
                   }
               ,'es':
                   {'short': 'silvicult.'
                   ,'title': 'Silvicultura'
                   }
               ,'uk':
                   {'short': 'ліс.'
                   ,'title': 'Лісівництво'
                   }
               }
           ,'forestr., amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'forestr., amer.usg.'
                   ,'title': 'Forestry, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'лес., амер.'
                   ,'title': 'Лесоводство, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Forst, Amerik.'
                   ,'title': 'Forstbau, Amerikanisch'
                   }
               ,'es':
                   {'short': 'silvicult., amer.'
                   ,'title': 'Silvicultura, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ліс., амер.вир.'
                   ,'title': 'Лісівництво, Американський вираз (не варыант мови)'
                   }
               }
           ,'forex':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'forex'
                   ,'title': 'Foreign exchange market'
                   }
               ,'ru':
                   {'short': 'валют.рын.'
                   ,'title': 'Валютный рынок (форекс)'
                   }
               ,'de':
                   {'short': 'Devisengesch.'
                   ,'title': 'Devisengeschäfte'
                   }
               ,'es':
                   {'short': 'forex'
                   ,'title': 'Foreign exchange market'
                   }
               ,'uk':
                   {'short': 'валют.рин.'
                   ,'title': 'Валютний ринок (форекс)'
                   }
               }
           ,'forg.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'forg.'
                   ,'title': 'Forging'
                   }
               ,'ru':
                   {'short': 'ков.'
                   ,'title': 'Ковка'
                   }
               ,'de':
                   {'short': 'Schm.'
                   ,'title': 'Schmieden'
                   }
               ,'es':
                   {'short': 'forg.'
                   ,'title': 'Forging'
                   }
               ,'uk':
                   {'short': 'кув.'
                   ,'title': 'Кування'
                   }
               }
           ,'formal':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'formal'
                   ,'title': 'Formal'
                   }
               ,'ru':
                   {'short': 'офиц.'
                   ,'title': 'Официальный стиль'
                   }
               ,'de':
                   {'short': 'form.Sp.'
                   ,'title': 'Formale Sprache'
                   }
               ,'es':
                   {'short': 'formal'
                   ,'title': 'Formal'
                   }
               ,'uk':
                   {'short': 'офіц.'
                   ,'title': 'Офіційний вираз'
                   }
               }
           ,'found.engin.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'found.engin.'
                   ,'title': 'Foundation engineering'
                   }
               ,'ru':
                   {'short': 'фунд.'
                   ,'title': 'Фундаментостроение'
                   }
               ,'de':
                   {'short': 'found.engin.'
                   ,'title': 'Foundation engineering'
                   }
               ,'es':
                   {'short': 'found.engin.'
                   ,'title': 'Foundation engineering'
                   }
               ,'uk':
                   {'short': 'фунд.буд.'
                   ,'title': 'Фундаментобудування'
                   }
               }
           ,'foundr.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'foundr.'
                   ,'title': 'Foundry'
                   }
               ,'ru':
                   {'short': 'литейн.'
                   ,'title': 'Литейное производство'
                   }
               ,'de':
                   {'short': 'foundr.'
                   ,'title': 'Foundry'
                   }
               ,'es':
                   {'short': 'foundr.'
                   ,'title': 'Foundry'
                   }
               ,'uk':
                   {'short': 'лив.вир.'
                   ,'title': 'Ливарне виробництво'
                   }
               }
           ,'fr.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'fr.'
                   ,'title': 'French'
                   }
               ,'ru':
                   {'short': 'фр.'
                   ,'title': 'Французский язык'
                   }
               ,'de':
                   {'short': 'Franz. Sp.'
                   ,'title': 'Französisch'
                   }
               ,'es':
                   {'short': 'fr.'
                   ,'title': 'Francés'
                   }
               ,'uk':
                   {'short': 'фр.'
                   ,'title': 'Французька мова'
                   }
               }
           ,'furn.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'furn.'
                   ,'title': 'Furniture'
                   }
               ,'ru':
                   {'short': 'меб.'
                   ,'title': 'Мебель'
                   }
               ,'de':
                   {'short': 'möb.'
                   ,'title': 'Möbel'
                   }
               ,'es':
                   {'short': 'furn.'
                   ,'title': 'Furniture'
                   }
               ,'uk':
                   {'short': 'меб.'
                   ,'title': 'Меблі'
                   }
               }
           ,'gaelic':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'gaelic'
                   ,'title': 'Gaelic'
                   }
               ,'ru':
                   {'short': 'гэльск.'
                   ,'title': 'Гэльский (шотландский) язык'
                   }
               ,'de':
                   {'short': 'gaelic'
                   ,'title': 'Gaelic'
                   }
               ,'es':
                   {'short': 'gaelic'
                   ,'title': 'Gaelic'
                   }
               ,'uk':
                   {'short': 'гельськ.'
                   ,'title': 'Гельська (шотландська) мова'
                   }
               }
           ,'galv.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'galv.'
                   ,'title': 'Galvanizing'
                   }
               ,'ru':
                   {'short': 'цинк.'
                   ,'title': 'Цинкование'
                   }
               ,'de':
                   {'short': 'galv.'
                   ,'title': 'Galvanizing'
                   }
               ,'es':
                   {'short': 'galv.'
                   ,'title': 'Galvanizing'
                   }
               ,'uk':
                   {'short': 'оцинк.'
                   ,'title': 'Оцинкування'
                   }
               }
           ,'galv.plast.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'galv.plast.'
                   ,'title': 'Galvanoplasty'
                   }
               ,'ru':
                   {'short': 'гальв.'
                   ,'title': 'Гальванотехника'
                   }
               ,'de':
                   {'short': 'Galv.tech.'
                   ,'title': 'Galvanotechnik'
                   }
               ,'es':
                   {'short': 'galv.plast.'
                   ,'title': 'Galvanoplasty'
                   }
               ,'uk':
                   {'short': 'гальв.'
                   ,'title': 'Гальванотехніка'
                   }
               }
           ,'gambl.':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'gambl.'
                   ,'title': 'Gambling'
                   }
               ,'ru':
                   {'short': 'азартн.'
                   ,'title': 'Азартные игры'
                   }
               ,'de':
                   {'short': 'gambl.'
                   ,'title': 'Gambling'
                   }
               ,'es':
                   {'short': 'gambl.'
                   ,'title': 'Gambling'
                   }
               ,'uk':
                   {'short': 'азартн.'
                   ,'title': 'Азартні ігри'
                   }
               }
           ,'games':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': True
               ,'en':
                   {'short': 'games'
                   ,'title': 'Games (other than sports)'
                   }
               ,'ru':
                   {'short': 'игры.'
                   ,'title': 'Игры (кроме спорта)'
                   }
               ,'de':
                   {'short': 'games'
                   ,'title': 'Games (other than sports)'
                   }
               ,'es':
                   {'short': 'games'
                   ,'title': 'Games (other than sports)'
                   }
               ,'uk':
                   {'short': 'ігри.'
                   ,'title': 'Ігри (окрім спорту)'
                   }
               }
           ,'garden.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'garden.'
                   ,'title': 'Gardening'
                   }
               ,'ru':
                   {'short': 'сад.'
                   ,'title': 'Садоводство'
                   }
               ,'de':
                   {'short': 'Garten.'
                   ,'title': 'Gartenarbeit'
                   }
               ,'es':
                   {'short': 'garden.'
                   ,'title': 'Gardening'
                   }
               ,'uk':
                   {'short': 'садівн.'
                   ,'title': 'Садівництво'
                   }
               }
           ,'gas.proc.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'gas.proc.'
                   ,'title': 'Gas processing plants'
                   }
               ,'ru':
                   {'short': 'гпз.'
                   ,'title': 'Газоперерабатывающие заводы'
                   }
               ,'de':
                   {'short': 'gas.proc.'
                   ,'title': 'Gas processing plants'
                   }
               ,'es':
                   {'short': 'gas.proc.'
                   ,'title': 'Gas processing plants'
                   }
               ,'uk':
                   {'short': 'ГПЗ'
                   ,'title': 'Газопереробні заводи'
                   }
               }
           ,'gastroent.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'gastroent.'
                   ,'title': 'Gastroenterology'
                   }
               ,'ru':
                   {'short': 'гастр.'
                   ,'title': 'Гастроэнтерология'
                   }
               ,'de':
                   {'short': 'Gastroent.'
                   ,'title': 'Gastroenterologie'
                   }
               ,'es':
                   {'short': 'gastroent.'
                   ,'title': 'Gastroenterología'
                   }
               ,'uk':
                   {'short': 'гастр.'
                   ,'title': 'Гастроентерологія'
                   }
               }
           ,'gear.tr.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'gear.tr.'
                   ,'title': 'Gear train'
                   }
               ,'ru':
                   {'short': 'зубч.перед.'
                   ,'title': 'Зубчатые передачи'
                   }
               ,'de':
                   {'short': 'gear.tr.'
                   ,'title': 'Gear train'
                   }
               ,'es':
                   {'short': 'gear.tr.'
                   ,'title': 'Gear train'
                   }
               ,'uk':
                   {'short': 'зубч.перед.'
                   ,'title': 'Зубчасті передачі'
                   }
               }
           ,'gem.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'gem.'
                   ,'title': 'Gemmology'
                   }
               ,'ru':
                   {'short': 'гем.'
                   ,'title': 'Геммология'
                   }
               ,'de':
                   {'short': 'gem.'
                   ,'title': 'Gemmology'
                   }
               ,'es':
                   {'short': 'gem.'
                   ,'title': 'Gemmology'
                   }
               ,'uk':
                   {'short': 'гем.'
                   ,'title': 'Гемологія'
                   }
               }
           ,'gen.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'gen.'
                   ,'title': 'General'
                   }
               ,'ru':
                   {'short': 'общ.'
                   ,'title': 'Общая лексика'
                   }
               ,'de':
                   {'short': 'Allg.'
                   ,'title': 'Allgemeine Lexik'
                   }
               ,'es':
                   {'short': 'gen.'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'заг.'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'gen.eng.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'gen.eng.'
                   ,'title': 'Genetic engineering'
                   }
               ,'ru':
                   {'short': 'ген.инж.'
                   ,'title': 'Генная инженерия'
                   }
               ,'de':
                   {'short': 'gen.eng.'
                   ,'title': 'Genetic engineering'
                   }
               ,'es':
                   {'short': 'gen.eng.'
                   ,'title': 'Genetic engineering'
                   }
               ,'uk':
                   {'short': 'ген.інж.'
                   ,'title': 'Генна інженерія'
                   }
               }
           ,'geneal.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'geneal.'
                   ,'title': 'Genealogy'
                   }
               ,'ru':
                   {'short': 'генеал.'
                   ,'title': 'Генеалогия'
                   }
               ,'de':
                   {'short': 'geneal.'
                   ,'title': 'Genealogy'
                   }
               ,'es':
                   {'short': 'geneal.'
                   ,'title': 'Genealogy'
                   }
               ,'uk':
                   {'short': 'генеал.'
                   ,'title': 'Генеалогія'
                   }
               }
           ,'genet.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'genet.'
                   ,'title': 'Genetics'
                   }
               ,'ru':
                   {'short': 'ген.'
                   ,'title': 'Генетика'
                   }
               ,'de':
                   {'short': 'gen.'
                   ,'title': 'Genetik'
                   }
               ,'es':
                   {'short': 'genét.'
                   ,'title': 'Genética'
                   }
               ,'uk':
                   {'short': 'ген.'
                   ,'title': 'Генетика'
                   }
               }
           ,'geobot.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'geobot.'
                   ,'title': 'Geobotanics'
                   }
               ,'ru':
                   {'short': 'геобот.'
                   ,'title': 'Геоботаника'
                   }
               ,'de':
                   {'short': 'geobot.'
                   ,'title': 'Geobotanics'
                   }
               ,'es':
                   {'short': 'geobot.'
                   ,'title': 'Geobotanics'
                   }
               ,'uk':
                   {'short': 'геобот.'
                   ,'title': 'Геоботаніка'
                   }
               }
           ,'geochem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'geochem.'
                   ,'title': 'Geochemistry'
                   }
               ,'ru':
                   {'short': 'геохим.'
                   ,'title': 'Геохимия'
                   }
               ,'de':
                   {'short': 'Geochem.'
                   ,'title': 'Geochemie'
                   }
               ,'es':
                   {'short': 'geochem.'
                   ,'title': 'Geochemistry'
                   }
               ,'uk':
                   {'short': 'геохім.'
                   ,'title': 'Геохімія'
                   }
               }
           ,'geochron.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'geochron.'
                   ,'title': 'Geochronology'
                   }
               ,'ru':
                   {'short': 'геохрон.'
                   ,'title': 'Геохронология'
                   }
               ,'de':
                   {'short': 'geochron.'
                   ,'title': 'Geochronology'
                   }
               ,'es':
                   {'short': 'geochron.'
                   ,'title': 'Geochronology'
                   }
               ,'uk':
                   {'short': 'геохрон.'
                   ,'title': 'Геохронологія'
                   }
               }
           ,'geogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': True
               ,'en':
                   {'short': 'geogr.'
                   ,'title': 'Geography'
                   }
               ,'ru':
                   {'short': 'геогр.'
                   ,'title': 'География'
                   }
               ,'de':
                   {'short': 'Geogr.'
                   ,'title': 'Geographie'
                   }
               ,'es':
                   {'short': 'geogr.'
                   ,'title': 'Geografía'
                   }
               ,'uk':
                   {'short': 'геогр.'
                   ,'title': 'Географія'
                   }
               }
           ,'geol.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': True
               ,'en':
                   {'short': 'geol.'
                   ,'title': 'Geology'
                   }
               ,'ru':
                   {'short': 'геол.'
                   ,'title': 'Геология'
                   }
               ,'de':
                   {'short': 'Geol.'
                   ,'title': 'Geologie'
                   }
               ,'es':
                   {'short': 'geol.'
                   ,'title': 'Geología'
                   }
               ,'uk':
                   {'short': 'геолог.'
                   ,'title': 'Геологія'
                   }
               }
           ,'geom.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'geom.'
                   ,'title': 'Geometry'
                   }
               ,'ru':
                   {'short': 'геом.'
                   ,'title': 'Геометрия'
                   }
               ,'de':
                   {'short': 'Geomet.'
                   ,'title': 'Geometrie'
                   }
               ,'es':
                   {'short': 'geom.'
                   ,'title': 'Geometría'
                   }
               ,'uk':
                   {'short': 'геом.'
                   ,'title': 'Геометрія'
                   }
               }
           ,'geomech.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'geomech.'
                   ,'title': 'Geomechanics'
                   }
               ,'ru':
                   {'short': 'геомех.'
                   ,'title': 'Геомеханика'
                   }
               ,'de':
                   {'short': 'geomech.'
                   ,'title': 'Geomechanics'
                   }
               ,'es':
                   {'short': 'geomech.'
                   ,'title': 'Geomechanics'
                   }
               ,'uk':
                   {'short': 'геомех.'
                   ,'title': 'Геомеханіка'
                   }
               }
           ,'geomorph.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'geomorph.'
                   ,'title': 'Geomorphology'
                   }
               ,'ru':
                   {'short': 'геоморф.'
                   ,'title': 'Геоморфология'
                   }
               ,'de':
                   {'short': 'Geomorphol.'
                   ,'title': 'Geomorphologie'
                   }
               ,'es':
                   {'short': 'geomorph.'
                   ,'title': 'Geomorphology'
                   }
               ,'uk':
                   {'short': 'геоморф.'
                   ,'title': 'Геоморфологія'
                   }
               }
           ,'geophys.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'geophys.'
                   ,'title': 'Geophysics'
                   }
               ,'ru':
                   {'short': 'геофиз.'
                   ,'title': 'Геофизика'
                   }
               ,'de':
                   {'short': 'Geophys.'
                   ,'title': 'Geophysik'
                   }
               ,'es':
                   {'short': 'geophys.'
                   ,'title': 'Geophysics'
                   }
               ,'uk':
                   {'short': 'геофіз.'
                   ,'title': 'Геофізика'
                   }
               }
           ,'germ.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'germ.'
                   ,'title': 'German'
                   }
               ,'ru':
                   {'short': 'нем.'
                   ,'title': 'Немецкий язык'
                   }
               ,'de':
                   {'short': 'Deu.'
                   ,'title': 'Deutsch'
                   }
               ,'es':
                   {'short': 'alem.'
                   ,'title': 'Alemán'
                   }
               ,'uk':
                   {'short': 'нім.'
                   ,'title': 'Німецька мова'
                   }
               }
           ,'glass':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'glass'
                   ,'title': 'Glass production'
                   }
               ,'ru':
                   {'short': 'стекл.'
                   ,'title': 'Стеклоделие'
                   }
               ,'de':
                   {'short': 'glass'
                   ,'title': 'Glass production'
                   }
               ,'es':
                   {'short': 'glass'
                   ,'title': 'Glass production'
                   }
               ,'uk':
                   {'short': 'склян.'
                   ,'title': 'Склоробство'
                   }
               }
           ,'glass.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'glass.'
                   ,'title': 'Glass container manufacture'
                   }
               ,'ru':
                   {'short': 'стеклотар.'
                   ,'title': 'Стеклотарная промышленность'
                   }
               ,'de':
                   {'short': 'glass.'
                   ,'title': 'Glass container manufacture'
                   }
               ,'es':
                   {'short': 'glass.'
                   ,'title': 'Glass container manufacture'
                   }
               ,'uk':
                   {'short': 'склотар.'
                   ,'title': 'Склотарна промисловість'
                   }
               }
           ,'gloom.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'gloom.'
                   ,'title': 'Gloomy'
                   }
               ,'ru':
                   {'short': 'мрачн.'
                   ,'title': 'Мрачно'
                   }
               ,'de':
                   {'short': 'Düster.'
                   ,'title': 'Düster'
                   }
               ,'es':
                   {'short': 'sombr.'
                   ,'title': 'Sombrío'
                   }
               ,'uk':
                   {'short': 'похмур.'
                   ,'title': 'Похмуро'
                   }
               }
           ,'goldmin.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'goldmin.'
                   ,'title': 'Gold mining'
                   }
               ,'ru':
                   {'short': 'золот.'
                   ,'title': 'Золотодобыча'
                   }
               ,'de':
                   {'short': 'goldmin.'
                   ,'title': 'Gold mining'
                   }
               ,'es':
                   {'short': 'goldmin.'
                   ,'title': 'Gold mining'
                   }
               ,'uk':
                   {'short': 'зол.доб.'
                   ,'title': 'Золотодобування'
                   }
               }
           ,'golf.':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'golf.'
                   ,'title': 'Golf'
                   }
               ,'ru':
                   {'short': 'гольф.'
                   ,'title': 'Гольф'
                   }
               ,'de':
                   {'short': 'golf.'
                   ,'title': 'Golf'
                   }
               ,'es':
                   {'short': 'golf.'
                   ,'title': 'Golf'
                   }
               ,'uk':
                   {'short': 'гольф.'
                   ,'title': 'Гольф'
                   }
               }
           ,'gov.':
               {'is_valid': False
               ,'major_en': 'Government, administration and public services'
               ,'is_major': True
               ,'en':
                   {'short': 'gov.'
                   ,'title': 'Government, administration and public services'
                   }
               ,'ru':
                   {'short': 'гос.'
                   ,'title': 'Государственный аппарат и госуслуги'
                   }
               ,'de':
                   {'short': 'gov.'
                   ,'title': 'Government, administration and public services'
                   }
               ,'es':
                   {'short': 'gov.'
                   ,'title': 'Government, administration and public services'
                   }
               ,'uk':
                   {'short': 'держ.'
                   ,'title': 'Державний апарат та державні послуги'
                   }
               }
           ,'gram.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'gram.'
                   ,'title': 'Grammar'
                   }
               ,'ru':
                   {'short': 'грам.'
                   ,'title': 'Грамматика'
                   }
               ,'de':
                   {'short': 'Gramm.'
                   ,'title': 'Grammatik'
                   }
               ,'es':
                   {'short': 'gram.'
                   ,'title': 'Gramática'
                   }
               ,'uk':
                   {'short': 'грам.'
                   ,'title': 'Граматика'
                   }
               }
           ,'grav.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'grav.'
                   ,'title': 'Gravimetry'
                   }
               ,'ru':
                   {'short': 'грав.'
                   ,'title': 'Гравиметрия'
                   }
               ,'de':
                   {'short': 'grav.'
                   ,'title': 'Gravimetry'
                   }
               ,'es':
                   {'short': 'grav.'
                   ,'title': 'Gravimetry'
                   }
               ,'uk':
                   {'short': 'грав.'
                   ,'title': 'Гравіметрія'
                   }
               }
           ,'greek.lang.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'greek.lang.'
                   ,'title': 'Greek'
                   }
               ,'ru':
                   {'short': 'греч.'
                   ,'title': 'Греческий язык'
                   }
               ,'de':
                   {'short': 'Griech.'
                   ,'title': 'Griechisch'
                   }
               ,'es':
                   {'short': 'gr.'
                   ,'title': 'Griego'
                   }
               ,'uk':
                   {'short': 'грецьк.'
                   ,'title': 'Грецька мова'
                   }
               }
           ,'green.tech.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'green.tech.'
                   ,'title': 'Greenhouse technology'
                   }
               ,'ru':
                   {'short': 'тепличн.тех.'
                   ,'title': 'Тепличные технологии'
                   }
               ,'de':
                   {'short': 'green.tech.'
                   ,'title': 'Greenhouse technology'
                   }
               ,'es':
                   {'short': 'green.tech.'
                   ,'title': 'Greenhouse technology'
                   }
               ,'uk':
                   {'short': 'тепличн.тех.'
                   ,'title': 'Тепличні технології'
                   }
               }
           ,'gymn.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'gymn.'
                   ,'title': 'Gymnastics'
                   }
               ,'ru':
                   {'short': 'гимн.'
                   ,'title': 'Гимнастика'
                   }
               ,'de':
                   {'short': 'gymn.'
                   ,'title': 'Gymnastics'
                   }
               ,'es':
                   {'short': 'gymn.'
                   ,'title': 'Gymnastics'
                   }
               ,'uk':
                   {'short': 'гімн.'
                   ,'title': 'Гімнастика'
                   }
               }
           ,'gyrosc.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'gyrosc.'
                   ,'title': 'Gyroscopes'
                   }
               ,'ru':
                   {'short': 'гироск.'
                   ,'title': 'Гироскопы'
                   }
               ,'de':
                   {'short': 'gyrosc.'
                   ,'title': 'Gyroscopes'
                   }
               ,'es':
                   {'short': 'gyrosc.'
                   ,'title': 'Gyroscopes'
                   }
               ,'uk':
                   {'short': 'гіроск.'
                   ,'title': 'Гіроскопи'
                   }
               }
           ,'h.rghts.act.':
               {'is_valid': True
               ,'major_en': 'Human rights activism'
               ,'is_major': True
               ,'en':
                   {'short': 'h.rghts.act.'
                   ,'title': 'Human rights activism'
                   }
               ,'ru':
                   {'short': 'прав.чел.'
                   ,'title': 'Права человека и правозащитная деят.'
                   }
               ,'de':
                   {'short': 'MR.Akt.'
                   ,'title': 'Menschenrechtsaktivismus'
                   }
               ,'es':
                   {'short': 'h.rghts.act.'
                   ,'title': 'Human rights activism'
                   }
               ,'uk':
                   {'short': 'прав.люд.'
                   ,'title': 'Права людини і правозахисна діяльність'
                   }
               }
           ,'hab.':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'hab.'
                   ,'title': 'Haberdashery'
                   }
               ,'ru':
                   {'short': 'галант.'
                   ,'title': 'Галантерея'
                   }
               ,'de':
                   {'short': 'hab.'
                   ,'title': 'Haberdashery'
                   }
               ,'es':
                   {'short': 'hab.'
                   ,'title': 'Haberdashery'
                   }
               ,'uk':
                   {'short': 'галант.'
                   ,'title': 'Галантерея'
                   }
               }
           ,'hack.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'hack.'
                   ,'title': 'Hacking'
                   }
               ,'ru':
                   {'short': 'хакер.'
                   ,'title': 'Хакерство'
                   }
               ,'de':
                   {'short': 'hack.'
                   ,'title': 'Hacking'
                   }
               ,'es':
                   {'short': 'hack.'
                   ,'title': 'Hacking'
                   }
               ,'uk':
                   {'short': 'хакер.'
                   ,'title': 'Хакерство'
                   }
               }
           ,'handb.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'handb.'
                   ,'title': 'Handball'
                   }
               ,'ru':
                   {'short': 'ганд.'
                   ,'title': 'Гандбол'
                   }
               ,'de':
                   {'short': 'handb.'
                   ,'title': 'Handball'
                   }
               ,'es':
                   {'short': 'handb.'
                   ,'title': 'Handball'
                   }
               ,'uk':
                   {'short': 'гандб.'
                   ,'title': 'Гандбол'
                   }
               }
           ,'handicraft.':
               {'is_valid': True
               ,'major_en': 'Hobbies and pastimes'
               ,'is_major': False
               ,'en':
                   {'short': 'handicraft.'
                   ,'title': 'Handicraft'
                   }
               ,'ru':
                   {'short': 'рукод.'
                   ,'title': 'Рукоделие'
                   }
               ,'de':
                   {'short': 'handicraft.'
                   ,'title': 'Handicraft'
                   }
               ,'es':
                   {'short': 'handicraft.'
                   ,'title': 'Handicraft'
                   }
               ,'uk':
                   {'short': 'рукод.'
                   ,'title': 'Рукоділля'
                   }
               }
           ,'hawai.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'hawai.'
                   ,'title': 'Hawaii'
                   }
               ,'ru':
                   {'short': 'гавайск.'
                   ,'title': 'Гавайский'
                   }
               ,'de':
                   {'short': 'Hawaii'
                   ,'title': 'Hawaiisch'
                   }
               ,'es':
                   {'short': 'hawai.'
                   ,'title': 'Hawaii'
                   }
               ,'uk':
                   {'short': 'Гаваї'
                   ,'title': 'Гаваї'
                   }
               }
           ,'health.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'health.'
                   ,'title': 'Health care'
                   }
               ,'ru':
                   {'short': 'здрав.'
                   ,'title': 'Здравоохранение'
                   }
               ,'de':
                   {'short': 'health.'
                   ,'title': 'Health care'
                   }
               ,'es':
                   {'short': 'health.'
                   ,'title': 'Health care'
                   }
               ,'uk':
                   {'short': 'ох.здор.'
                   ,'title': 'Охорона здоров’я'
                   }
               }
           ,'hear.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'hear.'
                   ,'title': 'Hearing aid'
                   }
               ,'ru':
                   {'short': 'слух.'
                   ,'title': 'Слуховые аппараты'
                   }
               ,'de':
                   {'short': 'Hörg.'
                   ,'title': 'Hörgeräte'
                   }
               ,'es':
                   {'short': 'hear.'
                   ,'title': 'Hearing aid'
                   }
               ,'uk':
                   {'short': 'слух.ап.'
                   ,'title': 'Слухові апарати'
                   }
               }
           ,'heat.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'heat.'
                   ,'title': 'Heating'
                   }
               ,'ru':
                   {'short': 'отопл.'
                   ,'title': 'Отопление'
                   }
               ,'de':
                   {'short': 'Hzg.'
                   ,'title': 'Heizung'
                   }
               ,'es':
                   {'short': 'heat.'
                   ,'title': 'Heating'
                   }
               ,'uk':
                   {'short': 'опален.'
                   ,'title': 'Опалення'
                   }
               }
           ,'heat.exch.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'heat.exch.'
                   ,'title': 'Heat exchangers'
                   }
               ,'ru':
                   {'short': 'тепл.апп.'
                   ,'title': 'Теплообменные аппараты'
                   }
               ,'de':
                   {'short': 'heat.exch.'
                   ,'title': 'Heat exchangers'
                   }
               ,'es':
                   {'short': 'heat.exch.'
                   ,'title': 'Heat exchangers'
                   }
               ,'uk':
                   {'short': 'тепл.ап.'
                   ,'title': 'Теплообмінні апарати'
                   }
               }
           ,'heat.transf.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'heat.transf.'
                   ,'title': 'Heat transfer'
                   }
               ,'ru':
                   {'short': 'теплоперед.'
                   ,'title': 'Теплопередача'
                   }
               ,'de':
                   {'short': 'heat.transf.'
                   ,'title': 'Heat transfer'
                   }
               ,'es':
                   {'short': 'heat.transf.'
                   ,'title': 'Heat transfer'
                   }
               ,'uk':
                   {'short': 'теплопер.'
                   ,'title': 'Теплопередача'
                   }
               }
           ,'heavy.eq.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'heavy.eq.'
                   ,'title': 'Heavy equipment vehicles'
                   }
               ,'ru':
                   {'short': 'строй.тех.'
                   ,'title': 'Строительная техника'
                   }
               ,'de':
                   {'short': 'heavy.eq.'
                   ,'title': 'Heavy equipment vehicles'
                   }
               ,'es':
                   {'short': 'heavy.eq.'
                   ,'title': 'Heavy equipment vehicles'
                   }
               ,'uk':
                   {'short': 'буд.тех.'
                   ,'title': 'Будівельна техніка'
                   }
               }
           ,'helic.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'helic.'
                   ,'title': 'Helicopters'
                   }
               ,'ru':
                   {'short': 'верт.'
                   ,'title': 'Вертолёты'
                   }
               ,'de':
                   {'short': 'helic.'
                   ,'title': 'Helicopters'
                   }
               ,'es':
                   {'short': 'helic.'
                   ,'title': 'Helicopters'
                   }
               ,'uk':
                   {'short': 'гелік.'
                   ,'title': 'Гелікоптери'
                   }
               }
           ,'helminth.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'helminth.'
                   ,'title': 'Helminthology'
                   }
               ,'ru':
                   {'short': 'гельм.'
                   ,'title': 'Гельминтология'
                   }
               ,'de':
                   {'short': 'Helminthol.'
                   ,'title': 'Helminthologie'
                   }
               ,'es':
                   {'short': 'helmint.'
                   ,'title': 'Helmintología'
                   }
               ,'uk':
                   {'short': 'гельм.'
                   ,'title': 'Гельмінтологія'
                   }
               }
           ,'hemat.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'hemat.'
                   ,'title': 'Hematology'
                   }
               ,'ru':
                   {'short': 'гемат.'
                   ,'title': 'Гематология'
                   }
               ,'de':
                   {'short': 'Hämatol.'
                   ,'title': 'Hämatologie'
                   }
               ,'es':
                   {'short': 'hemat.'
                   ,'title': 'Hematología'
                   }
               ,'uk':
                   {'short': 'гемат.'
                   ,'title': 'Гематологія'
                   }
               }
           ,'herald.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'herald.'
                   ,'title': 'Heraldry'
                   }
               ,'ru':
                   {'short': 'геральд.'
                   ,'title': 'Геральдика'
                   }
               ,'de':
                   {'short': 'Heral.'
                   ,'title': 'Heraldik'
                   }
               ,'es':
                   {'short': 'heráld.'
                   ,'title': 'Heráldica'
                   }
               ,'uk':
                   {'short': 'геральд.'
                   ,'title': 'Геральдика'
                   }
               }
           ,'herpet.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'herpet.'
                   ,'title': 'Herpetology (incl. serpentology)'
                   }
               ,'ru':
                   {'short': 'герпет.'
                   ,'title': 'Герпетология (вкл. с серпентологией)'
                   }
               ,'de':
                   {'short': 'herpet.'
                   ,'title': 'Herpetology (incl. serpentology)'
                   }
               ,'es':
                   {'short': 'herpet.'
                   ,'title': 'Herpetology (incl. serpentology)'
                   }
               ,'uk':
                   {'short': 'герпет.'
                   ,'title': 'Герпетологія (вкл. з серпентологією)'
                   }
               }
           ,'hi-fi':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'hi-fi'
                   ,'title': 'Hi-Fi'
                   }
               ,'ru':
                   {'short': 'hi-fi.'
                   ,'title': 'Hi-Fi акустика'
                   }
               ,'de':
                   {'short': 'hi-fi'
                   ,'title': 'Hi-Fi'
                   }
               ,'es':
                   {'short': 'hi-fi'
                   ,'title': 'Hi-Fi'
                   }
               ,'uk':
                   {'short': 'Hi-Fi'
                   ,'title': 'Hi-Fi'
                   }
               }
           ,'hi.jump.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'hi.jump.'
                   ,'title': 'High jump'
                   }
               ,'ru':
                   {'short': 'прыж.выс.'
                   ,'title': 'Прыжки в высоту'
                   }
               ,'de':
                   {'short': 'hi.jump.'
                   ,'title': 'High jump'
                   }
               ,'es':
                   {'short': 'hi.jump.'
                   ,'title': 'High jump'
                   }
               ,'uk':
                   {'short': 'стриб.вис.'
                   ,'title': 'Стрибки у висоту'
                   }
               }
           ,'hindi':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'hindi'
                   ,'title': 'Hindi'
                   }
               ,'ru':
                   {'short': 'хинд.'
                   ,'title': 'Хинди'
                   }
               ,'de':
                   {'short': 'Ind.'
                   ,'title': 'Indisch'
                   }
               ,'es':
                   {'short': 'hindi'
                   ,'title': 'Hindi'
                   }
               ,'uk':
                   {'short': 'хінді'
                   ,'title': 'Хінді'
                   }
               }
           ,'hist.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': True
               ,'en':
                   {'short': 'hist.'
                   ,'title': 'Historical'
                   }
               ,'ru':
                   {'short': 'ист.'
                   ,'title': 'История'
                   }
               ,'de':
                   {'short': 'Gesch.'
                   ,'title': 'Geschichte'
                   }
               ,'es':
                   {'short': 'hist.'
                   ,'title': 'Historia'
                   }
               ,'uk':
                   {'short': 'іст.'
                   ,'title': 'Історія'
                   }
               }
           ,'hist.fig.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'hist.fig.'
                   ,'title': 'Historical figure'
                   }
               ,'ru':
                   {'short': 'ист.личн.'
                   ,'title': 'Исторические личности'
                   }
               ,'de':
                   {'short': 'hist.fig.'
                   ,'title': 'Historical figure'
                   }
               ,'es':
                   {'short': 'hist.fig.'
                   ,'title': 'Historical figure'
                   }
               ,'uk':
                   {'short': 'іст.особ.'
                   ,'title': 'Історичні особистості'
                   }
               }
           ,'histol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'histol.'
                   ,'title': 'Histology'
                   }
               ,'ru':
                   {'short': 'гистол.'
                   ,'title': 'Гистология'
                   }
               ,'de':
                   {'short': 'Histol.'
                   ,'title': 'Histologie'
                   }
               ,'es':
                   {'short': 'histol.'
                   ,'title': 'Histología'
                   }
               ,'uk':
                   {'short': 'гіст.'
                   ,'title': 'Гістологія'
                   }
               }
           ,'hobby':
               {'is_valid': False
               ,'major_en': 'Hobbies and pastimes'
               ,'is_major': True
               ,'en':
                   {'short': 'hobby'
                   ,'title': 'Hobbies and pastimes'
                   }
               ,'ru':
                   {'short': 'хобби.'
                   ,'title': 'Хобби, увлечения, досуг'
                   }
               ,'de':
                   {'short': 'H.u.Fr.z.'
                   ,'title': 'Hobby und Freizeit'
                   }
               ,'es':
                   {'short': 'hobby'
                   ,'title': 'Hobbies and pastimes'
                   }
               ,'uk':
                   {'short': 'хобі.'
                   ,'title': 'Хобі, захоплення, дозвілля'
                   }
               }
           ,'hockey.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'hockey.'
                   ,'title': 'Hockey'
                   }
               ,'ru':
                   {'short': 'хок.'
                   ,'title': 'Хоккей'
                   }
               ,'de':
                   {'short': 'hockey.'
                   ,'title': 'Hockey'
                   }
               ,'es':
                   {'short': 'hockey.'
                   ,'title': 'Hockey'
                   }
               ,'uk':
                   {'short': 'хокей'
                   ,'title': 'Хокей'
                   }
               }
           ,'homeopath.':
               {'is_valid': True
               ,'major_en': 'Medicine - Alternative medicine'
               ,'is_major': False
               ,'en':
                   {'short': 'homeopath.'
                   ,'title': 'Homeopathy'
                   }
               ,'ru':
                   {'short': 'гомеопат.'
                   ,'title': 'Гомеопатия'
                   }
               ,'de':
                   {'short': 'homeopath.'
                   ,'title': 'Homeopathy'
                   }
               ,'es':
                   {'short': 'homeopath.'
                   ,'title': 'Homeopathy'
                   }
               ,'uk':
                   {'short': 'гомеопат.'
                   ,'title': 'Гомеопатія'
                   }
               }
           ,'horse.breed.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'ru':
                   {'short': 'кон.'
                   ,'title': 'Коневодство'
                   }
               ,'de':
                   {'short': 'horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'es':
                   {'short': 'horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'uk':
                   {'short': 'кон.'
                   ,'title': 'Конярство'
                   }
               }
           ,'horse.rac.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'horse.rac.'
                   ,'title': 'Horse racing'
                   }
               ,'ru':
                   {'short': 'скачк.'
                   ,'title': 'Скачки'
                   }
               ,'de':
                   {'short': 'horse.rac.'
                   ,'title': 'Horse racing'
                   }
               ,'es':
                   {'short': 'horse.rac.'
                   ,'title': 'Horse racing'
                   }
               ,'uk':
                   {'short': 'кінн.перег.'
                   ,'title': 'Кінні перегони'
                   }
               }
           ,'horticult.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'horticult.'
                   ,'title': 'Horticulture'
                   }
               ,'ru':
                   {'short': 'раст.'
                   ,'title': 'Растениеводство'
                   }
               ,'de':
                   {'short': 'horticult.'
                   ,'title': 'Horticulture'
                   }
               ,'es':
                   {'short': 'horticult.'
                   ,'title': 'Horticulture'
                   }
               ,'uk':
                   {'short': 'росл.'
                   ,'title': 'Рослинництво'
                   }
               }
           ,'hotels':
               {'is_valid': True
               ,'major_en': 'Service industry'
               ,'is_major': False
               ,'en':
                   {'short': 'hotels'
                   ,'title': 'Hotel industry'
                   }
               ,'ru':
                   {'short': 'гост.'
                   ,'title': 'Гостиничное дело'
                   }
               ,'de':
                   {'short': 'hotels'
                   ,'title': 'Hotel industry'
                   }
               ,'es':
                   {'short': 'hotels'
                   ,'title': 'Hotel industry'
                   }
               ,'uk':
                   {'short': 'готел.'
                   ,'title': 'Готельна справа'
                   }
               }
           ,'house.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'house.'
                   ,'title': 'Household appliances'
                   }
               ,'ru':
                   {'short': 'быт.тех.'
                   ,'title': 'Бытовая техника'
                   }
               ,'de':
                   {'short': 'Haush.ger.'
                   ,'title': 'Haushaltsgeräte'
                   }
               ,'es':
                   {'short': 'house.'
                   ,'title': 'Household appliances'
                   }
               ,'uk':
                   {'short': 'побут.тех.'
                   ,'title': 'Побутова техніка'
                   }
               }
           ,'hovercr.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'hovercr.'
                   ,'title': 'Hovercraft'
                   }
               ,'ru':
                   {'short': 'СВП.'
                   ,'title': 'Суда на воздушной подушке'
                   }
               ,'de':
                   {'short': 'hovercr.'
                   ,'title': 'Hovercraft'
                   }
               ,'es':
                   {'short': 'hovercr.'
                   ,'title': 'Hovercraft'
                   }
               ,'uk':
                   {'short': 'СПП'
                   ,'title': 'Судна на повітряній подушці'
                   }
               }
           ,'humor.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'humor.'
                   ,'title': 'Humorous / Jocular'
                   }
               ,'ru':
                   {'short': 'шутл.'
                   ,'title': 'Шутливое выражение'
                   }
               ,'de':
                   {'short': 'scherzh.'
                   ,'title': 'Scherzhafter Ausdruck'
                   }
               ,'es':
                   {'short': 'humor.'
                   ,'title': 'Humorístico'
                   }
               ,'uk':
                   {'short': 'жарт.'
                   ,'title': 'Жартівливий вираз'
                   }
               }
           ,'hunt.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'hunt.'
                   ,'title': 'Hunting'
                   }
               ,'ru':
                   {'short': 'охот.'
                   ,'title': 'Охота и охотоведение'
                   }
               ,'de':
                   {'short': 'Jagd.'
                   ,'title': 'Jagd'
                   }
               ,'es':
                   {'short': 'caza'
                   ,'title': 'Caza y cinegética'
                   }
               ,'uk':
                   {'short': 'мислив.'
                   ,'title': 'Мисливство та мисливствознавство'
                   }
               }
           ,'hydr.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'hydr.'
                   ,'title': 'Hydraulic engineering'
                   }
               ,'ru':
                   {'short': 'гидротех.'
                   ,'title': 'Гидротехника'
                   }
               ,'de':
                   {'short': 'hydr.'
                   ,'title': 'Hydraulic engineering'
                   }
               ,'es':
                   {'short': 'hydr.'
                   ,'title': 'Hydraulic engineering'
                   }
               ,'uk':
                   {'short': 'гідротех.'
                   ,'title': 'Гідротехніка'
                   }
               }
           ,'hydraul.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'hydraul.'
                   ,'title': 'Hydraulics'
                   }
               ,'ru':
                   {'short': 'гидравл.'
                   ,'title': 'Гидравлика'
                   }
               ,'de':
                   {'short': 'Hydr.'
                   ,'title': 'Hydraulik'
                   }
               ,'es':
                   {'short': 'hydraul.'
                   ,'title': 'Hydraulics'
                   }
               ,'uk':
                   {'short': 'гідравл.'
                   ,'title': 'Гідравліка'
                   }
               }
           ,'hydroac.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'hydroac.'
                   ,'title': 'Hydroacoustics'
                   }
               ,'ru':
                   {'short': 'гидроак.'
                   ,'title': 'Гидроакустика'
                   }
               ,'de':
                   {'short': 'hydroac.'
                   ,'title': 'Hydroacoustics'
                   }
               ,'es':
                   {'short': 'hydroac.'
                   ,'title': 'Hydroacoustics'
                   }
               ,'uk':
                   {'short': 'гідроак.'
                   ,'title': 'Гідроакустика'
                   }
               }
           ,'hydrobiol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'hydrobiol.'
                   ,'title': 'Hydrobiology'
                   }
               ,'ru':
                   {'short': 'гидробиол.'
                   ,'title': 'Гидробиология'
                   }
               ,'de':
                   {'short': 'Hydrobiol.'
                   ,'title': 'Hydrobiologie'
                   }
               ,'es':
                   {'short': 'hydrobiol.'
                   ,'title': 'Hydrobiology'
                   }
               ,'uk':
                   {'short': 'гідробіол.'
                   ,'title': 'Гідробіологія'
                   }
               }
           ,'hydroel.st.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'hydroel.st.'
                   ,'title': 'Hydroelectric power stations'
                   }
               ,'ru':
                   {'short': 'ГЭС.'
                   ,'title': 'Гидроэлектростанции'
                   }
               ,'de':
                   {'short': 'WKW.'
                   ,'title': 'Wasserkraftwerk'
                   }
               ,'es':
                   {'short': 'hydroel.st.'
                   ,'title': 'Hydroelectric power stations'
                   }
               ,'uk':
                   {'short': 'ГЕС'
                   ,'title': 'Гідроелектростанції'
                   }
               }
           ,'hydrogeol.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'hydrogeol.'
                   ,'title': 'Hydrogeology'
                   }
               ,'ru':
                   {'short': 'гидрогеол.'
                   ,'title': 'Гидрогеология'
                   }
               ,'de':
                   {'short': 'Hydrogeol.'
                   ,'title': 'Hydrogeologie'
                   }
               ,'es':
                   {'short': 'hydrogeol.'
                   ,'title': 'Hydrogeology'
                   }
               ,'uk':
                   {'short': 'гідрогеол.'
                   ,'title': 'Гідрогеологія'
                   }
               }
           ,'hydrogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'hydrogr.'
                   ,'title': 'Hydrography'
                   }
               ,'ru':
                   {'short': 'гидр.'
                   ,'title': 'Гидрография'
                   }
               ,'de':
                   {'short': 'Hydrogr.'
                   ,'title': 'Hydrographie'
                   }
               ,'es':
                   {'short': 'hidrogr.'
                   ,'title': 'Hidrografía'
                   }
               ,'uk':
                   {'short': 'гідр.'
                   ,'title': 'Гідрографія'
                   }
               }
           ,'hydrol.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'hydrol.'
                   ,'title': 'Hydrology'
                   }
               ,'ru':
                   {'short': 'гидрол.'
                   ,'title': 'Гидрология'
                   }
               ,'de':
                   {'short': 'hydrol.'
                   ,'title': 'Hydrology'
                   }
               ,'es':
                   {'short': 'hydrol.'
                   ,'title': 'Hydrology'
                   }
               ,'uk':
                   {'short': 'гідрол.'
                   ,'title': 'Гідрологія'
                   }
               }
           ,'hydromech.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'hydromech.'
                   ,'title': 'Hydromechanics'
                   }
               ,'ru':
                   {'short': 'гидромех.'
                   ,'title': 'Гидромеханика'
                   }
               ,'de':
                   {'short': 'hydromech.'
                   ,'title': 'Hydromechanics'
                   }
               ,'es':
                   {'short': 'hydromech.'
                   ,'title': 'Hydromechanics'
                   }
               ,'uk':
                   {'short': 'гідромех.'
                   ,'title': 'Гідромеханіка'
                   }
               }
           ,'hydropl.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'hydropl.'
                   ,'title': 'Hydroplanes'
                   }
               ,'ru':
                   {'short': 'гидропл.'
                   ,'title': 'Гидропланы'
                   }
               ,'de':
                   {'short': 'hydropl.'
                   ,'title': 'Hydroplanes'
                   }
               ,'es':
                   {'short': 'hydropl.'
                   ,'title': 'Hydroplanes'
                   }
               ,'uk':
                   {'short': 'гідропл.'
                   ,'title': 'Гідроплани'
                   }
               }
           ,'hygien.':
               {'is_valid': True
               ,'major_en': 'Wellness'
               ,'is_major': False
               ,'en':
                   {'short': 'hygien.'
                   ,'title': 'Hygiene'
                   }
               ,'ru':
                   {'short': 'гиг.'
                   ,'title': 'Гигиена'
                   }
               ,'de':
                   {'short': 'Hygiene.'
                   ,'title': 'Hygiene'
                   }
               ,'es':
                   {'short': 'hygien.'
                   ,'title': 'Hygiene'
                   }
               ,'uk':
                   {'short': 'гіг.'
                   ,'title': 'Гігієна'
                   }
               }
           ,'ice.form.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'ice.form.'
                   ,'title': 'Ice formation'
                   }
               ,'ru':
                   {'short': 'льдообр.'
                   ,'title': 'Льдообразование'
                   }
               ,'de':
                   {'short': 'ice.form.'
                   ,'title': 'Ice formation'
                   }
               ,'es':
                   {'short': 'ice.form.'
                   ,'title': 'Ice formation'
                   }
               ,'uk':
                   {'short': 'льодоутв.'
                   ,'title': 'Льодоутворення'
                   }
               }
           ,'icel.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'icel.'
                   ,'title': 'Iceland'
                   }
               ,'ru':
                   {'short': 'исл.'
                   ,'title': 'Исландский язык'
                   }
               ,'de':
                   {'short': 'Isl.'
                   ,'title': 'Isländisch'
                   }
               ,'es':
                   {'short': 'icel.'
                   ,'title': 'Iceland'
                   }
               ,'uk':
                   {'short': 'ісл.'
                   ,'title': 'Ісландська мова'
                   }
               }
           ,'ichtyol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'ichtyol.'
                   ,'title': 'Ichthyology'
                   }
               ,'ru':
                   {'short': 'ихт.'
                   ,'title': 'Ихтиология'
                   }
               ,'de':
                   {'short': 'Ichthyol.'
                   ,'title': 'Ichthyologie'
                   }
               ,'es':
                   {'short': 'ichtyol.'
                   ,'title': 'Ichthyology'
                   }
               ,'uk':
                   {'short': 'іхт.'
                   ,'title': 'Іхтіологія'
                   }
               }
           ,'idiom':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'idiom'
                   ,'title': 'Idiomatic'
                   }
               ,'ru':
                   {'short': 'идиом.'
                   ,'title': 'Идиоматическое выражение'
                   }
               ,'de':
                   {'short': 'idiom'
                   ,'title': 'Idiomatic'
                   }
               ,'es':
                   {'short': 'idiom'
                   ,'title': 'Idiomatic'
                   }
               ,'uk':
                   {'short': 'ідіом.в.'
                   ,'title': 'Ідіоматичний вираз'
                   }
               }
           ,'idiom, amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'idiom, amer.usg.'
                   ,'title': 'Idiomatic, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'идиом., амер.'
                   ,'title': 'Идиоматическое выражение, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'idiom, Amerik.'
                   ,'title': 'Idiomatic, Amerikanisch'
                   }
               ,'es':
                   {'short': 'idiom, amer.'
                   ,'title': 'Idiomatic, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ідіом.в., амер.вир.'
                   ,'title': 'Ідіоматичний вираз, Американський вираз (не варыант мови)'
                   }
               }
           ,'idiom, brit.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'idiom, brit.usg.'
                   ,'title': 'Idiomatic, British (usage, not BrE)'
                   }
               ,'ru':
                   {'short': 'идиом., брит.'
                   ,'title': 'Идиоматическое выражение, Британское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'idiom, Brit.'
                   ,'title': 'Idiomatic, Britische Redensart (Usus)'
                   }
               ,'es':
                   {'short': 'idiom, brit.usg.'
                   ,'title': 'Idiomatic, British (usage, not BrE)'
                   }
               ,'uk':
                   {'short': 'ідіом.в., брит.вир.'
                   ,'title': 'Ідіоматичний вираз, Британський вираз (не варіант мови)'
                   }
               }
           ,'imitat.':
               {'is_valid': True
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'imitat.'
                   ,'title': 'Iimitative (onomatopoeic)'
                   }
               ,'ru':
                   {'short': 'звукоподр.'
                   ,'title': 'Звукоподражание'
                   }
               ,'de':
                   {'short': 'Onomatop.'
                   ,'title': 'Onomatopöie'
                   }
               ,'es':
                   {'short': 'imitat.'
                   ,'title': 'Iimitative (onomatopoeic)'
                   }
               ,'uk':
                   {'short': 'звуконасл.'
                   ,'title': 'Звуконаслідування'
                   }
               }
           ,'immigr.':
               {'is_valid': True
               ,'major_en': 'Foreign affairs'
               ,'is_major': False
               ,'en':
                   {'short': 'immigr.'
                   ,'title': 'Immigration and citizenship'
                   }
               ,'ru':
                   {'short': 'иммигр.'
                   ,'title': 'Иммиграция и гражданство'
                   }
               ,'de':
                   {'short': 'immigr.'
                   ,'title': 'Immigration and citizenship'
                   }
               ,'es':
                   {'short': 'immigr.'
                   ,'title': 'Immigration and citizenship'
                   }
               ,'uk':
                   {'short': 'іміграц.'
                   ,'title': 'Іміграція та громадянство'
                   }
               }
           ,'immunol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'immunol.'
                   ,'title': 'Immunology'
                   }
               ,'ru':
                   {'short': 'иммун.'
                   ,'title': 'Иммунология'
                   }
               ,'de':
                   {'short': 'Immun.'
                   ,'title': 'Immunologie'
                   }
               ,'es':
                   {'short': 'inmunol.'
                   ,'title': 'Inmunología'
                   }
               ,'uk':
                   {'short': 'імун.'
                   ,'title': 'Імунологія'
                   }
               }
           ,'indust.hyg.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'indust.hyg.'
                   ,'title': 'Industrial hygiene'
                   }
               ,'ru':
                   {'short': 'пром.гиг.'
                   ,'title': 'Промышленная гигиена'
                   }
               ,'de':
                   {'short': 'indust.hyg.'
                   ,'title': 'Industrial hygiene'
                   }
               ,'es':
                   {'short': 'indust.hyg.'
                   ,'title': 'Industrial hygiene'
                   }
               ,'uk':
                   {'short': 'пром.гіг.'
                   ,'title': 'Промислова гігієна'
                   }
               }
           ,'industr.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': True
               ,'en':
                   {'short': 'industr.'
                   ,'title': 'Industry'
                   }
               ,'ru':
                   {'short': 'пром.'
                   ,'title': 'Промышленность'
                   }
               ,'de':
                   {'short': 'Industr.'
                   ,'title': 'Industrie'
                   }
               ,'es':
                   {'short': 'industr.'
                   ,'title': 'Industry'
                   }
               ,'uk':
                   {'short': 'пром.'
                   ,'title': 'Промисловість'
                   }
               }
           ,'inet.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'inet.'
                   ,'title': 'Internet'
                   }
               ,'ru':
                   {'short': 'инт.'
                   ,'title': 'Интернет'
                   }
               ,'de':
                   {'short': 'inet.'
                   ,'title': 'Internet'
                   }
               ,'es':
                   {'short': 'inet.'
                   ,'title': 'Internet'
                   }
               ,'uk':
                   {'short': 'інт.'
                   ,'title': 'Інтернет'
                   }
               }
           ,'inf.secur.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'inf.secur.'
                   ,'title': 'Information security'
                   }
               ,'ru':
                   {'short': 'инф.безоп.'
                   ,'title': 'Информационная безопасность'
                   }
               ,'de':
                   {'short': 'Inf.Sich.'
                   ,'title': 'Informationssicherheit'
                   }
               ,'es':
                   {'short': 'inf.secur.'
                   ,'title': 'Information security'
                   }
               ,'uk':
                   {'short': 'інф.безп.'
                   ,'title': 'Інформаційна безпека'
                   }
               }
           ,'inform.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'inform.'
                   ,'title': 'Informal'
                   }
               ,'ru':
                   {'short': 'разг.'
                   ,'title': 'Разговорная лексика'
                   }
               ,'de':
                   {'short': 'Umg.'
                   ,'title': 'Umgangssprache'
                   }
               ,'es':
                   {'short': 'inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'infr.techn.':
               {'is_valid': True
               ,'major_en': 'Security systems'
               ,'is_major': False
               ,'en':
                   {'short': 'infr.techn.'
                   ,'title': 'Infrared technology'
                   }
               ,'ru':
                   {'short': 'инфр.'
                   ,'title': 'Инфракрасная техника'
                   }
               ,'de':
                   {'short': 'infr.techn.'
                   ,'title': 'Infrared technology'
                   }
               ,'es':
                   {'short': 'infr.techn.'
                   ,'title': 'Infrared technology'
                   }
               ,'uk':
                   {'short': 'інфр.'
                   ,'title': 'Інфрачервона техніка'
                   }
               }
           ,'inherit.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'inherit.law.'
                   ,'title': 'Inheritance law'
                   }
               ,'ru':
                   {'short': 'наслед.'
                   ,'title': 'Наследственное право'
                   }
               ,'de':
                   {'short': 'Erbr.'
                   ,'title': 'Erbrecht'
                   }
               ,'es':
                   {'short': 'inherit.law.'
                   ,'title': 'Inheritance law'
                   }
               ,'uk':
                   {'short': 'спадк.пр.'
                   ,'title': 'Спадкове право'
                   }
               }
           ,'inorg.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'inorg.chem.'
                   ,'title': 'Inorganic chemistry'
                   }
               ,'ru':
                   {'short': 'неорг.хим.'
                   ,'title': 'Неорганическая химия'
                   }
               ,'de':
                   {'short': 'inorg.chem.'
                   ,'title': 'Inorganic chemistry'
                   }
               ,'es':
                   {'short': 'inorg.chem.'
                   ,'title': 'Inorganic chemistry'
                   }
               ,'uk':
                   {'short': 'неорг.хім.'
                   ,'title': 'Неорганічна хімія'
                   }
               }
           ,'insur.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'insur.'
                   ,'title': 'Insurance'
                   }
               ,'ru':
                   {'short': 'страх.'
                   ,'title': 'Страхование'
                   }
               ,'de':
                   {'short': 'Versich.'
                   ,'title': 'Versicherung'
                   }
               ,'es':
                   {'short': 'segur.'
                   ,'title': 'Seguros'
                   }
               ,'uk':
                   {'short': 'страх.'
                   ,'title': 'Страхування'
                   }
               }
           ,'int. law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'int. law.'
                   ,'title': 'International law'
                   }
               ,'ru':
                   {'short': 'межд. прав.'
                   ,'title': 'Международное право'
                   }
               ,'de':
                   {'short': 'int. law.'
                   ,'title': 'International law'
                   }
               ,'es':
                   {'short': 'int. law.'
                   ,'title': 'International law'
                   }
               ,'uk':
                   {'short': 'міжн. прав.'
                   ,'title': 'Міжнародне право'
                   }
               }
           ,'int.circ.':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'int.circ.'
                   ,'title': 'Integrated circuits'
                   }
               ,'ru':
                   {'short': 'интегр.сх.'
                   ,'title': 'Интегральные схемы'
                   }
               ,'de':
                   {'short': 'int.Schaltkr.'
                   ,'title': 'Integrierte Schaltkreise'
                   }
               ,'es':
                   {'short': 'int.circ.'
                   ,'title': 'Integrated circuits'
                   }
               ,'uk':
                   {'short': 'інтегр.сх.'
                   ,'title': 'Інтегральні схеми'
                   }
               }
           ,'int.rel.':
               {'is_valid': True
               ,'major_en': 'Foreign affairs'
               ,'is_major': False
               ,'en':
                   {'short': 'int.rel.'
                   ,'title': 'International relations'
                   }
               ,'ru':
                   {'short': 'межд.отн.'
                   ,'title': 'Международные отношения'
                   }
               ,'de':
                   {'short': 'int.rel.'
                   ,'title': 'International relations'
                   }
               ,'es':
                   {'short': 'int.rel.'
                   ,'title': 'International relations'
                   }
               ,'uk':
                   {'short': 'міжн.відн.'
                   ,'title': 'Міжнародні відносини'
                   }
               }
           ,'int.transport.':
               {'is_valid': True
               ,'major_en': 'Logistics'
               ,'is_major': False
               ,'en':
                   {'short': 'int.transport.'
                   ,'title': 'International transportation'
                   }
               ,'ru':
                   {'short': 'межд.перевозки.'
                   ,'title': 'Международные перевозки'
                   }
               ,'de':
                   {'short': 'int.transport.'
                   ,'title': 'International transportation'
                   }
               ,'es':
                   {'short': 'int.transport.'
                   ,'title': 'International transportation'
                   }
               ,'uk':
                   {'short': 'міжн.перевез.'
                   ,'title': 'Міжнародні перевезення'
                   }
               }
           ,'intell.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'intell.'
                   ,'title': 'Intelligence and security services'
                   }
               ,'ru':
                   {'short': 'спецсл.'
                   ,'title': 'Спецслужбы и разведка'
                   }
               ,'de':
                   {'short': 'intell.'
                   ,'title': 'Intelligence and security services'
                   }
               ,'es':
                   {'short': 'intell.'
                   ,'title': 'Intelligence and security services'
                   }
               ,'uk':
                   {'short': 'спецсл.'
                   ,'title': 'Спецслужби та розвідка'
                   }
               }
           ,'interntl.trade.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'interntl.trade.'
                   ,'title': 'International trade'
                   }
               ,'ru':
                   {'short': 'междун.торг.'
                   ,'title': 'Международная торговля'
                   }
               ,'de':
                   {'short': 'interntl.trade.'
                   ,'title': 'International trade'
                   }
               ,'es':
                   {'short': 'interntl.trade.'
                   ,'title': 'International trade'
                   }
               ,'uk':
                   {'short': 'міжн.торг.'
                   ,'title': 'Міжнародна торгівля'
                   }
               }
           ,'invect.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'invect.'
                   ,'title': 'Invective'
                   }
               ,'ru':
                   {'short': 'руг.'
                   ,'title': 'Ругательство'
                   }
               ,'de':
                   {'short': 'Schimpf.'
                   ,'title': 'Schimpfwort'
                   }
               ,'es':
                   {'short': 'invect.'
                   ,'title': 'Invective'
                   }
               ,'uk':
                   {'short': 'лайка'
                   ,'title': 'Лайка'
                   }
               }
           ,'invest.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'invest.'
                   ,'title': 'Investment'
                   }
               ,'ru':
                   {'short': 'инвест.'
                   ,'title': 'Инвестиции'
                   }
               ,'de':
                   {'short': 'Invest.'
                   ,'title': 'Investitionen'
                   }
               ,'es':
                   {'short': 'invest.'
                   ,'title': 'Investment'
                   }
               ,'uk':
                   {'short': 'інвест.'
                   ,'title': 'Інвестиції'
                   }
               }
           ,'irish.lang.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'irish.lang.'
                   ,'title': 'Irish'
                   }
               ,'ru':
                   {'short': 'ирл.яз.'
                   ,'title': 'Ирландский язык'
                   }
               ,'de':
                   {'short': 'Irisch.'
                   ,'title': 'Irisch'
                   }
               ,'es':
                   {'short': 'irland.'
                   ,'title': 'Irlandés'
                   }
               ,'uk':
                   {'short': 'ірл.мов.'
                   ,'title': 'Ірландська мова'
                   }
               }
           ,'ironic.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'ironic.'
                   ,'title': 'Ironical'
                   }
               ,'ru':
                   {'short': 'ирон.'
                   ,'title': 'Ирония'
                   }
               ,'de':
                   {'short': 'Iron.'
                   ,'title': 'Ironie'
                   }
               ,'es':
                   {'short': 'iron.'
                   ,'title': 'Ironía'
                   }
               ,'uk':
                   {'short': 'ірон.'
                   ,'title': 'Іронія'
                   }
               }
           ,'isol.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'isol.'
                   ,'title': 'Isolation'
                   }
               ,'ru':
                   {'short': 'изол.'
                   ,'title': 'Изоляция'
                   }
               ,'de':
                   {'short': 'isol.'
                   ,'title': 'Isolation'
                   }
               ,'es':
                   {'short': 'isol.'
                   ,'title': 'Isolation'
                   }
               ,'uk':
                   {'short': 'ізол.'
                   ,'title': 'Ізоляція'
                   }
               }
           ,'ital.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'ital.'
                   ,'title': 'Italian'
                   }
               ,'ru':
                   {'short': 'ит.'
                   ,'title': 'Итальянский язык'
                   }
               ,'de':
                   {'short': 'Ital.'
                   ,'title': 'Italienisch'
                   }
               ,'es':
                   {'short': 'ital.'
                   ,'title': 'Italiano'
                   }
               ,'uk':
                   {'short': 'італ.'
                   ,'title': 'Італійська мова'
                   }
               }
           ,'jamaic.eng.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'jamaic.eng.'
                   ,'title': 'Jamaican English'
                   }
               ,'ru':
                   {'short': 'ямайск.анг.'
                   ,'title': 'Ямайский английский'
                   }
               ,'de':
                   {'short': 'Jam.Engl.'
                   ,'title': 'Jamaika-Englisch'
                   }
               ,'es':
                   {'short': 'jamaic.eng.'
                   ,'title': 'Jamaican English'
                   }
               ,'uk':
                   {'short': 'ямайск.анг.'
                   ,'title': 'Ямайська англійська'
                   }
               }
           ,'jap.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'jap.'
                   ,'title': 'Japanese language'
                   }
               ,'ru':
                   {'short': 'яп.'
                   ,'title': 'Японский язык'
                   }
               ,'de':
                   {'short': 'Japan.'
                   ,'title': 'Japanisch'
                   }
               ,'es':
                   {'short': 'jap.'
                   ,'title': 'Japanese language'
                   }
               ,'uk':
                   {'short': 'яп.'
                   ,'title': 'Японська мова'
                   }
               }
           ,'jarg.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'jarg.'
                   ,'title': 'Jargon'
                   }
               ,'ru':
                   {'short': 'жарг.'
                   ,'title': 'Жаргон'
                   }
               ,'de':
                   {'short': 'Jar.'
                   ,'title': 'Jargon (Slang)'
                   }
               ,'es':
                   {'short': 'argot'
                   ,'title': 'Argot'
                   }
               ,'uk':
                   {'short': 'жарг.'
                   ,'title': 'Жаргон'
                   }
               }
           ,'jet.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'jet.'
                   ,'title': 'Jet engines'
                   }
               ,'ru':
                   {'short': 'реакт.'
                   ,'title': 'Реактивные двигатели'
                   }
               ,'de':
                   {'short': 'jet.'
                   ,'title': 'Jet engines'
                   }
               ,'es':
                   {'short': 'jet.'
                   ,'title': 'Jet engines'
                   }
               ,'uk':
                   {'short': 'реакт.дв.'
                   ,'title': 'Реактивні двигуни'
                   }
               }
           ,'jewl.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'jewl.'
                   ,'title': 'Jewelry'
                   }
               ,'ru':
                   {'short': 'юв.'
                   ,'title': 'Ювелирное дело'
                   }
               ,'de':
                   {'short': 'jewl.'
                   ,'title': 'Jewelry'
                   }
               ,'es':
                   {'short': 'jewl.'
                   ,'title': 'Jewelry'
                   }
               ,'uk':
                   {'short': 'юв.'
                   ,'title': 'Ювелірна справа'
                   }
               }
           ,'journ.':
               {'is_valid': True
               ,'major_en': 'Mass media'
               ,'is_major': False
               ,'en':
                   {'short': 'journ.'
                   ,'title': 'Journalism (terminology)'
                   }
               ,'ru':
                   {'short': 'журн.'
                   ,'title': 'Журналистика (терминология)'
                   }
               ,'de':
                   {'short': 'journ.'
                   ,'title': 'Journalism (terminology)'
                   }
               ,'es':
                   {'short': 'journ.'
                   ,'title': 'Journalism (terminology)'
                   }
               ,'uk':
                   {'short': 'журн.'
                   ,'title': 'Журналістика (термінологія)'
                   }
               }
           ,'judo.':
               {'is_valid': False
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': False
               ,'en':
                   {'short': 'judo.'
                   ,'title': 'Judo'
                   }
               ,'ru':
                   {'short': 'борьб., дзюд.'
                   ,'title': 'Дзюдо'
                   }
               ,'de':
                   {'short': 'judo.'
                   ,'title': 'Judo'
                   }
               ,'es':
                   {'short': 'judo.'
                   ,'title': 'Judo'
                   }
               ,'uk':
                   {'short': 'дз.'
                   ,'title': 'Дзюдо'
                   }
               }
           ,'karate.':
               {'is_valid': True
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': False
               ,'en':
                   {'short': 'karate.'
                   ,'title': 'Karate'
                   }
               ,'ru':
                   {'short': 'карате.'
                   ,'title': 'Карате'
                   }
               ,'de':
                   {'short': 'karate.'
                   ,'title': 'Karate'
                   }
               ,'es':
                   {'short': 'karate.'
                   ,'title': 'Karate'
                   }
               ,'uk':
                   {'short': 'карате.'
                   ,'title': 'Карате'
                   }
               }
           ,'knit.goods':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'knit.goods'
                   ,'title': 'Knitted goods'
                   }
               ,'ru':
                   {'short': 'трик.'
                   ,'title': 'Трикотаж'
                   }
               ,'de':
                   {'short': 'Strickw.'
                   ,'title': 'Strickwaren'
                   }
               ,'es':
                   {'short': 'knit.goods'
                   ,'title': 'Knitted goods'
                   }
               ,'uk':
                   {'short': 'трик.'
                   ,'title': 'Трикотаж'
                   }
               }
           ,'korea.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'korea.'
                   ,'title': 'Korean'
                   }
               ,'ru':
                   {'short': 'кор.'
                   ,'title': 'Корейский язык'
                   }
               ,'de':
                   {'short': 'Korean.'
                   ,'title': 'Koreanisch'
                   }
               ,'es':
                   {'short': 'korea.'
                   ,'title': 'Korean'
                   }
               ,'uk':
                   {'short': 'кор.'
                   ,'title': 'Корейська мова'
                   }
               }
           ,'lab.eq.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'lab.eq.'
                   ,'title': 'Laboratory equipment'
                   }
               ,'ru':
                   {'short': 'лаб.'
                   ,'title': 'Лабораторное оборудование'
                   }
               ,'de':
                   {'short': 'Lab.Ausstatt.'
                   ,'title': 'Laborausstattung'
                   }
               ,'es':
                   {'short': 'lab.eq.'
                   ,'title': 'Equipamiento de laboratorio'
                   }
               ,'uk':
                   {'short': 'лаб.'
                   ,'title': 'Лабораторне обладнання'
                   }
               }
           ,'lab.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'lab.law.'
                   ,'title': 'Labor law'
                   }
               ,'ru':
                   {'short': 'труд.прав.'
                   ,'title': 'Трудовое право'
                   }
               ,'de':
                   {'short': 'lab.law.'
                   ,'title': 'Labor law'
                   }
               ,'es':
                   {'short': 'lab.law.'
                   ,'title': 'Labor law'
                   }
               ,'uk':
                   {'short': 'труд.пр.'
                   ,'title': 'Трудове право'
                   }
               }
           ,'labor.org.':
               {'is_valid': True
               ,'major_en': 'Management'
               ,'is_major': False
               ,'en':
                   {'short': 'labor.org.'
                   ,'title': 'Labor organization'
                   }
               ,'ru':
                   {'short': 'орг.пр.'
                   ,'title': 'Организация производства'
                   }
               ,'de':
                   {'short': 'Betriebswirt.'
                   ,'title': 'Betriebswirtschft'
                   }
               ,'es':
                   {'short': 'labor.org.'
                   ,'title': 'Labor organization'
                   }
               ,'uk':
                   {'short': 'орг.вироб.'
                   ,'title': 'Організація виробництва'
                   }
               }
           ,'landsc.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'landsc.'
                   ,'title': 'Landscaping'
                   }
               ,'ru':
                   {'short': 'ландш.диз.'
                   ,'title': 'Ландшафтный дизайн'
                   }
               ,'de':
                   {'short': 'landsc.'
                   ,'title': 'Landscaping'
                   }
               ,'es':
                   {'short': 'landsc.'
                   ,'title': 'Landscaping'
                   }
               ,'uk':
                   {'short': 'ландш.диз.'
                   ,'title': 'Ландшафтний дизайн'
                   }
               }
           ,'laser.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'laser.'
                   ,'title': 'Lasers'
                   }
               ,'ru':
                   {'short': 'лазер.'
                   ,'title': 'Лазеры'
                   }
               ,'de':
                   {'short': 'laser.'
                   ,'title': 'Lasers'
                   }
               ,'es':
                   {'short': 'laser.'
                   ,'title': 'Lasers'
                   }
               ,'uk':
                   {'short': 'лаз.'
                   ,'title': 'Лазери'
                   }
               }
           ,'laser.med.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'laser.med.'
                   ,'title': 'Laser medicine'
                   }
               ,'ru':
                   {'short': 'лазер.мед.'
                   ,'title': 'Лазерная медицина'
                   }
               ,'de':
                   {'short': 'laser.med.'
                   ,'title': 'Laser medicine'
                   }
               ,'es':
                   {'short': 'laser.med.'
                   ,'title': 'Laser medicine'
                   }
               ,'uk':
                   {'short': 'лазер.мед.'
                   ,'title': 'Лазерна медицина'
                   }
               }
           ,'lat.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'lat.'
                   ,'title': 'Latin'
                   }
               ,'ru':
                   {'short': 'лат.'
                   ,'title': 'Латынь'
                   }
               ,'de':
                   {'short': 'Lat.'
                   ,'title': 'Latein'
                   }
               ,'es':
                   {'short': 'lat.'
                   ,'title': 'Latín'
                   }
               ,'uk':
                   {'short': 'лат.'
                   ,'title': 'Латинська мова'
                   }
               }
           ,'lat.amer.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'lat.amer.'
                   ,'title': 'Latin American'
                   }
               ,'ru':
                   {'short': 'лат.амер.'
                   ,'title': 'Латиноамериканское выражение'
                   }
               ,'de':
                   {'short': 'lat.amer.'
                   ,'title': 'Latin American'
                   }
               ,'es':
                   {'short': 'lat.amer.'
                   ,'title': 'Latin American'
                   }
               ,'uk':
                   {'short': 'лат.амер.'
                   ,'title': 'Латиноамериканський вираз'
                   }
               }
           ,'lat.amer.sl.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'lat.amer.sl.'
                   ,'title': 'Latin American slang'
                   }
               ,'ru':
                   {'short': 'лат.амер.сл.'
                   ,'title': 'Латиноамериканский сленг'
                   }
               ,'de':
                   {'short': 'Lat.am.sl.'
                   ,'title': 'Lateinamerikanischer Slang'
                   }
               ,'es':
                   {'short': 'lat.amer.sl.'
                   ,'title': 'Latin American slang'
                   }
               ,'uk':
                   {'short': 'лат.амер.жарг.'
                   ,'title': 'Латиноамериканський жаргон'
                   }
               }
           ,'laud.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'laud.'
                   ,'title': 'Laudatory'
                   }
               ,'ru':
                   {'short': 'одобр.'
                   ,'title': 'Одобрительно'
                   }
               ,'de':
                   {'short': 'Zustim.'
                   ,'title': 'Zustimmend'
                   }
               ,'es':
                   {'short': 'laud.'
                   ,'title': 'Laudatory'
                   }
               ,'uk':
                   {'short': 'схвал.'
                   ,'title': 'Схвально'
                   }
               }
           ,'law':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': True
               ,'en':
                   {'short': 'law'
                   ,'title': 'Law'
                   }
               ,'ru':
                   {'short': 'юр.'
                   ,'title': 'Юридическая лексика'
                   }
               ,'de':
                   {'short': 'Recht.'
                   ,'title': 'Recht'
                   }
               ,'es':
                   {'short': 'jur.'
                   ,'title': 'Jurídico'
                   }
               ,'uk':
                   {'short': 'юр.'
                   ,'title': 'Юридична лексика'
                   }
               }
           ,'law, ADR':
               {'is_valid': False
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'law, ADR'
                   ,'title': 'Alternative dispute resolution'
                   }
               ,'ru':
                   {'short': 'юр., АУС'
                   ,'title': 'Альтернативное урегулирование споров'
                   }
               ,'de':
                   {'short': 'law, ADR'
                   ,'title': 'Alternative dispute resolution'
                   }
               ,'es':
                   {'short': 'jur.,SAC'
                   ,'title': 'Solución alternativa de controversias'
                   }
               ,'uk':
                   {'short': 'юр., АВС'
                   ,'title': 'Альтернативне врегулювання спорів'
                   }
               }
           ,'law, amer.usg.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'law, amer.usg.'
                   ,'title': 'Law, American (usage, not AmE)'
                   }
               ,'ru':
                   {'short': 'юр., амер.'
                   ,'title': 'Юридическая лексика, Американское выражение (не вариант языка)'
                   }
               ,'de':
                   {'short': 'Recht., Amerik.'
                   ,'title': 'Recht, Amerikanisch'
                   }
               ,'es':
                   {'short': 'jur., amer.'
                   ,'title': 'Jurídico, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'юр., амер.вир.'
                   ,'title': 'Юридична лексика, Американський вираз (не варыант мови)'
                   }
               }
           ,'law, com.law':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'law, com.law'
                   ,'title': 'Common law (Anglo-Saxon legal system)'
                   }
               ,'ru':
                   {'short': 'юр., англос.'
                   ,'title': 'Общее право (англосаксонская правовая система)'
                   }
               ,'de':
                   {'short': 'angelsächs. Recht'
                   ,'title': 'Rechtskunde: angelsächsisches Rechtssystem'
                   }
               ,'es':
                   {'short': 'jur.:anglosaj.'
                   ,'title': 'Jurídico: sistema anglosajón'
                   }
               ,'uk':
                   {'short': 'юр., англос.'
                   ,'title': 'Загальне право (англосаксонська правова система)'
                   }
               }
           ,'law, contr., context.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'law, contr., context.'
                   ,'title': 'Contracts, Contextual meaning'
                   }
               ,'ru':
                   {'short': 'юр., дог., конт.'
                   ,'title': 'Договоры и контракты, Контекстуальное значение'
                   }
               ,'de':
                   {'short': 'Vertr., context.'
                   ,'title': 'Verträge, Contextual meaning'
                   }
               ,'es':
                   {'short': 'contr.jur., context.'
                   ,'title': 'Contratos jurídicos, Contextual meaning'
                   }
               ,'uk':
                   {'short': 'юр., дог., конт.'
                   ,'title': 'Договори та контракти, Контекстуальне значення'
                   }
               }
           ,'law, copyr.':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'law, copyr.'
                   ,'title': 'Copyright'
                   }
               ,'ru':
                   {'short': 'юр., автор.'
                   ,'title': 'Авторское право'
                   }
               ,'de':
                   {'short': 'Urheberrecht'
                   ,'title': 'Urheberrecht'
                   }
               ,'es':
                   {'short': 'law, copyr.'
                   ,'title': 'Copyright'
                   }
               ,'uk':
                   {'short': 'юр., автор.'
                   ,'title': 'Авторське право'
                   }
               }
           ,'law, copyr., abbr.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'law, copyr., abbr.'
                   ,'title': 'Copyright, Abbreviation'
                   }
               ,'ru':
                   {'short': 'юр., автор., сокр.'
                   ,'title': 'Авторское право, Сокращение'
                   }
               ,'de':
                   {'short': 'Urheberrecht, Abkürz.'
                   ,'title': 'Urheberrecht, Abkürzung'
                   }
               ,'es':
                   {'short': 'law, copyr., abrev.'
                   ,'title': 'Copyright, Abreviatura'
                   }
               ,'uk':
                   {'short': 'юр., автор., абрев.'
                   ,'title': 'Авторське право, Абревіатура'
                   }
               }
           ,'law, court':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'law, court'
                   ,'title': 'Court (law)'
                   }
               ,'ru':
                   {'short': 'юр., суд.'
                   ,'title': 'Судебная лексика'
                   }
               ,'de':
                   {'short': 'law, court'
                   ,'title': 'Court (law)'
                   }
               ,'es':
                   {'short': 'law, court'
                   ,'title': 'Court (law)'
                   }
               ,'uk':
                   {'short': 'юр., суд.'
                   ,'title': 'Судова лексика'
                   }
               }
           ,'law.enf.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': True
               ,'en':
                   {'short': 'law.enf.'
                   ,'title': 'Law enforcement'
                   }
               ,'ru':
                   {'short': 'правоохр.'
                   ,'title': 'Правоохранительная деятельность'
                   }
               ,'de':
                   {'short': 'law.enf.'
                   ,'title': 'Law enforcement'
                   }
               ,'es':
                   {'short': 'law.enf.'
                   ,'title': 'Law enforcement'
                   }
               ,'uk':
                   {'short': 'правоохор.'
                   ,'title': 'Правоохоронна діяльність'
                   }
               }
           ,'lean.prod.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': False
               ,'en':
                   {'short': 'lean.prod.'
                   ,'title': 'Lean production'
                   }
               ,'ru':
                   {'short': 'береж.произв.'
                   ,'title': 'Бережливое производство'
                   }
               ,'de':
                   {'short': 'lean.prod.'
                   ,'title': 'Lean production'
                   }
               ,'es':
                   {'short': 'lean.prod.'
                   ,'title': 'Lean production'
                   }
               ,'uk':
                   {'short': 'ощ.вироб.'
                   ,'title': 'Ощадливе виробництво'
                   }
               }
           ,'leath.':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'leath.'
                   ,'title': 'Leather'
                   }
               ,'ru':
                   {'short': 'кож.'
                   ,'title': 'Кожевенная промышленность'
                   }
               ,'de':
                   {'short': 'Lederindust.'
                   ,'title': 'Lederindustrie'
                   }
               ,'es':
                   {'short': 'leath.'
                   ,'title': 'Leather'
                   }
               ,'uk':
                   {'short': 'шкір.'
                   ,'title': 'Шкіряна промисловість'
                   }
               }
           ,'leg.ent.typ.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'leg.ent.typ.'
                   ,'title': 'Legal entity types (business legal structures)'
                   }
               ,'ru':
                   {'short': 'форм.комп.'
                   ,'title': 'Организационно-правовые формы компаний'
                   }
               ,'de':
                   {'short': 'leg.ent.typ.'
                   ,'title': 'Legal entity types (business legal structures)'
                   }
               ,'es':
                   {'short': 'leg.ent.typ.'
                   ,'title': 'Legal entity types (business legal structures)'
                   }
               ,'uk':
                   {'short': 'форм.комп.'
                   ,'title': 'Організаційно-правові форми компаній'
                   }
               }
           ,'legal.theor.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'legal.theor.'
                   ,'title': 'Legal theory'
                   }
               ,'ru':
                   {'short': 'теор.прав.'
                   ,'title': 'Теория права'
                   }
               ,'de':
                   {'short': 'legal.theor.'
                   ,'title': 'Legal theory'
                   }
               ,'es':
                   {'short': 'legal.theor.'
                   ,'title': 'Legal theory'
                   }
               ,'uk':
                   {'short': 'теор.прав.'
                   ,'title': 'Теорія права'
                   }
               }
           ,'level.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'level.'
                   ,'title': 'Level measurement'
                   }
               ,'ru':
                   {'short': 'уровнеметр.'
                   ,'title': 'Уровнеметрия'
                   }
               ,'de':
                   {'short': 'level.'
                   ,'title': 'Level measurement'
                   }
               ,'es':
                   {'short': 'level.'
                   ,'title': 'Level measurement'
                   }
               ,'uk':
                   {'short': 'рівнеметр.'
                   ,'title': 'Рівнеметрія'
                   }
               }
           ,'lgbt':
               {'is_valid': True
               ,'major_en': 'Human rights activism'
               ,'is_major': False
               ,'en':
                   {'short': 'lgbt'
                   ,'title': 'LGBT'
                   }
               ,'ru':
                   {'short': 'лгбт.'
                   ,'title': 'ЛГБТ'
                   }
               ,'de':
                   {'short': 'lgbt'
                   ,'title': 'LGBT'
                   }
               ,'es':
                   {'short': 'lgbt'
                   ,'title': 'LGBT'
                   }
               ,'uk':
                   {'short': 'лгбт'
                   ,'title': 'ЛГБТ'
                   }
               }
           ,'libr.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'libr.'
                   ,'title': 'Librarianship'
                   }
               ,'ru':
                   {'short': 'библиот.'
                   ,'title': 'Библиотечное дело'
                   }
               ,'de':
                   {'short': 'libr.'
                   ,'title': 'Librarianship'
                   }
               ,'es':
                   {'short': 'libr.'
                   ,'title': 'Librarianship'
                   }
               ,'uk':
                   {'short': 'бібліот.'
                   ,'title': 'Бібліотечна справа'
                   }
               }
           ,'life.sc.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': True
               ,'en':
                   {'short': 'life.sc.'
                   ,'title': 'Life sciences'
                   }
               ,'ru':
                   {'short': 'мед.-биол.'
                   ,'title': 'Медико-биологические науки'
                   }
               ,'de':
                   {'short': 'life.sc.'
                   ,'title': 'Life sciences'
                   }
               ,'es':
                   {'short': 'life.sc.'
                   ,'title': 'Life sciences'
                   }
               ,'uk':
                   {'short': 'мед.біол.'
                   ,'title': 'Медико-біологічні науки'
                   }
               }
           ,'light.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'light.'
                   ,'title': 'Lighting (other than cinema)'
                   }
               ,'ru':
                   {'short': 'свет.'
                   ,'title': 'Светотехника (кроме кино)'
                   }
               ,'de':
                   {'short': 'light.'
                   ,'title': 'Lighting (other than cinema)'
                   }
               ,'es':
                   {'short': 'light.'
                   ,'title': 'Lighting (other than cinema)'
                   }
               ,'uk':
                   {'short': 'світл.'
                   ,'title': 'Світлотехніка'
                   }
               }
           ,'limn.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'limn.'
                   ,'title': 'Limnology'
                   }
               ,'ru':
                   {'short': 'лимн.'
                   ,'title': 'Лимнология'
                   }
               ,'de':
                   {'short': 'limn.'
                   ,'title': 'Limnology'
                   }
               ,'es':
                   {'short': 'limn.'
                   ,'title': 'Limnology'
                   }
               ,'uk':
                   {'short': 'лімн.'
                   ,'title': 'Лімнологія'
                   }
               }
           ,'ling.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': True
               ,'en':
                   {'short': 'ling.'
                   ,'title': 'Linguistics'
                   }
               ,'ru':
                   {'short': 'лингв.'
                   ,'title': 'Лингвистика'
                   }
               ,'de':
                   {'short': 'Ling.'
                   ,'title': 'Linguistik'
                   }
               ,'es':
                   {'short': 'ling.'
                   ,'title': 'Lingüística'
                   }
               ,'uk':
                   {'short': 'лінгв.'
                   ,'title': 'Лінгвістика'
                   }
               }
           ,'lit.':
               {'is_valid': True
               ,'major_en': 'Literature'
               ,'is_major': True
               ,'en':
                   {'short': 'lit.'
                   ,'title': 'Literature'
                   }
               ,'ru':
                   {'short': 'лит.'
                   ,'title': 'Литература'
                   }
               ,'de':
                   {'short': 'lit.'
                   ,'title': 'Literatur'
                   }
               ,'es':
                   {'short': 'lit.'
                   ,'title': 'Literatura'
                   }
               ,'uk':
                   {'short': 'літ.'
                   ,'title': 'Література'
                   }
               }
           ,'lit., f.tales':
               {'is_valid': False
               ,'major_en': 'Literature'
               ,'is_major': False
               ,'en':
                   {'short': 'lit., f.tales'
                   ,'title': 'Fairy tales'
                   }
               ,'ru':
                   {'short': 'лит., сказк.'
                   ,'title': 'Сказки'
                   }
               ,'de':
                   {'short': 'lit., f.tales'
                   ,'title': 'Fairy tales'
                   }
               ,'es':
                   {'short': 'lit., f.tales'
                   ,'title': 'Fairy tales'
                   }
               ,'uk':
                   {'short': 'літ., казк.'
                   ,'title': 'Казки'
                   }
               }
           ,'liter.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'liter.'
                   ,'title': 'Literally'
                   }
               ,'ru':
                   {'short': 'букв.'
                   ,'title': 'Буквальное значение'
                   }
               ,'de':
                   {'short': 'liter.'
                   ,'title': 'Literally'
                   }
               ,'es':
                   {'short': 'liter.'
                   ,'title': 'Literally'
                   }
               ,'uk':
                   {'short': 'букв.'
                   ,'title': 'Буквальне значення'
                   }
               }
           ,'lithol.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'lithol.'
                   ,'title': 'Lithology'
                   }
               ,'ru':
                   {'short': 'литол.'
                   ,'title': 'Литология'
                   }
               ,'de':
                   {'short': 'Lithol.'
                   ,'title': 'Lithologie'
                   }
               ,'es':
                   {'short': 'lithol.'
                   ,'title': 'Lithology'
                   }
               ,'uk':
                   {'short': 'літол.'
                   ,'title': 'Літологія'
                   }
               }
           ,'load.equip.':
               {'is_valid': True
               ,'major_en': 'Logistics'
               ,'is_major': False
               ,'en':
                   {'short': 'load.equip.'
                   ,'title': 'Loading equipment'
                   }
               ,'ru':
                   {'short': 'погр.'
                   ,'title': 'Погрузочное оборудование'
                   }
               ,'de':
                   {'short': 'load.equip.'
                   ,'title': 'Loading equipment'
                   }
               ,'es':
                   {'short': 'load.equip.'
                   ,'title': 'Loading equipment'
                   }
               ,'uk':
                   {'short': 'вант.уст.'
                   ,'title': 'Вантажне устаткування'
                   }
               }
           ,'loc.name.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'loc.name.'
                   ,'title': 'Local name'
                   }
               ,'ru':
                   {'short': 'местн.'
                   ,'title': 'Местное название'
                   }
               ,'de':
                   {'short': 'loc.name.'
                   ,'title': 'Local name'
                   }
               ,'es':
                   {'short': 'loc.name.'
                   ,'title': 'Local name'
                   }
               ,'uk':
                   {'short': 'місц.'
                   ,'title': 'Місцева назва'
                   }
               }
           ,'logging':
               {'is_valid': True
               ,'major_en': 'Wood, pulp and paper industries'
               ,'is_major': False
               ,'en':
                   {'short': 'logging'
                   ,'title': 'Logging'
                   }
               ,'ru':
                   {'short': 'лесозаг.'
                   ,'title': 'Лесозаготовка'
                   }
               ,'de':
                   {'short': 'logging'
                   ,'title': 'Logging'
                   }
               ,'es':
                   {'short': 'logging'
                   ,'title': 'Logging'
                   }
               ,'uk':
                   {'short': 'ліс.заг.'
                   ,'title': 'Заготівля лісу'
                   }
               }
           ,'logic':
               {'is_valid': True
               ,'major_en': 'Philosophy'
               ,'is_major': False
               ,'en':
                   {'short': 'logic'
                   ,'title': 'Logic'
                   }
               ,'ru':
                   {'short': 'лог.'
                   ,'title': 'Логика'
                   }
               ,'de':
                   {'short': 'Logik.'
                   ,'title': 'Logik'
                   }
               ,'es':
                   {'short': 'lóg.'
                   ,'title': 'Lógica'
                   }
               ,'uk':
                   {'short': 'логіка'
                   ,'title': 'Логіка'
                   }
               }
           ,'logist.':
               {'is_valid': True
               ,'major_en': 'Logistics'
               ,'is_major': True
               ,'en':
                   {'short': 'logist.'
                   ,'title': 'Logistics'
                   }
               ,'ru':
                   {'short': 'логист.'
                   ,'title': 'Логистика'
                   }
               ,'de':
                   {'short': 'logist.'
                   ,'title': 'Logistics'
                   }
               ,'es':
                   {'short': 'logist.'
                   ,'title': 'Logistics'
                   }
               ,'uk':
                   {'short': 'логіст.'
                   ,'title': 'Логістика'
                   }
               }
           ,'logop.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'logop.'
                   ,'title': 'Logopedics'
                   }
               ,'ru':
                   {'short': 'логоп.'
                   ,'title': 'Логопедия'
                   }
               ,'de':
                   {'short': 'logop.'
                   ,'title': 'Logopedics'
                   }
               ,'es':
                   {'short': 'logop.'
                   ,'title': 'Logopedics'
                   }
               ,'uk':
                   {'short': 'логоп.'
                   ,'title': 'Логопедія'
                   }
               }
           ,'low':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'low'
                   ,'title': 'Low register'
                   }
               ,'ru':
                   {'short': 'сниж.'
                   ,'title': 'Сниженный регистр'
                   }
               ,'de':
                   {'short': 'Mind.Niveau'
                   ,'title': 'Minderniveau'
                   }
               ,'es':
                   {'short': 'low'
                   ,'title': 'Low register'
                   }
               ,'uk':
                   {'short': 'зниж.'
                   ,'title': 'Знижений регістр'
                   }
               }
           ,'low.germ.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'low.germ.'
                   ,'title': 'Lower German'
                   }
               ,'ru':
                   {'short': 'н.-нем.'
                   ,'title': 'Нижне-немецкое выражение'
                   }
               ,'de':
                   {'short': 'Nied.dt.'
                   ,'title': 'Niederdeutsch'
                   }
               ,'es':
                   {'short': 'low.germ.'
                   ,'title': 'Lower German'
                   }
               ,'uk':
                   {'short': 'ниж.нім.'
                   ,'title': 'Нижньо-німецький вираз'
                   }
               }
           ,'luge.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'luge.'
                   ,'title': 'Luge'
                   }
               ,'ru':
                   {'short': 'санн.спорт.'
                   ,'title': 'Санный спорт'
                   }
               ,'de':
                   {'short': 'luge.'
                   ,'title': 'Luge'
                   }
               ,'es':
                   {'short': 'luge.'
                   ,'title': 'Luge'
                   }
               ,'uk':
                   {'short': 'санн.'
                   ,'title': 'Санний спорт'
                   }
               }
           ,'mach.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'mach.'
                   ,'title': 'Machine tools'
                   }
               ,'ru':
                   {'short': 'станк.'
                   ,'title': 'Станки'
                   }
               ,'de':
                   {'short': 'mach.'
                   ,'title': 'Machine tools'
                   }
               ,'es':
                   {'short': 'mach.'
                   ,'title': 'Machine tools'
                   }
               ,'uk':
                   {'short': 'верст.'
                   ,'title': 'Верстати'
                   }
               }
           ,'mach.comp.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'mach.comp.'
                   ,'title': 'Machine components'
                   }
               ,'ru':
                   {'short': 'д.маш.'
                   ,'title': 'Детали машин'
                   }
               ,'de':
                   {'short': 'mach.comp.'
                   ,'title': 'Machine components'
                   }
               ,'es':
                   {'short': 'mach.comp.'
                   ,'title': 'Machine components'
                   }
               ,'uk':
                   {'short': 'д.маш.'
                   ,'title': 'Деталі машин'
                   }
               }
           ,'magn.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'magn.'
                   ,'title': 'Magnetics'
                   }
               ,'ru':
                   {'short': 'магн.'
                   ,'title': 'Магнетизм'
                   }
               ,'de':
                   {'short': 'Magnet.'
                   ,'title': 'Magnetismus'
                   }
               ,'es':
                   {'short': 'magn.'
                   ,'title': 'Magnetics'
                   }
               ,'uk':
                   {'short': 'магн.'
                   ,'title': 'Магнетизм'
                   }
               }
           ,'magn.tomogr.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'magn.tomogr.'
                   ,'title': 'Magnetic tomography'
                   }
               ,'ru':
                   {'short': 'магн.томогр.'
                   ,'title': 'Магнитнорезонансная томография'
                   }
               ,'de':
                   {'short': 'magn.tomogr.'
                   ,'title': 'Magnetic tomography'
                   }
               ,'es':
                   {'short': 'magn.tomogr.'
                   ,'title': 'Magnetic tomography'
                   }
               ,'uk':
                   {'short': 'томогр.'
                   ,'title': 'Томографія'
                   }
               }
           ,'magnet.image.rec.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'magnet.image.rec.'
                   ,'title': 'Magnetic image recording'
                   }
               ,'ru':
                   {'short': 'м.з.и.'
                   ,'title': 'Магнитная запись изображения'
                   }
               ,'de':
                   {'short': 'magnet.image.rec.'
                   ,'title': 'Magnetic image recording'
                   }
               ,'es':
                   {'short': 'magnet.image.rec.'
                   ,'title': 'Magnetic image recording'
                   }
               ,'uk':
                   {'short': 'магн.зобр.'
                   ,'title': 'Магнітний запис зображення'
                   }
               }
           ,'malac.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'malac.'
                   ,'title': 'Malacology'
                   }
               ,'ru':
                   {'short': 'мал.'
                   ,'title': 'Малакология'
                   }
               ,'de':
                   {'short': 'malac.'
                   ,'title': 'Malacology'
                   }
               ,'es':
                   {'short': 'malac.'
                   ,'title': 'Malacology'
                   }
               ,'uk':
                   {'short': 'малак.'
                   ,'title': 'Малакологія'
                   }
               }
           ,'malay.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'malay.'
                   ,'title': 'Malay'
                   }
               ,'ru':
                   {'short': 'малайск.'
                   ,'title': 'Малайский язык'
                   }
               ,'de':
                   {'short': 'Mala. Sp.'
                   ,'title': 'Malaiisch'
                   }
               ,'es':
                   {'short': 'malay.'
                   ,'title': 'Malay'
                   }
               ,'uk':
                   {'short': 'малайськ.'
                   ,'title': 'Малайська мова'
                   }
               }
           ,'mamal.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'mamal.'
                   ,'title': 'Mammalogy'
                   }
               ,'ru':
                   {'short': 'мам.'
                   ,'title': 'Маммология'
                   }
               ,'de':
                   {'short': 'mamal.'
                   ,'title': 'Mammalogy'
                   }
               ,'es':
                   {'short': 'mamal.'
                   ,'title': 'Mammalogy'
                   }
               ,'uk':
                   {'short': 'мамол.'
                   ,'title': 'Мамологія'
                   }
               }
           ,'mamm.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'mamm.'
                   ,'title': 'Mammals'
                   }
               ,'ru':
                   {'short': 'млек.'
                   ,'title': 'Млекопитающие'
                   }
               ,'de':
                   {'short': 'mamm.'
                   ,'title': 'Mammals'
                   }
               ,'es':
                   {'short': 'mamm.'
                   ,'title': 'Mammals'
                   }
               ,'uk':
                   {'short': 'ссавц.'
                   ,'title': 'Ссавці'
                   }
               }
           ,'manag.':
               {'is_valid': True
               ,'major_en': 'Management'
               ,'is_major': True
               ,'en':
                   {'short': 'manag.'
                   ,'title': 'Management'
                   }
               ,'ru':
                   {'short': 'менедж.'
                   ,'title': 'Менеджмент'
                   }
               ,'de':
                   {'short': 'Managem.'
                   ,'title': 'Management'
                   }
               ,'es':
                   {'short': 'manag.'
                   ,'title': 'Management'
                   }
               ,'uk':
                   {'short': 'менедж.'
                   ,'title': 'Менеджмент'
                   }
               }
           ,'manga.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'manga.'
                   ,'title': 'Manga'
                   }
               ,'ru':
                   {'short': 'манга.'
                   ,'title': 'Манга'
                   }
               ,'de':
                   {'short': 'manga.'
                   ,'title': 'Manga'
                   }
               ,'es':
                   {'short': 'manga.'
                   ,'title': 'Manga'
                   }
               ,'uk':
                   {'short': 'манґа'
                   ,'title': 'Манґа'
                   }
               }
           ,'maor.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'maor.'
                   ,'title': 'Maori'
                   }
               ,'ru':
                   {'short': 'маори.'
                   ,'title': 'Маори'
                   }
               ,'de':
                   {'short': 'maor.'
                   ,'title': 'Maori'
                   }
               ,'es':
                   {'short': 'maor.'
                   ,'title': 'Maori'
                   }
               ,'uk':
                   {'short': 'маорі'
                   ,'title': 'Маорі'
                   }
               }
           ,'mar.law':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'mar.law'
                   ,'title': 'Maritime law & Law of the Sea'
                   }
               ,'ru':
                   {'short': 'мор.пр.'
                   ,'title': 'Морское право'
                   }
               ,'de':
                   {'short': 'mar.law'
                   ,'title': 'Maritime law & Law of the Sea'
                   }
               ,'es':
                   {'short': 'mar.law'
                   ,'title': 'Maritime law & Law of the Sea'
                   }
               ,'uk':
                   {'short': 'мор.пр.'
                   ,'title': 'Морське право'
                   }
               }
           ,'market.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'market.'
                   ,'title': 'Marketing'
                   }
               ,'ru':
                   {'short': 'марк.'
                   ,'title': 'Маркетинг'
                   }
               ,'de':
                   {'short': 'market.'
                   ,'title': 'Marketing'
                   }
               ,'es':
                   {'short': 'market.'
                   ,'title': 'Marketing'
                   }
               ,'uk':
                   {'short': 'марк.'
                   ,'title': 'Маркетинг'
                   }
               }
           ,'mart.arts':
               {'is_valid': True
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': True
               ,'en':
                   {'short': 'mart.arts'
                   ,'title': 'Martial arts and combat sports'
                   }
               ,'ru':
                   {'short': 'боев.иск.'
                   ,'title': 'Боевые искусства и единоборства'
                   }
               ,'de':
                   {'short': 'Kampfsport'
                   ,'title': 'Zweikampf und Kampfkunst'
                   }
               ,'es':
                   {'short': 'artes.marc.'
                   ,'title': 'Artes marciales y deportes de combate'
                   }
               ,'uk':
                   {'short': 'бой.мист.'
                   ,'title': 'Бойові мистецтва та єдиноборства'
                   }
               }
           ,'match.prod.':
               {'is_valid': True
               ,'major_en': 'Wood, pulp and paper industries'
               ,'is_major': False
               ,'en':
                   {'short': 'match.prod.'
                   ,'title': 'Matches'
                   }
               ,'ru':
                   {'short': 'спич.'
                   ,'title': 'Спичечное производство'
                   }
               ,'de':
                   {'short': 'Str.Holz.Prod.'
                   ,'title': 'Streichholzproduktion'
                   }
               ,'es':
                   {'short': 'match.prod.'
                   ,'title': 'Matches'
                   }
               ,'uk':
                   {'short': 'сірн.'
                   ,'title': 'Сірникове виробництво'
                   }
               }
           ,'mater.sc.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'mater.sc.'
                   ,'title': 'Materials science'
                   }
               ,'ru':
                   {'short': 'материаловед.'
                   ,'title': 'Материаловедение'
                   }
               ,'de':
                   {'short': 'mater.sc.'
                   ,'title': 'Materials science'
                   }
               ,'es':
                   {'short': 'mater.sc.'
                   ,'title': 'Materials science'
                   }
               ,'uk':
                   {'short': 'матеріалозн.'
                   ,'title': 'Матеріалознавство'
                   }
               }
           ,'math.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': True
               ,'en':
                   {'short': 'math.'
                   ,'title': 'Mathematics'
                   }
               ,'ru':
                   {'short': 'мат.'
                   ,'title': 'Математика'
                   }
               ,'de':
                   {'short': 'Math.'
                   ,'title': 'Mathematik'
                   }
               ,'es':
                   {'short': 'mat.'
                   ,'title': 'Matemáticas'
                   }
               ,'uk':
                   {'short': 'мат.'
                   ,'title': 'Математика'
                   }
               }
           ,'math.anal.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'math.anal.'
                   ,'title': 'Mathematical analysis'
                   }
               ,'ru':
                   {'short': 'мат.ан.'
                   ,'title': 'Математический анализ'
                   }
               ,'de':
                   {'short': 'Math.Anal.'
                   ,'title': 'Mathematische Analyse'
                   }
               ,'es':
                   {'short': 'math.anal.'
                   ,'title': 'Mathematical analysis'
                   }
               ,'uk':
                   {'short': 'мат.ан.'
                   ,'title': 'Математичний аналіз'
                   }
               }
           ,'mean.2':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'mean.2'
                   ,'title': 'Meaning 2'
                   }
               ,'ru':
                   {'short': 'знач.2'
                   ,'title': 'Значение 2'
                   }
               ,'de':
                   {'short': 'mean.2'
                   ,'title': 'Meaning 2'
                   }
               ,'es':
                   {'short': 'mean.2'
                   ,'title': 'Meaning 2'
                   }
               ,'uk':
                   {'short': 'знач.2'
                   ,'title': 'Значення 2'
                   }
               }
           ,'meas.inst.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'meas.inst.'
                   ,'title': 'Measuring instruments'
                   }
               ,'ru':
                   {'short': 'изм.пр.'
                   ,'title': 'Измерительные приборы'
                   }
               ,'de':
                   {'short': 'meas.inst.'
                   ,'title': 'Measuring instruments'
                   }
               ,'es':
                   {'short': 'meas.inst.'
                   ,'title': 'Measuring instruments'
                   }
               ,'uk':
                   {'short': 'вим.пр.'
                   ,'title': 'Вимірювальні прилади'
                   }
               }
           ,'meat.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'meat.'
                   ,'title': 'Meat processing'
                   }
               ,'ru':
                   {'short': 'мяс.'
                   ,'title': 'Мясное производство'
                   }
               ,'de':
                   {'short': 'meat.'
                   ,'title': 'Meat processing'
                   }
               ,'es':
                   {'short': 'meat.'
                   ,'title': 'Meat processing'
                   }
               ,'uk':
                   {'short': "м'яс.вир.", 'title': 'М’ясне виробництво'
                   }
               }
           ,'mech.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'mech.'
                   ,'title': 'Mechanics'
                   }
               ,'ru':
                   {'short': 'мех.'
                   ,'title': 'Механика'
                   }
               ,'de':
                   {'short': 'Mech.'
                   ,'title': 'Mechanik'
                   }
               ,'es':
                   {'short': 'mech.'
                   ,'title': 'Mechanics'
                   }
               ,'uk':
                   {'short': 'мех.'
                   ,'title': 'Механіка'
                   }
               }
           ,'mech.eng.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'mech.eng.'
                   ,'title': 'Mechanic engineering'
                   }
               ,'ru':
                   {'short': 'маш.'
                   ,'title': 'Машиностроение'
                   }
               ,'de':
                   {'short': 'Maschinenb.'
                   ,'title': 'Maschinenbau'
                   }
               ,'es':
                   {'short': 'mech.eng.'
                   ,'title': 'Mechanic engineering'
                   }
               ,'uk':
                   {'short': 'маш.'
                   ,'title': 'Машинобудування'
                   }
               }
           ,'med.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': True
               ,'en':
                   {'short': 'med.'
                   ,'title': 'Medical'
                   }
               ,'ru':
                   {'short': 'мед.'
                   ,'title': 'Медицина'
                   }
               ,'de':
                   {'short': 'Med.'
                   ,'title': 'Medizin'
                   }
               ,'es':
                   {'short': 'med.'
                   ,'title': 'Medicina'
                   }
               ,'uk':
                   {'short': 'мед.'
                   ,'title': 'Медицина'
                   }
               }
           ,'med., alt.':
               {'is_valid': False
               ,'major_en': 'Medicine - Alternative medicine'
               ,'is_major': True
               ,'en':
                   {'short': 'med., alt.'
                   ,'title': 'Medicine - Alternative medicine'
                   }
               ,'ru':
                   {'short': 'мед., нетрад.'
                   ,'title': 'Медицина нетрадиционная (альтернативная)'
                   }
               ,'de':
                   {'short': 'med., alt.'
                   ,'title': 'Medicine - Alternative medicine'
                   }
               ,'es':
                   {'short': 'med., alt.'
                   ,'title': 'Medicine - Alternative medicine'
                   }
               ,'uk':
                   {'short': 'мед., нетрад.'
                   ,'title': 'Медицина нетрадиційна (альтернативна)'
                   }
               }
           ,'med., epid.':
               {'is_valid': False
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'med., epid.'
                   ,'title': 'Epidemiology'
                   }
               ,'ru':
                   {'short': 'мед., эпид.'
                   ,'title': 'Эпидемиология'
                   }
               ,'de':
                   {'short': 'Epidem.'
                   ,'title': 'Epidemiologie'
                   }
               ,'es':
                   {'short': 'med., epid.'
                   ,'title': 'Epidemiology'
                   }
               ,'uk':
                   {'short': 'мед., епід.'
                   ,'title': 'Епідеміологія'
                   }
               }
           ,'med.appl.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': True
               ,'en':
                   {'short': 'med.appl.'
                   ,'title': 'Medical appliances'
                   }
               ,'ru':
                   {'short': 'мед.тех.'
                   ,'title': 'Медицинская техника'
                   }
               ,'de':
                   {'short': 'Med.Tech.'
                   ,'title': 'Medizintechnik'
                   }
               ,'es':
                   {'short': 'med.appl.'
                   ,'title': 'Medical appliances'
                   }
               ,'uk':
                   {'short': 'мед.тех.'
                   ,'title': 'Медична техніка'
                   }
               }
           ,'media.':
               {'is_valid': True
               ,'major_en': 'Mass media'
               ,'is_major': True
               ,'en':
                   {'short': 'media.'
                   ,'title': 'Mass media'
                   }
               ,'ru':
                   {'short': 'СМИ.'
                   ,'title': 'Средства массовой информации'
                   }
               ,'de':
                   {'short': 'Massenmed.'
                   ,'title': 'Massenmedien'
                   }
               ,'es':
                   {'short': 'media.'
                   ,'title': 'Mass media'
                   }
               ,'uk':
                   {'short': 'ЗМІ'
                   ,'title': 'Засоби масової інформації'
                   }
               }
           ,'melior.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'melior.'
                   ,'title': 'Melioration'
                   }
               ,'ru':
                   {'short': 'мелиор.'
                   ,'title': 'Мелиорация'
                   }
               ,'de':
                   {'short': 'melior.'
                   ,'title': 'Melioration'
                   }
               ,'es':
                   {'short': 'melior.'
                   ,'title': 'Melioration'
                   }
               ,'uk':
                   {'short': 'меліор.'
                   ,'title': 'Меліорація'
                   }
               }
           ,'merch.nav.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'merch.nav.'
                   ,'title': 'Merchant navy'
                   }
               ,'ru':
                   {'short': 'торг.флот.'
                   ,'title': 'Торговый флот'
                   }
               ,'de':
                   {'short': 'merch.nav.'
                   ,'title': 'Merchant navy'
                   }
               ,'es':
                   {'short': 'merch.nav.'
                   ,'title': 'Merchant navy'
                   }
               ,'uk':
                   {'short': 'торг.флот'
                   ,'title': 'Торгівельний флот'
                   }
               }
           ,'met.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': True
               ,'en':
                   {'short': 'met.'
                   ,'title': 'Metallurgy'
                   }
               ,'ru':
                   {'short': 'мет.'
                   ,'title': 'Металлургия'
                   }
               ,'de':
                   {'short': 'Metall.'
                   ,'title': 'Metallurgie'
                   }
               ,'es':
                   {'short': 'metal.'
                   ,'title': 'Metalurgia'
                   }
               ,'uk':
                   {'short': 'мет.'
                   ,'title': 'Металургія'
                   }
               }
           ,'met.health.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': False
               ,'en':
                   {'short': 'met.health.'
                   ,'title': 'Mental health'
                   }
               ,'ru':
                   {'short': 'психогиг.'
                   ,'title': 'Психогигиена'
                   }
               ,'de':
                   {'short': 'met.health.'
                   ,'title': 'Mental health'
                   }
               ,'es':
                   {'short': 'met.health.'
                   ,'title': 'Mental health'
                   }
               ,'uk':
                   {'short': 'психогіг.'
                   ,'title': 'Психогігієна'
                   }
               }
           ,'met.sci.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'met.sci.'
                   ,'title': 'Metal science'
                   }
               ,'ru':
                   {'short': 'мтв.'
                   ,'title': 'Металловедение'
                   }
               ,'de':
                   {'short': 'Metkunde'
                   ,'title': 'Metallkunde'
                   }
               ,'es':
                   {'short': 'met.sci.'
                   ,'title': 'Metal science'
                   }
               ,'uk':
                   {'short': 'метзнав.'
                   ,'title': 'Металознавство'
                   }
               }
           ,'met.work.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'met.work.'
                   ,'title': 'Metalworking'
                   }
               ,'ru':
                   {'short': 'мет.обр.'
                   ,'title': 'Металлообработка'
                   }
               ,'de':
                   {'short': 'Met.ver.'
                   ,'title': 'Metallverarbeitung'
                   }
               ,'es':
                   {'short': 'met.work.'
                   ,'title': 'Metalworking'
                   }
               ,'uk':
                   {'short': 'мет.обр.'
                   ,'title': 'Металообробка'
                   }
               }
           ,'meteorol.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'meteorol.'
                   ,'title': 'Meteorology'
                   }
               ,'ru':
                   {'short': 'метеор.'
                   ,'title': 'Метеорология'
                   }
               ,'de':
                   {'short': 'Meteorol.'
                   ,'title': 'Meteorologie'
                   }
               ,'es':
                   {'short': 'meteorol.'
                   ,'title': 'Meteorología'
                   }
               ,'uk':
                   {'short': 'метео.'
                   ,'title': 'Метеорологія'
                   }
               }
           ,'metro':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'metro'
                   ,'title': 'Metro and rapid transit'
                   }
               ,'ru':
                   {'short': 'метро.'
                   ,'title': 'Метрополитен и скоростной транспорт'
                   }
               ,'de':
                   {'short': 'metro'
                   ,'title': 'Metro and rapid transit'
                   }
               ,'es':
                   {'short': 'metro'
                   ,'title': 'Metro and rapid transit'
                   }
               ,'uk':
                   {'short': 'метро.'
                   ,'title': 'Метрополітен і швидкісний транспорт'
                   }
               }
           ,'metrol.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'metrol.'
                   ,'title': 'Metrology'
                   }
               ,'ru':
                   {'short': 'метрол.'
                   ,'title': 'Метрология'
                   }
               ,'de':
                   {'short': 'Metrol.'
                   ,'title': 'Metrologie'
                   }
               ,'es':
                   {'short': 'metrol.'
                   ,'title': 'Metrology'
                   }
               ,'uk':
                   {'short': 'метр.'
                   ,'title': 'Метрологія'
                   }
               }
           ,'mexic.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'mexic.'
                   ,'title': 'Mexican'
                   }
               ,'ru':
                   {'short': 'мекс.'
                   ,'title': 'Мексиканское выражение'
                   }
               ,'de':
                   {'short': 'mexic.'
                   ,'title': 'Mexican'
                   }
               ,'es':
                   {'short': 'mexic.'
                   ,'title': 'Mexican'
                   }
               ,'uk':
                   {'short': 'мекс.'
                   ,'title': 'Мексиканський вираз'
                   }
               }
           ,'microbiol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'microbiol.'
                   ,'title': 'Microbiology'
                   }
               ,'ru':
                   {'short': 'микробиол.'
                   ,'title': 'Микробиология'
                   }
               ,'de':
                   {'short': 'mikrobiol.'
                   ,'title': 'Mikrobiologie'
                   }
               ,'es':
                   {'short': 'microbiol.'
                   ,'title': 'Microbiología'
                   }
               ,'uk':
                   {'short': 'мікр.'
                   ,'title': 'Мікробіологія'
                   }
               }
           ,'microel.':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'microel.'
                   ,'title': 'Microelectronics'
                   }
               ,'ru':
                   {'short': 'микроэл.'
                   ,'title': 'Микроэлектроника'
                   }
               ,'de':
                   {'short': 'Mikroel.'
                   ,'title': 'Mikroelektronik'
                   }
               ,'es':
                   {'short': 'microel.'
                   ,'title': 'Microelectronics'
                   }
               ,'uk':
                   {'short': 'мікроел.'
                   ,'title': 'Мікроелектроніка'
                   }
               }
           ,'microsc.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'microsc.'
                   ,'title': 'Microscopy'
                   }
               ,'ru':
                   {'short': 'микроск.'
                   ,'title': 'Микроскопия'
                   }
               ,'de':
                   {'short': 'microsc.'
                   ,'title': 'Microscopy'
                   }
               ,'es':
                   {'short': 'microsc.'
                   ,'title': 'Microscopy'
                   }
               ,'uk':
                   {'short': 'мікроск.'
                   ,'title': 'Мікроскопія'
                   }
               }
           ,'mid.chin.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'mid.chin.'
                   ,'title': 'Middle Chinese'
                   }
               ,'ru':
                   {'short': 'ср.кит.'
                   ,'title': 'Средне-китайский'
                   }
               ,'de':
                   {'short': 'mid.chin.'
                   ,'title': 'Middle Chinese'
                   }
               ,'es':
                   {'short': 'mid.chin.'
                   ,'title': 'Middle Chinese'
                   }
               ,'uk':
                   {'short': 'сер.кит.'
                   ,'title': 'Середньо-китайська'
                   }
               }
           ,'mil.':
               {'is_valid': True
               ,'major_en': 'Military'
               ,'is_major': True
               ,'en':
                   {'short': 'mil.'
                   ,'title': 'Military'
                   }
               ,'ru':
                   {'short': 'воен.'
                   ,'title': 'Военный термин'
                   }
               ,'de':
                   {'short': 'Mil.'
                   ,'title': 'Militär'
                   }
               ,'es':
                   {'short': 'mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'mil., AAA':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., AAA'
                   ,'title': 'Anti-air artillery'
                   }
               ,'ru':
                   {'short': 'воен., ЗА'
                   ,'title': 'Зенитная артиллерия'
                   }
               ,'de':
                   {'short': 'mil., AAA'
                   ,'title': 'Anti-air artillery'
                   }
               ,'es':
                   {'short': 'mil., AAA'
                   ,'title': 'Anti-air artillery'
                   }
               ,'uk':
                   {'short': 'військ., ЗА'
                   ,'title': 'Зенітна артилерія'
                   }
               }
           ,'mil., WMD':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., WMD'
                   ,'title': 'Weapons of mass destruction'
                   }
               ,'ru':
                   {'short': 'воен., ОМП.'
                   ,'title': 'Оружие массового поражения'
                   }
               ,'de':
                   {'short': 'mil., WMD'
                   ,'title': 'Weapons of mass destruction'
                   }
               ,'es':
                   {'short': 'mil., WMD'
                   ,'title': 'Weapons of mass destruction'
                   }
               ,'uk':
                   {'short': 'військ., ЗМУ'
                   ,'title': 'Зброя масового ураження'
                   }
               }
           ,'mil., ammo':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., ammo'
                   ,'title': 'Ammunition'
                   }
               ,'ru':
                   {'short': 'воен., боепр.'
                   ,'title': 'Боеприпасы'
                   }
               ,'de':
                   {'short': 'mil., ammo'
                   ,'title': 'Ammunition'
                   }
               ,'es':
                   {'short': 'mil., ammo'
                   ,'title': 'Ammunition'
                   }
               ,'uk':
                   {'short': 'військ., боєпр.'
                   ,'title': 'Боєприпаси'
                   }
               }
           ,'mil., arm.veh.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'ru':
                   {'short': 'воен., брон.'
                   ,'title': 'Бронетехника'
                   }
               ,'de':
                   {'short': 'mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'es':
                   {'short': 'mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'uk':
                   {'short': 'військ., брон.'
                   ,'title': 'Бронетехніка'
                   }
               }
           ,'mil., artil.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., artil.'
                   ,'title': 'Artillery'
                   }
               ,'ru':
                   {'short': 'воен., арт.'
                   ,'title': 'Артиллерия'
                   }
               ,'de':
                   {'short': 'Artil.'
                   ,'title': 'Artillerie'
                   }
               ,'es':
                   {'short': 'mil.,artill.'
                   ,'title': 'Artillería'
                   }
               ,'uk':
                   {'short': 'військ., арт.'
                   ,'title': 'Артилерія'
                   }
               }
           ,'mil., avia.':
               {'is_valid': False
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'ru':
                   {'short': 'воен., авиац.'
                   ,'title': 'Военная авиация'
                   }
               ,'de':
                   {'short': 'mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'es':
                   {'short': 'mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'uk':
                   {'short': 'військ., авіац.'
                   ,'title': 'Військова авіація'
                   }
               }
           ,'mil., grnd.forc.':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., grnd.forc.'
                   ,'title': 'Ground forces (Army)'
                   }
               ,'ru':
                   {'short': 'воен., сухоп.'
                   ,'title': 'Сухопутные силы'
                   }
               ,'de':
                   {'short': 'mil., grnd.forc.'
                   ,'title': 'Ground forces (Army)'
                   }
               ,'es':
                   {'short': 'mil., grnd.forc.'
                   ,'title': 'Ground forces (Army)'
                   }
               ,'uk':
                   {'short': 'військ., сухоп.'
                   ,'title': 'Сухопутні сили'
                   }
               }
           ,'mil., lingo':
               {'is_valid': False
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., lingo'
                   ,'title': 'Military lingo'
                   }
               ,'ru':
                   {'short': 'воен., жарг.'
                   ,'title': 'Военный жаргон'
                   }
               ,'de':
                   {'short': 'Milit. Jargon'
                   ,'title': 'Militärjargon'
                   }
               ,'es':
                   {'short': 'jerg.mil.'
                   ,'title': 'Jerga militar'
                   }
               ,'uk':
                   {'short': 'військ., жарг.'
                   ,'title': 'Військовий жаргон'
                   }
               }
           ,'mil., mil., arm.veh.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'mil., mil., arm.veh.'
                   ,'title': 'Military, Armored vehicles'
                   }
               ,'ru':
                   {'short': 'воен., воен., брон.'
                   ,'title': 'Военный термин, Бронетехника'
                   }
               ,'de':
                   {'short': 'Mil., mil., arm.veh.'
                   ,'title': 'Militär, Armored vehicles'
                   }
               ,'es':
                   {'short': 'mil., mil., arm.veh.'
                   ,'title': 'Término militar, Armored vehicles'
                   }
               ,'uk':
                   {'short': 'військ., військ., брон.'
                   ,'title': 'Військовий термін, Бронетехніка'
                   }
               }
           ,'mil., navy':
               {'is_valid': False
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'mil., navy'
                   ,'title': 'Navy'
                   }
               ,'ru':
                   {'short': 'воен., мор.'
                   ,'title': 'Военно-морской флот'
                   }
               ,'de':
                   {'short': 'mil., navy'
                   ,'title': 'Navy'
                   }
               ,'es':
                   {'short': 'mil., navy'
                   ,'title': 'Navy'
                   }
               ,'uk':
                   {'short': 'військ., мор.'
                   ,'title': 'Військово-морський флот'
                   }
               }
           ,'milk.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'milk.'
                   ,'title': 'Milk production'
                   }
               ,'ru':
                   {'short': 'мол.'
                   ,'title': 'Молочное производство'
                   }
               ,'de':
                   {'short': 'milk.'
                   ,'title': 'Milk production'
                   }
               ,'es':
                   {'short': 'milk.'
                   ,'title': 'Milk production'
                   }
               ,'uk':
                   {'short': 'мол.'
                   ,'title': 'Молочне виробництво'
                   }
               }
           ,'min.class.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'min.class.'
                   ,'title': 'Mineral classification'
                   }
               ,'ru':
                   {'short': 'класс.мин.'
                   ,'title': 'Классификация минералов'
                   }
               ,'de':
                   {'short': 'min.class.'
                   ,'title': 'Mineral classification'
                   }
               ,'es':
                   {'short': 'min.class.'
                   ,'title': 'Mineral classification'
                   }
               ,'uk':
                   {'short': 'клас.мін.'
                   ,'title': 'Класифікація мінералів'
                   }
               }
           ,'min.proc.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'min.proc.'
                   ,'title': 'Mineral processing'
                   }
               ,'ru':
                   {'short': 'обогащ.'
                   ,'title': 'Обогащение полезных ископаемых'
                   }
               ,'de':
                   {'short': 'Aufber.Bdsch.'
                   ,'title': 'Aufbereitung der Bodenschätze'
                   }
               ,'es':
                   {'short': 'min.proc.'
                   ,'title': 'Mineral processing'
                   }
               ,'uk':
                   {'short': 'збагач.'
                   ,'title': 'Збагачення корисних копалин'
                   }
               }
           ,'min.prod.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'min.prod.'
                   ,'title': 'Mineral products'
                   }
               ,'ru':
                   {'short': 'полезн.иск.'
                   ,'title': 'Полезные ископаемые'
                   }
               ,'de':
                   {'short': 'min.prod.'
                   ,'title': 'Mineral products'
                   }
               ,'es':
                   {'short': 'min.prod.'
                   ,'title': 'Mineral products'
                   }
               ,'uk':
                   {'short': 'кор.коп.'
                   ,'title': 'Корисні копалини'
                   }
               }
           ,'mine.surv.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'mine.surv.'
                   ,'title': 'Mine surveying'
                   }
               ,'ru':
                   {'short': 'маркш.'
                   ,'title': 'Маркшейдерское дело'
                   }
               ,'de':
                   {'short': 'mine.surv.'
                   ,'title': 'Mine surveying'
                   }
               ,'es':
                   {'short': 'mine.surv.'
                   ,'title': 'Mine surveying'
                   }
               ,'uk':
                   {'short': 'маркш.'
                   ,'title': 'Маркшейдерська справа'
                   }
               }
           ,'mineral.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'mineral.'
                   ,'title': 'Mineralogy'
                   }
               ,'ru':
                   {'short': 'минерал.'
                   ,'title': 'Минералогия'
                   }
               ,'de':
                   {'short': 'Mineral.'
                   ,'title': 'Mineralogie'
                   }
               ,'es':
                   {'short': 'mineral.'
                   ,'title': 'Mineralogía'
                   }
               ,'uk':
                   {'short': 'мінер.'
                   ,'title': 'Мінералогія'
                   }
               }
           ,'mining.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': True
               ,'en':
                   {'short': 'mining.'
                   ,'title': 'Mining'
                   }
               ,'ru':
                   {'short': 'горн.'
                   ,'title': 'Горное дело'
                   }
               ,'de':
                   {'short': 'Bergb.'
                   ,'title': 'Bergbau'
                   }
               ,'es':
                   {'short': 'minería'
                   ,'title': 'Minería'
                   }
               ,'uk':
                   {'short': 'гірн.'
                   ,'title': 'Гірнича справа'
                   }
               }
           ,'missil.':
               {'is_valid': True
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'missil.'
                   ,'title': 'Missiles'
                   }
               ,'ru':
                   {'short': 'ркт.'
                   ,'title': 'Ракетная техника'
                   }
               ,'de':
                   {'short': 'Rak.tech.'
                   ,'title': 'Raketentechnik'
                   }
               ,'es':
                   {'short': 'missil.'
                   ,'title': 'Missiles'
                   }
               ,'uk':
                   {'short': 'ракетн.'
                   ,'title': 'Ракетна техніка'
                   }
               }
           ,'misused':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'misused'
                   ,'title': 'Misused'
                   }
               ,'ru':
                   {'short': 'ошиб.'
                   ,'title': 'Ошибочное или неправильное'
                   }
               ,'de':
                   {'short': 'misused'
                   ,'title': 'Misused'
                   }
               ,'es':
                   {'short': 'misused'
                   ,'title': 'Misused'
                   }
               ,'uk':
                   {'short': 'помилк.'
                   ,'title': 'Помилкове або неправильне'
                   }
               }
           ,'mob.com.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'mob.com.'
                   ,'title': 'Mobile and cellular communications'
                   }
               ,'ru':
                   {'short': 'моб.св.'
                   ,'title': 'Мобильная и сотовая связь'
                   }
               ,'de':
                   {'short': 'mob.com.'
                   ,'title': 'Mobile and cellular communications'
                   }
               ,'es':
                   {'short': 'mob.com.'
                   ,'title': 'Mobile and cellular communications'
                   }
               ,'uk':
                   {'short': 'моб.зв.'
                   ,'title': "Мобільний та стільниковий зв'язок"}}, 'modern':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'modern'
                   ,'title': 'Modern use'
                   }
               ,'ru':
                   {'short': 'совр.'
                   ,'title': 'Современное выражение'
                   }
               ,'de':
                   {'short': 'Modern.'
                   ,'title': 'Moderner Ausdruck'
                   }
               ,'es':
                   {'short': 'modern'
                   ,'title': 'Modern use'
                   }
               ,'uk':
                   {'short': 'сучас.'
                   ,'title': 'Сучасний вираз'
                   }
               }
           ,'mol.biol.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'mol.biol.'
                   ,'title': 'Molecular biology'
                   }
               ,'ru':
                   {'short': 'мол.биол.'
                   ,'title': 'Молекулярная биология'
                   }
               ,'de':
                   {'short': 'mol.biol.'
                   ,'title': 'Molecular biology'
                   }
               ,'es':
                   {'short': 'mol.biol.'
                   ,'title': 'Molecular biology'
                   }
               ,'uk':
                   {'short': 'мол.біол.'
                   ,'title': 'Молекулярна біологія'
                   }
               }
           ,'moldav.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'moldav.'
                   ,'title': 'Moldavian'
                   }
               ,'ru':
                   {'short': 'молдавск.'
                   ,'title': 'Молдавский язык'
                   }
               ,'de':
                   {'short': 'Mold.'
                   ,'title': 'Moldauisch'
                   }
               ,'es':
                   {'short': 'moldav.'
                   ,'title': 'Moldavian'
                   }
               ,'uk':
                   {'short': 'молдов.'
                   ,'title': 'Молдовська мова'
                   }
               }
           ,'morph.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'morph.'
                   ,'title': 'Morphology'
                   }
               ,'ru':
                   {'short': 'морф.'
                   ,'title': 'Морфология'
                   }
               ,'de':
                   {'short': 'morph.'
                   ,'title': 'Morphology'
                   }
               ,'es':
                   {'short': 'morph.'
                   ,'title': 'Morphology'
                   }
               ,'uk':
                   {'short': 'морф.'
                   ,'title': 'Морфологія'
                   }
               }
           ,'moto.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'moto.'
                   ,'title': 'Motorcycles'
                   }
               ,'ru':
                   {'short': 'мото.'
                   ,'title': 'Мотоциклы'
                   }
               ,'de':
                   {'short': 'moto.'
                   ,'title': 'Motorcycles'
                   }
               ,'es':
                   {'short': 'moto.'
                   ,'title': 'Motorcycles'
                   }
               ,'uk':
                   {'short': 'мото.'
                   ,'title': 'Мотоцикли'
                   }
               }
           ,'mount.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'mount.'
                   ,'title': 'Mountaineering'
                   }
               ,'ru':
                   {'short': 'альп.'
                   ,'title': 'Альпинизм'
                   }
               ,'de':
                   {'short': 'mount.'
                   ,'title': 'Mountaineering'
                   }
               ,'es':
                   {'short': 'mount.'
                   ,'title': 'Mountaineering'
                   }
               ,'uk':
                   {'short': 'альп.'
                   ,'title': 'Альпінізм'
                   }
               }
           ,'multimed.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': True
               ,'en':
                   {'short': 'multimed.'
                   ,'title': 'Multimedia'
                   }
               ,'ru':
                   {'short': 'мультимед.'
                   ,'title': 'Мультимедиа'
                   }
               ,'de':
                   {'short': 'multimed.'
                   ,'title': 'Multimedia'
                   }
               ,'es':
                   {'short': 'multimed.'
                   ,'title': 'Multimedia'
                   }
               ,'uk':
                   {'short': 'мультимед.'
                   ,'title': 'Мультимедіа'
                   }
               }
           ,'mun.plan.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'mun.plan.'
                   ,'title': 'Municipal planning'
                   }
               ,'ru':
                   {'short': 'городск.застр.'
                   ,'title': 'Городская застройка'
                   }
               ,'de':
                   {'short': 'mun.plan.'
                   ,'title': 'Municipal planning'
                   }
               ,'es':
                   {'short': 'mun.plan.'
                   ,'title': 'Municipal planning'
                   }
               ,'uk':
                   {'short': 'міськ.забуд.'
                   ,'title': 'Міська забудова'
                   }
               }
           ,'mus.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'mus.'
                   ,'title': 'Music'
                   }
               ,'ru':
                   {'short': 'муз.'
                   ,'title': 'Музыка'
                   }
               ,'de':
                   {'short': 'Mus.'
                   ,'title': 'Musik'
                   }
               ,'es':
                   {'short': 'mús.'
                   ,'title': 'Música'
                   }
               ,'uk':
                   {'short': 'муз.'
                   ,'title': 'Музика'
                   }
               }
           ,'mus.instr.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'mus.instr.'
                   ,'title': 'Musical instruments'
                   }
               ,'ru':
                   {'short': 'муз.инстр.'
                   ,'title': 'Музыкальные инструменты'
                   }
               ,'de':
                   {'short': 'mus.instr.'
                   ,'title': 'Musical instruments'
                   }
               ,'es':
                   {'short': 'mus.instr.'
                   ,'title': 'Musical instruments'
                   }
               ,'uk':
                   {'short': 'муз.інстр.'
                   ,'title': 'Музичні інструменти'
                   }
               }
           ,'museum.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'museum.'
                   ,'title': 'Museums'
                   }
               ,'ru':
                   {'short': 'музей.'
                   ,'title': 'Музеи'
                   }
               ,'de':
                   {'short': 'museum.'
                   ,'title': 'Museums'
                   }
               ,'es':
                   {'short': 'museum.'
                   ,'title': 'Museums'
                   }
               ,'uk':
                   {'short': 'музейн.'
                   ,'title': 'Музеї'
                   }
               }
           ,'myth.':
               {'is_valid': True
               ,'major_en': 'Mythology'
               ,'is_major': True
               ,'en':
                   {'short': 'myth.'
                   ,'title': 'Mythology'
                   }
               ,'ru':
                   {'short': 'миф.'
                   ,'title': 'Мифология'
                   }
               ,'de':
                   {'short': 'Myth.'
                   ,'title': 'Mythologie'
                   }
               ,'es':
                   {'short': 'mitol.'
                   ,'title': 'Mitología'
                   }
               ,'uk':
                   {'short': 'міф.'
                   ,'title': 'Міфологія'
                   }
               }
           ,'myth., gr.-rom.':
               {'is_valid': False
               ,'major_en': 'Mythology'
               ,'is_major': False
               ,'en':
                   {'short': 'myth., gr.-rom.'
                   ,'title': 'Greek and Roman mythology'
                   }
               ,'ru':
                   {'short': 'миф., ант.'
                   ,'title': 'Древнегреческая и древнеримская мифология'
                   }
               ,'de':
                   {'short': 'Griech. Myth.'
                   ,'title': 'Griechische Mythologie'
                   }
               ,'es':
                   {'short': 'mitol.antig.'
                   ,'title': 'Mitología helénica y romana'
                   }
               ,'uk':
                   {'short': 'міф., ант.'
                   ,'title': 'Давньогрецька та давньоримська міфологія'
                   }
               }
           ,'myth., nors., myth.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'myth., nors., myth.'
                   ,'title': 'Norse mythology, Mythology'
                   }
               ,'ru':
                   {'short': 'миф., сканд., миф.'
                   ,'title': 'Скандинавская мифология, Мифология'
                   }
               ,'de':
                   {'short': 'myth., nors., Myth.'
                   ,'title': 'Norse mythology, Mythologie'
                   }
               ,'es':
                   {'short': 'myth., nors., mitol.'
                   ,'title': 'Norse mythology, Mitología'
                   }
               ,'uk':
                   {'short': 'міф., сканд., міф.'
                   ,'title': 'Скандинавська міфологія, Міфологія'
                   }
               }
           ,'n.amer.':
               {'is_valid': False
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'n.amer.'
                   ,'title': 'North American (USA and Canada)'
                   }
               ,'ru':
                   {'short': 'США, Кан.'
                   ,'title': 'Североамериканское выр. (США, Канада)'
                   }
               ,'de':
                   {'short': 'n.amer.'
                   ,'title': 'North American (USA and Canada)'
                   }
               ,'es':
                   {'short': 'n.amer.'
                   ,'title': 'North American (USA and Canada)'
                   }
               ,'uk':
                   {'short': 'США, Кан.'
                   ,'title': 'Північноамериканський вираз (США, Канада)'
                   }
               }
           ,'names':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': False
               ,'en':
                   {'short': 'names'
                   ,'title': 'Names and surnames'
                   }
               ,'ru':
                   {'short': 'имен.фам.'
                   ,'title': 'Имена и фамилии'
                   }
               ,'de':
                   {'short': 'names'
                   ,'title': 'Names and surnames'
                   }
               ,'es':
                   {'short': 'names'
                   ,'title': 'Names and surnames'
                   }
               ,'uk':
                   {'short': 'ім.прізв.'
                   ,'title': 'Імена й прізвища'
                   }
               }
           ,'nano':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'nano'
                   ,'title': 'Nanotechnology'
                   }
               ,'ru':
                   {'short': 'нано.'
                   ,'title': 'Нанотехнологии'
                   }
               ,'de':
                   {'short': 'nano'
                   ,'title': 'Nanotechnology'
                   }
               ,'es':
                   {'short': 'nano'
                   ,'title': 'Nanotechnology'
                   }
               ,'uk':
                   {'short': 'нано'
                   ,'title': 'Нанотехнології'
                   }
               }
           ,'narrow.film.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'narrow.film.'
                   ,'title': 'Narrow film'
                   }
               ,'ru':
                   {'short': 'узк.'
                   ,'title': 'Узкоплёночное кино'
                   }
               ,'de':
                   {'short': 'narrow.film.'
                   ,'title': 'Narrow film'
                   }
               ,'es':
                   {'short': 'narrow.film.'
                   ,'title': 'Narrow film'
                   }
               ,'uk':
                   {'short': 'вузькопл.'
                   ,'title': 'Вузькоплівкове кіно'
                   }
               }
           ,'nat.res.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': True
               ,'en':
                   {'short': 'nat.res.'
                   ,'title': 'Natural resourses and wildlife conservation'
                   }
               ,'ru':
                   {'short': 'прир.рес.'
                   ,'title': 'Природные ресурсы и охрана природы'
                   }
               ,'de':
                   {'short': 'nat.res.'
                   ,'title': 'Natural resourses and wildlife conservation'
                   }
               ,'es':
                   {'short': 'nat.res.'
                   ,'title': 'Natural resourses and wildlife conservation'
                   }
               ,'uk':
                   {'short': 'прир.рес.'
                   ,'title': 'Природні ресурси та охорона природи'
                   }
               }
           ,'nat.sc.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'nat.sc.'
                   ,'title': 'Natural sciences'
                   }
               ,'ru':
                   {'short': 'естеств.науки.'
                   ,'title': 'Естественные науки'
                   }
               ,'de':
                   {'short': 'nat.sc.'
                   ,'title': 'Natural sciences'
                   }
               ,'es':
                   {'short': 'nat.sc.'
                   ,'title': 'Natural sciences'
                   }
               ,'uk':
                   {'short': 'прир.науки'
                   ,'title': 'Природничі науки'
                   }
               }
           ,'nautic.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': True
               ,'en':
                   {'short': 'nautic.'
                   ,'title': 'Nautical'
                   }
               ,'ru':
                   {'short': 'мор.'
                   ,'title': 'Морской термин'
                   }
               ,'de':
                   {'short': 'Mar.'
                   ,'title': 'Marine'
                   }
               ,'es':
                   {'short': 'náut.'
                   ,'title': 'Náutico'
                   }
               ,'uk':
                   {'short': 'мор.'
                   ,'title': 'Морський термін'
                   }
               }
           ,'navig.':
               {'is_valid': True
               ,'major_en': 'Aviation'
               ,'is_major': False
               ,'en':
                   {'short': 'navig.'
                   ,'title': 'Navigation'
                   }
               ,'ru':
                   {'short': 'нав.'
                   ,'title': 'Навигация'
                   }
               ,'de':
                   {'short': 'Navig.'
                   ,'title': 'Navigation'
                   }
               ,'es':
                   {'short': 'navig.'
                   ,'title': 'Navigation'
                   }
               ,'uk':
                   {'short': 'нав.'
                   ,'title': 'Навігація'
                   }
               }
           ,'neol.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'neol.'
                   ,'title': 'Neologism'
                   }
               ,'ru':
                   {'short': 'неол.'
                   ,'title': 'Неологизм'
                   }
               ,'de':
                   {'short': 'Neol.'
                   ,'title': 'Neologismus'
                   }
               ,'es':
                   {'short': 'neol.'
                   ,'title': 'Neologism'
                   }
               ,'uk':
                   {'short': 'неол.'
                   ,'title': 'Неологізм'
                   }
               }
           ,'nephr.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'nephr.'
                   ,'title': 'Nephrology'
                   }
               ,'ru':
                   {'short': 'нефр.'
                   ,'title': 'Нефрология'
                   }
               ,'de':
                   {'short': 'Nephrol.'
                   ,'title': 'Nephrologie'
                   }
               ,'es':
                   {'short': 'nephr.'
                   ,'title': 'Nephrology'
                   }
               ,'uk':
                   {'short': 'нефр.'
                   ,'title': 'Нефрологія'
                   }
               }
           ,'neugoling.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'neugoling.'
                   ,'title': 'Neurolinguistics'
                   }
               ,'ru':
                   {'short': 'нейролингв.'
                   ,'title': 'Нейролингвистика'
                   }
               ,'de':
                   {'short': 'neugoling.'
                   ,'title': 'Neurolinguistics'
                   }
               ,'es':
                   {'short': 'neugoling.'
                   ,'title': 'Neurolinguistics'
                   }
               ,'uk':
                   {'short': 'нейролінгв.'
                   ,'title': 'Нейролінгвістика'
                   }
               }
           ,'neur.net.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'neur.net.'
                   ,'title': 'Neural networks'
                   }
               ,'ru':
                   {'short': 'нейр.сет.'
                   ,'title': 'Нейронные сети'
                   }
               ,'de':
                   {'short': 'Neur.Netzw.'
                   ,'title': 'Neurale Netzwerke'
                   }
               ,'es':
                   {'short': 'neur.net.'
                   ,'title': 'Neural networks'
                   }
               ,'uk':
                   {'short': 'нейр.м.'
                   ,'title': 'Нейронні мережі'
                   }
               }
           ,'neurol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'neurol.'
                   ,'title': 'Neurology'
                   }
               ,'ru':
                   {'short': 'невр.'
                   ,'title': 'Неврология'
                   }
               ,'de':
                   {'short': 'Neurol.'
                   ,'title': 'Neurologie'
                   }
               ,'es':
                   {'short': 'neurol.'
                   ,'title': 'Neurología'
                   }
               ,'uk':
                   {'short': 'невр.'
                   ,'title': 'Неврологія'
                   }
               }
           ,'neuropsychol.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': False
               ,'en':
                   {'short': 'neuropsychol.'
                   ,'title': 'Neuropsychology'
                   }
               ,'ru':
                   {'short': 'нейропсихол.'
                   ,'title': 'Нейропсихология'
                   }
               ,'de':
                   {'short': 'neuropsychol.'
                   ,'title': 'Neuropsychology'
                   }
               ,'es':
                   {'short': 'neuropsychol.'
                   ,'title': 'Neuropsychology'
                   }
               ,'uk':
                   {'short': 'нейропсихол.'
                   ,'title': 'Нейропсихологія'
                   }
               }
           ,'neurosurg.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'neurosurg.'
                   ,'title': 'Neurosurgery'
                   }
               ,'ru':
                   {'short': 'нейрохир.'
                   ,'title': 'Нейрохирургия'
                   }
               ,'de':
                   {'short': 'Neurochir.'
                   ,'title': 'Neurochirurgie'
                   }
               ,'es':
                   {'short': 'neurosurg.'
                   ,'title': 'Neurosurgery'
                   }
               ,'uk':
                   {'short': 'нейрохір.'
                   ,'title': 'Нейрохірургія'
                   }
               }
           ,'new.zeal.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'new.zeal.'
                   ,'title': 'New Zealand'
                   }
               ,'ru':
                   {'short': 'н.-зел.'
                   ,'title': 'Новозеландское выражение'
                   }
               ,'de':
                   {'short': 'neus.Ausdr.'
                   ,'title': 'neuseeländischer Ausdruck'
                   }
               ,'es':
                   {'short': 'new.zeal.'
                   ,'title': 'New Zealand'
                   }
               ,'uk':
                   {'short': 'новозел.'
                   ,'title': 'Новозеландський вираз'
                   }
               }
           ,'news':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'news'
                   ,'title': 'News style'
                   }
               ,'ru':
                   {'short': 'публиц.'
                   ,'title': 'Публицистический стиль'
                   }
               ,'de':
                   {'short': 'Presse'
                   ,'title': 'Pressestil'
                   }
               ,'es':
                   {'short': 'news'
                   ,'title': 'News style'
                   }
               ,'uk':
                   {'short': 'публіц.'
                   ,'title': 'Публіцистичний стиль'
                   }
               }
           ,'nonferr.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'nonferr.'
                   ,'title': 'Nonferrous industry'
                   }
               ,'ru':
                   {'short': 'цв.мет.'
                   ,'title': 'Цветная металлургия'
                   }
               ,'de':
                   {'short': 'N.eis.met.'
                   ,'title': 'Nichteisenmetallurgie'
                   }
               ,'es':
                   {'short': 'nonferr.'
                   ,'title': 'Nonferrous industry'
                   }
               ,'uk':
                   {'short': 'кол.мет.'
                   ,'title': 'Кольорова металургія'
                   }
               }
           ,'nonlin.opt.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'nonlin.opt.'
                   ,'title': 'Nonlinear optics'
                   }
               ,'ru':
                   {'short': 'нелин.опт.'
                   ,'title': 'Нелинейная оптика'
                   }
               ,'de':
                   {'short': 'nonlin.opt.'
                   ,'title': 'Nonlinear optics'
                   }
               ,'es':
                   {'short': 'nonlin.opt.'
                   ,'title': 'Nonlinear optics'
                   }
               ,'uk':
                   {'short': 'нелін.опт.'
                   ,'title': 'Нелінійна оптика'
                   }
               }
           ,'nonstand.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'nonstand.'
                   ,'title': 'Nonstandard'
                   }
               ,'ru':
                   {'short': 'прост.'
                   ,'title': 'Просторечие'
                   }
               ,'de':
                   {'short': 'Volksm.'
                   ,'title': 'Volksmund'
                   }
               ,'es':
                   {'short': 'nonstand.'
                   ,'title': 'Nonstandard'
                   }
               ,'uk':
                   {'short': 'прост.'
                   ,'title': 'Просторіччя'
                   }
               }
           ,'norw.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'norw.'
                   ,'title': 'Norway'
                   }
               ,'ru':
                   {'short': 'норв.'
                   ,'title': 'Норвежский язык'
                   }
               ,'de':
                   {'short': 'Norweg.'
                   ,'title': 'Norwegisch'
                   }
               ,'es':
                   {'short': 'norw.'
                   ,'title': 'Norway'
                   }
               ,'uk':
                   {'short': 'норв.'
                   ,'title': 'Норвезька мова'
                   }
               }
           ,'notar.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'notar.'
                   ,'title': 'Notarial practice'
                   }
               ,'ru':
                   {'short': 'нотар.'
                   ,'title': 'Нотариальная практика'
                   }
               ,'de':
                   {'short': 'Notar.'
                   ,'title': 'Notarielle Praxis'
                   }
               ,'es':
                   {'short': 'notar.'
                   ,'title': 'Notarial practice'
                   }
               ,'uk':
                   {'short': 'нотар.'
                   ,'title': 'Нотаріальна практика'
                   }
               }
           ,'nucl.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'nucl.chem.'
                   ,'title': 'Nuclear chemistry'
                   }
               ,'ru':
                   {'short': 'яд.хим.'
                   ,'title': 'Ядерная химия'
                   }
               ,'de':
                   {'short': 'nucl.chem.'
                   ,'title': 'Nuclear chemistry'
                   }
               ,'es':
                   {'short': 'nucl.chem.'
                   ,'title': 'Nuclear chemistry'
                   }
               ,'uk':
                   {'short': 'яд.хім.'
                   ,'title': 'Ядерна хімія'
                   }
               }
           ,'nucl.phys.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'nucl.phys.'
                   ,'title': 'Nuclear physics'
                   }
               ,'ru':
                   {'short': 'яд.физ.'
                   ,'title': 'Ядерная физика'
                   }
               ,'de':
                   {'short': 'Kernphys.'
                   ,'title': 'Kernphysik'
                   }
               ,'es':
                   {'short': 'nucl.phys.'
                   ,'title': 'Nuclear physics'
                   }
               ,'uk':
                   {'short': 'яд.фіз.'
                   ,'title': 'Ядерна фізика'
                   }
               }
           ,'nucl.pow.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'nucl.pow.'
                   ,'title': 'Nuclear and fusion power'
                   }
               ,'ru':
                   {'short': 'атом.эн.'
                   ,'title': 'Атомная и термоядерная энергетика'
                   }
               ,'de':
                   {'short': 'Kernenerg.'
                   ,'title': 'Kernenergie'
                   }
               ,'es':
                   {'short': 'nucl.pow.'
                   ,'title': 'Nuclear and fusion power'
                   }
               ,'uk':
                   {'short': 'атом.ен.'
                   ,'title': 'Атомна та термоядерна енергетика'
                   }
               }
           ,'numism.':
               {'is_valid': True
               ,'major_en': 'Collecting'
               ,'is_major': False
               ,'en':
                   {'short': 'numism.'
                   ,'title': 'Numismatics'
                   }
               ,'ru':
                   {'short': 'нумизм.'
                   ,'title': 'Нумизматика'
                   }
               ,'de':
                   {'short': 'numism.'
                   ,'title': 'Numismatics'
                   }
               ,'es':
                   {'short': 'numism.'
                   ,'title': 'Numismatics'
                   }
               ,'uk':
                   {'short': 'нумізм.'
                   ,'title': 'Нумізматика'
                   }
               }
           ,'nurs.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'nurs.'
                   ,'title': 'Nursing'
                   }
               ,'ru':
                   {'short': 'сестр.'
                   ,'title': 'Сестринское дело'
                   }
               ,'de':
                   {'short': 'nurs.'
                   ,'title': 'Nursing'
                   }
               ,'es':
                   {'short': 'nurs.'
                   ,'title': 'Nursing'
                   }
               ,'uk':
                   {'short': 'сестр.'
                   ,'title': 'Сестринська справа'
                   }
               }
           ,'obs.':
               {'is_valid': False
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'obs.'
                   ,'title': 'Obsolete / dated'
                   }
               ,'ru':
                   {'short': 'уст.'
                   ,'title': 'Устаревшее'
                   }
               ,'de':
                   {'short': 'veralt.'
                   ,'title': 'Veraltet'
                   }
               ,'es':
                   {'short': 'antic.'
                   ,'title': 'Anticuado'
                   }
               ,'uk':
                   {'short': 'застар.'
                   ,'title': 'Застаріле'
                   }
               }
           ,'obs., inform.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'obs., inform.'
                   ,'title': 'Obsolete / dated, Informal'
                   }
               ,'ru':
                   {'short': 'Gruzovik, уст.'
                   ,'title': 'Устаревшее'
                   }
               ,'de':
                   {'short': 'veralt., Umg.'
                   ,'title': 'Veraltet, Umgangssprache'
                   }
               ,'es':
                   {'short': 'Gruzovik, antic.'
                   ,'title': 'Anticuado'
                   }
               ,'uk':
                   {'short': 'Gruzovik, застар.'
                   ,'title': 'Застаріле'
                   }
               }
           ,'obs., ironic.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'obs., ironic.'
                   ,'title': 'Obsolete / dated, Ironical'
                   }
               ,'ru':
                   {'short': 'Gruzovik, ритор.'
                   ,'title': 'Риторика'
                   }
               ,'de':
                   {'short': 'veralt., Iron.'
                   ,'title': 'Veraltet, Ironie'
                   }
               ,'es':
                   {'short': 'Gruzovik, retór.'
                   ,'title': 'Retórica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ритор.'
                   ,'title': 'Риторика'
                   }
               }
           ,'obs., mil.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'obs., mil.'
                   ,'title': 'Obsolete / dated, Military'
                   }
               ,'ru':
                   {'short': 'Gruzovik, воен.'
                   ,'title': 'Военный термин'
                   }
               ,'de':
                   {'short': 'veralt., Mil.'
                   ,'title': 'Veraltet, Militär'
                   }
               ,'es':
                   {'short': 'Gruzovik, mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'obst.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'obst.'
                   ,'title': 'Obstetrics'
                   }
               ,'ru':
                   {'short': 'акуш.'
                   ,'title': 'Акушерство'
                   }
               ,'de':
                   {'short': 'geburt.'
                   ,'title': 'Geburtshilfe'
                   }
               ,'es':
                   {'short': 'obstetr.'
                   ,'title': 'Obstetricia'
                   }
               ,'uk':
                   {'short': 'акуш.'
                   ,'title': 'Акушерство'
                   }
               }
           ,'ocean.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'ru':
                   {'short': 'океан.'
                   ,'title': 'Океанология (океанография)'
                   }
               ,'de':
                   {'short': 'Ozeanogr.'
                   ,'title': 'Ozeanographie'
                   }
               ,'es':
                   {'short': 'ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'uk':
                   {'short': 'океан.'
                   ,'title': 'Океанологія (океанографія)'
                   }
               }
           ,'offic.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'offic.'
                   ,'title': 'Officialese'
                   }
               ,'ru':
                   {'short': 'канц.'
                   ,'title': 'Канцеляризм'
                   }
               ,'de':
                   {'short': 'Amt.Sp.'
                   ,'title': 'Amtssprache'
                   }
               ,'es':
                   {'short': 'offic.'
                   ,'title': 'Officialese'
                   }
               ,'uk':
                   {'short': 'канц.'
                   ,'title': 'Канцеляризм'
                   }
               }
           ,'office.equip.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'office.equip.'
                   ,'title': 'Office equipment'
                   }
               ,'ru':
                   {'short': 'орг.тех.'
                   ,'title': 'Оргтехника'
                   }
               ,'de':
                   {'short': 'office.equip.'
                   ,'title': 'Office equipment'
                   }
               ,'es':
                   {'short': 'office.equip.'
                   ,'title': 'Office equipment'
                   }
               ,'uk':
                   {'short': 'орг.тех.'
                   ,'title': 'Оргтехніка'
                   }
               }
           ,'offsh.comp.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'offsh.comp.'
                   ,'title': 'Offshore companies'
                   }
               ,'ru':
                   {'short': 'оффш.'
                   ,'title': 'Оффшоры'
                   }
               ,'de':
                   {'short': 'offsh.comp.'
                   ,'title': 'Offshore companies'
                   }
               ,'es':
                   {'short': 'offsh.comp.'
                   ,'title': 'Offshore companies'
                   }
               ,'uk':
                   {'short': 'офш.'
                   ,'title': 'Офшори'
                   }
               }
           ,'oil':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'oil'
                   ,'title': 'Oil / petroleum'
                   }
               ,'ru':
                   {'short': 'нефт.'
                   ,'title': 'Нефть'
                   }
               ,'de':
                   {'short': 'E.öl.'
                   ,'title': 'Erdöl'
                   }
               ,'es':
                   {'short': 'petról.'
                   ,'title': 'Petróleo'
                   }
               ,'uk':
                   {'short': 'нафт.'
                   ,'title': 'Нафта'
                   }
               }
           ,'oil.lubr.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'oil.lubr.'
                   ,'title': 'Oils and lubricants'
                   }
               ,'ru':
                   {'short': 'ГСМ.'
                   ,'title': 'Горюче-смазочные материалы'
                   }
               ,'de':
                   {'short': 'oil.lubr.'
                   ,'title': 'Oils and lubricants'
                   }
               ,'es':
                   {'short': 'oil.lubr.'
                   ,'title': 'Oils and lubricants'
                   }
               ,'uk':
                   {'short': 'пал.-маст.'
                   ,'title': 'Паливно-мастильні матеріали'
                   }
               }
           ,'oil.proc.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'oil.proc.'
                   ,'title': 'Oil processing plants'
                   }
               ,'ru':
                   {'short': 'нпз.'
                   ,'title': 'Нефтеперерабатывающие заводы'
                   }
               ,'de':
                   {'short': 'oil.proc.'
                   ,'title': 'Oil processing plants'
                   }
               ,'es':
                   {'short': 'oil.proc.'
                   ,'title': 'Oil processing plants'
                   }
               ,'uk':
                   {'short': 'НПЗ'
                   ,'title': 'Нафтопереробні заводи'
                   }
               }
           ,'old.fash.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'old.fash.'
                   ,'title': 'Old-fashioned'
                   }
               ,'ru':
                   {'short': 'старом.'
                   ,'title': 'Старомодное (выходит из употребления)'
                   }
               ,'de':
                   {'short': 'Altmod.'
                   ,'title': 'Altmodisch'
                   }
               ,'es':
                   {'short': 'old.fash.'
                   ,'title': 'Old-fashioned'
                   }
               ,'uk':
                   {'short': 'старом.'
                   ,'title': 'Старомодне (виходить з вжитку)'
                   }
               }
           ,'old.orth.':
               {'is_valid': True
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'old.orth.'
                   ,'title': 'Old orthography'
                   }
               ,'ru':
                   {'short': 'стар.орф.'
                   ,'title': 'Старая орфография'
                   }
               ,'de':
                   {'short': 'alt.R.schr.'
                   ,'title': 'Alte Rechtschreibung'
                   }
               ,'es':
                   {'short': 'old.orth.'
                   ,'title': 'Old orthography'
                   }
               ,'uk':
                   {'short': 'стар.орф.'
                   ,'title': 'Стара орфографія'
                   }
               }
           ,'oncol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'oncol.'
                   ,'title': 'Oncology'
                   }
               ,'ru':
                   {'short': 'онк.'
                   ,'title': 'Онкология'
                   }
               ,'de':
                   {'short': 'Onkol.'
                   ,'title': 'Onkologie'
                   }
               ,'es':
                   {'short': 'oncol.'
                   ,'title': 'Oncology'
                   }
               ,'uk':
                   {'short': 'онк.'
                   ,'title': 'Онкологія'
                   }
               }
           ,'op.hearth.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'op.hearth.'
                   ,'title': 'Open-hearth process'
                   }
               ,'ru':
                   {'short': 'март.'
                   ,'title': 'Мартеновское производство'
                   }
               ,'de':
                   {'short': 'S-M-Betr.'
                   ,'title': 'Siemens-Martin-Betrieb'
                   }
               ,'es':
                   {'short': 'op.hearth.'
                   ,'title': 'Open-hearth process'
                   }
               ,'uk':
                   {'short': 'мартен.'
                   ,'title': 'Мартенівське виробництво'
                   }
               }
           ,'op.syst.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'op.syst.'
                   ,'title': 'Operation systems'
                   }
               ,'ru':
                   {'short': 'оп.сист.'
                   ,'title': 'Операционные системы'
                   }
               ,'de':
                   {'short': 'Betr.Syst.'
                   ,'title': 'Betriebssysteme'
                   }
               ,'es':
                   {'short': 'op.syst.'
                   ,'title': 'Operation systems'
                   }
               ,'uk':
                   {'short': 'оп.сист.'
                   ,'title': 'Операційні системи'
                   }
               }
           ,'ophtalm.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'ophtalm.'
                   ,'title': 'Ophthalmology'
                   }
               ,'ru':
                   {'short': 'офт.'
                   ,'title': 'Офтальмология'
                   }
               ,'de':
                   {'short': 'augenh.'
                   ,'title': 'Augenheilkunde'
                   }
               ,'es':
                   {'short': 'oftalm.'
                   ,'title': 'Oftalmología'
                   }
               ,'uk':
                   {'short': 'офт.'
                   ,'title': 'Офтальмологія'
                   }
               }
           ,'opt.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'opt.'
                   ,'title': 'Optics (branch of physics)'
                   }
               ,'ru':
                   {'short': 'опт.'
                   ,'title': 'Оптика (раздел физики)'
                   }
               ,'de':
                   {'short': 'Opt.'
                   ,'title': 'Optik'
                   }
               ,'es':
                   {'short': 'ópt.'
                   ,'title': 'Óptica (rama de la física)'
                   }
               ,'uk':
                   {'short': 'опт.'
                   ,'title': 'Оптика (розділ фізики)'
                   }
               }
           ,'optometr.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'optometr.'
                   ,'title': 'Optometry'
                   }
               ,'ru':
                   {'short': 'оптометр.'
                   ,'title': 'Оптометрия'
                   }
               ,'de':
                   {'short': 'optometr.'
                   ,'title': 'Optometry'
                   }
               ,'es':
                   {'short': 'optometr.'
                   ,'title': 'Optometry'
                   }
               ,'uk':
                   {'short': 'оптометр.'
                   ,'title': 'Оптометрія'
                   }
               }
           ,'ore.form.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'ore.form.'
                   ,'title': 'Ore formation'
                   }
               ,'ru':
                   {'short': 'рудн.'
                   ,'title': 'Рудные месторождения'
                   }
               ,'de':
                   {'short': 'Erzvorkom.'
                   ,'title': 'Erzvorkommen'
                   }
               ,'es':
                   {'short': 'ore.form.'
                   ,'title': 'Ore formation'
                   }
               ,'uk':
                   {'short': 'рудн.'
                   ,'title': 'Рудні родовища'
                   }
               }
           ,'org.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'org.chem.'
                   ,'title': 'Organic chemistry'
                   }
               ,'ru':
                   {'short': 'орг.хим.'
                   ,'title': 'Органическая химия'
                   }
               ,'de':
                   {'short': 'org.chem.'
                   ,'title': 'Organic chemistry'
                   }
               ,'es':
                   {'short': 'org.chem.'
                   ,'title': 'Organic chemistry'
                   }
               ,'uk':
                   {'short': 'орг.хім.'
                   ,'title': 'Органічна хімія'
                   }
               }
           ,'org.crime.':
               {'is_valid': True
               ,'major_en': 'Law enforcement'
               ,'is_major': False
               ,'en':
                   {'short': 'org.crime.'
                   ,'title': 'Organized crime'
                   }
               ,'ru':
                   {'short': 'преступн.'
                   ,'title': 'Преступность'
                   }
               ,'de':
                   {'short': 'org.crime.'
                   ,'title': 'Organized crime'
                   }
               ,'es':
                   {'short': 'org.crime.'
                   ,'title': 'Organized crime'
                   }
               ,'uk':
                   {'short': 'злочин.'
                   ,'title': 'Злочинність'
                   }
               }
           ,'org.name.':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': False
               ,'en':
                   {'short': 'org.name.'
                   ,'title': 'Name of organization'
                   }
               ,'ru':
                   {'short': 'назв.орг.'
                   ,'title': 'Название организации'
                   }
               ,'de':
                   {'short': 'org.name.'
                   ,'title': 'Name of organization'
                   }
               ,'es':
                   {'short': 'org.name.'
                   ,'title': 'Name of organization'
                   }
               ,'uk':
                   {'short': 'назв.орг.'
                   ,'title': 'Назва організації'
                   }
               }
           ,'orient.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'orient.'
                   ,'title': 'Oriental'
                   }
               ,'ru':
                   {'short': 'восточн.'
                   ,'title': 'Восточное выражение'
                   }
               ,'de':
                   {'short': 'orient.'
                   ,'title': 'Oriental'
                   }
               ,'es':
                   {'short': 'orient.'
                   ,'title': 'Oriental'
                   }
               ,'uk':
                   {'short': 'східн.'
                   ,'title': 'Східний вираз'
                   }
               }
           ,'orthop.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'orthop.'
                   ,'title': 'Orthopedics'
                   }
               ,'ru':
                   {'short': 'ортоп.'
                   ,'title': 'Ортопедия'
                   }
               ,'de':
                   {'short': 'Orthop.'
                   ,'title': 'Orthopädie'
                   }
               ,'es':
                   {'short': 'orthop.'
                   ,'title': 'Orthopedics'
                   }
               ,'uk':
                   {'short': 'ортоп.'
                   ,'title': 'Ортопедія'
                   }
               }
           ,'pack.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'pack.'
                   ,'title': 'Packaging'
                   }
               ,'ru':
                   {'short': 'упак.'
                   ,'title': 'Упаковка'
                   }
               ,'de':
                   {'short': 'Verpack.'
                   ,'title': 'Verpackung'
                   }
               ,'es':
                   {'short': 'pack.'
                   ,'title': 'Packaging'
                   }
               ,'uk':
                   {'short': 'пак.'
                   ,'title': 'Пакування'
                   }
               }
           ,'paint.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'paint.'
                   ,'title': 'Painting'
                   }
               ,'ru':
                   {'short': 'живоп.'
                   ,'title': 'Живопись'
                   }
               ,'de':
                   {'short': 'Mal.'
                   ,'title': 'Malerei'
                   }
               ,'es':
                   {'short': 'pint.'
                   ,'title': 'Pintura'
                   }
               ,'uk':
                   {'short': 'живоп.'
                   ,'title': 'Живопис'
                   }
               }
           ,'paint.varn.':
               {'is_valid': False
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'paint.varn.'
                   ,'title': 'Paint, varnish and lacquer'
                   }
               ,'ru':
                   {'short': 'ЛКМ.'
                   ,'title': 'Лакокрасочные материалы'
                   }
               ,'de':
                   {'short': 'paint.varn.'
                   ,'title': 'Paint, varnish and lacquer'
                   }
               ,'es':
                   {'short': 'paint.varn.'
                   ,'title': 'Paint, varnish and lacquer'
                   }
               ,'uk':
                   {'short': 'ЛФМ'
                   ,'title': 'Лакофарбові матеріали'
                   }
               }
           ,'paint.w.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'paint.w.'
                   ,'title': 'Paint work'
                   }
               ,'ru':
                   {'short': 'маляр.'
                   ,'title': 'Малярное дело'
                   }
               ,'de':
                   {'short': 'Malerarb.'
                   ,'title': 'Malerarbeit'
                   }
               ,'es':
                   {'short': 'paint.w.'
                   ,'title': 'Paint work'
                   }
               ,'uk':
                   {'short': 'маляр.'
                   ,'title': 'Малярська справа'
                   }
               }
           ,'pal.bot.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'pal.bot.'
                   ,'title': 'Paleobotany'
                   }
               ,'ru':
                   {'short': 'пбот.'
                   ,'title': 'Палеоботаника'
                   }
               ,'de':
                   {'short': 'pal.bot.'
                   ,'title': 'Paleobotany'
                   }
               ,'es':
                   {'short': 'pal.bot.'
                   ,'title': 'Paleobotany'
                   }
               ,'uk':
                   {'short': 'палеобот.'
                   ,'title': 'Палеоботаніка'
                   }
               }
           ,'paleogr.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'paleogr.'
                   ,'title': 'Palaeography'
                   }
               ,'ru':
                   {'short': 'палеогр.'
                   ,'title': 'Палеография'
                   }
               ,'de':
                   {'short': 'paleogr.'
                   ,'title': 'Palaeography'
                   }
               ,'es':
                   {'short': 'paleogr.'
                   ,'title': 'Palaeography'
                   }
               ,'uk':
                   {'short': 'палеогр.'
                   ,'title': 'Палеографія'
                   }
               }
           ,'paleont.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'paleont.'
                   ,'title': 'Paleontology'
                   }
               ,'ru':
                   {'short': 'палеонт.'
                   ,'title': 'Палеонтология'
                   }
               ,'de':
                   {'short': 'Paläontol.'
                   ,'title': 'Paläontologie'
                   }
               ,'es':
                   {'short': 'paleont.'
                   ,'title': 'Paleontology'
                   }
               ,'uk':
                   {'short': 'палеонт.'
                   ,'title': 'Палеонтологія'
                   }
               }
           ,'paleozool.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'paleozool.'
                   ,'title': 'Paleozoology'
                   }
               ,'ru':
                   {'short': 'палеозоол.'
                   ,'title': 'Палеозоология'
                   }
               ,'de':
                   {'short': 'paleozool.'
                   ,'title': 'Paleozoology'
                   }
               ,'es':
                   {'short': 'paleozool.'
                   ,'title': 'Paleozoology'
                   }
               ,'uk':
                   {'short': 'палеозоол.'
                   ,'title': 'Палеозоологія'
                   }
               }
           ,'palyn.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'palyn.'
                   ,'title': 'Palynology'
                   }
               ,'ru':
                   {'short': 'палин.'
                   ,'title': 'Палинология'
                   }
               ,'de':
                   {'short': 'palyn.'
                   ,'title': 'Palynology'
                   }
               ,'es':
                   {'short': 'palyn.'
                   ,'title': 'Palynology'
                   }
               ,'uk':
                   {'short': 'палін.'
                   ,'title': 'Палінологія'
                   }
               }
           ,'parapsych.':
               {'is_valid': True
               ,'major_en': 'Parasciences'
               ,'is_major': False
               ,'en':
                   {'short': 'parapsych.'
                   ,'title': 'Parapsychology'
                   }
               ,'ru':
                   {'short': 'парапсихол.'
                   ,'title': 'Парапсихология'
                   }
               ,'de':
                   {'short': 'parapsych.'
                   ,'title': 'Parapsychology'
                   }
               ,'es':
                   {'short': 'parapsych.'
                   ,'title': 'Parapsychology'
                   }
               ,'uk':
                   {'short': 'парапсихол.'
                   ,'title': 'Парапсихологія'
                   }
               }
           ,'parasitol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'parasitol.'
                   ,'title': 'Parasitology'
                   }
               ,'ru':
                   {'short': 'паразитол.'
                   ,'title': 'Паразитология'
                   }
               ,'de':
                   {'short': 'Parasitol.'
                   ,'title': 'Parasitologie'
                   }
               ,'es':
                   {'short': 'parasit.'
                   ,'title': 'Parasitología'
                   }
               ,'uk':
                   {'short': 'параз.'
                   ,'title': 'Паразитологія'
                   }
               }
           ,'patents.':
               {'is_valid': False
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'patents.'
                   ,'title': 'Patents'
                   }
               ,'ru':
                   {'short': 'юр., пат.'
                   ,'title': 'Патенты'
                   }
               ,'de':
                   {'short': 'Patent.'
                   ,'title': 'Patente'
                   }
               ,'es':
                   {'short': 'patents.'
                   ,'title': 'Patents'
                   }
               ,'uk':
                   {'short': 'юр., пат.'
                   ,'title': 'Патенти'
                   }
               }
           ,'pathol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'pathol.'
                   ,'title': 'Pathology'
                   }
               ,'ru':
                   {'short': 'патол.'
                   ,'title': 'Патология'
                   }
               ,'de':
                   {'short': 'Pathol.'
                   ,'title': 'Pathologie'
                   }
               ,'es':
                   {'short': 'patol.'
                   ,'title': 'Patología'
                   }
               ,'uk':
                   {'short': 'патол.'
                   ,'title': 'Патологія'
                   }
               }
           ,'pedag.':
               {'is_valid': True
               ,'major_en': 'Education'
               ,'is_major': False
               ,'en':
                   {'short': 'pedag.'
                   ,'title': 'Pedagogics'
                   }
               ,'ru':
                   {'short': 'педаг.'
                   ,'title': 'Педагогика'
                   }
               ,'de':
                   {'short': 'pedag.'
                   ,'title': 'Pedagogics'
                   }
               ,'es':
                   {'short': 'pedag.'
                   ,'title': 'Pedagogics'
                   }
               ,'uk':
                   {'short': 'педаг.'
                   ,'title': 'Педагогіка'
                   }
               }
           ,'pediatr.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'pediatr.'
                   ,'title': 'Pediatrics'
                   }
               ,'ru':
                   {'short': 'пед.'
                   ,'title': 'Педиатрия'
                   }
               ,'de':
                   {'short': 'Pädiatr.'
                   ,'title': 'Pädiatrie'
                   }
               ,'es':
                   {'short': 'pediatr.'
                   ,'title': 'Pediatrics'
                   }
               ,'uk':
                   {'short': 'педіатр.'
                   ,'title': 'Педіатрія'
                   }
               }
           ,'pejor.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'pejor.'
                   ,'title': 'Pejorative'
                   }
               ,'ru':
                   {'short': 'унич.'
                   ,'title': 'Уничижительно'
                   }
               ,'de':
                   {'short': 'pejor.'
                   ,'title': 'Pejorative'
                   }
               ,'es':
                   {'short': 'pejor.'
                   ,'title': 'Pejorative'
                   }
               ,'uk':
                   {'short': 'приниз.'
                   ,'title': 'Принизливо'
                   }
               }
           ,'penitent.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'penitent.'
                   ,'title': 'Penitentiary system'
                   }
               ,'ru':
                   {'short': 'пенитенц.'
                   ,'title': 'Пенитенциарная система'
                   }
               ,'de':
                   {'short': 'penitent.'
                   ,'title': 'Penitentiary system'
                   }
               ,'es':
                   {'short': 'penitent.'
                   ,'title': 'Penitentiary system'
                   }
               ,'uk':
                   {'short': 'пенітенц.'
                   ,'title': 'Пенітенціарна система'
                   }
               }
           ,'perf.':
               {'is_valid': True
               ,'major_en': 'Wellness'
               ,'is_major': False
               ,'en':
                   {'short': 'perf.'
                   ,'title': 'Perfume'
                   }
               ,'ru':
                   {'short': 'парф.'
                   ,'title': 'Парфюмерия'
                   }
               ,'de':
                   {'short': 'Parfüm.'
                   ,'title': 'Parfümerie'
                   }
               ,'es':
                   {'short': 'perf.'
                   ,'title': 'Perfume'
                   }
               ,'uk':
                   {'short': 'парф.'
                   ,'title': 'Парфумерія'
                   }
               }
           ,'permits.':
               {'is_valid': True
               ,'major_en': 'Occupational health & safety'
               ,'is_major': False
               ,'en':
                   {'short': 'permits.'
                   ,'title': 'Permit to work system'
                   }
               ,'ru':
                   {'short': 'наряд-допуск.'
                   ,'title': 'Система наряд-допусков'
                   }
               ,'de':
                   {'short': 'permits.'
                   ,'title': 'Permit to work system'
                   }
               ,'es':
                   {'short': 'permits.'
                   ,'title': 'Permit to work system'
                   }
               ,'uk':
                   {'short': 'наряд-доп.'
                   ,'title': 'Система наряд-допусків'
                   }
               }
           ,'pers.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'pers.'
                   ,'title': 'Persian'
                   }
               ,'ru':
                   {'short': 'перс.'
                   ,'title': 'Персидский язык (фарси)'
                   }
               ,'de':
                   {'short': 'pers.'
                   ,'title': 'Persische Sprache'
                   }
               ,'es':
                   {'short': 'pers.'
                   ,'title': 'Persa (farsi)'
                   }
               ,'uk':
                   {'short': 'перськ.'
                   ,'title': 'Перська мова'
                   }
               }
           ,'pest.contr.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'pest.contr.'
                   ,'title': 'Pest control'
                   }
               ,'ru':
                   {'short': 'вред.'
                   ,'title': 'Борьба с вредителями'
                   }
               ,'de':
                   {'short': 'Schädl.bek.'
                   ,'title': 'Schädlingsbekämpfung'
                   }
               ,'es':
                   {'short': 'pest.contr.'
                   ,'title': 'Pest control'
                   }
               ,'uk':
                   {'short': 'шкідн.'
                   ,'title': 'Боротьба з шкідниками'
                   }
               }
           ,'pet.':
               {'is_valid': True
               ,'major_en': 'Companion animals'
               ,'is_major': False
               ,'en':
                   {'short': 'pet.'
                   ,'title': 'Pets'
                   }
               ,'ru':
                   {'short': 'дом.жив.'
                   ,'title': 'Домашние животные'
                   }
               ,'de':
                   {'short': 'pet.'
                   ,'title': 'Pets'
                   }
               ,'es':
                   {'short': 'pet.'
                   ,'title': 'Pets'
                   }
               ,'uk':
                   {'short': 'дом.твар.'
                   ,'title': 'Домашні тварини'
                   }
               }
           ,'petrogr.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'petrogr.'
                   ,'title': 'Petrography'
                   }
               ,'ru':
                   {'short': 'петр.'
                   ,'title': 'Петрография'
                   }
               ,'de':
                   {'short': 'Petrograph.'
                   ,'title': 'Petrographie'
                   }
               ,'es':
                   {'short': 'petrogr.'
                   ,'title': 'Petrography'
                   }
               ,'uk':
                   {'short': 'петр.'
                   ,'title': 'Петрографія'
                   }
               }
           ,'phaler.':
               {'is_valid': True
               ,'major_en': 'Collecting'
               ,'is_major': False
               ,'en':
                   {'short': 'phaler.'
                   ,'title': 'Phaleristics'
                   }
               ,'ru':
                   {'short': 'фалер.'
                   ,'title': 'Фалеристика'
                   }
               ,'de':
                   {'short': 'phaler.'
                   ,'title': 'Phaleristics'
                   }
               ,'es':
                   {'short': 'phaler.'
                   ,'title': 'Phaleristics'
                   }
               ,'uk':
                   {'short': 'фалер.'
                   ,'title': 'Фалеристика'
                   }
               }
           ,'pharm.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'pharm.'
                   ,'title': 'Pharmacology'
                   }
               ,'ru':
                   {'short': 'фарм.'
                   ,'title': 'Фармакология'
                   }
               ,'de':
                   {'short': 'Pharm.'
                   ,'title': 'Pharmakologie'
                   }
               ,'es':
                   {'short': 'farm.'
                   ,'title': 'Farmacología'
                   }
               ,'uk':
                   {'short': 'фарм.'
                   ,'title': 'Фармакологія'
                   }
               }
           ,'pharmac.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'pharmac.'
                   ,'title': 'Pharmacy'
                   }
               ,'ru':
                   {'short': 'фармац.'
                   ,'title': 'Фармация'
                   }
               ,'de':
                   {'short': 'pharmac.'
                   ,'title': 'Pharmacy'
                   }
               ,'es':
                   {'short': 'pharmac.'
                   ,'title': 'Pharmacy'
                   }
               ,'uk':
                   {'short': 'фармац.'
                   ,'title': 'Фармація'
                   }
               }
           ,'philat.':
               {'is_valid': True
               ,'major_en': 'Collecting'
               ,'is_major': False
               ,'en':
                   {'short': 'philat.'
                   ,'title': 'Philately / stamp collecting'
                   }
               ,'ru':
                   {'short': 'филател.'
                   ,'title': 'Филателия'
                   }
               ,'de':
                   {'short': 'Philat.'
                   ,'title': 'Philatelie'
                   }
               ,'es':
                   {'short': 'philat.'
                   ,'title': 'Philately / stamp collecting'
                   }
               ,'uk':
                   {'short': 'філат.'
                   ,'title': 'Філателія'
                   }
               }
           ,'philos.':
               {'is_valid': True
               ,'major_en': 'Philosophy'
               ,'is_major': True
               ,'en':
                   {'short': 'philos.'
                   ,'title': 'Philosophy'
                   }
               ,'ru':
                   {'short': 'филос.'
                   ,'title': 'Философия'
                   }
               ,'de':
                   {'short': 'Philos.'
                   ,'title': 'Philosophie'
                   }
               ,'es':
                   {'short': 'filos.'
                   ,'title': 'Filosofía'
                   }
               ,'uk':
                   {'short': 'філос.'
                   ,'title': 'Філософія'
                   }
               }
           ,'phonol.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'phonol.'
                   ,'title': 'Phonology'
                   }
               ,'ru':
                   {'short': 'фонол.'
                   ,'title': 'Фонология'
                   }
               ,'de':
                   {'short': 'phonol.'
                   ,'title': 'Phonology'
                   }
               ,'es':
                   {'short': 'phonol.'
                   ,'title': 'Phonology'
                   }
               ,'uk':
                   {'short': 'фонол.'
                   ,'title': 'Фонологія'
                   }
               }
           ,'photo.':
               {'is_valid': True
               ,'major_en': 'Photography'
               ,'is_major': True
               ,'en':
                   {'short': 'photo.'
                   ,'title': 'Photography'
                   }
               ,'ru':
                   {'short': 'фото.'
                   ,'title': 'Фотография'
                   }
               ,'de':
                   {'short': 'Foto.'
                   ,'title': 'Foto'
                   }
               ,'es':
                   {'short': 'fotogr.'
                   ,'title': 'Fotografía'
                   }
               ,'uk':
                   {'short': 'фото'
                   ,'title': 'Фотографія'
                   }
               }
           ,'photo.sound.rec.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'photo.sound.rec.'
                   ,'title': 'Photographical sound recording'
                   }
               ,'ru':
                   {'short': 'зв.фот.'
                   ,'title': 'Фотографическая запись звука'
                   }
               ,'de':
                   {'short': 'photo.sound.rec.'
                   ,'title': 'Photographical sound recording'
                   }
               ,'es':
                   {'short': 'photo.sound.rec.'
                   ,'title': 'Photographical sound recording'
                   }
               ,'uk':
                   {'short': 'фот.звукоз.'
                   ,'title': 'Фотографічний звукозапис'
                   }
               }
           ,'photometr.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'photometr.'
                   ,'title': 'Photometry'
                   }
               ,'ru':
                   {'short': 'фотометр.'
                   ,'title': 'Фотометрия'
                   }
               ,'de':
                   {'short': 'photometr.'
                   ,'title': 'Photometry'
                   }
               ,'es':
                   {'short': 'photometr.'
                   ,'title': 'Photometry'
                   }
               ,'uk':
                   {'short': 'фотометр.'
                   ,'title': 'Фотометрія'
                   }
               }
           ,'phras.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'phras.'
                   ,'title': 'Phraseological unit'
                   }
               ,'ru':
                   {'short': 'фраз.'
                   ,'title': 'Фразеологизм'
                   }
               ,'de':
                   {'short': 'phras.'
                   ,'title': 'Phraseological unit'
                   }
               ,'es':
                   {'short': 'phras.'
                   ,'title': 'Phraseological unit'
                   }
               ,'uk':
                   {'short': 'фраз.'
                   ,'title': 'Фразеологізм'
                   }
               }
           ,'phys.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': True
               ,'en':
                   {'short': 'phys.'
                   ,'title': 'Physics'
                   }
               ,'ru':
                   {'short': 'физ.'
                   ,'title': 'Физика'
                   }
               ,'de':
                   {'short': 'Phys.'
                   ,'title': 'Physik'
                   }
               ,'es':
                   {'short': 'fís.'
                   ,'title': 'Física'
                   }
               ,'uk':
                   {'short': 'фіз.'
                   ,'title': 'Фізика'
                   }
               }
           ,'phys.chem.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'phys.chem.'
                   ,'title': 'Physical chemistry'
                   }
               ,'ru':
                   {'short': 'физ.-хим.'
                   ,'title': 'Физическая химия'
                   }
               ,'de':
                   {'short': 'phys.chem.'
                   ,'title': 'Physical chemistry'
                   }
               ,'es':
                   {'short': 'phys.chem.'
                   ,'title': 'Physical chemistry'
                   }
               ,'uk':
                   {'short': 'фіз.-хім.'
                   ,'title': 'Фізична хімія'
                   }
               }
           ,'physiol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'physiol.'
                   ,'title': 'Physiology'
                   }
               ,'ru':
                   {'short': 'физиол.'
                   ,'title': 'Физиология'
                   }
               ,'de':
                   {'short': 'Physiol.'
                   ,'title': 'Physiologie'
                   }
               ,'es':
                   {'short': 'fisiol.'
                   ,'title': 'Fisiología'
                   }
               ,'uk':
                   {'short': 'фізіол.'
                   ,'title': 'Фізіологія'
                   }
               }
           ,'physioth.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'physioth.'
                   ,'title': 'Physiotherapy'
                   }
               ,'ru':
                   {'short': 'физиотер.'
                   ,'title': 'Физиотерапия'
                   }
               ,'de':
                   {'short': 'physioth.'
                   ,'title': 'Physiotherapy'
                   }
               ,'es':
                   {'short': 'physioth.'
                   ,'title': 'Physiotherapy'
                   }
               ,'uk':
                   {'short': 'фізіотер.'
                   ,'title': 'Фізіотерапія'
                   }
               }
           ,'phytophathol.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'phytophathol.'
                   ,'title': 'Phytophathology'
                   }
               ,'ru':
                   {'short': 'фитопат.'
                   ,'title': 'Фитопатология'
                   }
               ,'de':
                   {'short': 'phytophathol.'
                   ,'title': 'Phytophathology'
                   }
               ,'es':
                   {'short': 'phytophathol.'
                   ,'title': 'Phytophathology'
                   }
               ,'uk':
                   {'short': 'фітопатол.'
                   ,'title': 'Фітопатологія'
                   }
               }
           ,'piez.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'piez.'
                   ,'title': 'Piezoelectric crystals'
                   }
               ,'ru':
                   {'short': 'пьез.'
                   ,'title': 'Пьезокристаллы'
                   }
               ,'de':
                   {'short': 'Piez.'
                   ,'title': 'Piezokristalle'
                   }
               ,'es':
                   {'short': 'piez.'
                   ,'title': 'Piezoelectric crystals'
                   }
               ,'uk':
                   {'short': "п'єз.", 'title': "П'єзокристали"}}, 'pipes.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'pipes.'
                   ,'title': 'Pipelines'
                   }
               ,'ru':
                   {'short': 'труб.'
                   ,'title': 'Трубопроводы'
                   }
               ,'de':
                   {'short': 'pipes.'
                   ,'title': 'Pipelines'
                   }
               ,'es':
                   {'short': 'pipes.'
                   ,'title': 'Pipelines'
                   }
               ,'uk':
                   {'short': 'труб.'
                   ,'title': 'Трубопроводи'
                   }
               }
           ,'plann.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'plann.'
                   ,'title': 'Planning'
                   }
               ,'ru':
                   {'short': 'план.'
                   ,'title': 'Планирование'
                   }
               ,'de':
                   {'short': 'Plan.'
                   ,'title': 'Planung'
                   }
               ,'es':
                   {'short': 'plann.'
                   ,'title': 'Planning'
                   }
               ,'uk':
                   {'short': 'план.'
                   ,'title': 'Планування'
                   }
               }
           ,'plast.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'plast.'
                   ,'title': 'Plastics'
                   }
               ,'ru':
                   {'short': 'пласт.'
                   ,'title': 'Пластмассы'
                   }
               ,'de':
                   {'short': 'Kunstst.'
                   ,'title': 'Kunststoffe'
                   }
               ,'es':
                   {'short': 'plast.'
                   ,'title': 'Plastics'
                   }
               ,'uk':
                   {'short': 'пласт.'
                   ,'title': 'Пластмаси'
                   }
               }
           ,'plumb.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'plumb.'
                   ,'title': 'Plumbing'
                   }
               ,'ru':
                   {'short': 'сантех.'
                   ,'title': 'Сантехника'
                   }
               ,'de':
                   {'short': 'Sanitär.'
                   ,'title': 'Sanitärtechnik'
                   }
               ,'es':
                   {'short': 'plumb.'
                   ,'title': 'Plumbing'
                   }
               ,'uk':
                   {'short': 'сантех.'
                   ,'title': 'Сантехніка'
                   }
               }
           ,'pmp.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'pmp.'
                   ,'title': 'Pumps'
                   }
               ,'ru':
                   {'short': 'насос.'
                   ,'title': 'Насосы'
                   }
               ,'de':
                   {'short': 'pmp.'
                   ,'title': 'Pumps'
                   }
               ,'es':
                   {'short': 'pmp.'
                   ,'title': 'Pumps'
                   }
               ,'uk':
                   {'short': 'насос.'
                   ,'title': 'Насоси'
                   }
               }
           ,'pneum.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'pneum.'
                   ,'title': 'Pneumatics'
                   }
               ,'ru':
                   {'short': 'пневм.'
                   ,'title': 'Пневматические устройства'
                   }
               ,'de':
                   {'short': 'pneum.'
                   ,'title': 'Pneumatics'
                   }
               ,'es':
                   {'short': 'pneum.'
                   ,'title': 'Pneumatics'
                   }
               ,'uk':
                   {'short': 'пневм.'
                   ,'title': 'Пневматичні пристрої'
                   }
               }
           ,'poetic':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'poetic'
                   ,'title': 'Poetic'
                   }
               ,'ru':
                   {'short': 'поэт.'
                   ,'title': 'Поэтический язык'
                   }
               ,'de':
                   {'short': 'Poet.'
                   ,'title': 'Poetisch'
                   }
               ,'es':
                   {'short': 'poét.'
                   ,'title': 'Poético'
                   }
               ,'uk':
                   {'short': 'поет.'
                   ,'title': 'Поетична мова'
                   }
               }
           ,'poetry':
               {'is_valid': True
               ,'major_en': 'Literature'
               ,'is_major': False
               ,'en':
                   {'short': 'poetry'
                   ,'title': 'Poetry (terminology)'
                   }
               ,'ru':
                   {'short': 'поэз.'
                   ,'title': 'Поэзия (терминология)'
                   }
               ,'de':
                   {'short': 'Poe.'
                   ,'title': 'Poesie'
                   }
               ,'es':
                   {'short': 'poesía'
                   ,'title': 'Poesía (terminología)'
                   }
               ,'uk':
                   {'short': 'поез.'
                   ,'title': 'Поезія (термінологія)'
                   }
               }
           ,'police':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'police'
                   ,'title': 'Police'
                   }
               ,'ru':
                   {'short': 'полиц.'
                   ,'title': 'Полиция'
                   }
               ,'de':
                   {'short': 'Poliz.'
                   ,'title': 'Polizei'
                   }
               ,'es':
                   {'short': 'police'
                   ,'title': 'Police'
                   }
               ,'uk':
                   {'short': 'поліц.'
                   ,'title': 'Поліція'
                   }
               }
           ,'police.jarg.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'police.jarg.'
                   ,'title': 'Police jargon'
                   }
               ,'ru':
                   {'short': 'полиц.жарг.'
                   ,'title': 'Полицейский жаргон'
                   }
               ,'de':
                   {'short': 'Poliz.jarg.'
                   ,'title': 'Polizeijargon'
                   }
               ,'es':
                   {'short': 'police.jarg.'
                   ,'title': 'Police jargon'
                   }
               ,'uk':
                   {'short': 'поліц.жарг.'
                   ,'title': 'Поліцейський жаргон'
                   }
               }
           ,'polish.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'polish.'
                   ,'title': 'Polish'
                   }
               ,'ru':
                   {'short': 'польск.'
                   ,'title': 'Польский язык'
                   }
               ,'de':
                   {'short': 'Poln.'
                   ,'title': 'Polnisch'
                   }
               ,'es':
                   {'short': 'polish.'
                   ,'title': 'Polish'
                   }
               ,'uk':
                   {'short': 'польськ.'
                   ,'title': 'Польська мова'
                   }
               }
           ,'polit.':
               {'is_valid': True
               ,'major_en': 'Politics'
               ,'is_major': True
               ,'en':
                   {'short': 'polit.'
                   ,'title': 'Politics'
                   }
               ,'ru':
                   {'short': 'полит.'
                   ,'title': 'Политика'
                   }
               ,'de':
                   {'short': 'Polit.'
                   ,'title': 'Politik'
                   }
               ,'es':
                   {'short': 'polít.'
                   ,'title': 'Política'
                   }
               ,'uk':
                   {'short': 'політ.'
                   ,'title': 'Політика'
                   }
               }
           ,'polit.econ.':
               {'is_valid': True
               ,'major_en': 'Economy'
               ,'is_major': False
               ,'en':
                   {'short': 'polit.econ.'
                   ,'title': 'Political economy'
                   }
               ,'ru':
                   {'short': 'политэк.'
                   ,'title': 'Политэкономия'
                   }
               ,'de':
                   {'short': 'polit.econ.'
                   ,'title': 'Political economy'
                   }
               ,'es':
                   {'short': 'polit.econ.'
                   ,'title': 'Political economy'
                   }
               ,'uk':
                   {'short': 'політ.ек.'
                   ,'title': 'Політична економія'
                   }
               }
           ,'polite':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'polite'
                   ,'title': 'Polite'
                   }
               ,'ru':
                   {'short': 'вежл.'
                   ,'title': 'Вежливо'
                   }
               ,'de':
                   {'short': 'polite'
                   ,'title': 'Polite'
                   }
               ,'es':
                   {'short': 'polite'
                   ,'title': 'Polite'
                   }
               ,'uk':
                   {'short': 'ввічл.'
                   ,'title': 'Ввічливо'
                   }
               }
           ,'polygr.':
               {'is_valid': True
               ,'major_en': 'Publishing'
               ,'is_major': False
               ,'en':
                   {'short': 'polygr.'
                   ,'title': 'Polygraphy'
                   }
               ,'ru':
                   {'short': 'полигр.'
                   ,'title': 'Полиграфия'
                   }
               ,'de':
                   {'short': 'Polygr.'
                   ,'title': 'Polygraphie'
                   }
               ,'es':
                   {'short': 'poligr.'
                   ,'title': 'Poligrafía'
                   }
               ,'uk':
                   {'short': 'полігр.'
                   ,'title': 'Поліграфія'
                   }
               }
           ,'polym.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'polym.'
                   ,'title': 'Polymers'
                   }
               ,'ru':
                   {'short': 'полим.'
                   ,'title': 'Полимеры'
                   }
               ,'de':
                   {'short': 'Polym.'
                   ,'title': 'Polymere'
                   }
               ,'es':
                   {'short': 'polym.'
                   ,'title': 'Polymers'
                   }
               ,'uk':
                   {'short': 'полім.'
                   ,'title': 'Полімери'
                   }
               }
           ,'polynes.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'polynes.'
                   ,'title': 'Polynesian'
                   }
               ,'ru':
                   {'short': 'полинез.'
                   ,'title': 'Полинезийское выражение'
                   }
               ,'de':
                   {'short': 'polynes.'
                   ,'title': 'Polynesian'
                   }
               ,'es':
                   {'short': 'polynes.'
                   ,'title': 'Polynesian'
                   }
               ,'uk':
                   {'short': 'полінез.'
                   ,'title': 'Полінезійський вираз'
                   }
               }
           ,'pomp.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'pomp.'
                   ,'title': 'Pompous'
                   }
               ,'ru':
                   {'short': 'высок.'
                   ,'title': 'Высокопарно'
                   }
               ,'de':
                   {'short': 'Schwülst.'
                   ,'title': 'Schwülstig'
                   }
               ,'es':
                   {'short': 'pomp.'
                   ,'title': 'Pompous'
                   }
               ,'uk':
                   {'short': 'високом.'
                   ,'title': 'Високомовно'
                   }
               }
           ,'port.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'port.'
                   ,'title': 'Portuguese'
                   }
               ,'ru':
                   {'short': 'порт.'
                   ,'title': 'Португальский язык'
                   }
               ,'de':
                   {'short': 'Portug.'
                   ,'title': 'Portugiesisch'
                   }
               ,'es':
                   {'short': 'port.'
                   ,'title': 'Portuguese'
                   }
               ,'uk':
                   {'short': 'португ.'
                   ,'title': 'Португальська мова'
                   }
               }
           ,'post':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'post'
                   ,'title': 'Postal service'
                   }
               ,'ru':
                   {'short': 'почт.'
                   ,'title': 'Почта'
                   }
               ,'de':
                   {'short': 'Post'
                   ,'title': 'Post'
                   }
               ,'es':
                   {'short': 'post'
                   ,'title': 'Postal service'
                   }
               ,'uk':
                   {'short': 'пошт.'
                   ,'title': 'Пошта'
                   }
               }
           ,'pow.el.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'pow.el.'
                   ,'title': 'Power electronics'
                   }
               ,'ru':
                   {'short': 'сил.эл.'
                   ,'title': 'Силовая электроника'
                   }
               ,'de':
                   {'short': 'Leist.el.'
                   ,'title': 'Leistungselektronik'
                   }
               ,'es':
                   {'short': 'pow.el.'
                   ,'title': 'Power electronics'
                   }
               ,'uk':
                   {'short': 'сил.ел.'
                   ,'title': 'Силова електроніка'
                   }
               }
           ,'powd.met.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'powd.met.'
                   ,'title': 'Powder metallurgy'
                   }
               ,'ru':
                   {'short': 'пор.мет.'
                   ,'title': 'Порошковая металлургия'
                   }
               ,'de':
                   {'short': 'Pul.met.'
                   ,'title': 'Pulvermetallurgie'
                   }
               ,'es':
                   {'short': 'powd.met.'
                   ,'title': 'Powder metallurgy'
                   }
               ,'uk':
                   {'short': 'пор.мет.'
                   ,'title': 'Порошкова металургія'
                   }
               }
           ,'pragm.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'pragm.'
                   ,'title': 'Pragmatics'
                   }
               ,'ru':
                   {'short': 'прагм.'
                   ,'title': 'Прагматика'
                   }
               ,'de':
                   {'short': 'pragm.'
                   ,'title': 'Pragmatics'
                   }
               ,'es':
                   {'short': 'pragm.'
                   ,'title': 'Pragmatics'
                   }
               ,'uk':
                   {'short': 'прагм.'
                   ,'title': 'Прагматика'
                   }
               }
           ,'press.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'press.'
                   ,'title': 'Press equipment'
                   }
               ,'ru':
                   {'short': 'пресс.'
                   ,'title': 'Прессовое оборудование'
                   }
               ,'de':
                   {'short': 'Press.'
                   ,'title': 'Pressanlagen'
                   }
               ,'es':
                   {'short': 'press.'
                   ,'title': 'Press equipment'
                   }
               ,'uk':
                   {'short': 'прес.'
                   ,'title': 'Пресове обладнання'
                   }
               }
           ,'pris.sl.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'pris.sl.'
                   ,'title': 'Prison slang'
                   }
               ,'ru':
                   {'short': 'тюр.жарг.'
                   ,'title': 'Тюремный жаргон'
                   }
               ,'de':
                   {'short': 'Dieb.jarg.'
                   ,'title': 'Diebesjargon'
                   }
               ,'es':
                   {'short': 'pris.sl.'
                   ,'title': 'Prison slang'
                   }
               ,'uk':
                   {'short': "в'язн.жарг.", 'title': 'В’язничний жаргон'
                   }
               }
           ,'priv.int.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'priv.int.law.'
                   ,'title': 'Private international law'
                   }
               ,'ru':
                   {'short': 'междун.частн.прав.'
                   ,'title': 'Международное частное право'
                   }
               ,'de':
                   {'short': 'priv.int.law.'
                   ,'title': 'Private international law'
                   }
               ,'es':
                   {'short': 'priv.int.law.'
                   ,'title': 'Private international law'
                   }
               ,'uk':
                   {'short': 'міжн.прив.пр.'
                   ,'title': 'Міжнародне приватне право'
                   }
               }
           ,'procur.':
               {'is_valid': True
               ,'major_en': 'Logistics'
               ,'is_major': False
               ,'en':
                   {'short': 'procur.'
                   ,'title': 'Procurement'
                   }
               ,'ru':
                   {'short': 'снабж.'
                   ,'title': 'Снабжение'
                   }
               ,'de':
                   {'short': 'procur.'
                   ,'title': 'Procurement'
                   }
               ,'es':
                   {'short': 'procur.'
                   ,'title': 'Procurement'
                   }
               ,'uk':
                   {'short': 'постач.'
                   ,'title': 'Постачання'
                   }
               }
           ,'product.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': True
               ,'en':
                   {'short': 'product.'
                   ,'title': 'Production'
                   }
               ,'ru':
                   {'short': 'произв.'
                   ,'title': 'Производство'
                   }
               ,'de':
                   {'short': 'Produkt.'
                   ,'title': 'Produktion'
                   }
               ,'es':
                   {'short': 'product.'
                   ,'title': 'Production'
                   }
               ,'uk':
                   {'short': 'вироб.'
                   ,'title': 'Виробництво'
                   }
               }
           ,'prof.jarg.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'prof.jarg.'
                   ,'title': 'Professional jargon'
                   }
               ,'ru':
                   {'short': 'проф.жарг.'
                   ,'title': 'Профессиональный жаргон'
                   }
               ,'de':
                   {'short': 'Fachj.'
                   ,'title': 'Fachjargon'
                   }
               ,'es':
                   {'short': 'profesion.'
                   ,'title': 'Jerga profesional'
                   }
               ,'uk':
                   {'short': 'проф.жарг.'
                   ,'title': 'Професійний жаргон'
                   }
               }
           ,'progr.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'progr.'
                   ,'title': 'Programming'
                   }
               ,'ru':
                   {'short': 'прогр.'
                   ,'title': 'Программирование'
                   }
               ,'de':
                   {'short': 'Progr.'
                   ,'title': 'Programmierung'
                   }
               ,'es':
                   {'short': 'progr.'
                   ,'title': 'Programming'
                   }
               ,'uk':
                   {'short': 'прогр.'
                   ,'title': 'Програмування'
                   }
               }
           ,'proj.manag.':
               {'is_valid': True
               ,'major_en': 'Management'
               ,'is_major': False
               ,'en':
                   {'short': 'proj.manag.'
                   ,'title': 'Project management'
                   }
               ,'ru':
                   {'short': 'управл.проект.'
                   ,'title': 'Управление проектами'
                   }
               ,'de':
                   {'short': 'proj.manag.'
                   ,'title': 'Project management'
                   }
               ,'es':
                   {'short': 'proj.manag.'
                   ,'title': 'Project management'
                   }
               ,'uk':
                   {'short': 'управл.проект.'
                   ,'title': 'Управління проектами'
                   }
               }
           ,'project.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'project.'
                   ,'title': 'Projectors'
                   }
               ,'ru':
                   {'short': 'проекц.'
                   ,'title': 'Проекторы'
                   }
               ,'de':
                   {'short': 'project.'
                   ,'title': 'Projectors'
                   }
               ,'es':
                   {'short': 'project.'
                   ,'title': 'Projectors'
                   }
               ,'uk':
                   {'short': 'проекц.'
                   ,'title': 'Проектори'
                   }
               }
           ,'prop.&figur.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'ru':
                   {'short': 'прям.перен.'
                   ,'title': 'Прямой и переносный смысл'
                   }
               ,'de':
                   {'short': 'prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'es':
                   {'short': 'prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'uk':
                   {'short': 'прям.перен.'
                   ,'title': 'Прямий і переносний сенс'
                   }
               }
           ,'prop.name':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': True
               ,'en':
                   {'short': 'prop.name'
                   ,'title': 'Proper name'
                   }
               ,'ru':
                   {'short': 'собств.'
                   ,'title': 'Имя собственное'
                   }
               ,'de':
                   {'short': 'Eig.name.'
                   ,'title': 'Eigenname'
                   }
               ,'es':
                   {'short': 'prop.name'
                   ,'title': 'Proper name'
                   }
               ,'uk':
                   {'short': 'власн.ім.'
                   ,'title': 'Власний іменник'
                   }
               }
           ,'protozool.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'protozool.'
                   ,'title': 'Protozoology'
                   }
               ,'ru':
                   {'short': 'протист.'
                   ,'title': 'Протистология'
                   }
               ,'de':
                   {'short': 'protozool.'
                   ,'title': 'Protozoology'
                   }
               ,'es':
                   {'short': 'protozool.'
                   ,'title': 'Protozoology'
                   }
               ,'uk':
                   {'short': 'протист.'
                   ,'title': 'Протистологія'
                   }
               }
           ,'proverb':
               {'is_valid': True
               ,'major_en': 'Folklore'
               ,'is_major': False
               ,'en':
                   {'short': 'proverb'
                   ,'title': 'Proverb'
                   }
               ,'ru':
                   {'short': 'посл.'
                   ,'title': 'Пословица'
                   }
               ,'de':
                   {'short': 'Sprw.'
                   ,'title': 'Sprichwort'
                   }
               ,'es':
                   {'short': 'proverb'
                   ,'title': 'Proverb'
                   }
               ,'uk':
                   {'short': 'присл.'
                   ,'title': 'Прислів’я'
                   }
               }
           ,'psychiat.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'psychiat.'
                   ,'title': 'Psychiatry'
                   }
               ,'ru':
                   {'short': 'психиатр.'
                   ,'title': 'Психиатрия'
                   }
               ,'de':
                   {'short': 'Psych.'
                   ,'title': 'Psychiatrie'
                   }
               ,'es':
                   {'short': 'psiq.'
                   ,'title': 'Psiquiatría'
                   }
               ,'uk':
                   {'short': 'психіатр.'
                   ,'title': 'Психіатрія'
                   }
               }
           ,'psychol.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': True
               ,'en':
                   {'short': 'psychol.'
                   ,'title': 'Psychology'
                   }
               ,'ru':
                   {'short': 'психол.'
                   ,'title': 'Психология'
                   }
               ,'de':
                   {'short': 'Psychol.'
                   ,'title': 'Psychologie'
                   }
               ,'es':
                   {'short': 'psic.'
                   ,'title': 'Psicología'
                   }
               ,'uk':
                   {'short': 'психол.'
                   ,'title': 'Психологія'
                   }
               }
           ,'psycholing.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'psycholing.'
                   ,'title': 'Psycholinguistics'
                   }
               ,'ru':
                   {'short': 'психолингв.'
                   ,'title': 'Психолингвистика'
                   }
               ,'de':
                   {'short': 'psycholing.'
                   ,'title': 'Psycholinguistics'
                   }
               ,'es':
                   {'short': 'psycholing.'
                   ,'title': 'Psycholinguistics'
                   }
               ,'uk':
                   {'short': 'психолінгв.'
                   ,'title': 'Психолінгвістика'
                   }
               }
           ,'psychopathol.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': False
               ,'en':
                   {'short': 'psychopathol.'
                   ,'title': 'Psychopathology'
                   }
               ,'ru':
                   {'short': 'психопатол.'
                   ,'title': 'Психопатология'
                   }
               ,'de':
                   {'short': 'psychopathol.'
                   ,'title': 'Psychopathology'
                   }
               ,'es':
                   {'short': 'psychopathol.'
                   ,'title': 'Psychopathology'
                   }
               ,'uk':
                   {'short': 'психопатол.'
                   ,'title': 'Психопатологія'
                   }
               }
           ,'psychophys.':
               {'is_valid': True
               ,'major_en': 'Psychology'
               ,'is_major': False
               ,'en':
                   {'short': 'psychophys.'
                   ,'title': 'Psychophysiology'
                   }
               ,'ru':
                   {'short': 'психофиз.'
                   ,'title': 'Психофизиология'
                   }
               ,'de':
                   {'short': 'psychophys.'
                   ,'title': 'Psychophysiology'
                   }
               ,'es':
                   {'short': 'psychophys.'
                   ,'title': 'Psychophysiology'
                   }
               ,'uk':
                   {'short': 'психофіз.'
                   ,'title': 'Психофізіологія'
                   }
               }
           ,'psychother.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'psychother.'
                   ,'title': 'Psychotherapy'
                   }
               ,'ru':
                   {'short': 'психотер.'
                   ,'title': 'Психотерапия'
                   }
               ,'de':
                   {'short': 'psychother.'
                   ,'title': 'Psychotherapy'
                   }
               ,'es':
                   {'short': 'psychother.'
                   ,'title': 'Psychotherapy'
                   }
               ,'uk':
                   {'short': 'психотер.'
                   ,'title': 'Психотерапія'
                   }
               }
           ,'publ.law.':
               {'is_valid': True
               ,'major_en': 'Law'
               ,'is_major': False
               ,'en':
                   {'short': 'publ.law.'
                   ,'title': 'Public law'
                   }
               ,'ru':
                   {'short': 'публ.прав.'
                   ,'title': 'Публичное право'
                   }
               ,'de':
                   {'short': 'publ.law.'
                   ,'title': 'Public law'
                   }
               ,'es':
                   {'short': 'publ.law.'
                   ,'title': 'Public law'
                   }
               ,'uk':
                   {'short': 'публ.прав.'
                   ,'title': 'Публічне право'
                   }
               }
           ,'publ.transp.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'publ.transp.'
                   ,'title': 'Public transportation'
                   }
               ,'ru':
                   {'short': 'общ.трансп.'
                   ,'title': 'Общественный транспорт'
                   }
               ,'de':
                   {'short': 'publ.transp.'
                   ,'title': 'Public transportation'
                   }
               ,'es':
                   {'short': 'publ.transp.'
                   ,'title': 'Public transportation'
                   }
               ,'uk':
                   {'short': 'гром.трансп.'
                   ,'title': 'Громадський транспорт'
                   }
               }
           ,'publ.util.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'publ.util.'
                   ,'title': 'Public utilities'
                   }
               ,'ru':
                   {'short': 'ком.хоз.'
                   ,'title': 'Коммунальное хозяйство'
                   }
               ,'de':
                   {'short': 'publ.util.'
                   ,'title': 'Public utilities'
                   }
               ,'es':
                   {'short': 'publ.util.'
                   ,'title': 'Public utilities'
                   }
               ,'uk':
                   {'short': 'комун.госп.'
                   ,'title': 'Комунальне господарство'
                   }
               }
           ,'publish.':
               {'is_valid': True
               ,'major_en': 'Publishing'
               ,'is_major': True
               ,'en':
                   {'short': 'publish.'
                   ,'title': 'Publishing'
                   }
               ,'ru':
                   {'short': 'издат.'
                   ,'title': 'Издательское дело'
                   }
               ,'de':
                   {'short': 'Verlagswes.'
                   ,'title': 'Verlagswesen'
                   }
               ,'es':
                   {'short': 'publish.'
                   ,'title': 'Publishing'
                   }
               ,'uk':
                   {'short': 'видавн.'
                   ,'title': 'Видавнича справа'
                   }
               }
           ,'puert.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'puert.'
                   ,'title': 'Puerto Rican Spanish'
                   }
               ,'ru':
                   {'short': 'пуэрт.'
                   ,'title': 'Пуэрто-риканский диалект испанского языка'
                   }
               ,'de':
                   {'short': 'puert.'
                   ,'title': 'Puerto Rican Spanish'
                   }
               ,'es':
                   {'short': 'puert.'
                   ,'title': 'Puerto Rican Spanish'
                   }
               ,'uk':
                   {'short': 'пуерт.'
                   ,'title': 'Пуерто-риканський діалект іспанської мови'
                   }
               }
           ,'pulm.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'pulm.'
                   ,'title': 'Pulmonology'
                   }
               ,'ru':
                   {'short': 'пульм.'
                   ,'title': 'Пульмонология'
                   }
               ,'de':
                   {'short': 'Pulm.'
                   ,'title': 'Pulmonologie'
                   }
               ,'es':
                   {'short': 'pulm.'
                   ,'title': 'Pulmonology'
                   }
               ,'uk':
                   {'short': 'пульм.'
                   ,'title': 'Пульмонологія'
                   }
               }
           ,'pulp.n.paper':
               {'is_valid': True
               ,'major_en': 'Wood, pulp and paper industries'
               ,'is_major': False
               ,'en':
                   {'short': 'pulp.n.paper'
                   ,'title': 'Pulp and paper industry'
                   }
               ,'ru':
                   {'short': 'целл.бум.'
                   ,'title': 'Целлюлозно-бумажная промышленность'
                   }
               ,'de':
                   {'short': 'papier.zellst.'
                   ,'title': 'Papier- und Zellstoffindustrie'
                   }
               ,'es':
                   {'short': 'pulp.n.paper'
                   ,'title': 'Pulp and paper industry'
                   }
               ,'uk':
                   {'short': 'цел.папер.'
                   ,'title': 'Целюлозно-паперова промисловість'
                   }
               }
           ,'pwr.lines.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'pwr.lines.'
                   ,'title': 'Power lines'
                   }
               ,'ru':
                   {'short': 'лин.'
                   ,'title': 'Линии электропередач'
                   }
               ,'de':
                   {'short': 'pwr.lines.'
                   ,'title': 'Power lines'
                   }
               ,'es':
                   {'short': 'pwr.lines.'
                   ,'title': 'Power lines'
                   }
               ,'uk':
                   {'short': 'ЛЕП'
                   ,'title': 'Лінії електропередачі'
                   }
               }
           ,'qual.cont.':
               {'is_valid': True
               ,'major_en': 'Quality control and standards'
               ,'is_major': True
               ,'en':
                   {'short': 'qual.cont.'
                   ,'title': 'Quality control and standards'
                   }
               ,'ru':
                   {'short': 'контр.кач.'
                   ,'title': 'Контроль качества и стандартизация'
                   }
               ,'de':
                   {'short': 'Qual.Kontr.'
                   ,'title': 'Qualitätskontrolle und Normierung'
                   }
               ,'es':
                   {'short': 'qual.cont.'
                   ,'title': 'Quality control and standards'
                   }
               ,'uk':
                   {'short': 'контр.як.'
                   ,'title': 'Контроль якості та стандартизація'
                   }
               }
           ,'quant.el.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'quant.el.'
                   ,'title': 'Quantum electronics'
                   }
               ,'ru':
                   {'short': 'квант.эл.'
                   ,'title': 'Квантовая электроника'
                   }
               ,'de':
                   {'short': 'quant.el.'
                   ,'title': 'Quantum electronics'
                   }
               ,'es':
                   {'short': 'quant.el.'
                   ,'title': 'Quantum electronics'
                   }
               ,'uk':
                   {'short': 'квант.ел.'
                   ,'title': 'Квантова електроніка'
                   }
               }
           ,'quant.mech.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'quant.mech.'
                   ,'title': 'Quantum mechanics'
                   }
               ,'ru':
                   {'short': 'квант.мех.'
                   ,'title': 'Квантовая механика'
                   }
               ,'de':
                   {'short': 'Quant.mech.'
                   ,'title': 'Quantenmechanik'
                   }
               ,'es':
                   {'short': 'quant.mech.'
                   ,'title': 'Quantum mechanics'
                   }
               ,'uk':
                   {'short': 'квант.мех.'
                   ,'title': 'Квантова механіка'
                   }
               }
           ,'quar.':
               {'is_valid': True
               ,'major_en': 'Mining'
               ,'is_major': False
               ,'en':
                   {'short': 'quar.'
                   ,'title': 'Quarrying'
                   }
               ,'ru':
                   {'short': 'карьер.'
                   ,'title': 'Карьерные работы'
                   }
               ,'de':
                   {'short': 'quar.'
                   ,'title': 'Quarrying'
                   }
               ,'es':
                   {'short': 'quar.'
                   ,'title': 'Quarrying'
                   }
               ,'uk':
                   {'short': "кар'єр.", 'title': 'Кар’єрні роботи'
                   }
               }
           ,'quran':
               {'is_valid': True
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'quran'
                   ,'title': 'Quran'
                   }
               ,'ru':
                   {'short': 'коран.'
                   ,'title': 'Коран'
                   }
               ,'de':
                   {'short': 'Kor.'
                   ,'title': 'Koran'
                   }
               ,'es':
                   {'short': 'quran'
                   ,'title': 'Quran'
                   }
               ,'uk':
                   {'short': 'коран'
                   ,'title': 'Коран'
                   }
               }
           ,'racing':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'racing'
                   ,'title': 'Racing and motorsport'
                   }
               ,'ru':
                   {'short': 'гонки.'
                   ,'title': 'Гонки и автоспорт'
                   }
               ,'de':
                   {'short': 'racing'
                   ,'title': 'Racing and motorsport'
                   }
               ,'es':
                   {'short': 'racing'
                   ,'title': 'Racing and motorsport'
                   }
               ,'uk':
                   {'short': 'перег.'
                   ,'title': 'Перегони та автоспорт'
                   }
               }
           ,'rad.geod.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'rad.geod.'
                   ,'title': 'Radiogeodesy'
                   }
               ,'ru':
                   {'short': 'рдгд.'
                   ,'title': 'Радиогеодезия'
                   }
               ,'de':
                   {'short': 'rad.geod.'
                   ,'title': 'Radiogeodesy'
                   }
               ,'es':
                   {'short': 'rad.geod.'
                   ,'title': 'Radiogeodesy'
                   }
               ,'uk':
                   {'short': 'р.геод.'
                   ,'title': 'Радіогеодезія'
                   }
               }
           ,'radio':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'radio'
                   ,'title': 'Radio'
                   }
               ,'ru':
                   {'short': 'радио.'
                   ,'title': 'Радио'
                   }
               ,'de':
                   {'short': 'Radio.'
                   ,'title': 'Radio'
                   }
               ,'es':
                   {'short': 'radio'
                   ,'title': 'Radio'
                   }
               ,'uk':
                   {'short': 'радіо'
                   ,'title': 'Радіо'
                   }
               }
           ,'radio, amer.usg., abbr.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'radio, amer.usg., abbr.'
                   ,'title': 'Radio, American (usage, not AmE), Abbreviation'
                   }
               ,'ru':
                   {'short': 'радио., амер., сокр.'
                   ,'title': 'Радио, Американское выражение (не вариант языка), Сокращение'
                   }
               ,'de':
                   {'short': 'Radio., Amerik., Abkürz.'
                   ,'title': 'Radio, Amerikanisch, Abkürzung'
                   }
               ,'es':
                   {'short': 'radio, amer., abrev.'
                   ,'title': 'Radio, Americano (uso), Abreviatura'
                   }
               ,'uk':
                   {'short': 'радіо, амер.вир., абрев.'
                   ,'title': 'Радіо, Американський вираз (не варыант мови), Абревіатура'
                   }
               }
           ,'radioastron.':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': False
               ,'en':
                   {'short': 'radioastron.'
                   ,'title': 'Radioastronomy'
                   }
               ,'ru':
                   {'short': 'рда.'
                   ,'title': 'Радиоастрономия'
                   }
               ,'de':
                   {'short': 'radioastron.'
                   ,'title': 'Radioastronomy'
                   }
               ,'es':
                   {'short': 'radioastron.'
                   ,'title': 'Radioastronomy'
                   }
               ,'uk':
                   {'short': 'радіоастр.'
                   ,'title': 'Радіоастрономія'
                   }
               }
           ,'radiobiol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'radiobiol.'
                   ,'title': 'Radiobiology'
                   }
               ,'ru':
                   {'short': 'радиобиол.'
                   ,'title': 'Радиобиология'
                   }
               ,'de':
                   {'short': 'radiobiol.'
                   ,'title': 'Radiobiology'
                   }
               ,'es':
                   {'short': 'radiobiol.'
                   ,'title': 'Radiobiology'
                   }
               ,'uk':
                   {'short': 'радіобіологія'
                   ,'title': 'Радіобіологія'
                   }
               }
           ,'radiogr.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'radiogr.'
                   ,'title': 'Radiography'
                   }
               ,'ru':
                   {'short': 'рентгр.'
                   ,'title': 'Рентгенография'
                   }
               ,'de':
                   {'short': 'radiogr.'
                   ,'title': 'Radiography'
                   }
               ,'es':
                   {'short': 'radiogr.'
                   ,'title': 'Radiography'
                   }
               ,'uk':
                   {'short': 'рентгр.'
                   ,'title': 'Рентгенографія'
                   }
               }
           ,'radiol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'radiol.'
                   ,'title': 'Radiology'
                   }
               ,'ru':
                   {'short': 'рентг.'
                   ,'title': 'Рентгенология'
                   }
               ,'de':
                   {'short': 'radiol.'
                   ,'title': 'Radiologie'
                   }
               ,'es':
                   {'short': 'radiol.'
                   ,'title': 'Radiología'
                   }
               ,'uk':
                   {'short': 'рентг.'
                   ,'title': 'Рентгенологія'
                   }
               }
           ,'radioloc.':
               {'is_valid': True
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'radioloc.'
                   ,'title': 'Radiolocation'
                   }
               ,'ru':
                   {'short': 'рлк.'
                   ,'title': 'Радиолокация'
                   }
               ,'de':
                   {'short': 'Funkort.'
                   ,'title': 'Funkortung'
                   }
               ,'es':
                   {'short': 'radioloc.'
                   ,'title': 'Radiolocation'
                   }
               ,'uk':
                   {'short': 'р.лок.'
                   ,'title': 'Радіолокація'
                   }
               }
           ,'railw.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'railw.'
                   ,'title': 'Railway term'
                   }
               ,'ru':
                   {'short': 'ж/д.'
                   ,'title': 'Железнодорожный термин'
                   }
               ,'de':
                   {'short': 'Eisnbnw.'
                   ,'title': 'Eisenbahnwesen'
                   }
               ,'es':
                   {'short': 'ferroc.'
                   ,'title': 'Ferrocarril'
                   }
               ,'uk':
                   {'short': 'залізнич.'
                   ,'title': 'Залізничний термін'
                   }
               }
           ,'rare':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'rare'
                   ,'title': 'Rare'
                   }
               ,'ru':
                   {'short': 'редк.'
                   ,'title': 'Редко'
                   }
               ,'de':
                   {'short': 'selt.'
                   ,'title': 'Seltener Ausdruck'
                   }
               ,'es':
                   {'short': 'rar.'
                   ,'title': 'Raramente'
                   }
               ,'uk':
                   {'short': 'рідк.'
                   ,'title': 'Рідко'
                   }
               }
           ,'real.est.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'real.est.'
                   ,'title': 'Real estate'
                   }
               ,'ru':
                   {'short': 'недвиж.'
                   ,'title': 'Недвижимость'
                   }
               ,'de':
                   {'short': 'Immobil.'
                   ,'title': 'Immobilien'
                   }
               ,'es':
                   {'short': 'real.est.'
                   ,'title': 'Real estate'
                   }
               ,'uk':
                   {'short': 'нерух.'
                   ,'title': 'Нерухомість'
                   }
               }
           ,'rec.mngmt':
               {'is_valid': True
               ,'major_en': 'Records management'
               ,'is_major': True
               ,'en':
                   {'short': 'rec.mngmt'
                   ,'title': 'Records management'
                   }
               ,'ru':
                   {'short': 'делопр.'
                   ,'title': 'Делопроизводство'
                   }
               ,'de':
                   {'short': 'rec.mngmt'
                   ,'title': 'Records management'
                   }
               ,'es':
                   {'short': 'rec.mngmt'
                   ,'title': 'Records management'
                   }
               ,'uk':
                   {'short': 'діловод.'
                   ,'title': 'Діловодство'
                   }
               }
           ,'refr.mat.':
               {'is_valid': True
               ,'major_en': 'Building materials'
               ,'is_major': False
               ,'en':
                   {'short': 'refr.mat.'
                   ,'title': 'Refractory materials'
                   }
               ,'ru':
                   {'short': 'огнеуп.'
                   ,'title': 'Огнеупорные материалы'
                   }
               ,'de':
                   {'short': 'refr.mat.'
                   ,'title': 'Refractory materials'
                   }
               ,'es':
                   {'short': 'refr.mat.'
                   ,'title': 'Refractory materials'
                   }
               ,'uk':
                   {'short': 'вогнетр.'
                   ,'title': 'Вогнетривкі матеріали'
                   }
               }
           ,'refrig.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'refrig.'
                   ,'title': 'Refrigeration'
                   }
               ,'ru':
                   {'short': 'холод.'
                   ,'title': 'Холодильная техника'
                   }
               ,'de':
                   {'short': 'Kühltech.'
                   ,'title': 'Kühltechnik'
                   }
               ,'es':
                   {'short': 'refrig.'
                   ,'title': 'Refrigeration'
                   }
               ,'uk':
                   {'short': 'холод.'
                   ,'title': 'Холодильна техніка'
                   }
               }
           ,'reg.usg.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': True
               ,'en':
                   {'short': 'reg.usg.'
                   ,'title': 'Regional usage (other than language varieties)'
                   }
               ,'ru':
                   {'short': 'рег.выр.'
                   ,'title': 'Региональные выражения (не варианты языка)'
                   }
               ,'de':
                   {'short': 'landsch.'
                   ,'title': 'Landschaftlich'
                   }
               ,'es':
                   {'short': 'reg.usg.'
                   ,'title': 'Regional usage (other than language varieties)'
                   }
               ,'uk':
                   {'short': 'рег.вир.'
                   ,'title': 'Регіональні вирази (не варіанти мови)'
                   }
               }
           ,'rel., budd.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., budd.'
                   ,'title': 'Buddhism'
                   }
               ,'ru':
                   {'short': 'рел., будд.'
                   ,'title': 'Буддизм'
                   }
               ,'de':
                   {'short': 'Budd.'
                   ,'title': 'Buddhismus'
                   }
               ,'es':
                   {'short': 'rel., budd.'
                   ,'title': 'Buddhism'
                   }
               ,'uk':
                   {'short': 'будд.'
                   ,'title': 'Буддизм'
                   }
               }
           ,'rel., cath.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., cath.'
                   ,'title': 'Catholic'
                   }
               ,'ru':
                   {'short': 'рел., катол.'
                   ,'title': 'Католицизм'
                   }
               ,'de':
                   {'short': 'rel., cath.'
                   ,'title': 'Catholic'
                   }
               ,'es':
                   {'short': 'rel., cath.'
                   ,'title': 'Catholic'
                   }
               ,'uk':
                   {'short': 'католиц.'
                   ,'title': 'Католицизм'
                   }
               }
           ,'rel., christ.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., christ.'
                   ,'title': 'Christianity'
                   }
               ,'ru':
                   {'short': 'рел., христ.'
                   ,'title': 'Христианство'
                   }
               ,'de':
                   {'short': 'rel., christ.'
                   ,'title': 'Christianity'
                   }
               ,'es':
                   {'short': 'rel., christ.'
                   ,'title': 'Christianity'
                   }
               ,'uk':
                   {'short': 'христ.'
                   ,'title': 'Християнство'
                   }
               }
           ,'rel., east.orth.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., east.orth.'
                   ,'title': 'Eastern Orthodoxy'
                   }
               ,'ru':
                   {'short': 'рел., правосл.'
                   ,'title': 'Православие'
                   }
               ,'de':
                   {'short': 'rel., east.orth.'
                   ,'title': 'Eastern Orthodoxy'
                   }
               ,'es':
                   {'short': 'rel., east.orth.'
                   ,'title': 'Eastern Orthodoxy'
                   }
               ,'uk':
                   {'short': 'рел., правосл.'
                   ,'title': "Православ'я"}}, 'rel., hind.':
               {'is_valid': False
               ,'major_en': 'Mythology'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., hind.'
                   ,'title': 'Hinduism'
                   }
               ,'ru':
                   {'short': 'рел., инд.'
                   ,'title': 'Индуизм'
                   }
               ,'de':
                   {'short': 'rel., hind.'
                   ,'title': 'Hinduism'
                   }
               ,'es':
                   {'short': 'rel., hind.'
                   ,'title': 'Hinduism'
                   }
               ,'uk':
                   {'short': 'рел., інд.'
                   ,'title': 'Індуїзм'
                   }
               }
           ,'rel., islam':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'rel., islam'
                   ,'title': 'Islam'
                   }
               ,'ru':
                   {'short': 'рел., ислам.'
                   ,'title': 'Ислам'
                   }
               ,'de':
                   {'short': 'rel., islam'
                   ,'title': 'Islam'
                   }
               ,'es':
                   {'short': 'rel., islam'
                   ,'title': 'Islam'
                   }
               ,'uk':
                   {'short': 'іслам'
                   ,'title': 'Іслам'
                   }
               }
           ,'reliabil.':
               {'is_valid': True
               ,'major_en': 'Quality control and standards'
               ,'is_major': False
               ,'en':
                   {'short': 'reliabil.'
                   ,'title': 'Reliability'
                   }
               ,'ru':
                   {'short': 'над.'
                   ,'title': 'Надёжность'
                   }
               ,'de':
                   {'short': 'Sicher.'
                   ,'title': 'Sicherheit'
                   }
               ,'es':
                   {'short': 'reliabil.'
                   ,'title': 'Reliability'
                   }
               ,'uk':
                   {'short': 'надійн.'
                   ,'title': 'Надійність'
                   }
               }
           ,'relig.':
               {'is_valid': True
               ,'major_en': 'Religion'
               ,'is_major': True
               ,'en':
                   {'short': 'relig.'
                   ,'title': 'Religion'
                   }
               ,'ru':
                   {'short': 'рел.'
                   ,'title': 'Религия'
                   }
               ,'de':
                   {'short': 'Rel.'
                   ,'title': 'Religion'
                   }
               ,'es':
                   {'short': 'rel.'
                   ,'title': 'Religión'
                   }
               ,'uk':
                   {'short': 'рел.'
                   ,'title': 'Релігія'
                   }
               }
           ,'rem.sens.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'rem.sens.'
                   ,'title': 'Remote sensing'
                   }
               ,'ru':
                   {'short': 'дист.зонд.'
                   ,'title': 'Дистанционное зондирование Земли'
                   }
               ,'de':
                   {'short': 'Fernmess.'
                   ,'title': 'Fernmessungen'
                   }
               ,'es':
                   {'short': 'rem.sens.'
                   ,'title': 'Remote sensing'
                   }
               ,'uk':
                   {'short': 'дист.зонд.'
                   ,'title': 'Дистанційне зондування Землі'
                   }
               }
           ,'reptil.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'reptil.'
                   ,'title': 'Amphibians and reptiles'
                   }
               ,'ru':
                   {'short': 'рептил.'
                   ,'title': 'Амфибии и рептилии'
                   }
               ,'de':
                   {'short': 'reptil.'
                   ,'title': 'Amphibians and reptiles'
                   }
               ,'es':
                   {'short': 'reptil.'
                   ,'title': 'Amphibians and reptiles'
                   }
               ,'uk':
                   {'short': 'плаз.земнов.'
                   ,'title': 'Плазуни і земноводні'
                   }
               }
           ,'resin.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'resin.'
                   ,'title': 'Resins'
                   }
               ,'ru':
                   {'short': 'резин.'
                   ,'title': 'Резиновая промышленность'
                   }
               ,'de':
                   {'short': 'Kautschukind.'
                   ,'title': 'Kautschukindustrie'
                   }
               ,'es':
                   {'short': 'resin.'
                   ,'title': 'Resins'
                   }
               ,'uk':
                   {'short': 'гумов.'
                   ,'title': 'Гумова промисловість'
                   }
               }
           ,'respect.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'respect.'
                   ,'title': 'Respectful'
                   }
               ,'ru':
                   {'short': 'почтит.'
                   ,'title': 'Почтительно'
                   }
               ,'de':
                   {'short': 'respect.'
                   ,'title': 'Respectful'
                   }
               ,'es':
                   {'short': 'respect.'
                   ,'title': 'Respectful'
                   }
               ,'uk':
                   {'short': 'шаноб.'
                   ,'title': 'Шанобливо'
                   }
               }
           ,'rhetor.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'rhetor.'
                   ,'title': 'Rhetoric'
                   }
               ,'ru':
                   {'short': 'ритор.'
                   ,'title': 'Риторика'
                   }
               ,'de':
                   {'short': 'Rhet.'
                   ,'title': 'Rhetorik'
                   }
               ,'es':
                   {'short': 'retór.'
                   ,'title': 'Retórica'
                   }
               ,'uk':
                   {'short': 'ритор.'
                   ,'title': 'Риторика'
                   }
               }
           ,'risk.man.':
               {'is_valid': True
               ,'major_en': 'Management'
               ,'is_major': False
               ,'en':
                   {'short': 'risk.man.'
                   ,'title': 'Risk Management'
                   }
               ,'ru':
                   {'short': 'упр.риск.'
                   ,'title': 'Управление рисками'
                   }
               ,'de':
                   {'short': 'Ris.man.'
                   ,'title': 'Risikomanagement'
                   }
               ,'es':
                   {'short': 'risk.man.'
                   ,'title': 'Risk Management'
                   }
               ,'uk':
                   {'short': 'упр.ризик.'
                   ,'title': 'Управління ризиками'
                   }
               }
           ,'rit.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'rit.'
                   ,'title': 'Ritual'
                   }
               ,'ru':
                   {'short': 'рит.'
                   ,'title': 'Ритуал'
                   }
               ,'de':
                   {'short': 'Rit.'
                   ,'title': 'Ritual'
                   }
               ,'es':
                   {'short': 'rit.'
                   ,'title': 'Ritual'
                   }
               ,'uk':
                   {'short': 'рит.'
                   ,'title': 'Ритуал'
                   }
               }
           ,'road.constr.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'road.constr.'
                   ,'title': 'Road construction'
                   }
               ,'ru':
                   {'short': 'дор.стр.'
                   ,'title': 'Дорожное строительство'
                   }
               ,'de':
                   {'short': 'road.constr.'
                   ,'title': 'Road construction'
                   }
               ,'es':
                   {'short': 'road.constr.'
                   ,'title': 'Road construction'
                   }
               ,'uk':
                   {'short': 'дор.буд.'
                   ,'title': 'Дорожнє будівництво'
                   }
               }
           ,'road.sign.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'road.sign.'
                   ,'title': 'Road sign'
                   }
               ,'ru':
                   {'short': 'дор.зн.'
                   ,'title': 'Дорожный знак'
                   }
               ,'de':
                   {'short': 'road.sign.'
                   ,'title': 'Road sign'
                   }
               ,'es':
                   {'short': 'road.sign.'
                   ,'title': 'Road sign'
                   }
               ,'uk':
                   {'short': 'дор.зн.'
                   ,'title': 'Дорожній знак'
                   }
               }
           ,'road.surf.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'road.surf.'
                   ,'title': 'Road surface'
                   }
               ,'ru':
                   {'short': 'дор.покр.'
                   ,'title': 'Дорожное покрытие'
                   }
               ,'de':
                   {'short': 'road.surf.'
                   ,'title': 'Road surface'
                   }
               ,'es':
                   {'short': 'road.surf.'
                   ,'title': 'Road surface'
                   }
               ,'uk':
                   {'short': 'дор.покр.'
                   ,'title': 'Дорожне покриття'
                   }
               }
           ,'road.wrk.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'road.wrk.'
                   ,'title': 'Road works'
                   }
               ,'ru':
                   {'short': 'дор.'
                   ,'title': 'Дорожное дело'
                   }
               ,'de':
                   {'short': 'Straßenb.'
                   ,'title': 'Straßenbau'
                   }
               ,'es':
                   {'short': 'carret.'
                   ,'title': 'Obras de carreteras'
                   }
               ,'uk':
                   {'short': 'дор.спр.'
                   ,'title': 'Дорожня справа'
                   }
               }
           ,'robot.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'robot.'
                   ,'title': 'Robotics'
                   }
               ,'ru':
                   {'short': 'рбт.'
                   ,'title': 'Робототехника'
                   }
               ,'de':
                   {'short': 'Rob.'
                   ,'title': 'Robotik'
                   }
               ,'es':
                   {'short': 'robot.'
                   ,'title': 'Robotics'
                   }
               ,'uk':
                   {'short': 'робот.'
                   ,'title': 'Робототехніка'
                   }
               }
           ,'roll.':
               {'is_valid': True
               ,'major_en': 'Metallurgy'
               ,'is_major': False
               ,'en':
                   {'short': 'roll.'
                   ,'title': 'Roll stock'
                   }
               ,'ru':
                   {'short': 'прок.'
                   ,'title': 'Прокат (металлургия)'
                   }
               ,'de':
                   {'short': 'Walz.'
                   ,'title': 'Walzgut (Metal.)'
                   }
               ,'es':
                   {'short': 'roll.'
                   ,'title': 'Roll stock'
                   }
               ,'uk':
                   {'short': 'вальц.'
                   ,'title': 'Вальцювання'
                   }
               }
           ,'romanian.lang.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'romanian.lang.'
                   ,'title': 'Romanian'
                   }
               ,'ru':
                   {'short': 'рум.'
                   ,'title': 'Румынский язык'
                   }
               ,'de':
                   {'short': 'Rumän.'
                   ,'title': 'Rumänisch'
                   }
               ,'es':
                   {'short': 'romanian.lang.'
                   ,'title': 'Romanian'
                   }
               ,'uk':
                   {'short': 'румун.'
                   ,'title': 'Румунська мова'
                   }
               }
           ,'rude':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'rude'
                   ,'title': 'Rude'
                   }
               ,'ru':
                   {'short': 'груб.'
                   ,'title': 'Грубо'
                   }
               ,'de':
                   {'short': 'grob.'
                   ,'title': 'Grob'
                   }
               ,'es':
                   {'short': 'rudo'
                   ,'title': 'Rudo'
                   }
               ,'uk':
                   {'short': 'груб.'
                   ,'title': 'Грубо'
                   }
               }
           ,'rugb.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'rugb.'
                   ,'title': 'Rugby football'
                   }
               ,'ru':
                   {'short': 'регби.'
                   ,'title': 'Регби'
                   }
               ,'de':
                   {'short': 'rugb.'
                   ,'title': 'Rugby football'
                   }
               ,'es':
                   {'short': 'rugb.'
                   ,'title': 'Rugby football'
                   }
               ,'uk':
                   {'short': 'регбі'
                   ,'title': 'Регбі'
                   }
               }
           ,'russ.lang.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'russ.lang.'
                   ,'title': 'Russian language'
                   }
               ,'ru':
                   {'short': 'русск.'
                   ,'title': 'Русский язык'
                   }
               ,'de':
                   {'short': 'Rus.'
                   ,'title': 'Russisch'
                   }
               ,'es':
                   {'short': 'ruso'
                   ,'title': 'Idioma ruso'
                   }
               ,'uk':
                   {'short': 'рос.мов.'
                   ,'title': 'Російська мова'
                   }
               }
           ,'s.germ.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 's.germ.'
                   ,'title': 'South German'
                   }
               ,'ru':
                   {'short': 'южн.нем.'
                   ,'title': 'Южнонемецкое выражение'
                   }
               ,'de':
                   {'short': 'Süddt.'
                   ,'title': 'Süddeutsches Dialekt'
                   }
               ,'es':
                   {'short': 's.germ.'
                   ,'title': 'South German'
                   }
               ,'uk':
                   {'short': 'півд.нім.'
                   ,'title': 'Південнонімецький вираз'
                   }
               }
           ,'sail.ships':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'sail.ships'
                   ,'title': 'Sailing ships'
                   }
               ,'ru':
                   {'short': 'парусн.'
                   ,'title': 'Парусные суда'
                   }
               ,'de':
                   {'short': 'sail.ships'
                   ,'title': 'Sailing ships'
                   }
               ,'es':
                   {'short': 'sail.ships'
                   ,'title': 'Sailing ships'
                   }
               ,'uk':
                   {'short': 'вітрил.'
                   ,'title': 'Вітрильні судна'
                   }
               }
           ,'sanit.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'sanit.'
                   ,'title': 'Sanitation'
                   }
               ,'ru':
                   {'short': 'санит.'
                   ,'title': 'Санитария'
                   }
               ,'de':
                   {'short': 'Sanität.'
                   ,'title': 'Sanitätswesen'
                   }
               ,'es':
                   {'short': 'sanit.'
                   ,'title': 'Sanitation'
                   }
               ,'uk':
                   {'short': 'саніт.'
                   ,'title': 'Санітарія'
                   }
               }
           ,'sanscr.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'sanscr.'
                   ,'title': 'Sanskrit'
                   }
               ,'ru':
                   {'short': 'санскр.'
                   ,'title': 'Санскрит'
                   }
               ,'de':
                   {'short': 'Sanskr.'
                   ,'title': 'Sanskrit'
                   }
               ,'es':
                   {'short': 'sánscr.'
                   ,'title': 'Sánscrito'
                   }
               ,'uk':
                   {'short': 'санскр.'
                   ,'title': 'Санскрит'
                   }
               }
           ,'sarcast.':
               {'is_valid': True
               ,'major_en': 'Emotional values'
               ,'is_major': False
               ,'en':
                   {'short': 'sarcast.'
                   ,'title': 'Sarcastical'
                   }
               ,'ru':
                   {'short': 'сарк.'
                   ,'title': 'Сарказм'
                   }
               ,'de':
                   {'short': 'Sark.'
                   ,'title': 'Sarkasmus'
                   }
               ,'es':
                   {'short': 'sarcast.'
                   ,'title': 'Sarcastical'
                   }
               ,'uk':
                   {'short': 'сарк.'
                   ,'title': 'Сарказм'
                   }
               }
           ,'sat.comm.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'sat.comm.'
                   ,'title': 'Satellite communications'
                   }
               ,'ru':
                   {'short': 'спут.'
                   ,'title': 'Спутниковая связь'
                   }
               ,'de':
                   {'short': 'sat.comm.'
                   ,'title': 'Satellite communications'
                   }
               ,'es':
                   {'short': 'sat.comm.'
                   ,'title': 'Satellite communications'
                   }
               ,'uk':
                   {'short': 'супутн.зв.'
                   ,'title': 'Супутниковий зв’язок'
                   }
               }
           ,'saying.':
               {'is_valid': True
               ,'major_en': 'Folklore'
               ,'is_major': False
               ,'en':
                   {'short': 'saying.'
                   ,'title': 'Saying'
                   }
               ,'ru':
                   {'short': 'погов.'
                   ,'title': 'Поговорка'
                   }
               ,'de':
                   {'short': 'saying.'
                   ,'title': 'Saying'
                   }
               ,'es':
                   {'short': 'saying.'
                   ,'title': 'Saying'
                   }
               ,'uk':
                   {'short': 'приказ.'
                   ,'title': 'Приказка'
                   }
               }
           ,'school.sl.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'school.sl.'
                   ,'title': 'School'
                   }
               ,'ru':
                   {'short': 'школ.'
                   ,'title': 'Школьное выражение'
                   }
               ,'de':
                   {'short': 'Schule.'
                   ,'title': 'Schule'
                   }
               ,'es':
                   {'short': 'esc.'
                   ,'title': 'Escolar'
                   }
               ,'uk':
                   {'short': 'шкільн.'
                   ,'title': 'Шкільний вираз'
                   }
               }
           ,'scient.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'scient.'
                   ,'title': 'Scientific'
                   }
               ,'ru':
                   {'short': 'науч.'
                   ,'title': 'Научный термин'
                   }
               ,'de':
                   {'short': 'Wissensch.'
                   ,'title': 'Wissenschaftlicher Ausdruck'
                   }
               ,'es':
                   {'short': 'scient.'
                   ,'title': 'Scientific'
                   }
               ,'uk':
                   {'short': 'науков.'
                   ,'title': 'Науковий термін'
                   }
               }
           ,'scottish':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'scottish'
                   ,'title': 'Scottish (usage)'
                   }
               ,'ru':
                   {'short': 'шотл.выр.'
                   ,'title': 'Шотландское выражение'
                   }
               ,'de':
                   {'short': 'Schott.'
                   ,'title': 'Schottisch (Slang)'
                   }
               ,'es':
                   {'short': 'scottish'
                   ,'title': 'Scottish (usage)'
                   }
               ,'uk':
                   {'short': 'шотл.вир.'
                   ,'title': 'Шотландський вираз'
                   }
               }
           ,'scr.':
               {'is_valid': True
               ,'major_en': 'Literature'
               ,'is_major': False
               ,'en':
                   {'short': 'scr.'
                   ,'title': 'Screenwriting'
                   }
               ,'ru':
                   {'short': 'сцен.'
                   ,'title': 'Сценарное мастерство'
                   }
               ,'de':
                   {'short': 'scr.'
                   ,'title': 'Screenwriting'
                   }
               ,'es':
                   {'short': 'scr.'
                   ,'title': 'Screenwriting'
                   }
               ,'uk':
                   {'short': 'сцен.'
                   ,'title': 'Сценарна майстерність'
                   }
               }
           ,'scub.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'scub.'
                   ,'title': 'Scuba diving'
                   }
               ,'ru':
                   {'short': 'подводн.'
                   ,'title': 'Подводное плавание'
                   }
               ,'de':
                   {'short': 'scub.'
                   ,'title': 'Scuba diving'
                   }
               ,'es':
                   {'short': 'scub.'
                   ,'title': 'Scuba diving'
                   }
               ,'uk':
                   {'short': 'підв.плав.'
                   ,'title': 'Підводне плавання'
                   }
               }
           ,'sec.sys.':
               {'is_valid': True
               ,'major_en': 'Security systems'
               ,'is_major': True
               ,'en':
                   {'short': 'sec.sys.'
                   ,'title': 'Security systems'
                   }
               ,'ru':
                   {'short': 'сист.без.'
                   ,'title': 'Системы безопасности'
                   }
               ,'de':
                   {'short': 'sec.sys.'
                   ,'title': 'Security systems'
                   }
               ,'es':
                   {'short': 'sec.sys.'
                   ,'title': 'Security systems'
                   }
               ,'uk':
                   {'short': 'сист.безп.'
                   ,'title': 'Системи безпеки'
                   }
               }
           ,'securit.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'securit.'
                   ,'title': 'Securities'
                   }
               ,'ru':
                   {'short': 'ЦБ.'
                   ,'title': 'Ценные бумаги'
                   }
               ,'de':
                   {'short': 'securit.'
                   ,'title': 'Securities'
                   }
               ,'es':
                   {'short': 'securit.'
                   ,'title': 'Securities'
                   }
               ,'uk':
                   {'short': 'ЦП'
                   ,'title': 'Цінні папери'
                   }
               }
           ,'seism.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'seism.'
                   ,'title': 'Seismology'
                   }
               ,'ru':
                   {'short': 'сейсм.'
                   ,'title': 'Сейсмология'
                   }
               ,'de':
                   {'short': 'Seismol.'
                   ,'title': 'Seismologie'
                   }
               ,'es':
                   {'short': 'seism.'
                   ,'title': 'Seismology'
                   }
               ,'uk':
                   {'short': 'сейсм.'
                   ,'title': 'Сейсмологія'
                   }
               }
           ,'seism.res.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'seism.res.'
                   ,'title': 'Seismic resistance'
                   }
               ,'ru':
                   {'short': 'сейсм.соор.'
                   ,'title': 'Сейсмостойкость сооружений'
                   }
               ,'de':
                   {'short': 'seism.res.'
                   ,'title': 'Seismic resistance'
                   }
               ,'es':
                   {'short': 'seism.res.'
                   ,'title': 'Seismic resistance'
                   }
               ,'uk':
                   {'short': 'сейсм.спор.'
                   ,'title': 'Сейсмостійкість споруд'
                   }
               }
           ,'sel.breed.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'sel.breed.'
                   ,'title': 'Selective breeding'
                   }
               ,'ru':
                   {'short': 'сел.'
                   ,'title': 'Селекция'
                   }
               ,'de':
                   {'short': 'sel.breed.'
                   ,'title': 'Selective breeding'
                   }
               ,'es':
                   {'short': 'sel.breed.'
                   ,'title': 'Selective breeding'
                   }
               ,'uk':
                   {'short': 'селек.'
                   ,'title': 'Селекція'
                   }
               }
           ,'semant.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'semant.'
                   ,'title': 'Semantics'
                   }
               ,'ru':
                   {'short': 'семант.'
                   ,'title': 'Семантика'
                   }
               ,'de':
                   {'short': 'semant.'
                   ,'title': 'Semantics'
                   }
               ,'es':
                   {'short': 'semant.'
                   ,'title': 'Semantics'
                   }
               ,'uk':
                   {'short': 'семант.'
                   ,'title': 'Семантика'
                   }
               }
           ,'semicond.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'semicond.'
                   ,'title': 'Semiconductors'
                   }
               ,'ru':
                   {'short': 'полупр.'
                   ,'title': 'Полупроводники'
                   }
               ,'de':
                   {'short': 'Halbleit.'
                   ,'title': 'Halbleiter'
                   }
               ,'es':
                   {'short': 'semicond.'
                   ,'title': 'Semiconductors'
                   }
               ,'uk':
                   {'short': 'напівпр.'
                   ,'title': 'Напівпровідники'
                   }
               }
           ,'semiot.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'semiot.'
                   ,'title': 'Semiotics'
                   }
               ,'ru':
                   {'short': 'семиот.'
                   ,'title': 'Семиотика'
                   }
               ,'de':
                   {'short': 'semiot.'
                   ,'title': 'Semiotics'
                   }
               ,'es':
                   {'short': 'semiot.'
                   ,'title': 'Semiotics'
                   }
               ,'uk':
                   {'short': 'семіот.'
                   ,'title': 'Семіотика'
                   }
               }
           ,'sens.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'sens.'
                   ,'title': 'Sensitometry'
                   }
               ,'ru':
                   {'short': 'сенс.'
                   ,'title': 'Сенситометрия'
                   }
               ,'de':
                   {'short': 'sens.'
                   ,'title': 'Sensitometry'
                   }
               ,'es':
                   {'short': 'sens.'
                   ,'title': 'Sensitometry'
                   }
               ,'uk':
                   {'short': 'сенсит.'
                   ,'title': 'Сенситометрія'
                   }
               }
           ,'sew.':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'sew.'
                   ,'title': 'Sewing and clothing industry'
                   }
               ,'ru':
                   {'short': 'швейн.'
                   ,'title': 'Пошив одежды и швейная промышленность'
                   }
               ,'de':
                   {'short': 'Näh.'
                   ,'title': 'Bekleidungs- und Näherzeugnis-Industrie'
                   }
               ,'es':
                   {'short': 'sew.'
                   ,'title': 'Sewing and clothing industry'
                   }
               ,'uk':
                   {'short': 'швац.'
                   ,'title': 'Пошив одягу та швацька промисловість'
                   }
               }
           ,'sewage':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'sewage'
                   ,'title': 'Sewage and wastewater treatment'
                   }
               ,'ru':
                   {'short': 'кнлз.'
                   ,'title': 'Канализация и очистка сточных вод'
                   }
               ,'de':
                   {'short': 'sewage'
                   ,'title': 'Sewage and wastewater treatment'
                   }
               ,'es':
                   {'short': 'sewage'
                   ,'title': 'Sewage and wastewater treatment'
                   }
               ,'uk':
                   {'short': 'кнлз.'
                   ,'title': 'Каналізація та очищення стічних вод'
                   }
               }
           ,'sex':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'sex'
                   ,'title': 'Sex and sexual subcultures'
                   }
               ,'ru':
                   {'short': 'секс.'
                   ,'title': 'Секс и психосексуальные субкультуры'
                   }
               ,'de':
                   {'short': 'sex'
                   ,'title': 'Sexuell'
                   }
               ,'es':
                   {'short': 'sex'
                   ,'title': 'Sex and sexual subcultures'
                   }
               ,'uk':
                   {'short': 'секс.'
                   ,'title': 'Секс та психосексуальні субкультури'
                   }
               }
           ,'sexol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'sexol.'
                   ,'title': 'Sexology'
                   }
               ,'ru':
                   {'short': 'сексопат.'
                   ,'title': 'Сексопатология'
                   }
               ,'de':
                   {'short': 'Sexualpathol.'
                   ,'title': 'Sexualpathologie'
                   }
               ,'es':
                   {'short': 'sexol.'
                   ,'title': 'Sexology'
                   }
               ,'uk':
                   {'short': 'сексопат.'
                   ,'title': 'Сексопатологія'
                   }
               }
           ,'shinto.':
               {'is_valid': True
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'shinto.'
                   ,'title': 'Shinto'
                   }
               ,'ru':
                   {'short': 'синто.'
                   ,'title': 'Синтоизм'
                   }
               ,'de':
                   {'short': 'shinto.'
                   ,'title': 'Shinto'
                   }
               ,'es':
                   {'short': 'shinto.'
                   ,'title': 'Shinto'
                   }
               ,'uk':
                   {'short': 'синто'
                   ,'title': 'Синтоїзм'
                   }
               }
           ,'ship.handl.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'ship.handl.'
                   ,'title': 'Ship handling'
                   }
               ,'ru':
                   {'short': 'корабл.'
                   ,'title': 'Кораблевождение'
                   }
               ,'de':
                   {'short': 'ship.handl.'
                   ,'title': 'Ship handling'
                   }
               ,'es':
                   {'short': 'ship.handl.'
                   ,'title': 'Ship handling'
                   }
               ,'uk':
                   {'short': 'корабл.'
                   ,'title': 'Кораблеводіння'
                   }
               }
           ,'shipb.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'shipb.'
                   ,'title': 'Shipbuilding'
                   }
               ,'ru':
                   {'short': 'судостр.'
                   ,'title': 'Судостроение'
                   }
               ,'de':
                   {'short': 'shipb.'
                   ,'title': 'Shipbuilding'
                   }
               ,'es':
                   {'short': 'shipb.'
                   ,'title': 'Shipbuilding'
                   }
               ,'uk':
                   {'short': 'суднобуд.'
                   ,'title': 'Суднобудування'
                   }
               }
           ,'shoot.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'shoot.'
                   ,'title': 'Shooting sport'
                   }
               ,'ru':
                   {'short': 'стрелк.спорт.'
                   ,'title': 'Стрелковый спорт'
                   }
               ,'de':
                   {'short': 'shoot.'
                   ,'title': 'Shooting sport'
                   }
               ,'es':
                   {'short': 'shoot.'
                   ,'title': 'Shooting sport'
                   }
               ,'uk':
                   {'short': 'стріл.сп.'
                   ,'title': 'Стрілецький спорт'
                   }
               }
           ,'show.biz.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'show.biz.'
                   ,'title': 'Show business'
                   }
               ,'ru':
                   {'short': 'шоу.биз.'
                   ,'title': 'Шоу-бизнес (индустрия развлечений)'
                   }
               ,'de':
                   {'short': 'show.biz.'
                   ,'title': 'Show business'
                   }
               ,'es':
                   {'short': 'show.biz.'
                   ,'title': 'Show business'
                   }
               ,'uk':
                   {'short': 'шоу-біз.'
                   ,'title': 'Шоу-бізнес'
                   }
               }
           ,'signall.':
               {'is_valid': True
               ,'major_en': 'Security systems'
               ,'is_major': False
               ,'en':
                   {'short': 'signall.'
                   ,'title': 'Signalling'
                   }
               ,'ru':
                   {'short': 'сигн.'
                   ,'title': 'Сигнализация'
                   }
               ,'de':
                   {'short': 'signall.'
                   ,'title': 'Signalling'
                   }
               ,'es':
                   {'short': 'signall.'
                   ,'title': 'Signalling'
                   }
               ,'uk':
                   {'short': 'сигн.'
                   ,'title': 'Сигналізація'
                   }
               }
           ,'silic.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'silic.'
                   ,'title': 'Silicate industry'
                   }
               ,'ru':
                   {'short': 'силик.'
                   ,'title': 'Силикатная промышленность'
                   }
               ,'de':
                   {'short': 'Silikatprod.'
                   ,'title': 'Silikatproduktion'
                   }
               ,'es':
                   {'short': 'silic.'
                   ,'title': 'Silicate industry'
                   }
               ,'uk':
                   {'short': 'силік.'
                   ,'title': 'Силікатна промисловість'
                   }
               }
           ,'ski.jump.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'ski.jump.'
                   ,'title': 'Ski jumping'
                   }
               ,'ru':
                   {'short': 'прыж.трампл.'
                   ,'title': 'Прыжки с трамплина'
                   }
               ,'de':
                   {'short': 'ski.jump.'
                   ,'title': 'Ski jumping'
                   }
               ,'es':
                   {'short': 'ski.jump.'
                   ,'title': 'Ski jumping'
                   }
               ,'uk':
                   {'short': 'стриб.трампл.'
                   ,'title': 'Стрибки з трампліна'
                   }
               }
           ,'skiing':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'skiing'
                   ,'title': 'Skiing'
                   }
               ,'ru':
                   {'short': 'лыжн.спорт.'
                   ,'title': 'Лыжный спорт'
                   }
               ,'de':
                   {'short': 'skiing'
                   ,'title': 'Skiing'
                   }
               ,'es':
                   {'short': 'skiing'
                   ,'title': 'Skiing'
                   }
               ,'uk':
                   {'short': 'лиж.'
                   ,'title': 'Лижний спорт'
                   }
               }
           ,'skydive.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'skydive.'
                   ,'title': 'Skydiving'
                   }
               ,'ru':
                   {'short': 'параш.спорт.'
                   ,'title': 'Прыжки с парашютом'
                   }
               ,'de':
                   {'short': 'skydive.'
                   ,'title': 'Skydiving'
                   }
               ,'es':
                   {'short': 'skydive.'
                   ,'title': 'Skydiving'
                   }
               ,'uk':
                   {'short': 'парашут.'
                   ,'title': 'Стрибки з парашутом'
                   }
               }
           ,'sl., drug.':
               {'is_valid': False
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'sl., drug.'
                   ,'title': 'Drug-related slang'
                   }
               ,'ru':
                   {'short': 'нарк.жарг.'
                   ,'title': 'Жаргон наркоманов'
                   }
               ,'de':
                   {'short': 'Drogen.sl.'
                   ,'title': 'Drogensüchtigenslang'
                   }
               ,'es':
                   {'short': 'sl., drug.'
                   ,'title': 'Drug-related slang'
                   }
               ,'uk':
                   {'short': 'нарк.жарг.'
                   ,'title': 'Жаргон наркоманів'
                   }
               }
           ,'sl., teen.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'sl., teen.'
                   ,'title': 'Teenager slang'
                   }
               ,'ru':
                   {'short': 'сл., молод.'
                   ,'title': 'Молодёжный сленг'
                   }
               ,'de':
                   {'short': 'Jug.spr.'
                   ,'title': 'Jugendsprache'
                   }
               ,'es':
                   {'short': 'sl., teen.'
                   ,'title': 'Teenager slang'
                   }
               ,'uk':
                   {'short': 'сл., молод.'
                   ,'title': 'Молодіжний сленг'
                   }
               }
           ,'slang':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'slang'
                   ,'title': 'Slang'
                   }
               ,'ru':
                   {'short': 'сл.'
                   ,'title': 'Сленг'
                   }
               ,'de':
                   {'short': 'Slang.'
                   ,'title': 'Slang'
                   }
               ,'es':
                   {'short': 'jerg.'
                   ,'title': 'Jerga'
                   }
               ,'uk':
                   {'short': 'сленг'
                   ,'title': 'Сленг'
                   }
               }
           ,'sms':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'sms'
                   ,'title': 'Short message service'
                   }
               ,'ru':
                   {'short': 'СМС.'
                   ,'title': 'Короткие текстовые сообщения'
                   }
               ,'de':
                   {'short': 'sms'
                   ,'title': 'Short message service'
                   }
               ,'es':
                   {'short': 'sms'
                   ,'title': 'Short message service'
                   }
               ,'uk':
                   {'short': 'СМС'
                   ,'title': 'СМС'
                   }
               }
           ,'snd.proc.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'snd.proc.'
                   ,'title': 'Digital sound processing'
                   }
               ,'ru':
                   {'short': 'обраб.зв.'
                   ,'title': 'Цифровая обработка звука'
                   }
               ,'de':
                   {'short': 'snd.proc.'
                   ,'title': 'Digital sound processing'
                   }
               ,'es':
                   {'short': 'snd.proc.'
                   ,'title': 'Digital sound processing'
                   }
               ,'uk':
                   {'short': 'оброб.зв.'
                   ,'title': 'Цифрова обробка звуку'
                   }
               }
           ,'snd.rec.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'snd.rec.'
                   ,'title': 'Sound recording'
                   }
               ,'ru':
                   {'short': 'звукозап.'
                   ,'title': 'Звукозапись'
                   }
               ,'de':
                   {'short': 'snd.rec.'
                   ,'title': 'Sound recording'
                   }
               ,'es':
                   {'short': 'snd.rec.'
                   ,'title': 'Sound recording'
                   }
               ,'uk':
                   {'short': 'звукозап.'
                   ,'title': 'Звукозапис'
                   }
               }
           ,'snowb.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'snowb.'
                   ,'title': 'Snowboard'
                   }
               ,'ru':
                   {'short': 'сноуб.'
                   ,'title': 'Сноуборд'
                   }
               ,'de':
                   {'short': 'snowb.'
                   ,'title': 'Snowboard'
                   }
               ,'es':
                   {'short': 'snowb.'
                   ,'title': 'Snowboard'
                   }
               ,'uk':
                   {'short': 'сноуб.'
                   ,'title': 'Сноуборд'
                   }
               }
           ,'soc.med.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'soc.med.'
                   ,'title': 'Social media'
                   }
               ,'ru':
                   {'short': 'соц.сети.'
                   ,'title': 'Социальные сети'
                   }
               ,'de':
                   {'short': 'soc.med.'
                   ,'title': 'Social media'
                   }
               ,'es':
                   {'short': 'soc.med.'
                   ,'title': 'Social media'
                   }
               ,'uk':
                   {'short': 'соц.мер.'
                   ,'title': 'Соціальні мережі'
                   }
               }
           ,'social.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'social.'
                   ,'title': 'Socialism'
                   }
               ,'ru':
                   {'short': 'соц.'
                   ,'title': 'Социализм'
                   }
               ,'de':
                   {'short': 'Soz.'
                   ,'title': 'Sozialismus'
                   }
               ,'es':
                   {'short': 'social.'
                   ,'title': 'Socialism'
                   }
               ,'uk':
                   {'short': 'соц.'
                   ,'title': 'Соціалізм'
                   }
               }
           ,'sociol.':
               {'is_valid': True
               ,'major_en': 'Sociology'
               ,'is_major': True
               ,'en':
                   {'short': 'sociol.'
                   ,'title': 'Sociology'
                   }
               ,'ru':
                   {'short': 'социол.'
                   ,'title': 'Социология'
                   }
               ,'de':
                   {'short': 'Soziol.'
                   ,'title': 'Soziologie'
                   }
               ,'es':
                   {'short': 'sociol.'
                   ,'title': 'Sociology'
                   }
               ,'uk':
                   {'short': 'соціол.'
                   ,'title': 'Соціологія'
                   }
               }
           ,'socioling.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'socioling.'
                   ,'title': 'Sociolinguistics'
                   }
               ,'ru':
                   {'short': 'социолингв.'
                   ,'title': 'Социолингвистика'
                   }
               ,'de':
                   {'short': 'socioling.'
                   ,'title': 'Sociolinguistics'
                   }
               ,'es':
                   {'short': 'socioling.'
                   ,'title': 'Sociolinguistics'
                   }
               ,'uk':
                   {'short': 'соціолінгв.'
                   ,'title': 'Соціолінгвістика'
                   }
               }
           ,'softw.':
               {'is_valid': True
               ,'major_en': 'Computing'
               ,'is_major': False
               ,'en':
                   {'short': 'softw.'
                   ,'title': 'Software'
                   }
               ,'ru':
                   {'short': 'ПО.'
                   ,'title': 'Программное обеспечение'
                   }
               ,'de':
                   {'short': 'softw.'
                   ,'title': 'Software'
                   }
               ,'es':
                   {'short': 'softw.'
                   ,'title': 'Software'
                   }
               ,'uk':
                   {'short': 'ПЗ'
                   ,'title': 'Програмне забезпечення'
                   }
               }
           ,'soil.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'soil.'
                   ,'title': 'Soil science'
                   }
               ,'ru':
                   {'short': 'почв.'
                   ,'title': 'Почвоведение'
                   }
               ,'de':
                   {'short': 'soil.'
                   ,'title': 'Soil science'
                   }
               ,'es':
                   {'short': 'soil.'
                   ,'title': 'Soil science'
                   }
               ,'uk':
                   {'short': 'ґрунт.'
                   ,'title': 'Ґрунтознавство'
                   }
               }
           ,'soil.mech.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'soil.mech.'
                   ,'title': 'Soil mechanics'
                   }
               ,'ru':
                   {'short': 'мех.гр.'
                   ,'title': 'Механика грунтов'
                   }
               ,'de':
                   {'short': 'soil.mech.'
                   ,'title': 'Soil mechanics'
                   }
               ,'es':
                   {'short': 'soil.mech.'
                   ,'title': 'Soil mechanics'
                   }
               ,'uk':
                   {'short': 'мех.ґр.'
                   ,'title': 'Механіка ґрунтів'
                   }
               }
           ,'sol.pow.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'sol.pow.'
                   ,'title': 'Solar power'
                   }
               ,'ru':
                   {'short': 'солн.эн.'
                   ,'title': 'Солнечная энергетика'
                   }
               ,'de':
                   {'short': 'Solarenerg.'
                   ,'title': 'Solarenergie'
                   }
               ,'es':
                   {'short': 'sol.pow.'
                   ,'title': 'Solar power'
                   }
               ,'uk':
                   {'short': 'сон.енерг.'
                   ,'title': 'Сонячна енергетика'
                   }
               }
           ,'solid.st.phys.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'solid.st.phys.'
                   ,'title': 'Solid-state physics'
                   }
               ,'ru':
                   {'short': 'фтт.'
                   ,'title': 'Физика твёрдого тела'
                   }
               ,'de':
                   {'short': 'solid.st.phys.'
                   ,'title': 'Solid-state physics'
                   }
               ,'es':
                   {'short': 'solid.st.phys.'
                   ,'title': 'Solid-state physics'
                   }
               ,'uk':
                   {'short': 'фтт.'
                   ,'title': 'Фізика твердого тіла'
                   }
               }
           ,'som.':
               {'is_valid': True
               ,'major_en': 'Medicine - Alternative medicine'
               ,'is_major': False
               ,'en':
                   {'short': 'som.'
                   ,'title': 'Somatics'
                   }
               ,'ru':
                   {'short': 'сом.'
                   ,'title': 'Соматика'
                   }
               ,'de':
                   {'short': 'som.'
                   ,'title': 'Somatics'
                   }
               ,'es':
                   {'short': 'som.'
                   ,'title': 'Somatics'
                   }
               ,'uk':
                   {'short': 'сом.'
                   ,'title': 'Соматика'
                   }
               }
           ,'sound.eng.':
               {'is_valid': True
               ,'major_en': 'Cinematography'
               ,'is_major': False
               ,'en':
                   {'short': 'sound.eng.'
                   ,'title': 'Sound engineering'
                   }
               ,'ru':
                   {'short': 'зв.реж.'
                   ,'title': 'Звукорежиссура'
                   }
               ,'de':
                   {'short': 'sound.eng.'
                   ,'title': 'Sound engineering'
                   }
               ,'es':
                   {'short': 'sound.eng.'
                   ,'title': 'Sound engineering'
                   }
               ,'uk':
                   {'short': 'зв.реж.'
                   ,'title': 'Звукорежисура'
                   }
               }
           ,'south.Dutch.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'south.Dutch.'
                   ,'title': 'Southern Dutch'
                   }
               ,'ru':
                   {'short': 'южнонид.'
                   ,'title': 'Южнонидерландское выражение'
                   }
               ,'de':
                   {'short': 'south.Dutch.'
                   ,'title': 'Southern Dutch'
                   }
               ,'es':
                   {'short': 'south.Dutch.'
                   ,'title': 'Southern Dutch'
                   }
               ,'uk':
                   {'short': 'півд.нід.'
                   ,'title': 'Південнонідерландський вираз'
                   }
               }
           ,'south.afr.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'south.afr.'
                   ,'title': 'South African'
                   }
               ,'ru':
                   {'short': 'южноафр.'
                   ,'title': 'Южноафриканское выражение'
                   }
               ,'de':
                   {'short': 'Südafrik. Redewend.'
                   ,'title': 'Südafrikanische Redewendung'
                   }
               ,'es':
                   {'short': 'south.afr.'
                   ,'title': 'South African'
                   }
               ,'uk':
                   {'short': 'півд.афр.'
                   ,'title': 'Південноафриканський вираз'
                   }
               }
           ,'soviet.':
               {'is_valid': True
               ,'major_en': 'Historical'
               ,'is_major': False
               ,'en':
                   {'short': 'soviet.'
                   ,'title': 'Soviet'
                   }
               ,'ru':
                   {'short': 'советск.'
                   ,'title': 'Советский термин или реалия'
                   }
               ,'de':
                   {'short': 'Sowjet.'
                   ,'title': 'Sowjetischer Ausdruck'
                   }
               ,'es':
                   {'short': 'soviet.'
                   ,'title': 'Soviet'
                   }
               ,'uk':
                   {'short': 'радянськ.'
                   ,'title': 'Радянський термін або реалія'
                   }
               }
           ,'sp.dis.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'sp.dis.'
                   ,'title': 'Speech disorders'
                   }
               ,'ru':
                   {'short': 'расстр.реч.'
                   ,'title': 'Расстройства речи'
                   }
               ,'de':
                   {'short': 'sp.dis.'
                   ,'title': 'Speech disorders'
                   }
               ,'es':
                   {'short': 'sp.dis.'
                   ,'title': 'Speech disorders'
                   }
               ,'uk':
                   {'short': 'розл.мовл.'
                   ,'title': 'Розлади мовлення'
                   }
               }
           ,'space':
               {'is_valid': True
               ,'major_en': 'Space'
               ,'is_major': True
               ,'en':
                   {'short': 'space'
                   ,'title': 'Space'
                   }
               ,'ru':
                   {'short': 'косм.'
                   ,'title': 'Космос'
                   }
               ,'de':
                   {'short': 'weltraum'
                   ,'title': 'Weltraum'
                   }
               ,'es':
                   {'short': 'space'
                   ,'title': 'Space'
                   }
               ,'uk':
                   {'short': 'косм.'
                   ,'title': 'Космос'
                   }
               }
           ,'span.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'span.'
                   ,'title': 'Spanish'
                   }
               ,'ru':
                   {'short': 'исп.'
                   ,'title': 'Испанский язык'
                   }
               ,'de':
                   {'short': 'Span.'
                   ,'title': 'Spanisch'
                   }
               ,'es':
                   {'short': 'esp.'
                   ,'title': 'Español'
                   }
               ,'uk':
                   {'short': 'ісп.'
                   ,'title': 'Іспанська мова'
                   }
               }
           ,'span.-am.':
               {'is_valid': False
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'span.-am.'
                   ,'title': 'Spanish-American'
                   }
               ,'ru':
                   {'short': 'исп.-амер.'
                   ,'title': 'Испано-американский жаргон'
                   }
               ,'de':
                   {'short': 'Span. Amer.'
                   ,'title': 'Spanisches Amerikanisch, Jargon'
                   }
               ,'es':
                   {'short': 'hisp.-am.'
                   ,'title': 'Hispanoamericano'
                   }
               ,'uk':
                   {'short': 'ісп.-амер.'
                   ,'title': 'Іспано-американський жаргон'
                   }
               }
           ,'spectr.':
               {'is_valid': True
               ,'major_en': 'Chemistry'
               ,'is_major': False
               ,'en':
                   {'short': 'spectr.'
                   ,'title': 'Spectroscopy'
                   }
               ,'ru':
                   {'short': 'спектр.'
                   ,'title': 'Спектроскопия'
                   }
               ,'de':
                   {'short': 'spectr.'
                   ,'title': 'Spectroscopy'
                   }
               ,'es':
                   {'short': 'spectr.'
                   ,'title': 'Spectroscopy'
                   }
               ,'uk':
                   {'short': 'спектр.'
                   ,'title': 'Спектроскопія'
                   }
               }
           ,'speed.skat.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'speed.skat.'
                   ,'title': 'Speed skating'
                   }
               ,'ru':
                   {'short': 'коньк.'
                   ,'title': 'Конькобежный спорт'
                   }
               ,'de':
                   {'short': 'speed.skat.'
                   ,'title': 'Speed skating'
                   }
               ,'es':
                   {'short': 'speed.skat.'
                   ,'title': 'Speed skating'
                   }
               ,'uk':
                   {'short': 'ковз.'
                   ,'title': 'Ковзани'
                   }
               }
           ,'speleo.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'speleo.'
                   ,'title': 'Speleology'
                   }
               ,'ru':
                   {'short': 'спелеол.'
                   ,'title': 'Спелеология'
                   }
               ,'de':
                   {'short': 'speleo.'
                   ,'title': 'Speleology'
                   }
               ,'es':
                   {'short': 'speleo.'
                   ,'title': 'Speleology'
                   }
               ,'uk':
                   {'short': 'спелеол.'
                   ,'title': 'Спелеологія'
                   }
               }
           ,'spice.':
               {'is_valid': True
               ,'major_en': 'Cooking'
               ,'is_major': False
               ,'en':
                   {'short': 'spice.'
                   ,'title': 'Spices'
                   }
               ,'ru':
                   {'short': 'специи.'
                   ,'title': 'Специи'
                   }
               ,'de':
                   {'short': 'Gew.'
                   ,'title': 'Gewürze'
                   }
               ,'es':
                   {'short': 'spice.'
                   ,'title': 'Spices'
                   }
               ,'uk':
                   {'short': 'спеції'
                   ,'title': 'Спеції'
                   }
               }
           ,'spoken':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'spoken'
                   ,'title': 'Spoken'
                   }
               ,'ru':
                   {'short': 'устн.'
                   ,'title': 'Устная речь'
                   }
               ,'de':
                   {'short': 'Gesproch.'
                   ,'title': 'Gesprochene Sprache'
                   }
               ,'es':
                   {'short': 'spoken'
                   ,'title': 'Spoken'
                   }
               ,'uk':
                   {'short': 'усн.мов.'
                   ,'title': 'Усне мовлення'
                   }
               }
           ,'sport, bask.':
               {'is_valid': False
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'sport, bask.'
                   ,'title': 'Basketball'
                   }
               ,'ru':
                   {'short': 'баск.'
                   ,'title': 'Баскетбол'
                   }
               ,'de':
                   {'short': 'sport, bask.'
                   ,'title': 'Basketball'
                   }
               ,'es':
                   {'short': 'sport, bask.'
                   ,'title': 'Basketball'
                   }
               ,'uk':
                   {'short': 'спорт, баск.'
                   ,'title': 'Баскетбол'
                   }
               }
           ,'sport.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': True
               ,'en':
                   {'short': 'sport.'
                   ,'title': 'Sports'
                   }
               ,'ru':
                   {'short': 'спорт.'
                   ,'title': 'Спорт'
                   }
               ,'de':
                   {'short': 'Sport.'
                   ,'title': 'Sport'
                   }
               ,'es':
                   {'short': 'dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'st.exch.':
               {'is_valid': True
               ,'major_en': 'Finances'
               ,'is_major': False
               ,'en':
                   {'short': 'st.exch.'
                   ,'title': 'Stock Exchange'
                   }
               ,'ru':
                   {'short': 'бирж.'
                   ,'title': 'Биржевой термин'
                   }
               ,'de':
                   {'short': 'Börse.'
                   ,'title': 'Börse'
                   }
               ,'es':
                   {'short': 'burs.'
                   ,'title': 'Bursátil'
                   }
               ,'uk':
                   {'short': 'бірж.'
                   ,'title': 'Біржовий термін'
                   }
               }
           ,'starch.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'starch.'
                   ,'title': 'Starch industry'
                   }
               ,'ru':
                   {'short': 'крахм.'
                   ,'title': 'Крахмально-паточная промышленность'
                   }
               ,'de':
                   {'short': 'starch.'
                   ,'title': 'Starch industry'
                   }
               ,'es':
                   {'short': 'starch.'
                   ,'title': 'Starch industry'
                   }
               ,'uk':
                   {'short': 'крохм.'
                   ,'title': 'Крохмалепатокова промисловість'
                   }
               }
           ,'stat.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'stat.'
                   ,'title': 'Statistics'
                   }
               ,'ru':
                   {'short': 'стат.'
                   ,'title': 'Статистика'
                   }
               ,'de':
                   {'short': 'Stat.'
                   ,'title': 'Statistik'
                   }
               ,'es':
                   {'short': 'estad.'
                   ,'title': 'Estadísticas'
                   }
               ,'uk':
                   {'short': 'стат.'
                   ,'title': 'Статистика'
                   }
               }
           ,'station.':
               {'is_valid': True
               ,'major_en': 'Records management'
               ,'is_major': False
               ,'en':
                   {'short': 'station.'
                   ,'title': 'Stationery'
                   }
               ,'ru':
                   {'short': 'канц.тов.'
                   ,'title': 'Канцтовары'
                   }
               ,'de':
                   {'short': 'station.'
                   ,'title': 'Stationery'
                   }
               ,'es':
                   {'short': 'station.'
                   ,'title': 'Stationery'
                   }
               ,'uk':
                   {'short': 'канц.тов.'
                   ,'title': 'Канцтовари'
                   }
               }
           ,'stereo.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'stereo.'
                   ,'title': 'Stereo'
                   }
               ,'ru':
                   {'short': 'стерео.'
                   ,'title': 'Стерео'
                   }
               ,'de':
                   {'short': 'stereo.'
                   ,'title': 'Stereo'
                   }
               ,'es':
                   {'short': 'stereo.'
                   ,'title': 'Stereo'
                   }
               ,'uk':
                   {'short': 'стерео'
                   ,'title': 'Стерео'
                   }
               }
           ,'stmp.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'stmp.'
                   ,'title': 'Stamping'
                   }
               ,'ru':
                   {'short': 'штмп.'
                   ,'title': 'Штамповка'
                   }
               ,'de':
                   {'short': 'Stz.'
                   ,'title': 'Stanzen'
                   }
               ,'es':
                   {'short': 'stmp.'
                   ,'title': 'Stamping'
                   }
               ,'uk':
                   {'short': 'штамп.'
                   ,'title': 'Штампування'
                   }
               }
           ,'stn.mas.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'stn.mas.'
                   ,'title': 'Stonemasonry'
                   }
               ,'ru':
                   {'short': 'кам.'
                   ,'title': 'Каменные конструкции'
                   }
               ,'de':
                   {'short': 'stn.mas.'
                   ,'title': 'Stonemasonry'
                   }
               ,'es':
                   {'short': 'stn.mas.'
                   ,'title': 'Stonemasonry'
                   }
               ,'uk':
                   {'short': 'кам.'
                   ,'title': 'Кам’яні конструкції'
                   }
               }
           ,'str.mater.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'str.mater.'
                   ,'title': 'Strength of materials'
                   }
               ,'ru':
                   {'short': 'сопромат.'
                   ,'title': 'Сопротивление материалов'
                   }
               ,'de':
                   {'short': 'Werkstoffwiderst.'
                   ,'title': 'Werkstoffwiderstand'
                   }
               ,'es':
                   {'short': 'str.mater.'
                   ,'title': 'Strength of materials'
                   }
               ,'uk':
                   {'short': 'оп.мат.'
                   ,'title': 'Опір матеріалів'
                   }
               }
           ,'strat.plast.':
               {'is_valid': True
               ,'major_en': 'Chemical industry'
               ,'is_major': False
               ,'en':
                   {'short': 'strat.plast.'
                   ,'title': 'Stratified plastics'
                   }
               ,'ru':
                   {'short': 'слоист.пл.'
                   ,'title': 'Слоистые пластики'
                   }
               ,'de':
                   {'short': 'Schichtpress.'
                   ,'title': 'Schichtpressstoffe'
                   }
               ,'es':
                   {'short': 'strat.plast.'
                   ,'title': 'Stratified plastics'
                   }
               ,'uk':
                   {'short': 'шар.пласт.'
                   ,'title': 'Шаруваті пластики'
                   }
               }
           ,'stratigr.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'stratigr.'
                   ,'title': 'Stratigraphy'
                   }
               ,'ru':
                   {'short': 'страт.'
                   ,'title': 'Стратиграфия'
                   }
               ,'de':
                   {'short': 'Stratigr.'
                   ,'title': 'Stratigraphie'
                   }
               ,'es':
                   {'short': 'stratigr.'
                   ,'title': 'Stratigraphy'
                   }
               ,'uk':
                   {'short': 'страт.'
                   ,'title': 'Стратиграфія'
                   }
               }
           ,'stylist.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'stylist.'
                   ,'title': 'Stylistics'
                   }
               ,'ru':
                   {'short': 'стилист.'
                   ,'title': 'Стилистика'
                   }
               ,'de':
                   {'short': 'Stilist.'
                   ,'title': 'Stilistik'
                   }
               ,'es':
                   {'short': 'estilíst.'
                   ,'title': 'Estilística'
                   }
               ,'uk':
                   {'short': 'стил.'
                   ,'title': 'Стилістика'
                   }
               }
           ,'subl.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'subl.'
                   ,'title': 'Sublime'
                   }
               ,'ru':
                   {'short': 'возвыш.'
                   ,'title': 'Возвышенное выражение'
                   }
               ,'de':
                   {'short': 'Gehob.'
                   ,'title': 'Gehoben'
                   }
               ,'es':
                   {'short': 'subl.'
                   ,'title': 'Sublime'
                   }
               ,'uk':
                   {'short': 'піднес.'
                   ,'title': 'Піднесений вираз'
                   }
               }
           ,'subm.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'subm.'
                   ,'title': 'Submarines'
                   }
               ,'ru':
                   {'short': 'подв.'
                   ,'title': 'Подводные лодки'
                   }
               ,'de':
                   {'short': 'subm.'
                   ,'title': 'Submarines'
                   }
               ,'es':
                   {'short': 'subm.'
                   ,'title': 'Submarines'
                   }
               ,'uk':
                   {'short': 'підвод.'
                   ,'title': 'Підводні човни'
                   }
               }
           ,'sugar.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'sugar.'
                   ,'title': 'Sugar production'
                   }
               ,'ru':
                   {'short': 'сахар.'
                   ,'title': 'Сахарное производство'
                   }
               ,'de':
                   {'short': 'Zucker.'
                   ,'title': 'Zuckerproduktion'
                   }
               ,'es':
                   {'short': 'sugar.'
                   ,'title': 'Sugar production'
                   }
               ,'uk':
                   {'short': 'цукр.'
                   ,'title': 'Цукрове виробництво'
                   }
               }
           ,'supercond.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'supercond.'
                   ,'title': 'Superconductivity'
                   }
               ,'ru':
                   {'short': 'сверхпров.'
                   ,'title': 'Сверхпроводимость'
                   }
               ,'de':
                   {'short': 'Supraleit.'
                   ,'title': 'Supraleitfähigkeit'
                   }
               ,'es':
                   {'short': 'supercond.'
                   ,'title': 'Superconductivity'
                   }
               ,'uk':
                   {'short': 'надпров.'
                   ,'title': 'Надпровідність'
                   }
               }
           ,'superl.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'superl.'
                   ,'title': 'Superlative'
                   }
               ,'ru':
                   {'short': 'превосх.'
                   ,'title': 'Превосходная степень'
                   }
               ,'de':
                   {'short': 'superl.'
                   ,'title': 'Superlative'
                   }
               ,'es':
                   {'short': 'superl.'
                   ,'title': 'Superlative'
                   }
               ,'uk':
                   {'short': 'найв.ст.'
                   ,'title': 'Найвищий ступінь'
                   }
               }
           ,'surg.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'surg.'
                   ,'title': 'Surgery'
                   }
               ,'ru':
                   {'short': 'хир.'
                   ,'title': 'Хирургия'
                   }
               ,'de':
                   {'short': 'Chirurg.'
                   ,'title': 'Chirurgie'
                   }
               ,'es':
                   {'short': 'cirug.'
                   ,'title': 'Cirugía'
                   }
               ,'uk':
                   {'short': 'хір.'
                   ,'title': 'Хірургія'
                   }
               }
           ,'surn.':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': False
               ,'en':
                   {'short': 'surn.'
                   ,'title': 'Surname'
                   }
               ,'ru':
                   {'short': 'фамил.'
                   ,'title': 'Фамилия'
                   }
               ,'de':
                   {'short': 'surn.'
                   ,'title': 'Surname'
                   }
               ,'es':
                   {'short': 'surn.'
                   ,'title': 'Surname'
                   }
               ,'uk':
                   {'short': 'прізвищ.'
                   ,'title': 'Прізвище'
                   }
               }
           ,'survey.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'survey.'
                   ,'title': 'Surveying'
                   }
               ,'ru':
                   {'short': 'геод.'
                   ,'title': 'Геодезия'
                   }
               ,'de':
                   {'short': 'Landvermes.'
                   ,'title': 'Landvermessung'
                   }
               ,'es':
                   {'short': 'geod.'
                   ,'title': 'Geodesia'
                   }
               ,'uk':
                   {'short': 'геод.'
                   ,'title': 'Геодезія'
                   }
               }
           ,'svc.ind.':
               {'is_valid': True
               ,'major_en': 'Service industry'
               ,'is_major': True
               ,'en':
                   {'short': 'svc.ind.'
                   ,'title': 'Service industry'
                   }
               ,'ru':
                   {'short': 'сф.обсл.'
                   ,'title': 'Сфера обслуживания'
                   }
               ,'de':
                   {'short': 'Dienstind.'
                   ,'title': 'Dienstleistungsindustrie'
                   }
               ,'es':
                   {'short': 'svc.ind.'
                   ,'title': 'Service industry'
                   }
               ,'uk':
                   {'short': 'сф.обсл.'
                   ,'title': 'Сфера обслуговування'
                   }
               }
           ,'swed.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'swed.'
                   ,'title': 'Swedish'
                   }
               ,'ru':
                   {'short': 'шведск.'
                   ,'title': 'Шведский язык'
                   }
               ,'de':
                   {'short': 'Schwed.'
                   ,'title': 'Schwedisch'
                   }
               ,'es':
                   {'short': 'swed.'
                   ,'title': 'Swedish'
                   }
               ,'uk':
                   {'short': 'швед.'
                   ,'title': 'Шведська мова'
                   }
               }
           ,'swim.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'swim.'
                   ,'title': 'Swimming'
                   }
               ,'ru':
                   {'short': 'плав.'
                   ,'title': 'Плавание'
                   }
               ,'de':
                   {'short': 'swim.'
                   ,'title': 'Swimming'
                   }
               ,'es':
                   {'short': 'swim.'
                   ,'title': 'Swimming'
                   }
               ,'uk':
                   {'short': 'плав.'
                   ,'title': 'Плавання'
                   }
               }
           ,'swiss.':
               {'is_valid': True
               ,'major_en': 'Regional usage (other than language varieties)'
               ,'is_major': False
               ,'en':
                   {'short': 'swiss.'
                   ,'title': 'Swiss term'
                   }
               ,'ru':
                   {'short': 'швейц.'
                   ,'title': 'Швейцарское выражение'
                   }
               ,'de':
                   {'short': 'Schweiz'
                   ,'title': 'Schwizerdütsch'
                   }
               ,'es':
                   {'short': 'swiss.'
                   ,'title': 'Swiss term'
                   }
               ,'uk':
                   {'short': 'швейц.'
                   ,'title': 'Швейцарський вираз'
                   }
               }
           ,'swtch.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'swtch.'
                   ,'title': 'Switches'
                   }
               ,'ru':
                   {'short': 'перекл.'
                   ,'title': 'Переключатели'
                   }
               ,'de':
                   {'short': 'swtch.'
                   ,'title': 'Switches'
                   }
               ,'es':
                   {'short': 'swtch.'
                   ,'title': 'Switches'
                   }
               ,'uk':
                   {'short': 'вимик.'
                   ,'title': 'Вимикачі'
                   }
               }
           ,'synt.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'synt.'
                   ,'title': 'Syntax'
                   }
               ,'ru':
                   {'short': 'синт.'
                   ,'title': 'Синтаксис'
                   }
               ,'de':
                   {'short': 'synt.'
                   ,'title': 'Syntax'
                   }
               ,'es':
                   {'short': 'synt.'
                   ,'title': 'Syntax'
                   }
               ,'uk':
                   {'short': 'синт.'
                   ,'title': 'Синтаксис'
                   }
               }
           ,'tab.tenn.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'tab.tenn.'
                   ,'title': 'Table tennis'
                   }
               ,'ru':
                   {'short': 'наст.тенн.'
                   ,'title': 'Настольный теннис'
                   }
               ,'de':
                   {'short': 'tab.tenn.'
                   ,'title': 'Table tennis'
                   }
               ,'es':
                   {'short': 'tab.tenn.'
                   ,'title': 'Table tennis'
                   }
               ,'uk':
                   {'short': 'н.тенн.'
                   ,'title': 'Настільний теніс'
                   }
               }
           ,'tabl.game':
               {'is_valid': True
               ,'major_en': 'Games (other than sports)'
               ,'is_major': False
               ,'en':
                   {'short': 'tabl.game'
                   ,'title': 'Tabletop games'
                   }
               ,'ru':
                   {'short': 'наст.игр.'
                   ,'title': 'Настольные игры'
                   }
               ,'de':
                   {'short': 'Brtsp.'
                   ,'title': 'Brettspiele'
                   }
               ,'es':
                   {'short': 'tabl.game'
                   ,'title': 'Tabletop games'
                   }
               ,'uk':
                   {'short': 'наст.ірг.'
                   ,'title': 'Настільні ігри'
                   }
               }
           ,'taboo':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'taboo'
                   ,'title': 'Taboo expressions and obscenities'
                   }
               ,'ru':
                   {'short': 'табу.'
                   ,'title': 'Табуированная (обсценная) лексика'
                   }
               ,'de':
                   {'short': 'taboo'
                   ,'title': 'Taboo expressions and obscenities'
                   }
               ,'es':
                   {'short': 'taboo'
                   ,'title': 'Taboo expressions and obscenities'
                   }
               ,'uk':
                   {'short': 'табу.'
                   ,'title': 'Табуйована (обсценна) лексика'
                   }
               }
           ,'taboo, amer.usg., black.sl., slang':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'taboo, amer.usg., black.sl., slang'
                   ,'title': 'Taboo expressions and obscenities, American (usage, not AmE), Black slang, Slang'
                   }
               ,'ru':
                   {'short': 'табу., амер., негр., сл.'
                   ,'title': 'Табуированная (обсценная) лексика, Американское выражение (не вариант языка), Негритянский жаргон, Сленг'
                   }
               ,'de':
                   {'short': 'taboo, Amerik., Neg.Slang, Slang.'
                   ,'title': 'Taboo expressions and obscenities, Amerikanisch, Negerslang, Slang'
                   }
               ,'es':
                   {'short': 'taboo, amer., black.sl., jerg.'
                   ,'title': 'Taboo expressions and obscenities, Americano (uso), Black slang, Jerga'
                   }
               ,'uk':
                   {'short': 'табу., амер.вир., негр., сленг'
                   ,'title': 'Табуйована (обсценна) лексика, Американський вираз (не варыант мови), Негритянський жаргон, Сленг'
                   }
               }
           ,'taiw.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'taiw.'
                   ,'title': 'Taiwan'
                   }
               ,'ru':
                   {'short': 'тайв.'
                   ,'title': 'Тайвань'
                   }
               ,'de':
                   {'short': 'taiw.'
                   ,'title': 'Taiwan'
                   }
               ,'es':
                   {'short': 'taiw.'
                   ,'title': 'Taiwan'
                   }
               ,'uk':
                   {'short': 'тайв.'
                   ,'title': 'Тайвань'
                   }
               }
           ,'tao.':
               {'is_valid': False
               ,'major_en': 'Religion'
               ,'is_major': False
               ,'en':
                   {'short': 'tao.'
                   ,'title': 'Taoism'
                   }
               ,'ru':
                   {'short': 'рел., даос.'
                   ,'title': 'Даосизм'
                   }
               ,'de':
                   {'short': 'tao.'
                   ,'title': 'Taoism'
                   }
               ,'es':
                   {'short': 'tao.'
                   ,'title': 'Taoism'
                   }
               ,'uk':
                   {'short': 'даос.'
                   ,'title': 'Даосизм'
                   }
               }
           ,'tat.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'tat.'
                   ,'title': 'Tatar'
                   }
               ,'ru':
                   {'short': 'татарск.'
                   ,'title': 'Татарский язык'
                   }
               ,'de':
                   {'short': 'tat.'
                   ,'title': 'Tatar'
                   }
               ,'es':
                   {'short': 'tat.'
                   ,'title': 'Tatar'
                   }
               ,'uk':
                   {'short': 'татарськ.'
                   ,'title': 'Татарська мова'
                   }
               }
           ,'taur.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'taur.'
                   ,'title': 'Tauromachy'
                   }
               ,'ru':
                   {'short': 'тавромах.'
                   ,'title': 'Тавромахия'
                   }
               ,'de':
                   {'short': 'taur.'
                   ,'title': 'Tauromachy'
                   }
               ,'es':
                   {'short': 'taur.'
                   ,'title': 'Tauromachy'
                   }
               ,'uk':
                   {'short': 'тавромах.'
                   ,'title': 'Тавромахія'
                   }
               }
           ,'tax.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'tax.'
                   ,'title': 'Taxes'
                   }
               ,'ru':
                   {'short': 'налог.'
                   ,'title': 'Налоги'
                   }
               ,'de':
                   {'short': 'Steuer.'
                   ,'title': 'Steuern'
                   }
               ,'es':
                   {'short': 'tax.'
                   ,'title': 'Taxes'
                   }
               ,'uk':
                   {'short': 'под.'
                   ,'title': 'Податки'
                   }
               }
           ,'tech.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': True
               ,'en':
                   {'short': 'tech.'
                   ,'title': 'Technology'
                   }
               ,'ru':
                   {'short': 'тех.'
                   ,'title': 'Техника'
                   }
               ,'de':
                   {'short': 'Tech.'
                   ,'title': 'Technik'
                   }
               ,'es':
                   {'short': 'tec.'
                   ,'title': 'Tecnología'
                   }
               ,'uk':
                   {'short': 'техн.'
                   ,'title': 'Техніка'
                   }
               }
           ,'tecton.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'tecton.'
                   ,'title': 'Tectonics'
                   }
               ,'ru':
                   {'short': 'тект.'
                   ,'title': 'Тектоника'
                   }
               ,'de':
                   {'short': 'Tekton.'
                   ,'title': 'Tektonik'
                   }
               ,'es':
                   {'short': 'tecton.'
                   ,'title': 'Tectonics'
                   }
               ,'uk':
                   {'short': 'тект.'
                   ,'title': 'Тектоніка'
                   }
               }
           ,'tel.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'tel.'
                   ,'title': 'Telephony'
                   }
               ,'ru':
                   {'short': 'тлф.'
                   ,'title': 'Телефония'
                   }
               ,'de':
                   {'short': 'Telef.'
                   ,'title': 'Telefonie'
                   }
               ,'es':
                   {'short': 'tel.'
                   ,'title': 'Telephony'
                   }
               ,'uk':
                   {'short': 'тлф.'
                   ,'title': 'Телефонія'
                   }
               }
           ,'tel.mech.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'tel.mech.'
                   ,'title': 'Telemechanics'
                   }
               ,'ru':
                   {'short': 'тлм.'
                   ,'title': 'Телемеханика'
                   }
               ,'de':
                   {'short': 'tel.mech.'
                   ,'title': 'Telemechanics'
                   }
               ,'es':
                   {'short': 'tel.mech.'
                   ,'title': 'Telemechanics'
                   }
               ,'uk':
                   {'short': 'тлм.'
                   ,'title': 'Телемеханіка'
                   }
               }
           ,'telecom.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'telecom.'
                   ,'title': 'Telecommunications'
                   }
               ,'ru':
                   {'short': 'телеком.'
                   ,'title': 'Телекоммуникации'
                   }
               ,'de':
                   {'short': 'Telekomm.'
                   ,'title': 'Telekommunikation'
                   }
               ,'es':
                   {'short': 'telecom.'
                   ,'title': 'Telecomunicación'
                   }
               ,'uk':
                   {'short': 'телеком.'
                   ,'title': 'Телекомунікації'
                   }
               }
           ,'telegr.':
               {'is_valid': True
               ,'major_en': 'Communications'
               ,'is_major': False
               ,'en':
                   {'short': 'telegr.'
                   ,'title': 'Telegraphy'
                   }
               ,'ru':
                   {'short': 'телегр.'
                   ,'title': 'Телеграфия'
                   }
               ,'de':
                   {'short': 'Telegr.'
                   ,'title': 'Telegrafie'
                   }
               ,'es':
                   {'short': 'telegr.'
                   ,'title': 'Telegraphy'
                   }
               ,'uk':
                   {'short': 'телегр.'
                   ,'title': 'Телеграфія'
                   }
               }
           ,'tenn.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'tenn.'
                   ,'title': 'Tennis'
                   }
               ,'ru':
                   {'short': 'тенн.'
                   ,'title': 'Теннис'
                   }
               ,'de':
                   {'short': 'tenn.'
                   ,'title': 'Tennis'
                   }
               ,'es':
                   {'short': 'tenn.'
                   ,'title': 'Tennis'
                   }
               ,'uk':
                   {'short': 'теніс'
                   ,'title': 'Теніс'
                   }
               }
           ,'textile':
               {'is_valid': True
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'textile'
                   ,'title': 'Textile industry'
                   }
               ,'ru':
                   {'short': 'текст.'
                   ,'title': 'Текстильная промышленность'
                   }
               ,'de':
                   {'short': 'Textil'
                   ,'title': 'Textil'
                   }
               ,'es':
                   {'short': 'textil'
                   ,'title': 'Industria textil'
                   }
               ,'uk':
                   {'short': 'текстиль.'
                   ,'title': 'Текстиль'
                   }
               }
           ,'thai.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'thai.'
                   ,'title': 'Thai'
                   }
               ,'ru':
                   {'short': 'тайск.'
                   ,'title': 'Тайский язык'
                   }
               ,'de':
                   {'short': 'thai.'
                   ,'title': 'Thai'
                   }
               ,'es':
                   {'short': 'thai.'
                   ,'title': 'Thai'
                   }
               ,'uk':
                   {'short': 'тайськ.'
                   ,'title': 'Тайська мова'
                   }
               }
           ,'theatre.':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'theatre.'
                   ,'title': 'Theatre'
                   }
               ,'ru':
                   {'short': 'театр.'
                   ,'title': 'Театр'
                   }
               ,'de':
                   {'short': 'Theater.'
                   ,'title': 'Theater'
                   }
               ,'es':
                   {'short': 'teatr.'
                   ,'title': 'Teatro'
                   }
               ,'uk':
                   {'short': 'театр.'
                   ,'title': 'Театр'
                   }
               }
           ,'therm.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'therm.'
                   ,'title': 'Thermodynamics'
                   }
               ,'ru':
                   {'short': 'терм.'
                   ,'title': 'Термодинамика'
                   }
               ,'de':
                   {'short': 'therm.'
                   ,'title': 'Thermodynamics'
                   }
               ,'es':
                   {'short': 'therm.'
                   ,'title': 'Thermodynamics'
                   }
               ,'uk':
                   {'short': 'терм.'
                   ,'title': 'Термодинаміка'
                   }
               }
           ,'therm.energ.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'therm.energ.'
                   ,'title': 'Thermal Energy'
                   }
               ,'ru':
                   {'short': 'тепл.энерг.'
                   ,'title': 'Теплоэнергетика'
                   }
               ,'de':
                   {'short': 'therm.energ.'
                   ,'title': 'Thermal Energy'
                   }
               ,'es':
                   {'short': 'therm.energ.'
                   ,'title': 'Thermal Energy'
                   }
               ,'uk':
                   {'short': 'тепл.енерг.'
                   ,'title': 'Теплоенергетика'
                   }
               }
           ,'therm.eng.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'therm.eng.'
                   ,'title': 'Thermal engineering'
                   }
               ,'ru':
                   {'short': 'тепл.'
                   ,'title': 'Теплотехника'
                   }
               ,'de':
                   {'short': 'Wärmetech.'
                   ,'title': 'Wärmetechnik'
                   }
               ,'es':
                   {'short': 'therm.eng.'
                   ,'title': 'Thermal engineering'
                   }
               ,'uk':
                   {'short': 'тепл.'
                   ,'title': 'Теплотехніка'
                   }
               }
           ,'timb.float.':
               {'is_valid': True
               ,'major_en': 'Wood, pulp and paper industries'
               ,'is_major': False
               ,'en':
                   {'short': 'timb.float.'
                   ,'title': 'Timber floating'
                   }
               ,'ru':
                   {'short': 'лесоспл.'
                   ,'title': 'Лесосплав'
                   }
               ,'de':
                   {'short': 'Flöß.'
                   ,'title': 'Flößerei'
                   }
               ,'es':
                   {'short': 'timb.float.'
                   ,'title': 'Timber floating'
                   }
               ,'uk':
                   {'short': 'лісоспл.'
                   ,'title': 'Лісосплав'
                   }
               }
           ,'tin.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'tin.'
                   ,'title': 'Tinware'
                   }
               ,'ru':
                   {'short': 'жест.'
                   ,'title': 'Жестяные изделия'
                   }
               ,'de':
                   {'short': 'tin.'
                   ,'title': 'Tinware'
                   }
               ,'es':
                   {'short': 'tin.'
                   ,'title': 'Tinware'
                   }
               ,'uk':
                   {'short': 'бляш.вир'
                   ,'title': 'Бляшані вироби'
                   }
               }
           ,'tirk.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'tirk.'
                   ,'title': 'Turk'
                   }
               ,'ru':
                   {'short': 'тюрк.'
                   ,'title': 'Тюркские языки'
                   }
               ,'de':
                   {'short': 'Turksp.'
                   ,'title': 'Turksprachen'
                   }
               ,'es':
                   {'short': 'tirk.'
                   ,'title': 'Turk'
                   }
               ,'uk':
                   {'short': 'тюрк.'
                   ,'title': 'Тюркські мови'
                   }
               }
           ,'titles':
               {'is_valid': True
               ,'major_en': 'Art and culture (n.e.s.)'
               ,'is_major': False
               ,'en':
                   {'short': 'titles'
                   ,'title': 'Titles of works of art'
                   }
               ,'ru':
                   {'short': 'назв.произв.'
                   ,'title': 'Название произведения'
                   }
               ,'de':
                   {'short': 'titles'
                   ,'title': 'Titles of works of art'
                   }
               ,'es':
                   {'short': 'titles'
                   ,'title': 'Titles of works of art'
                   }
               ,'uk':
                   {'short': 'назв.тв.'
                   ,'title': 'Назва твору'
                   }
               }
           ,'tobac.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'tobac.'
                   ,'title': 'Tobacco industry'
                   }
               ,'ru':
                   {'short': 'таб.'
                   ,'title': 'Табачная промышленность'
                   }
               ,'de':
                   {'short': 'tobac.'
                   ,'title': 'Tobacco industry'
                   }
               ,'es':
                   {'short': 'tobac.'
                   ,'title': 'Tobacco industry'
                   }
               ,'uk':
                   {'short': 'тютюн.'
                   ,'title': 'Тютюнова промисловість'
                   }
               }
           ,'tools':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'tools'
                   ,'title': 'Tools'
                   }
               ,'ru':
                   {'short': 'инстр.'
                   ,'title': 'Инструменты'
                   }
               ,'de':
                   {'short': 'Wzg.'
                   ,'title': 'Werkzeuge'
                   }
               ,'es':
                   {'short': 'tools'
                   ,'title': 'Tools'
                   }
               ,'uk':
                   {'short': 'інстр.'
                   ,'title': 'Інструменти'
                   }
               }
           ,'topogr.':
               {'is_valid': True
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'topogr.'
                   ,'title': 'Topography'
                   }
               ,'ru':
                   {'short': 'топогр.'
                   ,'title': 'Топография'
                   }
               ,'de':
                   {'short': 'Topogr.'
                   ,'title': 'Topographie'
                   }
               ,'es':
                   {'short': 'topogr.'
                   ,'title': 'Topografía'
                   }
               ,'uk':
                   {'short': 'топ.'
                   ,'title': 'Топографія'
                   }
               }
           ,'topol.':
               {'is_valid': True
               ,'major_en': 'Mathematics'
               ,'is_major': False
               ,'en':
                   {'short': 'topol.'
                   ,'title': 'Topology'
                   }
               ,'ru':
                   {'short': 'топол.'
                   ,'title': 'Топология'
                   }
               ,'de':
                   {'short': 'Topol.'
                   ,'title': 'Topologie'
                   }
               ,'es':
                   {'short': 'topol.'
                   ,'title': 'Topology'
                   }
               ,'uk':
                   {'short': 'топол.'
                   ,'title': 'Топологія'
                   }
               }
           ,'topon.':
               {'is_valid': True
               ,'major_en': 'Proper name'
               ,'is_major': False
               ,'en':
                   {'short': 'topon.'
                   ,'title': 'Toponym'
                   }
               ,'ru':
                   {'short': 'топон.'
                   ,'title': 'Топоним'
                   }
               ,'de':
                   {'short': 'topon.'
                   ,'title': 'Toponym'
                   }
               ,'es':
                   {'short': 'topon.'
                   ,'title': 'Toponym'
                   }
               ,'uk':
                   {'short': 'топон.'
                   ,'title': 'Топонім'
                   }
               }
           ,'torped.':
               {'is_valid': True
               ,'major_en': 'Military'
               ,'is_major': False
               ,'en':
                   {'short': 'torped.'
                   ,'title': 'Torpedoes'
                   }
               ,'ru':
                   {'short': 'торп.'
                   ,'title': 'Торпеды'
                   }
               ,'de':
                   {'short': 'torped.'
                   ,'title': 'Torpedoes'
                   }
               ,'es':
                   {'short': 'torped.'
                   ,'title': 'Torpedoes'
                   }
               ,'uk':
                   {'short': 'торп.'
                   ,'title': 'Торпеди'
                   }
               }
           ,'toxicol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'toxicol.'
                   ,'title': 'Toxicology'
                   }
               ,'ru':
                   {'short': 'токсикол.'
                   ,'title': 'Токсикология'
                   }
               ,'de':
                   {'short': 'Toxikol.'
                   ,'title': 'Toxikologie'
                   }
               ,'es':
                   {'short': 'toxicol.'
                   ,'title': 'Toxicology'
                   }
               ,'uk':
                   {'short': 'токсикол.'
                   ,'title': 'Токсикологія'
                   }
               }
           ,'toy.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'toy.'
                   ,'title': 'Toys'
                   }
               ,'ru':
                   {'short': 'игруш.'
                   ,'title': 'Игрушки'
                   }
               ,'de':
                   {'short': 'toy.'
                   ,'title': 'Toys'
                   }
               ,'es':
                   {'short': 'toy.'
                   ,'title': 'Toys'
                   }
               ,'uk':
                   {'short': 'іграш.'
                   ,'title': 'Іграшки'
                   }
               }
           ,'tradem.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'tradem.'
                   ,'title': 'Trademark'
                   }
               ,'ru':
                   {'short': 'т.м.'
                   ,'title': 'Торговая марка'
                   }
               ,'de':
                   {'short': 'Marke.'
                   ,'title': 'Markenzeichen'
                   }
               ,'es':
                   {'short': 'tradem.'
                   ,'title': 'Trademark'
                   }
               ,'uk':
                   {'short': 'фірм.зн.'
                   ,'title': 'Фірмовий знак'
                   }
               }
           ,'traf.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'traf.'
                   ,'title': 'Road traffic'
                   }
               ,'ru':
                   {'short': 'дор.движ.'
                   ,'title': 'Дорожное движение'
                   }
               ,'de':
                   {'short': 'traf.'
                   ,'title': 'Road traffic'
                   }
               ,'es':
                   {'short': 'traf.'
                   ,'title': 'Road traffic'
                   }
               ,'uk':
                   {'short': 'дор.рух'
                   ,'title': 'Дорожній рух'
                   }
               }
           ,'traf.contr.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'traf.contr.'
                   ,'title': 'Traffic control'
                   }
               ,'ru':
                   {'short': 'рег.дв.'
                   ,'title': 'Регулирование движения'
                   }
               ,'de':
                   {'short': 'traf.contr.'
                   ,'title': 'Traffic control'
                   }
               ,'es':
                   {'short': 'traf.contr.'
                   ,'title': 'Traffic control'
                   }
               ,'uk':
                   {'short': 'рег.руху'
                   ,'title': 'Регулювання руху'
                   }
               }
           ,'trampol.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'trampol.'
                   ,'title': 'Trampolining'
                   }
               ,'ru':
                   {'short': 'прыж.батут.'
                   ,'title': 'Прыжки на батуте'
                   }
               ,'de':
                   {'short': 'trampol.'
                   ,'title': 'Trampolining'
                   }
               ,'es':
                   {'short': 'trampol.'
                   ,'title': 'Trampolining'
                   }
               ,'uk':
                   {'short': 'батут'
                   ,'title': 'Стрибки на батуті'
                   }
               }
           ,'transf.':
               {'is_valid': True
               ,'major_en': 'Electrical engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'transf.'
                   ,'title': 'Transformers'
                   }
               ,'ru':
                   {'short': 'трансф.'
                   ,'title': 'Трансформаторы'
                   }
               ,'de':
                   {'short': 'Transf.'
                   ,'title': 'Transformatoren'
                   }
               ,'es':
                   {'short': 'transf.'
                   ,'title': 'Transformers'
                   }
               ,'uk':
                   {'short': 'трансф.'
                   ,'title': 'Трансформатори'
                   }
               }
           ,'transp.':
               {'is_valid': True
               ,'major_en': 'Transport'
               ,'is_major': True
               ,'en':
                   {'short': 'transp.'
                   ,'title': 'Transport'
                   }
               ,'ru':
                   {'short': 'трансп.'
                   ,'title': 'Транспорт'
                   }
               ,'de':
                   {'short': 'Verk.'
                   ,'title': 'Verkehr'
                   }
               ,'es':
                   {'short': 'transp.'
                   ,'title': 'Transport'
                   }
               ,'uk':
                   {'short': 'трансп.'
                   ,'title': 'Транспорт'
                   }
               }
           ,'transpl.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'transpl.'
                   ,'title': 'Transplantology'
                   }
               ,'ru':
                   {'short': 'транспл.'
                   ,'title': 'Трансплантология'
                   }
               ,'de':
                   {'short': 'transpl.'
                   ,'title': 'Transplantology'
                   }
               ,'es':
                   {'short': 'transpl.'
                   ,'title': 'Transplantology'
                   }
               ,'uk':
                   {'short': 'транспл.'
                   ,'title': 'Трансплантологія'
                   }
               }
           ,'traumat.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'traumat.'
                   ,'title': 'Traumatology'
                   }
               ,'ru':
                   {'short': 'травм.'
                   ,'title': 'Травматология'
                   }
               ,'de':
                   {'short': 'Traumat.'
                   ,'title': 'Traumatologie'
                   }
               ,'es':
                   {'short': 'traumat.'
                   ,'title': 'Traumatology'
                   }
               ,'uk':
                   {'short': 'травм.'
                   ,'title': 'Травматологія'
                   }
               }
           ,'trav.':
               {'is_valid': True
               ,'major_en': 'Travel'
               ,'is_major': True
               ,'en':
                   {'short': 'trav.'
                   ,'title': 'Travel'
                   }
               ,'ru':
                   {'short': 'тур.'
                   ,'title': 'Туризм'
                   }
               ,'de':
                   {'short': 'Tourism.'
                   ,'title': 'Tourismus'
                   }
               ,'es':
                   {'short': 'trav.'
                   ,'title': 'Travel'
                   }
               ,'uk':
                   {'short': 'турист.'
                   ,'title': 'Туризм'
                   }
               }
           ,'trd.class.':
               {'is_valid': True
               ,'major_en': 'Business'
               ,'is_major': False
               ,'en':
                   {'short': 'trd.class.'
                   ,'title': 'Trade classification'
                   }
               ,'ru':
                   {'short': 'КВЭД.'
                   ,'title': 'Классификация видов экон. деятельности'
                   }
               ,'de':
                   {'short': 'Gewerbeklass.'
                   ,'title': 'Gewerbeklassifizierung'
                   }
               ,'es':
                   {'short': 'trd.class.'
                   ,'title': 'Trade classification'
                   }
               ,'uk':
                   {'short': 'квед'
                   ,'title': 'Класифікація видів економічної діяльності'
                   }
               }
           ,'trib.':
               {'is_valid': True
               ,'major_en': 'Physics'
               ,'is_major': False
               ,'en':
                   {'short': 'trib.'
                   ,'title': 'Tribology'
                   }
               ,'ru':
                   {'short': 'триб.'
                   ,'title': 'Трибология'
                   }
               ,'de':
                   {'short': 'trib.'
                   ,'title': 'Tribology'
                   }
               ,'es':
                   {'short': 'trib.'
                   ,'title': 'Tribology'
                   }
               ,'uk':
                   {'short': 'трибол.'
                   ,'title': 'Трибологія'
                   }
               }
           ,'trucks':
               {'is_valid': False
               ,'major_en': 'Transport'
               ,'is_major': False
               ,'en':
                   {'short': 'trucks'
                   ,'title': 'Trucks/Lorries'
                   }
               ,'ru':
                   {'short': 'автом., груз.'
                   ,'title': 'Грузовой транспорт'
                   }
               ,'de':
                   {'short': 'trucks'
                   ,'title': 'Trucks/Lorries'
                   }
               ,'es':
                   {'short': 'trucks'
                   ,'title': 'Trucks/Lorries'
                   }
               ,'uk':
                   {'short': 'автом., вант.'
                   ,'title': 'Вантажний транспорт'
                   }
               }
           ,'tunn.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'tunn.'
                   ,'title': 'Tunneling'
                   }
               ,'ru':
                   {'short': 'тунн.'
                   ,'title': 'Туннелестроение и проходческие работы'
                   }
               ,'de':
                   {'short': 'tunn.'
                   ,'title': 'Tunneling'
                   }
               ,'es':
                   {'short': 'tunn.'
                   ,'title': 'Tunneling'
                   }
               ,'uk':
                   {'short': 'тун.буд.'
                   ,'title': 'Тунелебудування'
                   }
               }
           ,'turb.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'turb.'
                   ,'title': 'Turbines'
                   }
               ,'ru':
                   {'short': 'турб.'
                   ,'title': 'Турбины'
                   }
               ,'de':
                   {'short': 'Turb.'
                   ,'title': 'Turbinen'
                   }
               ,'es':
                   {'short': 'turb.'
                   ,'title': 'Turbines'
                   }
               ,'uk':
                   {'short': 'турб.'
                   ,'title': 'Турбіни'
                   }
               }
           ,'turkish':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'turkish'
                   ,'title': 'Turkish language'
                   }
               ,'ru':
                   {'short': 'турец.'
                   ,'title': 'Турецкий язык'
                   }
               ,'de':
                   {'short': 'Türk.'
                   ,'title': 'Türkisch'
                   }
               ,'es':
                   {'short': 'turc.'
                   ,'title': 'Turco'
                   }
               ,'uk':
                   {'short': 'тур.'
                   ,'title': 'Турецька мова'
                   }
               }
           ,'typogr.':
               {'is_valid': True
               ,'major_en': 'Publishing'
               ,'is_major': False
               ,'en':
                   {'short': 'typogr.'
                   ,'title': 'Typography'
                   }
               ,'ru':
                   {'short': 'типогр.'
                   ,'title': 'Типографика'
                   }
               ,'de':
                   {'short': 'typogr.'
                   ,'title': 'Typography'
                   }
               ,'es':
                   {'short': 'typogr.'
                   ,'title': 'Typography'
                   }
               ,'uk':
                   {'short': 'типогр.'
                   ,'title': 'Типографіка'
                   }
               }
           ,'typol.':
               {'is_valid': True
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'typol.'
                   ,'title': 'Typology'
                   }
               ,'ru':
                   {'short': 'типол.'
                   ,'title': 'Типология'
                   }
               ,'de':
                   {'short': 'typol.'
                   ,'title': 'Typology'
                   }
               ,'es':
                   {'short': 'typol.'
                   ,'title': 'Typology'
                   }
               ,'uk':
                   {'short': 'типол.'
                   ,'title': 'Типологія'
                   }
               }
           ,'ufol.':
               {'is_valid': True
               ,'major_en': 'Parasciences'
               ,'is_major': False
               ,'en':
                   {'short': 'ufol.'
                   ,'title': 'Ufology'
                   }
               ,'ru':
                   {'short': 'уфол.'
                   ,'title': 'Уфология'
                   }
               ,'de':
                   {'short': 'ufol.'
                   ,'title': 'Ufology'
                   }
               ,'es':
                   {'short': 'ufol.'
                   ,'title': 'Ufology'
                   }
               ,'uk':
                   {'short': 'уфол.'
                   ,'title': 'Уфологія'
                   }
               }
           ,'ultrasnd.':
               {'is_valid': True
               ,'major_en': 'Medical appliances'
               ,'is_major': False
               ,'en':
                   {'short': 'ultrasnd.'
                   ,'title': 'Ultrasound'
                   }
               ,'ru':
                   {'short': 'ультразв.'
                   ,'title': 'Ультразвук'
                   }
               ,'de':
                   {'short': 'Ultrasch.'
                   ,'title': 'Ultraschall'
                   }
               ,'es':
                   {'short': 'ultrasnd.'
                   ,'title': 'Ultrasound'
                   }
               ,'uk':
                   {'short': 'ультразв.'
                   ,'title': 'Ультразвук'
                   }
               }
           ,'unions.':
               {'is_valid': True
               ,'major_en': 'Production'
               ,'is_major': False
               ,'en':
                   {'short': 'unions.'
                   ,'title': 'Trade unions'
                   }
               ,'ru':
                   {'short': 'профс.'
                   ,'title': 'Профсоюзы'
                   }
               ,'de':
                   {'short': 'unions.'
                   ,'title': 'Trade unions'
                   }
               ,'es':
                   {'short': 'unions.'
                   ,'title': 'Trade unions'
                   }
               ,'uk':
                   {'short': 'профс.'
                   ,'title': 'Профспілки'
                   }
               }
           ,'unit.meas.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'unit.meas.'
                   ,'title': 'Unit measures'
                   }
               ,'ru':
                   {'short': 'ед.изм.'
                   ,'title': 'Единицы измерений'
                   }
               ,'de':
                   {'short': 'unit.meas.'
                   ,'title': 'Unit measures'
                   }
               ,'es':
                   {'short': 'unit.meas.'
                   ,'title': 'Unit measures'
                   }
               ,'uk':
                   {'short': 'од.вимір.'
                   ,'title': 'Одиниці вимірювання'
                   }
               }
           ,'univer.':
               {'is_valid': True
               ,'major_en': 'Education'
               ,'is_major': False
               ,'en':
                   {'short': 'univer.'
                   ,'title': 'University'
                   }
               ,'ru':
                   {'short': 'унив.'
                   ,'title': 'Университет'
                   }
               ,'de':
                   {'short': 'Uni.'
                   ,'title': 'Universität'
                   }
               ,'es':
                   {'short': 'univ.'
                   ,'title': 'Universidad'
                   }
               ,'uk':
                   {'short': 'унів.'
                   ,'title': 'Університет'
                   }
               }
           ,'urol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'urol.'
                   ,'title': 'Urology'
                   }
               ,'ru':
                   {'short': 'урол.'
                   ,'title': 'Урология'
                   }
               ,'de':
                   {'short': 'Urol.'
                   ,'title': 'Urologie'
                   }
               ,'es':
                   {'short': 'urol.'
                   ,'title': 'Urology'
                   }
               ,'uk':
                   {'short': 'урол.'
                   ,'title': 'Урологія'
                   }
               }
           ,'urug.sp.':
               {'is_valid': True
               ,'major_en': 'Dialectal'
               ,'is_major': False
               ,'en':
                   {'short': 'urug.sp.'
                   ,'title': 'Uruguayan Spanish'
                   }
               ,'ru':
                   {'short': 'уругв.'
                   ,'title': 'Уругвайский диалект испанского языка'
                   }
               ,'de':
                   {'short': 'urug.sp.'
                   ,'title': 'Uruguayan Spanish'
                   }
               ,'es':
                   {'short': 'urug.sp.'
                   ,'title': 'Uruguayan Spanish'
                   }
               ,'uk':
                   {'short': 'уругв.'
                   ,'title': 'Уругвайський діалект іспанської мови'
                   }
               }
           ,'vac.tub.':
               {'is_valid': True
               ,'major_en': 'Electronics'
               ,'is_major': False
               ,'en':
                   {'short': 'vac.tub.'
                   ,'title': 'Vacuum tubes'
                   }
               ,'ru':
                   {'short': 'эл.ламп.'
                   ,'title': 'Электронные лампы'
                   }
               ,'de':
                   {'short': 'Vak.rohr.'
                   ,'title': 'Vakuumröhren'
                   }
               ,'es':
                   {'short': 'vac.tub.'
                   ,'title': 'Vacuum tubes'
                   }
               ,'uk':
                   {'short': 'ел.ламп.'
                   ,'title': 'Електронні лампи'
                   }
               }
           ,'valves':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'valves'
                   ,'title': 'Valves'
                   }
               ,'ru':
                   {'short': 'труб.армат.'
                   ,'title': 'Трубопроводная арматура'
                   }
               ,'de':
                   {'short': 'valves'
                   ,'title': 'Valves'
                   }
               ,'es':
                   {'short': 'valves'
                   ,'title': 'Valves'
                   }
               ,'uk':
                   {'short': 'труб.армат.'
                   ,'title': 'Трубопровідна арматура'
                   }
               }
           ,'venereol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'venereol.'
                   ,'title': 'Venereology'
                   }
               ,'ru':
                   {'short': 'венерол.'
                   ,'title': 'Венерология'
                   }
               ,'de':
                   {'short': 'Venerol.'
                   ,'title': 'Venerologie'
                   }
               ,'es':
                   {'short': 'venereol.'
                   ,'title': 'Venereology'
                   }
               ,'uk':
                   {'short': 'венерол.'
                   ,'title': 'Венерологія'
                   }
               }
           ,'vent.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'vent.'
                   ,'title': 'Ventilation'
                   }
               ,'ru':
                   {'short': 'вент.'
                   ,'title': 'Вентиляция'
                   }
               ,'de':
                   {'short': 'vent.'
                   ,'title': 'Ventilation'
                   }
               ,'es':
                   {'short': 'vent.'
                   ,'title': 'Ventilation'
                   }
               ,'uk':
                   {'short': 'вент.'
                   ,'title': 'Вентиляція'
                   }
               }
           ,'verbat.':
               {'is_valid': True
               ,'major_en': 'Subjects for Chinese dictionaries (container)'
               ,'is_major': False
               ,'en':
                   {'short': 'verbat.'
                   ,'title': 'Verbatim'
                   }
               ,'ru':
                   {'short': 'досл.'
                   ,'title': 'Дословно'
                   }
               ,'de':
                   {'short': 'verbat.'
                   ,'title': 'Verbatim'
                   }
               ,'es':
                   {'short': 'verbat.'
                   ,'title': 'Verbatim'
                   }
               ,'uk':
                   {'short': 'досл.'
                   ,'title': 'Дослівно'
                   }
               }
           ,'verl.':
               {'is_valid': True
               ,'major_en': 'Jargon and slang'
               ,'is_major': False
               ,'en':
                   {'short': 'verl.'
                   ,'title': 'Verlan'
                   }
               ,'ru':
                   {'short': 'верл.'
                   ,'title': 'Верлан'
                   }
               ,'de':
                   {'short': 'verl.'
                   ,'title': 'Verlan'
                   }
               ,'es':
                   {'short': 'verl.'
                   ,'title': 'Verlan'
                   }
               ,'uk':
                   {'short': 'верл.'
                   ,'title': 'Верлан'
                   }
               }
           ,'vernac.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'vernac.'
                   ,'title': 'Vernacular language'
                   }
               ,'ru':
                   {'short': 'народн.'
                   ,'title': 'Народное выражение'
                   }
               ,'de':
                   {'short': 'vernac.'
                   ,'title': 'Vernacular language'
                   }
               ,'es':
                   {'short': 'vernac.'
                   ,'title': 'Vernacular language'
                   }
               ,'uk':
                   {'short': 'народн.'
                   ,'title': 'Народний вираз'
                   }
               }
           ,'vet.med.':
               {'is_valid': True
               ,'major_en': 'Medical'
               ,'is_major': False
               ,'en':
                   {'short': 'vet.med.'
                   ,'title': 'Veterinary medicine'
                   }
               ,'ru':
                   {'short': 'вет.'
                   ,'title': 'Ветеринария'
                   }
               ,'de':
                   {'short': 'Vet.med.'
                   ,'title': 'Veterinärmedizin'
                   }
               ,'es':
                   {'short': 'vet.'
                   ,'title': 'Medicina veterinaria'
                   }
               ,'uk':
                   {'short': 'вет.'
                   ,'title': 'Ветеринарія'
                   }
               }
           ,'vibr.monit.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'vibr.monit.'
                   ,'title': 'Vibration monitoring'
                   }
               ,'ru':
                   {'short': 'вибр.монит.'
                   ,'title': 'Вибромониторинг'
                   }
               ,'de':
                   {'short': 'vibr.monit.'
                   ,'title': 'Vibration monitoring'
                   }
               ,'es':
                   {'short': 'vibr.monit.'
                   ,'title': 'Vibration monitoring'
                   }
               ,'uk':
                   {'short': 'вібр.моніт.'
                   ,'title': 'Вібромоніторинг'
                   }
               }
           ,'video.':
               {'is_valid': True
               ,'major_en': 'Multimedia'
               ,'is_major': False
               ,'en':
                   {'short': 'video.'
                   ,'title': 'Video recording'
                   }
               ,'ru':
                   {'short': 'видео.'
                   ,'title': 'Видеозапись'
                   }
               ,'de':
                   {'short': 'Video.'
                   ,'title': 'Videoaufzeichnung'
                   }
               ,'es':
                   {'short': 'video.'
                   ,'title': 'Video recording'
                   }
               ,'uk':
                   {'short': 'відео'
                   ,'title': 'Відеозапис'
                   }
               }
           ,'viet.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'viet.'
                   ,'title': 'Vietnamese'
                   }
               ,'ru':
                   {'short': 'вьет.'
                   ,'title': 'Вьетнамский язык'
                   }
               ,'de':
                   {'short': 'viet.'
                   ,'title': 'Vietnamese'
                   }
               ,'es':
                   {'short': 'viet.'
                   ,'title': 'Vietnamese'
                   }
               ,'uk':
                   {'short': 'в’єтн.'
                   ,'title': 'В’єтнамська мова'
                   }
               }
           ,'virol.':
               {'is_valid': True
               ,'major_en': 'Life sciences'
               ,'is_major': False
               ,'en':
                   {'short': 'virol.'
                   ,'title': 'Virology'
                   }
               ,'ru':
                   {'short': 'вирусол.'
                   ,'title': 'Вирусология'
                   }
               ,'de':
                   {'short': 'Virol.'
                   ,'title': 'Virologie'
                   }
               ,'es':
                   {'short': 'virol.'
                   ,'title': 'Virología'
                   }
               ,'uk':
                   {'short': 'вірусол.'
                   ,'title': 'Вірусологія'
                   }
               }
           ,'volcan.':
               {'is_valid': True
               ,'major_en': 'Geology'
               ,'is_major': False
               ,'en':
                   {'short': 'volcan.'
                   ,'title': 'Volcanology'
                   }
               ,'ru':
                   {'short': 'вулк.'
                   ,'title': 'Вулканология'
                   }
               ,'de':
                   {'short': 'Vulkanol.'
                   ,'title': 'Vulkanologie'
                   }
               ,'es':
                   {'short': 'volcan.'
                   ,'title': 'Volcanology'
                   }
               ,'uk':
                   {'short': 'вулк.'
                   ,'title': 'Вулканологія'
                   }
               }
           ,'voll.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'voll.'
                   ,'title': 'Volleyball'
                   }
               ,'ru':
                   {'short': 'волейб.'
                   ,'title': 'Волейбол'
                   }
               ,'de':
                   {'short': 'voll.'
                   ,'title': 'Volleyball'
                   }
               ,'es':
                   {'short': 'voll.'
                   ,'title': 'Volleyball'
                   }
               ,'uk':
                   {'short': 'волейб.'
                   ,'title': 'Волейбол'
                   }
               }
           ,'vulg.':
               {'is_valid': True
               ,'major_en': 'Stylistic values'
               ,'is_major': False
               ,'en':
                   {'short': 'vulg.'
                   ,'title': 'Vulgar'
                   }
               ,'ru':
                   {'short': 'вульг.'
                   ,'title': 'Вульгаризм'
                   }
               ,'de':
                   {'short': 'vulg.'
                   ,'title': 'Vulgar'
                   }
               ,'es':
                   {'short': 'vulg.'
                   ,'title': 'Vulgar'
                   }
               ,'uk':
                   {'short': 'вульг.'
                   ,'title': 'Вульгаризм'
                   }
               }
           ,'wales':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'wales'
                   ,'title': 'Wales'
                   }
               ,'ru':
                   {'short': 'Уэльс.'
                   ,'title': 'Уэльс'
                   }
               ,'de':
                   {'short': 'wales'
                   ,'title': 'Wales'
                   }
               ,'es':
                   {'short': 'wales'
                   ,'title': 'Wales'
                   }
               ,'uk':
                   {'short': 'уельс'
                   ,'title': 'Уельс'
                   }
               }
           ,'wareh.':
               {'is_valid': True
               ,'major_en': 'Logistics'
               ,'is_major': False
               ,'en':
                   {'short': 'wareh.'
                   ,'title': 'Warehouse'
                   }
               ,'ru':
                   {'short': 'склад.'
                   ,'title': 'Складское дело'
                   }
               ,'de':
                   {'short': 'Lagerw.'
                   ,'title': 'Lagerwesen'
                   }
               ,'es':
                   {'short': 'wareh.'
                   ,'title': 'Warehouse'
                   }
               ,'uk':
                   {'short': 'склад.'
                   ,'title': 'Складська справа'
                   }
               }
           ,'waste.man.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'waste.man.'
                   ,'title': 'Waste management'
                   }
               ,'ru':
                   {'short': 'утил.отх.'
                   ,'title': 'Утилизация отходов'
                   }
               ,'de':
                   {'short': 'waste.man.'
                   ,'title': 'Waste management'
                   }
               ,'es':
                   {'short': 'waste.man.'
                   ,'title': 'Waste management'
                   }
               ,'uk':
                   {'short': 'утил.відх.'
                   ,'title': 'Утилізація відходів'
                   }
               }
           ,'watchm.':
               {'is_valid': True
               ,'major_en': 'Machinery and mechanisms'
               ,'is_major': False
               ,'en':
                   {'short': 'watchm.'
                   ,'title': 'Watchmaking'
                   }
               ,'ru':
                   {'short': 'час.'
                   ,'title': 'Часовое дело'
                   }
               ,'de':
                   {'short': 'Uhr.'
                   ,'title': 'Uhrherstellung'
                   }
               ,'es':
                   {'short': 'watchm.'
                   ,'title': 'Watchmaking'
                   }
               ,'uk':
                   {'short': 'годинн.'
                   ,'title': 'Годинникарство'
                   }
               }
           ,'water.res.':
               {'is_valid': True
               ,'major_en': 'Natural resourses and wildlife conservation'
               ,'is_major': False
               ,'en':
                   {'short': 'water.res.'
                   ,'title': 'Water resources'
                   }
               ,'ru':
                   {'short': 'вод.рес.'
                   ,'title': 'Водные ресурсы'
                   }
               ,'de':
                   {'short': 'Wass.vork.'
                   ,'title': 'Wasservorkommen'
                   }
               ,'es':
                   {'short': 'water.res.'
                   ,'title': 'Water resources'
                   }
               ,'uk':
                   {'short': 'вод.рес.'
                   ,'title': 'Водні ресурси'
                   }
               }
           ,'water.suppl.':
               {'is_valid': True
               ,'major_en': 'Engineering'
               ,'is_major': False
               ,'en':
                   {'short': 'water.suppl.'
                   ,'title': 'Water supply'
                   }
               ,'ru':
                   {'short': 'вод.'
                   ,'title': 'Водоснабжение'
                   }
               ,'de':
                   {'short': 'water.suppl.'
                   ,'title': 'Water supply'
                   }
               ,'es':
                   {'short': 'water.suppl.'
                   ,'title': 'Water supply'
                   }
               ,'uk':
                   {'short': 'водопост.'
                   ,'title': 'Водопостачання'
                   }
               }
           ,'waterski.':
               {'is_valid': True
               ,'major_en': 'Outdoor activities and extreme sports'
               ,'is_major': False
               ,'en':
                   {'short': 'waterski.'
                   ,'title': 'Waterskiing'
                   }
               ,'ru':
                   {'short': 'водн.лыж.'
                   ,'title': 'Водные лыжи'
                   }
               ,'de':
                   {'short': 'waterski.'
                   ,'title': 'Waterskiing'
                   }
               ,'es':
                   {'short': 'waterski.'
                   ,'title': 'Waterskiing'
                   }
               ,'uk':
                   {'short': 'вод.лиж.'
                   ,'title': 'Водні лижі'
                   }
               }
           ,'weap.':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'ru':
                   {'short': 'оруж.'
                   ,'title': 'Оружие и оружейное производство'
                   }
               ,'de':
                   {'short': 'Waffen'
                   ,'title': 'Waffen und Waffenindustrie'
                   }
               ,'es':
                   {'short': 'weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'uk':
                   {'short': 'зброя'
                   ,'title': 'Зброя та зброярство'
                   }
               }
           ,'weightlift.':
               {'is_valid': True
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'weightlift.'
                   ,'title': 'Weightlifting'
                   }
               ,'ru':
                   {'short': 'тяж.атл.'
                   ,'title': 'Тяжёлая атлетика'
                   }
               ,'de':
                   {'short': 'weightlift.'
                   ,'title': 'Weightlifting'
                   }
               ,'es':
                   {'short': 'weightlift.'
                   ,'title': 'Weightlifting'
                   }
               ,'uk':
                   {'short': 'в.атл.'
                   ,'title': 'Важка атлетика'
                   }
               }
           ,'weld.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'weld.'
                   ,'title': 'Welding'
                   }
               ,'ru':
                   {'short': 'свар.'
                   ,'title': 'Сварка'
                   }
               ,'de':
                   {'short': 'Schweiß.'
                   ,'title': 'Schweißen'
                   }
               ,'es':
                   {'short': 'weld.'
                   ,'title': 'Welding'
                   }
               ,'uk':
                   {'short': 'звар.'
                   ,'title': 'Зварювання'
                   }
               }
           ,'welf.':
               {'is_valid': True
               ,'major_en': 'Government, administration and public services'
               ,'is_major': False
               ,'en':
                   {'short': 'welf.'
                   ,'title': 'Welfare & Social Security'
                   }
               ,'ru':
                   {'short': 'собес.'
                   ,'title': 'Социальное обеспечение'
                   }
               ,'de':
                   {'short': 'Sozialleist.'
                   ,'title': 'Sozialleistungen'
                   }
               ,'es':
                   {'short': 'welf.'
                   ,'title': 'Welfare & Social Security'
                   }
               ,'uk':
                   {'short': 'соц.заб.'
                   ,'title': 'Соціальне забезпечення'
                   }
               }
           ,'well.contr.':
               {'is_valid': True
               ,'major_en': 'Oil and gas'
               ,'is_major': False
               ,'en':
                   {'short': 'well.contr.'
                   ,'title': 'Well control'
                   }
               ,'ru':
                   {'short': 'скваж.'
                   ,'title': 'Управление скважиной'
                   }
               ,'de':
                   {'short': 'Bohrl.Kontr.'
                   ,'title': 'Bohrlochkontrolle'
                   }
               ,'es':
                   {'short': 'well.contr.'
                   ,'title': 'Well control'
                   }
               ,'uk':
                   {'short': 'упр.свердл.'
                   ,'title': 'Управління свердловиною'
                   }
               }
           ,'welln.':
               {'is_valid': True
               ,'major_en': 'Wellness'
               ,'is_major': True
               ,'en':
                   {'short': 'welln.'
                   ,'title': 'Wellness'
                   }
               ,'ru':
                   {'short': 'крас.здор.'
                   ,'title': 'Красота и здоровье'
                   }
               ,'de':
                   {'short': 'welln.'
                   ,'title': 'Wellness'
                   }
               ,'es':
                   {'short': 'welln.'
                   ,'title': 'Wellness'
                   }
               ,'uk':
                   {'short': 'крас.здор.'
                   ,'title': "Краса і здоров'я"}}, 'west.Ind.':
               {'is_valid': True
               ,'major_en': 'Countries and regions'
               ,'is_major': False
               ,'en':
                   {'short': 'west.Ind.'
                   ,'title': 'West Indies'
                   }
               ,'ru':
                   {'short': 'кариб.'
                   ,'title': 'Карибский регион'
                   }
               ,'de':
                   {'short': 'west.Ind.'
                   ,'title': 'West Indies'
                   }
               ,'es':
                   {'short': 'west.Ind.'
                   ,'title': 'West Indies'
                   }
               ,'uk':
                   {'short': 'кариб.'
                   ,'title': 'Карибський регіон'
                   }
               }
           ,'win.tast.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'win.tast.'
                   ,'title': 'Wine tasting'
                   }
               ,'ru':
                   {'short': 'дегуст.'
                   ,'title': 'Дегустация'
                   }
               ,'de':
                   {'short': 'win.tast.'
                   ,'title': 'Wine tasting'
                   }
               ,'es':
                   {'short': 'win.tast.'
                   ,'title': 'Wine tasting'
                   }
               ,'uk':
                   {'short': 'дегуст.'
                   ,'title': 'Дегустація'
                   }
               }
           ,'wind.':
               {'is_valid': True
               ,'major_en': 'Energy industry'
               ,'is_major': False
               ,'en':
                   {'short': 'wind.'
                   ,'title': 'Wind Energy'
                   }
               ,'ru':
                   {'short': 'ветр.'
                   ,'title': 'Ветроэнергетика'
                   }
               ,'de':
                   {'short': 'wind.'
                   ,'title': 'Wind Energy'
                   }
               ,'es':
                   {'short': 'wind.'
                   ,'title': 'Wind Energy'
                   }
               ,'uk':
                   {'short': 'вітроен.'
                   ,'title': 'Вітроенергетика'
                   }
               }
           ,'windows':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'windows'
                   ,'title': 'Windows'
                   }
               ,'ru':
                   {'short': 'окна.'
                   ,'title': 'Окна'
                   }
               ,'de':
                   {'short': 'windows'
                   ,'title': 'Windows'
                   }
               ,'es':
                   {'short': 'windows'
                   ,'title': 'Windows'
                   }
               ,'uk':
                   {'short': 'вікна.'
                   ,'title': 'Вікна'
                   }
               }
           ,'wine.gr.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'wine.gr.'
                   ,'title': 'Wine growing'
                   }
               ,'ru':
                   {'short': 'вин.'
                   ,'title': 'Виноградарство'
                   }
               ,'de':
                   {'short': 'wine.gr.'
                   ,'title': 'Wine growing'
                   }
               ,'es':
                   {'short': 'wine.gr.'
                   ,'title': 'Wine growing'
                   }
               ,'uk':
                   {'short': 'вин.'
                   ,'title': 'Виноградарство'
                   }
               }
           ,'winemak.':
               {'is_valid': True
               ,'major_en': 'Food industry'
               ,'is_major': False
               ,'en':
                   {'short': 'winemak.'
                   ,'title': 'Winemaking'
                   }
               ,'ru':
                   {'short': 'винодел.'
                   ,'title': 'Виноделие'
                   }
               ,'de':
                   {'short': 'winemak.'
                   ,'title': 'Winemaking'
                   }
               ,'es':
                   {'short': 'winemak.'
                   ,'title': 'Winemaking'
                   }
               ,'uk':
                   {'short': 'винороб.'
                   ,'title': 'Виноробство'
                   }
               }
           ,'wir.':
               {'is_valid': True
               ,'major_en': 'Construction'
               ,'is_major': False
               ,'en':
                   {'short': 'wir.'
                   ,'title': 'Wiring'
                   }
               ,'ru':
                   {'short': 'монт.'
                   ,'title': 'Монтажное дело'
                   }
               ,'de':
                   {'short': 'wir.'
                   ,'title': 'Wiring'
                   }
               ,'es':
                   {'short': 'wir.'
                   ,'title': 'Wiring'
                   }
               ,'uk':
                   {'short': 'монт.'
                   ,'title': 'Монтажна справа'
                   }
               }
           ,'wire.drw.':
               {'is_valid': True
               ,'major_en': 'Industry'
               ,'is_major': False
               ,'en':
                   {'short': 'wire.drw.'
                   ,'title': 'Wire drawing'
                   }
               ,'ru':
                   {'short': 'влч.'
                   ,'title': 'Волочение'
                   }
               ,'de':
                   {'short': 'Ausz.'
                   ,'title': 'Ausziehen'
                   }
               ,'es':
                   {'short': 'wire.drw.'
                   ,'title': 'Wire drawing'
                   }
               ,'uk':
                   {'short': 'волоч.'
                   ,'title': 'Волочіння'
                   }
               }
           ,'wnd.':
               {'is_valid': True
               ,'major_en': 'Technology'
               ,'is_major': False
               ,'en':
                   {'short': 'wnd.'
                   ,'title': 'Winding'
                   }
               ,'ru':
                   {'short': 'обм.'
                   ,'title': 'Обмотки'
                   }
               ,'de':
                   {'short': 'wnd.'
                   ,'title': 'Winding'
                   }
               ,'es':
                   {'short': 'wnd.'
                   ,'title': 'Winding'
                   }
               ,'uk':
                   {'short': 'обм.'
                   ,'title': 'Обмотки'
                   }
               }
           ,'wood.':
               {'is_valid': True
               ,'major_en': 'Wood, pulp and paper industries'
               ,'is_major': False
               ,'en':
                   {'short': 'wood.'
                   ,'title': 'Wood processing'
                   }
               ,'ru':
                   {'short': 'дерев.'
                   ,'title': 'Деревообработка'
                   }
               ,'de':
                   {'short': 'Holz.'
                   ,'title': 'Holzverarbeitung'
                   }
               ,'es':
                   {'short': 'wood.'
                   ,'title': 'Wood processing'
                   }
               ,'uk':
                   {'short': 'дерев.'
                   ,'title': 'Деревообробка'
                   }
               }
           ,'work.fl.':
               {'is_valid': True
               ,'major_en': 'Records management'
               ,'is_major': False
               ,'en':
                   {'short': 'work.fl.'
                   ,'title': 'Work flow'
                   }
               ,'ru':
                   {'short': 'докум.'
                   ,'title': 'Документооборот'
                   }
               ,'de':
                   {'short': 'work.fl.'
                   ,'title': 'Work flow'
                   }
               ,'es':
                   {'short': 'work.fl.'
                   ,'title': 'Work flow'
                   }
               ,'uk':
                   {'short': 'докум.'
                   ,'title': 'Документообіг'
                   }
               }
           ,'wrest.':
               {'is_valid': True
               ,'major_en': 'Martial arts and combat sports'
               ,'is_major': False
               ,'en':
                   {'short': 'wrest.'
                   ,'title': 'Wrestling'
                   }
               ,'ru':
                   {'short': 'борьб.'
                   ,'title': 'Борьба'
                   }
               ,'de':
                   {'short': 'wrest.'
                   ,'title': 'Wrestling'
                   }
               ,'es':
                   {'short': 'wrest.'
                   ,'title': 'Wrestling'
                   }
               ,'uk':
                   {'short': 'бор.'
                   ,'title': 'Боротьба'
                   }
               }
           ,'yacht.':
               {'is_valid': True
               ,'major_en': 'Nautical'
               ,'is_major': False
               ,'en':
                   {'short': 'yacht.'
                   ,'title': 'Yachting'
                   }
               ,'ru':
                   {'short': 'яхт.'
                   ,'title': 'Яхтенный спорт'
                   }
               ,'de':
                   {'short': 'yacht.'
                   ,'title': 'Yachting'
                   }
               ,'es':
                   {'short': 'yacht.'
                   ,'title': 'Yachting'
                   }
               ,'uk':
                   {'short': 'яхт.'
                   ,'title': 'Яхтовий спорт'
                   }
               }
           ,'yiddish.':
               {'is_valid': True
               ,'major_en': 'Languages'
               ,'is_major': False
               ,'en':
                   {'short': 'yiddish.'
                   ,'title': 'Yiddish'
                   }
               ,'ru':
                   {'short': 'идиш.'
                   ,'title': 'Идиш'
                   }
               ,'de':
                   {'short': 'yiddish.'
                   ,'title': 'Yiddish'
                   }
               ,'es':
                   {'short': 'yiddish.'
                   ,'title': 'Yiddish'
                   }
               ,'uk':
                   {'short': 'їдиш'
                   ,'title': 'Їдиш'
                   }
               }
           ,'zool.':
               {'is_valid': True
               ,'major_en': 'Biology'
               ,'is_major': False
               ,'en':
                   {'short': 'zool.'
                   ,'title': 'Zoology'
                   }
               ,'ru':
                   {'short': 'зоол.'
                   ,'title': 'Зоология'
                   }
               ,'de':
                   {'short': 'Zool.'
                   ,'title': 'Zoologie'
                   }
               ,'es':
                   {'short': 'zool.'
                   ,'title': 'Zoología'
                   }
               ,'uk':
                   {'short': 'зоол.'
                   ,'title': 'Зоологія'
                   }
               }
           ,'zoot.':
               {'is_valid': True
               ,'major_en': 'Agriculture'
               ,'is_major': False
               ,'en':
                   {'short': 'zoot.'
                   ,'title': 'Zootechnics'
                   }
               ,'ru':
                   {'short': 'зоот.'
                   ,'title': 'Зоотехния'
                   }
               ,'de':
                   {'short': 'zoot.'
                   ,'title': 'Zootechnics'
                   }
               ,'es':
                   {'short': 'zoot.'
                   ,'title': 'Zootechnics'
                   }
               ,'uk':
                   {'short': 'зоот.'
                   ,'title': 'Зоотехнія'
                   }
               }
           ,'Игорь Миг':
               {'is_valid': True
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг'
                   ,'title': 'General'
                   }
               ,'ru':
                   {'short': 'Игорь Миг'
                   ,'title': 'Общая лексика'
                   }
               ,'de':
                   {'short': 'Игорь Миг'
                   ,'title': 'Allgemeine Lexik'
                   }
               ,'es':
                   {'short': 'Игорь Миг'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'Игорь Миг'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'Игорь Миг, abbr.':
               {'is_valid': False
               ,'major_en': 'Grammatical labels'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, abbr.'
                   ,'title': 'Abbreviation'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, сокр.'
                   ,'title': 'Сокращение'
                   }
               ,'de':
                   {'short': 'Игорь Миг, Abkürz.'
                   ,'title': 'Abkürzung'
                   }
               ,'es':
                   {'short': 'Игорь Миг, abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'Игорь Миг, calque.':
               {'is_valid': False
               ,'major_en': 'Auxilliary categories (editor use only)'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, calque.'
                   ,'title': 'Loan translation'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, калька.'
                   ,'title': 'Калька'
                   }
               ,'de':
                   {'short': 'Игорь Миг, calque.'
                   ,'title': 'Loan translation'
                   }
               ,'es':
                   {'short': 'Игорь Миг, calque.'
                   ,'title': 'Loan translation'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, калька'
                   ,'title': 'Калька'
                   }
               }
           ,'Игорь Миг, cloth.':
               {'is_valid': False
               ,'major_en': 'Light industries'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, одеж.'
                   ,'title': 'Одежда'
                   }
               ,'de':
                   {'short': 'Игорь Миг, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'es':
                   {'short': 'Игорь Миг, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'Игорь Миг, earth.sc.':
               {'is_valid': False
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, earth.sc.'
                   ,'title': 'Earth sciences'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, землевед.'
                   ,'title': 'Землеведение'
                   }
               ,'de':
                   {'short': 'Игорь Миг, earth.sc.'
                   ,'title': 'Earth sciences'
                   }
               ,'es':
                   {'short': 'Игорь Миг, earth.sc.'
                   ,'title': 'Earth sciences'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, землезн.'
                   ,'title': 'Землезнавство'
                   }
               }
           ,'Игорь Миг, hydrom.':
               {'is_valid': False
               ,'major_en': 'Geography'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, hydrom.'
                   ,'title': 'Hydrometry'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, гидром.'
                   ,'title': 'Гидрометрия'
                   }
               ,'de':
                   {'short': 'Игорь Миг, hydrom.'
                   ,'title': 'Hydrometry'
                   }
               ,'es':
                   {'short': 'Игорь Миг, hydrom.'
                   ,'title': 'Hydrometry'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, гідром.'
                   ,'title': 'Гідрометрія'
                   }
               }
           ,'Игорь Миг, inform.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, inform.'
                   ,'title': 'Informal'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, разг.'
                   ,'title': 'Разговорная лексика'
                   }
               ,'de':
                   {'short': 'Игорь Миг, Umg.'
                   ,'title': 'Umgangssprache'
                   }
               ,'es':
                   {'short': 'Игорь Миг, inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'Игорь Миг, quot.aph.':
               {'is_valid': False
               ,'major_en': 'Literature'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, quot.aph.'
                   ,'title': 'Quotes and aphorisms'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, цит.афор.'
                   ,'title': 'Цитаты, афоризмы и крылатые выражения'
                   }
               ,'de':
                   {'short': 'Игорь Миг, quot.aph.'
                   ,'title': 'Quotes and aphorisms'
                   }
               ,'es':
                   {'short': 'Игорь Миг, quot.aph.'
                   ,'title': 'Quotes and aphorisms'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, цит.афор.'
                   ,'title': 'Цитати, афоризми та крилаті вирази'
                   }
               }
           ,'Игорь Миг, sport.':
               {'is_valid': False
               ,'major_en': 'Sports'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, sport.'
                   ,'title': 'Sports'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, спорт.'
                   ,'title': 'Спорт'
                   }
               ,'de':
                   {'short': 'Игорь Миг, Sport.'
                   ,'title': 'Sport'
                   }
               ,'es':
                   {'short': 'Игорь Миг, dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'Игорь Миг, tagmem.':
               {'is_valid': False
               ,'major_en': 'Linguistics'
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, tagmem.'
                   ,'title': 'Tagmemics'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, тагмем.'
                   ,'title': 'Тагмемика'
                   }
               ,'de':
                   {'short': 'Игорь Миг, tagmem.'
                   ,'title': 'Tagmemics'
                   }
               ,'es':
                   {'short': 'Игорь Миг, tagmem.'
                   ,'title': 'Tagmemics'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, тагмем.'
                   ,'title': 'Тагмеміка'
                   }
               }
           ,'Игорь Миг, weap.':
               {'is_valid': False
               ,'major_en': ''
               ,'is_major': False
               ,'en':
                   {'short': 'Игорь Миг, weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'ru':
                   {'short': 'Игорь Миг, оруж.'
                   ,'title': 'Оружие и оружейное производство'
                   }
               ,'de':
                   {'short': 'Игорь Миг, Waffen'
                   ,'title': 'Waffen und Waffenindustrie'
                   }
               ,'es':
                   {'short': 'Игорь Миг, weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, зброя'
                   ,'title': 'Зброя та зброярство'
                   }
               }
           }


class Subjects:
    
    def __init__(self):
        self.lang = 'en'
        self.set_lang()
    
    def get_title(self,short):
        ''' Short titles are more valid than full titles, e.g.,
            'Gruzovik, obs.' -> 'Obsolete / dated' due to a bug
            at multitran.com. Thus, it's not necessary to check for
            'is_valid' key there.
        '''
        for key in SUBJECTS.keys():
            if SUBJECTS[key][self.lang]['short'] == short:
                return SUBJECTS[key][self.lang]['title']
        return short
    
    def set_lang(self):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.set_lang'
        result = locale.getdefaultlocale()
        if result and result[0]:
            result = result[0]
            if 'ru' in result:
                self.lang = 'ru'
            elif 'de' in result:
                self.lang = 'de'
            elif 'es' in result:
                self.lang = 'es'
            elif 'uk' in result:
                self.lang = 'uk'
        mes = '{} -> {}'.format(result,self.lang)
        sh.objs.get_mes(f,mes,True).show_debug()

    def _get_major_en(self,title):
        f = '[MClient] plugins.multitrancom.subjects.Subjects._get_group_en'
        for key in SUBJECTS.keys():
            if title == SUBJECTS[key][self.lang]['title']:
                return SUBJECTS[key]['major_en']
    
    def get_majors(self):
        # Takes ~0.0016s on Intel Atom
        majors = []
        for key in SUBJECTS.keys():
            if SUBJECTS[key]['is_major'] and SUBJECTS[key]['is_valid']:
                majors.append(SUBJECTS[key][self.lang]['title'])
        return sorted(majors)
    
    def get_major(self,title):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.get_major'
        major_en = self._get_major_en(title)
        if major_en:
            for key in SUBJECTS.keys():
                if major_en == SUBJECTS[key]['major_en'] \
                and SUBJECTS[key]['is_major']:
                    return SUBJECTS[key][self.lang]['title']
        else:
            sh.com.rep_empty(f)
    
    def get_group_with_header(self,title):
        ''' A possible way to speed up (if needed):
            1) get keys by the title, including the major subject
            2) iterate the resulting keys to find the major subject
            3) put the major subject to the top
            4) get titles by the resulting keys
        '''
        f = '[MClient] plugins.multitrancom.subjects.Subjects.get_group_with_header'
        major = self.get_major(title)
        group = self.get_group(title)
        if major and group:
            return [major] + group
        else:
            sh.com.rep_empty(f)
        return []
    
    def get_group(self,title):
        f = '[MClient] plugins.multitrancom.subjects.Subjects.get_group'
        # Takes ~0.002s on Intel Atom
        group = []
        major_en = self._get_major_en(title)
        if major_en:
            for key in SUBJECTS.keys():
                if major_en == SUBJECTS[key]['major_en'] \
                and not SUBJECTS[key]['is_major']:
                    group.append(SUBJECTS[key][self.lang]['title'])
        else:
            sh.com.rep_empty(f)
        return sorted(set(group))
    
    def get_list(self):
        # Takes ~0.15s on Intel Atom
        f = '[MClient] plugins.multitrancom.subjects.Subjects.get_list'
        lst = []
        majors = self.get_majors()
        for major in majors:
            group = self.get_group(major)
            if group:
                # Embedded lists
                #lst.append([major]+group)
                # Plain list
                lst += [major]
                lst += group
            else:
                mes = _('Wrong input data: "{}"!').format(major)
                sh.objs.get_mes(f,mes,True).show_warning()
        return lst



class Objects:
    
    def __init__(self):
        self.subjects = None
    
    def get_subjects(self):
        if self.subjects is None:
            self.subjects = Subjects()
        return self.subjects


objs = Objects()


if __name__ == '__main__':
    f = '[MClient] plugins.multitrancom.subjects.__main__'
    sh.com.start()
    isubj = Subjects()
    timer = sh.Timer(f)
    timer.start()
    #print(isubj.get_majors('uk'))
    #print(isubj.get_group('Біологія','uk'))
    #print(isubj.get_list())
    short = 'оруж.'
    mes = '"{}"'.format(isubj.get_title(short))
    sh.objs.get_mes(f,mes,True).show_debug()
    timer.end()
    sh.com.end()
