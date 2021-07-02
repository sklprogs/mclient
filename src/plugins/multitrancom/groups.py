#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import locale

from skl_shared.localize import _
import skl_shared.shared as sh

SUBJECTS = {'AI.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'AI.'
                   ,'title': 'Artificial intelligence'
                   }
               ,'uk':
                   {'short': 'шт.інтел.'
                   ,'title': 'Штучний інтелект'
                   }
               }
           ,'AIDS.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'AIDS.'
                   ,'title': 'AIDS'
                   }
               ,'uk':
                   {'short': 'СНІД'
                   ,'title': 'СНІД'
                   }
               }
           ,'AMEX.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'AMEX.'
                   ,'title': 'American stock exchange'
                   }
               ,'uk':
                   {'short': 'AMEX'
                   ,'title': 'Американська фондова біржа'
                   }
               }
           ,'ASCII.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'ASCII.'
                   ,'title': 'ASCII'
                   }
               ,'uk':
                   {'short': 'ASCII'
                   ,'title': 'ASCII'
                   }
               }
           ,'Alg.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Alg.'
                   ,'title': 'Algeria'
                   }
               ,'uk':
                   {'short': 'Алж.'
                   ,'title': 'Алжир'
                   }
               }
           ,'AmE':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'AmE'
                   ,'title': 'American English'
                   }
               ,'uk':
                   {'short': 'ам.англ.'
                   ,'title': 'Американський варіант англійської мови'
                   }
               }
           ,'Ant.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Ant.'
                   ,'title': 'Antilles'
                   }
               ,'uk':
                   {'short': 'Ант.остр.'
                   ,'title': 'Антильські острови'
                   }
               }
           ,'Apollo-Soyuz':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'Apollo-Soyuz'
                   ,'title': 'Apollo-Soyuz'
                   }
               ,'uk':
                   {'short': 'Союз-Аполлон'
                   ,'title': 'Союз-Аполлон'
                   }
               }
           ,'Arag.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Arag.'
                   ,'title': 'Aragon'
                   }
               ,'uk':
                   {'short': 'Араг.'
                   ,'title': 'Арагон'
                   }
               }
           ,'Arg.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Arg.'
                   ,'title': 'Argentina'
                   }
               ,'uk':
                   {'short': 'Арген.'
                   ,'title': 'Аргентина'
                   }
               }
           ,'Australia':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Australia'
                   ,'title': 'Australia'
                   }
               ,'uk':
                   {'short': 'Австралія'
                   ,'title': 'Австралія'
                   }
               }
           ,'Austria':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Austria'
                   ,'title': 'Austria'
                   }
               ,'uk':
                   {'short': 'Австр.'
                   ,'title': 'Австрія'
                   }
               }
           ,'Belar.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Belar.'
                   ,'title': 'Belarus'
                   }
               ,'uk':
                   {'short': 'Білор.'
                   ,'title': 'Білорусь'
                   }
               }
           ,'BrE':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'ingl.brit.'
                   ,'title': 'Inglés británico'
                   }
               ,'uk':
                   {'short': 'бр.англ.'
                   ,'title': 'Британський варіант англійської мови'
                   }
               }
           ,'Braz.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Braz.'
                   ,'title': 'Brazil'
                   }
               ,'uk':
                   {'short': 'Браз.'
                   ,'title': 'Бразилія'
                   }
               }
           ,'C.-R.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'C.-R.'
                   ,'title': 'Costa Rica'
                   }
               ,'uk':
                   {'short': 'К.-Р.'
                   ,'title': 'Коста-Рика'
                   }
               }
           ,'CNC':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               ,'uk':
                   {'short': 'CNC'
                   ,'title': 'Computer numerical control'
                   }
               }
           ,'CRT':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'CRT'
                   ,'title': 'Cathode-ray tubes'
                   }
               ,'uk':
                   {'short': 'ЕПТ'
                   ,'title': 'Електронно-променеві трубки'
                   }
               }
           ,'CT':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'CT'
                   ,'title': 'Computer tomography'
                   }
               ,'uk':
                   {'short': 'КТ'
                   ,'title': "Комп'ютерна томографія"}}, 'Canada':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Canada'
                   ,'title': 'Canada'
                   }
               ,'uk':
                   {'short': 'Канада'
                   ,'title': 'Канада'
                   }
               }
           ,'Centr.Am.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Centr.Am.'
                   ,'title': 'Central America'
                   }
               ,'uk':
                   {'short': 'Ц.Ам.'
                   ,'title': 'Центральна Америка'
                   }
               }
           ,'Chil.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Chil.'
                   ,'title': 'Chile'
                   }
               ,'uk':
                   {'short': 'Чилі'
                   ,'title': 'Чилі'
                   }
               }
           ,'China':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'China'
                   ,'title': 'China'
                   }
               ,'uk':
                   {'short': 'Китай'
                   ,'title': 'Китай'
                   }
               }
           ,'Col.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Col.'
                   ,'title': 'Columbia'
                   }
               ,'uk':
                   {'short': 'Колум.'
                   ,'title': 'Колумбія'
                   }
               }
           ,'Cuba':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Cuba'
                   ,'title': 'Cuba'
                   }
               ,'uk':
                   {'short': 'Куба.'
                   ,'title': 'Куба'
                   }
               }
           ,'Cypr.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Cypr.'
                   ,'title': 'Cyprus'
                   }
               ,'uk':
                   {'short': 'Кіпр'
                   ,'title': 'Кіпр'
                   }
               }
           ,'Dutch':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'holand.'
                   ,'title': 'Holandés'
                   }
               ,'uk':
                   {'short': 'голл.'
                   ,'title': 'Голландська (нідерландська) мова'
                   }
               }
           ,'EBRD':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'EBRD'
                   ,'title': 'European Bank for Reconstruction and Development'
                   }
               ,'uk':
                   {'short': 'ЄБРР'
                   ,'title': 'Європейський банк реконструкції та розвитку'
                   }
               }
           ,'EU.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'EU.'
                   ,'title': 'European Union'
                   }
               ,'uk':
                   {'short': 'ЄС'
                   ,'title': 'Європейський Союз'
                   }
               }
           ,'Ecuad.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'Ecuad.'
                   ,'title': 'Ecuador'
                   }
               ,'uk':
                   {'short': 'Еквад.'
                   ,'title': 'Еквадор'
                   }
               }
           ,'FBI.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'FBI.'
                   ,'title': 'Federal Bureau of Investigation'
                   }
               ,'uk':
                   {'short': 'ФБР'
                   ,'title': 'Федеральне бюро розслідувань'
                   }
               }
           ,'GDR':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'GDR'
                   ,'title': 'East Germany'
                   }
               ,'uk':
                   {'short': 'іст., НДР'
                   ,'title': 'Термін часів НДР'
                   }
               }
           ,'Germ.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Germ.'
                   ,'title': 'Germany'
                   }
               ,'uk':
                   {'short': 'Німеч.'
                   ,'title': 'Німеччина'
                   }
               }
           ,'Gruzovik':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'Gruzovik'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'Gruzovik, GOST.':
               {'valid': False
               ,'major': False
               ,'group': 'Quality control and standards'
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
               ,'sp':
                   {'short': 'Gruzovik, GOST.'
                   ,'title': 'GOST'
                   }
               ,'uk':
                   {'short': 'Gruzovik, станд.'
                   ,'title': 'Стандарти'
                   }
               }
           ,'Gruzovik, IT':
               {'valid': False
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'Gruzovik, IT'
                   ,'title': 'Інформаційні технології'
                   }
               }
           ,'Gruzovik, abbr.':
               {'valid': False
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'Gruzovik, abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'Gruzovik, abbr., IT':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, abrev., IT'
                   ,'title': 'Abreviatura, Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., IT'
                   ,'title': 'Абревіатура, Інформаційні технології'
                   }
               }
           ,'Gruzovik, abbr., account.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, abrev., cont.'
                   ,'title': 'Abreviatura, Contabilidad'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., бухг.'
                   ,'title': 'Абревіатура, Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'Gruzovik, abbr., bank.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, abrev., bank.'
                   ,'title': 'Abreviatura, Banking'
                   }
               ,'uk':
                   {'short': 'Gruzovik, абрев., банк.'
                   ,'title': 'Абревіатура, Банки та банківська справа'
                   }
               }
           ,'Gruzovik, adm.law.':
               {'valid': False
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'Gruzovik, adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'uk':
                   {'short': 'Gruzovik, адмін.пр.'
                   ,'title': 'Адміністративне право'
                   }
               }
           ,'Gruzovik, adv.':
               {'valid': False
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'Gruzovik, adv.'
                   ,'title': 'Advertising'
                   }
               ,'uk':
                   {'short': 'Gruzovik, рекл.'
                   ,'title': 'Реклама'
                   }
               }
           ,'Gruzovik, aer.phot.':
               {'valid': False
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'Gruzovik, aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, аерофот.'
                   ,'title': 'Аерофозйомка та топографія'
                   }
               }
           ,'Gruzovik, agric.':
               {'valid': False
               ,'major': True
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'Gruzovik, agric.'
                   ,'title': 'Agricultura'
                   }
               ,'uk':
                   {'short': 'Gruzovik, с/г.'
                   ,'title': 'Сільське господарство'
                   }
               }
           ,'Gruzovik, ballist.':
               {'valid': False
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'Gruzovik, ballist.'
                   ,'title': 'Ballistics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, баліст.'
                   ,'title': 'Балістика'
                   }
               }
           ,'Gruzovik, biogeogr.':
               {'valid': False
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'Gruzovik, biogeogr.'
                   ,'title': 'Biogeography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, біогеогр.'
                   ,'title': 'Біогеографія'
                   }
               }
           ,'Gruzovik, bot.':
               {'valid': False
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'Gruzovik, bot.'
                   ,'title': 'Botánica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, бот.'
                   ,'title': 'Ботаніка'
                   }
               }
           ,'Gruzovik, cloth.':
               {'valid': False
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'Gruzovik, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'Gruzovik, comp.':
               {'valid': False
               ,'major': True
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'Gruzovik, comp.'
                   ,'title': 'Computadores'
                   }
               ,'uk':
                   {'short': 'Gruzovik, комп.'
                   ,'title': "Комп'ютери"}}, 'Gruzovik, cryptogr.':
               {'valid': False
               ,'major': False
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'Gruzovik, cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'uk':
                   {'short': 'Gruzovik, крипт.'
                   ,'title': 'Криптографія'
                   }
               }
           ,'Gruzovik, dial.':
               {'valid': False
               ,'major': True
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'Gruzovik, dial.'
                   ,'title': 'Dialecto'
                   }
               ,'uk':
                   {'short': 'Gruzovik, діал.'
                   ,'title': 'Діалектизм'
                   }
               }
           ,'Gruzovik, econ.':
               {'valid': False
               ,'major': True
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'Gruzovik, econ.'
                   ,'title': 'Economía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ек.'
                   ,'title': 'Економіка'
                   }
               }
           ,'Gruzovik, el.':
               {'valid': False
               ,'major': True
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'Gruzovik, electr.'
                   ,'title': 'Electrónica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ел.'
                   ,'title': 'Електроніка'
                   }
               }
           ,'Gruzovik, electric.':
               {'valid': False
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'Gruzovik, electric.'
                   ,'title': 'Electricity'
                   }
               ,'uk':
                   {'short': 'Gruzovik, електр.'
                   ,'title': 'Електричний струм'
                   }
               }
           ,'Gruzovik, email':
               {'valid': False
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'Gruzovik, email'
                   ,'title': 'E-mail'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ел.пошт.'
                   ,'title': 'Електронна пошта'
                   }
               }
           ,'Gruzovik, expl.':
               {'valid': False
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'Gruzovik, expl.'
                   ,'title': 'Explosives'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вибух.'
                   ,'title': 'Вибухові речовини'
                   }
               }
           ,'Gruzovik, fig.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, fig.'
                   ,'title': 'Figuradamente'
                   }
               ,'uk':
                   {'short': 'Gruzovik, перен.'
                   ,'title': 'Переносний сенс'
                   }
               }
           ,'Gruzovik, footwear':
               {'valid': False
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'Gruzovik, footwear'
                   ,'title': 'Footwear'
                   }
               ,'uk':
                   {'short': 'Gruzovik, взут.'
                   ,'title': 'Взуття'
                   }
               }
           ,'Gruzovik, fr.':
               {'valid': False
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'Gruzovik, fr.'
                   ,'title': 'Francés'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фр.'
                   ,'title': 'Французька мова'
                   }
               }
           ,'Gruzovik, garden.':
               {'valid': False
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'Gruzovik, garden.'
                   ,'title': 'Gardening'
                   }
               ,'uk':
                   {'short': 'Gruzovik, садівн.'
                   ,'title': 'Садівництво'
                   }
               }
           ,'Gruzovik, glac.':
               {'valid': False
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'Gruzovik, glac.'
                   ,'title': 'Glaciology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, гляц.'
                   ,'title': 'Гляціологія'
                   }
               }
           ,'Gruzovik, horse.breed.':
               {'valid': False
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'Gruzovik, horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'uk':
                   {'short': 'Gruzovik, кон.'
                   ,'title': 'Конярство'
                   }
               }
           ,'Gruzovik, hunt.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, caza'
                   ,'title': 'Caza y cinegética'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мислив.'
                   ,'title': 'Мисливство та мисливствознавство'
                   }
               }
           ,'Gruzovik, inform.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'Gruzovik, розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'Gruzovik, law':
               {'valid': False
               ,'major': True
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'Gruzovik, jur.'
                   ,'title': 'Jurídico'
                   }
               ,'uk':
                   {'short': 'Gruzovik, юр.'
                   ,'title': 'Юридична лексика'
                   }
               }
           ,'Gruzovik, mach.mech.':
               {'valid': False
               ,'major': True
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'Gruzovik, mach.mech.'
                   ,'title': 'Machinery and mechanisms'
                   }
               ,'uk':
                   {'short': 'Gruzovik, маш.мех.'
                   ,'title': 'Машини та механізми'
                   }
               }
           ,'Gruzovik, magn.':
               {'valid': False
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'Gruzovik, magn.'
                   ,'title': 'Magnetics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, магн.'
                   ,'title': 'Магнетизм'
                   }
               }
           ,'Gruzovik, math.':
               {'valid': False
               ,'major': True
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'Gruzovik, mat.'
                   ,'title': 'Matemáticas'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мат.'
                   ,'title': 'Математика'
                   }
               }
           ,'Gruzovik, med.':
               {'valid': False
               ,'major': True
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'Gruzovik, med.'
                   ,'title': 'Medicina'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мед.'
                   ,'title': 'Медицина'
                   }
               }
           ,'Gruzovik, media.':
               {'valid': False
               ,'major': True
               ,'group': 'Mass media'
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
               ,'sp':
                   {'short': 'Gruzovik, media.'
                   ,'title': 'Mass media'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ЗМІ'
                   ,'title': 'Засоби масової інформації'
                   }
               }
           ,'Gruzovik, met.phys.':
               {'valid': False
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'Gruzovik, met.phys.'
                   ,'title': 'Metal physics'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фіз.мет.'
                   ,'title': 'Фізика металів'
                   }
               }
           ,'Gruzovik, mil.':
               {'valid': False
               ,'major': True
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'Gruzovik, mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'Gruzovik, mil., air.def.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'Gruzovik, mil., air.def.'
                   ,'title': 'Air defense'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., ППО'
                   ,'title': 'Протиповітряна оборона'
                   }
               }
           ,'Gruzovik, mil., arm.veh.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'Gruzovik, mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., брон.'
                   ,'title': 'Бронетехніка'
                   }
               }
           ,'Gruzovik, mil., artil.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'Gruzovik, mil.,artill.'
                   ,'title': 'Artillería'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., арт.'
                   ,'title': 'Артилерія'
                   }
               }
           ,'Gruzovik, mil., avia.':
               {'valid': False
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'Gruzovik, mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ., авіац.'
                   ,'title': 'Військова авіація'
                   }
               }
           ,'Gruzovik, mycol.':
               {'valid': False
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'Gruzovik, mycol.'
                   ,'title': 'Mycology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мікол.'
                   ,'title': 'Мікологія'
                   }
               }
           ,'Gruzovik, myth.':
               {'valid': False
               ,'major': True
               ,'group': 'Mythology'
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
               ,'sp':
                   {'short': 'Gruzovik, mitol.'
                   ,'title': 'Mitología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, міф.'
                   ,'title': 'Міфологія'
                   }
               }
           ,'Gruzovik, nautic.':
               {'valid': False
               ,'major': True
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'Gruzovik, náut.'
                   ,'title': 'Náutico'
                   }
               ,'uk':
                   {'short': 'Gruzovik, мор.'
                   ,'title': 'Морський термін'
                   }
               }
           ,'Gruzovik, obs.':
               {'valid': False
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'Gruzovik, antic.'
                   ,'title': 'Anticuado'
                   }
               ,'uk':
                   {'short': 'Gruzovik, застар.'
                   ,'title': 'Застаріле'
                   }
               }
           ,'Gruzovik, ocean.':
               {'valid': False
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'Gruzovik, ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'uk':
                   {'short': 'Gruzovik, океан.'
                   ,'title': 'Океанологія (океанографія)'
                   }
               }
           ,'Gruzovik, paraglid.':
               {'valid': False
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'Gruzovik, paraglid.'
                   ,'title': 'Paragliding'
                   }
               ,'uk':
                   {'short': 'Gruzovik, параплан.'
                   ,'title': 'Парапланеризм'
                   }
               }
           ,'Gruzovik, philolog.':
               {'valid': False
               ,'major': True
               ,'group': 'Philology'
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
               ,'sp':
                   {'short': 'Gruzovik, philolog.'
                   ,'title': 'Philology'
                   }
               ,'uk':
                   {'short': 'Gruzovik, філол.'
                   ,'title': 'Філологія'
                   }
               }
           ,'Gruzovik, phonet.':
               {'valid': False
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'Gruzovik, fonét.'
                   ,'title': 'Fonética'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фон.'
                   ,'title': 'Фонетика'
                   }
               }
           ,'Gruzovik, photo.':
               {'valid': False
               ,'major': True
               ,'group': 'Photography'
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
               ,'sp':
                   {'short': 'Gruzovik, fotogr.'
                   ,'title': 'Fotografía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, фото'
                   ,'title': 'Фотографія'
                   }
               }
           ,'Gruzovik, poetic':
               {'valid': False
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'Gruzovik, poét.'
                   ,'title': 'Poético'
                   }
               ,'uk':
                   {'short': 'Gruzovik, поет.'
                   ,'title': 'Поетична мова'
                   }
               }
           ,'Gruzovik, polit.':
               {'valid': False
               ,'major': True
               ,'group': 'Politics'
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
               ,'sp':
                   {'short': 'Gruzovik, polít.'
                   ,'title': 'Política'
                   }
               ,'uk':
                   {'short': 'Gruzovik, політ.'
                   ,'title': 'Політика'
                   }
               }
           ,'Gruzovik, polygr.':
               {'valid': False
               ,'major': False
               ,'group': 'Publishing'
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
               ,'sp':
                   {'short': 'Gruzovik, poligr.'
                   ,'title': 'Poligrafía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, полігр.'
                   ,'title': 'Поліграфія'
                   }
               }
           ,'Gruzovik, prof.jarg.':
               {'valid': False
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'Gruzovik, profesion.'
                   ,'title': 'Jerga profesional'
                   }
               ,'uk':
                   {'short': 'Gruzovik, проф.жарг.'
                   ,'title': 'Професійний жаргон'
                   }
               }
           ,'Gruzovik, prop.&figur.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'uk':
                   {'short': 'Gruzovik, прям.перен.'
                   ,'title': 'Прямий і переносний сенс'
                   }
               }
           ,'Gruzovik, radio':
               {'valid': False
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'Gruzovik, radio'
                   ,'title': 'Radio'
                   }
               ,'uk':
                   {'short': 'Gruzovik, радіо'
                   ,'title': 'Радіо'
                   }
               }
           ,'Gruzovik, rel., jud.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'Gruzovik, rel., jud.'
                   ,'title': 'Judaism'
                   }
               ,'uk':
                   {'short': 'Gruzovik, юд.'
                   ,'title': 'Юдаїзм'
                   }
               }
           ,'Gruzovik, row.':
               {'valid': False
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'Gruzovik, row.'
                   ,'title': 'Rowing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, весл.'
                   ,'title': 'Веслування'
                   }
               }
           ,'Gruzovik, sail.':
               {'valid': False
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'Gruzovik, sail.'
                   ,'title': 'Sailing'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вітр.спорт'
                   ,'title': 'Вітрильний спорт'
                   }
               }
           ,'Gruzovik, scient.':
               {'valid': False
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'Gruzovik, scient.'
                   ,'title': 'Scientific'
                   }
               ,'uk':
                   {'short': 'Gruzovik, науков.'
                   ,'title': 'Науковий термін'
                   }
               }
           ,'Gruzovik, sculp.':
               {'valid': False
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'Gruzovik, sculp.'
                   ,'title': 'Sculpture'
                   }
               ,'uk':
                   {'short': 'Gruzovik, скульп.'
                   ,'title': 'Скульптура'
                   }
               }
           ,'Gruzovik, slang':
               {'valid': False
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'Gruzovik, jerg.'
                   ,'title': 'Jerga'
                   }
               ,'uk':
                   {'short': 'Gruzovik, сленг'
                   ,'title': 'Сленг'
                   }
               }
           ,'Gruzovik, slavon.':
               {'valid': False
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'Gruzovik, slavon.'
                   ,'title': 'Slavonic'
                   }
               ,'uk':
                   {'short': 'Gruzovik, слов’ян.'
                   ,'title': 'Слов’янський вираз'
                   }
               }
           ,'Gruzovik, social.sc.':
               {'valid': False
               ,'major': False
               ,'group': 'Education'
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
               ,'sp':
                   {'short': 'Gruzovik, social.sc.'
                   ,'title': 'Social science'
                   }
               ,'uk':
                   {'short': 'Gruzovik, суспільс.'
                   ,'title': 'Суспільствознавство'
                   }
               }
           ,'Gruzovik, spin.':
               {'valid': False
               ,'major': False
               ,'group': 'Crafts'
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
               ,'sp':
                   {'short': 'Gruzovik, spin.'
                   ,'title': 'Spinning'
                   }
               ,'uk':
                   {'short': 'Gruzovik, пряд.'
                   ,'title': 'Прядіння'
                   }
               }
           ,'Gruzovik, sport.':
               {'valid': False
               ,'major': True
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'Gruzovik, dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'Gruzovik, спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'Gruzovik, sport.goods':
               {'valid': False
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'Gruzovik, sport.goods'
                   ,'title': 'Sporting goods'
                   }
               ,'uk':
                   {'short': 'Gruzovik, спорт.тов.'
                   ,'title': 'Спорттовари'
                   }
               }
           ,'Gruzovik, surv.':
               {'valid': False
               ,'major': False
               ,'group': 'Sociology'
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
               ,'sp':
                   {'short': 'Gruzovik, surv.'
                   ,'title': 'Survey'
                   }
               ,'uk':
                   {'short': 'Gruzovik, соц.опит.'
                   ,'title': 'Соціологічне опитування'
                   }
               }
           ,'Gruzovik, tech.':
               {'valid': False
               ,'major': True
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'Gruzovik, tec.'
                   ,'title': 'Tecnología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, техн.'
                   ,'title': 'Техніка'
                   }
               }
           ,'Gruzovik, tel.':
               {'valid': False
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'Gruzovik, tel.'
                   ,'title': 'Telephony'
                   }
               ,'uk':
                   {'short': 'Gruzovik, тлф.'
                   ,'title': 'Телефонія'
                   }
               }
           ,'Gruzovik, terat.':
               {'valid': False
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'Gruzovik, terat.'
                   ,'title': 'Teratología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, терат.'
                   ,'title': 'Тератологія'
                   }
               }
           ,'Gruzovik, topogr.':
               {'valid': False
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'Gruzovik, topogr.'
                   ,'title': 'Topografía'
                   }
               ,'uk':
                   {'short': 'Gruzovik, топ.'
                   ,'title': 'Топографія'
                   }
               }
           ,'Gruzovik, typewrit.':
               {'valid': False
               ,'major': False
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'Gruzovik, typewrit.'
                   ,'title': 'Typewriters and typewriting'
                   }
               ,'uk':
                   {'short': 'Gruzovik, друк.маш.'
                   ,'title': 'Друкарські машинки та машинопис'
                   }
               }
           ,'Gruzovik, vent.':
               {'valid': False
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'Gruzovik, vent.'
                   ,'title': 'Ventilation'
                   }
               ,'uk':
                   {'short': 'Gruzovik, вент.'
                   ,'title': 'Вентиляція'
                   }
               }
           ,'Gruzovik, weav.':
               {'valid': False
               ,'major': False
               ,'group': 'Crafts'
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
               ,'sp':
                   {'short': 'Gruzovik, weav.'
                   ,'title': 'Weaving'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ткац.'
                   ,'title': 'Ткацтво'
                   }
               }
           ,'Gruzovik, written':
               {'valid': False
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'Gruzovik, written'
                   ,'title': 'Written'
                   }
               ,'uk':
                   {'short': 'Gruzovik, письм.'
                   ,'title': 'Письмове мовлення'
                   }
               }
           ,'Gruzovik, zool.':
               {'valid': False
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'Gruzovik, zool.'
                   ,'title': 'Zoología'
                   }
               ,'uk':
                   {'short': 'Gruzovik, зоол.'
                   ,'title': 'Зоологія'
                   }
               }
           ,'Guatem.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Guatem.'
                   ,'title': 'Guatemala'
                   }
               ,'uk':
                   {'short': 'Гват.'
                   ,'title': 'Гватемала'
                   }
               }
           ,'HF.electr.':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'HF.electr.'
                   ,'title': 'High frequency electronics'
                   }
               ,'uk':
                   {'short': 'ВЧ.ел.'
                   ,'title': 'Високочастотна електроніка'
                   }
               }
           ,'HR':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'HR'
                   ,'title': 'Human resources'
                   }
               ,'uk':
                   {'short': 'кадри'
                   ,'title': 'Кадри'
                   }
               }
           ,'IMF.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'IMF.'
                   ,'title': 'International Monetary Fund'
                   }
               ,'uk':
                   {'short': 'МВФ'
                   ,'title': 'Міжнародний валютний фонд'
                   }
               }
           ,'IT':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'IT'
                   ,'title': 'Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'IT'
                   ,'title': 'Інформаційні технології'
                   }
               }
           ,'India':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'India'
                   ,'title': 'India'
                   }
               ,'uk':
                   {'short': 'Індія'
                   ,'title': 'Індія'
                   }
               }
           ,'Indones.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'Indones.'
                   ,'title': 'Indonesian'
                   }
               ,'uk':
                   {'short': 'індонез.'
                   ,'title': 'Індонезійський вираз'
                   }
               }
           ,'Iran':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Iran'
                   ,'title': 'Iran'
                   }
               ,'uk':
                   {'short': 'Іран'
                   ,'title': 'Іран'
                   }
               }
           ,'Kazakh.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Kazakh.'
                   ,'title': 'Kazakhstan'
                   }
               ,'uk':
                   {'short': 'Казах.'
                   ,'title': 'Казахстан'
                   }
               }
           ,'Kyrgyz.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Kyrgyz.'
                   ,'title': 'Kyrgyzstan'
                   }
               ,'uk':
                   {'short': 'Киргиз.'
                   ,'title': 'Киргизстан'
                   }
               }
           ,'LP.play.':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'LP.play.'
                   ,'title': 'LP players'
                   }
               ,'uk':
                   {'short': 'прогр.вініл.'
                   ,'title': 'Програвачі вінілових дисків'
                   }
               }
           ,'MSDS':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'MSDS'
                   ,'title': 'Material safety data sheet'
                   }
               ,'uk':
                   {'short': 'ПБР'
                   ,'title': 'Паспорт безпеки речовини'
                   }
               }
           ,'Makarov.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Makarov.'
                   ,'title': 'Makarov'
                   }
               ,'uk':
                   {'short': 'Макаров'
                   ,'title': 'Макаров'
                   }
               }
           ,'Makarov., inform., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Makarov., inf., amer.'
                   ,'title': 'Makarov, Informal, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'Макаров, розмовн., амер.вир.'
                   ,'title': 'Макаров, Розмовна лексика, Американський вираз (не варыант мови)'
                   }
               }
           ,'Moroc.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Moroc.'
                   ,'title': 'Morocco'
                   }
               ,'uk':
                   {'short': 'Марок.'
                   ,'title': 'Марокко'
                   }
               }
           ,'N.Ireland.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'N.Ireland.'
                   ,'title': 'Northern Ireland'
                   }
               ,'uk':
                   {'short': 'Півн.Ірл.'
                   ,'title': 'Північна Ірландія'
                   }
               }
           ,'NASA':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'NASA'
                   ,'title': 'NASA'
                   }
               ,'uk':
                   {'short': 'НАСА'
                   ,'title': 'НАСА'
                   }
               }
           ,'NATO':
               {'valid': True
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'NATO'
                   ,'title': 'NATO'
                   }
               ,'uk':
                   {'short': 'НАТО'
                   ,'title': 'НАТО'
                   }
               }
           ,'NGO':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'NGO'
                   ,'title': 'Non-governmental organizations'
                   }
               ,'uk':
                   {'short': 'гром.орг.'
                   ,'title': 'Громадські організації'
                   }
               }
           ,'NYSE.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'NYSE.'
                   ,'title': 'New York Stock Exchange'
                   }
               ,'uk':
                   {'short': 'NYSE'
                   ,'title': 'Нью-Йоркська фондова біржа'
                   }
               }
           ,'Nasdaq':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'Nasdaq'
                   ,'title': 'NASDAQ'
                   }
               ,'uk':
                   {'short': 'НАСДАК'
                   ,'title': 'НАСДАК'
                   }
               }
           ,'Netherl., law, court':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Netherl., law, court'
                   ,'title': 'Netherlands, Court (law)'
                   }
               ,'uk':
                   {'short': 'Нідерл., юр., суд.'
                   ,'title': 'Нідерланди, Судова лексика'
                   }
               }
           ,'O&G':
               {'valid': True
               ,'major': True
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G'
                   ,'title': 'Oil and gas'
                   }
               ,'uk':
                   {'short': 'нафт.газ'
                   ,'title': 'Нафта і газ'
                   }
               }
           ,'O&G, casp.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, casp.'
                   ,'title': 'Caspian'
                   }
               ,'uk':
                   {'short': 'нафт.газ., касп.'
                   ,'title': 'Каспій'
                   }
               }
           ,'O&G, karach.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, karach.'
                   ,'title': 'Karachaganak'
                   }
               ,'uk':
                   {'short': 'нафт.газ., карач.'
                   ,'title': 'Карачаганак'
                   }
               }
           ,'O&G, molikpaq.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, molikpaq.'
                   ,'title': 'Molikpaq'
                   }
               ,'uk':
                   {'short': 'нафт.газ., молікп.'
                   ,'title': 'Молікпак'
                   }
               }
           ,'O&G, oilfield.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, oilfield.'
                   ,'title': 'Oilfields'
                   }
               ,'uk':
                   {'short': 'нафтопром.'
                   ,'title': 'Нафтопромисловий'
                   }
               }
           ,'O&G, sahk.r.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, sahk.r.'
                   ,'title': 'Sakhalin R'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.р.'
                   ,'title': 'Сахалін Р'
                   }
               }
           ,'O&G, sahk.s.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, sahk.s.'
                   ,'title': 'Sakhalin S'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.ю.'
                   ,'title': 'Сахалін Ю'
                   }
               }
           ,'O&G, sakh.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, sakh.'
                   ,'title': 'Sakhalin'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.'
                   ,'title': 'Сахалін'
                   }
               }
           ,'O&G, sakh., geol.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'O&G, sakh., geol.'
                   ,'title': 'Sakhalin, Geología'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал., геолог.'
                   ,'title': 'Сахалін, Геологія'
                   }
               }
           ,'O&G, sakh.a.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, sakh.a.'
                   ,'title': 'Sakhalin A'
                   }
               ,'uk':
                   {'short': 'нафт.газ., сахал.а.'
                   ,'title': 'Сахалін А'
                   }
               }
           ,'O&G, tengiz.':
               {'valid': False
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G, tengiz.'
                   ,'title': 'Tengiz'
                   }
               ,'uk':
                   {'short': 'нафт.газ., тенгіз.'
                   ,'title': 'Тенгізшевройл'
                   }
               }
           ,'O&G. tech.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'O&G. tech.'
                   ,'title': 'Oil and gas technology'
                   }
               ,'uk':
                   {'short': 'нафт.газ.тех.'
                   ,'title': 'Нафтогазова техніка'
                   }
               }
           ,'OHS':
               {'valid': True
               ,'major': True
               ,'group': 'Occupational health & safety'
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
               ,'sp':
                   {'short': 'OHS'
                   ,'title': 'Occupational health & safety'
                   }
               ,'uk':
                   {'short': 'ОПіТБ'
                   ,'title': 'Охорона праці та техніка безпеки'
                   }
               }
           ,'PCB':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'PCB'
                   ,'title': 'Printed circuit boards'
                   }
               ,'uk':
                   {'short': 'друк.пл.'
                   ,'title': 'Друковані плати'
                   }
               }
           ,'PPE':
               {'valid': True
               ,'major': False
               ,'group': 'Occupational health & safety'
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
               ,'sp':
                   {'short': 'PPE'
                   ,'title': 'Personal protective equipment'
                   }
               ,'uk':
                   {'short': 'зас.зах.'
                   ,'title': 'Засоби індивідуального захисту'
                   }
               }
           ,'PR':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'PR'
                   ,'title': 'Public relations'
                   }
               ,'uk':
                   {'short': 'піар.'
                   ,'title': 'Паблік рілейшнз'
                   }
               }
           ,'PSP':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'PSP'
                   ,'title': 'Power system protection'
                   }
               ,'uk':
                   {'short': 'РЗА'
                   ,'title': 'Релейний захист і автоматика'
                   }
               }
           ,'Panam.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Panam.'
                   ,'title': 'Panama'
                   }
               ,'uk':
                   {'short': 'Панама'
                   ,'title': 'Панама'
                   }
               }
           ,'Peru.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Peru.'
                   ,'title': 'Peru'
                   }
               ,'uk':
                   {'short': 'Перу'
                   ,'title': 'Перу'
                   }
               }
           ,'Philipp.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Philipp.'
                   ,'title': 'Philippines'
                   }
               ,'uk':
                   {'short': 'Філ.'
                   ,'title': 'Філіппіни'
                   }
               }
           ,'R&D.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'R&D.'
                   ,'title': 'Research and development'
                   }
               ,'uk':
                   {'short': 'наук.-досл.'
                   ,'title': 'Науково-дослідницька діяльність'
                   }
               }
           ,'Russia':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Russia'
                   ,'title': 'Russia'
                   }
               ,'uk':
                   {'short': 'Росія'
                   ,'title': 'Росія'
                   }
               }
           ,'S.Amer.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'S.Amer.'
                   ,'title': 'South America'
                   }
               ,'uk':
                   {'short': 'Півд.Ам.'
                   ,'title': 'Південна Америка'
                   }
               }
           ,'SAP.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'SAP.'
                   ,'title': 'SAP'
                   }
               ,'uk':
                   {'short': 'SAP'
                   ,'title': 'SAP'
                   }
               }
           ,'SAP.fin.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'SAP.fin.'
                   ,'title': 'SAP finance'
                   }
               ,'uk':
                   {'short': 'SAP фін.'
                   ,'title': 'SAP фінанси'
                   }
               }
           ,'SAP.tech.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'SAP.tech.'
                   ,'title': 'SAP tech.'
                   }
               ,'uk':
                   {'short': 'SAP тех.'
                   ,'title': 'SAP технічні терміни'
                   }
               }
           ,'Scotl.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Escoc.'
                   ,'title': 'Escocia'
                   }
               ,'uk':
                   {'short': 'Шотл.'
                   ,'title': 'Шотландія'
                   }
               }
           ,'Spain':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Spain'
                   ,'title': 'Spain'
                   }
               ,'uk':
                   {'short': 'Іспан.'
                   ,'title': 'Іспанія'
                   }
               }
           ,'TV':
               {'valid': True
               ,'major': False
               ,'group': 'Mass media'
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
               ,'sp':
                   {'short': 'TV'
                   ,'title': 'Televisión'
                   }
               ,'uk':
                   {'short': 'тлб.'
                   ,'title': 'Телебачення'
                   }
               }
           ,'UK':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'UK'
                   ,'title': 'United Kingdom'
                   }
               ,'uk':
                   {'short': 'Брит.'
                   ,'title': 'Велика Британія'
                   }
               }
           ,'UN':
               {'valid': True
               ,'major': True
               ,'group': 'United Nations'
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
               ,'sp':
                   {'short': 'UN'
                   ,'title': 'United Nations'
                   }
               ,'uk':
                   {'short': 'ООН'
                   ,'title': "Організація Об'єднаних Націй"}}, 'USA':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'USA'
                   ,'title': 'United States'
                   }
               ,'uk':
                   {'short': 'США'
                   ,'title': 'Сполучені Штати Америки'
                   }
               }
           ,'Ukraine':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Ukraine'
                   ,'title': 'Ukraine'
                   }
               ,'uk':
                   {'short': 'Україна'
                   ,'title': 'Україна'
                   }
               }
           ,'Venezuel.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'Venezuel.'
                   ,'title': 'Venezuela'
                   }
               ,'uk':
                   {'short': 'Венес.'
                   ,'title': 'Венесуела'
                   }
               }
           ,'WTO.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'WTO.'
                   ,'title': 'World trade organization'
                   }
               ,'uk':
                   {'short': 'СОТ'
                   ,'title': 'Світова організація торгівлі'
                   }
               }
           ,'abbr.':
               {'valid': True
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'abbr., O&G, casp.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, casp.'
                   ,'title': 'Abreviatura, Caspian'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., касп.'
                   ,'title': 'Абревіатура, Каспій'
                   }
               }
           ,'abbr., O&G, karach.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, karach.'
                   ,'title': 'Abreviatura, Karachaganak'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., карач.'
                   ,'title': 'Абревіатура, Карачаганак'
                   }
               }
           ,'abbr., O&G, sahk.r.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, sahk.r.'
                   ,'title': 'Abreviatura, Sakhalin R'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.р.'
                   ,'title': 'Абревіатура, Сахалін Р'
                   }
               }
           ,'abbr., O&G, sahk.s.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, sahk.s.'
                   ,'title': 'Abreviatura, Sakhalin S'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.ю.'
                   ,'title': 'Абревіатура, Сахалін Ю'
                   }
               }
           ,'abbr., O&G, sakh.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, sakh.'
                   ,'title': 'Abreviatura, Sakhalin'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.'
                   ,'title': 'Абревіатура, Сахалін'
                   }
               }
           ,'abbr., O&G, sakh.a.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., O&G, sakh.a.'
                   ,'title': 'Abreviatura, Sakhalin A'
                   }
               ,'uk':
                   {'short': 'абрев., нафт.газ., сахал.а.'
                   ,'title': 'Абревіатура, Сахалін А'
                   }
               }
           ,'abbr., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., amer.'
                   ,'title': 'Abreviatura, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'абрев., амер.вир.'
                   ,'title': 'Абревіатура, Американський вираз (не варыант мови)'
                   }
               }
           ,'abbr., amer.usg., slang':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., amer., jerg.'
                   ,'title': 'Abreviatura, Americano (uso), Jerga'
                   }
               ,'uk':
                   {'short': 'абрев., амер.вир., сленг'
                   ,'title': 'Абревіатура, Американський вираз (не варыант мови), Сленг'
                   }
               }
           ,'abbr., avia., avia., ICAO':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., avia., avia., ICAO'
                   ,'title': 'Abreviatura, Aviación, ICAO'
                   }
               ,'uk':
                   {'short': 'абрев., авіац., авіац., ІКАО'
                   ,'title': 'Абревіатура, Авіація, ІКАО'
                   }
               }
           ,'abbr., avia., med.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., avia., med.'
                   ,'title': 'Abreviatura, Aviation medicine'
                   }
               ,'uk':
                   {'short': 'абрев., авіац., мед.'
                   ,'title': 'Абревіатура, Авіаційна медицина'
                   }
               }
           ,'abbr., comp., MS':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., comp., MS'
                   ,'title': 'Abreviatura, Microsoft'
                   }
               ,'uk':
                   {'short': 'абрев., комп., Майкр.'
                   ,'title': 'Абревіатура, Майкрософт'
                   }
               }
           ,'abbr., comp., net.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., comp., net.'
                   ,'title': 'Abreviatura, Computer networks'
                   }
               ,'uk':
                   {'short': 'абрев., комп., мереж.'
                   ,'title': "Абревіатура, Комп'ютерні мережі"}}, 'abbr., comp., net., IT':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., comp., net., IT'
                   ,'title': 'Abreviatura, Computer networks, Tecnología de la información'
                   }
               ,'uk':
                   {'short': 'абрев., комп., мереж., IT'
                   ,'title': "Абревіатура, Комп'ютерні мережі, Інформаційні технології"}}, 'abbr., fant./sci-fi.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., fant./sci-fi.'
                   ,'title': 'Abreviatura, Fantasy and science fiction'
                   }
               ,'uk':
                   {'short': 'абрев., фант.'
                   ,'title': 'Абревіатура, Фантастика, фентезі'
                   }
               }
           ,'abbr., law, ADR':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., jur.,SAC'
                   ,'title': 'Abreviatura, Solución alternativa de controversias'
                   }
               ,'uk':
                   {'short': 'абрев., юр., АВС'
                   ,'title': 'Абревіатура, Альтернативне врегулювання спорів'
                   }
               }
           ,'abbr., law, copyr.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., law, copyr.'
                   ,'title': 'Abreviatura, Copyright'
                   }
               ,'uk':
                   {'short': 'абрев., юр., автор.'
                   ,'title': 'Абревіатура, Авторське право'
                   }
               }
           ,'abbr., mil., WMD':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., mil., WMD'
                   ,'title': 'Abreviatura, Weapons of mass destruction'
                   }
               ,'uk':
                   {'short': 'абрев., військ., ЗМУ'
                   ,'title': 'Абревіатура, Зброя масового ураження'
                   }
               }
           ,'abbr., mil., artil.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., mil.,artill.'
                   ,'title': 'Abreviatura, Artillería'
                   }
               ,'uk':
                   {'short': 'абрев., військ., арт.'
                   ,'title': 'Абревіатура, Артилерія'
                   }
               }
           ,'abbr., mil., navy':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., mil., navy'
                   ,'title': 'Abreviatura, Navy'
                   }
               ,'uk':
                   {'short': 'абрев., військ., мор.'
                   ,'title': 'Абревіатура, Військово-морський флот'
                   }
               }
           ,'abbr., patents.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., patents.'
                   ,'title': 'Abreviatura, Patents'
                   }
               ,'uk':
                   {'short': 'абрев., юр., пат.'
                   ,'title': 'Абревіатура, Патенти'
                   }
               }
           ,'abbr., sport, bask.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'abrev., sport, bask.'
                   ,'title': 'Abreviatura, Basketball'
                   }
               ,'uk':
                   {'short': 'абрев., спорт, баск.'
                   ,'title': 'Абревіатура, Баскетбол'
                   }
               }
           ,'account.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'cont.'
                   ,'title': 'Contabilidad'
                   }
               ,'uk':
                   {'short': 'бухг.'
                   ,'title': 'Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'accum.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'accum.'
                   ,'title': 'Accumulators'
                   }
               ,'uk':
                   {'short': 'акум.'
                   ,'title': 'Акумулятори'
                   }
               }
           ,'acoust.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'acoust.'
                   ,'title': 'Acoustics'
                   }
               ,'uk':
                   {'short': 'акуст.'
                   ,'title': 'Акустика'
                   }
               }
           ,'acrid.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'acrid.'
                   ,'title': 'Acridology'
                   }
               ,'uk':
                   {'short': 'акрід.'
                   ,'title': 'Акрідологія'
                   }
               }
           ,'acrob.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'acrob.'
                   ,'title': 'Acrobatics'
                   }
               ,'uk':
                   {'short': 'акроб.'
                   ,'title': 'Акробатика'
                   }
               }
           ,'acup.':
               {'valid': True
               ,'major': False
               ,'group': 'Medicine - Alternative medicine'
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
               ,'sp':
                   {'short': 'acup.'
                   ,'title': 'Acupuncture'
                   }
               ,'uk':
                   {'short': 'акуп.'
                   ,'title': 'Акупунктура'
                   }
               }
           ,'addit.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'addit.'
                   ,'title': 'Additive manufacturing & 3D printing'
                   }
               ,'uk':
                   {'short': 'адит.тех.'
                   ,'title': 'Адитивні технології та 3D-друк'
                   }
               }
           ,'adm.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'adm.law.'
                   ,'title': 'Administrative law'
                   }
               ,'uk':
                   {'short': 'адмін.пр.'
                   ,'title': 'Адміністративне право'
                   }
               }
           ,'admin.geo.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'admin.geo.'
                   ,'title': 'Administrative geography'
                   }
               ,'uk':
                   {'short': 'адм.под.'
                   ,'title': 'Адміністративний поділ'
                   }
               }
           ,'adv.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'adv.'
                   ,'title': 'Advertising'
                   }
               ,'uk':
                   {'short': 'рекл.'
                   ,'title': 'Реклама'
                   }
               }
           ,'aer.phot.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'aer.phot.'
                   ,'title': 'Aerial photography and topography'
                   }
               ,'uk':
                   {'short': 'аерофот.'
                   ,'title': 'Аерофозйомка та топографія'
                   }
               }
           ,'aerodyn.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'aerodyn.'
                   ,'title': 'Aerodynamics'
                   }
               ,'uk':
                   {'short': 'аеродин.'
                   ,'title': 'Аеродинаміка'
                   }
               }
           ,'aerohydr.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'aerohydr.'
                   ,'title': 'Aerohydrodynamics'
                   }
               ,'uk':
                   {'short': 'аерогідр.'
                   ,'title': 'Аерогідродинаміка'
                   }
               }
           ,'aeron.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'aeron.'
                   ,'title': 'Aeronautics'
                   }
               ,'uk':
                   {'short': 'повітр.'
                   ,'title': 'Повітроплавання'
                   }
               }
           ,'affect.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'affect.'
                   ,'title': 'Affectionate'
                   }
               ,'uk':
                   {'short': 'пестл.'
                   ,'title': 'Пестливо'
                   }
               }
           ,'afghan.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'afghan.'
                   ,'title': 'Afghanistan'
                   }
               ,'uk':
                   {'short': 'афган.'
                   ,'title': 'Афганістан'
                   }
               }
           ,'afr.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'afr.'
                   ,'title': 'Africa'
                   }
               ,'uk':
                   {'short': 'афр.'
                   ,'title': 'Африка'
                   }
               }
           ,'african.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'african.'
                   ,'title': 'African'
                   }
               ,'uk':
                   {'short': 'афр.вир.'
                   ,'title': 'Африканський вираз'
                   }
               }
           ,'agr.':
               {'valid': False
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'agr.'
                   ,'title': 'Agronomy'
                   }
               ,'uk':
                   {'short': 'агрон.'
                   ,'title': 'Агрономія'
                   }
               }
           ,'agric.':
               {'valid': True
               ,'major': True
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'agric.'
                   ,'title': 'Agricultura'
                   }
               ,'uk':
                   {'short': 'с/г.'
                   ,'title': 'Сільське господарство'
                   }
               }
           ,'agrochem.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'agrochem.'
                   ,'title': 'Agrochemistry'
                   }
               ,'uk':
                   {'short': 'агрохім.'
                   ,'title': 'Агрохімія'
                   }
               }
           ,'aikido.':
               {'valid': True
               ,'major': False
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'aikido.'
                   ,'title': 'Aikido'
                   }
               ,'uk':
                   {'short': 'айкідо.'
                   ,'title': 'Айкідо'
                   }
               }
           ,'airccon.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'airccon.'
                   ,'title': 'Air conditioners'
                   }
               ,'uk':
                   {'short': 'кондиц.'
                   ,'title': 'Кондиціонери'
                   }
               }
           ,'airports':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'airports'
                   ,'title': 'Airports and air traffic control'
                   }
               ,'uk':
                   {'short': 'аероп.'
                   ,'title': 'Аеропорти та керування повітряним рухом'
                   }
               }
           ,'airsh.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'airsh.'
                   ,'title': 'Airships'
                   }
               ,'uk':
                   {'short': 'држбл'
                   ,'title': 'Дирижаблі'
                   }
               }
           ,'alg.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'alg.'
                   ,'title': 'Algebra'
                   }
               ,'uk':
                   {'short': 'алг.'
                   ,'title': 'Алгебра'
                   }
               }
           ,'alk.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'alk.'
                   ,'title': 'Alkaloids'
                   }
               ,'uk':
                   {'short': 'алкал.'
                   ,'title': 'Алкалоїди'
                   }
               }
           ,'allergol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'alergol.'
                   ,'title': 'Alergología'
                   }
               ,'uk':
                   {'short': 'алерг.'
                   ,'title': 'Алергологія'
                   }
               }
           ,'alp.ski.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'alp.ski.'
                   ,'title': 'Alpine skiing'
                   }
               ,'uk':
                   {'short': 'гір.лиж.'
                   ,'title': 'Гірські лижі'
                   }
               }
           ,'alum.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'alum.'
                   ,'title': 'Aluminium industry'
                   }
               ,'uk':
                   {'short': 'алюм.'
                   ,'title': 'Алюмінієва промисловість'
                   }
               }
           ,'amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'amer.'
                   ,'title': 'Americano (uso)'
                   }
               ,'uk':
                   {'short': 'амер.вир.'
                   ,'title': 'Американський вираз (не варыант мови)'
                   }
               }
           ,'amer.usg., Makarov.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'amer., Makarov.'
                   ,'title': 'Americano (uso), Makarov'
                   }
               ,'uk':
                   {'short': 'амер.вир., Макаров'
                   ,'title': 'Американський вираз (не варыант мови), Макаров'
                   }
               }
           ,'amer.usg., account.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'amer., cont.'
                   ,'title': 'Americano (uso), Contabilidad'
                   }
               ,'uk':
                   {'short': 'амер.вир., бухг.'
                   ,'title': 'Американський вираз (не варыант мови), Бухгалтерський облік (крім аудиту)'
                   }
               }
           ,'anaesthes.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'anestes.'
                   ,'title': 'Anestesiología'
                   }
               ,'uk':
                   {'short': 'анест.'
                   ,'title': 'Анестезіологія'
                   }
               }
           ,'anat.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'anat.'
                   ,'title': 'Anatomía'
                   }
               ,'uk':
                   {'short': 'анат.'
                   ,'title': 'Анатомія'
                   }
               }
           ,'anc.fr.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'anc.fr.'
                   ,'title': 'Ancient French'
                   }
               ,'uk':
                   {'short': 'старофр.'
                   ,'title': 'Старофранцузька мова'
                   }
               }
           ,'anc.gr.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'gr.ant.'
                   ,'title': 'Griego antiguo'
                   }
               ,'uk':
                   {'short': 'давн.грец.'
                   ,'title': 'Давньогрецька мова'
                   }
               }
           ,'anc.hebr.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'anc.hebr.'
                   ,'title': 'Ancient Hebrew'
                   }
               ,'uk':
                   {'short': 'давн.євр.'
                   ,'title': 'Давньоєврейська мова'
                   }
               }
           ,'angl.':
               {'valid': True
               ,'major': False
               ,'group': 'Hobbies and pastimes'
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
               ,'sp':
                   {'short': 'angl.'
                   ,'title': 'Angling (hobby)'
                   }
               ,'uk':
                   {'short': 'рибол.'
                   ,'title': 'Риболовля (хобі)'
                   }
               }
           ,'anim.husb.':
               {'valid': False
               ,'major': False
               ,'group': 'Agriculture'
               ,'en':
                   {'short': 'anim.husb.'
                   ,'title': 'Animal husbandry'
                   }
               ,'ru':
                   {'short': 'с/х., животн.'
                   ,'title': 'Животноводство'
                   }
               ,'de':
                   {'short': 'anim.husb.'
                   ,'title': 'Animal husbandry'
                   }
               ,'sp':
                   {'short': 'anim.husb.'
                   ,'title': 'Animal husbandry'
                   }
               ,'uk':
                   {'short': 'тварин.'
                   ,'title': 'Тваринництво'
                   }
               }
           ,'animat.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'animat.'
                   ,'title': 'Animation and animated films'
                   }
               ,'uk':
                   {'short': 'мульт.'
                   ,'title': 'Мультфільми та мультиплікація'
                   }
               }
           ,'antarct.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'antarct.'
                   ,'title': 'Antarctic'
                   }
               ,'uk':
                   {'short': 'антаркт.'
                   ,'title': 'Антарктика'
                   }
               }
           ,'antenn.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'antenn.'
                   ,'title': 'Antennas and waveguides'
                   }
               ,'uk':
                   {'short': 'антен.'
                   ,'title': 'Антени і хвилеводи'
                   }
               }
           ,'anthr.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'anthr.'
                   ,'title': 'Anthropology'
                   }
               ,'uk':
                   {'short': 'антроп.'
                   ,'title': 'Антропологія'
                   }
               }
           ,'antitrust.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'antitrust.'
                   ,'title': 'Antitrust law'
                   }
               ,'uk':
                   {'short': 'антимон.'
                   ,'title': 'Антимонопольне законодавство'
                   }
               }
           ,'appl.math.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'appl.math.'
                   ,'title': 'Applied mathematics'
                   }
               ,'uk':
                   {'short': 'прикл.мат.'
                   ,'title': 'Прикладна математика'
                   }
               }
           ,'arabic':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'árab.'
                   ,'title': 'Árabe'
                   }
               ,'uk':
                   {'short': 'араб.'
                   ,'title': 'Арабська мова'
                   }
               }
           ,'arch.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'arch.'
                   ,'title': 'Archaic'
                   }
               ,'uk':
                   {'short': 'арх.'
                   ,'title': 'Архаїзм'
                   }
               }
           ,'archer.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'archer.'
                   ,'title': 'Archery'
                   }
               ,'uk':
                   {'short': 'стр.лук.'
                   ,'title': 'Стрільба з лука'
                   }
               }
           ,'archit.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'arquit.'
                   ,'title': 'Arquitectura'
                   }
               ,'uk':
                   {'short': 'архіт.'
                   ,'title': 'Архітектура'
                   }
               }
           ,'archive.':
               {'valid': True
               ,'major': False
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'archive.'
                   ,'title': 'Archiving'
                   }
               ,'uk':
                   {'short': 'архів.'
                   ,'title': 'Архівна справа'
                   }
               }
           ,'arts.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'arte'
                   ,'title': 'Arte'
                   }
               ,'uk':
                   {'short': 'мист.'
                   ,'title': 'Мистецтво'
                   }
               }
           ,'astr.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'astr.'
                   ,'title': 'Astronomía'
                   }
               ,'uk':
                   {'short': 'астр.'
                   ,'title': 'Астрономія'
                   }
               }
           ,'astrol.':
               {'valid': True
               ,'major': False
               ,'group': 'Parasciences'
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
               ,'sp':
                   {'short': 'astrol.'
                   ,'title': 'Astrology'
                   }
               ,'uk':
                   {'short': 'астрол.'
                   ,'title': 'Астрологія'
                   }
               }
           ,'astrometr.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'astrometr.'
                   ,'title': 'Astrometry'
                   }
               ,'uk':
                   {'short': 'астром.'
                   ,'title': 'Астрометрія'
                   }
               }
           ,'astronaut.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'astronaut.'
                   ,'title': 'Astronautics'
                   }
               ,'uk':
                   {'short': 'космон.'
                   ,'title': 'Космонавтика'
                   }
               }
           ,'astrophys.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'astrophys.'
                   ,'title': 'Astrophysics'
                   }
               ,'uk':
                   {'short': 'астрофіз.'
                   ,'title': 'Астрофізика'
                   }
               }
           ,'astrospectr.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'astrospectr.'
                   ,'title': 'Astrospectroscopy'
                   }
               ,'uk':
                   {'short': 'астроспек.'
                   ,'title': 'Астроспектроскопія'
                   }
               }
           ,'athlet.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'athlet.'
                   ,'title': 'Athletics'
                   }
               ,'uk':
                   {'short': 'л.атл.'
                   ,'title': 'Легка атлетика'
                   }
               }
           ,'atring.':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'atring.'
                   ,'title': 'Astringents'
                   }
               ,'uk':
                   {'short': 'в’яж.реч.'
                   ,'title': 'В’яжучі речовини'
                   }
               }
           ,'audio.el.':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'audio.el.'
                   ,'title': 'Audio electronics'
                   }
               ,'uk':
                   {'short': 'аудіотех.'
                   ,'title': 'Аудіотехніка'
                   }
               }
           ,'austral.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'austral.'
                   ,'title': 'Australiano (sólo uso)'
                   }
               ,'uk':
                   {'short': 'австрал.'
                   ,'title': 'Австралійський вираз'
                   }
               }
           ,'austrian':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'austrian'
                   ,'title': 'Austrian (usage)'
                   }
               ,'uk':
                   {'short': 'австрійськ.'
                   ,'title': 'Австрійський вираз'
                   }
               }
           ,'auto.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'automóv.'
                   ,'title': 'Automóviles'
                   }
               ,'uk':
                   {'short': 'авто.'
                   ,'title': 'Автомобілі'
                   }
               }
           ,'auto.ctrl.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'auto.ctrl.'
                   ,'title': 'Automatic control'
                   }
               ,'uk':
                   {'short': 'автом.рег.'
                   ,'title': 'Автоматичне регулювання'
                   }
               }
           ,'automat.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'automat.'
                   ,'title': 'Automated equipment'
                   }
               ,'uk':
                   {'short': 'автомат.'
                   ,'title': 'Автоматика'
                   }
               }
           ,'avia.':
               {'valid': True
               ,'major': True
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'avia.'
                   ,'title': 'Aviación'
                   }
               ,'uk':
                   {'short': 'авіац.'
                   ,'title': 'Авіація'
                   }
               }
           ,'avia., avia., ICAO':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'avia., avia., ICAO'
                   ,'title': 'Aviación, ICAO'
                   }
               ,'uk':
                   {'short': 'авіац., авіац., ІКАО'
                   ,'title': 'Авіація, ІКАО'
                   }
               }
           ,'avia., med.':
               {'valid': False
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'avia., med.'
                   ,'title': 'Aviation medicine'
                   }
               ,'uk':
                   {'short': 'авіац., мед.'
                   ,'title': 'Авіаційна медицина'
                   }
               }
           ,'avunc.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'avunc.'
                   ,'title': 'Avuncular'
                   }
               ,'uk':
                   {'short': 'фам.'
                   ,'title': 'Фамільярний вираз'
                   }
               }
           ,'bacteriol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'bact.'
                   ,'title': 'Bacteriología'
                   }
               ,'uk':
                   {'short': 'бакт.'
                   ,'title': 'Бактеріологія'
                   }
               }
           ,'baker.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'baker.'
                   ,'title': 'Bakery'
                   }
               ,'uk':
                   {'short': 'хліб.'
                   ,'title': 'Хліб та хлібопечення'
                   }
               }
           ,'ball.bear.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'ball.bear.'
                   ,'title': 'Ball bearings'
                   }
               ,'uk':
                   {'short': 'кульк.підш.'
                   ,'title': 'Кулькові підшипники'
                   }
               }
           ,'ballet.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'ballet.'
                   ,'title': 'Ballet'
                   }
               ,'uk':
                   {'short': 'балет'
                   ,'title': 'Балет'
                   }
               }
           ,'bank.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'bank.'
                   ,'title': 'Banking'
                   }
               ,'uk':
                   {'short': 'банк.'
                   ,'title': 'Банки та банківська справа'
                   }
               }
           ,'baseb.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'baseb.'
                   ,'title': 'Baseball'
                   }
               ,'uk':
                   {'short': 'бейсб.'
                   ,'title': 'Бейсбол'
                   }
               }
           ,'beekeep.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'beekeep.'
                   ,'title': 'Beekeeping'
                   }
               ,'uk':
                   {'short': 'бджіл.'
                   ,'title': 'Бджільництво'
                   }
               }
           ,'belg.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'belg.'
                   ,'title': 'Belgian (usage)'
                   }
               ,'uk':
                   {'short': 'бельг.вир.'
                   ,'title': 'Бельгійський вираз'
                   }
               }
           ,'bev.':
               {'valid': True
               ,'major': False
               ,'group': 'Cooking'
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
               ,'sp':
                   {'short': 'bev.'
                   ,'title': 'Beverages'
                   }
               ,'uk':
                   {'short': 'напої.'
                   ,'title': 'Напої'
                   }
               }
           ,'bible.term.':
               {'valid': True
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'bibl.'
                   ,'title': 'Biblia'
                   }
               ,'uk':
                   {'short': 'бібл.'
                   ,'title': 'Біблія'
                   }
               }
           ,'bibliogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'bibliogr.'
                   ,'title': 'Bibliography'
                   }
               ,'uk':
                   {'short': 'бібліогр.'
                   ,'title': 'Бібліографія'
                   }
               }
           ,'bill.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'bill.'
                   ,'title': 'Bills'
                   }
               ,'uk':
                   {'short': 'векс.'
                   ,'title': 'Вексельне право'
                   }
               }
           ,'billiar.':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'billiar.'
                   ,'title': 'Billiards'
                   }
               ,'uk':
                   {'short': 'більярд'
                   ,'title': 'Більярд'
                   }
               }
           ,'bioacoust.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'bioacoust.'
                   ,'title': 'Bioacoustics'
                   }
               ,'uk':
                   {'short': 'біоакуст.'
                   ,'title': 'Біоакустика'
                   }
               }
           ,'biochem.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'bioq.'
                   ,'title': 'Bioquímica'
                   }
               ,'uk':
                   {'short': 'біохім.'
                   ,'title': 'Біохімія'
                   }
               }
           ,'bioenerg.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'bioenerg.'
                   ,'title': 'Bioenergy'
                   }
               ,'uk':
                   {'short': 'біоенерг.'
                   ,'title': 'Біоенергетика'
                   }
               }
           ,'biol.':
               {'valid': True
               ,'major': True
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'biol.'
                   ,'title': 'Biología'
                   }
               ,'uk':
                   {'short': 'біол.'
                   ,'title': 'Біологія'
                   }
               }
           ,'biom.':
               {'valid': True
               ,'major': False
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'biom.'
                   ,'title': 'Biometry'
                   }
               ,'uk':
                   {'short': 'біом.'
                   ,'title': 'Біометрія'
                   }
               }
           ,'bion.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'bion.'
                   ,'title': 'Bionics'
                   }
               ,'uk':
                   {'short': 'біон.'
                   ,'title': 'Біоніка'
                   }
               }
           ,'biophys.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'biofís.'
                   ,'title': 'Biofísica'
                   }
               ,'uk':
                   {'short': 'біофіз.'
                   ,'title': 'Біофізика'
                   }
               }
           ,'biotaxy.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'biotaxy.'
                   ,'title': 'Biotaxy'
                   }
               ,'uk':
                   {'short': 'сист.орг.'
                   ,'title': 'Систематика організмів'
                   }
               }
           ,'biotechn.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'biotechn.'
                   ,'title': 'Biotechnology'
                   }
               ,'uk':
                   {'short': 'біот.'
                   ,'title': 'Біотехнологія'
                   }
               }
           ,'black.sl.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'black.sl.'
                   ,'title': 'Black slang'
                   }
               ,'uk':
                   {'short': 'негр.'
                   ,'title': 'Негритянський жаргон'
                   }
               }
           ,'bodybuild.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'bodybuild.'
                   ,'title': 'Bodybuilding'
                   }
               ,'uk':
                   {'short': 'бодібілд.'
                   ,'title': 'Бодібілдинг'
                   }
               }
           ,'book.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'lib.'
                   ,'title': 'Libresco/literario'
                   }
               ,'uk':
                   {'short': 'книжн.'
                   ,'title': 'Книжний / літературний вираз'
                   }
               }
           ,'book.bind.':
               {'valid': True
               ,'major': False
               ,'group': 'Publishing'
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
               ,'sp':
                   {'short': 'book.bind.'
                   ,'title': 'Book binding'
                   }
               ,'uk':
                   {'short': 'палітурн.'
                   ,'title': 'Палітурна справа'
                   }
               }
           ,'bot.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'bot.'
                   ,'title': 'Botánica'
                   }
               ,'uk':
                   {'short': 'бот.'
                   ,'title': 'Ботаніка'
                   }
               }
           ,'box.':
               {'valid': True
               ,'major': False
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'box.'
                   ,'title': 'Boxing'
                   }
               ,'uk':
                   {'short': 'бокс'
                   ,'title': 'Бокс'
                   }
               }
           ,'brew.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'brew.'
                   ,'title': 'Brewery'
                   }
               ,'uk':
                   {'short': 'пив.'
                   ,'title': 'Пивоваріння'
                   }
               }
           ,'bricks':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'bricks'
                   ,'title': 'Bricks'
                   }
               ,'uk':
                   {'short': 'цегл.'
                   ,'title': 'Цегла'
                   }
               }
           ,'bridg.constr.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'bridg.constr.'
                   ,'title': 'Bridge construction'
                   }
               ,'uk':
                   {'short': 'мост.'
                   ,'title': 'Мостобудування'
                   }
               }
           ,'brit.usg.':
               {'valid': False
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'brit.usg.'
                   ,'title': 'British (usage, not BrE)'
                   }
               ,'uk':
                   {'short': 'брит.вир.'
                   ,'title': 'Британський вираз (не варіант мови)'
                   }
               }
           ,'brit.usg., austral.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'brit.usg., austral.'
                   ,'title': 'British (usage, not BrE), Australiano (sólo uso)'
                   }
               ,'uk':
                   {'short': 'брит.вир., австрал.'
                   ,'title': 'Британський вираз (не варіант мови), Австралійський вираз'
                   }
               }
           ,'build.mat.':
               {'valid': True
               ,'major': True
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'build.mat.'
                   ,'title': 'Building materials'
                   }
               ,'uk':
                   {'short': 'буд.мат.'
                   ,'title': 'Будівельні матеріали'
                   }
               }
           ,'build.struct.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'build.struct.'
                   ,'title': 'Building structures'
                   }
               ,'uk':
                   {'short': 'буд.констр.'
                   ,'title': 'Будівельні конструкції'
                   }
               }
           ,'bus.styl.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'bus.styl.'
                   ,'title': 'Business style'
                   }
               ,'uk':
                   {'short': 'ділов.'
                   ,'title': 'Ділова лексика'
                   }
               }
           ,'busin.':
               {'valid': True
               ,'major': True
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'busin.'
                   ,'title': 'Business'
                   }
               ,'uk':
                   {'short': 'бізн.'
                   ,'title': 'Бізнес'
                   }
               }
           ,'cables':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'cables'
                   ,'title': 'Cables and cable production'
                   }
               ,'uk':
                   {'short': 'каб.'
                   ,'title': 'Кабелі та кабельне виробництво'
                   }
               }
           ,'calligr.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'calligr.'
                   ,'title': 'Calligraphy'
                   }
               ,'uk':
                   {'short': 'калігр.'
                   ,'title': 'Каліграфія'
                   }
               }
           ,'can.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'can.'
                   ,'title': 'Canning'
                   }
               ,'uk':
                   {'short': 'конс.'
                   ,'title': 'Консервування'
                   }
               }
           ,'canad.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'canad.'
                   ,'title': 'Canadian'
                   }
               ,'uk':
                   {'short': 'канад.'
                   ,'title': 'Канадський вираз'
                   }
               }
           ,'carcin.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'carcin.'
                   ,'title': 'Carcinology'
                   }
               ,'uk':
                   {'short': 'карц.'
                   ,'title': 'Карцинологія'
                   }
               }
           ,'cardiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'cardiol.'
                   ,'title': 'Cardiología'
                   }
               ,'uk':
                   {'short': 'кард.'
                   ,'title': 'Кардіологія'
                   }
               }
           ,'cards':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'cart.'
                   ,'title': 'Juego de cartas'
                   }
               ,'uk':
                   {'short': 'карти'
                   ,'title': 'Картярські ігри'
                   }
               }
           ,'cartogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'cartogr.'
                   ,'title': 'Cartography'
                   }
               ,'uk':
                   {'short': 'картогр.'
                   ,'title': 'Картографія'
                   }
               }
           ,'cartogr., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'cartogr., amer.'
                   ,'title': 'Cartography, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'картогр., амер.вир.'
                   ,'title': 'Картографія, Американський вираз (не варыант мови)'
                   }
               }
           ,'cel.mech.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'cel.mech.'
                   ,'title': 'Celestial mechanics'
                   }
               ,'uk':
                   {'short': 'неб.мех.'
                   ,'title': 'Небесна механіка'
                   }
               }
           ,'cem.':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'cem.'
                   ,'title': 'Cement'
                   }
               ,'uk':
                   {'short': 'цем.'
                   ,'title': 'Цемент'
                   }
               }
           ,'ceram.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'ceram.'
                   ,'title': 'Ceramics'
                   }
               ,'uk':
                   {'short': 'керам.'
                   ,'title': 'Кераміка'
                   }
               }
           ,'ceram.tile.':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'ceram.tile.'
                   ,'title': 'Ceramic tiles'
                   }
               ,'uk':
                   {'short': 'керам.пл.'
                   ,'title': 'Керамічна плитка'
                   }
               }
           ,'chalcid.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'chalcid.'
                   ,'title': 'Chalcidology'
                   }
               ,'uk':
                   {'short': 'халькід.'
                   ,'title': 'Халькідологія'
                   }
               }
           ,'charit.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'charit.'
                   ,'title': 'Charities'
                   }
               ,'uk':
                   {'short': 'благод.'
                   ,'title': 'Благодійні організації'
                   }
               }
           ,'chat.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'chat.'
                   ,'title': 'Chat and Internet slang'
                   }
               ,'uk':
                   {'short': 'чат.'
                   ,'title': 'Чати та інтернет-жаргон'
                   }
               }
           ,'chech.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'chech.'
                   ,'title': 'Czech'
                   }
               ,'uk':
                   {'short': 'чеськ.'
                   ,'title': 'Чеська мова'
                   }
               }
           ,'checkers.':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'checkers.'
                   ,'title': 'Checkers'
                   }
               ,'uk':
                   {'short': 'шашк.'
                   ,'title': 'Шашки'
                   }
               }
           ,'cheese':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'cheese'
                   ,'title': 'Cheesemaking (caseiculture)'
                   }
               ,'uk':
                   {'short': 'сир.'
                   ,'title': 'Сироваріння'
                   }
               }
           ,'chem.':
               {'valid': True
               ,'major': True
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'quím.'
                   ,'title': 'Química'
                   }
               ,'uk':
                   {'short': 'хім.'
                   ,'title': 'Хімія'
                   }
               }
           ,'chem.comp.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'chem.comp.'
                   ,'title': 'Chemical compounds'
                   }
               ,'uk':
                   {'short': 'хім.спол.'
                   ,'title': 'Хімічні сполуки'
                   }
               }
           ,'chem.fib.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'chem.fib.'
                   ,'title': 'Chemical fibers'
                   }
               ,'uk':
                   {'short': 'хім.волок.'
                   ,'title': 'Хімічні волокна'
                   }
               }
           ,'chem.ind.':
               {'valid': True
               ,'major': True
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'chem.ind.'
                   ,'title': 'Chemical industry'
                   }
               ,'uk':
                   {'short': 'хім.пром.'
                   ,'title': 'Хімічна промисловість'
                   }
               }
           ,'chem.nomencl.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'chem.nomencl.'
                   ,'title': 'Chemical nomenclature'
                   }
               ,'uk':
                   {'short': 'хім.номенкл.'
                   ,'title': 'Хімічна номенклатура'
                   }
               }
           ,'chess.term.':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'ajedr.'
                   ,'title': 'Ajedrez'
                   }
               ,'uk':
                   {'short': 'шах.'
                   ,'title': 'Шахи'
                   }
               }
           ,'child.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'infant.'
                   ,'title': 'Infantil'
                   }
               ,'uk':
                   {'short': 'дит.'
                   ,'title': 'Дитяче мовлення'
                   }
               }
           ,'chinese.lang.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'chin.'
                   ,'title': 'Chino'
                   }
               ,'uk':
                   {'short': 'кит.'
                   ,'title': 'Китайська мова'
                   }
               }
           ,'choreogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'choreogr.'
                   ,'title': 'Choreography'
                   }
               ,'uk':
                   {'short': 'хореогр.'
                   ,'title': 'Хореографія'
                   }
               }
           ,'chromat.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'chromat.'
                   ,'title': 'Chromatography'
                   }
               ,'uk':
                   {'short': 'хроматогр.'
                   ,'title': 'Хроматографія'
                   }
               }
           ,'cinema':
               {'valid': True
               ,'major': True
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'cine'
                   ,'title': 'Cinematógrafo'
                   }
               ,'uk':
                   {'short': 'кіно'
                   ,'title': 'Кінематограф'
                   }
               }
           ,'cinema.equip.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'cinema.equip.'
                   ,'title': 'Cinema equipment'
                   }
               ,'uk':
                   {'short': 'кінотех.'
                   ,'title': 'Кінотехніка'
                   }
               }
           ,'circus':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'circus'
                   ,'title': 'Circus'
                   }
               ,'uk':
                   {'short': 'цирк'
                   ,'title': 'Цирк'
                   }
               }
           ,'civ.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'civ.law.'
                   ,'title': 'Civil law'
                   }
               ,'uk':
                   {'short': 'цив.пр.'
                   ,'title': 'Цивільне право'
                   }
               }
           ,'civ.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'civ.proc.'
                   ,'title': 'Civil procedure'
                   }
               ,'uk':
                   {'short': 'цив.проц.пр.'
                   ,'title': 'Цивільно-процесуальне право'
                   }
               }
           ,'clas.ant.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'antig.'
                   ,'title': 'Antigüedad (sin mitología)'
                   }
               ,'uk':
                   {'short': 'антич.'
                   ,'title': 'Античність'
                   }
               }
           ,'cleric.':
               {'valid': True
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'ecles.'
                   ,'title': 'Eclesiástico'
                   }
               ,'uk':
                   {'short': 'церк.'
                   ,'title': 'Церковний термін'
                   }
               }
           ,'clich.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'clich.'
                   ,'title': 'Cliche'
                   }
               ,'uk':
                   {'short': 'кліше'
                   ,'title': 'Кліше'
                   }
               }
           ,'clim.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'clim.'
                   ,'title': 'Climatology'
                   }
               ,'uk':
                   {'short': 'клім.'
                   ,'title': 'Кліматологія'
                   }
               }
           ,'clin.trial.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'clin.trial.'
                   ,'title': 'Clinical trial'
                   }
               ,'uk':
                   {'short': 'клін.досл.'
                   ,'title': 'Клінічні дослідження'
                   }
               }
           ,'cloth.':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'coal.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'coal.'
                   ,'title': 'Coal'
                   }
               ,'uk':
                   {'short': 'вуг.'
                   ,'title': 'Вугілля'
                   }
               }
           ,'cockney':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'cockney'
                   ,'title': 'Cockney rhyming slang'
                   }
               ,'uk':
                   {'short': 'кокні'
                   ,'title': 'Кокні (римований сленг)'
                   }
               }
           ,'coff.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'coff.'
                   ,'title': 'Coffee'
                   }
               ,'uk':
                   {'short': 'кава'
                   ,'title': 'Кава'
                   }
               }
           ,'coll.':
               {'valid': True
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'colect.'
                   ,'title': 'Colectivo'
                   }
               ,'uk':
                   {'short': 'збірн.'
                   ,'title': 'Збірне поняття'
                   }
               }
           ,'collect.':
               {'valid': True
               ,'major': True
               ,'group': 'Collecting'
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
               ,'sp':
                   {'short': 'collect.'
                   ,'title': 'Collecting'
                   }
               ,'uk':
                   {'short': 'колекц.'
                   ,'title': 'Колекціонування'
                   }
               }
           ,'college.vern.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'college.vern.'
                   ,'title': 'College vernacular'
                   }
               ,'uk':
                   {'short': 'студ.сл.'
                   ,'title': 'Студентський сленг'
                   }
               }
           ,'colloid.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'colloid.chem.'
                   ,'title': 'Colloid chemistry'
                   }
               ,'uk':
                   {'short': 'колоїд.'
                   ,'title': 'Колоїдна хімія'
                   }
               }
           ,'combust.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'combust.'
                   ,'title': 'Combustion gas turbines'
                   }
               ,'uk':
                   {'short': 'газ.турб.'
                   ,'title': 'Газові турбіни'
                   }
               }
           ,'comic.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'comic.'
                   ,'title': 'Comics'
                   }
               ,'uk':
                   {'short': 'комікси'
                   ,'title': 'Комікси'
                   }
               }
           ,'commer.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'com.'
                   ,'title': 'Comercio'
                   }
               ,'uk':
                   {'short': 'торг.'
                   ,'title': 'Торгівля'
                   }
               }
           ,'commun.':
               {'valid': True
               ,'major': True
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'commun.'
                   ,'title': 'Communications'
                   }
               ,'uk':
                   {'short': 'зв’яз.'
                   ,'title': 'Зв’язок'
                   }
               }
           ,'comp.':
               {'valid': True
               ,'major': True
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp.'
                   ,'title': 'Computadores'
                   }
               ,'uk':
                   {'short': 'комп.'
                   ,'title': "Комп'ютери"}}, 'comp., MS':
               {'valid': False
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp., MS'
                   ,'title': 'Microsoft'
                   }
               ,'uk':
                   {'short': 'комп., Майкр.'
                   ,'title': 'Майкрософт'
                   }
               }
           ,'comp., net.':
               {'valid': False
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp., net.'
                   ,'title': 'Computer networks'
                   }
               ,'uk':
                   {'short': 'комп., мереж.'
                   ,'title': "Комп'ютерні мережі"}}, 'comp., net., abbr.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'comp., net., abrev.'
                   ,'title': 'Computer networks, Abreviatura'
                   }
               ,'uk':
                   {'short': 'комп., мереж., абрев.'
                   ,'title': "Комп'ютерні мережі, Абревіатура"}}, 'comp.games.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp.games.'
                   ,'title': 'Computer games'
                   }
               ,'uk':
                   {'short': 'комп.ігри'
                   ,'title': 'Комп’ютерні ігри'
                   }
               }
           ,'comp.graph.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp.graph.'
                   ,'title': 'Computer graphics'
                   }
               ,'uk':
                   {'short': 'комп.граф.'
                   ,'title': 'Комп’ютерна графіка'
                   }
               }
           ,'comp.name.':
               {'valid': True
               ,'major': False
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'comp.name.'
                   ,'title': 'Company name'
                   }
               ,'uk':
                   {'short': 'назв.комп.'
                   ,'title': 'Назва компанії'
                   }
               }
           ,'comp.sec.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'comp.sec.'
                   ,'title': 'Computer security'
                   }
               ,'uk':
                   {'short': 'комп.зах.'
                   ,'title': 'Комп’ютерний захист'
                   }
               }
           ,'comp.sl., humor.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'comp.sl., humor.'
                   ,'title': 'Computing slang, Humorístico'
                   }
               ,'uk':
                   {'short': 'комп.жар., жарт.'
                   ,'title': 'Комп’ютерний жаргон, Жартівливий вираз'
                   }
               }
           ,'compr.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               ,'uk':
                   {'short': 'compr.'
                   ,'title': 'Compressors'
                   }
               }
           ,'concr.':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'concr.'
                   ,'title': 'Concrete'
                   }
               ,'uk':
                   {'short': 'бетон.'
                   ,'title': 'Бетонне виробництво'
                   }
               }
           ,'confect.':
               {'valid': True
               ,'major': False
               ,'group': 'Cooking'
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
               ,'sp':
                   {'short': 'confect.'
                   ,'title': 'Confectionery'
                   }
               ,'uk':
                   {'short': 'солод.'
                   ,'title': 'Солодощі'
                   }
               }
           ,'construct.':
               {'valid': True
               ,'major': True
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'constr.'
                   ,'title': 'Construcción'
                   }
               ,'uk':
                   {'short': 'буд.'
                   ,'title': 'Будівництво'
                   }
               }
           ,'consult.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'consult.'
                   ,'title': 'Consulting'
                   }
               ,'uk':
                   {'short': 'консалт.'
                   ,'title': 'Консалтинг'
                   }
               }
           ,'contempt.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'despect.'
                   ,'title': 'Despectivamente'
                   }
               ,'uk':
                   {'short': 'презирл.'
                   ,'title': 'Презирливий вираз'
                   }
               }
           ,'context.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'context.'
                   ,'title': 'Contextual meaning'
                   }
               ,'uk':
                   {'short': 'конт.'
                   ,'title': 'Контекстуальне значення'
                   }
               }
           ,'conv.ind.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'conv.ind.'
                   ,'title': 'Converter industry'
                   }
               ,'uk':
                   {'short': 'конв.'
                   ,'title': 'Конвертерне виробництво'
                   }
               }
           ,'conv.notation.':
               {'valid': True
               ,'major': False
               ,'group': 'Subjects for Chinese dictionaries (container)'
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
               ,'sp':
                   {'short': 'conv.notation.'
                   ,'title': 'Conventional notation'
                   }
               ,'uk':
                   {'short': 'умов.'
                   ,'title': 'Умовне позначення'
                   }
               }
           ,'cook.':
               {'valid': True
               ,'major': True
               ,'group': 'Cooking'
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
               ,'sp':
                   {'short': 'cocina'
                   ,'title': 'Cocina'
                   }
               ,'uk':
                   {'short': 'кул.'
                   ,'title': 'Кулінарія'
                   }
               }
           ,'coop.':
               {'valid': True
               ,'major': False
               ,'group': 'Crafts'
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
               ,'sp':
                   {'short': 'coop.'
                   ,'title': 'Cooperage'
                   }
               ,'uk':
                   {'short': 'бонд.'
                   ,'title': 'Бондарство'
                   }
               }
           ,'corp.gov.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'corp.gov.'
                   ,'title': 'Corporate governance'
                   }
               ,'uk':
                   {'short': 'корп.упр.'
                   ,'title': 'Корпоративне управління'
                   }
               }
           ,'corrupt.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'corrupt.'
                   ,'title': 'Combating corruption'
                   }
               ,'uk':
                   {'short': 'корупц.'
                   ,'title': 'Боротьба з корупцією'
                   }
               }
           ,'cosmet.':
               {'valid': True
               ,'major': False
               ,'group': 'Wellness'
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
               ,'sp':
                   {'short': 'cosmet.'
                   ,'title': 'Cosmetics and cosmetology'
                   }
               ,'uk':
                   {'short': 'космет.'
                   ,'title': 'Косметика і косметологія'
                   }
               }
           ,'crim.jarg.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'crim.jarg.'
                   ,'title': 'Criminal jargon'
                   }
               ,'uk':
                   {'short': 'крим.жарг.'
                   ,'title': 'Кримінальний жаргон'
                   }
               }
           ,'crim.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'crim.law.'
                   ,'title': 'Criminal law'
                   }
               ,'uk':
                   {'short': 'крим.пр.'
                   ,'title': 'Кримінальне право'
                   }
               }
           ,'cryptogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'cryptogr.'
                   ,'title': 'Cryptography'
                   }
               ,'uk':
                   {'short': 'крипт.'
                   ,'title': 'Криптографія'
                   }
               }
           ,'crystall.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'crystall.'
                   ,'title': 'Crystallography'
                   }
               ,'uk':
                   {'short': 'крист.'
                   ,'title': 'Кристалографія'
                   }
               }
           ,'cultur.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'cultur.'
                   ,'title': 'Cultural studies'
                   }
               ,'uk':
                   {'short': 'культур.'
                   ,'title': 'Культурологія'
                   }
               }
           ,'curr.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'curr.'
                   ,'title': 'Currencies and monetary policy'
                   }
               ,'uk':
                   {'short': 'валют.'
                   ,'title': 'Валюти та монетарна політика (окрім форекс)'
                   }
               }
           ,'cust.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'cust.'
                   ,'title': 'Customs'
                   }
               ,'uk':
                   {'short': 'митн.'
                   ,'title': 'Митна справа'
                   }
               }
           ,'cyber.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'cyber.'
                   ,'title': 'Cybernetics'
                   }
               ,'uk':
                   {'short': 'кіб.'
                   ,'title': 'Кібернетика'
                   }
               }
           ,'cyc.sport':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'cyc.sport'
                   ,'title': 'Cycle sport'
                   }
               ,'uk':
                   {'short': 'вел.спорт'
                   ,'title': 'Велоспорт'
                   }
               }
           ,'cycl.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'cycl.'
                   ,'title': 'Cycling (other than sport)'
                   }
               ,'uk':
                   {'short': 'вело.'
                   ,'title': 'Велосипеди (крім спорту)'
                   }
               }
           ,'cytog.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'cytog.'
                   ,'title': 'Cytogenetics'
                   }
               ,'uk':
                   {'short': 'цитоген.'
                   ,'title': 'Цитогенетика'
                   }
               }
           ,'cytol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'citol.'
                   ,'title': 'Citología'
                   }
               ,'uk':
                   {'short': 'цитол.'
                   ,'title': 'Цитологія'
                   }
               }
           ,'d.b..':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'd.b..'
                   ,'title': 'Databases'
                   }
               ,'uk':
                   {'short': 'БД'
                   ,'title': 'Бази даних'
                   }
               }
           ,'dactyl.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'dactyl.'
                   ,'title': 'Dactyloscopy'
                   }
               ,'uk':
                   {'short': 'дактил.'
                   ,'title': 'Дактилоскопія'
                   }
               }
           ,'dam.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'dam.'
                   ,'title': 'Dams'
                   }
               ,'uk':
                   {'short': 'дамб.'
                   ,'title': 'Дамби'
                   }
               }
           ,'dan.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'dan.'
                   ,'title': 'Danish'
                   }
               ,'uk':
                   {'short': 'дан.'
                   ,'title': 'Данська мова'
                   }
               }
           ,'danc.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'danc.'
                   ,'title': 'Dancing'
                   }
               ,'uk':
                   {'short': 'танц.'
                   ,'title': 'Танці'
                   }
               }
           ,'dat.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'dat.proc.'
                   ,'title': 'Data processing'
                   }
               ,'uk':
                   {'short': 'обр.дан.'
                   ,'title': 'Обробка даних'
                   }
               }
           ,'deaf.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'deaf.'
                   ,'title': 'Deafblindness'
                   }
               ,'uk':
                   {'short': 'сліпоглух.'
                   ,'title': 'Сліпоглухота'
                   }
               }
           ,'demogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'demogr.'
                   ,'title': 'Demography'
                   }
               ,'uk':
                   {'short': 'демогр.'
                   ,'title': 'Демографія'
                   }
               }
           ,'dent.impl.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'dent.impl.'
                   ,'title': 'Dental implantology'
                   }
               ,'uk':
                   {'short': 'зуб.імп.'
                   ,'title': 'Зубна імплантологія'
                   }
               }
           ,'dentist.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'odont.'
                   ,'title': 'Odontología'
                   }
               ,'uk':
                   {'short': 'стом.'
                   ,'title': 'Стоматологія'
                   }
               }
           ,'derbet.':
               {'valid': True
               ,'major': False
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'derbet.'
                   ,'title': 'Derbet language'
                   }
               ,'uk':
                   {'short': 'дербет.'
                   ,'title': 'Дербетський діалект'
                   }
               }
           ,'dermat.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'dermat.'
                   ,'title': 'Dermatología'
                   }
               ,'uk':
                   {'short': 'дерм.'
                   ,'title': 'Дерматологія'
                   }
               }
           ,'derog.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'derog.'
                   ,'title': 'Derogatory'
                   }
               ,'uk':
                   {'short': 'зневаж.'
                   ,'title': 'Зневажливо'
                   }
               }
           ,'desert.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               ,'uk':
                   {'short': 'desert.'
                   ,'title': 'Desert science'
                   }
               }
           ,'design.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'design.'
                   ,'title': 'Design'
                   }
               ,'uk':
                   {'short': 'диз.'
                   ,'title': 'Дизайн'
                   }
               }
           ,'dial.':
               {'valid': True
               ,'major': True
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'dial.'
                   ,'title': 'Dialecto'
                   }
               ,'uk':
                   {'short': 'діал.'
                   ,'title': 'Діалектизм'
                   }
               }
           ,'dialys.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'dialys.'
                   ,'title': 'Dyalysis'
                   }
               ,'uk':
                   {'short': 'діаліз'
                   ,'title': 'Діаліз'
                   }
               }
           ,'diet.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'diet.'
                   ,'title': 'Dietology'
                   }
               ,'uk':
                   {'short': 'дієтол.'
                   ,'title': 'Дієтологія'
                   }
               }
           ,'dig.curr.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'dig.curr.'
                   ,'title': 'Digital and cryptocurrencies'
                   }
               ,'uk':
                   {'short': 'цифр.вал.'
                   ,'title': 'Цифрові та криптовалюти'
                   }
               }
           ,'dimin.':
               {'valid': True
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'dimin.'
                   ,'title': 'Diminutive'
                   }
               ,'uk':
                   {'short': 'зменш.'
                   ,'title': 'Зменшувально'
                   }
               }
           ,'dipl.':
               {'valid': True
               ,'major': False
               ,'group': 'Foreign affairs'
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
               ,'sp':
                   {'short': 'dipl.'
                   ,'title': 'Diplomacia'
                   }
               ,'uk':
                   {'short': 'дип.'
                   ,'title': 'Дипломатія'
                   }
               }
           ,'dipl., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'dipl., amer.'
                   ,'title': 'Diplomacia, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'дип., амер.вир.'
                   ,'title': 'Дипломатія, Американський вираз (не варыант мови)'
                   }
               }
           ,'disappr.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'desaprob.'
                   ,'title': 'Desaprobadoramente'
                   }
               ,'uk':
                   {'short': 'несхв.'
                   ,'title': 'Несхвально'
                   }
               }
           ,'disast.':
               {'valid': True
               ,'major': False
               ,'group': 'Politics'
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
               ,'sp':
                   {'short': 'disast.'
                   ,'title': 'Disaster recovery'
                   }
               ,'uk':
                   {'short': 'авар.'
                   ,'title': 'Аварійне відновлення'
                   }
               }
           ,'distil.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'distil.'
                   ,'title': 'Distillation'
                   }
               ,'uk':
                   {'short': 'дистил.'
                   ,'title': 'Дистиляція'
                   }
               }
           ,'dog.':
               {'valid': True
               ,'major': False
               ,'group': 'Companion animals'
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
               ,'sp':
                   {'short': 'dog.'
                   ,'title': 'Dog breeding'
                   }
               ,'uk':
                   {'short': 'собак.'
                   ,'title': 'Собаківництво'
                   }
               }
           ,'dominic.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'dominic.'
                   ,'title': 'Dominican Republic'
                   }
               ,'uk':
                   {'short': 'домінік.'
                   ,'title': 'Домініканська Республіка'
                   }
               }
           ,'dril.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'dril.'
                   ,'title': 'Drilling'
                   }
               ,'uk':
                   {'short': 'бур.'
                   ,'title': 'Буріння'
                   }
               }
           ,'drug.name':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'drug.name'
                   ,'title': 'Drug name'
                   }
               ,'uk':
                   {'short': 'назв.лік.'
                   ,'title': 'Назва лікарського засобу'
                   }
               }
           ,'drugs':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'drugs'
                   ,'title': 'Drugs and addiction medicine'
                   }
               ,'uk':
                   {'short': 'нарк.'
                   ,'title': 'Наркотики та наркологія'
                   }
               }
           ,'drv.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'drv.'
                   ,'title': 'Drives'
                   }
               ,'uk':
                   {'short': 'прив.'
                   ,'title': 'Привод'
                   }
               }
           ,'drw.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'drw.'
                   ,'title': 'Drawing'
                   }
               ,'uk':
                   {'short': 'крес.'
                   ,'title': 'Креслення'
                   }
               }
           ,'drywall':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'drywall'
                   ,'title': 'Drywall'
                   }
               ,'uk':
                   {'short': 'гіпсокарт.'
                   ,'title': 'Гипсокартон та сис-ми сухого будівництва'
                   }
               }
           ,'dye.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'dye.'
                   ,'title': 'Dyes'
                   }
               ,'uk':
                   {'short': 'барвн.'
                   ,'title': 'Барвники'
                   }
               }
           ,'ecol.':
               {'valid': True
               ,'major': False
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'ecol.'
                   ,'title': 'Ecology'
                   }
               ,'uk':
                   {'short': 'екол.'
                   ,'title': 'Екологія'
                   }
               }
           ,'econ.':
               {'valid': True
               ,'major': True
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'econ.'
                   ,'title': 'Economía'
                   }
               ,'uk':
                   {'short': 'ек.'
                   ,'title': 'Економіка'
                   }
               }
           ,'econ., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'econ., amer.'
                   ,'title': 'Economía, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ек., амер.вир.'
                   ,'title': 'Економіка, Американський вираз (не варыант мови)'
                   }
               }
           ,'econ.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'econ.law.'
                   ,'title': 'Economic law'
                   }
               ,'uk':
                   {'short': 'госп.пр.'
                   ,'title': 'Господарське право'
                   }
               }
           ,'econometr.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'econometr.'
                   ,'title': 'Econometrics'
                   }
               ,'uk':
                   {'short': 'економетр.'
                   ,'title': 'Економетрика'
                   }
               }
           ,'ed.':
               {'valid': True
               ,'major': True
               ,'group': 'Education'
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
               ,'sp':
                   {'short': 'ed.'
                   ,'title': 'Education'
                   }
               ,'uk':
                   {'short': 'осв.'
                   ,'title': 'Освіта'
                   }
               }
           ,'ed., subj.':
               {'valid': False
               ,'major': False
               ,'group': 'Education'
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
               ,'sp':
                   {'short': 'ed., subj.'
                   ,'title': 'School and university subjects'
                   }
               ,'uk':
                   {'short': 'осв., предм.'
                   ,'title': 'Назви навчальних предметів'
                   }
               }
           ,'egypt.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'egypt.'
                   ,'title': 'Egyptology'
                   }
               ,'uk':
                   {'short': 'єгипт.'
                   ,'title': 'Єгиптологія'
                   }
               }
           ,'el.':
               {'valid': True
               ,'major': True
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'electr.'
                   ,'title': 'Electrónica'
                   }
               ,'uk':
                   {'short': 'ел.'
                   ,'title': 'Електроніка'
                   }
               }
           ,'el.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'el.chem.'
                   ,'title': 'Electrochemistry'
                   }
               ,'uk':
                   {'short': 'ел.хім.'
                   ,'title': 'Електрохімія'
                   }
               }
           ,'el.com.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'el.com.'
                   ,'title': 'Electronic commerce'
                   }
               ,'uk':
                   {'short': 'ел.торг.'
                   ,'title': 'Електронна торгівля'
                   }
               }
           ,'el.gen.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'el.gen.'
                   ,'title': 'Electricity generation'
                   }
               ,'uk':
                   {'short': 'виробн.електр.'
                   ,'title': 'Виробництво електроенергії'
                   }
               }
           ,'el.mach.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'el.mach.'
                   ,'title': 'Electric machinery'
                   }
               ,'uk':
                   {'short': 'ел.маш.'
                   ,'title': 'Електричні машини'
                   }
               }
           ,'el.med.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'el.med.'
                   ,'title': 'Electromedicine'
                   }
               ,'uk':
                   {'short': 'ел.мед.'
                   ,'title': 'Електромедицина'
                   }
               }
           ,'el.met.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'el.met.'
                   ,'title': 'Electrometallurgy'
                   }
               ,'uk':
                   {'short': 'елмет.'
                   ,'title': 'Електрометалургія'
                   }
               }
           ,'el.mot.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'el.mot.'
                   ,'title': 'Electric motors'
                   }
               ,'uk':
                   {'short': 'ел.двиг.'
                   ,'title': 'Електродвигуни'
                   }
               }
           ,'el.therm.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'el.therm.'
                   ,'title': 'Electrothermy'
                   }
               ,'uk':
                   {'short': 'елтерм.'
                   ,'title': 'Електротермія'
                   }
               }
           ,'el.tract.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'el.tract.'
                   ,'title': 'Electric traction'
                   }
               ,'uk':
                   {'short': 'ел.тяга'
                   ,'title': 'Електротяга'
                   }
               }
           ,'elect.':
               {'valid': True
               ,'major': False
               ,'group': 'Politics'
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
               ,'sp':
                   {'short': 'elect.'
                   ,'title': 'Elections'
                   }
               ,'uk':
                   {'short': 'вибори'
                   ,'title': 'Вибори'
                   }
               }
           ,'electr.eng.':
               {'valid': True
               ,'major': True
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'electr.eng.'
                   ,'title': 'Electrical engineering'
                   }
               ,'uk':
                   {'short': 'ел.тех.'
                   ,'title': 'Електротехніка'
                   }
               }
           ,'electric.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'electric.'
                   ,'title': 'Electricity'
                   }
               ,'uk':
                   {'short': 'електр.'
                   ,'title': 'Електричний струм'
                   }
               }
           ,'electrophor.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'electrophor.'
                   ,'title': 'Electrophoresis'
                   }
               ,'uk':
                   {'short': 'електроф.'
                   ,'title': 'Електрофорез'
                   }
               }
           ,'elev.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'elev.'
                   ,'title': 'Elevators'
                   }
               ,'uk':
                   {'short': 'ліфти'
                   ,'title': 'Ліфти'
                   }
               }
           ,'els.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'els.'
                   ,'title': 'Electrolysis'
                   }
               ,'uk':
                   {'short': 'електрлз'
                   ,'title': 'Електроліз'
                   }
               }
           ,'embryol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'embriol.'
                   ,'title': 'Embriología'
                   }
               ,'uk':
                   {'short': 'ембр.'
                   ,'title': 'Ембріологія'
                   }
               }
           ,'emerg.care':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'emerg.care'
                   ,'title': 'Emergency medical care'
                   }
               ,'uk':
                   {'short': 'невідкл.доп.'
                   ,'title': 'Невідкладна медична допомога'
                   }
               }
           ,'emotive':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'emotive'
                   ,'title': 'Emotive'
                   }
               ,'uk':
                   {'short': 'емоц.'
                   ,'title': 'Емоційний вираз'
                   }
               }
           ,'empl.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'empl.'
                   ,'title': 'Employment'
                   }
               ,'uk':
                   {'short': 'зайн.'
                   ,'title': 'Зайнятість'
                   }
               }
           ,'endocr.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'endocr.'
                   ,'title': 'Endocrinology'
                   }
               ,'uk':
                   {'short': 'ендокр.'
                   ,'title': 'Ендокринологія'
                   }
               }
           ,'energ.distr.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'energ.distr.'
                   ,'title': 'Energy distribution'
                   }
               ,'uk':
                   {'short': 'розпод.ен.'
                   ,'title': 'Розподіл енергії'
                   }
               }
           ,'energ.ind.':
               {'valid': True
               ,'major': True
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'energ.ind.'
                   ,'title': 'Energy industry'
                   }
               ,'uk':
                   {'short': 'енерг.'
                   ,'title': 'Енергетика'
                   }
               }
           ,'energ.syst.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'energ.syst.'
                   ,'title': 'Energy system'
                   }
               ,'uk':
                   {'short': 'ен.сист.'
                   ,'title': 'Енергосистеми'
                   }
               }
           ,'eng.':
               {'valid': True
               ,'major': True
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'eng.'
                   ,'title': 'Engineering'
                   }
               ,'uk':
                   {'short': 'інж.'
                   ,'title': 'Інженерна справа'
                   }
               }
           ,'eng.geol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'eng.geol.'
                   ,'title': 'Engineering geology'
                   }
               ,'uk':
                   {'short': 'інж.геол.'
                   ,'title': 'Інженерна геологія'
                   }
               }
           ,'engin.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'engin.'
                   ,'title': 'Engines'
                   }
               ,'uk':
                   {'short': 'двиг.вн.зг.'
                   ,'title': 'Двигуни внутрішнього згоряння'
                   }
               }
           ,'engl.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'engl.'
                   ,'title': 'English'
                   }
               ,'uk':
                   {'short': 'англ.'
                   ,'title': 'Англійська мова'
                   }
               }
           ,'entomol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'entomol.'
                   ,'title': 'Entomologia'
                   }
               ,'uk':
                   {'short': 'ентом.'
                   ,'title': 'Ентомологія'
                   }
               }
           ,'environ.':
               {'valid': True
               ,'major': False
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'environ.'
                   ,'title': 'Environment'
                   }
               ,'uk':
                   {'short': 'довк.'
                   ,'title': 'Довкілля'
                   }
               }
           ,'epist.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'epist.'
                   ,'title': 'Epistolary'
                   }
               ,'uk':
                   {'short': 'епіст.'
                   ,'title': 'Епістолярний жанр'
                   }
               }
           ,'equestr.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'equestr.'
                   ,'title': 'Equestrianism'
                   }
               ,'uk':
                   {'short': 'кінн.сп.'
                   ,'title': 'Кінний спорт'
                   }
               }
           ,'eskim.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'esquim.'
                   ,'title': 'Esquimal'
                   }
               ,'uk':
                   {'short': 'еск.'
                   ,'title': 'Ескімоська мова'
                   }
               }
           ,'esot.':
               {'valid': True
               ,'major': False
               ,'group': 'Parasciences'
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
               ,'sp':
                   {'short': 'esot.'
                   ,'title': 'Esoterics'
                   }
               ,'uk':
                   {'short': 'езот.'
                   ,'title': 'Езотерика'
                   }
               }
           ,'esper.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'esper.'
                   ,'title': 'Esperanto'
                   }
               ,'uk':
                   {'short': 'еспер.'
                   ,'title': 'Есперанто'
                   }
               }
           ,'ethnogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'etnogr.'
                   ,'title': 'Etnografía'
                   }
               ,'uk':
                   {'short': 'етн.'
                   ,'title': 'Етнографія'
                   }
               }
           ,'ethnol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'ethnol.'
                   ,'title': 'Ethnology'
                   }
               ,'uk':
                   {'short': 'етнол.'
                   ,'title': 'Етнологія'
                   }
               }
           ,'ethnopsychol.':
               {'valid': True
               ,'major': False
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'ethnopsychol.'
                   ,'title': 'Ethnopsychology'
                   }
               ,'uk':
                   {'short': 'етнопсихол.'
                   ,'title': 'Етнопсихологія'
                   }
               }
           ,'ethol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'ethol.'
                   ,'title': 'Ethology'
                   }
               ,'uk':
                   {'short': 'етол.'
                   ,'title': 'Етологія'
                   }
               }
           ,'euph.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'eufem.'
                   ,'title': 'Eufemismo'
                   }
               ,'uk':
                   {'short': 'евф.'
                   ,'title': 'Евфемізм'
                   }
               }
           ,'evol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'evol.'
                   ,'title': 'Evolution'
                   }
               ,'uk':
                   {'short': 'евол.'
                   ,'title': 'Еволюція'
                   }
               }
           ,'excl.':
               {'valid': True
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'excl.'
                   ,'title': 'Exclamation'
                   }
               ,'uk':
                   {'short': 'оклик'
                   ,'title': 'Оклик'
                   }
               }
           ,'exhib.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'exhib.'
                   ,'title': 'Exhibitions'
                   }
               ,'uk':
                   {'short': 'вист.'
                   ,'title': 'Виставки'
                   }
               }
           ,'explan.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'explan.'
                   ,'title': 'Explanatory translation'
                   }
               ,'uk':
                   {'short': 'поясн.'
                   ,'title': 'Пояснювальний варіант перекладу'
                   }
               }
           ,'extr.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'extr.'
                   ,'title': 'Extrusion'
                   }
               ,'uk':
                   {'short': 'екструз.'
                   ,'title': 'Екструзія'
                   }
               }
           ,'f.trade.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'f.trade.'
                   ,'title': 'Foreign trade'
                   }
               ,'uk':
                   {'short': 'зовн. торг.'
                   ,'title': 'Зовнішня торгівля'
                   }
               }
           ,'facil.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'facil.'
                   ,'title': 'Facilities'
                   }
               ,'uk':
                   {'short': 'вир.приміщ.'
                   ,'title': 'Виробничі приміщення'
                   }
               }
           ,'fant./sci-fi., abbr.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'fant./sci-fi., abrev.'
                   ,'title': 'Fantasy and science fiction, Abreviatura'
                   }
               ,'uk':
                   {'short': 'фант., абрев.'
                   ,'title': 'Фантастика, фентезі, Абревіатура'
                   }
               }
           ,'fash.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'fash.'
                   ,'title': 'Fashion'
                   }
               ,'uk':
                   {'short': 'мод.'
                   ,'title': 'Мода'
                   }
               }
           ,'faux ami':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
               ,'en':
                   {'short': 'faux ami'
                   ,'title': "Translator's false friend"
                   }
               ,'ru':
                   {'short': 'ложн.друг.'
                   ,'title': 'Ложный друг переводчика'
                   }
               ,'de':
                   {'short': 'faux ami'
                   ,'title': "Translator's false friend"
                   }
               ,'sp':
                   {'short': 'faux ami'
                   ,'title': "Translator's false friend"
                   }
               ,'uk':
                   {'short': 'хибн.друг'
                   ,'title': 'Хибний друг перекладача'
                   }
               }
           ,'felin.':
               {'valid': True
               ,'major': False
               ,'group': 'Companion animals'
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
               ,'sp':
                   {'short': 'felin.'
                   ,'title': 'Felinology'
                   }
               ,'uk':
                   {'short': 'фелін.'
                   ,'title': 'Фелінологія'
                   }
               }
           ,'fenc.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'fenc.'
                   ,'title': 'Fencing'
                   }
               ,'uk':
                   {'short': 'фехт.'
                   ,'title': 'Фехтування'
                   }
               }
           ,'ferm.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'ferm.'
                   ,'title': 'Fermentation'
                   }
               ,'uk':
                   {'short': 'ферм.'
                   ,'title': 'Ферментація'
                   }
               }
           ,'fert.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'fert.'
                   ,'title': 'Fertilizers'
                   }
               ,'uk':
                   {'short': 'добр.'
                   ,'title': 'Добрива'
                   }
               }
           ,'fib.optic':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'fib.optic'
                   ,'title': 'Fiber optic'
                   }
               ,'uk':
                   {'short': 'опт.вол.'
                   ,'title': 'Оптичне волокно'
                   }
               }
           ,'fig.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'fig.'
                   ,'title': 'Figuradamente'
                   }
               ,'uk':
                   {'short': 'перен.'
                   ,'title': 'Переносний сенс'
                   }
               }
           ,'fig.of.sp.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'fig.of.sp.'
                   ,'title': 'Figure of speech'
                   }
               ,'uk':
                   {'short': 'образн.'
                   ,'title': 'Образний вислів'
                   }
               }
           ,'fig.skat.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'fig.skat.'
                   ,'title': 'Figure skating'
                   }
               ,'uk':
                   {'short': 'фіг.кат.'
                   ,'title': 'Фігурне катання'
                   }
               }
           ,'file.ext.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'file.ext.'
                   ,'title': 'File extension'
                   }
               ,'uk':
                   {'short': 'розшир.ф.'
                   ,'title': 'Розширення файла'
                   }
               }
           ,'film.equip.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'film.equip.'
                   ,'title': 'Filming equipment'
                   }
               ,'uk':
                   {'short': 'кіноап.'
                   ,'title': 'Кінознімальна апаратура'
                   }
               }
           ,'film.light.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'film.light.'
                   ,'title': 'Film lighting equipment'
                   }
               ,'uk':
                   {'short': 'к.осв.'
                   ,'title': 'Кіноосвітлювальна апаратура'
                   }
               }
           ,'film.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'film.proc.'
                   ,'title': 'Film processing'
                   }
               ,'uk':
                   {'short': 'обр.кіноф.мат.'
                   ,'title': 'Обробка кінофотоматеріалів'
                   }
               }
           ,'fin.':
               {'valid': True
               ,'major': True
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'fin.'
                   ,'title': 'Finanzas'
                   }
               ,'uk':
                   {'short': 'фін.'
                   ,'title': 'Фінанси'
                   }
               }
           ,'finn.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'finn.'
                   ,'title': 'Finnish language'
                   }
               ,'uk':
                   {'short': 'фінськ.'
                   ,'title': 'Фінська мова'
                   }
               }
           ,'fire.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'fire.'
                   ,'title': 'Firefighting and fire-control systems'
                   }
               ,'uk':
                   {'short': 'пожеж.'
                   ,'title': 'Пожежна справа та системи пожежогасіння'
                   }
               }
           ,'fish.farm.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'fish.farm.'
                   ,'title': 'Fish farming (pisciculture)'
                   }
               ,'uk':
                   {'short': 'риб.'
                   ,'title': 'Рибництво'
                   }
               }
           ,'fishery':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'fishery'
                   ,'title': 'Fishery (fishing industry)'
                   }
               ,'uk':
                   {'short': 'риболов.'
                   ,'title': 'Риболовство (промислове)'
                   }
               }
           ,'flor.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'flor.'
                   ,'title': 'Floriculture'
                   }
               ,'uk':
                   {'short': 'квіт.'
                   ,'title': 'Квітникарство'
                   }
               }
           ,'flour.prod.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'flour.prod.'
                   ,'title': 'Flour production'
                   }
               ,'uk':
                   {'short': 'борош.'
                   ,'title': 'Борошняне виробництво'
                   }
               }
           ,'flow.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'flow.'
                   ,'title': 'Flow measurement'
                   }
               ,'uk':
                   {'short': 'витрат.'
                   ,'title': 'Витратометрія'
                   }
               }
           ,'fodd.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'fodd.'
                   ,'title': 'Fodder'
                   }
               ,'uk':
                   {'short': 'корми'
                   ,'title': 'Корми'
                   }
               }
           ,'foil.ships':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'foil.ships'
                   ,'title': 'Foil ships'
                   }
               ,'uk':
                   {'short': 'СПК'
                   ,'title': 'Судна на підводних крилах'
                   }
               }
           ,'folk.':
               {'valid': True
               ,'major': True
               ,'group': 'Folklore'
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
               ,'sp':
                   {'short': 'folk.'
                   ,'title': 'Folklore'
                   }
               ,'uk':
                   {'short': 'фольк.'
                   ,'title': 'Фольклор'
                   }
               }
           ,'food.ind.':
               {'valid': True
               ,'major': True
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'food.ind.'
                   ,'title': 'Food industry'
                   }
               ,'uk':
                   {'short': 'харч.'
                   ,'title': 'Харчова промисловість'
                   }
               }
           ,'food.serv.':
               {'valid': True
               ,'major': False
               ,'group': 'Service industry'
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
               ,'sp':
                   {'short': 'food.serv.'
                   ,'title': 'Food service and catering'
                   }
               ,'uk':
                   {'short': 'гр.харч.'
                   ,'title': 'Громадське харчування'
                   }
               }
           ,'footb.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'footb.'
                   ,'title': 'Football'
                   }
               ,'uk':
                   {'short': 'футб.'
                   ,'title': 'Футбол'
                   }
               }
           ,'footwear':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'footwear'
                   ,'title': 'Footwear'
                   }
               ,'uk':
                   {'short': 'взут.'
                   ,'title': 'Взуття'
                   }
               }
           ,'for.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'for.chem.'
                   ,'title': 'Forest chemistry'
                   }
               ,'uk':
                   {'short': 'лісохім.'
                   ,'title': 'Лісохімія'
                   }
               }
           ,'for.pol.':
               {'valid': True
               ,'major': False
               ,'group': 'Foreign affairs'
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
               ,'sp':
                   {'short': 'for.pol.'
                   ,'title': 'Foreign policy'
                   }
               ,'uk':
                   {'short': 'зовн.політ.'
                   ,'title': 'Зовнішня політика'
                   }
               }
           ,'foreig.aff.':
               {'valid': True
               ,'major': True
               ,'group': 'Foreign affairs'
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
               ,'sp':
                   {'short': 'foreig.aff.'
                   ,'title': 'Foreign affairs'
                   }
               ,'uk':
                   {'short': 'МЗС'
                   ,'title': 'Міністерство закордонних справ'
                   }
               }
           ,'forens.med.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'forens.med.'
                   ,'title': 'Forensic medicine'
                   }
               ,'uk':
                   {'short': 'суд.мед.'
                   ,'title': 'Судова медицина'
                   }
               }
           ,'forestr.':
               {'valid': True
               ,'major': False
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'silvicult.'
                   ,'title': 'Silvicultura'
                   }
               ,'uk':
                   {'short': 'ліс.'
                   ,'title': 'Лісівництво'
                   }
               }
           ,'forestr., amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'silvicult., amer.'
                   ,'title': 'Silvicultura, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ліс., амер.вир.'
                   ,'title': 'Лісівництво, Американський вираз (не варыант мови)'
                   }
               }
           ,'forex':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'forex'
                   ,'title': 'Foreign exchange market'
                   }
               ,'uk':
                   {'short': 'валют.рин.'
                   ,'title': 'Валютний ринок (форекс)'
                   }
               }
           ,'forg.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'forg.'
                   ,'title': 'Forging'
                   }
               ,'uk':
                   {'short': 'кув.'
                   ,'title': 'Кування'
                   }
               }
           ,'formal':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'formal'
                   ,'title': 'Formal'
                   }
               ,'uk':
                   {'short': 'офіц.'
                   ,'title': 'Офіційний вираз'
                   }
               }
           ,'found.engin.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'found.engin.'
                   ,'title': 'Foundation engineering'
                   }
               ,'uk':
                   {'short': 'фунд.буд.'
                   ,'title': 'Фундаментобудування'
                   }
               }
           ,'foundr.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'foundr.'
                   ,'title': 'Foundry'
                   }
               ,'uk':
                   {'short': 'лив.вир.'
                   ,'title': 'Ливарне виробництво'
                   }
               }
           ,'fr.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'fr.'
                   ,'title': 'Francés'
                   }
               ,'uk':
                   {'short': 'фр.'
                   ,'title': 'Французька мова'
                   }
               }
           ,'furn.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'furn.'
                   ,'title': 'Furniture'
                   }
               ,'uk':
                   {'short': 'меб.'
                   ,'title': 'Меблі'
                   }
               }
           ,'gaelic':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'gaelic'
                   ,'title': 'Gaelic'
                   }
               ,'uk':
                   {'short': 'гельськ.'
                   ,'title': 'Гельська (шотландська) мова'
                   }
               }
           ,'galv.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'galv.'
                   ,'title': 'Galvanizing'
                   }
               ,'uk':
                   {'short': 'оцинк.'
                   ,'title': 'Оцинкування'
                   }
               }
           ,'galv.plast.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'galv.plast.'
                   ,'title': 'Galvanoplasty'
                   }
               ,'uk':
                   {'short': 'гальв.'
                   ,'title': 'Гальванотехніка'
                   }
               }
           ,'gambl.':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'gambl.'
                   ,'title': 'Gambling'
                   }
               ,'uk':
                   {'short': 'азартн.'
                   ,'title': 'Азартні ігри'
                   }
               }
           ,'games':
               {'valid': True
               ,'major': True
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'games'
                   ,'title': 'Games (other than sports)'
                   }
               ,'uk':
                   {'short': 'ігри.'
                   ,'title': 'Ігри (окрім спорту)'
                   }
               }
           ,'garden.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'garden.'
                   ,'title': 'Gardening'
                   }
               ,'uk':
                   {'short': 'садівн.'
                   ,'title': 'Садівництво'
                   }
               }
           ,'gas.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'gas.proc.'
                   ,'title': 'Gas processing plants'
                   }
               ,'uk':
                   {'short': 'ГПЗ'
                   ,'title': 'Газопереробні заводи'
                   }
               }
           ,'gastroent.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'gastroent.'
                   ,'title': 'Gastroenterología'
                   }
               ,'uk':
                   {'short': 'гастр.'
                   ,'title': 'Гастроентерологія'
                   }
               }
           ,'gear.tr.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'gear.tr.'
                   ,'title': 'Gear train'
                   }
               ,'uk':
                   {'short': 'зубч.перед.'
                   ,'title': 'Зубчасті передачі'
                   }
               }
           ,'gem.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'gem.'
                   ,'title': 'Gemmology'
                   }
               ,'uk':
                   {'short': 'гем.'
                   ,'title': 'Гемологія'
                   }
               }
           ,'gen.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'gen.'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'заг.'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'gen.eng.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'gen.eng.'
                   ,'title': 'Genetic engineering'
                   }
               ,'uk':
                   {'short': 'ген.інж.'
                   ,'title': 'Генна інженерія'
                   }
               }
           ,'geneal.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'geneal.'
                   ,'title': 'Genealogy'
                   }
               ,'uk':
                   {'short': 'генеал.'
                   ,'title': 'Генеалогія'
                   }
               }
           ,'genet.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'genét.'
                   ,'title': 'Genética'
                   }
               ,'uk':
                   {'short': 'ген.'
                   ,'title': 'Генетика'
                   }
               }
           ,'geobot.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'geobot.'
                   ,'title': 'Geobotanics'
                   }
               ,'uk':
                   {'short': 'геобот.'
                   ,'title': 'Геоботаніка'
                   }
               }
           ,'geochem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'geochem.'
                   ,'title': 'Geochemistry'
                   }
               ,'uk':
                   {'short': 'геохім.'
                   ,'title': 'Геохімія'
                   }
               }
           ,'geochron.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'geochron.'
                   ,'title': 'Geochronology'
                   }
               ,'uk':
                   {'short': 'геохрон.'
                   ,'title': 'Геохронологія'
                   }
               }
           ,'geogr.':
               {'valid': True
               ,'major': True
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'geogr.'
                   ,'title': 'Geografía'
                   }
               ,'uk':
                   {'short': 'геогр.'
                   ,'title': 'Географія'
                   }
               }
           ,'geol.':
               {'valid': True
               ,'major': True
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'geol.'
                   ,'title': 'Geología'
                   }
               ,'uk':
                   {'short': 'геолог.'
                   ,'title': 'Геологія'
                   }
               }
           ,'geom.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'geom.'
                   ,'title': 'Geometría'
                   }
               ,'uk':
                   {'short': 'геом.'
                   ,'title': 'Геометрія'
                   }
               }
           ,'geomech.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'geomech.'
                   ,'title': 'Geomechanics'
                   }
               ,'uk':
                   {'short': 'геомех.'
                   ,'title': 'Геомеханіка'
                   }
               }
           ,'geomorph.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'geomorph.'
                   ,'title': 'Geomorphology'
                   }
               ,'uk':
                   {'short': 'геоморф.'
                   ,'title': 'Геоморфологія'
                   }
               }
           ,'geophys.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'geophys.'
                   ,'title': 'Geophysics'
                   }
               ,'uk':
                   {'short': 'геофіз.'
                   ,'title': 'Геофізика'
                   }
               }
           ,'germ.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'alem.'
                   ,'title': 'Alemán'
                   }
               ,'uk':
                   {'short': 'нім.'
                   ,'title': 'Німецька мова'
                   }
               }
           ,'glass':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'glass'
                   ,'title': 'Glass production'
                   }
               ,'uk':
                   {'short': 'склян.'
                   ,'title': 'Склоробство'
                   }
               }
           ,'glass.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'glass.'
                   ,'title': 'Glass container manufacture'
                   }
               ,'uk':
                   {'short': 'склотар.'
                   ,'title': 'Склотарна промисловість'
                   }
               }
           ,'gloom.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'sombr.'
                   ,'title': 'Sombrío'
                   }
               ,'uk':
                   {'short': 'похмур.'
                   ,'title': 'Похмуро'
                   }
               }
           ,'goldmin.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'goldmin.'
                   ,'title': 'Gold mining'
                   }
               ,'uk':
                   {'short': 'зол.доб.'
                   ,'title': 'Золотодобування'
                   }
               }
           ,'golf.':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'golf.'
                   ,'title': 'Golf'
                   }
               ,'uk':
                   {'short': 'гольф.'
                   ,'title': 'Гольф'
                   }
               }
           ,'gov.':
               {'valid': False
               ,'major': True
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'gov.'
                   ,'title': 'Government, administration and public services'
                   }
               ,'uk':
                   {'short': 'держ.'
                   ,'title': 'Державний апарат та державні послуги'
                   }
               }
           ,'gram.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'gram.'
                   ,'title': 'Gramática'
                   }
               ,'uk':
                   {'short': 'грам.'
                   ,'title': 'Граматика'
                   }
               }
           ,'grav.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'grav.'
                   ,'title': 'Gravimetry'
                   }
               ,'uk':
                   {'short': 'грав.'
                   ,'title': 'Гравіметрія'
                   }
               }
           ,'greek.lang.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'gr.'
                   ,'title': 'Griego'
                   }
               ,'uk':
                   {'short': 'грецьк.'
                   ,'title': 'Грецька мова'
                   }
               }
           ,'green.tech.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'green.tech.'
                   ,'title': 'Greenhouse technology'
                   }
               ,'uk':
                   {'short': 'тепличн.тех.'
                   ,'title': 'Тепличні технології'
                   }
               }
           ,'gymn.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'gymn.'
                   ,'title': 'Gymnastics'
                   }
               ,'uk':
                   {'short': 'гімн.'
                   ,'title': 'Гімнастика'
                   }
               }
           ,'gyrosc.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'gyrosc.'
                   ,'title': 'Gyroscopes'
                   }
               ,'uk':
                   {'short': 'гіроск.'
                   ,'title': 'Гіроскопи'
                   }
               }
           ,'h.rghts.act.':
               {'valid': True
               ,'major': True
               ,'group': 'Human rights activism'
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
               ,'sp':
                   {'short': 'h.rghts.act.'
                   ,'title': 'Human rights activism'
                   }
               ,'uk':
                   {'short': 'прав.люд.'
                   ,'title': 'Права людини і правозахисна діяльність'
                   }
               }
           ,'hab.':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'hab.'
                   ,'title': 'Haberdashery'
                   }
               ,'uk':
                   {'short': 'галант.'
                   ,'title': 'Галантерея'
                   }
               }
           ,'hack.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'hack.'
                   ,'title': 'Hacking'
                   }
               ,'uk':
                   {'short': 'хакер.'
                   ,'title': 'Хакерство'
                   }
               }
           ,'handb.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'handb.'
                   ,'title': 'Handball'
                   }
               ,'uk':
                   {'short': 'гандб.'
                   ,'title': 'Гандбол'
                   }
               }
           ,'handicraft.':
               {'valid': True
               ,'major': False
               ,'group': 'Hobbies and pastimes'
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
               ,'sp':
                   {'short': 'handicraft.'
                   ,'title': 'Handicraft'
                   }
               ,'uk':
                   {'short': 'рукод.'
                   ,'title': 'Рукоділля'
                   }
               }
           ,'hawai.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'hawai.'
                   ,'title': 'Hawaii'
                   }
               ,'uk':
                   {'short': 'Гаваї'
                   ,'title': 'Гаваї'
                   }
               }
           ,'health.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'health.'
                   ,'title': 'Health care'
                   }
               ,'uk':
                   {'short': 'ох.здор.'
                   ,'title': 'Охорона здоров’я'
                   }
               }
           ,'hear.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'hear.'
                   ,'title': 'Hearing aid'
                   }
               ,'uk':
                   {'short': 'слух.ап.'
                   ,'title': 'Слухові апарати'
                   }
               }
           ,'heat.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'heat.'
                   ,'title': 'Heating'
                   }
               ,'uk':
                   {'short': 'опален.'
                   ,'title': 'Опалення'
                   }
               }
           ,'heat.exch.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'heat.exch.'
                   ,'title': 'Heat exchangers'
                   }
               ,'uk':
                   {'short': 'тепл.ап.'
                   ,'title': 'Теплообмінні апарати'
                   }
               }
           ,'heat.transf.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'heat.transf.'
                   ,'title': 'Heat transfer'
                   }
               ,'uk':
                   {'short': 'теплопер.'
                   ,'title': 'Теплопередача'
                   }
               }
           ,'heavy.eq.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'heavy.eq.'
                   ,'title': 'Heavy equipment vehicles'
                   }
               ,'uk':
                   {'short': 'буд.тех.'
                   ,'title': 'Будівельна техніка'
                   }
               }
           ,'helic.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'helic.'
                   ,'title': 'Helicopters'
                   }
               ,'uk':
                   {'short': 'гелік.'
                   ,'title': 'Гелікоптери'
                   }
               }
           ,'helminth.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'helmint.'
                   ,'title': 'Helmintología'
                   }
               ,'uk':
                   {'short': 'гельм.'
                   ,'title': 'Гельмінтологія'
                   }
               }
           ,'hemat.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'hemat.'
                   ,'title': 'Hematología'
                   }
               ,'uk':
                   {'short': 'гемат.'
                   ,'title': 'Гематологія'
                   }
               }
           ,'herald.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'heráld.'
                   ,'title': 'Heráldica'
                   }
               ,'uk':
                   {'short': 'геральд.'
                   ,'title': 'Геральдика'
                   }
               }
           ,'herpet.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'herpet.'
                   ,'title': 'Herpetology (incl. serpentology)'
                   }
               ,'uk':
                   {'short': 'герпет.'
                   ,'title': 'Герпетологія (вкл. з серпентологією)'
                   }
               }
           ,'hi-fi':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'hi-fi'
                   ,'title': 'Hi-Fi'
                   }
               ,'uk':
                   {'short': 'Hi-Fi'
                   ,'title': 'Hi-Fi'
                   }
               }
           ,'hi.jump.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'hi.jump.'
                   ,'title': 'High jump'
                   }
               ,'uk':
                   {'short': 'стриб.вис.'
                   ,'title': 'Стрибки у висоту'
                   }
               }
           ,'hindi':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'hindi'
                   ,'title': 'Hindi'
                   }
               ,'uk':
                   {'short': 'хінді'
                   ,'title': 'Хінді'
                   }
               }
           ,'hist.':
               {'valid': True
               ,'major': True
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'hist.'
                   ,'title': 'Historia'
                   }
               ,'uk':
                   {'short': 'іст.'
                   ,'title': 'Історія'
                   }
               }
           ,'hist.fig.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'hist.fig.'
                   ,'title': 'Historical figure'
                   }
               ,'uk':
                   {'short': 'іст.особ.'
                   ,'title': 'Історичні особистості'
                   }
               }
           ,'histol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'histol.'
                   ,'title': 'Histología'
                   }
               ,'uk':
                   {'short': 'гіст.'
                   ,'title': 'Гістологія'
                   }
               }
           ,'hobby':
               {'valid': False
               ,'major': True
               ,'group': 'Hobbies and pastimes'
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
               ,'sp':
                   {'short': 'hobby'
                   ,'title': 'Hobbies and pastimes'
                   }
               ,'uk':
                   {'short': 'хобі.'
                   ,'title': 'Хобі, захоплення, дозвілля'
                   }
               }
           ,'hockey.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'hockey.'
                   ,'title': 'Hockey'
                   }
               ,'uk':
                   {'short': 'хокей'
                   ,'title': 'Хокей'
                   }
               }
           ,'homeopath.':
               {'valid': True
               ,'major': False
               ,'group': 'Medicine - Alternative medicine'
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
               ,'sp':
                   {'short': 'homeopath.'
                   ,'title': 'Homeopathy'
                   }
               ,'uk':
                   {'short': 'гомеопат.'
                   ,'title': 'Гомеопатія'
                   }
               }
           ,'horse.breed.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'horse.breed.'
                   ,'title': 'Horse breeding'
                   }
               ,'uk':
                   {'short': 'кон.'
                   ,'title': 'Конярство'
                   }
               }
           ,'horse.rac.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'horse.rac.'
                   ,'title': 'Horse racing'
                   }
               ,'uk':
                   {'short': 'кінн.перег.'
                   ,'title': 'Кінні перегони'
                   }
               }
           ,'horticult.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'horticult.'
                   ,'title': 'Horticulture'
                   }
               ,'uk':
                   {'short': 'росл.'
                   ,'title': 'Рослинництво'
                   }
               }
           ,'hotels':
               {'valid': True
               ,'major': False
               ,'group': 'Service industry'
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
               ,'sp':
                   {'short': 'hotels'
                   ,'title': 'Hotel industry'
                   }
               ,'uk':
                   {'short': 'готел.'
                   ,'title': 'Готельна справа'
                   }
               }
           ,'house.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'house.'
                   ,'title': 'Household appliances'
                   }
               ,'uk':
                   {'short': 'побут.тех.'
                   ,'title': 'Побутова техніка'
                   }
               }
           ,'hovercr.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'hovercr.'
                   ,'title': 'Hovercraft'
                   }
               ,'uk':
                   {'short': 'СПП'
                   ,'title': 'Судна на повітряній подушці'
                   }
               }
           ,'humor.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'humor.'
                   ,'title': 'Humorístico'
                   }
               ,'uk':
                   {'short': 'жарт.'
                   ,'title': 'Жартівливий вираз'
                   }
               }
           ,'hunt.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'caza'
                   ,'title': 'Caza y cinegética'
                   }
               ,'uk':
                   {'short': 'мислив.'
                   ,'title': 'Мисливство та мисливствознавство'
                   }
               }
           ,'hydr.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'hydr.'
                   ,'title': 'Hydraulic engineering'
                   }
               ,'uk':
                   {'short': 'гідротех.'
                   ,'title': 'Гідротехніка'
                   }
               }
           ,'hydraul.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'hydraul.'
                   ,'title': 'Hydraulics'
                   }
               ,'uk':
                   {'short': 'гідравл.'
                   ,'title': 'Гідравліка'
                   }
               }
           ,'hydroac.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'hydroac.'
                   ,'title': 'Hydroacoustics'
                   }
               ,'uk':
                   {'short': 'гідроак.'
                   ,'title': 'Гідроакустика'
                   }
               }
           ,'hydrobiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'hydrobiol.'
                   ,'title': 'Hydrobiology'
                   }
               ,'uk':
                   {'short': 'гідробіол.'
                   ,'title': 'Гідробіологія'
                   }
               }
           ,'hydroel.st.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'hydroel.st.'
                   ,'title': 'Hydroelectric power stations'
                   }
               ,'uk':
                   {'short': 'ГЕС'
                   ,'title': 'Гідроелектростанції'
                   }
               }
           ,'hydrogeol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'hydrogeol.'
                   ,'title': 'Hydrogeology'
                   }
               ,'uk':
                   {'short': 'гідрогеол.'
                   ,'title': 'Гідрогеологія'
                   }
               }
           ,'hydrogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'hidrogr.'
                   ,'title': 'Hidrografía'
                   }
               ,'uk':
                   {'short': 'гідр.'
                   ,'title': 'Гідрографія'
                   }
               }
           ,'hydrol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'hydrol.'
                   ,'title': 'Hydrology'
                   }
               ,'uk':
                   {'short': 'гідрол.'
                   ,'title': 'Гідрологія'
                   }
               }
           ,'hydromech.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'hydromech.'
                   ,'title': 'Hydromechanics'
                   }
               ,'uk':
                   {'short': 'гідромех.'
                   ,'title': 'Гідромеханіка'
                   }
               }
           ,'hydropl.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'hydropl.'
                   ,'title': 'Hydroplanes'
                   }
               ,'uk':
                   {'short': 'гідропл.'
                   ,'title': 'Гідроплани'
                   }
               }
           ,'hygien.':
               {'valid': True
               ,'major': False
               ,'group': 'Wellness'
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
               ,'sp':
                   {'short': 'hygien.'
                   ,'title': 'Hygiene'
                   }
               ,'uk':
                   {'short': 'гіг.'
                   ,'title': 'Гігієна'
                   }
               }
           ,'ice.form.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'ice.form.'
                   ,'title': 'Ice formation'
                   }
               ,'uk':
                   {'short': 'льодоутв.'
                   ,'title': 'Льодоутворення'
                   }
               }
           ,'icel.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'icel.'
                   ,'title': 'Iceland'
                   }
               ,'uk':
                   {'short': 'ісл.'
                   ,'title': 'Ісландська мова'
                   }
               }
           ,'ichtyol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'ichtyol.'
                   ,'title': 'Ichthyology'
                   }
               ,'uk':
                   {'short': 'іхт.'
                   ,'title': 'Іхтіологія'
                   }
               }
           ,'idiom':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'idiom'
                   ,'title': 'Idiomatic'
                   }
               ,'uk':
                   {'short': 'ідіом.в.'
                   ,'title': 'Ідіоматичний вираз'
                   }
               }
           ,'idiom, amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'idiom, amer.'
                   ,'title': 'Idiomatic, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'ідіом.в., амер.вир.'
                   ,'title': 'Ідіоматичний вираз, Американський вираз (не варыант мови)'
                   }
               }
           ,'idiom, brit.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'idiom, brit.usg.'
                   ,'title': 'Idiomatic, British (usage, not BrE)'
                   }
               ,'uk':
                   {'short': 'ідіом.в., брит.вир.'
                   ,'title': 'Ідіоматичний вираз, Британський вираз (не варіант мови)'
                   }
               }
           ,'imitat.':
               {'valid': True
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'imitat.'
                   ,'title': 'Iimitative (onomatopoeic)'
                   }
               ,'uk':
                   {'short': 'звуконасл.'
                   ,'title': 'Звуконаслідування'
                   }
               }
           ,'immigr.':
               {'valid': True
               ,'major': False
               ,'group': 'Foreign affairs'
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
               ,'sp':
                   {'short': 'immigr.'
                   ,'title': 'Immigration and citizenship'
                   }
               ,'uk':
                   {'short': 'іміграц.'
                   ,'title': 'Іміграція та громадянство'
                   }
               }
           ,'immunol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'inmunol.'
                   ,'title': 'Inmunología'
                   }
               ,'uk':
                   {'short': 'імун.'
                   ,'title': 'Імунологія'
                   }
               }
           ,'indust.hyg.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'indust.hyg.'
                   ,'title': 'Industrial hygiene'
                   }
               ,'uk':
                   {'short': 'пром.гіг.'
                   ,'title': 'Промислова гігієна'
                   }
               }
           ,'industr.':
               {'valid': True
               ,'major': True
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'industr.'
                   ,'title': 'Industry'
                   }
               ,'uk':
                   {'short': 'пром.'
                   ,'title': 'Промисловість'
                   }
               }
           ,'inet.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'inet.'
                   ,'title': 'Internet'
                   }
               ,'uk':
                   {'short': 'інт.'
                   ,'title': 'Інтернет'
                   }
               }
           ,'inf.secur.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'inf.secur.'
                   ,'title': 'Information security'
                   }
               ,'uk':
                   {'short': 'інф.безп.'
                   ,'title': 'Інформаційна безпека'
                   }
               }
           ,'inform.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'infr.techn.':
               {'valid': True
               ,'major': False
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'infr.techn.'
                   ,'title': 'Infrared technology'
                   }
               ,'uk':
                   {'short': 'інфр.'
                   ,'title': 'Інфрачервона техніка'
                   }
               }
           ,'inherit.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'inherit.law.'
                   ,'title': 'Inheritance law'
                   }
               ,'uk':
                   {'short': 'спадк.пр.'
                   ,'title': 'Спадкове право'
                   }
               }
           ,'inorg.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'inorg.chem.'
                   ,'title': 'Inorganic chemistry'
                   }
               ,'uk':
                   {'short': 'неорг.хім.'
                   ,'title': 'Неорганічна хімія'
                   }
               }
           ,'insur.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'segur.'
                   ,'title': 'Seguros'
                   }
               ,'uk':
                   {'short': 'страх.'
                   ,'title': 'Страхування'
                   }
               }
           ,'int. law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'int. law.'
                   ,'title': 'International law'
                   }
               ,'uk':
                   {'short': 'міжн. прав.'
                   ,'title': 'Міжнародне право'
                   }
               }
           ,'int.circ.':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'int.circ.'
                   ,'title': 'Integrated circuits'
                   }
               ,'uk':
                   {'short': 'інтегр.сх.'
                   ,'title': 'Інтегральні схеми'
                   }
               }
           ,'int.rel.':
               {'valid': True
               ,'major': False
               ,'group': 'Foreign affairs'
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
               ,'sp':
                   {'short': 'int.rel.'
                   ,'title': 'International relations'
                   }
               ,'uk':
                   {'short': 'міжн.відн.'
                   ,'title': 'Міжнародні відносини'
                   }
               }
           ,'int.transport.':
               {'valid': True
               ,'major': False
               ,'group': 'Logistics'
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
               ,'sp':
                   {'short': 'int.transport.'
                   ,'title': 'International transportation'
                   }
               ,'uk':
                   {'short': 'міжн.перевез.'
                   ,'title': 'Міжнародні перевезення'
                   }
               }
           ,'intell.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'intell.'
                   ,'title': 'Intelligence and security services'
                   }
               ,'uk':
                   {'short': 'спецсл.'
                   ,'title': 'Спецслужби та розвідка'
                   }
               }
           ,'interntl.trade.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'interntl.trade.'
                   ,'title': 'International trade'
                   }
               ,'uk':
                   {'short': 'міжн.торг.'
                   ,'title': 'Міжнародна торгівля'
                   }
               }
           ,'invect.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'invect.'
                   ,'title': 'Invective'
                   }
               ,'uk':
                   {'short': 'лайка'
                   ,'title': 'Лайка'
                   }
               }
           ,'invest.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'invest.'
                   ,'title': 'Investment'
                   }
               ,'uk':
                   {'short': 'інвест.'
                   ,'title': 'Інвестиції'
                   }
               }
           ,'irish.lang.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'irland.'
                   ,'title': 'Irlandés'
                   }
               ,'uk':
                   {'short': 'ірл.мов.'
                   ,'title': 'Ірландська мова'
                   }
               }
           ,'ironic.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'iron.'
                   ,'title': 'Ironía'
                   }
               ,'uk':
                   {'short': 'ірон.'
                   ,'title': 'Іронія'
                   }
               }
           ,'isol.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'isol.'
                   ,'title': 'Isolation'
                   }
               ,'uk':
                   {'short': 'ізол.'
                   ,'title': 'Ізоляція'
                   }
               }
           ,'ital.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'ital.'
                   ,'title': 'Italiano'
                   }
               ,'uk':
                   {'short': 'італ.'
                   ,'title': 'Італійська мова'
                   }
               }
           ,'jamaic.eng.':
               {'valid': True
               ,'major': False
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'jamaic.eng.'
                   ,'title': 'Jamaican English'
                   }
               ,'uk':
                   {'short': 'ямайск.анг.'
                   ,'title': 'Ямайська англійська'
                   }
               }
           ,'jap.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'jap.'
                   ,'title': 'Japanese language'
                   }
               ,'uk':
                   {'short': 'яп.'
                   ,'title': 'Японська мова'
                   }
               }
           ,'jarg.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'argot'
                   ,'title': 'Argot'
                   }
               ,'uk':
                   {'short': 'жарг.'
                   ,'title': 'Жаргон'
                   }
               }
           ,'jet.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'jet.'
                   ,'title': 'Jet engines'
                   }
               ,'uk':
                   {'short': 'реакт.дв.'
                   ,'title': 'Реактивні двигуни'
                   }
               }
           ,'jewl.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'jewl.'
                   ,'title': 'Jewelry'
                   }
               ,'uk':
                   {'short': 'юв.'
                   ,'title': 'Ювелірна справа'
                   }
               }
           ,'journ.':
               {'valid': True
               ,'major': False
               ,'group': 'Mass media'
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
               ,'sp':
                   {'short': 'journ.'
                   ,'title': 'Journalism (terminology)'
                   }
               ,'uk':
                   {'short': 'журн.'
                   ,'title': 'Журналістика (термінологія)'
                   }
               }
           ,'judo.':
               {'valid': False
               ,'major': False
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'judo.'
                   ,'title': 'Judo'
                   }
               ,'uk':
                   {'short': 'дз.'
                   ,'title': 'Дзюдо'
                   }
               }
           ,'karate.':
               {'valid': True
               ,'major': False
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'karate.'
                   ,'title': 'Karate'
                   }
               ,'uk':
                   {'short': 'карате.'
                   ,'title': 'Карате'
                   }
               }
           ,'knit.goods':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'knit.goods'
                   ,'title': 'Knitted goods'
                   }
               ,'uk':
                   {'short': 'трик.'
                   ,'title': 'Трикотаж'
                   }
               }
           ,'korea.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'korea.'
                   ,'title': 'Korean'
                   }
               ,'uk':
                   {'short': 'кор.'
                   ,'title': 'Корейська мова'
                   }
               }
           ,'lab.eq.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'lab.eq.'
                   ,'title': 'Equipamiento de laboratorio'
                   }
               ,'uk':
                   {'short': 'лаб.'
                   ,'title': 'Лабораторне обладнання'
                   }
               }
           ,'lab.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'lab.law.'
                   ,'title': 'Labor law'
                   }
               ,'uk':
                   {'short': 'труд.пр.'
                   ,'title': 'Трудове право'
                   }
               }
           ,'labor.org.':
               {'valid': True
               ,'major': False
               ,'group': 'Management'
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
               ,'sp':
                   {'short': 'labor.org.'
                   ,'title': 'Labor organization'
                   }
               ,'uk':
                   {'short': 'орг.вироб.'
                   ,'title': 'Організація виробництва'
                   }
               }
           ,'landsc.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'landsc.'
                   ,'title': 'Landscaping'
                   }
               ,'uk':
                   {'short': 'ландш.диз.'
                   ,'title': 'Ландшафтний дизайн'
                   }
               }
           ,'laser.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'laser.'
                   ,'title': 'Lasers'
                   }
               ,'uk':
                   {'short': 'лаз.'
                   ,'title': 'Лазери'
                   }
               }
           ,'laser.med.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'laser.med.'
                   ,'title': 'Laser medicine'
                   }
               ,'uk':
                   {'short': 'лазер.мед.'
                   ,'title': 'Лазерна медицина'
                   }
               }
           ,'lat.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'lat.'
                   ,'title': 'Latín'
                   }
               ,'uk':
                   {'short': 'лат.'
                   ,'title': 'Латинська мова'
                   }
               }
           ,'lat.amer.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'lat.amer.'
                   ,'title': 'Latin American'
                   }
               ,'uk':
                   {'short': 'лат.амер.'
                   ,'title': 'Латиноамериканський вираз'
                   }
               }
           ,'lat.amer.sl.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'lat.amer.sl.'
                   ,'title': 'Latin American slang'
                   }
               ,'uk':
                   {'short': 'лат.амер.жарг.'
                   ,'title': 'Латиноамериканський жаргон'
                   }
               }
           ,'laud.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'laud.'
                   ,'title': 'Laudatory'
                   }
               ,'uk':
                   {'short': 'схвал.'
                   ,'title': 'Схвально'
                   }
               }
           ,'law':
               {'valid': True
               ,'major': True
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'jur.'
                   ,'title': 'Jurídico'
                   }
               ,'uk':
                   {'short': 'юр.'
                   ,'title': 'Юридична лексика'
                   }
               }
           ,'law, ADR':
               {'valid': False
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'jur.,SAC'
                   ,'title': 'Solución alternativa de controversias'
                   }
               ,'uk':
                   {'short': 'юр., АВС'
                   ,'title': 'Альтернативне врегулювання спорів'
                   }
               }
           ,'law, amer.usg.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'jur., amer.'
                   ,'title': 'Jurídico, Americano (uso)'
                   }
               ,'uk':
                   {'short': 'юр., амер.вир.'
                   ,'title': 'Юридична лексика, Американський вираз (не варыант мови)'
                   }
               }
           ,'law, com.law':
               {'valid': False
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'jur.:anglosaj.'
                   ,'title': 'Jurídico: sistema anglosajón'
                   }
               ,'uk':
                   {'short': 'юр., англос.'
                   ,'title': 'Загальне право (англосаксонська правова система)'
                   }
               }
           ,'law, contr., context.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'contr.jur., context.'
                   ,'title': 'Contratos jurídicos, Contextual meaning'
                   }
               ,'uk':
                   {'short': 'юр., дог., конт.'
                   ,'title': 'Договори та контракти, Контекстуальне значення'
                   }
               }
           ,'law, copyr.':
               {'valid': False
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'law, copyr.'
                   ,'title': 'Copyright'
                   }
               ,'uk':
                   {'short': 'юр., автор.'
                   ,'title': 'Авторське право'
                   }
               }
           ,'law, copyr., abbr.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'law, copyr., abrev.'
                   ,'title': 'Copyright, Abreviatura'
                   }
               ,'uk':
                   {'short': 'юр., автор., абрев.'
                   ,'title': 'Авторське право, Абревіатура'
                   }
               }
           ,'law, court':
               {'valid': False
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'law, court'
                   ,'title': 'Court (law)'
                   }
               ,'uk':
                   {'short': 'юр., суд.'
                   ,'title': 'Судова лексика'
                   }
               }
           ,'law.enf.':
               {'valid': True
               ,'major': True
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'law.enf.'
                   ,'title': 'Law enforcement'
                   }
               ,'uk':
                   {'short': 'правоохор.'
                   ,'title': 'Правоохоронна діяльність'
                   }
               }
           ,'lean.prod.':
               {'valid': True
               ,'major': False
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'lean.prod.'
                   ,'title': 'Lean production'
                   }
               ,'uk':
                   {'short': 'ощ.вироб.'
                   ,'title': 'Ощадливе виробництво'
                   }
               }
           ,'leath.':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'leath.'
                   ,'title': 'Leather'
                   }
               ,'uk':
                   {'short': 'шкір.'
                   ,'title': 'Шкіряна промисловість'
                   }
               }
           ,'leg.ent.typ.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'leg.ent.typ.'
                   ,'title': 'Legal entity types (business legal structures)'
                   }
               ,'uk':
                   {'short': 'форм.комп.'
                   ,'title': 'Організаційно-правові форми компаній'
                   }
               }
           ,'legal.theor.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'legal.theor.'
                   ,'title': 'Legal theory'
                   }
               ,'uk':
                   {'short': 'теор.прав.'
                   ,'title': 'Теорія права'
                   }
               }
           ,'level.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'level.'
                   ,'title': 'Level measurement'
                   }
               ,'uk':
                   {'short': 'рівнеметр.'
                   ,'title': 'Рівнеметрія'
                   }
               }
           ,'lgbt':
               {'valid': True
               ,'major': False
               ,'group': 'Human rights activism'
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
               ,'sp':
                   {'short': 'lgbt'
                   ,'title': 'LGBT'
                   }
               ,'uk':
                   {'short': 'лгбт'
                   ,'title': 'ЛГБТ'
                   }
               }
           ,'libr.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'libr.'
                   ,'title': 'Librarianship'
                   }
               ,'uk':
                   {'short': 'бібліот.'
                   ,'title': 'Бібліотечна справа'
                   }
               }
           ,'life.sc.':
               {'valid': True
               ,'major': True
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'life.sc.'
                   ,'title': 'Life sciences'
                   }
               ,'uk':
                   {'short': 'мед.біол.'
                   ,'title': 'Медико-біологічні науки'
                   }
               }
           ,'light.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'light.'
                   ,'title': 'Lighting (other than cinema)'
                   }
               ,'uk':
                   {'short': 'світл.'
                   ,'title': 'Світлотехніка'
                   }
               }
           ,'limn.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'limn.'
                   ,'title': 'Limnology'
                   }
               ,'uk':
                   {'short': 'лімн.'
                   ,'title': 'Лімнологія'
                   }
               }
           ,'ling.':
               {'valid': True
               ,'major': True
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'ling.'
                   ,'title': 'Lingüística'
                   }
               ,'uk':
                   {'short': 'лінгв.'
                   ,'title': 'Лінгвістика'
                   }
               }
           ,'lit.':
               {'valid': True
               ,'major': True
               ,'group': 'Literature'
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
               ,'sp':
                   {'short': 'lit.'
                   ,'title': 'Literatura'
                   }
               ,'uk':
                   {'short': 'літ.'
                   ,'title': 'Література'
                   }
               }
           ,'lit., f.tales':
               {'valid': False
               ,'major': False
               ,'group': 'Literature'
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
               ,'sp':
                   {'short': 'lit., f.tales'
                   ,'title': 'Fairy tales'
                   }
               ,'uk':
                   {'short': 'літ., казк.'
                   ,'title': 'Казки'
                   }
               }
           ,'liter.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'liter.'
                   ,'title': 'Literally'
                   }
               ,'uk':
                   {'short': 'букв.'
                   ,'title': 'Буквальне значення'
                   }
               }
           ,'lithol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'lithol.'
                   ,'title': 'Lithology'
                   }
               ,'uk':
                   {'short': 'літол.'
                   ,'title': 'Літологія'
                   }
               }
           ,'load.equip.':
               {'valid': True
               ,'major': False
               ,'group': 'Logistics'
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
               ,'sp':
                   {'short': 'load.equip.'
                   ,'title': 'Loading equipment'
                   }
               ,'uk':
                   {'short': 'вант.уст.'
                   ,'title': 'Вантажне устаткування'
                   }
               }
           ,'loc.name.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'loc.name.'
                   ,'title': 'Local name'
                   }
               ,'uk':
                   {'short': 'місц.'
                   ,'title': 'Місцева назва'
                   }
               }
           ,'logging':
               {'valid': True
               ,'major': False
               ,'group': 'Wood, pulp and paper industries'
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
               ,'sp':
                   {'short': 'logging'
                   ,'title': 'Logging'
                   }
               ,'uk':
                   {'short': 'ліс.заг.'
                   ,'title': 'Заготівля лісу'
                   }
               }
           ,'logic':
               {'valid': True
               ,'major': False
               ,'group': 'Philosophy'
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
               ,'sp':
                   {'short': 'lóg.'
                   ,'title': 'Lógica'
                   }
               ,'uk':
                   {'short': 'логіка'
                   ,'title': 'Логіка'
                   }
               }
           ,'logist.':
               {'valid': True
               ,'major': True
               ,'group': 'Logistics'
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
               ,'sp':
                   {'short': 'logist.'
                   ,'title': 'Logistics'
                   }
               ,'uk':
                   {'short': 'логіст.'
                   ,'title': 'Логістика'
                   }
               }
           ,'logop.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'logop.'
                   ,'title': 'Logopedics'
                   }
               ,'uk':
                   {'short': 'логоп.'
                   ,'title': 'Логопедія'
                   }
               }
           ,'low':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'low'
                   ,'title': 'Low register'
                   }
               ,'uk':
                   {'short': 'зниж.'
                   ,'title': 'Знижений регістр'
                   }
               }
           ,'low.germ.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'low.germ.'
                   ,'title': 'Lower German'
                   }
               ,'uk':
                   {'short': 'ниж.нім.'
                   ,'title': 'Нижньо-німецький вираз'
                   }
               }
           ,'luge.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'luge.'
                   ,'title': 'Luge'
                   }
               ,'uk':
                   {'short': 'санн.'
                   ,'title': 'Санний спорт'
                   }
               }
           ,'mach.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'mach.'
                   ,'title': 'Machine tools'
                   }
               ,'uk':
                   {'short': 'верст.'
                   ,'title': 'Верстати'
                   }
               }
           ,'mach.comp.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'mach.comp.'
                   ,'title': 'Machine components'
                   }
               ,'uk':
                   {'short': 'д.маш.'
                   ,'title': 'Деталі машин'
                   }
               }
           ,'magn.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'magn.'
                   ,'title': 'Magnetics'
                   }
               ,'uk':
                   {'short': 'магн.'
                   ,'title': 'Магнетизм'
                   }
               }
           ,'magn.tomogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'magn.tomogr.'
                   ,'title': 'Magnetic tomography'
                   }
               ,'uk':
                   {'short': 'томогр.'
                   ,'title': 'Томографія'
                   }
               }
           ,'magnet.image.rec.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'magnet.image.rec.'
                   ,'title': 'Magnetic image recording'
                   }
               ,'uk':
                   {'short': 'магн.зобр.'
                   ,'title': 'Магнітний запис зображення'
                   }
               }
           ,'malac.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'malac.'
                   ,'title': 'Malacology'
                   }
               ,'uk':
                   {'short': 'малак.'
                   ,'title': 'Малакологія'
                   }
               }
           ,'malay.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'malay.'
                   ,'title': 'Malay'
                   }
               ,'uk':
                   {'short': 'малайськ.'
                   ,'title': 'Малайська мова'
                   }
               }
           ,'mamal.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'mamal.'
                   ,'title': 'Mammalogy'
                   }
               ,'uk':
                   {'short': 'мамол.'
                   ,'title': 'Мамологія'
                   }
               }
           ,'mamm.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'mamm.'
                   ,'title': 'Mammals'
                   }
               ,'uk':
                   {'short': 'ссавц.'
                   ,'title': 'Ссавці'
                   }
               }
           ,'manag.':
               {'valid': True
               ,'major': True
               ,'group': 'Management'
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
               ,'sp':
                   {'short': 'manag.'
                   ,'title': 'Management'
                   }
               ,'uk':
                   {'short': 'менедж.'
                   ,'title': 'Менеджмент'
                   }
               }
           ,'manga.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'manga.'
                   ,'title': 'Manga'
                   }
               ,'uk':
                   {'short': 'манґа'
                   ,'title': 'Манґа'
                   }
               }
           ,'maor.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'maor.'
                   ,'title': 'Maori'
                   }
               ,'uk':
                   {'short': 'маорі'
                   ,'title': 'Маорі'
                   }
               }
           ,'mar.law':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'mar.law'
                   ,'title': 'Maritime law & Law of the Sea'
                   }
               ,'uk':
                   {'short': 'мор.пр.'
                   ,'title': 'Морське право'
                   }
               }
           ,'market.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'market.'
                   ,'title': 'Marketing'
                   }
               ,'uk':
                   {'short': 'марк.'
                   ,'title': 'Маркетинг'
                   }
               }
           ,'mart.arts':
               {'valid': True
               ,'major': True
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'artes.marc.'
                   ,'title': 'Artes marciales y deportes de combate'
                   }
               ,'uk':
                   {'short': 'бой.мист.'
                   ,'title': 'Бойові мистецтва та єдиноборства'
                   }
               }
           ,'match.prod.':
               {'valid': True
               ,'major': False
               ,'group': 'Wood, pulp and paper industries'
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
               ,'sp':
                   {'short': 'match.prod.'
                   ,'title': 'Matches'
                   }
               ,'uk':
                   {'short': 'сірн.'
                   ,'title': 'Сірникове виробництво'
                   }
               }
           ,'mater.sc.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'mater.sc.'
                   ,'title': 'Materials science'
                   }
               ,'uk':
                   {'short': 'матеріалозн.'
                   ,'title': 'Матеріалознавство'
                   }
               }
           ,'math.':
               {'valid': True
               ,'major': True
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'mat.'
                   ,'title': 'Matemáticas'
                   }
               ,'uk':
                   {'short': 'мат.'
                   ,'title': 'Математика'
                   }
               }
           ,'math.anal.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'math.anal.'
                   ,'title': 'Mathematical analysis'
                   }
               ,'uk':
                   {'short': 'мат.ан.'
                   ,'title': 'Математичний аналіз'
                   }
               }
           ,'mean.2':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'mean.2'
                   ,'title': 'Meaning 2'
                   }
               ,'uk':
                   {'short': 'знач.2'
                   ,'title': 'Значення 2'
                   }
               }
           ,'meas.inst.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'meas.inst.'
                   ,'title': 'Measuring instruments'
                   }
               ,'uk':
                   {'short': 'вим.пр.'
                   ,'title': 'Вимірювальні прилади'
                   }
               }
           ,'meat.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'meat.'
                   ,'title': 'Meat processing'
                   }
               ,'uk':
                   {'short': "м'яс.вир."
                   ,'title': 'М’ясне виробництво'
                   }
               }
           ,'mech.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'mech.'
                   ,'title': 'Mechanics'
                   }
               ,'uk':
                   {'short': 'мех.'
                   ,'title': 'Механіка'
                   }
               }
           ,'mech.eng.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'mech.eng.'
                   ,'title': 'Mechanic engineering'
                   }
               ,'uk':
                   {'short': 'маш.'
                   ,'title': 'Машинобудування'
                   }
               }
           ,'med.':
               {'valid': True
               ,'major': True
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'med.'
                   ,'title': 'Medicina'
                   }
               ,'uk':
                   {'short': 'мед.'
                   ,'title': 'Медицина'
                   }
               }
           ,'med., alt.':
               {'valid': False
               ,'major': True
               ,'group': 'Medicine - Alternative medicine'
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
               ,'sp':
                   {'short': 'med., alt.'
                   ,'title': 'Medicine - Alternative medicine'
                   }
               ,'uk':
                   {'short': 'мед., нетрад.'
                   ,'title': 'Медицина нетрадиційна (альтернативна)'
                   }
               }
           ,'med., epid.':
               {'valid': False
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'med., epid.'
                   ,'title': 'Epidemiology'
                   }
               ,'uk':
                   {'short': 'мед., епід.'
                   ,'title': 'Епідеміологія'
                   }
               }
           ,'med.appl.':
               {'valid': True
               ,'major': True
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'med.appl.'
                   ,'title': 'Medical appliances'
                   }
               ,'uk':
                   {'short': 'мед.тех.'
                   ,'title': 'Медична техніка'
                   }
               }
           ,'media.':
               {'valid': True
               ,'major': True
               ,'group': 'Mass media'
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
               ,'sp':
                   {'short': 'media.'
                   ,'title': 'Mass media'
                   }
               ,'uk':
                   {'short': 'ЗМІ'
                   ,'title': 'Засоби масової інформації'
                   }
               }
           ,'melior.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'melior.'
                   ,'title': 'Melioration'
                   }
               ,'uk':
                   {'short': 'меліор.'
                   ,'title': 'Меліорація'
                   }
               }
           ,'merch.nav.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'merch.nav.'
                   ,'title': 'Merchant navy'
                   }
               ,'uk':
                   {'short': 'торг.флот'
                   ,'title': 'Торгівельний флот'
                   }
               }
           ,'met.':
               {'valid': True
               ,'major': True
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'metal.'
                   ,'title': 'Metalurgia'
                   }
               ,'uk':
                   {'short': 'мет.'
                   ,'title': 'Металургія'
                   }
               }
           ,'met.health.':
               {'valid': True
               ,'major': False
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'met.health.'
                   ,'title': 'Mental health'
                   }
               ,'uk':
                   {'short': 'психогіг.'
                   ,'title': 'Психогігієна'
                   }
               }
           ,'met.sci.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'met.sci.'
                   ,'title': 'Metal science'
                   }
               ,'uk':
                   {'short': 'метзнав.'
                   ,'title': 'Металознавство'
                   }
               }
           ,'met.work.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'met.work.'
                   ,'title': 'Metalworking'
                   }
               ,'uk':
                   {'short': 'мет.обр.'
                   ,'title': 'Металообробка'
                   }
               }
           ,'meteorol.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
               ,'en':
                   {'short': 'meteorol.'
                   ,'title': 'Meteorology'
                   }
               ,'ru':
                   {'short': 'СМИ.'
                   ,'title': 'Средства массовой информации'
                   }
               ,'de':
                   {'short': 'Massenmed.'
                   ,'title': 'Massenmedien'
                   }
               ,'sp':
                   {'short': 'meteorol.'
                   ,'title': 'Meteorología'
                   }
               ,'uk':
                   {'short': 'ЗМІ'
                   ,'title': 'Засоби масової інформації'
                   }
               }
           ,'metro':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'metro'
                   ,'title': 'Metro and rapid transit'
                   }
               ,'uk':
                   {'short': 'метро.'
                   ,'title': 'Метрополітен і швидкісний транспорт'
                   }
               }
           ,'metrol.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'metrol.'
                   ,'title': 'Metrology'
                   }
               ,'uk':
                   {'short': 'метр.'
                   ,'title': 'Метрологія'
                   }
               }
           ,'mexic.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'mexic.'
                   ,'title': 'Mexican'
                   }
               ,'uk':
                   {'short': 'мекс.'
                   ,'title': 'Мексиканський вираз'
                   }
               }
           ,'microbiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'microbiol.'
                   ,'title': 'Microbiología'
                   }
               ,'uk':
                   {'short': 'мікр.'
                   ,'title': 'Мікробіологія'
                   }
               }
           ,'microel.':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'microel.'
                   ,'title': 'Microelectronics'
                   }
               ,'uk':
                   {'short': 'мікроел.'
                   ,'title': 'Мікроелектроніка'
                   }
               }
           ,'microsc.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'microsc.'
                   ,'title': 'Microscopy'
                   }
               ,'uk':
                   {'short': 'мікроск.'
                   ,'title': 'Мікроскопія'
                   }
               }
           ,'mid.chin.':
               {'valid': True
               ,'major': False
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'mid.chin.'
                   ,'title': 'Middle Chinese'
                   }
               ,'uk':
                   {'short': 'сер.кит.'
                   ,'title': 'Середньо-китайська'
                   }
               }
           ,'mil.':
               {'valid': True
               ,'major': True
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'mil., AAA':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., AAA'
                   ,'title': 'Anti-air artillery'
                   }
               ,'uk':
                   {'short': 'військ., ЗА'
                   ,'title': 'Зенітна артилерія'
                   }
               }
           ,'mil., WMD':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., WMD'
                   ,'title': 'Weapons of mass destruction'
                   }
               ,'uk':
                   {'short': 'військ., ЗМУ'
                   ,'title': 'Зброя масового ураження'
                   }
               }
           ,'mil., ammo':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., ammo'
                   ,'title': 'Ammunition'
                   }
               ,'uk':
                   {'short': 'військ., боєпр.'
                   ,'title': 'Боєприпаси'
                   }
               }
           ,'mil., arm.veh.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., arm.veh.'
                   ,'title': 'Armored vehicles'
                   }
               ,'uk':
                   {'short': 'військ., брон.'
                   ,'title': 'Бронетехніка'
                   }
               }
           ,'mil., artil.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil.,artill.'
                   ,'title': 'Artillería'
                   }
               ,'uk':
                   {'short': 'військ., арт.'
                   ,'title': 'Артилерія'
                   }
               }
           ,'mil., avia.':
               {'valid': False
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'mil., avia.'
                   ,'title': 'Military aviation'
                   }
               ,'uk':
                   {'short': 'військ., авіац.'
                   ,'title': 'Військова авіація'
                   }
               }
           ,'mil., grnd.forc.':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., grnd.forc.'
                   ,'title': 'Ground forces (Army)'
                   }
               ,'uk':
                   {'short': 'військ., сухоп.'
                   ,'title': 'Сухопутні сили'
                   }
               }
           ,'mil., lingo':
               {'valid': False
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'jerg.mil.'
                   ,'title': 'Jerga militar'
                   }
               ,'uk':
                   {'short': 'військ., жарг.'
                   ,'title': 'Військовий жаргон'
                   }
               }
           ,'mil., mil., arm.veh.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'mil., mil., arm.veh.'
                   ,'title': 'Término militar, Armored vehicles'
                   }
               ,'uk':
                   {'short': 'військ., військ., брон.'
                   ,'title': 'Військовий термін, Бронетехніка'
                   }
               }
           ,'mil., navy':
               {'valid': False
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'mil., navy'
                   ,'title': 'Navy'
                   }
               ,'uk':
                   {'short': 'військ., мор.'
                   ,'title': 'Військово-морський флот'
                   }
               }
           ,'milk.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'milk.'
                   ,'title': 'Milk production'
                   }
               ,'uk':
                   {'short': 'мол.'
                   ,'title': 'Молочне виробництво'
                   }
               }
           ,'min.class.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'min.class.'
                   ,'title': 'Mineral classification'
                   }
               ,'uk':
                   {'short': 'клас.мін.'
                   ,'title': 'Класифікація мінералів'
                   }
               }
           ,'min.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'min.proc.'
                   ,'title': 'Mineral processing'
                   }
               ,'uk':
                   {'short': 'збагач.'
                   ,'title': 'Збагачення корисних копалин'
                   }
               }
           ,'min.prod.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'min.prod.'
                   ,'title': 'Mineral products'
                   }
               ,'uk':
                   {'short': 'кор.коп.'
                   ,'title': 'Корисні копалини'
                   }
               }
           ,'mine.surv.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'mine.surv.'
                   ,'title': 'Mine surveying'
                   }
               ,'uk':
                   {'short': 'маркш.'
                   ,'title': 'Маркшейдерська справа'
                   }
               }
           ,'mineral.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'mineral.'
                   ,'title': 'Mineralogía'
                   }
               ,'uk':
                   {'short': 'мінер.'
                   ,'title': 'Мінералогія'
                   }
               }
           ,'mining.':
               {'valid': True
               ,'major': True
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'minería'
                   ,'title': 'Minería'
                   }
               ,'uk':
                   {'short': 'гірн.'
                   ,'title': 'Гірнича справа'
                   }
               }
           ,'missil.':
               {'valid': True
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'missil.'
                   ,'title': 'Missiles'
                   }
               ,'uk':
                   {'short': 'ракетн.'
                   ,'title': 'Ракетна техніка'
                   }
               }
           ,'misused':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'misused'
                   ,'title': 'Misused'
                   }
               ,'uk':
                   {'short': 'помилк.'
                   ,'title': 'Помилкове або неправильне'
                   }
               }
           ,'mob.com.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'mob.com.'
                   ,'title': 'Mobile and cellular communications'
                   }
               ,'uk':
                   {'short': 'моб.зв.'
                   ,'title': "Мобільний та стільниковий зв'язок"}}, 'modern':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'modern'
                   ,'title': 'Modern use'
                   }
               ,'uk':
                   {'short': 'сучас.'
                   ,'title': 'Сучасний вираз'
                   }
               }
           ,'mol.biol.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'mol.biol.'
                   ,'title': 'Molecular biology'
                   }
               ,'uk':
                   {'short': 'мол.біол.'
                   ,'title': 'Молекулярна біологія'
                   }
               }
           ,'moldav.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'moldav.'
                   ,'title': 'Moldavian'
                   }
               ,'uk':
                   {'short': 'молдов.'
                   ,'title': 'Молдовська мова'
                   }
               }
           ,'morph.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'morph.'
                   ,'title': 'Morphology'
                   }
               ,'uk':
                   {'short': 'морф.'
                   ,'title': 'Морфологія'
                   }
               }
           ,'moto.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'moto.'
                   ,'title': 'Motorcycles'
                   }
               ,'uk':
                   {'short': 'мото.'
                   ,'title': 'Мотоцикли'
                   }
               }
           ,'mount.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'mount.'
                   ,'title': 'Mountaineering'
                   }
               ,'uk':
                   {'short': 'альп.'
                   ,'title': 'Альпінізм'
                   }
               }
           ,'multimed.':
               {'valid': True
               ,'major': True
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'multimed.'
                   ,'title': 'Multimedia'
                   }
               ,'uk':
                   {'short': 'мультимед.'
                   ,'title': 'Мультимедіа'
                   }
               }
           ,'mun.plan.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'mun.plan.'
                   ,'title': 'Municipal planning'
                   }
               ,'uk':
                   {'short': 'міськ.забуд.'
                   ,'title': 'Міська забудова'
                   }
               }
           ,'mus.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'mús.'
                   ,'title': 'Música'
                   }
               ,'uk':
                   {'short': 'муз.'
                   ,'title': 'Музика'
                   }
               }
           ,'mus.instr.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'mus.instr.'
                   ,'title': 'Musical instruments'
                   }
               ,'uk':
                   {'short': 'муз.інстр.'
                   ,'title': 'Музичні інструменти'
                   }
               }
           ,'museum.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'museum.'
                   ,'title': 'Museums'
                   }
               ,'uk':
                   {'short': 'музейн.'
                   ,'title': 'Музеї'
                   }
               }
           ,'myth.':
               {'valid': True
               ,'major': True
               ,'group': 'Mythology'
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
               ,'sp':
                   {'short': 'mitol.'
                   ,'title': 'Mitología'
                   }
               ,'uk':
                   {'short': 'міф.'
                   ,'title': 'Міфологія'
                   }
               }
           ,'myth., gr.-rom.':
               {'valid': False
               ,'major': False
               ,'group': 'Mythology'
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
               ,'sp':
                   {'short': 'mitol.antig.'
                   ,'title': 'Mitología helénica y romana'
                   }
               ,'uk':
                   {'short': 'міф., ант.'
                   ,'title': 'Давньогрецька та давньоримська міфологія'
                   }
               }
           ,'myth., nors., myth.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'myth., nors., mitol.'
                   ,'title': 'Norse mythology, Mitología'
                   }
               ,'uk':
                   {'short': 'міф., сканд., міф.'
                   ,'title': 'Скандинавська міфологія, Міфологія'
                   }
               }
           ,'n.amer.':
               {'valid': False
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'n.amer.'
                   ,'title': 'North American (USA and Canada)'
                   }
               ,'uk':
                   {'short': 'США, Кан.'
                   ,'title': 'Північноамериканський вираз (США, Канада)'
                   }
               }
           ,'names':
               {'valid': True
               ,'major': False
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'names'
                   ,'title': 'Names and surnames'
                   }
               ,'uk':
                   {'short': 'ім.прізв.'
                   ,'title': 'Імена й прізвища'
                   }
               }
           ,'nano':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'nano'
                   ,'title': 'Nanotechnology'
                   }
               ,'uk':
                   {'short': 'нано'
                   ,'title': 'Нанотехнології'
                   }
               }
           ,'narrow.film.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'narrow.film.'
                   ,'title': 'Narrow film'
                   }
               ,'uk':
                   {'short': 'вузькопл.'
                   ,'title': 'Вузькоплівкове кіно'
                   }
               }
           ,'nat.res.':
               {'valid': True
               ,'major': True
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'nat.res.'
                   ,'title': 'Natural resourses and wildlife conservation'
                   }
               ,'uk':
                   {'short': 'прир.рес.'
                   ,'title': 'Природні ресурси та охорона природи'
                   }
               }
           ,'nat.sc.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'nat.sc.'
                   ,'title': 'Natural sciences'
                   }
               ,'uk':
                   {'short': 'прир.науки'
                   ,'title': 'Природничі науки'
                   }
               }
           ,'nautic.':
               {'valid': True
               ,'major': True
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'náut.'
                   ,'title': 'Náutico'
                   }
               ,'uk':
                   {'short': 'мор.'
                   ,'title': 'Морський термін'
                   }
               }
           ,'navig.':
               {'valid': True
               ,'major': False
               ,'group': 'Aviation'
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
               ,'sp':
                   {'short': 'navig.'
                   ,'title': 'Navigation'
                   }
               ,'uk':
                   {'short': 'нав.'
                   ,'title': 'Навігація'
                   }
               }
           ,'neol.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'neol.'
                   ,'title': 'Neologism'
                   }
               ,'uk':
                   {'short': 'неол.'
                   ,'title': 'Неологізм'
                   }
               }
           ,'nephr.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'nephr.'
                   ,'title': 'Nephrology'
                   }
               ,'uk':
                   {'short': 'нефр.'
                   ,'title': 'Нефрологія'
                   }
               }
           ,'neugoling.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'neugoling.'
                   ,'title': 'Neurolinguistics'
                   }
               ,'uk':
                   {'short': 'нейролінгв.'
                   ,'title': 'Нейролінгвістика'
                   }
               }
           ,'neur.net.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'neur.net.'
                   ,'title': 'Neural networks'
                   }
               ,'uk':
                   {'short': 'нейр.м.'
                   ,'title': 'Нейронні мережі'
                   }
               }
           ,'neurol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'neurol.'
                   ,'title': 'Neurología'
                   }
               ,'uk':
                   {'short': 'невр.'
                   ,'title': 'Неврологія'
                   }
               }
           ,'neuropsychol.':
               {'valid': True
               ,'major': False
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'neuropsychol.'
                   ,'title': 'Neuropsychology'
                   }
               ,'uk':
                   {'short': 'нейропсихол.'
                   ,'title': 'Нейропсихологія'
                   }
               }
           ,'neurosurg.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'neurosurg.'
                   ,'title': 'Neurosurgery'
                   }
               ,'uk':
                   {'short': 'нейрохір.'
                   ,'title': 'Нейрохірургія'
                   }
               }
           ,'new.zeal.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'new.zeal.'
                   ,'title': 'New Zealand'
                   }
               ,'uk':
                   {'short': 'новозел.'
                   ,'title': 'Новозеландський вираз'
                   }
               }
           ,'news':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'news'
                   ,'title': 'News style'
                   }
               ,'uk':
                   {'short': 'публіц.'
                   ,'title': 'Публіцистичний стиль'
                   }
               }
           ,'nonferr.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'nonferr.'
                   ,'title': 'Nonferrous industry'
                   }
               ,'uk':
                   {'short': 'кол.мет.'
                   ,'title': 'Кольорова металургія'
                   }
               }
           ,'nonlin.opt.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'nonlin.opt.'
                   ,'title': 'Nonlinear optics'
                   }
               ,'uk':
                   {'short': 'нелін.опт.'
                   ,'title': 'Нелінійна оптика'
                   }
               }
           ,'nonstand.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'nonstand.'
                   ,'title': 'Nonstandard'
                   }
               ,'uk':
                   {'short': 'прост.'
                   ,'title': 'Просторіччя'
                   }
               }
           ,'norw.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'norw.'
                   ,'title': 'Norway'
                   }
               ,'uk':
                   {'short': 'норв.'
                   ,'title': 'Норвезька мова'
                   }
               }
           ,'notar.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'notar.'
                   ,'title': 'Notarial practice'
                   }
               ,'uk':
                   {'short': 'нотар.'
                   ,'title': 'Нотаріальна практика'
                   }
               }
           ,'nucl.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'nucl.chem.'
                   ,'title': 'Nuclear chemistry'
                   }
               ,'uk':
                   {'short': 'яд.хім.'
                   ,'title': 'Ядерна хімія'
                   }
               }
           ,'nucl.phys.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'nucl.phys.'
                   ,'title': 'Nuclear physics'
                   }
               ,'uk':
                   {'short': 'яд.фіз.'
                   ,'title': 'Ядерна фізика'
                   }
               }
           ,'nucl.pow.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'nucl.pow.'
                   ,'title': 'Nuclear and fusion power'
                   }
               ,'uk':
                   {'short': 'атом.ен.'
                   ,'title': 'Атомна та термоядерна енергетика'
                   }
               }
           ,'numism.':
               {'valid': True
               ,'major': False
               ,'group': 'Collecting'
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
               ,'sp':
                   {'short': 'numism.'
                   ,'title': 'Numismatics'
                   }
               ,'uk':
                   {'short': 'нумізм.'
                   ,'title': 'Нумізматика'
                   }
               }
           ,'nurs.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'nurs.'
                   ,'title': 'Nursing'
                   }
               ,'uk':
                   {'short': 'сестр.'
                   ,'title': 'Сестринська справа'
                   }
               }
           ,'obs.':
               {'valid': False
               ,'major': False
               ,'group': 'Stylistic values'
               ,'en':
                   {'short': 'obs.'
                   ,'title': 'Obsolete / dated'
                   }
               ,'ru':
                   {'short': 'Gruzovik, спирт.'
                   ,'title': 'Производство спирта'
                   }
               ,'de':
                   {'short': 'veralt.'
                   ,'title': 'Veraltet'
                   }
               ,'sp':
                   {'short': 'Gruzovik, acl.'
                   ,'title': 'Alcohol distilling'
                   }
               ,'uk':
                   {'short': 'Gruzovik, спирт'
                   ,'title': 'Виробництво спирту'
                   }
               }
           ,'obs., inform.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, antic.'
                   ,'title': 'Anticuado'
                   }
               ,'uk':
                   {'short': 'Gruzovik, застар.'
                   ,'title': 'Застаріле'
                   }
               }
           ,'obs., ironic.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, retór.'
                   ,'title': 'Retórica'
                   }
               ,'uk':
                   {'short': 'Gruzovik, ритор.'
                   ,'title': 'Риторика'
                   }
               }
           ,'obs., mil.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Gruzovik, mil.'
                   ,'title': 'Término militar'
                   }
               ,'uk':
                   {'short': 'Gruzovik, військ.'
                   ,'title': 'Військовий термін'
                   }
               }
           ,'obst.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'obstetr.'
                   ,'title': 'Obstetricia'
                   }
               ,'uk':
                   {'short': 'акуш.'
                   ,'title': 'Акушерство'
                   }
               }
           ,'ocean.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'ocean.'
                   ,'title': 'Oceanography (oceanology)'
                   }
               ,'uk':
                   {'short': 'океан.'
                   ,'title': 'Океанологія (океанографія)'
                   }
               }
           ,'offic.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'offic.'
                   ,'title': 'Officialese'
                   }
               ,'uk':
                   {'short': 'канц.'
                   ,'title': 'Канцеляризм'
                   }
               }
           ,'office.equip.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'office.equip.'
                   ,'title': 'Office equipment'
                   }
               ,'uk':
                   {'short': 'орг.тех.'
                   ,'title': 'Оргтехніка'
                   }
               }
           ,'offsh.comp.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'offsh.comp.'
                   ,'title': 'Offshore companies'
                   }
               ,'uk':
                   {'short': 'офш.'
                   ,'title': 'Офшори'
                   }
               }
           ,'oil':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'petról.'
                   ,'title': 'Petróleo'
                   }
               ,'uk':
                   {'short': 'нафт.'
                   ,'title': 'Нафта'
                   }
               }
           ,'oil.lubr.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'oil.lubr.'
                   ,'title': 'Oils and lubricants'
                   }
               ,'uk':
                   {'short': 'пал.-маст.'
                   ,'title': 'Паливно-мастильні матеріали'
                   }
               }
           ,'oil.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'oil.proc.'
                   ,'title': 'Oil processing plants'
                   }
               ,'uk':
                   {'short': 'НПЗ'
                   ,'title': 'Нафтопереробні заводи'
                   }
               }
           ,'old.fash.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'old.fash.'
                   ,'title': 'Old-fashioned'
                   }
               ,'uk':
                   {'short': 'старом.'
                   ,'title': 'Старомодне (виходить з вжитку)'
                   }
               }
           ,'old.orth.':
               {'valid': True
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'old.orth.'
                   ,'title': 'Old orthography'
                   }
               ,'uk':
                   {'short': 'стар.орф.'
                   ,'title': 'Стара орфографія'
                   }
               }
           ,'oncol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'oncol.'
                   ,'title': 'Oncology'
                   }
               ,'uk':
                   {'short': 'онк.'
                   ,'title': 'Онкологія'
                   }
               }
           ,'op.hearth.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'op.hearth.'
                   ,'title': 'Open-hearth process'
                   }
               ,'uk':
                   {'short': 'мартен.'
                   ,'title': 'Мартенівське виробництво'
                   }
               }
           ,'op.syst.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'op.syst.'
                   ,'title': 'Operation systems'
                   }
               ,'uk':
                   {'short': 'оп.сист.'
                   ,'title': 'Операційні системи'
                   }
               }
           ,'ophtalm.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'oftalm.'
                   ,'title': 'Oftalmología'
                   }
               ,'uk':
                   {'short': 'офт.'
                   ,'title': 'Офтальмологія'
                   }
               }
           ,'opt.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'ópt.'
                   ,'title': 'Óptica (rama de la física)'
                   }
               ,'uk':
                   {'short': 'опт.'
                   ,'title': 'Оптика (розділ фізики)'
                   }
               }
           ,'optometr.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'optometr.'
                   ,'title': 'Optometry'
                   }
               ,'uk':
                   {'short': 'оптометр.'
                   ,'title': 'Оптометрія'
                   }
               }
           ,'ore.form.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'ore.form.'
                   ,'title': 'Ore formation'
                   }
               ,'uk':
                   {'short': 'рудн.'
                   ,'title': 'Рудні родовища'
                   }
               }
           ,'org.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'org.chem.'
                   ,'title': 'Organic chemistry'
                   }
               ,'uk':
                   {'short': 'орг.хім.'
                   ,'title': 'Органічна хімія'
                   }
               }
           ,'org.crime.':
               {'valid': True
               ,'major': False
               ,'group': 'Law enforcement'
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
               ,'sp':
                   {'short': 'org.crime.'
                   ,'title': 'Organized crime'
                   }
               ,'uk':
                   {'short': 'злочин.'
                   ,'title': 'Злочинність'
                   }
               }
           ,'org.name.':
               {'valid': True
               ,'major': False
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'org.name.'
                   ,'title': 'Name of organization'
                   }
               ,'uk':
                   {'short': 'назв.орг.'
                   ,'title': 'Назва організації'
                   }
               }
           ,'orient.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'orient.'
                   ,'title': 'Oriental'
                   }
               ,'uk':
                   {'short': 'східн.'
                   ,'title': 'Східний вираз'
                   }
               }
           ,'orthop.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'orthop.'
                   ,'title': 'Orthopedics'
                   }
               ,'uk':
                   {'short': 'ортоп.'
                   ,'title': 'Ортопедія'
                   }
               }
           ,'pack.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'pack.'
                   ,'title': 'Packaging'
                   }
               ,'uk':
                   {'short': 'пак.'
                   ,'title': 'Пакування'
                   }
               }
           ,'paint.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'pint.'
                   ,'title': 'Pintura'
                   }
               ,'uk':
                   {'short': 'живоп.'
                   ,'title': 'Живопис'
                   }
               }
           ,'paint.varn.':
               {'valid': False
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'paint.varn.'
                   ,'title': 'Paint, varnish and lacquer'
                   }
               ,'uk':
                   {'short': 'ЛФМ'
                   ,'title': 'Лакофарбові матеріали'
                   }
               }
           ,'paint.w.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'paint.w.'
                   ,'title': 'Paint work'
                   }
               ,'uk':
                   {'short': 'маляр.'
                   ,'title': 'Малярська справа'
                   }
               }
           ,'pal.bot.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'pal.bot.'
                   ,'title': 'Paleobotany'
                   }
               ,'uk':
                   {'short': 'палеобот.'
                   ,'title': 'Палеоботаніка'
                   }
               }
           ,'paleogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'paleogr.'
                   ,'title': 'Palaeography'
                   }
               ,'uk':
                   {'short': 'палеогр.'
                   ,'title': 'Палеографія'
                   }
               }
           ,'paleont.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'paleont.'
                   ,'title': 'Paleontology'
                   }
               ,'uk':
                   {'short': 'палеонт.'
                   ,'title': 'Палеонтологія'
                   }
               }
           ,'paleozool.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'paleozool.'
                   ,'title': 'Paleozoology'
                   }
               ,'uk':
                   {'short': 'палеозоол.'
                   ,'title': 'Палеозоологія'
                   }
               }
           ,'palyn.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'palyn.'
                   ,'title': 'Palynology'
                   }
               ,'uk':
                   {'short': 'палін.'
                   ,'title': 'Палінологія'
                   }
               }
           ,'parapsych.':
               {'valid': True
               ,'major': False
               ,'group': 'Parasciences'
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
               ,'sp':
                   {'short': 'parapsych.'
                   ,'title': 'Parapsychology'
                   }
               ,'uk':
                   {'short': 'парапсихол.'
                   ,'title': 'Парапсихологія'
                   }
               }
           ,'parasitol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'parasit.'
                   ,'title': 'Parasitología'
                   }
               ,'uk':
                   {'short': 'параз.'
                   ,'title': 'Паразитологія'
                   }
               }
           ,'patents.':
               {'valid': False
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'patents.'
                   ,'title': 'Patents'
                   }
               ,'uk':
                   {'short': 'юр., пат.'
                   ,'title': 'Патенти'
                   }
               }
           ,'pathol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'patol.'
                   ,'title': 'Patología'
                   }
               ,'uk':
                   {'short': 'патол.'
                   ,'title': 'Патологія'
                   }
               }
           ,'pedag.':
               {'valid': True
               ,'major': False
               ,'group': 'Education'
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
               ,'sp':
                   {'short': 'pedag.'
                   ,'title': 'Pedagogics'
                   }
               ,'uk':
                   {'short': 'педаг.'
                   ,'title': 'Педагогіка'
                   }
               }
           ,'pediatr.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'pediatr.'
                   ,'title': 'Pediatrics'
                   }
               ,'uk':
                   {'short': 'педіатр.'
                   ,'title': 'Педіатрія'
                   }
               }
           ,'pejor.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'pejor.'
                   ,'title': 'Pejorative'
                   }
               ,'uk':
                   {'short': 'приниз.'
                   ,'title': 'Принизливо'
                   }
               }
           ,'penitent.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'penitent.'
                   ,'title': 'Penitentiary system'
                   }
               ,'uk':
                   {'short': 'пенітенц.'
                   ,'title': 'Пенітенціарна система'
                   }
               }
           ,'perf.':
               {'valid': True
               ,'major': False
               ,'group': 'Wellness'
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
               ,'sp':
                   {'short': 'perf.'
                   ,'title': 'Perfume'
                   }
               ,'uk':
                   {'short': 'парф.'
                   ,'title': 'Парфумерія'
                   }
               }
           ,'permits.':
               {'valid': True
               ,'major': False
               ,'group': 'Occupational health & safety'
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
               ,'sp':
                   {'short': 'permits.'
                   ,'title': 'Permit to work system'
                   }
               ,'uk':
                   {'short': 'наряд-доп.'
                   ,'title': 'Система наряд-допусків'
                   }
               }
           ,'pers.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'pers.'
                   ,'title': 'Persa (farsi)'
                   }
               ,'uk':
                   {'short': 'перськ.'
                   ,'title': 'Перська мова'
                   }
               }
           ,'pest.contr.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'pest.contr.'
                   ,'title': 'Pest control'
                   }
               ,'uk':
                   {'short': 'шкідн.'
                   ,'title': 'Боротьба з шкідниками'
                   }
               }
           ,'pet.':
               {'valid': True
               ,'major': False
               ,'group': 'Companion animals'
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
               ,'sp':
                   {'short': 'pet.'
                   ,'title': 'Pets'
                   }
               ,'uk':
                   {'short': 'дом.твар.'
                   ,'title': 'Домашні тварини'
                   }
               }
           ,'petrogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'petrogr.'
                   ,'title': 'Petrography'
                   }
               ,'uk':
                   {'short': 'петр.'
                   ,'title': 'Петрографія'
                   }
               }
           ,'phaler.':
               {'valid': True
               ,'major': False
               ,'group': 'Collecting'
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
               ,'sp':
                   {'short': 'phaler.'
                   ,'title': 'Phaleristics'
                   }
               ,'uk':
                   {'short': 'фалер.'
                   ,'title': 'Фалеристика'
                   }
               }
           ,'pharm.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'farm.'
                   ,'title': 'Farmacología'
                   }
               ,'uk':
                   {'short': 'фарм.'
                   ,'title': 'Фармакологія'
                   }
               }
           ,'pharmac.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'pharmac.'
                   ,'title': 'Pharmacy'
                   }
               ,'uk':
                   {'short': 'фармац.'
                   ,'title': 'Фармація'
                   }
               }
           ,'philat.':
               {'valid': True
               ,'major': False
               ,'group': 'Collecting'
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
               ,'sp':
                   {'short': 'philat.'
                   ,'title': 'Philately / stamp collecting'
                   }
               ,'uk':
                   {'short': 'філат.'
                   ,'title': 'Філателія'
                   }
               }
           ,'philos.':
               {'valid': True
               ,'major': True
               ,'group': 'Philosophy'
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
               ,'sp':
                   {'short': 'filos.'
                   ,'title': 'Filosofía'
                   }
               ,'uk':
                   {'short': 'філос.'
                   ,'title': 'Філософія'
                   }
               }
           ,'phonol.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'phonol.'
                   ,'title': 'Phonology'
                   }
               ,'uk':
                   {'short': 'фонол.'
                   ,'title': 'Фонологія'
                   }
               }
           ,'photo.':
               {'valid': True
               ,'major': True
               ,'group': 'Photography'
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
               ,'sp':
                   {'short': 'fotogr.'
                   ,'title': 'Fotografía'
                   }
               ,'uk':
                   {'short': 'фото'
                   ,'title': 'Фотографія'
                   }
               }
           ,'photo.sound.rec.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'photo.sound.rec.'
                   ,'title': 'Photographical sound recording'
                   }
               ,'uk':
                   {'short': 'фот.звукоз.'
                   ,'title': 'Фотографічний звукозапис'
                   }
               }
           ,'photometr.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'photometr.'
                   ,'title': 'Photometry'
                   }
               ,'uk':
                   {'short': 'фотометр.'
                   ,'title': 'Фотометрія'
                   }
               }
           ,'phras.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'phras.'
                   ,'title': 'Phraseological unit'
                   }
               ,'uk':
                   {'short': 'фраз.'
                   ,'title': 'Фразеологізм'
                   }
               }
           ,'phys.':
               {'valid': True
               ,'major': True
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'fís.'
                   ,'title': 'Física'
                   }
               ,'uk':
                   {'short': 'фіз.'
                   ,'title': 'Фізика'
                   }
               }
           ,'phys.chem.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'phys.chem.'
                   ,'title': 'Physical chemistry'
                   }
               ,'uk':
                   {'short': 'фіз.-хім.'
                   ,'title': 'Фізична хімія'
                   }
               }
           ,'physiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'fisiol.'
                   ,'title': 'Fisiología'
                   }
               ,'uk':
                   {'short': 'фізіол.'
                   ,'title': 'Фізіологія'
                   }
               }
           ,'physioth.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'physioth.'
                   ,'title': 'Physiotherapy'
                   }
               ,'uk':
                   {'short': 'фізіотер.'
                   ,'title': 'Фізіотерапія'
                   }
               }
           ,'phytophathol.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'phytophathol.'
                   ,'title': 'Phytophathology'
                   }
               ,'uk':
                   {'short': 'фітопатол.'
                   ,'title': 'Фітопатологія'
                   }
               }
           ,'piez.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'piez.'
                   ,'title': 'Piezoelectric crystals'
                   }
               ,'uk':
                   {'short': "п'єз."
                   ,'title': "П'єзокристали"}}, 'pipes.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'pipes.'
                   ,'title': 'Pipelines'
                   }
               ,'uk':
                   {'short': 'труб.'
                   ,'title': 'Трубопроводи'
                   }
               }
           ,'plann.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'plann.'
                   ,'title': 'Planning'
                   }
               ,'uk':
                   {'short': 'план.'
                   ,'title': 'Планування'
                   }
               }
           ,'plast.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'plast.'
                   ,'title': 'Plastics'
                   }
               ,'uk':
                   {'short': 'пласт.'
                   ,'title': 'Пластмаси'
                   }
               }
           ,'plumb.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'plumb.'
                   ,'title': 'Plumbing'
                   }
               ,'uk':
                   {'short': 'сантех.'
                   ,'title': 'Сантехніка'
                   }
               }
           ,'pmp.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'pmp.'
                   ,'title': 'Pumps'
                   }
               ,'uk':
                   {'short': 'насос.'
                   ,'title': 'Насоси'
                   }
               }
           ,'pneum.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'pneum.'
                   ,'title': 'Pneumatics'
                   }
               ,'uk':
                   {'short': 'пневм.'
                   ,'title': 'Пневматичні пристрої'
                   }
               }
           ,'poetic':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'poét.'
                   ,'title': 'Poético'
                   }
               ,'uk':
                   {'short': 'поет.'
                   ,'title': 'Поетична мова'
                   }
               }
           ,'poetry':
               {'valid': True
               ,'major': False
               ,'group': 'Literature'
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
               ,'sp':
                   {'short': 'poesía'
                   ,'title': 'Poesía (terminología)'
                   }
               ,'uk':
                   {'short': 'поез.'
                   ,'title': 'Поезія (термінологія)'
                   }
               }
           ,'police':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'police'
                   ,'title': 'Police'
                   }
               ,'uk':
                   {'short': 'поліц.'
                   ,'title': 'Поліція'
                   }
               }
           ,'police.jarg.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'police.jarg.'
                   ,'title': 'Police jargon'
                   }
               ,'uk':
                   {'short': 'поліц.жарг.'
                   ,'title': 'Поліцейський жаргон'
                   }
               }
           ,'polish.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'polish.'
                   ,'title': 'Polish'
                   }
               ,'uk':
                   {'short': 'польськ.'
                   ,'title': 'Польська мова'
                   }
               }
           ,'polit.':
               {'valid': True
               ,'major': True
               ,'group': 'Politics'
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
               ,'sp':
                   {'short': 'polít.'
                   ,'title': 'Política'
                   }
               ,'uk':
                   {'short': 'політ.'
                   ,'title': 'Політика'
                   }
               }
           ,'polit.econ.':
               {'valid': True
               ,'major': False
               ,'group': 'Economy'
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
               ,'sp':
                   {'short': 'polit.econ.'
                   ,'title': 'Political economy'
                   }
               ,'uk':
                   {'short': 'політ.ек.'
                   ,'title': 'Політична економія'
                   }
               }
           ,'polite':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'polite'
                   ,'title': 'Polite'
                   }
               ,'uk':
                   {'short': 'ввічл.'
                   ,'title': 'Ввічливо'
                   }
               }
           ,'polygr.':
               {'valid': True
               ,'major': False
               ,'group': 'Publishing'
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
               ,'sp':
                   {'short': 'poligr.'
                   ,'title': 'Poligrafía'
                   }
               ,'uk':
                   {'short': 'полігр.'
                   ,'title': 'Поліграфія'
                   }
               }
           ,'polym.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'polym.'
                   ,'title': 'Polymers'
                   }
               ,'uk':
                   {'short': 'полім.'
                   ,'title': 'Полімери'
                   }
               }
           ,'polynes.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'polynes.'
                   ,'title': 'Polynesian'
                   }
               ,'uk':
                   {'short': 'полінез.'
                   ,'title': 'Полінезійський вираз'
                   }
               }
           ,'pomp.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'pomp.'
                   ,'title': 'Pompous'
                   }
               ,'uk':
                   {'short': 'високом.'
                   ,'title': 'Високомовно'
                   }
               }
           ,'port.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'port.'
                   ,'title': 'Portuguese'
                   }
               ,'uk':
                   {'short': 'португ.'
                   ,'title': 'Португальська мова'
                   }
               }
           ,'post':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'post'
                   ,'title': 'Postal service'
                   }
               ,'uk':
                   {'short': 'пошт.'
                   ,'title': 'Пошта'
                   }
               }
           ,'pow.el.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'pow.el.'
                   ,'title': 'Power electronics'
                   }
               ,'uk':
                   {'short': 'сил.ел.'
                   ,'title': 'Силова електроніка'
                   }
               }
           ,'powd.met.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'powd.met.'
                   ,'title': 'Powder metallurgy'
                   }
               ,'uk':
                   {'short': 'пор.мет.'
                   ,'title': 'Порошкова металургія'
                   }
               }
           ,'pragm.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'pragm.'
                   ,'title': 'Pragmatics'
                   }
               ,'uk':
                   {'short': 'прагм.'
                   ,'title': 'Прагматика'
                   }
               }
           ,'press.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'press.'
                   ,'title': 'Press equipment'
                   }
               ,'uk':
                   {'short': 'прес.'
                   ,'title': 'Пресове обладнання'
                   }
               }
           ,'pris.sl.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'pris.sl.'
                   ,'title': 'Prison slang'
                   }
               ,'uk':
                   {'short': "в'язн.жарг."
                   ,'title': 'В’язничний жаргон'
                   }
               }
           ,'priv.int.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'priv.int.law.'
                   ,'title': 'Private international law'
                   }
               ,'uk':
                   {'short': 'міжн.прив.пр.'
                   ,'title': 'Міжнародне приватне право'
                   }
               }
           ,'procur.':
               {'valid': True
               ,'major': False
               ,'group': 'Logistics'
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
               ,'sp':
                   {'short': 'procur.'
                   ,'title': 'Procurement'
                   }
               ,'uk':
                   {'short': 'постач.'
                   ,'title': 'Постачання'
                   }
               }
           ,'product.':
               {'valid': True
               ,'major': True
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'product.'
                   ,'title': 'Production'
                   }
               ,'uk':
                   {'short': 'вироб.'
                   ,'title': 'Виробництво'
                   }
               }
           ,'prof.jarg.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'profesion.'
                   ,'title': 'Jerga profesional'
                   }
               ,'uk':
                   {'short': 'проф.жарг.'
                   ,'title': 'Професійний жаргон'
                   }
               }
           ,'progr.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'progr.'
                   ,'title': 'Programming'
                   }
               ,'uk':
                   {'short': 'прогр.'
                   ,'title': 'Програмування'
                   }
               }
           ,'proj.manag.':
               {'valid': True
               ,'major': False
               ,'group': 'Management'
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
               ,'sp':
                   {'short': 'proj.manag.'
                   ,'title': 'Project management'
                   }
               ,'uk':
                   {'short': 'управл.проект.'
                   ,'title': 'Управління проектами'
                   }
               }
           ,'project.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'project.'
                   ,'title': 'Projectors'
                   }
               ,'uk':
                   {'short': 'проекц.'
                   ,'title': 'Проектори'
                   }
               }
           ,'prop.&figur.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'prop.&figur.'
                   ,'title': 'Proper and figurative'
                   }
               ,'uk':
                   {'short': 'прям.перен.'
                   ,'title': 'Прямий і переносний сенс'
                   }
               }
           ,'prop.name':
               {'valid': True
               ,'major': True
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'prop.name'
                   ,'title': 'Proper name'
                   }
               ,'uk':
                   {'short': 'власн.ім.'
                   ,'title': 'Власний іменник'
                   }
               }
           ,'protozool.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'protozool.'
                   ,'title': 'Protozoology'
                   }
               ,'uk':
                   {'short': 'протист.'
                   ,'title': 'Протистологія'
                   }
               }
           ,'proverb':
               {'valid': True
               ,'major': False
               ,'group': 'Folklore'
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
               ,'sp':
                   {'short': 'proverb'
                   ,'title': 'Proverb'
                   }
               ,'uk':
                   {'short': 'присл.'
                   ,'title': 'Прислів’я'
                   }
               }
           ,'psychiat.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'psiq.'
                   ,'title': 'Psiquiatría'
                   }
               ,'uk':
                   {'short': 'психіатр.'
                   ,'title': 'Психіатрія'
                   }
               }
           ,'psychol.':
               {'valid': True
               ,'major': True
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'psic.'
                   ,'title': 'Psicología'
                   }
               ,'uk':
                   {'short': 'психол.'
                   ,'title': 'Психологія'
                   }
               }
           ,'psycholing.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'psycholing.'
                   ,'title': 'Psycholinguistics'
                   }
               ,'uk':
                   {'short': 'психолінгв.'
                   ,'title': 'Психолінгвістика'
                   }
               }
           ,'psychopathol.':
               {'valid': True
               ,'major': False
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'psychopathol.'
                   ,'title': 'Psychopathology'
                   }
               ,'uk':
                   {'short': 'психопатол.'
                   ,'title': 'Психопатологія'
                   }
               }
           ,'psychophys.':
               {'valid': True
               ,'major': False
               ,'group': 'Psychology'
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
               ,'sp':
                   {'short': 'psychophys.'
                   ,'title': 'Psychophysiology'
                   }
               ,'uk':
                   {'short': 'психофіз.'
                   ,'title': 'Психофізіологія'
                   }
               }
           ,'psychother.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'psychother.'
                   ,'title': 'Psychotherapy'
                   }
               ,'uk':
                   {'short': 'психотер.'
                   ,'title': 'Психотерапія'
                   }
               }
           ,'publ.law.':
               {'valid': True
               ,'major': False
               ,'group': 'Law'
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
               ,'sp':
                   {'short': 'publ.law.'
                   ,'title': 'Public law'
                   }
               ,'uk':
                   {'short': 'публ.прав.'
                   ,'title': 'Публічне право'
                   }
               }
           ,'publ.transp.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'publ.transp.'
                   ,'title': 'Public transportation'
                   }
               ,'uk':
                   {'short': 'гром.трансп.'
                   ,'title': 'Громадський транспорт'
                   }
               }
           ,'publ.util.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'publ.util.'
                   ,'title': 'Public utilities'
                   }
               ,'uk':
                   {'short': 'комун.госп.'
                   ,'title': 'Комунальне господарство'
                   }
               }
           ,'publish.':
               {'valid': True
               ,'major': True
               ,'group': 'Publishing'
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
               ,'sp':
                   {'short': 'publish.'
                   ,'title': 'Publishing'
                   }
               ,'uk':
                   {'short': 'видавн.'
                   ,'title': 'Видавнича справа'
                   }
               }
           ,'puert.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'puert.'
                   ,'title': 'Puerto Rican Spanish'
                   }
               ,'uk':
                   {'short': 'пуерт.'
                   ,'title': 'Пуерто-риканський діалект іспанської мови'
                   }
               }
           ,'pulm.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'pulm.'
                   ,'title': 'Pulmonology'
                   }
               ,'uk':
                   {'short': 'пульм.'
                   ,'title': 'Пульмонологія'
                   }
               }
           ,'pulp.n.paper':
               {'valid': True
               ,'major': False
               ,'group': 'Wood, pulp and paper industries'
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
               ,'sp':
                   {'short': 'pulp.n.paper'
                   ,'title': 'Pulp and paper industry'
                   }
               ,'uk':
                   {'short': 'цел.папер.'
                   ,'title': 'Целюлозно-паперова промисловість'
                   }
               }
           ,'pwr.lines.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'pwr.lines.'
                   ,'title': 'Power lines'
                   }
               ,'uk':
                   {'short': 'ЛЕП'
                   ,'title': 'Лінії електропередачі'
                   }
               }
           ,'qual.cont.':
               {'valid': True
               ,'major': True
               ,'group': 'Quality control and standards'
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
               ,'sp':
                   {'short': 'qual.cont.'
                   ,'title': 'Quality control and standards'
                   }
               ,'uk':
                   {'short': 'контр.як.'
                   ,'title': 'Контроль якості та стандартизація'
                   }
               }
           ,'quant.el.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'quant.el.'
                   ,'title': 'Quantum electronics'
                   }
               ,'uk':
                   {'short': 'квант.ел.'
                   ,'title': 'Квантова електроніка'
                   }
               }
           ,'quant.mech.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'quant.mech.'
                   ,'title': 'Quantum mechanics'
                   }
               ,'uk':
                   {'short': 'квант.мех.'
                   ,'title': 'Квантова механіка'
                   }
               }
           ,'quar.':
               {'valid': True
               ,'major': False
               ,'group': 'Mining'
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
               ,'sp':
                   {'short': 'quar.'
                   ,'title': 'Quarrying'
                   }
               ,'uk':
                   {'short': "кар'єр."
                   ,'title': 'Кар’єрні роботи'
                   }
               }
           ,'quran':
               {'valid': True
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'quran'
                   ,'title': 'Quran'
                   }
               ,'uk':
                   {'short': 'коран'
                   ,'title': 'Коран'
                   }
               }
           ,'racing':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'racing'
                   ,'title': 'Racing and motorsport'
                   }
               ,'uk':
                   {'short': 'перег.'
                   ,'title': 'Перегони та автоспорт'
                   }
               }
           ,'rad.geod.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'rad.geod.'
                   ,'title': 'Radiogeodesy'
                   }
               ,'uk':
                   {'short': 'р.геод.'
                   ,'title': 'Радіогеодезія'
                   }
               }
           ,'radio':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'radio'
                   ,'title': 'Radio'
                   }
               ,'uk':
                   {'short': 'радіо'
                   ,'title': 'Радіо'
                   }
               }
           ,'radio, amer.usg., abbr.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'radio, amer., abrev.'
                   ,'title': 'Radio, Americano (uso), Abreviatura'
                   }
               ,'uk':
                   {'short': 'радіо, амер.вир., абрев.'
                   ,'title': 'Радіо, Американський вираз (не варыант мови), Абревіатура'
                   }
               }
           ,'radioastron.':
               {'valid': True
               ,'major': False
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'radioastron.'
                   ,'title': 'Radioastronomy'
                   }
               ,'uk':
                   {'short': 'радіоастр.'
                   ,'title': 'Радіоастрономія'
                   }
               }
           ,'radiobiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'radiobiol.'
                   ,'title': 'Radiobiology'
                   }
               ,'uk':
                   {'short': 'радіобіологія'
                   ,'title': 'Радіобіологія'
                   }
               }
           ,'radiogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'radiogr.'
                   ,'title': 'Radiography'
                   }
               ,'uk':
                   {'short': 'рентгр.'
                   ,'title': 'Рентгенографія'
                   }
               }
           ,'radiol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'radiol.'
                   ,'title': 'Radiología'
                   }
               ,'uk':
                   {'short': 'рентг.'
                   ,'title': 'Рентгенологія'
                   }
               }
           ,'radioloc.':
               {'valid': True
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'radioloc.'
                   ,'title': 'Radiolocation'
                   }
               ,'uk':
                   {'short': 'р.лок.'
                   ,'title': 'Радіолокація'
                   }
               }
           ,'railw.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'ferroc.'
                   ,'title': 'Ferrocarril'
                   }
               ,'uk':
                   {'short': 'залізнич.'
                   ,'title': 'Залізничний термін'
                   }
               }
           ,'rare':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'rar.'
                   ,'title': 'Raramente'
                   }
               ,'uk':
                   {'short': 'рідк.'
                   ,'title': 'Рідко'
                   }
               }
           ,'real.est.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'real.est.'
                   ,'title': 'Real estate'
                   }
               ,'uk':
                   {'short': 'нерух.'
                   ,'title': 'Нерухомість'
                   }
               }
           ,'rec.mngmt':
               {'valid': True
               ,'major': True
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'rec.mngmt'
                   ,'title': 'Records management'
                   }
               ,'uk':
                   {'short': 'діловод.'
                   ,'title': 'Діловодство'
                   }
               }
           ,'refr.mat.':
               {'valid': True
               ,'major': False
               ,'group': 'Building materials'
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
               ,'sp':
                   {'short': 'refr.mat.'
                   ,'title': 'Refractory materials'
                   }
               ,'uk':
                   {'short': 'вогнетр.'
                   ,'title': 'Вогнетривкі матеріали'
                   }
               }
           ,'refrig.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'refrig.'
                   ,'title': 'Refrigeration'
                   }
               ,'uk':
                   {'short': 'холод.'
                   ,'title': 'Холодильна техніка'
                   }
               }
           ,'reg.usg.':
               {'valid': True
               ,'major': True
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'reg.usg.'
                   ,'title': 'Regional usage (other than language varieties)'
                   }
               ,'uk':
                   {'short': 'рег.вир.'
                   ,'title': 'Регіональні вирази (не варіанти мови)'
                   }
               }
           ,'rel., budd.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel., budd.'
                   ,'title': 'Buddhism'
                   }
               ,'uk':
                   {'short': 'будд.'
                   ,'title': 'Буддизм'
                   }
               }
           ,'rel., cath.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel., cath.'
                   ,'title': 'Catholic'
                   }
               ,'uk':
                   {'short': 'католиц.'
                   ,'title': 'Католицизм'
                   }
               }
           ,'rel., christ.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel., christ.'
                   ,'title': 'Christianity'
                   }
               ,'uk':
                   {'short': 'христ.'
                   ,'title': 'Християнство'
                   }
               }
           ,'rel., east.orth.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel., east.orth.'
                   ,'title': 'Eastern Orthodoxy'
                   }
               ,'uk':
                   {'short': 'рел., правосл.'
                   ,'title': "Православ'я"}}, 'rel., hind.':
               {'valid': False
               ,'major': False
               ,'group': 'Mythology'
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
               ,'sp':
                   {'short': 'rel., hind.'
                   ,'title': 'Hinduism'
                   }
               ,'uk':
                   {'short': 'рел., інд.'
                   ,'title': 'Індуїзм'
                   }
               }
           ,'rel., islam':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel., islam'
                   ,'title': 'Islam'
                   }
               ,'uk':
                   {'short': 'іслам'
                   ,'title': 'Іслам'
                   }
               }
           ,'reliabil.':
               {'valid': True
               ,'major': False
               ,'group': 'Quality control and standards'
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
               ,'sp':
                   {'short': 'reliabil.'
                   ,'title': 'Reliability'
                   }
               ,'uk':
                   {'short': 'надійн.'
                   ,'title': 'Надійність'
                   }
               }
           ,'relig.':
               {'valid': True
               ,'major': True
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'rel.'
                   ,'title': 'Religión'
                   }
               ,'uk':
                   {'short': 'рел.'
                   ,'title': 'Релігія'
                   }
               }
           ,'rem.sens.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'rem.sens.'
                   ,'title': 'Remote sensing'
                   }
               ,'uk':
                   {'short': 'дист.зонд.'
                   ,'title': 'Дистанційне зондування Землі'
                   }
               }
           ,'reptil.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'reptil.'
                   ,'title': 'Amphibians and reptiles'
                   }
               ,'uk':
                   {'short': 'плаз.земнов.'
                   ,'title': 'Плазуни і земноводні'
                   }
               }
           ,'resin.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'resin.'
                   ,'title': 'Resins'
                   }
               ,'uk':
                   {'short': 'гумов.'
                   ,'title': 'Гумова промисловість'
                   }
               }
           ,'respect.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'respect.'
                   ,'title': 'Respectful'
                   }
               ,'uk':
                   {'short': 'шаноб.'
                   ,'title': 'Шанобливо'
                   }
               }
           ,'rhetor.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'retór.'
                   ,'title': 'Retórica'
                   }
               ,'uk':
                   {'short': 'ритор.'
                   ,'title': 'Риторика'
                   }
               }
           ,'risk.man.':
               {'valid': True
               ,'major': False
               ,'group': 'Management'
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
               ,'sp':
                   {'short': 'risk.man.'
                   ,'title': 'Risk Management'
                   }
               ,'uk':
                   {'short': 'упр.ризик.'
                   ,'title': 'Управління ризиками'
                   }
               }
           ,'rit.':
               {'valid': True
               ,'major': False
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'rit.'
                   ,'title': 'Ritual'
                   }
               ,'uk':
                   {'short': 'рит.'
                   ,'title': 'Ритуал'
                   }
               }
           ,'road.constr.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'road.constr.'
                   ,'title': 'Road construction'
                   }
               ,'uk':
                   {'short': 'дор.буд.'
                   ,'title': 'Дорожнє будівництво'
                   }
               }
           ,'road.sign.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'road.sign.'
                   ,'title': 'Road sign'
                   }
               ,'uk':
                   {'short': 'дор.зн.'
                   ,'title': 'Дорожній знак'
                   }
               }
           ,'road.surf.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'road.surf.'
                   ,'title': 'Road surface'
                   }
               ,'uk':
                   {'short': 'дор.покр.'
                   ,'title': 'Дорожне покриття'
                   }
               }
           ,'road.wrk.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'carret.'
                   ,'title': 'Obras de carreteras'
                   }
               ,'uk':
                   {'short': 'дор.спр.'
                   ,'title': 'Дорожня справа'
                   }
               }
           ,'robot.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'robot.'
                   ,'title': 'Robotics'
                   }
               ,'uk':
                   {'short': 'робот.'
                   ,'title': 'Робототехніка'
                   }
               }
           ,'roll.':
               {'valid': True
               ,'major': False
               ,'group': 'Metallurgy'
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
               ,'sp':
                   {'short': 'roll.'
                   ,'title': 'Roll stock'
                   }
               ,'uk':
                   {'short': 'вальц.'
                   ,'title': 'Вальцювання'
                   }
               }
           ,'romanian.lang.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'romanian.lang.'
                   ,'title': 'Romanian'
                   }
               ,'uk':
                   {'short': 'румун.'
                   ,'title': 'Румунська мова'
                   }
               }
           ,'rude':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'rudo'
                   ,'title': 'Rudo'
                   }
               ,'uk':
                   {'short': 'груб.'
                   ,'title': 'Грубо'
                   }
               }
           ,'rugb.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'rugb.'
                   ,'title': 'Rugby football'
                   }
               ,'uk':
                   {'short': 'регбі'
                   ,'title': 'Регбі'
                   }
               }
           ,'russ.lang.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'ruso'
                   ,'title': 'Idioma ruso'
                   }
               ,'uk':
                   {'short': 'рос.мов.'
                   ,'title': 'Російська мова'
                   }
               }
           ,'s.germ.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 's.germ.'
                   ,'title': 'South German'
                   }
               ,'uk':
                   {'short': 'півд.нім.'
                   ,'title': 'Південнонімецький вираз'
                   }
               }
           ,'sail.ships':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'sail.ships'
                   ,'title': 'Sailing ships'
                   }
               ,'uk':
                   {'short': 'вітрил.'
                   ,'title': 'Вітрильні судна'
                   }
               }
           ,'sanit.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'sanit.'
                   ,'title': 'Sanitation'
                   }
               ,'uk':
                   {'short': 'саніт.'
                   ,'title': 'Санітарія'
                   }
               }
           ,'sanscr.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'sánscr.'
                   ,'title': 'Sánscrito'
                   }
               ,'uk':
                   {'short': 'санскр.'
                   ,'title': 'Санскрит'
                   }
               }
           ,'sarcast.':
               {'valid': True
               ,'major': False
               ,'group': 'Emotional values'
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
               ,'sp':
                   {'short': 'sarcast.'
                   ,'title': 'Sarcastical'
                   }
               ,'uk':
                   {'short': 'сарк.'
                   ,'title': 'Сарказм'
                   }
               }
           ,'sat.comm.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'sat.comm.'
                   ,'title': 'Satellite communications'
                   }
               ,'uk':
                   {'short': 'супутн.зв.'
                   ,'title': 'Супутниковий зв’язок'
                   }
               }
           ,'saying.':
               {'valid': True
               ,'major': False
               ,'group': 'Folklore'
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
               ,'sp':
                   {'short': 'saying.'
                   ,'title': 'Saying'
                   }
               ,'uk':
                   {'short': 'приказ.'
                   ,'title': 'Приказка'
                   }
               }
           ,'school.sl.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'esc.'
                   ,'title': 'Escolar'
                   }
               ,'uk':
                   {'short': 'шкільн.'
                   ,'title': 'Шкільний вираз'
                   }
               }
           ,'scient.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'scient.'
                   ,'title': 'Scientific'
                   }
               ,'uk':
                   {'short': 'науков.'
                   ,'title': 'Науковий термін'
                   }
               }
           ,'scottish':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'scottish'
                   ,'title': 'Scottish (usage)'
                   }
               ,'uk':
                   {'short': 'шотл.вир.'
                   ,'title': 'Шотландський вираз'
                   }
               }
           ,'scr.':
               {'valid': True
               ,'major': False
               ,'group': 'Literature'
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
               ,'sp':
                   {'short': 'scr.'
                   ,'title': 'Screenwriting'
                   }
               ,'uk':
                   {'short': 'сцен.'
                   ,'title': 'Сценарна майстерність'
                   }
               }
           ,'scub.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'scub.'
                   ,'title': 'Scuba diving'
                   }
               ,'uk':
                   {'short': 'підв.плав.'
                   ,'title': 'Підводне плавання'
                   }
               }
           ,'sec.sys.':
               {'valid': True
               ,'major': True
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'sec.sys.'
                   ,'title': 'Security systems'
                   }
               ,'uk':
                   {'short': 'сист.безп.'
                   ,'title': 'Системи безпеки'
                   }
               }
           ,'securit.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'securit.'
                   ,'title': 'Securities'
                   }
               ,'uk':
                   {'short': 'ЦП'
                   ,'title': 'Цінні папери'
                   }
               }
           ,'seism.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'seism.'
                   ,'title': 'Seismology'
                   }
               ,'uk':
                   {'short': 'сейсм.'
                   ,'title': 'Сейсмологія'
                   }
               }
           ,'seism.res.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'seism.res.'
                   ,'title': 'Seismic resistance'
                   }
               ,'uk':
                   {'short': 'сейсм.спор.'
                   ,'title': 'Сейсмостійкість споруд'
                   }
               }
           ,'sel.breed.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'sel.breed.'
                   ,'title': 'Selective breeding'
                   }
               ,'uk':
                   {'short': 'селек.'
                   ,'title': 'Селекція'
                   }
               }
           ,'semant.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'semant.'
                   ,'title': 'Semantics'
                   }
               ,'uk':
                   {'short': 'семант.'
                   ,'title': 'Семантика'
                   }
               }
           ,'semicond.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'semicond.'
                   ,'title': 'Semiconductors'
                   }
               ,'uk':
                   {'short': 'напівпр.'
                   ,'title': 'Напівпровідники'
                   }
               }
           ,'semiot.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'semiot.'
                   ,'title': 'Semiotics'
                   }
               ,'uk':
                   {'short': 'семіот.'
                   ,'title': 'Семіотика'
                   }
               }
           ,'sens.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'sens.'
                   ,'title': 'Sensitometry'
                   }
               ,'uk':
                   {'short': 'сенсит.'
                   ,'title': 'Сенситометрія'
                   }
               }
           ,'sew.':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'sew.'
                   ,'title': 'Sewing and clothing industry'
                   }
               ,'uk':
                   {'short': 'швац.'
                   ,'title': 'Пошив одягу та швацька промисловість'
                   }
               }
           ,'sewage':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'sewage'
                   ,'title': 'Sewage and wastewater treatment'
                   }
               ,'uk':
                   {'short': 'кнлз.'
                   ,'title': 'Каналізація та очищення стічних вод'
                   }
               }
           ,'sex':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'sex'
                   ,'title': 'Sex and sexual subcultures'
                   }
               ,'uk':
                   {'short': 'секс.'
                   ,'title': 'Секс та психосексуальні субкультури'
                   }
               }
           ,'sexol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'sexol.'
                   ,'title': 'Sexology'
                   }
               ,'uk':
                   {'short': 'сексопат.'
                   ,'title': 'Сексопатологія'
                   }
               }
           ,'shinto.':
               {'valid': True
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'shinto.'
                   ,'title': 'Shinto'
                   }
               ,'uk':
                   {'short': 'синто'
                   ,'title': 'Синтоїзм'
                   }
               }
           ,'ship.handl.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'ship.handl.'
                   ,'title': 'Ship handling'
                   }
               ,'uk':
                   {'short': 'корабл.'
                   ,'title': 'Кораблеводіння'
                   }
               }
           ,'shipb.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'shipb.'
                   ,'title': 'Shipbuilding'
                   }
               ,'uk':
                   {'short': 'суднобуд.'
                   ,'title': 'Суднобудування'
                   }
               }
           ,'shoot.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'shoot.'
                   ,'title': 'Shooting sport'
                   }
               ,'uk':
                   {'short': 'стріл.сп.'
                   ,'title': 'Стрілецький спорт'
                   }
               }
           ,'show.biz.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'show.biz.'
                   ,'title': 'Show business'
                   }
               ,'uk':
                   {'short': 'шоу-біз.'
                   ,'title': 'Шоу-бізнес'
                   }
               }
           ,'signall.':
               {'valid': True
               ,'major': False
               ,'group': 'Security systems'
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
               ,'sp':
                   {'short': 'signall.'
                   ,'title': 'Signalling'
                   }
               ,'uk':
                   {'short': 'сигн.'
                   ,'title': 'Сигналізація'
                   }
               }
           ,'silic.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'silic.'
                   ,'title': 'Silicate industry'
                   }
               ,'uk':
                   {'short': 'силік.'
                   ,'title': 'Силікатна промисловість'
                   }
               }
           ,'ski.jump.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'ski.jump.'
                   ,'title': 'Ski jumping'
                   }
               ,'uk':
                   {'short': 'стриб.трампл.'
                   ,'title': 'Стрибки з трампліна'
                   }
               }
           ,'skiing':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'skiing'
                   ,'title': 'Skiing'
                   }
               ,'uk':
                   {'short': 'лиж.'
                   ,'title': 'Лижний спорт'
                   }
               }
           ,'skydive.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'skydive.'
                   ,'title': 'Skydiving'
                   }
               ,'uk':
                   {'short': 'парашут.'
                   ,'title': 'Стрибки з парашутом'
                   }
               }
           ,'sl., drug.':
               {'valid': False
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'sl., drug.'
                   ,'title': 'Drug-related slang'
                   }
               ,'uk':
                   {'short': 'нарк.жарг.'
                   ,'title': 'Жаргон наркоманів'
                   }
               }
           ,'sl., teen.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'sl., teen.'
                   ,'title': 'Teenager slang'
                   }
               ,'uk':
                   {'short': 'сл., молод.'
                   ,'title': 'Молодіжний сленг'
                   }
               }
           ,'slang':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'jerg.'
                   ,'title': 'Jerga'
                   }
               ,'uk':
                   {'short': 'сленг'
                   ,'title': 'Сленг'
                   }
               }
           ,'sms':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'sms'
                   ,'title': 'Short message service'
                   }
               ,'uk':
                   {'short': 'СМС'
                   ,'title': 'СМС'
                   }
               }
           ,'snd.proc.':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'snd.proc.'
                   ,'title': 'Digital sound processing'
                   }
               ,'uk':
                   {'short': 'оброб.зв.'
                   ,'title': 'Цифрова обробка звуку'
                   }
               }
           ,'snd.rec.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'snd.rec.'
                   ,'title': 'Sound recording'
                   }
               ,'uk':
                   {'short': 'звукозап.'
                   ,'title': 'Звукозапис'
                   }
               }
           ,'snowb.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'snowb.'
                   ,'title': 'Snowboard'
                   }
               ,'uk':
                   {'short': 'сноуб.'
                   ,'title': 'Сноуборд'
                   }
               }
           ,'soc.med.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'soc.med.'
                   ,'title': 'Social media'
                   }
               ,'uk':
                   {'short': 'соц.мер.'
                   ,'title': 'Соціальні мережі'
                   }
               }
           ,'social.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'social.'
                   ,'title': 'Socialism'
                   }
               ,'uk':
                   {'short': 'соц.'
                   ,'title': 'Соціалізм'
                   }
               }
           ,'sociol.':
               {'valid': True
               ,'major': True
               ,'group': 'Sociology'
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
               ,'sp':
                   {'short': 'sociol.'
                   ,'title': 'Sociology'
                   }
               ,'uk':
                   {'short': 'соціол.'
                   ,'title': 'Соціологія'
                   }
               }
           ,'socioling.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'socioling.'
                   ,'title': 'Sociolinguistics'
                   }
               ,'uk':
                   {'short': 'соціолінгв.'
                   ,'title': 'Соціолінгвістика'
                   }
               }
           ,'softw.':
               {'valid': True
               ,'major': False
               ,'group': 'Computing'
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
               ,'sp':
                   {'short': 'softw.'
                   ,'title': 'Software'
                   }
               ,'uk':
                   {'short': 'ПЗ'
                   ,'title': 'Програмне забезпечення'
                   }
               }
           ,'soil.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'soil.'
                   ,'title': 'Soil science'
                   }
               ,'uk':
                   {'short': 'ґрунт.'
                   ,'title': 'Ґрунтознавство'
                   }
               }
           ,'soil.mech.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'soil.mech.'
                   ,'title': 'Soil mechanics'
                   }
               ,'uk':
                   {'short': 'мех.ґр.'
                   ,'title': 'Механіка ґрунтів'
                   }
               }
           ,'sol.pow.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'sol.pow.'
                   ,'title': 'Solar power'
                   }
               ,'uk':
                   {'short': 'сон.енерг.'
                   ,'title': 'Сонячна енергетика'
                   }
               }
           ,'solid.st.phys.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'solid.st.phys.'
                   ,'title': 'Solid-state physics'
                   }
               ,'uk':
                   {'short': 'фтт.'
                   ,'title': 'Фізика твердого тіла'
                   }
               }
           ,'som.':
               {'valid': True
               ,'major': False
               ,'group': 'Medicine - Alternative medicine'
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
               ,'sp':
                   {'short': 'som.'
                   ,'title': 'Somatics'
                   }
               ,'uk':
                   {'short': 'сом.'
                   ,'title': 'Соматика'
                   }
               }
           ,'sound.eng.':
               {'valid': True
               ,'major': False
               ,'group': 'Cinematography'
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
               ,'sp':
                   {'short': 'sound.eng.'
                   ,'title': 'Sound engineering'
                   }
               ,'uk':
                   {'short': 'зв.реж.'
                   ,'title': 'Звукорежисура'
                   }
               }
           ,'south.Dutch.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'south.Dutch.'
                   ,'title': 'Southern Dutch'
                   }
               ,'uk':
                   {'short': 'півд.нід.'
                   ,'title': 'Південнонідерландський вираз'
                   }
               }
           ,'south.afr.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'south.afr.'
                   ,'title': 'South African'
                   }
               ,'uk':
                   {'short': 'півд.афр.'
                   ,'title': 'Південноафриканський вираз'
                   }
               }
           ,'soviet.':
               {'valid': True
               ,'major': False
               ,'group': 'Historical'
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
               ,'sp':
                   {'short': 'soviet.'
                   ,'title': 'Soviet'
                   }
               ,'uk':
                   {'short': 'радянськ.'
                   ,'title': 'Радянський термін або реалія'
                   }
               }
           ,'sp.dis.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'sp.dis.'
                   ,'title': 'Speech disorders'
                   }
               ,'uk':
                   {'short': 'розл.мовл.'
                   ,'title': 'Розлади мовлення'
                   }
               }
           ,'space':
               {'valid': True
               ,'major': True
               ,'group': 'Space'
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
               ,'sp':
                   {'short': 'space'
                   ,'title': 'Space'
                   }
               ,'uk':
                   {'short': 'косм.'
                   ,'title': 'Космос'
                   }
               }
           ,'span.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'esp.'
                   ,'title': 'Español'
                   }
               ,'uk':
                   {'short': 'ісп.'
                   ,'title': 'Іспанська мова'
                   }
               }
           ,'span.-am.':
               {'valid': False
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'hisp.-am.'
                   ,'title': 'Hispanoamericano'
                   }
               ,'uk':
                   {'short': 'ісп.-амер.'
                   ,'title': 'Іспано-американський жаргон'
                   }
               }
           ,'spectr.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemistry'
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
               ,'sp':
                   {'short': 'spectr.'
                   ,'title': 'Spectroscopy'
                   }
               ,'uk':
                   {'short': 'спектр.'
                   ,'title': 'Спектроскопія'
                   }
               }
           ,'speed.skat.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'speed.skat.'
                   ,'title': 'Speed skating'
                   }
               ,'uk':
                   {'short': 'ковз.'
                   ,'title': 'Ковзани'
                   }
               }
           ,'speleo.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'speleo.'
                   ,'title': 'Speleology'
                   }
               ,'uk':
                   {'short': 'спелеол.'
                   ,'title': 'Спелеологія'
                   }
               }
           ,'spice.':
               {'valid': True
               ,'major': False
               ,'group': 'Cooking'
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
               ,'sp':
                   {'short': 'spice.'
                   ,'title': 'Spices'
                   }
               ,'uk':
                   {'short': 'спеції'
                   ,'title': 'Спеції'
                   }
               }
           ,'spoken':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'spoken'
                   ,'title': 'Spoken'
                   }
               ,'uk':
                   {'short': 'усн.мов.'
                   ,'title': 'Усне мовлення'
                   }
               }
           ,'sport, bask.':
               {'valid': False
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'sport, bask.'
                   ,'title': 'Basketball'
                   }
               ,'uk':
                   {'short': 'спорт, баск.'
                   ,'title': 'Баскетбол'
                   }
               }
           ,'sport.':
               {'valid': True
               ,'major': True
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'st.exch.':
               {'valid': True
               ,'major': False
               ,'group': 'Finances'
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
               ,'sp':
                   {'short': 'burs.'
                   ,'title': 'Bursátil'
                   }
               ,'uk':
                   {'short': 'бірж.'
                   ,'title': 'Біржовий термін'
                   }
               }
           ,'starch.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'starch.'
                   ,'title': 'Starch industry'
                   }
               ,'uk':
                   {'short': 'крохм.'
                   ,'title': 'Крохмалепатокова промисловість'
                   }
               }
           ,'stat.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'estad.'
                   ,'title': 'Estadísticas'
                   }
               ,'uk':
                   {'short': 'стат.'
                   ,'title': 'Статистика'
                   }
               }
           ,'station.':
               {'valid': True
               ,'major': False
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'station.'
                   ,'title': 'Stationery'
                   }
               ,'uk':
                   {'short': 'канц.тов.'
                   ,'title': 'Канцтовари'
                   }
               }
           ,'stereo.':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'stereo.'
                   ,'title': 'Stereo'
                   }
               ,'uk':
                   {'short': 'стерео'
                   ,'title': 'Стерео'
                   }
               }
           ,'stmp.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'stmp.'
                   ,'title': 'Stamping'
                   }
               ,'uk':
                   {'short': 'штамп.'
                   ,'title': 'Штампування'
                   }
               }
           ,'stn.mas.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'stn.mas.'
                   ,'title': 'Stonemasonry'
                   }
               ,'uk':
                   {'short': 'кам.'
                   ,'title': 'Кам’яні конструкції'
                   }
               }
           ,'str.mater.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'str.mater.'
                   ,'title': 'Strength of materials'
                   }
               ,'uk':
                   {'short': 'оп.мат.'
                   ,'title': 'Опір матеріалів'
                   }
               }
           ,'strat.plast.':
               {'valid': True
               ,'major': False
               ,'group': 'Chemical industry'
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
               ,'sp':
                   {'short': 'strat.plast.'
                   ,'title': 'Stratified plastics'
                   }
               ,'uk':
                   {'short': 'шар.пласт.'
                   ,'title': 'Шаруваті пластики'
                   }
               }
           ,'stratigr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'stratigr.'
                   ,'title': 'Stratigraphy'
                   }
               ,'uk':
                   {'short': 'страт.'
                   ,'title': 'Стратиграфія'
                   }
               }
           ,'stylist.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'estilíst.'
                   ,'title': 'Estilística'
                   }
               ,'uk':
                   {'short': 'стил.'
                   ,'title': 'Стилістика'
                   }
               }
           ,'subl.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'subl.'
                   ,'title': 'Sublime'
                   }
               ,'uk':
                   {'short': 'піднес.'
                   ,'title': 'Піднесений вираз'
                   }
               }
           ,'subm.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'subm.'
                   ,'title': 'Submarines'
                   }
               ,'uk':
                   {'short': 'підвод.'
                   ,'title': 'Підводні човни'
                   }
               }
           ,'sugar.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'sugar.'
                   ,'title': 'Sugar production'
                   }
               ,'uk':
                   {'short': 'цукр.'
                   ,'title': 'Цукрове виробництво'
                   }
               }
           ,'supercond.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'supercond.'
                   ,'title': 'Superconductivity'
                   }
               ,'uk':
                   {'short': 'надпров.'
                   ,'title': 'Надпровідність'
                   }
               }
           ,'superl.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'superl.'
                   ,'title': 'Superlative'
                   }
               ,'uk':
                   {'short': 'найв.ст.'
                   ,'title': 'Найвищий ступінь'
                   }
               }
           ,'surg.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'cirug.'
                   ,'title': 'Cirugía'
                   }
               ,'uk':
                   {'short': 'хір.'
                   ,'title': 'Хірургія'
                   }
               }
           ,'surn.':
               {'valid': True
               ,'major': False
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'surn.'
                   ,'title': 'Surname'
                   }
               ,'uk':
                   {'short': 'прізвищ.'
                   ,'title': 'Прізвище'
                   }
               }
           ,'survey.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'geod.'
                   ,'title': 'Geodesia'
                   }
               ,'uk':
                   {'short': 'геод.'
                   ,'title': 'Геодезія'
                   }
               }
           ,'svc.ind.':
               {'valid': True
               ,'major': True
               ,'group': 'Service industry'
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
               ,'sp':
                   {'short': 'svc.ind.'
                   ,'title': 'Service industry'
                   }
               ,'uk':
                   {'short': 'сф.обсл.'
                   ,'title': 'Сфера обслуговування'
                   }
               }
           ,'swed.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'swed.'
                   ,'title': 'Swedish'
                   }
               ,'uk':
                   {'short': 'швед.'
                   ,'title': 'Шведська мова'
                   }
               }
           ,'swim.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'swim.'
                   ,'title': 'Swimming'
                   }
               ,'uk':
                   {'short': 'плав.'
                   ,'title': 'Плавання'
                   }
               }
           ,'swiss.':
               {'valid': True
               ,'major': False
               ,'group': 'Regional usage (other than language varieties)'
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
               ,'sp':
                   {'short': 'swiss.'
                   ,'title': 'Swiss term'
                   }
               ,'uk':
                   {'short': 'швейц.'
                   ,'title': 'Швейцарський вираз'
                   }
               }
           ,'swtch.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'swtch.'
                   ,'title': 'Switches'
                   }
               ,'uk':
                   {'short': 'вимик.'
                   ,'title': 'Вимикачі'
                   }
               }
           ,'synt.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'synt.'
                   ,'title': 'Syntax'
                   }
               ,'uk':
                   {'short': 'синт.'
                   ,'title': 'Синтаксис'
                   }
               }
           ,'tab.tenn.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'tab.tenn.'
                   ,'title': 'Table tennis'
                   }
               ,'uk':
                   {'short': 'н.тенн.'
                   ,'title': 'Настільний теніс'
                   }
               }
           ,'tabl.game':
               {'valid': True
               ,'major': False
               ,'group': 'Games (other than sports)'
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
               ,'sp':
                   {'short': 'tabl.game'
                   ,'title': 'Tabletop games'
                   }
               ,'uk':
                   {'short': 'наст.ірг.'
                   ,'title': 'Настільні ігри'
                   }
               }
           ,'taboo':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'taboo'
                   ,'title': 'Taboo expressions and obscenities'
                   }
               ,'uk':
                   {'short': 'табу.'
                   ,'title': 'Табуйована (обсценна) лексика'
                   }
               }
           ,'taboo, amer.usg., black.sl., slang':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'taboo, amer., black.sl., jerg.'
                   ,'title': 'Taboo expressions and obscenities, Americano (uso), Black slang, Jerga'
                   }
               ,'uk':
                   {'short': 'табу., амер.вир., негр., сленг'
                   ,'title': 'Табуйована (обсценна) лексика, Американський вираз (не варыант мови), Негритянський жаргон, Сленг'
                   }
               }
           ,'taiw.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'taiw.'
                   ,'title': 'Taiwan'
                   }
               ,'uk':
                   {'short': 'тайв.'
                   ,'title': 'Тайвань'
                   }
               }
           ,'tao.':
               {'valid': False
               ,'major': False
               ,'group': 'Religion'
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
               ,'sp':
                   {'short': 'tao.'
                   ,'title': 'Taoism'
                   }
               ,'uk':
                   {'short': 'даос.'
                   ,'title': 'Даосизм'
                   }
               }
           ,'tat.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'tat.'
                   ,'title': 'Tatar'
                   }
               ,'uk':
                   {'short': 'татарськ.'
                   ,'title': 'Татарська мова'
                   }
               }
           ,'taur.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'taur.'
                   ,'title': 'Tauromachy'
                   }
               ,'uk':
                   {'short': 'тавромах.'
                   ,'title': 'Тавромахія'
                   }
               }
           ,'tax.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'tax.'
                   ,'title': 'Taxes'
                   }
               ,'uk':
                   {'short': 'под.'
                   ,'title': 'Податки'
                   }
               }
           ,'tech.':
               {'valid': True
               ,'major': True
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'tec.'
                   ,'title': 'Tecnología'
                   }
               ,'uk':
                   {'short': 'техн.'
                   ,'title': 'Техніка'
                   }
               }
           ,'tecton.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'tecton.'
                   ,'title': 'Tectonics'
                   }
               ,'uk':
                   {'short': 'тект.'
                   ,'title': 'Тектоніка'
                   }
               }
           ,'tel.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'tel.'
                   ,'title': 'Telephony'
                   }
               ,'uk':
                   {'short': 'тлф.'
                   ,'title': 'Телефонія'
                   }
               }
           ,'tel.mech.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'tel.mech.'
                   ,'title': 'Telemechanics'
                   }
               ,'uk':
                   {'short': 'тлм.'
                   ,'title': 'Телемеханіка'
                   }
               }
           ,'telecom.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'telecom.'
                   ,'title': 'Telecomunicación'
                   }
               ,'uk':
                   {'short': 'телеком.'
                   ,'title': 'Телекомунікації'
                   }
               }
           ,'telegr.':
               {'valid': True
               ,'major': False
               ,'group': 'Communications'
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
               ,'sp':
                   {'short': 'telegr.'
                   ,'title': 'Telegraphy'
                   }
               ,'uk':
                   {'short': 'телегр.'
                   ,'title': 'Телеграфія'
                   }
               }
           ,'tenn.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'tenn.'
                   ,'title': 'Tennis'
                   }
               ,'uk':
                   {'short': 'теніс'
                   ,'title': 'Теніс'
                   }
               }
           ,'textile':
               {'valid': True
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'textil'
                   ,'title': 'Industria textil'
                   }
               ,'uk':
                   {'short': 'текстиль.'
                   ,'title': 'Текстиль'
                   }
               }
           ,'thai.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'thai.'
                   ,'title': 'Thai'
                   }
               ,'uk':
                   {'short': 'тайськ.'
                   ,'title': 'Тайська мова'
                   }
               }
           ,'theatre.':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'teatr.'
                   ,'title': 'Teatro'
                   }
               ,'uk':
                   {'short': 'театр.'
                   ,'title': 'Театр'
                   }
               }
           ,'therm.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'therm.'
                   ,'title': 'Thermodynamics'
                   }
               ,'uk':
                   {'short': 'терм.'
                   ,'title': 'Термодинаміка'
                   }
               }
           ,'therm.energ.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'therm.energ.'
                   ,'title': 'Thermal Energy'
                   }
               ,'uk':
                   {'short': 'тепл.енерг.'
                   ,'title': 'Теплоенергетика'
                   }
               }
           ,'therm.eng.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'therm.eng.'
                   ,'title': 'Thermal engineering'
                   }
               ,'uk':
                   {'short': 'тепл.'
                   ,'title': 'Теплотехніка'
                   }
               }
           ,'timb.float.':
               {'valid': True
               ,'major': False
               ,'group': 'Wood, pulp and paper industries'
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
               ,'sp':
                   {'short': 'timb.float.'
                   ,'title': 'Timber floating'
                   }
               ,'uk':
                   {'short': 'лісоспл.'
                   ,'title': 'Лісосплав'
                   }
               }
           ,'tin.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'tin.'
                   ,'title': 'Tinware'
                   }
               ,'uk':
                   {'short': 'бляш.вир'
                   ,'title': 'Бляшані вироби'
                   }
               }
           ,'tirk.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'tirk.'
                   ,'title': 'Turk'
                   }
               ,'uk':
                   {'short': 'тюрк.'
                   ,'title': 'Тюркські мови'
                   }
               }
           ,'titles':
               {'valid': True
               ,'major': False
               ,'group': 'Art and culture (n.e.s.)'
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
               ,'sp':
                   {'short': 'titles'
                   ,'title': 'Titles of works of art'
                   }
               ,'uk':
                   {'short': 'назв.тв.'
                   ,'title': 'Назва твору'
                   }
               }
           ,'tobac.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'tobac.'
                   ,'title': 'Tobacco industry'
                   }
               ,'uk':
                   {'short': 'тютюн.'
                   ,'title': 'Тютюнова промисловість'
                   }
               }
           ,'tools':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'tools'
                   ,'title': 'Tools'
                   }
               ,'uk':
                   {'short': 'інстр.'
                   ,'title': 'Інструменти'
                   }
               }
           ,'topogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'topogr.'
                   ,'title': 'Topografía'
                   }
               ,'uk':
                   {'short': 'топ.'
                   ,'title': 'Топографія'
                   }
               }
           ,'topol.':
               {'valid': True
               ,'major': False
               ,'group': 'Mathematics'
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
               ,'sp':
                   {'short': 'topol.'
                   ,'title': 'Topology'
                   }
               ,'uk':
                   {'short': 'топол.'
                   ,'title': 'Топологія'
                   }
               }
           ,'topon.':
               {'valid': True
               ,'major': False
               ,'group': 'Proper name'
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
               ,'sp':
                   {'short': 'topon.'
                   ,'title': 'Toponym'
                   }
               ,'uk':
                   {'short': 'топон.'
                   ,'title': 'Топонім'
                   }
               }
           ,'torped.':
               {'valid': True
               ,'major': False
               ,'group': 'Military'
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
               ,'sp':
                   {'short': 'torped.'
                   ,'title': 'Torpedoes'
                   }
               ,'uk':
                   {'short': 'торп.'
                   ,'title': 'Торпеди'
                   }
               }
           ,'toxicol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'toxicol.'
                   ,'title': 'Toxicology'
                   }
               ,'uk':
                   {'short': 'токсикол.'
                   ,'title': 'Токсикологія'
                   }
               }
           ,'toy.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'toy.'
                   ,'title': 'Toys'
                   }
               ,'uk':
                   {'short': 'іграш.'
                   ,'title': 'Іграшки'
                   }
               }
           ,'tradem.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'tradem.'
                   ,'title': 'Trademark'
                   }
               ,'uk':
                   {'short': 'фірм.зн.'
                   ,'title': 'Фірмовий знак'
                   }
               }
           ,'traf.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'traf.'
                   ,'title': 'Road traffic'
                   }
               ,'uk':
                   {'short': 'дор.рух'
                   ,'title': 'Дорожній рух'
                   }
               }
           ,'traf.contr.':
               {'valid': True
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'traf.contr.'
                   ,'title': 'Traffic control'
                   }
               ,'uk':
                   {'short': 'рег.руху'
                   ,'title': 'Регулювання руху'
                   }
               }
           ,'trampol.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'trampol.'
                   ,'title': 'Trampolining'
                   }
               ,'uk':
                   {'short': 'батут'
                   ,'title': 'Стрибки на батуті'
                   }
               }
           ,'transf.':
               {'valid': True
               ,'major': False
               ,'group': 'Electrical engineering'
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
               ,'sp':
                   {'short': 'transf.'
                   ,'title': 'Transformers'
                   }
               ,'uk':
                   {'short': 'трансф.'
                   ,'title': 'Трансформатори'
                   }
               }
           ,'transp.':
               {'valid': True
               ,'major': True
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'transp.'
                   ,'title': 'Transport'
                   }
               ,'uk':
                   {'short': 'трансп.'
                   ,'title': 'Транспорт'
                   }
               }
           ,'transpl.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'transpl.'
                   ,'title': 'Transplantology'
                   }
               ,'uk':
                   {'short': 'транспл.'
                   ,'title': 'Трансплантологія'
                   }
               }
           ,'traumat.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'traumat.'
                   ,'title': 'Traumatology'
                   }
               ,'uk':
                   {'short': 'травм.'
                   ,'title': 'Травматологія'
                   }
               }
           ,'trav.':
               {'valid': True
               ,'major': True
               ,'group': 'Travel'
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
               ,'sp':
                   {'short': 'trav.'
                   ,'title': 'Travel'
                   }
               ,'uk':
                   {'short': 'турист.'
                   ,'title': 'Туризм'
                   }
               }
           ,'trd.class.':
               {'valid': True
               ,'major': False
               ,'group': 'Business'
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
               ,'sp':
                   {'short': 'trd.class.'
                   ,'title': 'Trade classification'
                   }
               ,'uk':
                   {'short': 'квед'
                   ,'title': 'Класифікація видів економічної діяльності'
                   }
               }
           ,'trib.':
               {'valid': True
               ,'major': False
               ,'group': 'Physics'
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
               ,'sp':
                   {'short': 'trib.'
                   ,'title': 'Tribology'
                   }
               ,'uk':
                   {'short': 'трибол.'
                   ,'title': 'Трибологія'
                   }
               }
           ,'trucks':
               {'valid': False
               ,'major': False
               ,'group': 'Transport'
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
               ,'sp':
                   {'short': 'trucks'
                   ,'title': 'Trucks/Lorries'
                   }
               ,'uk':
                   {'short': 'автом., вант.'
                   ,'title': 'Вантажний транспорт'
                   }
               }
           ,'tunn.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'tunn.'
                   ,'title': 'Tunneling'
                   }
               ,'uk':
                   {'short': 'тун.буд.'
                   ,'title': 'Тунелебудування'
                   }
               }
           ,'turb.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'turb.'
                   ,'title': 'Turbines'
                   }
               ,'uk':
                   {'short': 'турб.'
                   ,'title': 'Турбіни'
                   }
               }
           ,'turkish':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'turc.'
                   ,'title': 'Turco'
                   }
               ,'uk':
                   {'short': 'тур.'
                   ,'title': 'Турецька мова'
                   }
               }
           ,'typogr.':
               {'valid': True
               ,'major': False
               ,'group': 'Publishing'
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
               ,'sp':
                   {'short': 'typogr.'
                   ,'title': 'Typography'
                   }
               ,'uk':
                   {'short': 'типогр.'
                   ,'title': 'Типографіка'
                   }
               }
           ,'typol.':
               {'valid': True
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'typol.'
                   ,'title': 'Typology'
                   }
               ,'uk':
                   {'short': 'типол.'
                   ,'title': 'Типологія'
                   }
               }
           ,'ufol.':
               {'valid': True
               ,'major': False
               ,'group': 'Parasciences'
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
               ,'sp':
                   {'short': 'ufol.'
                   ,'title': 'Ufology'
                   }
               ,'uk':
                   {'short': 'уфол.'
                   ,'title': 'Уфологія'
                   }
               }
           ,'ultrasnd.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical appliances'
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
               ,'sp':
                   {'short': 'ultrasnd.'
                   ,'title': 'Ultrasound'
                   }
               ,'uk':
                   {'short': 'ультразв.'
                   ,'title': 'Ультразвук'
                   }
               }
           ,'unions.':
               {'valid': True
               ,'major': False
               ,'group': 'Production'
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
               ,'sp':
                   {'short': 'unions.'
                   ,'title': 'Trade unions'
                   }
               ,'uk':
                   {'short': 'профс.'
                   ,'title': 'Профспілки'
                   }
               }
           ,'unit.meas.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'unit.meas.'
                   ,'title': 'Unit measures'
                   }
               ,'uk':
                   {'short': 'од.вимір.'
                   ,'title': 'Одиниці вимірювання'
                   }
               }
           ,'univer.':
               {'valid': True
               ,'major': False
               ,'group': 'Education'
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
               ,'sp':
                   {'short': 'univ.'
                   ,'title': 'Universidad'
                   }
               ,'uk':
                   {'short': 'унів.'
                   ,'title': 'Університет'
                   }
               }
           ,'urol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'urol.'
                   ,'title': 'Urology'
                   }
               ,'uk':
                   {'short': 'урол.'
                   ,'title': 'Урологія'
                   }
               }
           ,'urug.sp.':
               {'valid': True
               ,'major': False
               ,'group': 'Dialectal'
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
               ,'sp':
                   {'short': 'urug.sp.'
                   ,'title': 'Uruguayan Spanish'
                   }
               ,'uk':
                   {'short': 'уругв.'
                   ,'title': 'Уругвайський діалект іспанської мови'
                   }
               }
           ,'vac.tub.':
               {'valid': True
               ,'major': False
               ,'group': 'Electronics'
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
               ,'sp':
                   {'short': 'vac.tub.'
                   ,'title': 'Vacuum tubes'
                   }
               ,'uk':
                   {'short': 'ел.ламп.'
                   ,'title': 'Електронні лампи'
                   }
               }
           ,'valves':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'valves'
                   ,'title': 'Valves'
                   }
               ,'uk':
                   {'short': 'труб.армат.'
                   ,'title': 'Трубопровідна арматура'
                   }
               }
           ,'venereol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'venereol.'
                   ,'title': 'Venereology'
                   }
               ,'uk':
                   {'short': 'венерол.'
                   ,'title': 'Венерологія'
                   }
               }
           ,'vent.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'vent.'
                   ,'title': 'Ventilation'
                   }
               ,'uk':
                   {'short': 'вент.'
                   ,'title': 'Вентиляція'
                   }
               }
           ,'verbat.':
               {'valid': True
               ,'major': False
               ,'group': 'Subjects for Chinese dictionaries (container)'
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
               ,'sp':
                   {'short': 'verbat.'
                   ,'title': 'Verbatim'
                   }
               ,'uk':
                   {'short': 'досл.'
                   ,'title': 'Дослівно'
                   }
               }
           ,'verl.':
               {'valid': True
               ,'major': False
               ,'group': 'Jargon and slang'
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
               ,'sp':
                   {'short': 'verl.'
                   ,'title': 'Verlan'
                   }
               ,'uk':
                   {'short': 'верл.'
                   ,'title': 'Верлан'
                   }
               }
           ,'vernac.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'vernac.'
                   ,'title': 'Vernacular language'
                   }
               ,'uk':
                   {'short': 'народн.'
                   ,'title': 'Народний вираз'
                   }
               }
           ,'vet.med.':
               {'valid': True
               ,'major': False
               ,'group': 'Medical'
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
               ,'sp':
                   {'short': 'vet.'
                   ,'title': 'Medicina veterinaria'
                   }
               ,'uk':
                   {'short': 'вет.'
                   ,'title': 'Ветеринарія'
                   }
               }
           ,'vibr.monit.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'vibr.monit.'
                   ,'title': 'Vibration monitoring'
                   }
               ,'uk':
                   {'short': 'вібр.моніт.'
                   ,'title': 'Вібромоніторинг'
                   }
               }
           ,'video.':
               {'valid': True
               ,'major': False
               ,'group': 'Multimedia'
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
               ,'sp':
                   {'short': 'video.'
                   ,'title': 'Video recording'
                   }
               ,'uk':
                   {'short': 'відео'
                   ,'title': 'Відеозапис'
                   }
               }
           ,'viet.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'viet.'
                   ,'title': 'Vietnamese'
                   }
               ,'uk':
                   {'short': 'в’єтн.'
                   ,'title': 'В’єтнамська мова'
                   }
               }
           ,'virol.':
               {'valid': True
               ,'major': False
               ,'group': 'Life sciences'
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
               ,'sp':
                   {'short': 'virol.'
                   ,'title': 'Virología'
                   }
               ,'uk':
                   {'short': 'вірусол.'
                   ,'title': 'Вірусологія'
                   }
               }
           ,'volcan.':
               {'valid': True
               ,'major': False
               ,'group': 'Geology'
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
               ,'sp':
                   {'short': 'volcan.'
                   ,'title': 'Volcanology'
                   }
               ,'uk':
                   {'short': 'вулк.'
                   ,'title': 'Вулканологія'
                   }
               }
           ,'voll.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'voll.'
                   ,'title': 'Volleyball'
                   }
               ,'uk':
                   {'short': 'волейб.'
                   ,'title': 'Волейбол'
                   }
               }
           ,'vulg.':
               {'valid': True
               ,'major': False
               ,'group': 'Stylistic values'
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
               ,'sp':
                   {'short': 'vulg.'
                   ,'title': 'Vulgar'
                   }
               ,'uk':
                   {'short': 'вульг.'
                   ,'title': 'Вульгаризм'
                   }
               }
           ,'wales':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'wales'
                   ,'title': 'Wales'
                   }
               ,'uk':
                   {'short': 'уельс'
                   ,'title': 'Уельс'
                   }
               }
           ,'wareh.':
               {'valid': True
               ,'major': False
               ,'group': 'Logistics'
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
               ,'sp':
                   {'short': 'wareh.'
                   ,'title': 'Warehouse'
                   }
               ,'uk':
                   {'short': 'склад.'
                   ,'title': 'Складська справа'
                   }
               }
           ,'waste.man.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'waste.man.'
                   ,'title': 'Waste management'
                   }
               ,'uk':
                   {'short': 'утил.відх.'
                   ,'title': 'Утилізація відходів'
                   }
               }
           ,'watchm.':
               {'valid': True
               ,'major': False
               ,'group': 'Machinery and mechanisms'
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
               ,'sp':
                   {'short': 'watchm.'
                   ,'title': 'Watchmaking'
                   }
               ,'uk':
                   {'short': 'годинн.'
                   ,'title': 'Годинникарство'
                   }
               }
           ,'water.res.':
               {'valid': True
               ,'major': False
               ,'group': 'Natural resourses and wildlife conservation'
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
               ,'sp':
                   {'short': 'water.res.'
                   ,'title': 'Water resources'
                   }
               ,'uk':
                   {'short': 'вод.рес.'
                   ,'title': 'Водні ресурси'
                   }
               }
           ,'water.suppl.':
               {'valid': True
               ,'major': False
               ,'group': 'Engineering'
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
               ,'sp':
                   {'short': 'water.suppl.'
                   ,'title': 'Water supply'
                   }
               ,'uk':
                   {'short': 'водопост.'
                   ,'title': 'Водопостачання'
                   }
               }
           ,'waterski.':
               {'valid': True
               ,'major': False
               ,'group': 'Outdoor activities and extreme sports'
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
               ,'sp':
                   {'short': 'waterski.'
                   ,'title': 'Waterskiing'
                   }
               ,'uk':
                   {'short': 'вод.лиж.'
                   ,'title': 'Водні лижі'
                   }
               }
           ,'weap.':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'uk':
                   {'short': 'зброя'
                   ,'title': 'Зброя та зброярство'
                   }
               }
           ,'weightlift.':
               {'valid': True
               ,'major': False
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'weightlift.'
                   ,'title': 'Weightlifting'
                   }
               ,'uk':
                   {'short': 'в.атл.'
                   ,'title': 'Важка атлетика'
                   }
               }
           ,'weld.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'weld.'
                   ,'title': 'Welding'
                   }
               ,'uk':
                   {'short': 'звар.'
                   ,'title': 'Зварювання'
                   }
               }
           ,'welf.':
               {'valid': True
               ,'major': False
               ,'group': 'Government, administration and public services'
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
               ,'sp':
                   {'short': 'welf.'
                   ,'title': 'Welfare & Social Security'
                   }
               ,'uk':
                   {'short': 'соц.заб.'
                   ,'title': 'Соціальне забезпечення'
                   }
               }
           ,'well.contr.':
               {'valid': True
               ,'major': False
               ,'group': 'Oil and gas'
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
               ,'sp':
                   {'short': 'well.contr.'
                   ,'title': 'Well control'
                   }
               ,'uk':
                   {'short': 'упр.свердл.'
                   ,'title': 'Управління свердловиною'
                   }
               }
           ,'welln.':
               {'valid': True
               ,'major': True
               ,'group': 'Wellness'
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
               ,'sp':
                   {'short': 'welln.'
                   ,'title': 'Wellness'
                   }
               ,'uk':
                   {'short': 'крас.здор.'
                   ,'title': "Краса і здоров'я"}}, 'west.Ind.':
               {'valid': True
               ,'major': False
               ,'group': 'Countries and regions'
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
               ,'sp':
                   {'short': 'west.Ind.'
                   ,'title': 'West Indies'
                   }
               ,'uk':
                   {'short': 'кариб.'
                   ,'title': 'Карибський регіон'
                   }
               }
           ,'win.tast.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'win.tast.'
                   ,'title': 'Wine tasting'
                   }
               ,'uk':
                   {'short': 'дегуст.'
                   ,'title': 'Дегустація'
                   }
               }
           ,'wind.':
               {'valid': True
               ,'major': False
               ,'group': 'Energy industry'
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
               ,'sp':
                   {'short': 'wind.'
                   ,'title': 'Wind Energy'
                   }
               ,'uk':
                   {'short': 'вітроен.'
                   ,'title': 'Вітроенергетика'
                   }
               }
           ,'windows':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'windows'
                   ,'title': 'Windows'
                   }
               ,'uk':
                   {'short': 'вікна.'
                   ,'title': 'Вікна'
                   }
               }
           ,'wine.gr.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'wine.gr.'
                   ,'title': 'Wine growing'
                   }
               ,'uk':
                   {'short': 'вин.'
                   ,'title': 'Виноградарство'
                   }
               }
           ,'winemak.':
               {'valid': True
               ,'major': False
               ,'group': 'Food industry'
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
               ,'sp':
                   {'short': 'winemak.'
                   ,'title': 'Winemaking'
                   }
               ,'uk':
                   {'short': 'винороб.'
                   ,'title': 'Виноробство'
                   }
               }
           ,'wir.':
               {'valid': True
               ,'major': False
               ,'group': 'Construction'
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
               ,'sp':
                   {'short': 'wir.'
                   ,'title': 'Wiring'
                   }
               ,'uk':
                   {'short': 'монт.'
                   ,'title': 'Монтажна справа'
                   }
               }
           ,'wire.drw.':
               {'valid': True
               ,'major': False
               ,'group': 'Industry'
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
               ,'sp':
                   {'short': 'wire.drw.'
                   ,'title': 'Wire drawing'
                   }
               ,'uk':
                   {'short': 'волоч.'
                   ,'title': 'Волочіння'
                   }
               }
           ,'wnd.':
               {'valid': True
               ,'major': False
               ,'group': 'Technology'
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
               ,'sp':
                   {'short': 'wnd.'
                   ,'title': 'Winding'
                   }
               ,'uk':
                   {'short': 'обм.'
                   ,'title': 'Обмотки'
                   }
               }
           ,'wood.':
               {'valid': True
               ,'major': False
               ,'group': 'Wood, pulp and paper industries'
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
               ,'sp':
                   {'short': 'wood.'
                   ,'title': 'Wood processing'
                   }
               ,'uk':
                   {'short': 'дерев.'
                   ,'title': 'Деревообробка'
                   }
               }
           ,'work.fl.':
               {'valid': True
               ,'major': False
               ,'group': 'Records management'
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
               ,'sp':
                   {'short': 'work.fl.'
                   ,'title': 'Work flow'
                   }
               ,'uk':
                   {'short': 'докум.'
                   ,'title': 'Документообіг'
                   }
               }
           ,'wrest.':
               {'valid': True
               ,'major': False
               ,'group': 'Martial arts and combat sports'
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
               ,'sp':
                   {'short': 'wrest.'
                   ,'title': 'Wrestling'
                   }
               ,'uk':
                   {'short': 'бор.'
                   ,'title': 'Боротьба'
                   }
               }
           ,'yacht.':
               {'valid': True
               ,'major': False
               ,'group': 'Nautical'
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
               ,'sp':
                   {'short': 'yacht.'
                   ,'title': 'Yachting'
                   }
               ,'uk':
                   {'short': 'яхт.'
                   ,'title': 'Яхтовий спорт'
                   }
               }
           ,'yiddish.':
               {'valid': True
               ,'major': False
               ,'group': 'Languages'
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
               ,'sp':
                   {'short': 'yiddish.'
                   ,'title': 'Yiddish'
                   }
               ,'uk':
                   {'short': 'їдиш'
                   ,'title': 'Їдиш'
                   }
               }
           ,'zool.':
               {'valid': True
               ,'major': False
               ,'group': 'Biology'
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
               ,'sp':
                   {'short': 'zool.'
                   ,'title': 'Zoología'
                   }
               ,'uk':
                   {'short': 'зоол.'
                   ,'title': 'Зоологія'
                   }
               }
           ,'zoot.':
               {'valid': True
               ,'major': False
               ,'group': 'Agriculture'
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
               ,'sp':
                   {'short': 'zoot.'
                   ,'title': 'Zootechnics'
                   }
               ,'uk':
                   {'short': 'зоот.'
                   ,'title': 'Зоотехнія'
                   }
               }
           ,'Игорь Миг':
               {'valid': True
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Игорь Миг'
                   ,'title': 'General'
                   }
               ,'uk':
                   {'short': 'Игорь Миг'
                   ,'title': 'Загальна лексика'
                   }
               }
           ,'Игорь Миг, abbr.':
               {'valid': False
               ,'major': False
               ,'group': 'Grammatical labels'
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
               ,'sp':
                   {'short': 'Игорь Миг, abrev.'
                   ,'title': 'Abreviatura'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, абрев.'
                   ,'title': 'Абревіатура'
                   }
               }
           ,'Игорь Миг, calque.':
               {'valid': False
               ,'major': False
               ,'group': 'Auxilliary categories (editor use only)'
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
               ,'sp':
                   {'short': 'Игорь Миг, calque.'
                   ,'title': 'Loan translation'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, калька'
                   ,'title': 'Калька'
                   }
               }
           ,'Игорь Миг, cloth.':
               {'valid': False
               ,'major': False
               ,'group': 'Light industries'
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
               ,'sp':
                   {'short': 'Игорь Миг, cloth.'
                   ,'title': 'Clothing'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, одяг'
                   ,'title': 'Одяг'
                   }
               }
           ,'Игорь Миг, earth.sc.':
               {'valid': False
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'Игорь Миг, earth.sc.'
                   ,'title': 'Earth sciences'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, землезн.'
                   ,'title': 'Землезнавство'
                   }
               }
           ,'Игорь Миг, hydrom.':
               {'valid': False
               ,'major': False
               ,'group': 'Geography'
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
               ,'sp':
                   {'short': 'Игорь Миг, hydrom.'
                   ,'title': 'Hydrometry'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, гідром.'
                   ,'title': 'Гідрометрія'
                   }
               }
           ,'Игорь Миг, inform.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Игорь Миг, inf.'
                   ,'title': 'Informal'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, розмовн.'
                   ,'title': 'Розмовна лексика'
                   }
               }
           ,'Игорь Миг, quot.aph.':
               {'valid': False
               ,'major': False
               ,'group': 'Literature'
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
               ,'sp':
                   {'short': 'Игорь Миг, quot.aph.'
                   ,'title': 'Quotes and aphorisms'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, цит.афор.'
                   ,'title': 'Цитати, афоризми та крилаті вирази'
                   }
               }
           ,'Игорь Миг, sport.':
               {'valid': False
               ,'major': True
               ,'group': 'Sports'
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
               ,'sp':
                   {'short': 'Игорь Миг, dep.'
                   ,'title': 'Deporte'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, спорт.'
                   ,'title': 'Спорт'
                   }
               }
           ,'Игорь Миг, tagmem.':
               {'valid': False
               ,'major': False
               ,'group': 'Linguistics'
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
               ,'sp':
                   {'short': 'Игорь Миг, tagmem.'
                   ,'title': 'Tagmemics'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, тагмем.'
                   ,'title': 'Тагмеміка'
                   }
               }
           ,'Игорь Миг, weap.':
               {'valid': False
               ,'major': False
               ,'group': ''
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
               ,'sp':
                   {'short': 'Игорь Миг, weap.'
                   ,'title': 'Weapons and gunsmithing'
                   }
               ,'uk':
                   {'short': 'Игорь Миг, зброя'
                   ,'title': 'Зброя та зброярство'
                   }
               }
           }


