#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

import skl_shared_qt.shared as sh
from skl_shared_qt.localize import _

''' 'var MajorToMinor' sections from multitran.com do not comprise all subjects
    from 'var subjects' sections. Here we process "var subjects" sections
    (below) and supplement JSON files with absent subjects.
'''

en = ["Abbreviation", "Accounting", "Accumulators", "Acoustics", "Acridology", "Acrobatics", "Acupuncture", "Additive manufacturing & 3D printing", "Administrative geography", "Administrative law", "Advertising", "Aerial photography and topography", "Aerodynamics", "Aerohydrodynamics", "Aeronautics", "Affectionate", "Afghanistan", "Africa", "African", "Agriculture", "Agrochemistry", "Agronomy", "AIDS", "Aikido", "Air conditioners", "Air defense", "Airports and air traffic control", "Airships", "Albanian language", "Alcohol distilling", "Algebra", "Algeria", "Alkaloids", "Allergology", "Alloy addition", "Alpine skiing", "Alternative dispute resolution", "Aluminium industry", "Amateur radio service", "American (usage, not spelling)", "American English (spelling)", "American football", "American stock exchange", "Ammunition", "Ampelography", "Amphibians and reptiles", "Analytical chemistry", "Anatomy", "Ancient French", "Ancient Greek", "Ancient Hebrew", "Andalusia", "Anesthesiology", "Anglicanism", "Angling (hobby)", "Animal husbandry", "Animation and animated films", "Antarctic", "Antennas and waveguides", "Anthropology", "Anti-air artillery", "Antilles", "Antitrust law", "Apollo-Soyuz", "Applied mathematics", "Approving", "Arabic language", "Aragon", "Archaeology", "Archaic", "Archery", "Architecture", "Archiving", "Argentina", "Argot123", "Armored vehicles", "Art and culture", "Art", "Artificial intelligence", "Artillery", "ASCII", "Astringents", "Astrology", "Astrometry", "Astronautics", "Astronomy", "Astrophysics", "Astrospectroscopy", "Asturias", "Athletics", "Audio electronics", "Audit", "Augmentative", "Australia", "Australian", "Austria", "Austrian (usage)", "Automated equipment", "Automatic control", "Automobiles", "Auxilliary categories (editor use only)", "Aviation medicine", "Aviation", "Avuncular", "Bacteriology", "Badminton", "Bakery", "Ball bearings", "Ballet", "Ballistics", "Banking", "Barbarism", "Baseball", "Basketball", "Bavarian dialect", "Beekeeping", "Beijing dialect", "Belarus", "Belarusian (usage)", "Belarusian language", "Belgian (usage)", "Berlin expression", "Beverages", "Biathlon", "Bible", "Bibliography", "Billiards", "Bills", "Bioacoustics", "Biochemistry", "Bioenergy", "Biogeography", "Biology", "Biometry", "Bionics", "Biophysics", "Biotaxy", "Biotechnology", "Black slang / African-American Vernacular", "Blast-furnace practice", "Bobsley", "Bodybuilding", "Boiler equipment", "Bolivia", "Book binding", "Bookish / literary", "Botany", "Bowling", "Boxing", "Brazil", "Brewery", "Bricks", "Bridge (card game)", "Bridge construction", "British (usage, not spelling)", "British English (spelling)", "Buddhism", "Building materials", "Building structures", "Bulgarian language", "Business style", "Business", "Cables and cable production", "Calligraphy", "Canada", "Canadian", "Canning", "Cantonese", "Carcinology", "Card games", "Cardiology", "Cartography", "Caspian", "Cast iron", "Cathode-ray tubes", "Catholic", "Celestial mechanics", "Cement", "Central America", "Ceramic tiles", "Ceramics", "Chalcidology", "Champagne and sparkling wines", "Charities", "Chat and Internet slang", "Checkers", "Cheesemaking (caseiculture)", "Chemical compounds", "Chemical fibers", "Chemical industry", "Chemical nomenclature", "Chemistry", "Chess", "Childish", "Chile", "China", "Chinese", "Choreography", "Christianity", "Chromatography", "Cinema equipment", "Cinematography", "Circus", "Civil law", "Classical antiquity (excl. mythology)", "Clerical", "Cliche / convention", "Climatology", "Clinical trial", "Clothing", "Cloud technologies", "Coal", "Cockney rhyming slang", "Coelenterates", "Coffee", "Collecting", "Collective", "College vernacular", "Colloid chemistry", "Columbia", "Combating corruption", "Combustion gas turbines", "Comics", "Commerce", "Common law (Anglo-Saxon legal system)", "Communications", "Companies & Partnerships", "Companion animals", "Company name", "Compressors", "Computer games", "Computer graphics", "Computer networks", "Computer numerical control", "Computer security", "Computer tomography", "Computers", "Computing slang", "Concrete", "Confectionery", "Confucianism", "Construction", "Consulting", "Contemptuous", "Contextual meaning", "Continuous casting", "Contracts", "Conventional notation", "Converter industry", "Cooking", "Cooperage", "Copyright", "Corporate governance", "Cosmetics and cosmetology", "Costa Rica", "Countries and regions", "Court (law)", "Crafts", "Cricket", "Criminal jargon", "Criminal law", "Criminology", "Croquet", "Crustacean", "Cryptography", "Crystallography", "Cuba", "Cults and miscellaneous spiritual practices", "Cultural studies", "Curling", "Customs", "Cybernetics", "Cycle sport", "Cycling (other than sport)", "Cyprus", "Cytogenetics", "Cytology", "Czech", "Dactyloscopy", "Dams", "Dancing", "Danish", "Darts", "Data processing", "Databases", "Deafblindness", "Demography", "Dental implantology", "Dentistry", "Derbet language", "Dermatology", "Derogatory", "Desert science", "Design", "Dialectal", "Dice", "Diesel engines", "Dietology", "Digital currencies, cryptocurrencies, blockchain", "Digital sound processing", "Diminutive", "Diplomacy", "Disapproving", "Disaster recovery", "Diseases", "Distillation", "Dog breeding", "Dominican Republic", "Doping", "Dragon boat", "Dragon dance", "Drawing", "Drilling", "Drives", "Drug name", "Drug-related slang", "Drugs and addiction medicine", "Drywall", "Dutch", "Dyalysis", "Dyes", "E-mail", "Earth sciences", "East Germany", "East-Middle-German", "Eastern Chinese", "Eastern Orthodoxy", "Echinoderms", "Ecology", "Econometrics", "Economic law", "Economy", "Ecuador", "Education", "Egypt (modern state)", "Egyptian Arabic", "Egyptology", "Elections", "Electric machinery", "Electric motors", "Electric traction", "Electrical engineering", "Electricity generation", "Electricity", "Electrochemistry", "Electrolysis", "Electromedicine", "Electrometallurgy", "Electronic commerce", "Electronics", "Electrophoresis", "Electrothermy", "Elevators", "Embryology", "Emergency medical care", "Emotional values", "Emphatic", "Employment", "Enameling", "Endocrinology", "Energy distribution", "Energy industry", "Energy system", "Engineering geology", "Engineering", "Engines", "English", "Entomology", "Environment", "Epic of Jangar", "Epidemiology", "Epistolary", "Equestrian sports", "Eskimo (usage)", "Esoterics", "Esperanto", "Estonian language", "Ethnography", "Ethnology", "Ethnopsychology", "Ethology", "Euphemistic", "European Bank for Reconstruction and Development", "European Union", "Evolution", "Excavation support", "Exclamation", "Exhibitions", "Explanatory translation", "Explosives and Explosive Ordnance Disposal", "Extrusion", "Facilities", "Fairy tales", "Fantasy and science fiction", "Fashion", "Fat-and-oil industry", "Federal Bureau of Investigation", "Felinology", "Fencing", "Fermentation industry", "Fermentation", "Fertilizers", "Fiber optic", "Figurative", "Figure of speech", "Figure skating", "File extension", "Film lighting equipment", "Film processing", "Filming equipment", "Finances", "Finishing", "Finnish language", "Firefighting and fire-control systems", "Fish farming (pisciculture)", "Fishery (fishing industry)", "Floriculture", "Flour production", "Flow measurement", "Fodder", "Foil ships", "Folklore", "Food industry", "Food service and catering", "Football", "Footwear", "Foreign affairs", "Foreign exchange market", "Foreign policy", "Foreign trade", "Forensic medicine", "Forensics", "Forest chemistry", "Forestry", "Forging", "Formal", "Fortification", "Foundation engineering", "Foundry", "France", "French", "Furniture", "Gaelic", "Galicia", "Galvanizing", "Galvanoplasty", "Gambling", "Games (other than sports)", "Gardening", "Gas processing plants", "Gastroenterology", "Gear train", "Gemmology", "Genealogy", "General", "Genetic engineering", "Genetics", "Geobotanics", "Geochemistry", "Geochronology", "Geography", "Geology", "Geomechanics", "Geometry", "Geomorphology", "Geophysics", "German", "Germany", "Given name", "Glaciology", "Glass container manufacture", "Glass production", "Gloomy", "Gold mining", "Golf", "GOST", "Government, administration and public services", "Grammar", "Grammatical labels", "Grass hockey", "Gravimetry", "Greek and Roman mythology", "Greek", "Greenhouse technology", "Groceries", "Ground forces (Army)", "Guatemala", "Gymnastics", "Gynecology", "Gyroscopes", "Haberdashery", "Hacking", "Hairdressing", "Handball", "Handicraft", "Hawaii", "Health care", "Hearing aid", "Heat exchangers", "Heat transfer", "Heating", "Heavy equipment vehicles", "Hebrew", "Helicopters", "Helminthology", "Hematology", "Heraldry", "Herpetology (incl. serpentology)", "Hi-Fi", "High energy physics", "High frequency electronics", "High jump", "Hindi", "Hinduism", "Histology", "Historical figure", "Historical", "Hobbies and pastimes", "Homeopathy", "Hong Kong", "Horse breeding", "Horse racing", "Horse riding (equestrianism) & tack", "Horticulture", "Hotel industry", "Household appliances", "Hovercraft", "Human resources", "Human rights activism", "Humorous / Jocular", "Hungarian Language", "Hunting", "Hydraulic engineering", "Hydraulics", "Hydroacoustics", "Hydrobiology", "Hydroelectric power stations", "Hydrogeology", "Hydrography", "Hydrology", "Hydromechanics", "Hydrometry", "Hydroplanes", "Hygiene", "ICAO", "Ice formation", "Ice hockey", "Iceland", "Ichthyology", "Identification systems", "Idiomatic", "Iimitative (onomatopoeic)", "Immigration and citizenship", "Immunology", "India", "Indonesian", "Industrial hygiene", "Industry", "Informal", "Information security and data protection", "Information technology", "Infrared technology", "Inheritance law", "Inorganic chemistry", "Instead of", "Insurance", "Integrated circuits", "Intelligence and security services", "International Classification of Goods and Services", "International law", "International Monetary Fund", "International relations", "International trade", "International transportation", "Internet", "Invective", "Investment", "Iran", "Irish (usage, not language)", "Irish", "Ironical", "Islam", "Isolation", "Israel", "Italian", "Jamaican English", "Japan", "Japanese language", "Jargon and slang", "Jargon", "Jet engines", "Jewelry", "Journalism (terminology)", "Judaism", "Judo", "Kabaddi", "Karachaganak", "Karate", "Kayaking", "Kazakhstan", "Kick volleyball", "Knitted goods", "Korean", "Kyrgyzstan", "Labor law", "Labor organization", "Laboratory equipment", "Landscaping", "Languages", "Laser medicine", "Lasers", "Latin American slang", "Latin American", "Latin", "Law enforcement", "Law", "Lean production", "Leather", "Legal entity types (business legal structures)", "Legal theory / Jurisprudence", "Level measurement", "LGBT", "Librarianship", "Life sciences", "Light industries", "Lighting (other than cinema)", "Limnology", "Linguistics", "Literally", "Literature", "Lithology", "Loading equipment", "Loan translation", "Local name", "Logging", "Logic", "Logistics", "Logopedics", "Long jump", "Low register", "Lower German", "LP players", "Luge", "Lunfardo", "Machine components", "Machine tools", "Machinery and mechanisms", "Magnetic image recording", "Magnetic tomography", "Magnetics", "Mahjong", "Makarov", "Malacology", "Malay", "Mammalogy", "Mammals", "Management", "Manchu language", "Manga", "Manual therapy and osteopathy", "Maori", "Maritime law & Law of the Sea", "Marketing", "Martial arts and combat sports", "Mass media", "Matches", "Material safety data sheet", "Materials science", "Mathematical analysis", "Mathematics", "Meaning 1", "Meaning 2", "Meaning 3", "Meaning 4", "Measuring instruments", "Meat processing", "Mechanic engineering", "Mechanics", "Medical appliances", "Medical", "Medicine - Alternative medicine", "Melioration", "Mental health", "Merchant navy", "Metal physics", "Metal science", "Metallurgy", "Metalworking", "Meteorology", "Metro and rapid transit", "Metrology", "Mexican", "Microbiology", "Microelectronics", "Microscopy", "Microsoft", "Middle Chinese", "Middle German", "Military aviation", "Military lingo", "Military", "Milk production", "Mine surveying", "Mineral classification", "Mineral processing", "Mineral products", "Mineralogy", "Mining", "Missiles", "Misused", "Mobile and cellular communications", "Model sports", "Modern use", "Moldavian", "Molecular biology", "Molecular genetics", "Molikpaq", "Molluscs", "Money & world curencies", "Mongolian", "Morocco", "Morphology", "Motorcycles", "Mountaineering", "Multimedia", "Municipal planning", "Museums", "Music", "Musical instruments", "Mycology", "Mythology", "Name of organization", "Names and surnames", "Nanotechnology", "Narrow film", "NASA", "NASDAQ", "NATO", "Natural resourses and wildlife conservation", "Natural sciences", "Nautical", "Navigation", "Navy", "Neapolitan", "Neologism", "Nephrology", "Netherlands (usage)", "Netherlands", "Neural networks", "Neurolinguistics", "Neurology", "Neuropsychology", "Neurosurgery", "New York Stock Exchange", "New Zealand", "News style", "Non-destructive testing", "Non-governmental organizations", "Nonferrous industry", "Nonlinear optics", "Nonstandard", "Nonwoven fabric", "Norse mythology", "North American (USA and Canada)", "Northeastern Mandarin", "Northern Chinese", "Northern German", "Northern Ireland", "Norway", "Notarial practice", "Nuclear and fusion power", "Nuclear chemistry", "Nuclear physics", "Numismatics", "Nursing", "Obsolete / dated", "Obstetrics", "Occupational health & safety", "Oceanography & oceanology", "Office equipment", "Officialese", "Offshore companies", "Oil / petroleum", "Oil and gas technology", "Oil and gas", "Oil processing plants", "Oilfields", "Oils and lubricants", "Old orthography", "Old-fashioned or obsolescent", "Oncology", "Open-hearth process", "Opencast mining", "Operation systems", "Ophthalmology", "Optics (branch of physics)", "Optometry", "Ore formation", "Organic chemistry", "Organized crime", "Oriental", "Ornithology", "Orthopedics", "Outdoor activities and extreme sports", "Packaging", "Paint work", "Paint, varnish and lacquer", "Painting", "Palaeography", "Paleobotany", "Paleontology", "Paleozoology", "Palynology", "Panama", "Paragliding", "Parapsychology", "Parasciences", "Parasitology", "Patents", "Pathology", "Pedagogics", "Pediatrics", "Pejorative", "Penitentiary system", "Perfume", "Permit to work system", "Persian", "Personal protective equipment", "Peru", "Pest control", "Petanque", "Petrography", "Pets", "Phaleristics", "Pharmacology", "Pharmacy and pharmacology", "Philately / stamp collecting", "Philippines", "Philology", "Philosophy", "Phonetics", "Phonology", "Photographical sound recording", "Photography", "Photometry", "Physical chemistry", "Physical sciences", "Physics", "Physiology", "Physiotherapy", "Phytophathology", "Piezoelectric crystals", "Pigeon racing", "Pipelines", "Planning", "Plastics", "Platform diving", "Plumbing", "Pneumatics", "Poetic", "Poetry (terminology)", "Poland", "Pole vaults", "Police jargon", "Police", "Polish", "Polite", "Political economy", "Politics", "Polo", "Polygraphy", "Polymers", "Polynesian", "Pompous", "Portuguese", "Postal service", "Pottery", "Poultry farming", "Powder metallurgy", "Power electronics", "Power lines", "Power system protection", "Pragmatics", "Prefix", "Press equipment", "Printed circuit boards", "Prison slang", "Private international law", "Procedural law", "Procurement", "Product name", "Production", "Professional jargon", "Programming", "Project management", "Projectors", "Proper and figurative", "Proper name", "Protozoology", "Proverb", "Psychiatry", "Psycholinguistics", "Psychology", "Psychopathology", "Psychophysiology", "Psychotherapy", "Public law", "Public relations", "Public transportation", "Public utilities", "Publishing", "Puerto Rican Spanish", "Pulling equipment", "Pulmonology", "Pulp and paper industry", "Pumps", "Puzzle", "Quality control and standards", "Quantum electronics", "Quantum mechanics", "Quarrying", "Quotes and aphorisms", "Quran", "Racing and motorsport", "Radio", "Radioastronomy", "Radiobiology", "Radioengineering", "Radiogeodesy", "Radiography", "Radiolocation", "Radiology", "Rail transport", "Real estate", "Records management", "Refractory materials", "Refrigeration", "Regional usage (other than language varieties)", "Reinforced concrete", "Reliability", "Religion", "Remote sensing", "Research and development", "Reservoir simulation", "Resins", "Respectful", "Rhetoric", "Rhine", "Risk Management", "Ritual", "Road construction", "Road sign", "Road surface", "Road traffic", "Road works", "Robotics", "Roll stock", "Rollerblades", "Romanian", "Rowing", "Rude", "Rugby football", "Russia", "Russian (usage)", "Russian language", "Sailing ships", "Sailing", "Sakhalin A", "Sakhalin R", "Sakhalin S", "Sakhalin", "Salvadoran Spanish", "Sample preparation", "Sanitation", "Sanskrit", "SAP finance", "SAP tech.", "SAP", "Sarcastical", "Satellite communications", "Saying", "Scandinavian", "School (terminology)", "School and university subjects", "School", "Scientific", "Scotland", "Scottish (usage)", "Screenwriting", "Scuba diving", "Sculpture", "Securities", "Security systems", "Sedimentology", "Seismic resistance", "Seismology", "Selective breeding", "Semantics", "Semiconductors", "Semiotics", "Sensitometry", "Service industry", "Sewage and wastewater treatment", "Sewing and clothing industry", "Sex and sexual subcultures", "Sexology", "Shanghainese", "Shinto", "Ship handling", "Shipbuilding", "Shooting sport", "Short message service", "Show business", "Sicilian", "Signalling", "Silicate industry", "Skateboarding", "Ski jumping", "Skiing", "Skydiving", "Slang", "Slavonic", "Snowboard", "Social media", "Social science", "Socialism", "Sociolinguistics", "Sociology", "Software", "Soil mechanics", "Soil science", "Solar power", "Solid-state physics", "Somatics", "Sound engineering", "Sound recording", "South African", "South America", "South Asia", "South German", "South-West-German", "Southern Chinese", "Southern Dutch", "Soviet", "Space", "Spain", "Spanish-American", "Spanish", "Spectroscopy", "Speech disorders", "Speed skating", "Speleology", "Spices", "Spinning", "Spoken", "Sporting goods", "Sports", "Stamping", "Starch industry", "Stationery", "Statistics", "Steam boilers", "Steel production", "Stereo", "Stock Exchange", "Stonemasonry", "Stratified plastics", "Stratigraphy", "Strength of materials", "Stylistic values", "Stylistics", "Subjects for Chinese dictionaries", "Sublime", "Submarines", "Subsurface mining", "Sugar production", "Sumo", "Superconductivity", "Superlative", "Surfing, windsurfing, SUP surfing", "Surgery", "Surname", "Survey", "Surveying", "Swedish", "Swimming", "Swiss term", "Switches", "Syntax", "Table tennis", "Tabletop games", "Taboo expressions and obscenities", "Taekwondo", "Tagmemics", "Taiwan", "Taoism", "Tatar", "Tauromachy", "Taxation of forests", "Taxes", "Technology", "Tectonics", "Teenager slang", "Telecommunications", "Telegraphy", "Telemechanics", "Telephony", "Television", "Tenders", "Tengiz", "Tennis", "Teratology", "Textile industry", "Thai", "Theatre", "Theology", "Thermal Energy", "Thermal engineering", "Thermodynamics", "Throw", "Tibetan", "Timber floating", "Timberwork", "Tinware", "Titles of works of art", "Tobacco industry", "Tools", "Topography", "Topology", "Toponym", "Torgut language", "Torpedoes", "Toxicology", "Toys", "Trade classification", "Trade unions", "Trademark", "Traditional medicine", "Traffic control", "Trampolining", "Transformers", "Translator's false friend", "Transplantology", "Transport", "Traumatology", "Travel", "Tribology", "Trucks/Lorries", "Tunneling", "Turbines", "Turk", "Turkey", "Turkish language", "Tuscan", "Typewriters and typewriting", "Typography", "Typology", "Ufology", "Ukraine", "Ukrainian (usage)", "Ukrainian language", "Ultrasound", "Uncommon / rare", "Unit measures", "United Kingdom", "United Nations", "United States", "University", "Urology", "Uruguayan Spanish", "Vacuum technique", "Vacuum tubes", "Valves", "Venereology", "Venezuela", "Ventilation", "Verbatim", "Verlan", "Vernacular language", "Veterinary medicine", "Vibration monitoring", "Video recording", "Vienna dialect", "Vietnamese", "Virology", "Volcanology", "Volleyball", "Vulgar", "Wales", "Warehouse", "Waste management", "Watchmaking", "Water polo", "Water resources", "Water supply", "Waterskiing", "Weapons and gunsmithing", "Weapons of mass destruction", "Weaving", "Weightlifting", "Welding", "Welfare & Social Security", "Well control", "Wellness", "West Indies", "West-German", "Wind Energy", "Winding", "Windows", "Wine growing", "Wine tasting", "Winemaking", "Wire drawing", "Wiring", "Wood processing", "Wood, pulp and paper industries", "Word formation", "Work flow", "World trade organization", "Wrestling", "Written", "Wushu", "Yachting", "Yiddish", "Zoology", "Zootechnics"]
ru = []
de = []
es = []
uk = []
pl = []
zh = []


