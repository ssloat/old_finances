from finances import db
import finances.models.files
from finances.models.transaction import Transaction
from finances.models.trans_file import TransFile

import sys
import datetime

if __name__ == '__main__':
    start = datetime.date(*(map(int, sys.argv[1].split('-'))))
    end = datetime.date(*(map(int, sys.argv[2].split('-'))))

    trans_file = db.session.query(TransFile).filter_by(name='bofa_checking_2015.txt').first()
    print start, end, trans_file
    if trans_file:
        print trans_file
        for t in db.session.query(Transaction)\
                .join(TransFile)\
                .filter(TransFile.name==trans_file.name, 
                        Transaction.tdate>=start,
                        Transaction.tdate<=end)\
                .order_by(Transaction.tdate):

            print t
            db.session.delete(t)

    else:
        "Didn't find file"

        import sys
        sys.exit()

    finances.models.files.bofaCheckingTxt('../files/bofa_checking_2015.txt', 0, 0, start, end)

    db.session.commit()


