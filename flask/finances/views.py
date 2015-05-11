from flask import render_template, session, url_for
from finances import db, app
from finances.models.transaction import Transaction
from finances.models.category import Category
from finances.forms import TransactionsForm
import datetime
from monthdelta import monthdelta

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

@app.route('/categories')
def categories():
    q = db.session.query(Category)
    return render_template('categories.html', categories=q)


@app.route('/transactions', methods=['GET', 'POST']) 
@app.route('/transactions/<category_id>', methods=['GET', 'POST']) 
def transactions(category_id=None): 
    form = TransactionsForm()
    if form.validate_on_submit():
        print form.startdate.data
        print form.enddate.data

    q = db.session.query(Transaction)
    if category_id:
        q = q.join(Category).filter(Category.id==int(category_id))

    fr = form.startdate.data
    to = form.enddate.data
    q = q.filter(Transaction.tdate>=fr, Transaction.tdate<=to).order_by(Transaction.tdate)

    return render_template('transactions.html', form=form, transactions=q)

