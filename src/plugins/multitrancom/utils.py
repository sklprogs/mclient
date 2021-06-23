#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import os
import html
import operator
import urllib.request
from skl_shared.localize import _
import skl_shared.shared as sh


''' It seems to be highly difficult to extract short-full title pairs
    since, unlike multitran.ru, there are no '<a title' tags, such
    cases are coded as usual URLs. Use 'Commands.run_missing_titles' to
    manually fill up new titles.
'''


class Groups:
    
    def __init__(self):
        ''' Log in at multitran.com, select an article, click 'Add' and
            copy the value of 'var MajorToMinor='.
        '''
        self.lst = ["Computing", "Information technology", "Computing", "SAP", "Computing", "Computer networks", "Computing", "Programming", "Computing", "Operation systems", "Computing", "Data processing", "Computing", "Neural networks", "Computing", "Internet", "Computing", "File extension", "Computing", "SAP tech.", "Computing", "SAP finance", "Computing", "Computer graphics", "Computing", "Computer games", "Computing", "Microsoft", "Computing", "Hacking", "Computing", "Chat and Internet slang", "Computing", "Software", "Computing", "Databases", "Computing", "Office equipment", "Computing", "Information security", "Computing", "Social media", "Computing", "Artificial intelligence", "Computing", "Computing slang", "Computing", "E-mail", "Computing", "Computer security", "Computing", "ASCII", "Geology", "Mineralogy", "Geology", "Geophysics", "Geology", "Seismology", "Geology", "Tectonics", "Geology", "Petrography", "Geology", "Geomorphology", "Geology", "Geochemistry", "Geology", "Hydrogeology", "Geology", "Crystallography", "Geology", "Lithology", "Geology", "Stratigraphy", "Geology", "Volcanology", "Geology", "Engineering geology", "Geology", "Spectroscopy", "Geology", "Geochronology", "Geology", "Mineral classification", "Geology", "Geomechanics", "Geology", "Mineral products", "Geology", "Soil science", "Geology", "Glaciology", "Geology", "Reservoir simulation", "Geology", "Speleology", "Geology", "Gemmology", "Geology", "Sedimentology", "Biology", "Zoology", "Biology", "Botany", "Biology", "Anatomy", "Biology", "Entomology", "Biology", "Embryology", "Biology", "Biophysics", "Biology", "Genetics", "Biology", "Microbiology", "Biology", "Cytology", "Biology", "Helminthology", "Biology", "Biochemistry", "Biology", "Paleontology", "Biology", "Ichthyology", "Biology", "Biotechnology", "Biology", "Genetic engineering", "Biology", "Molecular genetics", "Biology", "Cytogenetics", "Biology", "Biotaxy", "Biology", "Paleobotany", "Biology", "Herpetology (incl. serpentology)", "Biology", "Ethology", "Biology", "Palynology", "Biology", "Mycology", "Biology", "Ornithology", "Biology", "Biogeography", "Biology", "Protozoology", "Biology", "Malacology", "Biology", "Bioacoustics", "Biology", "Evolution", "Biology", "Carcinology", "Biology", "Geobotanics", "Biology", "Molecular biology", "Biology", "Chalcidology", "Biology", "Amphibians and reptiles", "Biology", "Mammals", "Biology", "Paleozoology", "Biology", "Acridology", "Biology", "Ampelography", "Biology", "Hydrobiology", "Aviation", "Aeronautics", "Aviation", "Navigation", "Aviation", "Aerial photography and topography", "Aviation", "Aviation medicine", "Aviation", "Military aviation", "Aviation", "Airports and air traffic control", "Aviation", "Helicopters", "Aviation", "Hydroplanes", "Aviation", "Airships", "Aviation", "ICAO", "Nautical", "Foil ships", "Nautical", "Navigation", "Nautical", "Navy", "Nautical", "Yachting", "Nautical", "Fishery (fishing industry)", "Nautical", "Shipbuilding", "Nautical", "Hovercraft", "Nautical", "Submarines", "Nautical", "Sailing ships", "Nautical", "Merchant navy", "Nautical", "Maritime law & Law of the Sea", "Nautical", "Ship handling", "Medical", "Psychiatry", "Medical", "Veterinary medicine", "Medical", "Surgery", "Medical", "Obstetrics", "Medical", "Anesthesiology", "Medical", "Ophthalmology", "Medical", "Gastroenterology", "Medical", "Dentistry", "Medical", "Laboratory equipment", "Medical", "Gynecology", "Medical", "Oncology", "Medical", "Urology", "Medical", "Neurosurgery", "Medical", "Orthopedics", "Medical", "Pediatrics", "Medical", "Sanitation", "Medical", "Traumatology", "Medical", "Diseases", "Medical", "Chromatography", "Medical", "Transplantology", "Medical", "Aviation medicine", "Medical", "Drug name", "Medical", "Drugs and addiction medicine", "Medical", "Electromedicine", "Medical", "Psychotherapy", "Medical", "Laser medicine", "Medical", "Pharmacy", "Medical", "Health care", "Medical", "Clinical trial", "Medical", "AIDS", "Medical", "Nursing", "Medical", "Optometry", "Medical", "Deafblindness", "Medical", "Logopedics", "Medical", "Physiotherapy", "Medical", "Speech disorders", "Medical", "Emergency medical care", "Dialectal", "Southern Chinese", "Dialectal", "Cantonese", "Dialectal", "Ritual", "Dialectal", "Shanghainese", "Dialectal", "Northeastern Mandarin", "Dialectal", "Beijing dialect", "Dialectal", "Vienna dialect", "Dialectal", "Eastern Chinese", "Dialectal", "Jamaican English", "Dialectal", "Northern Chinese", "Dialectal", "Salvadoran Spanish", "Dialectal", "Uruguayan Spanish", "Dialectal", "Torgut language", "Dialectal", "Derbet language", "Dialectal", "Sicilian", "Dialectal", "Middle Chinese", "Sports", "Chess", "Sports", "Polo", "Sports", "Doping", "Sports", "Kick volleyball", "Sports", "Croquet", "Sports", "Baseball", "Sports", "Football", "Sports", "Petanque", "Sports", "Fencing", "Sports", "Hockey", "Sports", "Figure skating", "Sports", "Billiards", "Sports", "Yachting", "Sports", "Bodybuilding", "Sports", "Basketball", "Sports", "American football", "Sports", "Horse racing", "Sports", "Sailing", "Sports", "Gymnastics", "Sports", "Shooting sport", "Sports", "Cycle sport", "Sports", "Skiing", "Sports", "Platform diving", "Sports", "Throw", "Sports", "Equestrianism", "Sports", "Ski jumping", "Sports", "Athletics", "Sports", "Luge", "Sports", "Rowing", "Sports", "Swimming", "Sports", "Handball", "Sports", "Volleyball", "Sports", "Tennis", "Sports", "Long jump", "Sports", "High jump", "Sports", "Speed skating", "Sports", "Table tennis", "Sports", "Trampolining", "Sports", "Archery", "Sports", "Water polo", "Sports", "Rugby football", "Sports", "Pole vaults", "Sports", "Weightlifting", "Sports", "Acrobatics", "Sports", "Biathlon", "Sports", "Curling", "Sports", "Sporting goods", "Sports", "Racing and motorsport", "Sports", "Badminton", "Military", "Artillery", "Military", "Military lingo", "Military", "Radiolocation", "Military", "Missiles", "Military", "Aerial photography and topography", "Military", "Weapons of mass destruction", "Military", "Ground forces (Army)", "Military", "Navy", "Military", "Armored vehicles", "Military", "NATO", "Military", "Air defense", "Military", "Anti-air artillery", "Military", "Explosives", "Military", "Military aviation", "Military", "Intelligence and security services", "Military", "Torpedoes", "Military", "Fortification", "Military", "Ammunition", "Philosophy", "Logic", "Technology", "Laboratory equipment", "Technology", "Fiber optic", "Technology", "Cybernetics", "Technology", "Metrology", "Technology", "Refrigeration", "Technology", "Welding", "Technology", "Household appliances", "Technology", "Automated equipment", "Technology", "Extrusion", "Technology", "Robotics", "Technology", "Tools", "Technology", "Microscopy", "Technology", "Automatic control", "Technology", "Measuring instruments", "Technology", "Isolation", "Technology", "Accumulators", "Technology", "Drives", "Technology", "Switches", "Technology", "Lighting (other than cinema)", "Technology", "Winding", "Technology", "SAP tech.", "Technology", "Sensitometry", "Technology", "Disaster recovery", "Technology", "Infrared technology", "Technology", "Level measurement", "Technology", "Nanotechnology", "Technology", "Air conditioners", "Technology", "Lasers", "Technology", "Vibration monitoring", "Technology", "Gyroscopes", "Technology", "Additive manufacturing & 3D printing", "Technology", "Photometry", "Agriculture", "Gardening", "Agriculture", "Fish farming (pisciculture)", "Agriculture", "Beekeeping", "Agriculture", "Melioration", "Agriculture", "Soil science", "Agriculture", "Poultry farming", "Agriculture", "Meat processing", "Agriculture", "Horse breeding", "Agriculture", "Floriculture", "Agriculture", "Milk production", "Agriculture", "Wine growing", "Agriculture", "Selective breeding", "Agriculture", "Phytophathology", "Agriculture", "Fodder", "Agriculture", "Zootechnics", "Agriculture", "Agrochemistry", "Agriculture", "Horticulture", "Agriculture", "Greenhouse technology", "Agriculture", "Animal husbandry", "Agriculture", "Pest control", "Agriculture", "Agronomy", "Agriculture", "Fertilizers", "Historical", "Archaeology", "Historical", "Heraldry", "Historical", "Classical antiquity (excl. mythology)", "Historical", "Anthropology", "Historical", "Egyptology", "Historical", "Socialism", "Historical", "East Germany (history)", "Historical", "Genealogy", "Historical", "Soviet", "Historical", "Cultural studies", "Historical", "Historical figure", "Historical", "Palaeography", "Chemistry", "Biochemistry", "Chemistry", "Laboratory equipment", "Chemistry", "Geochemistry", "Chemistry", "Forest chemistry", "Chemistry", "Chromatography", "Chemistry", "Spectroscopy", "Chemistry", "Physical chemistry", "Chemistry", "Electrochemistry", "Chemistry", "Agrochemistry", "Chemistry", "Alkaloids", "Chemistry", "Chemical nomenclature", "Chemistry", "Nuclear chemistry", "Chemistry", "Organic chemistry", "Chemistry", "Chemical compounds", "Chemistry", "Distillation", "Chemistry", "Colloid chemistry", "Chemistry", "Inorganic chemistry", "Chemistry", "Dyalysis", "Chemistry", "Electrolysis", "Construction", "Architecture", "Construction", "Road works", "Construction", "Heavy equipment vehicles", "Construction", "Welding", "Construction", "Plumbing", "Construction", "Paint work", "Construction", "Tools", "Construction", "Reinforced concrete", "Construction", "Wiring", "Construction", "Foundation engineering", "Construction", "Stonemasonry", "Construction", "Tunneling", "Construction", "Soil mechanics", "Construction", "Building structures", "Construction", "Valves", "Construction", "Road construction", "Construction", "Landscaping", "Construction", "Windows", "Construction", "Bridge construction", "Construction", "Road surface", "Construction", "Pipelines", "Construction", "Municipal planning", "Construction", "Dams", "Mathematics", "Statistics", "Mathematics", "Geometry", "Mathematics", "Algebra", "Mathematics", "Applied mathematics", "Mathematics", "Topology", "Mathematics", "Mathematical analysis", "Mathematics", "Gravimetry", "Mathematics", "Econometrics", "Religion", "Clerical", "Religion", "Bible", "Religion", "Quran", "Religion", "Eastern Orthodoxy", "Religion", "Catholic", "Religion", "Christianity", "Religion", "Judaism", "Religion", "Buddhism", "Religion", "Shinto", "Religion", "Cults and miscellaneous spiritual practices", "Religion", "Taoism", "Religion", "Islam", "Religion", "Confucianism", "Religion", "Hinduism", "Law", "Alternative dispute resolution", "Law", "Contracts", "Law", "Common law (Anglo-Saxon legal system)", "Law", "Patents", "Law", "Criminal law", "Law", "Bills", "Law", "Copyright", "Law", "Inheritance law", "Law", "Notarial practice", "Law", "Labor law", "Law", "Private international law", "Law", "Procedural law", "Law", "Public law", "Law", "Legal theory", "Law", "Administrative law", "Law", "International law", "Law", "Economic law", "Law", "Civil law", "Law", "Civil procedure", "Law", "Maritime law & Law of the Sea", "Law", "Antitrust law", "Law", "Court (law)", "Economy", "Commerce", "Economy", "Insurance", "Economy", "Trade classification", "Economy", "Investment", "Economy", "Foreign trade", "Economy", "World trade organization", "Economy", "Marketing", "Economy", "Political economy", "Economy", "International trade", "Economy", "Employment", "Linguistics", "Grammar", "Linguistics", "Stylistics", "Linguistics", "Phonetics", "Linguistics", "Psycholinguistics", "Linguistics", "Phonology", "Linguistics", "Pragmatics", "Linguistics", "Syntax", "Linguistics", "Morphology", "Linguistics", "Semantics", "Linguistics", "Typology", "Linguistics", "Semiotics", "Linguistics", "Sociolinguistics", "Linguistics", "Tagmemics", "Linguistics", "Neurolinguistics", "Finances", "Accounting", "Finances", "Insurance", "Finances", "Stock Exchange", "Finances", "Banking", "Finances", "Audit", "Finances", "Foreign exchange market", "Finances", "Investment", "Finances", "European Bank for Reconstruction and Development", "Finances", "Currencies and monetary policy", "Finances", "SAP finance", "Finances", "Securities", "Finances", "NASDAQ", "Finances", "New York Stock Exchange", "Finances", "American stock exchange", "Finances", "International Monetary Fund", "Finances", "Charities", "Finances", "Digital and cryptocurrencies", "Finances", "Offshore companies", "Geography", "Meteorology", "Geography", "Hydrography", "Geography", "Topography", "Geography", "Ethnography", "Geography", "Cartography", "Geography", "Demography", "Geography", "Seismology", "Geography", "Geomorphology", "Geography", "Oceanography (oceanology)", "Geography", "Aerial photography and topography", "Geography", "Soil science", "Geography", "Ice formation", "Geography", "Antarctic", "Geography", "Hydrology", "Geography", "Ethnology", "Geography", "Earth sciences", "Geography", "Climatology", "Geography", "Limnology", "Geography", "Remote sensing", "Geography", "Hydrometry", "Geography", "Administrative geography", "Mining", "Ore formation", "Mining", "Drilling", "Mining", "Mineral processing", "Mining", "Mine surveying", "Mining", "Gold mining", "Mining", "Coal", "Mining", "Quarrying", "Cinematography", "Cinema equipment", "Cinematography", "Narrow film", "Cinematography", "Film lighting equipment", "Cinematography", "Photographical sound recording", "Cinematography", "Projectors", "Cinematography", "Sound recording", "Cinematography", "Film processing", "Cinematography", "Filming equipment", "Cinematography", "Magnetic image recording", "Cinematography", "Animation and animated films", "Cinematography", "Sound engineering", "Cooking", "Confectionery", "Cooking", "Spices", "Cooking", "Beverages", "Martial arts and combat sports", "Karate", "Martial arts and combat sports", "Boxing", "Martial arts and combat sports", "Aikido", "Martial arts and combat sports", "Wrestling", "Martial arts and combat sports", "Judo", "Martial arts and combat sports", "Sumo", "Martial arts and combat sports", "Wushu", "Martial arts and combat sports", "Taekwondo", "Metallurgy", "Roll stock", "Metallurgy", "Blast-furnace practice", "Metallurgy", "Open-hearth process", "Metallurgy", "Continuous casting", "Metallurgy", "Nonferrous industry", "Metallurgy", "Powder metallurgy", "Metallurgy", "Forging", "Metallurgy", "Metal science", "Metallurgy", "Electrothermy", "Metallurgy", "Electrometallurgy", "Metallurgy", "Foundry", "Metallurgy", "Aluminium industry", "Metallurgy", "Alloy addition", "Metallurgy", "Steel production", "Metallurgy", "Cast iron", "Mythology", "Greek and Roman mythology", "Mythology", "Norse mythology", "Mythology", "Hinduism", "Politics", "Foreign policy", "Politics", "Disaster recovery", "Politics", "International relations", "Politics", "Elections", "Politics", "Public relations", "Psychology", "Psychotherapy", "Psychology", "Psychophysiology", "Psychology", "Mental health", "Psychology", "Psycholinguistics", "Psychology", "Ethnopsychology", "Psychology", "Neuropsychology", "Psychology", "Psychopathology", "Physics", "Optics (branch of physics)", "Physics", "Biophysics", "Physics", "Mechanics", "Physics", "Magnetics", "Physics", "Nuclear physics", "Physics", "Acoustics", "Physics", "Hydraulics", "Physics", "Quantum mechanics", "Physics", "Nonlinear optics", "Physics", "Metal physics", "Physics", "Spectroscopy", "Physics", "Solid-state physics", "Physics", "Quantum electronics", "Physics", "Tribology", "Physics", "Aerodynamics", "Physics", "Thermodynamics", "Physics", "Aerohydrodynamics", "Physics", "Astrophysics", "Physics", "Ballistics", "Physics", "Heat transfer", "Physics", "Hydroacoustics", "Physics", "Electricity", "Physics", "Piezoelectric crystals", "Photography", "Film processing", "Electronics", "Integrated circuits", "Electronics", "Cathode-ray tubes", "Electronics", "Microelectronics", "Electronics", "High frequency electronics", "Electronics", "Printed circuit boards", "Electronics", "Vacuum tubes", "Electronics", "Power electronics", "Literature", "Poetry (terminology)", "Literature", "Fantasy and science fiction", "Literature", "Librarianship", "Literature", "Quotes and aphorisms", "Literature", "Fairy tales", "Literature", "Titles of works of art", "Literature", "Screenwriting", "Folklore", "Proverb", "Folklore", "Saying", "Folklore", "Puzzle", "Sociology", "Survey", "Communications", "Radio", "Communications", "Telecommunications", "Communications", "Postal service", "Communications", "Telephony", "Communications", "Telegraphy", "Communications", "Internet", "Communications", "Telemechanics", "Communications", "Short message service", "Communications", "Satellite communications", "Communications", "Antennas and waveguides", "Communications", "Mobile and cellular communications", "Communications", "E-mail", "Transport", "Railway term", "Transport", "Automobiles", "Transport", "Road works", "Transport", "Road traffic", "Transport", "Cycling (other than sport)", "Transport", "Motorcycles", "Transport", "Trucks/Lorries", "Transport", "Road sign", "Transport", "International transportation", "Transport", "Oils and lubricants", "Transport", "Metro and rapid transit", "Transport", "Helicopters", "Transport", "Traffic control", "Transport", "Public transportation", "Food industry", "Confectionery", "Food industry", "Canning", "Food industry", "Sugar production", "Food industry", "Brewery", "Food industry", "Meat processing", "Food industry", "Alcohol distilling", "Food industry", "Milk production", "Food industry", "Flour production", "Food industry", "Bakery", "Food industry", "Cheesemaking (caseiculture)", "Food industry", "Starch industry", "Food industry", "Fat-and-oil industry", "Food industry", "Glass container manufacture", "Food industry", "Winemaking", "Food industry", "Fermentation", "Food industry", "Champagne and sparkling wines", "Food industry", "Coffee", "Food industry", "Beverages", "Food industry", "Groceries", "Food industry", "Wine tasting", "Energy industry", "Nuclear and fusion power", "Energy industry", "Hydroelectric power stations", "Energy industry", "Solar power", "Energy industry", "Transformers", "Energy industry", "Power lines", "Energy industry", "Energy system", "Energy industry", "Energy distribution", "Energy industry", "Power system protection", "Energy industry", "Wind Energy", "Energy industry", "Thermal Energy", "Energy industry", "Bioenergy", "Energy industry", "Electricity generation", "Mass media", "Radio", "Mass media", "Television", "Mass media", "Advertising", "Mass media", "Internet", "Mass media", "Journalism (terminology)", "Business", "Alternative dispute resolution", "Business", "Commerce", "Business", "Contracts", "Business", "Business style", "Business", "Trademark", "Business", "Advertising", "Business", "Trade classification", "Business", "Investment", "Business", "Companies & Partnerships", "Business", "Exhibitions", "Business", "Human resources", "Business", "Corporate governance", "Business", "Public relations", "Business", "Consulting", "Business", "Electronic commerce", "Business", "Legal entity types (business legal structures)", "Business", "Offshore companies", "Publishing", "Polygraphy", "Publishing", "Copyright", "Publishing", "Typography", "Publishing", "Book binding", "Engineering", "Architecture", "Engineering", "Surveying", "Engineering", "Strength of materials", "Engineering", "Thermal engineering", "Engineering", "Refrigeration", "Engineering", "Hydraulics", "Engineering", "Heating", "Engineering", "Drawing", "Engineering", "Radiogeodesy", "Engineering", "Bionics", "Engineering", "Tunneling", "Engineering", "Soil mechanics", "Engineering", "Building structures", "Engineering", "Water supply", "Engineering", "Ventilation", "Engineering", "Valves", "Engineering", "Air conditioners", "Engineering", "Heat exchangers", "Engineering", "Landscaping", "Engineering", "Hydromechanics", "Engineering", "Sewage and wastewater treatment", "Engineering", "Pipelines", "Engineering", "Hydraulic engineering", "Engineering", "Municipal planning", "Engineering", "Seismic resistance", "Engineering", "Design", "Production", "Labor organization", "Production", "Packaging", "Production", "Planning", "Production", "Converter industry", "Production", "Jewelry", "Production", "Industrial hygiene", "Production", "Facilities", "Production", "Glass production", "Production", "Ceramics", "Production", "Trade unions", "Production", "Permit to work system", "Production", "Personal protective equipment", "Production", "Tinware", "Management", "Labor organization", "Management", "Human resources", "Management", "Project management", "Management", "Corporate governance", "Management", "Risk Management", "Education", "University", "Education", "School and university subjects", "Education", "Social science", "Education", "Physical sciences", "Education", "Pedagogics", "Industry", "Mechanic engineering", "Industry", "Silicate industry", "Industry", "Press equipment", "Industry", "Stamping", "Industry", "Wire drawing", "Industry", "Industrial hygiene", "Industry", "Waste management", "Industry", "Tobacco industry", "Industry", "Machine tools", "Industry", "Materials science", "Industry", "Metalworking", "Occupational health & safety", "Permit to work system", "Occupational health & safety", "Personal protective equipment", "Philology", "Rhetoric", "Philology", "Palaeography", "Travel", "Hotel industry", "Quality control and standards", "Reliability", "Quality control and standards", "Non-destructive testing", "Quality control and standards", "GOST", "Medical appliances", "Electrophoresis", "Medical appliances", "Microscopy", "Medical appliances", "Dental implantology", "Medical appliances", "Radiography", "Medical appliances", "Hearing aid", "Medical appliances", "Magnetic tomography", "Medical appliances", "Computer tomography", "Medical appliances", "Ultrasound", "Machinery and mechanisms", "Engines", "Machinery and mechanisms", "Automated equipment", "Machinery and mechanisms", "Watchmaking", "Machinery and mechanisms", "Electric machinery", "Machinery and mechanisms", "Electric traction", "Machinery and mechanisms", "Elevators", "Machinery and mechanisms", "Machine components", "Machinery and mechanisms", "Combustion gas turbines", "Machinery and mechanisms", "Pumps", "Machinery and mechanisms", "Gear train", "Machinery and mechanisms", "Jet engines", "Machinery and mechanisms", "Turbines", "Machinery and mechanisms", "Pneumatics", "Machinery and mechanisms", "Electric motors", "Machinery and mechanisms", "Ball bearings", "Security systems", "Cryptography", "Security systems", "Signalling", "Security systems", "Biometry", "Security systems", "Infrared technology", "Security systems", "Information security", "Security systems", "Computer security", "Security systems", "Identification systems", "Security systems", "Video recording", "Oil and gas", "Oil / petroleum", "Oil and gas", "Drilling", "Oil and gas", "Sakhalin", "Oil and gas", "Oil and gas technology", "Oil and gas", "Oilfields", "Oil and gas", "Sakhalin R", "Oil and gas", "Sakhalin S", "Oil and gas", "Sakhalin A", "Oil and gas", "Well control", "Oil and gas", "Molikpaq", "Oil and gas", "Gas processing plants", "Oil and gas", "Oil processing plants", "Oil and gas", "Tengiz", "Oil and gas", "Karachaganak", "Oil and gas", "Caspian", "Oil and gas", "Flow measurement", "Oil and gas", "Oils and lubricants", "Regional usage (other than language varieties)", "American (usage, not AmE)", "Regional usage (other than language varieties)", "Eskimo (usage)", "Regional usage (other than language varieties)", "Australian", "Regional usage (other than language varieties)", "South African", "Regional usage (other than language varieties)", "Ukrainian (usage)", "Regional usage (other than language varieties)", "New Zealand", "Regional usage (other than language varieties)", "Netherlands (usage)", "Regional usage (other than language varieties)", "British (usage, not BrE)", "Regional usage (other than language varieties)", "Irish (usage, not language)", "Regional usage (other than language varieties)", "Canadian", "Regional usage (other than language varieties)", "Scottish (usage)", "Regional usage (other than language varieties)", "Austrian (usage)", "Regional usage (other than language varieties)", "Rhine", "Regional usage (other than language varieties)", "Swiss term", "Regional usage (other than language varieties)", "South German", "Regional usage (other than language varieties)", "Northern German", "Regional usage (other than language varieties)", "Berlin expression", "Regional usage (other than language varieties)", "East-Middle-German", "Regional usage (other than language varieties)", "South-West-German", "Regional usage (other than language varieties)", "Middle German", "Regional usage (other than language varieties)", "Lower German", "Regional usage (other than language varieties)", "West-German", "Regional usage (other than language varieties)", "Local name", "Regional usage (other than language varieties)", "Mexican", "Regional usage (other than language varieties)", "North American (USA and Canada)", "Regional usage (other than language varieties)", "Slavonic", "Regional usage (other than language varieties)", "Oriental", "Regional usage (other than language varieties)", "Puerto Rican Spanish", "Regional usage (other than language varieties)", "Salvadoran Spanish", "Regional usage (other than language varieties)", "Uruguayan Spanish", "Regional usage (other than language varieties)", "Ecuador", "Regional usage (other than language varieties)", "Belgian (usage)", "Regional usage (other than language varieties)", "Indonesian", "Regional usage (other than language varieties)", "Southern Dutch", "Regional usage (other than language varieties)", "Polynesian", "Regional usage (other than language varieties)", "Tuscan", "Regional usage (other than language varieties)", "Neapolitan", "Regional usage (other than language varieties)", "Latin American", "Regional usage (other than language varieties)", "African", "Logistics", "Warehouse", "Logistics", "Procurement", "Logistics", "Loading equipment", "Logistics", "International transportation", "Foreign affairs", "Diplomacy", "Foreign affairs", "Foreign policy", "Foreign affairs", "International relations", "Foreign affairs", "Immigration and citizenship", "Building materials", "Concrete", "Building materials", "Bricks", "Building materials", "Refractory materials", "Building materials", "Paint, varnish and lacquer", "Building materials", "Cement", "Building materials", "Ceramic tiles", "Building materials", "Astringents", "Building materials", "Drywall", "Space", "Astronomy", "Space", "Astronautics", "Space", "Missiles", "Space", "Astrometry", "Space", "Astrophysics", "Space", "Radioastronomy", "Space", "Celestial mechanics", "Space", "Astrospectroscopy", "Space", "NASA", "Space", "Apollo-Soyuz", "Space", "Remote sensing", "Electrical engineering", "Transformers", "Electrical engineering", "Semiconductors", "Electrical engineering", "Tools", "Electrical engineering", "Cables and cable production", "Electrical engineering", "Electric machinery", "Electrical engineering", "Measuring instruments", "Electrical engineering", "Isolation", "Electrical engineering", "Power system protection", "Electrical engineering", "Electricity", "Electrical engineering", "Electric motors", "Electrical engineering", "Power electronics", "Electrical engineering", "Superconductivity", "United Nations", "World trade organization", "United Nations", "International Monetary Fund", "United Nations", "ICAO", "Life sciences", "Psychiatry", "Life sciences", "Pharmacology", "Life sciences", "Bacteriology", "Life sciences", "Physiology", "Life sciences", "Allergology", "Life sciences", "Cardiology", "Life sciences", "Anesthesiology", "Life sciences", "Ophthalmology", "Life sciences", "Radiology", "Life sciences", "Immunology", "Life sciences", "Neurology", "Life sciences", "Gastroenterology", "Life sciences", "Hematology", "Life sciences", "Dermatology", "Life sciences", "Pathology", "Life sciences", "Teratology", "Life sciences", "Parasitology", "Life sciences", "Histology", "Life sciences", "Virology", "Life sciences", "Toxicology", "Life sciences", "Oncology", "Life sciences", "Venereology", "Life sciences", "Urology", "Life sciences", "Nephrology", "Life sciences", "Sexology", "Life sciences", "Orthopedics", "Life sciences", "Pulmonology", "Life sciences", "Traumatology", "Life sciences", "Epidemiology", "Life sciences", "Endocrinology", "Life sciences", "Transplantology", "Life sciences", "Mammalogy", "Life sciences", "Radiobiology", "Life sciences", "Logopedics", "Life sciences", "Dietology", "Natural resourses and wildlife conservation", "Forestry", "Natural resourses and wildlife conservation", "Ecology", "Natural resourses and wildlife conservation", "Environment", "Natural resourses and wildlife conservation", "Taxation of forests", "Natural resourses and wildlife conservation", "Waste management", "Natural resourses and wildlife conservation", "Antarctic", "Natural resourses and wildlife conservation", "Lean production", "Natural resourses and wildlife conservation", "Water resources", "Hobbies and pastimes", "Handicraft", "Hobbies and pastimes", "Angling (hobby)", "Hobbies and pastimes", "Model sports", "Government, administration and public services", "Police", "Government, administration and public services", "Taxes", "Government, administration and public services", "Customs", "Government, administration and public services", "Welfare & Social Security", "Government, administration and public services", "Health care", "Government, administration and public services", "Public utilities", "Government, administration and public services", "Penitentiary system", "Human rights activism", "LGBT", "Medicine - Alternative medicine", "Acupuncture", "Medicine - Alternative medicine", "Homeopathy", "Medicine - Alternative medicine", "Somatics", "Medicine - Alternative medicine", "Traditional medicine", "Medicine - Alternative medicine", "Manual therapy and osteopathy", "Proper name", "Trademark", "Proper name", "Company name", "Proper name", "Drug name", "Proper name", "Names and surnames", "Proper name", "Toponym", "Proper name", "Surname", "Proper name", "Given name", "Proper name", "Name of organization", "Proper name", "Titles of works of art", "Chemical industry", "Resins", "Chemical industry", "Silicate industry", "Chemical industry", "Polymers", "Chemical industry", "Galvanoplasty", "Chemical industry", "Stratified plastics", "Chemical industry", "Plastics", "Chemical industry", "Forest chemistry", "Chemical industry", "Agrochemistry", "Chemical industry", "Galvanizing", "Chemical industry", "Chemical fibers", "Chemical industry", "Dyes", "Chemical industry", "Astringents", "Chemical industry", "Material safety data sheet", "Chemical industry", "Enameling", "Wellness", "Hygiene", "Wellness", "Perfume", "Wellness", "Cosmetics and cosmetology", "Wellness", "Hairdressing", "Wellness", "Dietology", "Records management", "Bibliography", "Records management", "Office equipment", "Records management", "Archiving", "Records management", "Work flow", "Records management", "Typewriters and typewriting", "Records management", "Stationery", "Multimedia", "Television", "Multimedia", "Projectors", "Multimedia", "Sound recording", "Multimedia", "Stereo", "Multimedia", "LP players", "Multimedia", "Hi-Fi", "Multimedia", "Digital sound processing", "Multimedia", "Video recording", "Multimedia", "Audio electronics", "Games (other than sports)", "Card games", "Games (other than sports)", "Chess", "Games (other than sports)", "Bridge (card game)", "Games (other than sports)", "Dice", "Games (other than sports)", "Tabletop games", "Games (other than sports)", "Checkers", "Games (other than sports)", "Billiards", "Games (other than sports)", "Gambling", "Games (other than sports)", "Bowling", "Games (other than sports)", "Mahjong", "Games (other than sports)", "Computer games", "Games (other than sports)", "Golf", "Games (other than sports)", "Darts", "Games (other than sports)", "Cricket", "Outdoor activities and extreme sports", "Aeronautics", "Outdoor activities and extreme sports", "Cycling (other than sport)", "Outdoor activities and extreme sports", "Alpine skiing", "Outdoor activities and extreme sports", "Scuba diving", "Outdoor activities and extreme sports", "Skateboarding", "Outdoor activities and extreme sports", "Skydiving", "Outdoor activities and extreme sports", "Mountaineering", "Outdoor activities and extreme sports", "Sailing", "Outdoor activities and extreme sports", "Speed skating", "Outdoor activities and extreme sports", "Waterskiing", "Outdoor activities and extreme sports", "Paragliding", "Outdoor activities and extreme sports", "Windsurfing", "Outdoor activities and extreme sports", "Snowboard", "Law enforcement", "Police", "Law enforcement", "Criminology", "Law enforcement", "Forensic medicine", "Law enforcement", "Procedural law", "Law enforcement", "Combating corruption", "Law enforcement", "Explosives", "Law enforcement", "Intelligence and security services", "Law enforcement", "Federal Bureau of Investigation", "Law enforcement", "Dactyloscopy", "Law enforcement", "Organized crime", "Law enforcement", "Penitentiary system", "Law enforcement", "Forensics", "Collecting", "Philately / stamp collecting", "Collecting", "Numismatics", "Collecting", "Phaleristics", "Service industry", "Hotel industry", "Service industry", "Hairdressing", "Service industry", "Food service and catering", "Languages", "Ancient Greek", "Languages", "French", "Languages", "Latin", "Languages", "Arabic language", "Languages", "Hungarian Language", "Languages", "Dutch", "Languages", "Greek", "Languages", "Hindi", "Languages", "Irish", "Languages", "Spanish", "Languages", "Italian", "Languages", "German", "Languages", "Russian language", "Languages", "Sanskrit", "Languages", "Turkish language", "Languages", "Persian", "Languages", "Chinese", "Languages", "Swedish", "Languages", "Czech", "Languages", "Turk", "Languages", "Scandinavian", "Languages", "Romanian", "Languages", "Portuguese", "Languages", "Polish", "Languages", "Moldavian", "Languages", "Malay", "Languages", "Korean", "Languages", "Iceland", "Languages", "Ancient Hebrew", "Languages", "Hebrew", "Languages", "Danish", "Languages", "Hawaii", "Languages", "Mongolian", "Languages", "Manchu language", "Languages", "Japanese language", "Languages", "Ancient French", "Languages", "Norway", "Languages", "Gaelic", "Languages", "Thai", "Languages", "Tatar", "Languages", "Yiddish", "Languages", "Maori", "Languages", "Esperanto", "Languages", "Vietnamese", "Languages", "Albanian language", "Languages", "Bulgarian language", "Languages", "Estonian language", "Languages", "Tibetan", "Languages", "English", "Languages", "Belarusian language", "Languages", "Ukrainian language", "Languages", "Finnish language", "Jargon and slang", "Jargon", "Jargon and slang", "Spanish-American", "Jargon and slang", "Professional jargon", "Jargon and slang", "Military lingo", "Jargon and slang", "School", "Jargon and slang", "Slang", "Jargon and slang", "College vernacular", "Jargon and slang", "Black slang", "Jargon and slang", "Criminal jargon", "Jargon and slang", "Cockney rhyming slang", "Jargon and slang", "Latin American slang", "Jargon and slang", "Drug-related slang", "Jargon and slang", "Verlan", "Jargon and slang", "Prison slang", "Jargon and slang", "Chat and Internet slang", "Jargon and slang", "Youth slang", "Jargon and slang", "Computing slang", "Jargon and slang", "Police jargon", "Stylistic values", "Obsolete / dated", "Stylistic values", "Poetic", "Stylistic values", "Bookish / literary", "Stylistic values", "Rude", "Stylistic values", "Childish", "Stylistic values", "Euphemistic", "Stylistic values", "Slang", "Stylistic values", "Business style", "Stylistic values", "Nonstandard", "Stylistic values", "Formal", "Stylistic values", "Officialese", "Stylistic values", "Sublime", "Stylistic values", "Low register", "Stylistic values", "Invective", "Stylistic values", "Scientific", "Stylistic values", "News style", "Stylistic values", "Old-fashioned", "Stylistic values", "Cliche", "Stylistic values", "Archaic", "Stylistic values", "Taboo expressions and obscenities", "Stylistic values", "Vernacular language", "Stylistic values", "Modern use", "Stylistic values", "Soviet", "Stylistic values", "Neologism", "Stylistic values", "Epistolary", "Stylistic values", "Barbarism", "Stylistic values", "Spoken", "Stylistic values", "Vulgar", "Stylistic values", "Written", "Countries and regions", "Scotland", "Countries and regions", "Turkey", "Countries and regions", "Canada", "Countries and regions", "Spain", "Countries and regions", "Australia", "Countries and regions", "Israel", "Countries and regions", "France", "Countries and regions", "Japan", "Countries and regions", "Belarus", "Countries and regions", "United Kingdom", "Countries and regions", "Germany", "Countries and regions", "Wales", "Countries and regions", "Northern Ireland", "Countries and regions", "West Indies", "Countries and regions", "Andalusia", "Countries and regions", "Antilles", "Countries and regions", "Aragon", "Countries and regions", "Argentina", "Countries and regions", "Asturias", "Countries and regions", "Bolivia", "Countries and regions", "Brazil", "Countries and regions", "Venezuela", "Countries and regions", "Galicia", "Countries and regions", "Guatemala", "Countries and regions", "Columbia", "Countries and regions", "Costa Rica", "Countries and regions", "Cuba", "Countries and regions", "Netherlands", "Countries and regions", "Morocco", "Countries and regions", "Panama", "Countries and regions", "Peru", "Countries and regions", "Philippines", "Countries and regions", "Central America", "Countries and regions", "Chile", "Countries and regions", "South Asia", "Countries and regions", "South America", "Countries and regions", "United States", "Countries and regions", "Africa", "Countries and regions", "European Union", "Countries and regions", "Dominican Republic", "Countries and regions", "Algeria", "Countries and regions", "Afghanistan", "Countries and regions", "Taiwan", "Countries and regions", "Ukraine", "Countries and regions", "Austria", "Countries and regions", "Kazakhstan", "Countries and regions", "Cyprus", "Countries and regions", "Russia", "Countries and regions", "India", "Countries and regions", "Kyrgyzstan", "Countries and regions", "China", "Countries and regions", "Iran", "Grammatical labels", "Collective", "Grammatical labels", "Abbreviation", "Grammatical labels", "Diminutive", "Grammatical labels", "Iimitative (onomatopoeic)", "Grammatical labels", "Exclamation", "Grammatical labels", "Augmentative", "Grammatical labels", "Affectionate", "Auxilliary categories (editor use only)", "British English", "Auxilliary categories (editor use only)", "American English", "Auxilliary categories (editor use only)", "Old orthography", "Auxilliary categories (editor use only)", "Misused", "Auxilliary categories (editor use only)", "Loan translation", "Auxilliary categories (editor use only)", "Meaning 1", "Auxilliary categories (editor use only)", "Meaning 2", "Auxilliary categories (editor use only)", "Meaning 3", "Auxilliary categories (editor use only)", "Translator's false friend", "Parasciences", "Astrology", "Parasciences", "Parapsychology", "Parasciences", "Esoterics", "Parasciences", "Ufology", "Art and culture (n.e.s.)", "Painting", "Art and culture (n.e.s.)", "Art", "Art and culture (n.e.s.)", "Music", "Art and culture (n.e.s.)", "Rhetoric", "Art and culture (n.e.s.)", "Theatre", "Art and culture (n.e.s.)", "Circus", "Art and culture (n.e.s.)", "Tauromachy", "Art and culture (n.e.s.)", "Choreography", "Art and culture (n.e.s.)", "Librarianship", "Art and culture (n.e.s.)", "Museums", "Art and culture (n.e.s.)", "Comics", "Art and culture (n.e.s.)", "Fashion", "Art and culture (n.e.s.)", "Cultural studies", "Art and culture (n.e.s.)", "Sculpture", "Art and culture (n.e.s.)", "Manga", "Art and culture (n.e.s.)", "Titles of works of art", "Art and culture (n.e.s.)", "Design", "Art and culture (n.e.s.)", "Musical instruments", "Art and culture (n.e.s.)", "Dancing", "Art and culture (n.e.s.)", "Calligraphy", "Art and culture (n.e.s.)", "Ballet", "Emotional values", "Ironical", "Emotional values", "Humorous / Jocular", "Emotional values", "Rude", "Emotional values", "Gloomy", "Emotional values", "Contemptuous", "Emotional values", "Disapproving", "Emotional values", "Emotive", "Emotional values", "Avuncular", "Emotional values", "Pompous", "Emotional values", "Derogatory", "Emotional values", "Affectionate", "Emotional values", "Respectful", "Emotional values", "Pejorative", "Emotional values", "Polite", "Emotional values", "Sarcastical", "Emotional values", "Laudatory", "Light industries", "Textile industry", "Light industries", "Leather", "Light industries", "Knitted goods", "Light industries", "Sewing and clothing industry", "Light industries", "Clothing", "Light industries", "Footwear", "Light industries", "Haberdashery", "Wood, pulp and paper industries", "Pulp and paper industry", "Wood, pulp and paper industries", "Wood processing", "Wood, pulp and paper industries", "Matches", "Wood, pulp and paper industries", "Timber floating", "Wood, pulp and paper industries", "Logging", "Crafts", "Cooperage", "Crafts", "Spinning", "Crafts", "Weaving", "Companion animals", "Dog breeding", "Companion animals", "Pets", "Companion animals", "Felinology", "Subjects for Chinese dictionaries (container)", "Dragon boat", "Subjects for Chinese dictionaries (container)", "Dragon dance", "Subjects for Chinese dictionaries (container)", "Northeastern Mandarin", "Subjects for Chinese dictionaries (container)", "Verbatim", "Subjects for Chinese dictionaries (container)", "Eastern Chinese", "Subjects for Chinese dictionaries (container)", "Kabaddi", "Subjects for Chinese dictionaries (container)", "Mahjong", "Subjects for Chinese dictionaries (container)", "Conventional notation", "Subjects for Chinese dictionaries (container)", "Middle Chinese", "Subjects for Chinese dictionaries (container)", "Pigeon racing", "Subjects for Chinese dictionaries (container)", "Instead of"]
        self.Success = True
        self.subjs = {}
        
    def run(self):
        self.check()
        self.parse()
        self.get_dict()
        self.get_list()
    
    def get_list(self):
        f = '[MClient] plugins.multitrancom.utils.Groups.get_list'
        if self.Success:
            lst = []
            majors = sorted(self.subjs.keys())
            for major in majors:
                minors = sorted(self.subjs[major])
                minors.insert(0,major)
                lst.append(minors)
            sh.com.run_fast_debug(f,lst)
        else:
            sh.com.cancel(f)
    
    def get_dict(self):
        f = '[MClient] plugins.multitrancom.utils.Groups.get_dict'
        if self.Success:
            mes = []
            majors = sorted(self.subjs.keys())
            for major in majors:
                minors = sorted(self.subjs[major])
                sub = ''''{}': {},\n'''.format(major,minors)
                mes.append(sub)
            mes = ''.join(mes)
            sh.com.run_fast_debug(f,mes)
        else:
            sh.com.cancel(f)
    
    def check(self):
        f = '[MClient] plugins.multitrancom.utils.Groups.check'
        if self.lst:
            if len(self.lst) % 2 != 0:
                self.Success = False
                sub = '{} % 2 == 0'.format(len(self.lst))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            self.Success = False
            sh.com.rep_empty(f)
    
    def parse(self):
        f = '[MClient] plugins.multitrancom.utils.Groups.parse'
        if self.Success:
            i = 0
            while i < len(self.lst):
                if not self.lst[i] in self.subjs:
                    self.subjs[self.lst[i]] = []
                self.subjs[self.lst[i]].append(self.lst[i+1])
                i += 2
        else:
            sh.com.cancel(f)



