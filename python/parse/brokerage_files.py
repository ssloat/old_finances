import datetime
import string
import re

def parse_date(s):
    mm, dd, yyyy = map(int, s.split('/'))
    return str(datetime.date(yyyy, mm, dd))

FUNDS_MAP = {
        'VANG INFL-PROT SEC':   'VIPIX',
        'PIM TOTAL RT INST':    'PTTRX',
        'VANG EXT MKT IDX IP':  'VEMPX',
        'VANG INST INDEX PLUS': 'VIIIX',
        'STABLE VALUE FUND':    'STABLE',
        'MFS INTL GRTH':        'MFS',
        'INTEREST CREDIT 10YR': 'INT10YR',
        'VANGUARD STK MKT IDX': 'VITPX',
        'FID DIVERSIFD INTL':   'FDIVX',
        'BAC COM STK FUND':     'BACSTKFND',
        'VANGUARD TOT STK MKT': 'VITPX',
        'LIFEPATH 2045 Q':      'LIFEPATH',
}

        
if __name__ == '__main__':
    for fn in ['pension_history.csv', 'pension_2015.csv']:
        with open('../files/%s' % fn) as f:
            for line in f.read().splitlines():
                date, fund, action, cost, shares = line.split(',')
                date = parse_date(date)
                #db.session.add( InvTransaction(date, 'Pension', FUNDS_MAP[fund], float(shares), float(cost), float(cost) / float(shares), action) )
                print ",".join([date, 'Pension', FUNDS_MAP[fund], shares, cost, str(float(cost) / float(shares)), action]) 

    for year in range(2006, 2017):
        with open('../files/401k_%s.csv' % year) as f:
            for line in f.read().splitlines():
                date, fund, action, cost, shares = line.split(',')
                date = parse_date(date)
                #db.session.add( InvTransaction(date, '401k', FUNDS_MAP[fund], float(shares), float(cost), float(cost) / float(shares), action) )
                print ",".join([date, '401k', FUNDS_MAP[fund], shares, cost, str(float(cost) / float(shares)), action]) 

    files = ['roth.csv'] + ['brokerage_%s.csv' % yr for yr in range(2012, 2017)]
    for fn in files:
        dividends = {}
        reinv = set()
        with open('../files/%s' % fn, 'r') as f:
            for line in f.read().splitlines()[1:]:
                data = line[1:-1].split('","')
        
                if data[6] == 'SecurityTransactions':
                    if data[7] == 'Divd Reinv':
                        match = re.match(r'.* REINV AMOUNT +\$([0-9.]+) +REINV PRICE +\$([0-9.]+) +QUANTITY BOT +([0-9\.]+) .*', data[8])
                        cost, price, qty = [match.group(x) for x in range(1, 4)] 
                        date = parse_date(data[1])
                        reinv.add(date+'-'+data[3])
                        print ",".join([date, data[3], data[9], qty, cost, price, data[7]])

                    elif data[7] == 'Journal Entry':
                        match = re.match(r'.* \$(\d+\.\d+)', data[8])
        
                        #db.session.add( InvTransaction(parse_date(data[1]), 'Brokerage', data[9], float(data[10]), float(data[-1]), float(match.group(1)), data[7]) )

                    elif data[7] == 'Stock Dividend':
                        match = re.match(r'.* ([0-9.]+) .*', data[8])

                        print ",".join([parse_date(data[1]), data[3], data[9], data[10], '0.0', match.group(1), data[7]])

                    elif data[7] == 'Purchase ' or data[7] == 'Sale ':
                        match = re.match(r'.* FRAC SHR QUANTITY +(.\d+)', data[8])
                        asset, qty, price, cost = data[-4:]
                        qty = float(qty)
                        if match:
                            qty = qty + (1 if qty>0 else -1) * float(match.group(1))

                        cost = cost.replace(',', '') 
                        if cost[0] == '(':
                            cost = '-'+cost[1:-1]
                        print ",".join([parse_date(data[1]), data[3], asset, str(qty), cost, price, data[7][:-1]])

                    elif data[7] == 'DUDB':
                        pass
                    else:
                        raise Exception("Unknown Security Transaction: %s" % data)

                elif data[6] == 'DividendAndInterest':
                    if data[7] in ['Dividend', 'Lg Tm Cap Gain', 'Sh Tm Cap Gain']:
                        div = '-'+data[-1][1:-1] if data[-1][0] == '(' else data[-1]
                        date = parse_date(data[1])
                        dividends[date+'-'+data[3]] = [date, data[3], data[-4], '0.0', div, '0.0', data[7]]
                    elif data[7] == 'Bank Interest':
                        pass
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))

                elif data[6] == 'Other':
                    if data[7] == 'Reinvestment':
                        pass
                    elif data[7] == 'Journal Entry' and re.search(r'SLOAT CASH GRANT', data[8]):
                        pass
                        #Not Brokerage item
                        #db.session.add( BrokerageT(data[1], 'N/A', 0.0, float(div), 0.0, 'Cash Grant') )
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))

                elif data[6] == 'FundTransfers':
                    if data[7] == 'Funds Transfer':
                        pass
                    else:
                        raise Exception("Unknown type: %s %s" % (data[6], data[7]))
                else:
                    raise Exception("Unknown category: %s %s" % (data[6], data[7]))

        for k, v in dividends.items():
            if k in reinv:
                continue

            print ",".join(v)

    with open('../files/vanguard.txt') as f:
        for line in f.read().splitlines():
            line = line.replace(',', '')

            date, fund, action, shares, price, amount = [string.rstrip(x) for x in line.split('\t')]
            mm, dd, yyyy = date.split('/')
            date = '-'.join([yyyy, mm, dd])

            shares = float(shares)
            price = float(price[1:])
            amount = float(amount[1:])

            if action == 'Buy':
                action = 'Purchase'
                amount = -1*amount
            elif action == 'Dividend':
                action = 'Divd Reinv'

            print ",".join([date, 'BROKERAGE', fund, str(shares), str(amount), str(price), action])

