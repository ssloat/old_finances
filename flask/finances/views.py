from flask import render_template
from finances import db, app
from finances.models.transaction import Transaction
from finances.models.category import Category
import datetime

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/transactions') 
@app.route('/transactions/<category>') 
def transactions(category=None): 
    fr = datetime.date(2015, 1, 1)
    to = datetime.date(2015, 12, 31)

    if category:
        q = db.session.query(Transaction).join(Category).\
                filter(Category.name=='giving', Transaction.tdate >= fr,
                        Transaction.tdate <= to).\
                order_by(Transaction.tdate)
    else:
        q = db.session.query(Transaction).\
                filter(Transaction.tdate >= fr,
                        Transaction.tdate <= to).\
                order_by(Transaction.tdate)

    return render_template('transactions.html', transactions=q)

