import datetime
import sys
from os import path

from finances import db
import finances.models.files
from finances.models.transaction import Transaction
from finances.models.trans_file import TransFile

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage: filename yyyy-mm"
        sys.exit()

    trans_file = db.session.query(TransFile).filter_by(name=path.basename(sys.argv[1])).first()
    if trans_file:
        for t in db.session.query(Transaction)\
                .join(TransFile)\
                .filter(TransFile.name==trans_file.name)\
                .order_by(Transaction.tdate):

            db.session.delete(t)

    
    finances.models.files.bofaCreditCardCsv(sys.argv[1], *map(int, sys.argv[2].split('-')))

    db.session.commit()

