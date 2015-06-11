import os
import unittest
from datetime import date

from config import basedir
from finances import app, db
from finances.models.transaction import Transaction, monthly
from finances.models.trans_file import TransFile
from finances.models.category import Category, create_categories, allChildren

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.create_all()

        top = Category('top', None, 0)
        a = Category('a', top)
        b = Category('b', top)
        a1 = Category('a1', a)
        a2 = Category('a2', a)
        a3 = Category('a3', a)
        b1 = Category('b1', b)
        a1i = Category('a1i', a1)
        a1ii = Category('a1ii', a1)
        tf = TransFile('Test File', 'Checking')
        db.session.add_all( [top, a, b, a1, a2, a3, b1, a1i, a1ii, tf] )

        db.session.add( Transaction(date(2015, 5, 15), 't1', a, 1.0, tf) )
        db.session.add( Transaction(date(2015, 5, 15), 't2', a1, 1.0, tf) )
        db.session.add( Transaction(date(2015, 5, 15), 't3', a1, 1.0, tf) )
        db.session.add( Transaction(date(2015, 5, 15), 't4', a1ii, 1.0, tf) )
        db.session.add( Transaction(date(2015, 5, 15), 't5', a3, 3.0, tf) )
        db.session.add( Transaction(date(2015, 5, 15), 't6', b1, 1.0, tf) )

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_one(self):
        top = db.session.query(Category).filter(Category.name=='top').first()
        assert top.name == 'top'

        a = db.session.query(Category).filter(Category.name=='a').first()
        assert a.parent.name == 'top'
        assert a.depth == 1

        assert set([
               db.session.query(Category).filter(Category.id==c.id).first().name 
               for c in allChildren(a)]
            ), \
            set(['a1', 'a1i', 'a1ii', 'a2'])

        '''
        top (8.0)
            A [1.0] (7.0)
                a1 [1.0, 1.0] (3.0)
                    a1i
                    a1ii [1.0]
                a2
                a3 [3.0]
            B [] (1.0)
                b1 [1.0]
        '''
        exp = [
            ['category', '2015-05', 'Average'],
            ['top', 8.0, 8.0],
            ['a', 7.0, 7.0],
            ['a1', 3.0, 3.0],
            ['a1i', 0.0, 0.0],
            ['a1ii', 1.0, 1.0],
            ['a2', 0.0, 0.0],
            ['a3', 3.0, 3.0],
            ['b', 1.0, 1.0],
            ['b1', 1.0, 1.0],
        ]
        self.assertEqual(exp, monthly(date(2015, 5, 1), date(2015, 5, 25)))

if __name__ == '__main__':
    unittest.main()

