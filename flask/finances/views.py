from flask import render_template, session, request, redirect, url_for

from finances import db, app
from finances.models.transaction import Transaction, monthly
from finances.models.trans_file import TransFile
from finances.models.category import Category, allChildren, categoriesSelectBox

from finances.models.budget import Budget

from finances.forms import TransactionForm, TransactionsForm, DateRangeForm, SplitTransactionForm

from finances.models import investments 

import datetime
import collections
from monthdelta import MonthDelta
from urllib import unquote
from sqlalchemy import desc

@app.template_filter('money')
def money_filter(s):
    return "${:,.2f}".format(s)

@app.template_filter('comma')
def comma_filter(s):
    return "{:,.2f}".format(s)



@app.route('/categories')
def categories():
    q = db.session.query(Category)
    return render_template('categories.html', categories=q)


@app.route('/tritransactions/<category_id>/<month>', methods=['GET', 'POST']) 
def tritransactions(category_id, month): 
    yyyy, mm = map(int, month.split('-'))
    date = datetime.date(yyyy, mm, 1) - MonthDelta(1)

    cat_ids = [category_id] + \
        [c.id for c in allChildren(db.session.query(Category).filter(Category.id==category_id).first())]

    tables = []
    for _ in range(3):
        tables.append( db.session.query(Transaction).join(Category)\
                .filter(Category.id.in_(cat_ids),
                    Transaction.bdate>=date, 
                    Transaction.bdate<date + MonthDelta(1),
                ).order_by(Transaction.bdate).all()
        )

        date += MonthDelta(1)

    return render_template('transactions.html', form=None, transactions=tables)

@app.route('/transactions', methods=['GET', 'POST']) 
@app.route('/transactions/<int:category_id>', methods=['GET', 'POST']) 
@app.route('/transactions/<int:category_id>/<name>', methods=['GET', 'POST']) 
def transactions(category_id=None, name=None): 
    form = TransactionsForm()
    form.category.choices = categoriesSelectBox()

    if form.validate_on_submit():
        category_id = form.category.data
        session['startdate'] = str(form.startdate.data)
        session['enddate'] = str(form.enddate.data)
    elif category_id:
        form.category.data = category_id

    if 'startdate' in session:
        form.startdate.data = datetime.date(*map(int, session['startdate'].split('-')))
    if 'enddate' in session:
        form.enddate.data = datetime.date(*map(int, session['enddate'].split('-')))

    q = db.session.query(Transaction)
    if form.category.data:
        c = db.session.query(Category).filter(Category.id==form.category.data).first()
        children = [c] + allChildren(c)
        q = q.join(Category).filter(Category.id.in_([child.id for child in children]))

    if name:
        name = unquote(name)
        q = q.filter(Transaction.name==name)

    q = q.filter(
        Transaction.bdate>=form.startdate.data, 
        Transaction.bdate<=form.enddate.data,
    ).order_by(desc(Transaction.bdate))

    graph = collections.defaultdict(float)
    for tran in q:
        if not tran.yearly:
            graph[tran.bdate.replace(day=1)] += tran.amount

    return render_template(
        'transactions.html', 
        form=form, 
        transactions=[q], 
        title='Transactions',
        graph=collections.OrderedDict([(k, abs(v)) for k, v in sorted(graph.items())]),
    )

@app.route('/transaction/<int:transaction_id>', methods=['GET', 'POST']) 
def transaction(transaction_id): 
    form = TransactionForm()
    form.category.choices = categoriesSelectBox()

    q = db.session.query(Transaction).filter(Transaction.id==transaction_id).first()
    if form.validate_on_submit():
        q.bdate = form.bdate.data
        q.name = form.name.data
        q.category_id = form.category.data
        q.amount = form.amount.data
        q.yearly = form.yearly.data

        db.session.commit()

        return redirect(url_for('transactions', category_id=q.category_id))

    else:
        form.tdate.data = q.tdate
        form.bdate.data = q.bdate
        form.name.data  = q.name
        form.category.data = q.category_id
        form.amount.data = q.amount
        form.yearly.data = q.yearly

    return render_template('transaction.html', form=form, transaction_id=transaction_id, title='Transaction')


