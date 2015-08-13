import datetime
import sys

from finances import db
from finances.models.investments import InvTransaction

if __name__ == '__main__':
    for t in db.session.query(InvTransaction):
        db.session.delete(t)

    
    with open('../files/investments.csv', 'r') as f:
        for line in f.read().splitlines():
            #date, acc, fund, shares, cost, price, action = line.split(',')
            args = line.split(',')
            date = datetime.date(*map(int, args[0].split('-')))
            shares, cost, price = map(float, args[3:6])
            acc, fund = args[1:3]
            action = args[-1]

            db.session.add( InvTransaction(date, acc, fund, shares, cost, price, action) )

    db.session.commit()

