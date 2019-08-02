#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import html
import operator
import urllib.request
import skl_shared.shared as sh

import gettext
import skl_shared.gettext_windows
skl_shared.gettext_windows.setup_env()
gettext.install('mclient','../resources/locale')

''' It seems to be highly difficult to extract abbreviation - full-title
    pairs since, unlike multitran.ru, there are no '<a title' tags, such
    cases are coded as usual URLs. Use 'Commands.missing_titles' to
    manually fill up new titles.
'''


class Pairs:
    # Determine language pairs supported by MT
    def __init__(self):
        self.values()
    
    def blacklist(self):
        ''' Read a list of URLs leading to network errors and return
            a list of pairs represented by language codes that
            cannot be used.
        '''
        f = '[MClient] plugins.multitrancom.utils.Pairs.blacklist'
        file    = '/tmp/urls'
        pattern = 'https\:\/\/www.multitran.com\/m.exe\?l1=(\d+)\&l2=(\d+)\&SHL=2\&s='
        text    = sh.ReadTextFile(file).get()
        if text:
            lst = text.splitlines()
            lst = [item.strip() for item in lst if item.strip()]
            if lst:
                codes = []
                for url in lst:
                    match = re.match(pattern,url)
                    if match:
                        code1 = int(match.group(1))
                        code2 = int(match.group(2))
                        codes.append((code1,code2))
                return codes
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def bad_gateway(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.bad_gateway'
        file    = '/tmp/urls'
        text    = sh.ReadTextFile(file).get()
        if text:
            lst = text.splitlines()
            lst = [item.strip() for item in lst if item.strip()]
            if lst:
                errors = []
                for i in range(len(lst)):
                    mes = '{}/{}'.format(i+1,len(lst))
                    sh.objs.mes(f,mes,True).info()
                    try:
                        req = urllib.request.Request (url     = lst[i]
                                                     ,data    = None
                                                     ,headers = {'User-Agent': \
                                                                 'Mozilla'
                                                                }
                                                     )
                        urllib.request.urlopen(req,timeout=12).read()
                        if self.Verbose:
                            mes = _('[OK]: "{}"').format(lst[i])
                            sh.objs.mes(f,mes,True).info()
                    except Exception as e:
                        if 'gateway' in str(e).lower():
                            errors.append(lst[i])
                if errors:
                    mes = '\n'.join(errors)
                    sh.objs.mes(f,mes,True).info()
                else:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes,True).info()
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def get_lang(self,code):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_lang'
        if isinstance(code,int):
            for lang in self._dic.keys():
                if self._dic[lang]['code'] == code:
                    return lang
        else:
            mes = _('Wrong input data: "{}"!').format(code)
            sh.objs.mes(f,mes).error()
    
    def remaining(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.remaining'
        file    = '/tmp/urls'
        pattern = 'https\:\/\/www.multitran.com\/m.exe\?l1=(\d+)\&l2=(\d+)\&SHL=2\&s='
        text    = sh.ReadTextFile(file).get()
        if text:
            lst = text.splitlines()
            lst = [item.strip() for item in lst if item.strip()]
            if lst:
                pairs = []
                for url in lst:
                    match = re.match(pattern,url)
                    if match:
                        code1 = int(match.group(1))
                        code2 = int(match.group(2))
                        if self.ispair(code1,code2):
                            lang1 = self.get_lang(code1)
                            lang2 = self.get_lang(code2)
                            if lang1 and lang2:
                                pairs.append(lang1 + ' <=> ' + lang2)
                            else:
                                sh.com.empty(f)
                if pairs:
                    mes = '\n'.join(pairs)
                    sh.objs.mes(f,mes).info()
                else:
                    mes = _('No matches!')
                    sh.objs.mes(f,mes,True).info()
            else:
                sh.com.empty(f)
        else:
            sh.com.empty(f)
    
    def get_dead(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_dead'
        dead = []
        for i in range(len(self._langs)):
            if self.isdead(i+1):
                dead.append(self._langs[i])
        self._alive = [lang for lang in self._langs if not lang in dead]
        message = _('Dead languages: {}').format(', '.join(dead))
        message += '\n'
        message += _('Languages: total: {}; alive: {}; dead: {}')
        message = message.format (len(self._langs)
                                 ,len(self._alive)
                                 ,len(dead)
                                 )
        message += '\n'
        sh.objs.mes(f,message,True).info()
        message = _('Alive languages:') + '\n' + ', '.join(self._alive)
        message += '\n\n'
        message += _('The entire dictionary:') + '\n' + str(self._dic)
        sh.objs.mes(f,message).info()
    
    def isdead(self,code1):
        f = '[MClient] plugins.multitrancom.utils.Pairs.isdead'
        url = self._deadr.format(code1)
        # We use '<=' since a language code starts with 1
        if 0 < code1 <= len(self._langs):
            code = ''
            while not code:
                code = sh.Get (url     = url
                              ,timeout = 20
                              ).run()
            if self._zero in code.replace('\n','').replace('\r',''):
                return True
        else:
            sub = '0 < {} <= {}'.format(code,len(self._alive))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).error()
    
    def fill(self):
        for i in range(len(self._langs)):
            self._dic[self._langs[i]] = {'code':i+1
                                        ,'pair':()
                                        }
    
    def get_pairs(self,lang1):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_pairs'
        if lang1:
            if lang1 in self._alive:
                lst = []
                for lang2 in self._alive:
                    if self.ispair (self._dic[lang1]['code']
                                   ,self._dic[lang2]['code']
                                   ):
                        lst.append(lang2)
                if lst:
                    lst.sort()
                    self._dic[lang1]['pair'] = tuple(lst)
                else:
                    ''' This error can be caused by network issues, so
                        we make it silent.
                    '''
                    mes = _('Language "{}" is alive but has no pairs!')
                    mes = mes.format(lang1)
                    sh.objs.mes(f,mes,True).warning()
            else:
                # We should pass only alive languages to this procedure
                mes = _('Language "{}" is dead!').format(lang1)
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.empty(f)
    
    def loop(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.loop'
        #note: Set this to the last processed language
        i = 0
        while i < len(self._alive):
            lang = self._alive[i]
            sh.objs.mes(f,lang,True).info()
            self.get_pairs(lang)
            self.write(lang)
            i += 1
    
    def write(self,lang='Last'):
        struct  = sorted(self._dic.items(),key=operator.itemgetter(0))
        message = _('Last processed language:') + ' ' + lang + '\n\n' \
                  + str(struct)
        if self._errors:
            message += '\n\n' + _('URLs that caused errors:') + '\n'
            message += '\n'.join(self._errors)
        sh.WriteTextFile (file    = self._filew
                         ,Rewrite = True
                         ).write(message)
    
    def run(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.run'
        timer = sh.Timer(f)
        timer.start()
        self.fill()
        self.loop()
        timer.end()
        self.write()
        sh.Launch(self._filew).default()
    
    def ispair(self,code1,code2):
        f = '[MClient] plugins.multitrancom.utils.Pairs.ispair'
        # We use '<=' since a language code starts with 1
        if 0 < code1 <= len(self._langs) \
        and 0 < code2 <= len(self._langs):
            if code1 == code2:
                sh.com.lazy(f)
            else:
                url  = self._root.format(code1,code2)
                '''
                code = ''
                while not code:
                    code = sh.Get(url=url).run()
                '''
                code = sh.Get (url     = url
                              ,timeout = 20
                              ).run()
                if 'Тематика' in code:
                    return True
                elif not code:
                    ''' Sometimes 'Bad Gateway' error is received which
                        can be witnessed in a browser too.
                    '''
                    self._errors.append(url)
        else:
            sub = '0 < {} <= {}, 0 < {} <= {}'.format (code1
                                                      ,len(self._langs)
                                                      ,code2
                                                      ,len(self._langs)
                                                      )
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.mes(f,mes).error()
    
    def values(self):
        self.Success = True
        self._root   = 'https://www.multitran.com/m.exe?l1={}&l2={}&SHL=2&s='
        self._deadr  = 'https://www.multitran.com/m.exe?l1={}&SHL=2&s='
        self._zero   = 'Количество терминов</a></td></tr><tr bgcolor=#DBDBDB><td>Всего</td><td></td><td align="right">0</td>'
        ''' A list of languages that have terms (and therefore pairs).
            This list is based on the output of 'self.get_dead'.
            Recreate it when necessary.
        '''
        self._alive  = (_('Abkhazian'),_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Bashkir'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Burmese'),_('Catalan'),_('Chechen'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Chuvash'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Gothic'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Ingush'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kalmyk'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Mongolian'),_('Montenegrin'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('South Ndebele'),_('Spanish'),_('Swahili'),_('Swati'),_('Swedish'),_('Tajik'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Venda'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yakut'),_('Yoruba'),_('Zulu'))
        ''' A total list of languages supported by Multitran.
            #note: Must be sorted by a language code in an ascending
            order.
        '''
        self._langs  = (_('English'),_('Russian'),_('German'),_('French'),_('Spanish'),_('Hebrew'),_('Serbian'),_('Croatian'),_('Tatar'),_('Arabic'),_('Portuguese'),_('Lithuanian'),_('Romanian'),_('Polish'),_('Bulgarian'),_('Czech'),_('Chinese'),_('Hindi'),_('Bengali'),_('Punjabi'),_('Vietnamese'),_('Danish'),_('Italian'),_('Dutch'),_('Azerbaijani'),_('Estonian'),_('Latvian'),_('Japanese'),_('Swedish'),_('Norwegian Bokmal'),_('Afrikaans'),_('Turkish'),_('Ukrainian'),_('Esperanto'),_('Kalmyk'),_('Finnish'),_('Latin'),_('Greek'),_('Korean'),_('Georgian'),_('Armenian'),_('Hungarian'),_('Kazakh'),_('Kirghiz'),_('Uzbek'),_('Romany'),_('Albanian'),_('Welsh'),_('Irish'),_('Icelandic'),_('Kurdish'),_('Persian'),_('Catalan'),_('Corsican'),_('Galician'),_('Mirandese'),_('Romansh'),_('Belarusian'),_('Ruthene'),_('Slovak'),_('Upper Sorbian'),_('Lower Sorbian'),_('Bosnian'),_('Montenegrin'),_('Macedonian'),_('Church Slavonic'),_('Slovenian'),_('Basque'),_('Svan'),_('Mingrelian'),_('Abkhazian'),_('Adyghe'),_('Chechen'),_('Avar'),_('Ingush'),_('Crimean Tatar'),_('Chuvash'),_('Maltese'),_('Khmer'),_('Nepali'),_('Amharic'),_('Assamese'),_('Lao'),_('Asturian'),_('Odia'),_('Indonesian'),_('Pashto'),_('Quechua'),_('Maori'),_('Marathi'),_('Tamil'),_('Telugu'),_('Thai'),_('Turkmen'),_('Yoruba'),_('Bosnian cyrillic'),_('Chinese simplified'),_('Chinese Taiwan'),_('Filipino'),_('Gujarati'),_('Hausa'),_('Igbo'),_('Inuktitut'),_('IsiXhosa'),_('Zulu'),_('Kannada'),_('Kinyarwanda'),_('Swahili'),_('Konkani'),_('Luxembourgish'),_('Malayalam'),_('Wolof'),_('Wayuu'),_('Serbian latin'),_('Tswana'),_('Sinhala'),_('Urdu'),_('Sesotho sa leboa'),_('Norwegian Nynorsk'),_('Malay'),_('Mongolian'),_('Frisian'),_('Faroese'),_('Friulian'),_('Ladin'),_('Sardinian'),_('Occitan'),_('Gaulish'),_('Gallegan'),_('Sami'),_('Breton'),_('Cornish'),_('Manh'),_('Scottish Gaelic'),_('Yiddish'),_('Tajik'),_('Tagalog'),_('Soninke'),_('Baoulé'),_('Javanese'),_('Wayana'),_('French Guiana Creole'),_('Mauritian Creole'),_('Seychellois Creole'),_('Guadeloupe Creole'),_('Rodriguan Creole'),_('Haitian Creole'),_('Mandinka'),_('Surigaonon'),_('Adangme'),_('Tok Pisin'),_('Cameroonian Creole'),_('Suriname Creole'),_('Belizean Creole'),_('Virgin Islands Creole'),_('Fon'),_('Kim'),_('Ivatan'),_('Gen'),_('Marshallese'),_('Wallisian'),_('Old Prussian'),_('Yom'),_('Tokelauan'),_('Zande'),_('Yao'),_('Waray'),_('Walmajarri'),_('Visayan'),_('Vili'),_('Venda'),_('Achinese'),_('Adjukru'),_('Agutaynen'),_('Afar'),_('Acoli'),_('Afrihili'),_('Ainu'),_('Akan'),_('Akkadian'),_('Aleut'),_('Southern Altai'),_('Old English'),_('Angika'),_('Official Aramaic'),_('Aragonese'),_('Mapudungun'),_('Arapaho'),_('Arawak'),_('Avestan'),_('Awadhi'),_('Aymara'),_('Bashkir'),_('Baluchi'),_('Bambara'),_('Balinese'),_('Basaa'),_('Beja'),_('Bemba'),_('Bhojpuri'),_('Bikol'),_('Bini'),_('Bislama'),_('Siksika'),_('Tibetan'),_('Braj'),_('Buriat'),_('Buginese'),_('Burmese'),_('Bilin'),_('Caddo'),_('Galibi Carib'),_('Cebuano'),_('Chamorro'),_('Chibcha'),_('Chagatai'),_('Chuukese'),_('Mari'),_('Chinook jargon'),_('Choctaw'),_('Chipewyan'),_('Cherokee'),_('Cheyenne'),_('Coptic'),_('Cree'),_('Kashubian'),_('Dakota'),_('Dargwa'),_('Delaware'),_('Slave'),_('Dogrib'),_('Dinka'),_('Dhivehi'),_('Dogri'),_('Duala'),_('Middle Dutch'),_('Dyula'),_('Dzongkha'),_('Efik'),_('Egyptian'),_('Ekajuk'),_('Elamite'),_('Middle English'),_('Ewe'),_('Ewondo'),_('Fang'),_('Fanti'),_('Fijian'),_('Middle French'),_('Old French'),_('Eastern Frisian'),_('Fulah'),_('Ga'),_('Gayo'),_('Gbaya'),_('Ge\'ez'),_('Gilbertese'),_('Middle High German'),_('Old High German'),_('Gondi'),_('Gorontalo'),_('Gothic'),_('Grebo'),_('Ancient Greek'),_('Guarani'),_('Swiss German'),_('Gwichʼin'),_('Haida'),_('Kikuyu'),_('Hawaiian'),_('Herero'),_('Hiligaynon'),_('Hittite'),_('Hmong'),_('Hiri Motu'),_('Hupa'),_('Iban'),_('Ido'),_('Sichuan Yi'),_('Interlingue'),_('Ilocano'),_('Interlingua'),_('Inupiaq'),_('Lojban'),_('Judeo-Persian'),_('Judeo-Arabic'),_('Kara-Kalpak'),_('Kabyle'),_('Kachin'),_('Kalaallisut'),_('Kamba'),_('Kashmiri'),_('Kanuri'),_('Kawi'),_('Kabardian'),_('Khasi'),_('Khotanese'),_('Kimbundu'),_('Komi'),_('Kongo'),_('Kosraean'),_('Kpelle'),_('Karachay-Balkar'),_('Karelian'),_('Kurukh'),_('Kuanyama'),_('Kumyk'),_('Kutenai'),_('Lahnda'),_('Lamba'),_('Lezghian'),_('Limburgan'),_('Lingala'),_('Mongo'),_('Lozi'),_('Luba-Lulua'),_('Luba-Katanga'),_('Ganda'),_('Luiseno'),_('Lunda'),_('Luo'),_('Lushai'),_('Madurese'),_('Magahi'),_('Maithili'),_('Makasar'),_('Masai'),_('Moksha'),_('Mandar'),_('Mende'),_('Middle Irish'),_('Mi\'kmaq'),_('Minangkabau'),_('Malagasy'),_('Manchu'),_('Manipuri'),_('Mohawk'),_('Mossi'),_('Creek'),_('Marwari'),_('Erzya'),_('Neapolitan'),_('Nauru'),_('Navajo'),_('South Ndebele'),_('North Ndebele'),_('Ndonga'),_('Low German'),_('Nepal Bhasa'),_('Nias'),_('Niuean'),_('Nogai'),_('Old Norse'),_('Sandawe'),_('N\'Ko'),_('Classical Newari'),_('Nyanja'),_('Nyamwezi'),_('Nyankole'),_('Nyoro'),_('Nzima'),_('Ojibwa'),_('Oromo'),_('Osage'),_('Ossetian'),_('Ottoman Turkish'),_('Pangasinan'),_('Pahlavi'),_('Pampanga'),_('Papiamento'),_('Palauan'),_('Old Persian'),_('Phoenician'),_('Pali'),_('Pohnpeian'),_('Old Occitan'),_('Rajasthani'),_('Rapanui'),_('Rarotongan'),_('Reunionese'),_('Rundi'),_('Macedo-Romanian'),_('Sango'),_('Yakut'),_('Samaritan Aramaic'),_('Sanskrit'),_('Sasak'),_('Sicilian'),_('Scots'),_('Selkup'),_('Old Irish'),_('Shan'),_('Sidamo'),_('Southern Sami'),_('Northern Sami'),_('Lule Sami'),_('Inari Sami'),_('Samoan'),_('Skolt Sami'),_('Shona'),_('Sindhi'),_('Sogdian'),_('Somali'),_('Sesotho'),_('Sranan Tongo'),_('Serer'),_('Swati'),_('Sukuma'),_('Sundanese'),_('Susu'),_('Sumerian'),_('Santali'),_('Syriac'),_('Tahitian'),_('Timne'),_('Tonga'),_('Tetum'),_('Tigre'),_('Tigrinya'),_('Tiv'),_('Shilluk'),_('Klingon'),_('Tlingit'),_('Tamashek'),_('Carolinian'),_('Portuguese creole'),_('Tuamotuan'),_('Numèè'),_('Gela'),_('Comorian'),_('Rennellese'),_('Emilian-Romagnol'),_('Mayan'),_('Caribbean Hindustani'),_('Khakas'),_('Kinga'),_('Kurmanji'),_('Kwangali'),_('Lango'),_('Ligurian'),_('Lombard'),_('Luguru'),_('Mamasa'),_('Mashi'),_('Meru'),_('Rotokas'),_('Moldovan'),_('Mongolian script'),_('Nasioi'),_('Nyakyusa'),_('Piedmontese'),_('Pinyin'),_('Sangu'),_('Shambala'),_('Shor'),_('Central Atlas Tamazight'),_('Thai Transliteration'),_('Tsonga'),_('Tuvan'),_('Valencian'),_('Venetian'),_('Walloon'),_('Wanji'),_('Zigula'),_('Korean Transliteration'),_('Mongolian Transliteration'),_('Assyrian'),_('Kaguru'),_('Kimakonde'),_('Kirufiji'),_('Mbwera'),_('Gronings'),_('Hadza'),_('Iraqw'),_('Kami'),_('Krio'),_('Tweants'),_('Abaza'))
        self._filew  = '/home/pete/tmp/ars/pairs'
        self._dic    = {}
        self._errors = []



class Topics:
    
    def __init__(self,url='https://www.multitran.com/m.exe?a=112&l1=1&l2=2'):
        self.values()
        self._url = url
        
    def values(self):
        self.Success = True
        self._html   = ''
        self._titles = []
        self._abbrs  = []
        
    def run(self):
        self.get_html()
        self.tags()
        
    def get_html(self):
        f = '[MClient] plugins.multitrancom.utils.Topics.get_html'
        if self.Success:
            self._html = sh.Get (url      = self._url
                                ,encoding = 'utf-8'
                                ).run()
            if self._html:
                self._html = self._html.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
                          
    def tags(self):
        f = '[MClient] plugins.multitrancom.utils.Topics.tags'
        if self.Success:
            tags = Tags (text   = self._html
                        ,search = 'href="/m.exe?a='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                #cur
                tags._urls = [tags._urls[0]]
                for i in range(len(tags._urls)):
                    abbr = Abbr (url   = tags._urls[i]
                                ,title = tags._titles[i]
                                )
                    abbr.run()
                    if len(abbr._titles) == len(abbr._abbrs):
                        for i in range(len(abbr._abbrs)):
                            if not abbr._abbrs[i] in self._abbrs:
                                self._abbrs.append(abbr._abbrs[i])
                                self._titles.append(abbr._titles[i])
                    else:
                        #todo: Should we toggle 'self.Success' here?
                        #self.Success = False
                        sub = '{} == {}'.format (len(abbr._titles)
                                                ,len(abbr._abbrs)
                                                )
                        mes = _('The condition "{}" is not observed!')
                        mes = mes.format(sub)
                        sh.objs.mes(f,mes).warning()
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)



class Abbr:
    
    def __init__(self,url,title):
        f = '[MClient] plugins.multitrancom.utils.Abbr.__init__'
        self.values()
        self._url   = url
        self._title = title
        if self._url and self._title:
            self.Success = True
        else:
            self.Success = False
            sh.com.empty(f)
                          
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.debug'
        if self.Success:
            text = ''
            for i in range(len(self._abbrs)):
                text += '%d: "%s": "%s"\n' % (i,self._titles[i]
                                             ,self._abbrs[i]
                                             )
            return text
        else:
            sh.com.cancel(f)
    
    def values(self):
        self._html   = ''
        self._html2  = ''
        self._url2   = ''
        self._titles = []
        self._abbrs  = []
                          
    def get(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.get'
        if self.Success:
            self._html = sh.Get (url      = self._url
                                ,encoding = 'utf-8'
                                ).run()
            if self._html:
                self._html = self._html.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def get2(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.get2'
        if self.Success:
            self._html2 = sh.Get (url      = self._url2
                                 ,encoding = 'utf-8'
                                 ).run()
            if self._html2:
                self._html2 = self._html2.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def tags(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.tags'
        if self.Success:
            tags = Tags (text   = self._html
                        ,search = 'href="/m.exe?a='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                if tags._urls and tags._urls[0]:
                    ''' #todo: try all URLs instead of the 1st one
                        (a Multitran's bug: some links may lead to
                        different dictionary titles).
                    '''
                    self._url2 = tags._urls[0]
                    ''' Avoid a Multitran's bug: the site generates URLs
                        with tabs, which cannot be downloaded. However,
                        those URLs work fine if tabs are deleted.
                    '''
                    self._url2 = self._url2.replace('\t','')
                else:
                    sh.com.empty(f)
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)
    
    def tags2(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.tags2'
        if self.Success:
            ''' Replace this so that 'Tags' would not treat this as
                a new tag.
            '''
            self._html2 = self._html2.replace('<i>','')
            tags = Tags (text   = self._html2
                        ,search = '<a title="'
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                self._titles = tags._urls
                self._abbrs  = tags._titles
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)
    
    def titles(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.titles'
        if self.Success:
            for i in range(len(self._titles)):
                if self._titles[i]:
                    self._titles[i] = self._titles[i].replace('<a title="','')
                    pos = sh.Search (text   = self._titles[i]
                                    ,search = '" href'
                                    ).next()
                    pos = sh.Input (title = f
                                   ,value = pos
                                   ).integer()
                    self._titles[i] = self._titles[i][:pos]
                    self._titles[i] = self._titles[i].strip()
                else:
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)
    
    def abbrs(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.abbrs'
        if self.Success:
            for i in range(len(self._abbrs)):
                self._abbrs[i] = self._abbrs[i].replace('<i>','').replace('</i>','')
                self._abbrs[i] = self._abbrs[i].strip()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get()
        self.tags()
        self.get2()
        self.tags2()
        self.titles()
        self.abbrs()



class Tags:
    
    def __init__(self,text,search='href="/m.exe?a='):
        f = '[MClient] plugins.multitrancom.utils.Tags.__init__'
        self.values()
        self.text   = text
        self.search = search
        if not self.text:
            self.Success = False
            sh.com.empty(f)
        
    def values(self):
        self.Success = True
        self._tags   = []
        self._titles = []
        self._urls   = []
        self._start  = []
        self._end    = []
        
    def equalize(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.equalize'
        if self.Success:
            if len(self._end) > len(self._start):
                tmp = []
                for i in range(len(self._start)):
                    while self._start[i] > self._end[i]:
                        del self._end[i]
                    tmp.append(self._end[i])
                self._end = tmp
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.split'
        if self.Success:
            self._start = sh.Search (text   = self.text
                                    ,search = self.search
                                    ).next_loop()
            self._end = sh.Search (text   = self.text
                                  ,search = '</a>'
                                  ).next_loop()
            self.equalize()
            if len(self._start) == len(self._end):
                for i in range(len(self._start)):
                    self._tags.append(self.text[self._start[i]:self._end[i]])
            else:
                self.Success = False
                sub = '{} == {}'.format (len(self._start)
                                        ,len(self._end)
                                        )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.mes(f,mes).warning()
            mes = _('{} tags have been extracted')
            mes = mes.format(len(self._tags))
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
                          
    def loop_trash(self,url):
        trash = ('m.exe?a=40pl'
                ,'m.exe?a=40&pl'
                ,'m.exe?a=256'
                )
        for item in trash:
            if item in url:
                return True
    
    def trash_urls(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.trash_urls'
        if self.Success:
            self._urls = [url for url in self._urls \
                          if not self.loop_trash(url)
                         ]
            for i in range(len(self._urls)):
                if self._urls[i]:
                    self._urls[i] = self._urls[i].replace('<a href="/m.exe?','https://www.multitran.com/m.exe?')
                    if self._urls[i].endswith('"'):
                        self._urls[i] = self._urls[i][:-1]
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(self._urls[i])
                        sh.objs.mes(f,mes,True).warning()
                else:
                    sh.com.empty(f)
        else:
            sh.com.cancel(f)

    def trash_titles(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.trash_titles'
        if self.Success:
            for i in range(len(self._titles)):
                self._titles[i] = html.unescape(self._titles[i])
        else:
            sh.com.cancel(f)
    
    def links(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.links'
        if self.Success:
            if self._tags:
                for tag in self._tags:
                    pos = sh.Search (text   = tag
                                    ,search = '>'
                                    ).next()
                    pos = sh.Input (title = 'Tags.links'
                                   ,value = pos
                                   ).integer()
                    self._urls.append(tag[:pos])
                    self._titles.append(tag[pos+1:])
            else:
                sh.com.empty(f)
            self._urls = [url.replace(' ','%20') for url in self._urls]
            self._urls = [url.replace('href="/m.exe?','https://www.multitran.com/m.exe?') for url in self._urls]
            mes = _('{} URLs have been extracted')
            mes = mes.format(len(self._urls))
            sh.objs.mes(f,mes,True).debug()
            mes = _('{} titles have been extracted')
            mes = mes.format(len(self._titles))
            sh.objs.mes(f,mes,True).debug()
        else:
            sh.com.cancel(f)
        
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.debug'
        if self.Success:
            text = ''
            for i in range(len(self._urls)):
                text += '{}: "{}": "{}"\n'.format (i,self._urls[i]
                                                  ,self._titles[i]
                                                  )
            return text
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.split()
        self.links()
        self.trash_urls()
        self.trash_titles()



class Commands:
    
    def format_gettext(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.format_gettext'
        text = sh.Clipboard().paste()
        if text:
            text = text.replace("('",'')
            text = text.replace("')",'')
            text = text.replace("', '",',')
            lst  = text.split(',')
            lst  = ["_('" + item.strip() + "')" for item in lst \
                    if item.strip()
                   ]
            text = '(' + ','.join(lst) + ')'
            sh.Clipboard().copy(text)
            input(_('Press any key to continue.'))
        else:
            sh.com.empty(f)
    
    # Transform new-line-delimited text into a list of languages
    def format_pairs(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.format_pairs'
        text = sh.Clipboard().paste()
        if text:
            text= text.replace(r"'",r"\'")
            lst = text.splitlines()
            lst  = ["_('" + item.strip() + "')" for item in lst \
                    if item.strip()
                   ]
            text = '(' + ','.join(lst) + ')'
            sh.Clipboard().copy(text)
            input(_('Press any key to continue.'))
        else:
            sh.com.empty(f)
    
    # Compare dictionary abbreviations for different languages
    def new_abbrs(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.new_abbrs'
        file1 = '/tmp/abbr.txt'
        file2 = '/tmp/abbr2.txt'
        dic1  = sh.Dic(file=file1)
        dic1.get()
        dic2  = sh.Dic(file=file2)
        dic2.get()
        if dic1.Success and dic2.Success:
            missing = []
            for i in range(len(dic2.orig)):
                if dic2.orig[i] not in dic1.orig:
                    missing.append(dic2.orig[i] + '\t' + dic2.transl[i])
            if missing:
                mes = '\n'.join(missing)
                sh.objs.mes(f,mes).info()
            else:
                sh.com.lazy(f)
        else:
            sh.com.cancel(f)
    
    # Compare dictionary topics for different languages
    def compare_topics(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.compare_topics'
        file1 = '/tmp/topics'
        file2 = '/tmp/topics2'
        text1 = sh.ReadTextFile(file=file1).get()
        text2 = sh.ReadTextFile(file=file2).get()
        if text1 and text2:
            text1 = text1.splitlines()
            text2 = text2.splitlines()
            missing = [item for item in text2 if item not in text1]
            if missing:
                mes = '\n'.join(missing)
                sh.objs.mes(f,mes).info()
            else:
                sh.com.lazy(f)
        else:
            sh.com.empty(f)
    
    def get_abbrs(self):
        ''' #NOTE: Will NOT work (titles are indistinguishable
            from other URLs).
        '''
        f = '[MClient] plugins.multitrancom.utils.Commands.get_abbrs'
        file_w = '/tmp/abbr.txt'
        # English
        url = 'https://www.multitran.com/m.exe?a=112&l1=1&l2=2'
        # German
        #url = 'https://www.multitran.com/m.exe?a=112&l1=3&l2=2'
        # Spanish
        #url = 'https://www.multitran.com/m.exe?a=112&l1=5&l2=2'
        # French
        #url = 'https://www.multitran.com/m.exe?a=112&l1=4&l2=2'
        # Dutch
        #url = 'https://www.multitran.com/m.exe?a=112&l1=24&l2=2'
        # Italian
        #url = 'https://www.multitran.com/m.exe?a=112&l1=23&l2=2'
        # Latvian
        #url = 'https://www.multitran.com/m.exe?a=112&l1=27&l2=2'
        # Estonian
        #url = 'https://www.multitran.com/m.exe?a=112&l1=26&l2=2'
        # Afrikaans
        #url = 'https://www.multitran.com/m.exe?a=112&l1=31&l2=2'
        # English-German
        #url = 'https://www.multitran.com/m.exe?a=112&l1=1&l2=3'
        # Esperanto
        #url = 'https://www.multitran.com/m.exe?a=112&l1=34&l2=2'
        # Kalmyk
        #url = 'https://www.multitran.com/m.exe?a=112&l1=35&l2=2'
        topics = Topics(url=url)
        topics.run()
        if topics._abbrs and topics._titles:
            text = ''
            for i in range(len(topics._abbrs)):
                text += topics._abbrs[i] + '\t' + topics._titles[i] + '\n'
            sh.WriteTextFile (file    = file_w
                             ,Rewrite = True
                             ).write(text)
            sh.objs.txt().reset()
            sh.objs._txt.title(_('Abbreviations:'))
            sh.objs._txt.insert(text)
            sh.objs._txt.show()
        else:
            sh.com.empty(f)
                          
    def missing_titles(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.missing_titles'
        ''' This is a list of dictionaries from
            https://www.multitran.com/m.exe?a=112&l1=1&l2=2.
        '''
        file1 = '/tmp/topics'
        ''' This is basically data generated by 'Commands.get_abbrs'
            with some trash deleted. 'dic.orig' - dictionary
            abbreviations, 'dic.transl' - full titles.
        '''
        file2 = '/tmp/abbr.txt'
        topics = sh.ReadTextFile(file=file1).get()
        dic  = sh.Dic (file     = file2
                      ,Sortable = True
                      )
        if topics and dic.orig and dic.transl:
            i = 0
            count = 0
            while i < len(dic.orig):
                ''' Multitran proposes only one full dictionary title
                    even when several abbreviations are given, so we
                    need only one abbreviation per line.
                '''
                if '., ' in dic.orig[i]:
                    del dic.orig[i]
                    del dic.transl[i]
                    count += 1
                    i -= 1
                i += 1
            mes = _('{} duplicates have been deleted').format(count)
            sh.objs.mes(f,mes,True).info()
            dic.orig, dic.transl = (list(x) for x \
            in zip (*sorted (zip (dic.orig, dic.transl)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                   )
            message = ''
            for i in range(len(dic.orig)):
                message += dic.orig[i] + '\t' + dic.transl[i] + '\n'
            sh.objs.mes(f,message).info()
            topics  = topics.splitlines()
            missing = []
            for i in range(len(topics)):
                topics[i] = topics[i].strip()
                if not topics[i] in dic.transl:
                    missing.append(topics[i])
            if missing:
                message = _('The following dictionary titles do not have abbreviations:')
                message += '\n'
                message += '\n'.join(missing)
                sh.objs.mes(f,message).warning()
        else:
            sh.com.empty(f)


com = Commands()


if __name__ == '__main__':
    sh.com.start()
    
    sh.com.end()
