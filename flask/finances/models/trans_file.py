from finances import db

class TransFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    account = db.Column(db.String)

    def __init__(self, name, account):
        self.name = name
        self.account = account

    def __repr__(self):
       return "<TransFile('%s', '%s')>" % (self.name, self.account)


