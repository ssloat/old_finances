from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired
import datetime
from monthdelta import MonthDelta

from finances.models.category import Category, categoriesSelectBox
from finances import db

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class TransactionsForm(Form):
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime.date.today() - MonthDelta(2))
    enddate   = DateField('enddate', format='%Y-%m-%d', default=datetime.date.today())
    category  = SelectField('category', coerce=int)

class TransactionForm(Form):
    tdate    = DateField('tdate', format='%Y-%m-%d')
    bdate    = DateField('bdate', format='%Y-%m-%d')
    name     = StringField('name')
    amount   = DecimalField('amount')
    category = SelectField('category', coerce=int)
    yearly   = BooleanField('yearly')

class SplitTransactionForm(Form):
    bdate_1    = DateField('bdate_1', format='%Y-%m-%d')
    name_1     = StringField('name_1')
    amount_1   = DecimalField('amount_1')
    category_1 = SelectField('category_1', coerce=int)
    yearly_1   = BooleanField('yearly_1')

    bdate_2    = DateField('bdate_2', format='%Y-%m-%d')
    name_2     = StringField('name_2')
    amount_2   = DecimalField('amount_2')
    category_2 = SelectField('category_2', coerce=int)
    yearly_2   = BooleanField('yearly_2')

class DateRangeForm(Form):
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime.date.today() - MonthDelta(12))
    enddate   = DateField('enddate', format='%Y-%m-%d', default=datetime.date.today())
