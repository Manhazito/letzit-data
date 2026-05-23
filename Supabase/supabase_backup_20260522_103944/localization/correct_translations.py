import csv, re

def correct(pt_source, english):
    r = english
    pt_lower = pt_source.lower()

    # Guard: remember if "without Sauce/Salt" is already present so we don't double-add
    already_has_without_sauce = 'without Sauce' in r
    already_has_without_salt  = 'without Salt' in r or 'Unsalted' in r

    # ══════════════════════════════════════════════════════════════════════
    # SPECIFIC MULTI-WORD PHRASES  (must come before single-word replacements)
    # ══════════════════════════════════════════════════════════════════════

    # "Óleos de milho" was translated as bare 'Oleos' — catch before generic Oleo
    if r.strip() in ('Oleos', 'Oleo'):
        if 'milho'    in pt_lower: return 'Corn Oil'
        if 'amendoim' in pt_lower: return 'Peanut Oil'
        return 'Oil'

    # Oils (specific → generic)
    for old, new in [
        ('Oleo Coco',     'Coconut Oil'),
        ('Oleo Girassol', 'Sunflower Oil'),
        ('Oleo Linhaca',  'Flaxseed Oil'),
        ('Oleo Palma',    'Palm Oil'),
        ('Oleo Soy',      'Soy Oil'),
        ('Oleo Sesamo',   'Sesame Oil'),
        ('Oleo Peanut',   'Peanut Oil'),
    ]:
        r = r.replace(old, new)
    r = re.sub(r'\bOleo\b', 'Oil', r)

    # Sausages (specific → generic)
    r = r.replace('Salsicha Tipo Frankfurt', 'Frankfurt-Style Sausage')
    r = r.replace('Salsicha', 'Sausage')

    # Nuts / seeds (specific → generic)
    r = r.replace('Castanha Brasil', 'Brazil Nut')   # before generic Castanha
    r = r.replace('Castanha Caju',   'Cashew Nut')
    r = r.replace('Castanha',        'Chestnut')

    # Garbled milk translations
    r = r.replace('Milk Lactose D B9 (acido Folico) Uht',
                  'Full-Fat Lactose-Free Milk Fortified with Vitamins A, D, E and B9 (Folic Acid) UHT')
    for old, new in [
        ('Milk Lean Po',          'Skimmed Milk Powder'),
        ('Milk Lean Uht',         'Skimmed Milk UHT'),
        ('Milk Lean Lactose Uht', 'Skimmed Lactose-Free Milk UHT'),
        ('Milk Lean',             'Skimmed Milk'),
        ('Milk Uht',              'Full-Fat Milk UHT'),
    ]:
        r = r.replace(old, new)

    # Leek
    r = r.replace('Alho-frances', 'Leek')

    # Couve compounds — specific before generic 'Couve'
    for old, new in [
        ('Couve-de-bruxelas',  'Brussels Sprouts'),
        ('Couve-de-Bruxelas',  'Brussels Sprouts'),
        ('Couve-flor',         'Cauliflower'),
        ('Couve-Flor',         'Cauliflower'),
        ('Couve-branca',       'White Cabbage'),
        ('Couve-galega',       'Kale'),
        ('Couve-lombarda',     'Savoy Cabbage'),
        ('Couve-portuguesa',   'Portuguese Cabbage'),
        ('Couve-roxa',         'Red Cabbage'),
    ]:
        r = r.replace(old, new)

    # Coffee phrases (specific → generic)
    r = r.replace('Cafe Infusao - Cafe Cafeteira', 'Coffee Infusion - Moka Pot Coffee')
    r = r.replace('Cafe Cafeteira',  'Moka Pot Coffee')   # catches remaining instances
    r = r.replace('Cafe Infusao',    'Coffee Infusion')
    r = r.replace('Cafeteira',       'Coffee Maker')
    r = r.replace('Infusao',         'Infusion')
    r = re.sub(r'\bBica\b', 'Espresso', r, flags=re.IGNORECASE)
    r = r.replace('Marcas',          'Brands')
    r = r.replace('Sucedaneo',       'Coffee Substitute')
    r = r.replace('Tisana',          'Herbal Tea')
    r = r.replace('Ervas',           'Herbs')
    r = r.replace('Soluvel',         'Soluble')
    r = r.replace('Cafeina',         'Caffeine')
    r = r.replace('Descafeinado',    'Decaffeinated')

    # Tea
    # Only replace "Cha" at start-of-string or after a space (not inside Chard/Chalota/etc.)
    r = re.sub(r'^Cha\b', 'Tea', r)
    r = re.sub(r'(?<=\s)Cha\b', 'Tea', r)

    # Flour types
    r = re.sub(r'\bTipo (\d)', r'Type \1', r)
    r = re.sub(r'valor Medio', 'Average Value', r, flags=re.IGNORECASE)

    # Parenthesised Portuguese words
    r = r.replace('(raiz)',      '(Root)')
    r = r.replace('(Raiz)',      '(Root)')
    r = r.replace('(floretes)', '(Florets)')
    r = r.replace('(Floretes)', '(Florets)')
    r = r.replace('(po)',        '(Powder)')
    r = r.replace('(Po)',        '(Powder)')
    r = r.replace('(Polpa)',     '(Flesh)')
    r = r.replace('(macio)',     '(Soft)')
    r = r.replace('(Macio)',     '(Soft)')
    r = r.replace('(palitos)',   '(Strips)')
    r = r.replace('(so Polpa)',  '(Flesh Only)')

    # ══════════════════════════════════════════════════════════════════════
    # FISH
    # ══════════════════════════════════════════════════════════════════════
    for old, new in [
        (r'\bAbrotea\b',   'Forkbeard'),
        (r'\bAnchova\b',   'Anchovy'),
        (r'\bBesugo\b',    'Atlantic Seabream'),
        (r'\bCarapau\b',   'Atlantic Horse Mackerel'),
        (r'\bCherne\b',    'Wreckfish'),
        (r'\bChicharro\b', 'Horse Mackerel'),
        (r'\bChoco\b',     'Cuttlefish'),
        (r'\bCorvina\b',   'Meagre'),
        (r'\bDourada\b',   'Gilt-head Bream'),
        (r'\bEnguia\b',    'Eel'),
        (r'\bFaneca\b',    'Pouting'),
        (r'\bGaroupa\b',   'Grouper'),
        (r'\bGoraz\b',     'Red Bream'),
        (r'\bLagosta\b',   'Lobster'),
        (r'\bLagostim\b',  'Langoustine'),
        (r'\bLampreia\b',  'Lamprey'),
        (r'\bLapas\b',     'Limpets'),
        (r'\bMaruca\b',    'Ling'),
        (r'\bOstra\b',     'Oyster'),
        (r'\bPercebes\b',  'Goose Barnacles'),
        (r'\bPota\b',      'Jumbo Squid'),
        (r'\bRobalo\b',    'Sea Bass'),
        (r'\bSalmonete\b', 'Red Mullet'),
        (r'\bSapateira\b', 'Spider Crab'),
        (r'\bSarda\b',     'Chub Mackerel'),
        (r'\bSardinha\b',  'Sardine'),
        (r'\bSolha\b',     'Plaice'),
        (r'\bTamboril\b',  'Monkfish'),
        (r'\bBuzio\b',     'Whelk'),
        (r'\bGambas\b',    'Prawns'),
        (r'\bLulas\b',     'Squid'),
        (r'\bSafio\b',     'Conger Eel'),
        (r'\bRaia\b',      'Skate'),
        (r'\bLinguado\b',  'Sole'),    # MUST precede Lingua→Tongue
    ]:
        r = re.sub(old, new, r)

    # ══════════════════════════════════════════════════════════════════════
    # SHELLFISH
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bMexilhao\b',    'Mussel',   r)
    r = re.sub(r'\bBerbigao\b',    'Cockle',   r)
    r = re.sub(r'\bAmejoa[s]?\b',  'Clam',     r, flags=re.IGNORECASE)
    r = re.sub(r'\bCarangueijo\b', 'Crab',     r)
    # Cação = dogfish (small shark) — translator stripped ç → gave "Cacao" (wrong)
    # Must check pt_source because "cacau" = cocoa also becomes "Cacao" without accents
    if 'cação' in pt_lower:
        r = re.sub(r'\bCacao\b', 'Dogfish', r)
    elif 'cacau' in pt_lower:
        r = re.sub(r'\bCacao\b', 'Cocoa', r)
    # "Cacau" kept verbatim by translator (not stripped to Cacao)
    r = re.sub(r'\bCacau\b', 'Cocoa', r)
    r = re.sub(r'\bSalmao\b',           'Salmon',              r, flags=re.IGNORECASE)
    r = re.sub(r'\bLucio\b',            'Pike',                r, flags=re.IGNORECASE)
    # Scabbardfish — specific before generic
    r = r.replace('Peixe-espada-branco', 'White Scabbardfish')
    r = r.replace('Peixe-espada-preto',  'Black Scabbardfish')
    r = re.sub(r'\bPeixe-espada\b',     'Scabbardfish',        r, flags=re.IGNORECASE)

    # ══════════════════════════════════════════════════════════════════════
    # MEAT & DAIRY ANIMALS
    # ══════════════════════════════════════════════════════════════════════
    if 'Bulhao Pato' not in r:         # "Bulhão Pato" is a dish name — don't translate here
        r = re.sub(r'\bPato\b', 'Duck', r)
    r = re.sub(r'\bPeru\b',       'Turkey',    r)
    r = re.sub(r'\bCavalo\b',     'Horse',     r)
    r = re.sub(r'\bAlcatra\b',    'Rump',      r)
    r = re.sub(r'\bEntrecosto\b', 'Spare Ribs', r)
    r = re.sub(r'\bRojoes\b',     'Pork Pieces', r)
    r = re.sub(r'\bFiambre\b',    'Ham',       r)
    r = re.sub(r'\bCabra\b',      'Goat',      r)
    r = re.sub(r'\bOvelha\b',     'Sheep',     r, flags=re.IGNORECASE)
    r = re.sub(r'\bChalota\b',    'Shallot',   r)
    r = re.sub(r'\bChambao\b',    'Shin',      r)
    r = re.sub(r'\bChamuca\b',    'Samosa',    r)

    # Tongue: after Linguado → Sole already done above
    r = re.sub(r'\bLingua\b',  'Tongue',    r)
    # Shoulder (Pá)
    r = re.sub(r'\bPa\b',      'Shoulder',  r)

    # ══════════════════════════════════════════════════════════════════════
    # CHEESE & DAIRY
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bRequeijao\b',   'Curd Cheese',  r)
    r = re.sub(r'\bAmanteigado\b', 'Creamy',       r)
    r = re.sub(r'\bAtabafado\b',   'Wrapped',      r)
    r = re.sub(r'\bMistura\b',     'Mixed',        r)

    # ══════════════════════════════════════════════════════════════════════
    # OFFAL
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bBaco\b',      'Spleen',       r)
    r = re.sub(r'\bCabeca\b',    'Head',         r)
    r = re.sub(r'\bChispe\b',    'Trotters',     r)
    r = re.sub(r'\bMorcela\b',   'Black Pudding', r)
    r = re.sub(r'\bOrelha\b',    'Ear',          r)
    r = re.sub(r'\bPulmoes\b',   'Lungs',        r)
    r = re.sub(r'\bTripa[s]?\b', 'Tripe',        r)
    r = re.sub(r'\bFigado\b',    'Liver',        r)
    r = re.sub(r'\bRins\b',      'Kidneys',      r)
    r = re.sub(r'\bRim\b',       'Kidney',       r)

    # ══════════════════════════════════════════════════════════════════════
    # VEGETABLES / FRUIT / PULSES
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bBeterraba\b',  'Beetroot',     r)
    r = re.sub(r'\bAnona\b',      'Custard Apple', r)
    r = re.sub(r'\bCardamomo\b',  'Cardamom',     r)
    r = re.sub(r'\bLentilhas\b',  'Lentils',      r)
    r = re.sub(r'\bFloretes\b',   'Florets',      r, flags=re.IGNORECASE)

    # ══════════════════════════════════════════════════════════════════════
    # HERBS & SPICES
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bAnis\b',         'Anise',      r)
    r = re.sub(r'\bCanela\b',       'Cinnamon',   r)
    r = re.sub(r'\bCoentro[s]?\b',  'Coriander',  r)
    r = re.sub(r'\bColorau\b',      'Paprika',    r)
    r = re.sub(r'\bCominhos\b',     'Cumin',      r)
    r = re.sub(r'\bCravinho[s]?\b', 'Cloves',     r)
    r = re.sub(r'\bEstragao\b',     'Tarragon',   r)
    r = re.sub(r'\bFuncho\b',       'Fennel',     r)
    r = re.sub(r'\bGengibre\b',     'Ginger',     r)
    r = re.sub(r'\bHortela\b',      'Mint',       r)
    r = re.sub(r'\bManjericao\b',   'Basil',      r)
    r = re.sub(r'\bManjerona\b',    'Marjoram',   r)
    r = re.sub(r'\bOregao[s]?\b',   'Oregano',    r)
    r = re.sub(r'\bPapoila[s]?\b',  'Poppy',      r)
    r = re.sub(r'\bPimenta\b',      'Pepper',     r)
    r = re.sub(r'\bTomilho\b',      'Thyme',      r)
    r = re.sub(r'\bCurcuma\b',      'Turmeric',   r)
    # "Açafrão-da-índia" transliterated as "Acafrao-da-india"
    r = r.replace('Acafrao-da-india', 'Turmeric')
    r = r.replace('Acafrao', 'Saffron')
    # Bay leaf — specific compound first, then bare word
    r = r.replace('Folha Louro', 'Bay Leaf')
    r = re.sub(r'\bLouro\b', 'Bay Laurel', r)

    # ══════════════════════════════════════════════════════════════════════
    # FRUIT
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bAlperce[s]?\b',     'Apricot',    r)
    r = re.sub(r'\bClementina[s]?\b',  'Clementine', r)
    r = re.sub(r'\bDiospiro[s]?\b',    'Persimmon',  r)
    r = re.sub(r'\bGoiaba[s]?\b',      'Guava',      r)
    r = re.sub(r'\bGroselha[s]?\b',    'Redcurrant', r)
    r = re.sub(r'\bLima[s]?\b',        'Lime',       r)
    r = re.sub(r'\bManga[s]?\b',       'Mango',      r)
    r = re.sub(r'\bTamarilho[s]?\b',   'Tamarillo',  r)
    r = re.sub(r'\bToranja[s]?\b',     'Grapefruit', r)
    r = re.sub(r'\bFigo[s]?\b',        'Fig',        r)
    r = re.sub(r'\bRoma[s]?\b',        'Pomegranate', r)
    r = re.sub(r'\bNespera[s]?\b',     'Loquat',     r)
    r = re.sub(r'\bMirtilo[s]?\b',     'Blueberry',  r)
    r = re.sub(r'\bFramboesa[s]?\b',   'Raspberry',  r)
    r = re.sub(r'\bMora[s]?\b',        'Blackberry', r)

    # ══════════════════════════════════════════════════════════════════════
    # VEGETABLES & PULSES (additional)
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bAlfarroba\b',       'Carob',         r)
    r = re.sub(r'\bBagas\b',           'Berries',       r)
    r = re.sub(r'\bFavas\b',           'Fava Beans',    r)
    r = r.replace('Feijao-verde',      'Green Bean')
    r = re.sub(r'\bRebentos\b',        'Sprouts',       r)
    r = re.sub(r'\bBambu\b',           'Bamboo',        r)
    r = re.sub(r'\bRucula\b',          'Rocket',        r)
    r = re.sub(r'\bNabo[s]?\b',        'Turnip',        r)
    r = re.sub(r'\bChicoria\b',        'Chicory',       r)
    r = re.sub(r'\bEspargos\b',        'Asparagus',     r)
    r = re.sub(r'\bEspargo\b',         'Asparagus',     r)
    r = re.sub(r'\bMilhete\b',         'Millet',        r)
    r = re.sub(r'\bTremocos\b',        'Lupin Beans',   r)

    # ══════════════════════════════════════════════════════════════════════
    # ADDITIONAL FOOD TERMS
    # ══════════════════════════════════════════════════════════════════════

    # Vegetables (additional)
    r = re.sub(r'\bCebolinho[s]?\b',     'Chive',         r, flags=re.IGNORECASE)
    r = re.sub(r'\bCebolinha[s]?\b',     'Spring Onion',  r, flags=re.IGNORECASE)
    r = re.sub(r'\bInhame[s]?\b',        'Yam',           r, flags=re.IGNORECASE)
    r = re.sub(r'\bRadicchio\b',         'Radicchio',     r)
    r = re.sub(r'\bRabanete[s]?\b',      'Radish',        r, flags=re.IGNORECASE)
    r = re.sub(r'\bFolhas?\b',           'Leaves',        r, flags=re.IGNORECASE)
    # "Folha" in context of lasagna/pastry = Sheet
    r = r.replace('Lasagna Egg (Leaves)', 'Lasagna Egg (Sheet)')
    r = r.replace('Gelatin (Powder or Leaves)', 'Gelatin (Powder or Sheet)')
    r = r.replace('Gelatin (po or Leaves)', 'Gelatin (Powder or Sheet)')

    # Grains & starches
    r = re.sub(r'\bMacarrao\b',          'Macaroni',      r, flags=re.IGNORECASE)
    r = re.sub(r'\bMacarr[aã]o\b',       'Macaroni',      r, flags=re.IGNORECASE)
    r = re.sub(r'\bSalpicao\b',          'Salpicão Sausage', r, flags=re.IGNORECASE)

    # Seeds
    r = re.sub(r'\bCanhamo\b',           'Hemp',          r, flags=re.IGNORECASE)
    r = re.sub(r'\bLinhaca\b',           'Flaxseed',      r, flags=re.IGNORECASE)

    # Puff pastry — must come BEFORE generic Massa→Pasta
    r = r.replace('Massa Folhada',       'Puff Pastry')
    r = r.replace('Massa folhada',       'Puff Pastry')
    r = re.sub(r'\bFolhados?\b',         'Puff Pastry',   r, flags=re.IGNORECASE)
    r = re.sub(r'\bPastel\b',            'Pastry',        r, flags=re.IGNORECASE)
    r = re.sub(r'\bMassa[s]?\b',         'Pasta',         r)

    # Cheese brands / regions
    r = r.replace('Cheese Parmesao',    'Parmesan Cheese')
    r = r.replace('Cheese Azeitao',     'Azeitão Cheese')
    r = r.replace('Cheese Sao Jorge',   'São Jorge Cheese')
    r = r.replace('Cheese Serra Estrela Velho', 'Aged Serra da Estrela Cheese')
    r = re.sub(r'\bParmesao\b',         'Parmesan',      r, flags=re.IGNORECASE)
    r = re.sub(r'\bVelho\b',            'Aged',          r)

    # Other terms
    r = re.sub(r'\bHumano\b',           'Human',         r)
    r = re.sub(r'\bTransicao\b',        'Transition',    r, flags=re.IGNORECASE)
    r = re.sub(r'\bCulinaria\b',        'Culinary',      r, flags=re.IGNORECASE)
    r = re.sub(r'\bPastilha Elastica\b', 'Chewing Gum',  r, flags=re.IGNORECASE)
    r = re.sub(r'\bPastilha\b',         'Lozenge',       r, flags=re.IGNORECASE)
    # Vinha de alhos = garlic wine marinade
    if 'vinha de alhos' in pt_lower:
        r = re.sub(r'\bVinha\b', 'Garlic Wine Marinade', r, flags=re.IGNORECASE)
    r = re.sub(r'\bPalhete\b',          'Palhete',       r)   # wine type — keep
    # Remove brand name leakage in water entry
    r = re.sub(r'\s*\(Água\s+\w+\)',    '',              r)

    # ══════════════════════════════════════════════════════════════════════
    # PREPARED DISHES & SAUCES
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bBolonhesa\b',       'Bolognese',     r)
    r = re.sub(r'\bCaril\b',           'Curry',         r)
    r = re.sub(r'\bCebolada\b',        'Onion Sauce',   r)
    r = re.sub(r'\bLasanha\b',         'Lasagna',       r)
    r = re.sub(r'\bEspetada\b',        'Skewer',        r)
    r = re.sub(r'\bCondimento\b',      'Condiment',     r)
    # Farinheira = specific Portuguese flour sausage
    r = re.sub(r'\bFarinheira\b',      'Farinheira Sausage', r)
    # Peixinhos da horta = battered/tempura fried green beans
    r = r.replace('Peixinhos Horta',   'Battered Green Beans')
    r = re.sub(r'\bPeixinhos\b',       'Battered Green Beans', r)
    # Word order: "Sauce Francesinha" → "Francesinha Sauce"
    r = r.replace('Sauce Francesinha', 'Francesinha Sauce')
    # Queijada = Portuguese curd tart (specific pastry)
    r = re.sub(r'\bQueijada\b',        'Curd Tart',          r)
    # "po or Leaves" in gelatin context = "Powder or Sheet" (folha de gelatina = gelatin sheet)
    r = r.replace('(po or Leaves)',     '(Powder or Sheet)')
    r = r.replace('(Po or Leaves)',     '(Powder or Sheet)')
    r = r.replace('(Powder or Leaves)', '(Powder or Sheet)')
    r = re.sub(r'\(po\b',              '(Powder',            r)
    # Word order fix: "Leaves Radish" → "Radish Leaves"
    r = r.replace('Leaves Radish',     'Radish Leaves')
    r = re.sub(r'\bAmido\b',           'Starch',        r)
    r = re.sub(r'\bGeleia\b',          'Jelly',         r)
    r = re.sub(r'\bMargarina\b',       'Margarine',     r)
    r = re.sub(r'\bSemola\b',          'Semolina',      r)
    r = re.sub(r'\bMiolo\b',           'Kernel',        r)
    r = re.sub(r'\bNata[s]?\b',        'Cream',         r)
    r = re.sub(r'\bManteiga\b',        'Butter',        r)
    r = re.sub(r'\bMel\b',             'Honey',         r)
    r = re.sub(r'\bAcucar\b',          'Sugar',         r)
    r = re.sub(r'\bAveia\b',           'Oat',           r)
    r = re.sub(r'\bCevada\b',          'Barley',        r)
    r = re.sub(r'\bCenteio\b',         'Rye',           r)
    r = re.sub(r'\bTrigo\b',           'Wheat',         r)
    r = re.sub(r'\bMilho\b',           'Corn',          r)
    r = re.sub(r'\bArranha\b',         'Scratch',       r)   # unlikely but safe
    # Remove parenthesised Portuguese leakage like "(Margarina)"
    r = re.sub(r'\s*\(Margarina\)',    '',              r)

    # Bacalhau (salt cod) — specific dish names before generic
    r = r.replace('Bacalhau A Bras',   'Salt Cod à Brás')
    r = re.sub(r'\bBacalhau\b',        'Salt Cod',      r)

    # Pão de Forma = Sliced Bread — specific compounds before generic
    r = r.replace('Bread Forma Wheat Passas', 'Wheat Sliced Bread with Raisins')
    r = r.replace('Bread Forma Wheat',        'Wheat Sliced Bread')
    r = r.replace('Bread Forma',              'Sliced Bread')
    r = r.replace('Bread Wheat Passas',       'Wholegrain Wheat Bread with Raisins')
    r = re.sub(r'\bForma\b',                  'Sliced',        r)
    # Passas = Raisins (also fixes "(passas)" parentheticals)
    r = re.sub(r'\bPassas?\b',                'Raisins',       r, flags=re.IGNORECASE)

    # Broa (cornbread), Canja (chicken broth soup)
    r = re.sub(r'\bBroa\b',            'Cornbread',     r)
    r = re.sub(r'\bCanja\b',           'Chicken Broth Soup', r)

    # Portuguese cured meats with no single English equivalent — label clearly
    r = re.sub(r'\bPresunto\b',        'Cured Ham',     r)
    r = re.sub(r'\bPaio\b',            'Cured Loin Sausage', r)
    r = re.sub(r'\bLinguica\b',        'Portuguese Sausage', r)
    r = re.sub(r'\bChourico\b',        'Chorizo',       r)

    # Aguardente = brandy/firewater
    r = re.sub(r'\bAguardente\b',      'Brandy',        r)

    # Nuts (Noz = walnut; specific before generic)
    r = r.replace('Noz Macadamia',     'Macadamia Nut')
    r = r.replace('Noz Pecan',         'Pecan Nut')
    r = re.sub(r'\bNoz\b',             'Walnut',        r)
    r = re.sub(r'\bPinhao\b',          'Pine Nut',      r)
    r = re.sub(r'\bAmendoa[s]?\b',     'Almond',        r)

    # Salsa in Portuguese = Parsley (not the Mexican sauce)
    r = re.sub(r'\bSalsa\b',           'Parsley',       r)

    # Mostarda = Mustard
    r = re.sub(r'\bMostarda\b',        'Mustard',       r)

    # Vegetables
    r = re.sub(r'\bPepino[s]?\b',      'Cucumber',      r)
    r = re.sub(r'\bMelancia\b',        'Watermelon',    r)
    r = re.sub(r'\bMelao\b',           'Melon',         r)
    r = re.sub(r'\bMaracuja\b',        'Passion Fruit', r)
    r = re.sub(r'\bBatata[s]?\b',      'Potato',        r)
    r = re.sub(r'\bCenoura[s]?\b',     'Carrot',        r)
    r = re.sub(r'\bCebola[s]?\b',      'Onion',         r)
    r = re.sub(r'\bAlface\b',          'Lettuce',       r)
    r = re.sub(r'\bTomate[s]?\b',      'Tomato',        r)
    r = re.sub(r'\bEspinafre[s]?\b',   'Spinach',       r)
    r = re.sub(r'\bErvilha[s]?\b',     'Pea',           r)
    r = re.sub(r'\bBeringela[s]?\b',   'Aubergine',     r)
    r = re.sub(r'\bAbobora\b',         'Pumpkin',       r)
    r = re.sub(r'\bCogumelo[s]?\b',    'Mushroom',      r)
    r = re.sub(r'\bSalsao\b',          'Celery',        r)
    r = re.sub(r'\bAipo\b',            'Celery',        r)
    r = re.sub(r'\bAlface\b',          'Lettuce',       r)
    r = re.sub(r'\bPimento[s]?\b',     'Bell Pepper',   r)
    r = re.sub(r'\bAzeitona[s]?\b',    'Olive',         r)
    r = re.sub(r'\bGrao\b',            'Chickpea',      r)

    # Fruit
    r = re.sub(r'\bLaranja[s]?\b',     'Orange',        r)
    r = re.sub(r'\bLimao\b',           'Lemon',         r)
    r = re.sub(r'\bMaca[s]?\b',        'Apple',         r)
    r = re.sub(r'\bPera[s]?\b',        'Pear',          r)
    r = re.sub(r'\bUva[s]?\b',         'Grape',         r)
    r = re.sub(r'\bPessego[s]?\b',     'Peach',         r)
    r = re.sub(r'\bCereja[s]?\b',      'Cherry',        r)
    r = re.sub(r'\bAmeixa[s]?\b',      'Plum',          r)
    r = re.sub(r'\bMorango[s]?\b',     'Strawberry',    r)

    # Misc food terms
    r = re.sub(r'\bArroz\b',           'Rice',          r)
    r = re.sub(r'\bFarinha\b',         'Flour',         r)
    r = re.sub(r'\bAzeite\b',          'Olive Oil',     r)
    r = re.sub(r'\bQueijo[s]?\b',      'Cheese',        r)
    r = re.sub(r'\bAmendoim\b',        'Peanut',        r)
    r = re.sub(r'\bNozes\b',           'Walnuts',       r)

    # Colours used as food descriptors
    # "Verde/Verdes" = Green — but NOT inside "Vinho Verde" or "Caldo Verde" (proper names)
    r = re.sub(r'(?<!Vinho )(?<!Caldo )\bVerdes?\b', 'Green', r)
    r = re.sub(r'\bVermelha[s]?\b', 'Red',    r)
    r = re.sub(r'\bEncarnada\b',    'Red',    r)

    # ══════════════════════════════════════════════════════════════════════
    # PROCESSED FOODS
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bMaionese\b',   'Mayonnaise', r)
    r = re.sub(r'\bHamburguer\b', 'Hamburger',  r)
    r = re.sub(r'\bBiscoitos\b',  'Biscuits',   r)
    r = re.sub(r'\bGelatina\b',   'Gelatin',    r)

    # Biscuit sub-types (after Biscoitos→Biscuits above)
    r = r.replace('Biscuits Linguas Gato',  "Cat's Tongue Biscuits")
    r = r.replace('Biscuits Linguas Veado', "Deer Tongue Biscuits")
    r = r.replace('Biscuits Argolas',       "Ring Biscuits")
    r = r.replace('Biscuits Caseiros',      "Homemade Biscuits")

    # ══════════════════════════════════════════════════════════════════════
    # COOKING TERMS & STATES
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bBranqueado\b',        'Blanched',           r)
    r = re.sub(r'\bEscorridos?\b',       'Drained',            r, flags=re.IGNORECASE)
    r = re.sub(r'\bEvaporado\b',         'Evaporated',         r)
    r = re.sub(r'\bForno\b',             'Oven',               r)
    r = re.sub(r'\bBrasa\b',             'Charcoal Grill',     r)
    r = re.sub(r'\bCasei(?:ro|ra)[s]?\b',  'Homemade',           r)  # masc+fem+plural
    r = re.sub(r'\bPanado\b',            'Breaded',            r)
    r = re.sub(r'\bSalgada\b',           'Salted',             r)
    r = re.sub(r'\bEnlatados?\b',        'Canned',             r)   # singular + plural
    r = re.sub(r'\bCozer Ou Estufar\b',  'Boiling or Braising', r, flags=re.IGNORECASE)
    r = re.sub(r'\bCozer\b',             'Boil',               r)
    r = re.sub(r'\bEstufar\b',           'Braise',             r)
    r = re.sub(r'\bPreparada\b',         'Prepared',           r)
    r = re.sub(r'\bPilada\b',            'Shelled',            r)
    r = re.sub(r'\bDemolhadas?\b',       'Soaked',             r, flags=re.IGNORECASE)
    r = re.sub(r'\bFermentad[ao]s?\b',   'Fermented',          r)
    # Nabica = turnip greens
    r = re.sub(r'\bNabica[s]?\b',        'Turnip Greens',      r, flags=re.IGNORECASE)
    # Aves = poultry (birds)
    r = re.sub(r'\bAves\b',              'Poultry',            r)
    r = re.sub(r'\bSecas?\b',            'Dried',              r)
    r = re.sub(r'\bTorrad[ao]s?\b',      'Roasted',            r)
    r = re.sub(r'\bGrelhadoa?s?\b',      'Grilled',            r)
    r = re.sub(r'\bAssad[ao]s?\b',       'Roasted',            r)
    r = re.sub(r'\bCozid[ao]s?\b',       'Boiled',             r)
    r = re.sub(r'\bFrit[ao]s?\b',        'Fried',              r)
    r = re.sub(r'\bEnsopado\b',          'Stew',               r)
    r = re.sub(r'\bRefogado\b',          'Sautéed',            r)
    r = re.sub(r'\bDesidratad[ao]s?\b',  'Dehydrated',         r)
    r = re.sub(r'\bCongelad[ao]s?\b',    'Frozen',             r)
    # Standalone "Po"/"po" = powder (not inside Porco, Polvo, etc.)
    # Match when surrounded by spaces OR at end of string
    r = re.sub(r'(?<=\s)Po\b', 'Powder', r)
    r = re.sub(r'(?<=\s)po\b', 'powder', r)

    # ══════════════════════════════════════════════════════════════════════
    # DESCRIPTORS
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bMagra[s]?\b',     'Lean',   r)
    r = re.sub(r'\bMagro\b',         'Lean',   r)
    r = re.sub(r'\bAberto[sa]?[s]?\b', 'Opened', r)   # masc+fem+plural
    r = re.sub(r'\bAberta[s]?\b',    'Opened', r)     # explicit feminine form
    r = re.sub(r'\bGordo[as]?\b',    'Full-Fat', r)
    r = re.sub(r'\bGorda[s]?\b',     'Full-Fat', r)
    r = re.sub(r'\bIntegral\b',      'Wholegrain', r)
    r = re.sub(r'\bNatural\b',       'Natural',    r)   # already correct but ensures consistency
    r = re.sub(r'\bFumad[ao]s?\b',   'Smoked',     r)
    r = re.sub(r'\bCurad[ao]s?\b',   'Cured',      r)
    r = re.sub(r'\bMoido\b',         'Ground',     r)
    r = re.sub(r'\bMoida\b',         'Ground',     r)
    r = re.sub(r'\bInteiro[as]?\b',  'Whole',      r)
    r = re.sub(r'\bInteira[s]?\b',   'Whole',      r)
    r = re.sub(r'\bRalado\b',        'Grated',     r)
    r = re.sub(r'\bRalada\b',        'Grated',     r)
    r = re.sub(r'\bFatiado[as]?\b',  'Sliced',     r)
    r = re.sub(r'\bFatiada[s]?\b',   'Sliced',     r)
    r = re.sub(r'\bSeco[as]?\b',     'Dried',      r)
    r = re.sub(r'\bSeca[s]?\b',      'Dried',      r)

    # ══════════════════════════════════════════════════════════════════════
    # GRAMMAR
    # ══════════════════════════════════════════════════════════════════════
    r = re.sub(r'\bUht\b', 'UHT', r)
    r = re.sub(r' Ou ',    ' or ', r)
    r = re.sub(r'^Ou ',    'or ', r)

    # Final pass: remaining bare "Cafe" not yet replaced
    r = re.sub(r'\bCafe\b', 'Coffee', r)

    # Post-grammar fixes that depend on "or" already being in place
    # "Gelatin (Powder or Leaves)" — "Leaves" here = sheet, not botanical leaves
    r = r.replace('(Powder or Leaves)', '(Powder or Sheet)')
    r = r.replace('(powder or leaves)', '(Powder or Sheet)')

    # ══════════════════════════════════════════════════════════════════════
    # "SEM" (WITHOUT) FIXES  — applied after word replacements
    # ══════════════════════════════════════════════════════════════════════

    # sem molho = without sauce
    if 'sem molho' in pt_lower and not already_has_without_sauce:
        r = re.sub(r'\bSauce\b', 'without Sauce', r)

    # sem sal = unsalted
    if 'sem sal' in pt_lower and not already_has_without_salt:
        r = re.sub(r'(?<!\w)Salt(?!\w)', 'Unsalted', r)

    # com sal = salted (bare "Salt" at end)
    if 'com sal' in pt_lower and 'sem sal' not in pt_lower:
        r = re.sub(r'(?<!\w)Salt(?!\w)', 'Salted', r)

    # sem espinha = boneless
    if 'sem espinha' in pt_lower:
        r = re.sub(r'\bEspinha\b', 'Boneless', r, flags=re.IGNORECASE)

    # sem açúcar = sugar-free (only fixes the specific bare "sugar" mistranslation)
    if 'sem açúcar' in pt_lower or 'sem acucar' in pt_lower:
        r = re.sub(r'\(sugar\)', '(sugar-free)', r)

    # ══════════════════════════════════════════════════════════════════════
    # PUNCTUATION: add comma between food name and preparation state
    # Pattern: "Forkbeard Cooked" → "Forkbeard, Cooked"
    # Only insert when no comma already precedes the state word.
    # Match state word at end of string OR before a parenthetical or "without/with".
    # ══════════════════════════════════════════════════════════════════════
    PREP_STATES = (
        'Raw', 'Cooked', 'Fried', 'Grilled', 'Smoked', 'Blanched', 'Drained',
        'Boiled', 'Braised', 'Roasted', 'Dried', 'Frozen', 'Fermented',
        'Dehydrated', 'Shelled', 'Breaded', 'Prepared', 'Salted', 'Unsalted',
        'Canned', 'Sliced', 'Grated', 'Opened', 'Stewed', 'Sautéed',
        # Additional preparation/quality adjectives
        'Fresh', 'Natural', 'Sweetened', 'Unsweetened', 'Homemade',
        'Lean', 'Skinless', 'Boneless', 'Ground', 'Whole', 'Creamy',
        'Liquid', 'Soluble', 'Decaffeinated',
        # NOTE: 'Powder' deliberately excluded — "Garlic Powder", "Cocoa Powder" etc.
        # are compound nouns in English and must not be split with a comma.
    )
    for state in PREP_STATES:
        # Insert comma before state word when:
        # - preceded by a non-comma character + space (but NOT by "and " or "or ")
        # - followed by end-of-string, "with/without …", or a parenthetical
        r = re.sub(
            rf'(?<![,])(?<! and)(?<! or )\s+\b({re.escape(state)})\b'
            rf'((?:\s+(?:with(?:out)?\b).*|(?:\s*\().*|$))',
            rf', \1\2',
            r
        )

    return r


# ══════════════════════════════════════════════════════════════════════════
# READ → APPLY → WRITE
# ══════════════════════════════════════════════════════════════════════════
CSV_PATH = '/sessions/eager-beautiful-maxwell/mnt/localization/full_translation_review.csv'

with open(CSV_PATH, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = 0
for row in rows:
    original  = row['english_applied']
    corrected = correct(row['portuguese_source'], original)
    if corrected != original:
        row['reviewed_english'] = corrected
        changed += 1
    else:
        row['reviewed_english'] = ''

with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Rows processed : {len(rows)}")
print(f"Rows corrected : {changed}")
print("File saved.")
