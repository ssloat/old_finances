from finances import db
from finances.models.category import CategoryRE, create_category_res

if __name__ == '__main__':
    for re in db.session.query(CategoryRE):
        db.session.delete(re)

    create_category_res()

    db.session.commit()

