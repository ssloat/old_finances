from finances import db

class Category(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name      = db.Column(db.String)
    depth     = db.Column(db.Integer, default=0)

    children = db.relationship("Category", 
                backref=db.backref('parent', remote_side=[id])
            )

    def __init__(self, name, parent=None, depth=0):
        self.name   = name
        if parent:
            self.parent = parent
            self.depth  = parent.depth + 1
        else:
            self.depth = depth

    def __repr__(self):
       return "<Category('%s')>" % (self.name)

def allChildren(cat=None):
    cat = cat or db.session.query(Category).filter(Category.name=='top').first()
    results = []
    for c in list(cat.children):
        results.append(c)
        results += allChildren(c)

    return results

def categoriesSelectBox(cat=None):
    cat = cat or db.session.query(Category).filter(Category.name=='top').first()
    #results = [(cat.id, unicode("".join(cat.depth*['&nbsp;'] + [cat.name])))]
    results = [(cat.id, unicode("".join(cat.depth*['..'] + [cat.name])))]
    for c in cat.children:
        results += categoriesSelectBox(c)

    return results
    

class CategoryRE(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    pattern     = db.Column(db.String)
    yearly      = db.Column(db.Boolean, default=False)

    category = db.relationship("Category")

    def __init__(self, name, category, pattern, yearly=False):
        self.name = name
        self.category = category
        self.pattern = pattern
        self.yearly = yearly

    def __repr__(self):
       return "<CategoryRE('%s, %s, %s')>" % (self.name, self.category.name,
               self.pattern)


def create_categories():
    top = Category('top', None, 0)

    jnl = Category('journal', top)
    boachk = Category('bofa chk', jnl)

    trans = Category('transactions', top)

    _401k = Category('401k', trans)

    bofa     = Category('bofa', trans)
    inc      = Category('bofa income', bofa)
    taxes    = Category('inc taxes', bofa)
    pretax   = Category('preTax', bofa)
    match    = Category('401k match', bofa)

    give      = Category('giving', trans)
    rez       = Category('rez', give)
    comp_intl = Category('comp intl', give)
    gfa       = Category('gfa', give)
    keith     = Category('keith', give)
    stanley   = Category('stanley', give)
    keane     = Category('keane', give)
    stott     = Category('stott', give)
    stars     = Category('stars', give)

    house     = Category('house', trans)
    rent      = Category('rent', house)
    mort      = Category('mortgage', house)
    mort_int  = Category('mortgage int', mort)
    mort_prin = Category('mortgage prin', mort)
    htax      = Category('property tax', house)
    hrep      = Category('house maint', house)
    utils     = Category('house utilities', house)
    h_ins     = Category('house insurance', house)

    budget   = Category('budget', trans)
    monthly  = Category('monthly', budget)

    car      = Category('car', budget)
    kona     = Category('kona', budget)
    ent      = Category('entertainment', budget)
    group    = Category('group outing', ent)
    amazon   = Category('amazon', ent)
    movies   = Category('movies', ent)
    sports   = Category('sports', ent)

    food     = Category('food', budget)
    fin      = Category('food in', food)
    fout     = Category('food out', food)
    fogroup  = Category('fo group', fout)
    fosolo   = Category('fo solo', fout)

    uncat    = Category('uncategorized', budget)
    chks     = Category('checks', uncat)
    clothes  = Category('clothes', uncat)
    cash     = Category('cash', uncat)
    girl     = Category('girl', budget)
    dates    = Category('dates', girl)
    presents = Category('presents', girl)
    travel   = Category('travel', budget)

    nontaxable = Category('nontaxable income', trans)

    db.session.add_all([top, 
        jnl, boachk, _401k,
        trans,
        bofa, inc, taxes, pretax, match,
        give, 
        house, rent, mort, mort_int, mort_prin, htax, hrep, utils, h_ins,
        budget, monthly, 
        car, kona, ent, group, amazon, movies, sports, 
        food, fin, fout, fogroup, fosolo, 
        uncat, chks, clothes, cash, girl, dates, presents, travel,
        nontaxable,
    ])

def create_category_res():
    jnl    = db.session.query(Category).filter_by(name='journal').first()
    boachk = db.session.query(Category).filter_by(name='bofa chk').first()

    trans = db.session.query(Category).filter_by(name='transactions').first()

    bofa     = db.session.query(Category).filter_by(name='bofa').first()
    inc      = db.session.query(Category).filter_by(name='bofa income').first()
    taxes    = db.session.query(Category).filter_by(name='inc taxes').first()
    pretax   = db.session.query(Category).filter_by(name='preTax').first()

    give     = db.session.query(Category).filter_by(name='giving').first()

    house     = db.session.query(Category).filter_by(name='house').first()
    rent      = db.session.query(Category).filter_by(name='rent').first()
    mort      = db.session.query(Category).filter_by(name='mortgage').first()
    mort_int  = db.session.query(Category).filter_by(name='mortgage int').first()
    mort_prin = db.session.query(Category).filter_by(name='mortgage prin').first()
    htax      = db.session.query(Category).filter_by(name='property tax').first()
    hrep      = db.session.query(Category).filter_by(name='house maint').first()
    h_ins     = db.session.query(Category).filter_by(name='house insurance').first()

    budget   = db.session.query(Category).filter_by(name='budget').first()
    monthly  = db.session.query(Category).filter_by(name='monthly').first()

    car      = db.session.query(Category).filter_by(name='car').first()
    kona     = db.session.query(Category).filter_by(name='kona').first()
    ent      = db.session.query(Category).filter_by(name='entertainment').first()
    group    = db.session.query(Category).filter_by(name='group outing').first()
    amazon   = db.session.query(Category).filter_by(name='amazon').first()
    movies   = db.session.query(Category).filter_by(name='movies').first()
    sports   = db.session.query(Category).filter_by(name='sports').first()

    food     = db.session.query(Category).filter_by(name='food').first()
    fin      = db.session.query(Category).filter_by(name='food in').first()
    fout     = db.session.query(Category).filter_by(name='food out').first()
    fogroup  = db.session.query(Category).filter_by(name='fo group').first()
    fosolo   = db.session.query(Category).filter_by(name='fo solo').first()

    uncat    = db.session.query(Category).filter_by(name='uncategorized').first()
    chks     = db.session.query(Category).filter_by(name='checks').first()
    clothes  = db.session.query(Category).filter_by(name='clothes').first()
    cash     = db.session.query(Category).filter_by(name='cash').first()
    girl     = db.session.query(Category).filter_by(name='girl').first()
    dates    = db.session.query(Category).filter_by(name='dates').first()
    presents = db.session.query(Category).filter_by(name='presents').first()
    travel   = db.session.query(Category).filter_by(name='travel').first()

    nontaxable = db.session.query(Category).filter_by(name='nontaxable income').first()


    db.session.add( CategoryRE("Check", chks, r"^Check ") )

    db.session.add( CategoryRE("Rent", rent, r"ATM.* DEPOSIT ") )
    #db.session.add( CategoryRE("Rent", rent, r"JPMorgan Chase DES:QuickPay") )
    db.session.add( CategoryRE("Rent", rent, r"Counter Credit") )
    db.session.add( CategoryRE("Bofa chk Interest", nontaxable, r"Interest Earned") )
    db.session.add( CategoryRE("Credit Card cash reward", nontaxable, r"FIA CARD SVCS DES:CASHREWARD") )
    db.session.add( CategoryRE("Credit Card cash reward", nontaxable, r"Bank of America DES:CASHREWARD") )
    db.session.add( CategoryRE("Tax Rebate", nontaxable, r"TAX REBATE", True) )
    db.session.add( CategoryRE("Tax Rebate", nontaxable, r"TAX PRODUCTS PE2", True) )
    db.session.add( CategoryRE("Tax Rebate", nontaxable, r"US TREASURY", True) )
    db.session.add( CategoryRE("Tax Rebate", nontaxable, r"Tax Refund ID", True) )

    db.session.add( CategoryRE("Bofa chk withdrawal ", cash, r"BKOFAMERICA ATM.*WITHDRWL") )
    db.session.add( CategoryRE("Bofa chk withdrawal ", cash, r"WITHDRWL 520") )
    db.session.add( CategoryRE("Bofa chk withdrawal ", cash, r"ATM Operator Refund") )
    db.session.add( CategoryRE("USAA chk withdrawal ", cash, r"444 MAIN ST") )

    db.session.add( CategoryRE("Bofa cc payment", boachk, r"BANK OF AMERICA CREDIT CARD Bill Payment") )
    db.session.add( CategoryRE("Bofa cc payment", boachk, r"Bank of America Credit Card Bill Payment") )
    db.session.add( CategoryRE("USAA cc payment", boachk, r"USAA.COM PAYMNT ") )
    db.session.add( CategoryRE("USAA cc payment", boachk, r"Payment Thank You") )
    db.session.add( CategoryRE("xfer from USAA", boachk, r"USAA CHK-INTRNT DES:TRANSFER ") )
    db.session.add( CategoryRE("xfer from USAA", boachk, r"USAA SAV-INTRNT DES:TRANSFER ") )
    db.session.add( CategoryRE("xfer to brkrg", boachk, r"Online Banking transfer to BRK") )
    db.session.add( CategoryRE("xfer from brkrg", boachk, r"Online Banking transfer from BRK") )
    db.session.add( CategoryRE("xfer to vanguard", boachk, r"VGI-EX IDX ADM DES:INVESTMENT") )
    db.session.add( CategoryRE("usaa cc payment", boachk, r"USAA.COM PMT") )

#    db.session.add( CategoryRE("Mortgage", house, r"Bank of America DES:MORTGAGE") )
    db.session.add( CategoryRE("House Ins", house, r"QBE AMERICAS") )

    db.session.add( CategoryRE("Property Tax", htax, r"Collector Online DES:onlinetax", True) )

    db.session.add( CategoryRE("Home Depot", hrep, r"THE HOME DEPOT ") )
    db.session.add( CategoryRE("Home Depot", hrep, r"HOMEDEPOT") )
    db.session.add( CategoryRE("Menards", hrep, r"MENARDS ") )
    db.session.add( CategoryRE("Ace Hardware", hrep, r"LEN'S ACE ") )
    db.session.add( CategoryRE("Chimney Ext", hrep, r"PAYPAL +FIREPLACE") )
    db.session.add( CategoryRE("Furniture", hrep, r"JUBILEE FURNITURE") )
    db.session.add( CategoryRE("Roto Rooter", hrep, r"ROTO-ROOTER") )
    db.session.add( CategoryRE("Shower head", hrep, r"GUILLENS PLUMBING") )
    db.session.add( CategoryRE("Angie's List", hrep, r"ANGIES LIST") )
    db.session.add( CategoryRE("Furnace/AC", hrep, r"WELLS FARGO CARD DES", True) )
    db.session.add( CategoryRE("Furnace/AC", hrep, r"WFFNB CREDITCARD DES", True) )
    db.session.add( CategoryRE("Tree removal", hrep, r"Tree Service", True) )
    db.session.add( CategoryRE("Tree removal", hrep, r"ElecCheck 1139", True) )

    stott  = db.session.query(Category).filter_by(name='stott').first()
    stars  = db.session.query(Category).filter_by(name='stars').first()
    comp_intl  = db.session.query(Category).filter_by(name='comp intl').first()
    gfa  = db.session.query(Category).filter_by(name='gfa').first()
    rez  = db.session.query(Category).filter_by(name='rez').first()
    keane  = db.session.query(Category).filter_by(name='keane').first()
    keith  = db.session.query(Category).filter_by(name='keith').first()
    stanley  = db.session.query(Category).filter_by(name='stanley').first()

    db.session.add( CategoryRE("John Stott", stott, r"JOHN STOTT MIN") )
    db.session.add( CategoryRE("John Stott", stott, r"LANGHAM PARTNERS") )
    db.session.add( CategoryRE("STARS", stars, r"COLLEGE CHURCH") )
    db.session.add( CategoryRE("STARS", stars, r"^BILL PAY CHECK \d+$") )
    db.session.add( CategoryRE("STARS", stars, r"^Bill Pay Check \d+$") )
    db.session.add( CategoryRE("STARS", stars, r"^Bill Pay Check \d+: COLLEGE CHURCH") )
    db.session.add( CategoryRE("STARS", stars, r"^College Church") )
    db.session.add( CategoryRE("Compassion Intl", comp_intl, r"COMPASSION INT'L") )
    db.session.add( CategoryRE("GFA", gfa, r"Gospel for Asia") )
    db.session.add( CategoryRE("GFA", gfa, r"GOSPEL FOR ASIA") )
    db.session.add( CategoryRE("Rez", rez, r"Resurrection") )
    db.session.add( CategoryRE("Keane", keane, r"TEACHBEYOND") )
    db.session.add( CategoryRE("Keane", keane, r"TeachBeyond") )
    db.session.add( CategoryRE("Keith", keith, r"^Bill Pay Check \d+: GREENHOUSE") )
    db.session.add( CategoryRE("Keith", keith, r"^Bill Pay Check \d+: Greenhouse") )
    db.session.add( CategoryRE("Keith", keith, r"^Greenhouse") )
    db.session.add( CategoryRE("Stanley", stanley, r"GREATEREUROPEMIS") )

    db.session.add( CategoryRE("Jewel", fin, r"JEWEL ") )
    db.session.add( CategoryRE("Marianos", fin, r"MARIANOS ") )
    db.session.add( CategoryRE("Trader Joes", fin, 'TRADER JOE') )
    db.session.add( CategoryRE("Binnys", fin, 'BINNYS BEVERAGE') )
    db.session.add( CategoryRE("Binnys", fin, 'Binny\'s') )
    db.session.add( CategoryRE("Malloys", fin, 'MALLOYS') )
    db.session.add( CategoryRE("King Soopers", fin, 'KING SOOPERS') )
    db.session.add( CategoryRE("Giant", fin, 'GIANT 0756') )

    db.session.add( CategoryRE("Potbelly", fosolo, 'POTBELLY') )
    db.session.add( CategoryRE("Potbelly", fosolo, 'Potbelly') )
    db.session.add( CategoryRE("Dunkin Donuts", fosolo, 'Dunkin\' Donuts') )
    db.session.add( CategoryRE("Dunkin Donuts", fosolo, 'DUNKIN') )
    db.session.add( CategoryRE("Dunkin Donuts", fosolo, 'DD/BR') )
    db.session.add( CategoryRE("Chipotle", fosolo, 'CHIPOTLE') )
    db.session.add( CategoryRE("Wendys", fosolo, 'WENDY\'S') )
    db.session.add( CategoryRE("Wendys", fosolo, 'WENDYS') )
    db.session.add( CategoryRE("Panda Express", fosolo, 'PANDA EXPRESS') )
    db.session.add( CategoryRE("Meatheads", fosolo, 'MEATHEAD') )
    db.session.add( CategoryRE("Portillos", fosolo, 'PORTILLOS') )
    db.session.add( CategoryRE("Starbucks", fosolo, 'STARBUCKS') )
    db.session.add( CategoryRE("Little Caesars", fosolo, 'LITTLE CAESARS') )
    db.session.add( CategoryRE("Barnellis", fosolo, 'BARNELLI\'S') )
    db.session.add( CategoryRE("Venice Cafe", fosolo, 'VENICE CAFE') )
    db.session.add( CategoryRE("Noodles", fosolo, 'NOODLES') )
    db.session.add( CategoryRE("540 Cafeteria", fosolo, 'BAC 540 MADISON') )
    db.session.add( CategoryRE("7-Eleven", fosolo, '7-ELEVEN') )
    db.session.add( CategoryRE("Subway", fosolo, 'SUBWAY') )
    db.session.add( CategoryRE("Panera", fosolo, 'PANERA') )
    db.session.add( CategoryRE("Augustinos", fosolo, 'AUGUSTINO\'?S') )
    db.session.add( CategoryRE("Wing Stop", fosolo, 'WING STOP') )
    db.session.add( CategoryRE("McDonalds", fosolo, 'MCDONALD\'S') )
    db.session.add( CategoryRE("Burger King", fosolo, 'BURGER KING') )
    db.session.add( CategoryRE("Jack Straws", fosolo, 'JACK STRAWS') )
    db.session.add( CategoryRE("Dairy Queen", fosolo, 'DAIRY QUEEN') )
    db.session.add( CategoryRE("Caribou", fosolo, 'CARIBOU COFFEE') )
    db.session.add( CategoryRE("Garret's", fosolo, 'GARRETT POPCORN') )
    db.session.add( CategoryRE("Chick-Fil-A", fosolo, 'CHICK-FIL-A') )
    db.session.add( CategoryRE("I Have a Bean", fosolo, 'I HAVE A BEAN') )
    db.session.add( CategoryRE("Bricks", fosolo, 'BRICKS WOOD') )
    db.session.add( CategoryRE("Lillie's Q", fosolo, "LILLIE'S Q") )
    db.session.add( CategoryRE("Wingstop", fosolo, "WINGSTOP") )
    db.session.add( CategoryRE("Five Guys", fosolo, "FIVE GUYS") )
    db.session.add( CategoryRE("Jamba Juice", fosolo, "JAMBA JUICE") )
    db.session.add( CategoryRE("Chicks n Salsa", fosolo, "CHICKS N SALSA") )
    db.session.add( CategoryRE("Haifa", fosolo, "HAIFA ON CLINTON") )
    db.session.add( CategoryRE("Los Burritos", fosolo, "LOS BURRITOS") )
    db.session.add( CategoryRE("Los Burritos", fosolo, "Los Burritos") )
    db.session.add( CategoryRE("Burrito Beach", fosolo, "BURRITO BEACH") )
    db.session.add( CategoryRE("Jets Pizza", fosolo, "JETS PIZZA") )
    db.session.add( CategoryRE("540 Cafe", fosolo, "BAC PLAZA CAFE") )
    db.session.add( CategoryRE("135 Cafe", fosolo, "VAULT") )
    db.session.add( CategoryRE("135 Cafe", fosolo, "VAULT 5019123") )
    db.session.add( CategoryRE("135 Cafe", fosolo, "VAULT +40063489") )
    db.session.add( CategoryRE("135 Cafe", fosolo, "LASALLE CAFE") )
    db.session.add( CategoryRE("Culvers", fosolo, "CULVERS") )
    db.session.add( CategoryRE("Zoup Soup", fosolo, "ZOUP\] ADAMS") )
    db.session.add( CategoryRE("That Burger Joint", fosolo, "THAT BURGER") )

    db.session.add( CategoryRE("Honey", dates, 'HONEY') )
    db.session.add( CategoryRE("Einstein Bros", dates, 'EINSTEIN BROS') )
    db.session.add( CategoryRE("Bacci", dates, 'MEGA BITES PIZZA') )
    db.session.add( CategoryRE("Il Sogno di Barrella", dates, 'IL SOGNO DI') )
    db.session.add( CategoryRE("Thipi Thai", dates, 'THIPI THAI') )
    db.session.add( CategoryRE("Naf Naf", dates, 'NAF-NAF GRILL') )
    db.session.add( CategoryRE("Giordanos", dates, 'GIORDANO\'S') )
    db.session.add( CategoryRE("Dominos", dates, 'DOMINO\'S') )
    db.session.add( CategoryRE("Boston Market", dates, 'BOSTON MARKET') )
    db.session.add( CategoryRE("Cab's", dates, 'CAB\'S WINE BAR') )
    db.session.add( CategoryRE("Cab's", dates, 'CABS WINE BAR') )
    db.session.add( CategoryRE("The Bank", dates, 'THE BANK') )
    db.session.add( CategoryRE("Adelle's", dates, "ADELLE`S FINE AMERICAN") )

    db.session.add( CategoryRE("Elephant & Castle", fogroup, 'ELEPHANT & CASTLE') )
    db.session.add( CategoryRE("Chilis", fogroup, 'CHILI\'S') )
    db.session.add( CategoryRE("Santa Fe", fogroup, 'SANTA FE RESTAURANT') )
    db.session.add( CategoryRE("Anyways", fogroup, 'ANYWAYS PUB') )
    db.session.add( CategoryRE("Anyways", fogroup, '304 W  Army Trail') )
    db.session.add( CategoryRE("My Thai", fogroup, 'MY THAI') )
    db.session.add( CategoryRE("DMK", fogroup, 'DMK DMK') )
    db.session.add( CategoryRE("DMK", fogroup, 'DMK BURGER BAR') )
    db.session.add( CategoryRE("Joy Yee", fogroup, 'JOY YEE NOODLE') )
    db.session.add( CategoryRE("Egglectic", fogroup, 'EGGLECTIC CAFE') )
    db.session.add( CategoryRE("Red Robin", fogroup, 'RED ROBIN') )
    db.session.add( CategoryRE("Buffalo Wild Wings", fogroup, 'BUFFALO WILD WINGS') )
    db.session.add( CategoryRE("Rock Bottom", fogroup, 'RB YORKTOWN') )
    db.session.add( CategoryRE("Blackberry", fogroup, 'BLACKBERRY MARKET') )
    db.session.add( CategoryRE("Warren's Ale", fogroup, 'WARREN') )
    db.session.add( CategoryRE("New Line", fogroup, 'NEW LINE') )
    db.session.add( CategoryRE("Jefferson Tap", fogroup, 'JEFFERSON TAP') )
    db.session.add( CategoryRE("Northside", fogroup, '^CANTINA ') )
    db.session.add( CategoryRE("Old Towne Pub", fogroup, 'OLD TOWNE PUB') )
    db.session.add( CategoryRE("Linger", fogroup, 'LINGER LINGER') )
    db.session.add( CategoryRE("Giordano's", fogroup, 'GIORDANO') )
    db.session.add( CategoryRE("The Brown Cow", fogroup, 'THE BROWN COW') )
    db.session.add( CategoryRE("Olive Garden", fogroup, 'THE OLIVE GARDEN') )
    db.session.add( CategoryRE("Tap House", fogroup, 'TAP HOUSE GRILL') )
    db.session.add( CategoryRE("Goose Island", fogroup, 'GOOSE ISLAND') )
    db.session.add( CategoryRE("Shannon's Pub", fogroup, "SHANNON'S IRISH PUB") )
    db.session.add( CategoryRE("Boston Beer Works", fogroup, "BOSTON BEER WORKS") )
    db.session.add( CategoryRE("Poag Mahones", fogroup, "POAG MAHONES") )
    db.session.add( CategoryRE("Wisconsin Camping", fogroup, "VILLAGE MARKET WISC DELLS") )
    db.session.add( CategoryRE("Muldoons", fogroup, "MULDOONS") )
    db.session.add( CategoryRE("Dinicos Pizze", fogroup, "DINICO\'S") )
    db.session.add( CategoryRE("Big Bricks", fogroup, "BIG BRICKS") )
    db.session.add( CategoryRE("The Florentine", fogroup, "THE FLORENTINE") )
    db.session.add( CategoryRE("Devil's Lake", fogroup, "DEVIL'S LAKE") )
    db.session.add( CategoryRE("Culvers", fogroup, "CULVER'S") )
    db.session.add( CategoryRE("Heaven on Seven", fogroup, "HEAVEN ON SEVEN") )
    db.session.add( CategoryRE("Warrens", fogroup, "Warrens Ale House") )

    utils = db.session.query(Category).filter_by(name='house utilities').first()
    tv = db.session.query(Category).filter(Category.name=='internet/tv').first()
    gas = db.session.query(Category).filter(Category.name=='gas').first()
    elec = db.session.query(Category).filter(Category.name=='electricity').first()
    water = db.session.query(Category).filter(Category.name=='water').first()

    db.session.add( CategoryRE("Comcast", tv, 'COMCAST CHICAGO') )
    db.session.add( CategoryRE("At&t", tv, 'AT&T BILL') )
    db.session.add( CategoryRE("At&t", tv, 'ATT[* ]BILL PAYMENT') )
    db.session.add( CategoryRE("DirecTv", tv, 'DIRECTV SERVICE') )
    db.session.add( CategoryRE("Nicor", gas, 'NORTHERN ILL') )
    db.session.add( CategoryRE("Nicor", gas, 'Nicor Gas') )
    db.session.add( CategoryRE("ComEd", elec, 'COMED DES:') )
    db.session.add( CategoryRE("Water", water, 'VILLAGE OF GLEN') )

    db.session.add( CategoryRE("Gas", car, 'SHELL OIL') )
    db.session.add( CategoryRE("Gas", car, 'EXXONMOBIL') )
    db.session.add( CategoryRE("Gas", car, 'SPEEDWAY') )
    db.session.add( CategoryRE("Gas", car, 'SUNOCO') )
    db.session.add( CategoryRE("Gas", car, 'RWJ MGMT CO') )
    db.session.add( CategoryRE("Gas", car, 'GLEN ELLYN BP') )
    db.session.add( CategoryRE("Gas", car, 'IRVING PETROL') )
    db.session.add( CategoryRE("IPASS", car, 'IPASS AUTO') )
    db.session.add( CategoryRE("Maint/Repair", car, 'AUTOZONE ' ) )
    db.session.add( CategoryRE("Maint/Repair", car, 'AUTO ZONE ' ) )
    db.session.add( CategoryRE("Maint/Repair", car, 'LORDS AUTO ', True ) )
    db.session.add( CategoryRE("Maint/Repair", car, "LORD'S AUTO ", True ) )
    db.session.add( CategoryRE("Maint/Repair", car, "US AUTO PARTS NETWORK", True ) )
    db.session.add( CategoryRE("Car Tax", car, 'INTERNET VEHICLE ' ) )
    db.session.add( CategoryRE("Car Tax", car, 'IL WEB PLATE RENEWAL ' ) )
    db.session.add( CategoryRE("GE Permit", car, 'GE Car Permit' ) )
    db.session.add( CategoryRE("Parking", car, 'O\'HARE PARK MAINLOT ' ) )
    db.session.add( CategoryRE("Parking", car, 'PARKING METER ' ) )
    db.session.add( CategoryRE("Parking", car, 'ARLINGTON METER PARK' ) )
    db.session.add( CategoryRE("Parking", car, 'COC O\'HARE' ) )
    db.session.add( CategoryRE("Parking", car, 'PARKWHIZ' ) )
    db.session.add( CategoryRE("Parking", car, 'PARKINGMETER' ) )
    db.session.add( CategoryRE("Ticket", car, '18TH JUDICIAL CIRCUIT' ) )
    db.session.add( CategoryRE("Taxi", car, 'CHI TAXI' ) )

    db.session.add( CategoryRE("Verizon", monthly, 'VERIZON WIRELESS') )
    db.session.add( CategoryRE("Verizon", monthly, 'VERIZON WRLS') )
    db.session.add( CategoryRE("Sprint", monthly, 'SPRINT WIRELESS') )
    db.session.add( CategoryRE("Metra", monthly, 'METRA ' ) )
    db.session.add( CategoryRE("Netflix", monthly, 'NETFLIX') )
    db.session.add( CategoryRE("Hand & Stone", monthly, 'HAND & STONE MASSAGE') )
    db.session.add( CategoryRE("Hand & Stone", monthly, 'HAND AND STONE MASSAGE') )
    db.session.add( CategoryRE("Python Anywhere", monthly, 'PYTHONANYWH') )

    #db.session.add( CategoryRE("Car Insurance", monthly, 'USAA P&C' ) )


    db.session.add( CategoryRE("Plane Ticket", travel, 'UNITED A ', True) )
    db.session.add( CategoryRE("Plane Ticket", travel, 'JETBLUE ', True) )
    db.session.add( CategoryRE("Plane Ticket", travel, 'SPIRIT A ', True) )
    db.session.add( CategoryRE("Rental Car", travel, 'HOTWIRE-SALES', True) )
    db.session.add( CategoryRE("Gas", travel, 'KUM & GO', True) )
    db.session.add( CategoryRE("Gas", travel, 'HUCK\'S FOOD', True) )
    db.session.add( CategoryRE("Gas", travel, "BUCKY'S EXPRESS", True) )
    db.session.add( CategoryRE("Gas", travel, "LEXINGTON TRAVEL PLZ", True) )
    db.session.add( CategoryRE("Gas", travel, "MENTZER I-80", True) )
    db.session.add( CategoryRE("Gas", travel, "SUPERAMERICA", True) )
    db.session.add( CategoryRE("Gas", travel, "SNYDER'S GATEWAY", True) )
    db.session.add( CategoryRE("Gas", travel, "MURPHY7248ATWALMRT", True) )
    db.session.add( CategoryRE("Hotel", travel, "LA QUINTA", True) )
    db.session.add( CategoryRE("Hotel", travel, "HOTELS\.COM", True) )
    db.session.add( CategoryRE("Taxi", travel, "BOSTON TAXI", True) )
    db.session.add( CategoryRE("Taxi", travel, "BOS TAXI", True) )
    db.session.add( CategoryRE("Taxi", travel, "NAPERVILLE TAXI", True) )
    db.session.add( CategoryRE("Book", travel, "BARBARAS BOOKSTORE", True) )
    db.session.add( CategoryRE("NY Subway", travel, "MTA MVM", True) )
    db.session.add( CategoryRE("Chicago L", travel, "VENTRA VENDING", True) )
    
    db.session.add( CategoryRE("Petsmart", kona, 'PETSMART INC') )
    db.session.add( CategoryRE("Petco", kona, 'PETCO ') )
    db.session.add( CategoryRE("Vet", kona, 'GLENDALE ANIMAL') )
    db.session.add( CategoryRE("Dog id", kona, 'DOGIDS') )
    db.session.add( CategoryRE("Dog park", kona, 'Dog Park') )

    db.session.add( CategoryRE("Redbox", movies, 'REDBOX +\*?DVD') )
    db.session.add( CategoryRE("Movie Theater", movies, 'STUDIO MOVIE GR') )
    db.session.add( CategoryRE("Movie Theater", movies, 'AMC YORKTOWN') )
    db.session.add( CategoryRE("Movie Theater", movies, 'OGDEN 6') )
    db.session.add( CategoryRE("Movie Theater", movies, 'REGAL CANTERA') )
    db.session.add( CategoryRE("Movie Theater", movies, 'REGAL CINEMAS') )
    db.session.add( CategoryRE("Movie Theater", movies, 'WOODFIELD 20') )
    db.session.add( CategoryRE("Movie Theater", movies, 'FANDANGO') )
    db.session.add( CategoryRE("Movie Theater", movies, 'CINEMARK THEAT') )
    db.session.add( CategoryRE("Movie Theater", movies, 'REGAL KINGSTOWNE') )
    db.session.add( CategoryRE("Movie Theater", movies, 'ADDISON CINEMAS') )
    db.session.add( CategoryRE("Movie Theater", movies, 'PICTURE SHOW') )
    db.session.add( CategoryRE("Amazon VOD", movies, 'AMAZON VIDEO ON DEMAND') )
    db.session.add( CategoryRE("Amazon VOD", movies, 'Amazon Video On Demand') )

    db.session.add( CategoryRE("Google", ent, 'GOOGLE') )
    db.session.add( CategoryRE("Amazon", amazon, 'AMAZON.COM') )
    db.session.add( CategoryRE("Amazon", amazon, 'Amazon.com') )
    db.session.add( CategoryRE("Amazon", amazon, 'AMAZON DIGITAL') )
    db.session.add( CategoryRE("Amazon", amazon, 'AMAZON MKTPLACE') )
    db.session.add( CategoryRE("Amazon Prime", ent, 'AMAZONPRIME') )
    db.session.add( CategoryRE("Amazon Prime", ent, 'AmazonPrime Membership') )
    db.session.add( CategoryRE("Newegg", ent, 'NEWEGG.COM') )
    db.session.add( CategoryRE("Best Buy", ent, 'BEST BUY CO') )
    db.session.add( CategoryRE("Groupon", ent, 'GROUPON INC') )
    db.session.add( CategoryRE("Goodwill", ent, 'GOODWILL') )
    db.session.add( CategoryRE("Fox Soccer", ent, 'FOXSOCCER') )
    db.session.add( CategoryRE("ESPN Insider", ent, 'ESPN') )
    db.session.add( CategoryRE("Ravinia", group, 'RAVINIA') )
    db.session.add( CategoryRE("Bowling", group, 'CHALET LANES') )
    db.session.add( CategoryRE("Cubs", group, '2WRIGLEY FIELD') )
    db.session.add( CategoryRE("FIFA 15", ent, 'PAYPAL \*MICROSOFTCO') )
    db.session.add( CategoryRE("Kindle", amazon, 'Amazon Services-Kindle') )

    db.session.add( CategoryRE("TJ and Dave", group, 'TJANDDAVE') )
    db.session.add( CategoryRE("Marine Museum", group, 'NATL MUSEUM OF TRIANGLE') )
    db.session.add( CategoryRE("Architecture Boat", group, 'TM - TICKETMASTER L\.') )
    db.session.add( CategoryRE("Solemn Oath", group, 'SOLEMN OATH BREWERY') )
    db.session.add( CategoryRE("Dry City", group, 'DRYCITY BREW WORKS') )
    db.session.add( CategoryRE("The Moth", group, 'TIX\*THEMOTH') )

    db.session.add( CategoryRE("Cantigny", dates, 'CANTIGNY VISITORS CENT') )
    db.session.add( CategoryRE("Art Museum", dates, 'MUSEUM TICKETS') )

    db.session.add( CategoryRE("Earrings", presents, "MACY'S") )
    db.session.add( CategoryRE("Mixer", presents, "EVERYTHING KITCHENS") )
    db.session.add( CategoryRE("Flowers", presents, "FTD FTD.COM") )
    db.session.add( CategoryRE("Christmas Lights", presents, "TICKETFLY EVENTS") )
    db.session.add( CategoryRE("Diecast Model", presents, "DIECASTMODELSWHOLES") )

    db.session.add( CategoryRE("Run 4 Stars", sports, 'ACT\*RUNFORSTAR') )
    db.session.add( CategoryRE("8 miler", sports, 'GET ME REGISTERED') )
    db.session.add( CategoryRE("NCA 5k", sports, 'NAPERVILLE CHRISTIAN') )
    db.session.add( CategoryRE("Human Race", sports, 'HUMAN RACE') )
    db.session.add( CategoryRE("Chicago Half", sports, 'CHIHALFREG') )
    db.session.add( CategoryRE("Chicago Half", sports, 'CHRONO RUN BIKE REG') )
    db.session.add( CategoryRE("Chicago Half", sports, 'CT EVENT REG') )
    db.session.add( CategoryRE("Marathon", sports, 'BK OF AM CHICAGO MARAT') )
    db.session.add( CategoryRE("Shamrock Shuffle", sports, 'BK OF AM SHAMROCK') )
    db.session.add( CategoryRE("Run 4 Animals", sports, 'RUNFORANIM') )
    db.session.add( CategoryRE("Run 4 Animals", sports, 'ACT\*ACTIVE.comC-187') )
    db.session.add( CategoryRE("Des Plaines Half", sports, 'RUN RACE') )
    db.session.add( CategoryRE("Running Watch", sports, 'ERICFARRELL') )
    db.session.add( CategoryRE("Bike", sports, 'ELEMENT MULTISPORT GLE') )
    db.session.add( CategoryRE("Bike", sports, 'PRAIRIE PATH CYCLES', True) )
    db.session.add( CategoryRE("Soccer", sports, 'THE SOCCER EDGE') )

    db.session.add( CategoryRE("sport shoes", sports, 'RUN TODAY CORP') )
    db.session.add( CategoryRE("sport shoes", sports, 'THE SOCCER POST') )

    db.session.add( CategoryRE("sports authority", sports, 'SPORTS AUTHORI') )
    db.session.add( CategoryRE("sports authority", sports, 'MC SPORTS') )

    db.session.add( CategoryRE("Target", uncat, 'TARGET') )
    db.session.add( CategoryRE("CVS", uncat, 'CVS ') )
    db.session.add( CategoryRE("CVS", uncat, 'CVS/PHARM') )
    db.session.add( CategoryRE("CVS", uncat, 'HIGHLAND PARK CVS') )
    db.session.add( CategoryRE("Staples", uncat, 'STAPLES') )
    db.session.add( CategoryRE("Walgreens", uncat, 'WALGREENS') )
    db.session.add( CategoryRE("Dental", uncat, 'DISTINCTIVE DENTAL') )
    db.session.add( CategoryRE("Optometry", uncat, 'GLEN ELLYN FAMILY EYE') )
    db.session.add( CategoryRE("Doctor", uncat, 'CORNERSTONE MEDICAL') )
    db.session.add( CategoryRE("Tax Prep", uncat, 'TURBOTAX') )
    db.session.add( CategoryRE("Tax Prep", uncat, 'EVANHOUSE') )

    db.session.add( CategoryRE("Retreat", uncat, 'CHURCH OF RESSURECTION') )

    db.session.add( CategoryRE("Old Navy", clothes, 'OLD NAVY') )
    db.session.add( CategoryRE("Jos A Bank", clothes, 'JOSABANK') )
    db.session.add( CategoryRE("Kohls", clothes, "KOHL'S") )

