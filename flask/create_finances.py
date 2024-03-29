from finances import db

import datetime

import finances.models.files
from finances.models.category import create_categories
from finances.models.mort_schedule import create_mort_schedule
from finances.models.investments import create_investments
from finances.models.stock import load_prices

db.create_all()

db.session.commit()

create_categories()
create_mort_schedule()

#d = '/home/stephen/Dropbox/BankStatements/'
d = '../files/'
finances.models.files.bofaCreditCardCsv(d + 'January2012_7377.csv', 2012, 1)
finances.models.files.bofaCreditCardCsv(d + 'February2012_7377.csv', 2012, 2)
finances.models.files.bofaCreditCardCsv(d + 'March2012_7377.csv',   2012, 3)
finances.models.files.bofaCreditCardCsv(d + 'April2012_7377.csv',   2012, 4)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-05-14.txt', 2012, 5)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-06-14.txt', 2012, 6)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-07-14.txt', 2012, 7)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-08-14.txt', 2012, 8)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-09-14.txt', 2012, 9)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-10-15.txt', 2012, 10)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-11-13.txt', 2012, 11)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2012-12-13.txt', 2012, 12)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-01-14.txt', 2013, 1)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-02-13.txt', 2013, 2)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-03-14.txt', 2013, 3)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-04-13.txt', 2013, 4)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-05-13.txt', 2013, 5)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-06-14.txt', 2013, 6)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-07-15.txt', 2013, 7)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-08-14.txt', 2013, 8)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-09-13.txt', 2013, 9)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-10-15.txt', 2013, 10)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-11-14.txt', 2013, 11)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2013-12-13.txt', 2013, 12)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-01-14.txt', 2014, 1)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-02-13.txt', 2014, 2)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-03-14.txt', 2014, 3)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-04-12.txt', 2014, 4)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-05-14.txt', 2014, 5)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-06-13.txt', 2014, 6)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-07-15.txt', 2014, 7)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-08-16.txt', 2014, 8)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-09-13.txt', 2014, 9)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-10-15.txt', 2014, 10)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-11-13.txt', 2014, 11)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-11-13_amex.txt', 2014, 11)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2014-12-13.txt', 2014, 12)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-01-14.txt', 2015, 01)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-02-16.txt', 2015, 02)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-03-16.txt', 2015, 03)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-04-16.txt', 2015, 04)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-05-16.txt', 2015, 05)
finances.models.files.bofaCreditCardTxt(d + 'eStmt_2015-06-16.txt', 2015, 06)
#finances.models.files.bofaCreditCardCsv(d + 'currentTransaction_8733.csv', 2015, 01)

#finances.models.files.usaa('/home/stephen/Downloads/stmt.txt')
finances.models.files.bofaCheckingCsv(d + 'bofa_checking_0.txt', 0, 0)
finances.models.files.bofaCheckingTxt(d + 'bofa_checking_1.txt', 0, 0)
finances.models.files.bofaCheckingTxt(d + 'bofa_checking_2014.txt', 0, 0)
finances.models.files.bofaCheckingTxt(d + 'bofa_checking_2015.txt', 0, 0)

finances.models.files.usaa(d + 'usaa_1.csv', 0, 0)

#add_tax_rates(db.session)
#create_budget(db.session)
create_investments()
for yr in range(2008, 2016):
    load_prices(datetime.date(yr, 1, 1), datetime.date(yr, 12, 31))

db.session.commit()


