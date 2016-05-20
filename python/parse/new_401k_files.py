import string

FUNDS_MAP = {
        'MFS INTERNATIONAL GROWTH': 'MFS INTL GRTH',
        'VANGUARD INSTITUTIONAL INDEX': 'VANG INST INDEX PLUS',
        'VANGUARD EXTENDED MARKET INDEX': 'VANG EXT MKT IDX IP',
        'PIMCO TOTAL RETURN PORT. INSTL': 'PIM TOTAL RT INST',
        'VANGUARD INFLATION-PROTECTED': 'VANG INFL-PROT SEC',

#        'VANG INFL-PROT SEC':   'VIPIX',
#        'PIM TOTAL RT INST':    'PTTRX',
#        'VANG EXT MKT IDX IP':  'VEMPX',
#        'VANG INST INDEX PLUS': 'VIIIX',
#        'STABLE VALUE FUND':    'STABLE',
#        'INTEREST CREDIT 10YR': 'INT10YR',
#        'VANGUARD STK MKT IDX': 'VITPX',
#        'FID DIVERSIFD INTL':   'FDIVX',
#        'BAC COM STK FUND':     'BACSTKFND',
#        'VANGUARD TOT STK MKT': 'VITPX',
#        'LIFEPATH 2045 Q':      'LIFEPATH',
}

if __name__ == '__main__':

    with open('../files/401k_2016_contrib.txt') as f:
        for line in f.read().splitlines()[1:]:
            date, fund, contrib, _, match, shares, cost = line.split('\t')
            fund = string.rstrip(fund)
            date = string.rstrip(date)
            contrib = float(contrib[1:])
            match = float(match[1:])
            cost = float(cost[1:])
            shares = float(shares)

            perc = contrib / (contrib + match)



            if contrib > 0.0:
                print ",".join([date, FUNDS_MAP[fund], 'Personal Contrib', str(contrib), '%.4f' % (perc*shares)])

            if match > 0.0:
                print ",".join([date, FUNDS_MAP[fund], 'BofA Match', str(match), '%.4f' % (shares-perc*shares)])

    '''
    with open('../files/401k_2015_fee.txt') as f:
        for line in f.read().splitlines()[1:]:
            date, fund, cost, shares, _ = line.split('\t')
            date = string.rstrip(date)
            fund = string.rstrip(fund)
            cost = -1*float(cost[1:])
            shares = -1*float(shares)

            print ",".join([date, FUNDS_MAP[fund], 'RECORDKEEPKING FEE', str(cost), str(shares)])

    with open('../files/401k_2015_dividends.txt') as f:
        for line in f.read().splitlines()[1:]:
            fund, date, cost, shares, _ = line.split('\t')
            fund = string.rstrip(fund)
            date = string.rstrip(date)
            cost = float(cost[1:])
            shares = float(shares)

            print ",".join([date, FUNDS_MAP[fund], 'Dividends', str(cost), str(shares)])

    '''