class Groups:
    
    def __init__(self):
        self.lang = 'en'
        self.set_lang()
    
    def set_lang(self):
        f = '[MClient] plugins.multitrancom.groups.Groups.set_lang'
        result = locale.getdefaultlocale()
        if result and result[0]:
            result = result[0]
            if 'ru' in result:
                self.lang = 'ru'
            elif 'de' in result:
                self.lang = 'de'
            elif 'sp' in result:
                self.lang = 'sp'
            elif 'uk' in result:
                self.lang = 'uk'
        mes = '{} -> {}'.format(result,self.lang)
        sh.objs.get_mes(f,mes,True).show_debug()

    def _get_major_en(self,major):
        for key in SUBJECTS.keys():
            if major == SUBJECTS[key][self.lang]['title']:
                return SUBJECTS[key]['en']['title']
    
    def get_majors(self):
        # Takes ~0.0016s on Intel Atom
        majors = []
        for key in SUBJECTS.keys():
            if SUBJECTS[key]['major'] and SUBJECTS[key]['valid']:
                majors.append(SUBJECTS[key][self.lang]['title'])
        return sorted(majors)
    
    def get_group(self,major):
        # Takes ~0.002s on Intel Atom
        group = []
        major_en = self._get_major_en(major)
        if major_en:
            for key in SUBJECTS.keys():
                if major_en == SUBJECTS[key]['group'] \
                and not SUBJECTS[key]['major']:
                    group.append(SUBJECTS[key][self.lang]['title'])
        return sorted(group)
    
    def get_list(self):
        # Takes ~0.15s on Intel Atom
        f = '[MClient] plugins.multitrancom.groups.Groups.get_list'
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
                sh.objs.get_mes(f,mes,True).show_debug()
        return lst


if __name__ == '__main__':
    f = '[MClient] plugins.multitrancom.groups.__main__'
    sh.com.start()
    igroups = Groups()
    timer = sh.Timer(f)
    timer.start()
    #print(igroups.get_majors('uk'))
    #print(igroups.get_group('Біологія','uk'))
    print(igroups.get_list())
    timer.end()
    sh.com.end()
