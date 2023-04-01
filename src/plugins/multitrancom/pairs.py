#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh

LANG1 = _('Russian')
LANG2 = _('English')

''' Bad Gateway:209 (Burmese), 262 (Gothic)
    #NOTE: do not forget to put ',' at the end of a pair tuple (otherwise,
    single symbols will be iterated).
'''
LANGS = {_('Abaza'):
            {'code': 478
            ,'pair': ()
            }
        ,_('Abkhazian'):
            {'code': 71
            ,'pair': (_('Russian'),)
            }
        ,_('Achinese'):
            {'code': 172
            ,'pair': ()
            }
        ,_('Acoli'):
            {'code': 176
            ,'pair': ()
            }
        ,_('Adangme'):
            {'code': 150
            ,'pair': ()
            }
        ,_('Adjukru'):
            {'code': 173
            ,'pair': ()
            }
        ,_('Adyghe'):
            {'code': 72
            ,'pair': ()
            }
        ,_('Afar'):
            {'code': 175
            ,'pair': ()
            }
        ,_('Afrihili'):
            {'code': 177
            ,'pair': ()
            }
        ,_('Afrikaans'):
            {'code': 31
            ,'pair': (_('Arabic')
                     ,_('Basque'),_('Catalan'),_('Chinese'),_('Danish')
                     ,_('Dutch'),_('English'),_('Estonian'),_('Finnish')
                     ,_('French'),_('German'),_('Greek'),_('Hungarian')
                     ,_('Icelandic'),_('IsiXhosa'),_('Italian')
                     ,_('Korean'),_('Lithuanian'),_('Norwegian Bokmal')
                     ,_('Persian'),_('Polish'),_('Portuguese')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Sesotho'),_('Sesotho sa leboa'),_('Slovenian')
                     ,_('South Ndebele'),_('Spanish'),_('Swati')
                     ,_('Swedish'),_('Tsonga'),_('Tswana'),_('Turkish')
                     ,_('Ukrainian'),_('Venda'),_('Zulu')
                     )
            }
        ,_('Agutaynen'):
            {'code': 174
            ,'pair': ()
            }
        ,_('Ainu'):
            {'code': 178
            ,'pair': ()
            }
        ,_('Akan'):
            {'code': 179
            ,'pair': ()
            }
        ,_('Akkadian'):
            {'code': 180
            ,'pair': ()
            }
        ,_('Albanian'):
            {'code': 47
            ,'pair': (_('Amharic'),_('Arabic'),_('Armenian')
                     ,_('Assamese'),_('Azerbaijani'),_('Basque')
                     ,_('Belarusian'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Breton'),_('Bulgarian')
                     ,_('Catalan'),_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Cornish'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Esperanto'),_('Estonian'),_('Faroese')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Frisian'),_('Friulian'),_('Galician')
                     ,_('Gallegan'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Ladin'),_('Lao'),_('Latin')
                     ,_('Latvian'),_('Lithuanian'),_('Lower Sorbian')
                     ,_('Luxembourgish'),_('Macedonian'),_('Malay')
                     ,_('Malayalam'),_('Maltese'),_('Manh'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish')
                     ,_('Tamil'),_('Tatar'),_('Telugu'),_('Thai')
                     ,_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Upper Sorbian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Aleut'):
            {'code': 181
            ,'pair': ()
            }
        ,_('Amharic'):
            {'code': 81
            ,'pair': (_('Albanian'),_('Arabic'),_('Armenian')
                     ,_('Assamese'),_('Azerbaijani'),_('Basque')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Ancient Greek'):
            {'code': 264
            ,'pair': ()
            }
        ,_('Angika'):
            {'code': 184
            ,'pair': ()
            }
        ,_('Arabic'):
            {'code': 10
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Croatian'),_('Czech')
                     ,_('Danish'),_('Dutch'),_('English'),_('Estonian')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Galician'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Lao'),_('Latin'),_('Latvian')
                     ,_('Lithuanian'),_('Luxembourgish'),_('Macedonian')
                     ,_('Malay'),_('Malayalam'),_('Maltese'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Odia'),_('Pashto')
                     ,_('Persian'),_('Polish'),_('Portuguese')
                     ,_('Punjabi'),_('Quechua'),_('Romanian')
                     ,_('Russian'),_('Serbian'),_('Serbian latin')
                     ,_('Sesotho sa leboa'),_('Sinhala'),_('Slovak')
                     ,_('Slovenian'),_('Spanish'),_('Swahili')
                     ,_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu')
                     ,_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Aragonese'):
            {'code': 186
            ,'pair': ()
            }
        ,_('Arapaho'):
            {'code': 188
            ,'pair': ()
            }
        ,_('Arawak'):
            {'code': 189
            ,'pair': ()
            }
        ,_('Armenian'):
            {'code': 41
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Assamese'),_('Azerbaijani'),_('Basque')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Assamese'):
            {'code': 82
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Azerbaijani'),_('Basque')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Assyrian'):
            {'code': 467
            ,'pair': ()
            }
        ,_('Asturian'):
            {'code': 84
            ,'pair': ()
            }
        ,_('Avar'):
            {'code': 74
            ,'pair': ()
            }
        ,_('Avestan'):
            {'code': 190
            ,'pair': ()
            }
        ,_('Awadhi'):
            {'code': 191
            ,'pair': ()
            }
        ,_('Aymara'):
            {'code': 192
            ,'pair': ()
            }
        ,_('Azerbaijani'):
            {'code': 25
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Basque')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Balinese'):
            {'code': 196
            ,'pair': ()
            }
        ,_('Baluchi'):
            {'code': 194
            ,'pair': ()
            }
        ,_('Bambara'):
            {'code': 195
            ,'pair': ()
            }
        ,_('Baoulé'):
            {'code': 139
            ,'pair': ()
            }
        ,_('Basaa'):
            {'code': 197
            ,'pair': ()
            }
        ,_('Bashkir'):
            {'code': 193
            ,'pair': (_('Russian'),)
            }
        ,_('Basque'):
            {'code': 68
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic')
                     ,_('Arabic'),_('Armenian'),_('Assamese')
                     ,_('Azerbaijani'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Cornish'),_('Croatian'),_('Czech'),_('Danish')
                     ,_('Dutch'),_('English'),_('Esperanto')
                     ,_('Estonian'),_('Faroese'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Galician'),_('Gallegan')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin')
                     ,_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Manh'),_('Maori'),_('Marathi')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Beja'):
            {'code': 198
            ,'pair': ()
            }
        ,_('Belarusian'):
            {'code': 58
            ,'pair': (_('Albanian'),_('Basque'),_('Breton')
                     ,_('Bulgarian'),_('Catalan'),_('Cornish')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Gallegan'),_('German'),_('Greek')
                     ,_('Hungarian'),_('Icelandic'),_('Irish')
                     ,_('Italian'),_('Ladin'),_('Latin'),_('Latvian')
                     ,_('Lithuanian'),_('Lower Sorbian'),_('Macedonian')
                     ,_('Maltese'),_('Manh'),_('Norwegian Bokmal')
                     ,_('Occitan'),_('Polish'),_('Portuguese')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian'),_('Slovak')
                     ,_('Slovenian'),_('Spanish'),_('Swedish')
                     ,_('Turkish'),_('Ukrainian'),_('Upper Sorbian')
                     ,_('Welsh')
                     )
            }
        ,_('Belizean Creole'):
            {'code': 154
            ,'pair': ()
            }
        ,_('Bemba'):
            {'code': 199
            ,'pair': ()
            }
        ,_('Bengali'):
            {'code': 19
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Bhojpuri'):
            {'code': 200
            ,'pair': ()
            }
        ,_('Bikol'):
            {'code': 201
            ,'pair': ()
            }
        ,_('Bilin'):
            {'code': 210
            ,'pair': ()
            }
        ,_('Bini'):
            {'code': 202
            ,'pair': ()
            }
        ,_('Bislama'):
            {'code': 203
            ,'pair': ()
            }
        ,_('Bosnian'):
            {'code': 63
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian cyrillic')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Bosnian cyrillic'):
            {'code': 96
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Estonian'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Galician')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Braj'):
            {'code': 206
            ,'pair': ()
            }
        ,_('Breton'):
            {'code': 131
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian')
                     ,_('Bulgarian'),_('Catalan'),_('Cornish')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Finnish'),_('French')
                     ,_('Frisian'),_('Friulian'),_('Gallegan')
                     ,_('German'),_('Greek'),_('Hungarian')
                     ,_('Icelandic'),_('Irish'),_('Italian'),_('Ladin')
                     ,_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Macedonian'),_('Maltese')
                     ,_('Manh'),_('Norwegian Bokmal'),_('Occitan')
                     ,_('Polish'),_('Portuguese'),_('Romanian')
                     ,_('Romansh'),_('Romany'),_('Russian'),_('Sami')
                     ,_('Sardinian'),_('Scottish Gaelic'),_('Serbian')
                     ,_('Slovak'),_('Slovenian'),_('Spanish')
                     ,_('Swedish'),_('Turkish'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Welsh')
                     )
            }
        ,_('Buginese'):
            {'code': 208
            ,'pair': ()
            }
        ,_('Bulgarian'):
            {'code': 15
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Catalan'),_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Cornish'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Esperanto'),_('Estonian'),_('Faroese')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Frisian'),_('Friulian'),_('Galician')
                     ,_('Gallegan'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Ladin'),_('Lao'),_('Latin')
                     ,_('Latvian'),_('Lithuanian'),_('Lower Sorbian')
                     ,_('Luxembourgish'),_('Macedonian'),_('Malay')
                     ,_('Malayalam'),_('Maltese'),_('Manh'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Buriat'):
            {'code': 207
            ,'pair': ()
            }
        ,_('Burmese'):
            {'code': 209
            ,'pair': ()
            }
        ,_('Caddo'):
            {'code': 211
            ,'pair': ()
            }
        ,_('Cameroonian Creole'):
            {'code': 152
            ,'pair': ()
            }
        ,_('Caribbean Hindustani'):
            {'code': 434
            ,'pair': ()
            }
        ,_('Carolinian'):
            {'code': 425
            ,'pair': ()
            }
        ,_('Catalan'):
            {'code': 53
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Bulgarian'),_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Cornish'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Esperanto'),_('Estonian'),_('Faroese')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Frisian'),_('Friulian'),_('Galician')
                     ,_('Gallegan'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Ladin'),_('Lao'),_('Latin')
                     ,_('Latvian'),_('Lithuanian'),_('Lower Sorbian')
                     ,_('Luxembourgish'),_('Macedonian'),_('Malay')
                     ,_('Malayalam'),_('Maltese'),_('Manh'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Cebuano'):
            {'code': 213
            ,'pair': ()
            }
        ,_('Central Atlas Tamazight'):
            {'code': 456
            ,'pair': ()
            }
        ,_('Chagatai'):
            {'code': 216
            ,'pair': ()
            }
        ,_('Chamorro'):
            {'code': 214
            ,'pair': ()
            }
        ,_('Chechen'):
            {'code': 73
            ,'pair': (_('Russian'),)
            }
        ,_('Cherokee'):
            {'code': 222
            ,'pair': ()
            }
        ,_('Cheyenne'):
            {'code': 223
            ,'pair': ()
            }
        ,_('Chibcha'):
            {'code': 215
            ,'pair': ()
            }
        ,_('Chinese'):
            {'code': 17
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic')
                     ,_('Arabic'),_('Armenian'),_('Assamese')
                     ,_('Azerbaijani'),_('Basque'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian')
                     ,_('Catalan'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Croatian'),_('Czech')
                     ,_('Danish'),_('Dutch'),_('English'),_('Estonian')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Galician'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Lao'),_('Latin'),_('Latvian')
                     ,_('Lithuanian'),_('Luxembourgish'),_('Macedonian')
                     ,_('Malay'),_('Malayalam'),_('Maltese'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Odia'),_('Pashto')
                     ,_('Persian'),_('Polish'),_('Portuguese')
                     ,_('Punjabi'),_('Quechua'),_('Romanian')
                     ,_('Russian'),_('Serbian'),_('Serbian latin')
                     ,_('Sesotho sa leboa'),_('Sinhala'),_('Slovak')
                     ,_('Slovenian'),_('Spanish'),_('Swahili')
                     ,_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu')
                     ,_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Chinese Taiwan'):
            {'code': 98
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese simplified'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Estonian'),_('Filipino'),_('Finnish')
                     ,_('French'),_('Galician'),_('Georgian')
                     ,_('German'),_('Greek'),_('Gujarati'),_('Hausa')
                     ,_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Chinese simplified'):
            {'code': 97
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Estonian'),_('Filipino'),_('Finnish')
                     ,_('French'),_('Galician'),_('Georgian')
                     ,_('German'),_('Greek'),_('Gujarati'),_('Hausa')
                     ,_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Chinook jargon'):
            {'code': 219
            ,'pair': ()
            }
        ,_('Chipewyan'):
            {'code': 221
            ,'pair': ()
            }
        ,_('Choctaw'):
            {'code': 220
            ,'pair': ()
            }
        ,_('Church Slavonic'):
            {'code': 66
            ,'pair': ()
            }
        ,_('Chuukese'):
            {'code': 217
            ,'pair': ()
            }
        ,_('Chuvash'):
            {'code': 77
            ,'pair': (_('Russian'),)
            }
        ,_('Classical Newari'):
            {'code': 356
            ,'pair': ()
            }
        ,_('Comorian'):
            {'code': 430
            ,'pair': ()
            }
        ,_('Coptic'):
            {'code': 224
            ,'pair': ()
            }
        ,_('Cornish'):
            {'code': 132
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian')
                     ,_('Breton'),_('Bulgarian'),_('Catalan')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Gallegan'),_('German'),_('Greek')
                     ,_('Hungarian'),_('Icelandic'),_('Irish')
                     ,_('Italian'),_('Ladin'),_('Latin'),_('Latvian')
                     ,_('Lithuanian'),_('Lower Sorbian'),_('Macedonian')
                     ,_('Maltese'),_('Manh'),_('Norwegian Bokmal')
                     ,_('Occitan'),_('Polish'),_('Portuguese')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian'),_('Slovak')
                     ,_('Slovenian'),_('Spanish'),_('Swedish')
                     ,_('Turkish'),_('Ukrainian'),_('Upper Sorbian')
                     ,_('Welsh')
                     )
            }
        ,_('Corsican'):
            {'code': 54
            ,'pair': ()
            }
        ,_('Cree'):
            {'code': 225
            ,'pair': ()
            }
        ,_('Creek'):
            {'code': 339
            ,'pair': ()
            }
        ,_('Crimean Tatar'):
            {'code': 76
            ,'pair': ()
            }
        ,_('Croatian'):
            {'code': 8
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Cornish'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Filipino'),_('Finnish')
                     ,_('French'),_('Frisian'),_('Friulian')
                     ,_('Galician'),_('Gallegan'),_('Georgian')
                     ,_('German'),_('Greek'),_('Gujarati'),_('Hausa')
                     ,_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin')
                     ,_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Manh'),_('Maori'),_('Marathi')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Czech'):
            {'code': 16
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Bulgarian'),_('Catalan'),_('Chinese')
                     ,_('Chinese Taiwan'),_('Chinese simplified')
                     ,_('Cornish'),_('Croatian'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Filipino'),_('Finnish')
                     ,_('French'),_('Frisian'),_('Friulian')
                     ,_('Galician'),_('Gallegan'),_('Georgian')
                     ,_('German'),_('Greek'),_('Gujarati'),_('Hausa')
                     ,_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin')
                     ,_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Manh'),_('Maori'),_('Marathi')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Dakota'):
            {'code': 227
            ,'pair': ()
            }
        ,_('Danish'):
            {'code': 22
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Dargwa'):
            {'code': 228
            ,'pair': ()
            }
        ,_('Delaware'):
            {'code': 229
            ,'pair': ()
            }
        ,_('Dhivehi'):
            {'code': 233
            ,'pair': ()
            }
        ,_('Dinka'):
            {'code': 232
            ,'pair': ()
            }
        ,_('Dogri'):
            {'code': 234
            ,'pair': ()
            }
        ,_('Dogrib'):
            {'code': 231
            ,'pair': ()
            }
        ,_('Duala'):
            {'code': 235
            ,'pair': ()
            }
        ,_('Dutch'):
            {'code': 24
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Dyula'):
            {'code': 237
            ,'pair': ()
            }
        ,_('Dzongkha'):
            {'code': 238
            ,'pair': ()
            }
        ,_('Eastern Frisian'):
            {'code': 251
            ,'pair': ()
            }
        ,_('Efik'):
            {'code': 239
            ,'pair': ()
            }
        ,_('Egyptian'):
            {'code': 240
            ,'pair': ()
            }
        ,_('Ekajuk'):
            {'code': 241
            ,'pair': ()
            }
        ,_('Elamite'):
            {'code': 242
            ,'pair': ()
            }
        ,_('Emilian-Romagnol'):
            {'code': 432
            ,'pair': ()
            }
        ,_('English'):
            {'code': 1
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic')
                     ,_('Arabic'),_('Armenian'),_('Assamese')
                     ,_('Azerbaijani'),_('Basque'),_('Belarusian')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Breton'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Cornish'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('Esperanto')
                     ,_('Estonian'),_('Faroese'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Galician'),_('Gallegan')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin')
                     ,_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Manh'),_('Maori'),_('Marathi')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho')
                     ,_('Sesotho sa leboa'),_('Sinhala'),_('Slovak')
                     ,_('Slovenian'),_('South Ndebele'),_('Spanish')
                     ,_('Swahili'),_('Swati'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga')
                     ,_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Upper Sorbian'),_('Urdu')
                     ,_('Uzbek'),_('Venda'),_('Vietnamese'),_('Wayana')
                     ,_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Erzya'):
            {'code': 341
            ,'pair': ()
            }
        ,_('Esperanto'):
            {'code': 34
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian')
                     ,_('Breton'),_('Bulgarian'),_('Catalan')
                     ,_('Cornish'),_('Croatian'),_('Czech'),_('Danish')
                     ,_('Dutch'),_('English'),_('Estonian'),_('Faroese')
                     ,_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Gallegan'),_('German'),_('Greek')
                     ,_('Hungarian'),_('Icelandic'),_('Irish')
                     ,_('Italian'),_('Ladin'),_('Latin'),_('Latvian')
                     ,_('Lithuanian'),_('Lower Sorbian'),_('Macedonian')
                     ,_('Maltese'),_('Manh'),_('Norwegian Bokmal')
                     ,_('Occitan'),_('Polish'),_('Portuguese')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian'),_('Slovak')
                     ,_('Slovenian'),_('Spanish'),_('Swedish')
                     ,_('Turkish'),_('Ukrainian'),_('Upper Sorbian')
                     ,_('Welsh')
                     )
            }
        ,_('Estonian'):
            {'code': 26
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic')
                     ,_('Arabic'),_('Armenian'),_('Assamese')
                     ,_('Azerbaijani'),_('Basque'),_('Belarusian')
                     ,_('Bengali'),_('Bosnian'),_('Bosnian cyrillic')
                     ,_('Breton'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Cornish'),_('Croatian')
                     ,_('Czech'),_('Danish'),_('Dutch'),_('English')
                     ,_('Esperanto'),_('Faroese'),_('Filipino')
                     ,_('Finnish'),_('French'),_('Frisian')
                     ,_('Friulian'),_('Galician'),_('Gallegan')
                     ,_('Georgian'),_('German'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Inuktitut'),_('Irish'),_('IsiXhosa')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin')
                     ,_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian')
                     ,_('Lower Sorbian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Manh'),_('Maori'),_('Marathi')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany')
                     ,_('Russian'),_('Sami'),_('Sardinian')
                     ,_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian')
                     ,_('Upper Sorbian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof')
                     ,_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Ewe'):
            {'code': 244
            ,'pair': ()
            }
        ,_('Ewondo'):
            {'code': 245
            ,'pair': ()
            }
        ,_('Fang'):
            {'code': 246
            ,'pair': ()
            }
        ,_('Fanti'):
            {'code': 247
            ,'pair': ()
            }
        ,_('Faroese'):
            {'code': 123
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Fijian'):
            {'code': 248
            ,'pair': ()
            }
        ,_('Filipino'):
            {'code': 99
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Finnish'):
            {'code': 36
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Fon'):
            {'code': 156
            ,'pair': ()
            }
        ,_('French'):
            {'code': 4
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('French Guiana Creole'):
            {'code': 142
            ,'pair': ()
            }
        ,_('Frisian'):
            {'code': 122
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Friulian'):
            {'code': 124
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Fulah'):
            {'code': 252
            ,'pair': ()
            }
        ,_('Ga'):
            {'code': 253
            ,'pair': ()
            }
        ,_('Galibi Carib'):
            {'code': 212
            ,'pair': ()
            }
        ,_('Galician'):
            {'code': 55
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Croatian'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Gallegan'):
            {'code': 129
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Ganda'):
            {'code': 318
            ,'pair': ()
            }
        ,_('Gaulish'):
            {'code': 128
            ,'pair': ()
            }
        ,_('Gayo'):
            {'code': 254
            ,'pair': ()
            }
        ,_('Gbaya'):
            {'code': 255
            ,'pair': ()
            }
        ,_("Ge'ez"):
            {'code': 256
            ,'pair': ()
            }
        ,_('Gela'):
            {'code': 429
            ,'pair': ()
            }
        ,_('Gen'):
            {'code': 159
            ,'pair': ()
            }
        ,_('Georgian'):
            {'code': 40
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('German'):
            {'code': 3
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tajik'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Gilbertese'):
            {'code': 257
            ,'pair': ()
            }
        ,_('Gondi'):
            {'code': 260
            ,'pair': ()
            }
        ,_('Gorontalo'):
            {'code': 261
            ,'pair': ()
            }
        ,_('Gothic'):
            {'code': 262
            ,'pair': ()
            }
        ,_('Grebo'):
            {'code': 263
            ,'pair': ()
            }
        ,_('Greek'):
            {'code': 38
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Konkani'),_('Ladin'),_('Lao'),_('Latin'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Gronings'):
            {'code': 472
            ,'pair': ()
            }
        ,_('Guadeloupe Creole'):
            {'code': 145
            ,'pair': ()
            }
        ,_('Guarani'):
            {'code': 265
            ,'pair': ()
            }
        ,_('Gujarati'):
            {'code': 100
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Gwichʼin'):
            {'code': 267
            ,'pair': ()
            }
        ,_('Hadza'):
            {'code': 473
            ,'pair': ()
            }
        ,_('Haida'):
            {'code': 268
            ,'pair': ()
            }
        ,_('Haitian Creole'):
            {'code': 147
            ,'pair': ()
            }
        ,_('Hausa'):
            {'code': 101
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Hawaiian'):
            {'code': 270
            ,'pair': ()
            }
        ,_('Hebrew'):
            {'code': 6
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Herero'):
            {'code': 271
            ,'pair': ()
            }
        ,_('Hiligaynon'):
            {'code': 272
            ,'pair': ()
            }
        ,_('Hindi'):
            {'code': 18
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Hiri Motu'):
            {'code': 275
            ,'pair': ()
            }
        ,_('Hittite'):
            {'code': 273
            ,'pair': ()
            }
        ,_('Hmong'):
            {'code': 274
            ,'pair': ()
            }
        ,_('Hungarian'):
            {'code': 42
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Hupa'):
            {'code': 276
            ,'pair': ()
            }
        ,_('Iban'):
            {'code': 277
            ,'pair': ()
            }
        ,_('Icelandic'):
            {'code': 50
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Ido'):
            {'code': 278
            ,'pair': ()
            }
        ,_('Igbo'):
            {'code': 102
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Ilocano'):
            {'code': 281
            ,'pair': ()
            }
        ,_('Inari Sami'):
            {'code': 397
            ,'pair': ()
            }
        ,_('Indonesian'):
            {'code': 86
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Ingush'):
            {'code': 75
            ,'pair': (_('Russian'),)
            }
        ,_('Interlingua'):
            {'code': 282
            ,'pair': ()
            }
        ,_('Interlingue'):
            {'code': 280
            ,'pair': ()
            }
        ,_('Inuktitut'):
            {'code': 103
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Inupiaq'):
            {'code': 283
            ,'pair': ()
            }
        ,_('Iraqw'):
            {'code': 474
            ,'pair': ()
            }
        ,_('Irish'):
            {'code': 49
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('IsiXhosa'):
            {'code': 104
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('South Ndebele'),_('Spanish'),_('Swahili'),_('Swati'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Venda'),_('Vietnamese'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Italian'):
            {'code': 23
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Ivatan'):
            {'code': 158
            ,'pair': ()
            }
        ,_('Japanese'):
            {'code': 28
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Javanese'):
            {'code': 140
            ,'pair': ()
            }
        ,_('Judeo-Arabic'):
            {'code': 286
            ,'pair': ()
            }
        ,_('Judeo-Persian'):
            {'code': 285
            ,'pair': ()
            }
        ,_('Kabardian'):
            {'code': 295
            ,'pair': ()
            }
        ,_('Kabyle'):
            {'code': 288
            ,'pair': ()
            }
        ,_('Kachin'):
            {'code': 289
            ,'pair': ()
            }
        ,_('Kaguru'):
            {'code': 468
            ,'pair': ()
            }
        ,_('Kalaallisut'):
            {'code': 290
            ,'pair': ()
            }
        ,_('Kalmyk'):
            {'code': 35
            ,'pair': (_('Russian'),)
            }
        ,_('Kamba'):
            {'code': 291
            ,'pair': ()
            }
        ,_('Kami'):
            {'code': 475
            ,'pair': ()
            }
        ,_('Kannada'):
            {'code': 106
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Kanuri'):
            {'code': 293
            ,'pair': ()
            }
        ,_('Kara-Kalpak'):
            {'code': 287
            ,'pair': ()
            }
        ,_('Karachay-Balkar'):
            {'code': 303
            ,'pair': ()
            }
        ,_('Karelian'):
            {'code': 304
            ,'pair': ()
            }
        ,_('Kashmiri'):
            {'code': 292
            ,'pair': ()
            }
        ,_('Kashubian'):
            {'code': 226
            ,'pair': ()
            }
        ,_('Kawi'):
            {'code': 294
            ,'pair': ()
            }
        ,_('Kazakh'):
            {'code': 43
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Khakas'):
            {'code': 435
            ,'pair': ()
            }
        ,_('Khasi'):
            {'code': 296
            ,'pair': ()
            }
        ,_('Khmer'):
            {'code': 79
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Khotanese'):
            {'code': 297
            ,'pair': ()
            }
        ,_('Kikuyu'):
            {'code': 269
            ,'pair': ()
            }
        ,_('Kim'):
            {'code': 157
            ,'pair': ()
            }
        ,_('Kimakonde'):
            {'code': 469
            ,'pair': ()
            }
        ,_('Kimbundu'):
            {'code': 298
            ,'pair': ()
            }
        ,_('Kinga'):
            {'code': 436
            ,'pair': ()
            }
        ,_('Kinyarwanda'):
            {'code': 107
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Kirghiz'):
            {'code': 44
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Kirufiji'):
            {'code': 470
            ,'pair': ()
            }
        ,_('Klingon'):
            {'code': 422
            ,'pair': ()
            }
        ,_('Komi'):
            {'code': 299
            ,'pair': ()
            }
        ,_('Kongo'):
            {'code': 300
            ,'pair': ()
            }
        ,_('Konkani'):
            {'code': 109
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Korean'):
            {'code': 39
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Korean Transliteration'):
            {'code': 465
            ,'pair': ()
            }
        ,_('Kosraean'):
            {'code': 301
            ,'pair': ()
            }
        ,_('Kpelle'):
            {'code': 302
            ,'pair': ()
            }
        ,_('Krio'):
            {'code': 476
            ,'pair': ()
            }
        ,_('Kuanyama'):
            {'code': 306
            ,'pair': ()
            }
        ,_('Kumyk'):
            {'code': 307
            ,'pair': ()
            }
        ,_('Kurdish'):
            {'code': 51
            ,'pair': ()
            }
        ,_('Kurmanji'):
            {'code': 437
            ,'pair': ()
            }
        ,_('Kurukh'):
            {'code': 305
            ,'pair': ()
            }
        ,_('Kutenai'):
            {'code': 308
            ,'pair': ()
            }
        ,_('Kwangali'):
            {'code': 438
            ,'pair': ()
            }
        ,_('Ladin'):
            {'code': 125
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Lahnda'):
            {'code': 309
            ,'pair': ()
            }
        ,_('Lamba'):
            {'code': 310
            ,'pair': ()
            }
        ,_('Lango'):
            {'code': 439
            ,'pair': ()
            }
        ,_('Lao'):
            {'code': 83
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Latin'):
            {'code': 37
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Japanese'),_('Korean'),_('Ladin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Latvian'):
            {'code': 27
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Lezghian'):
            {'code': 311
            ,'pair': ()
            }
        ,_('Ligurian'):
            {'code': 440
            ,'pair': ()
            }
        ,_('Limburgan'):
            {'code': 312
            ,'pair': ()
            }
        ,_('Lingala'):
            {'code': 313
            ,'pair': ()
            }
        ,_('Lithuanian'):
            {'code': 12
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Lojban'):
            {'code': 284
            ,'pair': ()
            }
        ,_('Lombard'):
            {'code': 441
            ,'pair': ()
            }
        ,_('Low German'):
            {'code': 348
            ,'pair': ()
            }
        ,_('Lower Sorbian'):
            {'code': 62
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Lozi'):
            {'code': 315
            ,'pair': ()
            }
        ,_('Luba-Katanga'):
            {'code': 317
            ,'pair': ()
            }
        ,_('Luba-Lulua'):
            {'code': 316
            ,'pair': ()
            }
        ,_('Luguru'):
            {'code': 442
            ,'pair': ()
            }
        ,_('Luiseno'):
            {'code': 319
            ,'pair': ()
            }
        ,_('Lule Sami'):
            {'code': 396
            ,'pair': ()
            }
        ,_('Lunda'):
            {'code': 320
            ,'pair': ()
            }
        ,_('Luo'):
            {'code': 321
            ,'pair': ()
            }
        ,_('Lushai'):
            {'code': 322
            ,'pair': ()
            }
        ,_('Luxembourgish'):
            {'code': 110
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Macedo-Romanian'):
            {'code': 382
            ,'pair': ()
            }
        ,_('Macedonian'):
            {'code': 65
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'))
            }
        ,_('Madurese'):
            {'code': 323
            ,'pair': ()
            }
        ,_('Magahi'):
            {'code': 324
            ,'pair': ()
            }
        ,_('Maithili'):
            {'code': 325
            ,'pair': ()
            }
        ,_('Makasar'):
            {'code': 326
            ,'pair': ()
            }
        ,_('Malagasy'):
            {'code': 334
            ,'pair': ()
            }
        ,_('Malay'):
            {'code': 120
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Malayalam'):
            {'code': 111
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Maltese'):
            {'code': 78
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Mamasa'):
            {'code': 443
            ,'pair': ()
            }
        ,_('Manchu'):
            {'code': 335
            ,'pair': ()
            }
        ,_('Mandar'):
            {'code': 329
            ,'pair': ()
            }
        ,_('Mandinka'):
            {'code': 148
            ,'pair': ()
            }
        ,_('Manh'):
            {'code': 133
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Manipuri'):
            {'code': 336
            ,'pair': ()
            }
        ,_('Maori'):
            {'code': 89
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Mapudungun'):
            {'code': 187
            ,'pair': ()
            }
        ,_('Marathi'):
            {'code': 90
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Mari'):
            {'code': 218
            ,'pair': ()
            }
        ,_('Marshallese'):
            {'code': 160
            ,'pair': ()
            }
        ,_('Marwari'):
            {'code': 340
            ,'pair': ()
            }
        ,_('Masai'):
            {'code': 327
            ,'pair': ()
            }
        ,_('Mashi'):
            {'code': 444
            ,'pair': ()
            }
        ,_('Mauritian Creole'):
            {'code': 143
            ,'pair': ()
            }
        ,_('Mayan'):
            {'code': 433
            ,'pair': ()
            }
        ,_('Mbwera'):
            {'code': 471
            ,'pair': ()
            }
        ,_('Mende'):
            {'code': 330
            ,'pair': ()
            }
        ,_('Meru'):
            {'code': 445
            ,'pair': ()
            }
        ,_("Mi'kmaq"):
            {'code': 332
            ,'pair': ()
            }
        ,_('Middle Dutch'):
            {'code': 236
            ,'pair': ()
            }
        ,_('Middle English'):
            {'code': 243
            ,'pair': ()
            }
        ,_('Middle French'):
            {'code': 249
            ,'pair': ()
            }
        ,_('Middle High German'):
            {'code': 258
            ,'pair': ()
            }
        ,_('Middle Irish'):
            {'code': 331
            ,'pair': ()
            }
        ,_('Minangkabau'):
            {'code': 333
            ,'pair': ()
            }
        ,_('Mingrelian'):
            {'code': 70
            ,'pair': ()
            }
        ,_('Mirandese'):
            {'code': 56
            ,'pair': ()
            }
        ,_('Mohawk'):
            {'code': 337
            ,'pair': ()
            }
        ,_('Moksha'):
            {'code': 328
            ,'pair': ()
            }
        ,_('Moldovan'):
            {'code': 447
            ,'pair': ()
            }
        ,_('Mongo'):
            {'code': 314
            ,'pair': ()
            }
        ,_('Mongolian'):
            {'code': 121
            ,'pair': (_('Russian'),)
            }
        ,_('Mongolian Transliteration'):
            {'code': 466
            ,'pair': ()
            }
        ,_('Mongolian script'):
            {'code': 448
            ,'pair': ()
            }
        ,_('Montenegrin'):
            {'code': 64
            ,'pair': (_('Russian'),)
            }
        ,_('Mossi'):
            {'code': 338
            ,'pair': ()
            }
        ,_("N'Ko"):
            {'code': 355
            ,'pair': ()
            }
        ,_('Nasioi'):
            {'code': 449
            ,'pair': ()
            }
        ,_('Nauru'):
            {'code': 343
            ,'pair': ()
            }
        ,_('Navajo'):
            {'code': 344
            ,'pair': ()
            }
        ,_('Ndonga'):
            {'code': 347
            ,'pair': ()
            }
        ,_('Neapolitan'):
            {'code': 342
            ,'pair': ()
            }
        ,_('Nepal Bhasa'):
            {'code': 349
            ,'pair': ()
            }
        ,_('Nepali'):
            {'code': 80
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Nias'):
            {'code': 350
            ,'pair': ()
            }
        ,_('Niuean'):
            {'code': 351
            ,'pair': ()
            }
        ,_('Nogai'):
            {'code': 352
            ,'pair': ()
            }
        ,_('North Ndebele'):
            {'code': 346
            ,'pair': ()
            }
        ,_('Northern Sami'):
            {'code': 395
            ,'pair': ()
            }
        ,_('Norwegian Bokmal'):
            {'code': 30
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Norwegian Nynorsk'):
            {'code': 119
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Numèè'):
            {'code': 428
            ,'pair': ()
            }
        ,_('Nyakyusa'):
            {'code': 450
            ,'pair': ()
            }
        ,_('Nyamwezi'):
            {'code': 358
            ,'pair': ()
            }
        ,_('Nyanja'):
            {'code': 357
            ,'pair': ()
            }
        ,_('Nyankole'):
            {'code': 359
            ,'pair': ()
            }
        ,_('Nyoro'):
            {'code': 360
            ,'pair': ()
            }
        ,_('Nzima'):
            {'code': 361
            ,'pair': ()
            }
        ,_('Occitan'):
            {'code': 127
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Odia'):
            {'code': 85
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Official Aramaic'):
            {'code': 185
            ,'pair': ()
            }
        ,_('Ojibwa'):
            {'code': 362
            ,'pair': ()
            }
        ,_('Old English'):
            {'code': 183
            ,'pair': ()
            }
        ,_('Old French'):
            {'code': 250
            ,'pair': ()
            }
        ,_('Old High German'):
            {'code': 259
            ,'pair': ()
            }
        ,_('Old Irish'):
            {'code': 391
            ,'pair': ()
            }
        ,_('Old Norse'):
            {'code': 353
            ,'pair': ()
            }
        ,_('Old Occitan'):
            {'code': 376
            ,'pair': ()
            }
        ,_('Old Persian'):
            {'code': 372
            ,'pair': ()
            }
        ,_('Old Prussian'):
            {'code': 162
            ,'pair': ()
            }
        ,_('Oromo'):
            {'code': 363
            ,'pair': ()
            }
        ,_('Osage'):
            {'code': 364
            ,'pair': ()
            }
        ,_('Ossetian'):
            {'code': 365
            ,'pair': ()
            }
        ,_('Ottoman Turkish'):
            {'code': 366
            ,'pair': ()
            }
        ,_('Pahlavi'):
            {'code': 368
            ,'pair': ()
            }
        ,_('Palauan'):
            {'code': 371
            ,'pair': ()
            }
        ,_('Pali'):
            {'code': 374
            ,'pair': ()
            }
        ,_('Pampanga'):
            {'code': 369
            ,'pair': ()
            }
        ,_('Pangasinan'):
            {'code': 367
            ,'pair': ()
            }
        ,_('Papiamento'):
            {'code': 370
            ,'pair': ()
            }
        ,_('Pashto'):
            {'code': 87
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Persian'):
            {'code': 52
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Phoenician'):
            {'code': 373
            ,'pair': ()
            }
        ,_('Piedmontese'):
            {'code': 451
            ,'pair': ()
            }
        ,_('Pinyin'):
            {'code': 452
            ,'pair': ()
            }
        ,_('Pohnpeian'):
            {'code': 375
            ,'pair': ()
            }
        ,_('Polish'):
            {'code': 14
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Portuguese'):
            {'code': 11
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Portuguese creole'):
            {'code': 426
            ,'pair': ()
            }
        ,_('Punjabi'):
            {'code': 20
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Quechua'):
            {'code': 88
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Rajasthani'):
            {'code': 377
            ,'pair': ()
            }
        ,_('Rapanui'):
            {'code': 378
            ,'pair': ()
            }
        ,_('Rarotongan'):
            {'code': 379
            ,'pair': ()
            }
        ,_('Rennellese'):
            {'code': 431
            ,'pair': ()
            }
        ,_('Reunionese'):
            {'code': 380
            ,'pair': ()
            }
        ,_('Rodriguan Creole'):
            {'code': 146
            ,'pair': ()
            }
        ,_('Romanian'):
            {'code': 13
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Romansh'):
            {'code': 57
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Romany'):
            {'code': 46
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Rotokas'):
            {'code': 446
            ,'pair': ()
            }
        ,_('Rundi'):
            {'code': 381
            ,'pair': ()
            }
        ,_('Russian'):
            {'code': 2
            ,'pair': (_('Abkhazian'),_('Afrikaans'),_('Albanian')
                     ,_('Amharic'),_('Arabic'),_('Armenian')
                     ,_('Assamese'),_('Azerbaijani'),_('Bashkir')
                     ,_('Basque'),_('Belarusian'),_('Bengali')
                     ,_('Bosnian'),_('Bosnian cyrillic'),_('Breton')
                     ,_('Bulgarian'),_('Catalan'),_('Chechen')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Chuvash'),_('Cornish')
                     ,_('Croatian'),_('Czech'),_('Danish'),_('Dutch')
                     ,_('English'),_('Esperanto'),_('Estonian')
                     ,_('Faroese'),_('Filipino'),_('Finnish')
                     ,_('French'),_('Frisian'),_('Friulian')
                     ,_('Galician'),_('Gallegan'),_('Georgian')
                     ,_('German'),_('Gothic'),_('Greek'),_('Gujarati')
                     ,_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian')
                     ,_('Icelandic'),_('Igbo'),_('Indonesian')
                     ,_('Ingush'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kalmyk'),_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Ladin'),_('Lao'),_('Latin')
                     ,_('Latvian'),_('Lithuanian'),_('Lower Sorbian')
                     ,_('Luxembourgish'),_('Macedonian'),_('Malay')
                     ,_('Malayalam'),_('Maltese'),_('Manh'),_('Maori')
                     ,_('Marathi'),_('Mongolian'),_('Montenegrin')
                     ,_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Occitan'),_('Odia')
                     ,_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Romansh'),_('Romany'),_('Sami')
                     ,_('Sardinian'),_('Scottish Gaelic'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish')
                     ,_('Tajik'),_('Tamil'),_('Tatar'),_('Telugu')
                     ,_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Upper Sorbian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh')
                     ,_('Wolof'),_('Yakut'),_('Yoruba'),_('Zulu')
                     )
            }
        ,_('Ruthene'):
            {'code': 59
            ,'pair': ()
            }
        ,_('Samaritan Aramaic'):
            {'code': 385
            ,'pair': ()
            }
        ,_('Sami'):
            {'code': 130
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Samoan'):
            {'code': 398
            ,'pair': ()
            }
        ,_('Sandawe'):
            {'code': 354
            ,'pair': ()
            }
        ,_('Sango'):
            {'code': 383
            ,'pair': ()
            }
        ,_('Sangu'):
            {'code': 453
            ,'pair': ()
            }
        ,_('Sanskrit'):
            {'code': 386
            ,'pair': ()
            }
        ,_('Santali'):
            {'code': 412
            ,'pair': ()
            }
        ,_('Sardinian'):
            {'code': 126
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Sasak'):
            {'code': 387
            ,'pair': ()
            }
        ,_('Scots'):
            {'code': 389
            ,'pair': ()
            }
        ,_('Scottish Gaelic'):
            {'code': 134
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Upper Sorbian'),_('Welsh'))
            }
        ,_('Selkup'):
            {'code': 390
            ,'pair': ()
            }
        ,_('Serbian'):
            {'code': 7
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Serbian latin'):
            {'code': 114
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Serer'):
            {'code': 406
            ,'pair': ()
            }
        ,_('Sesotho'):
            {'code': 404
            ,'pair': (_('Swati'),_('Tsonga'))
            }
        ,_('Sesotho sa leboa'):
            {'code': 118
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('South Ndebele'),_('Spanish'),_('Swahili'),_('Swati'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Venda'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Seychellois Creole'):
            {'code': 144
            ,'pair': ()
            }
        ,_('Shambala'):
            {'code': 454
            ,'pair': ()
            }
        ,_('Shan'):
            {'code': 392
            ,'pair': ()
            }
        ,_('Shilluk'):
            {'code': 421
            ,'pair': ()
            }
        ,_('Shona'):
            {'code': 400
            ,'pair': ()
            }
        ,_('Shor'):
            {'code': 455
            ,'pair': ()
            }
        ,_('Sichuan Yi'):
            {'code': 279
            ,'pair': ()
            }
        ,_('Sicilian'):
            {'code': 388
            ,'pair': ()
            }
        ,_('Sidamo'):
            {'code': 393
            ,'pair': ()
            }
        ,_('Siksika'):
            {'code': 204
            ,'pair': ()
            }
        ,_('Sindhi'):
            {'code': 401
            ,'pair': ()
            }
        ,_('Sinhala'):
            {'code': 116
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Skolt Sami'):
            {'code': 399
            ,'pair': ()
            }
        ,_('Slave'):
            {'code': 230
            ,'pair': ()
            }
        ,_('Slovak'):
            {'code': 60
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Slovenian'):
            {'code': 67
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Sogdian'):
            {'code': 402
            ,'pair': ()
            }
        ,_('Somali'):
            {'code': 403
            ,'pair': ()
            }
        ,_('Soninke'):
            {'code': 138
            ,'pair': ()
            }
        ,_('South Ndebele'):
            {'code': 345
            ,'pair': (_('Sesotho'),_('Swati'),_('Tsonga'))
            }
        ,_('Southern Altai'):
            {'code': 182
            ,'pair': ()
            }
        ,_('Southern Sami'):
            {'code': 394
            ,'pair': ()
            }
        ,_('Spanish'):
            {'code': 5
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Sranan Tongo'):
            {'code': 405
            ,'pair': ()
            }
        ,_('Sukuma'):
            {'code': 408
            ,'pair': ()
            }
        ,_('Sumerian'):
            {'code': 411
            ,'pair': ()
            }
        ,_('Sundanese'):
            {'code': 409
            ,'pair': ()
            }
        ,_('Surigaonon'):
            {'code': 149
            ,'pair': ()
            }
        ,_('Suriname Creole'):
            {'code': 153
            ,'pair': ()
            }
        ,_('Susu'):
            {'code': 410
            ,'pair': ()
            }
        ,_('Svan'):
            {'code': 69
            ,'pair': ()
            }
        ,_('Swahili'):
            {'code': 108
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Swati'):
            {'code': 407
            ,'pair': (_('Tsonga'),)
            }
        ,_('Swedish'):
            {'code': 29
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Swiss German'):
            {'code': 266
            ,'pair': ()
            }
        ,_('Syriac'):
            {'code': 413
            ,'pair': ()
            }
        ,_('Tagalog'):
            {'code': 137
            ,'pair': ()
            }
        ,_('Tahitian'):
            {'code': 414
            ,'pair': ()
            }
        ,_('Tajik'):
            {'code': 136
            ,'pair': (_('Russian'),)
            }
        ,_('Tamashek'):
            {'code': 424
            ,'pair': ()
            }
        ,_('Tamil'):
            {'code': 91
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Tatar'):
            {'code': 9
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Telugu'):
            {'code': 92
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Tetum'):
            {'code': 417
            ,'pair': ()
            }
        ,_('Thai'):
            {'code': 93
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Thai Transliteration'):
            {'code': 457
            ,'pair': ()
            }
        ,_('Tibetan'):
            {'code': 205
            ,'pair': ()
            }
        ,_('Tigre'):
            {'code': 418
            ,'pair': ()
            }
        ,_('Tigrinya'):
            {'code': 419
            ,'pair': ()
            }
        ,_('Timne'):
            {'code': 415
            ,'pair': ()
            }
        ,_('Tiv'):
            {'code': 420
            ,'pair': ()
            }
        ,_('Tlingit'):
            {'code': 423
            ,'pair': ()
            }
        ,_('Tok Pisin'):
            {'code': 151
            ,'pair': ()
            }
        ,_('Tokelauan'):
            {'code': 164
            ,'pair': ()
            }
        ,_('Tonga'):
            {'code': 416
            ,'pair': ()
            }
        ,_('Tsonga'):
            {'code': 458
            ,'pair': ()
            }
        ,_('Tswana'):
            {'code': 115
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('South Ndebele'),_('Spanish'),_('Swahili'),_('Swati'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Venda'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Tuamotuan'):
            {'code': 427
            ,'pair': ()
            }
        ,_('Turkish'):
            {'code': 32
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Turkmen'):
            {'code': 94
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Tuvan'):
            {'code': 459
            ,'pair': ()
            }
        ,_('Tweants'):
            {'code': 477
            ,'pair': ()
            }
        ,_('Ukrainian'):
            {'code': 33
            ,'pair': (_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Upper Sorbian'):
            {'code': 61
            ,'pair': (_('Albanian'),_('Basque'),_('Belarusian'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Gallegan'),_('German'),_('Greek'),_('Hungarian'),_('Icelandic'),_('Irish'),_('Italian'),_('Ladin'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Macedonian'),_('Maltese'),_('Manh'),_('Norwegian Bokmal'),_('Occitan'),_('Polish'),_('Portuguese'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swedish'),_('Turkish'),_('Ukrainian'),_('Welsh'))
            }
        ,_('Urdu'):
            {'code': 117
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Uzbek'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Uzbek'):
            {'code': 45
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Valencian'):
            {'code': 460
            ,'pair': ()
            }
        ,_('Venda'):
            {'code': 171
            ,'pair': (_('Sesotho'),_('South Ndebele'),_('Swati')
                     ,_('Tsonga')
                     )
            }
        ,_('Venetian'):
            {'code': 461
            ,'pair': ()
            }
        ,_('Vietnamese'):
            {'code': 21
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Vili'):
            {'code': 170
            ,'pair': ()
            }
        ,_('Virgin Islands Creole'):
            {'code': 155
            ,'pair': ()
            }
        ,_('Visayan'):
            {'code': 169
            ,'pair': ()
            }
        ,_('Wallisian'):
            {'code': 161
            ,'pair': ()
            }
        ,_('Walloon'):
            {'code': 462
            ,'pair': ()
            }
        ,_('Walmajarri'):
            {'code': 168
            ,'pair': ()
            }
        ,_('Wanji'):
            {'code': 463
            ,'pair': ()
            }
        ,_('Waray'):
            {'code': 167
            ,'pair': ()
            }
        ,_('Wayana'):
            {'code': 141
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Croatian'),_('Czech')
                     ,_('Danish'),_('Dutch'),_('English'),_('Estonian')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Galician'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('Italian'),_('Japanese'),_('Kannada')
                     ,_('Kazakh'),_('Khmer'),_('Kinyarwanda')
                     ,_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao')
                     ,_('Latvian'),_('Lithuanian'),_('Luxembourgish')
                     ,_('Macedonian'),_('Malay'),_('Malayalam')
                     ,_('Maltese'),_('Maori'),_('Marathi'),_('Nepali')
                     ,_('Norwegian Bokmal'),_('Norwegian Nynorsk')
                     ,_('Odia'),_('Pashto'),_('Persian'),_('Polish')
                     ,_('Portuguese'),_('Punjabi'),_('Quechua')
                     ,_('Romanian'),_('Russian'),_('Serbian')
                     ,_('Serbian latin'),_('Sesotho sa leboa')
                     ,_('Sinhala'),_('Slovak'),_('Slovenian')
                     ,_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil')
                     ,_('Tatar'),_('Telugu'),_('Thai'),_('Tswana')
                     ,_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu')
                     ,_('Uzbek'),_('Vietnamese')
                     )
            }
        ,_('Wayuu'):
            {'code': 113
            ,'pair': ()
            }
        ,_('Welsh'):
            {'code': 48
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Wolof'),_('Yoruba'),_('Zulu'))
            }
        ,_('Wolof'):
            {'code': 112
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Welsh'),_('Yoruba'),_('Zulu'))
            }
        ,_('Yakut'):
            {'code': 384
            ,'pair': (_('Russian'),)
            }
        ,_('Yao'):
            {'code': 166
            ,'pair': ()
            }
        ,_('Yiddish'):
            {'code': 135
            ,'pair': ()
            }
        ,_('Yom'):
            {'code': 163
            ,'pair': ()
            }
        ,_('Yoruba'):
            {'code': 95
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Basque'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Estonian'),_('Filipino'),_('Finnish'),_('French'),_('Galician'),_('Georgian'),_('German'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Maori'),_('Marathi'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Russian'),_('Serbian'),_('Serbian latin'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('Spanish'),_('Swahili'),_('Swedish'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Urdu'),_('Uzbek'),_('Vietnamese'),_('Welsh'),_('Wolof'),_('Zulu'))
            }
        ,_('Zande'):
            {'code': 165
            ,'pair': ()
            }
        ,_('Zigula'):
            {'code': 464
            ,'pair': ()
            }
        ,_('Zulu'):
            {'code': 105
            ,'pair': (_('Albanian'),_('Amharic'),_('Arabic')
                     ,_('Armenian'),_('Assamese'),_('Azerbaijani')
                     ,_('Basque'),_('Bengali'),_('Bosnian')
                     ,_('Bosnian cyrillic'),_('Bulgarian'),_('Catalan')
                     ,_('Chinese'),_('Chinese Taiwan')
                     ,_('Chinese simplified'),_('Croatian'),_('Czech')
                     ,_('Danish'),_('Dutch'),_('English'),_('Estonian')
                     ,_('Filipino'),_('Finnish'),_('French')
                     ,_('Galician'),_('Georgian'),_('German'),_('Greek')
                     ,_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi')
                     ,_('Hungarian'),_('Icelandic'),_('Igbo')
                     ,_('Indonesian'),_('Inuktitut'),_('Irish')
                     ,_('IsiXhosa'),_('Italian'),_('Japanese')
                     ,_('Kannada'),_('Kazakh'),_('Khmer')
                     ,_('Kinyarwanda'),_('Kirghiz'),_('Konkani')
                     ,_('Korean'),_('Lao'),_('Latvian'),_('Lithuanian')
                     ,_('Luxembourgish'),_('Macedonian'),_('Malay')
                     ,_('Malayalam'),_('Maltese'),_('Maori')
                     ,_('Marathi'),_('Nepali'),_('Norwegian Bokmal')
                     ,_('Norwegian Nynorsk'),_('Odia'),_('Pashto')
                     ,_('Persian'),_('Polish'),_('Portuguese')
                     ,_('Punjabi'),_('Quechua'),_('Romanian')
                     ,_('Russian'),_('Serbian'),_('Serbian latin')
                     ,_('Sesotho'),_('Sesotho sa leboa'),_('Sinhala')
                     ,_('Slovak'),_('Slovenian'),_('South Ndebele')
                     ,_('Spanish'),_('Swahili'),_('Swati'),_('Swedish')
                     ,_('Tamil'),_('Tatar'),_('Telugu'),_('Thai')
                     ,_('Tsonga'),_('Tswana'),_('Turkish'),_('Turkmen')
                     ,_('Ukrainian'),_('Urdu'),_('Uzbek')
                     ,_('Vietnamese'),_('Welsh'),_('Wolof'),_('Yoruba')
                     )
            }
        }

''' This is a list of pairs (represented by language codes) that cannot be used
    owing to network errors.
'''
FLAWED = [(209,71),(209,31),(209,47),(209,81),(209,10),(209,41)
         ,(209,82),(209,25),(209,193),(209,68),(209,58),(209,19)
         ,(209,63),(209,96),(209,131),(209,15),(209,53),(209,73)
         ,(209,17),(209,98),(209,97),(209,77),(209,132),(209,8)
         ,(209,16),(209,22),(209,24),(209,1),(209,34),(209,26)
         ,(209,123),(209,99),(209,36),(209,4),(209,122),(209,124)
         ,(209,55),(209,129),(209,40),(209,3),(209,262),(209,38)
         ,(209,100),(209,101),(209,6),(209,18),(209,42),(209,50)
         ,(209,102),(209,86),(209,75),(209,103),(209,49),(209,104)
         ,(209,23),(209,28),(209,35),(209,106),(209,43),(209,79)
         ,(209,107),(209,44),(209,109),(209,39),(209,125),(209,83)
         ,(209,37),(209,27),(209,12),(209,62),(209,110),(209,65)
         ,(209,120),(209,111),(209,78),(209,133),(209,89),(209,90)
         ,(209,121),(209,64),(209,80),(209,30),(209,119),(209,127)
         ,(209,85),(209,87),(209,52),(209,14),(209,11),(209,20)
         ,(209,88),(209,13),(209,57),(209,46),(209,2),(209,130)
         ,(209,126),(209,134),(209,7),(209,114),(209,404),(209,118)
         ,(209,116),(209,60),(209,67),(209,345),(209,5),(209,108)
         ,(209,407),(209,29),(209,136),(209,91),(209,9),(209,92)
         ,(209,93),(209,458),(209,115),(209,32),(209,94),(209,33)
         ,(209,61),(209,117),(209,45),(209,171),(209,21),(209,141)
         ,(209,48),(209,112),(209,384),(209,95),(209,105),(53,71)
         ,(53,31),(124,101),(124,108),(124,29),(124,91),(124,93)
         ,(124,95),(55,17),(55,98),(55,97),(55,16),(55,22),(262,71)
         ,(262,31),(262,47),(262,81),(262,10),(262,41),(262,82)
         ,(262,25),(262,193),(262,68),(262,58),(262,19),(262,63)
         ,(262,96),(262,131),(262,15),(262,209),(262,53),(262,73)
         ,(262,17),(262,98),(262,97),(262,77),(262,132),(262,8)
         ,(262,16),(262,22),(262,24),(262,1),(262,34),(262,26)
         ,(262,123),(262,99),(262,36),(262,4),(262,122),(262,124)
         ,(262,55),(262,129),(262,40),(262,3),(262,38),(262,100)
         ,(262,101),(262,6),(262,18),(262,42),(262,50),(262,102)
         ,(262,86),(262,75),(262,103),(262,49),(262,104),(262,23)
         ,(262,28),(262,35),(262,106),(262,43),(262,79),(262,107)
         ,(262,44),(262,109),(262,39),(262,125),(262,83),(262,37)
         ,(262,27),(262,12),(262,62),(262,110),(262,65),(262,120)
         ,(262,111),(262,78),(262,133),(262,89),(262,90),(262,121)
         ,(262,64),(262,80),(262,30),(262,119),(262,127),(262,85)
         ,(262,87),(262,52),(262,14),(262,11),(262,20),(262,88)
         ,(262,13),(262,57),(262,46),(262,2),(262,130),(262,126)
         ,(262,134),(262,7),(262,114),(262,404),(262,118),(262,116)
         ,(262,60),(262,67),(262,345),(262,5),(262,108),(262,407)
         ,(262,29),(262,136),(262,91),(262,9),(262,92),(262,93)
         ,(262,458),(262,115),(262,32),(262,94),(262,33),(262,61)
         ,(262,117),(262,45),(262,171),(262,21),(262,141),(262,48)
         ,(262,112),(262,384),(262,95),(262,105),(38,73),(38,98)
         ,(38,97),(38,26),(38,79),(38,107),(38,44),(38,39),(38,27)
         ,(65,106),(65,136),(65,458),(65,171),(65,21),(65,105)
         ,(120,193),(120,68),(120,58)
         ]


class Pairs:
    
    def __init__(self):
        self.flawed = []
        self.alive = []
    
    def get_code(self,lang):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_code'
        if not lang:
            sh.com.rep_empty(f)
            return
        try:
            return LANGS[lang]['code']
        except KeyError:
            mes = _('Wrong input data: "{}"!').format(lang)
            sh.objs.get_mes(f,mes).show_error()
    
    def get_alive(self):
        if not self.alive:
            for lang in LANGS.keys():
                if LANGS[lang]['pair']:
                    self.alive.append(lang)
            self.alive.sort()
        return self.alive
    
    def get_lang(self,code):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_lang'
        if not isinstance(code,int):
            mes = _('Wrong input data: "{}"!').format(code)
            sh.objs.get_mes(f,mes).show_error()
            return
        for lang in LANGS.keys():
            if LANGS[lang]['code'] == code:
                return lang
    
    def delete_flawed(self):
        # Takes ~0.06s on AMD E-300
        f = '[MClient] plugins.multitrancom.utils.Pairs.delete_flawed'
        global LANGS
        count = 0
        nonpair1 = []
        nonpair2 = []
        for pair in self.get_flawed():
            if pair[1] in LANGS[pair[0]]['pair']:
                LANGS[pair[0]]['pair'] = list(LANGS[pair[0]]['pair'])
                nonpair1.append(pair[0])
                nonpair2.append(pair[1])
                LANGS[pair[0]]['pair'].remove(pair[1])
                LANGS[pair[0]]['pair'] = tuple(LANGS[pair[0]]['pair'])
                count += 1
            if pair[0] in LANGS[pair[1]]['pair']:
                LANGS[pair[1]]['pair'] = list(LANGS[pair[1]]['pair'])
                nonpair1.append(pair[0])
                nonpair2.append(pair[1])
                LANGS[pair[1]]['pair'].remove(pair[0])
                LANGS[pair[1]]['pair'] = tuple(LANGS[pair[1]]['pair'])
                count += 1
        # This message may be not shown, but the procedure runs anyway
        mes = _('{} items have been deleted').format(count)
        sh.objs.get_mes(f,mes,True).show_info()
        mes = []
        for i in range(len(nonpair1)):
            sub = '{}-{}'.format(nonpair1[i],nonpair2[i])
            mes.append(sub)
        mes.sort()
        mes = _('Unsupported pairs:') + ' ' + '; '.join(mes)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def get_flawed(self):
        if not self.flawed:
            for pair in FLAWED:
                self.flawed.append ((self.get_lang(pair[0])
                                    ,self.get_lang(pair[1])
                                    )
                                   )
        return self.flawed
    
    def get_pairs2(self,lang1):
        f = '[MClient] plugins.multitrancom.Pairs.get_pairs2'
        if not lang1:
            sh.com.rep_empty(f)
            return
        try:
            return sorted(LANGS[lang1]['pair'])
        except KeyError:
            mes = _('Wrong input data!')
            sh.objs.get_mes(f,mes).show_error()
    
    def get_pairs1(self,lang2):
        f = '[MClient] plugins.multitrancom.Pairs.get_pairs1'
        if not lang2:
            sh.com.rep_empty(f)
            return
        langs = [xlang for xlang in LANGS if lang2 in LANGS[xlang]['pair']]
        return sorted(langs)



class Objects:
    
    def __init__(self):
        self.pairs = None
    
    def get_pairs(self):
        if self.pairs is None:
            self.pairs = Pairs()
            self.pairs.delete_flawed()
        return self.pairs


objs = Objects()
objs.get_pairs()
