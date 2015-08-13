from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired
import datetime
from monthdelta import monthdelta

from finances.models.category import Category, categoriesSelectBox
from finances import db

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class TransactionsForm(Form):
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime.date.today() - monthdelta(2))
    enddate   = DateField('enddate', format='%Y-%m-%d', default=datetime.date.today())
    category  = SelectField('category', coerce=int)

class DateRangeForm(Form):
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime.date.today() - monthdelta(12))
    enddate   = DateField('enddate', format='%Y-%m-%d', default=datetime.date.today())
