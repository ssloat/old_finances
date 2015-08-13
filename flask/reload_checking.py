from finances import db
import finances.models.files
from finances.models.transaction import Transaction
from finances.models.trans_file import TransFile

if __name__ == '__main__':
    trans_file = db.session.query(TransFile).filter_by(name='bofa_checking_2015.txt').first()
    if trans_file:
        for t in db.session.query(Transaction)\
                .join(TransFile)\
                .filter(TransFile.name==trans_file.name)\
                .order_by(Transaction.tdate):

            db.session.delete(t)

    else:
        "Didn't find file"

        import sys
        sys.exit()

    
    finances.models.files.bofaCheckingTxt('../files/bofa_checking_2015.txt', 0, 0)

    db.session.commit()


