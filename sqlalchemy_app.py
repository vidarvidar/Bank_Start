# för att testa om sqlalchemy funkar med databasen

import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Base, Customer, Account, Transaction
from db_sqlalchemy import init_db, engine

def main():
    init_db()
    db = Session(engine)
    db.query(Customer).delete()
    db.commit()
    column_mapper = {'Customer': 'name', 'Address': 'address', 'Phone': 'phone', 'Personnummer': 'ssn'}

    df = pd.read_csv('data/sebank_customers_with_accounts.csv')
    df2 = df[['Customer', 'Address', 'Phone', 'Personnummer']].rename(columns=column_mapper).drop_duplicates()

    try:
        with db.begin():
            for row in df2.to_dict('records'):
                customer = Customer(name=row['name'], ssn=row['ssn'], address=row['address'], phone=row['phone'])
                db.add(customer)
            db.commit()
            print('Import Successful!')
    except SQLAlchemyError as e:
        print("Unsuccesful import", e)
        db.rollback()



    db.close()

if __name__ == '__main__':
    main()
