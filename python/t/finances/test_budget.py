from nose.tools import assert_equals

from finances.budget import Budget, BudgetEntry
from finances.category import Category

def test_budget():
    b = Budget('2015', 2015, 'Single')

    c = Category('Income', None)

    be = BudgetEntry('Bofa', b, c, 8000, 4000)
    be = BudgetEntry('Rent', b, c, 500)

    assert_equals(reduce(lambda x, y: x+y.amount(), b.entries, 0.0), 106000)