@app.route('/split_transaction/<int:transaction_id>', methods=['GET', 'POST']) 
def split_transaction(transaction_id): 
    q = db.session.query(Transaction).filter(Transaction.id==transaction_id).first()

    form = SplitTransactionForm()
    form.category_1.choices = categoriesSelectBox()
    form.category_2.choices = categoriesSelectBox()

    if form.validate_on_submit():
        q.bdate = form.bdate_1.data
        q.name = form.name_1.data
        q.category_id = form.category_1.data
        q.amount = form.amount_1.data
        q.yearly = form.yearly_1.data

        db.session.add(
            Transaction(q.tdate, form.name_2.data, form.category_2.data, form.amount_2.data,
                q.trans_file, form.bdate_2.data, form.yearly_2.data
            )
        )

        db.session.commit()

        return redirect(url_for('transactions', category_id=q.category_id))

    else:
        form.bdate_1.data = q.bdate
        form.name_1.data  = q.name
        form.category_1.data = q.category_id
        form.amount_1.data = q.amount
        form.yearly_1.data = q.yearly

        form.bdate_2.data = q.bdate

    return render_template('split_transaction.html', form=form, title='Split Transaction')

@app.route('/fundprices/<fund>', methods=['GET', 'POST']) 
def fundprices(fund): 
    form = DateRangeForm()
    table = investments.fundprices(fund, form.startdate.data, form.enddate.data)

    return render_template('fundprices.html', form=form, prices=table)

@app.route('/year_returns/<fund>')
def year_returns(fund):
    prices = investments.fundprices(fund, datetime.date(2005, 1, 1), datetime.date(2015, 12, 31))
    years = sorted(list(set([x['date'].year for x in prices])))

    t1 = collections.defaultdict(list)
    for p in prices[::-1]:
        t1[p['date'].year].append(p['price'])

    for k, v in t1.items():
        t1[k] = [(x-v[0])/v[0] for x in v[1:]]

    n = 1
    results = []
    while t1:
        row = [n]
        for year in years:
            if t1.get(year):
                row += [t1[year][0]]
                t1[year] = t1[year][1:]
            else:
                row += [None]
                t1.pop(year, None)

        results.append(row)
        n += 1

    return render_template('year_returns.html', prices=results, keys=years)

@app.route('/budget', methods=['GET', 'POST']) 
def _budget(): #category_id=None): 
    form = DateRangeForm()

    if form.validate_on_submit():
        session['startdate'] = str(form.startdate.data)
        session['enddate'] = str(form.enddate.data)

    if 'startdate' in session:
        form.startdate.data = datetime.date(*map(int, session['startdate'].split('-')))
    if 'enddate' in session:
        form.enddate.data = datetime.date(*map(int, session['enddate'].split('-')))
 
    table = monthly(form.startdate.data, form.enddate.data)

    return render_template('budget.html', form=form, table=table, title='Budget')

@app.route('/portfolio', methods=['GET', 'POST']) 
def portfolio():
    form = DateRangeForm()
    table = investments.portfolio(form.startdate.data, form.enddate.data)

    return render_template('portfolio.html', form=form, table=table, title='Portfolio')

@app.route('/history/<fund>')
def history(fund):
    trans = db.session.query(investments.InvTransaction).\
        filter(investments.InvTransaction.fund==fund,
            investments.InvTransaction.account=='401k',
        ).\
        order_by(investments.InvTransaction.date)

    total = 0.0
    table = []
    for row in trans:
        total += row.shares
        table.append([row.date, row.action, row.shares, total])

    return render_template('history.html', table=table[::-1])
 
@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/hist_budget')
def hist_budget():

    keys, table, graph = foo.budget()

    return render_template('hist_budget.html', keys=keys, table=table, graph=graph)

@app.route('/')
def _foo():
    b = Budget('blah', 2015)
    return render_template('foo.html', tables=[
        b.income_t(), b.pretax_t(), b.taxes_t(), b.giving_t(), b.deductions_t()
    ])
