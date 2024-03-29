from finances.category import Category, CategoryRE
from finances.transaction import Transaction
from finances.trans_file import TransFile
from finances import Base
import finances.transaction

import re
import datetime
from os import path

from sqlalchemy import Column, Integer, String


def bofaCreditCardTxt(session, filename, year, month):
    _readFile(session, filename, 'BOA Credit Card', _ccTransTxt, year, month)

def _ccTransTxt(line, year, month):
    line = line.strip()

    if not re.search('^\d\d/\d\d\s+\d\d/\d\d\s+', line) or re.search('PAYMENT - THANK', line):
        return None, None, None

    if (int(line[0:2]) > month):
        year = year - 1

    dt = datetime.date(year, int(line[0:2]), int(line[3:5]))
    des = line[23:68].strip()
    amt = line.split()[-1].replace(",", "")

    return -1 * float(amt), dt, des

def bofaCreditCardCsv(session, filename, year, month):
    _readFile(session, filename, 'BOA Credit Card', _ccTransCsv, year, month)

def _ccTransCsv(line, year, month):
    line = line.strip().replace("\"", "")
    dt, idn, des, loc, amt = line.split(',')

    if dt == 'Posted Date' or float(amt) >= 0:
        return None, None, None

    m, d, y = map(int, dt.split('/'))
    return float(amt), datetime.date(y, m, d), des

def bofaCheckingCsv(session, filename, year, month):
    _readFile(session, filename, 'BOA Checking', _chkTransCsv, year, month)

def _chkTransCsv(line, year, month):
    if not re.match('^\d\d/\d\d/\d\d\d\d,"', line):
        return None, None, None

    m, d, y = line[:10].split('/')
    dt = datetime.date(int(y), int(m), int(d))

    des, amt, bal = line[12:-1].split('","')

    if not amt:
        return None, None, None

    return float(amt), dt, des

def bofaCheckingTxt(session, filename, year, month):
    _readFile(session, filename, 'BOA Checking', _chkTransTxt, year, month)

def _chkTransTxt(line, year, month):
    if not re.match('^\d\d/\d\d/\d\d\d\d ', line):
        return None, None, None

    m, d, y = line[:10].split('/')
    dt = datetime.date(int(y), int(m), int(d))

    line = line[12:].strip()

    amt = line[-24:]
    amt = amt[:12].strip().replace(",", "")
    if not amt:
        return None, None, None

    des = line[:-24].strip()

    return float(amt), dt, des

def usaa(session, filename, year, month):
    _readFile(session, filename, 'USAA', _usaa, year, month)

def _usaa(line, year, month):
    if not re.match('posted,', line):
        return None, None, None

    line = line.strip()
    junk1, junk2, dt, junk3, des, grp, amt = line.split(',')

    m, d, y = map(int, dt.split('/'))
    return float(amt), datetime.date(y, m, d), des


def _readFile(session, filename, acc_name, parser, year, month):
    uncat = session.query(Category).filter_by(name='uncategorized').first()
    res = session.query(CategoryRE).all()
    print "read " + filename

    trans_file = TransFile(path.basename(filename), acc_name)
    session.add( trans_file )
    with open(filename, 'r') as f:
        for line in f:
            amt, dt, des = parser(line, year, month)
            if not amt:
                continue

            yearly = None
            if re.match("Check ", des, flags=re.IGNORECASE) and amt < -500:
                if (dt == datetime.date(2014, 3, 15) and amt == -900) \
                or (dt == datetime.date(2014, 4, 30) and amt == -1000) \
                or amt < -1500:
                    yearly = True
                des = "Resurrection"

            if re.match("JPM", des) and amt==-1333.66:
                finances.transaction.mortgage(session, dt, amt, trans_file)
            elif re.match("Bank of America DES:MORTGAGE", des):
                finances.transaction.bac_mortgage(session, dt, amt, trans_file)

            elif re.match("BANK OF AMERICA DES:PAYROLL", des):
                finances.transaction.bofa(session, dt, amt, trans_file)

            else:
                for r in res:
                    if re.search(r.pattern, des):
                        session.add( 
                                Transaction(dt, r.name, r.category, amt,
                                    trans_file, yearly=yearly or r.yearly
                                ) 
                            )
                        break
                else:
                    print "Uncategorized: %s, %s, %s" % (dt, des, amt)
                    session.add( Transaction(dt, des, uncat, amt, trans_file) )

    f.closed


#if __name__ == '__main__':
