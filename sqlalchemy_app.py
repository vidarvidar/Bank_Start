# för att testa om sqlalchemy funkar med databasen
import csv

from sqlalchemy import insert
from sqlalchemy.orm import Session
from models import Base, Customer, Account, Transaction
from db_sqlalchemy import init_db, engine

def main(): #funker inte just nu
    init_db()
    db = Session(engine)

    try:
        with open('data/sebank_customers_with_accounts.csv') as f:
            reader = csv.DictReader(f)
            for row in reader:
                db.execute(insert(Customer).values(**row))
        db.commit()
        print('Import Successful!')
    except Exception as e:
        print(e)
        db.rollback()

    db.close()

if __name__ == '__main__':
    main()