class Unique:
    
    def __init__(self, file, majors):
        self.Success = True
        self.not_found = []
        self.subjects = {}
        self.majors = majors
        self.file = file
    
    def load(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        text = sh.ReadTextFile(self.file).get()
        if not text:
            self.Success = False
            sh.com.rep_empty(f)
            return
        try:
            self.subjects = json.loads(text)
        except Exception as e:
            self.Success = False
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            sh.objs.get_mes(f, mes).show_error()
    
    def _search(self, subject):
        for key, value in self.subjects.items():
            if key == subject:
                return True
            if subject in value:
                return True
    
    def search(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.search'
        if not self.Success:
            sh.com.cancel(f)
            return
        for major in self.majors:
            if not self._search(major):
                self.not_found.append(major)
    
    def report(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.report'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.not_found:
            mes = _('All subjects have been found!')
            sh.objs.get_mes(f, mes).show_info()
            return
        mes = [f'{f}:']
        sub = _('Subjects that have not been found: {}')
        sub = sub.format(len(self.not_found))
        mes.append(sub)
        mes.append('')
        mes += self.not_found
        return '\n'.join(mes)
    
    def add(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.add'
        if not self.Success:
            sh.com.cancel(f)
            return
        for subject in self.not_found:
            self.subjects[subject] = {}
    
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.debug'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            dic = json.dumps(self.subjects, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
            return
        return f'{f}:\n{dic}'
    
    def sort(self):
        f = '[MClient] plugins.multitrancom.utils.subjects.absent_subjects.Unique.sort'
        if not self.Success:
            sh.com.cancel(f)
            return
        subjects = {}
        keys = sorted(self.subjects.keys())
        for key in keys:
            values = sorted(self.subjects[key])
            subjects[key] = {}
            for value in values:
                subjects[key][value] = {}
        self.subjects = subjects
    
    def run(self):
        self.load()
        self.search()
        self.add()
        self.sort()



class Loop:
    
    def __init__(self):
        self.Success = True
        self.langs = ('en', 'ru', 'de', 'es', 'uk', 'pl', 'zh')
        self.lang = 'en'
        self.file_ptrn = sh.objs.get_pdir().add ('..', '..', '..', '..', '..'
                                                ,'resources', 'plugins'
                                                ,'multitrancom', 'subjects'
                                                ,'{}.json'
                                                )
        self.file = ''
    
    def set_input(self):
        f = '[MClientQt] plugins.multitrancom.utils.subjects.absent_subjects.Loop.set_input'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.lang == 'en':
            self.data = en
        elif self.lang == 'ru':
            self.data = ru
        elif self.lang == 'de':
            self.data = de
        elif self.lang == 'es':
            self.data = es
        elif self.lang == 'uk':
            self.data = uk
        elif self.lang == 'pl':
            self.data = pl
        elif self.lang == 'zh':
            self.data = zh
        else:
            self.Success = False
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.lang, ', '.join(self.langs))
            sh.objs.get_mes(f, mes).show_warning()
            return
        self.file = self.file_ptrn.format(self.lang)
    
    def loop(self):
        for self.lang in self.langs:
            self.set_input()
            iunique = Unique(self.file, self.data)
            iunique.run()
            self.Success = iunique.Success
            if not self.Success:
                return
    
    def run(self):
        self.loop()
        return self.Success


if __name__ == '__main__':
    f = '[MClientQt] plugins.multitrancom.utils.subjects.absent_subjects.__main__'
    sh.com.start()
    file = '/home/pete/bin/mclientqt/resources/plugins/multitrancom/subjects/en.json'
    iunique = Unique(file, en)
    iunique.run()
    #idebug = sh.Debug(f, iunique.report())
    idebug = sh.Debug(f, iunique.debug())
    idebug.show()
    sh.com.end()
