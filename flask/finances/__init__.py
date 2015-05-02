from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import basedir

import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from finances.models import transaction, category, trans_file, mort_schedule
from finances import views
