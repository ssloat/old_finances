from flask import render_template, session, url_for
from finances import db, app
from finances.models.transaction import Transaction, monthly
from finances.models.category import Category, allChildren, categoriesSelectBox
from finances.forms import TransactionForm, TransactionsForm, DateRangeForm

from finances.models import investments 

import datetime
from monthdelta import monthdelta

@app.template_filter('money')
def money_filter(s):
    return "${:,.2f}".format(s)




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

@app.route('/transaction/<transaction_id>', methods=['GET', 'POST']) 
def transaction(transaction_id): 
    form = TransactionForm()
    form.category.choices = categoriesSelectBox()

    if form.validate_on_submit():
        print form.startdate.data
        print form.enddate.data

    q = db.session.query(Transaction).filter(Transaction.id==4).first()

    form.tdate.data = q.tdate
    form.bdate.data = q.bdate
    form.name.data  = q.name
    form.category.data = q.category_id
    form.amount.data   = q.amount

    return render_template('transaction.html', form=form)

@app.route('/fundprices/<fund>', methods=['GET', 'POST']) 
def fundprices(fund): 
    form = DateRangeForm()
    table = investments.fundprices(fund, form.startdate.data, form.enddate.data)

    return render_template('fundprices.html', form=form, prices=table)

@app.route('/budget', methods=['GET', 'POST']) 
def budget(): #category_id=None): 
    form = DateRangeForm()

    table = monthly(form.startdate.data, form.enddate.data)

    return render_template('budget.html', form=form, table=table)

@app.route('/portfolio', methods=['GET', 'POST']) 
def portfolio():
    form = DateRangeForm()
    table = investments.portfolio(form.startdate.data, form.enddate.data)

    return render_template('portfolio.html', form=form, table=table)


@app.route('/example')
def example():
    return render_template('example.html')