class Pairs:
    # Determine language pairs supported by MT
    def __init__(self):
        self.set_values()
    
    def get_blacklist(self):
        ''' Read a list of URLs leading to network errors and return
            a list of pairs represented by language codes that
            cannot be used.
        '''
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_blacklist'
        file = '/tmp/urls'
        pattern = 'https\:\/\/www.multitran.com\/m.exe\?l1=(\d+)\&l2=(\d+)\&SHL=2\&s='
        text = sh.ReadTextFile(file).get()
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
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_bad_gateway(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_bad_gateway'
        file = '/tmp/urls'
        text = sh.ReadTextFile(file).get()
        if text:
            lst = text.splitlines()
            lst = [item.strip() for item in lst if item.strip()]
            if lst:
                errors = []
                for i in range(len(lst)):
                    mes = '{}/{}'.format(i+1,len(lst))
                    sh.objs.get_mes(f,mes,True).show_info()
                    try:
                        req = urllib.request.Request (url = lst[i]
                                                     ,data = None
                                                     ,headers = {'User-Agent': \
                                                                 'Mozilla'
                                                                }
                                                     )
                        urllib.request.urlopen(req,timeout=12).read()
                        if self.Verbose:
                            mes = _('[OK]: "{}"').format(lst[i])
                            sh.objs.get_mes(f,mes,True).show_info()
                    except Exception as e:
                        if 'gateway' in str(e).lower():
                            errors.append(lst[i])
                if errors:
                    mes = '\n'.join(errors)
                    sh.objs.get_mes(f,mes,True).show_info()
                else:
                    mes = _('No matches!')
                    sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_lang(self,code):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_lang'
        if isinstance(code,int):
            for lang in self.dic.keys():
                if self.dic[lang]['code'] == code:
                    return lang
        else:
            mes = _('Wrong input data: "{}"!').format(code)
            sh.objs.get_mes(f,mes).show_error()
    
    def rep_remaining(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.rep_remaining'
        file = '/tmp/urls'
        pattern = 'https\:\/\/www.multitran.com\/m.exe\?l1=(\d+)\&l2=(\d+)\&SHL=2\&s='
        text = sh.ReadTextFile(file).get()
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
                        if self.is_pair(code1,code2):
                            lang1 = self.get_lang(code1)
                            lang2 = self.get_lang(code2)
                            if lang1 and lang2:
                                pairs.append(lang1 + ' <=> ' + lang2)
                            else:
                                sh.com.rep_empty(f)
                if pairs:
                    mes = '\n'.join(pairs)
                    sh.objs.get_mes(f,mes).show_info()
                else:
                    mes = _('No matches!')
                    sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.rep_empty(f)
    
    def get_dead(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_dead'
        dead = []
        for i in range(len(self.langs)):
            if self.isdead(i+1):
                dead.append(self.langs[i])
        self.alive = [lang for lang in self.langs if not lang in dead]
        message = _('Dead languages: {}').format(', '.join(dead))
        message += '\n'
        message += _('Languages: total: {}; alive: {}; dead: {}')
        message = message.format (len(self.langs)
                                 ,len(self.alive)
                                 ,len(dead)
                                 )
        message += '\n'
        sh.objs.get_mes(f,message,True).show_info()
        message = _('Alive languages:') + '\n' + ', '.join(self.alive)
        message += '\n\n'
        message += _('The entire dictionary:') + '\n' + str(self.dic)
        sh.objs.get_mes(f,message).show_info()
    
    def is_dead(self,code1):
        f = '[MClient] plugins.multitrancom.utils.Pairs.is_dead'
        url = self.deadr.format(code1)
        # We use '<=' since a language code starts with 1
        if 0 < code1 <= len(self.langs):
            code = ''
            while not code:
                code = sh.Get (url = url
                              ,timeout = 20
                              ).run()
            if self.zero in code.replace('\n','').replace('\r',''):
                return True
        else:
            sub = '0 < {} <= {}'.format(code,len(self.alive))
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
    
    def fill(self):
        for i in range(len(self.langs)):
            self.dic[self.langs[i]] = {'code':i+1
                                      ,'pair':()
                                      }
    
    def get_pairs(self,lang1):
        f = '[MClient] plugins.multitrancom.utils.Pairs.get_pairs'
        if lang1:
            if lang1 in self.alive:
                lst = []
                for lang2 in self.alive:
                    if self.is_pair (self.dic[lang1]['code']
                                    ,self.dic[lang2]['code']
                                    ):
                        lst.append(lang2)
                if lst:
                    lst.sort()
                    self.dic[lang1]['pair'] = tuple(lst)
                else:
                    ''' This error can be caused by network issues, so
                        we make it silent.
                    '''
                    mes = _('Language "{}" is alive but has no pairs!')
                    mes = mes.format(lang1)
                    sh.objs.get_mes(f,mes,True).show_warning()
            else:
                # We should pass only alive languages to this procedure
                mes = _('Language "{}" is dead!').format(lang1)
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def loop(self):
        f = '[MClient] plugins.multitrancom.utils.Pairs.loop'
        #NOTE: Set this to the last processed language
        i = 0
        while i < len(self.alive):
            lang = self.alive[i]
            sh.objs.get_mes(f,lang,True).show_info()
            self.get_pairs(lang)
            self.write(lang)
            i += 1
    
    def write(self,lang='Last'):
        struct = sorted(self.dic.items(),key=operator.itemgetter(0))
        message = _('Last processed language:') + ' ' + lang + '\n\n' \
                  + str(struct)
        if self.errors:
            message += '\n\n' + _('URLs that caused errors:') + '\n'
            message += '\n'.join(self.errors)
        sh.WriteTextFile (file = self.filew
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
        sh.Launch(self.filew).launch_default()
    
    def is_pair(self,code1,code2):
        f = '[MClient] plugins.multitrancom.utils.Pairs.is_pair'
        # We use '<=' since a language code starts with 1
        if 0 < code1 <= len(self.langs) \
        and 0 < code2 <= len(self.langs):
            if code1 == code2:
                sh.com.rep_lazy(f)
            else:
                url = self.root.format(code1,code2)
                '''
                code = ''
                while not code:
                    code = sh.Get(url=url).run()
                '''
                code = sh.Get (url = url
                              ,timeout = 20
                              ).run()
                if 'Тематика' in code:
                    return True
                elif not code:
                    ''' Sometimes 'Bad Gateway' error is received which
                        can be witnessed in a browser too.
                    '''
                    self.errors.append(url)
        else:
            sub = '0 < {} <= {}, 0 < {} <= {}'.format (code1
                                                      ,len(self.langs)
                                                      ,code2
                                                      ,len(self.langs)
                                                      )
            mes = _('The condition "{}" is not observed!').format(sub)
            sh.objs.get_mes(f,mes).show_error()
    
    def set_values(self):
        self.Success = True
        self.root = 'https://www.multitran.com/m.exe?l1={}&l2={}&SHL=2&s='
        self.deadr = 'https://www.multitran.com/m.exe?l1={}&SHL=2&s='
        self.zero = 'Количество терминов</a></td></tr><tr bgcolor=#DBDBDB><td>Всего</td><td></td><td align="right">0</td>'
        ''' A list of languages that have terms (and therefore pairs).
            This list is based on the output of 'self.get_dead'.
            Recreate it when necessary.
        '''
        self.alive = (_('Abkhazian'),_('Afrikaans'),_('Albanian'),_('Amharic'),_('Arabic'),_('Armenian'),_('Assamese'),_('Azerbaijani'),_('Bashkir'),_('Basque'),_('Belarusian'),_('Bengali'),_('Bosnian'),_('Bosnian cyrillic'),_('Breton'),_('Bulgarian'),_('Burmese'),_('Catalan'),_('Chechen'),_('Chinese'),_('Chinese Taiwan'),_('Chinese simplified'),_('Chuvash'),_('Cornish'),_('Croatian'),_('Czech'),_('Danish'),_('Dutch'),_('English'),_('Esperanto'),_('Estonian'),_('Faroese'),_('Filipino'),_('Finnish'),_('French'),_('Frisian'),_('Friulian'),_('Galician'),_('Gallegan'),_('Georgian'),_('German'),_('Gothic'),_('Greek'),_('Gujarati'),_('Hausa'),_('Hebrew'),_('Hindi'),_('Hungarian'),_('Icelandic'),_('Igbo'),_('Indonesian'),_('Ingush'),_('Inuktitut'),_('Irish'),_('IsiXhosa'),_('Italian'),_('Japanese'),_('Kalmyk'),_('Kannada'),_('Kazakh'),_('Khmer'),_('Kinyarwanda'),_('Kirghiz'),_('Konkani'),_('Korean'),_('Ladin'),_('Lao'),_('Latin'),_('Latvian'),_('Lithuanian'),_('Lower Sorbian'),_('Luxembourgish'),_('Macedonian'),_('Malay'),_('Malayalam'),_('Maltese'),_('Manh'),_('Maori'),_('Marathi'),_('Mongolian'),_('Montenegrin'),_('Nepali'),_('Norwegian Bokmal'),_('Norwegian Nynorsk'),_('Occitan'),_('Odia'),_('Pashto'),_('Persian'),_('Polish'),_('Portuguese'),_('Punjabi'),_('Quechua'),_('Romanian'),_('Romansh'),_('Romany'),_('Russian'),_('Sami'),_('Sardinian'),_('Scottish Gaelic'),_('Serbian'),_('Serbian latin'),_('Sesotho'),_('Sesotho sa leboa'),_('Sinhala'),_('Slovak'),_('Slovenian'),_('South Ndebele'),_('Spanish'),_('Swahili'),_('Swati'),_('Swedish'),_('Tajik'),_('Tamil'),_('Tatar'),_('Telugu'),_('Thai'),_('Tsonga'),_('Tswana'),_('Turkish'),_('Turkmen'),_('Ukrainian'),_('Upper Sorbian'),_('Urdu'),_('Uzbek'),_('Venda'),_('Vietnamese'),_('Wayana'),_('Welsh'),_('Wolof'),_('Yakut'),_('Yoruba'),_('Zulu'))
        ''' A total list of languages supported by Multitran.
            #NOTE: Must be sorted by a language code in an ascending
            order.
        '''
        self.langs = (_('English'),_('Russian'),_('German'),_('French'),_('Spanish'),_('Hebrew'),_('Serbian'),_('Croatian'),_('Tatar'),_('Arabic'),_('Portuguese'),_('Lithuanian'),_('Romanian'),_('Polish'),_('Bulgarian'),_('Czech'),_('Chinese'),_('Hindi'),_('Bengali'),_('Punjabi'),_('Vietnamese'),_('Danish'),_('Italian'),_('Dutch'),_('Azerbaijani'),_('Estonian'),_('Latvian'),_('Japanese'),_('Swedish'),_('Norwegian Bokmal'),_('Afrikaans'),_('Turkish'),_('Ukrainian'),_('Esperanto'),_('Kalmyk'),_('Finnish'),_('Latin'),_('Greek'),_('Korean'),_('Georgian'),_('Armenian'),_('Hungarian'),_('Kazakh'),_('Kirghiz'),_('Uzbek'),_('Romany'),_('Albanian'),_('Welsh'),_('Irish'),_('Icelandic'),_('Kurdish'),_('Persian'),_('Catalan'),_('Corsican'),_('Galician'),_('Mirandese'),_('Romansh'),_('Belarusian'),_('Ruthene'),_('Slovak'),_('Upper Sorbian'),_('Lower Sorbian'),_('Bosnian'),_('Montenegrin'),_('Macedonian'),_('Church Slavonic'),_('Slovenian'),_('Basque'),_('Svan'),_('Mingrelian'),_('Abkhazian'),_('Adyghe'),_('Chechen'),_('Avar'),_('Ingush'),_('Crimean Tatar'),_('Chuvash'),_('Maltese'),_('Khmer'),_('Nepali'),_('Amharic'),_('Assamese'),_('Lao'),_('Asturian'),_('Odia'),_('Indonesian'),_('Pashto'),_('Quechua'),_('Maori'),_('Marathi'),_('Tamil'),_('Telugu'),_('Thai'),_('Turkmen'),_('Yoruba'),_('Bosnian cyrillic'),_('Chinese simplified'),_('Chinese Taiwan'),_('Filipino'),_('Gujarati'),_('Hausa'),_('Igbo'),_('Inuktitut'),_('IsiXhosa'),_('Zulu'),_('Kannada'),_('Kinyarwanda'),_('Swahili'),_('Konkani'),_('Luxembourgish'),_('Malayalam'),_('Wolof'),_('Wayuu'),_('Serbian latin'),_('Tswana'),_('Sinhala'),_('Urdu'),_('Sesotho sa leboa'),_('Norwegian Nynorsk'),_('Malay'),_('Mongolian'),_('Frisian'),_('Faroese'),_('Friulian'),_('Ladin'),_('Sardinian'),_('Occitan'),_('Gaulish'),_('Gallegan'),_('Sami'),_('Breton'),_('Cornish'),_('Manh'),_('Scottish Gaelic'),_('Yiddish'),_('Tajik'),_('Tagalog'),_('Soninke'),_('Baoulé'),_('Javanese'),_('Wayana'),_('French Guiana Creole'),_('Mauritian Creole'),_('Seychellois Creole'),_('Guadeloupe Creole'),_('Rodriguan Creole'),_('Haitian Creole'),_('Mandinka'),_('Surigaonon'),_('Adangme'),_('Tok Pisin'),_('Cameroonian Creole'),_('Suriname Creole'),_('Belizean Creole'),_('Virgin Islands Creole'),_('Fon'),_('Kim'),_('Ivatan'),_('Gen'),_('Marshallese'),_('Wallisian'),_('Old Prussian'),_('Yom'),_('Tokelauan'),_('Zande'),_('Yao'),_('Waray'),_('Walmajarri'),_('Visayan'),_('Vili'),_('Venda'),_('Achinese'),_('Adjukru'),_('Agutaynen'),_('Afar'),_('Acoli'),_('Afrihili'),_('Ainu'),_('Akan'),_('Akkadian'),_('Aleut'),_('Southern Altai'),_('Old English'),_('Angika'),_('Official Aramaic'),_('Aragonese'),_('Mapudungun'),_('Arapaho'),_('Arawak'),_('Avestan'),_('Awadhi'),_('Aymara'),_('Bashkir'),_('Baluchi'),_('Bambara'),_('Balinese'),_('Basaa'),_('Beja'),_('Bemba'),_('Bhojpuri'),_('Bikol'),_('Bini'),_('Bislama'),_('Siksika'),_('Tibetan'),_('Braj'),_('Buriat'),_('Buginese'),_('Burmese'),_('Bilin'),_('Caddo'),_('Galibi Carib'),_('Cebuano'),_('Chamorro'),_('Chibcha'),_('Chagatai'),_('Chuukese'),_('Mari'),_('Chinook jargon'),_('Choctaw'),_('Chipewyan'),_('Cherokee'),_('Cheyenne'),_('Coptic'),_('Cree'),_('Kashubian'),_('Dakota'),_('Dargwa'),_('Delaware'),_('Slave'),_('Dogrib'),_('Dinka'),_('Dhivehi'),_('Dogri'),_('Duala'),_('Middle Dutch'),_('Dyula'),_('Dzongkha'),_('Efik'),_('Egyptian'),_('Ekajuk'),_('Elamite'),_('Middle English'),_('Ewe'),_('Ewondo'),_('Fang'),_('Fanti'),_('Fijian'),_('Middle French'),_('Old French'),_('Eastern Frisian'),_('Fulah'),_('Ga'),_('Gayo'),_('Gbaya'),_('Ge\'ez'),_('Gilbertese'),_('Middle High German'),_('Old High German'),_('Gondi'),_('Gorontalo'),_('Gothic'),_('Grebo'),_('Ancient Greek'),_('Guarani'),_('Swiss German'),_('Gwichʼin'),_('Haida'),_('Kikuyu'),_('Hawaiian'),_('Herero'),_('Hiligaynon'),_('Hittite'),_('Hmong'),_('Hiri Motu'),_('Hupa'),_('Iban'),_('Ido'),_('Sichuan Yi'),_('Interlingue'),_('Ilocano'),_('Interlingua'),_('Inupiaq'),_('Lojban'),_('Judeo-Persian'),_('Judeo-Arabic'),_('Kara-Kalpak'),_('Kabyle'),_('Kachin'),_('Kalaallisut'),_('Kamba'),_('Kashmiri'),_('Kanuri'),_('Kawi'),_('Kabardian'),_('Khasi'),_('Khotanese'),_('Kimbundu'),_('Komi'),_('Kongo'),_('Kosraean'),_('Kpelle'),_('Karachay-Balkar'),_('Karelian'),_('Kurukh'),_('Kuanyama'),_('Kumyk'),_('Kutenai'),_('Lahnda'),_('Lamba'),_('Lezghian'),_('Limburgan'),_('Lingala'),_('Mongo'),_('Lozi'),_('Luba-Lulua'),_('Luba-Katanga'),_('Ganda'),_('Luiseno'),_('Lunda'),_('Luo'),_('Lushai'),_('Madurese'),_('Magahi'),_('Maithili'),_('Makasar'),_('Masai'),_('Moksha'),_('Mandar'),_('Mende'),_('Middle Irish'),_('Mi\'kmaq'),_('Minangkabau'),_('Malagasy'),_('Manchu'),_('Manipuri'),_('Mohawk'),_('Mossi'),_('Creek'),_('Marwari'),_('Erzya'),_('Neapolitan'),_('Nauru'),_('Navajo'),_('South Ndebele'),_('North Ndebele'),_('Ndonga'),_('Low German'),_('Nepal Bhasa'),_('Nias'),_('Niuean'),_('Nogai'),_('Old Norse'),_('Sandawe'),_('N\'Ko'),_('Classical Newari'),_('Nyanja'),_('Nyamwezi'),_('Nyankole'),_('Nyoro'),_('Nzima'),_('Ojibwa'),_('Oromo'),_('Osage'),_('Ossetian'),_('Ottoman Turkish'),_('Pangasinan'),_('Pahlavi'),_('Pampanga'),_('Papiamento'),_('Palauan'),_('Old Persian'),_('Phoenician'),_('Pali'),_('Pohnpeian'),_('Old Occitan'),_('Rajasthani'),_('Rapanui'),_('Rarotongan'),_('Reunionese'),_('Rundi'),_('Macedo-Romanian'),_('Sango'),_('Yakut'),_('Samaritan Aramaic'),_('Sanskrit'),_('Sasak'),_('Sicilian'),_('Scots'),_('Selkup'),_('Old Irish'),_('Shan'),_('Sidamo'),_('Southern Sami'),_('Northern Sami'),_('Lule Sami'),_('Inari Sami'),_('Samoan'),_('Skolt Sami'),_('Shona'),_('Sindhi'),_('Sogdian'),_('Somali'),_('Sesotho'),_('Sranan Tongo'),_('Serer'),_('Swati'),_('Sukuma'),_('Sundanese'),_('Susu'),_('Sumerian'),_('Santali'),_('Syriac'),_('Tahitian'),_('Timne'),_('Tonga'),_('Tetum'),_('Tigre'),_('Tigrinya'),_('Tiv'),_('Shilluk'),_('Klingon'),_('Tlingit'),_('Tamashek'),_('Carolinian'),_('Portuguese creole'),_('Tuamotuan'),_('Numèè'),_('Gela'),_('Comorian'),_('Rennellese'),_('Emilian-Romagnol'),_('Mayan'),_('Caribbean Hindustani'),_('Khakas'),_('Kinga'),_('Kurmanji'),_('Kwangali'),_('Lango'),_('Ligurian'),_('Lombard'),_('Luguru'),_('Mamasa'),_('Mashi'),_('Meru'),_('Rotokas'),_('Moldovan'),_('Mongolian script'),_('Nasioi'),_('Nyakyusa'),_('Piedmontese'),_('Pinyin'),_('Sangu'),_('Shambala'),_('Shor'),_('Central Atlas Tamazight'),_('Thai Transliteration'),_('Tsonga'),_('Tuvan'),_('Valencian'),_('Venetian'),_('Walloon'),_('Wanji'),_('Zigula'),_('Korean Transliteration'),_('Mongolian Transliteration'),_('Assyrian'),_('Kaguru'),_('Kimakonde'),_('Kirufiji'),_('Mbwera'),_('Gronings'),_('Hadza'),_('Iraqw'),_('Kami'),_('Krio'),_('Tweants'),_('Abaza'))
        self.filew = '/home/pete/tmp/ars/pairs'
        self.dic = {}
        self.errors = []



class Subjects:
    
    def __init__(self,url='https://www.multitran.com/m.exe?a=112&l1=1&l2=2'):
        self.set_values()
        self.url = url
        
    def set_values(self):
        self.Success = True
        self.htm = ''
        self.titles = []
        self.abbrs = []
        
    def run(self):
        self.get_htm()
        self.run_tags()
        
    def get_htm(self):
        f = '[MClient] plugins.multitrancom.utils.Subjects.get_htm'
        if self.Success:
            self.htm = sh.Get (url = self.url
                              ,coding = 'utf-8'
                              ).run()
            if self.htm:
                self.htm = self.htm.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
                          
    def run_tags(self):
        f = '[MClient] plugins.multitrancom.utils.Subjects.run_tags'
        if self.Success:
            tags = Tags (text = self.htm
                        ,search = 'href="/m.exe?a='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                if tags.urls:
                    tags.urls = [tags.urls[0]]
                    for i in range(len(tags.urls)):
                        abbr = Abbr (url = tags.urls[i]
                                    ,title = tags.titles[i]
                                    )
                        abbr.run()
                        if len(abbr.titles) == len(abbr.abbrs):
                            for i in range(len(abbr.abbrs)):
                                if not abbr.abbrs[i] in self.abbrs:
                                    self.abbrs.append(abbr.abbrs[i])
                                    self.titles.append(abbr.titles[i])
                        else:
                            #TODO: Should we toggle 'self.Success' here?
                            #self.Success = False
                            sub = '{} == {}'.format (len(abbr.titles)
                                                    ,len(abbr.abbrs)
                                                    )
                            mes = _('The condition "{}" is not observed!')
                            mes = mes.format(sub)
                            sh.objs.get_mes(f,mes).show_warning()
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)



class Abbr:
    
    def __init__(self,url,title):
        f = '[MClient] plugins.multitrancom.utils.Abbr.__init__'
        self.set_values()
        self.url = url
        self.title = title
        if self.url and self.title:
            self.Success = True
        else:
            self.Success = False
            sh.com.rep_empty(f)
                          
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.debug'
        if self.Success:
            text = ''
            for i in range(len(self.abbrs)):
                text += '%d: "%s": "%s"\n' % (i,self.titles[i]
                                             ,self.abbrs[i]
                                             )
            return text
        else:
            sh.com.cancel(f)
    
    def set_values(self):
        self.htm = ''
        self.htm2 = ''
        self.url2 = ''
        self.titles = []
        self.abbrs = []
                          
    def get(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.get'
        if self.Success:
            self.htm = sh.Get (url = self.url
                              ,coding = 'utf-8'
                              ).run()
            if self.htm:
                self.htm = self.htm.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get2(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.get2'
        if self.Success:
            self.htm2 = sh.Get (url = self.url2
                               ,coding = 'utf-8'
                               ).run()
            if self.htm2:
                self.htm2 = self.htm2.replace('&amp;','&')
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run_tags(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.run_tags'
        if self.Success:
            tags = Tags (text = self.htm
                        ,search = 'href="/m.exe?a='
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                if tags.urls and tags.urls[0]:
                    ''' #TODO: try all URLs instead of the 1st one
                        (a Multitran's bug: some links may lead to
                        different dictionary titles).
                    '''
                    self.url2 = tags.urls[0]
                    ''' Avoid a Multitran's bug: the site generates URLs
                        with tabs, which cannot be downloaded. However,
                        those URLs work fine if tabs are deleted.
                    '''
                    self.url2 = self.url2.replace('\t','')
                else:
                    sh.com.rep_empty(f)
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)
    
    def run_tags2(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.run_tags2'
        if self.Success:
            ''' Replace this so that 'Tags' would not treat this as
                a new tag.
            '''
            self.htm2 = self.htm2.replace('<i>','')
            tags = Tags (text = self.htm2
                        ,search = '<a title="'
                        )
            tags.run()
            self.Success = tags.Success
            if self.Success:
                self.titles = tags.urls
                self.abbrs = tags.titles
            else:
                sh.com.cancel(f)
        else:
            sh.com.cancel(f)
    
    def set_titles(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.set_titles'
        if self.Success:
            for i in range(len(self.titles)):
                if self.titles[i]:
                    self.titles[i] = self.titles[i].replace('<a title="','')
                    pos = sh.Search (text = self.titles[i]
                                    ,pattern = '" href'
                                    ).get_next()
                    pos = sh.Input(f,pos).get_integer()
                    self.titles[i] = self.titles[i][:pos]
                    self.titles[i] = self.titles[i].strip()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def run_abbrs(self):
        f = '[MClient] plugins.multitrancom.utils.Abbr.run_abbrs'
        if self.Success:
            for i in range(len(self.abbrs)):
                self.abbrs[i] = self.abbrs[i].replace('<i>','')
                self.abbrs[i] = self.abbrs[i].replace('</i>','')
                self.abbrs[i] = self.abbrs[i].strip()
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.get()
        self.run_tags()
        self.get2()
        self.run_tags2()
        self.set_titles()
        self.run_abbrs()



class Tags:
    
    def __init__(self,text,search='href="/m.exe?a='):
        f = '[MClient] plugins.multitrancom.utils.Tags.__init__'
        self.set_values()
        self.text = text
        self.search = search
        if not self.text:
            self.Success = False
            sh.com.rep_empty(f)
        
    def set_values(self):
        self.Success = True
        self.tags = []
        self.titles = []
        self.urls = []
        self.start = []
        self.end = []
        
    def equalize(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.equalize'
        if self.Success:
            if len(self.end) > len(self.start):
                tmp = []
                for i in range(len(self.start)):
                    while self.start[i] > self.end[i]:
                        del self.end[i]
                    tmp.append(self.end[i])
                self.end = tmp
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    def split(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.split'
        if self.Success:
            self.start = sh.Search (text = self.text
                                   ,pattern = self.search
                                   ).get_next_loop()
            self.end = sh.Search (text = self.text
                                 ,pattern = '</a>'
                                 ).get_next_loop()
            self.equalize()
            if len(self.start) == len(self.end):
                for i in range(len(self.start)):
                    self.tags.append(self.text[self.start[i]:self.end[i]])
            else:
                self.Success = False
                sub = '{} == {}'.format (len(self.start)
                                        ,len(self.end)
                                        )
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                sh.objs.get_mes(f,mes).show_warning()
            mes = _('{} tags have been extracted')
            mes = mes.format(len(self.tags))
            sh.objs.get_mes(f,mes,True).show_debug()
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
            self.urls = [url for url in self.urls \
                         if not self.loop_trash(url)
                        ]
            for i in range(len(self.urls)):
                if self.urls[i]:
                    self.urls[i] = self.urls[i].replace('<a href="/m.exe?','https://www.multitran.com/m.exe?')
                    if self.urls[i].endswith('"'):
                        self.urls[i] = self.urls[i][:-1]
                    else:
                        mes = _('Wrong input data: "{}"!')
                        mes = mes.format(self.urls[i])
                        sh.objs.get_mes(f,mes,True).show_warning()
                else:
                    sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)

    def trash_titles(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.trash_titles'
        if self.Success:
            for i in range(len(self.titles)):
                self.titles[i] = html.unescape(self.titles[i])
        else:
            sh.com.cancel(f)
    
    def set_urls(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.set_urls'
        if self.Success:
            if self.tags:
                for tag in self.tags:
                    pos = sh.Search (text = tag
                                    ,pattern = '>'
                                    ).get_next()
                    pos = sh.Input('Tags.links',pos).get_integer()
                    self.urls.append(tag[:pos])
                    self.titles.append(tag[pos+1:])
            else:
                sh.com.rep_empty(f)
            self.urls = [url.replace(' ','%20') for url in self.urls]
            self.urls = [url.replace ('href="/m.exe?'
                                     ,'https://www.multitran.com/m.exe?'
                                     ) \
                         for url in self.urls
                        ]
            mes = _('{} URLs have been extracted')
            mes = mes.format(len(self.urls))
            sh.objs.get_mes(f,mes,True).show_debug()
            mes = _('{} titles have been extracted')
            mes = mes.format(len(self.titles))
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.cancel(f)
        
    def debug(self):
        f = '[MClient] plugins.multitrancom.utils.Tags.debug'
        if self.Success:
            text = ''
            for i in range(len(self.urls)):
                text += '{}: "{}": "{}"\n'.format (i,self.urls[i]
                                                  ,self.titles[i]
                                                  )
            return text
        else:
            sh.com.cancel(f)
    
    def run(self):
        self.split()
        self.set_urls()
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
            lst = text.split(',')
            lst = ["_('" + item.strip() + "')" for item in lst \
                    if item.strip()
                   ]
            text = '(' + ','.join(lst) + ')'
            sh.Clipboard().copy(text)
            input(_('Press any key to continue.'))
        else:
            sh.com.rep_empty(f)
    
    # Transform new-line-delimited text into a list of languages
    def format_pairs(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.format_pairs'
        text = sh.Clipboard().paste()
        if text:
            text= text.replace(r"'",r"\'")
            lst = text.splitlines()
            lst = ["_('" + item.strip() + "')" for item in lst \
                   if item.strip()
                  ]
            text = '(' + ','.join(lst) + ')'
            sh.Clipboard().copy(text)
            input(_('Press any key to continue.'))
        else:
            sh.com.rep_empty(f)
    
    # Compare short dictionary titles for different languages
    def rep_new_abbrs(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.rep_new_abbrs'
        file1 = '/tmp/abbr.txt'
        file2 = '/tmp/abbr2.txt'
        dic1 = sh.Dic(file=file1)
        dic1.get()
        dic2 = sh.Dic(file=file2)
        dic2.get()
        if dic1.Success and dic2.Success:
            missing = []
            for i in range(len(dic2.orig)):
                if dic2.orig[i] not in dic1.orig:
                    missing.append(dic2.orig[i] + '\t' + dic2.transl[i])
            if missing:
                mes = '\n'.join(missing)
                sh.objs.get_mes(f,mes).show_info()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.cancel(f)
    
    # Compare dictionary subjects for different languages
    def compare_subjects(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.compare_subjects'
        file1 = '/tmp/subjects'
        file2 = '/tmp/subjects2'
        text1 = sh.ReadTextFile(file=file1).get()
        text2 = sh.ReadTextFile(file=file2).get()
        if text1 and text2:
            text1 = text1.splitlines()
            text2 = text2.splitlines()
            missing = [item for item in text2 if item not in text1]
            if missing:
                mes = '\n'.join(missing)
                sh.objs.get_mes(f,mes).show_info()
            else:
                sh.com.rep_lazy(f)
        else:
            sh.com.rep_empty(f)
    
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
        subjects = Subjects(url=url)
        subjects.run()
        if subjects.abbrs and subjects.titles:
            text = ''
            for i in range(len(subjects.abbrs)):
                text += subjects.abbrs[i] + '\t' + subjects.titles[i] + '\n'
            sh.WriteTextFile (file = file_w
                             ,Rewrite = True
                             ).write(text)
            sh.objs.get_txt().reset()
            sh.objs.txt.set_title(_('Abbreviations:'))
            sh.objs.txt.insert(text)
            sh.objs.txt.show()
        else:
            sh.com.rep_empty(f)
                          
    def run_missing_titles(self):
        f = '[MClient] plugins.multitrancom.utils.Commands.run_missing_titles'
        ''' This is a list of dictionaries from
            https://www.multitran.com/m.exe?a=112&l1=1&l2=2.
        '''
        file1 = '/tmp/subjects'
        ''' This is basically data generated by 'Commands.get_abbrs'
            with some trash deleted. 'dic.orig' - short dictionary
            titles, 'dic.transl' - full titles.
        '''
        file2 = '/tmp/abbr.txt'
        subjects = sh.ReadTextFile(file=file1).get()
        dic = sh.Dic (file = file2
                     ,Sortable = True
                     )
        if subjects and dic.orig and dic.transl:
            i = 0
            count = 0
            while i < len(dic.orig):
                ''' Multitran proposes only one full dictionary title
                    even when several short titles are given, so we
                    need only one short title per line.
                '''
                if '., ' in dic.orig[i]:
                    del dic.orig[i]
                    del dic.transl[i]
                    count += 1
                    i -= 1
                i += 1
            mes = _('{} duplicates have been deleted').format(count)
            sh.objs.get_mes(f,mes,True).show_info()
            dic.orig, dic.transl = (list(x) for x \
            in zip (*sorted (zip (dic.orig, dic.transl)
                            ,key = lambda x:x[0].lower()
                            )
                   )
                                   )
            message = ''
            for i in range(len(dic.orig)):
                message += dic.orig[i] + '\t' + dic.transl[i] + '\n'
            sh.objs.get_mes(f,message).show_info()
            subjects = subjects.splitlines()
            missing = []
            for i in range(len(subjects)):
                subjects[i] = subjects[i].strip()
                if not subjects[i] in dic.transl:
                    missing.append(subjects[i])
            if missing:
                message = _('The following dictionaries do not have short titles:')
                message += '\n'
                message += '\n'.join(missing)
                sh.objs.get_mes(f,message).show_warning()
        else:
            sh.com.rep_empty(f)


com = Commands()


if __name__ == '__main__':
    f = '[MClient] plugins.multitrancom.utils.__main__'
    sh.com.start()
    # Туннелестроение и проходческие работы
    url = 'https://www.multitran.com/m.exe?a=110&l1=1&l2=2&sc=723'
    isubj = Subjects(url)
    isubj.run()
    if isubj.titles and isubj.abbrs:
        titles = '; '.format(isubj.titles)
        abbrs = '; '.format(isubj.abbrs)
        mes = _('Titles: {}').format(titles)
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = _('Abbreviations: {}').format(abbrs)
        sh.objs.get_mes(f,mes,True).show_debug()
    else:
        sh.com.rep_empty(f)
    sh.com.end()
