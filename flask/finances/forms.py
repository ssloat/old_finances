from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired
import datetime
from monthdelta import monthdelta

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class TransactionsForm(Form):
    startdate = DateField('startdate', format='%Y-%m-%d', default=datetime.date.today() - monthdelta(2))
    enddate = DateField('enddate', format='%Y-%m-%d', default=datetime.date.today())
