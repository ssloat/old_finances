import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'finance.db')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
