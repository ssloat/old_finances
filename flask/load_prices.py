import datetime
import sys

from finances import db
from finances.models.stock import load_prices

if __name__ == '__main__':
    start = datetime.date(*map(int, sys.argv[1].split('-')))
    end = datetime.date(*map(int, sys.argv[2].split('-'))) if len(sys.argv) > 2 else datetime.date.today()

    load_prices(start, end)

    db.session.commit()
