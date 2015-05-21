from flask import render_template, session, url_for
from finances import db, app
from finances.models.transaction import Transaction, monthly
from finances.models.category import Category, allChildren, categoriesSelectBox
from finances.forms import TransactionsForm, BudgetForm
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


@app.route('/tritransactions/<category_id>/<month>', methods=['GET', 'POST']) 
def tritransactions(category_id, month): 
    yyyy, mm = map(int, month.split('-'))
    date = datetime.date(yyyy, mm, 1) - monthdelta(1)

    cat_ids = [category_id] + \
        [c.id for c in allChildren(db.session.query(Category).filter(Category.id==category_id).first())]

    tables = []
    for _ in range(3):
        tables.append( db.session.query(Transaction).join(Category)\
                .filter(Category.id.in_(cat_ids),
                    Transaction.tdate>=date, 
                    Transaction.tdate<date + monthdelta(1),
                ).order_by(Transaction.tdate).all()
        )

        date += monthdelta(1)

    return render_template('transactions.html', form=None, transactions=tables)

@app.route('/transactions', methods=['GET', 'POST']) 
#@app.route('/transactions/<category_id>', methods=['GET', 'POST']) 
def transactions(): #category_id=None): 
    form = TransactionsForm()
    form.category.choices = categoriesSelectBox()

    if form.validate_on_submit():
        print form.startdate.data
        print form.enddate.data

    q = db.session.query(Transaction)
    if form.category.data:
        c = db.session.query(Category).filter(Category.id==form.category.data).first()
        q = q.join(Category).filter(Category.id.in_(allChildren(c)))

    fr = form.startdate.data
    to = form.enddate.data
    q = q.filter(Transaction.tdate>=fr, Transaction.tdate<=to).order_by(Transaction.tdate)

    return render_template('transactions.html', form=form, transactions=[q])

@app.route('/budget', methods=['GET', 'POST']) 
def budget(): #category_id=None): 
    form = BudgetForm()

    table = monthly(form.startdate.data, form.enddate.data)

    return render_template('budget.html', form=form, table=table)
