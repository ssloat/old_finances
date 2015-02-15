from sqlalchemy import create_engine
from finances import Base, Session
from finances.category import Category, CategoryRE, create_categories
from finances.mort_schedule import MortgageSchedule, create_mort_schedule
from finances.transaction import Transaction
import finances.transaction
import finances.files

from finances.trans_file import TransFile 
from finances.tax_rates import add_tax_rates

import re
import datetime
import sys
from monthdelta import MonthDelta

#Base.metadata.create_all(engine) 

class Finance():
    session   = None
    startdate = datetime.date(1900, 1, 1)
    enddate   = datetime.date(2100, 1, 1)

    def __init__(self, db=':memory:'):
        engine = create_engine('sqlite:///' + db, echo=False)
        Base.metadata.create_all(engine) 

        Session.configure(bind=engine)
        self.session = Session()

    def cats(self):
        return [(c.id, c.name, c.parent_id) for c in self.session.query(Category)]

    def categories(self):
        d = dict()
        self._categories(self.session.query(Category).filter_by(parent_id=0).first(), d)

    def _categories(self, cat, d):
        pass
        
    
    def queryParent(self, cat, fr=None, to=None):
        fr = fr or self.startdate 
        to = to or self.enddate

        tmpf = fr.replace(day=1)
        tmpt = to.replace(day=1)
        md = MonthDelta(1)
        headings = ["%17s" % ('category')]
        while tmpf <= tmpt:
            headings.append("%04d-%02d" % (tmpf.year, tmpf.month))
            tmpf = tmpf + md
        headings.append('average')
        headings.append('yearly')

        print ", ".join(["%11s" % (x) for x in headings])

        self._queryParent(cat, fr, to, headings[1:])

    def _queryParent(self, cat, fr, to, headings):
        cat = self.session.query(Category).filter_by(name=cat).first()

        for kid in cat.children:
            q = self.session.query(Transaction).join(Category).\
                    filter(Category.name==kid.name, Transaction.tdate >= fr,
                            Transaction.tdate <= to).\
                    order_by(Transaction.tdate)

            months = {}
            for t in q:
                key = 'yearly' if t.yearly else "%04d-%02d" % (t.tdate.year, t.tdate.month)
                months[key] = months.get(key, 0) + t.amount

            yearly = months.pop('yearly', 0.0)
            total = reduce(lambda x, y: x+y, months.itervalues(), 0.0)

            print "%17s" % (kid.name), 
            if len(months) or yearly:
                for h in headings[:-2]:
                    if h in months:
                        print ", %10.2f" % (months[h]),
                    else:
                        print ", %10.2f" % (0),

                print ", %10.2f, %10.2f" % (total / (len(headings)-2), yearly)
            else:
                print ""
                
            if len(kid.children) > 0:
                self._queryParent(kid.name, fr, to, headings)


    def query(self, cat, fr=None, to=None, tran=None):
        fr = fr or self.startdate
        to = to or self.enddate

        if tran:
            q = self.session.query(Transaction).join(Category).\
                    filter(Category.name==cat, Transaction.tdate >= fr,
                            Transaction.tdate <= to, Transaction.name==tran).\
                    order_by(Transaction.tdate)
        else:
            q = self.session.query(Transaction).join(Category).\
                    filter(Category.name==cat, Transaction.tdate >= fr,
                            Transaction.tdate <= to).\
                    order_by(Transaction.tdate)

        months = {}
        for t in q:
            print t
            key = 'yearly' if t.yearly else "%04d-%02d" % (t.tdate.year, t.tdate.month)
            months[key] = months.get(key, 0) + t.amount

        total = reduce(lambda x, y: x+y, months.itervalues(), 0.0)

        for k in sorted(months.iterkeys()):
            print "%s: %0.2f" % (k, months[k])

        print "%0.2f avg: %0.2f" % (total, total / len(months))

    def revenue(self, fr=None, to=None):
        fr = fr or self.startdate
        to = to or self.enddate

        q = self.session.query(Transaction).join(Category).\
                filter(Category.name!='bofa chk', Transaction.tdate >= fr,
                        Transaction.tdate <= to).\
                order_by(Transaction.tdate)

        months = {}
        for t in q:
            if t.yearly:
                print ",".join([str(x) for x in [t.tdate, t.category.name, t.amount]])
            key = 'yearly' if t.yearly else "%04d-%02d" % (t.tdate.year, t.tdate.month)
            months[key] = months.get(key, 0) + t.amount

        yearly = months.pop('yearly', 0.0)
        total = reduce(lambda x, y: x+y, months.itervalues(), 0.0)

        for k in sorted(months.iterkeys()):
            print "%s: %0.2f" % (k, months[k])

        print "avg:    %0.2f" % (total / len(months))
        print "yearly: %0.2f" % yearly
        print "total:  %0.2f" % (yearly + total)

    def query_account(self, acc_name, fr=None, to=None):
        fr = fr or self.startdate
        to = to or self.enddate

        print acc_name
        q = self.session.query(Transaction).join(TransFile).\
                filter(TransFile.account==acc_name, Transaction.tdate >= fr,
                        Transaction.tdate <= to).\
                order_by(Transaction.tdate)

        months = {}
        for t in q:
            print ','.join(map(str, [ t.tdate, t.name, t.amount ]))
            key = "%04d-%02d" % (t.tdate.year, t.tdate.month)
            months[key] = months.get(key, 0) + t.amount

        if not months.keys():
            return

        total = reduce(lambda x, y: x+y, months.itervalues(), 0.0)

        for k in sorted(months.iterkeys()):
            print "%s: %0.2f" % (k, months[k])

        print "%0.2f avg: %0.2f" % (total, total / len(months))

 
    def setup_db(self):
        create_categories(self.session)
        create_mort_schedule(self.session)
        self.session.commit()

        #d = '/home/stephen/Dropbox/BankStatements/'
        d = './files/'
        finances.files.bofaCreditCardCsv(self.session, d + 'January2012_7377.csv', 2012, 1)
        finances.files.bofaCreditCardCsv(self.session, d + 'February2012_7377.csv', 2012, 2)
        finances.files.bofaCreditCardCsv(self.session, d + 'March2012_7377.csv',   2012, 3)
        finances.files.bofaCreditCardCsv(self.session, d + 'April2012_7377.csv',   2012, 4)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-05-14.txt', 2012, 5)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-06-14.txt', 2012, 6)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-07-14.txt', 2012, 7)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-08-14.txt', 2012, 8)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-09-14.txt', 2012, 9)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-10-15.txt', 2012, 10)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-11-13.txt', 2012, 11)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2012-12-13.txt', 2012, 12)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-01-14.txt', 2013, 1)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-02-13.txt', 2013, 2)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-03-14.txt', 2013, 3)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-04-13.txt', 2013, 4)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-05-13.txt', 2013, 5)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-06-14.txt', 2013, 6)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-07-15.txt', 2013, 7)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-08-14.txt', 2013, 8)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-09-13.txt', 2013, 9)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-10-15.txt', 2013, 10)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-11-14.txt', 2013, 11)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2013-12-13.txt', 2013, 12)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-01-14.txt', 2014, 1)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-02-13.txt', 2014, 2)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-03-14.txt', 2014, 3)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-04-12.txt', 2014, 4)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-05-14.txt', 2014, 5)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-06-13.txt', 2014, 6)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-07-15.txt', 2014, 7)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-08-16.txt', 2014, 8)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-09-13.txt', 2014, 9)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-10-15.txt', 2014, 10)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-11-13.txt', 2014, 11)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-11-13_amex.txt', 2014, 11)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2014-12-13.txt', 2014, 12)
        finances.files.bofaCreditCardTxt(self.session, d + 'eStmt_2015-01-14.txt', 2015, 01)
        finances.files.bofaCreditCardCsv(self.session, d + 'currentTransaction_8733.csv', 2015, 01)

        #finances.files.usaa('/home/stephen/Downloads/stmt.txt')
        finances.files.bofaCheckingCsv(self.session, d + 'bofa_checking_0.txt', 0, 0)
        finances.files.bofaCheckingTxt(self.session, d + 'bofa_checking_1.txt', 0, 0)
        finances.files.bofaCheckingTxt(self.session, d + 'bofa_checking_2014.txt', 0, 0)
        finances.files.bofaCheckingTxt(self.session, d + 'bofa_checking_2015.txt', 0, 0)

        finances.files.usaa(self.session, d + 'usaa_1.csv', 0, 0)

        add_tax_rates(self.session)

        self.session.commit()


if __name__ == '__main__':
    #startdate = datetime.date(2013, 3, 1)
    #startdate = datetime.date(2014, 1, 1)
    startdate = datetime.date(2013, 12, 1)
    enddate   = datetime.date(2015, 1, 31)
    f = Finance('finances.db')
    if sys.argv[1] == 'create':
        f.setup_db()
    elif sys.argv[1] == 'query':
        f.query(sys.argv[2], startdate, enddate, sys.argv[3] if len(sys.argv) > 3 else None)
    elif sys.argv[1] == 'query_acc':
        f.query_account(sys.argv[2], startdate, enddate)
    elif sys.argv[1] == 'queryp':
        f.queryParent(sys.argv[2], startdate, enddate)
    elif sys.argv[1] == 'change':
        t = f.session.query(Transaction).filter_by(id=int(sys.argv[2])).first()
        t.category = f.session.query(Category).filter_by(name=sys.argv[3]).first()
        t.name = sys.argv[4]
        f.session.commit()
    elif sys.argv[1] == 'revenue':
        f.revenue(startdate, enddate)
    else:
        print "Need a selection"



